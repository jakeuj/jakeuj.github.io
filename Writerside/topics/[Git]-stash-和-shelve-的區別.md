# [Git] stash 和 shelve 的區別

> 首次發表：2023-12-25

---

Jetbrains IDE 內建 stash 和 shelve

## 結論

我不知道差在哪

- stash
  - 會把改的檔案還原回未變更之前的檔案，同時將差異的部分暫存起來
  - 之後可以再 unstash，把檔案在從原始版本變成剛剛修改後的內容
- shelve
  - 會把改的檔案還原回未變更之前的檔案，同時將差異的部分暫存起來
  - 之後可以再 unshelve，把檔案在從原始版本變成剛剛修改後的內容

## Shelve

    1. Shelve

![1. Shelve](dotblogs-557af885-1703499873.jpg)

    2. 檔案會被還原

![2. 檔案會被還原](dotblogs-557af885-1703499903.jpg)

    3. UnShelve

![3. UnShelve](dotblogs-557af885-1703499940.jpg)

    4. 檔案會被復原

![4. 檔案會被復原](dotblogs-557af885-1703499963.jpg)

    5. 這些操作都不會在版控上留下紀錄

## Stash

1. 修改 appsettings.secrets.json

![修改 appsettings.secrets.json](dotblogs-557af885-1703498250.jpg)

    2. 選擇 git stash changes

![2. 選擇 git stash changes](dotblogs-557af885-1703498295.jpg)

    3. 輸入 stash 的訊息並建立該 stash

![3. 輸入 stash 的訊息並建立該 stash](dotblogs-557af885-1703497497.jpg)

    4. appsettings.secrets.json 已被還原回未更改的內容

![4. appsettings.secrets.json 已被還原回未更改的內容](dotblogs-557af885-1703497536.jpg)

    5. 選擇 git unstash changes

![5. 選擇 git unstash changes](dotblogs-557af885-1703497692.jpg)

    6. 選擇欲還原的 stash 並 Apply Stash

![6. 選擇欲還原的 stash 並 Apply Stash](dotblogs-557af885-1703497723.jpg)

    7. appsettings.secrets.json 會再變成該 stash 的內容

![7. appsettings.secrets.json 會再變成該 stash 的內容](dotblogs-557af885-1703497761.jpg)

    8. 這些操作都不會在版控上留下紀錄

### 參照

[idea中好用的git shelve changes和stash changes-CSDN博客](https://blog.csdn.net/eclipse1024/article/details/116352777)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Git
- JetBrains

- 回首頁

---

*本文章從點部落遷移至 Writerside*
