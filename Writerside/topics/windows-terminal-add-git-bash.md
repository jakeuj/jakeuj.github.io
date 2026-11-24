# Windows Terminal 加入 Git Bash

<web-summary>在 Windows Terminal 新增 Git Bash 設定檔，命令列指向 Git 的 bin\bash.exe；Git Bash 沒有 dig 時改用 WSL 或 Resolve-DnsName。</web-summary>

> 首次發表：2024-02-19

在 Windows Terminal 的設定新增一個設定檔，命令列填 `C:\Program Files\Git\bin\bash.exe`，就能直接開 Git Bash。

## 設定

| 欄位 | 值 |
| --- | --- |
| 名稱 | Git Bash |
| 命令列 | `C:\Program Files\Git\bin\bash.exe` |
| 啟動時載入的目錄 | 使用者資料夾（環境變數 `USERPROFILE`） |

## Git Bash 沒有 dig

我原本是想用 `dig` 查 DNS，但 Git Bash 沒有這個指令：

```text
bash: dig: command not found
```

最後還是用 WSL：

```bash
dig example.com +noall +answer -t A
```

不想開 WSL 的話，PowerShell 內建的 `Resolve-DnsName` 也能查：

```powershell
Resolve-DnsName example.com -Type A
```

## 參照

[如何给 Windows Terminal 增加一个新的终端（以 Bash 为例） - walterlv](https://blog.walterlv.com/post/add-a-new-profile-for-windows-terminal.html)

[How to Install Dig on Windows (phoenixnap.com)](https://phoenixnap.com/kb/dig-windows)
