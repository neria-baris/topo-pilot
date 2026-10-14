# Per-row numerical certificate for the K4 score (job 0016, v2.2)

Status: SYMBOLIC derivation plus a per-row certificate PROCEDURE. Nothing here has been run on
real arrays. The procedure runs only on released calibration and validation rows, after a
coordinator release. Scored-row certificates are implemented but locked until the owner releases
scoring. The cap is unchanged: every certified score error must be ≤ 1e-4.

Revision history:
- **v2.2** applies the reference-final, pipeline-freeze and generating-law
  reviews (sections 8 and 9): separate exact even/odd Taylor series bounds, process-bound
  validated reference keys, exact gap comparison, a persisted verified reference, and the
  implemented process-law bound under an explicitly IDEALIZED sampling law.
- **v1** was the job-0015 draft (sha256 3d12aaf5…). It modelled float64 rounding with
  relative-plus-absolute terms. The coordinator's independent review (jobs/0016/
  coordinator_continuation_review.md) found five defects in it: a circular mass lower bound,
  incomplete DAZ division handling, unproven Decimal slack, an ad-hoc 1+1e-6 multiplier, and
  C versus C2 in norm bounds.
- **v2.1** (this version) applies the six corrections of jobs/0016/NUMERICAL_V2_STATIC_REVIEW.md:
  1. the reference score and residuals are assembled in exact rationals;
  2. the Taylor tail uses exact rational term bounds with a fixed, verified N;
  3. the operational phase check is separated from the analytic interval;
  4. the sampling TV bound uses both adjacent CDF-boundary errors;
  5. score certificates come after the chart transform;
  6. the K1 four-lowest-row references are kept explicitly.
- **v2 replaces the float error MODEL with a finite-row CERTIFICATE.** It is the reviewer's
  candidate approach. For every released row, the float result is compared with an independent
  high-precision reference, and a PROVEN envelope bounds that reference's own error. v2 therefore
  makes no assumption about float64 rounding, BLAS summation order, FMA, underflow or
  flush-to-zero: whatever the float pipeline did is measured, not modelled.

## 1. Targets

For a row with canonical history w_1..w_32 and a model's SAVED extended phase φ (a float64 value,
used as an exact real number):
- The operational process P_op is the normalised stored-weight likelihood calculation. The
  stored float64 T̂, Ê = E_named[:, perm] and π̂ are taken as exact real numbers. These stored
  weights need not define an exactly stochastic or stationary process: M*_K is simply the
  normalised suffix-likelihood-weighted mean that the job-0014 filter computes in exact
  arithmetic. The stationary generating law and the sampling law are treated separately in §6.
- The exact features are c*(s) = (cos(2πx_s/12), sin(2πx_s/12)), with x_s = coords[s, 0].
- M*_K is the exact posterior mean of c* given the last K observations under P_op, using the
  restart-at-π̂ suffix filter of CONTRACT.json.
- v* = (cos φ, sin φ) is computed EXACTLY for the binary value of φ.
- The target score is X* = v* · (M*_32 − M*_4).

These are the definitions the certificate bounds. The saved φ DEFINES the operational chart.
How well that chart approximates any ideal topological map is a separate question, outside this
bound. The process-law approximation (§6) is also separate.

The computed score X̂ comes from the actual float pipeline:
- the job-0014 `suffix_posterior` and `posterior_means`, reused unchanged;
- the float `circle_features`;
- û = (np.cos φ, np.sin φ);
- `scores`.

## 2. Independent reference R and the certified bound

All reference arithmetic runs inside a caller-owned context, `trapping_context(prec)`. This
follows jobs/0016/DECIMAL_REFERENCE_REVIEW.md. The context sets the following EXPLICITLY:
- rounding ROUND_HALF_EVEN;
- Emin = −999999, Emax = 999999 and clamp = 0;
- traps ON for Underflow, Subnormal, Overflow, Clamped, InvalidOperation and DivisionByZero;
- traps OFF for Inexact and Rounded, which are expected, and for FloatOperation, so the
  intentional exact `Decimal(float)` constructors are allowed.

The unchanged job-0014 reference uses `localcontext()` and sets only the precision, so it
inherits all of these settings. After each reference call the procedure also checks the context
flags for Underflow, Subnormal and Overflow. Any trap or flag makes the row FAIL_TECHNICAL.

