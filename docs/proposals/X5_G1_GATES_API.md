# X5 G1 gates — public API specification (builder and independent test writer)

**Authority.** This implements the frozen [x5g1-feas-v2](X5_G1_FEASIBILITY_PROTOCOL_V2.md) and [plan v2](X5_G1_IMPLEMENTATION_PLAN_V2.md) (D-065). The protocol governs. This file adds signatures only, never numbers.

**Conventions.**

* float64; `topo_pilot.contracts.StageFailure` / `ErrorCode` for errors.
* Status strings are returned values, not exceptions.

## 1. process (`src/topo_pilot/process/conductance.py`, exported from `topo_pilot.process`)

```python
@dataclass(frozen=True)
class ConductanceConfig:
    a: float = 0.20
    move: float = 0.8
```

```python
def warp_profile(dims: tuple[int, int], a: float) -> tuple[ndarray, ndarray]
```

* Returns (f [ny], l_h [ny]) with ny = dims[1], R = dims[0]/(2π) and y = 0..ny−1.
* f(y) = R·(1 + a·cos(2πy/(ny − 1))), and l_h(y) = f(y)·2π/dims[0] = 1 + a·cos(2πy/(ny − 1)).
* Raises `INVALID_CONFIG` if |a| ≥ 1, or if ny < 2.

```python
def conductance_kernel(world: WorldSpec, cfg: ConductanceConfig) -> tuple[TransitionSpec, dict]
```

* **State order.** Requires state id = x·dims[1] + y; otherwise `STATE_ORDER_MISMATCH` (existing check).
* **Edge classes.** Each edge is horizontal iff its endpoints share coords[:, 1] (y), and vertical iff they share coords[:, 0] (x). Any other edge raises `STATE_ORDER_MISMATCH`.
* **Conductances.** c = 1/l_h(y)² for horizontal edges and 1 for vertical ones, symmetric, zero off edges.
* **Kernel.** C_max = max row sum of c. T_ij = move·c_ij/C_max for i ≠ j, and T_ii = 1 − move·rowsum_i/C_max.
* **TransitionSpec.** T, π = 1/N, p_stay = 1 − move, d_max = max graph degree (int); `validate()` is called.
* **Support.** Support outside edges and the diagonal raises `NONSTOCHASTIC`.
* **Metadata dict** (JSON-serialisable floats and ints): {"kind": "metric_conductance", "a", "move", "f_y" (list), "l_h" (list), "C_max", "n_edges_h", "n_edges_v"}.
* **Required behaviour.** At a = 0 on the stored 12×12 cylinder (or the same world built by `topo_pilot.world.build_world`), T equals `TransitionBuilder().build(world, TransitionConfig("max_degree_lazy_walk", 0.2)).T` within 1e-15.

```python
ProcessStage.run_conductance_transition(world_id: str, cfg: ConductanceConfig, store: ArtifactStore) -> str
```

* Loads the WorldSpec (consumer "process"), builds the kernel, and saves the TransitionSpec.
* The saved config is the metadata dict; the parent is [world_id].

## 2. analysis (`src/topo_pilot/analysis/x5_kernel.py`, `x5_context.py`, exported from `topo_pilot.analysis`)

### `x5_kernel.py`

```python
def movement_rate(T, pi) -> float
```

* Returns Σ_z π_z (1 − T_zz).

```python
def is_connected(T) -> bool
```

* Undirected connectivity of the graph {i ≠ j : T_ij > 0 or T_ji > 0}.

```python
@dataclass(frozen=True, eq=False)
class SpectrumReport:
    eigenvalues: ndarray    # descending
    gap: float              # 1 − λ2
    abs_gap: float          # 1 − max(|λ2|, |λ_min|)
    t_rel: float | None
    mixing_bound: int | None
    status: str

def spectrum_report(T, pi, eps=0.25) -> SpectrumReport
```

* The eigenvalues come from the symmetrisation S = diag(√π) T diag(1/√π), using `eigvalsh` of (S + Sᵀ)/2.
* Status is one of: "ok", "REDUCIBLE" (when `is_connected` is False) or "NEAR_UNIT_GAP" (connected, and abs_gap ≤ 1e-12).
* When the status is "ok": t_rel = 1/abs_gap and mixing_bound = ceil(t_rel · log(1/(eps · min π))). Otherwise both are None.

```python
def integrated_autocorrelation(T, pi, g) -> tuple[float | None, str]
```

* The value is Σ_{k≥2} w_k(1 + λ_k)/(1 − λ_k) / Σ_{k≥2} w_k, where:
  - (λ_k, φ_k) is the eigendecomposition of S, sorted descending, with k = 1 the top mode;
  - w_k = (Σ_z √π_z (g_z − ḡ_π) φ_k(z))².
* Returns (None, "UNDEFINED_CONSTANT") if Var_π(g) ≤ 1e-12.
* Returns (None, "REDUCIBLE") if λ_k ≥ 1 − 1e-12 for some k ≥ 2.
* Otherwise returns (value, "ok").

```python
def rate_matched_kernel(T, alpha) -> tuple[ndarray | None, str]
```

* T_α = I + α(T − I).
* Returns (None, "INVALID_KERNEL") if alpha ≤ 0, if T_α has a negative entry, or if min diag(T_α) < 0.2 − 1e-12.
* Otherwise returns (T_α, "ok").

### `x5_context.py`

