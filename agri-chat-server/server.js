/**
 * Agri-Chat 服務器
 * 在 Render 上運行的後端服務
 */

require('dotenv').config({ path: '.env.local' });
require('dotenv').config();

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const KnowledgeBaseSearch = require('./search');
const OpenRouterLLM = require('./llm');

const app = express();
const PORT = process.env.PORT || 3000;

// 簡易 rate limiter (記憶體內)
const requestCounts = new Map();
function rateLimitMiddleware(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const windowMs = 60000; // 1 分鐘
  const maxRequests = 20; // 每分鐘最多 20 次

  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, []);
  }

  const timestamps = requestCounts.get(ip);
  const recentRequests = timestamps.filter((t) => now - t < windowMs);

  if (recentRequests.length >= maxRequests) {
    return res.status(429).json({
      error: '請求過於頻繁，請稍後再試',
    });
  }

  recentRequests.push(now);
  requestCounts.set(ip, recentRequests);
  next();
}

// CORS allowlist
// 從環境變數 CORS_ORIGINS 讀取，逗號分隔。
// 範例: CORS_ORIGINS=https://ahnchen1983.github.io,http://localhost:4321
//
// Fail-open 設計：未設定時印警告但仍運作（允許所有 origin），避免部署
// 時忘記設環境變數導致線上斷服務。設定後即進入嚴格 allowlist 模式。
const ALLOWED_ORIGINS = (process.env.CORS_ORIGINS || '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);

const CORS_MODE = ALLOWED_ORIGINS.length > 0 ? 'allowlist' : 'open';

if (CORS_MODE === 'open' && process.env.NODE_ENV === 'production') {
  console.warn(
    '⚠️  CORS_ORIGINS 未設定！目前允許所有 origin（不安全）。' +
      '請在 Render Dashboard 設定 CORS_ORIGINS 環境變數後重新部署。',
  );
}

app.use(
  cors({
    origin: (origin, cb) => {
      // 允許無 origin（curl、伺服器間、同源請求）
      if (!origin) return cb(null, true);
      if (CORS_MODE === 'open') return cb(null, true);
      if (ALLOWED_ORIGINS.includes(origin)) return cb(null, true);
      cb(new Error(`Origin ${origin} not allowed by CORS`));
    },
  }),
);

// 中間件
app.use(
  bodyParser.json({
    limit: '1mb', // 限制請求大小
  }),
);
app.use((req, res, next) => {
  req.setTimeout(30000); // 30 秒超時
  next();
});

// 初始化搜索和 LLM
let search;
let llm;

// 啟動時載入知識庫索引
function initializeKnowledgeBase() {
  try {
    const indexPath = path.join(__dirname, 'knowledge-index.json');

    if (!fs.existsSync(indexPath)) {
      console.error(
        '❌ knowledge-index.json 不存在，請先執行 npm run build-index',
      );
      process.exit(1);
    }

    const indexData = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
    search = new KnowledgeBaseSearch(indexData);

    console.log(`✅ 知識庫已載入 (${indexData.totalDocuments} 個文件)`);
  } catch (error) {
    console.error('❌ 載入知識庫失敗:', error.message);
    process.exit(1);
  }
}

// 初始化 LLM
function initializeLLM() {
  const apiKey = process.env.OPENROUTER_API_KEY;

  if (!apiKey) {
    console.error('❌ 未設定 OPENROUTER_API_KEY 環境變數');
    process.exit(1);
  }

  llm = new OpenRouterLLM(apiKey);
  console.log('✅ OpenRouter LLM 已初始化');
}

// 健康檢查
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    knowledge_base_ready: !!search,
    llm_ready: !!llm,
    timestamp: new Date().toISOString(),
  });
});

// 使用量監控
let apiStats = {
  totalRequests: 0,
  totalTokens: 0,
  lastReset: new Date(),
};

