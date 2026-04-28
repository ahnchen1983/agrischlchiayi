# DEVELOPER-GUIDE — 開發手冊

> 本文件是任務級操作手冊：怎麼跑專案、怎麼做常見變更、出問題怎麼排查。
> 系統架構與設計決策請見 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 1. 快速啟動

### 1.1 環境需求

- **Node.js**：22+（CI 用 Node 22，本地建議一致）
- **Git**：2.0+
- **bash / Python 3**：部分腳本與 hooks 需要
- **VS Code**（推薦）

### 1.2 第一次啟動

```bash
git clone https://github.com/ahnchen1983/agrischlchiayi.git
cd agrischlchiayi
npm install
npm run dev
```

開啟 http://localhost:4321/agrischlchiayi/ 應看到首頁。

### 1.3 第一次驗證 hooks

剛 clone 下來時，請確認 git hooks 有執行權限（否則 pre-commit / commit-msg 會被靜默跳過）：

```bash
chmod +x .husky/pre-commit .husky/commit-msg
ls -l .husky/pre-commit .husky/commit-msg   # 應顯示 x 權限
```

### 1.4 5 分鐘導覽

| 路徑 | 用途 |
|---|---|
| `/` | 首頁、分類導覽、搜尋 |
| `/[category]/` | 分類首頁，例如 `/crop-production/` |
| `/[category]/[slug]/` | 文章頁 |
| `/graph` | 知識圖譜（D3.js） |
| 搜尋（Ctrl+K） | MiniSearch 全文搜尋 |

## 2. 專案結構速查

```
agrischlchiayi/
├── knowledge/          # ⭐ 內容 SSOT，所有文章從這裡開始改
├── src/
│   ├── pages/          # 路由
│   ├── components/     # .astro 元件
│   ├── layouts/        # Layout.astro（唯一）
│   ├── templates/      # 大型頁面模板
│   └── content/zh-TW/  # 由 sync.sh 從 knowledge/ 產生（勿直接編輯）
├── scripts/
│   ├── core/           # 建置管線
│   └── tools/          # 維運工具（去識別化、wikilink 驗證等）
├── public/api/         # build 期產出的 JSON API
├── docs/               # 本資料夾
└── .husky/             # Git hooks
```

