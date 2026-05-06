# Session 交接紀錄 — 2026-05-04

> **目的**：完整交代「12 張業者卡片進 repo」+「Hub 自動化工具」+「_Home.md 重構」三個階段的工作內容、產出、commit 鏈、與下一步必要動作。
>
> **撰寫時機**：6 個 commit 全部 push 完成、所有驗證綠燈。本檔讓下一位接手者（你自己回電腦、或下一輪 Code session）可以無對話歷史也能完整接續。
>
> **與前一份的關係**：本檔接續 [SESSION-HANDOFF-2026-05-01.md](SESSION-HANDOFF-2026-05-01.md)。前一份完成「Phase A：白名單機制」+「Phase B：121 課程整合」並留下 4 大後續工作（§7）。本檔處理其中 P0 兩項（修 wikilink + 更新 Hub）+ P1 業者卡片整合 + 額外加做 Hub 維運工具與 _Home 重構。

---

## 0. 30 秒摘要

| 項目 | 狀態 |
|---|---|
| P0：修 24 檔 / 45 個 wikilink 斷鏈 | ✅ 完成（commit `9e6486a36`） |
| P0：更新 Hub 索引（170 檔） | ✅ 完成（commit `c71c7ab34`） |
| P1：12 張業者卡片進 repo（指南型文章） | ✅ 完成（commit `acdcd8ff6`） |
| 副工作：Hub 二次重建（納入新增 12 檔） | ✅ 完成（commit `a2beb6d8`） |
| 副工作：寫 `regenerate-hubs.py` 維運工具 | ✅ 完成（commit `7fef9bb52`） |
| 副工作：重構 `_Home.md`（解決 13 Hub-title 斷鏈） | ✅ 完成（commit `ca94987b0`） |
| LECTURER-WHITELIST 擴增（5+2 → 13+10） | ✅ 完成（與 `acdcd8ff6` 同 commit） |
| 全 repo 驗證 | ✅ wikilink 0 斷鏈、deidentification 0 hits、pre-commit hook 全綠 |

**目前 repo 狀態**：
- main HEAD = `ca94987b0`，與 origin/main 同步
- `knowledge/`：**182 檔**（49 既有 + 121 課程 + 12 業者指南）
- `LECTURER-WHITELIST.md`：**23 entries**（13 公開講師 + 10 服務機構）
- `scripts/tools/`：**18 個工具**（含新增 `regenerate-hubs.py`）

---

## 1. 起點：對話接手

對話起點是 user 想把 `__preview_md__/_OPERATORS/` 12 張業者卡片倒進 repo。但前一輪 SESSION-HANDOFF-2026-05-01 留下的 §7 工作清單還沒處理：

- [P0] 修 24 檔 / 45 個 wikilink 斷鏈
- [P0] 更新 12 個 Hub 檔
- [P1] 處理跨屆衝突檔
- [P2] 移除 SESSION-HANDOFF-2026-05-01.md 或保留

優先級判斷：先做 P0 兩項解鎖正常 commit hook（不再用 `--no-verify`），再處理業者卡片。

---

## 2. 工作鏈（6 個 commit）

### Commit 1：`9e6486a36` — fix: resolve 45 broken wikilinks

**問題**：前一輪 commit 用 `--no-verify` 跳過 wikilink-validate hook，留下 24 檔 / 45 個斷鏈。

**修法分三類**：

- **Type A（30 處）**：alias to existing file
  - 例 `[[嘉義四季耕作節奏規劃]]` → `[[嘉義農場四季耕作節奏規劃指南|嘉義四季耕作節奏規劃]]`
  - 例 `[[小黃瓜銷售通路策略：批發、行口、直銷的成本效益分析]]` → `[[小黃瓜銷售通路策略|...]]`
- **Type B（5 處）**：strip brackets to plain text（target 真不存在）
  - 圓夢計畫鳳梨切苗、批發市場運作機制、農業電商平台評估（×2）、農場社群經營 IG/FB/LINE、農作物栽培技術
- **Type C（7 處）**：category-name wikilinks → plain text
  - `[[Agri-Marketing|...]]`, `[[Crop-Production|...]]` 等 → 移除 brackets

**腳本**：兩支 Python 腳本（exact-string 套替換 + regex 含 alias 替換）。

**驗證**：`wikilink-validate.sh knowledge/` → 0 broken across all 170 articles。

---

### Commit 2：`c71c7ab34` — feat: rebuild all 13 Hub indexes (10 category + 3 cross-cutting)

