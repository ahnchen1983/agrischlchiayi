#!/usr/bin/env python3
"""
Deidentify raw farmer data files.

Reads files from `source-raw/` (raw, real-name filenames), applies
replacement rules, and writes anonymised versions to `source/` with
Farmer-X / [Farm-X] codes.

Both folders are git-ignored. The name→code mapping lives in
`.dev/deidentification-mapping.txt` (also git-ignored). If this
mapping file does not exist, it is created on first run.

Workflow:
  1. Put raw files in source-raw/ (filename = farmer's real name,
     e.g. `某農友.md`). Existing source-raw/ is only read, never
     modified or deleted.
  2. (Optional) Pre-populate .dev/deidentification-mapping.txt to
     keep codes consistent with prior work:

       # Format: CODE = NAME1, NAME2, NAME3
       Farmer-A = 某農友
       Farmer-B = 某農友乙
       [Farm-A] = 某農場全名, 某農場簡稱

  3. Run: python3 scripts/tools/deidentify-source.py
  4. Review the deidentified output in source/
  5. Registered names automatically get their hashes added to
     scripts/tools/deidentification-check.py so the commit hook
     will catch future accidental leaks.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "source-raw"
OUT_DIR = REPO_ROOT / "source"
DEV_DIR = REPO_ROOT / ".dev"
MAPPING_FILE = DEV_DIR / "deidentification-mapping.txt"
CHECK_PY = REPO_ROOT / "scripts" / "tools" / "deidentification-check.py"
ADD_NAME_PY = REPO_ROOT / "scripts" / "tools" / "add-sensitive-name.py"

# --------------------------------------------------------------------------
# Substitution patterns (regex)
# --------------------------------------------------------------------------
PHONE_RE = re.compile(r"09\d{2}[- ]?\d{3}[- ]?\d{3}")
LANDLINE_RE = re.compile(r"\b0[2-8][- ]?\d{3,4}[- ]?\d{4}\b")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
LINE_ID_RE = re.compile(r"(?:LINE|Line|line)[\s:：]*[\w@.-]{3,}", re.IGNORECASE)
# Precise address: township/區 + village + (number or 第N鄰 or 路N號)
ADDRESS_RE = re.compile(
    r"[\u4e00-\u9fff]+[鄉鎮區]\s*[\u4e00-\u9fff]+[村里]\s*"
    r"(?:第\s*\d+\s*鄰|[\u4e00-\u9fff]*路\s*\d+\s*號?|\d+\s*號)?"
)

# Terminal colors
if sys.stdout.isatty():
    G, Y, R, B, RST = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"
else:
    G = Y = R = B = RST = ""


# --------------------------------------------------------------------------
# Mapping file I/O
# --------------------------------------------------------------------------
def load_mapping() -> dict[str, list[str]]:
    """Return {code: [name, name, ...]} from the mapping file."""
    if not MAPPING_FILE.exists():
        return {}
    mapping: dict[str, list[str]] = {}
    for raw_line in MAPPING_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        code, names_part = line.split("=", 1)
        code = code.strip()
        names = [n.strip() for n in names_part.split(",") if n.strip()]
        if code and names:
            mapping[code] = names
    return mapping


def save_mapping(mapping: dict[str, list[str]]) -> None:
    DEV_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Deidentification mapping — PRIVATE, never commit.",
        "# Edit manually to add aliases (e.g. nicknames, surname+title).",
        "# Format: CODE = NAME1, NAME2, NAME3",
        "",
    ]
    # Sort: Farmer-A..Z first, then Farmer-AA.., then [Farm-X]
    def sort_key(code: str) -> tuple[int, str]:
        if code.startswith("Farmer-"):
            suffix = code[len("Farmer-"):]
            return (0, f"{len(suffix):02d}{suffix}")
        if code.startswith("[Farm-"):
            return (1, code)
        return (2, code)

    for code in sorted(mapping.keys(), key=sort_key):
        lines.append(f"{code} = {', '.join(mapping[code])}")
    MAPPING_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_name_to_code(mapping: dict[str, list[str]]) -> dict[str, str]:
    """Invert mapping for fast lookup."""
    rev: dict[str, str] = {}
    for code, names in mapping.items():
        for n in names:
            rev[n] = code
    return rev


def next_farmer_code(mapping: dict[str, list[str]]) -> str:
    used = {c for c in mapping if c.startswith("Farmer-")}
    # Skip K to stay consistent with the original assignment that skipped K
    for c in "ABCDEFGHIJLMNOPQRSTUVWXYZ":
        code = f"Farmer-{c}"
        if code not in used:
            return code
    for c1 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for c2 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            code = f"Farmer-{c1}{c2}"
            if code not in used:
                return code
    raise RuntimeError("Ran out of farmer codes")


def next_farm_code(mapping: dict[str, list[str]]) -> str:
    used = {c for c in mapping if c.startswith("[Farm-")}
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        code = f"[Farm-{c}]"
        if code not in used:
            return code
    raise RuntimeError("Ran out of farm codes")


# --------------------------------------------------------------------------
# Core deidentification
# --------------------------------------------------------------------------
def deidentify(content: str, name_to_code: dict[str, str]) -> tuple[str, dict]:
    """Apply all replacements. Returns (new_content, report_dict)."""
    report = {"names": {}, "phones": 0, "landlines": 0,
              "emails": 0, "line_ids": 0, "addresses": 0}

    # Replace names — longest first to avoid partial clobbering
    for name in sorted(name_to_code.keys(), key=len, reverse=True):
        code = name_to_code[name]
        occurrences = content.count(name)
        if occurrences > 0:
            content = content.replace(name, code)
            report["names"][name] = (code, occurrences)

    # Structured PII patterns → redacted tokens
    def _sub(pattern, token, key):
        nonlocal content
        matches = pattern.findall(content)
        if matches:
            content = pattern.sub(token, content)
            report[key] = len(matches)

    _sub(PHONE_RE, "[REDACTED-MOBILE]", "phones")
    _sub(LANDLINE_RE, "[REDACTED-LANDLINE]", "landlines")
    _sub(EMAIL_RE, "[REDACTED-EMAIL]", "emails")
    _sub(LINE_ID_RE, "[REDACTED-LINE-ID]", "line_ids")
    _sub(ADDRESS_RE, "[REDACTED-ADDRESS]", "addresses")

    return content, report


def extract_candidate_names(content: str) -> set[str]:
    """Best-effort heuristic: find possible Chinese personal names not yet
    in the mapping. The user should review these — this is a hint, not a
    guarantee."""
    candidates: set[str] = set()

    # Pattern A: NAME + role suffix (e.g. 王先生, 某某某老師)
    suffix_pattern = re.compile(
        r"([\u4e00-\u9fff]{2,4})"
        r"(?:先生|小姐|老師|太太|妻子|配偶|兒子|女兒|女士|師傅|老闆|農友|同仁|員工)"
    )
    for m in suffix_pattern.finditer(content):
        candidates.add(m.group(1))

    # Pattern B: relation prefix + NAME (e.g. 兒子某某某, 老婆某某某, 父親某某某)
    # Names are usually 2-3 Chinese chars; stop before common non-name
    # characters (verbs, particles) to avoid grabbing "某某某將".
    prefix_pattern = re.compile(
        r"(?:兒子|女兒|配偶|妻子|老婆|丈夫|老公|父親|母親|爸爸|媽媽|"
        r"哥哥|弟弟|姊姊|妹妹|叔叔|伯父|舅舅|岳父|岳母|合夥人|夥伴)"
        r"([\u4e00-\u9fff]{2,3})"
        r"(?=將|也|是|在|於|和|跟|與|及|以|從|到|由|把|被|的|了|們|就|都|還|"
        r"先生|小姐|一|今|昨|明|每|去|來|前|後|跟我|說|表示|認為|想|"
        r"之|之後|之前|而|而且|，|。|、|\s|$)"
    )
    # Block list: common Chinese words that aren't names (reduce noise)
    stoplist = {
        "他們", "我們", "你們", "大家", "各位", "朋友", "夥伴",
        "一起", "合作", "互相", "許多", "某位", "某個",
    }
    for m in prefix_pattern.finditer(content):
        cand = m.group(1)
        if cand not in stoplist:
            candidates.add(cand)

    return candidates


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    if not RAW_DIR.exists():
        print(f"{R}✗{RST} {RAW_DIR} 不存在。")
        print(f"  請先建立這個資料夾並放入原始檔案（檔名 = 農友真名）。")
        return 1

    OUT_DIR.mkdir(exist_ok=True)
    DEV_DIR.mkdir(exist_ok=True)

    raw_files = sorted(RAW_DIR.glob("*.md"))
    if not raw_files:
        print(f"{R}✗{RST} {RAW_DIR} 裡沒有 .md 檔案。")
        return 1

    mapping = load_mapping()
    name_to_code = build_name_to_code(mapping)

    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}")
    print(f"{B} 去識別化處理：{len(raw_files)} 個原始檔案{RST}")
    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}")
    if mapping:
        print(f"  已載入 {len(mapping)} 個現有代號對應")
    else:
        print(f"  對應表為空，將為每個檔案自動分配代號")
    print()

    newly_registered: list[str] = []
    suspicious_hits: dict[str, set[str]] = {}

    for raw_file in raw_files:
        name = raw_file.stem  # 某農友.md → 某農友

        if name in name_to_code:
            code = name_to_code[name]
            marker = f"{G}✓{RST}"
            status = "已對應"
        else:
            code = next_farmer_code(mapping)
            mapping[code] = [name]
            name_to_code[name] = code
            newly_registered.append(name)
            marker = f"{Y}🆕{RST}"
            status = "新分配"

        content = raw_file.read_text(encoding="utf-8", errors="replace")

        # Look for candidate names not yet mapped (warn user)
        unknown = extract_candidate_names(content) - set(name_to_code.keys())
        if unknown:
            suspicious_hits[raw_file.name] = unknown

        anonymized, report = deidentify(content, name_to_code)

        out_file = OUT_DIR / f"{code}.md"
        out_file.write_text(anonymized, encoding="utf-8")

        # Summary
        name_count = sum(c for _, c in report["names"].values())
        total_pii = (report["phones"] + report["landlines"] +
                     report["emails"] + report["line_ids"] +
                     report["addresses"])
        print(f"{marker} {raw_file.name:30} → {out_file.name:18} [{status}]")
        print(f"    姓名替換：{name_count}  電話：{report['phones']+report['landlines']}  "
              f"Email：{report['emails']}  Line：{report['line_ids']}  "
              f"地址：{report['addresses']}")

    # Save updated mapping
    save_mapping(mapping)

    print()
    print(f"{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RST}")

    if newly_registered:
        print(f"{G}✓{RST} 新登錄 {len(newly_registered)} 個農友到對應表：")
        for n in newly_registered:
            print(f"    • {n} → {name_to_code[n]}")

        # Register hashes into the check script
        print(f"\n  登錄 hash 到 commit hook...")
        try:
            subprocess.run(
                [sys.executable, str(ADD_NAME_PY), *newly_registered],
                check=True, cwd=str(REPO_ROOT),
            )
        except Exception as e:
            print(f"  {Y}⚠ add-sensitive-name.py 執行失敗：{e}{RST}")
            print(f"  請手動執行：python3 {ADD_NAME_PY.relative_to(REPO_ROOT)} \"name1\" \"name2\"")

    if suspicious_hits:
        print(f"\n{Y}⚠ 發現未登錄的疑似姓名（請人工檢查）：{RST}")
        for fname, names in suspicious_hits.items():
            still_unknown = names - set(name_to_code.keys())
            if still_unknown:
                print(f"    在 {fname}: {', '.join(sorted(still_unknown))}")
        print(f"\n  若這些是農友/家人姓名，請編輯對應表加入：")
        print(f"    {MAPPING_FILE.relative_to(REPO_ROOT)}")
        print(f"  格式範例：Farmer-A = 某農友, 某先生, 某農友爸")
        print(f"  然後重跑此腳本。")

    print()
    print(f"{B}輸出：{RST}")
    print(f"  去識別化後檔案：{OUT_DIR.relative_to(REPO_ROOT)}/")
    print(f"  對應表（私密）：{MAPPING_FILE.relative_to(REPO_ROOT)}")
    print()
    print(f"{B}下一步：{RST}")
    print(f"  1. 檢查 {OUT_DIR.relative_to(REPO_ROOT)}/ 裡的檔案是否乾淨")
    print(f"  2. 人工審查「疑似姓名」並決定是否加進對應表")
    print(f"  3. 撰寫文章時參考 {OUT_DIR.relative_to(REPO_ROOT)}/Farmer-X.md")
    print(f"  4. commit 時 pre-commit hook 會擋住意外洩漏")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
