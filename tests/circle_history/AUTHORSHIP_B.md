# Authorship: independent test author B (job 0016)

These files were written by independent Claude test author B (model Claude Opus 5.5, `claude-opus-5-5`):

- `test_scores_precision.py`
- `test_scores_precision_gates.py`
- `test_error_bound.py`
- `test_adapter.py`
- `test_reference_binding.py`
- `test_reference_cache.py`
- `test_process_law.py`
- `test_controls.py`

The precision tests were split out of `test_scores_precision.py` to stay under the 400-line limit.

## Spec versions

The tests target spec v2.4 (commit 65792a0; ERROR_BOUND.md v2.2). Writing started from v2 (9d91cdf). The tests were then aligned to each later version:

- **v2.1** (2f4cbd4) and **v2.2** (6e525a7). The v2.2 delivery is committed unmodified at a9381ce.
- **v2.3** (0c11e9b). Only `test_error_bound.py` and `test_adapter.py` changed, adding the B10 scoring-authority cases.
- **v2.4** (65792a0). Four NEW files were added:
  - `test_reference_binding.py`: B11, the ERROR_BOUND v2.2 section 8 Taylor bounds, and certify_rows `moment_check_max_by_K`;
  - `test_reference_cache.py`: B12;
  - `test_process_law.py`: B13 and B14;
  - `test_controls.py`: B15 and B16.

  No earlier file was changed for v2.4, because no v2.3 expectation is contradicted by v2.4.

## What was read

- `tools/x4_circle_history/`: `API.md`, `CONTRACT.json`, `ERROR_BOUND.md` and `TEST_PLAN.md`. These were read in full at v2 and v2.1. Later versions were read as git diffs: v2.2, v2.3, and v2.4 (`git diff 0c11e9b..65792a0` restricted to these four files).
- `tools/x4_oracle_profile/API.md`.
- `tests/oracle_profile/independent_reference.py`.
- `src/topo_pilot/contracts/`: `README.md`, `SPEC.md`, `__init__.py`, `testing.py`, `store.py`, `schemas.py`, `base.py`, `ids.py`, `_schemas_data.py` and `_schemas_results.py`.
- For v2.4: `src/topo_pilot/dataset/sampler.py` (frozen project code, permitted by the coordinator; replicated in a test, not imported).
- `docs/CONVENTIONS.md` and `pyproject.toml`.
- The git history of this author's own test files and of this file.

## What was not read

- No production `.py` file under `tools/x4_circle_history/` or `tools/x4_oracle_profile/` was opened, listed, grepped or read. That includes `process_law.py` and `reference_cache.py`.
- Production and other-author file NAMES appeared only in `git diff --stat` / `git show --stat` summaries. No content of those files was viewed.
- No other worktree was read.
- No builder or author-A test file was opened.
- `test_reference_cache.py` hashes `tools/x4_circle_history/error_bound.py` at test run time (`source_identity`). The author never viewed that file.

## Execution

Nothing was executed: no pytest run and no test code run. The one exception is a mistaken shell command that started `python -` with an empty heredoc; it ran no code. No state-changing git command was used.
