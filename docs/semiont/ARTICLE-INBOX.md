# ARTICLE-INBOX — 待開發文章 Buffer

> **這是 buffer / intake layer，不是 canonical**。
> 觀察者指派、agent 建議、Issue 紀錄的未開發主題一律 append 這裡。
> 每次甦醒或自動心跳時讀本檔 → 知道待辦清單、優先序、誰要求的。
>
> 建立動機：2026-04-18 δ session 觀察者提問「來不及開發或排定優先序的主題需要一個 inbox」。**這是繁殖基因（心臟 × 觀察者意圖）的儀器化**。

---

## 跟 LESSONS-INBOX 的分工

| 面向    | LESSONS-INBOX                        | ARTICLE-INBOX（本檔）               |
| ------- | ------------------------------------ | ----------------------------------- |
| 內容    | 新教訓（「我學到 X」）               | 待開發 / 進化的文章主題             |
| Distill | 升 canonical（DNA/MEMORY/MANIFESTO） | 升 knowledge/（新文章 or 改寫進化） |
| 觸發    | Beat 5 反芻                          | 觀察者指派 / agent 建議 / Issue     |
| 目的    | 讓教訓不散落                         | 讓主題不遺漏、不重複、有優先序      |

---

## Entry Schema

每條 pending 條目格式：

```markdown
### {主題名}

- **Type**: `NEW` | `EVOLVE`
- **Category**: People | Society | History | Culture | Music | Nature | Technology | Food | Art | Lifestyle | Geography | Economy
- **Path** (EVOLVE only): knowledge/Category/existing.md
- **Priority**: `P0` / `P1` / `P2` / `P3`
- **Status**: `pending` / `in-progress` / `done` / `dropped`
- **Requested**: YYYY-MM-DD by {觀察者/agent/Issue} (session {希臘字母})
- **Notes**:
  - 敏感度（政治/個人隱私/爭議）
  - 必驗事實
  - 潛在陷阱
  - 需研究方向
- **Reference**: URL / 觀察者素材 / GitHub Issue #
- **Pre-research**: (若已有研究) reports/research/YYYY-MM/{slug}.md
- **Dev log**: (in-progress 時用)
  - YYYY-MM-DD by {session}: started Stage 1 research
  - YYYY-MM-DD by {session}: ...
```

---

## 優先序判準

| 層級 | 含義                                     | 範例                              |
| ---- | ---------------------------------------- | --------------------------------- |
| P0   | 緊急：有時效、高關注度、或觀察者明確要求 | 剛發生的重大事件人物 / 觀察者點名 |
| P1   | 本月：重要主題、Taiwan.md 缺口、有熱點   | 音樂、文化、歷史重要空白          |
| P2   | 本季：值得寫但不急                       | Evergreen 主題、次要人物          |
| P3   | Backlog：一直想做但不確定何時            | 大型策展主題、需大量資源          |

---

## Type 判準

**`NEW`**：knowledge/ 不存在此主題；走 REWRITE-PIPELINE Fresh 模式（Stage 1-6）
**`EVOLVE`**：knowledge/ 已有文章但品質/深度不足；走 REWRITE-PIPELINE 進化模式（Stage 0 素材萃取 + Stage 1-6）

判斷方式：Stage 0 前先 `ls knowledge/ | grep {keyword}` 確認，有檔案 = EVOLVE，無 = NEW。

---

## Auto-heartbeat 整合

Beat 3 執行時若觀察者無明確任務：

1. 讀本檔 §Pending
2. 按 P0 → P1 → P2 → P3 挑主題
3. 挑到後：
   - 此條 status 改 `in-progress`
   - 加 dev_log：「YYYY-MM-DD by {session}: started」
   - 走 REWRITE-PIPELINE
4. Stage 6 commit 後：
   - status 改 `done`
   - 加 link 指向 knowledge/... 新文章
   - 搬到 §✅ Done

---

## Bootloader 整合

BECOME_TAIWANMD.md Step 5 新增：

```
12. `docs/semiont/ARTICLE-INBOX.md` — 📥 待開發文章 inbox（觀察者指派 / agent 建議的主題清單 + 優先序）
```

