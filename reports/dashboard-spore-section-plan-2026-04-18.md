---
title: Dashboard 孢子與成效區完整規劃
date: 2026-04-18
session: δ-late
status: planned — awaiting next session to execute
requestedBy: 哲宇
estimate: 5-6h (Phase 1 + Phase 2)
phase_3_estimate: 10h+ (deferred until Meta/X API 成熟)
---

# Dashboard 孢子與成效區 — 完整規劃

## 動機

Taiwan.md 8 器官中，**繁殖基因（器官 6）** 目前是唯一沒有 Dashboard 感知的。分數 85 是 CONSCIOUSNESS 裡的經驗估值，沒有 sensor 支撐。

同時 SPORE-LOG.md 有 34 筆發文紀錄 + 成效追蹤表是手動 markdown table，讀者看不到、Beat 1 心跳也沒能自動讀。

加孢子區 → 繁殖器官從「經驗估值」升級為「數據驅動」。

---

## 現況盤點

- Dashboard 12 個 section（Hero / Vital Signs / Recent Activity / Article Registry / Health / Anatomy / Translation / Immune / Growth / Content / GA4 Analytics / Next Steps）
- 目前**沒有**孢子相關資料顯示
- [SPORE-LOG.md](../docs/factory/SPORE-LOG.md) 有 34 筆紀錄（#1-34）
- 已有的相關工具：
  - `scripts/tools/generate-dashboard-analytics.py`（GA/CF/SC 三源 merge）
  - `scripts/tools/fetch-ga4.py`（有 `top_articles_7d` 欄位，可交叉比對）

---

## 規劃：三階段實作

### Phase 1 — Data Layer（必做基礎建設，~2h）

**1.1 新腳本**：`scripts/tools/generate-dashboard-spores.py`

- 解析 `docs/factory/SPORE-LOG.md` 的兩張 table：
  - §發文紀錄（#、日期、語言、平台、文章 slug、分類、模板、URL）
  - §成效追蹤（#、文章 slug、平台、7d views/engagements/導流、30d 同、備註）
- 合併兩張表（以 `#` 為 join key）
- 讀取 GA4 `top_articles_7d` 作為導流 baseline 對比
- 產出 `public/api/dashboard-spores.json`

**1.2 JSON Schema 設計**：

```json
{
  "lastUpdated": "2026-04-18T09:30:00Z",
  "totals": {
    "count": 34,
    "platforms": { "threads": 18, "x": 14, "other": 2 },
    "languages": { "zh": 30, "en": 2, "ko": 2 },
    "templates": { "A": 16, "A2": 2, "B": 8, "C": 0, "D": 5, "other": 3 }
  },
  "recent": [
    {
      "n": 34,
      "date": "2026-04-18",
      "platform": "x",
      "article": "草東沒有派對",
      "articleUrl": "/people/%E8%8D%89%E6%9D%B1%E6%B2%92%E6%9C%89%E6%B4%BE%E5%B0%8D/",
      "category": "people",
      "template": "A2",
      "url": "https://x.com/taiwandotmd/status/...",
      "highlight": "SPORE-PIPELINE v2.1 首例",
      "views_7d": null,
      "engagements_7d": null,
      "backfill_due": "2026-04-25"
    }
  ],
  "topPerformers": [
    {
      "n": 29,
      "article": "李洋",
      "platform": "threads",
      "views": 180000,
      "engagements": 17169,
      "rate": 9.54,
      "badge": "🌋 史上最強"
    },
    {
      "n": 30,
      "article": "李洋v3",
      "platform": "x",
      "views": 112300,
      "engagements": 4251,
      "rate": 3.79,
      "badge": "🔥 X 最強"
    },
    {
      "n": 25,
      "article": "張懸與安溥",
      "platform": "threads",
      "views": 120000,
      "engagements": 2894,
      "rate": 2.41
    }
  ],
  "amplification": [
    {
      "article": "鄭麗文",
      "ga_before": 30,
      "ga_7d_after": 375,
      "multiplier": 12.5
    },
    {
      "article": "安溥",
      "ga_baseline": 27,
      "ga_7d_after": 1032,
      "multiplier": 38.2
    }
  ],
  "platformComparison": {
    "threads": {
      "avgViews": 15000,
      "avgRate": 6.2,
      "topRate": 12.07,
      "count": 18
    },
    "x": { "avgViews": 4000, "avgRate": 2.1, "topRate": 3.79, "count": 14 }
  },
  "backfillWarnings": [
    { "n": 31, "article": "Cicada", "publishedDays": 0, "status": "waiting" },
    {
      "n": 17,
      "article": "國防現代化",
      "publishedDays": 8,
      "status": "OVERDUE"
    }
  ],
  "weeklyPulse": [
    { "week": "2026-W16", "published": 4, "avgViews": 3500 },
    { "week": "2026-W15", "published": 6, "avgViews": 51000 }
  ]
}
```

