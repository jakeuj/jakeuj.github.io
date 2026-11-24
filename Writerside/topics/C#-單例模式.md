# C# 單例模式

> 首次發表：2017-10-30

---

C# 單例模式

```

public sealed class Singleton
{
    public static Singleton Instance { get; private set; } = null;

    static Singleton()
    {
        Instance = new Singleton();
    }

    private Singleton()
    {
    }
}
```

Lazy (.Net 4.0 +)

```

public sealed class Singleton
{
    private static readonly Lazy<Singleton> lazy = new Lazy<Singleton>();
    private Singleton() { }
    public static Singleton Instance => lazy.Value;
}
```

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