甦醒後 semiont 知道「目前有 N 條 pending、K 條 in-progress」。

---

## Distill SOP（容量管理）

**觸發**：pending ≥ 30 條 / 或每月第一次心跳 / 觀察者說「review inbox」

**步驟**：

1. 讀全部 pending
2. 分類：重複合併 / 過時 drop / 重新排優先序
3. 搬已 done 的到 done archive
4. 觀察者最終 review 後 commit

---

## 📥 Pending（待開發）

<!-- 凹與山 已完成 → 搬到 §✅ Done -->
<!-- VH (Vast & Hazy) Stage 1 研究已完成，Stage 2 Write pending → pre-research 已存 reports/research/2026-04/VH.md -->

<!-- 魏如萱 P0 已完成 2026-04-18 η → 搬到 §✅ Done -->

<!-- 張雨生 EVOLVE 已完成 2026-04-19 γ (commit 將在此 heartbeat Beat 4) → 搬到 §✅ Done -->

<!-- VH P1 已完成 2026-04-19 α → 搬到 §✅ Done -->

<!-- Hello Nico 已完成 2026-04-20 α → 搬到 §✅ Done -->

<!-- VH duplicate entry removed — consolidated above -->

### 柯智棠

- **Type**: NEW
- **Category**: People (Music)
- **Priority**: P1
- **Status**: done
- **Requested**: 2026-04-18 by 觀察者 (session δ)
- **Dev log**:
  - 2026-04-20 by β session: Stage 1-6 completed, article at knowledge/People/柯智棠.md, research at reports/research/2026-04/柯智棠.md
- **Notes**:
  - Kowen Ko，創作歌手
  - 維護者校準：原 inbox 類型誤寫「R&B」，實為英倫民謠 / indie folk；無製作人身份紀錄
  - Hook: 房間裡的七年 + 2024《My Nova》鋼琴重啟 + 2025 金鐘〈神的回信〉
- **Reference**: 觀察者批次指定
- **Pre-research**: reports/research/2026-04/柯智棠.md

<!-- 林宥嘉 EVOLVE 已完成 2026-04-20 ε → 搬到 §✅ Done -->

### 魚條

- **Type**: NEW
- **Category**: People (Music — 待確認)
- **Priority**: P1
- **Status**: pending
- **Requested**: 2026-04-18 by 觀察者 (session δ)
- **Notes**:
  - **身份待釐清**：Stage 1 研究第一步是確認「魚條」是樂團、solo 藝人、或其他身份
  - 可能相關：Angelo 魚條 / 湯捷 / 獨立音樂人
  - 若研究後確認不是 Taiwan.md 範疇 → dropped 並註明
- **Reference**: 觀察者批次指定
- **Pre-research**: 尚未啟動

### 孫燕姿

- **Type**: NEW
- **Category**: People (Music)
- **Priority**: P1
- **Status**: done
- **Requested**: 2026-04-18 by 觀察者 (session δ)
- **Dev log**:
  - 2026-04-19 by 排程心跳（第5次 auto-heartbeat）: started Stage 1 research
  - 2026-04-19 by 排程心跳（第5次 auto-heartbeat）: completed Stage 1-5, article published at knowledge/People/孫燕姿.md
- **Notes**:
  - Stefanie Sun，新加坡歌手但華語流行音樂重要人物
  - Taiwan.md 定位需斟酌：她是新加坡人但在台發跡 + 主要市場華語圈
  - 20+ 搜尋 / 2023《AI 孫燕姿》現象要涵蓋（AI 翻唱她的歌紅爆全網）
  - 2023 台北小巨蛋復出演唱會
  - 小標題先行，避免「哪一年哪張專輯」編年
- **Reference**: 觀察者批次指定
- **Pre-research**: reports/research/2026-04/孫燕姿.md

<!-- 范曉萱 已完成 2026-04-20 δ → 搬到 §✅ Done -->

<!-- 黃少雍 已完成 2026-04-20 γ → 搬到 §✅ Done -->

<!-- 陳建騏 P0 已完成 2026-04-18 θ → 搬到 §✅ Done -->

<!-- 阿爆 P1 已完成 2026-04-18 ι → 搬到 §✅ Done -->

