# Entity Framework Core Computed Column

> 首次發表：2023-07-10

---

計算資料行是一個虛擬資料行，除非資料行標示了PERSISTED，否則，並未實際儲存在資料表中。

![計算資料行是一個虛擬資料行，除非資料行標示了PERSISTED，否則，並未實際儲存在資料表中。](dotblogs-26095bf3-1688983414.jpg)

## Entity

```
public class Test : FullAuditedAggregateRoot<Guid>
{
    public virtual int Total{ get; set; }
    public virtual int Used { get; set; }
    public virtual int Unused  { get; private set; }
}
```

## DbContext

### 虛擬資料行

```
modelBuilder.Entity<Test>()
    .Property(p => p.Unused)
    .HasComputedColumnSql("([Total] - [Used])");
```

實際上不儲存該值，每次要用的時候即時運算出該欄位

### 實值資料行

```
modelBuilder.Entity<Test>()
    .Property(p => p.Unused)
    .HasComputedColumnSql("([Total] - [Used])", stored: true);
```

每次更新時重新計算，並將結果作為值寫入資料庫

## 參照

[Generated Values - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/modeling/generated-properties?tabs=data-annotations#computed-columns)

### 延伸

[ABP.IO WEB應用程式框架 取得關聯資料](ABP.IO-WEB應用程式框架-取得關聯資料-include.md)
