# x4_circle_history: public API (job 0016; continues the BLOCKED job-0015 draft)

Status: written specification, fixed BEFORE production implementation, for independent test
authors. The machine contract is CONTRACT.json; the numerical bound is ERROR_BOUND.md. Every
function is a pure kernel: inputs are arrays/config/injected guard and clock; there is no hidden
file I/O and no hidden randomness. Import side effects are forbidden: importing a module must not
read data, create files or start processes.

Package location: `tools/x4_circle_history/`. Tests insert that directory (and, where stated,
`tools/x4_oracle_profile/` and `tests/oracle_profile/`) into `sys.path` and import modules by
plain name. pytest runs with `--import-mode=importlib`; every test file starts with
`pytestmark = pytest.mark.analysis`.

## errors.py
```python
class Invalid(RuntimeError)      # numerical/integrity/implementation defect -> FAIL_TECHNICAL
class Unresolved(RuntimeError)   # valid criterion not met / unsupported / exhausted -> INCONCLUSIVE
class AccessDenied(RuntimeError) # scored-panel or scored-row access without a scoring release
class JoinError(RuntimeError)    # cross-model pairing or lineage mismatch: stop for review
```

## cochain.py: integer cochains on the Vietoris–Rips 1- and 2-skeleton

Conventions:
- **Vertices** are 0..n−1.
- **Edges** are int64 [E,2] with i < j, listed in row-major upper-triangle order: lexicographic in
  (i, j).
- **A 1-cochain** is an int64 [E] value on the oriented edge i→j.
- **Triangles** are int64 [T,3] with i < j < k, all three edges present, in lexicographic order.
- **Coboundary.** D1 is the int64 sparse [T,E] matrix with (D1 a)(i,j,k) = a(j,k) − a(i,k) +
  a(i,j). The vertex coboundary is (δf)(i,j) = f(j) − f(i).

```python
def edge_list(D: NDArray[float64] [n,n], radius: float) -> NDArray[int64] [E,2]
    # all i<j with D[i,j] <= radius, lexicographic order.
def triangle_system(edges, n) -> tuple[scipy.sparse.csr_matrix (int64) [T,E], NDArray[int64] [T,3]]
def check_closure(alpha, edges, triangles) -> None
    # Invalid unless alpha(j,k) - alpha(i,k) + alpha(i,j) == 0 for EVERY triangle (explicit sums).
def check_congruence(alpha, a, p) -> None
    # Invalid unless (alpha - a) % p == 0 for every edge.
def integer_lift(a, D1, edges, triangles, n, cfg, guard=None, clock=time.process_time)
        -> tuple[NDArray[int64] alpha, dict info]
```

integer_lift does the following:
1. Set defect = D1 @ a (exact int64).
2. If any defect % p ≠ 0, raise Invalid("not a cocycle mod p").
3. If defect == 0 everywhere, return alpha = a and info["kind"] = "centered_exact", with
   solver_calls 0 and l1_correction 0. Even then, run the closure and congruence checks.
4. Otherwise set b = defect // p. For each bound B in cfg["lift_bounds"], in order:
   - call guard() if it is given;
   - if clock() − start ≥ cfg["lift_cpu_cap_s"], raise Unresolved;
   - solve the feasibility MILP with integer z, −B ≤ z ≤ B, D1 z = b, zero objective,
     node_limit cfg["lift_node_limit"], threads 1;
   - accept the FIRST bound whose solution x rounds (|x − round(x)| ≤ cfg["lift_rounding_tol"]) to
     an integer z with |z| ≤ B and D1 z == b exactly.

   If no bound succeeds, raise Unresolved.
5. **Local improvement:** exactly cfg["local_passes"] passes. Each pass goes over vertices v = 0 ..
   min(cfg["local_vertices"], n) − 1 in ascending order:
   - form d = δe_v (+1 on edges (i,v), −1 on edges (v,j));
   - for s in (−1, +1), keep trial = z + s·d only if its L1 norm is STRICTLY below the current
     L1 norm;
   - among the kept trials choose the minimum by (L1 norm, tuple(trial)) and replace z.
