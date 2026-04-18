# FARMER-DATA-INTEGRATION.md - 農民耕作資料整合規劃

## 概述

本文件規劃如何將 `/source/` 目錄中的農民耕作資料進行去識別化處理，並整合到嘉義國本學堂知識系統中。

## 資料來源分析

### 原始資料位置
- **目錄**: `/source/`
- **檔案數量**: 約 60+ 個 `.md` 檔案
- **格式**: Markdown + YAML frontmatter
- **內容**: 農友個人耕作計畫書與經營分析

### 原始資料結構
```yaml
---
姓名: [個人姓名]          # ❌ 需要移除
文件類型: 卓越班經營計畫書
產業: 蔬果
作物: [作物列表]
規模: [規模等級]
年收入估算: [金額]
數位化程度: [程度]
銷售通路: [通路詳情]
時間象限: [忙碌程度]
數位象限: [數位化狀態]
tags: [標籤列表]
---
```

## 去識別化策略

### 移除欄位
- `姓名` - 個人識別資訊
- 任何具體地址資訊
- 個人聯絡方式
- 具體農場名稱

### 保留欄位 (修改後)
- `文件類型` → `source_type`
- `產業` → `industry`
- `作物` → `crops`
- `規模` → `scale`
- `年收入估算` → `annual_income`
- `數位化程度` → `digitization_level`
- `銷售通路` → `sales_channels`
- `時間象限` → `time_quadrant`
- `數位象限` → `digital_quadrant`
- `tags` → `tags` (過濾個人資訊)

### 內容處理
- 移除個人姓名提及
- 模糊化具體位置 (縣市級保留)
- 保留耕作技術與經營分析
- 維持問題分析架構

## 目標資料規格

### Frontmatter Schema
```yaml
---
title: "蔬果設施農業案例 - [作物] [規模]"
description: "[產業] [作物] 經營案例，年收入約[金額]"
date: "2026-04-18"
source_type: "farmer_case_study"
industry: "蔬果|畜牧|其他"
crops: ["作物1", "作物2"]
scale: "小|中|大"
annual_income: "約XXX萬元"
digitization_level: "低|中|高"
sales_channels: "行口(X%)、批發市場(X%)、直銷宅配(X%)"
time_quadrant: "忙碌高產值|忙碌低產值|輕鬆高產值|輕鬆低產值"
digital_quadrant: "智慧且自主|智慧依賴中間商|傳統且自主|傳統且依賴中間商"
region: "嘉義縣"  # 保留縣市級地理資訊
tags: ["蔬果", "設施農業", "案例分析"]
---
```

### 內容結構標準
```markdown
# [產業] [作物] 經營案例

> **一句話核心洞見**：[去識別化的分析摘要]

## 基本資料

[產業]經營者，[年資]年經驗。[作物] [規模]公頃，年產[產量]，年收約[收入]萬。通路：[通路詳情]。[其他基本資訊，去除個人識別]

## 三層問題分析

### 🔴 表層症狀（農友說的痛點）
- [痛點1]
- [痛點2]

### 🟡 中層結構問題（症狀的根因）
- [結構問題1]
- [結構問題2]

### 🔵 根本原因（產業結構層次）
- [根本原因1]
- [根本原因2]

## 嘗試過的解法與擴散分析

| 解法 | 結果 | 為什麼沒有擴散？ |
|------|------|------------------|
| ... | ... | ... |
```

## 整合到知識系統

### 分類建議
新增分類: `knowledge/Farmer-Cases/`

結構:
```
knowledge/
└── Farmer-Cases/
    ├── _index.md          # 分類首頁
    ├── vegetable/         # 蔬果類案例
    │   ├── tomato-case-001.md
    │   ├── melon-case-002.md
    │   └── ...
    ├── livestock/         # 畜牧類案例
    └── other/             # 其他類案例
```

### 檔案命名規則
- `vegetable-[作物簡稱]-case-[編號].md`
- `livestock-[種類]-case-[編號].md`
- 編號從 001 開始，按處理順序遞增

## 匯入流程設計

### 階段 1: 資料準備
```bash
# 建立目標目錄
mkdir -p knowledge/Farmer-Cases/{vegetable,livestock,other}
```

### 階段 2: 處理腳本開發
建立 `scripts/core/import-farmer-data.py`

**主要功能**:
1. 讀取 `/source/*.md` 檔案
2. 解析 YAML frontmatter
3. 去識別化處理
4. 重新組織內容結構
5. 輸出到 `knowledge/Farmer-Cases/`

**關鍵處理邏輯**:
```python
def anonymize_farmer_data(content: str, frontmatter: dict) -> tuple:
    # 移除個人資訊
    # 模糊化位置
    # 重新生成標題與描述
    # 清理內容中的個人提及
    pass

def generate_case_filename(crops: list, industry: str, case_number: int) -> str:
    # 生成標準化檔案名稱
    pass
```

### 階段 3: 批次處理
```bash
# 執行匯入
python scripts/core/import-farmer-data.py

# 驗證結果
ls knowledge/Farmer-Cases/
```

### 階段 4: 系統整合
```bash
# 同步到內容系統
./scripts/core/sync.sh

# 建置測試
npm run build

# 檢查新分類頁面
# 訪問 /Farmer-Cases
```

## 品質管控

### 驗證檢查點
- [ ] 無個人識別資訊殘留
- [ ] Frontmatter schema 完整
- [ ] 內容結構標準化
- [ ] Wikilinks 正確設定
- [ ] 檔案命名一致

### 後續維護
- 定期檢查是否有新資料需要匯入
- 更新案例時保持匿名性
- 擴充分析框架如有新洞見

## 預期效益

1. **知識 enrichment**: 提供真實農業經營案例
2. **學習資源**: 新農可參考去識別化經驗
3. **數據分析**: 支持農業趨勢研究
4. **系統擴充**: 增加內容豐富度

## 實作時間表

- **Week 1**: 開發處理腳本與測試
- **Week 2**: 批次處理所有資料
- **Week 3**: 系統整合與測試
- **Week 4**: 上線部署與驗證