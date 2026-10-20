# `src/topo_pilot/oracle/_common.py`

- Source: [src/topo_pilot/oracle/_common.py](../../../../../../src/topo_pilot/oracle/_common.py)
- Kind: python
- Lines: 83

## Module docstring

> Shared validation helpers for the oracle kernels (no I/O).

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

- [src/topo_pilot/oracle/_filter.py](_filter.py.md) (line 12, import)
- [src/topo_pilot/oracle/_futures.py](_futures.py.md) (line 10, import)
- [src/topo_pilot/oracle/stage.py](stage.py.md) (line 22, import)

## Top-level constants

- `COMPONENT`
- `SUM_TOL`

## Classes and functions

- **function `fail`** [L14-16]: `def fail(code: ErrorCode, check: str, detail: str) -> StageFailure` - Build a ``StageFailure`` attributed to the oracle.
- **function `check_rows_sum_to_one`** [L19-23]: `def check_rows_sum_to_one(rows: NDArray[np.float64], check: str) -> None` - Raise ``NUMERICAL_FAILURE`` unless every last-axis sum is 1 within ``SUM_TOL``.
- **function `as_model`** [L26-48]: `def as_model(T: np.ndarray, E: np.ndarray, pi: np.ndarray | None) -> tuple` - Float64 copies of ``T [N,N]``, ``E [N,V]`` and ``pi [N]`` (or ``None``), shape-checked.
- **function `check_tokens`** [L51-67]: `def check_tokens(tokens: np.ndarray, n_symbols: int, max_len: int = 33) -> np.ndarray` - Return ``tokens`` as int64 ``[R, P]``; raise ``ALIGNMENT_ERROR`` if malformed.
- **function `normalise_rows`** [L70-83]: `def normalise_rows(unnorm: NDArray[np.float64], check: str) -> tuple` - Divide rows by their sums; return ``(rows, sums)``.

