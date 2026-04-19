# 系統文檔與搜尋優化規劃
# (Documentation & Search Optimization Master Plan)

**版本**: 1.0  
**日期**: 2026-04-19  
**目的**: 完善系統文檔與優化搜尋功能、知識圖譜

---

## 📚 第一部分：系統文檔完善

### 當前狀態

✅ 已有：
- WORKFLOW-TRIGGER-GUIDE.md (800+ 行) — 工作流觸發指南
- CATEGORY-MAPPING-GUIDE.md (351 行) — 分類對應指南  
- FARMER-DATA-PROCESSING-CHECKLIST.md (304 行) — 農友數據處理檢查清單
- DEIDENTIFICATION-CHECKLIST.md (405 行) — 去識別化檢查清單
- CONTENT-RESTRUCTURING-PLAN.md (800+ 行) — 內容重組計劃
- FARMER-DATA-UTILIZATION-PLAN.md (350+ 行) — 農友數據利用計劃

❌ 缺少：
- ARCHITECTURE.md — 系統架構與技術決策
- DEVELOPER-GUIDE.md — 開發者工作流程
- ONBOARDING.md — 新貢獻者上手指南
- SITE-MAP.md — 網站結構與路由表
- design/CONTENT-PIPELINE.md — 內容流程（knowledge → content → pages）
- design/SEARCH-SYSTEM.md — 搜尋系統設計
- design/GRAPH-SYSTEM.md — 知識圖譜設計

### 優先級 1：核心文檔（第1週）

#### 📄 **ARCHITECTURE.md** (400-500 行)

**涵蓋內容**：
```
1. 系統概覽
   - 本專案是什麼？(农业知识平台)
   - 技术栈 (Astro, D3.js, MiniSearch)
   - 部署方式 (GitHub Pages, /agrischlchiayi 子路徑)

2. 核心架構層
   ├─ Content Layer (知識內容)
   │  └─ knowledge/ (source of truth)
   │
   ├─ Sync Layer (同步)
   │  └─ src/content/zh-TW/ (投影層)
   │
   ├─ Build Layer (構建)
   │  └─ dist/ (靜態網站)
   │
   └─ Search & Graph Layer
      ├─ search-index.json
      ├─ search-minisearch.json
      └─ D3.js graph

3. 資料流完整路徑
   knowledge/Crop-Production/小番茄栽培.md
     ↓ (npm run sync)
   src/content/zh-TW/crop-production/小番茄栽培.md
     ↓ (astro build → prebuild: generate-api.js)
   dist/crop-production/小番茄栽培/index.html
   public/api/search-index.json (已索引)

4. Frontmatter 標準格式
   ```yaml
   title: 文章標題
   description: 一句話描述
   tags: [tag1, tag2, tag3]
   level: 初階|進階|卓越
   crop: [作物1, 作物2]
   tech: [技術1, 技術2]
   source: 來源
   ```

5. 已知陷阱與解決方案
   - BASE_URL: ${import.meta.env.BASE_URL} 用於 GitHub Pages /agrischlchiayi
   - Husky PATH: 確保 node_modules/.bin 在 PATH
   - D3.js graph: 需要 SVG viewBox 正確設置
   - CJK 搜尋: MiniSearch 需要 bigram 分詞

6. 技術決策記錄
   - 為什麼選 Astro? (靜態站點, 快速構建, 支持多框架)
   - 為什麼 knowledge/ SSOT? (版本控制, 去識別化在 git 中可見)
   - 為什麼 MiniSearch? (離線全文搜尋, CJK 支持)
```

**預期時間**: 4 小時

---

#### 📄 **DEVELOPER-GUIDE.md** (500-600 行)

