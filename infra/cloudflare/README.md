# Cloudflare：舊網址轉址

2026-11-16 起，所有專案站都放在 `https://jakeuj.com/<slug>/`，舊子網域與 `blog.jakeuj.com` 由 Cloudflare 永久 301。轉址要長期保留（Google 建議至少一年），不要刪。

帳號 `a91315bdbfb8c6c1d3b8747479a94e44`、zone `jakeuj.com`（`6a0f6ddf50c541f42994fd0dad53f162`）、Free 方案。

## 一般舊主機：Bulk Redirects

- Redirect list `jakeuj_legacy_hosts`（帳號層級）。
- 帳號 ruleset `http_request_redirect` 的一條規則：`http.request.full_uri in $jakeuj_legacy_hosts`。
- 每個舊主機一筆：source `<host>/`（不寫 scheme，http/https 都比對）→ `https://jakeuj.com/<slug>/`，開 `subpath_matching`、`preserve_path_suffix`、`preserve_query_string`，301。
- blog：`blog.jakeuj.com/` → `https://jakeuj.com/`（不保留路徑），另有 `wow-forever-professions`、`architect-pc-builder` 的專案別名（有、無尾斜線各一筆）。路徑最具體的那筆優先。
- 舊主機的 DNS 記錄保留原本的 CNAME `jakeuj.github.io`，只改成 proxied；轉址在 Cloudflare 邊緣完成，不會回源。

## 有 service worker 的舊主機：Worker

舊訪客瀏覽器裡的 service worker 會直接從快取開舊版，碰不到 301。這些主機改由 Worker `jakeuj-legacy-pwa`（原始碼 `legacy-pwa-worker.mjs`）處理：

- 舊的 `/sw.js` 回傳會自我解除註冊並重新載入的 service worker；
- 其他路徑 301 到新網址。

目前：`bahamut-markdown-converter.jakeuj.com`、`bandit.jakeuj.com`。這些主機**不能**同時放進 Bulk Redirect 清單（Bulk Redirects 比 Workers 先執行，會連 `/sw.js` 一起轉走）。路由為 zone Worker route `<host>/*`；workers.dev 網址已關閉。

更新 Worker：用 Cloudflare API `PUT /accounts/{account}/workers/scripts/jakeuj-legacy-pwa`（module 上傳），或 `wrangler deploy`。

## 其他

- apex `jakeuj.com` 是 DNS-only CNAME → `jakeuj.github.io`（Cloudflare CNAME flattening），不受 GitHub Pages IP 變動影響。
- `www.jakeuj.com` 是 proxied CNAME → `jakeuj.github.io`，301 到 apex 由 GitHub Pages 自動處理。
- 新專案不設 Pages 自訂網域，也不用新增 DNS 記錄。
