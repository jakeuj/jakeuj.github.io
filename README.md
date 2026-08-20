# Jake's Hexo Blog

這是 [Jake's Hexo Blog](https://jakeuj.github.io/) 的 GitHub Pages repository，內容由 Hexo 3.8.0 產生，主要記錄 Hexo、VS Code 與 Markdown 相關筆記。

## Repository 內容

這個 repository 保存可直接部署的靜態網站，而不是 Hexo 的原始文章與設定檔。

- `index.html`：網站首頁
- `2019/`：依日期整理的文章頁面
- `categories/`、`tags/`、`archives/`：分類、標籤與文章封存頁面
- `css/`、`js/`、`fancybox/`：網站樣式、腳本與圖片瀏覽元件

## 本機預覽

在 repository 根目錄啟動靜態檔案伺服器：

```bash
python3 -m http.server 8000
```

接著開啟 [http://localhost:8000](http://localhost:8000)。

## 更新與部署

更新網站時，請先在 Hexo 原始專案重新產生靜態檔案，再將產出同步到這個 repository。推送至 GitHub Pages 發布分支（目前為 `master`）後，網站內容便會更新。
