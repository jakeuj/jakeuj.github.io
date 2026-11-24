# Azure App Service Git Authentication failed for

> 首次發表：2021-02-23

---

心血來潮用了一下 Azure App Service 的 Git 部屬

結果一直登入失敗，筆記下最後成功

Git 格式 `git clone https://{UserName}@{SiteName}.scm.azurewebsites.net/{SiteName}.git`

其中原本複製的會有 :443 我這邊是拿掉

登入名稱打在原本網址前面加 @ 的前面

網站上會長成 `xxxx\$xxxx` 只要打\的後面那串

特殊符號可能要先編碼

`UrlEncode $ => %24`

最後範例

`git clone https://%24jakeuj@jakeuj.scm.azurewebsites.net/jakeuj.git`

P.S. FTPS

- 自動生成帳號 `xxxx\$xxxx` 與 `$xxxx` 都可以
- 自訂帳號說明一定要 `xxxx\$xxxx`
- 如果不行可能是防火牆鎖了 Port
  我因此撞牆一下午，請改用手機分享網路試試
