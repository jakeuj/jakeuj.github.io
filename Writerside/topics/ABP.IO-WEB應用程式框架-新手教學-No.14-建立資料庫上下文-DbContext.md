# ABP.IO 新手教學 No.14 建立資料庫上下文 DbContext

> 首次發表：2021-07-19

---

[ABP.IO WEB應用程式框架 新手教學 No.0 索引](abp-io-tutorial-00-index.md)

這步驟跟原本 Entity Framework 其實是一樣的

到 Acme.BookStore.EntityFrameworkCore 專案的 BookStoreDbContext 加入 Book

```
public class BookStoreDbContext : AbpDbContext<BookStoreDbContext>
{
    public DbSet<Book> Books { get; set; }
    //...
}
```

然後關於表的額外設定要到 BookStoreDbContextModelCreatingExtensions 去新增

![然後關於表的額外設定要到 BookStoreDbContextModelCreatingExtensions 去新增](dotblogs-f1e3a920-1626681339.jpg)

```
namespace Acme.BookStore.EntityFrameworkCore
{
    public static class BookStoreDbContextModelCreatingExtensions
    {
        public static void ConfigureBookStore(this ModelBuilder builder)
        {
            Check.NotNull(builder, nameof(builder));

            /* Configure your own tables/entities inside here */

            builder.Entity<Book>(b =>
            {
                b.ToTable(BookStoreConsts.DbTablePrefix + "Books",
                          BookStoreConsts.DbSchema);
                b.ConfigureByConvention(); //auto configure for the base class props
                b.Property(x => x.Name).IsRequired().HasMaxLength(128);
            });
        }
    }
}
```

- BookStoreConsts 含有用於表的架構和表前綴的常量值. 你不必使用它,但建議在單點控製表前綴.
  定義在 Domain.Share 裡面，就是表前綴這類大家會需要用到的東西，建議統一定義在一個地方，大家要找要改比較方便
- ConfigureByConvention() 方法優雅的配置/映射繼承的屬性,應始終對你所有的實體使用它.

裡面東西應該跟原本 EF 是一樣的定義方式，如果沒用過 EF 或不太熟可以去 MSDN 先看一下說明

大概就是資料表的名稱，這邊會加上前綴(App)，然後定義一些必要欄位不能是null，還有字串欄位長度上限…等等。

---

[多個連線字串對應到不同DbContext](https://docs.abp.io/en/abp/latest/Connection-Strings#set-the-connection-string-name)

[ABP.IO WEB應用程式框架 新手教學 No.4 資料庫遷移 Migration](ABP.IO-WEB應用程式框架-新手教學-No.15-資料庫遷移-Migration.md)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
