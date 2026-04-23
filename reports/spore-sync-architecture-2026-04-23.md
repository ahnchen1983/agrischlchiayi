# 孢子數據雙寫架構：從 process rule 到 structural SSOT

> 起源：2026-04-23 δ session。觀察者指出孢子發佈 + harvest 後，文章底下 `SporeFootprint.astro` 的 section 讀的是文章 frontmatter `sporeLinks`，但 SPORE-PIPELINE 只寫 SPORE-LOG.md，導致讀者看不到孢子足跡。當下用 v2.6「雙寫原則」作為 process rule 修補，但這只是**紀律層**的補丁。本 report 思考**長期結構層**怎麼讓這個問題不再依賴紀律。

---

## 一、問題的結構性定位

### 1.1 現狀（v2.6 之後）

每次 harvest 要寫兩處：

```
harvest 事件
├─ docs/factory/SPORE-LOG.md            ← 工廠層（累積、session 備註、診斷文字）
└─ src/content/{lang}/{cat}/{slug}.md   ← 讀者層（當下快照、frontmatter sporeLinks）
   frontmatter.sporeLinks[]
```

這是**手動雙寫**，依賴 AI session 或人類記得兩邊都寫。

### 1.2 為什麼 process rule 不夠

v2.6 把「每次 harvest 都要雙寫」寫進 SPORE-HARVEST-PIPELINE Step 1.5，這是**必要條件**但**不充分**：

- **證據 1**：本次 δ session 發現 6 篇文章（謝德慶/草東/高鐵/Cicada/韓國瑜/鄭麗文）都已發孢子但沒 sporeLinks。代表 v2.6 之前沒人寫過——連「張懸與安溥」跟「李洋」這兩個例外都是觀察者手動加的。
- **證據 2**：多語言會放大——每篇文章 zh-TW/en/ja/ko 最多 4 份 frontmatter，一次 harvest 要寫 2 平台 × 4 語言 = 8 處。任何一處忘了寫就 drift。
- **證據 3**：紀律永遠有漏網。DNA #15 「工具造橋比紀律可靠」在這裡同樣成立——文件化寫成紅字只能降低漏網率，不能歸零。

### 1.3 失敗模式分類

| 模式               | 原因                                                        | 頻率                                           | v2.6 rule 能否抓到 |
| ------------------ | ----------------------------------------------------------- | ---------------------------------------------- | ------------------ |
| **漏寫（初次）**   | 發孢子時只記 SPORE-LOG，沒初始化文章 frontmatter sporeLinks | 高（歷史 90%+ 都沒）                           | ⚠️ 靠紀律          |
| **漏寫（後續）**   | 做了 harvest 卻只更新 SPORE-LOG，文章數字過期               | 中（每次 harvest 都有風險）                    | ⚠️ 靠紀律          |
| **跨層數字 drift** | 兩邊都寫但數字不一致（複製貼上錯誤、session 中斷）          | 低                                             | ❌ 無法偵測        |
| **URL 漂移**       | X edit 造成 v1/v2 URL 切換，文章 frontmatter 還指 v1        | 中（已發生兩次：#36 高鐵 / #42 認知作戰）      | ❌ 無法偵測        |
| **多語言 drift**   | zh-TW 更新了但 en/ja/ko 沒跟上                              | 高（翻譯 session 跟 harvest session 通常分開） | ❌ 無法偵測        |
| **孤兒指標**       | SPORE-LOG 有 row 但所有文章都沒 sporeLinks 指過去（或反之） | 中                                             | ❌ 無法偵測        |

結論：v2.6 rule **只能降低模式 1/2 的發生率**，模式 3-6 是結構問題，不是紀律問題。

---

## 二、架構選項

列出六種架構方向，每個都檢查：「**數據流向**」「**SSOT 在哪**」「**失敗模式解決率**」「**遷移成本**」。

### 2.1 Option A：SPORE-LOG 為 SSOT，文章 frontmatter 是 derived

- **數據流**：harvest → SPORE-LOG（唯一寫入點）→ 腳本解析 SPORE-LOG → 產出 `spore-metrics.json` → SporeFootprint 讀 JSON 而非 frontmatter
- **SSOT**：SPORE-LOG.md
- **失敗模式解決**：模式 1-6 全部消失（文章 frontmatter 不再存數字）
- **成本**：
  - 需要寫 SPORE-LOG 的 markdown parser（現況自由文字、table 格式混用，parse 難度中等）
  - SporeFootprint 從 frontmatter 讀改成 build-time join JSON
  - 失去「從文章檔案 grep 出哪些孢子指著它」的能力
