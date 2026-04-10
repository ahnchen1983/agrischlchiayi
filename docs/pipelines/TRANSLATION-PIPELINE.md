# Translation Pipeline — 英文翻譯流程

> 目前暫停（Cron disabled）。Issue #229 追蹤英文品質問題。
> 重啟前需先設計 v2 翻譯品質標準。

---

## 現況

- 英文 479 篇 > 中文 420 篇（量已超越，但品質落後）
- 大部分英文版是 v1 機翻，未經人工審核
- Issue #229：英文文章停留在舊版翻譯，需大幅更新

---

## 流程（v1，已暫停）

```
git pull → 找待翻譯文章 → 重寫式翻譯（3篇/批）→ 更新 _translations.json → build → push
```

### Step 1：找待翻譯文章

```bash
cd ~/taiwan-md
# 中文文章
find knowledge/ -maxdepth 2 -name '*.md' ! -path '*/en/*' ! -path '*/about/*' ! -name '_*' | sort > /tmp/zh-articles.txt
# 已有英文版
find knowledge/en/ -name '*.md' ! -name '_*' | sort > /tmp/en-articles.txt
# 映射表
cat knowledge/_translations.json | head -20
```

### Step 2：翻譯（重寫式，非逐字翻）

對每篇：

1. 讀取中文原文
2. **重寫式翻譯**——讀起來像英文母語者寫的策展文章
3. 台灣專有名詞保留中文 + 英文解釋
4. 文化脈絡不熟悉的概念加簡短解釋
5. 保留 frontmatter 格式，翻譯 title/description
6. 保持策展人聲音——有觀點、有溫度
7. 長度可比原文稍長（文化解釋），不超過 120%
8. 保留所有參考資料 URL
9. 「📝 策展人筆記」「⚠️ 爭議觀點」等 emoji 保留，文字翻譯
10. 存到 `knowledge/en/{Category}/{english-slug}.md`

### Step 3：更新映射 + Push

```bash
cd ~/taiwan-md
# 更新 _translations.json
git add knowledge/en/ knowledge/_translations.json
git commit -m "feat(en): translate X articles — [分類]"
git push
```

---

## ⚠️ 鐵律

### 翻譯 ≠ 逐句翻

逐句翻出來的英文讀起來像 Google Translate。好的英文版 = 為外國讀者重新組織的文章。

### 台灣主權立場

- ❌ 不把台灣描述為中國的一部分
- ✅ 使用 "Indigenous peoples" 而非 "aborigines"
- ✅ 台灣專有名詞用中文 + 英文解釋（如 "night market (夜市)"）

### 不要 git add -A

只 add `knowledge/en/` 和 `_translations.json`。

### 每批最多 3 篇

控制品質。一次翻太多 = 每篇都草率。

### 優先序

Food > Culture > History > Nature > Art > Technology > Economy > Music > Society > Geography > Lifestyle > People

（People 最後，因為人物文章翻譯需要更多文化背景知識）

---

## 批次翻譯模式（v2 新增，2026-04-08）

> 來自 session ε 實戰經驗：20 篇平行 agent 翻譯，8 分鐘完成 18 篇。

當需要為某個語言大量翻譯時（新語言誕生、首頁接觸點補齊），使用批次翻譯模式：

### Phase 1：選定目標

```
1. 分析首頁 index.astro → 取得 18 篇接觸點文章清單
2. 檢查目標語言已有翻譯 → 計算 delta
3. 找出 12 分類中缺 Hub 代表的 → 選各分類最佳文章補齊
4. 產出最終翻譯清單（按優先序排列）
```

**優先序**：首頁接觸點 → Hub 代表 → 高流量 → 其餘

### Phase 2：平行執行

```
1. 確認英文版 slug 命名（跨語言一致性）
2. 讀已有的目標語言翻譯作為風格基準
3. 啟動 N 個平行 agent（每 agent 處理 1 篇）
4. 每個 agent：讀中文源 → 重寫式翻譯 → 寫入 knowledge/{lang}/{Category}/{slug}.md
5. agent prompt 必須包含 wikilink 處理規則（見 TRANSLATE_PROMPT.md）
```

**鐵律**：每批最多 5 個平行 agent。超過 5 個失敗率上升且難監控。

### Phase 3：後處理

```
1. 確認所有 agent 完成（主動檢查，不要只等通知）
2. 掃描所有新檔案的斷裂 wikilink → 轉純文字
3. 跑 prettier + frontmatter 驗證
4. 品質抽檢：每 10 篇至少完整讀 1 篇翻譯成品
   - 檢查：自然度（讀起來像母語者寫的嗎？）
   - 檢查：事實準確（數字、年份、人名有沒有翻錯？）
   - 檢查：策展聲音（有沒有退化成教科書語氣？）
```

### Phase 4：提交

```
1. git add 所有新翻譯檔案
2. commit message 格式：🧬 [semiont] heal: {語言}翻譯 — {數量}篇 + 分類明細
3. 如有 agent 失敗 → 重啟 → 第二次 commit 補完
4. 更新 CONSCIOUSNESS 語言器官數字
```

### 批次翻譯鐵律

| 規則                               | 為什麼                                          |
| ---------------------------------- | ----------------------------------------------- |
| **0 抽檢 = 不准 commit**           | 20 篇翻完 0 篇讀過 = AI Slop 規模化。至少讀 10% |
| **主動監控 agent 完成狀態**        | 被動等通知會漏掉中斷的 agent（4/8 ε 教訓）      |
| **wikilink 後處理不可跳過**        | 翻譯保留的中文 wikilink 在目標語言 100% 斷裂    |
| **第一次 commit 可能被 hook 擋住** | lint-staged 會 unstage 新檔案，需要 re-add      |