**涵蓋內容**：
```
1. 環境設置
   - Node 版本要求 (22.12.0+)
   - npm install 步驟
   - 本地開發 (npm run dev)
   - 預覽構建 (npm run preview)

2. 常見開發任務
   
   a) 新增一篇文章
      步驟:
      1. 在 knowledge/[Category]/ 創建 .md
      2. 編寫 frontmatter (title, description, tags, etc.)
      3. 編寫內容 (支持 Wikilinks [[Article Title]])
      4. 運行 npm run sync (同步到 src/content/)
      5. npm run dev 本地預覽
      6. npm run test 驗證 frontmatter
      7. git add, git commit, git push
      8. GitHub Pages 自動部署

   b) 新增一個分類
      步驟:
      1. 在 knowledge/ 創建新分類目錄
      2. 在 src/consts.ts 或 config 中註冊
      3. 創建 Hub 文件: _[Category]-Hub.md
      4. npm run sync && npm run build
      5. 測試路由 /[category-slug]/

   c) 更新搜尋索引
      步驟:
      1. 編輯 knowledge 中的文件
      2. npm run sync (同步內容)
      3. npm run build (觸發 prebuild → generate-api.js → build-search-index.mjs)
      4. 清除瀏覽器快取 (Cmd+Shift+R)

   d) 調試 D3 知識圖譜
      步驟:
      1. 修改 src/pages/index.astro 中的圖譜配置 (nodes, edges)
      2. npm run dev 實時預覽
      3. 檢查瀏覽器 DevTools (Network, Console)
      4. 注意 viewBox 尺寸對應 SVG 實際寬高

3. 構建流程詳解
   
   npm run build 執行：
   ├─ prebuild (npm run test, generate-api.js, build-search-index.mjs)
   ├─ astro build (編譯 Astro 頁面)
   ├─ postbuild (post-build-check.mjs)
   └─ 生成靜態文件到 dist/

   每個 stage 的職責:
   - prebuild: 驗證 frontmatter, 生成搜尋索引, 生成 API
   - astro build: 渲染 .astro 頁面, 處理路由, 優化資源
   - postbuild: 驗證構建成果 (頁數, 分類健康度)

4. 文件組織慣例
   ```
   knowledge/
   ├─ Crop-Production/
   │  ├─ _Crop-Production-Hub.md (分類首頁)
   │  ├─ 小番茄栽培技術.md
   │  └─ 百香果種植指南.md
   │
   src/
   ├─ pages/
   │  ├─ index.astro (首頁)
   │  ├─ graph.astro (知識圖譜)
   │  └─ [category]/index.astro (分類頁)
   │
   scripts/core/
   ├─ sync.sh (同步 knowledge → src/content)
   ├─ build-search-index.mjs (構建搜尋索引)
   ├─ generate-api.js (生成 API 終點)
   └─ post-build-check.mjs (構建驗證)
   ```

5. 除錯技巧
   - Frontmatter 錯誤: npm run test (驗證格式)
   - 搜尋不工作: 檢查 public/api/search-index.json 是否存在
   - 圖譜顯示異常: 檢查瀏覽器 console 是否有 D3 報錯
   - BASE_URL 問題: 本地 / 對應 GitHub Pages /agrischlchiayi

6. CI/CD 流程
   - GitHub Actions 觸發: push main 分支
   - 執行: npm run sync && npm run build
   - 部署: dist/ 自動發布到 GitHub Pages
```

**預期時間**: 4.5 小時

---

#### 📄 **ONBOARDING.md** (400-450 行)

**涵蓋內容**：
```
# 新貢獻者上手指南 (0→1 在 30 分鐘內)

## 第 1 步：環境設置 (5 分鐘)
- Clone repo
- npm install
- npm run dev
- 瀏覽 http://localhost:3000/agrischlchiayi

## 第 2 步：理解結構 (10 分鐘)
- knowledge/ (52 篇文章, 10 個分類)
- src/pages/ (Astro 頁面)
- scripts/core/ (構建流程)

## 第 3 步：你的第一篇文章 (15 分鐘)

a) 創建文件
   touch knowledge/Crop-Production/新文章.md

b) 複製範本
   ```markdown
   ---
   title: '文章標題'
   description: '簡短描述'
   date: 2026-04-19
   tags: [標籤1, 標籤2]
   level: '進階'
   crop: ['作物']
   tech: ['技術']
   source: '來源'
   status: 'published'
   ---

   ## 簡介
   
   ## 核心內容
   
   ## Wikilinks 範例
   [[農作物病徵診斷指南]]
   ```

c) 同步與預覽
   npm run sync
   npm run dev

d) 提交
   git add knowledge/Crop-Production/新文章.md
   git commit -m "content: add new article"

## 常見問題
- Q: 如何添加到分類?
  A: 自動的, 放入對應分類目錄即可

- Q: 如何連接其他文章?
  A: [[文章標題]] 語法, Wikilinks

- Q: 如何去識別化農友案例?
  A: 參考 DEIDENTIFICATION-CHECKLIST.md
```

**預期時間**: 3 小時

---

#### 📄 **SITE-MAP.md** (300-400 行)

