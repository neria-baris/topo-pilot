# `src/topo_pilot/experiment/x5g1_oracle.py`

- Source: [src/topo_pilot/experiment/x5g1_oracle.py](../../../../../../src/topo_pilot/experiment/x5g1_oracle.py)
- Kind: python
- Lines: 90

## Module docstring

> X5 G1 oracle quantities at p32 (x5g1-feas-v2 §5); history w1..w32 only, w33 never read.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import kl_rows` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 10, via package root)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)
- `from topo_pilot.oracle import BayesFilter, LastSymbolPosterior` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 12, via package root)

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

- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 44, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 46, import)
- [tests/experiment/test_x5g1_lineage.py](../../../tests/experiment/test_x5g1_lineage.py.md) (line 36, import)

## Top-level constants

- `BATCH`
- `END`

## Classes and functions

- **function `_entropy`** [L18-20]: `def _entropy(q: NDArray) -> NDArray[np.float64]`
- **function `_valid_rows`** [L23-25]: `def _valid_rows(q: NDArray) -> bool`
- **function `gate_quantities`** [L28-73]: `def gate_quantities(T: NDArray, E: NDArray, pi: NDArray, tokens33: NDArray, guard: Callable[[str], None] | None = None) -> dict` - Per-row KL of the full-history predictive against last-symbol, stationary-marginal and
- **function `bootstrap_means`** [L76-90]: `def bootstrap_means(values: NDArray, rng: np.random.Generator, n_draws: int = 2000, batch: int = 500, guard: Callable[[str], None] | None = None) -> NDArray` - Means of ``values[rng.integers(0, n, n)]`` for ``n_draws`` draws, in batches with the

