---
type: cli-roadmap
created: 2026-04-20
session: ε
status: draft — awaiting CheYu review
---

# Taiwan.md CLI Evolution Roadmap (v0.5 → v1.x)

## Executive Summary

`taiwanmd` today is a 15-command read/write CLI shipped on npm (v0.5.0). It proved的 core loop：900+ articles 可以從 terminal search / read / validate / pipe 進 LLM。未來 12 個月要把它變成 Taiwan.md 的 **operating surface** — agents、貢獻者、讀者、Semiont 本身摸到生命體的規範管道。

ε session（2026-04-20）誕生的四個 canonical 升級強制 CLI 進化：

1. **幻覺鐵律（MANIFESTO §10）** — 幻覺以指數速率摧毀可信度。CLI 必須成為 **anti-hallucination 工具**，不只是 retrieval 工具。優先指令：`taiwanmd audit`。
2. **Stage 3.5 Hallucination Audit** — 強制 pipeline gate。CLI 應讓貢獻者在 PR 前本地跑 Stage 3.5。優先指令：`taiwanmd audit <slug>`。
3. **ARTICLE-INBOX / ARTICLE-DONE-LOG** — intake / history 分離需要 CLI surface。優先指令：`taiwanmd inbox`。
4. **SPORE-LOG** — 孢子 pipeline 需要跟 article 同等 first-class 待遇。優先指令：`taiwanmd spore`。

roadmap 提出 v0.6（canonical-sync release）、v0.7（MCP server）、v0.8（organism introspection）、v1.0（first stable + brew + plugins）、v1.x（ecosystem）。

---

## Current State (v0.5.0)

**Distribution**：npm only（`npm install -g taiwanmd`）

**Commands (15)**：

| Phase       | Commands                                             |
| ----------- | ---------------------------------------------------- |
| Phase 0 MVP | `search`, `read`, `list`, `random`, `stats`, `sync`  |
| Phase 1     | auto-sync, remote fallback, multilingual `read --en` |
| Phase 2     | `today`, `quiz`, `explore`, `diff`, `graph`          |
| Phase 3     | `rag`, `contribute`, `validate`                      |
| v0.5.0      | `terminology`                                        |

**Architecture**：

- Node.js ES modules (`"type": "module"`)
- Entry: `cli/src/index.js` dispatched via `commander`
- Data sync: git sparse-checkout to `~/.taiwanmd/knowledge/`
- Search: `minisearch` in-memory index
- Rendering: `marked` + `marked-terminal` + `chalk` + `cli-table3`
- 0 tests（no test framework in `package.json`）
- Engines: Node ≥18

**Lib surface**（`cli/src/lib/`）：`ensure-data.js`、`knowledge.js`、`render.js`、`search.js` — 薄、可重用、新指令的好基底。

---

## User Personas

### 1. AI Agents（RAG consumers）

- **Who**：LLM pipelines、Claude Desktop / Cursor / Warp MCP clients、外部 inference agents
- **Needs**：deterministic structured output（`--json`、`--raw`）、low-latency citations、verified source URLs、stable schema
- **Pain today**：沒有 MCP endpoint；`rag` 回傳 full body 但無 per-claim source links；沒有 `cite` primitive
- **Top wants**：`cite`、MCP server、bundle export、snippet export for AI SEO

### 2. Contributors

- **Who**：CheYu + 外部 PR 作者
- **Needs**：低摩擦 draft → validate → submit loop；PR 前做幻覺檢查；知道「什麼主題可安全寫」
- **Pain today**：`validate` 檢查 formal quality（字數、標題）但不檢查事實基礎。沒有 Stage 3.5 runner。無法 claim inbox 項目
- **Top wants**：`audit`、`inbox claim`、`cite`、Obsidian sync

### 3. Readers

- **Who**：好奇瀏覽者、台灣海外僑民、學生、想離線學習台灣的開發者
- **Needs**：快速 search、愉悅的 terminal 渲染、discovery、`random`、multilingual
- **Pain today**：能用但無 bookmarks、無閱讀歷史、無「從離開的地方繼續」
- **Top wants**：bookmarks、閱讀歷史、`chat` mode、更乾淨的 install（brew）

### 4. Maintainers / Semiont 本身

