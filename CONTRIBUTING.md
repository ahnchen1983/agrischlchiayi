# 貢獻指南 Contributing Guide

感謝你有興趣為嘉義國本學堂貢獻內容！本指南說明如何投稿文章、修正內容、以及提交 Pull Request。

## 快速開始

1. Fork 本 repo
2. 在 `knowledge/` 對應類別資料夾新增 `.md` 文章
3. 確保 frontmatter 格式正確
4. 提交 Pull Request

## 文章放置位置

所有文章放在 `knowledge/` 目錄下，依類別分資料夾：

| 資料夾              | 類別         |
| ------------------- | ------------ |
| `Agri-Basics/`      | 農業基礎入門 |
| `Agri-Advanced/`    | 農業進階實務 |
| `Farm-Management/`  | 農場經營管理 |
| `Crop-Production/`  | 作物生產技術 |
| `Facility-Farming/` | 設施農業     |
| `Smart-Farming/`    | 智慧農業     |
| `Agri-Marketing/`   | 農產品銷售   |
| `Grants-Planning/`  | 計畫撰寫補助 |
| `Field-Visits/`     | 場域交流觀摩 |
| `Livestock-Health/` | 畜牧健康     |

## Frontmatter 模板

每篇文章開頭必須包含以下 YAML frontmatter：

```yaml
---
title: '文章標題'
description: '一句話摘要（50 字以內）'
date: 2026-04-04
tags: [國本學堂, 相關標籤]
subcategory: '子分類名稱'
level: '初階' # 初階 / 進階 / 卓越
crop: ['水稻', '番茄'] # 相關作物（選填）
tech: ['土壤檢測'] # 相關技術（選填）
source: '資料來源'
featured: false
status: 'published' # draft / published / archived
---
```

### 選填欄位

- `instructor`: 講師姓名
- `courseDate`: 課程日期（YYYY-MM-DD）
- `accupassUrl`: Accupass 活動連結
- `year`: 年份

## Wikilinks

文章內可使用 `[[文章標題]]` 語法建立跨文章連結：

```markdown
相關主題請參考 [[土壤基礎知識]] 和 [[水資源管理入門]]。
```

## PR 流程

1. 確保文章通過 frontmatter 驗證：`npm run test`
2. 確保網站可正常建置：`npm run build`
3. 提交 PR 時簡述文章內容與分類理由
4. 維護者會進行內容審核

## 內容準則

- 以嘉義地區農業實務為主軸
- 內容應具備實用性，避免過度理論化
- 引用資料請標明來源
- 使用繁體中文，專有名詞保留原文

## 🚨 涉及農友個人資料時

若文章內容引用任何農友個人資料、案例或計畫書，**提交前必讀** [`DEIDENTIFICATION-POLICY.md`](DEIDENTIFICATION-POLICY.md)。簡要原則：

- 移除姓名、聯絡方式、家族成員、具體地址
- 保留作物、規模、成本結構、銷售比例、技術方案
- 文章須混合 ≥ 2 位農友的特徵以避免反向工程識別
- commit message 不可含農友姓名或敏感檔名

操作流程詳見 [`docs/FARMER-DATA-WORKFLOW.md`](docs/FARMER-DATA-WORKFLOW.md)。

## 問題回報

- 內容錯誤：使用 Issue Template「內容修正」
- 新文章提案：使用 Issue Template「文章提案」
- 技術問題：使用 Issue Template「Bug Report」

---

本專案基於 [taiwan-md](https://github.com/frank890417/taiwan-md) 架構開發。