**涵蓋內容**：
```
# 網站結構與路由表

## 頁面總覽

### 首頁與導航
- / (首頁)
  - 首屏: HeroSection (品牌)
  - ReadingPath (7篇入門文章)
  - Categories (10大分類)
  - Recent Updates (最新更新)

### 分類頁面 (10 個)
- /agri-basics/ (農業基礎)
- /agri-advanced/ (進階實務)
- /farm-management/ (農場經營)
- /crop-production/ (作物生產)
- /facility-farming/ (設施農業)
- /smart-farming/ (智慧農業)
- /agri-marketing/ (農產銷售)
- /grants-planning/ (補助計劃)
- /field-visits/ (場域交流)
- /livestock-health/ (畜牧健康)

### 文章頁面
- /[category]/[slug]/ (文章詳頁)
  - 包含: 目錄、內容、Wikilinks、延伸閱讀

### 特殊頁面
- /graph (知識圖譜) — D3.js 互動圖
- /about (關於)
- /contribute (貢獻指南)
- /resources (資源)
- /changelog (更新日誌)

## API 終點

### 搜尋 API
- GET /api/search-index.json
  返回: 所有文章的標題、描述、標籤
  
- GET /api/search-minisearch.json
  返回: MiniSearch 已索引的全文搜尋資料

### OG 圖片
- /og/[category]/[slug]/index.html
  動態生成 OG 預覽圖

## 路由命名慣例
- Category slug: kebab-case (agri-basics, farm-management)
- Article slug: url-encoded 文章標題
- 全部小寫, 支援中文 URI

## 靜態資源
- public/ (靜態檔案)
  ├─ api/ (搜尋索引)
  ├─ og/ (OG 預覽圖)
  └─ assets/ (圖片等)

- dist/ (構建輸出, GitHub Pages 發布)
```

**預期時間**: 2.5 小時

---

### 優先級 2：設計文檔（第2週）

#### 📄 **design/CONTENT-PIPELINE.md** (300 行)

詳解：knowledge → src/content → dist → public/api 的完整流程

#### 📄 **design/SEARCH-SYSTEM.md** (250 行)

詳解：MiniSearch 實現、CJK 分詞、索引生成、搜尋前端

#### 📄 **design/GRAPH-SYSTEM.md** (250 行)

詳解：D3.js 知識圖譜、節點邊、交互、性能優化

---

## 🔍 第二部分：搜尋功能優化

### 當前搜尋實現分析

**現狀**:
- ✅ MiniSearch 全文搜尋（CJK 支持）
- ✅ 前端搜尋框（src/components/SearchInput.astro）
- ✅ 搜尋索引自動生成（build-search-index.mjs）
- ❌ 搜尋結果排序邏輯簡陋
- ❌ 沒有搜尋分析（用戶搜了什麼）
- ❌ 沒有搜尋建議（自動補全、熱門搜尋）
- ❌ 中文分詞可能不夠精準

### 優化方案

#### 🔴 **優先級 1：搜尋結果排序優化**

**目標**: 提升搜尋相關性

**實現**:
```
1. 基於字段權重的排序
   - 標題匹配: 權重 3.0
   - 描述匹配: 權重 2.0
   - 標籤匹配: 權重 1.5
   - 內容匹配: 權重 1.0

2. 基於上下文的排序
   - 同分類內優先
   - 同級別內優先 (進階文章對進階用戶)
   - 最近更新優先

3. 程式碼實現 (修改 SearchInput.astro)
   ```javascript
   const results = minisearch.search(query, {
     boost: { title: 3, description: 2, tags: 1.5 },
     processTerm: (term) => term.toLowerCase(),
   });
   
   // 後處理排序
   results.sort((a, b) => {
     // 標題精確匹配優先
     if (a.title.includes(query)) return -1;
     // 同分類優先
     if (a.category === userCategory) return -1;
     // 最後按相關度
     return b.score - a.score;
   });
   ```

4. 測試
   - 搜尋「小番茄」應返回小番茄相關文章最上面
   - 搜尋「灌溉」應返回 Smart-Farming 相關文章優先
   - 搜尋「農場」應返回 Farm-Management 優先
```

**預期時間**: 3-4 小時

---

#### 🟡 **優先級 2：搜尋自動補全與建議**

**目標**: 改善用戶體驗

