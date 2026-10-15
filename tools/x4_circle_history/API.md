# x4_circle_history: public API (jobs 0016-0017, spec v2.5; continues the BLOCKED job-0015 draft)

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
    # (cos, sin, eps_v) of Decimal(x) exactly; fixed N = 48 Taylor terms (TAYLOR_N); exact-rational
    # eps_v per ERROR_BOUND.md v2.1 section 4; Invalid unless finite and 0 <= x <= 6284/1000
    # (ANALYTIC interval). The OPERATIONAL chart check 0 <= phi < 2*np.pi is done by certify_rows.
def posterior_envelope(L, S) -> Fraction      # beta of section 3(a), N = 1 + (L-1)(2S+2)
def moment_envelope(beta, S) -> Fraction      # eps_M of section 3(c)
def reference_moments(T, E, pi, coords, canonical32, Ks=(4, 32), cache=None, cache_only=False) -> list[dict]
    # (v2.4 erratum: coords and cache_only were missing from this line; one {K: (Mx, My)} per row)
    # {K: (Mx, My) Decimals} via independent_reference.decimal_suffix_posterior(digits=60) inside
    # trapping_context(60) (flags Underflow/Subnormal/Overflow also checked after each call),
    # then exact-feature moments at 80 digits; a trap or raised flag -> Invalid.
def row_bound(x_hat, phi, M4, M32, eps_M4, eps_M32) -> dict
    # exact rationals {"R", "Delta", "E_ref", "B"}: R = sum_j Fraction(v_j)*(Fraction(M32_j)-Fraction(M4_j));
    # Delta = |Fraction(Decimal(x_hat)) - R|; E_ref = eps_v*sum_j|r_j| + 2*(eps_M4 + eps_M32); B = Delta + E_ref.
def reference_check_rows(T, E, pi, coords, canonical32, m_hat: dict, Ks, split,
                         scoring_release=None, cache=None) -> dict
    # early gate: for every row and K in Ks, max_j |m_hat[K][row, j] - M_ref_K,j| <= 1e-10;
    # {"status": "PASS" | "FAIL_TECHNICAL", "moment_check_max": {K: float}, "rows": n};
    # split "scoring" without scoring_release -> AccessDenied before computation.
def certify_rows(T, E, pi, coords, canonical32, phi, x_hat, m4_hat, m32_hat, split,
                 scoring_release=None, cap=1e-4, cache=None) -> dict
    # split in {"calibration", "validation", "scoring"}; "scoring" without scoring_release ->
    # AccessDenied BEFORE any computation. Per row: operational phase check 0 <= phi < 2*np.pi
    # (else FAIL_TECHNICAL), moment check |m_hat - M_ref| <= 1e-10
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

## Spec v2.2 clarifications (coordinator code-draft review; normative)

1. **integer_lift CPU cap (aggregate, per chart).** Let elapsed = clock() − start, with start
   taken when the bounded search begins, and cap = cfg["lift_cpu_cap_s"]. Each condition below
   raises Unresolved, never PASS:
   - (a) before each solver call: elapsed ≥ cap;
   - (b) IMMEDIATELY AFTER each solver call, before its candidate is accepted: elapsed ≥ cap.
     A candidate that arrives after the cap is rejected.
   - (c) at every vertex step of the local L1 passes: elapsed ≥ cap;
   - (d) after the final closure and congruence verification: elapsed ≥ cap.

   Each native call also gets time_limit = min(cap − elapsed, cfg.get("native_operation_wall_s",
   180)). Tests inject a fake `clock` callable. The search bounds and node limits are unchanged.
2. **HiGHS threads.** The solver options are pinned explicitly: threads = 1 and parallel = False.
   scipy forwards them to HiGHS verbatim. If HiGHS rejects or ignores any option, which shows up
   as a scipy OptimizeWarning during the call, integer_lift raises Invalid (fail closed). The
   module exposes `cochain.HIGHS_PINNED == {"threads": 1, "parallel": False}`.
3. **extend normalisation.** The weights are computed as w_j = exp(ℓ_j − max_k ℓ_k), with
   ℓ_j = −½(d_j/σ)². This is the same normalised weighting as exp(ℓ_j)/Σexp(ℓ_k), without
   underflow. There is NO denominator floor, so a far query keeps the exact normalised resultant
   of its 8 neighbours: its phase and |z| equal the near-query formula after subtracting the
   largest log-weight. A non-finite z raises Invalid. Support semantics are unchanged.
