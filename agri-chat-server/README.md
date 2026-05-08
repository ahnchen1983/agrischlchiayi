# Agri-Chat 服務器

嘉義農業知識助手 — 基於 OpenRouter + Gemini 的知識庫 RAG 系統。

## 📋 前置需求

- Node.js >= 18.0.0
- OpenRouter API key (免費註冊: https://openrouter.io)

## 🚀 本地運行

### 1. 建立知識庫索引

```bash
npm run build-index
```

這會掃描 repo 根目錄的 `knowledge/` 資料夾，建立搜索索引。

### 2. 設定環境變數

```bash
cp .env.example .env
# 編輯 .env，填入你的 OpenRouter API key
```

### 3. 安裝並啟動

```bash
npm install
npm start
```

服務器會運行在 `http://localhost:3000`

### 4. 測試 API

**搜索測試：**
```bash
curl "http://localhost:3000/api/search?q=虱目魚養殖"
```

**聊天測試：**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "如何養殖虱目魚？"}'
```

## 📁 結構

```
agri-chat-server/
├── server.js                 # Express 服務器
├── search.js                 # 知識庫搜索模組
├── llm.js                    # OpenRouter API 調用
├── build-knowledge-index.js  # 索引生成工具
├── package.json
├── .env.example
├── public/
│   └── chat-widget.js        # Web Component
└── knowledge-index.json      # 預生成的索引 (執行 build-index 生成)
```

## 🌐 在 Astro 中嵌入

在你的 Astro 頁面或佈局中加入：

```astro
<agri-chat api-url="http://localhost:3000"></agri-chat>
<script src="http://localhost:3000/chat-widget.js"></script>
```

## 🔒 安全性

- **知識庫隔離** — LLM 只能基於 markdown 文件回答
- **API Key 保護** — OpenRouter 密鑰存在後端
- **行為限制** — 系統提示詞禁止超出範疇的請求
- **無代碼執行** — 完全無法執行程式或訪問外部資源

## 📊 API 端點

### POST /api/chat
發送訊息並獲取回答。

**請求：**
```json
{
  "message": "如何養殖虱目魚？"
}
```

**回應：**
```json
{
  "success": true,
  "answer": "虱目魚養殖...\n\n**相關文檔：**\n- [文檔標題](url)",
  "sources_found": 3,
  "timestamp": "2026-05-07T..."
}
```

### GET /api/search
直接搜索知識庫（用於調試）。

**查詢：**
```
GET /api/search?q=虱目魚養殖
```

### GET /health
健康檢查。

### GET /chat-widget.js
獲取 Web Component。

## 🚀 部署到 Render

見 [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)

## 💾 更新知識庫

```bash
# 當知識庫內容改變時，重新生成索引
npm run build-index

# 提交更新
git add knowledge-index.json
git commit -m "chore: regenerate knowledge index"
git push
```

## 🐛 故障排查

### OpenRouter API key 無效
```bash
# 檢查 .env 是否正確設定
echo $OPENROUTER_API_KEY
```

### 知識庫索引失敗
```bash
# 確認 knowledge/ 目錄在 repo 根目錄
ls -la ../knowledge
```

### Web Component 無法載入
- 檢查 CORS 是否已啟用（已在 server.js 中）
- 檢查 API URL 是否正確
- 查看瀏覽器控制臺的錯誤訊息

## 📈 成本估算

**Gemini 2.0 Flash 定價：**
- 輸入：$0.075 / 100K tokens
- 輸出：$0.30 / 100M tokens

**典型成本：**
- 單次提問：~$0.002 USD
- 每月 1000 次：~$2 USD

## 📞 支援

- OpenRouter 文件：https://openrouter.io/docs
- Render 文件：https://render.com/docs
