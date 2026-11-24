# Entity Framework (EF) Core SQL Logger with ABP(ASP.NET Boilerplate)

> 首次發表：2019-06-25

---

紀錄 EF 所生成的 SQL 語法

常想把 LinqToSql 印出來以利 Debug 調校效能

以ABP來說是位於公共設施層 - EntityFrameworkCore 專案

注入 ILoggerFactory 然後 UseLoggerFactory

EntityFrameworkModule.cs

```

private readonly ILoggerFactory _loggerFactory;

public MyProjectEntityFrameworkModule(ILoggerFactory loggerFactory)
{
  _loggerFactory = loggerFactory;
}

public override void PreInitialize()
{
  Configuration.Modules.AbpEfCore().AddDbContext<FirstDbContext>(options=>
  {
    if (options.ExistingConnection != null)
      FirstDbContextOptionsConfigurer
        .Configure(options.DbContextOptions, options.ExistingConnection);
    else
      FirstDbContextOptionsConfigurer
        .Configure(options.DbContextOptions, options.ConnectionString);
    // add sql log
    options.DbContextOptions.UseLoggerFactory(loggerFactory)
      .EnableSensitiveDataLogging();
  });
}
```

執行有跑到SQL就會印出語法到主控台

![執行有跑到SQL就會印出語法到主控台](dotblogs-31e8dfca-1561394166_29885.png)

參照：[記錄 - EF Core](https://docs.microsoft.com/zh-tw/ef/core/miscellaneous/logging#other-applications​)

參照：[Logging in EF Core 2.2 Has a Simpler Syntax–More like ASP.NET Core](http://thedatafarm.com/data-access/logging-in-ef-core-2-2-has-a-simpler-syntax-more-like-asp-net-core/)

參照：[資料點-EF Core 中的 SQL 和變更追蹤的事件記錄](http://​https://msdn.microsoft.com/zh-tw/magazine/mt830355.aspx) (已過時)

參照：[ABP框架將EntityFrameworkCore生成的SQL語句輸出到控制台](https://www.cnblogs.com/WNpursue/p/ABP-USE-UseLoggerFactory-ILoggerFactory.html)
