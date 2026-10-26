# `tools/hws/hws_stats.py`

- Source: [tools/hws/hws_stats.py](../../../../../tools/hws/hws_stats.py)
- Kind: python
- Lines: 112

## Module docstring

> HWS statistics: means, SEs, bounds, z constants, bootstrap, E5, nulls (API.md §2).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 13, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 14, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 15, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 17, via unique basename)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 10)
- `math` (lines 9)
- `statistics` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_a_stats.py](../../tests/hws/test_a_stats.py.md) (line 24, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 20, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 20, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 21, import)
- [tools/hws/hws_records.py](hws_records.py.md) (line 22, import)
- [tools/hws/hws_select.py](hws_select.py.md) (line 14, import)

## Top-level constants

- `ALPHA_F`
- `DRAWS`
- `RANK_F`
- `Z1`
- `Z3`
- `Z975`
- `ZNULL`
- `ZW`
- `_Z`

## Classes and functions

- **function `z_of`** [L22-23]: `def z_of(alpha: Fraction) -> float`
- **function `_finite`** [L38-42]: `def _finite(x) -> np.ndarray`
- **function `summary`** [L45-49]: `def summary(x) -> dict`
- **function `screen_bounds`** [L52-55]: `def screen_bounds(x) -> dict`
- **function `s3_bounds`** [L58-65]: `def s3_bounds(x, boot) -> dict`
- **function `normal95`** [L68-69]: `def normal95(s) -> tuple`
- **function `bootstrap`** [L72-73]: `def bootstrap(arrays: dict, seed: int) -> dict`
- **function `null_z`** [L76-82]: `def null_z(x) -> dict`
- **function `e5`** [L85-104]: `def e5(m32) -> dict` - §2.5 on point values (choice 11): 95 % norm >= 0.2, 12 bins >= n/64, resultant <= 0.30.
- **function `pinsker_violations`** [L107-108]: `def pinsker_violations(slack, tol=1e-12) -> int`
- **function `entropy_diff`** [L111-112]: `def entropy_diff(ha, hb) -> dict`

