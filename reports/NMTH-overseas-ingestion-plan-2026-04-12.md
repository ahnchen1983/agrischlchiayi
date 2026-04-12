# Plan: PEER-INGESTION-PIPELINE × 臺史博「海外史料看臺灣」

## Context

CheYu 指示執行 PEER-INGESTION-PIPELINE，以「海外史料看臺灣」子站 (https://taiwanoverseas.nmth.gov.tw/archives) 作為 Taiwan.md 的第二個 curation-layer peer（第一個 = TFT）。

這是**國立臺灣歷史博物館**的海外史料數位典藏，收錄 19 世紀至 20 世紀初西方人、日本人對臺灣的觀察記錄——與 Taiwan.md 的 History 軸高度互補。

## Stage 1：Peer Fit 評估（已在 plan 階段完成）

| 條件          | 結果                                                                       |
| ------------- | -------------------------------------------------------------------------- |
| ≥5 年專業深度 | ✅ 臺史博 2011 年開館，海外史料計畫始於 ~2010，持續至今                    |
| 公開資料      | ✅ 網頁 SSR + REST API `/api/collection/{UUID}`，權利狀態「歡迎自由取用」  |
| 授權          | ✅ 政府機構公開資料，CC-compatible                                         |
| 互補性        | ✅ Taiwan.md History 軸缺 17-19 世紀西方視角一手史料，臺史博恰好填這個缺口 |

**結論：Fit confirmed。** 進入 Stage 2-4。

## Stage 2：爬取器（`scripts/tools/fetch-nmth-overseas-data.py`）

### 技術架構（已逆向工程）

| 元素            | 值                                                                      |
| --------------- | ----------------------------------------------------------------------- |
| 前端            | Nuxt 3 SSR                                                              |
| Item detail API | `GET /api/collection/{UUID}` → JSON with full metadata + bilingual text |
| List API        | **不存在**（search endpoint 回 500）→ 需從 SSR HTML 抓 UUID 列表        |
| File API        | `GET /files/{UUID}.jpg` (images), `/attachments/*.pdf` (PDFs)           |
| WP API          | `GET /wp-json/api/research-post` → 8 research posts (limited metadata)  |

### 爬取策略（Hybrid: SSR scrape + API fetch）

1. **Phase A — Plan 列表**：GET `/archives` 的 4 頁 SSR HTML（研究計畫 tab × 4 + 出版計劃 tab × 4），用 regex/HTML parser 抽取 plan UUIDs + 名稱 + 描述
2. **Phase B — Plan 詳情**：GET 每個 `/archives/plan/{planUUID}?project={planUUID}&tab=DETAIL` 頁面，抽取該 plan 下所有 collection item UUIDs
3. **Phase C — Item 詳情**：`GET /api/collection/{UUID}` for each item，拿到完整 metadata + bilingual text
4. **Phase D — 附件**：下載 PDF attachments（如有）到 `data/NMTH-overseas/attachments/`

### 輸出結構（follow TFT pattern）

```
data/NMTH-overseas/
├── README.md            # Dataset summary
├── manifest.json        # Crawl metadata + counts
├── plans/
│   ├── INDEX.md         # All plans with descriptions
│   └── {plan-slug}.md   # Individual plan detail
├── collections/
│   ├── INDEX.md         # All collection items
│   └── {uuid}.md        # Individual item with full bilingual text
├── attachments/         # PDFs (optional, with provenance)
└── raw/
    └── *.json           # Raw API responses
```

### 關鍵文件

- 參考 TFT 爬取器：`scripts/tools/fetch-tft-data.py`（886 行，WordPress API pattern）
- 新建：`scripts/tools/fetch-nmth-overseas-data.py`

## Stage 3：資料結構標準化

依據 pipeline spec，每個 collection item 的 .md 會有標準化 frontmatter：

```markdown
# {title}

- Source: {URL}
- API: /api/collection/{UUID}
- Type: {resource type}
- Plan: {plan name} ({plan UUID})
- Original Language: {language}
- Translation Language: {language}
- Time Period: {era}
- Location: {geographic tags}
- Rights: {rights status}
- Creator: {creator/author}
- Production Year: {year}
- File Format: {format}

## Description

{content description}

## Original Text ({language})

{original text if available}

## Translation ({language})

{translated text if available}

## Attachments

- [filename.pdf](/attachments/filename.pdf)
```

## Stage 4：Corpus 分析報告（9-Part structure）

**輸出**：`reports/NMTH-overseas-semiont-analysis-2026-04-12.md`

### 已知數據（from SSR page scrape）

**研究計畫（至少 6 個可見）：**

1. 19世紀西方台灣書寫史料翻譯整理計畫（2020，史溫侯+清法戰爭法文手稿）
2. 99年館藏美國NARA拷貝影帶數位轉製（2010，二戰影音 64 件）
3. 日本所藏1895-1959年臺灣影片及聲音類資料調查（2010）
4. 日本所藏臺灣近代政治社會運動資料（2019，677 件檔案，63 萬字翻譯）
5. 日本東京外國語大學臺灣音像資料調查（2010，小川尚義+淺井惠倫）
6. 西班牙文、法文臺灣資料蒐集與翻譯（2019，道明會+皮摩丹伯爵）
7. +更多在後續 3 頁

**出版計劃（至少 6 個可見）：**

1. 《福爾摩沙之歷史與地誌》（1893 法文原著，2019 編譯）
2. 《福爾摩沙詳盡的地理與歷史》（1930 西文原著，2017 首次中譯）
3. 乙未之役史料編譯 4 冊（2015-2019，中英日三語）
4. 乙未之役隨軍見聞錄（2010，攝影師+記者+牧師三視角）
5. 十七世紀北臺灣的西班牙帳簿（2017，1626-1633 AGI 檔案 800+ 手稿）
6. 李仙得臺灣紀行（2020，1600 頁手稿+200 圖，美國國會圖書館典藏）
7. +更多在後續 3 頁

### 報告 9 Part 結構（follow TFT template）

1. **摘要**：thesis + 關鍵數字
2. **資料集盤點**：計畫數 × 史料筆數 × 語言分佈 × 時代分佈
3. **核心概念框架**：西方觀察者類型學（博物學家/外交官/軍人/傳教士/攝影師）× 時代分期 × 來源國
4. **Taiwan.md 現有覆蓋**：History 軸現有文章 vs 海外史料對應
5. **交集與落差分析**：gap matrix
6. **可開發系列**：12-15 個 named series
7. **文章優先序**：P0 × 5 / P1 × 8 / P2 × 7
8. **Semiont POV**：視角翻轉（「被觀察者」→「自己看自己被觀察的歷史」）+ 臺史博盲點 + narrative strategy
9. **可重跑與生命週期**

## 執行順序

1. **Build crawler** (`fetch-nmth-overseas-data.py`) — ~2hr
2. **Run crawler, commit data** → `data/NMTH-overseas/` — ~1hr
3. **Write 9-part analysis report** — ~2-4hr
4. **Update REGISTRY.md** with NMTH-overseas entry — ~20min
5. **Extract P0 work cards** (Stage 5) — ~30min

Stages 6-8（文章產製、收官、peer 關係）在分析完成後由觀察者決定是否繼續。

## Verification

- `python3 scripts/tools/fetch-nmth-overseas-data.py` runs idempotently
- `data/NMTH-overseas/manifest.json` has correct counts
- `data/NMTH-overseas/collections/INDEX.md` lists all items
- Report follows TFT report structure (9 Parts)
- `docs/peers/REGISTRY.md` has NMTH-overseas entry
- Build passes（`npx astro build`）