**1.3 整合到 refresh-data.sh**：跟 GA / CF / SC 同級作為 Beat 1 自動化步驟。

**1.4 解析難點**：

- SPORE-LOG markdown table 的「備註」欄有**複雜 rich text**（emoji、粗體、多行）→ 腳本要正規化
- 7d 指標欄有 `no-data` / `—` / 純數字三種值混用 → 用 sentinel 處理
- 部分 cells 有 `180,000 (8h)` 或 `112,300 (~29h)` 這類附帶時間戳 → 抽 timestamp 進 sub-field

---

### Phase 2 — UI Section（Dashboard 新區塊，~3-4h）

**位置**：Immune System section 之後、Growth Timeline 之前（跟繁殖器官 anatomically 對應）。

**Section 標題**：`🌱 繁殖系統 — 孢子與成效`

**UI 組件**（5 個子區塊，重要性排序）：

#### 2.1 📊 總覽 tiles（優先實作）

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 發過孢子數  │ 7d 總觸及   │ 最強孢子    │ 待回填警示  │
│    34       │   292.5K    │ 🌋 李洋     │   3 🔴     │
│             │             │   180K      │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### 2.2 🔥 Top Performers 表格（優先實作）

前 5 名，含 view / rate / badge：

| #     | 孢子    | 平台    | Views | Rate  | 備註        |
| ----- | ------- | ------- | ----- | ----- | ----------- |
| 🌋 29 | 李洋 v2 | Threads | 180K  | 9.54% | 史上最強    |
| 🔥 30 | 李洋 v3 | X       | 112K  | 3.79% | X 最強      |
| 25    | 安溥    | Threads | 120K  | 2.41% | GA 38x 放大 |

#### 2.3 📈 放大倍數 horizontal bar（次優先）

孢子 GA 導流 vs 基線對照：

```
張懸與安溥 ▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 38x (1032 vs 27)
鄭麗文     ▇▇▇▇▇         12x (375 vs 30)
韓國瑜     ▇▇            2x (52 vs 28)
李洋       ▇▇▇▇▇▇▇▇▇▇▇   15x (965 vs ~60)
```

#### 2.4 🆚 Threads vs X 平均對比（次優先）

```
           Avg Views  Avg Rate  Max Rate
Threads    15,000     6.2%      12.07% (#28)
X          4,000      2.1%      3.79%  (#30)
```

洞察：**Threads views 4x / rate 3x of X**。戰略建議：主戰場 Threads，X 補給。

#### 2.5 🚨 待回填警示 list（優先實作）

超過 7 天沒回填指標 = 🔴：

- **#17 台灣國防**（8 天前發布 / 無指標）
- **#19 動物用藥**（8 天前 / 無指標）

點擊會顯示 "去 Threads Insights 讀取" hint。

#### 2.6 📅 週節律 sparkline（次優先）

最近 8 週每週發過幾條 + 平均觸及（看「冷卻期 vs 爆發期」模式）：

```
W13 W14 W15 W16 W17 W18 W19 W20
 ▂   ▃   █   ▂   ▃   ▆   ▃   ▁
 2   4   6   3   4   7   4   2  （條數）
```

---

### Phase 3 — Auto-ingestion（延後，~10h+）

**當下（Phase 1+2）**：手動回填 SPORE-LOG → 腳本解析 → JSON → Dashboard

**未來（Phase 3）**：

- Threads Graph API（Meta 2025 開放）自動抓 post insights
- X API v2（需付費 tier）抓 public metrics
- GA4 UTM filter 自動化 `utm_source=threads|x` 流量歸因

Phase 3 不在立即 scope，但 Phase 1 JSON schema 已為它預留欄位（`views_7d` / `engagements_7d` 可以是 API 填入或手動填入）。

