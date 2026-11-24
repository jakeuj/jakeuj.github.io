# Azure App Service 存取限制

> 首次發表：2021-09-01

---

筆記一下鬼打牆後的解決方案

## 結論

存取限制 > 允許 > 來源設定 > 服務標籤 > AzureCloud

之後就可以了

## 案發現場

IS4 噴 500 Error，找元凶是裡面 Get /.well-known/openid-configuration 噴 403 Error…

[ABP.IO WEB應用程式框架 AzureAD 登入](ABP.IO-WEB應用程式框架-AzureAD-登入.md)

## TODO

應該是有範圍比較小的允許設定

但我試了 AppService.SouthEastAsia 沒用

有空再找找看

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- App Service
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
