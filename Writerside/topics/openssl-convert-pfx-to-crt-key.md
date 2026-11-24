# OpenSSL 把 PFX 轉成 CRT 與 KEY

<web-summary>在 Windows 用 Git 內附的 OpenSSL 把 PFX 憑證轉出 server.crt 與 server.key，供 Apache 更新 SSL 憑證使用。</web-summary>

> 首次發表：2024-03-26

更新 Apache 的 SSL 憑證時，收到的是 PFX，要轉成憑證檔和私密金鑰檔。Git for Windows 內附 OpenSSL，不用另外安裝。

## 步驟

先把 Git 的工具路徑加進這個 CMD 視窗的環境變數：

```bat
set PATH=%PATH%;C:\Program Files\Git\usr\bin
```

轉出伺服器憑證：

```bat
openssl pkcs12 -in server.pfx -nokeys -password "pass:<pfx-password>" -out - 2>nul | openssl x509 -out server.crt
```

轉出私密金鑰：

```bat
openssl pkcs12 -in server.pfx -nocerts -password "pass:<pfx-password>" -nodes -out server.key
```

開啟目前資料夾，複製 `server.crt` 和 `server.key`，替換 Apache 設定中指定的憑證檔案：

```bat
explorer .
```

`-nodes` 產生的 `server.key` 沒有密碼保護，用完要限制存取權限，也不要放進版本控制。把密碼寫在命令列會留在命令紀錄，處理正式憑證時可以省略 `-password`，改為互動輸入。

## 參照

[常見的 PowerShell 輸出訊息的 2 種方法](powershell-output-redirection.md)

[如何在收到 PFX 或 CER 憑證檔之後使用 OpenSSL 進行常見的格式轉換 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2019/04/17/Convert-PFX-and-CER-format-using-OpenSSL)
