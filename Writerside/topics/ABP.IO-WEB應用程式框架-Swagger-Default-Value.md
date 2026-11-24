# ABP.IO Swagger Default Value

> 首次發表：2022-09-30

---

筆記下 Swagger Input 提供 預設值 的方法

## 參照

[Get started with Swashbuckle and ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-swashbuckle?view=aspnetcore-6.0&tabs=visual-studio-code#xml-comments)

### 產生 xml

YourProject.Application.Contracts.csproj

```
<PropertyGroup>
   <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

### 設定 Swagger

YourProject.HttpApi.Host/YourProjectHttpApiHostModule.cs => ConfigureServices => ConfigureSwaggerServices

```
options =>
{
   // using System.Reflection;
   var xmlFilename = "YourProject.Application.Contracts.xml";
   options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFilename));
});
```

### 加上預設值

YourProject.Application.Contracts/YourDto.cs

```
[DefaultValue("HelloWorld")]
public string Message { get; set; }

[DefaultValue(new string[] { "a", "b" })]
public List<string> Users { get; set; }
```

![YourProject.Application.Contracts/YourDto.cs](dotblogs-3d8e3847-1669104103.jpg)
