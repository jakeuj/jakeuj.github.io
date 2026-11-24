# C# Swagger Enum 顯示

> 首次發表：2023-04-25

---

Swagger UI 列舉值 1,2,3 改用文字顯示的方法

![Swagger UI 列舉值 1,2,3 改用文字顯示的方法](dotblogs-aaeff51c-1682406548.jpg)

## 結論

### 新增

src/Project.HttpApi.Host/Swagger/EnumSchemaFilter.cs

```
internal sealed class EnumSchemaFilter : ISchemaFilter
{
    public void Apply(OpenApiSchema model, SchemaFilterContext context)
    {
        if (!context.Type.IsEnum)
        {
            return;
        }

        model.Enum.Clear();
        Enum
            .GetNames(context.Type)
            .ToList()
            .ForEach(name => model.Enum.Add(new OpenApiString($"{name}")));
        model.Type = "string";
        model.Format = string.Empty;
    }
}
```

### 修改

src/Project.HttpApi.Host/ProjectHttpApiHostModule.cs

`options.SchemaFilter<EnumSchemaFilter>();`

```
private static void ConfigureSwaggerServices(
  ServiceConfigurationContext context,
  IConfiguration configuration)
{
    context.Services.AddAbpSwaggerGenWithOAuth(
        configuration["AuthServer:Authority"],
        new Dictionary<string, string>
        {
            { "Project", "Project API" }
        },
        options =>
        {
            options.SwaggerDoc("v1", new OpenApiInfo { Title = "Project API", Version = "v1" });
            options.DocInclusionPredicate((docName, description) => true);
            options.CustomSchemaIds(type => type.FullName);
            // 使用 Filter
            options.SchemaFilter<EnumSchemaFilter>();
        });
}
```

### 備註

這邊是只改 Swagger UI 選單的顯示部分 (不影響 API)

還有另一種是直接把原本 API 由 enum int 改傳 string

### 參照

[C# convert enum value to String](https://jakeuj.com/c-convert-enum-value-to-string.html)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Swagger

- 回首頁

---

*本文章從點部落遷移至 Writerside*
