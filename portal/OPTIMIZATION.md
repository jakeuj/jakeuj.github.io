# 入口首頁優化驗收（2026-11-17）

以 `865f390` 為基準，在 `portal/optimize` worktree 修改；主 checkout 的未提交檔案另存雜湊核對。此次交付為本機驗收與分支 commit，尚未 push／部署。

## 稽核與優先序

| 優先序 | 面向 | 問題與處理 |
| --- | --- | --- |
| High | 效能／SEO | 256px、90,412 bytes 的頭像兼作宣告 16px 的 favicon。改用 responsive WebP、PNG fallback、實際 16／32／48px favicon 與 180px apple icon。 |
| Medium | SEO | JSON-LD 只有 WebSite。補上同一個 graph 的 Person、ItemList，資料來自 sites.json；選填 person 有驗證及舊資料預設值。 |
| Medium | 分享／效能 | OG PNG 為 207,694 bytes。另存首頁專用 1200×630 PNG，移除完全不透明的 alpha，RGB 像素差異為零。 |
| Medium | 部署 | Writerside 不保證打包未被文章引用的新圖片。入口產生器明確複製已提交的 assets，預覽與正式部署走同一段程式。 |
| Low | 無障礙 | 多個卡片的原始碼連結都只叫 GitHub。加入包含專案名稱的 aria-label。 |
| Low | 無障礙 | 卡片點擊區涵蓋整張，但原焦點框只包住標題。焦點框改為涵蓋卡片，跳過導覽明確聚焦 main。 |
| Low | 無障礙 | 未指定主題時，作業系統配色改變會讓按鈕的可存取標籤過期。監聽系統配色變化，且保留使用者的手動選擇。 |

未發現首頁 crawl/index blocker。canonical、首頁非轉址、H1→H2→H3→H4 層級、既有 alt 與內部連結均適合保留。草莓紅、初音青及深淺色 token 完全未改。

保持原有六分類、18 張卡片、最新五篇文章、主題入口與 default.html 入口。大幅改版、卡片圖示／截圖及新內容區塊留待另案。

## 資源大小

使用同一份已提交文章資料，於本機 Chromium、DPR 1、相同 Python HTTP server 測量；回應沒有壓縮。表中以 bytes 計算，並依資源 URL 去重。

| 項目 | 修改前 | 修改後 | 差異 |
| --- | ---: | ---: | ---: |
| HTML | 26,521 | 33,431 | +6,910（主要為結構化資料） |
| 375px 頁面顯示資源，含 HTML／logo／選中的頭像／favicon | 132,781 | 54,755 | −58.76% |
| 768／1280px 頁面顯示資源，含上述項目 | 132,781 | 59,889 | −54.90% |
| OG 分享圖 | 207,694 | 157,769 | −24.04% |
| 所有引用圖片，包含全部 srcset、PNG fallback、所有 icon 與 OG | 313,954 | 297,204 | −5.34% |
| HTML ＋全部引用圖片 | 340,475 | 330,635 | −2.89% |

OG、apple icon、未選中的 srcset 版本與 PNG fallback 不會全部在一般瀏覽時下載，所以上表另外列出最保守的完整引用清單。原 favicon 與頭像網址相同，只在去重清單計算一次。

另以停用快取的 Chromium Resource Timing 記錄實際請求：修改前 `transferSize` 合計 224,393；修改後手機 55,955、平板／桌面 61,089。此模式下原 miku.png 因頭像與 favicon 用途被請求兩次；這組數字保留重複請求及 Resource Timing 的傳輸開銷，不能和去重本體大小混用。

線上原首頁 HTML 為 26,634 bytes，顯示資源去重總量為 132,894，含 OG 為 340,588。線上產物另經 RSS 發布步驟處理，與直接執行舊入口產生器的本機基準相差 113 bytes；上述前後比較採相同建置條件。

## 版面、無障礙與連結

| 寬度 | 淺色 | 深色 | 水平溢出／重疊 | 載入 CLS |
| --- | --- | --- | --- | ---: |
| 375 | 通過 | 通過 | 兩種主題皆無 | 0 |
| 768 | 通過 | 通過 | 兩種主題皆無 | 0 |
| 1280 | 通過 | 通過 | 兩種主題皆無 | 0 |