**問題**：170 檔倒入 `knowledge/` 後，沒被任何 Hub 收錄；前台類別頁、Hub 精選清單、學習路徑都缺。

**作法**：

- **10 個類別 Hub**：append `## 國本學堂歷屆課程` 段，依屆別分組（第一屆～第五屆 + 其他）
- **_Crop-Index Hub**：依 `crop[]` 自動分群，7 大類（果菜／果樹／飲品／雜糧／水產／畜禽／設施通用），211 entries
- **_Tech-Index Hub**：依 `tech[]` 歸入 12 主題群，191 entries
- **_Learning-Paths Hub**：append 跨屆主題系列 A–H 共 8 條（手動策展，含養液滴灌／智慧雞舍／文蛤戰略／品牌建構／設施溫室／植物保護／戰略班四大產業／碳權淨零）
- **冪等**：所有自動段都用 `<!-- AUTO-GENERATED: ... START/END -->` markers 包住，未來可重跑不破壞 curated 內容（核心文章／相關主題）

**腳本**：當時是兩支臨時 Python 腳本，後在 commit 5 整合進 `regenerate-hubs.py`。

---

### Commit 3：`acdcd8ff6` — feat: add 12 public-lecturer guide articles + expand whitelist to 23 entries

**前置**：12 張業者卡片在 `__preview_md__/_OPERATORS/` 下，需評估如何進 repo。

**盤點報告**（`__preview_md__/_OPERATORS/REPO_FARMER_DATA_INVENTORY.md`）發現：

repo 已有完整的「農友／業者建檔」**四層體系**：
- L1 真相層：`農民md檔/`（gitignored，77 檔）
- L2 案例層：`knowledge/Farmer-Cases/`（規劃中）
- L3 指南層：`knowledge/<10 大類>/`（已有 8 篇含農友案例）
- L4 例外層：`LECTURER-WHITELIST.md`（公開講師例外）

**12 張業者卡片定位**：屬於 L4 例外層。

**3 路徑評估**：
- 路徑 A（推薦）：套 §8.2 公開講師例外，改寫成「指南型文章」進 `knowledge/<Cat>/`
- 路徑 B：新增 `operators` collection（次選）
- 路徑 C：放 `Farmer-Cases/`（性質衝突，不適用）

**user 裁示走 A**。執行步驟：

1. **計算 16 個 hash**（8 人 + 8 機構）：陳昆懷／陳明輝／陳俊翰／洪睿弘／陳惠琪／楊宜樺／陳明瞭／詹勝仁 + 8 個對應服務機構
2. **補登記 LECTURER-WHITELIST.md**：v1.2 → v1.3，從 7 entries（5 人 + 2 機構）擴增至 **23 entries（13 人 + 10 機構）**
3. **改寫 12 張卡片**：frontmatter 對齊 zh-TW schema（移除 `type`/`operator`/`specialties` 等非 schema 欄位、`crops` → `crop`、補 `level`/`category`/`year`/`courseDate`）
4. **落點分布**：
   - Smart-Farming（+2）：東昀農場、天賜的禮物
   - Livestock-Health（+1）：蛤董養殖
   - Agri-Marketing（+3）：裕泰農場、卡維蘭、純淨農產合作社
   - Farm-Management（+1）：旺萊山
   - Facility-Farming（+2）：奕家果園、耿赫智能農場
   - Field-Visits（+3）：打寶蛤、哈哈魚場、新農果菜合作社
5. **修內部 wikilink**：原業者卡片互相用 `[[<農場>（<人名>）]]` 引用，新檔名變了，需一輪 alias 替換

**結果**：knowledge/ 從 170 → **182 檔**，全綠 wikilink + deidentification（白名單覆蓋成功）。

---

### Commit 4：`a2beb6d8` — chore: regenerate Hub indexes after operator article additions

**作法**：跑 commit 2 的兩支腳本第二次，把新增的 12 篇納入 Hub。

**結果**：

| 類別 Hub | 之前 | 現在 | 變化 |
|---------|-----|-----|-----|
| Smart-Farming | 30 | 32 | +2 |
| Livestock-Health | 16 | 17 | +1 |
| Agri-Marketing | 27 | 30 | +3 |
| Farm-Management | 14 | 15 | +1 |
| Facility-Farming | 13 | 15 | +2 |
| Field-Visits | 14 | 17 | +3 |
| Crop-Index | 211 | 229 | +18 |
| Tech-Index | 191 | 204 | +13 |

