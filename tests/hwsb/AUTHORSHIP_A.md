# Authorship record: HWSB test author A (job 0161)

**Author:** a clean-context Claude subagent (test author A) of coordinator db858736, 2026-10-27.
Worktree `X:/Downloads/projects/topo-pilot/topo-pilot-hws`, branch `hwsb-impl`, spec commit 8407a76.

## Files written

`tests/hwsb/test_a_learning.py`, `test_a_endpoints.py`, `test_a_ladder.py`, `test_a_capture.py`,
`test_a_outcomes.py`, `test_a_enclosure_proof.py` (TEST_PLAN §2, DRB5, DRB8, DRB9, DRB10, DRB11,
DRB12), and this file.

## What was read

- Job: `agent-handoff/jobs/0161/task.md`, `agent-handoff/jobs/0161/rulings-phase1.md`.
- Spec: `tools/hwsb/PROTOCOL_HWSB_v1.md` (whole), `tools/hwsb/API.md` (whole),
  `tools/hwsb/TEST_PLAN.md` (whole), `tools/hwsb/CONTRACT.json` (sections `thresholds`,
  `licences`, `handoff`, `outcomes`, `cpu`, `annotations`, `law`, `seeds`, `masters`,
  `dry_masters`, `sizes`, `world`, `tests`, `number_format`, `modules`; key list of the rest).
- Reused modules (source, read for their public behaviour): `tools/k4b/k4b_stats.py`,
  `tools/c1prime/c1_means.py`, `tools/x4_circle_history/precision.py`,
  `tools/k4b/k4b_config.py` (lines 1-70 and the constant names), `tools/k4b/k4b_cert.py`
  (`F_plan` and imports), `tools/hws/hws_oracle.py` (lines 1-100), `tools/k4b/k4b_scores.py`,
  `src/topo_pilot/prediction/metrics.py`, `tools/x4_circle_history/process_law.py`
  (lines 1-140), `tools/x4_circle_history/error_bound.py` (`trapping_context`, `u_digits`,
  imports), `tools/x4_circle_history/errors.py` (lines 1-30), the function signatures of
  `tools/x4_circle_history/scores.py` (grep), and the sys.path lines of `tools/hws/hws_worlds.py`.
- An existing test of another study, for the import pattern only: the first 80 lines of
  `tests/k4b/test_a_ranks_ladder.py`.
- `pyproject.toml` (pytest options).

## What was not read

- No `tools/hwsb/*.py` file was opened, read or searched, and no `tests/hwsb/test_b_*` file.
  (A `git status` before committing printed the names of untracked `tools/hwsb/*.py` files; their
  content was not looked at.) `tools/hwsb/ENCLOSURE_PROOF.md` was not read; one test checks at run
  time that it exists and names δ and rounding.
- No store, payload, `state.pt`, `sealed/` or `hist/` file; no public research-summary path.

## How the tests were run

`X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s -m pytest tests/hwsb/test_a_*.py -p no:cacheprovider --basetemp X:/Downloads/topo-scratch/test_hwsb-0161/A/pytest`
with `PYTHONPATH=<worktree>/src` and TEMP/TMP under `X:/Downloads/topo-scratch/test_hwsb-0161/A/tmp`.
No `.npz` or `.npy` file is written by these tests. No formatter was run.

## Assumptions marked in the tests

- `# API-AMBIGUITY` (test_a_endpoints): `b4_status` may read `cal["status"][j]` or
  `cal["per_model"][j]["status"]`; both are planted consistently.
- `# API-AMBIGUITY` (test_a_capture): `b5`'s `sdU_minus` may be keyed by `j` or by `(j, "-")`;
  the planted map carries both.
- `# API-AMBIGUITY` (test_a_outcomes): `licence` fills `{models}` from `oc["models"]`; both
  `str(list)` and a joined rendering are accepted.
