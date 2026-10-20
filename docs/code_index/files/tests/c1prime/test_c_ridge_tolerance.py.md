# `tests/c1prime/test_c_ridge_tolerance.py`

- Source: [tests/c1prime/test_c_ridge_tolerance.py](../../../../../tests/c1prime/test_c_ridge_tolerance.py)
- Kind: python
- Lines: 54

## Module docstring

> Coordinator regression test (job 0042 review, ruling R13): `c1_fit.equivalence_tolerance`
> is the M1 cho_solve-vs-lstsq tolerance max(1e-10, 64·ε·κ₂(Xc'Xc+λI)·‖pred‖∞). Synthetic only.

## Imports

### Internal (repo files)

- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 18, via sys.path edit)

### External (third-party)

- `numpy` (lines 9)
- `scipy` (lines 10)

### Standard library

- `__future__` (lines 4)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `_two_solvers`** [L21-26]: `def _two_solvers(F, Y, lam)`
- **test `test_well_conditioned_keeps_frozen_1e10`** [L29-35]: `def test_well_conditioned_keeps_frozen_1e10()`
- **test `test_ill_conditioned_solver_gap_is_within_bound`** [L38-46]: `def test_ill_conditioned_solver_gap_is_within_bound()`
- **test `test_implementation_mismatch_still_fails`** [L49-54]: `def test_implementation_mismatch_still_fails()`

