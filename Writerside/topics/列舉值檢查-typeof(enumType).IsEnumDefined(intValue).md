# 列舉值檢查 typeof(enumType).IsEnumDefined(intValue)

> 首次發表：2019-06-13

---

typeof(enumType).IsEnumDefined(intValue)

```

public enum MyEnum
{
    DOG=1,
    CAT,
    Willy
}
void Main()
{
    TestFunction((MyEnum)0);
}
void TestFunction(MyEnum inputEnum)
{
    //會進來不會報錯，API也可以正常Call，監看式這邊inputEnum=0
}
```

所以只好加上一段檢查

```

typeof(MyEnum).IsEnumDefined(inputEnum)
```