4. **control_vectors / angular_instability.** Nonzero vectors are normalised scale-first: divide
   by the maximum absolute component, then by the Euclidean norm of the scaled vector.
   - EXACT (0.0, 0.0) maps to (1, 0).
   - Tiny normal or subnormal nonzero vectors give finite unit vectors in the correct direction.
     For example (5e-324, 0) → (1, 0) and (−5e-324, 5e-324) → (−√½, √½).
   - angular_instability uses the same stable magnitude. Non-finite input, or a negative or
     non-finite bound, raises Invalid.
5. **precision_summary / b4_summary fail closed.** They raise Invalid when models is empty or has
   duplicates, when a draw matrix is not 2-D with ≥ 1 row and exactly len(models) columns, on
   non-finite values, or (b4_summary) when the point keys differ from models.

## Spec v2.3 clarifications (coordinator guard review; normative)

1. **Scoring authority.** The ONLY value that unlocks scored access is an instance of
   `errors.ScoringAuthority`, a frozen dataclass with fields owner_record_path: str,
   owner_record_sha256: str (64 hex), scope: tuple and release_job_id: str, whose scope contains
   "scoring".
   - `errors.require_scoring(x)` raises AccessDenied for anything else: None, False, True, {},
     a string, an arbitrary object, a ScoringAuthority whose scope lacks "scoring", or one with
     a malformed sha256.
   - Production code obtains a ScoringAuthority only from `release.scoring_authority(rel)`.
     Tests may construct one directly as a synthetic fixture.
   - The rule applies identically to `RestrictedE4Adapter(..., scoring_release=...)` for panels
     outside {1, 2} (checked before any store.load), and to `error_bound.certify_rows` and
     `reference_check_rows` with split "scoring" (checked before any computation).
2. **Release (`release.py`; builder-tested).**
   - `scoring_released` must be a strict bool.
   - A True value requires owner_scoring_release_ref = {path, sha256, scope}, naming an existing
     file whose sha256 matches, with "scoring" in scope.
   - A feasibility release (scoring_released False) never yields scored access.
   - HEAD is read from the git files; no subprocess is used.
3. **Metering (`meter_bind.py`; builder-tested).**
   - During supervision the stage ceiling is enforced on stage spent + current child + current
     supervisor CPU + tail allowance.
   - Only `--finalization` with stage export may run past 3480, up to 3600.
4. **Source integrity before payload I/O (`live_context.py`; builder-tested).** Before any store
   access, every frozen file hash, the frozen file set, the module paths and the installed
   dependency set are re-checked against FREEZE.json. A dirty source is refused.

## Spec v2.4 clarifications (coordinator reference-final, pipeline-freeze and allocation reviews; normative)

Sources: messages coordinator-0016-reference-final-review (A43DDDC2…),
coordinator-0016-pipeline-freeze-review (B481F090…), jobs/0016/PIPELINE_DRAFT_STATIC_REVIEW.md
(0FBD542B…) and coordinator-0016-prospective-resource-allocation (9C7BE6D5…). Scientific gates,
thresholds, panels, methods, seeds and the history-ID chart order / sequence-ID precision order
are UNCHANGED. Items 1–6 are tested by the independent authors (A: items 5–6; B: items 1–4);
items 7–12 are builder-tested runtime.

1. **Error taxonomy (errors.py, runner).** `JoinError` now means a TECHNICAL identity defect:
   cross-model pairing, artifact lineage, checksum, canonical join, persisted-ID or
   source-integrity mismatch. The runner records `Invalid` AND `JoinError` as FAIL_TECHNICAL
   (overall FAIL); only `Unresolved` (valid criterion not met, unsupported, missing chart,
   resource exhaustion, inadequate precision) is INCONCLUSIVE. Which calls raise JoinError is
   unchanged (adapter lineage/join, cross_model_join). A blocked gate still ends the cohort.

