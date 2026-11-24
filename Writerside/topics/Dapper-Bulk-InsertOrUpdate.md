# Dapper Bulk InsertOrUpdate

> 首次發表：2019-09-29

---

Dapper 大量 插入或更新

就丟List<實體>進去，有Id就更新，否則插入

PM > Install-Package Z.Dapper.Plus

```
//Merge a single order.
connection.BulkMerge(order);

//Merge multiple orders.
connection.BulkMerge(order1, order2, order3);
```

<https://dapper-plus.net/bulk-merge>
