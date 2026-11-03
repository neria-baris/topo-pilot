# `tools/hwsg/hwsg_ratio.py`

- Source: [tools/hwsg/hwsg_ratio.py](../../../../../tools/hwsg/hwsg_ratio.py)
- Kind: python
- Lines: 81

## Module docstring

> HWSG capture ratio rho = X- / Delta4_orc with its joint bootstrap (API.md §7; N1, N7).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 8, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 9, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 10, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 12, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 13, via unique basename)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 3)
- `pathlib` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsg/test_a_ratio.py](../../tests/hwsg/test_a_ratio.py.md) (line 24, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 10, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 8, import)

## Top-level constants

- `D_KEY`
- `NUM`
- `UNRESOLVED`

## Classes and functions

- **function `draws`** [L20-21]: `def draws(arrays, controls, seed) -> dict`
- **function `ratio_draws`** [L24-28]: `def ratio_draws(dr, j) -> dict`
- **function `_tm`** [L31-32]: `def _tm(x) -> float`
- **function `model_ratio`** [L35-45]: `def model_ratio(dr, j, point_minus, point_D) -> dict`
- **function `_lu`** [L48-49]: `def _lu(v)`
- **function `ratio_gate`** [L52-81]: `def ratio_gate(ctx, result, world_b4_pass, seed, out=None) -> dict`

