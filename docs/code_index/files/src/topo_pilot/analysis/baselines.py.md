# `src/topo_pilot/analysis/baselines.py`

- Source: [src/topo_pilot/analysis/baselines.py](../../../../../../src/topo_pilot/analysis/baselines.py)
- Kind: python
- Lines: 61

## Module docstring

> Process-level representation baselines R2 / R3: spectral embedding of the symbol kernel.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/analysis/spaces.py](spaces.py.md) (line 23, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L13-14]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `spectral_embedding`** [L17-49]: `def spectral_embedding(E: NDArray[np.float64], T: NDArray[np.float64], pi: NDArray[np.float64], k: int) -> NDArray[np.float64]` - Spectral embedding phi of the symbol transition matrix.
- **function `r2_points`** [L52-55]: `def r2_points(tokens_hist: NDArray, phi: NDArray[np.float64]) -> NDArray[np.float64]` - R2 = ``1/2 [phi(w_32) + phi(w_31)]`` for ``tokens_hist: [M, 32]`` -> ``[M, k]``.
- **function `r3_points`** [L58-61]: `def r3_points(tokens_hist: NDArray, phi: NDArray[np.float64]) -> NDArray[np.float64]` - R3 = ``mean_t phi(w_t)`` over the history tokens -> ``[M, k]``.