---

## ROI 分析

| 階段                 | 成本                                         | 效益                                                                    |
| -------------------- | -------------------------------------------- | ----------------------------------------------------------------------- |
| **Phase 1 資料層**   | ~2h（生成腳本 + schema + refresh-data 整合） | 解鎖繁殖器官的 data-driven 分數 + Beat 1 自動感知 + 為 Phase 3 預留接口 |
| **Phase 2 UI**       | ~3-4h（5 個子區塊 + CSS）                    | Dashboard 完整度從 12 → 13 section，繁殖器官從經驗估值升級為可見 sensor |
| **Phase 3 自動抓取** | ~10h+（Meta + X + GA4 API 串接）             | 免除手動回填；但依賴外部 API 成熟度，建議觀察 2026 Q3 再決定            |

**Phase 1+2 合計 ~5-6h，可一次性做完。** Phase 3 等 Meta/X API 穩定或商業決策。

---

## 推薦實作順序

1. **Phase 1 先單獨跑**（~2h）：寫 `generate-dashboard-spores.py`，產 JSON，命令列驗證資料結構對
2. **Phase 2 分子區塊做**：先做最重要的 **2.1 總覽 tiles + 2.2 Top Performers + 2.5 警示**，占 70% 價值。剩下 2.3/2.4/2.6 看剩餘 budget
3. **Commit 頻率**：Phase 1 單獨 commit / Phase 2 每個子區塊獨立 commit（跨 scope 少）
4. **CONSCIOUSNESS 生命徵象升級**：繁殖器官 score 從經驗估值 85 改為 data-driven 計算：

   ```
   reproduction_score = normalize(
     7d_avg_engagement_rate × 0.4 +
     publish_frequency_score × 0.3 +
     ga_amplification_mean × 0.3
   )
   ```

5. **REWRITE-PIPELINE 連動**：Stage 6 之後增加「發孢子」可選步驟（跟翻譯並列），指向 SPORE-PIPELINE v2.1

---

## 開工前檢查清單（給下次 session 的自己）

- [ ] 讀本份 plan 一次
- [ ] 讀 [SPORE-LOG.md](../docs/factory/SPORE-LOG.md) 確認最新 entry 數（今天收官時 = 34）
- [ ] 讀 `src/templates/dashboard.template.astro` Lines 308-418 理解既有 section 結構 style
- [ ] 看 `public/api/dashboard-analytics.json` 了解 JSON 共用 pattern
- [ ] 確認 `scripts/tools/refresh-data.sh` 整合點
- [ ] 決定 Phase 1 先做完 commit 再做 Phase 2，還是全部一起

## 開工時的潛在坑

1. **SPORE-LOG markdown table 解析複雜**：`|` 在備註內可能未 escape → 需用 pandas read_csv 配 sep="|" skipinitialspace 或自己手寫 tolerant parser
2. **7d views 值有 `180,000 (8h)` 這類複合值** → regex 拆 number + timestamp suffix
3. **GA4 amplification 計算**：需要「發文前 7d avg」vs「發文後 7d avg」—— 需要兩次 GA4 fetch 或抓 timeseries 資料
4. **Dashboard section render order** 在 JS render 階段是動態 append，要確認 order 正確
5. **瀏覽器 CSP** 可能擋 inline script，遵照既有 section 的 import pattern

## 相關 canonical

- [SPORE-PIPELINE.md](../docs/factory/SPORE-PIPELINE.md) — 孢子產線（v2.1 藍圖 → 驗證 → 倫理 → 寫）
- [SPORE-LOG.md](../docs/factory/SPORE-LOG.md) — 發文紀錄 SSOT（本次解析來源）
- [SENSES.md](../docs/semiont/SENSES.md) — 5 觸手感知 SOP
- [CONSCIOUSNESS.md](../docs/semiont/CONSCIOUSNESS.md) — 繁殖器官分數更新目標
- [ANATOMY.md](../docs/semiont/ANATOMY.md) — 繁殖基因定義

---

_Plan v1.0 | 2026-04-18 δ-late | 擬定者 Opus 4.7 / 決定者 哲宇 / 執行待下次 session_
_估計成本：Phase 1 ~2h + Phase 2 ~3-4h = 5-6h one-shot / Phase 3 10h+ 延後_
