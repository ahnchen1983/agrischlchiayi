# 農友資料去識別化政策

**生效日期**: 2026-04-20  
**適用範圍**: 所有涉及農友數據的開發工作

---

## 🚨 **嚴禁事項**

### ❌ 提交信息中
- **禁止出現農友真實姓名**（如：Farmer-A、Farmer-B、Farmer-C等）
- **禁止出現農場名稱**（如：[Farm-A]、[Farm-B]等）
- **禁止出現具體的驗證報告檔名**（如：VERIFICATION-REPORT-2.1.md）
- **禁止出現電話、地址、社交媒體帳號**

**示例：**
- ❌ `docs: add VERIFICATION-REPORT-2.1 with Farmer-A and Farmer-B case studies`
- ✅ `docs: add internal farmer case study documentation`

### ❌ 版控追蹤的檔案中
- **禁止提交 source/ 資料夾**（包含農友原始資料）
- **禁止提交含農友姓名的敏感文件**
- **禁止提交未去識別化的驗證報告**
- **禁止在 EXECUTION-SCHEDULE 等文件中列舉農友真實姓名**

### ❌ 代碼註解中
- **禁止在註解中提及農友姓名或敏感細節**
- **禁止在代碼中硬編碼農友資料**

---

## ✅ **允許做法**

### 提交信息格式
使用通用、中立的描述：
```
# 允許的提交信息格式：

docs: update internal farmer data documentation
docs: add deidentified farmer case study
content: add [Crop Name] cultivation guide with anonymized case studies
fix: remove sensitive information from data sources
refactor: reorganize internal farmer reference materials
```

### 檔案放置
- **機密資料**：放在 `.gitignore` 排除的路徑（如 `source/`、`.dev/` 等）
- **敏感分析**：存放在 **Private Repository** 或 **Google Drive/OneDrive** 等雲端服務
- **去識別化資料**：使用通用代稱（F1、F2、F3 或「某農友」等）才能提交

### 去識別化要求
涉及農友數據的文件必須：
1. **移除農友真實姓名** → 用「某農友」、「農友案例 1」等代稱
2. **移除詳細地址** → 只保留「東石鄉」等地區級地名
3. **移除聯絡方式** → 完全刪除電話、郵箱、社交媒體帳號
4. **移除家庭信息** → 刪除配偶、子女名字等
5. **創建驗證報告** → 驗證報告本身也必須去識別化

---

## 📊 **.gitignore 必須包含**

```gitignore
# Farmer source data - NEVER COMMIT
source/
*.json.bak
*.md.bak

# Sensitive documentation
docs/FARMER-DATA-*
docs/VERIFICATION-REPORT-*.md

# Private configuration
.env.local
.credentials/
private/
```

---

## 🔄 **提交前檢查清單**

在執行 `git add` 前，必須檢查：

- [ ] 提交信息中**沒有農友真實姓名**
- [ ] 提交信息中**沒有敏感檔名**（VERIFICATION-REPORT、source 等）
- [ ] 提交信息中**沒有具體地址或聯絡方式**
- [ ] 代碼/文件中**所有農友資料已去識別化**
- [ ] **不會將 source/ 或敏感檔案提交到 public repo**
- [ ] 執行 `git diff --cached` 再次確認內容安全

**建議命令**：
```bash
# 查看即將提交的內容
git diff --cached

# 搜尋敏感詞彙
git diff --cached | grep -i "農友姓名\|電話\|地址\|source"

# 只有確認安全後才提交
git commit -m "safe commit message"
```

---

## 📁 **推薦的資料結構**

```
repo/
├── .gitignore                    # 包含 source/, docs/sensitive/ 等
├── source/                       # 農友原始資料（本地備份，不提交）
│   ├── Farmer-A.md
│   ├── Farmer-B.md
│   └── ... (所有原始資料)
│
├── docs/
│   ├── DEIDENTIFICATION-POLICY.md    # 本政策文件
│   ├── FARMER-DATA-EXECUTION-SCHEDULE.md  # 使用通用代稱(F1, F2, F3...)
│   └── ❌ 不包含 VERIFICATION-REPORT-*.md （敏感，不追蹤）
│
├── knowledge/
│   └── Crop-Production/
│       ├── 蝴蝶蘭種苗生產技術.md      # 完全去識別化
│       ├── 小黃瓜設施栽培技術.md      # 完全去識別化
│       └── ... (其他已去識別化的文章)
│
└── private/                      # Private repo 或外部存儲
    ├── VERIFICATION-REPORT-2.1.md (敏感分析)
    ├── farmer-original-data/      (農友原始資料)
    └── ... (其他機密資料)
```

---

## 🚨 **違反規範的後果**

如果提交中包含敏感資料，必須：

1. **立即停止工作** — 不要繼續提交
2. **執行歷史清理** — 使用 `git-filter-repo` 從 git 歷史中移除
3. **強制推送** — 覆寫 GitHub 上的歷史
4. **通知相關人員** — 確保敏感資料已被清理
5. **更新此政策** — 防止未來重複

---

## 📞 **疑問時的處理方式**

**如果不確定某些資料是否能提交，請：**

1. **預設為敏感** — 當有疑問時，假設資料是敏感的
2. **放在 .gitignore 路徑** — 將其放在 `source/` 或其他排除路徑
3. **詢問** — 在提交前確認
4. **分離存儲** — 考慮使用 Private Repo 或雲端服務

**不確定的資料 > 敏感處理 > 公開洩露**

---

## 簽核

| 項目 | 內容 |
|------|------|
| **政策制定** | Claude |
| **生效日期** | 2026-04-20 |
| **審核者** | ahnchen |
| **版本** | 1.0 |

---

**最後更新**: 2026-04-20  
**下次審查**: 2026-05-20