**實現**:
```
1. 熱門搜尋詞 (基於分析)
   - 定期統計搜尋日誌
   - 提示「大多人搜尋: 小番茄, 灌溉, 補助」

2. 自動補全
   - 當用戶輸入「小」時, 建議「小番茄、小黃瓜」
   - 實現: Trie 結構或簡單的前綴匹配

3. 拼音搜尋 (可選)
   - 使用 opencc-js (已在 package.json 中)
   - 「xiaofanqie」自動轉換為「小番茄」
   - 支持簡體/繁體混搜
```

**預期時間**: 4-5 小時

---

#### 🟡 **優先級 3：搜尋分析與日誌**

**目標**: 理解用戶需求

**實現**:
```
1. 搜尋日誌收集
   - 記錄: 搜尋詞、結果數、點擊率
   - 存儲: public/api/search-analytics.json (簡單方案)
   - 或使用 Google Analytics 事件追蹤

2. 分析儀表板
   - 建立 /admin/search-analytics 頁面
   - 展示: 熱門搜尋詞、無結果搜尋、搜尋趨勢

3. 用途
   - 發現內容缺口（用戶搜不到 = 缺少這篇文章）
   - 改進分類架構
   - 優化首頁推薦
```

**預期時間**: 5-6 小時

---

## 🕸️ 第三部分：知識圖譜優化

### 當前知識圖譜實現分析

**現狀**:
- ✅ D3.js 力導向圖（src/pages/index.astro 中）
- ✅ 10 個分類節點 + 中心節點
- ✅ 基本的跨分類連線
- ❌ 沒有點擊交互（點擊節點應導航）
- ❌ 沒有邊的標籤（連線代表什麼關係？）
- ❌ 沒有動態節點（應該加入具體文章）
- ❌ 性能可能有問題（大型圖的渲染）

### 優化方案

#### 🔴 **優先級 1：完整知識圖譜頁面 (/graph)**

**目標**: 打造互動式知識地圖

**實現**:
```
1. 圖譜規模擴展
   當前: 10 分類 + 1 中心 = 11 個節點
   目標: 10 分類 + 重要文章 (30-50 篇) = 40-60 個節點

2. 節點類型
   - 紅色: 中心 (嘉義國本學堂)
   - 綠色: 分類 (10 個)
   - 藍色: 文章 (根據重要度篩選)
   - 金色: 農友案例 (可選)

3. 邊的含義
   - 實線: 直接相關 (Wikilinks)
   - 虛線: 間接相關 (同分類)
   - 粗線: 高相關度 (被引用多次)

4. 交互功能
   - 點擊節點: 導航到文章 /[category]/[slug]
   - 懸停節點: 顯示工具提示 (標題、描述)
   - 雙擊: 聚焦於該節點的子圖
   - 拖拽: 重新排列節點位置 (本地存儲)

5. 性能優化
   - 使用 Web Worker 計算物理模擬
   - 實現虛擬化 (只渲染可見節點)
   - 限制邊的數量 (根據相關度閾值)
   - 增量加載 (點擊時加載更多節點)

6. 視覺設計
   - 添加圖例 (節點類型、邊的含義)
   - 添加搜尋框 (在圖上搜尋)
   - 添加導出功能 (SVG, PNG, JSON)
   - 添加統計信息 (節點數、邊數、平均度數)
```

**預期時間**: 8-10 小時

---

#### 🟡 **優先級 2：知識圖譜自動生成**

**目標**: 從 Wikilinks 自動構建圖譜

**實現**:
```
1. 解析 Wikilinks
   - 掃描所有 knowledge/*.md 文件
   - 提取 [[Article Title]] 格式的連結
   - 建立文章 → 文章 的有向圖

2. 圖譜自動更新
   - npm run build 時自動生成
   - 生成 public/api/graph-data.json
   {
     "nodes": [
       { "id": "article-slug", "label": "文章標題", "category": "crop-production", "weight": 5 }
     ],
     "edges": [
       { "source": "article1", "target": "article2", "type": "wikilink" }
     ]
   }

3. 視覺化規則
   - 節點大小 = 被引用次數 (度數)
   - 邊顏色 = 邊的類型 (wikilink, same-category, etc.)
   - 節點位置 = D3 力模擬計算
```

**預期時間**: 4-5 小時

---

#### 🟢 **優先級 3：知識圖譜統計與分析**

**目標**: 理解知識庫結構

