# Edge 刪除 localhost 的 HSTS

<web-summary>本機舊網站在 Edge 一直被強制轉成 HTTPS 時，到 edge://net-internals/#hsts 刪除 localhost 的 HSTS，網域不要填 port。</web-summary>

> 首次發表：2024-01-03

開發只有 HTTP 的舊網站時，Edge 可能因為之前記住了 `localhost` 的 HSTS 而強制轉成 HTTPS，導致網站打不開。刪掉那筆記錄就好：

1. 開啟 `edge://net-internals/#hsts`。
2. 找到 **Delete domain security policies**。
3. 網域填 `localhost`，按 **Delete**。

![刪除 localhost 的 HSTS](dotblogs-b2d2194f-1704261878.jpg)

## 注意

- 填 `localhost` 就好，**不要帶 port**。HSTS 是依主機名稱記錄的，所以同一台機器上任何一個 localhost 專案送過 HSTS，其他 port 的專案也會受影響。
- 之後再開到會送 HSTS 標頭的本機網站，記錄又會出現。開發環境不要啟用 `UseHsts`，可以避免一再發生。

## 延伸閱讀

[HSTS (HTTP Strict Transport Security) & HTTPS redirection (Enforce HTTPS in ASP.NET Core)](HSTS-And-HTTPS-Redirection-In-ASP-NET-Core.md)

## 參照

[解決 Edge chromium http 強制導向 https 問題](https://www.dotblogs.com.tw/ian/2019/12/19/edge_http_autoredirect_https)
