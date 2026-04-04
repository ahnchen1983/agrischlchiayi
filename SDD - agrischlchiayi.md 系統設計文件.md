# SDD - agrischlchiayi 系統設計文件

## 1. 專案基本資訊

- **專案名稱**：嘉義國本學堂
- **Repo 名稱**：`agrischlchiayi`
- **GitHub Repo**：https://github.com/ahnchen1983/agrischlchiayi
- **更新日期**：2026-04-05
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
- `10` 大農業主類別頁
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

## 5. 實際目錄結構（摘要）

```text
agrischlchiayi/
├── knowledge/              # Markdown 內容 SSOT
├── src/
│   ├── components/         # UI 元件
│   ├── content/zh-TW/      # 給 Astro 使用的內容投影
│   ├── pages/              # 路由頁面
│   ├── templates/          # 大型頁面模板
│   ├── i18n/               # 文案與語系工具
│   └── lib/utils/          # 共用邏輯
├── scripts/core/           # 建置、同步、索引生成
├── public/api/             # 前端讀取的資料 API
├── docs/                   # 文件與工作流說明
├── astro.config.mjs
├── README.md
└── CONTRIBUTING.md
```

## 6. 與原始設計的符合度

| 項目                 | 狀態 | 說明                         |
| -------------------- | ---- | ---------------------------- |
| Markdown 為主體      | ✅   | `knowledge/` 為 SSOT         |
| 圖譜探索             | ✅   | `/graph` 可正常建置          |
| 分類式知識入口       | ✅   | 已有 10 大類別               |
| GitHub Pages 部署    | ✅   | `npm run build` 已驗證通過   |
| Base path 正確處理   | ✅   | 已補強 `BASE_URL` 用法       |
| 專案 branding 一致性 | ⚠️   | 仍有部分 fork 遺留文字待整理 |

## 7. 近期優先事項

1. 持續把 `Taiwan.md` 遺留文案收斂為「嘉義國本學堂」
2. 補齊農業專屬 About / Contribute 內容
3. 擴充 `knowledge/` 條目、索引頁與來源品質
4. 規範多語系與 SEO 策略

## 8. 成功標準

- 使用者能透過首頁、分類頁與圖譜快速找到農業知識
- `knowledge/` 與網站輸出保持一致，不產生幽靈內容
- GitHub Pages 子路徑部署下，所有內部連結與資產都正常
- 新貢獻者能依 `README` 與 `CONTRIBUTING.md` 直接參與
