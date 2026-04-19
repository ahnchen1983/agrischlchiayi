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

### 4. 知識圖譜開發

#### 圖譜系統概述

知識圖譜由以下組件組成：
1. **圖譜資料生成**：`src/pages/graph.astro` 掃描 knowledge/ 目錄，從 frontmatter 與 wikilinks 構建節點和邊
2. **D3.js 視覺化**：Force-directed graph，支援拖動、縮放、點擊
3. **圖譜頁面 UI**：`src/pages/graph.astro` 渲染 HTML + inline D3 script

#### 圖譜優化路線圖

**P1：互動式圖譜增強**（8-10 小時）
- 實現 click-to-navigate：點擊節點跳轉到文章
- 實現 hover tooltip：懸停節點顯示標題與簡短描述
- 實現 double-click focus：雙擊節點隔離其相鄰節點（星形視圖）
- 實現拖動重排：用戶可拖動節點改變布局

**P2：自動圖譜生成**（4-5 小時）
- 解析 Wikilinks `[[Article Title]]` 語法
- 從標籤、作物、技術標籤自動生成邊
- 動態節點大小（基於出度/入度）
- 圖譜去重與優化

**P3：圖譜統計與分析**（5-6 小時）
- 計算節點中心性（Betweenness、Closeness、Degree）
- 識別社群（Clustering 算法）
- 路徑分析（最短路徑、相似度）
- 產生統計面板（最重要的文章、知識孤島等）

#### 圖譜資料結構

```javascript
// 節點格式
{
  id: "crop-production/小黃瓜",      // category/slug
  label: "小黃瓜設施栽培技術",
  group: "crop-production",           // 分類
  size: 8,                            // 基於出度
  tags: ["設施", "小黃瓜"]
}

// 邊格式
{
  source: "crop-production/小黃瓜",
  target: "smart-farming/IoT灌溉",
  label: "技術關聯"                   // tag_shared, crop_shared, etc
}
```

#### Debug 圖譜頁面

**圖譜不顯示**
```bash
# 檢查圖譜是否正確渲染
npm run build
grep -c "nodes.push" dist/graph/index.html

# 檢查瀏覽器 console 是否有 D3.js 錯誤
```

**節點點擊無反應**
- 檢查 `src/pages/graph.astro` 中的 click event listener
- 驗證 `BASE_URL` 正確設定
- 檢查目標文章 URL 是否有效

**邊與節點數量不對**
- 驗證 wikilinks 解析邏輯
- 檢查 frontmatter 中 tags、crop、tech 字段是否完整
- 檢查去重邏輯

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

### 6. 搜尋功能開發

#### 搜尋系統架構

搜尋功能由三部分組成：
1. **搜尋索引生成**（build 時）：`scripts/core/build-search-index.mjs`
2. **前端搜尋引擎**（執行時）：MiniSearch 或 fallback indexOf
3. **搜尋 UI**（HTML/CSS）：`src/components/Header.astro` 中的搜尋模態框

#### 生成搜尋索引

```bash
# 自動生成（npm run build 時執行）
npm run build

# 手動重新生成
node scripts/core/build-search-index.mjs

# 驗證輸出
cat public/api/search-minisearch.json | head -50
```

#### 搜尋結果優化任務

**P1：改進搜尋排序**
- 編輯 `src/layouts/Layout.astro` 中的 `_doSearch()` 函數
- 調整 MiniSearch 的 boost 加權：`{ title_bigram: 6, tags_bigram: 4, desc_bigram: 2 }`
- 實現自訂評分函數考慮相關性、新鮮度、人氣度

**P2：搜尋自動補全**
- 從搜尋索引提取熱門術語（按搜尋頻率或農業重要性排序）
- 在 `Layout.astro` 中實現 autocomplete dropdown
- 示例熱門術語：「小黃瓜」「IoT 灌溉」「設施農業」等

**P3：搜尋分析**
- 記錄用戶搜尋詞（可選，涉及隱私）
- 追蹤點擊率最高的文章
- 產生月度搜尋報告

#### 搜尋流程圖

```
用戶輸入 "小黃瓜"
    ↓
_doSearch(q, lang)
    ↓
MiniSearch.search("小|黃|瓜", prefix=true, limit=200)
    ↓
評分排序（title > tags > desc）、語言優先
    ↓
取前 30 結果
    ↓
_renderResult() 渲染 HTML
    ↓
顯示在 search-results 區域
```

#### 常見搜尋 Bug

- **CJK 分詞失敗**：檢查 bigram tokenizer 是否正確
- **搜尋結果為空**：驗證 search-minisearch.json 是否包含預期數據
- **自動補全無效**：確認 autocomplete 列表已從索引生成

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

### 9. 農民耕作資料整合

#### 農民數據處理工作流

本專案包含 73 份來自嘉義國本學堂課程學員的農民經營計畫書（位於 `source/` 目錄）。通過系統化處理，可轉化為 70-80 篇去識別化的農業知識文章。

#### 處理步驟

1. **從農友數據中識別知識點**
   - 瀏覽 `source/` 中的農友檔案
   - 找出 3 個以上農友的共同問題（作物、技術、經營模式）
   - 記錄農友樣本數與共同點

