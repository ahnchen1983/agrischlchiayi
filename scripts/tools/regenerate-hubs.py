#!/usr/bin/env python3
"""
regenerate-hubs.py
重建 knowledge/ 內所有類別 Hub 與跨類別索引 Hub 的自動生成段。

處理範圍：
  - 10 個類別 Hub（_<Cat> Hub.md）：插入「國本學堂歷屆課程」段，依 frontmatter `tags` 內 `第N屆` 分組
  - _Crop-Index Hub.md：依 `crop[]` 自動分群（果菜／果樹／飲品／雜糧／水產／畜禽／設施通用 7 大類）
  - _Tech-Index Hub.md：依 `tech[]` 歸入 12 大主題群（智慧農業／設施環控／灌溉養液／病蟲害／水產／家禽／品牌行銷／經營管理／認證碳權／外銷／計畫書／場域教育）
  - _Learning-Paths Hub.md：手動策展，**本工具不動**（避免破壞 curated 系列）

設計原則：
  1. **冪等**：所有自動生成段都用 `<!-- AUTO-GENERATED: ... START/END -->` markers 包住
     重跑時只替換 marker 內，不影響 curated 內容（核心文章／相關主題等）
  2. **不破壞既有 curated**：類別 Hub 的「核心文章」「相關主題」不動
  3. **可驗證**：執行完後跑 wikilink-validate.sh 確認 0 斷鏈

使用方式：
  python3 scripts/tools/regenerate-hubs.py            # 重建全部 12 個 Hub
  python3 scripts/tools/regenerate-hubs.py --dry-run  # 只報告差異不寫檔
  python3 scripts/tools/regenerate-hubs.py --check    # 檢查 Hub 是否與當前內容同步
  python3 scripts/tools/regenerate-hubs.py --help

退出碼：
  0  全部成功（含 --check 同步）
  1  --check 模式下發現 Hub 與內容不同步
  2  腳本本身錯誤（路徑不存在、無權限等）
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# ──────────────────────────────────────────────
# ANSI Colors
# ──────────────────────────────────────────────
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
GRAY = "\033[0;90m"
BOLD = "\033[1m"
NC = "\033[0m"

# ──────────────────────────────────────────────
# 路徑解析（從 script 位置回推 repo root）
# ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"

# ──────────────────────────────────────────────
# Markers（所有自動生成段都用這套標記，確保冪等）
# ──────────────────────────────────────────────
CAT_GEN_BEGIN = "<!-- AUTO-GENERATED: 國本學堂歷屆課程 START -->"
CAT_GEN_END = "<!-- AUTO-GENERATED: 國本學堂歷屆課程 END -->"
IDX_GEN_BEGIN = "<!-- AUTO-GENERATED: 全站索引 START -->"
IDX_GEN_END = "<!-- AUTO-GENERATED: 全站索引 END -->"

# ──────────────────────────────────────────────
# 類別與分組定義
# ──────────────────────────────────────────────
CATEGORY_DIRS = [
    "Agri-Basics", "Agri-Advanced", "Agri-Marketing",
    "Crop-Production", "Facility-Farming", "Farm-Management",
    "Field-Visits", "Grants-Planning", "Livestock-Health", "Smart-Farming",
]

GEN_LABELS = {
    "第一屆": "第一屆（2021）",
    "第二屆": "第二屆（2021–2022）",
    "第三屆": "第三屆（2023）",
    "第四屆": "第四屆（2024）",
    "第五屆": "第五屆（2025–2026）",
}

CROP_GROUPS = {
    "果菜類": ["小番茄", "番茄", "小黃瓜", "甜瓜", "美濃瓜", "哈密瓜", "洋香瓜",
               "茄子", "瓜類", "彩椒", "辣椒"],
    "果樹類": ["鳳梨", "酪梨", "百香果", "蜜棗", "芒果", "柑橘", "果樹", "棗子"],
    "飲品作物": ["咖啡", "茶葉"],
    "雜糧／葉菜／菇類": ["麻竹筍", "竹筍", "山葵", "葉菜", "菇類", "稻米", "小麥", "大豆"],
    "水產類": ["文蛤", "虱目魚", "白蝦", "烏魚", "鱸魚", "石斑魚", "水產"],
    "畜禽類": ["蛋雞", "肉雞", "家禽", "鵪鶉", "鵪鶉蛋", "豬", "鴨", "鵝"],
    "設施／通用": ["設施作物", "通用"],
}

TECH_THEMES = {
    "智慧農業／IoT／AI": [
        "IoT", "智慧農業", "AI", "感測器", "智慧灌溉", "智慧環控", "雲端環控", "PLC模組",
        "積木堆疊", "數位轉型", "農業AIoT", "RFID", "聲紋識別", "雲端監控", "區塊鏈",
    ],
    "設施環控／溫室": [
        "設施農業", "設施環控", "環控系統", "環控設備", "溫室結構", "溫室規劃",
        "微霧降溫", "電動遮陰", "捲揚通風", "雨知感測", "暗管排水", "淺層暗管",
        "設施栽培", "環境監控", "VPD飽差", "HD飽差", "蒸散管理", "FOEAS", "光合作用全速",
    ],
    "灌溉／養液／施肥": [
        "滴灌", "養液栽培", "養液配方", "養液滴灌", "穩壓滴頭", "AB養液桶",
        "Fertigation", "碟式過濾器", "穩壓", "EC", "pH", "張力計", "素瓷杯",
        "石膏塊", "田間容水量", "肥料管理", "肥培", "合理化施肥", "土壤檢測",
    ],
    "病蟲害管理／生物防治": [
        "IPM", "生物防治", "微生物製劑", "芽孢桿菌", "木黴菌", "PGPR", "生物刺激素",
        "費洛蒙誘殺", "OneHealth", "三向度觀察法", "邏輯排除法", "田間診斷",
        "植物醫學", "望聞問切", "菌泥檢測", "柯霍氏準則", "ITS分子鑑定",
        "Decline三因子", "零檢出", "質譜快篩", "光合菌", "免登記資材", "安全用藥",
    ],
    "水產養殖": [
        "潮汐取水", "池塘穩定化", "批次保本收穫", "低密度養殖", "底土ORP",
        "溶氧監測", "鹽度管理", "枯草桿菌", "藍碳", "診斷陪伴", "水質管理", "益生菌",
    ],
    "家禽飼養／畜牧": [
        "智慧雞舍", "家禽飼養", "飼料配方", "飼料添加", "農副產物循環", "翦抗", "減抗",
        "熱緊迫管理", "間歇光照", "瘤胃球菌", "植生素添加", "抗氧化飼養",
        "機能性酵素", "友善飼養", "動物福利", "淨零", "減碳", "區塊鏈溯源",
    ],
    "品牌行銷／通路": [
        "品牌行銷", "品牌戰略", "品牌定位", "AISAS", "集客式行銷", "差別取價",
        "B2C品牌SOP", "4P組合", "通路選擇", "聯名合作", "B2B/B2C/B2B2C", "市場定位",
        "觀眾分類法", "參展效能公式", "行銷漏斗", "視覺陳列", "大數據決策",
        "產製儲銷玩", "計畫性生產", "異業結盟", "食農教育", "集貨宅配",
        "六級產業化", "Slogan行銷", "IQF急速冷凍", "TAP溯源", "通路E化系統",
    ],
    "經營管理／戰略": [
        "KPI設定", "平衡計分卡", "PDCA", "OEE", "績效管理", "資產週轉率",
        "策略地圖", "農場財務", "農業人力", "ERP導入", "農業營運模式", "目標管理",
        "工具應用", "八大指標評估", "診斷式輔導", "產業聯盟", "資源盤點",
        "戰略規劃", "農業政策",
    ],
    "認證／補助／碳權／ESG": [
        "產銷履歷", "HACCP", "ISO22000", "TAP", "GLOBAL G.A.P.", "嘉義優鮮",
        "標章驗證", "ESG", "碳盤查", "ISO14064-1", "黃碳", "碳權", "MRV",
        "農業減碳", "綠色供應鏈", "碳足跡", "災損補助80%", "環控補助50%",
        "GPS拍照核銷", "設施年限", "法規遵循", "容許使用申請", "設施補助",
    ],
    "外銷／國際化": ["全濕式管理", "光波選別", "SOP對接", "國際外銷", "冷鏈外銷", "外銷標準"],
    "計畫書撰寫／提案": ["計畫書撰寫", "提案規劃", "公部門文件", "經營計畫書"],
    "場域交流／教育": ["場域交流", "養殖紀錄", "食農教育", "食魚教育", "六級化", "創業輔導"],
}


# ──────────────────────────────────────────────
# Frontmatter parsing helpers
# ──────────────────────────────────────────────
def parse_fm(path: Path) -> dict:
    """簡易 YAML frontmatter parser（只處理單行欄位）。"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def parse_array(s: str) -> list[str]:
    """解析 inline YAML array 如 'tags: [a, b, c]'。"""
    if not s or s.strip() in ("[]", "''", '""'):
        return []
    s = s.strip().strip("[]")
    if not s:
        return []
    return [p.strip().strip("'\"") for p in s.split(",") if p.strip()]


