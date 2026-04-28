# ARCHITECTURE — 嘉義國本學堂系統設計文件（SDD）

> 本文件是專案的單一架構真相來源（SDD）。任何系統層的變動都應同步更新本文件。
> 任務操作流程請見 [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md)。

## 1. 專案基本資訊

- **專案名稱**：嘉義國本學堂
- **Repo**：[ahnchen1983/agrischlchiayi](https://github.com/ahnchen1983/agrischlchiayi)
- **部署網址**：https://ahnchen1983.github.io/agrischlchiayi/
- **負責人**：ahnchen
- **本文件最後更新**：2026-04-28

## 2. 專案願景

將嘉義縣政府農業處「國本學堂」與延伸在地農業資料，整理為一個：

- **公開可讀**：任何人都能直接瀏覽學習
- **開源可編修**：以 Markdown 為主體，方便協作與版本管理
- **可持續成長**：隨著課程、案例、交流持續擴充

讓新農、返鄉青年、學生與農場經營者，有一個結構清楚、可搜尋、可視覺化探索的農業知識入口。

### 目標使用者

新農與返鄉青年・農業課程學員・學生與研究者・農場經營者與農企業主。

## 3. 系統架構總覽

### 3.1 高階資料流

```
knowledge/  (Markdown SSOT)
   │
   ├─ scripts/core/sync.sh                  → src/content/zh-TW/  (Astro 投影層)
   ├─ scripts/core/generate-api.js          → public/api/articles.json + stats.json
   ├─ scripts/core/build-search-index.mjs   → public/api/search-minisearch.json
   │
   ▼
Astro Content Collections
   │
   ▼
src/pages/ + src/components/  (SSG 渲染)
   │
   ▼
dist/  (靜態檔案)
   │
   ▼
GitHub Pages (子路徑 /agrischlchiayi)
```

### 3.2 技術選型

| 領域 | 選用 | 用途 |
|---|---|---|
| 框架 | Astro 6 | 靜態網站生成，零 JS by default |
| UI | `.astro` 元件 + Tailwind | 全部元件皆為 `.astro`，無 React/TSX |
| 視覺化 | D3.js（force-directed） | 知識圖譜頁面 |
| 搜尋 | MiniSearch（CJK bigram） | 客戶端全文索引，支援中文分詞 |
| 內容 | Markdown + YAML frontmatter | SSOT 為 `knowledge/` |
| 建置腳本 | Node.js / bash / Python | `scripts/core/` 與 `scripts/tools/` |
| Hooks | Husky + Python | 去識別化檢查、frontmatter 驗證 |
| 部署 | GitHub Pages | 子路徑部署 `/agrischlchiayi` |

### 3.3 Base URL 與 Routing 規範

部署於 GitHub Pages 子路徑，`astro.config.mjs` 設定：

```js
base: '/agrischlchiayi'
```

因此撰寫 `.astro` 與相關腳本時：

- **`.astro` 內部連結與資源**：使用 `import.meta.env.BASE_URL`
- **inline script**：透過 `window.__BASE__` 或 Astro 注入變數取得 base
- **避免**直接寫死 `href="/..."` 或 `src="/..."`
- **`generate-api.js`**：BASE_URL 已硬編碼為 `https://ahnchen1983.github.io/agrischlchiayi`，更換網域時需同步調整

## 4. 內容管線（Content Pipeline）

### 4.1 SSOT 鐵律

`knowledge/` 是內容唯一真相來源，`src/content/zh-TW/` 為 build 期產物，由 `sync.sh` 重建：

```
編輯內容 ──► knowledge/*.md ──► npm run sync ──► src/content/zh-TW/ ──► npm run build ──► dist/
```

`sync.sh` 會 `rm -rf src/content/zh-TW` 後從 `knowledge/` 完整重建。**直接修改 `src/content/` 會在下一次 sync 被覆寫**。

### 4.2 知識分類（13 個目錄）

10 個主分類 + 3 個索引/路徑類：

| # | 目錄 | 中文 | 類型 |
|---|---|---|---|
| 1 | `Agri-Basics/` | 農業基礎入門 | 主分類 |
| 2 | `Agri-Advanced/` | 農業進階實務 | 主分類 |
| 3 | `Farm-Management/` | 農場經營管理 | 主分類 |
| 4 | `Crop-Production/` | 作物生產技術 | 主分類 |
| 5 | `Facility-Farming/` | 設施農業 | 主分類 |
| 6 | `Smart-Farming/` | 智慧農業 | 主分類 |
| 7 | `Agri-Marketing/` | 農產品銷售 | 主分類 |
| 8 | `Grants-Planning/` | 計畫撰寫補助 | 主分類 |
| 9 | `Field-Visits/` | 場域交流觀摩 | 主分類 |
| 10 | `Livestock-Health/` | 畜牧健康 | 主分類 |
| 11 | `Crop-Index/` | 作物索引 | 索引（規劃中） |
| 12 | `Tech-Index/` | 技術索引 | 索引（規劃中） |
| 13 | `Learning-Paths/` | 學習路徑 | 路徑（規劃中） |

詳細分類定義與內容缺口分析見 [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md)。

### 4.3 Frontmatter Schema

每篇 `.md` 必須包含以下欄位（詳見 [../CONTRIBUTING.md](../CONTRIBUTING.md)）：

```yaml
---
title: '文章標題'
description: '一句話摘要'
date: 2026-04-04
tags: [國本學堂, 相關標籤]
subcategory: '子分類名稱'
level: '初階'        # 初階 / 進階 / 卓越
crop: ['番茄']       # 選填
tech: ['設施農業']   # 選填
source: '資料來源'
status: 'published'  # draft / published / archived
---
```

驗證腳本：[scripts/core/test-frontmatter.mjs](../scripts/core/test-frontmatter.mjs)

## 5. 目錄結構

### 5.1 專案頂層

```
agrischlchiayi/
├── knowledge/          # 內容 SSOT（13 個分類目錄）
├── src/                # Astro 應用程式碼
├── scripts/            # 建置與工具腳本
├── public/             # 靜態資源 + 建置後 API JSON
├── docs/               # 本資料夾（架構與流程文件）
├── data/               # YAML/JSON 資料檔
├── i18n/               # 多語系字串
├── plugins/            # 自訂 remark/rehype plugins
├── cli/                # 獨立 CLI 模組（與站點建置解耦）
├── reports/            # 自動產出的分析報告
├── astro.config.mjs
├── package.json
└── .husky/             # Git hooks（pre-commit + commit-msg）
```

### 5.2 `src/` 內部

| 子目錄 | 職責 |
|---|---|
| `src/pages/` | 路由與頁面（見 §6） |
| `src/components/` | 可重用 UI 元件，全部為 `.astro`（共 16 個） |
| `src/layouts/` | `Layout.astro`（唯一全站佈局） |
| `src/templates/` | 較大型頁面模板（如 `about.template.astro`），由 `src/pages/` 引用 |
| `src/content/zh-TW/` | Astro 內容投影層（由 `sync.sh` 從 `knowledge/` 產生，不要直接編輯） |
| `src/lib/` | 共用模組（如 `commits.ts`） |
| `src/utils/` | 工具函式（如 `getLangSwitchPath.ts`） |
| `src/i18n/` | 語言字串檔（目前僅 zh-TW 啟用） |

### 5.3 `scripts/` 內部

| 子目錄 | 用途 |
|---|---|
| `scripts/core/` | 建置管線核心腳本（7 支，見 §7） |
| `scripts/tools/` | 維運工具（去識別化、wikilink 驗證、術語審計、品質掃描等） |
| `scripts/utils/` | 共用工具函式 |
| `scripts/deprecated/` | 已棄用腳本（保留作參考） |

## 6. 頁面與路由地圖

### 6.1 靜態路由

| 路由 | 檔案 | 用途 |
|---|---|---|
| `/` | [src/pages/index.astro](../src/pages/index.astro) | 首頁 |
| `/about` | [src/pages/about.astro](../src/pages/about.astro) | 專案介紹 |
| `/contribute` | [src/pages/contribute.astro](../src/pages/contribute.astro) | 貢獻指南入口 |
| `/data` | [src/pages/data.astro](../src/pages/data.astro) | 資料視覺化 |
| `/resources` | [src/pages/resources.astro](../src/pages/resources.astro) | 外部資源連結 |
| `/changelog` | [src/pages/changelog.astro](../src/pages/changelog.astro) | 更新紀錄 |
| `/graph` | [src/pages/graph.astro](../src/pages/graph.astro) | 知識圖譜（D3.js force-directed） |
| `/404` | [src/pages/404.astro](../src/pages/404.astro) | 404 頁面 |

### 6.2 動態路由

| 路由 | 檔案 | 用途 |
|---|---|---|
| `/[category]/` | `src/pages/[category]/index.astro` | 分類首頁，列出該分類所有文章 |
| `/[category]/[slug]/` | `src/pages/[category]/[slug].astro` | 文章頁 |
| `/og/[category]/[slug]` | `src/pages/og/[category]/[slug].astro` | 動態 Open Graph 圖片 |

### 6.3 API / Feed

| 路由 | 檔案 | 用途 |
|---|---|---|
| `/api/search-index.json` | [src/pages/api/search-index.json.ts](../src/pages/api/search-index.json.ts) | 搜尋索引運行時端點 |
| `/feed.xml` | [src/pages/feed.xml.ts](../src/pages/feed.xml.ts) | RSS Feed |
| `/rss.xml` | [src/pages/rss.xml.ts](../src/pages/rss.xml.ts) | RSS Feed（別名） |

### 6.4 公開 JSON API（build 期產出）

| 路徑 | 產生腳本 | 用途 |
|---|---|---|
| `public/api/articles.json` | `generate-api.js` | 全文章 metadata + readingTime |
| `public/api/stats.json` | `generate-api.js` | 分類計數、熱門 tags |
| `public/api/search-minisearch.json` | `build-search-index.mjs` | MiniSearch 序列化索引 |

## 7. 建置流程

### 7.1 npm scripts（package.json）

| 指令 | 動作 |
|---|---|
| `npm run dev` | astro dev（本地伺服器，預設 http://localhost:4321/agrischlchiayi/） |
| `npm run sync` | bash `scripts/core/sync.sh`（重建 `src/content/zh-TW/`） |
| `npm run sync:build` | sync + astro build |
| `npm run prebuild` | `generate-api.js` + `build-search-index.mjs`（自動於 build 前觸發） |
| `npm run build` | astro build → `dist/` |
| `npm run postbuild` | `post-build-check.mjs`（smoke test） |
| `npm run preview` | astro preview（檢視已建置的 `dist/`） |
| `npm test` | `test-frontmatter.mjs`（驗證 YAML frontmatter） |
| `npm run test:ci` | `test-frontmatter.mjs --ci`（只檢查 git diff 變動檔） |
| `npm run check-images` | `check-images.mjs`（檢查圖片參考） |
| `npm run check-links` | `check-links.sh`（驗證內部連結與 wikilinks） |
| `npm run format::check` / `format::write` | prettier |
| `npm run prepare` | husky（git hooks 安裝） |

### 7.2 `scripts/core/` 7 支核心腳本

| 腳本 | 工作 |
|---|---|
| [sync.sh](../scripts/core/sync.sh) | 從 `knowledge/` 重建 `src/content/zh-TW/`，呼叫 frontmatter 修復、執行圖片健檢 |
| [generate-api.js](../scripts/core/generate-api.js) | 解析 `knowledge/*.md` → `articles.json` + `stats.json`（**直讀 knowledge/，不經 sync**） |
| [build-search-index.mjs](../scripts/core/build-search-index.mjs) | CJK bigram + 拉丁分詞 → `search-minisearch.json` |
| [test-frontmatter.mjs](../scripts/core/test-frontmatter.mjs) | YAML 驗證；支援 `--ci`（只檢查 diff）、`--staged`（pre-commit 用） |
| [post-build-check.mjs](../scripts/core/post-build-check.mjs) | smoke test：`dist/` 至少 20 個 HTML、每分類至少 1 篇 |
| [generate-dashboard-data.js](../scripts/core/generate-dashboard-data.js) | Dashboard 用統計資料 |
| [generate-map-markers.js](../scripts/core/generate-map-markers.js) | Map 頁面標記資料 |

## 8. 部署流程與 Git Hooks

### 8.1 GitHub Actions 工作流

| Workflow | 觸發 | 用途 |
|---|---|---|
| [deploy.yml](../.github/workflows/deploy.yml) | push to `main` | 建置並部署到 GitHub Pages |
| [pr-review.yml](../.github/workflows/pr-review.yml) | PR | 自動 PR 審查 |
| [translation-check.yml](../.github/workflows/translation-check.yml) | PR | 翻譯一致性檢查 |

### 8.2 部署步驟（deploy.yml）

```
1. checkout (fetch-depth: 0)
2. setup-node@v4 (Node 22)
3. npm install
4. bash scripts/core/sync.sh
5. node scripts/core/test-frontmatter.mjs --ci
6. npm run build         # 觸發 prebuild + build + postbuild
7. actions/upload-pages-artifact (./dist)
8. actions/deploy-pages
```

push 到 `main` 自動部署，無需手動介入。

### 8.3 Husky Git Hooks

| Hook | 檢查項目 |
|---|---|
| [.husky/pre-commit](../.husky/pre-commit) | 1. 去識別化檢查（`scripts/tools/deidentification-check.sh`）<br>2. lint-staged（prettier）<br>3. `test-frontmatter.mjs --staged`<br>4. wikilink 驗證 |
| [.husky/commit-msg](../.husky/commit-msg) | 雜湊式去識別化檢查（commit message 中是否含敏感姓名/檔名） |

詳見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

> ⚠️ 已知問題：當前 hook 檔案缺少執行權限，會被 git 靜默跳過。修復：`chmod +x .husky/pre-commit .husky/commit-msg`

## 9. 已知陷阱（Known Traps）

### 9.1 BASE_URL 硬編碼

- `astro.config.mjs` 設 `base: '/agrischlchiayi'`
- `scripts/core/generate-api.js` 硬編碼 `BASE_URL = 'https://ahnchen1983.github.io/agrischlchiayi'`
- 所有元件以 `.replace(/\/$/, '')` 處理尾斜線
- **更換部署網域時需同步修改三處**

### 9.2 `sync.sh` 會清空 `src/content/zh-TW`

- `sync.sh` 採取「`rm -rf` 再重建」策略以保證冪等
- **直接修改 `src/content/zh-TW/` 的內容會在下次 sync 全部消失**
- 修改一律從 `knowledge/` 開始

### 9.3 `generate-api.js` 直讀 `knowledge/`

- 該腳本不經 `src/content/zh-TW/`，直接讀 `knowledge/`
- 若 frontmatter YAML 有錯，腳本會 `console.error` 但不中斷，造成 `articles.json` 缺漏
- 排錯：先跑 `npm test` 確認 frontmatter 有效

### 9.4 Wikilink 在清單項中失效

- 自訂 plugin [plugins/remark-wikilinks.mjs](../plugins/remark-wikilinks.mjs) 在 `- [[X]]` 形式（清單項內）渲染不正常
- pre-commit hook 會擋；若需在清單中連結，改用標準 Markdown `[X](/url)`

### 9.5 i18n 尚未啟用

- `src/i18n/` 有 13 個 .ts 檔，但目前僅 zh-TW 實際渲染
- `knowledge/` 下若有 `en/`、`es/`、`ja/` 子目錄，目前不會被建置
- 多語系切換 UI 也尚未在 Header 中實作

### 9.6 `cli/` 與站點解耦

- `cli/` 是獨立 npm 模組，有自己的 `package-lock.json`
- 站點 build 不會處理 `cli/`；兩者共用 `knowledge/` 來源
- 新增分類時，站點的 schema 與 cli 的常數需同步維護

### 9.7 Husky hook 執行權限

如本文 §8.3 所述，當前 hook 因 chmod 缺失而靜默跳過。提交前先確認：

```bash
ls -l .husky/pre-commit .husky/commit-msg   # 應出現 x 權限
```

## 10. 設計決策（Why）

### 10.1 為什麼採 SSOT 架構（`knowledge/` → `src/content/`）

- Markdown 易於版本控制與協作
- `src/content/` 為投影層，不提交 git（在 `.gitignore`）
- 變更流向單一：編輯 → sync → build → dist
- 杜絕「幽靈版本」與內容分散

### 10.2 為什麼用 MiniSearch 而非伺服器端搜尋

- GitHub Pages 純靜態，無 server
- MiniSearch ~30KB gzipped，原生支援 CJK bigram
- JSON 序列化易於版本控制與快取

### 10.3 為什麼用 D3 force-directed graph

- 可控視覺化，與 Astro `client:load` 相容
- 中等規模圖（40-100 節點）效能足夠
- 學習曲線友善

### 10.4 為什麼 Frontmatter 統一 schema

- 多維度濾篩（作物、技術、難度）
- SEO 與 OG 自動化
- 便於圖譜邊建構（共享 tag/crop/tech）
- 對貢獻者規範清楚

## 11. 演進方向（路線圖）

| 期程 | 主題 |
|---|---|
| 短期（4 週內） | 搜尋排序優化、自動補全、圖譜互動增強（click-to-navigate, focus, 統計） |
| 中期（8 週內） | 多語系深化、農友資料批量去識別化、推薦引擎初版 |
| 長期（6 個月） | 語義搜尋（向量化）、社群功能（評論/案例討論）、離線版本 |

## 12. 成功標準

- 使用者能透過首頁、分類頁、搜尋與圖譜快速找到農業知識
- `knowledge/` 與網站輸出完全同步，無幽靈內容
- 子路徑部署下所有內部連結與資產正常
- 搜尋索引涵蓋所有已發布文章，查詢回應 <100ms
- 知識圖譜支援 50+ 節點互動
- 建置流程穩定可重現，無需手動介入
- 新貢獻者依 [README](../README.md) 與 [CONTRIBUTING](../CONTRIBUTING.md) 即可參與

## 13. 相關文件

- [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md) — 開發手冊（任務級操作）
- [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) — 13 大分類定義與內容缺口
- [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) — 農友資料整合架構
- [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) — 農友資料處理流程
- [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — 去識別化政策與檢查清單
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — 投稿指南
