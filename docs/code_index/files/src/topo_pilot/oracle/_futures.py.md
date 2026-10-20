# `src/topo_pilot/oracle/_futures.py`

- Source: [src/topo_pilot/oracle/_futures.py](../../../../../../src/topo_pilot/oracle/_futures.py)
- Kind: python
- Lines: 107

## Module docstring

> Futures, observability and context gain (pure kernels).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)
- `from ._common import as_model, check_rows_sum_to_one, fail` -> [src/topo_pilot/oracle/_common.py](_common.py.md) (line 10, via relative)

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

- [src/topo_pilot/oracle/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/oracle/stage.py](stage.py.md) (line 24, import)

## Top-level constants

- `_BELIEF_TOL`

## Classes and functions

- **class `FutureOperator`** [L15-77] - Exact one- and two-step futures from a belief ``b`` and the observability spectrum.
- **method `FutureOperator.__init__`** [L35-37]: `def __init__(self, T: np.ndarray, E: np.ndarray) -> None`
- **method `FutureOperator._beliefs`** [L39-45]: `def _beliefs(self, b: np.ndarray) -> NDArray[np.float64]`
- **method `FutureOperator.F1`** [L47-51]: `def F1(self, b: np.ndarray) -> NDArray[np.float64]` - Next-symbol law ``b T E``, ``[R, V]``.
- **method `FutureOperator.F2`** [L53-60]: `def F2(self, b: np.ndarray) -> NDArray[np.float64]` - Two-step joint ``F2[r, i, j] = b T diag(E[:, i]) T E[:, j]``, ``[R, V, V]``.
- **method `FutureOperator.observability_matrices`** [L62-73]: `def observability_matrices(self, k_max: int) -> list[NDArray[np.float64]]` - ``[O_1, ..., O_{k_max}]``; ``O_k`` has rows = strings of length ``<= k``, cols = N.
- **method `FutureOperator.observability_singular_values`** [L75-77]: `def observability_singular_values(self, k_max: int = 3) -> list[NDArray[np.float64]]` - Singular values of ``O_k`` (descending, unthresholded) for ``k = 1..k_max``.
- **function `context_gain`** [L80-107]: `def context_gain(q_C: np.ndarray, q_last: np.ndarray) -> float` - Mean over rows of ``KL(q_C || q_last)`` in nats.

