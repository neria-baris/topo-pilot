STATUS: FREEZE_READY

# C1 numerical certificate: replacement §15.3 (planning track L, request `coord-c1-numcert-20261015`)

**Readiness.** The proof below is complete for the computation it prescribes. Freeze still needs two things:
- the independent review that the protocol requires for §15.3;
- the coordinator's confirmation of two computational prescriptions made inside the certificate (open questions 1 and 2).

Neither prescription changes the science, a threshold, a seed or a gate order.

**Basis (read-only).**
- `C1-MERGED-v2.md`, §15.3 and the sections it touches.
- Review `coord-c1-merged-review-20261015.codex.md`, required change 6, read in full.
- Code at main @4f219d6:
  - `src/topo_pilot/oracle/_filter.py` and `_common.py` (`BayesFilter.run`, `normalise_rows`);
  - `src/topo_pilot/learner/model.py`;
  - `tools/x4_circle_history/error_bound.py` and `ERROR_BOUND.md` v2.2;
  - `tools/x4_oracle_profile/oracle_profile.py` (`bootstrap_profile`, `percentile_interval`);
  - `tests/oracle_profile/independent_reference.py`;
  - numpy 2.2.6 (pinned in `requirements.lock`): `_quantile` (`inverted_cdf` has `fix_gamma=None`, so the element is *taken*, with no interpolation) and `_methods._mean` (`umr_sum` followed by `true_divide`).

No code was run, no test was executed, and no data or payload was opened.

---

## 1. Summary (≤ 250 words)

The certificate is a Higham-style forward error analysis of the actual float64 computation plus cheap per-row checks; no all-row Decimal filtering.

**Oracle.** Every filter quantity is positive. Errors are therefore tracked as the oscillation of componentwise log-ratios, which is the Hilbert projective metric:
- an exact positive linear map never increases this oscillation;
- normalisation removes the common factor;
- each filter step adds the width of at most N+2 roundings.

For the 32-step `BayesFilter` and the T·E prediction, this proves |log q̂(v) − log q*(v)| ≤ ρ_q = 9486·u/(1−u) ≈ 1.053·10⁻¹² for **every** symbol v, however small q(v) is. The one precondition, P1, is that no posterior entry falls below about 10⁻²⁸⁰, so nothing underflows. P1 is checked per history. A history that fails it gets a validated K4-style Decimal enclosure instead.

**Post-logit.** A is evaluated as ½Σ(q̂⁺−q̂⁻)(z⁺−z⁻) directly from the recorded logits. The log-softmax normaliser cancels except for a proved residual of at most ω_TE·‖Δz‖∞. No exp or log enters A, so 2⁻⁴⁴ is not needed. G uses 72 logs per row; each is checked against a correctly rounded 40-digit Decimal ln.

**Bounds.**
- Explicit per-row bounds b^A, b^G, b^Y, b^Z and b^Zfull.
- r^mean = γ_n·max|Ẑ|.
- An order-statistic lemma carries these bounds to the bootstrap bounds.
- Every bound is inflated outward and compared in exact rationals.
- Signed guards cover H5 and V3.

**Size.** Projected B_num,j is 10⁻¹¹ to 10⁻¹⁰ against a 0.10·Ḡ margin of 10⁻³ to 10⁻². The 10⁻⁹ floor binds; P(INCONCLUSIVE/NUMERICAL) ≲ 10⁻⁴. Cost: under 0.1 CPU-h.

---

## 2. Replacement text for §15.3 (complete; replaces the v2 §15.3 in full)

### 15.3 Numerical certificate

**Status: PROOF ATTACHED. Before freeze it must pass the independent review the protocol requires.**

#### 15.3.1 What is certified, and against what

**Certified decisions.**
- **(E)** The per-model endpoint statuses PASS_j, FAIL_j and INC_j, through L_j and U_j (§12.3, §13).
- **(H)** The headroom gate H5 on validation and on fresh rows (§3.5).
- **(V)** The positive-control gate V3 on validation and on fresh rows (§11).

**Exact-arithmetic counterpart.** For each certified decision, D* is the decision obtained by evaluating the declared formulas in exact real arithmetic on exactly the same inputs:
- the stored float64 arrays T̂, Ê_canon and π̂, read as exact reals. This is the operational oracle of §3.3; the stored rows need not be exactly stochastic;
- the recorded float64 logits, read as exact reals. These are the operational model output (§15.1);
- the operationally eligible rows (§4);
- the same bootstrap index draws;
- the same order-statistic index that numpy's `inverted_cdf` selects for the declared tail probability.

The exact quantities, per donor history h ∈ {H⁺_i, H⁻_i}, are:
- b*_t, the exact normalised forward filter. Its unnormalised vector g_t is defined by g_1 = π̂ ⊙ Ê[:, w_1] and g_{t+1} = (b*_t T̂) ⊙ Ê[:, w_{t+1}]; then b*_t = g_t / Σ g_t;
- q* = b*_32 T̂ Ê;
- G* = ½ Σ_v (q*⁺ − q*⁻)(v)·(log q*⁺(v) − log q*⁻(v));
- for each arm X, ℓ*_X = z_X − lse(z_X), the exact log-softmax of the recorded logits;
- A*(X) = ½ Σ_v (q*⁺ − q*⁻)(v)·(ℓ*_{X⁺}(v) − ℓ*_{X⁻}(v));
- Y*, Z* = Y* − (1/10)G* and Z*_full = A*_full − (3/10)G*;
- the bootstrap means m*, and the order statistics L*, U* and lower*.

Theorem 6 (§15.3.11) proves that whenever the signed guards of §15.3.11 pass, the computed decision equals D*.

**Operational, not certified.** The following are deterministic rules applied to computed float64 values, recorded as computed:
- eligibility and s_max;
- κ_ν;
- every fit (FWL, Σ_W, decoders, chart);
- the M, F, V1 and V2 gates;
- the P1 ladder;
- θ̂ and every secondary quantity.

They define the population, the frozen objects or the test size. A numerical perturbation of them changes *which* valid quantity is assessed. It cannot make a certified decision about that quantity wrong. The statistical meaning of L* and U* (nominal levels, §13) is unchanged; this section concerns arithmetic only.

#### 15.3.2 Permitted computation (prescribed; the implementation must use exactly these expressions)

- **C1 Oracle.** `oracle.BayesFilter(T̂, Ê_canon, π̂).run(tokens)` unchanged, on the canonical H⁺ and H⁻. q̂^± = `q[:, 32]` and b̂_t = `b[:, t−1]`.
- **C2 Logs.** ℓ̂^± = `np.log(q̂^±)`, stored as float64 arrays and measured as in §15.3.6.
- **C3 G.** Ĝ = `0.5 * np.sum((q̂⁺ − q̂⁻) * (ℓ̂⁺ − ℓ̂⁻), axis=-1)` in canonical order, computed **once per row**. This Ĝ is the value used by H5, V3, Z, Z_full and θ̂ for all three models. The per-model named-order G values serve only the H3 cross-model identity check.
- **C4 A (logit-difference form).** For an arm pair X = (X⁺, X⁻), with recorded float64 logits gathered into canonical order (the gather is exact):
  - d̂ = `q̂⁺ − q̂⁻` (the same array as in C3);
  - Δ̂ = `z_{X⁺} − z_{X⁻}`;
  - Â = `0.5 * np.sum(d̂ * Δ̂, axis=-1)`.

  A_full uses the same form with the donor logits.