2. **error_bound.py corrections (reference-final review).**
   - Taylor constants: for first ∈ {0 (even/cos), 1 (odd/sin)} the COMPLETE positive series
     Σ_k X^(2k+first)/(2k+first)! is bounded exactly by Σ_{k≤N} t_k + t_{N+1}/(1 − r) with
     r = X²/((2N+3+first)(2N+4+first)) < 1; both bounds must be ≤ A = 270. The alternating
     remainder is bounded by its first neglected term (Leibniz; ratio < 1 verified); rounding
     uses Σ_{k≤N}|t_k| ≤ complete positive series ≤ A. The module refuses import (Invalid) if
     any check fails.
   - `process_digest(T, E, pi, coords) -> str`: sha256 over, for name in ("T", "E", "pi",
     "coords") in that order, the bytes of f"{name}:{a.dtype.str}:{list(a.shape)}\n" followed by
     a.tobytes(), where a = np.ascontiguousarray(np.asarray(x, dtype=np.float64)).
   - Histories are validated BEFORE any conversion: ndim 2, exactly 32 columns, integer dtype
     (kind "i" or "u"), every value in 0..V−1 with V = E.shape[1]; otherwise Invalid. A float,
     bool, negative, ≥ V or wrapped (e.g. 260 as uint8 = 4) history is never accepted.
   - Cache key = (process_digest, K, int64 row bytes). A cache filled under one process is never
     hit under another; two histories that would collide after a narrowing conversion never
     share a key.
   - New keyword `cache_only=False` on reference_moments, reference_check_rows and
     certify_rows: when True, a missing key raises Invalid("reference cache miss") BEFORE any
     reference computation (no silent recomputation). The miss is `errors.CacheMiss`, a subclass
     of Invalid, and certify_rows re-raises it instead of folding it into a status (the runner
     records it as FAIL_TECHNICAL at row_score_certificates).
   - Moment gaps are exact: |Fraction(float(m̂)) − Fraction(M_ref)| compared with
     Fraction(1, 10**10). The returned "moment_check_max" values are floats for REPORTING only;
     "moment_check_max_exact" gives str(Fraction). A gap of exactly 1e-10 as a rational passes;
     a gap whose float rounds to 1e-10 but whose exact value exceeds Fraction(1, 10**10) fails.
   - certify_rows reports "moment_check_max" (float max over K) and "moment_check_max_by_K".
   - Decimal traps propagate into the nested reference context; its flags do not propagate
     back, so the outer flag inspection covers only outer operations.

3. **reference_cache.py (new; persisted exact references).**
   ```python
   SCHEMA = "x4-circle-reference-cache-v2"
   def identity(T, E, pi, coords) -> dict
       # {"process_digest": error_bound.process_digest(...),
       #  "feature_identity": sha256 hex of "\n".join(f"{c}|{s}" for (c, s) in
       #       error_bound.exact_features(arange(12) as [12,1] coords)) + f"|{FEATURE_DIGITS}|{REF_DIGITS}",
       #  "source_identity": {"independent_reference": sha256 of tests/oracle_profile/independent_reference.py,
       #                      "error_bound": sha256 of tools/x4_circle_history/error_bound.py}}
   def export_cache(cache, ident, rows) -> dict
       # {"schema", "identity": ident, "rows": rows, "entries": [...]};
       # entries sorted by key: {"process_digest", "K", "history": int64-bytes hex, "mx": str(Decimal), "my": str(Decimal)};
       # rows: list of {"model", "split", "panel", "history_id": [str], "sequence_id": [int],
       #                "history": [int64-bytes hex per row]} in the stage's row order.
   def load_cache(obj, ident_expected) -> dict
       # Invalid on: schema mismatch; identity != ident_expected (any field); an entry whose
       # process_digest differs; a duplicate (digest, K, history) key; an mx/my string that is not
       # a finite Decimal. Returns {(digest, K, bytes): (Decimal, Decimal)} with Decimal(str) exact.
   def verify_rows(obj, model, split, panel, history_id, sequence_id, canonical32, Ks=(4, 32)) -> None
       # Invalid unless obj["rows"] holds exactly one record for (model, split) whose panel,
       # history_id (as str), sequence_id (as int64) and history hex (int64 bytes of the validated
       # canonical rows) are EXACTLY equal, in order, to the arguments; and every (digest, K, row)
       # entry for K in Ks is present.
   ```
   Decimal strings are never converted through float. Only calibration and validation rows are
   ever stored.

