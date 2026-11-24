# Azure App Service 混合式連線 (HCM)

> 首次發表：2021-08-27

---

筆記一下 Azure App Service 連到內部不對外的服務

## Step 0

### 情境

- 內部不對外的服務
  Example: DB
- Azure 需要連到地端的服務
  Example: Azure app service

### 前提

轉送機制需要有一台中介機器可以透過 443 與 Azure 溝通

既然叫中介機器了就必須可以與地端服務溝通 (DB)

機制如下圖所示：

![機制如下圖所示：](dotblogs-57dca308-1630054072.jpg)

設定方式請參照官方文件

[混合式連線 - Azure App Service | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/app-service/app-service-hybrid-connections)

## Step 1

首先在 App Service > 網路 > 混合連線 > 新增

新增的時候會要你輸入 Host 與 Port

Host  要輸入你實際要連的服務的電腦名稱 (不是 IP)

![Host 要輸入你實際要連的服務的電腦名稱 (不是 IP)](dotblogs-57dca308-1630055533.jpg)

### 案例一 DB

比如打開 SSMS 連 DB 輸入的伺服器名稱是 PrivateDbServer

那就填這個 PrivateDbServer 進去

這同時也會是 App Service >  Appsetting.json > ConnectionStrings > Server=PrivateDbServer

至於 Port 就比如 Mssql 預設就填 1433

### 案例二 Docker

比如我在我電腦用 Docker 起了一個 Redis 服務

那在混合連線 Host 要輸入 localhost

Port 則是 6379

最後點新增好的連線內容，把連線字串複製一下，下面會用到

## Step 2

![Step 2](dotblogs-57dca308-1630055546.jpg)

設定完後點 下載連線管理員 並安裝

打開剛裝好的 連線管理員 右下按 手動輸入

把剛剛複製的連線字串貼進去並 Save

之後理應要顯示 已連線

這時 App Service 就可以正常連到本地資料庫了

## Step 3 ?

如果顯示未連接，請參照以下文檔查看錯誤訊息

[Troubleshooting Hybrid Connections with Logging - Microsoft Tech Community](https://techcommunity.microsoft.com/t5/apps-on-azure/troubleshooting-hybrid-connections-with-logging/ba-p/392384)

實際上我設定完就是顯示未連接

重開機在打開連線管理員也還是未連接

照著文檔到 Windows 事件日誌 看訊息沒有錯誤 還看到一個成功訊息

然後再回去看 連線管理員 就顯示連接成功？

總之如果沒成功，要確保 443 Port 有通，然後重開機，然後多等等，可能就好了

## 延伸閱讀

[透過 Proxy 使用 Azure HCM (混合式連線管理員)](https://jakeuj.com/透過-proxy-使用-azure-hcm-混合式連線管理員.html)
