# Linq 加總兩個欄位

> 首次發表：2021-07-19

---

SQL SUM(A), SUM(B) FROM C

在 Linq 一時之間竟然打不出來..

趕緊筆記一下

直接結論

```
Products
 .GroupBy(p => 1)
 .Select(p => new {
  TotalSid = p.Sum(x => x.SupplierID),
  TotalCid = p.Sum(x => x.CategoryID)
 })
```
