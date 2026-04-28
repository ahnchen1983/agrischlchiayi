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
    "9494328e3a68dc3b",  # len=3 (added)
    "732a732701125dab",  # len=3 (added)
    "8ffdff3b76d33720",  # len=3 (added)
    "ebc0c541652397ce",  # len=3 (added)
    "66b42845d2aa6dfa",  # len=3 (added)
    "c4029b8f4cec01c9",  # len=4 (added)
    "7b8f6635a8e48154",  # len=3 (added)
    "d79ee0d146343f7f",  # len=5 (added)
    "12cc56f9fa9db353",  # len=3 (added)
    "b6513a3d64a65ffd",  # len=3 (added)
    "5fefdfb82164daa5",  # len=3 (added)
    "e742a2e3ffb1c442",  # len=3 (added)
    "73d99e922d4b2aa4",  # len=10 (added)
    "03d97c6b864708b8",  # len=4 (added)
    "a626e6c6d4d2a27a",  # len=3 (added)
    "09a07d6168002b1a",  # len=3 (added)
    "d02aa6dfa1a2f9ee",  # len=3 (added)
    "38241b7784ab47b1",  # len=3 (added)
    "8b69e0a2fa7646d9",  # len=3 (added)
    "08aae78cc2a557a7",  # len=3 (added)
    "de359ed8cfde1cd7",  # len=3 (added)
    "bb5b8da329382c0e",  # len=3 (added)
    "6dc93ad942a7ea55",  # len=3 (added)
    "ba2a01e330cabd77",  # len=3 (added)
    "6981968863c275c0",  # len=3 (added)
    "5bc48cabc58b5c3e",  # len=3 (added)
    "91ee7f921ec168ad",  # len=3 (added)
    "e85b8052f3569125",  # len=3 (added)
    "3977fe8f7d3036c5",  # len=7 (added)
    "1af46825aabd3058",  # len=5 (added)
    "1f1e19f97895785b",  # len=3 (added)
    "f60b57c431a0d6ab",  # len=3 (added)
    "f8d3f635ad35e8a6",  # len=3 (added)
    "fd5cf39b0f82f0af",  # len=3 (added)
    "da86d3f747c31ff8",  # len=3 (added)
    "6c70970ca65d1d8b",  # len=3 (added)
    "07bcc96731869be4",  # len=3 (added)
    "f5b06582b8461ed7",  # len=3 (added)
    "a93936d7429ada02",  # len=3 (added)
    "488fc84e240bd354",  # len=3 (added)
    "a77cd200459b61db",  # len=3 (added)
    "bdc0294a782377bf",  # len=3 (added)
    "6732ed500187e3ae",  # len=3 (added)
    "59d4a892c6e9e554",  # len=3 (added)
    "f0b01fc841fac20b",  # len=9 (added)
    "ad0d8570d4800fe7",  # len=3 (added)
    "0e6470a3ca7a48d3",  # len=3 (added)
    "3268310720890a43",  # len=3 (added)
    "33c77a7803878c48",  # len=3 (added)
    "d7b88974f74e442f",  # len=3 (added)
    "e80765856e025948",  # len=3 (added)
    "5a9e05101ded26f5",  # len=3 (added)
    "b184d623831683ae",  # len=3 (added)
    "2440f225c6caf7b9",  # len=3 (added)
    "36841e9880431f18",  # len=2 (added)
    "a666dd6a6f00081d",  # len=3 (added)
    "663d056daf2172b2",  # len=3 (added)
    "f85893cd4b29dc79",  # len=3 (added)
    "9b95965273e7d08e",  # len=3 (added)
    "5620778be96d2ecf",  # len=3 (added)
    "e048493dfa731556",  # len=3 (added)
    "3317a6824b3d6012",  # len=3 (added)
    "c0fe62f0afa6105a",  # len=3 (added)
    "da2559912e020fe6",  # len=3 (added)
    "d60917d493657a50",  # len=3 (added)
    "dfbc29dccb00d546",  # len=3 (added)
    "c734b0e6c45f887d",  # len=3 (added)
    "fc1a1cfec5ab64a5",  # len=3 (added)
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
# Address: 鄉/鎮/區 + 村/里 + (第N鄰 or 路N號), tolerating whitespace anywhere
ADDRESS_RE = re.compile(
    r"[\u4e00-\u9fff]+[鄉鎮區]\s*[\u4e00-\u9fff]+[村里]\s*(?:第\s*\d+\s*鄰|路\s*\d+\s*號)"
)


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
    # -c core.quotepath=false ensures non-ASCII filenames (e.g. Chinese)
    # come through as UTF-8 rather than octal-escaped, which would break
    # path-based git diff queries.
    try:
        return subprocess.check_output(
            ["git", "-c", "core.quotepath=false", *args],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace")
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