- **風險**：SPORE-LOG 現在是「人/AI 手寫的敘事 log」，要當機器可解析的 SSOT 需要 schema 收斂；敘事性跟結構性互相拉扯

### 2.2 Option B：文章 frontmatter 為 SSOT，SPORE-LOG 是 derived

- **數據流**：harvest → 文章 frontmatter（唯一寫入點）→ 腳本掃 471 篇文章 → 聚合產出 SPORE-LOG
- **SSOT**：frontmatter
- **失敗模式解決**：解決模式 3（跨層 drift）；模式 1/2/4/5 仍在
- **成本**：
  - SPORE-LOG 的敘事內容（D+0/D+1/D+7 切片、session 備註、跨筆比較、Pattern 觀察）在 frontmatter 放不下（會污染 prose metadata）
  - 聚合查詢需要 build 階段掃描全部 content
- **風險**：SPORE-LOG 的「診斷故事」價值高於「metrics 數據」，把 SSOT 從 log 抽走等於削弱它的用途

### 2.3 Option C：獨立 metrics 資料庫（`spore-metrics.json`）

- **數據流**：harvest → `public/api/spore-metrics.json`（以 URL 或 spore_id 為 key）→ SPORE-LOG 寫 narrative row（引用 metrics JSON）→ SporeFootprint 讀 JSON
- **SSOT**：spore-metrics.json（只放數字）
- **失敗模式解決**：模式 1/2/3/4 全部消失；模式 5（多語言）變成一次寫（JSON 跨語言共用）；模式 6 靠 CI
- **成本**：
  - 新建 JSON schema + generator script
  - SporeFootprint 改讀 JSON + frontmatter（frontmatter 只留 pointer: platform/date/url）
  - SPORE-LOG 繼續存在但不再是數字 SSOT
- **風險**：多了一個資料層；需要 refresh-data 流程納入 metrics JSON 生成

### 2.4 Option D：自動化 harvest 工具（維持雙寫，但腳本化）

- **數據流**：harvest 不改，但 `scripts/tools/harvest-spore.py <URL>` 一次性寫 SPORE-LOG + 文章 frontmatter
- **SSOT**：無（仍然雙寫）
- **失敗模式解決**：模式 1/2 降到近零（只要用腳本）；模式 3/4/5/6 未解
- **成本**：低（一個 script）
- **風險**：腳本 bug = drift；AI session 如果不用腳本改回手動就退回原狀

### 2.5 Option E：Hybrid — 指標 JSON 為 SSOT + 文章 frontmatter 放 pointer（**推薦**）

- **數據流**：

  ```
  publish 事件（一次性）：
    文章 frontmatter.sporeLinks 加 {platform, date, url} 指標
    SPORE-LOG 加 row（含 URL）

  harvest 事件（反覆）：
    Chrome MCP a11y snapshot
      → spore-metrics.json[url] = {views, likes, reposts, comments, shares, snapshot_at}
      → SPORE-LOG.md row.最後 harvest 欄加敘事（D+0/D+1 切片 + 跨筆比較）
    文章 frontmatter 不動（pointer 不變）

  render 事件（build）：
    SporeFootprint.astro 讀 frontmatter.sporeLinks[].url
      → 用 url 查 spore-metrics.json 取數字
      → 渲染「這篇文章去過的地方」section
  ```

- **SSOT**：
  - Pointer（platform/date/url）→ 文章 frontmatter
  - Metrics（views/likes/reposts/comments/shares）→ spore-metrics.json
  - Narrative（切片、session 備註）→ SPORE-LOG.md
- **失敗模式解決**：
  - 模式 1（初次漏寫 pointer）→ 仍靠紀律，但只需一次寫
  - 模式 2（後續漏寫數字）→ **消失**（harvest 只寫 JSON）
  - 模式 3（跨層 drift）→ **消失**（數字只一個來源）
  - 模式 4（URL 漂移）→ **減輕**（改 pointer 一次即可，不用同步多處）
  - 模式 5（多語言 drift）→ **消失**（JSON 跨語言共用，frontmatter pointer 可選同步或用共享 ID）
  - 模式 6（孤兒指標）→ 靠 CI（Option F）
- **成本**：
  - 新建 `spore-metrics.json` schema + generator
  - `SporeFootprint.astro` 改成讀 frontmatter + JSON join
  - 既有 `dashboard-spores.json` 可合併或共用資料源
- **風險**：建構期需要 JSON 可用（Astro build 讀 public/api/）；第一次上線需要 backfill