- **Who**：CheYu 維護者模式、Semiont 的 cron agents、heartbeat 循環
- **Needs**：audit trails、vital signs、harvest metrics、supporter data、publish workflow
- **Pain today**：vital signs 埋在 `stats` 裡；沒有 `organs`、`heartbeat`、`supporters`、`sense` 指令
- **Top wants**：`organs`、`heartbeat`、`supporters`、`sense`、`spore harvest`

---

## Version Roadmap

### v0.6 — Canonical Sync Release（next minor）

**Theme**：讓 ε session 的 canonical 升級在 CLI 成為 first-class。
**New commands (6)**：`audit`、`inbox`、`inbox claim`、`spore new`、`spore harvest`、`spore log`
**Estimated effort**：約 3 週（1 dev）
**Key deps**：none new — 借用 `yaml`、現有 `ensure-data` sync。Optional：`inquirer` for interactive `inbox claim`
**Breaking changes**：none
**Success gate**：`taiwanmd audit` 能在 80%+ seeded test cases 偵測 5 個幻覺 pattern

### v0.7 — MCP Server Mode

**Theme**：讓 taiwanmd 從 Claude Desktop / Cursor / Warp 直接可用。
**New commands (2)**：`mcp serve`、`mcp install`（emit Claude Desktop config snippet）
**Architecture**：加入 `@modelcontextprotocol/sdk` dep；`search`、`read`、`rag`、`cite`、`stats` 暴露為 MCP tools
**Estimated effort**：約 2 週
**Key deps**：`@modelcontextprotocol/sdk`
**Breaking changes**：none
**Success gate**：taiwanmd 可透過一行 config 從 Claude Desktop 被 query

### v0.8 — Organism Introspection

**Theme**：讓 Semiont 的 vitals 透過 CLI 浮現
**New commands (5)**：`organs`、`heartbeat`、`supporters`、`sense`、`cite`
**Data sources**：`public/api/dashboard-*.json`（跟 knowledge 一起 sync）
**Estimated effort**：約 3 週
**Key deps**：none new
**Breaking changes**：`stats` output 重新分區 — 舊的 embedded organ data 移到 `organs`。`--legacy` flag 保留到 v0.9 for back-compat

### v0.9 — Pre-stable hardening

**Theme**：testing、performance、offline-first、upgrade path
**New commands (2)**：`upgrade`（self-update）、`doctor`（diagnose install/sync）
**Focus**：80%+ test coverage、snapshot tests for output、offline fallback across all commands、bundle audit（target <2MB install）
**Estimated effort**：約 3 週

### v1.0 — First Stable

**Theme**：承諾 semver、擴展 distribution、enable plugins
**New commands (3)**：`chat`、`bookmark`、`plugin list/install`
**Distribution**：Homebrew formula（`brew install taiwanmd`）、Docker image（`ghcr.io/frank890417/taiwanmd`）、native binaries via `pkg`（macOS arm64/x64、Linux x64、Windows x64）、Raycast extension
**Estimated effort**：約 4 週
**Breaking changes**：lock CLI schema + JSON output contracts；publish `CLI_CONTRACT.md`

### v1.x — Ecosystem

- **v1.1**：Plugin ecosystem（`taiwanmd plugin install @taiwan-md/alumni`）— 第三方 subcommand discovery 類似 git
- **v1.2**：Obsidian sync（`taiwanmd obsidian link`）+ `snippet export` for AI-SEO bundles（Grokipedia-style）
- **v1.3**：`review <pr-url>` — PR review helper，跑 `audit` + `validate` on PR diffs
- **v1.4**：Alfred workflow、VS Code extension、Warp workflows pack

---

## New Commands Detail

### `taiwanmd audit <slug>` — **v0.6, highest priority**

**Purpose**：本地跑 Stage 3.5 Hallucination Audit。強制執行 幻覺鐵律 before PR
**Syntax**：

```
taiwanmd audit <slug> [--json] [--strict] [--fix-interactive]
```

**Output**：

