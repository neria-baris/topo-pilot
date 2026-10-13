# SPEC: `process` (wave W1)

## Purpose

Builds the two parts of the hidden Markov model, **separately**:
- the transition kernel T, together with π;
- the emission matrix E.

There are two builders. The emission builder never sees T, and the transition builder never sees E.

## Public API

```python
@dataclass(frozen=True)
class TransitionConfig:
    kind: Literal["max_degree_lazy_walk"] = "max_degree_lazy_walk"
    p_stay: float = 0.2

class TransitionBuilder:
    def build(self, world: WorldSpec, cfg: TransitionConfig) -> TransitionSpec: ...
    # T_ij = (1-p_stay)/D_max for neighbours; T_ii = 1 - deg(i)(1-p_stay)/D_max; pi uniform

class CenterStrategy(ABC):
    name: ClassVar[str]
    @abstractmethod
    def centers(self, world: WorldSpec, n_centers: int, rng: np.random.Generator) -> np.ndarray: ...  # [V,D]
class GridCenters(CenterStrategy): ...   # core: c_ab = (0.5+2a, 0.5+2b), a,b in 0..5 (V=36)
class FPSCenters(CenterStrategy): ...    # extensions: farthest-point sampling on world.dist (vertex coords)

class EmissionModel(ABC):
    mode: ClassVar[str]
    @abstractmethod
    def build(self, world: WorldSpec, cfg: EmissionConfig, rng_tree: SeedTree) -> EmissionSpec: ...
class OverlapGaussian(EmissionModel):  mode = "overlap"
class AxisPermuted(EmissionModel):     mode = "axis_permuted"   # E_P[(x,y)] = E_O[(sx(x), sy(y))]
class FullPermuted(EmissionModel):     mode = "full_permuted"   # extension
class Identical(EmissionModel):        mode = "identical"
class Unique(EmissionModel):           mode = "unique"

@dataclass(frozen=True)
class EmissionConfig:
    mode: str; V: int = 36; sigma: float | None = 1.25
    center_strategy: str = "grid"; source_mode: str | None = None   # for permuted modes
    metric: Literal["flat", "graph"] = "flat"

EMISSION_REGISTRY: dict[str, type[EmissionModel]]; CENTER_REGISTRY: dict[str, type[CenterStrategy]]

class ProcessStage:   # I/O
    def run_transition(self, world_id: str, cfg: TransitionConfig, store) -> str: ...
    def run_emission(self, world_id: str, cfg: EmissionConfig, seeds: SeedTree, store) -> str: ...
```

## Logic requirements

- **Overlap (O).** `E[z, j] = softmax_j(−d(z, c_j)² / 2σ²)`, computed with log-sum-exp in float64 and with no truncation. The distance from a state to a non-vertex center uses the same flat-quotient formula as the world. On the cylinder, the x distance is periodic with period 12. Symbol names are permuted using `rng_tree.generator("symbol_names", world_family, replicate)`.
- **Product structure.** For O on the core worlds, `diagnostics.factorizes` must be `True`. Check it numerically: E reshaped to `[12, 12, 6, 6]` must equal the outer product of its x and y marginal kernels to within 1e-12.
- **Axis-permuted (P).** The source is the O spec with the same σ. Draw a fixed permutation σ_x of the 12 x values and σ_y of the 12 y values, seeded per world and **not** per replicate. Then set `E_P[(x, y)] = E_O[(σ_x(x), σ_y(y))]`. The row multiset, p(w), H(W|Z), and the factorisation are all preserved.
- **Identical (N).** `E = 1/V`.
- **Unique (U).** `V = N` and E is a permutation matrix.
- **Diagnostics** (computed under π):
  - `p_w = π E`;
  - `H_W`, `H_W_given_Z`;
  - the coverage radius (maximum distance from a state to its nearest center);
  - row-entropy quantiles.
- **σ selection** is **not** done here. It happens in `analysis` (S2), which needs the oracle. This module builds specs for each σ requested.

## X5 G1 metric-conductance kernel

`conductance.py` (`ConductanceConfig`, `warp_profile`, `conductance_kernel`) and `ProcessStage.run_conductance_transition`. Specified in `docs/proposals/X5_G1_GATES_API.md` (frozen x5g1-feas-v2, D-065). Independent tests: `tests/process/test_conductance.py`.

## Invariants and errors

| Condition | Error |
|---|---|
| a negative entry, or a row sum ≠ 1 ± 1e-12 (T or E) | `NONSTOCHASTIC` |
| π T ≠ π | `STATIONARITY_FAILURE` |
| T not symmetric | `NONSTOCHASTIC` (detail: `asymmetric`) |
| T has support off the edges and self-loops | `NONSTOCHASTIC` (detail: `illegal_support`) |
| σ ≤ 0 for overlap, or a center outside the world chart | `INVALID_SIGMA` |
| some `p_w < 1e-4` | `INVALID_SIGMA` (detail: `dead_symbol`) |
| state order differs from the world's | `STATE_ORDER_MISMATCH` |

## Dependencies and forbidden information

`contracts`, plus the public types of `world` (`WorldSpec` via contracts). Must not use tokens, models, or any results.

## Done when

The TEST_PLAN passes, and the README shows a worked example (n = 3) of T at an interior vertex, an edge vertex, and a corner vertex, and of the axis-wise permutation.