Exponent reasoning, which a test verifies:
- **Lower end.** Every input is a nonnegative binary64 value ≤ 1 with positive values
  ≥ 2^-1074. A positive forward path multiplies at most 2L ≤ 64 such factors, so every nonzero
  product is ≥ 2^-68736 ≈ 10^-20692. That is far above 10^Emin.
- **Upper end.** Every unnormalised forward value is ≤ (max row sum)^L ≤ 1.000001, moments
  satisfy |·| ≤ 1, and Taylor terms are ≤ e^7. That is far below 10^Emax.
- Under- and overflow are therefore excluded by construction for valid inputs, and checked by
  traps and flags rather than assumed.

1. **Posteriors.** P̃_K = `decimal_suffix_posterior(T̂, Ê, π̂, last K tokens, digits=60)` for
   K ∈ {4, 32}. This is the job-0014 independent reference, reused UNCHANGED. Its own
   `localcontext()` inherits the enclosing traps and sets the precision to p = 60.
2. **Features.** c̃_s are exact algebraic values computed at precision q = 80. x_s ∈ {0..11}
   gives cos/sin of multiples of π/6, so every coordinate is one of 0, ±1, ±1/2 or ±√3/2. √3 is
   computed with Decimal `sqrt`, which is correctly rounded, then halved.
3. **Moments.** M̃_K = Σ_s P̃_K,s · c̃_s, accumulated in index order at precision q.
4. **Unit vector.** ṽ = (cos, sin) of x = Decimal(φ), which is exact, by a Taylor series at
   precision q (§4). The procedure requires 0 ≤ φ < 2π, and so |x| < 7.
5. **Reference score.** R is assembled EXACTLY in rationals. With r̃_j = Fraction(M̃_32,j) −
   Fraction(M̃_4,j), R = Σ_j Fraction(ṽ_j)·r̃_j. No Decimal subtraction or dot rounding is used.
6. **Observed discrepancy.** Δ = |Fraction(Decimal(X̂)) − Fraction(R)| in exact rational
   arithmetic. The reference is never converted to float.
7. **Certified bound.** B = Δ + E_ref (§3), an exact rational compared exactly with 1e-4.

Rules for the row:
- **CERTIFIED** iff B ≤ 1e-4.
- **INCONCLUSIVE** (criterion not met) if B is finite and > 1e-4.
- **FAIL_TECHNICAL** on any trap or flag, a nonfinite input, an operational phase-range
  violation, or a moment-check violation: max_j |m̂_K,j − M̃_K,j| > 1e-10 for K ∈ {4, 32}.

**Phase ranges.**
- The OPERATIONAL check is the canonical chart range: 0 ≤ φ < 2π_float, where 2π_float =
  2·np.pi as float64. It is a defect check.
- The ANALYTIC Taylor interval used in §4 is the wider rational interval [0, X_max] with
  X_max = 6284/1000 > 2π_float. That interval does not by itself enforce the chart range.

The moment check implements the contract's reference tolerance on EVERY released row, not only
on four selected rows.

## 3. Reference envelope E_ref ≥ |R − X*|

Notation:
- For Decimal precision n digits, u_n = ½·10^(1−n), a bound on the relative error of one
  correctly rounded operation.
- γ^(n)_k = k·u_n / (1 − k·u_n).
- Conversions `Decimal(float)` are exact.

**(a) Posterior (p = 60, unnormalised forward summation, all terms nonnegative).** This
follows the conservative path count of DECIMAL_REFERENCE_REVIEW.md.
- **Operation count.** Step 1 is one product per state. Each later step forms S products
  α_i·T_ij and S additions (the sum starts from Decimal(0)), then one emission product.
- **Path factor.** That gives at most N = 1 + (L − 1)(2S + 2) correctly rounded operations per
  positive path. With v = u_60 and h = γ^(60)_N, positivity gives
  α̃_i ∈ [(1 − h)α_i, (1 + h)α_i], and exact zeros stay zero.
- **Final normalisation.** One S-term sum (t = γ^(60)_S) and one division (v). With
  ℓ = (1−h)(1−v)/((1+h)(1+t)) and q = (1+h)(1+v)/((1−h)(1−t)), each P̃_s/P*_s ∈ [ℓ, q].
- **Result.** ‖P̃ − P*‖₁ ≤ β := max(1 − ℓ, q − 1), and componentwise
  |P̃_s − P*_s| ≤ β·P*_s.