### 2.6 Option F：CI lint（**跟 A-E 正交，可疊加**）

- **做什麼**：pre-commit 或 GitHub Actions 檢查
  - 每個 SPORE-LOG row 的 URL → 必須在某篇文章的 `sporeLinks[].url` 裡找到（Portaly 類 orphan 用白名單）
  - 每個文章的 `sporeLinks[].url` → 必須在 SPORE-LOG 有 row
  - 數字一致性（如果選擇 A/B/D 架構，需要檢查跨層數字；如果選 C/E，此項不需要）
- **解決**：模式 6（孤兒）+ 模式 1 的偵測（無法預防但會在 commit 時擋下）
- **成本**：低（一個 script + CI hook）
- **建議**：**無論選哪個架構都要加**

---

## 三、推薦方案：Option E + F

### 3.1 為什麼是 E

分層決策的核心是「**依照變動頻率分層**」：

| 資料                                     | 變動頻率                                  | 合適儲存                                   |
| ---------------------------------------- | ----------------------------------------- | ------------------------------------------ |
| Pointer（platform/date/url）             | 一次性（publish 時定下，URL edit 罕見）   | 文章 frontmatter（git-native、co-located） |
| Metrics（views/likes/…）                 | 每次 harvest（D+0/D+1/D+3/D+7/D+14/D+30） | JSON（append-friendly、跨語言共用）        |
| Narrative（切片、session 備註、Pattern） | 每次 harvest，但是**敘事性**              | SPORE-LOG.md（人類可讀、AI 可寫）          |

這樣每一層都在**它最擅長的載體**：

- frontmatter 擅長 co-located、不頻繁、跨語言獨立（每個翻譯檔各有 pointer）
- JSON 擅長高頻寫、機器讀、單一來源
- Markdown log 擅長敘事、時間線、診斷故事

### 3.2 為什麼要加 F

CI lint 是最後防線。即使 E 把失敗模式 1-5 大部分消掉，模式 6（孤兒 row / 孤兒 pointer）仍可能出現：

- 刪文章但忘了從 SPORE-LOG 拉掉 row
- 加 SPORE-LOG row 但忘了指向文章（或故意不指，像 Portaly 站方公告）

Lint 讓這些狀況**commit 時就擋下**，避免 silent drift 累積。

### 3.3 保留 SPORE-LOG 的敘事價值

這個架構**不削弱** SPORE-LOG。相反：

- SPORE-LOG 從「metrics 存檔」解放，回歸它真正擅長的——**診斷敘事**
- 像 #29 李洋 8h 快照後的曲線形狀辯論（尖峰 / S / 高原三次修正）、#30 X 平台史上最強孢子元教訓——這些段落的價值遠高於當下數字快照
- 數字 SSOT 移到 JSON 後，SPORE-LOG 可以寫得更像「研究札記 + 累積切片」，不需要擔心覆寫最新數字

---

## 四、遷移路徑（從現狀到 Option E+F）

分 5 phase，每 phase 獨立可驗證、可回滾。

### Phase 1：設計 schema（低風險、純文件）

- 定義 `public/api/spore-metrics.json` schema：
  ```json
  {
    "schema_version": 1,
    "generated_at": "ISO8601",
    "spores": {
      "https://www.threads.com/@taiwandotmd/post/DXdyoqkEdma": {
        "platform": "threads",
        "publish_date": "2026-04-23",
        "latest_snapshot": {
          "captured_at": "2026-04-23T22:00+0800",
          "session": "δ",
          "views": 1831,
          "likes": 209,
          "reposts": 24,
          "comments": 5,
          "shares": 4
        },
        "history": [
          { "captured_at": "...", "session": "...", "views": ..., ... }
        ]
      }
    }
  }
  ```
- 定義簡化後的 frontmatter schema：`sporeLinks: [{platform, date, url}]`（去掉 views/likes/…）
- 決定 canonical 工具路徑：`scripts/tools/harvest-spore.mjs` / `scripts/tools/spore-metrics-generate.mjs` / `scripts/tools/spore-lint.mjs`

### Phase 2：建 generator + SporeFootprint 讀雙源（可並行既有）

- 寫 `scripts/tools/spore-metrics-generate.mjs`：從 SPORE-LOG 解析 最新 harvest 結果，產出 `public/api/spore-metrics.json`
- 重構 `SporeFootprint.astro`：
  - 先讀 frontmatter.sporeLinks（pointer）
  - 若 frontmatter 含 views 欄（向後相容）→ 用 frontmatter 數字
  - 否則查 JSON → 用 JSON 數字