def detect_gen(tags_str: str) -> str | None:
    """從 tags 字串偵測屆別標籤（第一屆～第五屆）。"""
    if not tags_str:
        return None
    for k in GEN_LABELS:
        if k in tags_str:
            return k
    return None


# ──────────────────────────────────────────────
# Phase 1: Category Hubs（10 個類別）
# ──────────────────────────────────────────────
def build_category_section(cat_dir: str) -> str | None:
    """產生單一類別 Hub 的「國本學堂歷屆課程」段。"""
    cat_path = KNOWLEDGE_DIR / cat_dir
    files = sorted(p for p in cat_path.glob("*.md") if not p.name.startswith("_"))
    if not files:
        return None

    by_gen = {k: [] for k in GEN_LABELS}
    others = []
    for p in files:
        fm = parse_fm(p)
        if not fm:
            others.append((p, "無 frontmatter"))
            continue
        gen = detect_gen(fm.get("tags", ""))
        title = fm.get("title", p.stem).strip("'\"")
        if gen:
            by_gen[gen].append((p, title))
        else:
            others.append((p, title))

    total = sum(len(v) for v in by_gen.values()) + len(others)
    lines = [
        CAT_GEN_BEGIN,
        "",
        "## 國本學堂歷屆課程",
        "",
        f"*本類別共 {total} 篇課程／知識紀錄，依屆別分組：*",
        "",
    ]
    for gen_key, file_list in by_gen.items():
        if not file_list:
            continue
        lines.append(f"### {GEN_LABELS[gen_key]}")
        lines.append("")
        for p, _ in sorted(file_list, key=lambda x: x[1]):
            lines.append(f"- [[{p.stem}]]")
        lines.append("")
    if others:
        lines.append("### 其他（既有知識主檔）")
        lines.append("")
        for p, _ in sorted(others, key=lambda x: x[1]):
            lines.append(f"- [[{p.stem}]]")
        lines.append("")
    lines.append(CAT_GEN_END)
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Phase 2: Cross-cutting Hubs（Crop-Index, Tech-Index）
# ──────────────────────────────────────────────
def collect_all_articles() -> list[tuple[str, str, list[str], list[str], str | None]]:
    """掃全 knowledge/，回傳 (slug, title, crops, techs, gen) 列表。"""
    items = []
    for p in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        if p.name.startswith("_"):
            continue
        fm = parse_fm(p)
        if not fm:
            continue
        slug = p.stem
        title = fm.get("title", slug).strip("'\"")
        crops = parse_array(fm.get("crop", ""))
        techs = parse_array(fm.get("tech", ""))
        tags = parse_array(fm.get("tags", ""))
        gen = next((t for t in tags if re.match(r"第[一二三四五]屆", t)), None)
        items.append((slug, title, crops, techs, gen))
    return items