六組均另存完整頁面及首屏 JPEG。逐組檢查圖片成功解碼、頁首、hero、筆記面板、專案卡片與頁尾；量測頁寬、卡片資訊列及主要區塊的邊界。這是本機未節流的載入觀察，並非真實使用者 Core Web Vitals。

- 目前量測最低一般文字對比：淺色 5.17:1、深色 6.82:1；單元測試另檢查文字與焦點所用配色組合，不需要改色。
- Tab 第一個焦點為跳過導覽，Enter 後 activeElement 為 main。卡片標題的鍵盤焦點框為 3px 初音青、offset 2px，涵蓋整張卡片，原始碼連結仍可獨立聚焦。
- 沒有儲存設定時，系統由淺色切深色，按鈕標籤會同步；手動選淺色後，即使系統改變或重新載入仍維持淺色。localStorage key 沿用 `jakeuj-portal:theme`。
- 由生成 HTML 擷取的 33 個不重複同站 HTTP 連結全部 GET 200，這次不需重試；頁內錨點全數存在。
- JSON-LD 可由 json.loads 解析，18 個專案位置連續、順序與畫面一致；WebSite、Person、ItemList 的 ID 互相連結。
- 根 sitemap 含首頁；不含 `/evennia/` 專案網址。robots 沒有 Evennia 的 Sitemap 或 Disallow，線上該站仍有 noindex。名稱含 evennia 的既有筆記文章仍正常保留。

## 測試證據

入口共 18 項 unittest 通過，另以 `python3 -S` 執行同一套測試，確認不需要 site-packages。209 個預覽成品（含原圖片）連續建置兩次，逐檔 SHA-256 相同。

| Requirement | Evidence |
| --- | --- |
| canonical、非轉址、最新文章與卡片完整、二進位重複建置 | `test_build_is_idempotent_and_complete` |
| 三種 JSON-LD 類型、作者資料與畫面專案一致 | `test_jsonld_links_website_person_and_visible_projects` |
| 排除子網域及相似主機、保留畫面順序、無同站專案時空清單 | `test_jsonld_excludes_other_hosts_and_keeps_visible_order`、`test_jsonld_handles_no_main_host_projects` |
| 舊 JSON 相容、新作者欄位驗證、社群資料選填 | `test_old_sites_json_builds_with_default_person`、`test_rejects_invalid_person`、`test_person_without_social_profiles` |
| 特殊字元可往返且不注入 HTML | `test_jsonld_and_cards_escape_user_text` |
| 複製圖片、PNG／WebP 尺寸、responsive 宣告與 OG metadata | `test_images_are_copied_with_correct_dimensions_and_metadata` |
| 禁止網路與 DNS 連線仍能建置 | `test_build_uses_only_local_inputs` |
| 跳過導覽、標題層級、專案原始碼可存取名稱與 alt | `test_accessible_markup_and_heading_order` |
| 配色文字／焦點對比 | `test_color_tokens_meet_text_and_focus_contrast` |
| Evennia 可見但無 sitemap／robots 宣告 | `test_evennia_stays_visible_without_crawl_or_sitemap_rules` |
| RSS 發布重複執行仍只保留一個 alternate | `test_rss_publication_keeps_one_alternate` |
| 既有資料與轉址保護 | `test_rejects_duplicate_slug`、`test_rejects_main_host_url_not_matching_slug`、`test_only_main_host_sitemaps_go_to_robots`、`test_alias_must_not_overwrite_real_page` |

另通過 publication 的 7 項測試、`npm run pre-deploy`（含 601 篇 Markdown、publication 同步及 XML 檢查），以及入口 README／本報告的 markdownlint。建置與測試未新增 Python 或前端依賴。

## 發布狀態

本輪只在 `portal/optimize` commit，不 push。worktree 與本機預覽保留供審閱。確認發布後才快轉推送遠端 master，等待該 commit 的 build、test、deploy、publish-indexes 四個 job 成功，再用 curl 核對線上首頁、新圖片、canonical、JSON-LD 及連結，最後停止預覽並移除 worktree。
