# Per-row numerical certificate for the K4 score (job 0016, v2)

Status: SYMBOLIC derivation plus a per-row certificate PROCEDURE. Nothing here has been run on
real arrays. The procedure runs only on released calibration and validation rows, after a
coordinator release. Scored-row certificates are implemented but locked until the owner releases
scoring. The cap is unchanged: every certified score error must be ≤ 1e-4.

Revision history:
- **v1** was the job-0015 draft (sha256 3d12aaf5…). It modelled float64 rounding with
  relative-plus-absolute terms. The coordinator's independent review (jobs/0016/
  coordinator_continuation_review.md) found five defects in it: a circular mass lower bound,
  incomplete DAZ division handling, unproven Decimal slack, an ad-hoc 1+1e-6 multiplier, and
  C versus C2 in norm bounds.
- **v2 replaces the float error MODEL with a finite-row CERTIFICATE.** It is the reviewer's
  candidate approach. For every released row, the float result is compared with an independent
  high-precision reference, and a PROVEN envelope bounds that reference's own error. v2 therefore
  makes no assumption about float64 rounding, BLAS summation order, FMA, underflow or
  flush-to-zero: whatever the float pipeline did is measured, not modelled.

## 1. Targets

For a row with canonical history w_1..w_32 and a model's SAVED extended phase φ (a float64 value,
used as an exact real number):
- The operational process P_op takes the stored float64 T̂, Ê = E_named[:, perm] and π̂ as exact
  real numbers.
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
5. **Reference score.** R = ṽ_x (M̃_32,x − M̃_4,x) + ṽ_y (M̃_32,y − M̃_4,y) at precision q.
6. **Observed discrepancy.** Δ = |Fraction(Decimal(X̂)) − Fraction(R)| in exact rational
   arithmetic. The reference is never converted to float.
7. **Certified bound.** B = Δ + E_ref (§3), an exact rational compared exactly with 1e-4.

Rules for the row:
- **CERTIFIED** iff B ≤ 1e-4.
- **INCONCLUSIVE** (criterion not met) if B is finite and > 1e-4.
- **FAIL_TECHNICAL** on any trap, a nonfinite input, a range violation, or a moment-check
  violation: max_j |m̂_K,j − M̃_K,j| > 1e-10 for K ∈ {4, 32}.

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

**(e) Score.** Write r̃ = M̃_32 − M̃_4 (each coordinate one rounding at precision q) and
r* = M*_32 − M*_4. Then

  |R − X*| ≤ Σ_j |ṽ_j − v*_j|·|r̃_j|                       (unit-vector error)
           + Σ_j |v*_j|·|r̃_j − r*_j|                        (moment error; |v*_j| ≤ 1)
           + γ^(80)_3·Σ_j |ṽ_j r̃_j|                         (two products and one sum)

  with |r̃_j − r*_j| ≤ ε_M,32 + ε_M,4 + u_80·|r̃_j|.

So E_ref = ε_v·Σ_j|r̃_j| + Σ_j(ε_M,32 + ε_M,4 + u_80|r̃_j|) + γ^(80)_3·Σ_j|ṽ_j r̃_j|.

**Rigorous evaluation of the bound itself.**
- Every envelope constant (u, γ, h, ℓ, q, β, ε_c, ε_M and ε_v) is evaluated in EXACT rational
  arithmetic (`fractions.Fraction`).
- Every per-row Decimal quantity enters exactly through Fraction(Decimal), including Decimal(X̂),
  R and r̃.
- So Δ = |Fraction(Decimal(X̂)) − Fraction(R)| is exact, B = Δ + E_ref is an exact rational, and
  the comparison B ≤ 1/10000 is exact.
- No outward-rounding heuristic and no slack multiplier are used.
- The only rounding is inside the reference's own arithmetic, which E_ref covers.

For scale: with S = 144 and L = 32, ε_P ≈ 2·9300·5e-60 ≈ 1e-55, so E_ref is about 1e-54. The
certificate is decided by the observed float discrepancy Δ. E_ref only makes the reference's
own error explicit.

## 4. Decimal cos and sin (precision q = 80, no argument reduction, no π)

Use cos x = Σ_k (−1)^k x^(2k)/(2k)! and sin x = Σ_k (−1)^k x^(2k+1)/(2k+1)!, with |x| < 7.

- **Recurrence.** t_{k+1} = −t_k·x² / ((2k+1)(2k+2)) for cos, and analogously for sin. Each step
  is three correctly rounded operations: x², a product, and a division by an exact integer
  product.
- **Truncation.** Stop after term N, the first index with 2N+2 > |x| (so terms decrease from
  there) and |t_N| < 10^-75. The tail is alternating and decreasing in magnitude, so its
  absolute value is ≤ |t_{N+1}| ≤ |t_N| < 10^-75.
- **Rounding.** The computed t̃_k satisfies |t̃_k − t_k| ≤ γ^(80)_{3k}·|t_k|. The sequential
  summation of N+1 terms adds γ^(80)_{N+1}·Σ|t̃_k|. With Σ_k |t_k| ≤ cosh|x| ≤ e^7:

  ε_v ≤ 10^-75 + (γ^(80)_{3N} + γ^(80)_{N+1}·(1 + γ^(80)_{3N}))·1100,

  This uses the exact rational upper bound 1100 > e^7 ≈ 1096.63, the actual N, and exact
  rational evaluation. The stored φ must satisfy 0 ≤ φ ≤ 6.284 (less than 2π + 1e-3); the
  procedure checks this.

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
- Per categorical draw, TV(q_row, p\*_row) ≤ ½Σ_j(2^-53 + |cum-sum rounding|_j + |p̂_j − p\*_j|).
- Cum-sum rounding is bounded at release from the actual float cumsums against exact rational
  partial sums.
- TV(Q, P\*) ≤ the sum over the 64 draws (π, 32 emissions, 31 transitions).
- ASSUMED: PCG64 output is uniform on its grid.

**Zero-benchmark discrepancy.** For any suffix-only unit g:

  |E_Q[g·(M32 − M4)]| ≤ 2·C2·(ρ_κ − 1) + 2·C2·2·TV(Q, P\*) =: Z_bound, with C2 = max_s‖c*_s‖₂ = 1.

This is reported beside the controls, as the documented deviation of the "population zero". It
is never presented as an exact identity of the sampled data.

## 7. Implemented procedure (error_bound.py) and its locks

```
certify_rows(T, E, pi, canonical32, phi, x_hat, m4_hat, m32_hat, split, scoring_release=None, cap=1e-4)
```

The procedure does the following:
- **Access.** split ∈ {calibration, validation, scoring}. split == "scoring" without a release
  token raises AccessDenied BEFORE any computation.
- **Per row:**
  - reference posteriors for K ∈ {4, 32}, cached by canonical-history digest;
  - exact-feature moments;
  - the moment check (≤ 1e-10);
  - ṽ and ε_v;
  - R, Δ, E_ref and B.
- **Returns** per-row B, Δ, E_ref, the moment-check maxima and status counts, plus the overall
  status CERTIFIED / INCONCLUSIVE / FAIL_TECHNICAL. It returns no endpoint aggregate.
