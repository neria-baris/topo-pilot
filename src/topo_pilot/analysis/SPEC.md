# SPEC: `analysis` (waves W2, W4, W5, critical, independent tests; Tier-A review)

## Purpose

Project-aware analysis:
- build the comparison spaces on the **same histories**;
- run PH through `topology`;
- apply the pre-registered decision rules.

| Part | Wave | Contents |
|---|---|---|
| (a) | W2 | reference spaces, σ calibration, discriminability table |
| (b) | W4 | F1 rule, Δgeom, baselines R0–R3, Gaussian floor, layer sweep, dynamics with the checkpoint-order null |
| (c) | W5 | sensitivity grid, circular-coordinate correspondence |
| (d) | WX4 | readout-geometry helpers for X4 (LN gauge, readout projector, predictive cloud) |

## Public API

```python
@dataclass(frozen=True)
class PointSet:
    space: str                 # "world" | "emission" | "belief32" | "belief1" | "future1" | "future2"
                               # | "act:<hook>" | "base:R0..R3" | "null:iso" | "null:cov"
    X: np.ndarray | None       # features, or None if only D is given
    D: np.ndarray | None
    ids: list[str]             # history_ids (or state ids for world/emission)
    metric: str

class SpaceBuilder:
    def __init__(self, store: ArtifactStore): ...              # consumer "analysis"
    def world(self, world_id) -> PointSet: ...
    def emission(self, emission_id) -> PointSet: ...
    def beliefs(self, oracle_id, which: Literal["b32", "b1"], panel: int) -> PointSet: ...
    def futures(self, oracle_id, horizon: Literal[1, 2], panel: int) -> PointSet: ...
    def activations(self, activation_set_id, hook: str, panel: int) -> PointSet: ...
    def baseline(self, kind: Literal["R0", "R1", "R2", "R3"], panel: int, **refs) -> PointSet: ...
    def null(self, like: PointSet, kind: Literal["iso", "cov"], rng) -> PointSet: ...

class SigmaCalibrator:                        # (a) S2
    def select(self, rows: Sequence[SigmaRow]) -> SigmaDecision: ...
    # rows per (sigma, world): mean_H_b1, G_C, min p_w; rule & fallback exactly RESEARCH_SUMMARY §4

class DiscriminabilityTable:                  # (a) S2: S for world/emission/belief32/belief1/future1/future2 × worlds × {O,P}
    def compute(self, refs: Mapping[str, str], panels: Sequence[int]) -> MetricRecords: ...

class F1Decision:                             # (b) pure; independent tests mandatory
    def contrasts(self, S: Mapping[tuple[str, str, int], float]) -> np.ndarray: ...
    # S keyed by (world in {cyl,sq}, ckpt in {init,final}, panel 1..8) -> D_i [8]
    def noise_envelope(self, S: Mapping[tuple[str, str, int], float]) -> float: ...   # u_r
    def verdict(self, per_replicate: Sequence[tuple[np.ndarray, float]],
                learning_gate_passed: Sequence[bool]) -> F1Verdict: ...
    # F1Verdict(status in {SUPPORTED, REJECTED, INCONCLUSIVE}, reasons, per-replicate details)

class GeometryAlignment:                      # (b) Δgeom
    def delta_geom(self, D_A, D_B32, D_B1, last_symbol: np.ndarray | None = None) -> dict[str, float]: ...
    # keys: "all", "same_last_symbol"; Spearman on upper-triangle pairs

class Dynamics:                               # (b) S6
    def curves(self, refs) -> MetricRecords: ...                       # S and regret per checkpoint
    def checkpoint_order_null(self, values: np.ndarray, n_perm: int, rng) -> dict[str, float]: ...

class LayerSweep:                             # (b) secondary: all hooks + concatenation
    def run(self, refs) -> MetricRecords: ...

class Sensitivity:                            # (c) S7, one factor at a time
    def run(self, refs, factors: Mapping[str, Sequence[Any]]) -> MetricRecords: ...

class CircularCorrespondence:                 # (c) S7: circular coords of activations vs latent x angle
    def run(self, activation_ref, sidecar_ref, panel) -> MetricRecords: ...

class AnalysisStage:  # I/O wrappers per stage S2/S4/S5/S6/S7; writes DistanceArtifact, Diagrams, MetricRecords
```

## Part (d): readout-geometry helpers (wave WX4; `PREREGISTRATION_X4.md`)

Pure functions, exported from `topo_pilot.analysis`. All computation is in float64; inputs may be float32.

```python
def ln_gauge_free(Z: NDArray, eps: float = 1e-5) -> NDArray[np.float64]: ...
def readout_projector(gamma: NDArray, W_U: NDArray, rtol: float | None = None) -> NDArray[np.float64]: ...
def split_readout(U: NDArray, P: NDArray) -> tuple[NDArray[np.float64], NDArray[np.float64]]: ...
def predictive_pointset(logits: NDArray, ids: Sequence[str], space: str = "pred:softmax") -> PointSet: ...
```

