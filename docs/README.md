# 📚 docs/ — 文件索引

> 本資料夾收錄專案的架構、開發、與內容管線文件。
> 對外的專案入口請見 [../README.md](../README.md)。

## 文件地圖

```
agrischlchiayi/
├── README.md                    # 對外專案入口
├── CONTRIBUTING.md              # 投稿指南
├── DEIDENTIFICATION-POLICY.md   # 去識別化政策（含檢查清單）
└── docs/
    ├── README.md                # ← 你正在讀這份
    ├── ARCHITECTURE.md          # 系統設計文件（SDD）
    ├── DEVELOPER-GUIDE.md       # 開發手冊與常見任務
    ├── CATEGORY-MAPPING.md      # 13 大分類定義與內容缺口
    ├── FARMER-DATA-PIPELINE.md  # 農友資料整合架構
    ├── FARMER-DATA-WORKFLOW.md  # 農友資料處理流程
    └── reports/                 # 自動化分析報告
```

## 依角色推薦的閱讀順序

### 🌱 內容貢獻者

1. [../README.md](../README.md) — 專案總覽
2. [../CONTRIBUTING.md](../CONTRIBUTING.md) — 投稿規範
3. [DEVELOPER-GUIDE.md §1-§4.1](DEVELOPER-GUIDE.md) — 環境設定與新增文章
4. [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) — 該寫什麼、放哪裡

若涉及農友資料：
5. [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — **必讀**
6. [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) — 處理流程

### 🛠 功能開發者

1. [../README.md](../README.md) — 專案總覽
2. [ARCHITECTURE.md](ARCHITECTURE.md) — 系統架構（資料流、目錄、路由、建置、陷阱）
3. [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md) — 任務級操作手冊

### 📊 想了解農友資料管線

1. [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) — 為什麼 / 怎麼做（架構面）
2. [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) — 6 步操作流程
3. [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) — 去識別化規範

## 文件職責對照

| 文件 | 回答什麼問題 |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 系統怎麼長的？資料怎麼流？什麼決策為什麼？ |
| [DEVELOPER-GUIDE.md](DEVELOPER-GUIDE.md) | 怎麼跑專案？怎麼新增文章 / 元件 / API？出錯怎麼辦？ |
| [CATEGORY-MAPPING.md](CATEGORY-MAPPING.md) | 13 大分類各代表什麼？該寫什麼？目前缺什麼？ |
| [FARMER-DATA-PIPELINE.md](FARMER-DATA-PIPELINE.md) | 農友原始資料如何系統化轉成知識文章？ |
| [FARMER-DATA-WORKFLOW.md](FARMER-DATA-WORKFLOW.md) | 拿到一份農友資料，下一步該做什麼？ |
| [../DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) | 什麼資料能 / 不能寫？提交前要檢查什麼？ |

## 維護原則

- 一個主題一份文件，不重複
- 每份文件目標 ≤ 500 行，便於 session 載入
- 每份文件開頭聲明適用範圍與相關文件
- 路徑與指令必須與實際 codebase 一致（不寫 aspirational 內容）

## reports/ 子資料夾

存放自動產出的分析報告（GA4、SEO、UX 審計等）。內容由 `scripts/` 中的工具腳本生成，僅供參考、不影響系統行為。
