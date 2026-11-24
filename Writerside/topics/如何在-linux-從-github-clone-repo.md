# 如何在 linux 從 github clone repo

> 首次發表：2023-10-04

---

筆記在 GCE ubuntu 使用 ssh 方式從 github 取得專案

結論

```
ssh-keygen
```

![結論](dotblogs-67d1de2f-1696402201.jpg)

把產出的 `/home/jake/.ssh/id_rsa.pub` 內容貼到 GITHUB [Add new SSH key (github.com)](https://github.com/settings/ssh/new)

![把產出的 /home/jake/.ssh/idrsa.pub 內容貼到 GITHUB Add new SSH key (github.com)](dotblogs-67d1de2f-1696402458.jpg)

就可以直接 gti clone 了

`git clone git@github.com:jakeuj/demo.git`

![git clone git@github.com:jakeuj/demo.git](dotblogs-67d1de2f-1696402559.jpg)

參照

[【Git教學】手把手 Github SSH 連線設定教學 (Windows/Mac) - Max行銷誌 (maxlist.xyz)](https://www.maxlist.xyz/2022/12/22/github-ssh-setting/)

[Git 踩坑紀錄（二）git clone with SSH keys 或 HTTPS 設定步驟 | by TSENG FU CHUN / 豆腐 | Medium](https://tsengbatty.medium.com/git-%E8%B8%A9%E5%9D%91%E7%B4%80%E9%8C%84-%E4%BA%8C-git-clone-with-ssh-keys-%E6%88%96-https-%E8%A8%AD%E5%AE%9A%E6%AD%A5%E9%A9%9F-bdb721bd7cf2)
{ignore-vars="true"}

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- GCP
- Git
- Github
- Linux

- 回首頁

---

*本文章從點部落遷移至 Writerside*
