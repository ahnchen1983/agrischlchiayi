# ARCHITECTURE.md - 嘉義國本學堂完整系統架構

## 1. 專案基本資訊

- **專案名稱**：嘉義國本學堂
- **Repo 名稱**：`agrischlchiayi`
- **GitHub Repo**：https://github.com/ahnchen1983/agrischlchiayi
- **更新日期**：2026-04-18
- **負責人**：ahnchen

## 2. 專案願景

將嘉義縣政府農業處「國本學堂」與延伸在地農業資料，整理為一個：

- **公開可讀**：任何人都能直接瀏覽學習
- **開源可編修**：以 Markdown 為主體，方便協作與版本管理
- **可持續成長**：隨著課程、案例、交流持續擴充

核心願景是讓新農、返鄉青年、學生與農場經營者，有一個結構清楚、可搜尋、可視覺化探索的農業知識入口。

## 3. 核心功能設定

### 已實作功能

- 首頁與主題導覽
- `13` 大農業主類別頁
- 文章頁面與 frontmatter schema
- `graph` 知識圖譜頁面
- 搜尋索引與 `public/api` JSON 輸出
- `RSS / feed.xml`
- GitHub Pages 靜態部署

### 持續演進項目

- 內容量擴充與來源補強
- `Taiwan.md` fork 遺留頁面與品牌文字清理
- 多語系與農業專屬 SEO 微調
- 更多學習路徑與主題索引
- 農民耕作資料整合

## 4. 系統架構

### 4.1 Content Architecture

```text
knowledge/                  -> 內容真相來源（SSOT）
   │
   └─ scripts/core/sync.sh  -> 同步 / 清理 / frontmatter 修復
         │
         ▼
src/content/zh-TW/          -> Astro 內容投影層
         │
         ▼
src/pages + src/templates   -> 頁面渲染
         │
         ▼
GitHub Pages                -> 靜態網站輸出
```

### 4.2 技術選型

- **框架**：Astro 6
- **視覺化**：D3.js
- **內容格式**：Markdown + YAML frontmatter
- **建置腳本**：Node.js / bash / Python 輔助腳本
- **部署**：GitHub Pages

### 4.3 Base URL / Routing 規範

目前部署在 GitHub Pages 子路徑：

```js
base: '/agrischlchiayi';
```

因此：

- `.astro` 檔案的內部連結應優先使用 `import.meta.env.BASE_URL`
- inline script 應透過 `window.__BASE__` 或注入變數取得 base
- 不建議直接寫死 `href="/..."` 或 `src="/..."`

## 5. 詳細資料流圖

### 5.1 內容處理流程

```mermaid
graph TD
    A[knowledge/*.md] --> B[scripts/core/sync.sh]
    B --> C[frontmatter 驗證與修復]
    B --> D[內容清理與格式化]
    C --> E[src/content/zh-TW/ 投影]
    D --> E
    E --> F[Astro Content Collections]
    F --> G[src/pages/[category]/[slug].astro]
    F --> H[src/pages/[category]/index.astro]
    G --> I[靜態 HTML 生成]
    H --> I
    I --> J[public/ 輸出]
```

### 5.2 搜尋索引生成流程

```mermaid
graph TD
    A[knowledge/ 內容] --> B[scripts/core/build-search-index.mjs]
    B --> C[解析 Markdown + frontmatter]
    B --> D[提取標題、描述、標籤]
    B --> E[CJK 分詞（Bigram tokenization）]
    C --> F[MiniSearch 序列化]
    D --> F
    E --> F
    F --> G[public/api/search-minisearch.json]
    F --> H[public/api/search-index.json 備用索引]
    G --> I[前端 MiniSearch 引擎<br/>含 boost 加權]
    H --> J[降級方案：indexOf 搜尋]
```

#### 搜尋系統架構
- **主索引**：MiniSearch（支援 CJK bigram）
  - 字段：title_bigram (boost: 6)、desc_bigram (boost: 4)、tags_bigram (boost: 2)
  - 前綴匹配、模糊搜尋、多語言支援
- **備用索引**：簡易 indexOf（無網路或 MiniSearch 失敗時）
- **語言優先排序**：當前頁面語言優先顯示

### 5.3 圖譜生成流程

```mermaid
graph TD
    A[knowledge/ 文章] --> B[src/pages/graph.astro]
    B --> C[掃描 frontmatter<br/>title, tags, crop, tech]
    B --> D[掃描 Wikilinks<br/>[[Article Title]]語法]
    C --> E[組建圖節點<br/>category+slug id]
    D --> E
    E --> F[組建圖邊<br/>tag/topic 連接]
    F --> G[D3.js force-directed graph]
    G --> H[互動式知識圖譜頁面<br/>點擊、懸停、拖動]
```

