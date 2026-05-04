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
    "LECTURER-WHITELIST.md",
}

# ---------------------------------------------------------------------------
# Public Lecturer Whitelist — hashes loaded from LECTURER-WHITELIST.md.
# Names matching these hashes ARE allowed to appear in files under the
# whitelist's allowed paths (default: knowledge/).
# Per DEIDENTIFICATION-POLICY.md § Public Lecturer Exception.
# ---------------------------------------------------------------------------
LECTURER_WHITELIST_FILE = (
    Path(__file__).resolve().parent.parent.parent / "LECTURER-WHITELIST.md"
)


def load_lecturer_whitelist() -> dict[str, list[str]]:
    """Parse LECTURER-WHITELIST.md and return {hash: [allowed_path_prefixes]}.
    Each entry in the file is expected to have:
      - `hash`: `XXXXXXXXXXXXXXXX`
      - `paths`: knowledge/, ...
    Returns empty dict if file missing or unparseable."""
    if not LECTURER_WHITELIST_FILE.exists():
        return {}
    try:
        text = LECTURER_WHITELIST_FILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    entries: dict[str, list[str]] = {}
    current_hash: str | None = None
    current_paths: list[str] = []
    hash_re = re.compile(r"^\s*-\s*`hash`\s*:\s*`([0-9a-f]{16})`")
    paths_re = re.compile(r"^\s*-\s*`paths`\s*:\s*(.+)$")
    for line in text.splitlines():
        m = hash_re.match(line)
        if m:
            if current_hash and current_paths:
                entries[current_hash] = current_paths
            current_hash = m.group(1)
            current_paths = []
            continue
        m = paths_re.match(line)
        if m and current_hash:
            current_paths = [
                p.strip().rstrip("/") + "/"
                for p in m.group(1).split(",")
                if p.strip()
            ]
    if current_hash and current_paths:
        entries[current_hash] = current_paths
    return entries


LECTURER_WHITELIST: dict[str, list[str]] = load_lecturer_whitelist()


# Exclusion list — paths where the lecturer whitelist NEVER applies, even if
# the file is under a whitelisted entry's `paths` prefix. Use this to protect
# farmer-case-study aggregation areas where dual-role lecturers must remain
# anonymized as farmers (per DEIDENTIFICATION-POLICY.md § Public Lecturer Exception).
LECTURER_WHITELIST_EXCLUDE_PATTERNS = [
    re.compile(r"^knowledge/Farmer-Cases/"),
    re.compile(r"^農民md檔/"),
    re.compile(r"^source/"),
    re.compile(r"^private/"),
]

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


def find_hash_hits(text: str, file_path: str | None = None) -> set[str]:
    """Scan text for Chinese substrings whose hash matches any known sensitive hash.
    Returns the set of matched CLEARTEXT substrings so the user can see what
    was detected (these are the farmer's own names — we're only surfacing what
    the user is already trying to commit).

    When file_path is provided, applies the public-lecturer whitelist:
    if a matched hash is in LECTURER_WHITELIST and file_path starts with one
    of its allowed path prefixes, the match is treated as compliant. Sub-window
    matches that fall ENTIRELY inside a whitelisted match are also exempted
    (e.g. if 張耿赫 is whitelisted at 3-char window, the 2-char "耿赫" window
    inside it is also skipped — this prevents collateral hits when a public
    lecturer's name overlaps with an unrelated sensitive substring).
    See DEIDENTIFICATION-POLICY.md § Public Lecturer Exception.
    """
    # Pass 1: find all (abs_start, abs_end, window, whitelisted?) for sensitive hashes
    matches: list[tuple[int, int, str, bool]] = []
    for run_match in CHINESE_CHAR_RUN.finditer(text):
        run = run_match.group(0)
        run_start = run_match.start()
        for size in HASH_WINDOW_SIZES:
            for i in range(0, len(run) - size + 1):
                window = run[i : i + size]
                window_hash = sha16(window)
                if window_hash not in SENSITIVE_HASHES:
                    continue
                whitelisted = False
                if file_path and window_hash in LECTURER_WHITELIST:
                    excluded = any(
                        pat.search(file_path)
                        for pat in LECTURER_WHITELIST_EXCLUDE_PATTERNS
                    )
                    if not excluded:
                        allowed = LECTURER_WHITELIST[window_hash]
                        if any(file_path.startswith(p) for p in allowed):
                            whitelisted = True
                matches.append((run_start + i, run_start + i + size, window, whitelisted))

    # Pass 2: collect ranges of whitelisted matches; suppress sub-window hits
    # that fall fully inside any whitelisted range.
    whitelisted_ranges = [(s, e) for s, e, _, w in matches if w]
    hits: set[str] = set()
    for start, end, window, whitelisted in matches:
        if whitelisted:
            continue
        if any(ws <= start and we >= end for ws, we in whitelisted_ranges):
            continue
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
    # Per-file scanning so the public-lecturer whitelist can apply path-based.
    scan_files = [p for p in staged if p not in SELF_FILES]
    aggregated_added = ""  # for phone/address checks (path-agnostic)
    all_name_hits: set[str] = set()
    files_with_hits: list[str] = []

    for f in scan_files:
        file_diff = run_git(["diff", "--cached", "--no-color", "--", f])
        file_added = extract_added_lines(file_diff)
        aggregated_added += "\n" + file_added
        file_hits = find_hash_hits(file_added, file_path=f)
        if file_hits:
            all_name_hits.update(file_hits)
            files_with_hits.append(f)

    if all_name_hits:
        print_block(
            "敏感姓名/名稱檢查失敗 — 新增內容含有已登錄的敏感識別字串：",
            sorted(all_name_hits),
            "替代方案：用 Farmer-A/B/C... 或「某農友」、[Farm-A]、「某農場」代稱\n   公開講師例外請見 LECTURER-WHITELIST.md",
        )
        print(f"   {C['yellow']}受影響檔案：{C['reset']}")
        for f in files_with_hits:
            print(f"      • {f}")
        violations += 1

    # Phone numbers (path-agnostic — never allowed regardless of file location)
    phones = sorted(set(PHONE_RE.findall(aggregated_added)))
    if phones:
        print_block(
            "電話號碼檢查失敗 — 新增內容含有手機號碼：",
            phones,
            "聯絡方式絕對不能提交；改為「可透過農會聯繫」",
        )
        violations += 1

    # Precise addresses (path-agnostic — never allowed regardless of file location)
    addrs = sorted(set(ADDRESS_RE.findall(aggregated_added)))
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
