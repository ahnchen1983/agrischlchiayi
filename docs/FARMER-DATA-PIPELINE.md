# FARMER-DATA-PIPELINE — 農友資料整合架構

> 本文件描述「農友經營計畫書」如何從原始資料 (`source/`) 系統化轉化為知識庫文章 (`knowledge/`) 的**架構面**。
> 操作層的 6 步流程、檢查清單、Session 接續方式請見 [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md)。
> 去識別化規範請見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

## 1. 為什麼有這條管線

嘉義國本學堂課程累積了一批由學員撰寫的「農友經營計畫書」原始資料，內含實際的作物選擇、規模、成本結構、銷售通路、技術導入、痛點與解法。這批資料若放在抽屜裡，無法成為公開可學的知識；若直接公開，又涉及農友隱私。

本管線解決三件事：

1. **隱私保護**：所有原始檔僅留在本地 `source/`，永不進 git，永不上線
2. **知識萃取**：把通用的農業技術、經營策略、案例脈絡萃取出來，去識別化後成為文章
3. **規模化**：把 70+ 份原始資料系統化處理為 70-100 篇知識文章，避免一人一文的碎片化

## 2. 資料來源

### 2.1 原始資料位置

- **路徑**：`source/`（已在 `.gitignore`，永不提交）
- **規模**：約 70+ 份 `.md` 檔
- **格式**：Markdown + YAML frontmatter
- **內容**：個人耕作計畫書、經營分析、痛點與解法

### 2.2 原始 frontmatter 結構（典型樣本）

```yaml
---
姓名: [個人姓名]            # ❌ 移除
文件類型: 卓越班經營計畫書   # → source_type
產業: 蔬果                  # → industry
作物: [作物列表]            # → crops
規模: [規模等級]            # → scale
年收入估算: [金額]          # → annual_income
數位化程度: [程度]          # → digitization_level
銷售通路: [通路詳情]        # → sales_channels
時間象限: [忙碌程度]        # → time_quadrant
數位象限: [數位化狀態]      # → digital_quadrant
tags: [標籤列表]            # → tags（過濾個人資訊）
---
```

## 3. 整合架構

### 3.1 高階資料流

```
source/                       (本地原始檔，gitignored)
   │
   │  人工 + 工具輔助
   │  (deidentify-source.sh / .py)
   ▼
[暫存] 去識別化草稿
   │
   │  撰寫 / 結構化 / 案例融合
   │  （遵循 FARMER-DATA-WORKFLOW 6 步）
   ▼
knowledge/<Category>/<article>.md   (去識別化後的成品)
   │
   │  npm run sync → npm run build
   ▼
公開站點（GitHub Pages）
```

### 3.2 三條原則

1. **原始資料不出 `source/`**：所有跨檔操作（讀、彙整、轉寫）都在本地，產出物只進 `knowledge/`
2. **混合 ≥ 2 位農友的特徵**：每篇文章彙整多位案例，避免可被反向工程識別到單一個人
3. **保留量化資料、移除身份資料**：作物、規模、成本、通路比例等技術/經營資訊保留；姓名、地址、聯絡方式、家族成員、獨特背景一律移除或模糊化

完整的「保留 vs 移除」分級見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

## 4. Frontmatter 映射

從原始計畫書的 YAML 轉成標準化 article frontmatter：

| 原始欄位 | 標準化欄位 | 處理方式 |
|---|---|---|
| `姓名` | — | 移除 |
| `文件類型` | `source_type` | 直接對應，例：`farmer_case_study` |
| `產業` | `industry` | 直接對應 |
| `作物` | `crops` / `crop` | 陣列保留 |
| `規模` | `scale` | 量級分級（小 / 中 / 大）或保留具體公頃 |
| `年收入估算` | `annual_income` | **改為範圍**（例「100-150 萬」） |
| `數位化程度` | `digitization_level` | 低 / 中 / 高 |
| `銷售通路` | `sales_channels` | 比例可保留，組合過於獨特時模糊化 |
| `時間象限` | `time_quadrant` | 直接對應 |
| `數位象限` | `digital_quadrant` | 直接對應 |
| 地址欄位 | `region` | **僅保留至縣市級**（如「嘉義縣」） |
| `tags` | `tags` | 過濾掉個人資訊類標籤 |

成品 frontmatter 範例：