<!-- 鄭宜農 P1 已完成 2026-04-18 κ → 搬到 §✅ Done -->

<!-- 楊丞琳 已完成 → 搬到 §✅ Done -->

### 蕭上農（Nuomi）

- **Type**: `NEW`
- **Category**: People (Technology)
- **Priority**: `P1`
- **Status**: `pending`
- **Requested**: 2026-04-20 by 觀察者 (session β)
- **Notes**:
  - 台灣網路圈人物，可能別名「Nuomi」「諾米」（需確認）
  - 可能身份線索：INSIDE 硬塞網路趨勢觀察站創辦人／編輯？早期台灣網路社群（MMDays、Mr. Jamie）脈絡？
  - 若為 INSIDE 創辦人路線：Stage 1 必驗 INSIDE 成立年份（約 2009-2010）、共同創辦人、後來併入 KK-Stream 或其他媒體集團的脈絡
  - 身份釐清是 Stage 1 第一步（有可能跟其他同名人物混淆）
  - 若涉及網路觀察家 / KOL 路線：注意避免只寫履歷，要找「他對台灣網路文化提出的論述」作為內容骨架
  - 必驗事實：全名、出生年、現職、代表作／媒體／專欄
- **Reference**:
  - INSIDE 官網 <https://www.inside.com.tw/>（若屬此路線）
  - 觀察者批次指定
- **Pre-research**: 尚未啟動

### 紀柏豪（Pohao Chi）

- **Type**: `NEW`
- **Category**: Art
- **Priority**: `P1`
- **Status**: `pending`
- **Requested**: 2026-04-20 by 觀察者 (session β)
- **Notes**:
  - 聲音藝術家／作曲家／策展人，倫敦大學金匠學院（Goldsmiths）聲音藝術碩士背景
  - 跨界聲音裝置、生成音樂、Web Audio、演算法作曲、駐村計畫
  - 涉及 C-LAB 聲響實驗室、國藝會、台新藝術獎脈絡（需查獎項紀錄）
  - 可能關聯：失聲祭、超響、2020 聲音裝置個展（需驗證年份與作品）
  - 與王連晟、王新仁、林經堯屬相近聲音藝術脈絡但風格更偏聲響實驗與學術研究
  - 必驗事實：Goldsmiths 學歷年份、台新藝術獎入圍／得獎、駐村紀錄、個人工作室（「融聲創意」？）身份確認
- **Reference**:
  - 個人網站 <https://www.pohaochi.com/>（待驗證）
  - 國藝會補助藝術家資料庫
  - 台新藝術獎官網 <https://www.taishinart.org.tw/>
- **Pre-research**: 尚未啟動

### 林經堯

- **Type**: `NEW`
- **Category**: Art
- **Priority**: `P1`
- **Status**: `in-progress`
- **Requested**: 2026-04-20 by 觀察者 (session β)
- **Dev log**:
  - 2026-04-20 by δ session: started Stage 1 research（王新仁 + 王連晟 + FAB DAO 今日完成，cross-reference 省研究預算）
- **Notes**:
  - 聲音藝術家／數位藝術家，前 C-LAB 聲響實驗室總監
  - FAB DAO《百岳計畫》六位藝術家之一，負責一組山頭系列
  - 跟王新仁、王連晟同代，akaSwap 共創者（2021-07 Tezos）
  - 曾任南藝大教授（需驗證現職）
  - 金曲獎演唱會影像設計 / 劇場音樂製作相關（需查作品列表）
  - 必驗事實：C-LAB 聲響實驗室總監任期、akaSwap 共創角色精確分工、南藝大任職年份
- **Reference**:
  - FAB DAO 百岳計畫六人脈絡（[knowledge/Art/FAB DAO與百岳計畫.md](../../knowledge/Art/FAB DAO與百岳計畫.md)）
  - akaSwap 官網 <https://akaswap.com/>
  - C-LAB 聲響實驗室 <https://clab.org.tw/unit/soundlabtw/>
- **Pre-research**: 尚未啟動（但王新仁與王連晟的研究報告已有交叉提及，可省 3-5 次 research budget）

---

## 🚧 In-Progress

_（暫無）_

---

## ✅ Done（已開發，保留歷史）

