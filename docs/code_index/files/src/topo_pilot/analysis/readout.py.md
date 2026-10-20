# `src/topo_pilot/analysis/readout.py`

- Source: [src/topo_pilot/analysis/readout.py](../../../../../../src/topo_pilot/analysis/readout.py)
- Kind: python
- Lines: 178

## Module docstring

> Readout-geometry helpers (part d): gauge-free LayerNorm, readout projector, exact split.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from .pointset import PointSet` -> [src/topo_pilot/analysis/pointset.py](pointset.py.md) (line 12, via relative)

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

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 30, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L17-18]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `_as_f64`** [L21-26]: `def _as_f64(a: object, name: str, ndim: int) -> NDArray[np.float64]`
- **function `_require_finite`** [L29-31]: `def _require_finite(arr: NDArray[np.float64], name: str) -> None`
- **function `ln_gauge_free`** [L34-69]: `def ln_gauge_free(Z: NDArray, eps: float = 1e-05) -> NDArray[np.float64]` - LayerNorm without its affine part, applied row-wise.
- **function `readout_projector`** [L72-113]: `def readout_projector(gamma: NDArray, W_U: NDArray, rtol: float | None = None) -> NDArray[np.float64]` - Orthogonal projector onto the column space of the readout map ``A``.
- **function `split_readout`** [L116-144]: `def split_readout(U: NDArray, P: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]` - Split row-vectors into the readout-visible part and the null part.
- **function `predictive_pointset`** [L147-178]: `def predictive_pointset(logits: NDArray, ids: Sequence[str], space: str = 'pred:softmax') -> PointSet` - Predictive distributions of a model as a Hellinger point set.

