# Handoff: continuing with another model or session

The project must be resumable by a different model, vendor, or person using only the repository.

## 1. What carries state

| File | Rule |
|---|---|
| `state/PROGRESS.md` | **Overwritten** at the end of every work session and after every gate. At most 80 lines. Template below |
| `state/DECISIONS.md` | Append-only, one line per decision: `YYYY-MM-DD \| D-### \| decision \| reason \| ref` |
| `artifacts/` + RunManifests | Ground truth for what ran |
| git tags `E0..E4` | Reached exit points |

Nothing else is state. In particular, the following are **not** project state and are never stored in the repository:

- chat transcripts;
- agent reports;
- scratch notes.

## 2. PROGRESS.md template

```markdown
# Progress (updated YYYY-MM-DD by <model/person>)
Stage: S? | Wave: W? | Last exit reached: E?
## Modules
| module | status (todo/building/review/accepted) | owner tier | notes (≤10 words) |
## Gates
| gate | verdict | date | key value |
## Open issues (≤5)
## Next actions (≤5, concrete)
```

## 3. Start procedure for a new conductor

1. Read `ORCHESTRATOR_PROMPT.md` §1 (read order) and `state/PROGRESS.md`.
2. Sanity check:

   ```bash
   python -m pytest tests/contracts -q
   topo-pilot status
   ```

   `topo-pilot status` lists artifacts, gates, and runs.
3. If `PROGRESS.md` and `topo-pilot status` disagree, trust the artifacts. Rewrite `PROGRESS.md` and log the discrepancy in `DECISIONS.md`.
4. Continue the loop in `ORCHESTRATOR_PROMPT.md` §3.

## 4. Writing for portability

- Briefs, specs, and docs must be self-contained. They may not refer to "the earlier discussion".
- Model names appear only in the tier table, as examples. Instructions never depend on vendor-specific tools. If sub-agents are unavailable, the conductor executes the briefs itself, sequentially, while keeping the same file boundaries.
- Any non-obvious choice made during the build is captured in a module README (Logic section) or in `DECISIONS.md`, never only in a chat.