---

### Commit 5：`7fef9bb52` — feat: add regenerate-hubs.py tool

**動機**：前一個 commit 跑了兩支臨時腳本第二次，這代表「未來新增文章還要再跑一次」。把臨時腳本整合成正式 repo 工具。

**位置**：`scripts/tools/regenerate-hubs.py`（執行權限已開）

**功能**：
- 重建 10 個類別 Hub + Crop-Index Hub + Tech-Index Hub（共 12 個）
- `_Learning-Paths Hub.md` 不動（手動策展）
- 冪等用 `<!-- AUTO-GENERATED: ... START/END -->` markers
- 三種模式：
  - 預設：重建全部
  - `--dry-run`：預覽不寫檔
  - `--check`：CI 同步檢查（不同步 exit 1）
- 純標準函式庫，無外部依賴
- 路徑自動解析（從 script 位置回推 repo root）

**註冊**：`scripts/tools/TOOL-INVENTORY.md` 更新到 v1.1（17 → 18 個工具）。

**測試結果**：
```
$ python3 scripts/tools/regenerate-hubs.py --check
✅ 全部 12 個 Hub 與內容同步
$ python3 scripts/tools/regenerate-hubs.py --dry-run
△ DRY-RUN: 0 個 Hub 會被更新（未寫檔）
```

---

### Commit 6：`ca94987b0` — docs: refactor _Home.md

**問題**：`_Home.md` 有 13 個 wikilinks 指向 Hub `title`（如 `[[農業基礎入門]]` 對應 `_Agri-Basics Hub.md` 的 `title: 農業基礎入門`），但 wikilink-validate.sh 排除 `_*` 檔，導致永遠報 13 個斷鏈。預設掃描 `knowledge/` 跳過 `_*` 不會看到，但直接掃 `_Home.md` 會 fail。

**實際情境**：`_Home.md` 是 SSOT／Obsidian graph 用，**不被 Astro 首頁渲染**（`src/pages/index.astro` 用 React 元件，不讀 _Home.md）。

**重構策略：雙模式導航**

- **Markdown link**：給 Astro 訪客（網站）— `[類別名](slug/)` 直連類別 Hub 頁面
- **Wikilink**：給 Obsidian graph + validator — 改指該類別代表文章（如 `[[土壤基礎知識]]` 代表「農業基礎入門」類別）

**新版內容（66 行）**：

1. 介紹段（5 屆 182 篇、10 大領域）
2. 知識庫規模（檔案數／屆別／講師／系列）
3. 十大知識類別表格（類別 / Hub link / 代表文章 wikilink × 2）
4. 跨類別索引表格（3 個 cross-cutting Hub）
5. 推薦起步閱讀（複用 src/pages/index.astro 的 readingPathSteps）
6. 跨屆主題系列 A–H
7. 平台原則（連結 DEIDENTIFICATION-POLICY、LECTURER-WHITELIST）
8. 貢獻

**驗證**：`wikilink-validate.sh knowledge/_Home.md` → 0 broken（之前 13 broken）。

---

## 3. 目前 git 狀態

