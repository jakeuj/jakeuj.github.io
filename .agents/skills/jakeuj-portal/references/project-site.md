# 專案站：新增、搬入、改名、下線、恢復

每個段落都涉及兩邊：專案 repo（`jakeuj/<repo>`）和本 repo 的 `portal/sites.json`。Cloudflare 的 DNS 與 Bulk Redirect 操作照 cloudflare 技能的 `references/jakeuj-site-layout.md`。

## 新增專案站

1. 專案 repo 的 Pages：
   - 開 Pages、不設自訂網域、不放 `CNAME` 檔。Actions 部署用 `gh api -X POST repos/jakeuj/<repo>/pages -f build_type=workflow`。
   - repo 名稱就是網址 slug，用小寫短名。
2. 專案內容要能在 `/<repo>/` 底下運作：
   - 資源用相對路徑或框架的 base 設定（Vite `base`、Astro `site` + `base`、Jekyll `baseurl`、Sphinx `html_baseurl`）。開頭是 `/` 的絕對路徑會指到 `jakeuj.com` 根目錄。
   - Markdown 轉出的根目錄連結也要補 base；Astro 曾用 rehype plugin 處理。
   - canonical、`og:url`、sitemap `<loc>` 寫完整的 `https://jakeuj.com/<repo>/…`。
   - 子目錄的 `robots.txt` 無效，不放。要擋的子目錄寫進 `sites.json` 的 `disallow`。
   - PWA：註冊 `./sw.js`、scope `./`；manifest 的 `id`、`start_url`、`scope`、icons 用相對路徑；Workbox `navigateFallbackAllowlist` 限定在 `/<repo>/`。
   - localStorage、IndexedDB 的 key 加專案前綴，因為所有專案共用一個 origin。
   - 頁尾放回 `https://jakeuj.com/` 的連結。
3. repo 設定：`gh api -X PATCH repos/jakeuj/<repo> -f homepage=https://jakeuj.com/<repo>/`。
4. 本 repo：在 `sites.json` 加一筆，欄位照 `portal/README.md`。
   - 專案有 `sitemap.xml` 才設 `sitemap: true`。
   - 機器翻譯、鏡像這類不想被收錄的站：專案每頁加 `<meta name="robots" content="noindex">`，`sitemap`、`disallow` 都不設。
5. 驗證：`gh api repos/jakeuj/<repo>/pages` 的 `cname` 是 null、`html_url` 是 `https://jakeuj.com/<repo>/`；新網址和它引用的同源 JS、CSS、圖片都回 200。

## 從舊子網域搬入

照「新增專案站」準備好，再依序切換，避免中間出現 404：

1. 在 Cloudflare 加 Bulk Redirect 項目 `<host>/` → `https://jakeuj.com/<repo>/`。DNS 還沒開代理前，這筆不會生效。
2. 清掉專案的自訂網域 `gh api -X PUT repos/jakeuj/<repo>/pages -F cname=null`，刪掉 repo 裡的 `CNAME` 檔，push 部署。
3. 確認新網址回 200，再把舊主機的 DNS 記錄改成 proxied，301 才開始生效。
4. 舊主機裝過 PWA 的話，舊 service worker 會離線回應，301 到不了瀏覽器。這種主機改用 `infra/cloudflare/legacy-pwa-worker.mjs` 的 kill-switch Worker，不放進 Bulk Redirect 清單。
5. 更新 `sites.json` 的 `url`，再用 `git grep` 找 Writerside 筆記和 `~/.agents/skills` 裡寫死的舊網址一起改。

## repo 改名

- `gh repo rename <new> -R jakeuj/<old>`，再更新本機 clone 的 remote。
- 舊 Pages 路徑 `jakeuj.com/<old>/` 會變成 404。在 `sites.json` 改 `slug`、`url`、`repo`，並把舊名照原本的大小寫加進 `aliases`，建置時會產生 noindex 轉址頁。
- 一併更新：repo homepage、專案裡的 base 與 canonical、workflow 中寫死的 repo 名稱、目標指向舊路徑的 Bulk Redirect 項目。

## 下線

刪除前先向使用者確認。

- 刪掉 `sites.json` 那一筆。
- 停用 Pages：`gh api -X DELETE repos/jakeuj/<repo>/pages`。回 422「not allowed」表示 Pages 來源是 `gh-pages` 分支，要先刪分支才能停用。
- 舊子網域：保留 301 指到其他頁面，或刪除 Bulk Redirect 項目與 DNS 記錄。
- 用 `git grep` 找還連到這個站的筆記。

## 恢復已下線的站

- 重新開 Pages（見「新增專案站」），push 一個 commit 或 `gh workflow run <workflow 檔名> -R jakeuj/<repo>` 觸發部署。
- 改掉程式裡寫死的舊網址。例如 Sphinx 的 `html_baseurl`；`sphinx.ext.githubpages` 會依 `html_baseurl` 寫出 `CNAME` 檔，Actions 部署用不到，可以拿掉。
- 在 `sites.json` 加回卡片。
- 舊子網域要轉址時，先加 Bulk Redirect 項目，再建 proxied CNAME → `jakeuj.github.io`。