| Function | Math | Shapes | Invariants | Raises |
|---|---|---|---|---|
| `ln_gauge_free` | LayerNorm without its affine part, row-wise: `u = (z − mean(z)·1) / sqrt(var(z) + eps)`, population variance (ddof 0), as in `torch.nn.LayerNorm` | `Z [M, d]`, d ≥ 2 → `U [M, d]` | every row of U has mean 0; `U(Z + c·1) = U(Z)` for any per-row shift c and any eps; `U(αZ) = U(Z)` for α > 0 exactly when eps = 0 (up to eps otherwise) | `ALIGNMENT_ERROR` (not 2-D, or d < 2); `NUMERICAL_FAILURE` (non-finite Z, or a zero-variance row with eps = 0); `INVALID_CONFIG` (eps < 0) |
| `readout_projector` | `A = diag(gamma) W_U^T ∈ R^{d×V}`; thin SVD `A = Q Σ R^T`; keep the r columns of Q with `σ_k > tol`, `tol = rtol·σ_max`, default `rtol = max(d, V)·eps_float64` (the `numpy.linalg.matrix_rank` convention); `P = Q_r Q_r^T`. A = 0 gives P = 0 | `gamma [d]`, `W_U [V, d]` → `P [d, d]` | `P = P^T`; `P² = P`; `trace(P) = rank(A)`; `P A = A` | `ALIGNMENT_ERROR` (shapes); `NUMERICAL_FAILURE` (non-finite); `INVALID_CONFIG` (rtol < 0) |
| `split_readout` | rows are points: `U_visible = U P`, `U_null = U − U_visible` | `U [M, d]`, `P [d, d]` → two `[M, d]` | `U_visible + U_null = U`; row-wise `U_visible[i] · U_null[i] = 0` (P an orthogonal projector); the readout `U A` is unchanged when U is replaced by `U_visible` | `ALIGNMENT_ERROR` (shapes) |
| `predictive_pointset` | `p = softmax(logits)` per row (max-subtracted, float64) | `logits [M, V]`, M ids → `PointSet(space, X=p, D=None, ids=list(ids), metric="hellinger")` | rows of X sum to 1 and are positive | `ALIGNMENT_ERROR` (not 2-D, or len(ids) ≠ M); `NUMERICAL_FAILURE` (non-finite) |

Why the split is exact: with `logits = LN_f(z) W_U^T = u A + beta W_U^T` (no unembedding bias) and `(I − P) A = 0`, only `u P` reaches the logits; `u (I − P)` (dimension ≥ d − V) is invisible to the next-token output.

## Logic requirements (binding; see RESEARCH_SUMMARY §7)

- **Same histories.** Every comparison between spaces uses the identical `history_id` list; a mismatch raises `SAMPLE_ID_MISMATCH`. World and emission spaces are over all 144 states and are reported separately.
- **Metrics:** activations use raw Euclidean; distributions use Hellinger. Sensitivity variants run only in (c).
- **R2 and R3 baselines:**
  - φ is the spectral embedding of the symmetric matrix `M = E^T diag(π) T E`, using the top 8–16 non-trivial eigenvectors of its normalised Laplacian, with the count fixed in the config;
  - R2 = ½[φ(w₃₂) + φ(w₃₁)];
  - R3 = the mean of φ(w_t) for t = 1..32.

  Both are built from the **process** (E, T), the same knowledge level as the oracle, and are labelled as such. An alternative, label-free variant estimates M from train-token bigram counts; it is a sensitivity variant.
- **R0** is the step-0 checkpoint activations. **R1** is the trained embedding row of w₃₂.
- **Gaussian floor:** 20 isotropic draws and 20 covariance-matched draws, matching each activation cloud's M and dimension. Report the mean and the 95th percentile of S.
- **F1 rule:** exactly as RESEARCH_SUMMARY §7.4. The verdict is `INCONCLUSIVE` with a reason whenever any learning gate fails or any input status is not OK.
- **Δgeom:** Spearman correlation over the upper-triangle pairs. Same-last-symbol pairs are pairs (i, j) with w₃₂ⁱ = w₃₂ʲ. Fewer than 200 such pairs gives status `INCONCLUSIVE`.
- **Checkpoint-order null:**
  - **statistic:** the fraction of the total |ΔS| between consecutive checkpoints that falls within the first third of the checkpoints;
  - **null:** recompute the statistic on random permutations of the checkpoint order;
  - report the permutation p-value per run. This p-value is descriptive: it is not a replicate-level test.

## Invariants and errors

| Condition | Error or status |
|---|---|
| id mismatch between spaces | `SAMPLE_ID_MISMATCH` |
| missing parent | `MISSING_PARENT` |
| non-OK PH inputs | statuses propagate into results, never silently dropped |

## Dependencies and forbidden information

`contracts` and `topology` (public), plus artifacts through the store. May read `EvalSidecar`, but **only** in `CircularCorrespondence` and in boundary/component analyses (extensions). Every such use is labelled `privileged_eval` in MetricRecords.

## Done when

The TEST_PLAN passes. The README walks through the F1 rule on a toy table and explains each baseline.
