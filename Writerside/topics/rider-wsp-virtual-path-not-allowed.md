# Rider 偵錯 WSP 出現 virtual path maps to another application

<web-summary>Rider 偵錯 Web Site Project 出現 the virtual path maps to another application 時，把 .sln 的 Debug.AspNetCompiler.VirtualPath 改成根路徑。</web-summary>

> 首次發表：2024-01-04

修改 `.sln`，把 Web Site Project 的虛擬路徑改成根路徑：

```text
Debug.AspNetCompiler.VirtualPath = "/"
```

## 症狀

同一個方案在 Visual Studio 2022 偵錯正常，用 Rider 偵錯就報錯：

```text
the virtual path maps to another application, which is not allowed
```

## 原因與處理

`.sln` 裡原本的設定帶有子路徑：

```text
Debug.AspNetCompiler.VirtualPath = "/localhost_53574"
```

改成 `"/"` 之後 Rider 就能正常偵錯。這個設定是 Web Site Project（WSP）才有的；改用 Web Application Project 就不會遇到，可參考 [WSP 轉 WAP](https://jakeuj.com/convert-web-site-wsp-to-web-application-wap-with-visual-studio-2019.html)。

## 參照

[ASP.NET virtual path maps to another application which is not allowed (stackoverflow.com)](https://stackoverflow.com/questions/19277350/asp-net-virtual-path-maps-to-another-application-which-is-not-allowed)