- **C5 Y.** Ŷ = Â_T − `np.mean(Â_C, axis=<frame axis>)`, over the 32 frames.
- **C6 Z.** Ẑ = `Ŷ − 0.1 * Ĝ` and Ẑ_full = `Â_full − 0.3 * Ĝ`.
- **C7 Means and quantiles.**
  - Bootstrap means are `np.mean(x[idx])` per draw: the endpoint kernel (§12.3) and the reused `bootstrap_profile`.
  - Quantiles come from `np.quantile(..., method="inverted_cdf")`. At numpy 2.2.6 this returns an input element bitwise (`fix_gamma=None` takes the element, with no interpolation).

The float64 log-softmax is **not** on the certified path. It is computed only for secondary quantities and for the tail-path identity check of §5.4.

#### 15.3.3 Assumptions and checked preconditions

**Assumptions (not checkable from within the run; stated in full).**
- **A1 (IEEE arithmetic).**
  - Every float64 operation is an IEEE 754 binary64 operation with round-to-nearest, or a fused multiply-add rounded once, executed with SSE2/AVX (no x87 extended precision).
  - **Normal range.** If every operand and the exact result are 0 or of magnitude ≥ 2⁻¹⁰²², then fl(x∘y) = (x∘y)(1+δ) with |δ| ≤ u = 2⁻⁵³. Multiplication by 0.5 is exact. A difference with a subnormal result is exact or flushed.
  - **Below the normal range.** If an operand or the exact result is below 2⁻¹⁰²² in magnitude, the absolute error is at most 2⁻¹⁰⁰⁰·max(1, |other operand|). This covers gradual underflow, flush-to-zero and denormals-are-zero. Nothing is assumed about which of these modes is active.
- **A2 (reductions, including BLAS).** For every output entry of `np.matmul` (OpenBLAS or any other backend) and of `np.sum`/`np.mean`, the computed value is some binary tree of A1 operations: any order, blocking, vectorisation or thread split, and no Strassen-type algorithm. Consequences (Higham, *Accuracy and Stability*, Lemmas 3.1 and 3.3, §3.1, §2.6 for fma):
  - a dot product of nonnegative length-n vectors, in the normal range, equals Σ x_k y_k (1+θ_k) with (1−u)ⁿ ≤ 1+θ_k ≤ (1+u)ⁿ;
  - a sum of n nonnegative terms obeys the same bracket with n−1;
  - for signed terms, |fl(Σ t_k) − Σ t_k| ≤ γ_{n−1} Σ|t_k| for sums and γ_n Σ|x_k y_k| for dot products.

  Wider internal accumulation also satisfies these brackets. BLAS is used only for the filter's matrix products. Every reduction in C3–C7 is numpy's own `add.reduce`.
- **A3 (Decimal).** libmpdec rounds +, −, ×, ÷ and `ln` correctly at the context precision, and raises the enabled traps (Python `decimal` documentation; General Decimal Arithmetic specification). This is K4's trust base (ERROR_BOUND.md §5), extended to `ln`. Only "error ≤ one unit in the last digit" is used.
- **A4 (exact helpers).** Python `int`/`Fraction` arithmetic is exact. `float(Fraction)` rounds correctly to nearest, and `math.nextafter` is exact.

**Not assumed:**
- the accuracy of `np.log`, `np.exp`, libm, SVML, torch or any log-softmax;
- the floating-point mode (gradual underflow versus FTZ/DAZ);
- that the stored T̂ and Ê rows sum to exactly 1;
- any property of the model forward pass, since logits are the recorded operational output.

**Preconditions (checked; each failure has a fixed status).**
- **P0 (structural; once, at H1, in exact rationals on the stored arrays).** All of the following:
  - Ê_canon > 0 entrywise;
  - π̂ > 0;
  - T̂ ≥ 0 with a strictly positive diagonal;
  - the shapes N = 144 and V = 36 are read from the arrays;
  - π_min·ε_E ≥ 2⁻¹⁰⁰⁰ and τ⁺·ε_E ≥ 2⁻¹⁰⁰⁰, where ε_E = min Ê_canon, π_min = min π̂ and τ⁺ = the minimum positive entry of T̂.

  ω_TE (§15.3.4) is computed alongside. Failure → FAIL_TECHNICAL/IDENTITY.
- **P1 (per donor history h; validation at S3 and test inside T-PRE).**
  - Every entry of every stored b̂_t (t = 1..32) is finite.
  - ν_min(h) := min_{t,z} b̂_t(z) ≥ ν₀ := 2⁻¹⁰⁰⁰ / (τ⁺·ε_E). With τ⁺ = 0.2 and ε_E ≈ 2·10⁻²⁰, ν₀ ≈ 2·10⁻²⁸¹; the exact value comes from P0.

  Failure is **not** an error: history h is certified by route F (§15.3.7).
- **P2 (per certified row and model).** All of the following:
  - every logit used is finite with |z| ≤ 2¹⁹;
  - q̂ is finite and > 0;
  - ℓ̂ is finite;
  - Â, Ĝ, Ŷ, Ẑ and Ẑ_full are finite with magnitude ≤ 2²¹;
  - the measured ē_ℓ (§15.3.6) is ≤ 2²¹.

  Failure → FAIL_TECHNICAL/NUMERICAL. For this model, logits are expected well below 10² nats.
- **P3 (Decimal).** Any trap, or any watched flag (Underflow, Subnormal, Overflow) raised in a certificate Decimal computation → FAIL_TECHNICAL/NUMERICAL. This is K4's policy.

#### 15.3.4 Notation and constants

| Symbol | Definition | Value / bound |
|---|---|---|
| u, u′ | 2⁻⁵³; u/(1−u) | 1.1102·10⁻¹⁶ |
| γ_n | nu/(1−nu) | γ_36 ≈ 3.997·10⁻¹⁵; γ_31 ≈ 3.442·10⁻¹⁵; γ_4096 ≈ 4.548·10⁻¹³; γ_20480 ≈ 2.274·10⁻¹² |
| w_u | log((1+u)/(1−u)), the oscillation width of one rounding | ≤ 2u′ |
| m_u | −log(1−u), the magnitude of one rounding; log(1+u) ≤ m_u | ≤ u′ |
| θ(x̂:x) | componentwise log(x̂/x) for positive vectors | — |
| osc(x̂:x), mag(x̂:x) | max θ − min θ, and max \|θ\| | — |
| ω_TE | max_z r(z) − min_z r(z), with r(z) = Σ_{z′} T̂(z,z′)·Σ_v Ê_canon(z′,v), exact rationals | a few ulps (≈ 10⁻¹⁵) |
| ĉ₁, δ₁ | fl(0.1); \|ĉ₁ − 1/10\| = 1/(5·2⁵⁵) | 5.551·10⁻¹⁸ |
| ĉ₃, δ₃ | fl(0.3); \|ĉ₃ − 3/10\| = 1/(5·2⁵⁴) | 1.110·10⁻¹⁷ |
| ζ | underflow allowance | 2⁻⁸⁰⁰ ≈ 1.5·10⁻²⁴¹ |
| up(c) | `math.nextafter(float(c), +inf)` for a rational constant c; up(c) ≥ c | — |
| OUT(x) | (1 + 2⁻³⁰)·Fraction(x) + ζ, evaluated exactly | — |