完整職責對照表見 [ARCHITECTURE.md §5](ARCHITECTURE.md#5-目錄結構)。

## 3. 常用指令

| 指令 | 用途 |
|---|---|
| `npm run dev` | 啟動開發伺服器（hot reload） |
| `npm run sync` | 從 `knowledge/` 重建 `src/content/zh-TW/` |
| `npm run build` | 建置生產版本到 `dist/` |
| `npm run preview` | 預覽已建置的 `dist/` |
| `npm test` | frontmatter 驗證 |
| `npm run check-images` | 檢查圖片參考是否存在 |
| `npm run check-links` | 檢查內部連結與 wikilinks |
| `npm run format::write` | prettier 格式化 |

## 4. 常見任務

### 4.1 新增文章

```bash
# 1. 選擇分類目錄（13 選 1，見 CATEGORY-MAPPING.md）
ls knowledge/

# 2. 建立 .md 檔（檔名會成為 URL slug）
touch knowledge/Agri-Basics/my-article.md
```

最小 frontmatter：

```yaml
---
title: '文章標題'
description: '一句話摘要（≤ 160 字元）'
date: 2026-04-28
tags: ['國本學堂', '相關標籤']
subcategory: '子分類'
level: '初階'        # 初階 / 進階 / 卓越
status: 'published'  # draft / published / archived
---
```

完整 schema 見 [../CONTRIBUTING.md](../CONTRIBUTING.md)。

驗證與預覽：

```bash
npm test            # frontmatter 驗證
npm run sync        # 同步到 src/content/zh-TW
npm run dev         # 本地預覽
```

### 4.2 新增分類

新增 `knowledge/New-Category/` 目錄與 `_index.md`，並確認：

- `astro.config.mjs` / Content Collections schema 是否需要更新（見 `src/content.config.ts`）
- `cli/src/lib/` 中分類常數（如有）需同步
- `docs/CATEGORY-MAPPING.md` 補上分類定義

### 4.3 撰寫 Wikilinks

語法：

```markdown
相關主題請參考 [[土壤基礎知識]] 與 [[水資源管理入門]]。
```

注意事項：

- 解析由 [plugins/remark-wikilinks.mjs](../plugins/remark-wikilinks.mjs) 實作
- **不要在清單項中使用** `- [[X]]`，會渲染異常；改用 `- [X](/url)`
- 提交前 pre-commit hook 會跑 wikilink 驗證

### 4.4 修改佈景與元件

| 範圍 | 位置 |
|---|---|
| 全域樣式 | `src/styles/global.css` |
| 元件樣式 | 各 `.astro` 內 `<style>` 區塊 |
| Tailwind | 直接在元件中以 class 使用 |
| Layout | `src/layouts/Layout.astro` |
| 共用元件 | `src/components/*.astro`（16 個） |

> 內部連結請用 `import.meta.env.BASE_URL`，不要寫死 `/...`。

### 4.5 新增 API 端點

```bash
touch src/pages/api/my-endpoint.json.ts
```

```ts
export async function GET() {
  const data = { hello: 'world' };
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

驗證：

```bash
npm run dev
curl http://localhost:4321/agrischlchiayi/api/my-endpoint.json
```

### 4.6 知識圖譜開發

圖譜由 [src/pages/graph.astro](../src/pages/graph.astro) 渲染，掃描 `knowledge/` 的 frontmatter（`tags`、`crop`、`tech`）與 wikilinks 構建節點與邊。

| 症狀 | 排查 |
|---|---|
| 圖譜空白 | 檢查瀏覽器 console；驗證 `frontmatter` 完整；確認 D3.js 載入 |
| 節點點擊無反應 | 檢查 `BASE_URL`；驗證目標 URL 存在 |
| 邊數量異常 | 檢查 wikilinks 解析；驗證 `tags`/`crop`/`tech` 欄位 |

調整視覺化參數請編輯 `graph.astro` 內的 D3 force 設定。

### 4.7 搜尋功能調整

搜尋由 [scripts/core/build-search-index.mjs](../scripts/core/build-search-index.mjs) 在 build 期生成 MiniSearch 索引，由前端載入。

```bash
# 手動重建索引
node scripts/core/build-search-index.mjs

# 驗證
ls -lh public/api/search-minisearch.json
```

調整 boost 加權：編輯 `src/layouts/Layout.astro` 中的 `_doSearch()`：

```js
boost: { title_bigram: 6, tags_bigram: 4, desc_bigram: 2 }
```

### 4.8 部署到 GitHub Pages

push 到 `main` 會自動觸發 [.github/workflows/deploy.yml](../.github/workflows/deploy.yml)。完整步驟見 [ARCHITECTURE.md §8](ARCHITECTURE.md#8-部署流程與-git-hooks)。

部署前自查：

- [ ] `npm test` 通過
- [ ] `npm run build` 成功
- [ ] 本地 `npm run preview` 檢查連結與資源
- [ ] commit message 符合去識別化規範（見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)）

## 5. 故障排除

### 5.1 建置失敗

```bash
rm -rf node_modules/.astro
npm run build

# 仍失敗：完全重裝
rm -rf node_modules package-lock.json
npm install && npm run build
```

### 5.2 內容同步異常

```bash
# 確認 knowledge/ 與 src/content/zh-TW/ 一致
npm run sync
git status src/content/zh-TW/   # 應無未追蹤差異（src/content/ 在 .gitignore）
```

提醒：**直接編輯 `src/content/zh-TW/` 會在下次 sync 被覆寫**。

### 5.3 BASE_URL 連結 404

```bash
# 檢查是否有寫死 / 開頭的連結
grep -rn 'href="/[a-z]' src/ | grep -v 'BASE_URL'
grep -rn 'src="/[a-z]' src/ | grep -v 'BASE_URL'
```

修正：改用 `${import.meta.env.BASE_URL}path` 或 wikilink。

### 5.4 搜尋失效

```bash
node scripts/core/build-search-index.mjs
ls -lh public/api/search-minisearch.json     # 應有合理大小
```

若仍空白，檢查瀏覽器 Network 面板看 `search-minisearch.json` 是否成功載入。

### 5.5 圖譜空白

```bash
# 確認 knowledge/ 文章有 tags
grep -L "^tags:" knowledge/**/*.md   # 列出沒 tags 的檔案
```

D3 載入失敗：檢查瀏覽器 console。

### 5.6 部署後 404

- `astro.config.mjs` 的 `base` 必為 `/agrischlchiayi`
- GitHub Pages 設定：Settings → Pages → Source = GitHub Actions
- 檢查 [deploy.yml](../.github/workflows/deploy.yml) 最近一次 run 是否成功

### 5.7 Pre-commit hook 沒生效

```bash
# 檢查執行權限
ls -l .husky/pre-commit .husky/commit-msg

# 補上權限
chmod +x .husky/pre-commit .husky/commit-msg
```

### 5.8 commit message 被擋

去識別化檢查（[scripts/tools/deidentification-check.py](../scripts/tools/deidentification-check.py)）會比對雜湊清單。若 commit message 含敏感姓名/檔名會被擋。

修正：改用通用描述（如 `docs: update internal farmer data documentation`）。完整規範見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

## 6. 學習路徑（給新貢獻者）

依角色挑一條：

### 路徑 A — 內容貢獻者（4-6 小時）

1. 看 [../README.md](../README.md) 與 [../CONTRIBUTING.md](../CONTRIBUTING.md)
2. 跑通 §1 快速啟動
3. 開一篇現有文章來看 frontmatter 結構
4. 試新增一篇測試文章（§4.1）
5. 看 [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) 了解分類定義
6. 若涉及農友資料，務必先讀 [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) 與 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)

### 路徑 B — 功能開發者（6-10 小時）

1. 看 [ARCHITECTURE.md](ARCHITECTURE.md) §3-§7（資料流、目錄、路由、建置）
2. 跑通 §1 快速啟動
3. 試改一個元件（§4.4）並 hot reload 觀察
4. 試新增一個 API 端點（§4.5）
5. 看 [ARCHITECTURE.md §9](ARCHITECTURE.md#9-已知陷阱)（已知陷阱）

### 路徑 C — 全棧貢獻者（12+ 小時）

走完路徑 A + B，再讀：

- [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) — 農友資料整合架構
- [ARCHITECTURE.md §10](ARCHITECTURE.md#10-設計決策why) — 設計決策的 Why
- `scripts/tools/` 各工具腳本

## 7. 學習資源

- [Astro 官方文件](https://docs.astro.build/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [D3.js Getting Started](https://d3js.org/getting-started)
- [MiniSearch](https://lucaong.github.io/minisearch/)

## 8. 相關文件

- [ARCHITECTURE.md](ARCHITECTURE.md) — 系統架構（SDD）
- [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) — 13 大分類定義
- [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) — 農友資料整合架構
- [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) — 農友資料處理流程
- [../README.md](../README.md) — 專案總覽
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — 投稿指南
- [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — 去識別化政策