```
Stage 3.5 Hallucination Audit — 珍珠奶茶

Phase 1: Claim Table
  23 factual claims extracted
  8 numeric claims · 4 name claims · 3 location claims · 2 quote claims

Phase 2: 5-Pattern Flags
  [1] Award hallucination        0 flags
  [2] Names + precise numbers    2 flags  ⚠
      - L43: "1988年春水堂劉漢介發明" — needs source
      - L112: "年銷售額達 120 億" — no citation
  [3] Location displacement      0 flags
  [4] Fabricated direct quotes   1 flag  ⚠
      - L87: direct quote attributed to 劉漢介 — unverified
  [5] Co-creator omission        0 flags

Phase 3: Verification Checklist
  [ ] Verify L43 via 中國時報 archive
  [ ] Verify L112 via 經濟部統計處
  [ ] Confirm L87 quote or downgrade to paraphrase

Phase 4: Subject Confirmation
  Contact subject or authoritative source before publishing.

Verdict: ⚠ 3 flags · do not merge until resolved
Exit: 1
```

**Deps**：reuse `lib/knowledge.js`；新增 `lib/audit.js` 含 regex+heuristic rules per pattern
**Effort**：約 5 天（rules are heuristic；subject-confirmation cycle 為 manual）

### `taiwanmd inbox` — **v0.6**

**Purpose**：顯示 ARTICLE-INBOX pending/blocked/in-progress 項目
**Syntax**：

```
taiwanmd inbox                        # default: show all states grouped
taiwanmd inbox --state pending
taiwanmd inbox claim <slug>           # lock as in-progress (adds your name)
taiwanmd inbox release <slug>         # release lock
taiwanmd inbox done <slug>            # move to ARTICLE-DONE-LOG
```

**Output**（plain）：

```
ARTICLE-INBOX (12 items)

PENDING (7)
  珍珠奶茶的國際化    · added 2026-04-15 · priority:high
  戰後台灣電影工業    · added 2026-04-18 · priority:med
  ...

IN-PROGRESS (3)
  台積電與半導體鏈    · claimed by CheYu 2026-04-19 · 2d

BLOCKED (2)
  二二八事件深度擴寫  · blocked: awaiting source confirmation
```

**Deps**：read/write `ARTICLE-INBOX.md` 和 `ARTICLE-DONE-LOG.md` at repo root
**Effort**：約 3 天

### `taiwanmd spore` — **v0.6**

**Purpose**：孢子（社群貼文）pipeline
**Syntax**：

```
taiwanmd spore new <slug>                # generate spore draft from article
taiwanmd spore new <slug> --platform threads,x
taiwanmd spore harvest <spore-id>        # pull d+N engagement from Threads + X
taiwanmd spore log                       # show SPORE-LOG
```

**Output**（`spore harvest`）：

```
Spore #2026-04-12-01 — 珍珠奶茶的國際化
Platform: Threads
Posted: 2026-04-12 18:00
d+7 harvest window

  Impressions   12,400
  Likes            184
  Reshares          23
  Replies           12
  CTR to article  1.8%  (224 clicks)

Logged to SPORE-LOG.md
```

**Deps**：Threads + X API tokens（read from `~/.taiwanmd/config.json` or env）
**Effort**：約 4 天

### `taiwanmd cite <topic>` — **v0.8**

**Purpose**：Anti-hallucination search — 回傳 verified claim + source URL 而非 generated sentence。補完 `rag`
**Syntax**：

```
taiwanmd cite "珍珠奶茶發明年份"
taiwanmd cite "台積電 3nm 產能" --json
```

**Output**：

```
Claim: 1988年，台中春水堂劉漢介發明珍珠奶茶
Source: knowledge/Food/珍珠奶茶.md L43
Citation: 劉漢介 口述, 中國時報 1998-03-15
Confidence: high (3 cross-sources)
Last-verified: 2025-11-20
```

**Deps**：reuse search index + 新的 claim-extraction layer（regex on `## 參考資料` + inline links）
**Effort**：約 5 天

### `taiwanmd organs` — **v0.8**

**Purpose**：把現在埋在 `stats` 裡的 8 organ health scores 浮現出來
**Syntax**：

```
taiwanmd organs              # colored bar chart
taiwanmd organs --json
taiwanmd organs --delta      # show day-over-day change
```

**Output**：

