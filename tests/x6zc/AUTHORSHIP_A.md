# Authorship record: X6ZC independent tests, author A (job 0120)

**Author:** Claude subagent (clean context), independent test author A for coordinator Claude
8a9ab2e0, 2026-10-26. Not the implementer.
**Files:** `tests/x6zc/test_x6zc_core.py` (TEST_PLAN.md §2) and `tests/x6zc/test_x6zc_decide.py`
(TEST_PLAN.md §3). Worktree `topo-pilot-x6zc`, branch `x6zc-impl`, base 4a14f39.

## Read
- `tools/x6zc/PROTOCOL_X6ZC_v1.md` (whole), `tools/x6zc/API.md` (whole),
  `tools/x6zc/TEST_PLAN.md` (whole), `tools/x6zc/CONTRACT.json` (constants, thresholds, budget,
  store, outcomes, licences, not_licensed, x6s1_statement, reuse; the key outline of the rest).
- `agent-handoff/jobs/0120/task.md`, `agent-handoff/jobs/0117/review.md`.
- Reused production code, read-only: `tools/x6_stage0/x6_model.py` (whole),
  `tools/x6_stage0/x6_exact.py` (lines 60-299), `tools/x6_stage1/x6s1_pairs.py` (whole),
  `tools/x6_stage1/x6s1_eval.py` (lines 1-310), `tools/x6_stage1/x6s1_stats.py` (lines 130-169),
  `tools/x6_stage1/x6s1_data.py` (import header and constants, lines 1-110),
  `src/topo_pilot/contracts/ids.py` (`SeedTree`, `canonical_json` signatures).
- For style and lint conventions only: `pyproject.toml` (ruff section) and lines 1-90 of
  `tests/x6_stage1/test_a_designed.py` (an X6S1 author-A test; no X6S1 or X6ZC result in it).
  These two are outside the task's source list; recorded here for completeness.

## Not read
- Any `tools/x6zc/*.py` (never read, listed or searched; none existed at 4a14f39).
- Any store (`x6-stage1-store`, `x6zc-store`) or payload; any X6S1 or X6ZC result.
- `00_READ_ME_FIRST_*`, `docs/research_summary/`.
- Author B's files (`test_x6zc_dryrun.py`, `AUTHORSHIP_B.md`).

## Executed
- No pytest, no import of project code, no model, oracle or store access.
- `X:/Downloads/topo-scratch/0120a/check_syntax.py` run with the venv interpreter in isolated
  mode (`-I -S`): reads the two test files as text, `ast.parse` + `compile` in memory, and
  checks LF endings, line count (≤ 400) and line width (≤ 100). Nothing imported or executed.
- `X:/Downloads/topo-scratch/0120a/edit_*.py` (same interpreter, `-I -S`): plain string
  replacement inside my own test files while shortening them to 400 lines.
- Shell text tools (`git log/status`, `wc`, `sed`, `grep`, `ls tests`) over the files above.
- No formatter was run.

## Expected values
Protocol closed forms (§3.1, §6 K0-K3, §7 B9, §9, §13) and TEST_PLAN values; exact Fractions
recomputed in the tests through the reused stage-0 / X6S1 code (`sp.q_exact`, `xm.holonomy`,
`xm.parse`, `ss.boot_beta`, `ss.quantile`, `se.pair_terms`, `se.beta_fsum`). Fixtures are
synthetic: short token tuples and a 4,096-row random-walk pool from `np.random.default_rng`.