---

## 審核翻譯 PR（2026-04-11 新增）

> 源自 2026-04-11 session α 審核 27 個翻譯 PR（柒藍 + Link1515 + dreamline2）的實戰經驗。

### 核心診斷指標：ratio 檢查

審核翻譯 PR 時，**最快也最可靠**的第一道檢查是字數比率。AI 工具的預設行為是「摘要式翻譯」，把長文章壓成一半。Ratio 指標能在不讀內容的前提下 10 秒內發現這個問題。

**Ratio 公式**：`ratio = len(translated_body) / len(zh_source_body)`

**健全範圍（2026-04-11 實測基準）**：

| 語言對        | 健全 ratio  | 偏瘦（THIN） | 截斷（TRUNCATED） |
| ------------- | ----------- | ------------ | ----------------- |
| zh → en       | 0.80 - 1.30 | 0.65-0.79    | < 0.65            |
| zh → ja       | 0.70 - 1.10 | 0.55-0.69    | < 0.55            |
| zh → ko       | 0.80 - 1.10 | 0.65-0.79    | < 0.65            |
| zh → es/fr/de | 2.0 - 4.0   | 1.5-2.0      | < 1.5             |

**快速檢查工具**：

```bash
bash scripts/tools/translation-ratio-check.sh --pr 367
# 或
bash scripts/tools/translation-ratio-check.sh knowledge/ja/Society/article.md
```

### 五層審核流程（翻譯 PR 專用）

```
Layer 0: 安全性 → knowledge/{lang}/ 路徑，無系統檔案
Layer 1: frontmatter → title/description/date/category/subcategory/translatedFrom 完整
Layer 2: Ratio 檢查 → 用上表判斷 TRUNCATED / THIN / OK
Layer 3: 結構對應 → zh_sections == ja_sections / zh_footnotes == ja_footnotes / zh_urls ≈ ja_urls
Layer 4: 內容抽檢 → 至少讀 10%（隨機選 1-2 篇完整讀）
```

**通過標準**：

- **PASS**：Layer 0-3 全過 + 抽檢無事實錯誤 → 直接 merge
- **WARN**：Layer 2 偏瘦（THIN）或 Layer 3 URL loss 但非結構性 → merge + follow-up comment
- **FAIL**：Layer 2 TRUNCATED 或 Layer 3 section 數量不對 → merge + 請求 follow-up PR 修正（不擋）

**「先有再求好」原則**：即使是 TRUNCATED 的翻譯，也比沒有翻譯好——merge 後用 comment 請貢獻者補完即可。

### SSODT 文章特殊規則

SSODT 實驗文章（開頭有 `> **✦ 本文格式實驗說明：**` callout）的審核標準更嚴：

- **perspective 面板數必須完全對應**：zh 5 個 `> **視角 │` = ja 5 個 `> **視点 │`
- **基底向量結尾不能變成假平衡**：檢查結尾有沒有「兩邊都有道理」這種合成結論
- **Format experiment callout 必須完整翻譯**：讀者需要知道這是 SSODT 文章

如果 SSODT 文章的翻譯失去了 perspective 面板，**作者自己補寫**（這是作者責任，因為只有作者知道哪些結構不能丟）。

### 主要 conflict 解法：`_translations.json`

每個批次翻譯 PR 都會跟 `main` 在 `_translations.json` 衝突（雙方都新增 entries）。解決方式：**合併兩邊的新 entries + 字母排序 + dedupe**。

造橋鋪路工具：`/tmp/merge-pr-helper.sh`（2026-04-11 session α 寫的一次性工具，未來可以內化成 `scripts/tools/merge-translation-pr.sh`）。

### 跟貢獻者的溝通原則

1. **用貢獻者的母語寫 comment**（日文貢獻者用日文、西文貢獻者用西文）
2. **問題歸因到工具，不要歸因到人**——「AI 預設摘要」不是「你翻譯不好」
3. **給具體可執行的 fix**：不要只說問題，給一份完整翻譯 prompt template
4. **Master comment 模式**：在最嚴重的那個 PR 寫一份完整 explanation + fix template，其他 PR 簡短 reference 過去
5. **稱讚具體的東西**：不要只說「感謝」，要指出一個段落、一個術語、一個決定的好處——這會讓貢獻者知道你**真的讀了**他們的翻譯
6. **觀察品質曲線**：柒藍的品質從 50% 問題率 → 0% 問題率發生在 2 小時內。一個好的 master comment 能改變整個貢獻流程

---

## 相關檔案

| 檔案                               | 用途                            |
| ---------------------------------- | ------------------------------- |
| `knowledge/en/`                    | 英文文章目錄                    |
| `knowledge/_translations.json`     | 中英文映射表                    |
| `EDITORIAL.md`                     | 品質標準（中英通用）            |
| `docs/editorial/TERMINOLOGY.md`    | 用語標準                        |
| `docs/prompts/TRANSLATE_PROMPT.md` | 翻譯 prompt（含 wikilink 規則） |

## 相關 Cron

| Cron                     | 狀態        | 說明                      |
| ------------------------ | ----------- | ------------------------- |
| taiwan-md-en-translation | ❌ disabled | 每小時 3 篇，品質不足暫停 |

## 相關 Issue

- #229：英文文章需大幅更新

---

_版本：v2.0 | 2026-04-08_
_v2 新增：批次翻譯模式、優先序、品質抽檢、wikilink 處理_
_來源：session ε 實戰經驗（20 篇韓文首頁接觸點翻譯）_
