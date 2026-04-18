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

1. **首頁**: 主要分類入口
2. **圖譜頁面**: `/graph` - 知識網路視覺化
3. **分類頁面**: 點擊任一分類查看文章列表
4. **文章頁面**: 點擊文章標題閱讀內容

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

### 階段 3: 內容管理 (1-2 小時)

#### 學習目標
- 掌握內容格式標準
- 理解分類結構
- 熟悉 wikilinks 語法

#### 練習任務
1. 建立新分類目錄
2. 撰寫結構完整的文章
3. 設定文章間的 wikilinks

### 階段 4: 部署與貢獻 (1 小時)

#### 學習目標
- 理解 Git 工作流程
- 熟悉 Pull Request 流程
- 掌握部署檢查

#### 實作步驟
1. 建立功能分支
2. 提交變更
3. 建立 Pull Request
4. 檢查 CI/CD 狀態

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

## 🎉 完成檢查清單

- [ ] 成功啟動開發環境
- [ ] 理解專案基本結構
- [ ] 完成所有練習任務
- [ ] 熟悉建置與部署流程
- [ ] 閱讀核心文件

## 🚀 下一步

恭喜完成基礎學習！接下來你可以：

- 開始貢獻內容或功能
- 深入學習特定技術棧
- 參與專案討論與規劃
- 探索進階功能開發

歡迎加入嘉義國本學堂的開發行列！🌱