def build_crop_index(items: list) -> str:
    crop_to_articles: defaultdict[str, list] = defaultdict(list)
    for slug, title, crops, _, _ in items:
        if not crops:
            crop_to_articles["未標記作物"].append((slug, title))
        for c in crops:
            crop_to_articles[c].append((slug, title))

    lines = [
        IDX_GEN_BEGIN,
        "",
        "## 作物索引（自動生成）",
        "",
        f"*依 frontmatter `crop[]` 自動分群，共 {len(items)} 篇文章。同一篇文章若標記多個作物會在多處出現。*",
        "",
    ]
    seen = set()
    for group_name, group_crops in CROP_GROUPS.items():
        any_in = [c for c in group_crops if c in crop_to_articles]
        if not any_in:
            continue
        lines.append(f"### {group_name}")
        lines.append("")
        for c in sorted(any_in, key=lambda x: -len(crop_to_articles[x])):
            articles = sorted(crop_to_articles[c], key=lambda x: x[1])
            lines.append(f"#### {c}（{len(articles)} 篇）")
            lines.append("")
            for slug, _ in articles:
                lines.append(f"- [[{slug}]]")
            lines.append("")
            seen.add(c)

    other = [c for c in crop_to_articles if c not in seen and c != "未標記作物"]
    if other:
        lines.append("### 其他作物")
        lines.append("")
        for c in sorted(other, key=lambda x: -len(crop_to_articles[x])):
            articles = sorted(crop_to_articles[c], key=lambda x: x[1])
            lines.append(f"#### {c}（{len(articles)} 篇）")
            lines.append("")
            for slug, _ in articles:
                lines.append(f"- [[{slug}]]")
            lines.append("")

    lines.append(IDX_GEN_END)
    return "\n".join(lines)


