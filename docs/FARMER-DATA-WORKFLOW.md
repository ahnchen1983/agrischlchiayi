# FARMER-DATA-WORKFLOW — 農友資料處理流程

> 本文件是處理農友原始資料 (`source/`) → 轉化為知識庫文章 (`knowledge/`) 的**操作手冊**。
> 整體架構與內容缺口分析請見 [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md)。
> 去識別化分級規則與檢查清單請見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

## 1. 適用時機

每當有以下情境，跑這個流程：

- 拿到一份新的農友計畫書，要納入知識庫
- 要新建一篇基於 2+ 農友案例的文章
- 要在現有文章中補上一段去識別化案例

## 2. 標準 6 步流程

```
1️⃣ 基礎資料提取   →  2️⃣ 分類對齊   →  3️⃣ 去識別化驗證
4️⃣ 內容品質檢查   →  5️⃣ 決定行動   →  6️⃣ 最終發布
```

每篇文章預估 3-4 小時（含案例整理、去識別化、撰寫、驗證）。

### 2.1 第 1 步：基礎資料提取

從每位納入的農友（建議 ≥ 2 位）提取：

**作物資訊**
- [ ] 主作物（可複選）
- [ ] 副業作物
- [ ] 新導入品種（若有）

**經營規模**
- [ ] 總面積（公頃）
- [ ] 設施面積（若有）
- [ ] 年產量

**銷售通路**
- [ ] 主要通路：批發 / 行口 / 直銷 / 電商 / 超商 / 出口
- [ ] 各通路比例
- [ ] 年收入估計

**核心問題**（農友想解決什麼）
- [ ] 生產：品種 / 栽培 / 病蟲害 / 高溫乾旱
- [ ] 經營：成本 / 人力 / 財務
- [ ] 銷售：通路 / 價格 / 客戶 / 品牌
- [ ] 設施：溫室 / 環控 / 灌溉
- [ ] 技術：IoT / 無人機 / 其他

**其他重要資訊**
- [ ] 經驗年限
- [ ] 員工規模
- [ ] 品牌 / 認證狀態

> 同一篇文章記得用代號（F1、F2、F3）追蹤每位農友來源，便於後續驗證。

### 2.2 第 2 步：分類對齊

對照 [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) 的 13 大分類，判斷此案例該進哪一個：

| 農友主訴 | 對應分類 |
|---|---|
| 栽培技術 / 病蟲害 | Crop-Production |
| 溫室規劃 / 環控 | Facility-Farming |
| 通路 / 客戶 / 品牌 | Agri-Marketing |
| 財務 / 人力 / 成本 | Farm-Management |
| IoT / 無人機 / 自動化 | Smart-Farming |
| 補助申請 | Grants-Planning |
| 動物養殖 | Livestock-Health |
| 入門基礎 | Agri-Basics / Agri-Advanced |

**輸出**：列出此次案例對應的 1-3 個分類。

### 2.3 第 3 步：去識別化驗證

完整分級規則（RED / YELLOW / GREEN ZONE）與細節檢查清單在 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。本步驟跑該政策中的：

1. **檢查清單 A — 直接識別符**：姓名、地址、聯絡方式、家族成員
2. **檢查清單 B — 間接識別符**：獨特工作背景、特殊設備品牌、課程編號
3. **檢查清單 C — 反向工程測試**：能否從文章推測出特定農民？

> 疑問時：**寧刪勿留**。

### 2.4 第 4 步：內容品質檢查

**標題與描述**
- [ ] 標題清晰、無課程編號
- [ ] 描述為一句話摘要（≤ 160 字元）
- [ ] 標題 ≤ 60 字

**結構**
- [ ] 有清晰開場（核心問題或洞見）
- [ ] 5-8 個主章節
- [ ] 有實務檢查清單或行動步驟
- [ ] 有延伸閱讀的 wikilink

**格式**
- [ ] frontmatter 完整（見 [CONTRIBUTING.md](../CONTRIBUTING.md)）
- [ ] 程式碼區塊用 ` ``` `
- [ ] 表格格式正確
- [ ] wikilink 格式 `[[文章標題]]`，且**不在清單項中**（會渲染異常）

**案例與證據**
- [ ] 有 ≥ 2 位農友的去識別化案例
- [ ] 有量化資料支持（成本、收入、產量）
- [ ] 有適當的表格 / 圖示

### 2.5 第 5 步：決定行動

```
此次主題已有文章？
  ├─ 是，差別在「多一個案例」  →  情境 A：補現有文章
  ├─ 是，但案例量級不同 / 新角度  →  情境 A：補現有文章（加段落）
  └─ 否
       ├─ 確實是新作物 / 新技術 / 新通路  →  情境 B：新建文章
       └─ 過於特殊、僅 1-2 農友  →  情境 C：暫存，待累積