6. Set alpha = a − p·z. Verify D1 z == b, closure and congruence. info has kind
   "corrected_exact", solver_calls, a list of per-call (bound, status) records, and l1_correction
   = ‖z‖₁ after the passes.

cfg keys: field (47), lift_bounds, lift_node_limit, lift_cpu_cap_s, lift_rounding_tol,
local_passes, local_vertices.

```python
def primitive_class(alpha, edges, triangles, n, p) -> tuple[beta int64[E], q int64[n], g int]
```

primitive_class does the following:
1. **BFS from root 0.** The adjacency of i is the list of (j, value(i→j)) sorted ascending, where
   value(i→j) = alpha(i,j) if i < j and −alpha(j,i) otherwise. Set q[0] = 0 and
   q[j] = q[i] + value(i→j) on first visit.
2. A vertex is unreached if the graph is disconnected; raise Unresolved.
3. Compute periods(i,j) = alpha(i,j) − (q[j] − q[i]) and g = gcd(|periods|), starting from 0.
4. If g == 0 or g % p == 0, raise Unresolved.
5. Set beta = periods // g. Verify g·beta + (q[j] − q[i]) == alpha on every edge and
   check_closure(beta); otherwise raise Invalid.

```python
def smooth_phase(beta, edges, n) -> tuple[phi float64[n] in [0, 2pi), residual float]
```

smooth_phase does the following:
- Minimise ‖beta + B f‖₂² over f with f[0] = 0, where (B f)(i,j) = f(j) − f(i).
- Compute residual = max|Bᵀ(beta + B f)| / (1 + ‖beta‖₂). If residual > 1e-8, raise Invalid.
- Return phi = (2π f) mod 2π.

## chart.py: fitted, certified circular chart with a separate gauge and transform

```python
@dataclass(frozen=True) class Chart:
    landmark_ids: NDArray[str]   # strictly ascending
    landmarks: NDArray[float64]  # [n,d] copy
    phi: NDArray[float64]        # raw (ungauged) phase [n] in [0,2pi)
    sigma: float; support_radius: float; d8: NDArray[float64] [n]
    edges, cocycle, integer_lift, lift_correction, primitive, tree_potential: NDArray[int64]
    period_gcd: int
    info: dict  # birth, death, radius, bar_index, n_edges, n_triangles, lift info, smoothing_residual
@dataclass(frozen=True) class Gauge:
    sign: int; shift: float; alignment: float
@dataclass(frozen=True) class Extension:
    phase, resultant, eighth_distance: NDArray[float64]; supported, duplicate: NDArray[bool]

def select_h1_bar(dgm: NDArray [k,2]) -> int
    # largest strictly positive FINITE lifetime death-birth; ties: birth asc, death asc, index asc.
    # Unresolved if none.
def cocycle_to_edges(cocycle_rows, edges, p) -> NDArray[int64]
    # rows (x, y, value) from ripser: orientation sign +1 if x<y else -1; value v in 0..p-1 is
    # centred to v if v <= p//2 else v-p; a[edge(min,max)] = sign*centred; rows whose edge is not
    # in `edges` are ignored.
def fit_chart(X, landmark_ids, cfg, guard=None, timed=None) -> Chart
def fit_gauge(chart: Chart, m32: NDArray [n,2]) -> Gauge
def apply_gauge(phi, gauge) -> NDArray        # (sign*phi - shift) mod 2pi
def extend(chart: Chart, gauge: Gauge, Q: NDArray [m,d], cfg) -> Extension
def agreement(phi_a, phi_b) -> float          # max_s |mean exp(i(phi_a - s*phi_b))|, s in {+1,-1}
def phase_bin_counts(phi, bins=12) -> NDArray[int64]   # floor(phi*bins/(2pi)), clipped to bins-1
def overall_resultant(phi) -> float           # |mean exp(i*phi)|
def chart_gates(ext: Extension, direct_phi: NDArray, cfg) -> dict
def chart_to_arrays(chart, gauge) -> dict[str, NDArray];  chart_from_arrays(d) -> (Chart, Gauge)
```

fit_chart does the following:
- **Inputs.** X must be finite float with n ≥ 9 rows. landmark_ids must be unique and strictly
  ascending, with len == n; otherwise raise Invalid.