```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

最近 6 個 commits（origin/main HEAD = `ca94987b0`）：

```
ca94987b0 docs: refactor _Home.md to resolve 13 Hub-title wikilinks
7fef9bb52 feat: add regenerate-hubs.py tool
a2beb6d8f chore: regenerate Hub indexes after operator article additions
acdcd8ff6 feat: add 12 public-lecturer guide articles + expand whitelist to 23 entries
c71c7ab34 feat: rebuild all 13 Hub indexes (10 category + 3 cross-cutting)
9e6486a36 fix: resolve 45 broken wikilinks across 24 files
```

---

## 4. ⚠️ 已知未解問題

### 4.1 `.git/index.lock` 重現

**現況**：每次 sandbox 跑 `git status` 等指令會留 `.git/index.lock`（沙盒 mount 權限無法釋放）。下次需 commit 前要先 `rm -f .git/index.lock`。

**對策**：寫 commit 指令時內含 `rm -f .git/index.lock`，並改用 `find/cat/awk` 等 fs 指令查狀態（避免叫 `git`）。

### 4.2 剩餘 7 份待 OCR 骨架

| 屆 | 份數 | 位置 |
|---|---|---|
| 第二屆 | 1（從零開始養液滴灌03-水肥合一）| `__preview_md__/02.第二屆/_NOT_FOR_REPO_骨架未更新/` |
| 第三屆 | 5（農產品市場定位/場域交流補充/L4-print/品牌育成0425/0427無人機）| `__preview_md__/03.第三屆/_NOT_FOR_REPO_骨架未更新/` |
| 第四屆 | 1（0827 場農技課）| `__preview_md__/04.第四屆/_NOT_FOR_REPO_骨架未更新/` |

**處理路徑**：
1. user 本機 OCR（用 OCR 工具或上 GitHub `yuncidigital2018/line-ordering-systems-tw` 接續）
2. 完成後 Code session 接手回填、走 `FARMER-DATA-PROCESSING-CHECKLIST` 6 步流程

詳見各 `_NOT_FOR_REPO_骨架未更新/OCR_TODO.md`。

### 4.3 `regenerate-hubs.py --check` 未掛 pre-commit hook

**現況**：工具就位但 CI／hook 沒整合。新增文章後若忘記跑 `regenerate-hubs.py`，Hub 會與內容不同步（不會擋 commit，但前台精選清單會缺）。

**建議**：在 `.husky/pre-commit` 加：
```bash
# Hub sync check
python3 scripts/tools/regenerate-hubs.py --check || exit 1
```

或加進 GitHub Actions CI。預估 15 min。

### 4.4 `agri source/` 仍存於 repo？

第 1 輪 session 用 `git clone https://github.com/yuncidigital2018/line-ordering-systems-tw.git` 抓 OCR 來源，沙盒 `/tmp/line-ordering-systems-tw/` 已隨 session 結束清理。**不在 repo 內，無問題**。

### 4.5 `__preview_md__/_OPERATORS/SCHEMA_PROPOSAL.md` 已過時

該提案討論「業者卡片用獨立 collection 還是嵌入 knowledge」，user 採路徑 A（嵌入）後，提案內容已過時。**保留作歷史紀錄，無需處理**。

---

## 5. 下一步候選工作（給接手者）

### 5.1 [P1] 把 `regenerate-hubs.py --check` 掛 pre-commit hook

**目的**：防止以後新增文章忘記重建 Hub。

**做法**：

```bash
# 在 .husky/pre-commit 適當位置加：
echo "🔍 Hub sync check..."
python3 scripts/tools/regenerate-hubs.py --check || {
  echo "❌ Hub indexes are out-of-sync."
  echo "   執行: python3 scripts/tools/regenerate-hubs.py"
  echo "   然後重新 git add knowledge/ + commit"
  exit 1
}
```

**工程量**：15 min（含本機測試）。

### 5.2 [P2] 處理剩 7 份待 OCR 骨架

**前置**：等 user 完成 OCR（本機跑 OCR 工具或上傳到 `yuncidigital2018/line-ordering-systems-tw`）。

**做法**：照 commit 3 的模式（讀 OCR md → 對齊 frontmatter → 進 knowledge/<Cat>/ → 跑 `regenerate-hubs.py` → commit）。

**工程量**：每份 30–60 min。

### 5.3 [P2] 第二屆「養殖漁業銷售定位.md」既有不準

該檔（陳惠琪在第二屆養殖進階班）frontmatter 已經修正 instructor 為「陳惠琪（最正農婦／純淨農產合作社）」，但**內文** body 可能仍寫「Farmer 某某」之類。

**做法**：讀該檔，若有 body 仍有去識別化代號（與 frontmatter 真名不一致）需更新。

### 5.4 [P2] 業者卡片有效性追蹤

12 張卡片中有 LECTURER-WHITELIST 對應（13 人 + 10 機構），若未來該講師明確要求下架，需：

1. 從 LECTURER-WHITELIST.md 移除對應 entry
2. 在 knowledge/ 內搜尋下架對應內容
3. 從相關 Hub 與 _Home.md 移除引用
4. push hotfix

DEIDENTIFICATION-POLICY §8.2「移除白名單」流程已記載。

### 5.5 [P3] Operators 改用獨立 collection（未來重構）

若 user 後悔走「嵌入 knowledge/」路徑、想改用獨立 `operators` collection，可參考 `__preview_md__/_OPERATORS/SCHEMA_PROPOSAL.md` 既有設計。

**現況**：這條路徑暫不啟動，當 12 張卡片進 knowledge/ 後互動如預期，且 SOP 已套上 §8.2 例外。

---

## 6. 驗證指令清單（接手後第一件事）

