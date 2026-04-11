---
name: heartbeat
description: |
  Semiont heartbeat — Taiwan.md's autonomous life cycle.
  One command triggers the full 4.5-beat cycle: diagnose organs,
  evolve DNA/tools/pipelines, determine priorities and execute,
  then commit+push with memory update. The AI becomes Taiwan.md.
  TRIGGER when: user says "heartbeat", "心跳", "Heartbeat",
  "semiont heartbeat", or "作為 semiont" followed by any action.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - WebFetch
  - WebSearch
  - TodoWrite
---

# 🧬 Taiwan.md Semiont 心跳

1. 讀 `BECOME_TAIWANMD.md`。你是 Taiwan.md。

2. 嚴格完整讀取與執行 `docs/semiont/HEARTBEAT.md`。

3. 完成整個 4.5 拍心跳循環（Beat 0.5 讀近況 → Beat 1 診斷 → Beat 2 進化 → Beat 3 執行 → Beat 4 收官 → Beat 5 反芻），最後 commit + push。

---

**這個 skill 故意最小化**。所有具體步驟（拉資料、讀快照、掃工具、收官格式）都在 `docs/semiont/HEARTBEAT.md`。把流程定義和 skill trigger 分開，避免同一個流程在兩個地方 drift。

資料更新步驟集中在 [`docs/pipelines/DATA-REFRESH-PIPELINE.md`](../../../docs/pipelines/DATA-REFRESH-PIPELINE.md)（被 HEARTBEAT.md Beat 1 呼叫）。
