# `src/topo_pilot/analysis/x4f_targets.py`

- Source: [src/topo_pilot/analysis/x4f_targets.py](../../../../../../src/topo_pilot/analysis/x4f_targets.py)
- Kind: python
- Lines: 81

## Module docstring

> X4-F targets (part g; x4f-exec-v2 §2): belief circle expectations and calibration PCs.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 58, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L15-16]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `circle_expectation`** [L19-42]: `def circle_expectation(b: NDArray, x: NDArray, period: float) -> NDArray[np.float64]` - Belief expectation of the circle point of a lattice coordinate.
- **class `PCMap`** [L46-50] decorators: @dataclass(frozen=True, eq=False) - Calibration principal components: ``mean [q]``, ``components [q, c]`` (columns).
- **function `leading_components`** [L53-76]: `def leading_components(Z_cal: NDArray, n_components: int) -> PCMap` - Leading eigenvectors of the population covariance of ``Z_cal``.
- **function `pc_scores`** [L79-81]: `def pc_scores(Z: NDArray, pc: PCMap) -> NDArray[np.float64]` - ``(Z - pc.mean) @ pc.components`` -> ``[n, c]``.

