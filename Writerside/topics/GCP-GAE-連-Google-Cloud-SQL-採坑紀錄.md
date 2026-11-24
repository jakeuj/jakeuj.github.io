# GCP GAE 連接 Cloud SQL

> 首次發表：2023-11-29

---

Google App Engine 連 Google Cloud SQL (MSSQL) 沒有驅動

## 前言

以為 GAE 連自家 GCS MSSQL 應該是小菜一碟

沒想到沒有 ODBC 驅動程式

總之先筆記一下改建 PostgreSQL

## 參照

[从 App Engine 标准环境连接到 Cloud SQL for PostgreSQL  |  Google Cloud](https://cloud.google.com/sql/docs/postgres/connect-instance-app-engine?hl=zh-cn)

專用 IP (私人)

Default

![Default](dotblogs-4a6928f1-1701238811.jpg)

分配

![分配](dotblogs-4a6928f1-1701238693.jpg)

SQL

![SQL](dotblogs-4a6928f1-1701239275.jpg)

最後可以用私有 IP 並指定 Port 來連線

[从 App Engine 标准环境连接到 Cloud SQL for PostgreSQL  |  Google Cloud](https://cloud.google.com/sql/docs/postgres/connect-instance-app-engine?hl=zh-cn#python_1)

## 備註

GAE 沒有 SQL Driver 會連不到 MSSQL (PostgerSQL 不確定)

最後改用 Docker 裝 Driver 再 Deploy 到 GAE 彈性環境來連到 GCS MSSQL Server
