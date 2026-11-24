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
