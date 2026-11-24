# GCP Cloud SQL Proxy 本地連線不開白名單

> 首次發表：2023-12-08

---

筆記下浮動 IP 連 Google Cloud SQL 的代理連線方法

結論

1. 下載 [使用 Cloud SQL Auth 代理连接  |  Cloud SQL for PostgreSQL  |  Google Cloud](https://cloud.google.com/sql/docs/postgres/connect-auth-proxy?hl=zh-cn#install)
2. 驗證 gcloud auth application-default login
3. 執行 ./cloud-sql-proxy.x64.exe --address 0.0.0.0 --port 1234 myproject:myregion:myinstance
4. 連線 127.0.0.1,1234
5. P.S. 加 --address 0.0.0.0 可以用 localhost 連，省略則只能用 127.0.0.1 才連得到哦！

![P.S. 加 --address 0.0.0.0 可以用 localhost 連，省略則只能用 127.0.0.1 才連得到哦！](dotblogs-bb1646dd-1702017271.jpg)

參照

[GCP - Cloud SQL 的連線方式（cloud sql proxy） : Aaron Jen's Blog](https://aaronjen.github.io/2020-08-25-cloud_sql/)

[SQL Server 透過 TCP/IP 遠端連線時如何使用非 1433 埠號 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2009/03/29/How-to-connect-to-SQL-Server-using-non-default-1433-port)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CloudSQL
- GCP
- Proxy

- 回首頁

---

*本文章從點部落遷移至 Writerside*
