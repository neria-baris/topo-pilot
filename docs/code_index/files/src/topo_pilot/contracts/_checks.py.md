# `src/topo_pilot/contracts/_checks.py`

- Source: [src/topo_pilot/contracts/_checks.py](../../../../../../src/topo_pilot/contracts/_checks.py)
- Kind: python
- Lines: 97

## Module docstring

> Small pure validation helpers shared by the schema classes (internal).

## Imports

### Internal (repo files)

- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 9, via relative)

### External (third-party)

- `numpy` (lines 7)

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

- [src/topo_pilot/contracts/_schemas_data.py](_schemas_data.py.md) (line 11, import)
- [src/topo_pilot/contracts/_schemas_results.py](_schemas_results.py.md) (line 12, import)
- [src/topo_pilot/contracts/_schemas_world.py](_schemas_world.py.md) (line 11, import)

## Top-level constants

- none

## Classes and functions

- **function `fail`** [L12-14]: `def fail(owner: str, code: ErrorCode, check: str, detail: str) -> StageFailure` - Build a ``StageFailure`` attributed to ``contracts.<owner>``.
- **function `require_array`** [L17-23]: `def require_array(owner: str, name: str, arr: object, ndim: int, kinds: str = 'iuf', code: ErrorCode = ErrorCode.ALIGNMENT_ERROR) -> np.ndarray` - Require a numpy array of the given rank whose dtype kind is in ``kinds``.
- **function `require_dtype`** [L26-30]: `def require_dtype(owner: str, name: str, arr: np.ndarray, dtypes: Sequence[str]) -> None` - Require ``arr.dtype`` to be one of ``dtypes`` (numpy dtype names).
- **function `require_len`** [L33-37]: `def require_len(owner: str, name: str, arr: np.ndarray, n: int) -> None` - Require ``arr.shape[0] == n``.
- **function `require_finite`** [L40-44]: `def require_finite(owner: str, name: str, arr: np.ndarray) -> None` - Require every entry to be finite.
- **function `require_distribution_rows`** [L47-57]: `def require_distribution_rows(owner: str, name: str, P: np.ndarray, tol: float, code: ErrorCode = ErrorCode.NUMERICAL_FAILURE) -> None` - Require nonnegative finite rows summing to 1 (over the last axis, or the last two for
- **function `require_permutation`** [L60-65]: `def require_permutation(owner: str, name: str, perm: np.ndarray, n: int) -> None` - Require ``perm`` to be an integer permutation of ``0..n-1``.
- **function `require_unique`** [L68-71]: `def require_unique(owner: str, name: str, values: np.ndarray, code: ErrorCode) -> None` - Require all entries of a 1-d array to be distinct.
- **function `require_metric_matrix`** [L74-97]: `def require_metric_matrix(owner: str, name: str, D: np.ndarray, tol: float = 1e-09, triangle: bool = True, positive: bool = False) -> None` - Require a finite symmetric matrix with zero diagonal, nonnegative entries and, optionally,

