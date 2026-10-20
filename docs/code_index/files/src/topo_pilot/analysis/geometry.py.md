# `src/topo_pilot/analysis/geometry.py`

- Source: [src/topo_pilot/analysis/geometry.py](../../../../../../src/topo_pilot/analysis/geometry.py)
- Kind: python
- Lines: 72

## Module docstring

> GeometryAlignment: the H2 measure Delta-geom (RESEARCH_SUMMARY 7.5).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 5, 6)
- `scipy` (lines 7)

### Standard library

- `__future__` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 9, import)

## Top-level constants

- `MIN_SAME_PAIRS`
- `_COMPONENT`

## Classes and functions

- **function `_rho`** [L15-16]: `def _rho(a: NDArray[np.float64], b: NDArray[np.float64]) -> float`
- **class `GeometryAlignment`** [L19-72] - Spearman alignment of activation distances with belief distances.
- **method `GeometryAlignment.delta_geom`** [L46-72]: `def delta_geom(self, D_A, D_B32, D_B1, last_symbol=None) -> dict` - Return ``{"all", "same_last_symbol", "n_same_pairs", "status_same"}``.

