# `src/topo_pilot/topology/metrics.py`

- Source: [src/topo_pilot/topology/metrics.py](../../../../../../src/topo_pilot/topology/metrics.py)
- Kind: python
- Lines: 134

## Module docstring

> Pairwise distance metrics on rows of an array (pure kernels).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)

### External (third-party)

- `numpy` (lines 8, 9)
- `scipy` (lines 10)

### Standard library

- `__future__` (lines 3)
- `abc` (lines 5)
- `typing` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 5, import)
- [src/topo_pilot/topology/distance.py](distance.py.md) (line 13, import)

## Top-level constants

- `METRIC_REGISTRY`
- `_DIST_TOL`

## Classes and functions

- **function `_fail`** [L17-18]: `def _fail(code: ErrorCode, component: str, check: str, detail: str) -> StageFailure`
- **function `_check_matrix`** [L21-28]: `def _check_matrix(X: NDArray[np.float64], component: str) -> NDArray[np.float64]`
- **function `_check_distributions`** [L31-36]: `def _check_distributions(X: NDArray[np.float64], component: str) -> None`
- **function `_finish`** [L39-42]: `def _finish(D: NDArray[np.float64]) -> NDArray[np.float64]`
- **class `DistanceMetric(ABC)`** [L45-66] - Pairwise distance between the rows of ``X``.
- **method `DistanceMetric.pairwise`** [L65-66]: `def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]` decorators: @abstractmethod - Return the [M, M] distance matrix of the rows of ``X``.
- **class `Euclidean(DistanceMetric)`** [L69-76] - Euclidean distance ``||x - y||_2``.
- **method `Euclidean.pairwise`** [L74-76]: `def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]`
- **class `Chord(DistanceMetric)`** [L79-90] - Euclidean distance between L2-normalised rows. A zero row raises ``zero_vector``.
- **method `Chord.pairwise`** [L84-90]: `def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]`
- **class `Hellinger(DistanceMetric)`** [L93-102] - Hellinger distance ``||sqrt p - sqrt q||_2 / sqrt 2``; rows must be distributions.
- **method `Hellinger.pairwise`** [L98-102]: `def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]`
- **function `_entropy_rows`** [L105-107]: `def _entropy_rows(P: NDArray[np.float64]) -> NDArray[np.float64]`
- **class `SqrtJS(DistanceMetric)`** [L110-129] - Square root of the Jensen-Shannon divergence (natural log); rows are distributions.
- **method `SqrtJS.pairwise`** [L121-129]: `def pairwise(self, X: NDArray[np.float64]) -> NDArray[np.float64]`