#### 15.3.5 Lemmas

**L1 (nonnegative reductions).** Let x, y ≥ 0 be float vectors of length n. Assume every nonzero product x_k y_k and every nonzero partial result lies in the normal range. Then, under A1 and A2, fl(Σ x_k y_k) = Σ x_k y_k (1+θ_k) with (1−u)ⁿ ≤ 1+θ_k ≤ (1+u)ⁿ. Consequently, mag(fl(x·y) : x·y) ≤ n·m_u, and the computed values have oscillation ≤ n·w_u relative to any common factor.

*Proof.* In any binary tree with n leaves, a leaf has at most n−1 addition ancestors, plus its own product rounding (an fma merges the two into one rounding). Each rounding contributes a factor (1+δ) ∈ [1−u, 1+u] (A1, normal range). A zero product is exact and contributes nothing. Finally, (1+u)ⁿ ≤ e^{n·m_u} and (1−u)ⁿ = e^{−n·m_u}. ∎

**L2 (positive linear maps do not increase oscillation).** Let x, x̂ > 0 and M ≥ 0 with xM > 0, and let θ = θ(x̂:x). Then every component of θ(x̂M : xM) lies in [min θ, max θ].

*Proof.* (x̂M)_j = Σ_k x_k M_kj e^{θ_k}, which is a positive combination of the terms of (xM)_j, each scaled by a factor in [e^{min θ}, e^{max θ}]. ∎

**L3 (normalisation).** Let ĝ and g > 0 have length N, and let θ(ĝ:g) have range [a, a+w]. Define b = g/Σg and b̂ = fl(ĝ / fl(Σ ĝ)), in the normal range. Then osc(b̂:b) ≤ w + w_u and mag(b̂:b) ≤ w + N·m_u.

*Proof.*
- Write s = Σg and ŝ = fl(Σĝ). By L1, ŝ = Σ_k ĝ_k(1+θ′_k) with |log(1+θ′_k)| ≤ (N−1)m_u.
- So log(ŝ/s) = log Σ_k (g_k/s)·e^{θ_k}(1+θ′_k), which lies in [a − (N−1)m_u, a + w + (N−1)m_u].
- Then log(b̂_k/b_k) = θ_k + log(1+δ_k) − log(ŝ/s), with |log(1+δ_k)| ≤ m_u. This gives the magnitude bound.
- The term log(ŝ/s) is common to every k, so the oscillation grows only by the division's width w_u. ∎

**L4 (order statistics).** If x, y ∈ ℝ^D satisfy |x_d − y_d| ≤ B for all d, then |x_(k) − y_(k)| ≤ B for every k.

*Proof.* At least k entries of y are ≤ y_(k). Their partners in x are ≤ y_(k) + B, so x_(k) ≤ y_(k) + B. The other direction is symmetric. ∎

**L5 (outward evaluation of bounds).** Let E be an expression tree with:
- nonnegative float leaves, each ≤ 2²¹ (data magnitudes, or constants up(c) ≤ 1);
- internal nodes + and × only;
- at most 6 multiplications on any root-to-leaf path;
- at most 2¹⁶ leaves.

Let Ê be its float64 evaluation, with sums in any order. Under A1 and A2, the exact value satisfies E ≤ OUT(Ê).

*Proof.*
- Every term path carries at most K = 2¹⁶ + 6 relative roundings, so the relative part is at most (1−u)^{−K} ≤ 1 + 2⁻³⁶.
- An absolute underflow error of 2⁻¹⁰⁰⁰ per operation (A1) is multiplied by at most five later factors, each ≤ 2²¹, and there are at most 2¹⁷ operations. The total is ≤ 2¹⁷·2⁻¹⁰⁰⁰·2¹⁰⁵ = 2⁻⁸⁷⁸ < ζ. ∎

Every row bound in §15.3.8–15.3.10, fully expanded, meets these limits:
- at most 6 factors per term, the deepest being (3/10)·½·ρ̄·q̂·(ρ⁺+ρ⁻);
- fewer than 7,000 leaves per row and model;
- leaves ≤ 2²¹ by P2.

The implementation evaluates each bound as displayed, in float64, with constants up(·). OUT is monotone, so OUT(max_i b̂_i) ≥ max_i b_i.

#### 15.3.6 Oracle bound (Theorem 1) and measured logarithms

**Theorem 1 (oracle predictive, componentwise).** Assume A1, A2, P0, and P1 for history h. Then:

  mag(b̂_32 : b*_32) ≤ M_b := [N + 3 + 30(N+2)]·w_u + N·m_u ≤ 9198·u′ ≈ 1.0212·10⁻¹²,
  mag(q̂ : q*) ≤ ρ_q := M_b + 2N·m_u ≤ 9486·u′ < 1.05316·10⁻¹².

This holds for every symbol v, independently of the history and of the size of q*(v). For general L ≥ 2: ρ_q(L, N) ≤ (2[N + 3 + (L−2)(N+2)] + 3N)·u′.

*Proof.*

*Step 0: P1 keeps the whole filter in the normal range.*
- Products b̂_t(z′)·T̂(z′,z) with T̂(z′,z) > 0 are ≥ ν₀τ⁺ ≥ 2⁻¹⁰⁰⁰. Zero entries of T̂ give exact zeros.
- By L1, the prior satisfies â(z) ≥ (1−u)^N·b̂_t(z)·T̂(z,z) ≥ (1−u)^N ν₀ τ⁺.
- So the emission products satisfy â(z)·Ê(z,w) ≥ (1−u)^N·2⁻¹⁰⁰⁰.
- At t = 1, the products π̂·Ê are ≥ π_min ε_E ≥ 2⁻¹⁰⁰⁰ by P0.
- Products in fl(T̂Ê) are ≥ τ⁺ε_E ≥ 2⁻¹⁰⁰⁰ by P0. Products b̂_32(z)·(T̂Ê)^(z,v) are ≥ (1−u)^N·2⁻¹⁰⁰⁰.
- Sums of nonnegative normal terms are normal.
- Every stored quotient b̂_t(z) is ≥ ν₀ > 2⁻¹⁰⁰⁰. Rounding to nearest is monotone, so each exact quotient is ≥ 2⁻¹⁰²².
- All values are ≤ 2, so nothing overflows.

Hence A1's normal-range model holds for every operation of C1, and FTZ/DAZ cannot act. All exact quantities are strictly positive (Ê > 0, π̂ > 0 and the T̂ diagonal > 0), so every log-ratio is defined.

*Step 1 (t = 1).* ĝ_1 = fl(π̂ ⊙ Ê[:, w_1]) against g_1 = π̂ ⊙ Ê[:, w_1] has osc ≤ w_u. By L3, osc(b̂_1 : b*_1) ≤ 2w_u.

*Step 2 (t → t+1).*
- â = fl(b̂_t T̂) against a = b*_t T̂: by L2 (exact part) and L1 (rounding, n = N), every log-ratio lies in [min θ_t − N m_u, max θ_t + N m_u]. So osc ≤ osc_t + N·w_u.
- The emission multiplication adds w_u.
- The normalisation (L3) adds w_u.

So osc_{t+1} ≤ osc_t + (N+2)w_u, and therefore osc_t ≤ [2 + (t−1)(N+2)]·w_u.