**實現**:
```
1. 統計指標
   - 中心度 (Centrality): 哪些文章最重要？
   - 聚類係數 (Clustering): 哪些文章容易聚在一起？
   - 路徑長度: 從一篇文章到另一篇的平均步數？

2. 分析應用
   - 找出孤立文章 (沒有連線的)
   - 找出樞紐文章 (連接多個分類的)
   - 找出知識缺口 (應該有連線但沒有)

3. 可視化
   - 建立 /admin/knowledge-graph-stats 分析頁
   - 展示圖譜統計、建議改進
```

**預期時間**: 5-6 小時

---

## 📋 執行時間表

### 第 1 週：核心文檔 (16-18 小時)
| 任務 | 預估 | 狀態 |
|------|------|------|
| ARCHITECTURE.md | 4h | ⬜ |
| DEVELOPER-GUIDE.md | 4.5h | ⬜ |
| ONBOARDING.md | 3h | ⬜ |
| SITE-MAP.md | 2.5h | ⬜ |
| **小計** | **14h** | |

### 第 2 週：設計文檔 + 搜尋優化 (18-20 小時)
| 任務 | 預估 | 狀態 |
|------|------|------|
| design/* (3 份文檔) | 3h | ⬜ |
| 搜尋排序優化 | 3-4h | ⬜ |
| 搜尋自動補全 | 4-5h | ⬜ |
| 搜尋分析日誌 | 5-6h | ⬜ |
| **小計** | **15-18h** | |

### 第 3 週：知識圖譜優化 (15-20 小時)
| 任務 | 預估 | 狀態 |
|------|------|------|
| 完整知識圖譜頁面 | 8-10h | ⬜ |
| 圖譜自動生成 | 4-5h | ⬜ |
| 圖譜統計分析 | 5-6h | ⬜ |
| **小計** | **17-21h** | |

**總計**: 46-59 小時 (可分布在 3-4 週內)

---

## 🎯 優先順序建議

### **立即開始（本週）**
1. ✅ ARCHITECTURE.md — 給自己和未來開發者的知識庫
2. ✅ DEVELOPER-GUIDE.md — 加速未來貢獻速度

### **第 2 週**
3. ✅ ONBOARDING.md — 吸引新貢獻者
4. ✅ SITE-MAP.md — 網站導航與路由清晰化
5. ✅ 搜尋排序優化 — 提升核心功能

### **第 3 週**
6. ✅ 搜尋自動補全 — 改善用戶體驗
7. ✅ 知識圖譜完整化 — 視覺化知識結構

### **選擇性**
8. 搜尋分析日誌 — 了解用戶行為
9. 圖譜自動生成 — 維護成本優化
10. 圖譜統計分析 — 發現知識缺口

---

## 💡 實施建議

### 分段執行
- 每天 4-5 小時投入
- 先完成優先級 1（文檔）再進行優化
- 完成一個模塊後馬上提交 git commit

### 並行工作
- 文檔撰寫時可同時研究搜尋實現
- 知識圖譜設計可同時進行
- 農友數據處理與系統優化可並行

### 驗證質量
- 文檔完成後由陌生人（或假想的新開發者）測試
- 搜尋優化後用真實查詢測試
- 知識圖譜優化後檢查性能（加載時間、交互流暢度）

---

## 📚 交付成果清單

### 完成後的成果
- ✅ 4 份核心文檔 (ARCHITECTURE, DEVELOPER-GUIDE, ONBOARDING, SITE-MAP)
- ✅ 3 份設計文檔 (CONTENT-PIPELINE, SEARCH-SYSTEM, GRAPH-SYSTEM)
- ✅ 優化的搜尋功能 (排序、自動補全、分析)
- ✅ 增強的知識圖譜 (交互、動態、統計)
- ✅ 更詳細的 README 和貢獻指南
- ✅ 新開發者 30 分鐘內上手能力

### 對項目的影響
- 📈 新貢獻者入門時間：2 小時 → 30 分鐘
- 📈 搜尋相關性改善：預期 +30-40%
- 📈 知識圖譜交互性：從靜態 → 完全交互
- 📈 系統可維護性：從隱性知識 → 顯式文檔
- 📈 開發效率：有完整指南後，新功能開發速度加快

---

## 🚀 下一步

1. **確認優先順序**: 是否按照建議順序執行？
2. **時間投入**: 每週預計投入多少小時？
3. **協作分工**: 是否需要分配給他人協作？
4. **里程碑**: 何時完成優先級 1, 2, 3？

準備好開始了嗎？🎯