def build_tech_index(items: list) -> str:
    tech_to_articles: defaultdict[str, list] = defaultdict(list)
    article_to_techs: dict[str, tuple[str, list[str]]] = {}
    for slug, title, _, techs, _ in items:
        article_to_techs[slug] = (title, techs)
        for t in techs:
            tech_to_articles[t].append((slug, title))

    lines = [
        IDX_GEN_BEGIN,
        "",
        "## 技術索引（自動生成）",
        "",
        f"*依 frontmatter `tech[]` 自動歸入主題群，共 {len(items)} 篇文章。同一篇若涵蓋多技術會出現多次。*",
        "",
    ]

    classified: defaultdict[str, set] = defaultdict(set)
    for theme, theme_techs in TECH_THEMES.items():
        for t in theme_techs:
            if t in tech_to_articles:
                for slug, title in tech_to_articles[t]:
                    classified[theme].add((slug, title))

    for theme in TECH_THEMES:
        articles = classified.get(theme, set())
        if not articles:
            continue
        lines.append(f"### {theme}（{len(articles)} 篇）")
        lines.append("")
        for slug, _ in sorted(articles, key=lambda x: x[1]):
            lines.append(f"- [[{slug}]]")
        lines.append("")

    classified_slugs = {slug for s in classified.values() for slug, _ in s}
    untagged = [
        (s, t) for s, (t, techs) in article_to_techs.items()
        if s not in classified_slugs and techs
    ]
    if untagged:
        lines.append(f"### 其他技術主題（{len(untagged)} 篇）")
        lines.append("")
        for slug, _ in sorted(untagged, key=lambda x: x[1]):
            lines.append(f"- [[{slug}]]")
        lines.append("")

    lines.append(IDX_GEN_END)
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Replace markers in Hub file (idempotent)
# ──────────────────────────────────────────────
def replace_section(hub_path: Path, marker_begin: str, marker_end: str,
                    new_section: str, dry_run: bool = False) -> tuple[bool, str]:
    """
    將 hub_path 內 marker 包住的段替換為 new_section。
    若 marker 不存在則 append 在檔尾。

    Returns:
        (changed: bool, status_msg: str)
    """
    txt = hub_path.read_text(encoding="utf-8")
    pat = re.compile(re.escape(marker_begin) + r".*?" + re.escape(marker_end), re.DOTALL)
    if pat.search(txt):
        new_txt = pat.sub(new_section, txt)
        msg = "替換既有區塊"
    else:
        new_txt = txt.rstrip() + "\n\n" + new_section + "\n"
        msg = "新增區塊（首次）"

    if new_txt == txt:
        return False, "無變化"

    if not dry_run:
        hub_path.write_text(new_txt, encoding="utf-8")
    return True, msg


