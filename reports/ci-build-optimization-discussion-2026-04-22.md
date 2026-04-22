---
title: CI build time 優化討論 — 除了 OG pipeline 還能壓哪裡
session: 2026-04-22 β
status: discussion (未執行，等首次 v3 CI 跑完才定優先序)
related:
  - reports/og-pipeline-patch-plan-2026-04-22.md
  - .github/workflows/deploy.yml
---

# CI build 優化討論

## 起點

OG pipeline v3 做完後（commit `d0b6d91a`），觀察者問：**「原本文章 → build page 能不能用類似概念優化？平行 worker + cache？」**

先討論再動，不盲 refactor。

---

## OG 產圖 vs Astro build 本質差異

| 面向                  | OG 產圖                                 | Astro build                                      |
| --------------------- | --------------------------------------- | ------------------------------------------------ |
| **單位時間**          | 1 張 JPG ≈ 2.5s（Playwright 真 render） | 1 頁 HTML < 50ms（in-memory 編譯）               |
| **可否平行**          | ✓ 天然平行（Playwright multi-context）  | 部分 ✓（Vite/worker 內部已平行化）               |
| **依賴圖**            | 扁平（每篇獨立）                        | 複雜（cross-link、shared component、CSS bundle） |
| **1731 張/頁 總時間** | 序列 66 分 / 4 worker 17 分             | 目前全 build ~3-4 分鐘（已不是瓶頸）             |

關鍵認知：**Astro build 不是瓶頸，OG 產圖才是**。但 CI 其他 step 仍有壓縮空間。

---

## 當前 CI 時間拆解（v3 後估算）

```
[Install dependencies]       ~1-2 分      ← npm install
[Validate frontmatter]       ~10s
[Restore mtime from git]     ~20s          ← v3 新加
[Restore OG cache]           ~30s          ← 首次 miss 快，cache hit 大
[Install Playwright]         ~1-2 分       ← 每次重裝 chromium
[Generate OG images]         首次 ~15 分 / cache hit <1 分
[Build Astro]                ~3-4 分       ← 永遠全量
[Upload artifact + deploy]   ~1 分
────────────────────────────────────
首次:      ~22-26 分
Cache hit: ~6-8 分
```

`Build Astro 永遠全量` 是殘留最大 block，但要做 per-file incremental 非常難——見下節。

---

## 為什麼 Astro build 很難像 OG 一樣做 per-file incremental

### 1. 依賴圖複雜

OG 產圖：`md 變 → JPG 重產`，一對一純粹。

Astro build：改一個 md 可能觸發**多個頁面**重建：

- 本篇文章頁 ✓
- 該 category 的 category page（列表變了）
- 首頁 hot articles section
- Smart 404 索引（`article-index.json`）
- 搜尋索引（`build-search-index.mjs`）
- `sitemap.xml`
- RSS feed
- dashboard articles count

改一個 **shared component**（ArticleHero、Header、Layout）要**全量重 1761 頁**。

改一個 **global.css** 要**重 bundle 全站 CSS**。

### 2. Astro 本身沒 native page-level cache

- Astro 5 才有 `experimental.incremental`，還是實驗性
- Next.js ISR 是正式方案但需要 Node runtime（GitHub Pages 吃不下）
- Gatsby 曾有 incremental，後來 React Server Components 改寫打掉重練

社群過去 10 年都在這坑裡翻滾。自己寫 per-file incremental 會踩 N 個雷。

---

## 可執行的優化（按 CP 值排序）

### ⭐ Tier 1 — 5 分鐘實作，省 ~3 分/CI

**1. 快取 Playwright chromium binary（省 ~2 分）**

```yaml
- name: Cache Playwright binary
  uses: actions/cache@v4
  id: pw-cache
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ runner.os }}-${{ hashFiles('package-lock.json') }}

- name: Install Playwright Chromium
  if: steps.pw-cache.outputs.cache-hit != 'true'
  run: npx playwright install --with-deps chromium
```

**2. 快取 node_modules（省 ~30-60s）**

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: 'npm' # 內建 npm cache
```

或更激進快取整個 node_modules：

```yaml
- uses: actions/cache@v4
  with:
    path: node_modules
    key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
```

**3. 快取 `.astro/` content collection 解析結果（省 ~20-30s）**

```yaml
- uses: actions/cache@v4
  with:
    path: .astro
    key: astro-content-${{ hashFiles('src/content/**/*.md', 'knowledge/**/*.md') }}