- 這個 phase 不破壞既有（張懸/李洋/認知作戰 frontmatter 還有完整數字）

### Phase 3：Backfill pointer（處理歷史債）

- 已 spawn 的背景任務（6 篇補 sporeLinks）延伸目標：寫完整 schema（含數字）作為第一步
- 等 Phase 2 上線後，再寫一次性 migration：把既有 frontmatter 的數字欄位**剝掉**，只留 pointer
- 或者維持向後相容，讓 frontmatter 的數字變 cache，JSON 為權威

### Phase 4：Harvest 工具化

- 寫 `scripts/tools/harvest-spore.mjs <URL>`：
  - Chrome MCP 呼叫（或接收手工 JSON input）
  - 寫 `spore-metrics.json`（append to history + update latest_snapshot）
  - 產出 SPORE-LOG 敘事 row 的草稿（session 填入後貼上）
- AI session 的 SPORE-HARVEST-PIPELINE Step 1.5 改成呼叫這個工具

### Phase 5：CI lint

- 寫 `scripts/tools/spore-lint.mjs`：
  - 檢查 SPORE-LOG URL 與文章 frontmatter pointer 一對一（orphan 允許白名單）
  - 檢查每個 pointer 在 JSON 有 entry（或允許 publish-day pointer 還沒 harvest）
- 加進 `.husky/pre-commit` 與 GitHub Actions

---

## 五、開放問題（需要觀察者拍板）

1. **Orphan 白名單**：Portaly 贊助公告（#37/#38）沒有對應文章 article。要規範為「frontmatter 指向 homepage」？還是在 SPORE-LOG 加 `orphan: true` 旗標？
2. **URL edit 處理**：X edit 後 v1/v2 URL 要在 metrics JSON 保留兩筆（v1 死 + v2 活）還是合併？目前 SPORE-LOG 用「切換 canonical」方式（v1 備註刪、v2 接手累積）。JSON 應該跟同樣邏輯嗎？
3. **多語言 pointer 同步**：zh-TW/en/ja/ko frontmatter 都要獨立指標，還是用共享 spore_id（例如 `s41`）統一？後者 frontmatter 只寫 `sporeIds: [s41, s42]`，靠 JSON 展開。
4. **SPORE-LOG markdown parse**：Phase 1 需要從 SPORE-LOG 產 JSON。目前 SPORE-LOG 成效追蹤表是 markdown table + 自由文字 row，**既是結構化資料也是敘事**。要先把 metrics 抽成獨立 YAML block（HEREDOC in row）還是寫 tolerant parser？
5. **Dashboard spores JSON 合流**：`public/api/dashboard-spores.json` 已存在，跟 `spore-metrics.json` 要合併還是保持分離？合併的話 schema 要支援 dashboard 的聚合欄位（topSpores / backfillWarnings）。

---

## 六、落點建議

- **今天（2026-04-23 δ）已完成**：v2.6 process rule + 認知作戰.md frontmatter 補上 sporeLinks + 6 篇債已 spawn task backfill（以舊 schema 為準）
- **短期（1-2 個 session）**：執行 Phase 1（schema 設計 finalize）+ Phase 5（lint，不依賴架構遷移，可先上）
- **中期（下一週）**：Phase 2 + Phase 3（跟 backfill 合流）
- **長期（Phase 4）**：harvest 工具化，等 Chrome MCP 穩定後再做；或延後到 Threads Graph API 可用再一次到位

過程中一個重要判準：**不為了純度犧牲現有的手感**。SPORE-LOG 的敘事價值（session 內容、跨筆觀察、元教訓）是 Taiwan.md 的**隱性智慧**，任何架構變動都不能把 log 變成冷冰冰的機器 dump。E 架構的核心美感就是「把該分離的分離，但把該留敘事的地方守住」。

---

_v1.0 | 2026-04-23 δ session 後半_
_觸發事件：#41/#42 認知作戰 harvest 後觀察者指正「預設要像是安溥那篇，會出現在文章的下方 section，然後更新數據也要去更新文章裡提到的孢子」_
_核心主張：process rule（v2.6 雙寫）是必要但不充分，長期要靠分層 SSOT（Option E）+ CI lint（Option F）把紀律沉澱成結構_
_關聯：docs/factory/SPORE-PIPELINE.md §Step 4 step 6 + §Step 4.5e；docs/factory/SPORE-HARVEST-PIPELINE.md §Step 1.5；src/components/SporeFootprint.astro interface SporeLink_
