# Agri-Chat API 安全指南

## 🔐 核心原則

1. **API Key 完全隔離** — 只在後端 `process.env` 中
2. **前端無敏感信息** — Web Component 只調用代理端點
3. **請求速率限制** — 防止濫用和 DDoS
4. **使用量監控** — 檢測異常費用

## 📋 環境變數管理

### 本地開發

```bash
# 1. 建立本地 .env 檔案
cp .env.example .env.local

# 2. 填入真實 API key（只在本機）
echo "OPENROUTER_API_KEY=sk_..." >> .env.local

# 3. 確保 .gitignore 有包含 .env.local
git check-ignore .env.local  # 應該輸出路徑
```

### Staging / Production

```
環境      API Key             費用限制        Rotate 頻率
-----   ---------------    -----------    ----------
dev     個人開發用          無限制          無需
staging 測試環境            $10/月 quota    每月一次
prod    正式環境            $50/月 quota    每季一次
```

## 🛡️ 安全措施已實施

### Rate Limiting
- **限制**：20 次請求/分鐘（單 IP）
- **返回**：429 Too Many Requests
- **目的**：防止濫用和成本超支

### Request Validation
- **大小限制**：1 MB (JSON payload)
- **超時**：30 秒
- **驗證**：訊息非空且為字串

### 錯誤處理
- ❌ **不洩露**：內部路徑、堆棧跟蹤、細節實現
- ✅ **只返回**：使用者可讀的錯誤訊息

### 使用量監控
- **端點**：`GET /api/stats`（需 `Authorization` header）
- **記錄**：請求數、估算 token 數、記憶體使用

## 🚨 異常檢測清單

定期檢查以下指標（每日或每週）：

```
□ 請求數異常增加？
□ 時間戳異常（半夜大量請求）？
□ Rate limit 被觸發次數異常多？
□ 單個訊息包含大量 tokens？
□ 來自單一 IP 的集中請求？
```

## 🔄 API Key Rotation 流程

### 一旦懷疑外洩

```
1. 立即停止使用舊 key
   OPENROUTER_API_KEY=sk_old → 空值或新 key

2. 從 OpenRouter Dashboard 撤銷舊 key
   Settings → API Keys → Delete

3. 生成新 key
   Settings → Generate New Key

4. 更新環境變數
   Dev:     .env.local (本機)
   Staging: Render Dashboard
   Prod:    Render Dashboard + 備份通知

5. 驗證新 key 生效
   curl -X POST http://localhost:3000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "測試"}'

6. 監控 24 小時，確認舊 key 無動作
```

## 🔍 Pre-commit 檢查

自動檢測敏感信息，防止意外 commit：

```bash
# 安裝 pre-commit hooks
pip install pre-commit
pre-commit install

# 手動執行全倉庫掃描
pre-commit run --all-files

# 掃描敏感信息
gitleaks detect --source .

# 掃描私密金鑰
detect-secrets scan --all-files
```

## 📊 成本監控

### OpenRouter 計費模型

```
Gemini 2.0 Flash:
- 輸入：  $0.075 / 100K tokens
- 輸出：  $0.30 / 100M tokens

典型對話成本：~$0.002 USD

月度預算：
- 1,000 對話/月  → ~$2
- 10,000 對話/月 → ~$20
- 50,000 對話/月 → ~$100
```

### 成本異常警示

```
異常情況                    可能原因              立即行動
-----------              --------            ------
費用 > 預期 2 倍          API key 外洩           立即 rotate
請求數劇增               自動化濫用             檢查 rate limit
單次回答超過 2K tokens   輸入過長或迴圈         檢查知識庫搜索
```

## 🔐 安全檢查清單（部署前）

- [ ] `.env` 和 `.env.local` 已加入 `.gitignore`
- [ ] 無 API key 在 `git log` 歷史中
- [ ] 前端 JS 中無 API key 痕跡
- [ ] `server.js` 使用 `process.env.OPENROUTER_API_KEY`
- [ ] Rate limiting 已啟用
- [ ] Request 大小限制已設定
- [ ] 錯誤消息不洩露內部細節
- [ ] `/api/stats` 需要認證
- [ ] Pre-commit hooks 已安裝
- [ ] `gitleaks` 掃描通過

## 📞 應急聯絡

**懷疑 API key 外洩時：**

1. 停止服務（可選）
2. 撤銷舊 key
3. 生成新 key
4. 更新所有環境變數
5. 檢查 OpenRouter 使用日誌
6. 通知相關人員

---

**最後更新**: 2026-05-07
