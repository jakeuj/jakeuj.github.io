# ABP (ASP.NET Boilerplate) 新手教學 No.0 全篇索引

<web-summary>ASP.NET Boilerplate 新手教學系列索引，從建立專案、實體、資料庫、倉儲、應用服務到 WebApi 與單元測試共 15 篇。</web-summary>

> 首次發表：2016-07-28
>
> **更新日期：** 2026-11-25

這是我學 ASP.NET Boilerplate（官方簡稱 ABP）時寫的系列筆記。照 No.1 到 No.9 的順序做，會用地圖和玩家兩個實體，從下載樣板走到可以測試的 Web API。No.10 之後是 2019 年補的個別主題。

> 內容寫於 2016 到 2019 年，前九篇用 .NET Framework 和 Entity Framework 6。新專案請以[官方文件](https://aspnetboilerplate.com/Pages/Documents)為準。abp.io 的 ABP Framework 是另一套框架，請看[ABP.IO 新手教學索引](abp-io-tutorial-00-index.md)。
{style="note"}

## 入門九篇 {#basics}

| 文章 | 內容 |
| --- | --- |
| [No.1 建立專案](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-1-建立專案.html) | 下載官方樣板、改連線字串、用 `Update-Database` 建立資料庫 |
| [No.2 建立實體 Entity](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-2-建立實體-entity.html) | 分層說明，建立 `Map` 與 `Player` 兩個實體 |
| [No.3 建立資料庫上下文 DbContext](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-3-建立資料庫上下文-dbcontext.html) | 加上 `IDbSet`，設定 `Player` 對應 `Map` |
| [No.4 資料庫遷移 Migration](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-4-資料庫遷移-migration.html) | 撰寫 SeedData，用 `Add-Migration` 產生版本 |
| [No.5 建立倉儲 Repository](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-5-建立倉儲-repository.html) | 自訂倉儲介面與實作，`GetAll()` 和 `GetAllList()` 的差別 |
| [No.6 建立應用服務](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-6-建立應用服務.html) | DTO、輸入驗證與 `AppService` |
| [No.7 建立 WebApi](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-7-建立webapi.html) | 把自動產生的 API 從 POST 改成 GET |
| [No.8 單元測試](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-8-單元測試.html) | 用 xUnit 和記憶體資料庫測應用服務 |
| [No.9 全篇後記](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-9-全篇後記.html) | 系列整理與沒有講到的功能 |

## 個別主題 {#topics}

| 文章 | 內容 |
| --- | --- |
| [No.10 範例程式](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-新手教學-no-10-範例程式.html) | 官方 EventCloud 範例的中文翻譯 |
| [No.11 Client Proxies (Angular Service)](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-no-11-client-proxies.html) | API 更新後用 NSwag 重新產生前端服務 |
| [No.12 複數資料庫 (DbContext)](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-no-12-複數資料庫-dbcontext.html) | 同一個專案連兩個資料庫 |
| [No.13 Angular Service](https://jakeuj.com/abp-asp-net-boilerplate-應用程式開發框架-no-13-angular-service.html) | 從應用服務到 Angular 頁面，包含權限與多語系 |
| [No.14 SignalR with Angular](No.14-SignalR-with-Angular.md) | 自訂 Hub 並由 Angular 呼叫 |
| [No.15 Angular DateTime UTC Offset](No.15-Angular-DateTime-UTC-Offset.md) | 前後端時區對不起來的處理 |

## 參考來源 {#references}

前九篇是我看完 tkbSimplest 的系列教學後，換成自己的例子重做一次。程式碼有部分來自該教學與官方專案樣板，各篇文末都有連結。

- [ASP.NET Boilerplate 官方文件](https://aspnetboilerplate.com/Pages/Documents)
- [一步一步使用ABP框架搭建正式项目系列教程（tkbSimplest）](https://www.cnblogs.com/farb/p/ABPPracticeContent.html)
- [基于DDD的现代ASP.NET开发框架：ABP 系列文章总目录（阳光铭睿）](https://www.cnblogs.com/mienreal/p/4528470.html)
- [ABP 中文翻譯文件（GitHub）](https://github.com/ABPFrameWorkGroup/AbpDocument2Chinese)

2026-11-25 更新：移除原本取自前兩位作者文章的框架介紹與特性清單，以及一張 ABP.IO 官方文件的分層圖（那是另一套框架的架構）。想看完整介紹，請讀[ABP 总体介绍（阳光铭睿）](https://www.cnblogs.com/mienreal/p/4528641.html)或[介紹（tkbSimplest）](https://www.cnblogs.com/farb/p/ABPIntro.html)。
