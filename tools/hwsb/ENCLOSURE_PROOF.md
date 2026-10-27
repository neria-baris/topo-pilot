# The rounded softmax enclosure of `hwsb_law` (B8a; RC-1, OPEN-3)

**Scope.** This note proves the claim that `hwsb_law.softmax_enclosure_rounded(states, 60)` returns `(E_dec, lo', hi')` with every exact emission entry E\*_{s,j} in `[E_dec[s][j]/hi', E_dec[s][j]/lo']`. It is the replacement that `process_law.process_law_bound` (unchanged) receives while `hwsb_law.bound_law` is active. Protocol: `PROTOCOL_HWSB_v1.md` §4 B8a. Implementation: `tools/hwsb/hwsb_law.py`. Tests: author A checks the steps below (`test_a_enclosure_proof.py`); author B tests the enclosure independently (`test_b_meter_law.py`).

## 1. Setting

- States s = (x, y) of the 12 × 12 lattice; centres c_j = (1/2 + 2a, 1/2 + 2b), j = 6a + b, a, b < 6 (`process_law.LAW["grid"]` = 6); period 12 on the x axis.
- Exact logits (process_law.py:112-115): `dx = |x − cx| mod 12`, `d² = min(dx, 12 − dx)² + (y − cy)²`, **q_{s,j} = −d²/(2σ²)**, an exact `Fraction`.
- The exact emission row is the softmax E\*_{s,j} = e^{q_{s,j}} / Σ_k e^{q_{s,k}}.
- At σ = 5/4, 2σ² = 25/8 and q = −8d²/25 with d² a multiple of 1/4. Its denominator divides 2^a·5^b, so q has a terminating decimal expansion that the 60-digit context converts exactly. At σ = 7/4, 2σ² = 49/8 and q = −8d²/49. Unless d² = 0, the factor 7 stays in the denominator, so the decimal never terminates and the original `softmax_enclosure` raises `decimal.Inexact` (stage-A record: `UNAVAILABLE/NONTERMINATING_LOGIT`).

## 2. Rounding and δ (RC-1)

Each logit is converted **once** to q̃ = Decimal(q.numerator)/Decimal(q.denominator) in `error_bound.trapping_context(60)`. That context is ROUND_HALF_EVEN with precision 60; Inexact, Rounded and FloatOperation are not trapped, and every other trap is kept (`error_bound.py:54-65`). Define

  **δ := max_{s,j} |Fraction(q̃_{s,j}) − q_{s,j}|**, computed exactly with `Fraction`.

Round-to-nearest with 60 significant digits gives |q̃ − q| ≤ u·|q| with u = `u_digits(60)` = ½·10⁻⁵⁹. Hence δ ≤ u·Q_max with Q_max = max |q_{s,j}|. The code asserts δ ≤ u·Q_max and 2δ < 1, and returns `FAIL_TECHNICAL/LAW_BOUND` otherwise. Both values are exact, so the assertion is a check, not an assumption. At σ = 7/4, d² ≤ 5.5² + 10.5² = 140.5, so Q_max ≤ 140.5·8/49 < 23 and 2δ < 2.3·10⁻⁵⁸ ≪ 1 (the run records δ = 23/(49·10⁵⁸) and Q_max ≈ 22.94).

## 3. The three steps

**Step 1 (the existing analysis applies to q̃).** `process_law.softmax_enclosure` was proved for exact Decimal inputs: from those inputs it computes E_dec = exp(q̃_j)/Σ_k exp(q̃_k) in the 60-digit context with n_add = 36 additions, and its error analysis (one `exp` per entry, the sum, one division; each operation rounded to nearest at relative error ≤ u) gives

  softmax(q̃)_j ∈ [E_dec/hi, E_dec/lo], with lo = (1 − 2u)(1 − u)/((1 + 2u)(1 + u)^{n_add}), hi = (1 + 2u)(1 + u)/((1 − 2u)(1 − u)^{n_add}).

The q̃ values are exact Decimals, so this argument holds for q̃ unchanged. `softmax_enclosure_rounded` performs exactly these operations, in the same order and context, on q̃.

**Step 2 (from q̃ to q).** Let θ_k = q_k − q̃_k, so |θ_k| ≤ δ. Then

  softmax(q)_j / softmax(q̃)_j = e^{θ_j} · Σ_k e^{q̃_k} / Σ_k e^{q̃_k + θ_k} = e^{θ_j} / Σ_k w_k e^{θ_k},

with weights w_k = softmax(q̃)_k ≥ 0 summing to 1. The denominator is a convex combination of values in [e^{−δ}, e^{δ}], and the numerator lies in [e^{−δ}, e^{δ}]. So the ratio lies in **[e^{−2δ}, e^{2δ}]**.

**Step 3 (rational bounds).** For 0 ≤ 2δ < 1: e^{−2δ} ≥ 1 − 2δ, since e^{−t} ≥ 1 − t for every real t. Also e^{2δ} ≤ 1/(1 − 2δ), since e^{−t} ≥ 1 − t > 0 gives e^{t} ≤ 1/(1 − t). Combining with step 1:

  E\*_j = softmax(q)_j ∈ [(1 − 2δ)·E_dec/hi, E_dec/(lo·(1 − 2δ))] = [E_dec/hi', E_dec/lo'],

with **lo' = lo·(1 − 2δ)** and **hi' = hi/(1 − 2δ)**. These are exactly the values returned. Every quantity is an exact rational (lo, hi, δ) or an exact Decimal (E_dec), so `process_law_bound` consumes them as before. Its transport analysis is unchanged except for this lo/hi widening.

## 4. The terminating case (KB4, DRB12)

When every logit terminates (σ = 5/4), q̃ = q exactly, so δ = 0. Then lo' = lo·1 = lo and hi' = hi/1 = hi as Fractions. E_dec is computed by the same operations on the same Decimals, so every returned object equals `process_law.softmax_enclosure(states)` (E_dec entry by entry, lo and hi). KB4 therefore reproduces K4b's recorded Z_bound = 2116763197780003590583470649/10³⁹ exactly on the w0 process.

## 5. Binding and restoration

`bound_law(sigma, neighbour)` saves `process_law.LAW["sigma"]`, `LAW["neighbour"]` and `process_law.softmax_enclosure`. It sets them to the given Fractions and to `softmax_enclosure_rounded`, and restores all three in `finally`, including after an exception (the `hws_exact.law_bound_report` pattern). `process_law_bound` looks `softmax_enclosure` up as a module global at call time, so the rebinding takes effect without editing `process_law.py`.

## 6. What is not claimed

The note covers the emission-entry enclosure only. The kappa, TV and ρ steps of `process_law_bound` and its idealised sampling law are those of ERROR_BOUND.md v2.2 and are reused unchanged. The independent 200-digit `decimal_check` (DRB12) is a numerical cross-check on sampled entries, not part of the proof.
