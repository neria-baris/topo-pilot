# AUTHORSHIP_B: independent test author B (dry run and store records), X6ZC job 0120

**Protocol:** `tools/x6zc/PROTOCOL_X6ZC_v1.md` (sha256 2a711d16..., X6ZC-DESIGN-v1); contract `tools/x6zc/API.md` (80fd353a...), `tools/x6zc/CONTRACT.json` (54bacea8...), `tools/x6zc/TEST_PLAN.md` (bae45eba...); rulings R-0117-1..3 (`agent-handoff/jobs/0117/review.md`). Branch `x6zc-impl` at 4a14f39 when the work began.

**Author:** a clean-context Claude subagent launched by coordinator 8a9ab2e0 as "Author B" of job 0120. It shared no context with author A or with the implementer; it did not read author A's files.

**Assigned (task.md):** `tests/x6zc/test_x6zc_dryrun.py`: the §12 dry-run fixture table (every row's expected outcome), the report schema, the stage-1 store metadata no-write check, `EXPOSURE.jsonl` / `EVALUATIONS.jsonl`, the ledger and the 3x pause record.

## Read
- `agent-handoff/jobs/0120/task.md`, `agent-handoff/jobs/0117/review.md`.
- `tools/x6zc/TEST_PLAN.md`, `tools/x6zc/API.md`, `tools/x6zc/CONTRACT.json` (whole files).
- `tools/x6zc/PROTOCOL_X6ZC_v1.md`: §3.1-§5 and §8-§15 (the sections the fixtures and records depend on).
- Reused production code, read-only: `tools/x6_stage1/x6s1_pairs.py` (constants, `natural_prefixes`, `designed_*`, `q_*`), `tools/x6_stage1/x6s1_eval.py` (predictors, `qstar`, `quantise`, `score`, pair terms, `designed_stats`, `_clean`), `tools/x6_stage1/x6s1_stats.py` (`log_tables`, `quantile`, `boot_beta`, `qvals`), `tools/x6_stage1/x6s1_data.py` (constants, `init_state`), `tools/x6_stage0/x6_model.py` (constants, helpers, `parse`), `tools/x6_stage0/x6_exact.py` (`LOOPS`, witnesses), `src/topo_pilot/contracts/ids.py` (`SeedTree`, `canonical_json` signatures), `src/topo_pilot/learner/model.py` (the `TransformerLM` class line); `tests/x6_stage1/AUTHORSHIP_B.md` and the header of one X6S1 test, for format.

## Not read
- `tools/x6zc/*.py` (none existed; never listed, read or searched), author A's test files, any store (`x6-stage1-store`, `x6zc-store`), any X6S1 result or payload, `00_READ_ME_FIRST_*` and `docs/research_summary/`.

## Executed
- No project code, no pytest, no import of any project module, no formatter.
- Python was used only on the author's own file text from helper scripts under `X:/Downloads/topo-scratch/0120b/`: `ast.parse` + `compile` in memory, line count and line-length checks, and plain string replacements while shortening the file to 400 lines.

## Files
`test_x6zc_dryrun.py`: 400 lines, LF, lines <= 100 characters; 10 test functions (one parametrised over 9 planted fixtures: 18 test cases in all). No formatter was run over `tests/x6zc`.

## Notes
- Fixtures are synthetic only: a 4,096-row pool of random legal torus walks from `np.random.default_rng(2026102601)`, its D (`sp.designed_set`), fresh prefixes via `zc.fresh_prefixes`, n = 128 Stage-C prefixes, B = 500 draws (`zc.B_DRAWS` monkeypatched); pytest basetemps belong under `X:/Downloads/topo-scratch/<job>/`.
- Planted per-prefix factors f = 1 + u are centred over the prefix rows (u drawn on [-1/10, 1/10], |u| <= 1/5 after centring), so point values equal the exact protocol values; DR08 uses independent factors for w and pi so that the r_MM interval is not degenerate at the 1/2 bar.
- API ambiguities are listed in the job report to the coordinator. Corrections to this file are made only by this author.
