# NuGet Restore 找不到自訂套件來源

<web-summary>NuGet Restore 抓不到自訂來源時，把 NuGet.Config 從專案目錄移到 .sln 同一層，專案層級的 NuGet.config 已不正式支援。</web-summary>

> 首次發表：2024-03-04

把 `NuGet.Config` 從專案目錄移到 `.sln` 同一層目錄，還原時就會讀到自訂來源。

```
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <!-- remove any machine-wide sources with <clear/> -->
    <clear />
    <!-- add an Azure Artifacts feed -->
    <add key="nuget.server" value="https://<your-nuget-server>/v3/index.json" />
    <!-- also get packages from the NuGet Gallery -->
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
  </packageSources>
</configuration>
```

最新版本的 NuGet 不正式支持專案級 NuGet.config 檔。

相關文件與討論：

[fixing #1433 · NuGet/docs.microsoft.com-nuget@e3058f0 (github.com)](https://github.com/NuGet/docs.microsoft.com-nuget/commit/e3058f0061995ce8d5c5c71f6c9d9a865ce2384b)

[Rider 不會在“管理 Nuget 包”視窗中顯示存儲在專案級別的 NuGet.config 中的 NuGet 源：RIDER-19809 (jetbrains.com)](https://youtrack.jetbrains.com/issue/RIDER-19809/Rider-does-not-show-NuGet-feeds-from-NuGet.config-stored-at-project-level-in-Manage-Nuget-Packages-window)

[docs.microsoft.com-nuget/docs/consume-packages/configuring-nuget-behavior.md at main · NuGet/docs.microsoft.com-nuget (github.com)](https://github.com/NuGet/docs.microsoft.com-nuget/blob/main/docs/consume-packages/configuring-nuget-behavior.md#config-file-locations-and-uses)

## 情境

隔一段時間會遇到自定義 Nuget Server 沒有自動 Restore 的情況

可以按以下情況進行對應處理

- 無 Custom Nuget Server Url
  - 手動下載 .nuget 並於 nuget source 加入 local path
- 有 Custom Nuget Server Url
  - 有 NuGet.Config
    - 確認該檔路徑位於 .sln 目錄
  - 無 NuGet.Config
    - 於 .sln 目錄新建 NuGet.Config
    - 手動於 nuget source 加入 Url

## 延伸閱讀

[發布 Package 到自己的 Nuget Server](發布-Package-到自己的-Nuget-Server.md)

[指定 NuGet packages 存放位置 - Yowko's Notes](https://blog.yowko.com/nuget-folder/)
