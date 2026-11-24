# Azure Container Squid Proxy

> 首次發表：2022-11-24

---

筆記下如何突破 IT 封鎖？

1. 建立 ACI

```
az group create --name myResourceGroup --location southeastasia
az container create --resource-group myResourceGroup --name mycontainer --image ubuntu/squid --dns-name-label aci-demo --ports 80
```

參照

[快速入門 - 將 Docker 容器部署至容器執行個體 - Azure CLI - Azure Container Instances | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/container-instances/container-instances-quickstart)

     2. 安裝工具

```
apt-get update
apt-get install vim -y
apt-get install apache2-utils -y
apt-get install curl -y
curl -x http://127.0.0.1:3128 -L http://google.com
```

![2. 安裝工具](dotblogs-33840f72-1669279373.jpg)

    3. 編輯設定擋 squid.conf

`vim /etc/squid/squid.conf`

    3.1 允許外部連線

搜尋 `http_access allow localnet`

取消註解 #http\_access allow localnet

![取消註解 #http\access allow localnet](dotblogs-33840f72-1669279676.jpg)

    3.2 更改 Port

搜尋 `http_port 3128`

改成 `http_port 80`

![改成 httpport 80](dotblogs-33840f72-1669279934.jpg)

參照

[How to Setup Squid Proxy Cache in Azure (Secure Your Network/Internet) (cloudinfrastructureservices.co.uk)](https://cloudinfrastructureservices.co.uk/how-to-setup-squid-proxy-cache-in-azure/)

    3.3 啟用 SFTP

搜尋 `acl SSL_ports port`

新增以下字段

```
acl SSL_ports port 22
acl Safe_ports port 22          # ssh/sftp
```

![新增以下字段](dotblogs-33840f72-1669281158.jpg)

參照

[通過 Squid 代理隧道傳輸 SSH/SFTP (seniorlinuxadmin.co.uk)](https://www.seniorlinuxadmin.co.uk/ssh-over-proxy.html)

    3.4 設定密碼 (Optional)

`apt-get install apache2-utils -y`

搜尋 `auth_param basic program`

加入

```
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED
http_access allow authenticated
```

設定帳號密碼 (Example: jakeuj)

```
htpasswd -c /etc/squid/passwords jakeuj
```

參照

[How to set up a squid Proxy with basic username and password authentication? - Stack Overflow](https://stackoverflow.com/questions/3297196/how-to-set-up-a-squid-proxy-with-basic-username-and-password-authentication)

    4. 重啟服務

`` kill -HUP `cat /run/squid.pid` ``

參照

[pid 文件有哪些作用？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/20289583)

    5. 本地測試 80 Port

```
apt-get install curl -y
curl -x http://127.0.0.1:80 -L http://google.com
```

參照

[設定 CURL 透過 Proxy 抓取資料 – Tsung's Blog (longwin.com.tw)](https://blog.longwin.com.tw/2014/04/curl-cli-use-proxy-2014/)

    6. 遠端測試

![6. 遠端測試](dotblogs-33840f72-1669280521.jpg)

驗證帳號密碼

![驗證帳號密碼](dotblogs-33840f72-1669285340.jpg)

確認 IP 是否從台灣換成新加坡 (資源群組 東南亞 資料中心 位於 SG)

![確認 IP 是否從台灣換成新加坡 (資源群組 東南亞 資料中心 位於 SG)](dotblogs-33840f72-1669280578.jpg)

## 測試 SFTP

![測試 SFTP](dotblogs-33840f72-1669281376.jpg)

沒意外了話可以成功取得檔案

### 規格

CPU cores 1

Memory 1.5 GiB

### 價格

記憶體 每 GB NT$129.4533

vCPU 每 vCPU NT$1,184.5094

### 小計

1184+258=1442/月

## 結論

IT 何苦為難 RD？