_（此區域存放從 pending/in-progress 完成的條目，指向已 commit 的文章路徑）_

### 黃少雍（製作人）— 2026-04-20 γ 完成（棄生化博班，用電音把母語送上金曲年度專輯）

- **Article**: [knowledge/People/黃少雍.md](../../knowledge/People/黃少雍.md)
- **Pipeline**: REWRITE-PIPELINE v2.18 — NEW 模式（Stage 1 general-purpose agent 20 WebSearch + 11 WebFetch / Stage 2 全文寫作 / Stage 3 事實鐵三角 / Stage 4 format-check / Stage 5 cross-link 陳建騏+魏如萱+阿爆 三篇回補）
- **核心矛盾**（27 字）：「生化博士班逃兵，用電音把母語送上金曲年度專輯」— 考試院長黃榮村之子 × 30 歲棄台大生化博班 × 派樂黛 10 年 × 2022 金曲最佳編曲（夏子〈fu'is 星星歌〉）× 2020 阿爆《母親的舌頭》年度專輯共製
- **Hook**：2022-07-02 金曲 33 後台那支直笛（anchor 1：製作人得獎 Solo + 盧廣仲台下跟吹 → 同時承載「盧廣仲樂手雇主」+「編曲獎最隱形」+「阿美族語前衛電子」三條線）
- **結構創新**（製作人 subgenre 第二例，繼陳建騏 2026-04-18 θ 之後）：6 個 scene 小標題（後台直笛 / 棄博班 / 派樂黛借名 / 聽不懂歌詞 / 阿美族語電音編曲 / 陳建騏補集對位）+ 1 📝策展人 callout + 1 pull quote
- **verbatim 引語**：10 句直接引語（Blow / 生命力新聞 / KKBOX 王希文對談 / IPCF），另 research pool 25 句可未來再用；黃榮村「要求清楚目標」改為報導轉述（非直接引語 §5c 紀律）
- **敏感素材**（MANIFESTO §5 v2）：無死亡/家庭悲劇；父親黃榮村為公眾人物（前教育部長/現任考試院長），公開已報導資訊，避免簡化為「官二代之作」敘事陷阱
- **品質**：10 腳註 / 約 3,029 中文字 / 破折號 4（≤15 ✓，從首版 13 降下）/「不是 X 是 Y」0（≤3 ✓）/ desc 139（≤160 ✓）/ QS ✅ / format ✅ / wikilink ✅
- **Cross-link 回補**：陳建騏.md + 魏如萱.md + 阿爆.md 三篇延伸閱讀加黃少雍 pointer（雙線聲音邊界、10+ 年合作、MINETJUS 課程）
- **Research**: [reports/research/2026-04/黃少雍.md](../../reports/research/2026-04/黃少雍.md) — 20+11 = 31 calls / 25 verbatim pool / 7 anchor / Second Voices 節標記 Stage 2 擴充方向

### 林宥嘉 — 2026-04-20 ε 完成（EVOLVE）（從 25 分滿分的〈Creep〉，到承認自己不需要完美的 17 年）