#### 知識圖譜架構
- **節點類型**：中心節點、文章節點、特殊節點（About 等）
- **邊連接方式**：共享標籤、共享作物類型、共享技術標籤
- **視覺化**：D3.js force-directed，按分類著色
- **交互**：點擊跳轉、懸停顯示標題、拖動重排

## 6. 各 Component / Template 職責與 API

### 6.1 主要 Templates

| Template | 位置 | 職責 | API / Props |
|----------|------|------|------------|
| `ArticleLayout` | `src/layouts/ArticleLayout.astro` | 文章頁面佈局，包含導覽、內容、相關文章 | `title`, `description`, `content`, `related` |
| `CategoryLayout` | `src/layouts/CategoryLayout.astro` | 分類頁面佈局，展示文章列表 | `category`, `articles[]`, `description` |
| `BaseLayout` | `src/layouts/BaseLayout.astro` | 基礎佈局，包含 header, footer, SEO | `title`, `description`, `ogImage` |

### 6.2 核心 Components

| Component | 位置 | 職責 | API / Props |
|-----------|------|------|------------|
| `Graph` | `src/components/Graph.tsx` | D3.js 知識圖譜渲染 | `data: GraphData`, `width`, `height` |
| `Search` | `src/components/Search.tsx` | 搜尋功能組件 | `index: SearchIndex`, `onResult` |
| `ArticleCard` | `src/components/ArticleCard.astro` | 文章卡片展示 | `title`, `excerpt`, `slug`, `category` |
| `CategoryNav` | `src/components/CategoryNav.astro` | 分類導覽 | `categories[]`, `currentCategory` |
| `Header` | `src/components/Header.astro` | 網站標頭 | `baseUrl`, `navItems[]` |
| `Footer` | `src/components/Footer.astro` | 網站頁尾 | `links[]` |

### 6.3 Page Components

| Page | 職責 | 資料來源 |
|------|------|----------|
| `index.astro` | 首頁，展示精選內容與分類入口 | `src/content/zh-TW/_Home.md` |
| `[category]/index.astro` | 分類首頁，列表該分類所有文章 | Content Collections API |
| `[category]/[slug].astro` | 文章頁面，渲染單篇文章 | Content Collections API |
| `graph.astro` | 圖譜頁面，知識網路視覺化 | `public/api/graph.json` |
| `about.astro` | 關於頁面，專案介紹 | 靜態內容 |
| `contribute.astro` | 貢獻指南 | 靜態內容 + `CONTRIBUTING.md` |

## 7. 建置流程詳解

### 7.1 Prebuild 階段

```bash
# scripts/core/prebuild.sh
1. 驗證 knowledge/ 目錄結構
2. 檢查 frontmatter schema 完整性
3. 清理無效的 wikilinks
4. 生成分類索引
```

### 7.2 Build 階段 (Astro)

```bash
npm run build
1. Astro 編譯 .astro 檔案
2. 處理 Content Collections
3. 生成靜態 HTML
4. 優化資源 (CSS, JS, 圖片)
5. 輸出到 dist/
```

### 7.3 Postbuild 階段

```bash
# scripts/core/postbuild.sh
1. 複製 dist/ 到 public/
2. 生成搜尋索引 (search.json)
3. 生成圖譜資料 (graph.json)
4. 更新 RSS feed
5. 驗證內部連結完整性
```

### 7.4 完整建置指令

```bash
# 開發建置
npm run dev

# 生產建置
npm run build

# 完整流程 (含前後處理)
./scripts/core/full-build.sh
```

## 8. 部署流程與 CI/CD

### 8.1 GitHub Pages 部署

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: npm ci
    - run: npm run build
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
        cname: agrischlchiayi.github.io