- **Diagram.** D is the float64 Euclidean distance matrix. ripser(D, maxdim=1, coeff=p,
  distance_matrix=True, do_cocycles=True) gives the H1 diagram. select_h1_bar picks the bar, with
  radius = (birth + death)/2.
- **Lift and phase.** edges = edge_list(D, radius) and a = cocycle_to_edges(...). Then call
  integer_lift, primitive_class and smooth_phase. The chart carries the raw phi.
- **Extension scale.** d8_i is the 8th smallest D[i, j] over j ≠ i, so only i itself is excluded
  and duplicates at distance 0 do count. sigma = median(d8) (numpy median) and support_radius =
  2·quantile(d8, 0.99, method="inverted_cdf"). If sigma is not finite or not > 0, raise
  Unresolved.
- **No labels.** fit_chart never receives labels, targets or validation data.

fit_gauge does the following:
- m32 must be finite with shape [n,2]; otherwise raise Invalid.
- For s in (+1, −1), c_s = mean(exp(1j·s·phi)·conj(m32[:,0] + 1j·m32[:,1])).
- Choose the s with the larger |c_s|; if they tie exactly, s = +1.
- shift = angle(c_s) and alignment = |c_s|.
- If alignment is not finite, raise Invalid. If alignment == 0, raise Unresolved.

extend does the following, using phi_g = apply_gauge(chart.phi, gauge):
- Distances run from each query to every landmark (float64 Euclidean). The 8 nearest come from a
  stable argsort, so ties go to the lower landmark index, which is the lower ID.
- **Weights.** w = exp(−½(d/sigma)²) and z = Σ w·exp(i·phi_g) / max(Σw, float tiny).
- **Duplicates.** If the query has ANY landmark at distance exactly 0.0, then z = mean of
  exp(i·phi_g) over ALL landmarks at distance exactly 0, and duplicate = True. If 1 − |z| > 1e-8,
  raise Invalid.
- **Outputs.** phase = angle(z) mod 2π, resultant = |z|, and eighth_distance = 8th nearest
  distance. supported = (resultant ≥ 0.2) AND (eighth_distance ≤ support_radius).
- extend never modifies the chart or gauge.

chart_gates(ext, direct_phi, cfg) returns one record for each of support (all supported),
fidelity (agreement(ext.phase, direct_phi) >= 0.8), bins (every phase_bin_counts(ext.phase) >= 8)
and resultant (overall_resultant(ext.phase) <= 0.30):
- each record is {"status": "PASS" | "INCONCLUSIVE", "criterion_met": bool, "value": ..., "threshold": ...};
- a criterion that is not met is INCONCLUSIVE with criterion_met False, and the value is
  preserved;
- "overall" is the first non-PASS status in the order support, fidelity, bins, resultant, and
  otherwise "PASS".

Defects such as nonfinite phases or a shape mismatch raise Invalid, which is FAIL_TECHNICAL at the
runner. Equality follows the written inequalities with no tolerance.

## scores.py: oracle targets, scores and suffix-only controls

Reuses `oracle_profile` (job 0014) unchanged: `suffix_posterior`, `posterior_means`,
`canonical_emission`, `validate_process` and `circle_features`.

```python
def canonical_from_named(named, symbol_perm) -> NDArray[int64]
    # inverse = argsort(perm); canonical = inverse[named]; verify perm is a permutation of 0..V-1
    # and perm[canonical] == named; Invalid otherwise.
def history_digests(canonical32) -> list[str]
    # sha256 hex of each row's 32 canonical tokens as uint8 bytes; requires shape [n,32].
def oracle_moments(T, E_canon, pi, canonical32, features) -> dict {1,4,32: [n,2]}
    # requires canonical32.shape[1] == 32 exactly (w33 never accepted); posterior_means(K=(1,4,32)).
def unit_vectors(phi) -> [n,2]                 # column_stack(cos(phi), sin(phi))
def scores(u, m32, m4) -> [n]                  # sum(u * (m32 - m4), axis=1)
def r4_norms(m32, m4) -> [n]                   # sqrt(sum((m32-m4)**2, axis=1))
def sha256_phase(last4_row) -> float           # 2pi*int.from_bytes(sha256(bytes(uint8 row)).digest()[:8],'big')/2**64
def control_vectors(m1, m4, canonical32) -> dict
    # "m1_unit", "m4_unit": m/||m||, rows exactly (0.0,0.0) -> (1,0);
    # "sha256_last4": unit_vectors(sha256_phase(canonical32[i, 28:32])).
def angular_instability(m, bound) -> NDArray[bool]   # 0 < ||m|| <= bound (diagnostic only)
```

