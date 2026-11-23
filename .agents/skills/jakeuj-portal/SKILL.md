---
name: jakeuj-portal
description: jakeuj.com 入口首頁與 /<repo>/ 專案站。修改 portal/（sites.json 卡片、分類、作者資料、版面、圖片）；把 GitHub Pages 專案加進 jakeuj.com、改名、下線或恢復舊子網域；首頁建置、部署或線上驗證失敗時使用。寫 Writerside 文章用 writerside 技能。
---

# jakeuj.com 首頁與專案站

## 網站模型

本 repo 是 GitHub 使用者站 `jakeuj/jakeuj.github.io`（原名 `jakeuj/writerside`）。自訂網域 `jakeuj.com` 設在 Settings → Pages；用 Actions 部署時 GitHub 不看 `CNAME` 檔。同一個網域放三種內容：

- `/`：入口首頁，部署時由 `portal/` 產生，不是 Writerside 頁面。
- `/default.html`、`/<topic>.html`：Writerside 筆記。
- `/<repo>/`：其他 repo 的 Pages 專案站。專案 repo 不設自訂網域，GitHub 自動把它掛在使用者站網域底下，所以新專案不開子網域、不改 DNS。

三個會咬人的特性：

- Pages 路徑區分大小寫，repo 改名後 GitHub 只轉 repo 網址，不轉 Pages 路徑。
- 所有專案共用 `https://jakeuj.com` 這個 origin：service worker scope、manifest、localStorage key 都要限定在 `/<repo>/` 內。
- 舊子網域的 301 在 Cloudflare 邊緣處理。DNS、Bulk Redirect、Worker 的做法在 cloudflare 技能的 `references/jakeuj-site-layout.md`。

## 檔案

- `portal/README.md`：`sites.json` 欄位、`person`、首頁圖片、本機預覽方式的唯一說明。改到欄位或建置行為時同步改它。
- `portal/build_portal.py`：只用 Python 標準函式庫、離線、跑兩次結果相同。產生 `index.html`、舊 repo 名稱的 noindex 轉址頁，並把首頁加進 `sitemap.xml`、把專案 sitemap 與 `Disallow` 加進 `robots.txt`。
- `portal/portal.css` 建置時內嵌；`portal/assets/` 是預先產生的二進位圖片，建置只複製。
- `portal/test_build_portal.py`：所有行為都有測試，改程式就補測試。
- `.github/workflows/deploy.yml`：「Check portal data and tests」和「Build portal home page」兩步，之後驗證首頁 canonical 是 `https://jakeuj.com/`、沒有 meta refresh、`sitemap.xml` 有根網址、OG 圖存在。

## 工作規則

- **另開 worktree**：主 checkout 常有使用者還沒 commit 的筆記修改。每次都從 `origin/master` 開 worktree，例如 `git worktree add ../writerside-<task> -b <branch> origin/master`，做完移除 worktree 和分支。
- **push 就是上線**：push 到 master 會觸發部署，條件是 `deploy.yml` 的 paths 白名單（`portal/**` 但不含 `portal/**/*.md`、`Writerside/**`、`data/posts.json` 等）。任務沒說要上線時，停在分支 commit，把摘要交給使用者。
- **共用圖片不覆蓋**：`Writerside/images/miku.png` 也被 `Writerside/cfg/buildprofiles.xml` 使用。首頁要的新圖片用新檔名放進 `portal/assets/`。
- **相容性**：`sites.json` 只新增選填欄位，在 `load_sites()` 驗證並寫進 `portal/README.md`，舊資料不改也要能建置。

## 流程

- **改首頁**（卡片、分類、作者資料、版面、圖片）：讀 `portal/README.md` 和要改的函式與測試 → 修改 → 跑本機檢查 → 動到畫面時用 README 的暫存目錄方式建置預覽，375、768、1280 三種寬度各看淺色和深色。
- **新增、搬入、改名、下線、恢復專案站**：讀 [project-site.md](references/project-site.md)，照其中對應段落做完專案 repo 和本 repo 兩邊。

## 驗證

本機：

```bash
python3 portal/build_portal.py --check
python3 -m unittest discover -s portal -p "test_*.py"
```

上線後：

- `gh run watch <run-id> -R jakeuj/jakeuj.github.io --exit-status` 的 build、test、deploy、publish-indexes 四個 job 都成功。
- `https://jakeuj.com/` 回 200，canonical 是 `https://jakeuj.com/`，這次動到的卡片連結都回 200。
- `robots.txt` 對每個 `sitemap: true` 的站各有一行 `Sitemap:`，`sitemap.xml` 有 `<loc>https://jakeuj.com/</loc>`。
- 部署剛完成的幾分鐘內，GitHub Pages 偶爾回 503，隔一下重試。