*Step 3 (t = 32).* osc(ĝ_32 : g_32) ≤ osc_31 + (N+1)w_u = [2 + 30·146 + 145]·w_u = 4527·w_u. By L3, mag(b̂_32 : b*_32) ≤ 4527·w_u + 144·m_u = M_b.

*Step 4 (T·E prediction).*
- By L1, the computed `TE` = fl(T̂Ê) satisfies mag ≤ N·m_u entrywise.
- q̂_v = fl(Σ_z b̂_32(z)·TE(z,v)) = Σ_z b*_32(z)(T̂Ê)(z,v)·e^{θ_z + φ_zv}(1 + θ″_zv), with |θ_z| ≤ M_b, |φ_zv| ≤ N m_u and |log(1+θ″_zv)| ≤ N m_u.
- So mag(q̂ : q*) ≤ M_b + 2N·m_u.
- Numerically: 9054 + 144 + 288 = 9486 rounding units. ∎

**Consequences used below.**
- |q̂(v) − q*(v)| ≤ (e^ρ − 1)·q*(v) ≤ ρ̄·q̂(v), where ρ̄ := (e^ρ − 1)·e^ρ. Evaluated upward with e^x ≤ 1 + x + x² for 0 ≤ x ≤ 1: ρ̄ ≤ (ρ + ρ²)(1 + ρ + ρ²).
- ρ^± denotes the oracle bound for H^±_i: ρ_q under P1, or ρ_F(h) from route F.

**Measured logarithms (M-ln).** For every certified row i, sign ± and symbol v:
- inside `decimal.localcontext(error_bound.trapping_context(40))`, compute 𝓛 = `Decimal(q̂(v)).ln()` (the conversion is exact);
- set e = |Fraction(ℓ̂(v)) − Fraction(𝓛)| + 10⁻³⁸·|Fraction(𝓛)|;
- set ē_ℓ,i = up(max over the 72 values);
- a trap or flag triggers P3.

By A3, |𝓛 − log q̂(v)| ≤ 10⁻³⁹·|log q̂(v)| ≤ 10⁻³⁸·|𝓛|. Hence |ℓ̂^±(v) − log q̂^±(v)| ≤ ē_ℓ,i. No property of `np.log` is assumed.

**Corollary 1.** |ℓ̂^±(v) − log q*^±(v)| ≤ ρ^± + ē_ℓ,i for every v. No lower bound on q* is required. This answers RC6's tiny-probability point: an absolute L1 bound divided by min q (about 10⁻²¹ here) would be about 10⁹ and would force INCONCLUSIVE; the componentwise bound is about 10⁻¹².

#### 15.3.7 Route F: validated enclosure for a history that fails P1 (K4 machinery)

For a donor history h with ν_min(h) < ν₀, the filter may have underflowed, so Theorem 1 is not used for h. Instead:

1. **Decimal posterior.** b̃ = `independent_reference.decimal_suffix_posterior(T̂, Ê_canon, π̂, h, digits=60)`, with the suffix equal to all 32 tokens, which is exactly the restart-at-π̂ full filter. It runs inside `decimal.localcontext(error_bound.trapping_context(80))`, with K4's flag inspection. β = `error_bound.posterior_envelope(32, N)` (≈ 10⁻⁵⁵) gives |b̃ − b*_32| ≤ β·b*_32 componentwise (K4 ERROR_BOUND §3(a)).
2. **Decimal predictive.** q̃(v) = Σ_z b̃(z)·Σ_{z′} T̂(z,z′)Ê(z′,v), at 60 digits. This is the §3.4 helper, with at most 2N+2 roundings per positive path. Set β_q = (1+β)(1+γ^(60)_{2N+2}) − 1, with γ^(60) from `error_bound.gamma_digits(2N+2, 60)`. Then q̃/q* ∈ [1−β_q, 1+β_q].
3. **Measured discrepancy.** r = max_v |Fraction(q̂(v)) − Fraction(q̃(v))| / Fraction(q̃(v)), computed exactly.
4. **Row bound.** x = (1+r)(1+β_q) − 1. If x > 1/2 → FAIL_TECHNICAL/ORACLE. Otherwise ρ_F(h) = x/(1−x) ≥ mag(q̂ : q*), because q̂/q* ∈ [(1−r)(1−β_q), (1+r)(1+β_q)] and −log(1−x) ≤ x/(1−x).

ρ_F(h) then replaces ρ_q for that history. Everything else is unchanged. Route F makes no assumption about float64 arithmetic or BLAS; this is K4's assumption profile. Cost: 0.5–2 s per history, to be metered. The expected count is 0, because the projected ν_min for these processes is about 10⁻¹⁵⁰ or larger, far above ν₀ ≈ 10⁻²⁸⁰. The count is reported.

#### 15.3.8 G bound (Theorem 2)

Define, per row i and symbol v:
- d̂_v, the computed q̂⁺ − q̂⁻;
- λ̂_v, the computed ℓ̂⁺ − ℓ̂⁻;
- ε^d_v := u′|d̂_v| + ρ̄⁺q̂⁺_v + ρ̄⁻q̂⁻_v;
- ε^λ_v := u′|λ̂_v| + 2ē_ℓ,i + ρ⁺ + ρ⁻;
- b^G_i := ½ Σ_v [ ε^d_v|λ̂_v| + (|d̂_v| + ε^d_v)·ε^λ_v + γ_V|d̂_v||λ̂_v| ] + ζ.

**Theorem 2.** |Ĝ_i − G*_i| ≤ b^G_i.

*Proof.*
- **Subtraction error.** |fl(a − b) − (a − b)| ≤ u|a − b| ≤ u′|fl(a − b)|; a subnormal difference is absorbed in ζ.
- **Bound on d.** By Theorem 1 or route F, |d̂_v − d*_v| ≤ u′|d̂_v| + |q̂⁺_v − q*⁺_v| + |q̂⁻_v − q*⁻_v| ≤ ε^d_v.
- **Bound on λ.** By Corollary 1, |λ̂_v − λ*_v| ≤ ε^λ_v.
- **Product.** |d̂λ̂ − d*λ*| ≤ |d̂ − d*||λ̂| + |d*||λ̂ − λ*| ≤ ε^d|λ̂| + (|d̂| + ε^d)ε^λ.
- **Reduction.** The length-V dot product with fl products contributes ≤ γ_V Σ|d̂||λ̂| (A2). Multiplying by 0.5 is exact, or below ζ.
- Summing these terms gives the bound. ∎

#### 15.3.9 A bound, post-logit evaluation (Theorem 3)

For a pair X with recorded logits z^± in canonical order, write Δ_v = z⁺(v) − z⁻(v) (exact) and let Δ̂_v be the computed difference. Define:

  b^A_{X,i} := ½ [ (γ_V + u′)·Σ_v |d̂_v||Δ̂_v| + (1/(1−u))·( Σ_v ε^d_v|Δ̂_v| + ω_TE·max_v|Δ̂_v| ) ] + ζ.

**Theorem 3.** |Â_i(X) − A*_i(X)| ≤ b^A_{X,i}.

*Proof.*
1. **lse cancellation.** Since ℓ*_X = z_X − lse(z_X), A* = ½ Σ_v d*_v Δ_v − ½·Δlse·Σ_v d*_v, where Δlse = lse(z⁺) − lse(z⁻).
2. **Residual bound.**
   - lse is 1-Lipschitz in the ∞-norm, so |Δlse| ≤ max_v|Δ_v| ≤ max_v|Δ̂_v|/(1−u).
   - Σ_v q*^±(v) = Σ_z b*^±(z)·r(z), and Σ_z b*^± = 1 exactly. So both sums lie in [min r, max r], and |Σ_v d*_v| ≤ ω_TE.
