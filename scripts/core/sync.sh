#!/bin/bash
# agrischlchiayi 統一同步腳本
# 功能：knowledge/ SSOT → src/content/ + frontmatter 修復
# 用法：bash scripts/sync.sh

set -e  # 遇到錯誤立即退出

echo "🚀 agrischlchiayi 統一同步開始..."
echo "================================================="

# 1. 從 knowledge/ SSOT 同步到 src/content/ 投影層
echo ""
echo "🔄 步驟 1/2: 同步 knowledge/ → src/content/..."

# 冪等同步：先清空再重建，確保 src/content/ 是 knowledge/ 的純淨投影
# 這防止改名/刪除的檔案殘留為「幽靈細胞」
echo "🧹 清空 src/content/ 投影層（冪等重建）..."
if [ -d "src/content" ]; then
  rm -rf src/content/zh-TW
fi

# 建立目錄結構
echo "📁 建立目錄結構..."
mkdir -p src/content/zh-TW/{agri-basics,agri-advanced,farm-management,crop-production,facility-farming,smart-farming,agri-marketing,grants-planning,field-visits,livestock-health,crop-index,tech-index,learning-paths}

# 統計初始檔案數
KNOWLEDGE_COUNT=$(find knowledge/ -name "*.md" | wc -l)

echo "📊 knowledge/ 總檔案數: $KNOWLEDGE_COUNT"

# 同步根目錄檔案
echo "📄 同步根目錄檔案..."
if [ -f "knowledge/_Home.md" ]; then
    cp "knowledge/_Home.md" "src/content/zh-TW/_Home.md"
    echo "  ✅ _Home.md"
fi

# 定義資料夾名稱到 slug 的映射
folder_to_slug() {
  case "$1" in
    Agri-Basics)      echo "agri-basics" ;;
    Agri-Advanced)    echo "agri-advanced" ;;
    Farm-Management)  echo "farm-management" ;;
    Crop-Production)  echo "crop-production" ;;
    Facility-Farming) echo "facility-farming" ;;
    Smart-Farming)    echo "smart-farming" ;;
    Agri-Marketing)   echo "agri-marketing" ;;
    Grants-Planning)  echo "grants-planning" ;;
    Field-Visits)     echo "field-visits" ;;
    Livestock-Health) echo "livestock-health" ;;
    Crop-Index)       echo "crop-index" ;;
    Tech-Index)       echo "tech-index" ;;
    Learning-Paths)   echo "learning-paths" ;;
  esac
}

# 同步中文分類目錄
echo "🇹🇼 同步中文分類目錄..."
SYNCED_COUNT=0
for category in Agri-Basics Agri-Advanced Farm-Management Crop-Production Facility-Farming Smart-Farming Agri-Marketing Grants-Planning Field-Visits Livestock-Health Crop-Index Tech-Index Learning-Paths; do
  if [ -d "knowledge/$category" ]; then
    slug=$(folder_to_slug "$category")
    for file in knowledge/$category/*.md; do
      if [ -f "$file" ]; then
        filename=$(basename "$file")
        target_file="src/content/zh-TW/$slug/$filename"

        # 總是覆蓋以保持同步（SSOT 為準）
        cp "$file" "$target_file"
        echo "  ✅ $category/$filename"
        ((SYNCED_COUNT++))
      fi
    done
  fi
done

# 統計中間結果
CONTENT_AFTER_SYNC=$(find src/content/ -name "*.md" | wc -l)

echo ""
echo "🎉 步驟 1 完成！檔案同步完成"
echo "📊 同步後 src/content/ 檔案數: $CONTENT_AFTER_SYNC"

# 2. 修復 frontmatter
echo ""
echo "🔧 步驟 2/2: 修復 frontmatter..."

# 使用 Python 腳本修復 frontmatter
if [ -f "scripts/utils/fix-all-frontmatter.py" ]; then
    echo "🐍 執行 frontmatter 修復..."
    python3 scripts/utils/fix-all-frontmatter.py
    echo "  ✅ frontmatter 修復完成"
else
    echo "  ⚠️  找不到 fix-all-frontmatter.py，跳過 frontmatter 修復"
fi

# 最終統計
CONTENT_FINAL=$(find src/content/ -name "*.md" | wc -l)

echo ""
echo "🎊 agrischlchiayi 統一同步完成！"
echo "================================================="
echo "📊 knowledge/ 來源檔案: $KNOWLEDGE_COUNT"
echo "📊 最終 src/content/ 檔案數: $CONTENT_FINAL"
echo "🔄 處理檔案數: $SYNCED_COUNT"
echo ""
echo "✨ knowledge/ SSOT → src/content/ 投影層完整同步完成"
echo "🔧 frontmatter 格式已統一修復"

# 3. 圖片健康檢查
echo ""
echo "🖼️ 步驟 3: 圖片健康檢查..."
node scripts/utils/check-images.mjs || echo "  ⚠️  有缺失圖片，請執行 npm run check-images 查看細節"

echo ""
echo "▶️  下一步：執行 npm run build 建構網站"