**(b) Features.** |c̃_s,j − c*_s,j| ≤ ε_c = 2u_80: sqrt rounding plus one halving. 0, ±1 and ±1/2
are exact. Every |c*_s,j| ≤ 1, because the exact features lie on the unit circle; no float
feature norm is assumed.

**(c) Moment, per coordinate j** (precision 80; each P̃_s·c̃_s,j product is rounded and the S
terms are summed from 0). With Σ_s P*_s = 1 and |c*| ≤ 1:

  |M̃_K,j − M*_K,j| ≤ β + (1 + β)·ε_c + (1 + β)(1 + ε_c)·γ^(80)_{2S+2} =: ε_M,K.

This absolute bound covers signed cancellation.

**(d) Unit vector, per coordinate.** |ṽ_j − v*_j| ≤ ε_v (§4).

**(e) Score.** r̃ = M̃_32 − M̃_4 and R = ṽ·r̃ are EXACT rationals (§2), and r* = M*_32 − M*_4.
Then

  X* − R = Σ_j (v*_j − ṽ_j)·r̃_j + Σ_j v*_j·(r*_j − r̃_j),

so

  |R − X*| ≤ ε_v·Σ_j |r̃_j| + Σ_j (ε_M,32 + ε_M,4),

using |v*_j| ≤ 1 and |r*_j − r̃_j| ≤ ε_M,32 + ε_M,4, since r̃ is unrounded.

E_ref := ε_v·Σ_j |r̃_j| + 2·(ε_M,32 + ε_M,4).

For scale: with S = 144 and L = 32, β ≈ 2·9200·5e-60 ≈ 1e-55, so E_ref is about 1e-54. The
certificate is decided by the observed float discrepancy Δ. E_ref only makes the reference's
own error explicit.

## 4. Decimal cos and sin (precision q = 80, no argument reduction, no π)

Use cos x = Σ_k (−1)^k x^(2k)/(2k)! and sin x = Σ_k (−1)^k x^(2k+1)/(2k+1)!, with
0 ≤ x ≤ X_max = 6284/1000. Here x = Decimal(φ) is exact, and Fraction(x) is its exact rational
value.

- **Fixed term count.** N = 48. The sums run over k = 0..48. Two facts are verified EXACTLY in
  rational arithmetic, at import time and in the tests:
  - **Monotone tail.** The ratio of successive term magnitudes beyond N is below 1:
    X_max²/((2N+3)(2N+4)) < 1 for cos and X_max²/((2N+4)(2N+5)) < 1 for sin. The neglected
    tails are alternating with decreasing magnitude.
  - **Tail size.** The exact tails are bounded by their first neglected term:
    T_cos = X_max^(2N+2)/(2N+2)! and T_sin = X_max^(2N+3)/(2N+3)!. Both are < 10^-75 (checked
    as exact rationals: X_max^98/98! < 10^-75 and X_max^99/99! < 10^-75).

  Neither the stopping rule nor the tail bound uses computed terms.
- **Term rounding enclosure (proved).** The terms are computed by the recurrence
  t̃_{k+1} = fl(fl(t̃_k·x̃₂)/m_k), with x̃₂ = fl(x·x) computed once and m_k an exact integer
  (sin starts from t̃_0 = x, which is exact). Each term carries a relative factor in
  (1 ± γ^(80)_{3k}) against the exact t_k: x̃₂ contributes one rounding, and the product and
  division contribute one each per step. So |t̃_k − t_k| ≤ γ^(80)_{3N}·|t_k| for k ≤ N.
- **Summation.** Sequential summation of N + 1 computed terms in Decimal(80), starting from 0,
  adds at most γ^(80)_{N+1}·Σ_k|t̃_k|. The magnitudes satisfy Σ_k |t_k| ≤ cosh(X_max) ≤ A := 270.
  A is verified exactly: the rational partial sum Σ_{k=0}^{2N+3} X_max^k/k! plus its tail bound
  is ≤ 540, so cosh(X_max) ≤ 270.
- **Result (per coordinate, exact rational):**

  ε_v = max(T_cos, T_sin) + γ^(80)_{3N}·A + γ^(80)_{N+1}·(1 + γ^(80)_{3N})·A.

## 5. What is and is not assumed

**Assumed:** Python `decimal` (libmpdec) correctly rounds +, −, ×, ÷ and sqrt to the context
precision and raises the enabled traps, as the General Decimal Arithmetic specification states.
Independent tests check the reference and trigonometric routines against exact rational and
known values. That is evidence, not a proof of the library.