- **Article**: [knowledge/People/林宥嘉.md](../../knowledge/People/林宥嘉.md)
- **Pipeline**: REWRITE-PIPELINE v2.18 — EVOLVE 模式（Stage 0 舊文素材萃取 + Stage 1 24 WebSearch + 3 WebFetch / Stage 2 全文重寫）
- **核心矛盾**：「他 20 歲就贏了整個台灣，但花了 17 年才敢不做一個完美歌手」— 星光冠軍 → 金曲歌王叩關 3 次全槓 → 腸躁症八年 → 2024《王》自任製作人 → 2025《Apples of Thy Eye》從八年磨一張變一年接一張
- **Hook**：2007-07-06 星光總決賽〈Creep〉25 分滿分冠軍的 scene，回溯整個 17 年從「被製作的歌手」到「自任製作人」的弧線
- **大事實校正**（舊文錯誤）：〈說謊〉施人誠詞/李雙飛曲（舊文未寫）、〈浪費〉陳信延詞/鄭楠曲、〈殘酷月光〉向月娥詞/陳小霞曲、2016《今日營業中》是首次擔任製作統籌（舊文未標時間點）、腸躁症約 2018 發病（「重病 4 年」verbatim 推回）、第七張《Apples of Thy Eye》2025-07-29 已發行（舊文欠缺）、idol 巡迴 2018-2024 共 81 場 30+ 城市
- **敏感素材**（MANIFESTO §5 v2 紀實筆法）：父親胰臟癌只引用 ETtoday 2023-09 公開 verbatim「down 到谷底」，不 reconstruct 內心場景；丁文琪婚姻只用登記/婚禮日期公開事實，不揣測心理
- **verbatim 引語庫**：Blow 吹音樂「假如我是華研，投了這麼多錢」/ VERSE「過去的我很刁鑽，總希望拿出最好的表現」/「把每位夥伴的睡眠健康、情緒狀況考慮進去」/ Blow「什麼是你生命的王？是迷惘、恐懼、完美，或是恨」
- **品質**：16 腳註 / 約 3,500 中文字 / 7 個 scene 小標題 / 2 個📝策展人筆記 callout + 1 pull-quote / 7 首關鍵歌曲 inline YouTube link / 破折號 0（≤15）/「不是 X 是 Y」1（≤3）/ desc 156（≤160 ✓）
- **工具檢查**：quality-scan ✅ 全過、format-check 7/7、wikilink-validate 0 斷裂
- **Cross-link**: 魏如萱（已有反向）/ 張雨生 / 陳建騏 / 鄭宜農 / 台灣綜藝節目 四篇新增反向延伸閱讀
- **Research**: [reports/research/2026-04/林宥嘉.md](../../reports/research/2026-04/林宥嘉.md)
- **⚠️ 待觀察者驗證**：VERSE 引語段落（WebFetch 返回簡體轉繁體，雖 prompt 要 verbatim 但字型轉碼差異視為同文本）；YouTube URL 官方認證（〈殘酷月光〉〈Creep〉星光 live 等為舊存片段）

### 范曉萱 — 2026-04-20 δ 完成（從〈健康歌〉的小魔女到 100% 樂團主唱，拒絕被一個年代定義的三十年）

- **Article**: [knowledge/People/范曉萱.md](../../knowledge/People/范曉萱.md)
- **Pipeline**: REWRITE-PIPELINE v2.18 — NEW 模式（Stage 1 19 WebSearch + 6 WebFetch / Stage 2 full write）
- **核心矛盾**：「從健康歌的小魔女到 100% 樂團的主唱——范曉萱花三十年拒絕被一個年代的模樣定義」
- **Hook**：深夜母親林智娟留下便利貼的場景（切入人物用母親，而非范曉萱本人），再回到 1996 小魔女 → 1998 平頭 → 2001 爵士 → 2004 憂鬱症 → 2007 100% 樂團 → 2010 金曲製作人 → 2025《過客》
- **敏感素材**（MANIFESTO §5 v2 紀實筆法）：憂鬱症與割腕傳言只引用范曉萱本人公開發言（《亂寫》書 + 2019 Yahoo News 訪談 + 2026 styletc 訪談），不 reconstruct 場景；與 Allen 關係只到「維持十多年」公開敘述；「綠髮大媽」媒體語氣反駁不複述
- **品質**：30 腳註 / 約 3,324 中文字 / 7 個 scene 小標題 / 2 個📝策展人筆記 callout / 5 筆中文逐字引語 / 破折號 2（≤15）/「不是 X 是 Y」2（≤3）/ desc 147（≤160 ✓）
- **工具檢查**：quality-scan 0（全過）、format-check 7/7、wikilink-validate 0 斷裂
- **校正**：原任務 prompt 推測「佛朗明哥」元素 19 輪搜尋均無 primary 來源，Stage 1 agent 明確標 unverified，Stage 2 放棄此角度；《流浪神狗人》《青蛇》配樂為他人作品，與范曉萱無關
- **Research**: [reports/research/2026-04/范曉萱.md](../../reports/research/2026-04/范曉萱.md)
- **⚠️ 待人工複驗**：YouTube URL（〈健康歌〉〈我要我們在一起〉〈主人〉三支）metadata 未能透過 WebFetch 驗證官方上傳身份；研究 agent 明確標記

