# Win 11 Docker WSL MySQL Ubuntu

> 首次發表：2023-05-23

---

筆記下從無到有 起一個 MySQL 服務

![筆記下從無到有 起一個 MySQL 服務](dotblogs-3a02b151-1705909149.jpg)

Enable Virtual Machine Platform Feature and reboot

[how to fix WslRegisterDistribution failed with error: 0x8004032d ubuntu - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1424692/how-to-fix-wslregisterdistribution-failed-with-err)

安裝 WSL

[Windows Subsystem for Linux - Microsoft Store Apps](https://apps.microsoft.com/store/detail/windows-subsystem-for-linux/9P9TQF7MRM4R?hl=en-us&gl=us)

安裝 Ubuntu

[Ubuntu - Microsoft Store Apps](https://apps.microsoft.com/store/detail/ubuntu/9PDXGNCFSCZV?hl=en-us&gl=us)

初始化 Ubuntu

- 設定帳號密碼

安裝 Docker

[Install Docker Desktop on Windows | Docker Documentation](https://docs.docker.com/desktop/install/windows-install/)

安裝 MySQL

[mysql - Official Image | Docker Hub](https://hub.docker.com/_/mysql)

```
docker run --name some-mysql
 -p 3306:3306
 -d mysql:8.0.33
 -e MYSQL_ROOT_PASSWORD=my-secret-pw
 -e MYSQL_ROOT_HOST='%'
 -e MYSQL_USER=jakeuj
 -e MYSQL_PASSWORD=my-secret-pw
 -v /d/docker/mysql/data:/var/lib/mysql/
 -v /d/docker/mysql/conf/my.cnf:/etc/mysql/my.cnf
 --character-set-server=utf8mb4
 --collation-server=utf8mb4_general_ci
```

登入 MySQL

```
docker exec -it some-mysql mysql -u root -p
```

查詢 MySQL

```
> SELECT user,host FROM mysql.user;
```

GUI

![GUI](dotblogs-3a02b151-1684831054.jpg)

DataGrip

參照

[Windows10子系统中使用docker安装MySQL - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/374605968)

[DBeaver 连接 docker下mysql，并附带安装教程\_小朋友yo的博客-CSDN博客](https://blog.csdn.net/Eternalyii/article/details/126715960)
