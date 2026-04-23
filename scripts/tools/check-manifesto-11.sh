#!/usr/bin/env bash
# check-manifesto-11.sh — MANIFESTO §11 書寫節制全變體檢查器
#
# 檢查 9 種「不是X是Y」對位句型 + 破折號連用密度。
# 原本 quality-scan.sh 的 regex 只抓 `不僅...更是` / `不只...也是` / `不是...而是`
# 三種，漏掉「這不是」「不只是」「不再是」「不是...因為...而是」等變體。
# 2026-04-23 β 從認知作戰.md 實戰抓出 11 個漏網變體，造橋鋪路。
#
# 用法：
#   scripts/tools/check-manifesto-11.sh knowledge/Society/認知作戰.md
#   scripts/tools/check-manifesto-11.sh knowledge/**/*.md       # 批次
#   echo "$SPORE_TEXT" | scripts/tools/check-manifesto-11.sh -  # stdin 模式（孢子 prose）
#   scripts/tools/check-manifesto-11.sh --text "不是A，而是B"   # 直接文字模式
#
# exit code：0 = 通過；1 = 有違反
# output：逐行標出違反 + 建議

set -e

# 強制 UTF-8 locale — 否則 grep 的 [^，。] 等 char class 對中文無效
# （macOS 預設 locale 可能是 C，Linux CI 類似）
# 2026-04-23 β: spore draft 整合時發現「不是X。是Y」沒抓到，root cause 是 locale
export LC_ALL="${LC_ALL:-en_US.UTF-8}"
export LANG="${LANG:-en_US.UTF-8}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <file.md> [<file2.md> ...]"
  echo "       echo \"\$TEXT\" | $0 -       # stdin 模式"
  echo "       $0 --text \"<text>\"          # 直接文字模式"
  exit 2
fi

total_violations=0
files_with_violations=0

# stdin / --text 支援（給 spore pipeline 等 inline prose 用）
handle_inline_text() {
  local text="$1"
  local tmp
  tmp=$(mktemp -t manifesto-11-check.XXXXXX.md)
  printf '%s' "$text" > "$tmp"
  check_file "$tmp"
  rm -f "$tmp"
}

