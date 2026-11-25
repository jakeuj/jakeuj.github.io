# SQL Server 服務無法啟動 Error 1069：帳號密碼與 LocalDB 的判斷

<web-summary>Error 1069 是 Windows 服務無法用設定的帳號登入。依服務帳號判斷密碼要留空或更新，用事件 7038、7041 找原因；LocalDB 不是 Windows 服務，改用 sqllocaldb 排查。</web-summary>

> 首次發表：2022-03-14
>
> **更新日期：** 2026-11-25

Error 1069（The service did not start due to a logon failure）代表 Windows 服務無法用設定好的帳號登入。先看服務用哪一種帳號：

- **`NT SERVICE\...` 虛擬帳號**：密碼要留空。把兩個密碼欄都清空，再啟動服務。
- **本機或網域帳號**：要填目前有效的密碼，改過密碼就得跟著更新。
- **LocalDB**：它不是 Windows 服務，不會出現 1069，請看[LocalDB 連不上](#localdb)。

我在 2022 年遇到時，是到服務的登入頁把密碼清空，按確定後就能啟動。

> 這篇原本的標題寫「Local Db 服務」。微軟文件說明 LocalDB 不使用服務，所以出現 1069 的會是一般的 SQL Server 服務，或其他軟體自己建立的服務。
{style="note"}

## 確認服務帳號 {#service-account}

列出名稱含 SQL 的服務，以及各自的登入帳號：

```powershell
Get-CimInstance Win32_Service |
    Where-Object Name -Like '*SQL*' |
    Select-Object Name, StartName, State
```

`StartName` 就是登入帳號，對照下表決定密碼欄怎麼填：

| 帳號類型 | `StartName` 的樣子 | 密碼欄 |
| --- | --- | --- |
| 虛擬帳號 | `NT SERVICE\MSSQLSERVER`、`NT SERVICE\MSSQL$SQLEXPRESS` | 留空 |
| 群組受管理服務帳號（gMSA） | `<domain>\<name>$` | 留空 |
| 內建帳號 | `LocalSystem`、`NT AUTHORITY\NETWORK SERVICE` | 不需要密碼 |
| 本機使用者 | `.\<user>` | 目前的密碼 |
| 網域使用者 | `<domain>\<user>` | 目前的密碼 |

SQL Server 安裝程式預設使用虛擬帳號，名稱就是 `NT SERVICE\` 加上服務名稱。

## 從事件檢視器找原因 {#event-log}

1069 只告訴你登入失敗，原因記在系統記錄的事件 7038 或 7041：

```powershell
Get-WinEvent -MaxEvents 5 -FilterHashtable @{
    LogName      = 'System'
    ProviderName = 'Service Control Manager'
    Id           = 7038, 7041
} | Format-List TimeCreated, Id, Message
```

| 事件 | 原因 | 英文訊息關鍵字 | 處理方式 |
| --- | --- | --- | --- |
| 7041 | 沒有以服務方式登入的權限 | `not been granted the requested logon type` | [補上權限](#fix-logon-right) |
| 7038 | 帳號或密碼錯誤 | `user name or password is incorrect` | 核對[帳號密碼](#fix-password)；gMSA 看[受管理帳號旗標](#fix-gmsa) |
| 7038 | 帳號被停用 | `account is currently disabled` | 啟用該帳號 |
| 7038 | 帳號必須先變更密碼 | `password must be changed` | 取消「使用者必須在下次登入時變更密碼」，或改好密碼後更新服務設定 |
| 7038 | 帳號被鎖定 | `account is currently locked out` | 解除鎖定，再核對服務裡的密碼，避免又被鎖 |
| 7038 | 連不到網域 | `could not be contacted` | [開機時連不到網域](#fix-domain) |

中文版 Windows 的訊息會是中文，用事件編號和原因對照即可。

停用、鎖定和變更密碼這三項，本機帳號在 `compmgmt.msc` 處理，網域帳號要到「Active Directory 使用者和電腦」。

## 修正登入設定 {#fix}

### 用 SQL Server 組態管理員 {#fix-configuration-manager}

SQL Server 和 SQL Server Agent 的帳號或密碼，微軟建議一律用這個工具改。`services.msc` 只改帳號，不會一併調整登錄檔權限等相關設定，服務可能因此啟動不了。

1. 在開始功能表輸入 `SQLServerManager17.msc`。17 是 SQL Server 2025，2022 用 16，2019 用 15。
2. 選「SQL Server 服務」，在執行個體上按右鍵開啟「內容」，切到「登入」頁。
3. 虛擬帳號：帳號填 `NT SERVICE\MSSQL$<執行個體名稱>`，預設執行個體填 `NT SERVICE\MSSQLSERVER`，兩個密碼欄都留空。
4. 本機或網域帳號：重新輸入目前的密碼。
5. 按確定，再啟動服務。

### 用服務管理員 {#fix-services}

服務不是 SQL Server 本身，例如其他軟體自己建立的服務，才用 `services.msc`：

1. 在服務上按右鍵開啟「內容」，切到「登入」頁。
2. 依前面的表格清空密碼，或輸入目前的密碼。
3. 按確定，再啟動服務。

### 核對本機或網域帳號的密碼 {#fix-password}

用 `runas` 試登入，能開出命令提示字元就代表帳號密碼正確：

```console
runas /user:<電腦或網域>\<帳號> cmd
```

- 成功：回到組態管理員，把同一組帳號密碼重新輸入一次。
- 失敗：先重設該帳號的密碼，再更新服務設定。

### 補上以服務方式登入的權限 {#fix-logon-right}

1. 執行 `secpol.msc`，展開「本機原則」、「使用者權限指派」。
2. 確認服務帳號在「以服務方式登入」清單裡。
3. 確認它不在「拒絕以服務方式登入」清單裡。

設好之後又消失，通常是群組原則蓋掉了，要找網域管理員調整 GPO。

### gMSA 的受管理帳號旗標 {#fix-gmsa}

在命令提示字元查詢，結果應該是 true：

```console
sc qmanagedaccount MSSQL$SQLEXPRESS
```

是 false 就改成 true，再啟動服務：

```console
sc managedaccount MSSQL$SQLEXPRESS TRUE
```

### 開機時連不到網域 {#fix-domain}

手動啟動正常、只有重開機後失敗，多半是服務比網路或 Netlogon 早啟動。依序嘗試：

1. 把啟動類型改成「自動（延遲啟動）」。SQL Server 2022 起，安裝程式預設就是這樣。
2. 在服務的「復原」頁把失敗動作設成重新啟動服務。容錯移轉叢集和可用性群組不建議這樣做。
3. 仍不行，才讓服務相依於 Netlogon：

```console
sc config MSSQL$SQLEXPRESS depend=keyiso/netlogon
```

## 在 PowerShell 操作要注意的兩件事 {#powershell}

**具名執行個體的 `$` 會被當成變數。** 在 PowerShell 7.6.6 實測，服務名稱只有用單引號才完整：

| 寫法 | 實際傳入的名稱 |
| --- | --- |
| `MSSQL$SQLEXPRESS` | `MSSQL` |
| `"MSSQL$SQLEXPRESS"` | `MSSQL` |
| `'MSSQL$SQLEXPRESS'` | `MSSQL$SQLEXPRESS` |

**Windows PowerShell 5.1 的 `sc` 是 `Set-Content` 的別名。** 在裡面打 `sc qc MSSQLSERVER` 不會查服務，而是在目前資料夾建立一個叫 `qc` 的檔案。要寫成 `sc.exe`，或改用命令提示字元：

```powershell
sc.exe qc 'MSSQL$SQLEXPRESS'
```

## 驗證 {#verify}

```powershell
Start-Service -Name 'MSSQL$SQLEXPRESS'
Get-Service -Name 'MSSQL$SQLEXPRESS'
```

狀態是 `Running` 之後，再重跑一次[事件查詢](#event-log)，確認沒有新的 7038 或 7041。可以的話重開機一次，排除只在開機時發生的情況。

## LocalDB 連不上 {#localdb}

LocalDB 由使用者的程式按需啟動，以該使用者的身分執行，`services.msc` 裡找不到它。先確認執行個體的狀態：

```console
sqllocaldb info
sqllocaldb info MSSQLLocalDB
sqllocaldb start MSSQLLocalDB
```

啟動失敗就看錯誤記錄：

```powershell
Get-Content -Tail 50 "$env:LOCALAPPDATA\Microsoft\Microsoft SQL Server Local DB\Instances\MSSQLLocalDB\error.log"
```

| 狀況 | 處理方式 |
| --- | --- |
| 找不到 `sqllocaldb` 指令 | 沒有安裝或不在 `PATH`。從 SQL Server Express 或 Visual Studio Installer 安裝 LocalDB |
| 第一次連線逾時 | 正在建立自動執行個體，等幾秒再連 |
| 換一個 Windows 帳號就連不到 | 執行個體只屬於建立它的使用者，用同一個帳號執行，或由管理員設定共用 |
| 由 `SYSTEM` 等內建帳號使用 | 官方不建議，改用一般 Windows 帳號。網站或背景服務可以改裝 SQL Server Express |
| 記錄提到 sector size 或 misaligned log IOs | [磁碟磁區超過 4 KB](#localdb-sector-size) |

### 磁碟磁區超過 4 KB {#localdb-sector-size}

Windows 11 搭配部分 NVMe 硬碟會回報大於 4 KB 的磁區，SQL Server 各版本（含 LocalDB）都不支援。先檢查：

```console
fsutil fsinfo sectorinfo C:
```

看 `PhysicalBytesPerSectorForAtomicity` 和 `PhysicalBytesPerSectorForPerformance`，取較大的值。超過 4096 才需要處理，做法是依[官方文件](https://learn.microsoft.com/troubleshoot/sql/database-engine/database-file-operations/troubleshoot-os-4kb-disk-sector-size)新增 `ForcedPhysicalSectorSizeInBytes` 登錄值並重新開機。修改前先備份登錄檔。

### 重建執行個體 {#localdb-recreate}

其他方法都無效才重建：

```console
sqllocaldb stop MSSQLLocalDB
sqllocaldb delete MSSQLLocalDB
sqllocaldb create MSSQLLocalDB
sqllocaldb start MSSQLLocalDB
```

> 官方文件提醒，刪除執行個體會移除與它關聯的所有資料庫。執行前先備份需要的資料。
{style="warning"}

## 這次更新怎麼查證 {#how-verified}

事件對照、帳號規則和 LocalDB 的步驟整理自下列微軟文件，這次沒有在 Windows 上重現 1069。實際執行過的只有 PowerShell 的 `$` 展開，以及 `sc` 設成 `Set-Content` 別名時會建立檔案。

## 參考資料 {#references}

- [Error 1069 occurs when you start SQL Server Service](https://learn.microsoft.com/troubleshoot/sql/database-engine/startup-shutdown/error-1069-service-cannot-start)
- [設定 Windows 服務帳戶與權限](https://learn.microsoft.com/sql/database-engine/configure-windows/configure-windows-service-accounts-and-permissions)
- [變更服務啟動帳戶](https://learn.microsoft.com/sql/database-engine/configure-windows/scm-services-change-the-service-startup-account)
- [SQL Server Express LocalDB](https://learn.microsoft.com/sql/database-engine/configure-windows/sql-server-express-localdb)
- [LocalDB 執行個體 API：LocalDB 不使用服務](https://learn.microsoft.com/sql/relational-databases/express-localdb-instance-apis/sql-server-express-localdb-reference-instance-apis)
- [Set-Content 的別名（Windows PowerShell 5.1）](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/set-content?view=powershell-5.1)
- [JetBrains Rider 連接 LocalDB](JetBrains-Rider-connect-to-LocalDB.md)
