# MSSQL 抓半年內的資料

> 首次發表：2022-10-04

---

筆記下

結論

```
SELECT * FROM USERS WHERE DateDiff(MM,[CreationTime],GETDATE()) < 7
```

參考

```
SELECT * FROM USERS WHERE [CreationTime] > DATEADD(MONTH,-6,GETDATE())
```

參照

[SQL日期查詢-SQL查詢今天、昨天、7天內、30天，年 - 程式人生 (796t.com)](https://www.796t.com/content/1543417684.html)
