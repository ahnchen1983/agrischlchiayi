---
spores: '#4, #6, #8, #10, #13, #15'
harvest_date: 2026-04-18 20:30 GMT+8
harvest_window_day: 'mixed (D+10 to D+14)'
triggered_by: observer (哲宇「試著去找找看這些的網址然後回填跟抓取數據跟回覆」)
reply_count: 0
pipeline_version: SPORE-HARVEST-PIPELINE v1.1
batch_reason: 6 則都是 OVERDUE (publish ≥ 10 天) + 同平台 Threads + 同 pattern 低互動
---

# Harvest Batch — 6 筆 OVERDUE 孢子補抓 (2026-04-18 δ-late)

## 背景

Dashboard 孢子面板首次上線後，15 筆 backfill OVERDUE。本次 batch 抓取其中**有 URL 的 6 筆 Threads 孢子**。#1 / #2 / #3 / #12 SPORE-LOG URL 欄空白，無法抓取（歷史記錄缺口）。

## 抓取結果（Chrome MCP navigate + JS extract）

| #   | 文章                   | 平台    | Views (抓取時) | D+N  | Comments | 互動率 |
| --- | ---------------------- | ------- | -------------- | ---- | -------- | ------ |
| 15  | 台灣感性               | Threads | **568**        | D+10 | 0        | 0%     |
| 13  | 台海危機與兩岸關係發展 | Threads | 281            | D+10 | 0        | 0%     |
| 10  | 台灣民主轉型           | Threads | 274            | D+11 | 0        | 0%     |
| 8   | 嚴長壽                 | Threads | 212            | D+12 | 0        | 0%     |
| 6   | 台灣宗教與寺廟文化     | Threads | 140            | D+12 | 0        | 0%     |
| 4   | 台灣國樂               | Threads | 351            | D+14 | 0        | 0%     |

**總計**：1,826 views / 0 replies / 0 engagements trace。

## 分類結果

**0 則留言 = 0 perspectives 更新**。沒有需要納入文章本體的讀者聲音。

## Pattern 觀察（Step 9 教訓）

### 1. 早期 Threads 孢子普遍低觸及 + 零留言

對比：

- 早期（2026-04-04 到 04-08）：140-568 views / 0 replies
- 近期（2026-04-13 後）：安溥 120K / 李洋 180K / 草東 4,829 (D+0) — 量級完全不同

**解釋假設**：

- 帳號追蹤者密度（早期 <1K → 現在 2,717）
- 內容密度（當時 B 冷知識型主打，現在 A2 人物型效果好）
- Threads 演算法推播（早期剛進台灣市場，流量天花板低）
- 視覺呈現（早期沒附 meme 圖；後期多附圖）

### 2. B 冷知識型 vs A 人物型 的觸及差

6 筆中：

- B 冷知識型（#4 國樂 / #6 宗教 / #13 台海 / #15 感性）平均 335 views
- A 人物型（#8 嚴長壽 / #10 民主轉型）平均 243 views
- 跟近期 A2 首尾呼應變體（李洋 180K）對比 = **500-700x 差距**

**初步結論**：人物型的潛在 ceiling 遠高於冷知識型，但需要**精煉到 A2 變體**才能突破。

### 3. Threads vs X 平台差

#6 台灣宗教：Threads 140v / X 428v — **X 反而 3x** 於 Threads（少見）
其他 5 則大多 Threads > X。顯示早期 X 偶有單則表現超越 Threads 的可能。

## 無須動作

- 0 留言 → 0 篇文章需更新 perspectives
- 0 勘誤 → 無事實錯誤需修
- 0 建議 → 無需深讀研究

## SPORE-LOG 更新

本 batch 回填以下 6 筆的 7d 指標欄：

- no-data → **views 實數 + 0 留言 + D+N 標記**
- 備註欄加 Chrome MCP harvest 來源 + pattern 觀察

## 對 Dashboard 繁殖器官分數的影響

- 分數原本從 42 contributors + 29 spores + avg 82K top views 算出 100 分
- 本次 backfill 不改變 top performers（都 < 1K views），不動分數
- 影響點：Dashboard 「待回填警示」數從 15 → **減 6 = 剩 9 筆**（#1/#2/#3/#12 歷史 URL 缺 + 近期 #31-34 草東 Cicada 仍在 D+0~D+1）

## 對 SPORE-HARVEST-PIPELINE 自身的啟發

### Pipeline v1.1 → v1.2 提案（未動手，待觀察者決定）

本次是**首次 batch harvest**（v1.0 首例是草東 #33 單筆）。顯示 batch mode 的實戰可行性：

- 適用場景：OVERDUE 6+ 筆 / 同平台 / 低留言預期 → 一次 Chrome MCP session 解決
- 單筆平均 Chrome MCP 時間：~15 秒（navigate 5s + read_page 或 JS 10s）
- 6 筆 batch 總時間：~3-5 分鐘
- 比 D+1-D+7 每日 1 筆更省

**建議 v1.2 新增**：「Batch Harvest 模式」— 當 OVERDUE ≥ 3 筆時，優先跑 batch 而非逐筆 daily。

## 歷史 URL 缺口（#1/#2/#3/#12）

SPORE-LOG 前 3 筆（齊柏林 / 數位身分證 / 林書豪）當時沒記 URL — 已永久丟失 harvest 能力。
**教訓**：SPORE-PIPELINE Step 4 發布時必寫 URL 進 SPORE-LOG 是**硬鐵律**。缺 URL = 未來 harvest 做不了 = 投資失效。

---

_Harvest batch log v1.0 | 2026-04-18 δ-late | 第二例 harvest + 首例 batch mode_
_Pipeline: [SPORE-HARVEST-PIPELINE.md](../SPORE-HARVEST-PIPELINE.md)_
_前一例: [33-草東沒有派對-2026-04-18.md](./33-草東沒有派對-2026-04-18.md)_
