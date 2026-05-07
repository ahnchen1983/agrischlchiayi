/**
 * 知識庫搜索模組
 * 基於全文搜索 + 相關性排序
 */

function tokenize(text) {
  // 中文字符: 一-鿿
  // 英文單詞: [a-z0-9]+
  const chineseRegex = /[一-鿿]/g;
  const englishRegex = /[a-z0-9]+/gi;

  const tokens = new Set();

  // 提取中文字符
  const chineseChars = text.match(chineseRegex) || [];
  chineseChars.forEach(char => tokens.add(char));

  // 提取英文單詞
  const englishWords = text.match(englishRegex) || [];
  englishWords.forEach(word => {
    if (word.length > 1) {
      tokens.add(word.toLowerCase());
    }
  });

  return Array.from(tokens);
}

// BM25 相關性排序 (簡化版)
function calculateRelevance(query, doc) {
  const queryTokens = tokenize(query);
  const docTokens = new Set(tokenize(doc.title + ' ' + doc.description + ' ' + doc.content.slice(0, 1000)));

  let score = 0;

  queryTokens.forEach(token => {
    if (docTokens.has(token)) {
      // 標題匹配加倍
      if (tokenize(doc.title).includes(token)) score += 3;
      // 描述匹配加分
      else if (tokenize(doc.description).includes(token)) score += 2;
      // 內容匹配基礎分
      else score += 1;
    }
  });

  return score;
}

class KnowledgeBaseSearch {
  constructor(indexData) {
    this.documents = indexData.documents;
    this.invertedIndex = indexData.invertedIndex;
  }

  /**
   * 搜索知識庫
   * @param {string} query - 搜索查詢
   * @param {number} topK - 返回前 K 個結果 (default: 5)
   * @returns {Array} 相關文檔排序列表
   */
  search(query, topK = 5) {
    if (!query || query.trim().length === 0) {
      return [];
    }

    const queryTokens = tokenize(query);
    const relevantDocIndices = new Set();

    // 從反向索引獲取相關文檔
    queryTokens.forEach(token => {
      if (this.invertedIndex[token]) {
        this.invertedIndex[token].forEach(idx => relevantDocIndices.add(idx));
      }
    });

    // 如果搜索不到，返回空
    if (relevantDocIndices.size === 0) {
      return [];
    }

    // 計算相關性分數並排序
    const results = Array.from(relevantDocIndices)
      .map(idx => {
        const doc = this.documents[idx];
        return {
          ...doc,
          score: calculateRelevance(query, doc)
        };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);

    return results;
  }

  /**
   * 獲取相關文檔的上下文
   * 用於送給 LLM 作為背景資訊
   */
  getContext(query, topK = 3) {
    const results = this.search(query, topK);

    if (results.length === 0) {
      return null;
    }

    return {
      query,
      documents: results.map(doc => ({
        title: doc.title,
        url: doc.url,
        content: doc.content.slice(0, 2000), // 限制長度避免 token 超出
        score: doc.score
      }))
    };
  }
}

module.exports = KnowledgeBaseSearch;