```

### 8.2 部署檢查清單

- [ ] Base URL 正確設定 (`/agrischlchiayi`)
- [ ] 所有內部連結使用相對路徑或 `BASE_URL`
- [ ] 圖片與資源路徑正確
- [ ] 搜尋索引生成完成
- [ ] RSS feed 更新
- [ ] 404 頁面正常

## 9. 架構設計決策與原因

### 9.1 為什麼選擇 MiniSearch 而非傳統搜尋引擎？

**決策**：客戶端 MiniSearch library（而非伺服器 Elasticsearch 或 Algolia）

**原因**：
- 靜態網站無伺服器，GitHub Pages 只支援純靜態
- MiniSearch 體積小（~30KB gzipped），無額外依賴
- 支援 CJK bigram 分詞，適合中文農業術語
- JSON 序列化格式，易於版本控制與持續更新

### 9.2 為什麼採用 SSOT (Single Source of Truth) 架構？

**決策**：`knowledge/` 作為唯一源，通過 sync.sh 投影到 `src/content/zh-TW/`

**原因**：
- Markdown 文件易於版本控制、易於協作
- 生成的 `src/content/` 為暫時投影層，不提交 git
- 變更流向清晰：編輯 → knowledge/ → sync → src/content/ → build → dist
- 防止內容分散或「幽靈版本」

### 9.3 為什麼使用 D3.js Force-Directed Graph？

**決策**：D3.js 而非其他圖譜庫（如 vis.js 或 Cytoscape）

**原因**：
- 完全可控的視覺化，支援無限自訂
- 與 Astro 相容性強（client:load 指令）
- 適合中等規模圖（40-100 節點），效能足夠
- 學習曲線相對友善，生態豐富

### 9.4 為什麼 frontmatter 統一管理，而非分散？

**決策**：標準化 frontmatter schema（title, description, tags, level, crop, tech, status）

**原因**：
- 便於內容檢索、分類、圖譜生成
- 支援多維度濾篩（按作物、按技術、按難度）
- 易於 SEO 與 Open Graph 自動化
- 新貢獻者有清晰的編輯規範

## 10. 已知陷阱與解決方案

### 9.1 BASE_URL 處理

**問題**: GitHub Pages 子路徑部署時，絕對路徑會失效
**解決**: 
- 使用 `import.meta.env.BASE_URL` in .astro
- inline script 使用 `window.__BASE__`
- 避免硬編碼 `/path`

### 9.2 Husky PATH 問題

**問題**: Git hooks 無法找到 Node.js
**解決**: 
```bash
# .husky/pre-commit
#!/usr/bin/env bash
export PATH="/usr/local/bin:$PATH"
npx lint-staged
```

### 9.3 D3 Graph 渲染問題

**問題**: SSR 環境下 D3.js 無法正常渲染
**解決**: 
- 使用 `client:load` 指令
- 確保資料在 client 端載入
- 處理 hydration 時機

### 9.4 Frontmatter Schema 不一致

**問題**: 不同文章的 frontmatter 格式不統一
**解決**: 
- 使用 `scripts/core/sync.sh` 統一格式
- 定義標準 schema 在 `src/content/config.ts`

### 9.5 Wikilinks 解析

**問題**: `[[link]]` 語法在不同情境下解析不一致
**解決**: 
- 自訂 remark 插件 `plugins/remark-wikilinks.mjs`
- 統一解析邏輯在 `src/lib/utils/wikilinks.ts`

## 11. 架構演進方向（2026Q2-Q3）

### 短期（4 週內）
- 搜尋結果排序優化：按相關性、按分類、按新鮮度
- 搜尋自動補全：熱門農業術語提示
- 知識圖譜交互增強：click-to-navigate、focus 高亮、統計資訊

### 中期（8 週內）
- 多語系支援深化：英文農業內容補全、i18n SEO 最佳化
- 農民耕作資料整合：批量去識別化案例導入
- 推薦引擎初步版本：基於使用者瀏覽歷史的相關文章推薦

### 長期（6 個月）
- 全文搜尋與NLP：農業專屬詞彙向量化、語義搜尋
- 社群化功能：用戶評論、案例討論、經驗分享
- 移動應用考慮：Electron/Capacitor 離線版本

## 12. 成功標準

### 內容層面
- 使用者能透過首頁、分類頁、搜尋與圖譜快速找到農業知識
- `knowledge/` 與網站輸出完全同步，不產生幽靈內容
- 新貢獻者能依 `README` 與 `CONTRIBUTING.md` 直接參與

### 技術層面
- GitHub Pages 子路徑部署下，所有內部連結與資產都正常
- 搜尋索引完整包含 100+ 文章，查詢回應 <100ms
- 知識圖譜支援 50+ 節點的互動式操作
- 建置流程穩定、可重現、無手動介入需求
- 所有 assets 預算在 2MB 以內（gzip）

### 用戶體驗層面
- 首頁加載 <2s（3G 網路），搜尋結果 <0.5s 出現
- 圖譜交互流暢，懸停 <50ms 顯示節點資訊
- 移動設備適配，響應式設計完整
- 無障礙訪問達到 WCAG 2.1 AA 標準