# ONBOARDING.md - 新人 0→1 學習檔案

歡迎加入嘉義國本學堂專案！本文件將引導你從零開始上手這個專案。

## 🎯 學習目標

完成本指南後，你將能夠：
- 理解專案架構與工作流程
- 在本地環境中運行專案
- 進行基本的功能開發與修改
- 熟悉部署與貢獻流程

## 📋 前置準備

### 系統需求

- **Node.js**: 18.0 或更新版本
- **Git**: 2.0 或更新版本
- **VS Code**: 推薦安裝 (含 GitHub Copilot)
- **終端機**: 熟悉基本命令列操作

### 建議技能

- HTML/CSS/JavaScript 基礎
- Markdown 語法
- Git 版本控制
- 命令列操作

## 🚀 快速開始 (30 分鐘)

### 步驟 1: 複製專案

```bash
# 複製專案到本地
git clone https://github.com/ahnchen1983/agrischlchiayi.git

# 進入專案目錄
cd agrischlchiayi

# 安裝依賴套件
npm install
```

### 步驟 2: 啟動開發環境

```bash
# 啟動開發伺服器
npm run dev
```

打開瀏覽器訪問 `http://localhost:4321/agrischlchiayi/` 查看網站。

### 步驟 3: 基本導覽

1. **首頁** (`/`)
   - 展示核心農業挑戰與推薦學習路徑
   - 分類導覽與精選文章
   
2. **搜尋功能** (Ctrl+K 或點擊搜尋按鈕)
   - 全文搜尋所有文章
   - 按相關性、語言排序
   - 支援 CJK 分詞（中文詞彙搜尋）
   
3. **知識圖譜** (`/graph`)
   - 知識網路視覺化展示
   - 點擊節點跳轉文章
   - 懸停查看文章標題與摘要
   
4. **分類頁面** (如 `/crop-production`)
   - 該分類的所有文章列表
   - 篩選與排序功能
   
5. **文章頁面**
   - 完整文章內容
   - 相關文章推薦
   - Wikilinks 快速導航

## 📁 專案結構概覽

```
agrischlchiayi/
├── knowledge/          # 📚 內容來源 (Markdown)
├── src/
│   ├── pages/          # 🌐 頁面路由
│   ├── components/     # 🧩 UI 組件
│   ├── layouts/        # 📐 頁面佈局
│   └── content/        # 📄 內容設定
├── scripts/            # 🔧 建置腳本
├── public/             # 🖼️ 靜態資源
├── docs/               # 📖 文件
└── package.json        # ⚙️ 專案設定
```

### 關鍵目錄說明

| 目錄 | 用途 | 重要性 |
|------|------|--------|
| `knowledge/` | 所有內容的真相來源 | ⭐⭐⭐ |
| `src/pages/` | 定義網站路由與頁面 | ⭐⭐⭐ |
| `src/components/` | 可重用 UI 組件 | ⭐⭐⭐ |
| `scripts/core/` | 建置與處理腳本 | ⭐⭐ |
| `docs/` | 專案文件與指南 | ⭐⭐ |

## 📖 核心概念

### 內容管理

- **SSOT (Single Source of Truth)**: `knowledge/` 是唯一內容來源
- **Markdown + Frontmatter**: 文章格式
- **分類結構**: 按主題組織內容

### 技術架構

- **Astro 框架**: 靜態網站生成器
- **Content Collections**: Astro 的內容管理 API
- **GitHub Pages**: 部署平台 (子路徑 `/agrischlchiayi`)

### 開發流程

1. **編輯內容** → `knowledge/*.md`
2. **同步處理** → `scripts/core/sync.sh`
3. **建置網站** → `npm run build`
4. **部署上線** → GitHub Actions

## 🛠️ 實作練習 (1 小時)

### 練習 1: 修改現有文章

1. 打開 `knowledge/Agri-Basics/` 目錄
2. 編輯任一 `.md` 檔案
3. 修改內容或 frontmatter
4. 儲存並觀察開發伺服器自動重載

### 練習 2: 新增測試文章

1. 在 `knowledge/Agri-Basics/` 建立 `test-article.md`
2. 加入基本 frontmatter:
   ```yaml
   ---
   title: "測試文章"
   description: "這是測試用的文章"
   date: "2026-04-18"
   ---
   ```
3. 寫入一些 Markdown 內容
4. 訪問 `/Agri-Basics/test-article` 查看結果

### 練習 3: 測試建置流程

```bash
# 檢查內容同步
./scripts/core/sync.sh

# 建置生產版本
npm run build

# 預覽建置結果
npm run preview
```

## 🔍 深入學習

### 階段 2: 功能開發 (2-4 小時)

#### 學習目標
- 理解組件架構
- 修改現有功能
- 新增簡單功能

