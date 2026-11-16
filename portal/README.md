# 入口網站（https://jakeuj.com/）

`jakeuj.com/` 的首頁由這個資料夾產生，Writerside 筆記維持在 `/default.html` 與 `/<topic>.html`。

- `sites.json`：首頁卡片的唯一資料來源。每個專案一筆：
  - `slug`：最終路徑 `https://jakeuj.com/<slug>/`，等於 GitHub repo 名稱（小寫）。
  - `url`：目前實際網址。搬到 jakeuj.com 前填舊子網域，搬完改成 `https://jakeuj.com/<slug>/`。
  - `repo`：GitHub repo 名稱（改名後要跟著改）。
  - `sitemap`：專案根目錄有 `sitemap.xml` 時設 `true`；只有網址在 jakeuj.com 底下時才會寫進根目錄 `robots.txt`。
  - `aliases`（選填）：repo 改名前的舊名稱。會產生 `/<舊名>/` 的 noindex 轉址頁，讓 `jakeuj.github.io/<舊名>/` 這類舊連結導到新網址。
  - `disallow`（選填）：要禁止爬取的子目錄（相對於專案，結尾加 `/`），會寫進根目錄 `robots.txt`；子目錄自己的 robots.txt 無效。
- `build_portal.py`：部署時在 Writerside 輸出目錄執行，產生 `index.html` 與舊名轉址頁、把首頁加進 `sitemap.xml`、把專案 sitemap 與禁止爬取規則加進 `robots.txt`。重複執行結果相同。
- `portal.css`：首頁樣式，建置時內嵌進 `index.html`。

新增專案：repo 不設 Pages 自訂網域，GitHub 會自動放在 `https://jakeuj.com/<repo>/`；在 `sites.json` 加一筆即可。

本機檢查：

```bash
python3 portal/build_portal.py --check
python3 -m unittest discover -s portal -p "test_*.py"
```
