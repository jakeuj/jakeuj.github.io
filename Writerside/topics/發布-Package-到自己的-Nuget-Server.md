# 發布 Package 到自己的 Nuget Server

> 首次發表：2022-12-19

---

筆記下指令

Example

dotnet pack

dotnet nuget push YourLib.1.1.1.nupkg --api-key YourApiKey --source <https://your-nuget-server.azurewebsites.net/v3/index.json>

Ref

[連線到摘要併發布 NuGet 套件 - NuGet.exe - Azure Artifacts | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/devops/artifacts/nuget/publish?view=azure-devops#publish-packages-from-external-sources)
