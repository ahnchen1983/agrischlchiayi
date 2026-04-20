#!/usr/bin/env python3
"""
Deidentification Pre-commit Check (hash-based)
================================================
Scans staged changes for sensitive farmer data WITHOUT storing real
names in cleartext. Uses SHA256-16 hashes for detection so the
detection script itself contains no recoverable identifiers.

Detects:
  - Real farmer names (hash-matched against Chinese 2-4 char windows)
  - Taiwan mobile phone numbers
  - Precise addresses (鄉/鎮/區 + 村/里 + 號數)
  - Forbidden file paths (source/, VERIFICATION-REPORT-*, etc.)

Exit codes:
  0 — all clear
  1 — violations found; commit blocked

Bypass (emergency only): git commit --no-verify
See DEIDENTIFICATION-POLICY.md for full policy.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Hash table — SHA256-16 of known sensitive names.
# The source names are NOT stored here; only their hashes.
# To add a new name:
#   python3 -c "import hashlib; print(hashlib.sha256('NAME'.encode()).hexdigest()[:16])"
# ---------------------------------------------------------------------------
SENSITIVE_HASHES: set[str] = {
    "6f38e3042df13c90",
    "1bde4d547f2488de",
    "17eb58e7a3b44a6b",
    "43dc7543b1d3d2df",
    "ffb37c0425f0ddd4",
    "45995cfe14eb0887",
    "e1584dc3eee0ceec",
    "b7f763cd8592883a",
    "c5e839525d6db32b",
    "cc7c498447e8b3ce",
    "5df1c25f70a7d7ad",
    "4c90f80a99384d78",
    "f3cad159360b1e7c",
    "da9658e1fc134d6f",
    "1c25e3454d92a143",
    "f187e765f39c3e59",
    "a30c009b9a814fbe",
    "372e3628b388ac4f",
    "c4d3729aa49695c5",
}

# Windows sizes for Chinese char substring matching (covers 2-4 char names/farms)
HASH_WINDOW_SIZES = (2, 3, 4, 5, 6)

# ---------------------------------------------------------------------------
# Forbidden file paths — staged files matching these patterns block commit
# ---------------------------------------------------------------------------
FORBIDDEN_PATH_PATTERNS = [
    re.compile(r"^source/"),
    re.compile(r"^private/"),
    re.compile(r"/source/"),
    re.compile(r"^docs/VERIFICATION-REPORT-.*\.md$"),
    re.compile(r"^docs/FARMER-DATA-EXECUTION-SCHEDULE\.md$"),
    re.compile(r"^docs/FARMER-DATA-BACKUP-.*\.md$"),
    re.compile(r"^\.credentials/"),
    re.compile(r"\.env\.local$"),
    re.compile(r"\.env\.production$"),
]

# ---------------------------------------------------------------------------
# Self-exclusion — this script and the hooks must reference some patterns
# in regex form; exclude them from content scanning (paths are still checked)
# ---------------------------------------------------------------------------
SELF_FILES = {
    ".husky/pre-commit",
    ".husky/commit-msg",
    "scripts/tools/deidentification-check.sh",
    "scripts/tools/deidentification-check.py",
}

# ---------------------------------------------------------------------------
# Regex patterns (these can be cleartext; they describe PATTERNS not NAMES)
# ---------------------------------------------------------------------------
CHINESE_CHAR_RUN = re.compile(r"[\u4e00-\u9fff]+")
PHONE_RE = re.compile(r"09\d{2}[- ]?\d{3}[- ]?\d{3}")
ADDRESS_RE = re.compile(r"[\u4e00-\u9fff]+[鄉鎮區][\u4e00-\u9fff]+[村里](?:第?\d+鄰|路\d+號)")


# ---------------------------------------------------------------------------
# Terminal colors (disabled when stdout is not a TTY)
# ---------------------------------------------------------------------------
def _colors() -> dict[str, str]:
    if sys.stdout.isatty():
        return {
            "red": "\033[31m",
            "yellow": "\033[33m",
            "green": "\033[32m",
            "bold": "\033[1m",
            "reset": "\033[0m",
        }
    return {k: "" for k in ("red", "yellow", "green", "bold", "reset")}


C = _colors()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha16(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL).decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return ""


def extract_added_lines(diff: str) -> str:
    """Return only the added content from a unified diff (strip +++ headers)."""
    return "\n".join(
        line[1:]
        for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def find_hash_hits(text: str) -> set[str]:
    """Scan text for Chinese substrings whose hash matches any known sensitive hash.
    Returns the set of matched CLEARTEXT substrings so the user can see what
    was detected (these are the farmer's own names — we're only surfacing what
    the user is already trying to commit)."""
    hits: set[str] = set()
    for run_match in CHINESE_CHAR_RUN.finditer(text):
        run = run_match.group(0)
        for size in HASH_WINDOW_SIZES:
            for i in range(0, len(run) - size + 1):
                window = run[i : i + size]
                if sha16(window) in SENSITIVE_HASHES:
                    hits.add(window)
    return hits


def print_block(title: str, items: list[str], remediation: str) -> None:
    print()
    print(f"{C['red']}{C['bold']}❌ {title}{C['reset']}")
    for it in items:
        print(f"   {C['red']}→{C['reset']} {it}")
    print()
    print(f"   {C['yellow']}{remediation}{C['reset']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    staged = [p for p in run_git(["diff", "--cached", "--name-only", "--diff-filter=ACM"]).splitlines() if p]
    if not staged:
        return 0

    violations = 0

    # Check 1: forbidden paths
    forbidden = [p for p in staged if any(pat.search(p) for pat in FORBIDDEN_PATH_PATTERNS)]
    if forbidden:
        print_block(
            "敏感路徑檢查失敗 — 以下檔案禁止提交：",
            forbidden,
            "這些路徑應在 .gitignore 中排除。檢查 .gitignore 的 FARMER DATA PROTECTION 區塊。",
        )
        violations += 1

    # Check 2: content scans (exclude self-files)
    scan_files = [p for p in staged if p not in SELF_FILES]
    if scan_files:
        diff = run_git(["diff", "--cached", "--no-color", "--", *scan_files])
        added = extract_added_lines(diff)

        # Hash-based name detection
        name_hits = find_hash_hits(added)
        if name_hits:
            print_block(
                "敏感姓名/名稱檢查失敗 — 新增內容含有已登錄的敏感識別字串：",
                sorted(name_hits),
                "替代方案：用 Farmer-A/B/C... 或「某農友」、[Farm-A]、「某農場」代稱",
            )
            # Show which files contain them (best-effort)
            print(f"   {C['yellow']}受影響檔案（請手動檢查）：{C['reset']}")
            for f in scan_files:
                try:
                    content = Path(f).read_text(encoding="utf-8", errors="replace")
                    if find_hash_hits(content):
                        print(f"      • {f}")
                except (OSError, UnicodeDecodeError):
                    pass
            violations += 1

        # Phone numbers
        phones = sorted(set(PHONE_RE.findall(added)))
        if phones:
            print_block(
                "電話號碼檢查失敗 — 新增內容含有手機號碼：",
                phones,
                "聯絡方式絕對不能提交；改為「可透過農會聯繫」",
            )
            violations += 1

        # Precise addresses
        addrs = sorted(set(ADDRESS_RE.findall(added)))
        if addrs:
            print_block(
                "精確地址檢查失敗 — 新增內容含有可識別地址：",
                addrs,
                "精確地址絕對不能提交；只保留縣市級（如「嘉義縣」）",
            )
            violations += 1

    if violations:
        print()
        print(f"{C['red']}{C['bold']}═══════════════════════════════════════════════════════════{C['reset']}")
        print(f"{C['red']}{C['bold']}🚨 提交被阻擋：發現 {violations} 項去識別化違規{C['reset']}")
        print(f"{C['red']}{C['bold']}═══════════════════════════════════════════════════════════{C['reset']}")
        print()
        print(f"{C['bold']}修正方式：{C['reset']}")
        print(f"  1. 從 staging 區移除違規檔案：{C['green']}git restore --staged <file>{C['reset']}")
        print("  2. 編輯檔案移除敏感內容")
        print(f"  3. 重新 stage：{C['green']}git add <file>{C['reset']}")
        print("  4. 重新 commit")
        print()
        print(f"{C['bold']}緊急繞過（僅在極端情況使用）：{C['reset']}")
        print(f"  {C['yellow']}git commit --no-verify{C['reset']}")
        print()
        print(f"{C['bold']}完整政策：{C['reset']} DEIDENTIFICATION-POLICY.md")
        print()
        return 1

    print(f"{C['green']}✓ 去識別化檢查通過{C['reset']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
