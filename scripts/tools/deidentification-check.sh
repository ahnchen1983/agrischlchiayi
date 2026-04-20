#!/usr/bin/env bash
# ============================================================
# Deidentification Pre-commit Check
# ============================================================
# Scans staged changes for sensitive farmer data before allowing commit.
#
# Detects:
#   - Real farmer names (17 known)
#   - Real farm/company names
#   - Forbidden file paths (source/, docs/VERIFICATION-REPORT-*, etc.)
#   - Taiwan mobile phone numbers
#   - Precise addresses (鄉/鎮/村/里 with numbers)
#
# Exit codes:
#   0  — all clear
#   1  — violations found; commit blocked
#
# Bypass (emergency only): git commit --no-verify
# See DEIDENTIFICATION-POLICY.md for full policy.
# ============================================================

set -u

# Colors (disabled if not a TTY)
if [ -t 1 ]; then
  RED=$'\033[31m'
  YELLOW=$'\033[33m'
  GREEN=$'\033[32m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  RED=""; YELLOW=""; GREEN=""; BOLD=""; RESET=""
fi

# ------------------------------------------------------------
# Known sensitive identifiers (farmer and farm real names)
# ------------------------------------------------------------
FARMER_NAMES="Farmer-A|Farmer-B|Farmer-C|Farmer-D|Farmer-E|Farmer-F|Farmer-G|Farmer-H|Farmer-I|Farmer-J|Farmer-L|Farmer-M|Farmer-N|Farmer-O|[某農友真名]"

FARM_NAMES="[Farm-A]|[Farm-A]|[Farm-B]|[Farm-B]"

# ------------------------------------------------------------
# Forbidden paths (staged files matching these must not be committed)
# ------------------------------------------------------------
FORBIDDEN_PATHS_REGEX='(^source/|^private/|/source/|docs/VERIFICATION-REPORT-.*\.md$|docs/FARMER-DATA-EXECUTION-SCHEDULE\.md$|docs/FARMER-DATA-BACKUP-.*\.md$|\.credentials/|\.env\.local$|\.env\.production$)'

# ------------------------------------------------------------
# Pattern-based detection (regex applied to added lines only)
# ------------------------------------------------------------
# Taiwan mobile: 09XX-XXX-XXX or 09XXXXXXXX
PHONE_REGEX='09[0-9]{2}[- ]?[0-9]{3}[- ]?[0-9]{3}'

# Precise address (township/village + number): e.g. 中埔鄉民雄村第5鄰, 東石鄉XX路123號
ADDRESS_REGEX='[一-龥]+[鄉鎮區][一-龥]+[村里](第?[0-9]+鄰|路[0-9]+號)'

# ------------------------------------------------------------
# Self-exclusion: the hook and this script must contain the patterns
# they detect — exclude them from content scanning (but still scan paths)
# ------------------------------------------------------------
SELF_FILES_REGEX='^(\.husky/(pre-commit|commit-msg)|scripts/tools/deidentification-check\.sh)$'

# ------------------------------------------------------------
# Collect staged files and diff
# ------------------------------------------------------------
staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)

if [ -z "$staged_files" ]; then
  exit 0  # no staged files
fi

# Files to scan for content (excluding self-referencing hooks)
scan_files=$(echo "$staged_files" | grep -vE "$SELF_FILES_REGEX" || true)

violations=0

# ============================================================
# Check 1: Forbidden file paths
# ============================================================
forbidden_files=$(echo "$staged_files" | grep -E "$FORBIDDEN_PATHS_REGEX" || true)
if [ -n "$forbidden_files" ]; then
  echo ""
  echo "${RED}${BOLD}❌ 敏感路徑檢查失敗 — 以下檔案禁止提交：${RESET}"
  echo "$forbidden_files" | sed "s/^/   ${RED}→${RESET} /"
  echo ""
  echo "   ${YELLOW}這些路徑應在 .gitignore 中排除。檢查：${RESET}"
  echo "   ${YELLOW}grep -E \"source/|VERIFICATION|FARMER-DATA-EXECUTION\" .gitignore${RESET}"
  violations=$((violations + 1))
fi