4. **process_law.py (new; ERROR_BOUND.md v2.2 section 9, implemented).** Exact rationals
   (Fraction) and 60-digit Decimal only; the stored float arrays are exact reals. It follows the
   coordinator's generating-law clarification (01C0116D…).
   ```python
   LAW = {"dims": (12, 12), "x_period": 12, "neighbour": Fraction(1, 5), "grid": 6,
          "sigma": Fraction(5, 4), "L": 32, "draws": {"pi": 1, "emission": 32, "transition": 31}}
   def lattice_states(coords) -> list[tuple[int, int]]
       # (x, y) per state; Mismatch unless coords are exactly the integers (s // 12, s % 12).
   def documented_transition(states) -> list[list[Fraction]]
       # neighbours: same y and x differing by ±1 mod 12, or same x and |dy| = 1 (y not periodic);
       # T*[s][t] = 1/5 per neighbour, T*[s][s] = 1 - deg(s)/5, 0 otherwise.
   def ideal_identities(T_star, S) -> None
       # Mismatch unless, EXACTLY: T* symmetric, every row sums to 1, entries in [0, 1], and
       # pi* = (1/S, ..., 1/S) satisfies pi* T* = pi*.
   def softmax_enclosure(states, digits=60) -> tuple[list[list[Decimal]], Fraction, Fraction]
       # centre j = 6a + b at (1/2 + 2a, 1/2 + 2b); d² = min(|dx| mod 12, 12 - |dx| mod 12)² + dy²
       # (exact quarter-integers); logit = -8d²/25 formed EXACTLY in Decimal (Inexact trapped for
       # that division only); in a trapping 60-digit context: n_j = exp(logit_j), D = sum of the
       # 36 n_j from Decimal(0) (36 roundings), E_dec = n_j / D (one rounding).
       # u = u_digits(60); exp is allowed 2u relative error (correct rounding is not relied on):
       # lo = (1-2u)(1-u) / ((1+2u)(1+u)^36), hi = (1+2u)(1+u) / ((1-2u)(1-u)^36).
       # Every exact E*[s][j] lies in the POSITIVE interval [E_dec/hi, E_dec/lo].
   def sampler_cdf(P) -> np.ndarray
       # the ACTUAL sampler thresholds: src/topo_pilot/dataset/sampler.py `_cumulative_rows`
       # (loaded from that frozen file without importing the dataset package), applied as
       # HMMSampler does to T, E_canon and pi[None, :]. The sampler is neither edited nor rerun.
   def threshold_law(c_row) -> dict
       # c' = min(max(c, 0), 1) elementwise (observationally identical for u in [0, 1));
       # the draw is j = min(#{i: c'_i <= u}, V-1) for u = k·2^-53, k in 0..2^53-1.
       # With s = sorted(c') and s_{-1} = 0, G(x) = min(max(ceil(x·2^53), 0), 2^53):
       # P(N = j) = (G(s_j) - G(s_{j-1}))·2^-53 for j < V, P(N = V) = (2^53 - G(s_{V-1}))·2^-53,
       # q_j = P(N = j) for j < V-1 and q_{V-1} = P(N = V-1) + P(N = V)  (exact Fractions).
       # Returns {"q": [Fraction], "clamped": [Fraction], "monotone": bool (c' nondecreasing and
       # c'_{V-1} == 1)}.
   def row_tv(p_hat_row, dev_row, c_row) -> dict
       # dev_row[j] >= |p̂_j - p*_j| exactly. Returns {"grid": ½Σ_j(|q_j - p̂_j| + dev_j),
       # "documented": ½Σ_j(|e_j| + |e_{j-1}| + 2^-53 + dev_j) with e_j = c'_j - Σ_{i<=j} p̂_i,
       # e_{-1} = 0, ONLY when monotone (else None)}. "grid" is the bound used.
   def process_law_bound(T, E, pi, coords) -> dict
       # status "BOUNDED" or "UNAVAILABLE" (never Invalid for a mismatch; Invalid only for
       # non-finite or misshaped inputs). UNAVAILABLE with the exact reason when: coords are not
       # the documented lattice, S != 144 or V != 36, the ideal identities fail, the zero support
       # of T̂ differs from T*, some Ê or π̂ entry is not strictly positive, or kappa >= 1.
       # kappa_T = max over T* > 0 of |T̂ - T*|/T*; kappa_pi = max_s |π̂_s - 1/144|·144;
       # kappa_E = max_{s,j} max(|Ê - E_dec/hi|, |Ê - E_dec/lo|)/(E_dec/hi); kappa = max of the three.
       # rho_minus_1 = ((1 + kappa)/(1 - kappa))^(2L+1) - 1 with L = 32 (a length-L positive
       # path has 2L factors; 2L+1 is conservative).
       # dev: |π̂ - 1/144| (pi), |T̂ - T*| (T), max(|Ê - E_dec/hi|, |Ê - E_dec/lo|) (E).
       # TV = tv_pi + 32·max_s tv_E(s) + 31·max_s tv_T(s) (grid values); Z_bound = 2·(rho - 1) + 4·TV
       # (C2 = 1). Returns exact strings and floats for kappa_*, rho_minus_1, tv_pi, tv_E_max,
       # tv_T_max, TV, TV_documented (None if any row is non-monotone), Z_bound, the monotone
       # flags, and "claim": "bound on |E_Q[g·(M32-M4)]| under the IDEALIZED sampling law; not an
       # exact zero for the fixed saved data".
   ```
   Q is the IDEALIZED law: independent uniform 53-bit draws across every sampler call and
   trajectory, and independent panel assignment. Z_bound covers the parameter, CDF and grid
   discrepancy under that idealization only; it does not bound deterministic PRNG bias or
   correlation. `Mismatch` is a module-local exception caught inside process_law_bound
   (→ UNAVAILABLE). process_law_bound is reported beside the controls; it is not a gate and never
   changes a threshold.

