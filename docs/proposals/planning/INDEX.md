# Planning records: index

**What this is.** Byte-for-byte copies of the dual-track planning records: Codex track, Claude track, merge, independent review and freeze. They were imported in job 0022 from the mailbox git repository `agent-handoff` at commit **52cb2c0c73995bc1e633146a0a0b1ac8250db3f8**, directory `planning/`. Job 0024 added 10 files from mailbox commit **ccde1bd0defbbccd597ad3216e695f4ec441c19e**. They are documents only: no code, no results. Every file's sha256 equals its mailbox source.

**Layout.** The paths below mirror the mailbox: `requests/` holds what a round asked, and `responses/` holds the track answers, merges, reviews and frozen protocols.

| # | Round / topic | Status | Files (under this directory) |
|---|---|---|---|
| 1 | Dual-track planning process | process document | `PLANNING_PROTOCOL.md`, `codex_preamble.md` |
| 2 | Round 1: C1 causal use, freeze-readiness | MERGED (superseded by the C1 versions) | `requests/coord-c1-freeze-readiness-20261014.*`; `responses/coord-c1-freeze-readiness-20261014.{codex,claude,MERGE_ANALYSIS,MERGE}.md` and `.tracks.sha256`; `responses/owner-causal-protocol-c1-20261014.*` |
| 3 | C1 merged versions and independent reviews | MERGED, then frozen as row 5 | `responses/C1-MERGED-v1…v4` (with `.changes.md` and the v1 `.sha256`); `requests/coord-c1-merged-review-20261015.*`; `responses/coord-c1-merged-review-20261015.{codex,v3confirm.codex,v4confirm.codex}.md`; `responses/c1-v3-rulings.md` |
| 4 | Round 3: C1 numerical certificate | MERGED into C1 | `requests/coord-c1-numcert-20261015.*`; `responses/coord-c1-numcert-20261015.{codex,claude,MERGE}.md` and `.tracks.sha256` |
| 5 | **C1-FROZEN-v1** (causal use) | **FROZEN**; data stages BLOCKED under its own freeze, because K4 closed INCONCLUSIVE at chart_calibration (state D-078; the coordinator's job-0018 review) | `responses/C1-FROZEN-v1.md`, `.sha256` |
| 6 | Round 2: D-1 oracle proof, merged versions and reviews | MERGED, then frozen as row 7 | `requests/coord-d1-oracle-proof-20261015.*`; `responses/coord-d1-oracle-proof-20261015.{codex,claude,MERGE_ANALYSIS,MERGE}.md`; `responses/D1-MERGED-v1` (with `.sha256`) and `-v2` (with `.changes.md`); `requests/coord-d1-merged-review-20261015.md`; `responses/coord-d1-merged-review-20261015.{codex,confirm.codex}.md` |
| 7 | **D1-FROZEN-v1** (oracle-only horizon gap) | **FROZEN**; executed PASS (jobs 0019–0020, state D-079–080) | `responses/D1-FROZEN-v1.md`, `.sha256`, `.coordinator-addendum.md`, `.coordinator-addendum-2.md` |
| 8 | Chart redesign (after the K4 INCONCLUSIVE) | **DECIDED** (owner A); the geometry-only diagnostic CHART-DIAG-FROZEN-v1 gave **GO** (job 0023). K4 stays INCONCLUSIVE | `requests/coord-chart-redesign-20261015.*`; `responses/coord-chart-redesign-20261015.{codex,claude,MERGE}.md`; `responses/CHART-DIAG-FROZEN-v1.md`, `.sha256` |
| 9 | X2a stage 0 | **IN REVIEW**: X2A-MERGED-v1 under independent review | `requests/coord-x2a-stage0-20261015.*`; `responses/coord-x2a-stage0-20261015.{codex,claude,MERGE_ANALYSIS,MERGE}.md`; `responses/X2A-MERGED-v1.md`, `.sha256`; `requests/coord-x2a-merged-review-20261015.md`; `responses/coord-x2a-merged-review-20261015.codex.md` |
| 10 | D-2: trained lengths | **IN PLANNING** (request only) | `requests/coord-d2-trained-lengths-20261015.md`, `.sha256` |
| 11 | C1′ protocol delta (chart rule LCC ≥ 95% on C1's own fresh histories) | **IN PLANNING** (request only) | `requests/coord-c1prime-delta-20261015.md`, `.sha256` |

**Related drafts, cherry-picked with their original authorship and dates (job 0022):**
- `docs/proposals/CAUSAL_CIRCLE_STATE_FORCING_PROTOCOL_DRAFT.md`, from fc2c107: Codex's original C1 draft, branch planning-causal-state-forcing-20261014.
- `docs/proposals/X6_NONABELIAN_HOLONOMY_PROTOCOL_DRAFT.md`, from a881300: the X6 draft by another Claude window, branch x4-circle-k4-feas-0015.
  - That draft's uncommitted later modification, in the topo-pilot-x4b worktree, belongs to that window and is not included.

**Not imported:**
- CLI log files stay in the mailbox repository: `*.codex.jsonl`, `*.stderr.log`, `*.codex.prompt.md`, `*.exit` and `*.start`. There were 36 at job 0022 and 46 at job 0024.
- `planning/drafts/d1-oracle-check.task.md`, a draft task text that the import task does not list, also stays in the mailbox.
- `responses/X2A-MERGED-v2.md` is not listed by job 0024. At copy time it had uncommitted modifications in the mailbox, so it is still being written.

Counts:
- Job 0022: 98 files in the mailbox `planning/` = 61 imported + 36 logs + 1 draft task.
- Job 0024: 119 files = 71 imported + 46 logs + 1 draft task + `X2A-MERGED-v2.md`.