```
Organism vitals — 2026-04-20

  Knowledge    ████████░░  82  ↑2
  Heartbeat    ███████░░░  74  ↓1
  Sensory      ██████████  95  ↑5
  Immune       ███░░░░░░░  34  ↓8  ⚠
  Memory       █████████░  88  →
  Metabolic    ███████░░░  71  ↑3
  Reproductive ████████░░  80  ↑1
  Nervous      █████████░  89  ↑2

Overall: 76/100  (↑1 from yesterday)
```

**Deps**：`public/api/dashboard-organism.json`（已 sync）
**Effort**：約 2 天

### `taiwanmd heartbeat` — **v0.8**

**Purpose**：本地觸發 Semiont 4.5-beat cycle（等同 Muse 的 `heartbeat` skill）
**Syntax**：

```
taiwanmd heartbeat           # run full cycle
taiwanmd heartbeat --beat 2  # run single beat
taiwanmd heartbeat --dry-run
```

**Output**：stream 每個 beat 的進度；結尾寫入 `reports/heartbeat-YYYY-MM-DD.md`
**Deps**：reuse 現有 heartbeat scripts（likely `scripts/heartbeat/*.js`）
**Effort**：約 4 天（wrap 現有 scripts + progress stream）

### `taiwanmd supporters` — **v0.8**

**Purpose**：從 `data/supporters/transactions.json` 讀 Portaly 贊助資料
**Syntax**：

```
taiwanmd supporters                   # totals + recent
taiwanmd supporters --since 2026-04-01
taiwanmd supporters --json
```

**Output**：

```
Portaly Supporters — last 30d

Total:       47 transactions · NT$ 14,280
New donors:  12
Returning:   9
Top tier:    NT$ 2,000 × 2

Recent:
  2026-04-19  NT$ 500   一次性  anonymous
  2026-04-18  NT$ 200   月訂閱  supporter#0231
  ...
```

**Effort**：約 2 天

### `taiwanmd sense` — **v0.8**

**Purpose**：讀 GA4 / Search Console / Cloudflare sense data
**Syntax**：

```
taiwanmd sense                  # today's snapshot
taiwanmd sense --range 7d
taiwanmd sense --source ga4
```

**Output**：pageviews、top queries、top articles、referrers
**Deps**：`public/api/dashboard-analytics.json`
**Effort**：約 3 天

### `taiwanmd chat` — **v1.0**

**Purpose**：Interactive REPL 包 `rag` + `cite` + LLM backend
**Syntax**：

```
taiwanmd chat
> Tell me about 珍珠奶茶
[CLI assembles RAG context, sends to configured LLM, prints answer with citations]
```

**Deps**：user-configured LLM（OpenAI / Anthropic / Ollama local）。Never ships default key
**Effort**：約 5 天

### `taiwanmd upgrade` — **v0.9**

**Purpose**：從 npm self-update，preserving local config
**Effort**：約 1 天

### `taiwanmd doctor` — **v0.9**

**Purpose**：診斷 install、sync state、config、network reachability
**Effort**：約 2 天

### `taiwanmd bookmark` — **v1.0**

**Purpose**：Save + list + jump to favorite articles。儲存於 `~/.taiwanmd/bookmarks.json`
**Effort**：約 2 天

### `taiwanmd review <pr-url>` — **v1.3**

**Purpose**：PR review helper — fetch diff、run `audit` + `validate` on changed articles、post comment
**Deps**：`gh` CLI or GitHub API token
**Effort**：約 4 天

### `taiwanmd obsidian link|sync` — **v1.2**

**Purpose**：把 `knowledge/` mirror 到 Obsidian vault with wikilink rewriting
**Effort**：約 5 天

### `taiwanmd snippet export` — **v1.2**

**Purpose**：Export AI-SEO 優化 bundles（Grokipedia-style）— 一個 topic 一篇、pre-RAG'd、含結構化 claims
**Effort**：約 4 天

### `taiwanmd plugin list|install|uninstall` — **v1.1**

**Purpose**：Discover + load 第三方 subcommands from `~/.taiwanmd/plugins/`，使用 git-style `taiwanmd-<plugin>` binary lookup on PATH
**Effort**：約 4 天

---

## Architecture Evolution

### Phase A：MCP Server（v0.7）

