# App Service 部署出現 UnauthorizedAccessException

<web-summary>Azure App Service 部署 .NET 出現 System.UnauthorizedAccessException 時，加上 DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false，避免 CLI 修改 PATH。</web-summary>

> 首次發表：2024-02-21

部署失敗並出現 `System.UnauthorizedAccessException: Attempted to perform an unauthorized operation` 時，在應用程式設定加入 `DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false` 再重新部署。

## 結論

添加應用程式設定值

![添加應用程式設定值](dotblogs-cd613192-1708499037.jpg)

`DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false`

部署成功

## 徵狀

![徵狀](dotblogs-cd613192-1708499789.jpg)

```
2020-04-17T13:10:41.963 [Information] System.UnauthorizedAccessException: Attempted to perform an unauthorized operation.
2020-04-17T13:10:41.963 [Information] at Internal.Win32.RegistryKey.Win32Error(Int32 errorCode, String str)
2020-04-17T13:10:41.963 [Information] at Internal.Win32.RegistryKey.SetValue(String name, String value)
2020-04-17T13:10:41.983 [Information] at System.Environment.SetEnvironmentVariableFromRegistry(String variable, String value, Boolean fromMachine)
2020-04-17T13:10:41.983 [Information] at System.Environment.SetEnvironmentVariable(String variable, String value, EnvironmentVariableTarget target)
2020-04-17T13:10:42.011 [Information] at Microsoft.DotNet.Cli.Utils.EnvironmentProvider.SetEnvironmentVariable(String variable, String value, EnvironmentVariableTarget target)
2020-04-17T13:10:42.011 [Information] at Microsoft.DotNet.ShellShim.WindowsEnvironmentPath.AddPackageExecutablePathToUserPath()
2020-04-17T13:10:42.011 [Information] at Microsoft.DotNet.Configurer.DotnetFirstTimeUseConfigurer.Configure()
2020-04-17T13:10:42.021 [Information] at Microsoft.DotNet.Cli.Program.ConfigureDotNetForFirstTimeUse(IFirstTimeUseNoticeSentinel firstTimeUseNoticeSentinel, IAspNetCertificateSentinel aspNetCertificateSentinel, IFileSentinel toolPathSentinel, Boolean hasSuperUserAccess, DotnetFirstRunConfiguration dotnetFirstRunConfiguration, IEnvironmentProvider environmentProvider)
2020-04-17T13:10:42.021 [Information] at Microsoft.DotNet.Cli.Program.ProcessArgs(String[] args, ITelemetry telemetryClient)
2020-04-17T13:10:42.022 [Information] at Microsoft.DotNet.Cli.Program.Main(String[] args)
```

## 情境

Azure App Service 部屬中心 選擇 DevOps Repo 來源完成 CI/CD 設定

但觸發部署後一直失敗

關鍵訊息如下

`System.UnauthorizedAccessException: Attempted to perform an unauthorized operation.`

查了半天之後需要加設定值

`DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false`

## 原因

以下說明整理自當時 ChatGPT 的回覆。

設定 `DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false` 的作用是禁止 .NET Core CLI 在首次運行時將全局工具的路徑添加到系統的環境變數中。

當您執行 `dotnet` 命令時，.NET Core CLI 會檢查是否是首次運行，如果是，它會執行一些初始化操作，包括將全局工具的路徑添加到系統的 `PATH` 環境變數中。這樣做是為了讓全局安裝的 .NET 工具可以在任何地方被直接調用。然而，在某些受限的環境中，如 Azure App Service，應用程式可能沒有修改系統環境變數的權限，導致 `System.UnauthorizedAccessException` 錯誤。

通過設定 `DOTNET_ADD_GLOBAL_TOOLS_TO_PATH=false`，您告訴 .NET Core CLI 在首次運行時不要嘗試修改系統的 `PATH` 環境變數，從而避免了權限問題，使得您的應用程式可以正常部署。這種方法的缺點是您無法在該環境中直接使用全局安裝的 .NET 工具，但對於大多數 Web 應用程式來說，這通常不是問題。

## 參照

[使用 NuGet 引用的門戶內函數產生時發生錯誤 ·期刊 #5893 ·Azure/azure-functions-host (github.com)](https://github.com/Azure/azure-functions-host/issues/5893)
