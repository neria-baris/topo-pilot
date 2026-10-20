# `src/topo_pilot/oracle/_filter.py`

- Source: [src/topo_pilot/oracle/_filter.py](../../../../../../src/topo_pilot/oracle/_filter.py)
- Kind: python
- Lines: 123

## Module docstring

> Scaled forward filter and the last-symbol posterior (pure kernels).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from ._common import as_model, check_rows_sum_to_one, check_tokens, fail, normalise_rows` -> [src/topo_pilot/oracle/_common.py](_common.py.md) (line 12, via relative)

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

- [src/topo_pilot/oracle/__init__.py](__init__.py.md) (line 3, import)
- [src/topo_pilot/oracle/stage.py](stage.py.md) (line 23, import)

## Top-level constants

- none

## Classes and functions

- **class `FilterResult`** [L16-27] decorators: @dataclass(frozen=True, eq=False) - Output of :meth:`BayesFilter.run`.
- **class `BayesFilter`** [L30-90] - Exact scaled forward filter (row vectors, float64, reset to ``pi`` per row).
- **method `BayesFilter.__init__`** [L53-55]: `def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray) -> None`
- **method `BayesFilter.run`** [L57-77]: `def run(self, tokens: np.ndarray) -> FilterResult` - Filter every row of ``tokens [R, P]`` (see class docstring for the recursion).
- **method `BayesFilter.belief_at`** [L79-90]: `def belief_at(self, tokens: np.ndarray, p: int) -> NDArray[np.float64]` - ``b_p [R, N]`` (posterior after ``w_p``), ``1 <= p <= P``.
- **class `LastSymbolPosterior`** [L93-123] - Posterior from the last symbol alone, ``r_w``, and its predictive ``q_last = r_w T E``.
- **method `LastSymbolPosterior.__init__`** [L110-112]: `def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray) -> None`
- **method `LastSymbolPosterior.r`** [L114-117]: `def r(self, w: np.ndarray) -> NDArray[np.float64]` - ``r_w`` for each symbol in ``w``.
- **method `LastSymbolPosterior.q_last`** [L119-123]: `def q_last(self, w: np.ndarray) -> NDArray[np.float64]` - ``r_w T E`` for each symbol in ``w``.

