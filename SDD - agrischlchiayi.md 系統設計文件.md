# SDD - agrischlchiayi.md 系統設計文件

## 1. 專案基本資訊

- **專案中文名稱**：嘉義農業學堂
- **專案英文名稱 / Repo**：agrischlchiayi.md
- **GitHub Repo**：https://github.com/ahnchen1983/agrischlchiayi.md
- **建立日期**：2026年4月
- **負責人**：ahnchen

## 2. 專案目的與願景

將嘉義縣政府農業處「國本學堂」在 Accupass 上所有過去課程，轉化為一個**公開、開源、持續成長**的農業知識平台。

目標：

- 讓新農、轉行者、學生、農企業主能系統化學習。
- 透過 **Graph View（知識圖譜）** 呈現課程之間的關聯，讓學習路徑清晰可視。
- 成為嘉義（乃至台灣）農業的「大家彼此支持的大型學習性現場」。

## 3. 核心功能

- 互動式知識圖譜（類似 taiwan.md 的 /graph）
- 階層式分類（10大主類別 + 子類別 + 作物/技術索引）
- 統一 Frontmatter 支援搜尋、Dataview、Graph 聚類
- 開放貢獻機制（GitHub PR + 表單投稿）
- 推薦學習路徑地圖
- 完全本地 Markdown + Obsidian 友好

## 4. 技術架構

- 內容存放：`knowledge/` 資料夾（Single Source of Truth）
- 本地編輯工具：Obsidian（Graph View、Dataview、Templater）
- 網站框架：Fork 自 taiwan-md（Astro v5 + D3.js Graph）
- 部署：GitHub Pages（免費自動部署）

## 5. 資料夾結構（預覽）

agrischlchiayi.md/
├── knowledge/
│ ├── 01-農業基礎入門/
│ ├── 02-農業進階實務/
│ ├── ...（共10個主類別）
│ ├── 作物索引/
│ ├── 技術索引/
│ └── 學習路徑/
├── CONTRIBUTING.md
├── EDITORIAL.md
├── SDD.md
└── ...

## 6. 成功標準

- 本地 Obsidian 可看到完整 Graph View
- 網站 `/graph` 頁面正常運作
- 至少完成 10 個主類別索引頁 + 15 篇範例筆記
- 新手可透過 CONTRIBUTING.md 輕鬆投稿
