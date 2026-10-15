# Dual-track planning protocol (owner instruction, 2026-10-14 ~21:00Z)

**Owner instruction:** every planning task runs twice, independently: once by Codex and once by Claude here. The coordinator then extracts lessons and merges the two into one plan here. Execution stays with the coordinator.

## Tracks

| Track | Who | How it runs | Where it writes |
|---|---|---|---|
| **X (Codex)** | Codex CLI, headless, **read-only sandbox** | Launched by the coordinator in the background: `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high" -C <repo> -s read-only --json -o responses/<id>.codex.md -` (owner: sol 6.1, high reasoning), with stdin = `codex_preamble.md` + `requests/<id>.md`. (Owner's permission layer refused a write-enabled, no-approval launcher on 2026-10-14; read-only is the approved safer form.) | Nothing on disk itself. Its final message (the full plan) is saved by the CLI to `responses/<id>.codex.md`, and the coordinator commits it. |
| **L (Claude)** | Clean-context Claude subagent spawned by the coordinator | Same request text. It never sees track X output from the same round. | its own worktree `topo-pilot-planning-claude`, plus `responses/<id>.claude.md` |
| **M (merge)** | Coordinator | Diffs X and L, writes `responses/<id>.MERGE.md`: lessons, agreements, conflicts, the decision on each conflict, and what each track caught that the other missed. Commits the merged plan on the merge branch. | worktree `topo-pilot-planning-merged` |

## Rules

1. **Identical inputs.** Both tracks get the same request file (`requests/<id>.md`, with its SHA256) and the same base commit. Earlier merged documents may be shared inputs.
2. **Independence within a round.** Neither track reads the other's output for the same `<id>`.
3. **Committing.** The coordinator commits each track's files on its own branch (`planning-codex-<id>`, `planning-claude-<id>`), so provenance is kept and nothing is overwritten.
4. **Review before freeze.** A merged protocol that is meant for freeze needs a third, clean-context, result-blind review before any freeze.
5. **Codex unavailable.** This covers a non-zero exit, a credit or rate error, or more than 60 minutes. Track L proceeds alone and the merge note records `Codex unavailable` with the exit code and log.
6. **Scope.** Planning only. No scientific payload access, sampling, training or tests in either track.
7. **Log.** Every Codex run keeps `responses/<id>.codex.jsonl` (event log), `responses/<id>.codex.meta.json` (start, end, exit code, command) and the session id, so the coordinator can `codex exec resume` for follow-ups.