**Constants:** `GC_THRESHOLD = 0.03`; status strings `"PASS"`, `"FAIL"`, `"NEAR_THRESHOLD"`, `"INVALID_PREDICTIVE"`.

```python
def percentile_interval(values) -> tuple[float, float]
```

* `np.quantile(values, [0.025, 0.975], method="linear")`.

```python
def context_status(lo, hi, valid=True) -> str
```

* INVALID_PREDICTIVE if `not valid`, or if lo or hi is non-finite.
* Otherwise PASS iff lo ≥ 0.03, FAIL iff hi < 0.03, else NEAR_THRESHOLD.

```python
def x5_overall_verdict(arms: dict[str, dict], global_failed: list[str], global_inconclusive: list[str]) -> tuple[str, str]
# exported from topo_pilot.analysis as x5_overall_verdict; the name overall_verdict already belongs to X4 Phase B
```

* Each arm dict has keys "op" (one of "ok", "FAILED", "INVALID_KERNEL", "NEAR_UNIT_GAP") and "context" (a context status, or None when not computed).
* Precedence:
  1. **FAILED** if `global_failed` is non-empty or any arm op is FAILED;
  2. else **INCONCLUSIVE** if `global_inconclusive` is non-empty, or any arm op is INVALID_KERNEL or NEAR_UNIT_GAP, or any context is INVALID_PREDICTIVE, NEAR_THRESHOLD or None;
  3. else **WEAK_CONTEXT** if any context is FAIL;
  4. else **FEASIBLE**.
* The reason names the first deciding arm or entry.

## 3. experiment (`src/topo_pilot/experiment/x5g1_lineage.py`, `x5g1_oracle.py`, `x5g1_controls.py`)

### `x5g1_lineage.py`

**Constants:**

```python
STREAM = ("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")
N_POOL = 16_384
NAMESPACE_CODE = 8
ARMS = ("a0", "a020")
```

```python
def paired_generators() -> tuple[np.random.Generator, np.random.Generator]
```

* Two **separately created** generators: `SeedTree(0).generator(*STREAM)`, called twice.

```python
def sample_named(T, E, perm, pi, rng, n=N_POOL) -> ndarray[n, 33]
```

* A single call to `dataset.HMMSampler(T, E[:, perm], pi, SequenceLayout()).sample(n, rng)`, with the states discarded.
* Returns `perm[canon]`, the named tokens, in the sampler's dtype.

```python
def sequence_ids(arm, n=N_POOL) -> int64 ndarray
```

* `(process_code("cylinder", "overlap", "1.25", "x5g1-v1:calibration:" + arm) << 32) | (8 << 28) | arange(n)`.
* `process_code` is the documented dataset rule: the first 31 bits of `sha256(canonical_json([...]))`.
* An unknown arm raises `INVALID_CONFIG`.

```python
def calibration_obs(named, seq) -> ObservationSet
```

* Returns `ObservationSet(split="dev", V=36, sequence_id=seq, tokens=named)`.

### `x5g1_oracle.py`

```python
def gate_quantities(T, E, pi, tokens33) -> dict
```

* Uses only `tokens33[:, :32]` as the history. **Column 32 (w33) is never read.**
* Processes rows in batches of 4,096.
* Returns:
  - "kl_last": per-row KL(q_C ‖ q_last), with q_C = b32 T E and q_last = r_{w32} T E;
  - "kl_stationary": per-row KL(q_C ‖ πE);
  - "kl_two": per-row KL(q_C ‖ b2 T E), with b2 the posterior from (w31, w32) under π;
  - "position_entropy": a [33] array, the mean H(q_t) for t = 0..32;
  - "valid": a bool, True iff every predictive row is finite, non-negative and sums to 1 within 1e-10, and every KL is defined.
* Oracle failures (StageFailure NUMERICAL_FAILURE or IMPOSSIBLE_HISTORY) set valid = False instead of raising.

```python
def bootstrap_means(values, rng, n_draws=2000, batch=500, guard=None) -> ndarray
```

* Each draw takes `rng.integers(0, n, n)` and computes a mean.
* The draws run in batches; `guard()` is called before and after each batch when it is given.

### `x5g1_controls.py`

```python
class StopRequested(RuntimeError): ...
class BudgetExceeded(RuntimeError): ...

class RunControls:
    def __init__(self, ledger_path: Path, cap_s: float, stop_path: Path, job: str, cumulative_cap_s: float): ...
    def guard(self, step: str) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc, tb): ...
```

* **`guard(step)`:** raises StopRequested if `stop_path` exists. Raises BudgetExceeded if the CPU since entry exceeds cap_s, or if the prior cumulative plus this run's CPU exceeds cumulative_cap_s. Records the step.
* **Context manager.** On `__exit__`, **always** appends an entry to the ledger JSON at ledger_path: {"job", "cpu_s", "status", "steps"}, with status "ok", "stopped", "budget" or "error:<ExceptionName>". It also updates "cumulative_cpu_s", never resets it, and does not suppress exceptions.
* **Ledger file.** {"entries": [...], "cumulative_cpu_s": float}. A missing file starts at 0.

```python
def verify_parents(store, expected: dict[str, str]) -> list[str]
```

* `expected` maps artifact_id to an expected payload_sha256 prefix.
* Loads the metadata of each artifact. Returns a list of failure strings, one per artifact that is missing or whose `payload_sha256` does not start with the expected prefix. Never raises.
