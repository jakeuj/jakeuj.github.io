# Windows Server 2016 於 IIS 10 安裝  Web Farm Framework 問題與解答

<web-summary>IIS 10 安裝 Web Farm Framework 2.2 出現 iis version 7.0 or greater is required 的原因與登錄檔解法。WFF 已經停止提供，新環境請改用 ARR。</web-summary>

> 首次發表：2016-01-14
>
> **更新日期：** 2026-11-25

在 Windows Server 2016（IIS 10）安裝 Web Farm Framework（WFF）2.2，會停在這個訊息：

```text
iis version 7.0 or greater is required to install Web Farm Framework 2.2
```

安裝程式把 IIS 10 判斷成低於 7 的版本。當年的解法是安裝時暫時把登錄檔裡的 IIS 主要版本改成 9，裝完再改回 10。

> 微軟已經停止 WFF，[官方頁面](https://www.iis.net/downloads/microsoft/web-farm-framework)也不再提供下載。新環境請改用 [Application Request Routing（ARR）](https://learn.microsoft.com/iis/overview/scalable-web-infrastructure)。下面的步驟只適合還得維護舊環境、手上有安裝檔的情況。
{style="warning"}

## 步驟 {#steps}

1. 匯出 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\InetStp` 當備份。
2. 用系統管理員身分開啟 `regedit`，到同一個機碼。
3. 把 `MajorVersion` 改成十進位的 9。
4. 安裝 WFF 2.2。
5. 把 `MajorVersion` 改回十進位的 10（十六進位是 `a`）。

安裝完一定要改回來，否則其他程式會讀到錯誤的 IIS 版本。

我在 2016 年 1 月用 Windows Server 2016 技術預覽版 4（中文版）時，安裝 URL Rewrite 2.0 也遇到同樣的情形。

## 為什麼會誤判 {#reason}

微軟工程師處理 IIS Media Services 4.1 的相同訊息時，推測安裝程式只看版本字串的第一個字元，所以 10 被當成 1。他用的也是修改 `MajorVersion` 的做法，並註明這只是繞過檢查，IIS Media Services 4.1 並不支援 Windows Server 2016。

## 參考資料 {#references}

- [Web Farm Framework 官方頁面：已停止提供](https://www.iis.net/downloads/microsoft/web-farm-framework)
- [Workaround: error installing IIS Media Services on Windows Server 2016](https://learn.microsoft.com/archive/blogs/pkirchner/workaround-error-installing-iis-media-services-on-windows-server-2016)
- [Scalable Web Infrastructure（ARR）](https://learn.microsoft.com/iis/overview/scalable-web-infrastructure)

2026-11-25 更新：原文直接貼了英文問答，這次改成自己的說明，步驟順序不變。當年的回覆沒有留下網址，改附微軟部落格的同類案例。這次沒有在 Windows 上重跑。
