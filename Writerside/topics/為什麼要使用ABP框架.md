# 為什麼要使用ABP框架

<web-summary>ASP.NET Boilerplate（ABP）替企業網站處理好哪些共通功能、各自怎麼運作，以及採用前要考慮的事。</web-summary>

> 首次發表：2019-01-25
>
> **更新日期：** 2026-11-25

ASP.NET Boilerplate（ABP）把每個企業網站都要重做的功能先做好，例如權限、驗證、交易、稽核記錄和多語系，開發時可以專心在業務邏輯。代價是程式要照它的分層和慣例寫，也要花時間學。

## ABP 先處理好的事 {#features}

| 需求 | ABP 的做法 |
| --- | --- |
| 相依性注入 | 應用服務依慣例自動註冊，從建構函式注入就能用 |
| 資料存取 | 每個實體都有預設的 Repository，也能自己擴充 |
| 權限 | 在方法加上屬性，沒有權限就不會執行 |
| 輸入驗證 | 依資料註解檢查，不符合就回傳驗證錯誤 |
| 交易 | 每個應用服務方法預設是一個工作單元，全部成功才提交 |
| 稽核記錄 | 自動記下使用者、IP、方法、參數和執行時間 |
| 例外處理 | 自動記錄並回傳錯誤，預設不把例外內容給使用者；`UserFriendlyException` 的訊息才會顯示 |
| 多語系 | 用 `L("名稱")` 取得目前語系的文字 |
| Web API | 應用服務在執行時變成 API，不用另外寫 Controller |

## 採用前先考慮 {#tradeoffs}

- **要照它的架構走**：分層、模組和命名都有慣例，之後要抽換比較難。
- **要先懂幾個觀念**：至少包括分層架構、相依性注入和工作單元。
- **確認是哪一套 ABP**：ASP.NET Boilerplate 和 abp.io 的 ABP Framework 是兩套框架，文件和套件不能混用。
- **小專案先評估**：功能少、很快結束的專案，多半用不到這些功能。

## 從哪裡開始 {#start}

- 想學 ASP.NET Boilerplate：[ABP 新手教學 No.0 全篇索引](abp-asp-net-boilerplate-tutorial-00-index.md)
- 想學 abp.io 的 ABP Framework：[ABP.IO 新手教學 No.00 全篇索引](abp-io-tutorial-00-index.md)

## 參考來源 {#references}

- [ASP.NET Boilerplate 官方介紹](https://aspnetboilerplate.com/Pages/Documents/Introduction)

2026-11-25 更新：這頁原本的內容取自 CSDN 的[提升.NET开发效率](https://blog.csdn.net/echoshinian100/article/details/51595664)，當時沒有標示來源。這次全部移除，改依官方介紹重寫。
