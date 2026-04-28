# 嘉義國本學堂

> 將嘉義縣國本學堂課程與在地農業知識，整理成公開、開源、可持續成長的農業知識平台。

[網站首頁](https://ahnchen1983.github.io/agrischlchiayi/) · [知識圖譜](https://ahnchen1983.github.io/agrischlchiayi/graph) · [關於](https://ahnchen1983.github.io/agrischlchiayi/about) · [貢獻](https://ahnchen1983.github.io/agrischlchiayi/contribute)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

---

## 專案定位

`agrischlchiayi` 是一個以 **嘉義農業課程、在地經驗、可重用 Markdown 知識** 為核心的網站專案。
內容由 `knowledge/` 維護，網站由 Astro 讀取 `src/content/zh-TW/` 投影層輸出，並部署到 GitHub Pages。

### 目標使用者

- 新農與返鄉青年
- 農業課程學員
- 學生與研究者
- 農場經營者與農企業主

## 目前主題架構

| #   | 類別         | 說明                               |
| --- | ------------ | ---------------------------------- |
| 1   | 農業基礎入門 | 土壤、水資源、有機農法與入門概念   |
| 2   | 農業進階實務 | 栽培進階管理、實作工作坊與經驗整理 |
| 3   | 農場經營管理 | 財務、人力、經營策略               |
| 4   | 作物生產技術 | 小番茄、百香果等作物實務           |
| 5   | 設施農業     | 溫室、環控、滴灌與設施規劃         |
| 6   | 智慧農業     | 感測器、灌溉、無人機與智農應用     |
| 7   | 農產品銷售   | 品牌建立與通路經營                 |
| 8   | 計畫撰寫補助 | 補助申請與提案能力                 |
| 9   | 場域交流觀摩 | 參訪、交流會與案例觀摩             |
| 10  | 畜牧健康     | 家禽家畜管理與健康議題             |

## 技術架構

- **內容來源（SSOT）**：`knowledge/`
- **網站投影層**：`src/content/zh-TW/`
- **框架**：`Astro 6` + D3.js
- **搜尋 / API**：建置時產生 `public/api/*.json`
- **部署**：GitHub Pages
- **Base Path**：`/agrischlchiayi`

## 重要資料夾

```text
knowledge/              # 內容真相來源（Single Source of Truth）
src/content/zh-TW/      # 給 Astro 使用的內容投影層
src/pages/              # 各頁路由
src/components/         # 可重用 UI 元件
src/templates/          # 大型頁面模板
scripts/core/           # 建置、同步、索引生成腳本
public/api/             # 建置後可供前端讀取的 JSON API
```

## 開發指令

```bash
npm install
npm run dev        # 啟動開發伺服器
npm run sync       # knowledge/ -> src/content/zh-TW 同步
npm run build      # 建置站點
npm test           # frontmatter 驗證
```

## `.astro` / GitHub Pages Base Path 注意事項

本專案部署在 GitHub Pages 子路徑下，因此 `.astro` 內的內部連結與資產路徑，**請優先使用** `import.meta.env.BASE_URL`：

```astro
---
const base = import.meta.env.BASE_URL;
---

<a href={`${base}about`}>關於</a>
<img src={`${base}favicon.png`} alt="logo" />
```

若在 inline script 中需要路徑，請使用 `window.__BASE__` 或先由 Astro 注入 base，避免直接寫死 `"/..."`。

## 貢獻方式

- 直接修改 `knowledge/` Markdown
- 補齊 frontmatter 與來源欄位
- 提交 PR 或 Issue 回報內容問題

詳見 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

> ⚠️ **若涉及農友個人資料**，提交前必讀 [`DEIDENTIFICATION-POLICY.md`](DEIDENTIFICATION-POLICY.md)。

## 文件導覽

| 文件 | 用途 |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 系統設計文件（SDD） |
| [`docs/DEVELOPER-GUIDE.md`](docs/DEVELOPER-GUIDE.md) | 開發手冊與常見任務 |
| [`docs/CATEGORY-MAPPING.md`](docs/CATEGORY-MAPPING.md) | 13 大分類定義與內容缺口 |
| [`docs/FARMER-DATA-PIPELINE.md`](docs/FARMER-DATA-PIPELINE.md) | 農友資料整合架構 |
| [`docs/FARMER-DATA-WORKFLOW.md`](docs/FARMER-DATA-WORKFLOW.md) | 農友資料處理流程 |
| [`DEIDENTIFICATION-POLICY.md`](DEIDENTIFICATION-POLICY.md) | 去識別化政策與檢查清單 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 投稿指南 |

完整文件索引見 [`docs/README.md`](docs/README.md)。

## 授權

- **內容**： [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **程式碼**： MIT License
