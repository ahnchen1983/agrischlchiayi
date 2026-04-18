# DEVELOPER-GUIDE.md - 嘉義國本學堂開發手冊

## 概述

本手冊提供常見開發任務的步驟指南，幫助開發者快速上手專案維護與功能開發。

## 環境設定

### 必要工具

- Node.js 18+
- Git
- VS Code (推薦)

### 本地開發設定

```bash
# 複製專案
git clone https://github.com/ahnchen1983/agrischlchiayi.git
cd agrischlchiayi

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

### 建置檢查

```bash
# 完整建置測試
npm run build

# 檢查是否有錯誤
npm run check
```

## 常見任務指南

### 1. 新增文章

#### 步驟

1. **選擇分類目錄**
   ```bash
   # 查看現有分類
   ls knowledge/
   ```

2. **建立新文章檔案**
   ```bash
   # 在對應分類目錄下建立 .md 檔案
   touch knowledge/Agri-Basics/new-article.md
   ```

3. **撰寫 frontmatter**
   ```yaml
   ---
   title: "文章標題"
   description: "簡短描述"
   date: "2026-04-18"
   tags: ["標籤1", "標籤2"]
   related: ["相關文章slug"]
   ---
   ```

4. **撰寫內容**
   - 使用 Markdown 語法
   - 支援 wikilinks: `[[相關文章]]`
   - 支援圖片: `![alt](圖片路徑)`

5. **驗證與建置**
   ```bash
   # 檢查 frontmatter
   ./scripts/core/sync.sh

   # 本地預覽
   npm run dev
   ```

#### 注意事項

- 檔案名稱將成為 URL slug
- 標題應簡潔有力
- 描述不超過 160 字元 (SEO 最佳化)

### 2. 新增分類

#### 步驟

1. **建立分類目錄**
   ```bash
   mkdir knowledge/New-Category
   ```

2. **建立分類首頁**
   ```bash
   touch knowledge/New-Category/_index.md
   ```

3. **編寫分類描述**
   ```yaml
   ---
   title: "新分類"
   description: "分類簡介"
   ---
   # 新分類

   這裡是分類的介紹內容...
   ```

4. **更新導覽 (如需要)**
   - 檢查 `src/components/CategoryNav.astro`
   - 確保新分類出現在導覽中

5. **測試路由**
   ```bash
   npm run dev
   # 訪問 /New-Category
   ```

### 3. 修改佈景主題

#### 步驟

1. **識別要修改的組件**
   ```bash
   # 查看佈景相關檔案
   find src/ -name "*Layout*" -o -name "*theme*"
   ```

2. **編輯 CSS / 樣式**
   - 全域樣式: `src/styles/global.css`
   - 組件樣式: 組件內的 `<style>` 區塊
   - Tailwind 類別: 直接在組件中使用

3. **測試視覺變更**
   ```bash
   npm run dev
   ```

4. **檢查響應式設計**
   - 在不同螢幕尺寸下測試
   - 使用瀏覽器開發者工具

#### 佈景檔案結構

```
src/
├── layouts/          # 頁面佈局
├── components/       # UI 組件
├── styles/           # 全域樣式
└── assets/           # 圖片、字體等資源
```

### 4. Debug 圖譜頁面

#### 常見問題

**圖譜不顯示**
```bash
# 檢查圖譜資料是否存在
ls public/api/graph.json

# 重新生成圖譜資料
python scripts/core/graph-data.py
```

**節點點擊無反應**
- 檢查 `src/components/Graph.tsx` 的 click handler
- 驗證 `BASE_URL` 正確設定

**資料載入錯誤**
```bash
# 檢查瀏覽器 console
# 確認 API 路徑正確
curl http://localhost:4321/api/graph.json
```

#### Debug 步驟

1. **檢查資料來源**
   ```bash
   cat public/api/graph.json | head -20
   ```

2. **驗證 D3.js 渲染**
   - 在 `graph.astro` 中加入 console.log
   - 檢查組件 props 傳遞

3. **測試連結導航**
   - 確保 `BASE_URL` 正確
   - 檢查路由設定

### 5. 本地預覽與測試

#### 開發模式

```bash
# 啟動熱重載開發伺服器
npm run dev

# 訪問 http://localhost:4321/agrischlchiayi/
```

#### 生產建置預覽

```bash
# 建置生產版本
npm run build

# 預覽建置結果
npm run preview
```

#### 測試檢查

```bash
# 型別檢查
npm run check

# Linting
npm run lint

# 格式化
npm run format
```

### 6. 更新搜尋索引

#### 手動更新

```bash
# 執行搜尋索引生成腳本
python scripts/core/search-index.py

# 檢查輸出
ls public/api/search.json
```

#### 自動化

搜尋索引會在 `npm run build` 時自動生成。如需手動觸發：

```bash
./scripts/core/postbuild.sh
```

### 7. 處理 Wikilinks

#### 語法

- 內部連結: `[[文章標題]]`
- 分類連結: `[[Category/文章標題]]`

#### 驗證

```bash
# 檢查失效連結
./scripts/core/sync.sh --check-links
```

#### 自訂解析邏輯

編輯 `plugins/remark-wikilinks.mjs` 以修改解析行為。

### 8. 新增 API 端點

#### 步驟

1. **建立 API 檔案**
   ```bash
   touch src/pages/api/new-endpoint.json.ts
   ```

2. **實作端點邏輯**
   ```typescript
   export async function GET() {
     // API 邏輯
     return new Response(JSON.stringify(data), {
       headers: { 'Content-Type': 'application/json' }
     });
   }
   ```

3. **測試端點**
   ```bash
   curl http://localhost:4321/api/new-endpoint.json
   ```

### 9. 部署到 GitHub Pages

#### 自動部署

推送至 `main` 分支會自動觸發 GitHub Actions 部署。

#### 手動部署

```bash
# 建置
npm run build

# 部署 (需要 gh CLI)
gh workflow run deploy.yml
```

#### 部署檢查

- 確認 `BASE_URL` 設定正確
- 測試所有頁面連結
- 驗證搜尋與圖譜功能

## 故障排除

### 建置失敗

```bash
# 清除快取
rm -rf node_modules/.astro
npm run build
```

### 連結錯誤

```bash
# 檢查 BASE_URL
grep -r "BASE_URL" src/
```

### 內容不同步

```bash
# 重新同步
./scripts/core/sync.sh
npm run build
```

## 進階主題

- [SITE-MAP.md](SITE-MAP.md) - 網站功能地圖
- [ARCHITECTURE.md](ARCHITECTURE.md) - 完整系統架構
- [ONBOARDING.md](ONBOARDING.md) - 新人學習檔案
- `docs/design/` - 設計文件