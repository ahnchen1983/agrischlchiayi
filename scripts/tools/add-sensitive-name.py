#!/usr/bin/env python3
"""
Register new sensitive identifier(s) with the deidentification hook.

Names are accepted as command-line arguments (not from files) and
never written to disk. Only their SHA256-16 hashes are appended to:
  - scripts/tools/deidentification-check.py
  - .husky/commit-msg

Usage:
  python3 scripts/tools/add-sensitive-name.py "姓名1" ["姓名2" ...]
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PY_FILE = REPO_ROOT / "scripts" / "tools" / "deidentification-check.py"
HOOK_FILE = REPO_ROOT / ".husky" / "commit-msg"


def sha16(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def existing_hashes(path: Path) -> set[str]:
    """Extract all 16-hex-char hashes from a file."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'"([a-f0-9]{16})"', text))


def insert_hashes_py(path: Path, new_entries: list[tuple[str, int]]) -> None:
    """Insert into SENSITIVE_HASHES set in the Python file."""
    text = path.read_text(encoding="utf-8")
    # Find the closing brace of SENSITIVE_HASHES = { ... }
    marker_start = text.find("SENSITIVE_HASHES: set[str] = {")
    if marker_start < 0:
        # Try alternative marker (e.g. plain dict form)
        marker_start = text.find("SENSITIVE_HASHES = {")
    if marker_start < 0:
        raise RuntimeError(f"Could not find SENSITIVE_HASHES marker in {path}")

    # Find the closing '}' of this set
    brace_depth = 0
    i = text.find("{", marker_start)
    end = -1
    while i < len(text):
        if text[i] == "{":
            brace_depth += 1
        elif text[i] == "}":
            brace_depth -= 1
            if brace_depth == 0:
                end = i
                break
        i += 1
    if end < 0:
        raise RuntimeError(f"Could not find closing brace in {path}")

    # Build insertion lines
    lines_to_add = "".join(
        f'    "{h}",  # len={n} (added)\n' for h, n in new_entries
    )

    new_text = text[:end] + lines_to_add + text[end:]
    path.write_text(new_text, encoding="utf-8")


def insert_hashes_hook(path: Path, new_entries: list[tuple[str, int]]) -> None:
    """Insert into the SENSITIVE_HASHES set inside the commit-msg hook."""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    marker_start = text.find("SENSITIVE_HASHES = {")
    if marker_start < 0:
        return  # nothing to update

    brace_depth = 0
    i = text.find("{", marker_start)
    end = -1
    while i < len(text):
        if text[i] == "{":
            brace_depth += 1
        elif text[i] == "}":
            brace_depth -= 1
            if brace_depth == 0:
                end = i
                break
        i += 1
    if end < 0:
        return

    lines_to_add = "".join(f'    "{h}",\n' for h, _ in new_entries)
    new_text = text[:end] + lines_to_add + text[end:]
    path.write_text(new_text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: add-sensitive-name.py '姓名1' ['姓名2' ...]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Registers new sensitive identifiers with the deidentification hook.", file=sys.stderr)
        print("Plaintext names never land on disk — only SHA256-16 hashes are stored.", file=sys.stderr)
        return 1

    if not PY_FILE.exists():
        print(f"❌ 找不到 {PY_FILE}", file=sys.stderr)
        return 1

    known = existing_hashes(PY_FILE)
    to_add: list[tuple[str, int]] = []
    seen_in_batch: set[str] = set()

    for name in sys.argv[1:]:
        if not name:
            continue
        h = sha16(name)
        if h in known:
            print(f"⚠️  跳過（已存在）: hash={h} (len={len(name)})")
            continue
        if h in seen_in_batch:
            print(f"⚠️  跳過（本批重複）: hash={h}")
            continue
        seen_in_batch.add(h)
        to_add.append((h, len(name)))
        print(f"✓ 新增: hash={h} (len={len(name)})")

    if not to_add:
        print("\n沒有需要新增的 hash。結束。")
        return 0

    insert_hashes_py(PY_FILE, to_add)
    print(f"\n✓ 已更新 {PY_FILE.relative_to(REPO_ROOT)}")
    if HOOK_FILE.exists():
        insert_hashes_hook(HOOK_FILE, to_add)
        print(f"✓ 已更新 {HOOK_FILE.relative_to(REPO_ROOT)}")

    print()
    print("=" * 70)
    print("  📝 下一步：")
    print("    1. 檢查 git diff 確認只新增了 hash（無明文名字）")
    print("    2. 測試 hook 能抓到新名字")
    print("    3. commit 並 push 更新的 hash 清單")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