**NOT assumed:**
- any property of float64 arithmetic, BLAS, FMA, subnormals or FTZ/DAZ;
- library accuracy of `np.cos` or `np.sin`;
- that float features have unit length.

Every such effect is inside the measured Δ.

**Coverage:** EVERY released calibration and validation row, for each model's φ. Agreement on
selected rows is never treated as a global bound.

**Cost:**
- Targets M_K depend only on the canonical history, the shared T̂, π̂ and the identical canonical
  Ê. The job-0014 check found spread 0.0 across models; that must be re-verified at release. So
  the reference posteriors are computed once per unique sequence_id: 1024 cal/val histories.
- The unit vectors and scores are per model: 3072 trigonometric evaluations, which are cheap.
- The job-0014 dense reference is O(L·S²). Its synthetic per-step cost at S = 144 is measured in
  job 0016 and projected against the 400 CPU-second oracle ceiling (report §Costs). If the
  projection does not fit, that is reported before release, and the coordinator decides.

## 6. Process-law approximation (separate; reported, not part of the score certificate)

**Documented generating law P\*:**
- T\* is the lazy max-degree walk on the 12×12 x-periodic lattice: 1/5 per neighbour and
  1 − deg/5 on the diagonal. It is symmetric with rows summing to 1, so it is doubly
  stochastic, and the uniform law π\* = 1/144 is EXACTLY stationary.
- Ê\* is the exact softmax over the 6×6 grid centres with σ = 5/4 on the x-periodic flat chart.
- The suffix-only zero identity E[g(S4)·(M32 − M4)] = 0 holds EXACTLY for P\*.

**Stored parameters versus P\*** (instantiated once at release, from metadata-identified stored
arrays):
- κ = max of the entrywise RELATIVE errors of T̂, Ê and π̂ against P\*, with identical zero
  patterns required.
- T̂ and π̂ are compared by exact rational comparison.
- Ê is compared against a 60-digit Decimal softmax rebuild, with its own rounding envelope.
- The same nonnegative-product argument as §3(a) bounds the exact-arithmetic posterior change:
  ‖P_op − P_{P\*}‖₁ ≤ ρ_κ − 1, with ρ_κ = ((1 + κ)/(1 − κ))^(2L+1).

**Sampling law Q of the E4 data.** dataset.HMMSampler in canonical order (stage.py), using the
inverse CDF of float cumsums with the last positive entry set to 1, and `rng.random()` on the
2^-53 grid.
- **Per categorical draw.** Let C_j = Σ_{i≤j} p̂_i be the exact rational partial sums of the
  stored row, and Ĉ_j the stored float CDF after the last-positive substitution (Ĉ_j = 1 from
  the last positive index on). Let e_j = Ĉ_j − C_j, with e_{−1} = 0.
  - The sampler returns j iff u ∈ [Ĉ_{j−1}, Ĉ_j), with u uniform on the grid {k·2^-53}.
  - So its probability is q_j = (number of grid points in that interval)·2^-53, and
    |q_j − (Ĉ_j − Ĉ_{j−1})| ≤ 2^-53: grid quantisation of the two endpoints together.
  - Hence |q_j − p\*_j| ≤ |e_j| + |e_{j−1}| + 2^-53 + |p̂_j − p\*_j|, and

    TV(q_row, p\*_row) ≤ ½ Σ_j (|e_j| + |e_{j−1}| + 2^-53 + |p̂_j − p\*_j|).
- The e_j are computed EXACTLY at release, from the stored float CDF against exact rational
  partial sums.
- TV(Q, P\*) ≤ the sum over the 64 draws (π, 32 emissions, 31 transitions).
- ASSUMED: PCG64 output is uniform on its grid.

**Zero-benchmark discrepancy.** For any suffix-only unit g:

  |E_Q[g·(M32 − M4)]| ≤ 2·C2·(ρ_κ − 1) + 2·C2·2·TV(Q, P\*) =: Z_bound, with C2 = max_s‖c*_s‖₂ = 1.

This is reported beside the controls, as the documented deviation of the "population zero". It
is never presented as an exact identity of the sampled data.

## 7. Implemented procedure (error_bound.py), gate placement and locks