2. **去識別化資訊提取**
   - ✅ **保留**：作物類型、規模、成本結構、技術、銷售策略、營運模式
   - ❌ **移除**：農友姓名、聯絡方式、農場詳細地址、家庭信息

3. **撰寫標準化文章**
   - 標題：「作物 + 技術/策略」（例：「小黃瓜設施栽培技術指南」）
   - Frontmatter：填入 crop、tech、tags、level
   - 內容結構：
     - 前言（問題與機會）
     - 案例段落（基於去識別化農友數據）
     - 實務步驟（作業指南）
     - 成本與效益分析
     - 常見困境與解決方案
     - 檢查清單

4. **發布與連接**
   ```bash
   # 新增文章
   touch knowledge/Crop-Production/小黃瓜設施栽培技術指南.md
   
   # 編輯 frontmatter 與內容
   vim knowledge/Crop-Production/小黃瓜設施栽培技術指南.md
   
   # 同步與驗證
   ./scripts/core/sync.sh
   npm run build
   npm run dev
   ```

#### 優先級與估工

| 優先級 | 主題 | 預估工時 | 農友樣本 | 狀態 |
|--------|------|----------|---------|------|
| P1 | 小黃瓜栽培技術 | 4h | 5+ | 待製作 |
| P1 | IoT 灌溉導入指南 | 4h | 3+ | 待製作 |
| P1 | 嘉義四季耕作節奏 | 3h | 10+ | 待製作 |
| P2 | 蝴蝶蘭種苗生產 | 3.5h | 2+ | 待製作 |
| P2 | 農產品認證與品牌建立 | 4h | 3+ | 待製作 |

#### 使用參考文件

- [FARMER-DATA-PROCESSING-CHECKLIST.md](FARMER-DATA-PROCESSING-CHECKLIST.md) - 6 步處理清單
- [DEIDENTIFICATION-CHECKLIST.md](DEIDENTIFICATION-CHECKLIST.md) - 隱私保護規範
- [CATEGORY-MAPPING-GUIDE.md](CATEGORY-MAPPING-GUIDE.md) - 分類對應指南
- [FARMER-DATA-UTILIZATION-PLAN.md](FARMER-DATA-UTILIZATION-PLAN.md) - 完整批量處理計劃

### 11. 部署到 GitHub Pages

#### 自動部署

推送至 `main` 分支會自動觸發 GitHub Actions 部署。

#### 手動部署

```bash
# 建置
npm run build

# 部署 (需要 gh CLI)
gh workflow run deploy.yml
```

#### 部署檢查清單

- [ ] 確認 `BASE_URL` 設定為 `/agrischlchiayi`
- [ ] 測試所有頁面連結（內部與外部）
- [ ] 驗證搜尋功能（關鍵字搜尋、結果排序）
- [ ] 驗證圖譜功能（節點點擊、懸停提示）
- [ ] 檢查圖片與資源加載
- [ ] 檢查移動設備適配（iOS Safari, Android Chrome）
- [ ] 驗證分析數據（GA4、錯誤追蹤）

## 故障排除

### 建置失敗

```bash
# 清除 Astro 快取
rm -rf node_modules/.astro
npm run build

# 清除所有依賴並重新安裝
rm -rf node_modules package-lock.json
npm install && npm run build
```

### 連結錯誤

```bash
# 檢查 BASE_URL 設定
grep -r "BASE_URL" src/astro.config.mjs

# 檢查相對連結
grep -r "href=\"/[^/]" src/
```

### 內容不同步

```bash
# 檢查 knowledge/ 與 src/content/zh-TW/ 是否同步
./scripts/core/sync.sh --verify

# 強制重新同步
./scripts/core/sync.sh --force
npm run build
```

### 搜尋功能失效

```bash
# 重新生成搜尋索引
node scripts/core/build-search-index.mjs

# 驗證索引大小
ls -lh public/api/search-*.json

# 檢查瀏覽器 console 中的 MiniSearch 載入錯誤
```

### 圖譜頁面空白

```bash
# 驗證 frontmatter 完整性
grep -r "^tags:" src/content/zh-TW/

# 檢查 D3.js 是否載入
curl -s http://localhost:4321/agrischlchiayi/graph | grep "d3@"

# 檢查瀏覽器開發者工具中是否有 JS 錯誤
```

### 部署後 404

```bash
# 驗證 GitHub Pages 設定
# Settings → Pages → Source 應設為 "Deploy from a branch"
# Branch 應為 "gh-pages"

# 檢查 dist/ 目錄是否正確部署
ls -la dist/index.html
```

### 效能問題

```bash
# 檢查建置時間
time npm run build

# 測試頁面加載速度
# Chrome DevTools → Lighthouse → 檢查分數

# 分析資源大小
npm run build && du -sh dist/
```

## 進階主題

- [SITE-MAP.md](SITE-MAP.md) - 網站功能與頁面地圖
- [ARCHITECTURE.md](ARCHITECTURE.md) - 完整系統架構與決策說明
- [ONBOARDING.md](ONBOARDING.md) - 新貢獻者上手指南
- [DOCUMENTATION-AND-OPTIMIZATION-PLAN.md](DOCUMENTATION-AND-OPTIMIZATION-PLAN.md) - 搜尋與圖譜優化路線圖
- `docs/design/` - UI/UX 設計文件