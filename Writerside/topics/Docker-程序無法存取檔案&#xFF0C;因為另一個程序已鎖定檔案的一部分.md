# Docker 程序無法存取檔案&#xFF0C;因為另一個程序已鎖定檔案的一部分

> 首次發表：2024-03-07

---

Preparing build context archive…

Failed to deploy

`java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。`

![java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。](dotblogs-42fe5267-1709797808.jpg)

結論

將 Context folder 設為專案路徑 (等同於不設定 Context folder)

原因

Rider 直接執行專案內的 dockerfile 時，會把 Context folder 設為方案路徑 (也就是專案的上一層目錄)，導致路徑錯誤

![Rider 直接執行專案內的 dockerfile 時，會把 Context folder 設為方案路徑 (也就是專案的上一層目錄)，導致路徑錯誤](dotblogs-42fe5267-1709796319.jpg)

錯誤訊息

```
Deploying '<unknown> Dockerfile: Platform/Dockerfile'…
Building image…
Preparing build context archive…
[====>                                              ]15/159 files
Failed to deploy '<unknown> Dockerfile: Platform/Dockerfile': java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。
```

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Rider

- 回首頁

---

*本文章從點部落遷移至 Writerside*
