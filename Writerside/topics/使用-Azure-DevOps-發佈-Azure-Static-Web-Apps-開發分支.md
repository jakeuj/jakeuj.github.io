# Azure DevOps 發佈 Static Web Apps

> 首次發表：2023-08-08

---

筆記下 Azure 靜態網站部屬不同環境 (類似 App Service Slot)

## 結論

```
trigger:
  - main
  - dev
  - staging

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true
  - task: AzureStaticWebApp@0
    inputs:
      ...
      production_branch: 'main'
```

### 原本

```
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    submodules: true
  - task: AzureStaticWebApp@0
    inputs:
      ...
```

### Azure

![Azure](dotblogs-effc1a28-1691466037.jpg)

理論上在預覽環境就會多出來可以瀏覽的按鈕

## 參照

[在 Azure Static Web Apps 中建立分支預覽環境 | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/static-web-apps/branch-environments?tabs=azure-devops#example)

[使用 Azure DevOps 發佈 Azure Static Web Apps](使用-Azure-DevOps-發佈-Azure-Static-Web-Apps.md)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CI/CD
{ignore-vars="true"}
- DevOps
- Azure Static Web Apps
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
