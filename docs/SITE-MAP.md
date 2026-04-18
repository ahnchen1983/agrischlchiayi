# SITE-MAP.md - 嘉義國本學堂網站功能地圖

## 概述

嘉義國本學堂是一個基於 Astro 框架的靜態網站，提供農業知識的結構化展示、搜尋與視覺化探索。網站部署在 GitHub Pages 子路徑 `/agrischlchiayi` 下。

## 主要頁面與路由

### 核心頁面

| 路由 | 檔案 | 功能描述 | 狀態 |
|------|------|----------|------|
| `/` | `src/pages/index.astro` | 首頁 - 展示主要分類與導覽入口 | ✅ 實作 |
| `/about` | `src/pages/about.astro` | 關於頁面 - 專案介紹與團隊資訊 | ✅ 實作 |
| `/graph` | `src/pages/graph.astro` | 知識圖譜 - D3.js 視覺化知識網路 | ✅ 實作 |
| `/contribute` | `src/pages/contribute.astro` | 貢獻指南 - 如何參與專案 | ✅ 實作 |
| `/changelog` | `src/pages/changelog.astro` | 變更日誌 - 專案更新記錄 | ✅ 實作 |

### 分類頁面 (動態路由)

| 路由模式 | 檔案 | 功能描述 | 狀態 |
|----------|------|----------|------|
| `/[category]` | `src/pages/[category]/index.astro` | 分類首頁 - 展示該類別所有文章 | ✅ 實作 |
| `/[category]/[slug]` | `src/pages/[category]/[slug].astro` | 文章頁面 - 單篇文章內容展示 | ✅ 實作 |

**支援的分類** (對應 `knowledge/` 目錄):

- `Agri-Advanced` - 進階農業
- `Agri-Basics` - 農業基礎
- `Agri-Marketing` - 農業行銷
- `Crop-Index` - 作物索引
- `Crop-Production` - 作物生產
- `Facility-Farming` - 設施農業
- `Farm-Management` - 農場管理
- `Field-Visits` - 田間訪查
- `Grants-Planning` - 補助規劃
- `Learning-Paths` - 學習路徑
- `Livestock-Health` - 畜牧健康
- `Smart-Farming` - 智慧農業
- `Tech-Index` - 科技索引

### 工具與資源頁面

| 路由 | 檔案 | 功能描述 | 狀態 |
|------|------|----------|------|
| `/terminology` | `src/pages/terminology/index.astro` | 術語辭典 - 農業專用詞彙解釋 | ✅ 實作 |
| `/data` | `src/pages/data.astro` | 資料頁面 - 數據視覺化與下載 | ✅ 實作 |
| `/companies` | `src/pages/companies.astro` | 公司頁面 - 相關企業資訊 | ✅ 實作 |
| `/projects` | `src/pages/projects.astro` | 專案頁面 - 相關專案展示 | ✅ 實作 |
| `/resources` | `src/pages/resources.astro` | 資源頁面 - 外部資源連結 | ✅ 實作 |
| `/soundscape` | `src/pages/soundscape.astro` | 聲景頁面 - 農業音效體驗 | ✅ 實作 |
| `/map` | `src/pages/map.astro` | 地圖頁面 - 地理資訊展示 | ✅ 實作 |
| `/fork-graph` | `src/pages/fork-graph.astro` | Fork 圖譜 - 專案分支視覺化 | ✅ 實作 |
| `/dashboard` | `src/pages/dashboard.astro` | 儀表板 - 統計數據展示 | ✅ 實作 |

### API 端點

| 路由 | 檔案 | 功能描述 | 狀態 |
|------|------|----------|------|
| `/api/search.json` | `src/pages/api/search.json.ts` | 搜尋索引 API | ✅ 實作 |
| `/feed.xml` | `src/pages/feed.xml.ts` | RSS Feed | ✅ 實作 |
| `/rss.xml` | `src/pages/rss.xml.ts` | RSS Feed (別名) | ✅ 實作 |

### 其他

| 路由 | 檔案 | 功能描述 | 狀態 |
|------|------|----------|------|
| `/404` | `src/pages/404.astro` | 404 錯誤頁面 | ✅ 實作 |
| `/og/[...path]` | `src/pages/og/[...path].astro` | Open Graph 圖片生成 | ✅ 實作 |
| `/assets` | `src/pages/assets.astro` | 資產頁面 | ✅ 實作 |

## 網站功能地圖

```mermaid
graph TD
    A[首頁 /] --> B[分類導覽]
    A --> C[搜尋功能]
    A --> D[圖譜探索 /graph]
    
    B --> E[Agri-Basics]
    B --> F[Agri-Advanced]
    B --> G[其他分類...]
    
    E --> H[文章列表]
    H --> I[單篇文章頁面]
    
    D --> J[D3.js 知識網路]
    J --> K[節點點擊導航]
    
    L[工具頁面] --> M[/terminology]
    L --> N[/data]
    L --> O[/dashboard]
    
    P[API] --> Q[/api/search.json]
    P --> R[/feed.xml]
```

## 導覽結構

- **主要導覽**: 首頁 → 分類 → 文章
- **探索導覽**: 圖譜頁面提供視覺化探索
- **工具導覽**: 術語、資料、儀表板等輔助功能
- **外部連結**: 資源頁面提供外部參考

## 路由規範

- **Base URL**: `/agrischlchiayi` (GitHub Pages 子路徑)
- **動態路由**: 使用 `[category]` 和 `[slug]` 參數
- **API 路由**: `/api/` 前綴
- **靜態資源**: `/assets/` 路徑

## 未來擴充建議

1. 新增 `/learning-paths/[path]` 動態路由
2. 整合 `/field-visits` 與農民資料
3. 新增 `/api/articles.json` 文章列表 API
4. 支援 `/[locale]/[category]` 多語系路由