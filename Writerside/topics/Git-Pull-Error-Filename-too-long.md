# Git Pull Error Filename too long

> 首次發表：2021-07-27

---

最近從 Github 拉一些參考專案遇到兩次拉不下來的情況

反正是參考用的直接在網頁上看也是可以就沒特別注意

今天隨手查了一下順手作個紀錄怎麼解決

結論

系統管理員 終端機> git config --system core.longpaths true

參照：https://dotblogs.com.tw/clark/2016/01/11/124311
