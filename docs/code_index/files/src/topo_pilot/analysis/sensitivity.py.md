# `src/topo_pilot/analysis/sensitivity.py`

- Source: [src/topo_pilot/analysis/sensitivity.py](../../../../../../src/topo_pilot/analysis/sensitivity.py)
- Kind: python
- Lines: 92

## Module docstring

> Part (c) sensitivity variants: alternative distance matrices for S7 (pure, float64).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.topology import Chord, DistancePipeline, Euclidean, Hellinger, SqrtJS` -> [src/topo_pilot/topology/__init__.py](../topology/__init__.py.md) (line 9, via package root)

### External (third-party)

- `numpy` (lines 5, 6)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 31, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L14-15]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `_matrix`** [L18-25]: `def _matrix(a: object, name: str) -> NDArray[np.float64]`
- **class `Sensitivity`** [L28-92] - Distance-matrix variants for the one-factor-at-a-time sensitivity stage (S7).
- **method `Sensitivity.activation_D`** [L58-77]: `def activation_D(self, X: NDArray, variant: str, X_fit: NDArray | None = None, pca_dims: int = 32) -> NDArray[np.float64]` - Distance matrix of activation rows under ``variant`` (see class docstring).
- **method `Sensitivity.distribution_D`** [L79-85]: `def distribution_D(self, P: NDArray, variant: str) -> NDArray[np.float64]` - Distance matrix of distribution rows under ``variant`` (Hellinger or sqrt-JS).
- **method `Sensitivity.head`** [L88-92]: `def head(n: int, k: int) -> NDArray[np.int64]` decorators: @staticmethod - The first ``k`` row indices ``arange(k)`` of ``n`` rows; ``1 <= k <= n``.

