# ABP.IO EnableSensitiveDataLogging

> 首次發表：2021-11-05

---

本文說明如何在 ABP.IO WEB應用程式框架中啟用敏感資料紀錄（EnableSensitiveDataLogging）。

紀錄 Framework 啟用輸入值顯示在 Log 的設定

Logging 會隱藏 SQL 錯誤的一些敏感資料

可能是實際輸入的值之類的資訊

開發 Debug 需要看了話需要設定一下 `EnableSensitiveDataLogging`

```
options.Configure(configureOptions =>
{
  configureOptions.UseSqlServer();
  configureOptions.DbContextOptions.EnableSensitiveDataLogging();
});
```

參考

Project.EntityFrameworkCore.ProjectEntityFrameworkCoreModule.cs

```
Configure<AbpDbContextOptions>(options =>
{
    /* The main point to change your DBMS.
     * See also ProjectMigrationsDbContextFactory for EF Core tooling. */
    options.UseSqlServer();

    //TODO: Debug 用完需註解
    options.Configure(configureOptions =>
    {
        configureOptions.UseSqlServer();
        configureOptions.DbContextOptions.EnableSensitiveDataLogging();
    });
});
```

參照

[DbContextOptionsBuilder.EnableSensitiveDataLogging throws InvalidOperationException · Issue #4557 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/4557)
