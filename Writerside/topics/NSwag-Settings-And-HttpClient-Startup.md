# NSwag Settings &amp; HttpClient Startup {id="NSwag-Settings-And-HttpClient-Startup"}

> 首次發表：2022-09-27

---

筆記下用 NSwag 產生 HttpClient 的設定注意事項

## 結論

1. 按照微軟官方文件下載並安裝 NSwag 桌面應用程式
   [NSwag 與 ASP.NET Core 使用者入門 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/tutorials/getting-started-with-nswag?view=aspnetcore-6.0&tabs=visual-studio)
2. 設定 NSwag 產生 Client 的細節，改命名空間跟類別名稱
   這邊因為我打算從 Startup 用 Typed Client 的方式設定 baseUrl
   所以需要特別取消勾選 Use the base URL for the request

![所以需要特別取消勾選 Use the base URL for the request](dotblogs-8dc743da-1664251597.jpg)

      3. 在專案內建立一個程式碼檔案，並將產生的 Outputs 程式碼複製貼上，例如 TestProxy.cs

      4. 在 Startup 註冊該 TypedClient，並由 appsettings 設定 baseUrl

```
private void ConfigureHttpClient(
    ServiceConfigurationContext context,
    IConfiguration configuration)
{
    context.Services.AddHttpClient<ITestProxy,TestProxy>(opt =>
    {
        if(Uri.TryCreate(configuration["TestProxy:URL"], UriKind.Absolute,out var uri))
        {
            opt.BaseAddress = uri;
        }
    });
}
```

      5. 最後在需要使用的地方直接注入該 TypedClient，範例是 `ITestProxy`

```
private readonly ITestProxy _service;

public TestManager(ITestProxy service)
{
    _service = service;
}
```

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- HttpClinet
- NSwag
- Swagger

- 回首頁

---

*本文章從點部落遷移至 Writerside*
