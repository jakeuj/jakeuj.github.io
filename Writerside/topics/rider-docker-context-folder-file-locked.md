# Rider Docker 部署出現檔案被另一個程序鎖定

<web-summary>Rider 執行專案內的 Dockerfile 出現 java.io.IOException 檔案被鎖定時，把 Context folder 設為專案路徑即可。</web-summary>

> 首次發表：2024-03-07

在 Rider 的 Run/Debug Configurations 把 **Context folder** 設為專案路徑，或清空不設定，就能正常建置。

## 症狀

```text
Building image…
Preparing build context archive…
[====>                                              ]15/159 files
Failed to deploy '<unknown> Dockerfile: Platform/Dockerfile': java.io.IOException: 程序無法存取檔案，因為另一個程序已鎖定檔案的一部分。
```

## 原因

在 Rider 直接執行專案內的 Dockerfile 時，Context folder 會被設成方案路徑，也就是專案的上一層目錄。打包 build context 時會掃到不該打包的檔案，其中有些正被其他程序使用。

![Rider 的 Docker 執行設定](dotblogs-42fe5267-1709797808.jpg)
