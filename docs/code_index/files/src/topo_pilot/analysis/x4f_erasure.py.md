# `src/topo_pilot/analysis/x4f_erasure.py`

- Source: [src/topo_pilot/analysis/x4f_erasure.py](../../../../../../src/topo_pilot/analysis/x4f_erasure.py)
- Kind: python
- Lines: 219

## Module docstring

> X4-F whitening, oblique linear erasure and matched random families (x4f-exec-v2 §5–§6).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 12, 13)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 9)
- `dataclasses` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 34, import)
- [tests/analysis/test_x4f_family_maintenance.py](../../../tests/analysis/test_x4f_family_maintenance.py.md) (line 6, import)

## Top-level constants

- `ERASER_INVALID`
- `FAMILY_UNMATCHED`
- `FEATURES_DEGENERATE`
- `OK`
- `RANK_EXCEEDS_RETAINED`
- `TARGET_UNCORRELATED`
- `TARGET_ZERO_VARIANCE`
- `ZERO_DISPLACEMENT`
- `_ZERO`

## Classes and functions

- **class `Whitening`** [L27-37] decorators: @dataclass(frozen=True, eq=False) - Retained-range whitening: ``W = diag(lam^-1/2) U_keep^T`` ``[k, d]``,
- **function `whiten`** [L40-59]: `def whiten(X: NDArray, floor: float = 1e-10) -> Whitening` - Whitening of ``X [n, d]`` on its retained eigen-range.
- **function `apply_map`** [L62-64]: `def apply_map(X: NDArray, mu: NDArray, M: NDArray) -> NDArray[np.float64]` - ``(X - mu) @ M.T + mu`` (column-action map on a batch of rows).
- **function `eraser_from_basis`** [L67-70]: `def eraser_from_basis(wh: Whitening, Q_s: NDArray) -> tuple[NDArray, NDArray]` - ``E = W_pinv Q_s Q_s^T W`` and ``M = I - E`` for orthonormal ``Q_s [k, r]``.
- **function `_rank`** [L73-75]: `def _rank(A: NDArray, tol: float) -> int`
- **class `Eraser`** [L79-87] decorators: @dataclass(frozen=True, eq=False) - Fitted eraser: ``M, E [d, d]``, ``mu [d]``, lost ``rank``, ``status`` and ``checks``.
- **function `fit_oblique_eraser`** [L90-131]: `def fit_oblique_eraser(X_cal: NDArray, Z_cal: NDArray, wh: Whitening, rank_tol: float = 1e-08, exact_tol: float = 1e-08, idem_tol: float = 1e-10) -> Eraser` - Continuous-target oblique linear eraser on the retained whitening range.
- **function `displacements`** [L134-136]: `def displacements(X: NDArray, X_prime: NDArray) -> NDArray[np.float64]` - Row-wise L2 norms of ``X_prime - X``.
- **class `Family`** [L140-149] decorators: @dataclass(frozen=True, eq=False) - Matched random family: accepted draw indices, maps and calibration mean displacements.
- **function `random_family`** [L152-206]: `def random_family(X_cal: NDArray, wh: Whitening, rank: int, target_mean_disp: float, rng_for: Callable[[int], np.random.Generator], n_accept: int = 20, max_draws: int = 10000, tol: float = 0.05, checkpoint: Callable[[str], None] = lambda _: None) -> Family` - Random rank-``rank`` erasers in the retained range, matched in mean displacement.
- **function `mismatch_report`** [L209-219]: `def mismatch_report(d_target: NDArray, d_other: NDArray, scale: float) -> dict` - Quantiles of ``d_other`` and per-history ratio ``|d_other - d_t| / d_t`` (rows with

