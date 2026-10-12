# SPEC: `topology` (waves W1 and W5, critical, independent tests; **pure**)

## Purpose

A generic toolbox for distances and persistent homology. It knows nothing about HMMs, worlds, or models: it receives arrays and returns arrays and summaries. This makes it testable on shapes whose topology is known.

## Public API

```python
class DistanceMetric(ABC):
    name: ClassVar[str]
    @abstractmethod
    def pairwise(self, X: np.ndarray) -> np.ndarray: ...   # [M,F] -> [M,M] float64
class Euclidean(DistanceMetric): name = "euclidean"
class Chord(DistanceMetric): name = "chord"               # Euclidean on L2-normalised rows; zero row -> error
class Hellinger(DistanceMetric): name = "hellinger"       # ||sqrt p - sqrt q||_2 / sqrt 2 ; rows must be distributions
class SqrtJS(DistanceMetric): name = "sqrt_js"            # sqrt of Jensen–Shannon divergence, natural log
METRIC_REGISTRY: dict[str, type[DistanceMetric]]

@dataclass(frozen=True)
class PHConfig:
    maxdim: int = 1; coeff_p: int = 2; threshold: Literal["auto"] | float = "auto"
    pca_dims: int | None = None; landmarks: int | None = None; timeout_s: float = 600

class DistancePipeline:
    def __init__(self, metric: DistanceMetric, pca_dims: int | None = None): ...
    def fit_pca(self, X_fit: np.ndarray) -> "DistancePipeline": ...   # fitted on dev only (caller's duty)
    def compute(self, X: np.ndarray, ids: Sequence[str]) -> DistanceResult: ...
    # DistanceResult(D [M',M'], point_ids, dedup_map, scale_s=q95 of positive distances, status)

class PersistenceComputer:
    def __init__(self, cfg: PHConfig): ...
    def diagrams(self, D: np.ndarray) -> DiagramResult: ...
    # rows [n,4]: (dim, birth, death, censored); threshold "auto" = max(D) so all H1 bars close
    def maxmin_landmarks(self, D: np.ndarray, m: int, rng) -> np.ndarray: ...

class Summaries:          # pure functions on diagrams
    @staticmethod
    def S(diag, dim: int, scale_s: float) -> float: ...           # max finite (death-birth)/s, 0 if none
    @staticmethod
    def pi_max(diag, dim: int) -> float: ...                      # max death/birth over finite bars (birth>0)
    @staticmethod
    def top_k_persistence(diag, dim: int, k: int = 3) -> np.ndarray: ...
    @staticmethod
    def betti_curve(diag, dim: int, grid: np.ndarray) -> np.ndarray: ...

class NullClouds:
    @staticmethod
    def isotropic(M: int, F: int, rng) -> np.ndarray: ...
    @staticmethod
    def covariance_matched(X: np.ndarray, rng) -> np.ndarray: ...

class SyntheticShapes:    # for calibration (G-A) and tests
    @staticmethod
    def circle(M, ambient=128, noise=0.05, rng=None) -> np.ndarray: ...
    @staticmethod
    def disk(M, ambient=128, noise=0.05, rng=None) -> np.ndarray: ...
    @staticmethod
    def flat_torus(M, ambient=128, noise=0.05, rng=None) -> np.ndarray: ...
    @staticmethod
    def sphere(M, dim=2, ambient=128, noise=0.05, rng=None) -> np.ndarray: ...  # extensions

class CircularCoordinates:  # W5 (S7); de Silva–Morozov–Vejdemo-Johansson via a cocycle of the most persistent H1 bar
    def __init__(self, coeff_p: int = 47): ...
    def fit_transform(self, D: np.ndarray) -> np.ndarray: ...     # angles [M] in [0, 2π)
```

## Logic requirements

- **Ripser wrapper:** wrap `ripser` with `distance_matrix=True`, the requested `coeff`, `maxdim`, and `thresh`.
  - **Censoring:** any bar with death equal to ∞ in dimension ≥ 1 is `censored`. The H₀ infinite bar is expected and is not censored.
  - **Timeout:** a call exceeding `timeout_s` (run in a subprocess or with a guard) returns status `CENSORED` with partial information. It is never a crash.
- **Deduplication:** identical points (distance 0) are merged before PH, and `dedup_map` is kept. A fully collapsed cloud gives status `COLLAPSED` and S = 0.
- **Scale:** `scale_s` is the 95th percentile of the positive off-diagonal distances, in raw units. Normalisation by `s` happens only in `Summaries`.
- **Prohibitions:**
  - no k-NN graph distances;
  - no silent approximation;
  - landmarks are used only when `cfg.landmarks` is set, which happens only for `maxdim ≥ 2` (extensions).
- **Circular coordinates:**
  1. take the cocycle of the most persistent H₁ class at a scale inside its lifetime;
  2. lift it to real coefficients;
  3. solve the least-squares harmonic smoothing problem;
  4. return angles mod 2π.

  Document the method in the README (or vendor a small, documented implementation).

## Invariants and errors

| Condition | Error or status |
|---|---|
| D not symmetric, negative entries, or a nonzero diagonal | `NON_METRIC` |
| Hellinger or JS on non-distributions | `NUMERICAL_FAILURE` |
| chord on a zero row | `NUMERICAL_FAILURE` (detail: `zero_vector`) |
| resource limits | `PH_RESOURCE_LIMIT`, or status `CENSORED` |

## Dependencies

numpy, scipy, ripser, and `contracts` (errors and statuses only). `gudhi` is allowed **only in tests**, for cross-checks.

## Done when

The TEST_PLAN passes, including the calibration items that implement gate G-A.
