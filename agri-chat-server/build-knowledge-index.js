#!/usr/bin/env node

/**
 * 從 repo 的 knowledge/ 目錄讀取所有 markdown 文件，
 * 建立可搜索的知識庫索引
 */

const fs = require('fs');
const path = require('path');

const CATEGORY_ROUTES = {
  'Agri-Basics': 'agri-basics',
  'Agri-Advanced': 'agri-advanced',
  'Farm-Management': 'farm-management',
  'Crop-Production': 'crop-production',
  'Facility-Farming': 'facility-farming',
  'Smart-Farming': 'smart-farming',
  'Agri-Marketing': 'agri-marketing',
  'Grants-Planning': 'grants-planning',
  'Field-Visits': 'field-visits',
  'Livestock-Health': 'livestock-health',
};

const SITE_BASE_PATH = (
  process.env.SITE_BASE_PATH || '/agrischlchiayi'
).replace(/\/+$/, '');

function buildPublicUrl(relativePath) {
  const parts = relativePath.split('/');
  const folder = parts[0];
  const slug = parts.slice(1).join('/').replace(/\.md$/, '');
  const route = CATEGORY_ROUTES[folder];

  if (!route || !slug || slug.startsWith('_')) {
    return null;
  }

  return `${SITE_BASE_PATH}/${route}/${slug}`;
}

// 簡單的全文搜索 tokenizer - 支持中文
function tokenize(text) {
  // 中文字符: 一-鿿
  // 英文單詞: [a-z0-9]+
  const chineseRegex = /[一-鿿]/g;
  const englishRegex = /[a-z0-9]+/gi;

  const tokens = new Set();

  // 提取中文字符
  const chineseChars = text.match(chineseRegex) || [];
  chineseChars.forEach((char) => tokens.add(char));

  // 提取英文單詞
  const englishWords = text.match(englishRegex) || [];
  englishWords.forEach((word) => {
    if (word.length > 1) {
      tokens.add(word.toLowerCase());
    }
  });

  return Array.from(tokens);
}

// 建立反向索引 (token -> [doc indices])
function buildInvertedIndex(documents) {
  const invertedIndex = {};

  documents.forEach((doc, idx) => {
    const tokens = new Set([
      ...tokenize(doc.title),
      ...tokenize(doc.description),
      ...tokenize(doc.content.slice(0, 2000)), // 只索引前 2000 字
      ...(doc.tags || []),
    ]);

    tokens.forEach((token) => {
      if (!invertedIndex[token]) {
        invertedIndex[token] = [];
      }
      if (!invertedIndex[token].includes(idx)) {
        invertedIndex[token].push(idx);
      }
    });
  });

  return invertedIndex;
}

// 讀取 markdown 文件並解析 frontmatter
function parseMarkdownFile(filePath, knowledgeRoot) {
  const content = fs.readFileSync(filePath, 'utf-8');

  // 簡單的 YAML frontmatter 解析
  const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return null;
  }

  const [, frontmatterStr, mdContent] = match;
  const frontmatter = {};

  frontmatterStr.split('\n').forEach((line) => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      const value = valueParts
        .join(':')
        .trim()
        .replace(/^['"]|['"]$/g, '');
      frontmatter[key.trim()] = value;
    }
  });

  const relativePath = path
    .relative(knowledgeRoot, filePath)
    .replace(/\\/g, '/');

  return {
    title: frontmatter.title || path.basename(filePath),
    description: frontmatter.description || '',
    tags: frontmatter.tags
      ? frontmatter.tags.split(',').map((t) => t.trim())
      : [],
    content: mdContent,
    filePath: relativePath,
    url: buildPublicUrl(relativePath),
  };
}

// 遞迴掃描知識庫目錄
function scanKnowledgeDirectory(dirPath) {
  const documents = [];

  function walkDir(dir) {
    const files = fs.readdirSync(dir);

    files.forEach((file) => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        walkDir(filePath);
      } else if (file.endsWith('.md')) {
        const doc = parseMarkdownFile(filePath, dirPath);
        if (doc) {
          documents.push(doc);
        }
      }
    });
  }

  walkDir(dirPath);
  return documents;
}

// 主程式
function main() {
  const knowledgePath = path.join(process.cwd(), '..', 'knowledge');

  if (!fs.existsSync(knowledgePath)) {
    console.error('❌ ../knowledge 目錄不存在');
    process.exit(1);
  }

  console.log('📚 掃描知識庫...');
  const documents = scanKnowledgeDirectory(knowledgePath);

  console.log(`✅ 找到 ${documents.length} 個文件`);

  console.log('🔍 建立搜索索引...');
  const invertedIndex = buildInvertedIndex(documents);

  const index = {
    timestamp: new Date().toISOString(),
    totalDocuments: documents.length,
    documents,
    invertedIndex,
  };

  // 保存索引到 JSON
  const outputPath = path.join(process.cwd(), 'knowledge-index.json');
  fs.writeFileSync(outputPath, JSON.stringify(index, null, 2));

  console.log(`✅ 索引已保存到 ${outputPath}`);
  console.log(
    `📊 索引大小: ${(fs.statSync(outputPath).size / 1024).toFixed(2)} KB`,
  );
}

main();