加入 `taiwanmd mcp serve` using `@modelcontextprotocol/sdk`。暴露：

- `search(query, limit)`
- `read(slug, lang?)`
- `rag(query, limit)`
- `cite(topic)`
- `stats()`
- `organs()`

Claude Desktop config snippet（由 `taiwanmd mcp install` 產出）：

```json
{
  "mcpServers": {
    "taiwanmd": { "command": "taiwanmd", "args": ["mcp", "serve"] }
  }
}
```

**Why it matters**：Claude Desktop 使用者不用離開對話就能拿到台灣知識。2026 年 AI agent consumption 最低摩擦的 distribution channel。

### Phase B：Plugin Ecosystem（v1.1）

鏡像 git 的做法：任何 PATH 上名為 `taiwanmd-<name>` 的 binary 變成 subcommand。Core CLI shells out。`taiwanmd plugin list` scans PATH + `~/.taiwanmd/plugins/bin/`。

預期 first-party plugins：

- `taiwanmd-alumni` — 接收 alumni 故事投稿
- `taiwanmd-translate` — 批次翻譯到 en/ja
- `taiwanmd-archive` — Wayback Machine snapshot 所引用來源

### Phase C：Native Binaries + Brew（v1.0）

- Homebrew formula in `frank890417/homebrew-taiwanmd` tap，stable 後 submit to homebrew-core
- `pkg` 或 `nexe` 包 for macOS arm64/x64、Linux x64、Windows x64 — zero-dep install
- Docker image `ghcr.io/frank890417/taiwanmd:latest` for CI pipelines
- Raycast extension for macOS power users

### Offline-first（v0.9）

每個指令必須有 working offline mode。現在 `sync` 是 offline 的；`stats`、`organs`、`sense`、`supporters` 都依賴 sync'd dashboard JSON — 讓 sync 把它們包進來。`audit`、`cite` 完全 offline。`spore harvest`、`heartbeat` 需要 network（acceptable）。

### Auto-update（v0.9）

`taiwanmd upgrade` 跑 `npm install -g taiwanmd@latest`，preserve `~/.taiwanmd/config.json`。顯示 changelog snippet。

---

## Distribution

| Channel       | Version        | Command                                                       |
| ------------- | -------------- | ------------------------------------------------------------- |
| npm           | v0.5+（today） | `npm install -g taiwanmd`                                     |
| npx           | v0.5+（today） | `npx taiwanmd ...`                                            |
| Homebrew      | v1.0           | `brew install frank890417/taiwanmd/taiwanmd` → core           |
| Docker        | v1.0           | `docker run ghcr.io/frank890417/taiwanmd`                     |
| Native binary | v1.0           | GitHub release assets（darwin-arm64/x64、linux-x64、win-x64） |
| Raycast       | v1.0           | Raycast Store extension                                       |
| Alfred        | v1.4           | `.alfredworkflow`                                             |
| VS Code       | v1.4           | extension wrapping MCP                                        |
| Warp          | v1.4           | workflows pack                                                |

**Not planned**：pipx / Python rewrite（stack 維持 Node/JS — audience 已經為 Claude Code 有 Node）

---

## Testing Strategy

Current：zero tests。v0.9 target：80%+ statement coverage。

**Layers**：

1. **Unit** — `vitest` for pure functions in `lib/`（`knowledge.js`、`search.js`、`render.js`、新 `audit.js`、`claims.js`）
2. **Integration** — run 每個指令 against fixture knowledge base in `cli/test/fixtures/`。Network-dependent 指令用 `msw` 或 fs mocks stub
3. **Snapshot** — capture 每個指令 stdout with representative flags；`vitest` `toMatchSnapshot`。Catches accidental formatting regressions
4. **E2E** — CI only：real `sync`、real `search`、`rag` output 通過 `jq` schema check
5. **Regression** — dedicated suite for frontmatter parsing edge cases（malformed YAML、missing fields、unicode titles）

**CI**：GitHub Actions matrix Node 18/20/22、macOS + Linux。Smoke install test（`npm install -g .` then run 每指令 on fixtures）before publish。

**Seeded hallucination test set**：手工 curate 30 篇 articles with known-good + known-bad cases 用來追 `audit` precision/recall over time。Goal：precision ≥0.8、recall ≥0.7 at v1.0。