```

#### 情境 A：補現有文章（推薦）

- 找出目標文章
- 在「案例」/「農友案例」段落補上去識別化案例
- 更新文章 `date`
- 重建搜尋索引（會於 build 期自動跑）

#### 情境 B：新建文章（謹慎使用）

新文章前先自問：

- [ ] 是否確實是新主題？
- [ ] 是否在其他分類下有類似內容？
- [ ] 此主題是否有其他農友也會需要？
- [ ] 內容能否撐到 ≥ 2,000 字？

新文章標準：

- ≥ 2,000 字
- 含 3+ 農友案例或實務經驗
- 有完整檢查清單或實施步驟
- 有 wikilink 連到 ≥ 2 篇相關文章

#### 情境 C：暫存待決

- 把該農友案例存在 `source/待決/`
- 紀錄問題的通用描述
- 累積到 3+ 案例時再決定是否新建文章

### 2.6 第 6 步：最終發布

**發布前最終自查**

技術
- [ ] 已通過去識別化驗證（§2.3）
- [ ] frontmatter 完整正確
- [ ] wikilink / 連結都有效
- [ ] 無拼字 / 語法錯誤
- [ ] 本地預覽 OK（`npm run dev`）

內容
- [ ] 分類正確
- [ ] 與既有文章無大量重複
- [ ] 有 ≥ 2 位農友的混合特徵

SEO
- [ ] 標題含關鍵作物 / 技術名稱
- [ ] 描述含農友可能搜尋的詞
- [ ] tags 完整

**發布步驟**

```bash
git add knowledge/<Category>/<article>.md
git commit -m "content: add/update <article> with deidentified farmer case studies"
npm run sync
npm run build
git push
```

> commit message **不可**含農友姓名、敏感檔名、具體地址。完整規範見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)。

## 3. Session 接續工作流

當批量處理農友資料時，常需要跨多個 Session。本流程設計成「不依賴對話記憶」：

### 3.1 開新 Session

1. 開 [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) 看當前優先順序
2. 開本文件查標準 6 步流程
3. 進入 `source/` 找下一篇要處理的原始檔
4. 從 §2 第 1 步開始走

### 3.2 Session 中斷時

1. 在文章草稿頂端註明當前進度（已完成第幾步、卡在哪）
2. 把草稿存到本地暫存區（不要進 git）
3. 下次 Session：直接讀草稿頂端的進度註記，從那一步接續

### 3.3 完成一篇文章

1. 跑完第 6 步發布
2. 在 commit message 中註明「去識別化驗證 ✅ 通過」
3. 若有維護批次進度表，順手更新（避免進度表也成為含敏感資訊的檔案）

## 4. 驗證報告模板（選用）

對高敏感主題（例如獨特背景、特殊技術組合），建議補一份驗證紀錄。**驗證報告本身也必須去識別化**，且建議放在 `private/` 或外部存儲（見 [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md)）。

```markdown
# 去識別化驗證紀錄

文章：<title>
驗證日期：YYYY-MM-DD
案例來源：F1、F2（共 2 位）

## 檢查清單 A：直接識別符
- [✅] 無姓名
- [✅] 無詳細地址（僅保留至縣市級）
- [✅] 無聯絡方式
- [✅] 無家族成員名字

## 檢查清單 B：間接識別符
- [✅] 工作背景已模糊化
- [✅] 特殊設備改為通用描述
- [✅] 無特定課程 / 班別編號

## 檢查清單 C：反向工程測試
- 能否推測具體農民？  否（多位農友混合）
- 親友能否認出？        低風險
- 是否有集合特徵？       是

## 結論
✅ 通過，可發布
```

## 5. 常見陷阱與對策

| 陷阱 | 症狀 | 對策 |
|---|---|---|
| 故事太獨特，難去識別化 | 移除個人細節後文章變空泛 | 保留農業面細節、移除個人面；用「設施小黃瓜農場經營者」取代具體背景 |
| 過度簡化失去說服力 | 案例變得空泛無共鳴 | 保留具體數字（成本、收入、產量）、決策邏輯、失敗教訓 |
| 一農友一文，碎片化 | 每位農友各寫一篇 | 採「3 農友規則」：3+ 農友有同樣問題才考慮新文章；其餘優先補現有 |
| 文章成孤島 | 沒有 wikilink 連到他文 | 新文章前先找 2-3 篇相關文章，互加 wikilink |
| commit message 洩露 | 訊息含農友名 / 檔名 | 用通用描述（「update internal farmer case study」） |
| wikilink 在清單項失效 | `- [[X]]` 渲染異常 | 改用 `- [X](/url)` |

## 6. 工具速查

| 工具 | 用途 |
|---|---|
| [scripts/tools/deidentify-source.sh](../scripts/tools/deidentify-source.sh) | 批量替換已知敏感詞 |
| [scripts/tools/add-sensitive-name.sh](../scripts/tools/add-sensitive-name.sh) | 加新敏感詞到黑名單 |
| `git diff --cached` | 提交前最後檢查 |
| `npm test` | frontmatter 驗證 |
| `npm run dev` | 本地預覽 |

## 7. 相關文件

- [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) — 整體架構與內容缺口
- [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — 去識別化政策與分級規則
- [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) — 13 大分類定義
- [ARCHITECTURE.md](ARCHITECTURE.md) — 系統架構
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — 投稿指南
