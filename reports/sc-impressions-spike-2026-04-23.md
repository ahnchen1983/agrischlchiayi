---
title: SC 7d impressions 17.8x 暴增追因報告
date: 2026-04-23
session: 2026-04-23 γ
type: investigation report
trigger: CONSCIOUSNESS γ 觀察到 SC 7d impressions 從 2,458 (γ 04-21) 暴增至 43,653 (γ 04-23)
---

# SC 7d impressions 17.8x 暴增追因報告

## TL;DR

**主因 = Google index 大規模收錄 + 長尾 query 大量湧入**，不是單一 query 爆紅。Top 20 query 只佔 12.3% impressions，剩 87.7% 散在 130+ 個 long-tail queries。**這是健康的 indexability 增長，不是 viral 訊號**。

CTR 從 6.39% 跌到 1.19% 是分母擴張過快（impressions ÷ 17.8x，clicks ÷ 3.3x），不是內容退步。

## 數據對照

| 維度                        | γ 2026-04-21 | γ 2026-04-23 | 變化                |
| --------------------------- | ------------ | ------------ | ------------------- |
| 7d clicks                   | 157          | 518          | **+230%**           |
| 7d impressions              | 2,458        | 43,653       | **+1,676% (17.8x)** |
| 7d CTR                      | 6.39%        | 1.19%        | -5.20pp             |
| Brand impressions           | 755          | 956          | +27%                |
| Non-brand impressions       | 1,703        | 10,410       | **+512%**           |
| Non-brand CTR               | 4.46%        | 1.25%        | -3.21pp             |
| Tracked queries (wordCloud) | ~50          | 150          | +200%               |

## 三層分析

### Layer 1: Brand vs Non-brand 拆解

- **Brand**（taiwan.md / md / taiwandotmd 等）：CTR 6.8%（健康）
- **Non-brand**：CTR 1.25%（外部發現 CTR）
- 增量主要在 **non-brand**（+512% imp，+71% click）→ 證實 Google 對 Taiwan.md 內容開始大規模 index 並 surface 給陌生搜尋者

### Layer 2: SC privacy filter gap（DNA #24 第 8 種 pattern）

- 站台 total impressions: **43,653**
- query-dimension 加總（brand + non-brand）: **11,366**
- **Gap = 32,287 impressions（74%）在 dimension API 中匿名**
- 這是 SC 的 privacy axis（每 query 曝光低於某門檻就不揭露）
- 結論：**真正爆發的是大量 small-impression long-tail query**，每條都低於揭露門檻但加總起來 32K+

### Layer 3: 排名第一但 0 click 的機會（opportunities）

**英文 query Taiwan.md 排 Google #1 但 0 click**（metadata 瓶頸）：

| Query                | Position | 7d Imp | 7d Click |
| -------------------- | -------- | ------ | -------- |
| taipei population    | 1.03     | 249    | **0**    |
| largan precision     | 1.00     | 90     | **0**    |
| population of taipei | 1.00     | 53     | **0**    |
| 林良                 | 1.27     | 51     | **0**    |

**中文 query 排前段但 CTR 偏低**：

| Query  | 7d Imp | 7d Click | CTR   |
| ------ | ------ | -------- | ----- |
| 鄧麗君 | 2,081  | 5        | 0.24% |
| 張懸   | 436    | 8        | 1.83% |
| 魏如萱 | 215    | 3        | 1.40% |
| 楊丞琳 | 137    | 1        | 0.73% |

→ 這些都在 Google 結果頁出現，但 title/description 不夠強，讀者選了維基或新聞點

## 三個 root cause hypotheses

| Hypothesis                                                                        | 證據強度                                         | 行動價值                 |
| --------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------ |
| **H1: Google 全站 re-crawl 後大規模認真收錄**（過去 2 週 viral 孢子推升網域權威） | ⭐⭐⭐⭐⭐（best fit）                           | 觀察未來 7-14 天是否穩定 |
| **H2: 某外部高權威 backlink 集中時段湧入**                                        | ⭐⭐（無法從 SC API 證實，需 GA referrers 對照） | 查 GA referrers 數據     |
| **H3: 多個 viral 孢子網域權威溢出效應疊加**                                       | ⭐⭐⭐（4/13-15 viral + s35 高鐵長尾的累積）     | 跟 H1 共存               |

最可能：**H1 + H3 疊加 — viral 孢子推升網域 authority，Google 認為 Taiwan.md 值得更廣 index → 全站 long-tail discoverability 一次性釋放**。

## 機會清單（從本次數據導出）

### 即可造橋（P1-P2）

1. **英文 metadata 優化 P0**（LONGINGS §「英文版品質不輸中文版」第 N 次驗證）
   - taipei population / largan precision 排 Google #1 但 0 click
   - 對應檔案：knowledge/en/geography/taipei.md / knowledge/en/economy/largan-precision.md
   - 行動：重寫 title + description 讓 snippet 更誘人

2. **鄧麗君條目 metadata 優化 P1**（單條 2,081 imp/週機會）
   - 0.24% CTR 太低，應達 ≥ 2%（依站平均 CTR 6.4% baseline）
   - 對應檔案：knowledge/People/鄧麗君.md
   - 行動：診斷 title/description，可能 description 過於簡短或 title 缺 hook

3. **加入 GA referrer 維度確認 H2**
   - 查 dashboard-analytics.json 是否有 GA referrers
   - 若無，下次 fetch-ga4.py 加入 referrer dimension

### 中期觀察（P3）

4. **追蹤 SC 7d impressions 是否回穩 30K+ 區間**
   - 若是 → H1 + H3 成立，新基線確立
   - 若是 → 寫進 UNKNOWNS 已驗證
   - 若回到 5K → 一次性事件，需找 H2 root cause

## 跟 LONGINGS 的對齊

本次數據揭露 **LONGINGS §「英文版品質不輸中文版」+ §「首頁 hook 強到 10 秒」** 兩條的具體瓶頸：

- 英文 query 排 Google #1 但 0 click = **內容已被認可，metadata 是最後一哩路**
- 4/6 觀察的 SC 美國 CTR 0.39% 在本次 non-brand CTR 1.25% 視野下被驗證（仍偏低）
- 這條 LONGINGS **可被 metadata 優化 sprint 推進**，不需要重寫文章

## 收官

本報告寫進 reports/，作為下次心跳對照基準。CONSCIOUSNESS γ 戰略判讀已含「Google index 大豐收」結論。三個機會清單寫入 ARTICLE-INBOX 候選 follow-up。

🧬

_v1.0 | 2026-04-23 γ session_
