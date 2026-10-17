# K4b certificate v1 (job 0045)

Authority: `tools/k4b/PROTOCOL_K4B_v1.md` §1.3, §5, §7.1, §8. References: K4 `tools/x4_circle_history/ERROR_BOUND.md` (sha256 ccbf55c80ff5c014aa00c7dca0d97b4990e6d646d8fcffb351aea9dc68086705, cited EB §n) and C1′ `tools/c1prime/PROTOCOL_C1PRIME_v1.md` §15.3.11 (Theorem 5, Lemma L4, Theorem 6). This file restates; the protocol wins on conflict.

## 0. Assumptions

- **A1** IEEE binary64 elementwise arithmetic, round to nearest; `c1_cert.a1_selftest()` passes.
- **A3** libmpdec is correctly rounded, with traps enabled (`error_bound.trapping_context`).
- **A4** Python `int` and `Fraction` arithmetic is exact.
- **Sampler** The idealised law of EB §9 item 7: independent uniform 53-bit draws. Deterministic PCG64 bias and dependence are not bounded.
- **Checks** The moment checks, the cap, the P2 analogue and the rank checks pass.

## 1. Row level (EB §2–3; protocol §5.2)

For a validation or test row and K ∈ {1, 2, 4, 32}:
- M̃_K = `error_bound.reference_moments(...)` (60-digit posterior, 80-digit features). EB §3 gives |M̃_K − M*_K| ≤ ε_K per coordinate, with ε_K = `moment_envelope(posterior_envelope(K, 144), 144)`, where M*_K is the exact P_op moment.
- **Moment check:** |m̂_K − M̃_K| ≤ 1e-10 per coordinate, compared exactly with `MOMENT_TOL_EXACT`.
- **Phase score:** x̂ = u(φ̂)·(m̂32 − m̂K). `row_bound(x̂, φ̂, M̃K, M̃32, ε_K, ε32)["B"]` = Δ + E_ref bounds |x̂ − u(φ̂)·r*_K| (EB §2–3). It is generic in K, because EB §3(e) uses only the two envelopes.

## 2. Lemma T (transport; protocol §1.3)

Let f(h, r) be 1-Lipschitz in r ∈ ℝ² with |f(h, r)| ≤ ‖r‖. Then |E_Q[f(h, r_op)] − E_{P*}[f(h, r_*)]| ≤ Z_bound = 2(ρ_κ − 1) + 4·TV(Q, P*), returned by `process_law.process_law_bound` (rounded up on the 10⁻⁴⁰ grid).

*Proof sketch.* ‖r_op − r_*‖ ≤ ‖m32,op − m32,*‖ + ‖m4,op − m4,*‖ ≤ 2(ρ_κ − 1), because ‖c_s‖ = 1 and ρ_4 ≤ ρ_32 (EB §3(a), §6). Also |E_Q f_* − E_{P*} f_*| ≤ 2·sup|f_*|·TV ≤ 4·TV, because |f_*| ≤ 2 and f depends on (z, w) only through w1..w32. Summing gives the bound.

It applies to u·r (unit u), to ∓‖r‖ (reverse triangle inequality), and to ‖r‖ (B4).

## 3. Lemma N (norm bracket; protocol §5.3)

r̃ = M̃32 − M̃4 ∈ ℚ², s = r̃x² + r̃y² = a/b, D = 10⁸⁰, k = isqrt(⌊a·D²/b⌋), n̂ = float ‖r4‖ read exactly.

  B_N = max(|n̂ − k/D|, |n̂ − (k+1)/D|) + (3/2)(ε4 + ε32),  and  |n̂ − ‖r*‖| ≤ B_N.

*Proof.* k² ≤ aD²/b < (k+1)², so √s ∈ [k/D, (k+1)/D]. By the reverse triangle inequality, |‖r̃‖ − ‖r*‖| ≤ √2·(ε32 + ε4) < (3/2)(ε32 + ε4). s = 0 gives k = 0 and the bracket [0, 10⁻⁸⁰]. Only integer and Fraction arithmetic is used.

