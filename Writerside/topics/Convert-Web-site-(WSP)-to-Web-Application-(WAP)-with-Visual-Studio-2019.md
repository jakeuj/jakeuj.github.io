# Web Site Project (WSP) 轉 Web Application (WAP)：Visual Studio 2019 步驟

<web-summary>ASP.NET 網站型專案（WSP）轉成 Web 應用程式專案（WAP）的 Visual Studio 2019 步驟：App_Code 怎麼處理、轉換指令在哪裡，以及轉完常見的問題。</web-summary>

> 首次發表：2021-03-02
>
> **更新日期：** 2026-11-25

做法是另建一個空白的 WAP 專案，把舊網站的檔案複製進去，再執行「轉換成 Web 應用程式」。我在 Visual Studio 2019 找這個指令卡了很久：舊版在方案總管按右鍵就有，新版要從上方的「專案」選單點進去才看得到。

> 步驟是 2021 年的實作紀錄。這次更新依微軟文件補充說明，沒有在 Windows 上重跑。
{style="note"}

## 轉換步驟 {#steps}

1. 先確認舊網站能正常建置和執行，再新建一個空白的 ASP.NET Web 應用程式專案。
2. 把舊網站的頁面和程式碼（包含 `App_Code`）複製到新專案，並加入專案。
3. 全選 `App_Code` 裡的檔案，在「屬性」視窗的「進階」把「建置動作」從「內容」改成「編譯」。

   ![屬性視窗的建置動作選編譯](dotblogs-4d2ba2fb-1614670712.jpg)

4. 補上缺少的 NuGet 套件。
5. 排除其他編譯錯誤。我遇到的是把 A 頁面複製成 B 頁面時，忘記改 class 名稱，變成兩個同名的類別。
6. 點選上方「專案」選單最下面的「轉換成 Web 應用程式」。

   ![專案選單最下面的轉換成 Web 應用程式](dotblogs-4d2ba2fb-1614670402.jpg)

7. 建置並測試。

## 轉換指令會做什麼 {#convert}

依微軟文件，這個指令會：

- 替每個頁面、主版頁面和使用者控制項產生 `.designer.cs` 或 `.designer.vb`。
- 把 `.aspx`、`.ascx` 的 `codeFile` 屬性改成 `codeBehind`。
- 把 `App_Code` 改名成 `Old_App_Code`。

> 要編譯的類別不要留在 `App_Code`。ASP.NET 執行時會再動態編譯這個資料夾，同一個類別會出現兩份，可能發生「could not load type」。
{style="warning"}

## 轉完常見的問題 {#issues}

| 狀況 | 處理方式 |
| --- | --- |
| 舊專案本身就不能建置，卻想先偵錯 | 到「偵錯」、「偵錯屬性」、「建置」，改成不建置 |
| 不支援新版 C# 語法 | 編譯器改用 Roslyn，C# 版本從 5.0 升到 7.3，做法看[ASP.NET WebSite 使用新版 C Sharp](https://jakeuj.com/如何在舊的-asp-net-website-使用新版-c-語言特性-7-3.html) |
| 想加上命名空間 | WSP 的類別預設沒有命名空間。加上之後，`@ Page` 等指示詞的 `Inherits` 也要一起改 |
| 找不到 `Profile` | WAP 不會自動產生 `ProfileCommon`，要自己建立類別 |
| `App_Code` 裡有強型別 DataSet | 在設計工具裡重新設定每個 TableAdapter 的連線 |

## WSP 和 WAP 的差別 {#differences}

| 項目 | WSP | WAP |
| --- | --- | --- |
| 專案檔 | 沒有，資料夾裡的檔案都算在內 | 由 `.csproj` 或 `.vbproj` 列出 |
| 編譯 | 通常由 ASP.NET 在伺服器上動態編譯，也能先行編譯 | 事先編譯成單一組件 |
| 部署 | 通常要放原始碼 | 放組件和頁面，不用放原始碼 |
| 跨頁共用的類別 | 動態編譯時要放 `App_Code` | 可以放在任何資料夾 |
| 更新單一頁面 | 複製那個檔案就好 | 改到程式碼要重新部署整個組件 |

效能方面，微軟文件說兩者沒有差別，例外只有非常大的網站。新專案微軟建議用 WAP。

## 參考來源 {#references}

- <a href="https://learn.microsoft.com/previous-versions/aspnet/aa983476(v=vs.100)">逐步解說：將網站專案轉換成 Web 應用程式專案</a>
- <a href="https://learn.microsoft.com/previous-versions/aspnet/dd547590(v=vs.110)">Web 應用程式專案與網站專案的比較</a>
- [閒聊：Web Site Project為何沒落？（黑暗執行緒）](https://blog.darkthread.net/blog/why-wsp-fall/)

2026-11-25 更新：原本「WSP 缺點」六點取自黑暗執行緒的文章，當時沒有標示來源。這次移除，改依微軟文件整理差別。