---

## Success Metrics

Track 每月 in `reports/cli-metrics-YYYY-MM.md`：

| Metric                                             | v0.6 target | v1.0 target |
| -------------------------------------------------- | ----------- | ----------- |
| npm weekly downloads                               | 200         | 2,000       |
| `sync` success rate                                | 95%         | 99%         |
| `audit` runs per week                              | 10          | 200         |
| Articles merged with `audit` in commit trailer     | 5/mo        | 40/mo       |
| MCP query volume（Claude Desktop）                 | n/a         | 5,000/week  |
| Contributor conversion（`contribute` → PR merged） | 20%         | 35%         |
| Issue P0/P1 open time                              | <7d         | <3d         |
| Fresh-install-to-first-query time                  | <60s        | <30s        |

**Leading indicators**：

- `audit` verdict distribution（rising clean-pass rate = contributors learning）
- `cite` miss rate（rising miss rate = knowledge gaps worth filling）
- `organs` health trend（rising Immune organ = fewer regressions）

---

## Risks & Open Questions

### Name collision

`taiwanmd` 在 npm 目前 unique。Homebrew 無 collision。**Open**：要不要保留 `@taiwan-md/cli` 當 scoped backup？

### Bundle size creep

Current install ~1.5MB。加 MCP SDK、`inquirer`、optional LLM clients 可能到 5MB+。**Mitigation**：lazy-require per command（只在 `contribute` 或 `inbox claim` 跑時 load `inquirer`）；任何 >1MB 的 plugin-ify。

### Offline sync reliability

git sparse-checkout 在 flaky networks 脆弱。**Mitigation**：加 cached tarball fallback（`https://taiwan.md/releases/knowledge-latest.tar.gz`）with SHA256 verification。

### MCP protocol stability

MCP 在 2026 仍在演化。**Mitigation**：pin SDK minor version；在 v0.7 release notes 標示「MCP preview」status；hold v1.0 MCP guarantee 直到 MCP 自己 ship 1.0。

### Breaking changes strategy

v1.0 起：strict semver。Structured outputs（`--json`）documented in `CLI_CONTRACT.md` with versioned schemas。任何 breaking change = major bump with 1-minor deprecation window。

### Hallucination audit false positives

`audit` 是 heuristic — 精確數字 without adjacent citations 即使正確也會 flag。**Mitigation**：`--strict` 預設 off；`--fix-interactive` 讓 contributor 加 inline `[verified:source]` markers 壓制未來 flags。

### SPORE-LOG privacy

Harvest data 含 per-user reshare/like counts。只儲存 aggregates；never persist individual user IDs to repo。

### Supporter data sensitivity

`transactions.json` 可能含 donor emails/names。`supporters` 指令必須 default scrub PII；`--raw` 需要 `--i-know-what-im-doing` flag。

### Test infra effort

Zero → 80% coverage 是 2–3 週 focused work。**Decision needed**：優先 v0.7 MCP 還是 v0.9 testing？Recommendation：testing first — broken MCP server erodes trust faster than missing one。

---

## Recommended Next Steps for CheYu

1. **Approve v0.6 scope** — 決定 `audit`、`inbox`、`spore` 是否在一個 v0.6 release 一起 ship 還是拆分（`audit` in v0.6、`inbox`+`spore` in v0.6.1）
2. **Seed the audit test corpus** — 30 篇 labeled clean/dirty articles 是 `audit` 品質的最高槓桿 asset。Can be drafted in a weekend from existing `knowledge/` + 故意 perturbed copies
3. **Reserve distribution names** — claim `homebrew-taiwanmd` tap repo、`ghcr.io/frank890417/taiwanmd`、`@taiwan-md/*` scoped npm org。5 分鐘 each，prevents squatting
4. **Write `CLI_CONTRACT.md` skeleton** — 即使 stub committing to stable `--json` schemas from v0.6 onward 也 sets expectations for AI-agent integrators
5. **Decide MCP vs testing order** — 見 Risks section；recommendation is testing first
6. **Run the `plan-eng-review` skill** on this roadmap before execution

---

_Author：Plan agent（ε session）_
_Persisted：main session via CheYu's request_
