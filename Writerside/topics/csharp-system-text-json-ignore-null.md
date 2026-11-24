# System.Text.Json 輸出 JSON 時忽略 null

<web-summary>用 System.Text.Json 的 JsonIgnoreCondition.WhenWritingNull 讓 null 屬性不輸出到 JSON；int 這類不會是 null 的型別改用 WhenWritingDefault。</web-summary>

> 首次發表：2023-02-20

在屬性加上 `JsonIgnore` 並指定 `JsonIgnoreCondition.WhenWritingNull`，值是 null 時就不會出現在 JSON：

```c#
public class CreateTransactionDto
{
    public bool IsSuccess { get; set; }

    [property: JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public ApiException Ex { get; set; }

    [property: JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public CreateTransactionResult Result { get; set; }
}
```

## 效果

- 成功時輸出 `Result`，不輸出 `Ex`。
- 失敗時輸出 `Ex`，不輸出 `Result`。

## 不會是 null 的型別

`int` 這類型別不會是 null，可以改用 `JsonIgnoreCondition.WhenWritingDefault`，值等於型別預設值時就不輸出。要注意 `0` 或 `false` 如果是有意義的值，也會一起被省略。

## 參照

[JsonIgnoreAttribute Class (System.Text.Json.Serialization) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.text.json.serialization.jsonignoreattribute)
