# `src/topo_pilot/topology/persistence.py`

- Source: [src/topo_pilot/topology/persistence.py](../../../../../../src/topo_pilot/topology/persistence.py)
- Kind: python
- Lines: 219

## Module docstring

> Vietoris-Rips persistent homology via ripser, with censoring, dedup-safe input and timeout.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)

### External (third-party)

- `numpy` (lines 9, 11)
- `ripser` (lines 10)
- `scipy` (lines 12)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 6)
- `multiprocessing` (lines 5)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 6, import)

## Top-level constants

- `_COMPONENT`
- `_DIRECT_MAX_POINTS`

## Classes and functions

- **function `_is_prime`** [L20-21]: `def _is_prime(n: int) -> bool`
- **class `PHConfig`** [L25-48] decorators: @dataclass(frozen=True) - Persistent-homology configuration.
- **method `PHConfig.__post_init__`** [L39-48]: `def __post_init__(self) -> None`
- **class `DiagramResult`** [L52-71] decorators: @dataclass(frozen=True, eq=False) - Persistence diagrams (pure result; persisted later as ``Diagrams``).
- **function `_validate_matrix`** [L74-85]: `def _validate_matrix(D: NDArray[np.float64]) -> NDArray[np.float64]`
- **function `_rows_from_dgms`** [L88-98]: `def _rows_from_dgms(dgms: list[NDArray[np.float64]]) -> NDArray[np.float64]`
- **function `_ripser_job`** [L101-108]: `def _ripser_job(conn, D, maxdim, coeff, thresh) -> None`
- **function `_run_ripser_worker`** [L111-131]: `def _run_ripser_worker(D, maxdim, coeff, thresh, timeout_s)` - Run ripser in a spawned process; ``None`` on timeout (worker is terminated).
- **function `_h0_from_mst`** [L134-138]: `def _h0_from_mst(D: NDArray[np.float64]) -> list[NDArray[np.float64]]` - H0 diagram from the minimum spanning tree (cheap partial result after a timeout).
- **class `PersistenceComputer`** [L141-219] - Vietoris-Rips persistent homology of a distance matrix.
- **method `PersistenceComputer.__init__`** [L160-161]: `def __init__(self, cfg: PHConfig)`
- **method `PersistenceComputer._dgms`** [L163-174]: `def _dgms(self, D: NDArray[np.float64], thresh: float)`
- **method `PersistenceComputer.diagrams`** [L176-197]: `def diagrams(self, D: NDArray[np.float64]) -> DiagramResult` - Compute the diagrams of ``D`` (see class docstring); never crashes on a timeout.
- **method `PersistenceComputer._maxmin`** [L200-207]: `def _maxmin(D: NDArray[np.float64], m: int, start: int) -> NDArray[np.int64]` decorators: @staticmethod
- **method `PersistenceComputer.maxmin_landmarks`** [L209-219]: `def maxmin_landmarks(self, D: NDArray[np.float64], m: int, rng: np.random.Generator) -> NDArray[np.int64]` - Greedy farthest-point (maxmin) landmarks: random first point, then argmax of min-dist.

