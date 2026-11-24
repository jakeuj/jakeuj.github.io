# HttpClient GZip 壓縮

> 首次發表：2020-05-18

---

使用 HttpClient GetAsync PostAsync 啟用 gzip 壓縮

設定標頭 RequestHeaders accept-encoding gzip

使用 GZipStream 解壓 responseStream 後讀取資料

```

client.DefaultRequestHeaders.Add("accept-encoding","gzip");
```

```

using var responseStream = await response.Content.ReadAsStreamAsync();
using var decompressed = new GZipStream(responseStream, CompressionMode.Decompress);
using var sr = new StreamReader(decompressed);
var output = await sr.ReadToEndAsync();
Console.WriteLine(output);
```

有需要可以搭配Json使用

```

public static async Task<T> ReadAsJsonAsync<T>(this Stream content)
{
    return await JsonSerializer.DeserializeAsync<T>(content,
        new JsonSerializerOptions { PropertyNameCaseInsensitive = true, IgnoreNullValues = true });
}

public static async Task<T> ReadAsJsonAsync<InputT,T>(this InputT content) where InputT:Stream
{
    return await content.ReadAsJsonAsync<T>();
}
```