3. **Remaining errors.**
   - |Δ̂_v − Δ_v| ≤ u′|Δ̂_v| (a subnormal result goes into ζ).
   - |d̂_v − d*_v| ≤ ε^d_v (proof of Theorem 2).
   - The dot product and the ½ factor contribute ½γ_V Σ|d̂||Δ̂| (A2).
4. Collecting these terms gives the bound. ∎

**Relation to the review's guidance (RC6).** With ε± = 0 (no transcendental post-logit evaluation is certified) and the L1 η replaced by the componentwise ρ̄q̂^±:
- the review's term 2η‖ℓ̂₊ − ℓ̂₋‖∞ becomes Σ_v(ρ̄⁺q̂⁺_v + ρ̄⁻q̂⁻_v)|Δ̂_v|. This is a weighted mean of |Δ̂|, never larger;
- the log-softmax normaliser contributes only ω_TE·‖Δ‖∞;
- the arithmetic-rounding terms the review required are explicit (γ_V, u′ and ζ).

**Zero patch.** Bitwise-equal arm logits give Δ̂ = 0, so Â = 0 exactly (§15.1 check).

#### 15.3.10 Y, Z and Z_full (Theorem 4)

Per model j and row i, with T the primary pair and C_r the 32 control pairs:

  b^Y := u′|Ŷ| + b^A_T + (1/32)·Σ_r b^A_{C_r} + (γ_31/32)·Σ_r |Â_{C_r}| + ζ,
  b^Z_{j,i} := u′|Ẑ| + b^Y + (u′ĉ₁ + δ₁)·|Ĝ| + (1/10)·b^G_i + ζ,
  b^Zf_{j,i} := u′|Ẑ_full| + b^A_full + (u′ĉ₃ + δ₃)·|Ĝ| + (3/10)·b^G_i + ζ.

**Theorem 4.** |Ŷ − Y*| ≤ b^Y, |Ẑ − Z*| ≤ b^Z and |Ẑ_full − Z*_full| ≤ b^Zf.

*Proof.*
- **Frame mean.** The computed mean over the frames is fl(fl(Σ_r Â_r)/32). Division by 32 is exact (or below ζ), and the sum error is ≤ γ_31 Σ|Â_r|.
- **Y.** Ŷ = fl(Â_T − mean) has error ≤ u′|Ŷ|. Add b^A_T and (1/32)Σ b^A_{C_r} (Theorem 3).
- **Z.**
  - fl(ĉ₁Ĝ) differs from ĉ₁Ĝ by ≤ u′ĉ₁|Ĝ|;
  - |ĉ₁ − 1/10|·|Ĝ| = δ₁|Ĝ|;
  - (1/10)|Ĝ − G*| ≤ (1/10)b^G (Theorem 2);
  - the final subtraction costs u′|Ẑ|.
- **Z_full.** The same argument with ĉ₃, δ₃ and A_full. ∎

#### 15.3.11 Bootstrap means, B_num, guards and the decision theorem

**Theorem 5 (mean arithmetic).** For model j, any draw d and its index multiset I_d (of size n), let m̂_{j,d} = fl(fl(Σ_{k∈I_d} Ẑ_{j,k})/n) and m*_{j,d} = (1/n)Σ_{k∈I_d} Z*_{j,k}. Then

  |m̂_{j,d} − m*_{j,d}| ≤ max_i b^Z_{j,i} + r^mean_j,  with r^mean_j := γ_n·max_i|Ẑ_{j,i}| + ζ.

*Proof.*
- **Arithmetic part.** By A2, fl(Σ) = Σ Ẑ_k(1+θ_k) with |θ_k| ≤ γ_{n−1}. Division adds a factor (1+δ), and (1+u)(1+γ_{n−1}) ≤ 1+γ_n (Higham Lemma 3.3). So |m̂ − (1/n)ΣẐ_k| ≤ γ_n·max|Ẑ|. Underflow is absorbed by ζ.
- **Input part.** |(1/n)Σ(Ẑ_k − Z*_k)| ≤ max_i b^Z_{j,i} (Theorem 4). ∎

**Certified constants (exact rationals; n is the eligible-row count of the split).**
- B_num,j := OUT(max_i b̂^Z_{j,i}) + γ_n·Fraction(max_i|Ẑ_{j,i}|) + ζ.
- B^H := OUT(max_i b̂^G_i) + γ_n·Fraction(max_i|Ĝ_i|) + ζ. Here n and i run over the eligible rows of the split being gated (validation or fresh).
- B^V3_j := OUT(max_i b̂^Zf_{j,i}) + γ_n·Fraction(max_i|Ẑ_full,j,i|) + ζ.

By L5, these dominate the exact values of the displayed bounds. This matches the review's definition B_num,j = max_i b^Z_{j,i} + r^mean_j, rounded outward.

**Signed guards (all comparisons in exact rationals; the floor 10⁻⁹ is an extra conservative guard, not a proof of accuracy):**
- **(E) Endpoint, §13 step 2.** If for any j, |L̂_j| ≤ max(B_num,j, 10⁻⁹) or |Û_j| ≤ max(B_num,j, 10⁻⁹) → INCONCLUSIVE/NUMERICAL.
- **(H) H5.** Let Γ = Fraction(lower̂) − 1/100 and g = max(B^H, 10⁻⁹).
  - PASS iff Γ > g;
  - INCONCLUSIVE/HEADROOM iff Γ ≤ −g;
  - otherwise INCONCLUSIVE/NUMERICAL.

  Validation uses seed 520505 and fresh uses 520506.
- **(V) V3.** Let Γ_j = Fraction(L̂^V3_j) and g_j = max(B^V3_j, 10⁻⁹).
  - PASS iff Γ_j > g_j for every j;
  - INCONCLUSIVE/MODEL_HEADROOM iff Γ_j ≤ −g_j for some j;
  - otherwise INCONCLUSIVE/NUMERICAL.

  Validation uses seed 520504 and fresh uses 520507.

**Theorem 6 (decisions).** Under A1–A4, P0, P2, P3, and P1 or route F for every certified history:
- if the endpoint guard (E) is not triggered, every PASS_j / FAIL_j / INC_j, and hence the overall PASS / FAIL / MIXED, equals its exact-arithmetic counterpart;
- a PASS of (H) or (V) implies that the exact gate passes;
- an INCONCLUSIVE/HEADROOM or INCONCLUSIVE/MODEL_HEADROOM implies that the exact gate fails.

*Proof.*
1. By Theorem 5 and L5, |m̂_{j,d} − m*_{j,d}| ≤ B_num,j for every draw d.
2. Numpy's `inverted_cdf` returns an order statistic with the same index for both vectors (§15.3.2, C7). L4 then gives |L̂_j − L*_j| ≤ B_num,j and |Û_j − U*_j| ≤ B_num,j.
3. If |L̂_j| > B_num,j, then L*_j ≠ 0 and sign L*_j = sign L̂_j. The same holds for U.
4. The same argument applies to lower̂ with B^H, against the threshold 1/100, and to L̂^V3_j with B^V3_j. ∎

#### 15.3.12 η = 1e-12 and 2⁻⁴⁴ (RC6)