# ============================================================
# Check 2: Sensitive names in added content (diff + lines)
# ============================================================
# Only look at ADDED lines (not context, not removed), excluding self-files
if [ -n "$scan_files" ]; then
  # shellcheck disable=SC2086
  added_content=$(git diff --cached --no-color -- $scan_files 2>/dev/null | grep -E '^\+' | grep -v '^+++' || true)
else
  added_content=""
fi

if [ -n "$added_content" ]; then
  # Farmer names
  name_hits=$(echo "$added_content" | grep -oE "$FARMER_NAMES" | sort -u || true)
  if [ -n "$name_hits" ]; then
    echo ""
    echo "${RED}${BOLD}❌ 農友真名檢查失敗 — 以下新增內容含有真名：${RESET}"
    echo "$name_hits" | sed "s/^/   ${RED}→${RESET} /"
    echo ""
    echo "   ${YELLOW}替代方案：用 Farmer-A/B/C... 或「某農友」代稱${RESET}"
    # Show which files
    echo "   ${YELLOW}受影響檔案：${RESET}"
    for name in $name_hits; do
      files=$(git diff --cached --name-only -G"$name" 2>/dev/null || true)
      for f in $files; do
        echo "      • $f（含 \"$name\"）"
      done
    done
    violations=$((violations + 1))
  fi

  # Farm/company names
  farm_hits=$(echo "$added_content" | grep -oE "$FARM_NAMES" | sort -u || true)
  if [ -n "$farm_hits" ]; then
    echo ""
    echo "${RED}${BOLD}❌ 農場/企業名稱檢查失敗 — 以下新增內容含有可識別名稱：${RESET}"
    echo "$farm_hits" | sed "s/^/   ${RED}→${RESET} /"
    echo ""
    echo "   ${YELLOW}替代方案：用 [Farm-A/B] 或「某農場」代稱${RESET}"
    violations=$((violations + 1))
  fi

  # Phone numbers
  phone_hits=$(echo "$added_content" | grep -oE "$PHONE_REGEX" | sort -u || true)
  if [ -n "$phone_hits" ]; then
    echo ""
    echo "${RED}${BOLD}❌ 電話號碼檢查失敗 — 新增內容含有手機號碼：${RESET}"
    echo "$phone_hits" | sed "s/^/   ${RED}→${RESET} /"
    echo ""
    echo "   ${YELLOW}聯絡方式絕對不能提交；改為「可透過農會聯繫」${RESET}"
    violations=$((violations + 1))
  fi

  # Precise addresses
  addr_hits=$(echo "$added_content" | grep -oE "$ADDRESS_REGEX" | sort -u || true)
  if [ -n "$addr_hits" ]; then
    echo ""
    echo "${RED}${BOLD}❌ 精確地址檢查失敗 — 新增內容含有可識別地址：${RESET}"
    echo "$addr_hits" | sed "s/^/   ${RED}→${RESET} /"
    echo ""
    echo "   ${YELLOW}精確地址絕對不能提交；只保留縣市級（如「嘉義縣」）${RESET}"
    violations=$((violations + 1))
  fi
fi

# ============================================================
# Result
# ============================================================
if [ "$violations" -gt 0 ]; then
  echo ""
  echo "${RED}${BOLD}═══════════════════════════════════════════════════════════${RESET}"
  echo "${RED}${BOLD}🚨 提交被阻擋：發現 $violations 項去識別化違規${RESET}"
  echo "${RED}${BOLD}═══════════════════════════════════════════════════════════${RESET}"
  echo ""
  echo "${BOLD}修正方式：${RESET}"
  echo "  1. 從 staging 區移除違規檔案：${GREEN}git restore --staged <file>${RESET}"
  echo "  2. 編輯檔案移除敏感內容"
  echo "  3. 重新 stage：${GREEN}git add <file>${RESET}"
  echo "  4. 重新 commit"
  echo ""
  echo "${BOLD}緊急繞過（僅在極端情況使用）：${RESET}"
  echo "  ${YELLOW}git commit --no-verify${RESET}"
  echo ""
  echo "${BOLD}完整政策：${RESET} DEIDENTIFICATION-POLICY.md"
  echo ""
  exit 1
fi

# All clear
echo "${GREEN}✓ 去識別化檢查通過${RESET}"
exit 0
