# tests/x6_stage0: independence record (job 0058)

**Author:** an independent test author: a clean-context Claude Code subagent (general-purpose, agent id a52637b1adc1fdf6f), launched on 2026-10-17 by the worker session 3e84174c-98d1-400d-acea-7a15ee753836. It is a separate agent from the module author. It worked after the protocol was frozen (X6-FROZEN-v1, sha256 61DDA37B…B572) and after `tools/x6_stage0/API.md` was committed (af17d5e, sha256 f97e2064…8477), and before any module file existed (none existed at that commit or while it worked). It did not write, and will not write, the module. This record is written by the worker from the author's final report (§10.4: the worker records what was read, not read and executed).

**Files written by the author:**
- `tests/x6_stage0/test_x6_stage0.py`: 399 lines, 8 test functions (§10.4 tests 1–5, 9, 13, 14).
- `tests/x6_stage0/test_x6_stage0_dp.py`: 399 lines, 9 test functions (§10.4 tests 6–8, 10–12, 15–17). It imports reference helpers from `test_x6_stage0.py`.

One test function per §10.4 required test, 17 in all, each tagged with its number. No line exceeds 100 characters.

## What the author read

- `tools/x6_stage0/PROTOCOL_X6_v1.md`, lines 1–953 (§0–§10).
- `tools/x6_stage0/API.md`.
- `pyproject.toml`.
- `src/topo_pilot/world/`: `__init__.py`, `complex.py`, `registry.py`, `lattice.py`, `identification.py`.
- `src/topo_pilot/process/`: `__init__.py`, `transition.py`, `_geometry.py` (lines 40–69); `emission.py` by content search only.
- `tests/oracle_profile/independent_reference.py`.

## What the author did not read

- Any `tools/x6_stage0/*.py` file: never opened, listed, globbed or searched.
- Any other test directory, the git history, any store, report, transcript or log.

## What was executed

- By the author: nothing. No Python, pytest, shell, git or formatter; only file reads, writes and content searches.
- By the worker (job 0058): an in-memory syntax check only (`compile` of each file's source, plus an `ast` listing of the test functions and the maximum line length). The tests have never been run; PF runs them (job 0059). No formatter has been or may be run over `tests/x6_stage0`.

## Corrections

Corrections to a test file are made only by its author (§10.4).

- correction round 1 (2026-10-18): Decimal reference arithmetic moved into ≥80-digit localcontext in tests 04, 09 [+ 10, 11 in test_x6_stage0_dp.py]; read no module code. Module calls (`set_gap`, `block_comparator`, `kl_term`, `decimal_suffix_posterior`) stay outside the context; both files remain 400 lines, LF. Nothing executed.
- correction round 2 (2026-10-18): test_14 file set extended by x6_store.py per coordinator addendum 1 (X5); read no module code
- correction round 3 (2026-10-18): G5 reference error-key regression test (X7/D1); read no module code. Structural only (test_g5_reference_inputs_and_tolerances in test_x6_stage0_dp.py): API.md pins no Decimal-reference helper, its history input or its error-map keys, and `gate_G5(rows)` is expensive with unpinned `rows`/return keys; the test pins `gate_G5`'s signature, TOL_DEC/TOL_NUM/TOL_LOGEV, DIV_PREC/PRECS and the AB 120-digit (130-digit division) inputs. Compressed in place without changing assertion meaning; both files 400 lines, LF. Nothing executed.