Gate placement (CONTRACT gates):
- **Early "process_and_reference" gate (no chart needed):**
  - (i) the explicit FOUR-lowest-history-ID references for K ∈ {1, 4, 32}, per model and per
    split (calibration and validation), with max moment error ≤ 1e-10;
  - (ii) the all-row K4/K32 moment checks ≤ 1e-10 for every released row.

  Canonical reference results may be shared across models ONLY after the exact process
  equality and cross-model history equality checks pass.
- **"row_score_certificates" gate.** It runs after the chart, extension, fidelity, bins and
  resultant gates, because it needs the saved φ. Calibration rows use the gauged landmark
  phases; validation rows use the extended phases. It precedes B4 and precision.

```
reference_check_rows(T, E, pi, coords, canonical32, m_hat, Ks, cache=None) -> dict
certify_rows(T, E, pi, coords, canonical32, phi, x_hat, m4_hat, m32_hat, split,
             scoring_release=None, cap=1e-4, cache=None) -> dict
```

reference_check_rows performs the early moment checks: every row, every K in Ks, with
|m̂ − M̃| ≤ 1e-10. It needs no phase.

certify_rows does the following:
- **Access.** split ∈ {calibration, validation, scoring}. split == "scoring" without a release
  token raises AccessDenied BEFORE any computation (this applies to both functions).
- **Per row:**
  - the operational phase check;
  - reference posteriors for K ∈ {4, 32}, cached by canonical-history digest;
  - exact-feature moments;
  - the moment check (≤ 1e-10);
  - ṽ and ε_v;
  - exact-rational R, Δ, E_ref and B.
- **Returns** per-row B, Δ, E_ref, the moment-check maxima and status counts, plus the overall
  status CERTIFIED / INCONCLUSIVE / FAIL_TECHNICAL. It returns no endpoint aggregate.

## 8. v2.2 corrections (reference-final and pipeline-freeze reviews; normative)

**Taylor verification (corrects §4).** For first ∈ {0, 1} define the complete positive series
S_first = Σ_{k≥0} X^(2k+first)/(2k+first)! (cosh X and sinh X). For k > N the term ratio
t_{k+1}/t_k = X²/((2k+1+first)(2k+2+first)) decreases in k (erratum 2026-10-14: the first v2.2 text wrote (2k+2+first)(2k+3+first); r below was and is correct), so with
r = X²/((2N+3+first)(2N+4+first)) < 1,

  S_first ≤ Σ_{k≤N} t_k + t_{N+1}/(1 − r)   (exact rationals).

Both bounds must be ≤ A = 270. The cos/sin remainders alternate with decreasing magnitude
beyond N, so by Leibniz each is bounded by its first neglected term (T_cos, T_sin < 1e-75). The
rounding terms use Σ_{k≤N}|t_k| ≤ S_first ≤ A. The earlier draft compared partial + T_cos with
2A, which did not bound each series separately.

**Reference binding (corrects §7).** References are keyed by (process digest of T, E, pi,
coords; K; int64 history bytes) after validating the histories (integer dtype, 0..V−1, shape
[n, 32]) BEFORE any conversion. Moment gaps are compared EXACTLY with Fraction(1, 10^10). The
oracle stage persists the Decimal moments as strings with their process, feature and source
identities and the per-model/split row table (history_id, sequence_id, panel, history bytes);
the charts stage verifies that file and runs the certificate with cache_only (no silent
recomputation, no float conversion of a reference). Cost: the all-row references are computed
once per unique canonical history and charged to the oracle stage only.

**Decimal contexts.** Traps propagate into nested contexts; flags do not, so the outer flag
inspection covers only outer operations, and the nested reference is protected by the traps.

## 9. Process-law approximation: implemented procedure (process_law.py; completes §6)

Follows the coordinator's static generating-law review (message 01C0116D…), which confirmed
canonical sampling then renaming and emission-before-transition indexing against the unchanged
dataset/sampler.py, dataset/stage.py and process/emission.py. Inputs: the stored float arrays
T̂ (144×144), Ê_canon (144×36), π̂ (144) and coords, read as exact reals. Nothing is sampled and
the sampler is neither edited nor rerun.