#### 建議練習
1. **修改樣式**: 編輯 `src/components/Header.astro`
2. **新增組件**: 在 `src/components/` 建立新組件
3. **修改頁面**: 編輯 `src/pages/about.astro`

#### 學習資源
- [Astro 官方文件](https://docs.astro.build/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [D3.js 圖表](https://d3js.org/)

### 階段 2.5: 搜尋與圖譜功能 (1 小時)

#### 學習目標
- 理解搜尋系統如何運作
- 掌握知識圖譜的互動方式
- 了解如何優化搜尋結果

#### 練習任務
1. **搜尋功能探索**
   - 在首頁按 `Ctrl+K` 打開搜尋
   - 搜尋農業術語：「小黃瓜」「IoT」「設施農業」
   - 觀察搜尋結果的排序與相關性
   
2. **知識圖譜探索**
   - 進入 `/graph` 頁面
   - 點擊不同節點查看相關文章
   - 懸停節點查看標題提示
   - 注意不同顏色代表不同分類
   
3. **搜尋索引驗證**
   ```bash
   # 重新生成搜尋索引
   node scripts/core/build-search-index.mjs
   
   # 檢查索引大小與內容
   cat public/api/search-minisearch.json | grep -o '"id"' | wc -l
   ```

#### 後續深化
- 閱讀 [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md) 搜尋與圖譜章節
- 探索如何新增自訂搜尋加權規則
- 參與優化知識圖譜的互動體驗

### 階段 3: 內容管理 (1-2 小時)

#### 學習目標
- 掌握內容格式標準
- 理解分類結構
- 熟悉 wikilinks 語法

#### 練習任務
1. 建立新分類目錄
2. 撰寫結構完整的文章
3. 設定文章間的 wikilinks

### 階段 4: 農民數據整合 (進階，2-3 小時)

#### 學習目標
- 理解農民耕作資料如何轉化為知識文章
- 掌握去識別化處理流程
- 參與批量內容製作

#### 背景知識
- 專案包含 73 份農民經營計畫書（`source/` 目錄）
- 通過系統化處理，可轉化為 70-80 篇農業知識文章
- 去識別化是核心原則：保留農業知識，移除個人信息

#### 練習任務（高級）
1. **探索農民數據**
   ```bash
   # 查看農友檔案結構
   ls source/ | head -10
   
   # 檢查一份農友計畫書
   head -50 source/農友1.md
   ```

2. **試製一篇文章**
   - 選擇 2-3 份農友檔案（共同作物/技術）
   - 遵循 [FARMER-DATA-PROCESSING-CHECKLIST.md](FARMER-DATA-PROCESSING-CHECKLIST.md)
   - 撰寫去識別化的知識文章

3. **隱私保護驗證**
   - 檢查文章是否包含農友名字、聯絡方式
   - 確保保留了農業知識要點
   - 進行「反向工程測試」：讀者能否推斷出具體農民？

#### 參考文件
- [FARMER-DATA-PROCESSING-CHECKLIST.md](FARMER-DATA-PROCESSING-CHECKLIST.md) - 6 步處理指南
- [DEIDENTIFICATION-CHECKLIST.md](DEIDENTIFICATION-CHECKLIST.md) - 隱私保護規範
- [FARMER-DATA-UTILIZATION-PLAN.md](FARMER-DATA-UTILIZATION-PLAN.md) - 完整批量計劃

### 階段 5: 部署與貢獻 (1 小時)

#### 學習目標
- 理解 Git 工作流程與最佳實踐
- 熟悉 Pull Request 審查流程
- 掌握部署前檢查清單

#### 實作步驟
1. 建立功能分支 (`git checkout -b feature/xxx`)
2. 提交變更 (`git commit -m "..."`)
3. 建立 Pull Request
4. 通過 CI/CD 檢查 (GitHub Actions)
5. 獲得核心團隊審查通過
6. Merge 並自動部署

#### 提交最佳實踐
- Commit message 應清楚描述變更目的
- 提交前執行 `npm run check` 與 `npm run build`
- 遵循 [CONTRIBUTING.md](../CONTRIBUTING.md) 的貢獻指南

## 📚 必讀文件

按優先順序閱讀：

1. **[README.md](../README.md)** - 專案總覽
2. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - 貢獻指南
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - 系統架構
4. **[DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md)** - 開發手冊
5. **[SITE-MAP.md](SITE-MAP.md)** - 功能地圖

## 🆘 問題解決

### 常見問題

**Q: 開發伺服器啟動失敗？**
A: 確認 Node.js 版本為 18+，並重新執行 `npm install`

**Q: 頁面顯示 404？**
A: 檢查檔案路徑與命名，確保在正確目錄

**Q: 樣式不生效？**
A: 確認 Tailwind 類別正確，或檢查 `src/styles/global.css`

**Q: 建置失敗？**
A: 執行 `npm run check` 查看詳細錯誤

### 求助管道

1. **文件**: 先查閱 `docs/` 目錄
2. **程式碼**: 查看類似功能的實作
3. **Issues**: 在 GitHub 搜尋相關問題
4. **團隊**: 聯繫專案維護者

## 📊 學習進度總覽

| 階段 | 主題 | 時間 | 難度 | 必修 |
|------|------|------|------|------|
| 快速開始 | 環境設定與基本導覽 | 30 分鐘 | ⭐ | ✅ |
| 階段 1 | 實作練習（修改與新增） | 1 小時 | ⭐ | ✅ |
| 階段 2 | 功能開發與組件修改 | 2-4 小時 | ⭐⭐ | 若開發功能 |
| 階段 2.5 | 搜尋與圖譜探索 | 1 小時 | ⭐⭐ | 若參與優化 |
| 階段 3 | 內容管理與文章撰寫 | 1-2 小時 | ⭐⭐ | 若貢獻內容 |
| 階段 4 | 農民數據整合 | 2-3 小時 | ⭐⭐⭐ | 若參與批量製作 |
| 階段 5 | 部署與貢獻流程 | 1 小時 | ⭐ | ✅ |

## 🎉 完成檢查清單

**基礎級（必完成）**
- [ ] 成功啟動開發環境
- [ ] 理解專案基本結構
- [ ] 完成快速開始練習
- [ ] 熟悉部署與貢獻流程

**進階級（根據方向選擇）**
- [ ] 修改組件與樣式
- [ ] 撰寫新文章
- [ ] 優化搜尋功能
- [ ] 增強知識圖譜
- [ ] 處理農民數據

## 🚀 根據興趣的學習路徑

### 路徑 A: 內容貢獻者
最佳學習順序：快速開始 → 階段 1 → 階段 3 → 階段 4 → 階段 5
時間投入：4-6 小時

### 路徑 B: 功能開發者
最佳學習順序：快速開始 → 階段 1 → 階段 2 → 階段 2.5 → 階段 5
時間投入：6-10 小時

### 路徑 C: 全棧貢獻者
最佳學習順序：快速開始 → 全部階段 → 深化學習
時間投入：12-16 小時

## 💡 學習秘訣

1. **邊做邊學**：直接修改程式碼比閱讀文件更有效
2. **主動探索**：查看 `src/` 目錄中類似功能的實作
3. **善用搜尋**：使用 `grep` 與 IDE 搜尋功能找相關程式碼
4. **查閱文件**：遇到問題時優先查看 `docs/` 資料夾
5. **尋求協助**：在 GitHub Issues 或團隊內提問

## 🆘 如果卡住了

1. **檢查錯誤訊息**
   ```bash
   npm run build 2>&1 | tail -50
   ```

2. **查閱相關文件**
   - 開發問題 → [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md)
   - 架構問題 → [ARCHITECTURE.md](ARCHITECTURE.md)
   - 內容問題 → [CATEGORY-MAPPING-GUIDE.md](CATEGORY-MAPPING-GUIDE.md)

3. **搜尋程式碼**
   ```bash
   grep -r "你的搜尋詞" src/ knowledge/
   ```

4. **團隊協助**
   - GitHub Issues：報告 Bug 或提出功能請求
   - Discussions：尋求幫助或討論設計

## 📖 完整文件導覽

按推薦閱讀順序：

1. [README.md](../README.md) - 專案概述與願景
2. [CONTRIBUTING.md](../CONTRIBUTING.md) - 貢獻指南與規範
3. [ONBOARDING.md](ONBOARDING.md) - 本文件 (新人入門)
4. [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md) - 開發任務與工作流
5. [ARCHITECTURE.md](ARCHITECTURE.md) - 系統架構與設計決策
6. [SITE-MAP.md](SITE-MAP.md) - 網站功能地圖
7. [DOCUMENTATION-AND-OPTIMIZATION-PLAN.md](DOCUMENTATION-AND-OPTIMIZATION-PLAN.md) - 優化藍圖

## 🎓 進階資源

- **技術文檔**
  - [Astro 官方文件](https://docs.astro.build/)
  - [Tailwind CSS 文件](https://tailwindcss.com/)
  - [D3.js 教程](https://d3js.org/getting-started)

- **農業專欄**
  - [嘉義農業處](https://www.ciaext.gov.tw/)
  - [農試所資訊](https://www.tari.gov.tw/)

## 🌱 歡迎加入！

恭喜完成基礎學習！現在你已經準備好為嘉義國本學堂做出貢獻。

無論你選擇哪條學習路徑，記住：
- 📝 好的文件都是從第一次貢獻開始
- 💻 最好的代碼是被不斷改進的代碼
- 🤝 最強的團隊是互相幫助的團隊

如有任何問題或建議，歡迎在 GitHub Issues 中與我們分享！

歡迎加入嘉義國本學堂的開發行列！🌱🌾