# tests/d1_seam: independence record (job 0019)

**Author:** independent test author (a Claude Code subagent), 2026-10-15. I did not write the module.

**File written:** `tests/d1_seam/test_d1_seam.py` (399 lines, 21 test functions, 32 collected tests).

## What I read

- `agent-handoff/planning/responses/D1-FROZEN-v1.md`, all 975 lines. This is the authoritative protocol.
- `agent-handoff/planning/responses/D1-FROZEN-v1.coordinator-addendum.md`.
- `topo-pilot-d1/tools/d1_seam/API.md`, the written contract.
- Production code and the reference that the tests call:
  - `src/topo_pilot/world/__init__.py`, `registry.py`, `lattice.py` and `config.py`;
  - `src/topo_pilot/process/transition.py` and `_geometry.py`;
  - `src/topo_pilot/oracle/__init__.py`;
  - `tests/oracle_profile/independent_reference.py`;
  - `tests/oracle_profile/test_oracle_profile.py`, for its sys.path import pattern;
  - `pyproject.toml`.

## What I did not read

- `tools/d1_seam/d1_seam.py`. I never opened, listed or grepped it. I read no file under `tools/d1_seam/` except `API.md`.
- No other test directory, and no other file under `src/`: for example `world/complex.py`, `world/metrics.py`, `oracle/_filter.py` and `oracle/_futures.py`.
- No git history, no report, and no output store.

## What I executed

Nothing. I ran no Python, no pytest and no shell command that runs code, and no state-changing git command. My only tools were file reads, file writes and content searches, which I used to check line lengths and the line count. The tests have never been run.

## Independence of the exact reference

The `ref_*` functions in the test file are written from the protocol's equations. They cover:
- the 4×3 lattice with the C and M seams (§2.1);
- T with a = 1/5 per neighbour and 1 − deg/5 on the diagonal (§2.2);
- the literal E (§2.4) and the start law μ (§2.5);
- the control variants (§5.2 G6);
- a Fraction forward filter, Q1 = bTE, and J[v][u] = bT·diag(E[:, v])·T·E[:, u].

They import nothing from `d1_seam`. Module outputs are only compared against them.