# ──────────────────────────────────────────────
# Main flow
# ──────────────────────────────────────────────
def regenerate(dry_run: bool = False, check_only: bool = False) -> int:
    """
    重建所有 Hub。

    Returns:
        exit code: 0 = success, 1 = check-mode out-of-sync detected
    """
    if not KNOWLEDGE_DIR.exists():
        print(f"{RED}❌ knowledge/ 目錄不存在: {KNOWLEDGE_DIR}{NC}", file=sys.stderr)
        return 2

    out_of_sync = 0
    changes = []

    # Phase 1: Category Hubs
    print(f"{BOLD}=== Phase 1: 10 個類別 Hub ==={NC}")
    for cat in CATEGORY_DIRS:
        section = build_category_section(cat)
        if section is None:
            print(f"  {YELLOW}⚠️  {cat}: 無內容檔，跳過{NC}")
            continue
        hub_files = list((KNOWLEDGE_DIR / cat).glob("_*.md"))
        if not hub_files:
            print(f"  {YELLOW}⚠️  {cat}: 無 Hub 檔，跳過{NC}")
            continue
        hub = hub_files[0]
        changed, msg = replace_section(
            hub, CAT_GEN_BEGIN, CAT_GEN_END, section,
            dry_run=(dry_run or check_only),
        )
        n_entries = section.count("- [[")
        if changed:
            sym = "△" if (dry_run or check_only) else "✓"
            color = YELLOW if check_only else GREEN
            print(f"  {color}{sym}{NC}  {hub.name}: {n_entries} entries ({msg})")
            changes.append((str(hub.relative_to(REPO_ROOT)), msg))
            if check_only:
                out_of_sync += 1
        else:
            print(f"  {GRAY}·  {hub.name}: {n_entries} entries（已同步）{NC}")

    # Phase 2: Cross-cutting Hubs
    print(f"\n{BOLD}=== Phase 2: 跨類別索引 Hub ==={NC}")
    items = collect_all_articles()
    print(f"{GRAY}收集到 {len(items)} 篇內容檔{NC}")

    cross_hubs = [
        (KNOWLEDGE_DIR / "Crop-Index" / "_Crop-Index Hub.md", build_crop_index(items), "Crop-Index"),
        (KNOWLEDGE_DIR / "Tech-Index" / "_Tech-Index Hub.md", build_tech_index(items), "Tech-Index"),
    ]
    for hub, section, label in cross_hubs:
        if not hub.exists():
            print(f"  {YELLOW}⚠️  {label}: Hub 檔不存在 {hub.name}，跳過{NC}")
            continue
        changed, msg = replace_section(
            hub, IDX_GEN_BEGIN, IDX_GEN_END, section,
            dry_run=(dry_run or check_only),
        )
        n_entries = section.count("- [[")
        if changed:
            sym = "△" if (dry_run or check_only) else "✓"
            color = YELLOW if check_only else GREEN
            print(f"  {color}{sym}{NC}  {hub.name}: {n_entries} entries ({msg})")
            changes.append((str(hub.relative_to(REPO_ROOT)), msg))
            if check_only:
                out_of_sync += 1
        else:
            print(f"  {GRAY}·  {hub.name}: {n_entries} entries（已同步）{NC}")

    # Note about Learning-Paths
    print(f"\n{GRAY}註：_Learning-Paths Hub.md 內「跨屆主題系列 A-H」為手動策展，本工具不動。{NC}")

    # Summary
    print()
    if check_only:
        if out_of_sync:
            print(f"{RED}❌ {out_of_sync} 個 Hub 與當前內容不同步{NC}")
            print(f"{GRAY}   執行 python3 scripts/tools/regenerate-hubs.py 重建{NC}")
            return 1
        else:
            print(f"{GREEN}✅ 全部 12 個 Hub 與內容同步{NC}")
            return 0
    elif dry_run:
        print(f"{YELLOW}△ DRY-RUN: {len(changes)} 個 Hub 會被更新（未寫檔）{NC}")
        return 0
    else:
        if changes:
            print(f"{GREEN}✅ 已重建 {len(changes)} 個 Hub{NC}")
        else:
            print(f"{GREEN}✅ 全部 Hub 已是最新狀態{NC}")
        print(f"{GRAY}   建議：bash scripts/tools/wikilink-validate.sh knowledge/ 驗證 0 斷鏈{NC}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="重建 knowledge/ 的所有 Hub 索引（10 類別 + Crop-Index + Tech-Index）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  python3 scripts/tools/regenerate-hubs.py               # 重建全部
  python3 scripts/tools/regenerate-hubs.py --dry-run     # 預覽差異
  python3 scripts/tools/regenerate-hubs.py --check       # CI 同步檢查（不改檔）

何時跑：
  - 新增／刪除／重新命名 knowledge/<Cat>/*.md 後
  - 修改 frontmatter 的 tags / crop / tech / 第N屆 後
  - CI 可掛 --check 阻擋未同步的 commit
        """,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true",
                       help="只列出會變動的 Hub，不實際寫檔")
    group.add_argument("--check", action="store_true",
                       help="檢查 Hub 是否與內容同步，若不同步 exit 1（適合 CI）")
    args = parser.parse_args()

    sys.exit(regenerate(dry_run=args.dry_run, check_only=args.check))


if __name__ == "__main__":
    main()