Neither constant is retained.
- **η = 1e-12** is replaced by the derived componentwise bound ρ_q. Its L1 consequence, ‖q̂ − q*‖₁ ≤ (e^{ρ_q} − 1)(1 + ω_TE) ≈ 1.053·10⁻¹², is slightly **larger** than 1e-12. So 1e-12 could not have been kept as a worst-case L1 bound.
- **2⁻⁴⁴** has no role: no log-softmax is evaluated on the certified path (§15.3.2, C4).

The 1e-12 values in H3 remain implementation-check tolerances. §16 row 3 aligns them with the proved bounds.

#### 15.3.13 Expected magnitudes against the 0.10·G margin

These are projections from the bounds, not data. Ḡ is taken to be 10⁻² to 10⁻¹ nat, so 0.10·Ḡ is 10⁻³ to 10⁻².

| Quantity | Typical row | Plausible worst | Ratio to 0.10·Ḡ |
|---|---|---|---|
| ρ_q (log q, every v) | 1.053·10⁻¹² (fixed) | same | — |
| ē_ℓ (measured np.log error) | ≲ 10⁻¹⁴ (≤ 1 ulp of \|log q\| ≤ 47) | — | — |
| b^G | ≈ 10⁻¹² (‖d̂‖₁ε^λ + ρ̄Σ(q̂⁺+q̂⁻)\|λ̂\|) | ≤ 5·10⁻¹¹ (\|λ\| ≤ 47) | ≤ 5·10⁻⁸ |
| b^A per pair | ≈ ρ̄·(q-weighted mean \|Δz\|) ≈ 10⁻¹³ to 10⁻¹² | ≤ 10⁻¹¹ (‖Δz‖∞ ≤ 10 nats) | ≤ 10⁻⁸ |
| b^Y, b^Z, b^Zf | ≈ 10⁻¹² | ≤ 3·10⁻¹¹ | ≤ 3·10⁻⁸ |
| r^mean (n ≤ 20,480) | 2.27·10⁻¹²·max\|Ẑ\| | ≤ 2.3·10⁻¹¹ (max\|Ẑ\| ≤ 10) | ≤ 2·10⁻⁸ |
| B_num,j, B^H, B^V3_j | ≈ 10⁻¹¹ | ≤ 10⁻¹⁰ | ≤ 10⁻⁷ |
| Binding guard | the 10⁻⁹ floor | the 10⁻⁹ floor | 10⁻⁷ to 10⁻⁶ |

**Risk of INCONCLUSIVE/NUMERICAL.** P1's design implies a bootstrap standard error of the mean Z of about 0.10·Ḡ/3, so SE ≥ 10⁻⁴ for the smallest plausible Ḡ. The chance that one of the 6 endpoint bounds lands in a ±10⁻⁹ band is then at most about 6 × 2·10⁻⁹ × 1/(√(2π)·10⁻⁴) ≈ 5·10⁻⁵. Numerical inconclusiveness is therefore not near-certain; it is practically excluded. For contrast, the withdrawn v1 G bound (η/min q, with min q ≈ 10⁻²¹) would have been about 10⁹, making INCONCLUSIVE certain.

#### 15.3.14 Cost (single thread)

The oracle is canonical and model-independent. It costs 2 donor histories per row, not 2 × 3. The 3 models enter only the cheap A/Y/Z float arithmetic. There are at most about 24.6k certified rows: validation 4096·f plus fresh ≤ 5 × 4096.

| Item | Cost |
|---|---|
| Float filter (already in §17) | ≈ 1 MFLOP per history; ≈ 50k histories ⇒ minutes |
| P0 exact constants (ω_TE, ε_E, τ⁺, π_min) | ≈ 3·10⁴ Fraction operations, once: < 1 s |
| P1 | one minimum over the stored `b` per history: negligible |
| M-ln | ≤ 1.8·10⁶ Decimal `ln` at 40 digits, plus Fractions: ≤ about 3 min |
| Row bounds b^G, b^A (33 pairs), b^Y, b^Z, b^Zf | vectorised numpy, about 10⁸ flops: seconds |
| OUT, B constants, guards | a few Fraction operations per model and gate: negligible |
| Route F | 0.5–2 s per failing history (metered); expected 0; worst case, all ≈ 50k histories, about 7–28 CPU-h, uncapped and reported |
| **Expected total** | **< 0.1 CPU-h** |