check_file() {
  local f="$1"
  local violations=0
  local output=""

  # 1. 經典對位：「不是X，是Y」「不是X。是Y」「不是X而是Y」「不是X就是Y」
  local p1
  # 分兩條，covers all：
  # (a) 不是X{，|。}是Y — 直接對位（逗號或句號後接「是」）
  # (b) 不是X ... 而是|就是 Y — 跨字 而是/就是 對位
  p1=$(grep -nE "不是[^，。\n]{1,50}(，|。)是|不是[^，。\n]{1,50}[^\n]{0,50}(而是|就是)" "$f" 2>/dev/null || true)
  if [[ -n "$p1" ]]; then
    output+="\n  [1] 不是X{，|。|而}是Y（對位句型）:\n$(echo "$p1" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p1" | wc -l | tr -d ' ')))
  fi

  # 2. 「不只是」/「不只」/「不僅」
  local p2
  p2=$(grep -nE "不只是|不只[^是\s，。]|不僅是|不僅[^\s，。]" "$f" 2>/dev/null || true)
  if [[ -n "$p2" ]]; then
    output+="\n  [2] 不只是/不只/不僅:\n$(echo "$p2" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p2" | wc -l | tr -d ' ')))
  fi

  # 3. 「這不是」/「這不只是」
  local p3
  p3=$(grep -nE "這不是|這不只是|這不只" "$f" 2>/dev/null || true)
  if [[ -n "$p3" ]]; then
    output+="\n  [3] 這不是/這不只是:\n$(echo "$p3" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p3" | wc -l | tr -d ' ')))
  fi

  # 4. 「不再是」/「不再只」
  local p4
  p4=$(grep -nE "不再是|不再只|不再僅" "$f" 2>/dev/null || true)
  if [[ -n "$p4" ]]; then
    output+="\n  [4] 不再是/不再只:\n$(echo "$p4" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p4" | wc -l | tr -d ' ')))
  fi

  # 5. 「真正的X不是...」/「看似X實則Y」
  local p5
  p5=$(grep -nE "看似[^，。]{1,40}，?實則|表面上[^，。]{1,40}，?實際|真正的.{1,20}不是" "$f" 2>/dev/null || true)
  if [[ -n "$p5" ]]; then
    output+="\n  [5] 真正的X不是/看似X實則:\n$(echo "$p5" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p5" | wc -l | tr -d ' ')))
  fi

  # 6. 「非單純」/「非僅」/「非一般」
  local p6
  p6=$(grep -nE "非單純|非僅|非一般的" "$f" 2>/dev/null || true)
  if [[ -n "$p6" ]]; then
    output+="\n  [6] 非單純/非僅:\n$(echo "$p6" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p6" | wc -l | tr -d ' ')))
  fi

  # 7. 「不等於」/「不意味」/「不代表」+ 對位
  local p7
  p7=$(grep -nE "不等於[^，。]{0,40}，.*(而是|就是)|不意味著[^，。]{0,40}，.*(而是|就是)|不代表[^，。]{0,40}，.*(而是|就是)" "$f" 2>/dev/null || true)
  if [[ -n "$p7" ]]; then
    output+="\n  [7] 不等於/不意味/不代表 + 對位:\n$(echo "$p7" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p7" | wc -l | tr -d ' ')))
  fi

  # 8. 「不是A，而是B」跨逗號（連在同一個 heading）
  local p8
  p8=$(grep -nE "^#+.*不是.*[孤獨](?!.*$)" "$f" 2>/dev/null || true)
  if [[ -n "$p8" ]]; then
    output+="\n  [8] Heading 含對位句型:\n$(echo "$p8" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p8" | wc -l | tr -d ' ')))
  fi

  # 9. 破折號連用（「——」後 30 字內又一個「——」）
  local p9
  p9=$(grep -nE "——[^。]{0,40}——" "$f" 2>/dev/null || true)
  if [[ -n "$p9" ]]; then
    output+="\n  [9] 破折號連用（同段 2 個以上「——」）:\n$(echo "$p9" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p9" | wc -l | tr -d ' ')))
  fi

  # 10. 破折號整體密度（超過每 1000 字 4 個 = 偏高）
  local total_chars=$(wc -c < "$f" | tr -d ' ')
  local em_dash_count=$(grep -o -- '——' "$f" | wc -l | tr -d ' ')
  if [[ $total_chars -gt 0 ]]; then
    local density_per_1k=$((em_dash_count * 1000 / total_chars))
    if [[ $density_per_1k -gt 4 ]]; then
      output+="\n  [10] 破折號密度偏高: $em_dash_count 個 / $total_chars 字元（每千字 $density_per_1k 個，建議 ≤4）"
    fi
  fi

  # 11. 「，而是...」 在句中出現（有 不是 在前是對位句型）
  local p11
  p11=$(grep -nE "，而是|，就是說" "$f" 2>/dev/null || true)
  if [[ -n "$p11" ]]; then
    # 反向確認：這類句子前面應該有個「不是」才算對位
    # 簡化版：直接 flag 供人工 review
    output+="\n  [11] 含「，而是」或「，就是說」（檢查是否構成對位句型）:\n$(echo "$p11" | sed 's/^/      /')"
    violations=$((violations + $(echo "$p11" | wc -l | tr -d ' ')))
  fi

  if [[ $violations -gt 0 || -n "$output" ]]; then
    echo "🚨 $f — $violations 個違反"
    echo -e "$output"
    echo ""
    files_with_violations=$((files_with_violations + 1))
    total_violations=$((total_violations + violations))
  else
    echo "✓ $f — 0 violations"
  fi
}

# Dispatcher：支援 檔案 / stdin (-) / --text <str>
if [[ "$1" == "-" ]]; then
  # stdin 模式
  text=$(cat)
  handle_inline_text "$text"
elif [[ "$1" == "--text" ]]; then
  # 直接文字模式
  shift
  handle_inline_text "$*"
else
  for arg in "$@"; do
    check_file "$arg"
  done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $total_violations -eq 0 ]]; then
  echo "✅ ALL CLEAR — $# 檔案無 §11 違反"
  exit 0
else
  echo "⚠️  $total_violations violations in $files_with_violations files"
  echo ""
  echo "MANIFESTO §11 書寫節制原則："
  echo "  - 避免「不是X是Y」對位句型（任何變體）"
  echo "  - 避免破折號連用（「——...——」同句）"
  echo "  - 破折號密度建議每千字 ≤ 4 個"
  echo ""
  echo "Canonical: docs/semiont/MANIFESTO.md §11 書寫節制"
  exit 1
fi