5. **cochain.integer_lift timer (author A).** `start = clock()` is taken at ENTRY, before the
   defect D1·a is formed. EVERY successful return is preceded, after its final exact closure
   and congruence checks, by the cap check `clock() - start >= lift_cpu_cap_s → Unresolved`;
   this includes the already-closed (zero-defect) branch. The cap stays 30 CPU s per chart
   whatever the study budget.

6. **chart.py timed hook (author A).** `fit_chart(X, ids, cfg, guard=None, timed=None)` calls
   `timed(label, fn)` with a zero-argument callable for each of, in order: "distance" (cdist),
   "ph" (ripser), "edges" (edge_list), "two_skeleton", "integer_lift", "primitive",
   "smoothing", returning fn's result unchanged; timed=None runs each fn directly. An exception
   raised by timed (e.g. Unresolved for an exhausted operation) propagates unchanged and no later
   label is called. `extend(chart, gauge, Q, cfg, timed=None)` wraps its query-landmark distance
   computation as "extension_distance".

7. **Native-operation wall guard (op_guard.py + meter_bind; builder-tested).** The live context
   supplies `timed = op_guard.timed_factory(out, native_operation_wall_s)`:
   - before fn: appends {"event": "start", seq, label, utc} to out/OPERATIONS.jsonl and
     atomically writes out/OPERATION_ACTIVE.json {"state": "active", seq, label,
     "started_epoch", "deadline_s", pid};
   - after fn: writes {"state": "idle", seq, label} and appends {"event": "end", seq, label,
     elapsed_s}; an exception appends {"event": "error"} and re-raises;
   - secondary post-return check: elapsed ≥ deadline → {"event": "exhausted"} and Unresolved.
   The PRIMARY enforcement is the existing meter supervisor loop (no new watcher):
   meter_bind's stage limiter reads OPERATION_ACTIVE.json at every poll and returns the kill
   reason "native operation wall <d>s exceeded: <label> (seq <n>)" once now − started_epoch ≥
   deadline_s; the unchanged meter then terminates the Job Object and records killed_reason in
   the ledger. Before launching, meter_bind archives a stale active marker to
   out/operations/KILLED_<seq>.json (the killed-attempt record) and removes it. A killed or
   exhausted attempt is never retried (item 8).

