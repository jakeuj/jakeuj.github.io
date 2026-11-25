# MiniExcel 用樣板產生 Excel：1.x 與 2.0 寫法、串流回傳與常見錯誤

<web-summary>MiniExcel 用 Excel 樣板產生檔案：1.x 的 SaveAsByTemplate、2.0 的 FillTemplate、API 直接回傳串流、合計公式，以及升級 2.0 的編譯錯誤與 ValueTuple 例外的實測結果。</web-summary>

> 首次發表：2023-06-13
>
> **更新日期：** 2026-11-25

在 Excel 樣板裡寫 `{{employees.name}}` 這種佔位符，再交給 MiniExcel 填資料，就能保留樣板的格式產生檔案。寫法依版本不同：

- **2.0**：`MiniExcelV2.Templaters.GetOpenXmlTemplater().FillTemplate(...)`
- **1.x**：`MiniExcel.SaveAsByTemplate(...)`

新專案可以直接用 2.0。已經在用 1.x 的專案不必急著升級，先看[升級前要檢查的項目](#upgrade)。

## 版本差異 {#versions}

2.0.0 在 2026-11-23 發布，API 和部分預設行為都改了。下表除了 .NET Framework 那一列取自官方升級說明，其餘是用 1.47.1 和 2.0.0 各跑一次的結果。

| 項目 | 1.47.1 | 2.0.0 |
| --- | --- | --- |
| 命名空間 | `MiniExcelLibs` | `MiniExcelLib`、`MiniExcelLib.OpenXml` |
| 樣板方法 | `MiniExcel.SaveAsByTemplate` | `FillTemplate`、`FillTemplateAsync` |
| 輸出檔已存在 | 直接覆蓋 | 丟 `IOException`，要傳 `overwriteFile: true` |
| 最低 .NET Framework | 4.5 | 4.6.2 |
| 樣板填 10 萬列 × 3 欄 | 約 264 ms | 約 535 ms |
| 最大記憶體用量 | 97 MB | 96 MB |

時間是 Release 建置、同一個行程第 4 次執行的結果，環境為 .NET 10.0.12、Apple M4 Max。這只測了樣板填充一種情境，不代表查詢或匯出也是同樣的差距。

## 安裝 {#install}

```bash
dotnet add package MiniExcel --version 2.0.0
```

要留在 1.x 就指定版本：

```bash
dotnet add package MiniExcel --version 1.47.1
```

## 準備樣板 {#template}

佔位符的格式是 `{{集合名稱.欄位名稱}}`，佔位符可以和其他文字放在同一格：

![Excel 樣板：序號、名稱、主旨三欄，主旨欄混用文字與佔位符](dotblogs-90268042-1686621414.jpg)

後面的範例都用這個兩欄的樣板 `template.xlsx`：

| | A | B |
| --- | --- | --- |
| 1 | 姓名 | 部門 |
| 2 | `{{employees.name}}` | `{{employees.department}}` |

名稱要和程式裡的屬性一致，**大小寫也要相同**。以樣板的 `{{employees.name}}` 為例，兩種寫錯都不會報錯，但結果不同：

- 集合名稱寫成 `Employees`：佔位符原封不動留在輸出檔裡。
- 欄位名稱寫成 `Name`：那一格變成空白。

## 產生檔案 {#fill}

### 2.0 寫法 {#fill-v2}

```c#
using MiniExcelLib;
using MiniExcelLib.OpenXml;

var value = new
{
    employees = new[]
    {
        new { name = "Jack", department = "HR" },
        new { name = "Neo", department = "IT" },
    },
};

var templater = MiniExcelV2.Templaters.GetOpenXmlTemplater();
templater.FillTemplate("employees.xlsx", "template.xlsx", value, overwriteFile: true);
```

兩個容易卡住的地方：

- `GetOpenXmlTemplater` 是擴充方法，少了 `using MiniExcelLib.OpenXml;` 會出現 `CS1061`。
- 截至 2026-11-25，官方 README 多數範例寫的是 `ApplyTemplate`，但 2.0.0 套件裡沒有這個方法，要用 `FillTemplate`。

### 1.x 寫法 {#fill-v1}

```c#
using MiniExcelLibs;

var value = new
{
    employees = new[]
    {
        new { name = "Jack", department = "HR" },
        new { name = "Neo", department = "IT" },
    },
};

MiniExcel.SaveAsByTemplate("employees.xlsx", "template.xlsx", value);
```

## API 直接回傳 Excel {#return-stream}

不想先存檔，可以填進 `MemoryStream` 再回傳。填完後資料流的位置停在結尾，**回傳前要把 `Position` 設回 0**，否則 ASP.NET Core 會回 HTTP 500。

```c#
using MiniExcelLib;
using MiniExcelLib.OpenXml;

var app = WebApplication.CreateBuilder(args).Build();

app.MapGet("/employees.xlsx", async (CancellationToken ct) =>
{
    var value = new
    {
        employees = new[] { new { name = "Jack", department = "HR" } },
    };

    var stream = new MemoryStream();
    var templater = MiniExcelV2.Templaters.GetOpenXmlTemplater();
    await templater.FillTemplateAsync(stream, "template.xlsx", value, cancellationToken: ct);
    stream.Position = 0;

    return Results.File(
        stream,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "employees.xlsx");
});

app.Run();
```

在 ABP 裡做法相同，差別是從虛擬檔案系統讀樣板，並回傳 `RemoteStreamContent`。下面是原本用 1.x 寫的版本，這次更新沒有重跑：

```c#
public async Task<IRemoteStreamContent> GenerateExcels(List<User> input)
{
    var provider = CachedServiceProvider.GetRequiredService<IVirtualFileProvider>();
    var file = provider.GetFileInfo(UserConsts.TemplatePath);
    var template = await file.ReadBytesAsync();

    var memoryStream = new MemoryStream();
    await memoryStream.SaveAsByTemplateAsync(template, new { V = input });
    memoryStream.Seek(0, SeekOrigin.Begin);

    return new RemoteStreamContent(
        memoryStream,
        "Sample.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
}
```

## 在清單下方加總 {#sum}

### 用 Excel 公式 {#sum-formula}

公式前面加 `$`，並用 `$enumrowstart`、`$enumrowend` 代表清單的起訖列：

| | A | B |
| --- | --- | --- |
| 1 | 品項 | 金額 |
| 2 | `{{items.name}}` | `{{items.amount}}` |
| 3 | 合計 | `$=SUM(B{{$enumrowstart}}:B{{$enumrowend}})` |

填入 3 筆資料後，兩個版本都會產生公式 `SUM(B2:B4)`。

樣板請用 Excel 存檔。用 MiniExcel 1.47.1 自己的 `SaveAs` 產生的樣板來測，公式沒有被轉換；換成和 Excel 相同的 sharedStrings 格式就正常。

### 在程式裡先算好 {#sum-code}

也可以把合計算好，當成一般欄位傳入。合計列直接寫在清單的下一列，資料變多時會自動往下推：

![樣板：items 清單下方一列是 Total 與 totalPrice 佔位符](dotblogs-90268042-1687257170.jpg)

![輸出結果：兩筆資料下方顯示合計 150000](dotblogs-90268042-1687257311.jpg)

## 可以傳哪些型別 {#data-types}

兩個版本的結果相同：

| 清單的元素型別 | 結果 |
| --- | --- |
| 匿名型別、`class`、`record` | 正常 |
| `Dictionary<string, object>` | 正常 |
| `DataTable` | 正常 |
| `System.Tuple`（樣板寫 `{{employees.Item1}}`） | 正常 |
| `ValueTuple`，例如 `(string name, string department)` | 丟 `NullReferenceException` |

會出錯的只有 `ValueTuple`，不管樣板寫 `name` 還是 `Item1` 都一樣。合理的解釋是 MiniExcel 讀的是屬性，而 `ValueTuple` 的 `Item1`、`Item2` 是欄位，自訂的元素名稱也只存在於編譯期。改用 `record` 最省事：

```c#
public record Employee(string name, string department);
```

## 常見錯誤 {#errors}

| 狀況 | 原因 | 處理方式 |
| --- | --- | --- |
| 輸出檔還看得到 `{{employees.name}}` | 集合是 `null`、沒有傳這個名稱，或大小寫不同 | 補上資料；沒有資料就傳空集合，該列會被移除 |
| 儲存格變成空白 | 沒有傳這個欄位、值是 `null`，或欄位名稱大小寫不同 | 補上欄位，並核對大小寫 |
| `KeyNotFoundException` | 設定了 `IgnoreTemplateParameterMissing = false`，而且少傳名稱 | 這是刻意的檢查，補上缺少的名稱 |
| `IOException: The file ... already exists` | 2.0 預設不覆蓋輸出檔 | 傳 `overwriteFile: true` |
| `NullReferenceException` | 清單元素是 `ValueTuple` | 改用 `record` 或 `class` |
| API 回 HTTP 500 | 回傳前沒有把資料流位置設回 0 | `stream.Position = 0` |

少傳集合或單一變數時預設不會報錯，很容易把帶著佔位符的檔案寄出去。想提早發現，就打開檢查：

```c#
var config = new OpenXmlConfiguration { IgnoreTemplateParameterMissing = false };
templater.FillTemplate("employees.xlsx", "template.xlsx", value, configuration: config);
```

## 從 1.x 升級到 2.0 前 {#upgrade}

2.0 的完整套件保留了舊的 `MiniExcelLibs.MiniExcel`，同步的 `SaveAsByTemplate` 可以不改程式直接編譯，也維持覆蓋檔案的行為。但下面兩種寫法升級後**無法編譯**：

| 1.x 寫法 | 2.0.0 的編譯錯誤 | 改法 |
| --- | --- | --- |
| `SaveAsByTemplateAsync(stream, bytes, value, cancellationToken: ct)` | `CS1503` | 改用 `FillTemplateAsync`，它的多載都有 `cancellationToken` |
| `await MiniExcel.QueryAsync(path)` | `CS9353` | 現在回傳 `IAsyncEnumerable`，改用 `await foreach` |

另外要留意：

- 改用新 API 時，舊程式若依賴「自動覆蓋」，要補 `overwriteFile: true`。
- 專案還在 .NET Framework 4.5 到 4.6.1 的話，不能升級。
- 樣板資料量大、對時間敏感的工作，先用自己的資料量測再決定。

## 參考資料 {#references}

- [MiniExcel 官方 README（2.0）](https://github.com/mini-software/MiniExcel)
- [MiniExcel 2.0 升級說明](https://github.com/mini-software/MiniExcel/blob/master/V2-Upgrade-Notes.md)
- [MiniExcel 1.x README](https://github.com/mini-software/MiniExcel/blob/master/README_V1.md)
- [MiniExcel NuGet 套件](https://www.nuget.org/packages/MiniExcel)
- [C# 使用 CsvHelper 讀取 CSV](https://jakeuj.com/c-使用-csvhelper-讀取csv並略過前n行非csv內容.html)