function cleanAnswer(text) {
  return String(text || '')
    .replace(/\*\*相關文檔：\*\*[\s\S]*$/u, '')
    .replace(/^\s*#{1,6}\s+/gm, '')
    .replace(/^\s*[-*_]{3,}\s*$/gm, '')
    .replace(/\*\*\*/g, '')
    .replace(/\*\*/g, '')
    .replace(/\*([^*\n]+)\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/\[來源:\s*[^\]]+\]/g, '')
    .replace(/[ \t]+\n/g, '\n')
    .trim();
}

function buildSummary(answer) {
  const compact = cleanAnswer(answer)
    .replace(/\n+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  if (!compact) return '已根據國本學堂知識庫整理回答。';
  if (compact.length <= 90) return compact;
  return `${compact.slice(0, 90)}...`;
}

function buildSources(context) {
  if (!context || !Array.isArray(context.documents)) return [];
  return context.documents
    .filter((doc) => doc.url)
    .map((doc) => ({
      title: doc.title,
      url: doc.url,
      score: doc.score,
    }));
}

// 主要 API：發送訊息
app.post('/api/chat', rateLimitMiddleware, async (req, res) => {
  try {
    const { message } = req.body;

    if (
      !message ||
      typeof message !== 'string' ||
      message.trim().length === 0
    ) {
      return res.status(400).json({
        error: '無效的訊息',
      });
    }

    const userMessage = message.trim();

    // 1. 搜索知識庫
    console.log(`🔍 搜索: "${userMessage}"`);
    const context = search.getContext(userMessage, 3);

    // 2. 調用 LLM 生成回答
    console.log('🤖 生成回答...');
    const answer = cleanAnswer(await llm.generateAnswer(userMessage, context));
    const summary = buildSummary(answer);
    const sources = buildSources(context);

    // 記錄使用量（簡略估算）
    apiStats.totalRequests++;
    apiStats.totalTokens += userMessage.length / 4 + answer.length / 4;

    res.json({
      success: true,
      answer,
      summary,
      sources,
      sources_found: sources.length,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ 錯誤:', error.message);

    // 不要洩露內部實現細節
    const statusCode = error.message.includes('無效') ? 400 : 500;
    const errorMessage =
      statusCode === 500 ? '處理訊息時發生錯誤，請稍後再試' : error.message;

    res.status(statusCode).json({
      error: errorMessage,
    });
  }
});

// 使用量統計 (僅限本地/內部使用)
app.get('/api/stats', (req, res) => {
  // 簡單的驗證 (生產環境應該加入更嚴格的認證)
  const authHeader = req.get('Authorization');
  if (process.env.NODE_ENV === 'production' && !authHeader) {
    return res.status(401).json({ error: '未授權' });
  }

  res.json({
    requests: apiStats.totalRequests,
    estimatedTokens: Math.round(apiStats.totalTokens),
    lastReset: apiStats.lastReset,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
  });
});

// 搜索 API (用於調試)
app.get('/api/search', (req, res) => {
  const { q } = req.query;

  if (!q) {
    return res.status(400).json({
      error: '缺少查詢參數 q',
    });
  }

  const results = search.search(q, 5);

  res.json({
    query: q,
    results: results.map((r) => ({
      title: r.title,
      url: r.url,
      score: r.score,
      preview: r.content.slice(0, 300),
    })),
  });
});

// 提供 Web Component
app.get('/chat-widget.js', (req, res) => {
  res.setHeader('Content-Type', 'text/javascript');
  res.sendFile(path.join(__dirname, 'public', 'chat-widget.js'));
});

// 啟動服務器
function start() {
  initializeKnowledgeBase();
  initializeLLM();

  app.listen(PORT, () => {
    console.log(`🚀 服務器運行在 http://localhost:${PORT}`);
    console.log(`📝 API 端點:`);
    console.log(`   POST /api/chat - 發送訊息`);
    console.log(`   GET  /api/search - 搜索知識庫`);
    console.log(`   GET  /health - 健康檢查`);
    console.log(`   GET  /chat-widget.js - 獲取 Web Component`);
  });
}

start();

module.exports = app;