8. **Stage prerequisites and no recompute (stage_records.py; builder-tested).** out/STAGES.jsonl
   holds {"stage", "event": "STARTED" | "COMPLETED" | "REFUSED", "utc", "evidence": {file:
   sha256}, "reason"}. `begin(out, stage)` refuses (StageRefused, exit 3, a REFUSED line, no gate
   record) when the stage already has a STARTED line (no retry, no recompute, including after a
   kill), or when its prerequisites are missing:
   - oracle: identity COMPLETED, gate identity PASS, IDENTITY.json hash equal to its COMPLETED
     evidence, and IDENTITY.json showing every model joined on the same rows;
   - charts: oracle COMPLETED, gate process_and_reference PASS, evidence hashes of ORACLE.json,
     REFERENCE_CACHE.json and every oracle_<model>.npz equal;
   - precision: charts COMPLETED with one row_score_certificates PASS per model, evidence hashes
     of CHARTS.json and every chart_/phases_<model> file equal;
   - export: no prerequisite (closeout after any non-PASS), once.
   An evidence hash mismatch is an integrity REFUSED line with "integrity": true; export then
   reports overall FAIL. An empty or incomplete GATES history never opens a later stage.

9. **Persisted reference and ID alignment (runner; builder-tested).** The oracle stage computes
   all-row references once per unique canonical history (K4/K32 gated; K1 for every row as a
   diagnostic for the m1 control; the four lowest rows K1/K4/K32 gated), writes
   REFERENCE_CACHE.json (item 3) with the row table for every model and split, and records its
   sha256 and identity in ORACLE.json together with process_law_bound (item 4). The charts
   stage, BEFORE gauge/chart/certificate work, verifies the cache file hash, identity and
   verify_rows for each model/split, and compares the saved oracle history_id and sequence_id
   arrays EXACTLY with the reloaded rows (Invalid → FAIL_TECHNICAL at chart_calibration);
   certify_rows then runs with cache_only=True. The precision stage verifies, before any
   bootstrap, that every model's validation rows sorted by sequence_id have identical
   sequence_id arrays and identical canonical-history digests (Invalid → FAIL_TECHNICAL at
   B4_lower).

10. **Validation controls (precision.py, scores.py; author B for the kernels).**
    ```python
    scores.control_scores(m1, m4, m32, canonical32) -> dict
        # {name: u_c · (m32 - m4)} for name in ("m1_unit", "m4_unit", "sha256_last4"),
        # u_c = control_vectors(m1, m4, canonical32)[name]
    precision.control_summary(C, models, seed, draws) -> dict
        # C = {name: {model: [n] floats}} in evaluation order; rng = Generator(PCG64(seed));
        # for b in range(draws): idx = rng.integers(0, n, size=n), ONE call per draw shared by
        # every control and model; draw value = mean(C[name][model][idx]).
        # Per name and model: "point" = mean, "central95" = [q(.025), q(.975)],
        # "bonferroni" = [q(.05/3), q(1 - .05/3)], quantiles inverted_cdf. Invalid on non-finite,
        # unequal lengths, n < 2, empty or duplicate models, or unknown control names.
        # Returns no status: controls are reported, never gated, never used to recentre.
    ```
    The runner calls control_summary with seed = sd_seed and draws = sd_draws, so the control
    draws use exactly the SD/B4 index stream (joint whole-trajectory resampling). Near-zero
    angular diagnostics: for m1_unit and m4_unit, counts of
    angular_instability(m_K, bound_K) per model with bound_K = (exact max moment gap of K over
    the validation rows, rounded up to float) + float(moment_envelope(posterior_envelope(K,
    144), 144)) rounded up. PRECISION.json is written in every outcome (also after a B4 stop)
    and carries the controls, the instability counts and the oracle Z_bound.

