# 入口網站（https://jakeuj.com/）

`jakeuj.com/` 的首頁由這個資料夾產生，Writerside 筆記維持在 `/default.html` 與 `/<topic>.html`。

- `sites.json`：首頁卡片的唯一資料來源。每個專案一筆：
  - `slug`：最終路徑 `https://jakeuj.com/<slug>/`，等於 GitHub repo 名稱（小寫）。
  - `url`：目前實際網址。搬到 jakeuj.com 前填舊子網域，搬完改成 `https://jakeuj.com/<slug>/`。
  - `repo`：GitHub repo 名稱（改名後要跟著改）。
  - `sitemap`：專案根目錄有 `sitemap.xml` 時設 `true`；只有網址在 jakeuj.com 底下時才會寫進根目錄 `robots.txt`。
  - `aliases`（選填）：repo 改名前的舊名稱。會產生 `/<舊名>/` 的 noindex 轉址頁，讓 `jakeuj.github.io/<舊名>/` 這類舊連結導到新網址。
  - `disallow`（選填）：要禁止爬取的子目錄（相對於專案，結尾加 `/`），會寫進根目錄 `robots.txt`；子目錄自己的 robots.txt 無效。
  - 整站不想被搜尋收錄（例如機器翻譯的 `/evennia/`）時，在該站每頁加 `<meta name="robots" content="noindex">`，`sitemap` 與 `disallow` 都不設；被 `disallow` 擋住的頁面，Google 看不到 noindex。
- `build_portal.py`：部署時在 Writerside 輸出目錄執行，產生 `index.html` 與舊名轉址頁、把首頁加進 `sitemap.xml`、把專案 sitemap 與禁止爬取規則加進 `robots.txt`。重複執行結果相同。
- `portal.css`：首頁樣式，建置時內嵌進 `index.html`。
- `assets/`：預先產生的首頁圖片，建置時複製到輸出目錄的 `portal/`，不依賴 Writerside 是否收錄未被文章引用的圖片。

## 作者與結構化資料

`sites.json` 的頂層 `person` 為選填物件，供首頁 JSON-LD 的 `Person` 使用：

```json
{
  "person": {
    "name": "Jakeuj",
    "url": "https://jakeuj.com/",
    "sameAs": ["https://github.com/jakeuj"]
  }
}
```

- 提供物件時，`name` 必須是非空白字串、`url` 必須是有效 HTTPS 絕對網址；不接受帳密或空白字元。
- `sameAs` 選填，必須是 HTTPS 網址陣列；省略或空陣列時不輸出此屬性。只填頁面已公開的作者社群資料。
- 舊資料沒有 `person` 時，沿用 Jakeuj、首頁及現有 GitHub／LinkedIn／YouTube 的預設值，不必修改每筆專案。

首頁以單一 `@graph` 串聯 `WebSite`、`Person`、專案 `ItemList`。`WebSite.publisher` 指向作者，`mainEntity` 指向專案清單。項目依畫面分類與卡片順序產生，只列出網址主機為 `jakeuj.com` 的站；`numberOfItems` 與連續的 `position` 同步計算。這是目錄內容的描述，不代表專案可被索引：Evennia 仍可列在目錄，但不加入 sitemap 或 robots 宣告。

## 首頁圖片

- 頭像：96／192／256px WebP（quality 85、method 6），192px PNG fallback。`sizes` 對應框內實際寬度：手機 78px、768px 以上 174px；保留寬高與 alt，避免載入時跳動。
- 圖示：16／32／48px PNG favicon、180px PNG apple-touch-icon，宣告尺寸與實檔一致。
- 分享圖：`portal/portal-og.png`，1200×630 PNG。只移除原圖完全不透明的 alpha 並無損壓縮，RGB 像素保持相同；文章繼續使用原本 `images/og-image.png`。
- 原始 `Writerside/images/miku.png`、`og-image.png` 及頁首 SVG 不修改。

以上為已提交的二進位資產，正式建置只用 Python 標準函式庫複製，不轉檔、不連網。需要更新素材時可在維護環境以 Pillow 產生：頭像以原圖副本 `thumbnail((size, size), Image.Resampling.BICUBIC)` 縮小，WebP 使用上述參數，PNG 使用 `optimize=True`；分享圖確認 alpha 全為 255 後 `convert("RGB")`，以相同 PNG 參數儲存。Pillow 不屬於建置或測試依賴。

## 本機預覽與檢查

新增專案：repo 不設 Pages 自訂網域，GitHub 會自動放在 `https://jakeuj.com/<repo>/`；在 `sites.json` 加一筆即可。

先在暫存輸出目錄放入線上的 `sitemap.xml`、`robots.txt`，並將 `Writerside/images/` 複製為 `images/`。執行以下命令後，在該目錄以 `python3 -m http.server --bind 127.0.0.1` 預覽；筆記與專案內容沒有複製到預覽目錄，連結驗證應對照正式網址。

```bash
python3 portal/build_portal.py --site <暫存輸出目錄>
python3 portal/build_portal.py --check
python3 -m unittest discover -s portal -p "test_*.py"
```
