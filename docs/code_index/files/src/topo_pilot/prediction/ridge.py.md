# `src/topo_pilot/prediction/ridge.py`

- Source: [src/topo_pilot/prediction/ridge.py](../../../../../../src/topo_pilot/prediction/ridge.py)
- Kind: python
- Lines: 85

## Module docstring

> Closed-form ridge probe (part c). Pure numpy.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/prediction/__init__.py](__init__.py.md) (line 5, import)
- [tests/c1prime/test_b_decoder.py](../../../tests/c1prime/test_b_decoder.py.md) (line 24, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../../tests/c2_readout/test_b_fwl_l1.py.md) (line 28, import)
- [tools/c1prime/c1_fit.py](../../../tools/c1prime/c1_fit.py.md) (line 15, import)
- [tools/c2_readout/c2_stats.py](../../../tools/c2_readout/c2_stats.py.md) (line 30, import)
- [tools/k4b/k4b_decoder.py](../../../tools/k4b/k4b_decoder.py.md) (line 17, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_as2d`** [L15-17]: `def _as2d(a: np.ndarray) -> NDArray[np.float64]`
- **class `RidgeProbe`** [L20-85] - Affine ridge regression ``Y ~ X W + b`` with an unpenalised intercept.
- **method `RidgeProbe.__init__`** [L40-46]: `def __init__(self, lambdas: Sequence[float]) -> None`
- **method `RidgeProbe._solve`** [L49-51]: `def _solve(Xc: NDArray[np.float64], Yc: NDArray[np.float64], lam: float) -> NDArray[np.float64]` decorators: @staticmethod
- **method `RidgeProbe.fit`** [L53-70]: `def fit(self, X_fit: np.ndarray, Y_fit: np.ndarray, X_val: np.ndarray, Y_val: np.ndarray, splits: tuple[str, str] = ('dev_fit', 'dev_val')) -> RidgeProbe` - Fit on the fit rows for every lambda; keep the lambda with least validation MSE.
- **method `RidgeProbe.predict`** [L72-76]: `def predict(self, X: np.ndarray) -> np.ndarray` - Affine prediction ``[n, k]``.
- **method `RidgeProbe.score`** [L78-85]: `def score(self, X: np.ndarray, Y: np.ndarray) -> dict[str, float]` - Return ``{"mse": ..., "r2": ...}`` (no KL on raw ridge output).

