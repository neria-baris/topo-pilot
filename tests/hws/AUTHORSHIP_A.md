# Authorship record: HWS independent tests, author A (job 0119)

**Author:** clean-context Claude subagent (author A), for coordinator Claude 8a9ab2e0, 2026-10-26.
**Files written:** `tests/hws/test_a_identities.py`, `test_a_stats.py`, `test_a_classify.py`,
`test_a_outcomes.py`, `test_a_budget.py` and this file. No other file was created or changed.

## Read
- `agent-handoff/jobs/0119/task.md`; `agent-handoff/jobs/0118/review.md` (rulings R-0118-1..6).
- `tools/hws/PROTOCOL_HWS_v1.md` (all), `tools/hws/API.md` (all), `tools/hws/TEST_PLAN.md` (all),
  `tools/hws/CONTRACT.json` (all sections except part of the `alias.maps` table).
- Reused production code (API.md §8), read-only: `tools/c1prime/c1_means.py`;
  `tools/k4b/k4b_scores.py` (phase and score functions); `tools/x4_circle_history/scores.py`
  (`unit_vectors`, `scores`, `r4_norms`, `sha256_phase`); `tools/x4_oracle_profile/oracle_profile.py`
  (kernels up to `bootstrap_profile`); `src/topo_pilot/oracle/_futures.py` (`context_gain`) and the
  `topo_pilot.oracle` export list; `src/topo_pilot/contracts/_schemas_world.py` (`WorldSpec`);
  `src/topo_pilot/world/lattice.py` (cylinder builder coordinates); `pyproject.toml` (pytest options).
- Directory listings only: `tests/` (folder names), `tests/k4b` (file names), `tests/hws` (file
  names; author B's files were seen by name and never opened).

## Not read
- `tools/hws/*.py`: never read, listed or searched (none existed when checked by `git status`).
- Author B's files (`tests/hws/test_b_*.py`, `AUTHORSHIP_B.md`).
- `00_READ_ME_FIRST*`, `docs/research_summary/`, any store, payload, history or scientific record.

## Executed
- No pytest, no import of project code, no sampling, no formatter.
- `X:/Downloads/topo-scratch/0119a/check_files.py` (own helper; stdlib only, run with
  `.venv/Scripts/python.exe -I`): `ast.parse` + `compile` of my own files in memory, and line
  counts, line lengths, CR and trailing-space checks. Run six times.
- Text edits of my own files: once `sed` (four literal replacements in `test_a_stats.py`) and once
  a stdin Python script using only `pathlib` string replacement (in `test_a_classify.py` and
  `test_a_identities.py`, to trim lines). Both touched only my own files and imported nothing from
  the project; recorded here because they go beyond the in-memory parse check.
- `git status`, `git log`, `git add <own files by name>`, `git commit`.

## Fixtures
- Synthetic only. The identities file writes its own rational HMM (6 x 2 cylinder, dyadic T and E,
  anchored (6, 2) labels with two axial symbols, L = 6) and enumerates all 4,096 histories with
  integers, Fractions and 40-digit Decimals. Decision fixtures are planted records labelled
  `"fixture": true`; their classes come from an independent §5.4 classifier in the test.
- No test needs `tmp_path`; nothing is written by author A's tests.
