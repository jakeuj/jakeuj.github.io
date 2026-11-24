# C# Discord Bot

> 首次發表：2023-03-20

---

簡單記錄一下 DC 私聊機器人

![簡單記錄一下 DC 私聊機器人](dotblogs-621a0c42-1679278254.jpg)

Rider

結論

```
using Discord;
using Discord.WebSocket;

var client = new DiscordSocketClient();

client.Log += (message) =>
{
    Console.WriteLine(message);
    return Task.CompletedTask;
};

client.Ready += () =>
{
    Console.WriteLine("Bot is ready!");
    return Task.CompletedTask;
};

client.MessageReceived += async (message) =>
{
    Console.WriteLine(message);
    // Ignore messages sent by the bot itself
    if (message.Author.Id == client.CurrentUser.Id)
        return;

    // Respond to messages that contain "hello"
    if (message.Content.Contains("hello"))
    {
        await message.Channel.SendMessageAsync("Hi there!");
    }
};

await client.LoginAsync(TokenType.Bot, "YourTokenXxxxxxxx");
await client.StartAsync();
await Task.Delay(-1);
```

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Discord

- 回首頁

---

*本文章從點部落遷移至 Writerside*
