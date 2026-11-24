# 將 nullable DateTime? 轉成指定格式字串

> 首次發表：2023-02-01

---

筆記一下 DateTime?.ToString("yyyyMMdd") 的問題

![筆記一下 DateTime?.ToString("yyyyMMdd") 的問題](dotblogs-c3279c50-1675303184.jpg)

結論

`GetValueOrDefault()`

```
DateTime? youWinDate = null;
var yyyyMMdd = youWinDate.GetValueOrDefault().ToString("yyyyMMdd");
yyyyMMdd.Dump();
```

![GetValueOrDefault()](dotblogs-c3279c50-1675303258.jpg)![GetValueOrDefault() 2](dotblogs-c3279c50-1675303117.jpg)

參照

[How to parse nullable DateTime object in C# - Stack Overflow](https://stackoverflow.com/questions/19152764/how-to-parse-nullable-datetime-object-in-c-sharp)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