**Alternatives considered.**
- **(ii) A validated interval filter.** Because every quantity is positive, it reduces to running the float filter twice with the per-step factors (1 ± u)^{N+2}. That is route (i) under another name, since numpy offers no directed rounding. Its cost would be minutes.
- **All-row Decimal (K4's pattern).** About 50k histories at roughly 1 s each, so 14 CPU-h or more. That is feasible with uncapped CPU, but out of proportion to a study forecast of 2–6 CPU-h. It is retained as route F, and as a drop-in switch if A2 is rejected (open question 5).

#### 15.3.15 Placement and records

**Placement.**
- **P0:** at H1 (S3).
- **On validation eligible rows at S3, before H5** (new row 4a, §16): P1, route F, M-ln, b^G and B^H.
- **At V3 (S5):** b^Zf and B^V3.
- **On fresh rows inside T-PRE (row 20):** P1, route F, M-ln, B^H and B^V3.
- **At NUM (row 21):** b^Z and B_num,j.
- **Calibration:** no certified decision; Ḡ_cal is reported only.

**Records.** The following are saved immutably (`save_npz` / `write_new`):
- per row: ν_min^±, the route flag, ρ^±, ē_ℓ, b^G, b^A_T, the mean b^A_C, b^Y, b^Z and b^Zf;
- per gate and model, as exact rational strings: the P0 constants, B_num,j, B^H and B^V3_j, together with the guard outcome.

#### 15.3.16 Tests (S1, Author A, synthetic fixtures only)

1. **Theorem 1 on tiny positive HMMs** (N between 4 and 12, lazy walks, all L ≤ 33). Compare the float filter against an exact `Fraction` filter, and assert mag(q̂ : q*) ≤ ρ_q(L, N). Also verify that ρ_q(32, 144) = 9486·u′ exactly.
2. **Underflow.** Using crafted emissions with entries near 10⁻³⁰⁰, show that P1 fails, route F is taken, and ρ_F bounds the exact error. Show that x > 1/2 gives FAIL_TECHNICAL/ORACLE.
3. **Theorems 2 and 3 against exact rationals,** including q with entries of 10⁻²⁵⁰ (G must not blow up) and stored rows that are not exactly stochastic (the ω_TE term must be required and sufficient).
4. **Logit form.** The logit-difference form equals the log-softmax form exactly in rationals when Σd = 0. Equal logits give Â = 0 bitwise.
5. **M-ln.** Injecting a log error enlarges b^G accordingly. Decimal traps and flags give FAIL_TECHNICAL/NUMERICAL.
6. **L4 and quantiles.** L4 holds, and `inverted_cdf` returns an input element bitwise.
7. **L5.** OUT(evaluated) ≥ the exact rational value on random nonnegative trees, including subnormal leaves.
8. **Guards at their boundaries.** Γ = ±g exactly, the floor binding, and exact rational comparisons for (E), (H) and (V).
9. **Constants.** δ₁ and δ₃ are exact. up(c) ≥ c for every constant.
10. **P2.** Non-finite or out-of-range values give FAIL_TECHNICAL/NUMERICAL.

---

## 3. Exact edits

### 3.1 §13 step 2 (replace the item)

> 2. **Numerical certificate** (§15.3; proof attached, subject to its independent review before freeze). For each model j, B_num,j is computed as in §15.3.11. If, for any j, |L_j| ≤ max(B_num,j, 10⁻⁹) or |U_j| ≤ max(B_num,j, 10⁻⁹), compared in exact rational arithmetic, the outcome is INCONCLUSIVE/NUMERICAL. Otherwise, by §15.3 Theorem 6, every per-model status of step 3, and hence the overall outcome of step 4, equals the outcome that exact evaluation of the declared formulas would give on the same rows, recorded logits, stored process weights and bootstrap draws. A certificate precondition defect (§15.3.3, P0, P2 or P3) is FAIL_TECHNICAL and is decided before this step.

### 3.2 §16

**Conventions: add a bullet.**
> - Certified quantities (Ĝ, Â, Ŷ, Ẑ, Ẑ_full and their bootstrap means) are computed only by the prescribed expressions of §15.3.2. Certificate bounds are evaluated as §15.3.5 L5 prescribes, and every certificate comparison is made in exact rationals.

**Row 3 (H3 ORACLE).** Replace the Decimal clause of the criterion with:
> Decimal (§3.4): posterior and predictive componentwise |x̂/x̃ − 1| ≤ 2·10⁻¹² (a reference row that fails P1 is checked by route F, §15.3.7); surprisal ≤ 1e-10; |Ĝ − G̃| ≤ b^G_i + 10⁻³⁰ (b^G_i from §15.3.8). P0 (§15.3.3) holds exactly.

Status: unchanged (FAIL_TECHNICAL/ORACLE), with P0 failure → FAIL_TECHNICAL/IDENTITY.

**New row 4a, between rows 4 and 5:**

| 4a | S3 | N0 NUMERIC PRECONDITIONS (validation eligible rows) | §15.3.3: P1 for every donor history (route F, §15.3.7, where P1 fails; this is not a failure); M-ln (§15.3.6); P2 for q̂, ℓ̂ and Ĝ; b^G_i and B^H computed | FAIL_TECHNICAL/NUMERICAL (P2, P3); FAIL_TECHNICAL/ORACLE (route F x > 1/2) |

**Row 5 (H5 HEADROOM).** Replace the criterion and status with:
> `lower` from `bootstrap_profile(..., rng=np.random.Generator(np.random.PCG64(520505)), draws=5000)` and `percentile_interval(result["B"][:, 0], [0.05])[0]` (§3.5). Signed guard §15.3.11 (H): PASS iff lower − 1/100 > max(B^H, 10⁻⁹), in exact rationals.

> Status: lower − 1/100 ≤ −max(B^H, 10⁻⁹) → INCONCLUSIVE/HEADROOM; otherwise INCONCLUSIVE/NUMERICAL.

**Row 18 (V3).** Replace the criterion and status with:
> All three LB(Z_full) at 0.05/3 (seed 520504), with Z_full computed by §15.3.2 C4/C6, b^Zf_{j,i} and B^V3_j by §15.3.10–11. PASS iff L^V3_j > max(B^V3_j, 10⁻⁹) for every j, in exact rationals. Donor logits are first retained for scientific use here (§2.2).

> Status: some L^V3_j ≤ −max(B^V3_j, 10⁻⁹) → INCONCLUSIVE/MODEL_HEADROOM; otherwise INCONCLUSIVE/NUMERICAL.

**Row 20 (T-PRE).** In the criterion, after "H3 on test rows;" insert:
> N0 (row 4a) on test eligible rows;

Replace "LB Ḡ_test > 0.01 (seed 520506, same call as §3.5)" with:
> H5 on test with seed 520506 and the §15.3.11 (H) guard;

Replace "V3 (seed 520507)" with:
> V3 with seed 520507 and the §15.3.11 (V) guard;

Status: add "INCONCLUSIVE/NUMERICAL for a guard band hit; FAIL_TECHNICAL/NUMERICAL for P2 or P3".

**Row 21 (NUM).** Replace the row with:

| 21 | S7 | NUM | §15.3 (proof attached; independent review before freeze): P2 on all certified arrays; b^Z_{j,i} for every test eligible row; B_num,j = OUT(max_i b̂^Z_{j,i}) + γ_n·max_i\|Ẑ_{j,i}\| + ζ; per model \|L_j\| > max(B_num,j, 10⁻⁹) and \|U_j\| > max(B_num,j, 10⁻⁹), in exact rationals | INCONCLUSIVE/NUMERICAL (FAIL_TECHNICAL/NUMERICAL for P2 or P3) |

### 3.3 §20 item 14 (replace)

> 14. Symmetry tolerance 1e-14 (changed from L's 1e-15). The numerical certificate (§15.3; proof attached, independent review before freeze):
>   - **Oracle.** A proved componentwise oracle bound ρ_q = 9486·u/(1−u) ≈ 1.053·10⁻¹² (log-ratio, every symbol) for the 32-step float64 `BayesFilter` and its T·E prediction, under the per-history precondition P1 (no posterior entry below ν₀ ≈ 10⁻²⁸⁰). A history failing P1 is certified by a validated 60-digit Decimal enclosure (K4 machinery, route F).
>   - **Logs and A.** `np.log` errors are measured against correctly rounded 40-digit Decimal `ln`. A is evaluated in logit-difference form, so no log-softmax enters the certified path.
>   - **Bounds.** Per-row b^A, b^G, b^Y, b^Z and b^Zf. r^mean_j = γ_n·max|Ẑ| and B_num,j = OUT(max_i b^Z_{j,i}) + r^mean_j, with outward inflation (1 + 2⁻³⁰)·x + 2⁻⁸⁰⁰.
>   - **Guards.** Signed guards for H5 and V3.
>   - **Constants.** η = 1e-12 and 2⁻⁴⁴ are withdrawn, not retained. The H3 Decimal tolerances are aligned with the proved bounds (componentwise 2·10⁻¹²; per-row b^G).
>   - **Floor.** The numerical floor 1e-9 is retained as an additional conservative guard, not a proof of accuracy. It is the binding guard: the projected B_num,j is ≤ 10⁻¹⁰.

### 3.4 C-19 (replace the entry in §21)

> - **C-19 (X + W; v3: proof attached).** v1's constants (η = 1e-12 from four reference rows, and 2⁻⁴⁴ for the log-softmax) and the bounds built on them were withdrawn in v2 (review RC6). v3 attaches the proof in §15.3:
>   - a Higham-style forward analysis of the actual float64 filter, in the projective (log-ratio oscillation) metric, giving componentwise ρ_q ≈ 1.053·10⁻¹²;
>   - precondition P1, with route F (K4 Decimal enclosure) where it fails;
>   - measured logarithms;
>   - A in logit-difference form;
>   - explicit per-row b^A, b^G, b^Y, b^Z and b^Zf, r^mean = γ_n·max|Ẑ|, and B_num,j rounded outward;
>   - signed guards for H5 and V3;
>   - exact rational comparisons.
>
>   The certificate is relative to the recorded float64 logits and the stored process weights. It certifies the decisions (E), (H) and (V), not the operational definitions listed in §15.3.1. Neither η nor 2⁻⁴⁴ is retained.

### 3.5 Consequential edits outside the four named locations (flagged; each follows from §15.3 as written)

1. **Header (paragraph "What this document is").** Replace "**Freeze is additionally blocked until the numerical certificate of §15.3 (status NOT_READY) is attached and independently reviewed.**" with:
   > **The numerical certificate of §15.3 is attached (proof complete); freeze additionally requires its independent review.**

   Also update the §22.3 F2 flag accordingly.
2. **§3.3, append:**
   > **Operational G.** Ĝ_i is computed once per row, in canonical order, by §15.3.2 C3. It is the value used by H5, V3, Z, Z_full and θ̂ for all three models. The per-model named-order values serve only the cross-model identity check.
3. **§3.4 Tolerances.** Mirror §16 row 3: posterior and predictive componentwise relative ≤ 2·10⁻¹²; G ≤ b^G_i + 10⁻³⁰; surprisal unchanged.
4. **§11, after the A_full definition:**
   > A_full is computed in the logit-difference form of §15.3.2 C4, with the donor logits.
5. **§12.1, after the displayed A_i(X):**
   > **Computation (§15.3.2 C4).** The recorded float64 logits of both arms are gathered into canonical order, and Â = 0.5·Σ_v(q̂⁺ − q̂⁻)(v)·(z_{X⁺}(v) − z_{X⁻}(v)). In exact arithmetic this equals the log-softmax definition up to −½(lse(z_{X⁺}) − lse(z_{X⁻}))·Σ_v(q⁺ − q⁻)(v). That term vanishes for exactly normalised q and is bounded in §15.3.9 for the stored weights. The float64 log-softmax is computed only for secondary quantities and for the §5.4 tail-path check.
6. **§15.2.** Replace "All-row Decimal enclosures (X) are not used." with:
   > All-row Decimal enclosures (X) are not used for all rows; route F of §15.3.7 applies them only to donor histories failing precondition P1.
7. **§17 S1, Author A.** Replace "the numerical certificate;" with:
   > the numerical certificate (§15.3.16 items 1–10, synthetic fixtures only);
8. **§18.**
   - **Field 1, K4 helpers:** add `error_bound.u_digits`, `gamma_digits` and `posterior_envelope`.
   - **Field 1, oracle:** add `independent_reference.decimal_suffix_posterior` for route F.
   - **Field 3, item (5):** read "the certificate (§15.3: P0–P3 checks, route F, M-ln, row bounds, OUT, guards)".
9. **§21.** Add a changelog row:

   | 15.3 | v3 numerical certificate | Proof attached; C-19 |

---

## 4. Reuse note

**Reused unchanged from K4 `tools/x4_circle_history/error_bound.py`.** It is imported with `tools/x4_circle_history` on `sys.path`, as `precision.py` already is. Its import inserts `tests/oracle_profile` into `sys.path`, imports K4's `errors`, and verifies its Taylor constants exactly; these effects are harmless and recorded.
- `trapping_context(prec)`: every certificate Decimal computation (route F at 80, M-ln at 40).
- `u_digits(n)` and `gamma_digits(k, n)`: Decimal-precision constants for route F.
- `posterior_envelope(L, S)`: β for the 60-digit posterior in route F (L = 32, S = 144).

**Reused unchanged from job 0014.** `independent_reference.decimal_suffix_posterior` (route F), exactly as K4 uses it.

**Reused ideas from K4 ERROR_BOUND.md v2.2:**
- the target is the operational stored-weight filter in exact reals (§1);
- a measured discrepancy plus a proved reference envelope (§2–3): used in route F and in M-ln;
- final comparisons in exact rationals;
- the trap/flag policy, where any trap or flag gives FAIL_TECHNICAL (§2);
- "every row, never selected rows" (§5);
- the libmpdec correct-rounding assumption (§5), extended to `ln`.

**Not reused:**
- `certify_rows`, `reference_moments`, `row_bound` and the cos/sin Taylor machinery. They certify K4's circular moments M_32 − M_4, a different target.
- `_reference_posterior`, a private name. C1 replicates its 8-line wrapper (trapping context plus flag check) with provenance, rather than importing a private symbol (open question 10).
- `process_law.py`. C1's oracle is operational (§3.3), so the documented-law deviation is not part of any C1 claim.

K4 deliberately made **no** float64 model. C1 differs on purpose: the standard IEEE/BLAS model (A1, A2) for the filter is what makes an all-row certificate proportionate (under 0.1 CPU-h instead of 14 CPU-h or more). Route F keeps K4's assumption-free profile for any history that the model does not cover.

**New in C1:**
- L1–L5;
- Theorem 1 (projective forward analysis, ρ_q) with P0 and P1;
- the logit-difference evaluation of A and the ω_TE residual;
- Theorems 2–6 (b^G, b^A, b^Y, b^Z, b^Zf, r^mean, the order-statistic transfer);
- M-ln;
- OUT and the signed guards;
- the Decimal predictive helper, already planned as new in §3.4.

---

## 5. Open questions

1. **A in logit-difference form (C4).** Please confirm. The definition is unchanged: log-softmax stays the target. If the coordinator requires computing A from the float log-softmax instead, the certificate extends, because each lse error enters only multiplied by |Σ_v d̂_v| ≲ 10⁻¹². The per-v term u|ℓ̂_v| would then be added, and exp/log errors would have to be measured: about 2.4k Decimal exp/ln per row and model, roughly 1–3 CPU-h. Not recommended.
2. **Canonical Ĝ (C3).** Please confirm that the single canonical Ĝ is the value used everywhere (§3.3 edit). v2 left unspecified which of the per-model G values enters Z_j.
3. **H3 tolerances.** The previous absolute 1e-12 posterior and predictive tolerances sit marginally below the proved worst case for entries near 1 (≈ 1.02–1.05·10⁻¹²). So a correct pipeline could in principle trip them; in practice errors are about 10⁻¹⁵. The proposed componentwise 2·10⁻¹² and per-row b^G make an H3 failure a proof of a defect. Should the closed-form and named=canonical checks (absolute 1e-12) become componentwise 4·10⁻¹² for the same reason?
4. **Band hits in H5 and V3.** These are recorded as INCONCLUSIVE/NUMERICAL, distinct from a certified HEADROOM / MODEL_HEADROOM. Both stop. Please confirm the labels.
5. **A2 for OpenBLAS kernels.** This is standard but not verifiable from source. If the reviewer rejects it, route F can be applied to every donor history, at roughly 7–28 CPU-h, uncapped, with no other change to the certificate. A/G/Y/Z and the means use only numpy's own reductions, not BLAS.
6. **Route F volume.** There is no cap, and the count is reported. Should more than, say, 1% of histories failing P1 also be raised as an anomaly alarm? Posterior entries below 10⁻²⁸⁰ would be scientifically surprising for this process.
7. **P2 limits** (|z| ≤ 2¹⁹; magnitudes ≤ 2²¹) and their FAIL_TECHNICAL/NUMERICAL status: please confirm.
8. **The 10⁻⁹ floor is retained** and is the binding guard. Confirm there is no wish to raise it. Raising it to 10⁻⁷ would still leave P(NUMERICAL) ≲ 5·10⁻³.
9. **P1 ladder, eligibility, κ_ν and the M/V1/V2 gates** are declared operational, not certified (§15.3.1). Confirm that the reviewer accepts this scope argument.
10. **`error_bound._reference_posterior`.** Replicate it with provenance, as proposed, or import the private name?