## precision.py: fixed-chart validation precision gates

The model order is fixed as in CONTRACT models. X[m] and r4n[m] are float arrays of the same
length n (512) in EVALUATION order, which is ascending sequence_id.

```python
def sd_b4_draws(X: dict, r4n: dict, models, seed, draws, size) -> tuple[sd [draws,M], b4 [draws,M]]
    # rng = Generator(PCG64(seed)); for b in range(draws): idx = rng.integers(0, n, size=size)
    #   (ONE call per draw, shared by all models); for k, m in enumerate(models):
    #   sd[b,k] = std(X[m][idx], ddof=1); b4[b,k] = mean(r4n[m][idx])
def centered_draws(X: dict, models, seed, draws, size) -> e [draws,M]
    # rng = Generator(PCG64(seed)); per draw idx = rng.integers(0, n, size=size) shared by models;
    # e[b,k] = mean(X[m][idx]) - mean(X[m])
def mde(sd, cfg) -> float     # delta + (Nd.inv_cdf(1-alpha) + Nd.inv_cdf(power)) * sd / sqrt(N)
def precision_summary(sd, e, models, cfg) -> dict
    # per model: sd_lower = quantile(sd[:,k], alpha), sd_upper = quantile(sd[:,k], 1-alpha),
    # mde_lower, mde_upper, q_alpha = quantile(e[:,k], alpha),
    # power = mean(alternative + e[:,k] + q_alpha > delta); all quantiles inverted_cdf.
    # decision: "PASS" iff every model has mde_upper <= alternative AND power >= cfg power;
    # every other combination "INCONCLUSIVE" (criterion_met False); per-model mde_lower,
    # mde_upper, power always reported. Nonfinite inputs/draws -> Invalid.
def b4_summary(b4_draws, b4_point: dict, models, cfg) -> dict
    # lower = quantile(b4_draws[:,k], 0.05), upper = quantile(b4_draws[:,k], 0.95);
    # "PASS" iff every model lower > delta; otherwise "INCONCLUSIVE" (criterion_met False);
    # lower/upper always reported.
```

cfg keys: delta, alternative, power, alpha, projected_N. Nd is statistics.NormalDist().

## error_bound.py: the ERROR_BOUND.md v2 per-row certificate

```python
def u_digits(n) -> Fraction                   # Fraction(1, 2) * Fraction(10) ** (1 - n)   (exact)
def gamma_digits(k, n) -> Fraction            # k*u/(1-k*u), exact; ValueError if k*u >= 1
def trapping_context(prec) -> decimal.Context
    # prec, ROUND_HALF_EVEN, Emin -999999, Emax 999999, clamp 0; traps ON: Underflow, Subnormal,
    # Overflow, Clamped, InvalidOperation, DivisionByZero; traps OFF: Inexact, Rounded, FloatOperation.
def exact_features(coords) -> list[tuple[Decimal, Decimal]]
    # exact cos/sin(pi*x/6) for integer x in 0..11 at 80 digits (0, +-1, +-1/2, +-sqrt(3)/2);
    # Invalid for non-integer or out-of-range x.
def feature_envelope() -> Fraction            # eps_c = 2*u_digits(80)
def decimal_cos_sin(x: float, digits=80) -> tuple[Decimal, Decimal, Fraction]
    # (cos, sin, eps_v) of Decimal(x) exactly, Taylor series per ERROR_BOUND.md section 4;
    # Invalid unless finite and 0 <= x <= 6.284. eps_v is the exact-rational per-coordinate bound.
def posterior_envelope(L, S) -> Fraction      # beta of section 3(a), N = 1 + (L-1)(2S+2)
def moment_envelope(beta, S) -> Fraction      # eps_M of section 3(c)
def reference_moments(T, E, pi, canonical32, Ks=(4, 32), cache=None) -> dict
    # {K: (Mx, My) Decimals} via independent_reference.decimal_suffix_posterior(digits=60) inside
    # trapping_context(60) (flags Underflow/Subnormal/Overflow also checked after each call),
    # then exact-feature moments at 80 digits; a trap or raised flag -> Invalid.
def row_bound(x_hat, phi, M4, M32, eps_M4, eps_M32) -> dict
    # exact rationals: {"Delta", "E_ref", "B"} per ERROR_BOUND.md sections 2-3; phi must pass the
    # decimal_cos_sin range check.
def certify_rows(T, E, pi, coords, canonical32, phi, x_hat, m4_hat, m32_hat, split,
                 scoring_release=None, cap=1e-4) -> dict
    # split in {"calibration", "validation", "scoring"}; "scoring" without scoring_release ->
    # AccessDenied BEFORE any computation. Per row: moment check |m_hat - M_ref| <= 1e-10
    # (K4, K32), then the bound B. Returns {"status": "CERTIFIED" | "INCONCLUSIVE" | "FAIL_TECHNICAL",
    # "max_bound": float, "bounds": list, "moment_check_max": float, "rows": n, "reason": str};
    # INCONCLUSIVE iff some finite B > cap; FAIL_TECHNICAL on a trap, nonfinite, range or
    # moment-check violation.
```