```

**Tier 1 三項合計預期**：

- 首次 CI：~22 分（原）→ ~17-19 分
- Cache hit CI：~6-8 分（原）→ **~3-4 分**

---

### 🎯 Tier 2 — 中等工程，省 ~30s-1 分

**4. prebuild 腳本平行化**

現在 `package.json`：

```json
"prebuild": "node generate-api.js && node generate-map.js && node build-search-index.mjs && ..."
```

全部 `&&` 序列。改成平行（需安裝 `npm-run-all` 或用 shell `&` + `wait`）：

```json
"prebuild": "npm-run-all --parallel prebuild:*",
"prebuild:api": "node scripts/core/generate-api.js",
"prebuild:map": "node scripts/core/generate-map-markers.js",
"prebuild:search": "node scripts/core/build-search-index.mjs",
"prebuild:dashboard": "node scripts/core/generate-dashboard-data.js",
"prebuild:changelog": "node scripts/core/generate-changelog-data.js",
"prebuild:contributors": "node scripts/core/generate-contributors-data.js",
"prebuild:supporters": "node scripts/core/generate-supporters-data.js"
```

**前提驗證**：需確認這些 script 彼此獨立，不會 race（例如共寫同一檔）。快速 audit：

- `generate-api.js` → 寫 `public/api/*.json`
- `generate-map-markers.js` → 寫 `src/data/map-markers.json`
- `build-search-index.mjs` → 寫 `public/search-index.json`
- `generate-dashboard-data.js` → 寫 `public/api/dashboard-*.json`
- `generate-changelog-data.js` → 寫 `src/data/changelog-feed.json`
- `generate-contributors-data.js` → 寫 `public/api/contributors.json`
- `generate-supporters-data.js` → 寫 `public/api/supporters.json`

互不干擾，理論可平行。但 `generate-dashboard-data.js` 可能依賴 `generate-api.js` 的輸出（如果它讀 articles.json）→ 需實際 trace 才能確定。

---

### ⚠️ Tier 3 — 架構改動，需評估

**5. Astro 5 experimental incremental**

- Astro 6 → 5 是 downgrade 且有 breaking change
- 目前 Astro 6 最新，實驗性功能還沒定案
- **建議：觀察，別現在做**

**6. 遷移到支援 ISR 的平台**

- Cloudflare Pages + Workers（on-demand page render）
- Vercel（Next.js ISR style）
- 需要把 GitHub Pages 架構打掉重練
- 長期方向，但不是現在該做
- 跟 OG Phase 3 屬於同一個大遷移

---

## 建議優先序

| 優先 | 行動                                                 | 何時做             | 期待收益                        |
| ---- | ---------------------------------------------------- | ------------------ | ------------------------------- |
| 1    | 等 v3 CI 跑完看實際數字                              | **現在（進行中）** | 驗證優化前基線                  |
| 2    | 如果首次 ~12 分 + cache hit <2 分 → 已達標，先不優化 | 看結果             | -                               |
| 3    | 若覺得還是慢，做 Tier 1 三件                         | 1 個 session       | CI 首次 -5 分 / cache hit -3 分 |
| 4    | Tier 2 prebuild 平行化（需 audit 依賴）              | 有空時             | CI -30s-1 分                    |
| 5    | Tier 3 Astro incremental / 平台遷移                  | 半年以上           | 變成 "改 1 篇只重 1 頁"         |

---

## 不建議做的事

❌ **不要手寫 Astro page-level incremental**  
理由：依賴圖太複雜，社群過去 10 年沒人做成。跳進去會維護永遠。

❌ **不要先做 Tier 2 才做 Tier 1**  
理由：CP 值不對，Tier 1 10 分鐘實作、收益大 3 倍。

❌ **不要因為「好像可以優化」就優化**  
目前的 v3 架構（OG cache hit 後全 CI ~6-8 分）對每天 ~5 次 push 是可接受的。除非 CI 變 block（例如 cache miss 頻繁、或 push 頻率上升 10 倍），不必優化。

---

## 延後題目（待觀察）

- v3 首次 CI 實際跑幾分鐘？（run `24780797221`，觀察 `b0ie2a5du`）
- cache hit 後第二次 CI 真的是 <2 分嗎？
- `git-restore-mtime-action` 在 ~5000 檔 repo 要多久？
- `prebuild:*` scripts 是否真的獨立？需跑 `strace` / `lsof` audit 確認

當這些數字到手，再決定 Tier 1/2 要不要做。

---

_v1.0 | 2026-04-22 β — v3 OG pipeline 完工後的後續討論，未執行_
_記錄原因：觀察者問「能否對 build 做類似優化」，先討論架構差異避免盲目 refactor，等 CI 實際數字出來再定優先序_
