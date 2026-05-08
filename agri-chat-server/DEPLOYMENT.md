# 部署到 Render

完整的部署步驟指南。

## 步驟 1：準備 GitHub 倉庫

你的 repo 結構應該是：

```
agrischlchiayi/
├── knowledge/              # 現有知識庫
├── src/
├── agri-chat-server/       # ← 本目錄
│   ├── server.js
│   ├── search.js
│   ├── llm.js
│   ├── build-knowledge-index.js
│   ├── package.json
│   ├── .env.example
│   ├── public/
│   │   └── chat-widget.js
│   └── knowledge-index.json
└── ...
```

## 步驟 2：預生成知識庫索引

在本目錄執行：

```bash
npm run build-index
```

這會建立 `knowledge-index.json` 檔案。提交到 Git：

```bash
git add agri-chat-server/knowledge-index.json
git commit -m "chore: pregenerate knowledge base index"
git push
```

## 步驟 3：在 Render 上建立服務

1. 登入 https://render.com
2. 點擊 "New +" → "Web Service"
3. 連接你的 GitHub repo
4. 設定如下：

```
Name: agri-chat-server
Environment: Node
Root Directory: agri-chat-server
Build Command: npm install
Start Command: npm start
Instance Type: Free (足夠了)
```

## 步驟 4：設定環境變數

在 Render Dashboard 中：

1. 進入剛建立的服務設定
2. 在 "Environment" 部分新增：

```
OPENROUTER_API_KEY=sk_...  # 你的 OpenRouter API key
NODE_ENV=production
```

## 步驟 5：部署

點擊 "Deploy"。部署通常需要 2-3 分鐘。

部署完成後，你的服務 URL：
```
https://agri-chat-server.onrender.com
```

## 步驟 6：在 Astro 嵌入

在你的 Astro 佈局中（如 `src/layouts/Base.astro`）：

```astro
---
// src/layouts/Base.astro
---

<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <!-- 其他 head 標籤 -->
  </head>
  <body>
    <!-- 你的內容 -->

    <!-- 農業聊天助手 -->
    <agri-chat api-url="https://agri-chat-server.onrender.com"></agri-chat>
    <script src="https://agri-chat-server.onrender.com/chat-widget.js"></script>
  </body>
</html>
```

## 驗證部署

```bash
# 檢查服務健康狀態
curl https://agri-chat-server.onrender.com/health

# 測試搜索
curl "https://agri-chat-server.onrender.com/api/search?q=虱目魚"

# 測試聊天
curl -X POST https://agri-chat-server.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "農業是什麼？"}'
```

## 冷啟動延遲

Render 免費方案會在 15 分鐘無活動後休眠。第一次請求會有 ~50 秒的冷啟動延遲。

**升級選項：** 如果要避免冷啟動，升級到 Starter+ ($7/月)。

## 更新知識庫

當知識庫內容變化時：

```bash
# 1. 本地重新生成索引
npm run build-index

# 2. 提交更新
git add agri-chat-server/knowledge-index.json
git commit -m "chore: update knowledge base index"
git push

# 3. Render 會自動重新部署
```

## 故障排查

### 部署失敗

查看 Render Logs 中的錯誤訊息：
```
dashboard → service → Logs
```

常見問題：
- `knowledge-index.json` 未找到 → 執行 `npm run build-index`
- 依賴安裝失敗 → 檢查 `package.json` 語法

### API 返回錯誤 401

OpenRouter API key 無效或過期。在 Render Dashboard 更新環境變數。

### Web Component 無法載入

檢查瀏覽器控制臺的 CORS 錯誤。CORS 已在 server.js 中啟用，應該不會有問題。

## 監控和日誌

在 Render Dashboard 查看：
- **Logs** — 即時日誌輸出
- **Metrics** — CPU、記憶體、請求數
- **Events** — 部署歷史和狀態變更

## 成本

Render 免費方案：
- ✅ 無限制請求
- ⏰ 15 分鐘無活動後休眠（冷啟動延遲）
- 💰 完全免費

## 下一步

1. ✅ 本地測試成功
2. ✅ 部署到 Render
3. ✅ 在 Astro 中嵌入
4. 監控使用和成本
5. 根據反饋調整提示詞或搜索策略