11. **Frozen dependency manifest (freeze_bind, live_context; builder-tested).** frozen_files()
    also binds every file of src/topo_pilot/__init__.py, src/topo_pilot/contracts/** (all
    files, no __pycache__) and src/topo_pilot/dataset/sampler.py. Before any store access,
    live_context verifies those hashes and the exact file set, imports the contracts modules,
    and refuses if any loaded module from this worktree's src/, tools/ or tests/ is outside the
    frozen set. The runner re-checks the loaded-module set at stage end (Invalid on an unfrozen
    module). Those sources are never edited.

12. **Numerical implementation identity (env_identity.py; builder-tested).** The freeze runs a
    metered probe in the venv interpreter that imports the fixed scientific import list and
    records: interpreter version, executable sha256, base python310.dll/python3.dll/vcruntime
    sha256; sha256 of every loaded module file; for every site-packages top-level distribution
    with a loaded module, a tree digest (sorted relpath:sha256 lines) of that top-level entry and
    of its "<name>.libs" directory; platform, processor, numpy CPU-dispatch features and
    threadpool info (informational but verified). live_context recomputes the same record after
    the same imports and refuses unless equal. LIMITATION (stated, not overclaimed): OS DLLs
    outside the Python and site-packages trees, CPU microarchitecture, microcode and runtime SIMD
    / BLAS kernel selection are not bound by hashes; the per-row certificate measures the actual
    float result in the same run, so certificate validity does not depend on them, but
    bit-for-bit reproducibility on other hardware is not claimed.

13. **Resources: prospective allocation, then owner override (CONTRACT.json, ledger
    metadata).**
    - The coordinator's prospective subcaps (implementation 400, identity 200, oracle 900, charts
      1700, precision 200, export 200; total 3600; stop new non-finalization work at 3480) are
      recorded in CONTRACT resources.stage_caps_s. The previous caps (oracle 400, charts 2200) are
      kept in resources.allocation_history with the authorising message; the change was
      prospective, before any real oracle work.
    - The owner override (owner-overnight-coordinator-transfer-20261014, OWNER_MESSAGE 13160D21…)
      then CANCELLED all CPU-time ceilings and stage allocations prospectively, replacing them
      with safety limits: ≤ 4 threads and ≤ 12 GiB RAM per task, one scientific task at a time,
      large outputs on X: only, safe STOP if C: free < 2 GB or X: free < 30 GB. It is recorded in
      resources.owner_override. CPU measurement, the single ledger and reporting continue; old
      entries and provenance are preserved.
    - Interim binding, pending the incoming coordinator's review of a transparent binding change:
      the meter still enforces the recorded caps (conservative; 0016 uses the implementation
      stage only), threads stay 1, memory stays 8 GiB, and meter_bind ADDS the owner's disk
      safe-STOP to the stage limiter (kill reason "disk safe-STOP ..."; also checked before
      launch). meter_bind applies the recorded caps to the ledger metadata in the supervisor
      process (charged to that run), preserving every entry byte for byte, and refuses a ledger
      whose caps match neither the current nor a recorded previous allocation.
    - Methodological bounds stay unchanged: lift 30 CPU s per chart, six 512-row constructions,
      180 s per native operation, 128 nodes per bound, fixed search.

## Spec v2.5 clarifications (job 0017: coordinator review of 0016 and owner override; normative)

Sources: jobs/0017/task.md (355F19CC…), jobs/0016/review.md (ACCEPT; decisions 3 and F4), owner
overnight authorization (OWNER_MESSAGE 13160D21…). No scientific criterion, gate, threshold,
order, seed or method changes. All three items are builder-tested runtime.

1. **Release issuer binding (release.py).** `issued_by` is one of:
   - `"claude-coordinator"`: the release MUST also carry `coordinator_session_id` (str) and
     `coordinator_assumption_ref = {"path", "sha256"}`. verify() requires that the referenced
     file lies under `<mailbox>/archive/`, exists, has that sha256 (hex, case-insensitive), parses
     as JSON with `schema == "coordinator-assumption-v1"` and `coordinator_session_id` equal to
     the release value; and that `<mailbox>/coordinator_runtime.json` currently reports
     `mode == "ACTIVE_CLAUDE_COORDINATOR"`.
   - `"codex-coordinator"`: verified exactly as before (old records stay verifiable), but it may
     carry neither Claude field, and it is REFUSED while `coordinator_runtime.json` reports
     `mode == "ACTIVE_CLAUDE_COORDINATOR"` (Codex relinquished; a new Codex-issued release would
     be an impersonation).
   - anything else is refused.

   Every other check is unchanged: live RUN_NEXT job/task binding, release file inside the
   dispatched job directory, task.md digest, known released_stages, source HEAD from the git
   files, CONTRACT.json and FREEZE.json digests, strict-boolean `scoring_released` and, if True,
   `owner_scoring_release_ref {path, sha256, scope containing "scoring"}` (the only route to a
   ScoringAuthority).

   **RELEASE.json schema** (`schema: "x4-circle-history-release-v1"`), written by the
   coordinator at `<mailbox>/jobs/<job>/RELEASE.json`:

   | field | type | meaning |
   |---|---|---|
   | schema | str | `"x4-circle-history-release-v1"` |
   | job_id | str | the dispatched job (request.json job_id) |
   | task_sha256 | str | sha256 of that job's task.md (= request.json task_sha256) |
   | released_stages | list[str] | subset of identity, oracle, charts, precision, export, implementation |
   | source_commit | str | 40-hex HEAD of the worktree the runner executes |
   | freeze_sha256 | str | sha256 of `<output_root>/FREEZE.json` |
   | contract_sha256 | str | sha256 of tools/x4_circle_history/CONTRACT.json |
   | scoring_released | bool | strict boolean; false for feasibility |
   | issued_by | str | `"claude-coordinator"` (or historical `"codex-coordinator"`) |
   | coordinator_session_id | str | required for claude-coordinator |
   | coordinator_assumption_ref | {path, sha256} | required for claude-coordinator; under `<mailbox>/archive/` |
   | owner_scoring_release_ref | {path, sha256, scope} | required iff scoring_released is true |
   | stage_ceilings_s | {stage: float} | optional; ignored under the measure-only CPU policy |

   Example (feasibility, job 0018):
   ```json
   {
    "schema": "x4-circle-history-release-v1",
    "job_id": "0018",
    "task_sha256": "<sha256 of jobs/0018/task.md>",
    "released_stages": ["identity", "oracle", "charts", "precision", "export"],
    "source_commit": "<40-hex commit of the frozen build>",
    "freeze_sha256": "<sha256 of FREEZE.json>",
    "contract_sha256": "<sha256 of CONTRACT.json>",
    "scoring_released": false,
    "issued_by": "claude-coordinator",
    "coordinator_session_id": "c351b245-9ff3-4f5c-b324-60ee25725fd7",
    "coordinator_assumption_ref": {
     "path": "X:\\Downloads\\projects\\topo-pilot\\agent-handoff\\archive\\incoming-claude-coordinator-20261014T204705Z\\ASSUMPTION.json",
     "sha256": "91d80ff1f005ef5bf0326fff68d9ab4da27f5a5ae91cf3f5d4623c4c2fad3407"
    }
   }
   ```

2. **CPU measurement only (meter_bind; CONTRACT resources.cpu_policy =
   "MEASURE_ONLY_OWNER_OVERRIDE").** Every run is still metered and recorded in the single ledger
   (child, supervisor, measured, tail and charged CPU; label `<stage>__<label>`), but no stage,
   cumulative or per-run CPU limit stops or refuses a run: the stage limiter has no ceiling,
   meter CAP_S and STOP_NEW_S are unbounded, and `--max-cpu` is unbounded. Unchanged and still
   enforced: release gating of stages (an unreleased stage is still a refused no-op), the
   native-operation wall marker, the owner disk safe-STOP (C: < 2 GB, X: < 30 GB), STOP / INVALID
   controls, the non-hold wall limit (`--max-wall`, default 3600 s), the output cap, threads 1
   and memory 8 GiB. The previous stage_caps_s values stay recorded (history); the policy change
   is recorded in CONTRACT allocation_history and in the ledger metadata by meter_bind in the
   supervisor process, preserving every entry. Methodological bounds are frozen and unchanged:
   lift 30 CPU s per chart, 180 s per native operation, six 512-row constructions, 128 nodes per
   bound.

3. **Phase interval (F4).** chart.apply_gauge and chart.extend return phases in [0, 2π): after
   the modulo, any value ≥ 2π (the float rounding of a tiny negative angle) is replaced by 0.0.
   This is a numerical-correctness fix of the documented [0, 2π) convention; no gate or
   threshold changes.

## Runtime (builder-tested; not part of the independent numerical tests)

- meter_bind.py is the job-0015 binding of the job-0014 meter, winjob and controls modules,
  reused UNCHANGED through module-level rebinding. It adds per-stage ceilings.
- release.py verifies a coordinator release file.
- runner.py is the future stage driver. Without a matching release it refuses every scientific
  stage, and importing it has no side effects.