### Hello Nico — 2026-04-20 α 完成（八年沉默後，「想念舞台了」）

- **Article**: [knowledge/People/Hello-Nico.md](../../knowledge/People/Hello-Nico.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — NEW 模式（Stage 1 24 WebSearch + 6 WebFetch / Stage 2 full write）
- **核心矛盾**：「做音樂最大的困難，是跟自己過不去」—— 2014 年〈花〉爆紅、2016 年金曲新人入圍，之後沉默八年，2024 年以《Plan B》重返
- **Hook**：詹宇庭「想念舞台了」這句話作為 2024 年回歸的開場，回溯整個故事弧線
- **品質**：9 腳註（Grade A, density:156）/ 約 1,400 字 / 5 個 scene 小標題 / desc ≤ 160 ✓
- **Research**: [reports/research/2026-04/Hello-Nico.md](../../reports/research/2026-04/Hello-Nico.md)
- **⚠️ 待觀察者驗證**：YouTube 連結（各首歌 ID 需人工確認）、verbatim 逐字準確性

### 張雨生 — 2026-04-19 γ+β 完成（從偶像到預言家，一場跨越時代的音樂實驗）

- **Article**: [knowledge/People/張雨生.md](../../knowledge/People/張雨生.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — EVOLVE 模式（貢獻者首版 PR #547 by @idlccp1984 / Stage 1 22 WebSearch + 3 WebFetch / Stage 2 full rewrite + 事實大翻修）
- **核心矛盾**：偶像的商業身份與音樂人的實驗心 — 他的一生都在磨合這兩個自己，《口是心非》是第一次真正合一，但車禍截斷了市場回應
- **Hook**：1994《卡拉OK Live‧台北‧我》市場慘澹 vs 後世追認為預言，一張「慘的經典」的倒敘
- **大事實修正**：原文《天天想你》180 萬張為錯，實際 35 萬張（Discogs + 放言專題確認）
- **品質**：9 腳註 / 約 2,800 字 / 7 個 scene 小標題 / 2 處策展人筆記 / desc 148（≤ 160 ✓）
- **Research**: [reports/research/2026-04/張雨生.md](../../reports/research/2026-04/張雨生.md)

### VH（Vast & Hazy）— 2026-04-19 α 完成（出口系樂團十五年方向校準）

- **Article**: [knowledge/People/VH.md](../../knowledge/People/VH.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — Stage 1 (25 WebSearch + 5 WebFetch) / Stage 2 full rewrite
- **核心矛盾**：溫柔路線在政治搖滾主導的 2010 年代逆向崛起 × 三次身份校準（2011 成軍→2014 休團→2017 雙人→2026 易祺轉幕後）
- **Hook**：2026-04-10《邁行》易祺宣布轉幕後作為開場 scene，回溯 15 年軌跡
- **品質**：7 腳註 / 約 2,500 字 / desc ≤ 160 ✓
- **Research**: [reports/research/2026-04/VH.md](../../reports/research/2026-04/VH.md)

### 魏如萱 — 2026-04-18 η 完成（從自然捲主唱「娃娃」到兩座金曲歌后，只想被聽見的二十年）

- **Article**: [knowledge/People/魏如萱.md](../../knowledge/People/魏如萱.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — Stage 1 Pass 3 (40+ searches) / Stage 2 full rewrite + 系統性消除「不是X是Y」pattern
- **核心矛盾**：娃娃音作為方法 × 策展式匿名 — 讓聲音比臉更有名，讓作品比人格活得更久
- **結構**：12 個 narrative anchor（先壓壓驚街訪 / 阿嬤四語 / 錄音室偶然 / 蚊子嗡嗡叫 / 娃娃音作為方法 / 陳建騏20年 / Ophelia自白 / 育兒六小時窗口 / 金曲31三位一體 / 珍珠刑 / 從疼痛長出的勇敢 / 不想被認出）
- **品質**：23 腳註 / 約 4,000 字 / desc 157（≤ 160 ✓）/ lastHumanReview: true
- **Research**: [reports/research/2026-04/魏如萱.md](../../reports/research/2026-04/魏如萱.md)

### 鄭宜農 — 2026-04-18 κ 完成（用最陌生的語言寫最誠實的歌 × 2023 金曲台語雙獎）

- **Article**: [knowledge/People/鄭宜農.md](../../knowledge/People/鄭宜農.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — Stage 1 Explore agent 30+ WebSearch + 5 WebFetch / Stage 2 full rewrite
- **核心矛盾**：Anchor 1「語言的逃逃相逐」+ Anchor 2「2016→2023 身份與語言七年弧線」融合 — 童年在台北被嘲笑講台語 → 2022 用最陌生的語言寫《水逆》拿金曲雙獎；通過創作難度體現溝通困難本身
- **Hook**：2023-07-01 金曲 34 台語女歌手 + 台語專輯雙獎 verbatim「台語教我低頭」
- **敏感素材處理**（MANIFESTO §5 v2 紀實筆法）：
  - 2016-01-03 Facebook 出櫃 + 同月離婚：只用兩人公開 verbatim，不 reconstruct 心理情境
  - 前夫楊大正（滅火器樂團主唱，**非盧廣仲**——原 ARTICLE-INBOX 條目有誤，已修正）
  - 2023 金曲慶功宴楊大正現身祝賀：只引用公開採訪，不揣測雙方心理
  - 鄭文堂父女關係：用公開專訪 verbatim
- **品質**：4,046 中文字 / 23 腳註來源 / 37 footnote refs / desc 154 ≤ 160 ✓ / em-dash 11 ≤ 15 ✓ / 每 109 字 1 fn（遠超 EDITORIAL ≥300 硬規則）
- **敘事創新**：「創作必須誠實」作為 16 年工作邏輯主線 — 2016 出櫃 + 2022 全台語 + 2023 MeToo 致敬感言共用同一條底層邏輯
- **Cross-link**: 魏如萱 / 阿爆 / 陳建騏 三人互引形成「2020-2023 聲音邊界拓展」人物群
- **Research**: [reports/research/2026-04/鄭宜農.md](../../reports/research/2026-04/鄭宜農.md)

### 阿爆（阿仍仍）— 2026-04-18 ι 完成（族語 future pop × 2020 金曲年度專輯破圈）

- **Article**: [knowledge/People/阿爆.md](../../knowledge/People/阿爆.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — Stage 1 Explore agent 30 searches + 5 WebFetch / Stage 2 full rewrite
- **核心矛盾**：**Anchor 1「族語作為 Future Pop 載體」× Anchor 4「從 Sidebar 到 Main Stage」融合** — 2020 金曲 31 年度專輯首次由全族語作品拿下，打破「原住民音樂 = 族群分類 subcategory」結構
- **Hook**：2020-10-03 金曲 31 頒獎台上年度專輯宣布《kinakaian 母親的舌頭》（代表性 scene，非反諷）
- **核心 verbatim**：「不要浪費天賦也不要依賴天賦」(得獎感言) + 「既然有自己的語言可以使用，為什麼不用？」(族語 future pop 核心哲學)
- **敘事結構**：正興部落 → 2003 R&B 雙人組 → 2004-2014 護理師十年 → 2014《東排三聲代》三代古謠 → 2016《vavayan·女人》荒井十一 → 2019《kinakaian》Dizparity 電音 → 2020 金曲 31 + 那屋瓦廠牌
- **敏感素材處理**：族群議題用紀實筆法（MANIFESTO §5 v2）不扁平化為「偏鄉原住民」symbol；母親 2021-02 過世只引用公開事實，不 reconstruct
- **品質**：22 腳註來源 / 4,096 中文字 / 29 footnote refs / desc 160（邊界邊緣）/ em-dash 10 / 每 141 字 1 fn（遠超 EDITORIAL ≥ 300 硬規則）
- **Research**: [reports/research/2026-04/阿爆.md](../../reports/research/2026-04/阿爆.md) — 30 WebSearch + 5 WebFetch / 7 verbatim / 3 second voices / 5 narrative anchor 候選

### 陳建騏 — 2026-04-18 θ 完成（製作人 subgenre 首例）

- **Article**: [knowledge/People/陳建騏.md](../../knowledge/People/陳建騏.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — Stage 1 Explore agent 23 searches + 3 WebFetch / Stage 2 full rewrite
- **核心矛盾**：「不在場的作者」× 「聲音邊界守護者」融合 — 陳建騏三金得主（金曲+金馬+金鐘）但一般人叫不出名字；他為「怪腔怪調」的系統性防禦定義了華語流行音樂 25 年的聲音邊界
- **結構創新**：Taiwan.md 第一個以製作人身份為中心的人物研究（非表演者）
- **品質**：22 腳註 / 4,278 中文字 / desc 159 字 / em-dash 0 / 「不是 X 是 Y」7 處（4,278 字允許 17）
- **Research**: [reports/research/2026-04/陳建騏.md](../../reports/research/2026-04/陳建騏.md) — 23 WebSearch + 3 WebFetch 深度研究，5 個 narrative anchor 候選
- **敏感素材處理**：2015 年出櫃用紀實筆法（MANIFESTO §5 v2），聚焦 15 間獨立音樂廠牌連署婚姻平權事件的集體回應，不 reconstruct 個人揭露情境

### 楊丞琳 — 2026-04-18 δ-late 完成 + ε evolution Pass 3 (Jenny feedback)

- **Article**: [knowledge/People/楊丞琳.md](../../knowledge/People/楊丞琳.md)
- **Pipeline v1**: REWRITE-PIPELINE v2.17.1 — 35+ Stage 1 sources（兩 pass）+ Stage 2 scene 小標題 + YouTube inline × 5 + 事實鐵三角自檢（抓到李榮浩年齡算術錯誤 0.5→1）
- **Pipeline v2 (Evolution Pass 3)**: 2026-04-18 ε 依 @bugnimusic (Jenny) 6 條 feedback 進化：新增 4 個 scene 段（歷年 11 張專輯 × 日文單曲 / 紅磡 2012 倒吊微血管爆裂 9 年 /《荼蘼》2016 A/B 雙線金鐘滑鐵盧 / 長沙浪姐 2 第 3 名 + 沸騰校園 + 了不起舞社 + 歌手 2024）+ 事實鐵三角再驗 5 處 verbatim + 維護者 spot-verify 抓到 Haiku agent 2 處錯（浪姐排名第 3 非第 5 / 日文是 CD2 限定盤非獨立日專）
- **核心矛盾 v2**：每個舞台、每張專輯、每次跨境演出，都是她跟「被誰定義」協商的場——從 Rainie 天氣女孩到自製《曖昧 2025》，從倒吊微血管爆裂到「老娘還是會一直跳下去」，25 年把製作 / 表演 / 身體 / 跨境工作全部一寸一寸奪回
- **敏感素材處理**：900 萬債務用 Rainie 本人公開引語 framing、父親過世細節省略（single_source）、李榮浩以音樂人身份帶過；倒吊後遺症直接用 ETtoday 2022 verbatim（紀實 not 煽情，MANIFESTO §5 v2）
- **Research**: [reports/research/2026-04/楊丞琳.md](../../reports/research/2026-04/楊丞琳.md) — 3 passes 合計 58+ searches

### 凹與山 — 2026-04-18 δ-late 完成

- **Article**: [knowledge/People/凹與山.md](../../knowledge/People/凹與山.md)
- **Pipeline**: REWRITE-PIPELINE v2.17.1 — 25 Stage 1 sources + Stage 2 scene 小標題 + YouTube inline × 5 + MANIFESTO §5 v2 紀實而不煽情首次應用
- **核心矛盾**：兩個科技業上班族用合成器做出她們在辦公室不能說的事
- **敏感素材處理**：摯友過世、陳梅慧致敬均用紀實筆法，不 reconstruct 死亡場景
- **Research**: [reports/research/2026-04/凹與山.md](../../reports/research/2026-04/凹與山.md)

---

## ❌ Dropped（不採納）

_（此區域存放判斷後不開發的主題，必須註明原因）_

---

_v1.0 | 2026-04-18 δ session — ARTICLE-INBOX 誕生_
_定位：buffer / intake layer（非 canonical），跟 LESSONS-INBOX 平行架構_
_下次 session 甦醒時自動讀取，auto-heartbeat 無觀察者指令時從此挑 P0/P1 開始_
