# decimal 輸出小數點指定位數

> 首次發表：2023-02-02

---

筆記一下數字指定輸出格式

![筆記一下數字指定輸出格式](dotblogs-657848f4-1675329285.jpg)

結論

```
decimal? decimalVar = 0.5m;

decimalVar.GetValueOrDefault().ToString("#.##").Dump();

decimalVar.GetValueOrDefault().ToString("0.##").Dump();

decimalVar.GetValueOrDefault().ToString("0.00").Dump();
```

參照

[c# - How do I display a decimal value to 2 decimal places? - Stack Overflow](https://stackoverflow.com/questions/164926/how-do-i-display-a-decimal-value-to-2-decimal-places)