1. **Documented law P\* and its identities.** States s ↔ (x, y) = (s // 12, s mod 12), required
   exactly. T\*: 1/5 per neighbour (x ± 1 mod 12 with equal y; y ± 1 with equal x, y not
   periodic), 1 − deg/5 on the diagonal. π\* = 1/144. Verified EXACTLY in rationals: T\*
   symmetric, rows sum to 1, π\* T\* = π\*. Ê\*: softmax over the 36 centres (1/2 + 2a, 1/2 + 2b),
   column j = 6a + b, logits −8d²/25 (σ = 5/4) with the x-periodic flat distance.
2. **Required conditions.** κ < 1; T̂ has exactly the zero support of T\*; every Ê and π̂ entry
   is strictly positive (E\*, π\* are positive). Stored rows need NOT be exactly stochastic: the
   posterior is the normalised stored-weight calculation. Any failure makes the bound
   UNAVAILABLE with its exact reason; nothing is then claimed about the zero benchmark.
3. **Rigorous softmax enclosure.** d² is an exact quarter-integer and the logit −8d²/25 an
   exact finite decimal (Inexact trapped). In a trapping 60-digit context, n_j = exp(logit_j)
   (allowed relative error 2u; correct rounding is not relied on), D = Σ n_j from Decimal(0)
   (≤ 36 roundings), E_dec = n_j/D (one rounding). With u = ½·10^(−59),
   lo = (1−2u)(1−u)/((1+2u)(1+u)^36) and hi = (1+2u)(1+u)/((1−2u)(1−u)^36), every exact E\*
   lies in the positive interval [E_dec/hi, E_dec/lo]. The stored float geometry/log-sum-exp
   error enters only through comparing the stored Ê with that interval; the stored builder is
   never treated as exact.
4. **κ (exact).** κ_T = max_{T\*>0}|T̂ − T\*|/T\*, κ_π = 144·max|π̂ − 1/144|,
   κ_E = max max(|Ê − E_dec/hi|, |Ê − E_dec/lo|)/(E_dec/hi); κ = max. ρ_κ − 1 =
   ((1+κ)/(1−κ))^(2L+1) − 1 with L = 32; a length-L positive path has 2L factors, so 2L+1 is
   conservative.
5. **Sampler thresholds and the exact comparison-count law.** The actual `_draw` returns
   j = min(#{i : c_i ≤ u}, V−1), counting successful threshold comparisons; raw float cumsums
   can exceed 1 before the last-positive substitution. The thresholds c come from the ACTUAL
   `_cumulative_rows` (frozen file). For the proof they are clamped, c' = min(max(c, 0), 1),
   which is observationally identical for u ∈ [0, 1). With s = sorted(c'), s_{−1} = 0 and
   G(x) = min(max(⌈x·2^53⌉, 0), 2^53), the exact law of N = #{i : c'_i ≤ u} on the grid
   u = k·2^−53 is P(N = j) = (G(s_j) − G(s_{j−1}))·2^−53 (j < V) and P(N = V) = 1 − G(s_{V−1})·2^−53;
   q_j = P(N = j) for j < V−1 and q_{V−1} = P(N = V−1) + P(N = V). When c' is nondecreasing with
   c'_{V−1} = 1 this is the adjacent-interval law of §6, and the v2.1 formula
   ½Σ_j(|e_j| + |e_{j−1}| + 2^−53 + dev_j) with e_j = c'_j − Σ_{i≤j} p̂_i is also reported;
   otherwise that formula is marked not applicable and only the exact law is used.
6. **Per-draw TV and Z_bound.** TV(q_row, p\*_row) ≤ ½Σ_j(|q_j − p̂_j| + dev_j), with
   dev_j ≥ |p̂_j − p\*_j| exact for T and π and max(|Ê − E_dec/hi|, |Ê − E_dec/lo|) for E. Then
   TV(Q, P\*) ≤ tv_π + 32·max_s tv_E + 31·max_s tv_T, and Z_bound = 2(ρ_κ − 1) + 4·TV(Q, P\*)
   (C2 = 1).
7. **Idealisation (stated, not proved).** Q is the IDEALIZED sampling law: independent uniform
   53-bit draws across every relevant sampler call and trajectory, and independent
   panel-assignment randomness. Uniform marginal outputs alone would not justify the 64-step
   coupling or independent trajectories. Z_bound bounds |E_Q[g·(M32 − M4)]| for that
   idealization, covering the parameter, CDF and grid discrepancy only; it does not bound
   deterministic PRNG bias or correlation and does not establish an exact zero for the fixed
   saved data. It is reported beside the controls, is not a gate, and changes no threshold.
   Also assumed: libmpdec rounds +, −, ×, ÷ correctly (§5).