## adapter.py: restricted, read-only E4 adapter (store injected)

```python
@dataclass(frozen=True) class E4Manifest:
    per_model: dict[int, dict[str, str]]   # ObservationSet, HistoryIndex, ActivationSet, checkpoint
    hook: str = "resid_post_3"; end: int = 32; panel_size: int = 512; n_panels: int = 8
class RestrictedE4Adapter:
    def __init__(self, store: ArtifactStore, manifest: E4Manifest, *, scoring_release=None)
    def lineage(self, model) -> dict          # verified lineage facts; JoinError on mismatch
    def panels(self, model, panels=(1, 2)) -> dict[int, dict]
    def identity_report(self) -> dict
def cross_model_join(per_model: dict) -> dict
```

The adapter loads artifacts only through `store.load(cls, id, consumer="analysis")`, which
verifies checksum and schema.

lineage(model) checks the following; any failure raises JoinError:
- **ActivationSet.** Its meta parent_ids contain the manifest ObservationSet, HistoryIndex and
  checkpoint. source == "model", checkpoint_id == the manifest checkpoint, and the hook is
  present.
- **HistoryIndex.** dataset_id == the ObservationSet id, every end == 32, panel_size and n_panels
  as in the manifest. Its parent is the ObservationSet.
- **ObservationSet.** split == "test".
- **Row identity.** ActivationSet.history_id equals HistoryIndex.history_id, element by element.
  For every history, tokens_hash(O.tokens[row_of(sequence_id), :32]) equals
  HistoryIndex.tokens_hash, where row_of maps sequence_id to its ObservationSet row (sequence ids
  are unique).

panels(model, panels) returns, per requested panel, {"history_id", "sequence_id",
"named32" (O.tokens[:, :32]), "activation" (A[:, hook] as float64)}:
- rows are in ascending history_id order (the landmark order);
- the token column 32 (w33) is NEVER returned;
- a panel outside {1, 2} raises AccessDenied unless scoring_release is set; that check happens
  BEFORE any load.

identity_report() runs every lineage check for every model and panel (including 3–8). It returns
ONLY counts, booleans and digests; it returns no token, activation or score arrays.

cross_model_join({model: {"sequence_id", "canonical32", "panel"}}) does the following:
- Requires, for every model, identical per-panel sets of sequence_id and identical
  history_digests per sequence_id; otherwise JoinError.
- Returns {"order": {model: index array that sorts that model's rows by ascending sequence_id},
  "sequence_id": the common ascending ids}.
- There is no unpaired fallback.

## Runtime (builder-tested; not part of the independent numerical tests)

- meter_bind.py is the job-0015 binding of the job-0014 meter, winjob and controls modules,
  reused UNCHANGED through module-level rebinding. It adds per-stage ceilings.
- release.py verifies a coordinator release file.
- runner.py is the future stage driver. Without a matching release it refuses every scientific
  stage, and importing it has no side effects.
