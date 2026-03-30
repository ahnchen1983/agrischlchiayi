# Rewrite Pipeline (Cron) — 自動品質重寫流程

> 目前暫停（Cron disabled）。等品質革命 Phase 1 啟動再開。
> 相關文件：`docs/editorial/REWRITE-PIPELINE.md`（完整三階段流程）

---

## 現況

- quality-scan pass rate: **5.8%**（26/451 通過）
- human_reviewed: **0 篇**
- featured: 124 篇（30%，門檻過鬆）
- 已用此 Cron 重寫過 ~50 篇（v1 + v2）

---

## 流程

```
git pull → 選文 → REWRITE-PIPELINE 三階段 → quality-scan → sync → push
```

### Step 1：拉最新 + 選文

```bash
cd ~/taiwan-md && git pull
# 佇列頂端，跳過已重寫的
head -30 scripts/tools/rewrite-queue.txt
git log --oneline --since='2026-03-20' | grep -i 'rewrite:' | head -30
```

### Step 2：執行三階段

**嚴格按照 [`docs/editorial/REWRITE-PIPELINE.md`](../editorial/REWRITE-PIPELINE.md)**。
Pipeline 會告訴你每個 Stage 要讀哪個文件（RESEARCH.md → EDITORIAL.md → QUALITY-CHECKLIST.md）。

### Step 3：Commit

```bash
bash scripts/core/sync.sh
bash scripts/tools/quality-scan.sh knowledge/[Category]/[文章名].md  # ≤ 3 才 commit
git add knowledge/[Category]/[文章名].md src/content/
git commit -m "rewrite: [文章名] — EDITORIAL v4 + Pipeline v2.3"
git push
```

---

## ⚠️ 鐵律

### 進化模式 ≠ 在舊文上修補

> 「AI 讀了品質不佳的舊文會不自覺模仿它的語氣、結構、甚至壞習慣。把舊文當骨架 = 讓病毒感染新內容。」

**舊文降級為素材庫**，Stage 0 只提取事實清單。進入 Stage 1 後，不再回頭看舊文。

### 每批最多 1 篇

v1 時期每批 3 篇，品質明顯不穩。改成每批 1 篇後品質大幅提升。

### SSOT 在 knowledge/

只改 `knowledge/`，用 `scripts/core/sync.sh` 同步到 `src/content/`。不要直接改 `src/content/`。

### 不要 git add -A

只 add 改動的文章和同步後的 `src/content/` 對應目錄。

### 不要跑 npm run build

Build 由 CI/CD 處理。sub-agent 跑 build 容易 timeout 且浪費資源。

### quality-scan 分數 ≤ 3 才能 commit

不合格 → 修正重試，不直接 commit。

---

## 血淚教訓（7 天實戰）

1. **一次一篇**：多個 sub-agent 同時跑 = 搶檔案 + timeout + 殭屍 session
2. **至少 7 分鐘**：研究 3min + 寫作 2min + 驗證 2min = 最低要求
3. **prompt 裡寫「立刻執行，不要重述任務」**：否則 AI 花 30% 時間重述指令
4. **量化指標是 pre-filter 不是品質保證**：塑膠句數=0 ≠ 好文章，必須逐篇讀
5. **塑膠會變種**：AI 把被禁句式微調成看似不同的版本（"展現了"→"印證了"→"彰顯了"）
6. **Build 驗證不能省**：YAML frontmatter 偶爾壞掉，一篇壞 = 整個 category 炸
7. **結尾最後寫 = 品質最差**：Pipeline v2 改成結尾先行（Stage 2 先寫結尾再寫正文）

---

## 相關檔案

| 檔案                                  | 用途                   |
| ------------------------------------- | ---------------------- |
| `docs/editorial/REWRITE-PIPELINE.md`  | 完整三階段流程（SSOT） |
| `docs/editorial/RESEARCH.md`          | 研究方法論             |
| `docs/editorial/RESEARCH-TEMPLATE.md` | Stage 1 研究筆記模板   |
| `docs/editorial/EDITORIAL.md`         | 品質標準               |
| `docs/editorial/QUALITY-CHECKLIST.md` | Stage 3 驗證清單       |
| `scripts/tools/rewrite-queue.txt`     | 待重寫佇列             |
| `scripts/tools/quality-scan.sh`       | 品質掃描腳本           |

## 相關 Cron

| Cron                              | 狀態        | 說明                       |
| --------------------------------- | ----------- | -------------------------- |
| Taiwan.md Article Quality Rewrite | ❌ disabled | 每小時 1 篇，Opus model    |
| taiwan-md-rewrite (v1)            | ❌ disabled | 舊版每小時 3 篇，已淘汰    |
| taiwan-md-content-sprint          | ❌ disabled | 內容衝刺（新文章），已淘汰 |

---

## 重啟條件

品質革命 Phase 1 啟動時（預計 2026-04），需要：

1. 確認 EDITORIAL v4 的新標準（引語、因果鏈、切入人物）已整合到 prompt
2. 設定 featured 文章優先佇列（124 篇門面文章先洗）
3. 目標：pass rate 5.8% → 30%（3 個月內）

---

_版本：v1.0 | 2026-03-29_
_狀態：暫停中，等品質革命 Phase 1_