```bash
cd ~/Documents/Github/agrischlchiayi

# 1. 確認 lock 已清
ls .git/index.lock 2>&1 && echo "❌ lock 還在" || echo "✓ no lock"

# 2. 確認 commit chain
git log --oneline -6
# 預期：ca94987b0 ← 7fef9bb52 ← a2beb6d8f ← acdcd8ff6 ← c71c7ab34 ← 9e6486a36

# 3. knowledge/ 檔數
find knowledge/ -maxdepth 2 -name "*.md" -not -name "_*" | wc -l
# 預期：182

# 4. wikilink validate
bash scripts/tools/wikilink-validate.sh knowledge/
# 預期：✅ 全部 wikilink 目標都存在

# 5. _Home.md 直接掃
bash scripts/tools/wikilink-validate.sh knowledge/_Home.md
# 預期：✅ 0 broken（前一輪是 13 broken）

# 6. deidentification 全 sweep
python3 -c "
import importlib.util, os
from pathlib import Path
spec = importlib.util.spec_from_file_location('deid', 'scripts/tools/deidentification-check.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
issues = []
for root, dirs, files in os.walk('knowledge'):
    for f in files:
        if not f.endswith('.md') or f.startswith('_'): continue
        path = os.path.join(root, f)
        hits = m.find_hash_hits(Path(path).read_text(encoding='utf-8', errors='replace'), file_path=path)
        if hits: issues.append((path, sorted(hits)))
print(f'SENSITIVE_HASHES: {len(m.SENSITIVE_HASHES)}, LECTURER_WHITELIST: {len(m.LECTURER_WHITELIST)}')
print(f'Files with sensitive hits: {len(issues)}')
"
# 預期：SENSITIVE_HASHES: 87, LECTURER_WHITELIST: 23, Files with sensitive hits: 0

# 7. Hub 同步檢查
python3 scripts/tools/regenerate-hubs.py --check
# 預期：✅ 全部 12 個 Hub 與內容同步
```

---

## 7. 關鍵檔案速查

| 角色 | 檔案位置 |
|---|---|
| 政策 SSOT | [DEIDENTIFICATION-POLICY.md](../DEIDENTIFICATION-POLICY.md) v1.2 |
| 公開講師白名單 | [LECTURER-WHITELIST.md](../LECTURER-WHITELIST.md) v1.3（23 entries）|
| 去識別化檢查腳本 | [scripts/tools/deidentification-check.py](../scripts/tools/deidentification-check.py)（87 hashes + 2-pass whitelist）|
| Hub 重建工具 | [scripts/tools/regenerate-hubs.py](../scripts/tools/regenerate-hubs.py) |
| 工具索引 | [scripts/tools/TOOL-INVENTORY.md](../scripts/tools/TOOL-INVENTORY.md) v1.1 |
| 課程內容 | `knowledge/<10 大類>/*.md`（170 → **182 檔**）|
| 業者卡片預覽（已搬遷）| `~/Documents/國本學堂課程內容/__preview_md__/_OPERATORS/`（12 張卡 + INDEX + SCHEMA_PROPOSAL + REPO_FARMER_DATA_INVENTORY）|
| 跨屆衝突紀錄 | `~/Documents/國本學堂課程內容/__preview_md__/05.第五屆/CROSS_YEAR_CONFLICTS_FULL.md` |
| 待 OCR 清單 | `~/Documents/國本學堂課程內容/__preview_md__/0X.第X屆/_NOT_FOR_REPO_骨架未更新/OCR_TODO.md` |
| 前一份交接 | [SESSION-HANDOFF-2026-05-01.md](SESSION-HANDOFF-2026-05-01.md) |
| 本份交接 | `docs/SESSION-HANDOFF-2026-05-04.md` |

---

## 8. 簽核

| 項目 | 內容 |
|---|---|
| 撰寫 | Claude（Cowork dispatch session） |
| 撰寫日期 | 2026-05-04 |
| 工作鏈 | 6 個 commit（`9e6486a36` → `ca94987b0`） |
| 涵蓋工作 | P0 wikilink 修正 + P0 Hub 重建 + P1 業者卡片整合 + 維運工具 + _Home 重構 |
| 全 repo 驗證狀態 | ✅ wikilink 0 斷鏈、deidentification 0 hits、pre-commit hook 全綠 |
| 後續工作清單 | §5（5 大項，1 P1 + 3 P2 + 1 P3）|
| 待 user | 1) 確認 6 個 commit 都已 push；2) 視需要處理 §5 工作 |

---

**END**
