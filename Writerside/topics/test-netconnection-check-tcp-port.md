# Test-NetConnection 測試 TCP Port

<web-summary>用 PowerShell 的 Test-NetConnection 測試 FTP、SQL Server 或 HTTPS 的 TCP port 通不通，並說明如何判讀 TcpTestSucceeded。</web-summary>

> 首次發表：2024-05-15

Windows 內建的 `Test-NetConnection` 可以直接測目標主機的 TCP port，不用另外裝 telnet。結果看 `TcpTestSucceeded`，`True` 表示 port 連得上。

## 指令

```powershell
Test-NetConnection <host-or-ip> -Port 1433
```

| 服務 | 預設 port |
| --- | --- |
| FTP | 21 |
| HTTPS | 443 |
| SQL Server | 1433 |

只想拿到 `True` 或 `False`，例如要寫進腳本判斷時：

```powershell
Test-NetConnection <host-or-ip> -Port 1433 -InformationLevel Quiet
```

## 判讀

- `TcpTestSucceeded : True` 只代表 TCP 連線成功，不代表帳號密碼或服務本身正常。
- `PingSucceeded : False` 但 TCP 成功很常見，通常是 ICMP 被防火牆擋掉，以 TCP 結果為準。
- 這個指令只能測 TCP，不能測 UDP。
