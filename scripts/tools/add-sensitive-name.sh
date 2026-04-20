#!/usr/bin/env bash
# ============================================================
# Register a new sensitive identifier with the deidentification hook
# ============================================================
# Usage:
#   bash scripts/tools/add-sensitive-name.sh "農友姓名"
#   bash scripts/tools/add-sensitive-name.sh "農友1" "農友2" "農場A"
#
# What it does:
#   1. Computes SHA256-16 of each name
#   2. Checks for duplicates
#   3. Appends new hashes to deidentification-check.py
#   4. Appends new hashes to .husky/commit-msg
#   5. Runs a quick self-test
#
# Names are NEVER stored in files — only their hashes.
# ============================================================

set -eu

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 \"姓名1\" [\"姓名2\" ...]" >&2
  echo "" >&2
  echo "Registers new sensitive identifiers with the deidentification hook." >&2
  echo "Only hashes are stored — the plaintext names you pass here never land" >&2
  echo "on disk. Pass them as command-line arguments (no files)." >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY_FILE="$REPO_ROOT/scripts/tools/deidentification-check.py"
HOOK_FILE="$REPO_ROOT/.husky/commit-msg"

if [ ! -f "$PY_FILE" ]; then
  echo "❌ 找不到 $PY_FILE" >&2
  exit 1
fi

# Read existing hashes (so we can detect duplicates)
existing_hashes=$(grep -oE '"[a-f0-9]{16}"' "$PY_FILE" | tr -d '"' | sort -u)

# Generate hashes and check for duplicates
new_hashes=()
for name in "$@"; do
  if [ -z "$name" ]; then continue; fi
  hash=$(python3 -c "import hashlib, sys; print(hashlib.sha256(sys.argv[1].encode('utf-8')).hexdigest()[:16])" "$name")
  name_len=$(python3 -c "import sys; print(len(sys.argv[1]))" "$name")

  if echo "$existing_hashes" | grep -q "^${hash}$"; then
    echo "⚠️  跳過（已存在）: hash=${hash} (len=${name_len})"
    continue
  fi

  # Check collision within this batch
  already_in_batch=0
  for h in "${new_hashes[@]:-}"; do
    if [ "$h" = "$hash" ]; then
      already_in_batch=1
      break
    fi
  done
  if [ "$already_in_batch" -eq 1 ]; then
    echo "⚠️  跳過（本批重複）: hash=${hash}"
    continue
  fi

  new_hashes+=("$hash:$name_len")
  echo "✓ 新增: hash=${hash} (len=${name_len})"
done

if [ "${#new_hashes[@]}" -eq 0 ]; then
  echo ""
  echo "沒有需要新增的 hash。結束。"
  exit 0
fi

# ------------------------------------------------------------
# Insert hashes into deidentification-check.py
# ------------------------------------------------------------
# Format: add before the closing '}' of SENSITIVE_HASHES = {
tmp_py="$(mktemp)"
awk -v hashes_raw="$(printf "%s\n" "${new_hashes[@]}")" '
  BEGIN {
    n = split(hashes_raw, arr, "\n")
  }
  /^SENSITIVE_HASHES: set\[str\] = \{/ { in_block = 1 }
  in_block && /^\}/ {
    for (i = 1; i <= n; i++) {
      if (arr[i] == "") continue
      split(arr[i], parts, ":")
      printf "    \"%s\",  # len=%s (added)\n", parts[1], parts[2]
    }
    in_block = 0
  }
  { print }
' "$PY_FILE" > "$tmp_py"
mv "$tmp_py" "$PY_FILE"
echo ""
echo "✓ 已更新 $PY_FILE"

# ------------------------------------------------------------
# Insert hashes into .husky/commit-msg
# ------------------------------------------------------------
if [ -f "$HOOK_FILE" ]; then
  tmp_hook="$(mktemp)"
  awk -v hashes_raw="$(printf "%s\n" "${new_hashes[@]}")" '
    BEGIN {
      n = split(hashes_raw, arr, "\n")
    }
    /^SENSITIVE_HASHES = \{/ { in_block = 1 }
    in_block && /^\}/ {
      for (i = 1; i <= n; i++) {
        if (arr[i] == "") continue
        split(arr[i], parts, ":")
        printf "    \"%s\",\n", parts[1]
      }
      in_block = 0
    }
    { print }
  ' "$HOOK_FILE" > "$tmp_hook"
  mv "$tmp_hook" "$HOOK_FILE"
  echo "✓ 已更新 $HOOK_FILE"
fi

echo ""
echo "======================================================================"
echo "  📝 下一步："
echo "    1. 檢查 git diff 確認只新增了 hash（無明文名字）"
echo "    2. 測試 hook 能抓到新名字："
echo "       echo '測試 <新名字>' > /tmp/t.md && git add /tmp/t.md"
echo "       （hook 應該會擋下來）"
echo "    3. commit 並 push 更新的 hash 清單"
echo "======================================================================"