**Row bounds per array.** X±_j: `row_bound` B on supported rows, B_N on unsupported rows (X∓ = ∓n̂ exactly). B4 (n̂): B_N on every row. Control and descriptive phases: `row_bound` B. Cap: every primary B ≤ 1e-4 (exact). P2 analogue: every X̂ finite with |X̂| ≤ 4.

## 4. Mean level (C1′ §15.3.11, Theorem 5 and Lemma L4)

Every certified mean is `c1_means.tree_mean`, with d_n = ⌈log₂ n⌉ levels. For every bootstrap draw and every rank,

  |m̂ − m*| ≤ B_num  and  |q̂ − q*| ≤ B_num,  B_num = `c1_bounds.B_constant(max_i B_i, max_i |X̂_i|, n)` = OUT(max B) + γ_{d_n+1}·max|X̂| + ζ,

with OUT(x) = (1 + 2⁻³⁰)x + 2⁻⁸⁰⁰ and ζ = 2⁻⁸⁰⁰. Lemma L4: same-rank order statistics are 1-Lipschitz in the sup norm. The rank checks (`c1_means.quantile_with_rank`) verify the registered ranks 84, 4,917, 250, 125 and 4,875.

## 5. Decision margin and Theorem B′ (protocol §5.5)

F_{j,s} = max(B_num,j,s, 10⁻⁹) + Z_bound (exact).

**Theorem B′.** Under §0:
1. |L̂−_j − L*−_j| ≤ B_num,j,− and |Û+_j − U*+_j| ≤ B_num,j,+ (§4).
2. On {L*−_j ≤ E_Q[X*−_j]}: L̂−_j − F_{j,−} ≤ μ_{P*}(X−_j). On {U*+_j ≥ E_Q[X*+_j]}: Û+_j + F_{j,+} ≥ μ_{P*}(X+_j). The transported bounds cover at least as often as the exact-arithmetic bootstrap bounds. Numerical certification does not prove nominal statistical coverage.
3. L̂− − F > 0.01 ⇒ L*− − Z_bound > 0.01; Û+ + F < 0.01 ⇒ U*+ + Z_bound < 0.01; L̂− − F > −0.01 ⇒ L*− − Z_bound > −0.01. These are one-way implications: the allowance may turn an exact-arithmetic definite result into UNRESOLVED.
4. `guard_H5(lower, B^H + Z_bound)` PASSes only if the exact lower bound minus Z_bound exceeds 0.01. HEADROOM establishes failure of the registered lower-bound gate, not that B4 ≤ 0.01.

**Exclusivity.** X− ≤ X+ rowwise, and float addition is monotone, so L̂− ≤ (rank-84 of X+) ≤ Û+. SUPPORT needs L̂− > 0.01 and EXCLUDE needs Û+ < 0.01, so they cannot both hold.

## 6. Planning allowance F_plan (protocol §7.1)

F_plan = max{B_constant(1/10⁴, 4, 12288), 10⁻⁹} + Z_bound. d_n = bit_length(12287) = 14, so the factor is γ₁₅ = 15u/(1 − 15u), u = 2⁻⁵³. B_constant is nondecreasing in max_b, max_abs and n. So whenever the fresh cap and P2 checks pass at n ≤ 12,288, every fresh F_{j,s} ≤ F_plan. F_plan is used only for planning. The decision uses the actual F_{j,s}.

## 7. What is certified, and what is not

- **Certified:** the row and mean enclosures for the fixed operational coordinate and support rule; the same-rank quantiles; the arithmetic implications behind SUPPORT, EXCLUDE and the B4 guard; Lemma T transport under the idealised sampler.
- **Operational, not certified:** activations and forward passes, the chart (PH, lift, smoothing, gauge, extension), support flags, the precision ladder, the suffix decoder, and PCG64's deviation from the idealised law.
- **Statistical:** percentile-bootstrap bounds are nominal, conditional on the weights, charts and gauges.

## 8. Error rates (protocol §8.3)

Each one-sided bound uses α = 0.05/3. A false SUPPORT_j and a false EXCLUDE_j each have probability ≤ α (nominal), and they are disjoint opposite-tail events. The combined per-model false-claim probability is ≤ 2α. Across three models (Bonferroni) the bound is 6α = 0.10 for any false definite claim; each directional family has 0.05. Each all-three verdict has α; the union of the two erroneous overall verdicts has 2α.
