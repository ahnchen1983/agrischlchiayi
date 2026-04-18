# 現有文件狀態盤點

## ✅ 已有的文件

| 類別 | 檔案 | 狀態 |
|---|---|---|
| **系統設計文件 (SDD)** | `SDD - agrischlchiayi.md 系統設計文件.md` | 有，但只有 124 行，是高階摘要版 |
| **專案總覽** | `README.md` (96 行) | 基本的 fork 說明 |
| **貢獻指南** | `CONTRIBUTING.md` (86 行) | 從 taiwan-md 繼承的 |
| **Pipeline 說明** | `docs/pipelines/` (9 份) | 從 taiwan-md 繼承 (branch / contributors / daily-report / dashboard / evolve / maintainer / stats / translation) |
| **設計文件** | `docs/design/CITATION-SYSTEM.md` | 引用系統設計 |
| **其他** | `docs/editorial/`, `docs/factory/`, `docs/taxonomy/`, `docs/semiont/` 等 | 從 taiwan-md 繼承 |

## ❌ **還沒有**的東西

1. **網站功能地圖 (Site Feature Map)** — 目前沒有一份文件列出「這個網站總共有哪些頁面、每頁功能、路由表」
2. **各功能說明文件** — 例如 Graph 頁如何運作、搜尋索引怎麼建、wikilinks 怎麼解析、i18n 機制、BASE_URL 規範等都散落在程式碼裡
3. **學習檔案 / Onboarding 文件** — 給新開發者讀的「從 0 上手本專案」的手冊
4. **完整 SDD** — 現有的 SDD 只寫了「是什麼」，沒寫：
   - 資料流詳細圖（knowledge → content → pages → api 的完整路徑）
   - 各 component / template 的職責與 API
   - 建置流程 (prebuild → build → postbuild) 的每個腳本在做什麼
   - 部署流程與 CI/CD
   - 已知陷阱（BASE_URL、husky PATH、D3 graph 等 — 目前只存在 memory 裡）
5. **開發手冊** — 常見任務怎麼做：新增文章、新增類別、改佈景、debug graph、本地預覽

## 建議的新文件結構

```
docs/
├── SITE-MAP.md              # 網站功能地圖 + 路由表
├── ARCHITECTURE.md          # 完整 SDD (擴充現有的)
├── DEVELOPER-GUIDE.md       # 開發手冊（常見任務）
├── ONBOARDING.md            # 新人 0→1 學習檔案
└── design/
    ├── CITATION-SYSTEM.md   # (已有)
    ├── GRAPH-SYSTEM.md      # Graph 頁與 D3 邏輯
    ├── BASE-URL-CONVENTION.md  # 路由規範
    ├── CONTENT-PIPELINE.md  # knowledge → site 流程
    └── I18N-SYSTEM.md       # 多語系機制
```

## 建議的建置優先順序

1. **SITE-MAP.md** — 最快有感，也最基礎
2. **ARCHITECTURE.md** — 把散落的知識收斂
3. **DEVELOPER-GUIDE.md** — 給你自己未來用