```yaml
---
title: '蔬果設施小黃瓜栽培技術指南'
description: '結合多位嘉義設施農友案例的小黃瓜栽培管理'
date: 2026-04-28
source_type: 'farmer_case_study'
industry: '蔬果'
crops: ['小黃瓜']
scale: '小型（0.2-0.5 公頃）'
annual_income: '約 100-200 萬'
digitization_level: '初階至進階'
region: '嘉義縣'
tags: ['設施農業', '小黃瓜', '案例分析']
level: '進階'
status: 'published'
---
```

## 5. 內容缺口與優先級

### 5.1 高優先（P1）— 高度缺口、高度價值

#### Crop-Production：缺主要作物栽培指南

**缺**：小黃瓜、洋香瓜、木瓜、柑橘、蓮霧、花卉類（蝴蝶蘭、洋桔梗）的栽培篇
**有**：小番茄、百香果（已實作）

**可建文章估**：5-8 篇

#### Smart-Farming：缺實務 IoT 與機械化案例

**缺**：IoT 灌溉實施案例、無人機應用、精準施肥
**有**：理論面為主，案例不足

**可建文章估**：3-4 篇

#### Agri-Basics：補充新農常見困境

**缺**：肥料管理（不同作物差異）、農場工具選購、四季耕作節奏

**可建文章估**：3 篇

### 5.2 中優先（P2）— 補充深度

| 分類 | 補充方向 | 估 |
|---|---|---|
| Farm-Management | 人力招募與培訓、按規模的成本結構比較 | 2 篇 |
| Agri-Marketing | 有機/友善認證實務、電商平台銷售 | 2-3 篇 |
| Grants-Planning | 補助申請實案經驗 | 2 篇 |

### 5.3 低優先（P3）— 特殊主題

Livestock-Health：家禽家畜、水產混養（依原始資料中是否有對應樣本決定）

### 5.4 與分類體系的關係

每篇文章必須歸入既有 13 大分類之一。若某主題 3 位以上農友都有提及但分類體系尚未涵蓋，才考慮新建分類。詳細分類定義與內容缺口分析見 [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md)。

## 6. 預期效益

### 6.1 數量目標

```
當前：~50 篇
4 週內：70-80 篇
完全利用全部原始資料：90-100 篇
```

### 6.2 品質目標

- 每篇文章彙整 ≥ 2 位農友案例（避免單一農友被識別）
- 每個主分類至少 4-6 篇（Livestock 除外）
- 涵蓋嘉義主要作物（番茄、黃瓜、洋香瓜、柑橘等）
- 智慧農業、設施、銷售、財務各領域具實務深度

### 6.3 用戶體驗目標

- 新農友：「我的問題在這裡有答案」
- 返鄉青農：「同類型農民的經驗分享」
- 進階農友：「科技與商業模式的整合案例」

## 7. 工具支援

| 工具 | 路徑 | 用途 |
|---|---|---|
| 去識別化（bash） | [scripts/tools/deidentify-source.sh](../scripts/tools/deidentify-source.sh) | 批量替換已知敏感詞 |
| 去識別化（Python） | [scripts/tools/deidentify-source.py](../scripts/tools/deidentify-source.py) | 雜湊比對 + 進階替換 |
| 提交前檢查 | [scripts/tools/deidentification-check.sh](../scripts/tools/deidentification-check.sh) | pre-commit hook 用 |
| 提交訊息檢查 | [scripts/tools/deidentification-check.py](../scripts/tools/deidentification-check.py) | commit-msg hook 用 |
| 加入新敏感詞 | [scripts/tools/add-sensitive-name.sh](../scripts/tools/add-sensitive-name.sh) | 動態擴充黑名單 |

## 8. 後續維護

### 8.1 新原始資料進來時

1. 放入 `source/`（gitignored，本地保存）
2. 依 [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) 6 步流程處理
3. 若無新主題且現有文章已足，**優先補充現有文章的案例段落**而非新建文章

### 8.2 何時補現有文章 vs 新建文章

| 情境 | 行動 |
|---|---|
| 主題已有文章，只是多一個案例 | **補現有**（在「農友案例」段落加入） |
| 新作物 / 新技術 / 新通路（嘉義既有資料尚無） | **新建** |
| 主題太特殊、僅 1-2 農友提及 | **暫不處理**（累積至 3+ 案例再決定） |

詳細決策樹見 [FARMER-DATA-WORKFLOW.md §3](FARMER-DATA-WORKFLOW.md#3-第-5-步決定行動)。

## 9. 相關文件

- [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) — 操作層 6 步流程與 Session 接續
- [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — 去識別化政策與檢查清單
- [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) — 13 大分類定義與內容缺口
- [ARCHITECTURE.md](ARCHITECTURE.md) — 系統架構（SDD）
