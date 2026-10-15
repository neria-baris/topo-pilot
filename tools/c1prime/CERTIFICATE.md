# C1′ numerical certificate: implementation specification (§15.3 as frozen)

This file specifies how the frozen §15.3 of `PROTOCOL_C1PRIME_v1.md` (sha256 0B1F107E…F33A) is implemented. The protocol is authoritative. This file adds no target, coefficient, bound, guard, rank, precondition or route rule. It only fixes the implementation details that the protocol delegates (the A1 self-test vectors, coordinator ruling 7) and the exact code-level shapes.

## 1. Certified decisions and coverage (§15.3.1)

The certificate covers three decision types:
- (E) the per-model endpoint statuses at NUM (row 21);
- (H) H5 on validation (row 5) and on fresh rows (row 20);
- (V) V3 on validation (row 18) and on fresh rows (row 20).

The exact counterpart reads the stored float64 T, E_canon and π, and the recorded float64 logits, as exact reals.

Coverage:
- every eligible row of the gated split;
- both donor histories H⁺ and H⁻ (the oracle is canonical and computed once per row);
- the primary pair, the 32 control pairs and the full-donor pair;
- all three models.

No row is removed. A P1 failure routes the history to route F.

Operational only (not certified): eligibility, κ_ν, every fit, the M/F/V1/V2 gates, the P1 ladder, θ̂, the calibration Ḡ and the secondary quantities.

## 2. Prescribed kernels (§15.3.2)

| Kernel | Implementation | Module |
|---|---|---|
| C0 reference oracle | `c1_cert.reference_oracle` | Ordered sums `osum` over the explicit lists S_col(z) and S_row(z), each read from T > 0 in ascending order. Elementwise numpy `+ − * /` only, vectorised over rows. No `@`, `dot`, `matmul`, `einsum`, `sum` or `mean`. TE^ref is computed once. |
| C1 operational oracle | `oracle.BayesFilter` unchanged, via `c1_oracle.run_oracle` | Not assumed; it enters only through r_h |
| C2 logs | `np.log(q̂)` stored | Measured by M-ln |
| C3 G | `c1_oracle.G_hat` | d = q̂⁺ − q̂⁻, λ = ℓ̂⁺ − ℓ̂⁻, G = 0.5·osum_v(d_v·λ_v), with v in canonical order 0..35 |
| C4 A | `c1_endpoint.A_hat` | Δ = z⁺ − z⁻ (canonical gather), A = 0.5·osum_v(d_v·Δ_v) |
| C5 Y | `c1_endpoint.Y_hat` | m = osum_r(A_{C_r}) for r = 0..31, then ·2⁻⁵; Y = A_T − m |
| C6 Z | `c1_endpoint.Z_hat` / `Zfull_hat` | Z = Y − (0.1·G); Z_full = A_full − (0.3·G) |
| C7 means and quantiles | `c1_means.tree_mean`, `bootstrap_means`, `quantile_with_rank` | Balanced pairwise tree, then one division by n. One `rng.integers(0, n, size=n)` per draw. inverted_cdf with a run-time rank check. Ranks: 250 for H5, 84 for V3 and L, 4917 for U. |

`osum(cols)` is a left-to-right accumulation over a Python list of per-row arrays: `acc = cols[0]`, then `acc = acc + cols[k]`. Multiplication and addition are separate numpy operations.

## 3. Preconditions and their statuses (§15.3.3)

| Precondition | When | Check | Failure |
|---|---|---|---|
| P0 | H1 (S3) | In exact rationals: E_canon > 0, π > 0, T ≥ 0 with a positive diagonal; N = 144, V = 36; d (the maximum row or column support of T); π_min·ε_E ≥ 2⁻¹⁰⁰⁰ and τ⁺·ε_E ≥ 2⁻¹⁰⁰⁰; the three models' E_canon bitwise identical. ω_TE and ν₀ are recorded. | FAIL_TECHNICAL/IDENTITY |
| P1 | per history (C0) | every b̂_t(z), t = 1..32, finite and ≥ ν₀, exactly | not an error: route F |
| P2 | per certified row and model | see §5 | FAIL_TECHNICAL/NUMERICAL |
| P3 | every certificate Decimal computation | no trap; no Underflow, Subnormal or Overflow flag | FAIL_TECHNICAL/NUMERICAL (`CertificateFlag`) |
| P4 | per history | r_h ≤ 1/2 (main route) or x ≤ 1/2 (route F) | FAIL_TECHNICAL/ORACLE |

**A1 self-test (fixed here; coordinator ruling 7).** The test is run at H1 on numpy float64 arrays (elementwise, as the certified kernels use them) and on Python floats. Each case records the observed value. `ok` is True iff every case marked "required" holds. The subnormal case is recorded, and either outcome is consistent with A1's below-normal model.

| # | Case | Expression | Required result |
|---|---|---|---|
| 1 | round-half-to-even tie, down | 1.0 + 2⁻⁵³ | == 1.0 (required) |
| 2 | round-half-to-even tie, up | 1.0 + 3·2⁻⁵³ | == 1.0 + 2⁻⁵¹ (required) |
| 3 | correctly rounded quotient | 1.0 / 3.0 | == float(Fraction(1, 3)) (required) |
| 4 | correctly rounded quotient | 2.0 / 3.0 | == float(Fraction(2, 3)) (required) |
| 5 | correctly rounded product | 0.1 · 3.0 | == float(Fraction(0.1)·3) (required) |
| 6 | exact scaling | 0.5·x and 2⁻⁵·x for x = 0.1 | == Fraction(x)/2 and Fraction(x)/32 exactly (required) |
| 7 | subnormal product | 2⁻⁵⁰⁰ · 2⁻⁵⁶⁰ | == 2⁻¹⁰⁶⁰ (gradual underflow) or 0.0 (flush-to-zero); recorded |
| 8 | no extended precision | (1.0 + 2⁻⁵³) − 1.0 evaluated as two separate numpy ops | == 0.0 (required) |

## 4. Constants (§15.3.4)

The constants are exact `Fraction`s in `c1_cert`:
- u = 2⁻⁵³ and u′ = u/(1 − u);
- γ_n = n·u/(1 − n·u);
- ζ = 2⁻⁸⁰⁰;
- ρ̄_ref(L, N, d) = [2(L−1)(d+2) + 2 + 2N + d]·u′, so ρ̄_ref(32, 144, 5) = 729·u′ and ρ̄_ref(32, 144, 144) = 9486·u′;
- ĉ₁ = Fraction(0.1) with δ₁ = |ĉ₁ − 1/10| = 1/(5·2⁵⁵), and ĉ₃ = Fraction(0.3) with δ₃ = 1/(5·2⁵⁴);
- d_n = ⌈log₂ n⌉.

`up(c)` is the smallest float ≥ c. `OUT(x) = (1 + 2⁻³⁰)·Fraction(x) + ζ`.

## 5. P2 limits (§15.3.3; coordinator ruling 7; review fix 1)

- Every logit used is finite with |z| ≤ 2¹⁹.
- q̂ is finite and > 0, and ℓ̂ is finite.
- Â, Ĝ, Ŷ, Ẑ and Ẑ_full are finite with magnitude ≤ 2²¹.
- ē_ℓ ≤ 2²¹.
- Every data leaf of bound evaluation is ≤ 2²³: q̂^±_v, |d̂_v|, |λ̂_v|, |Δ̂_v|, max_v|Δ̂_v|, ρ^±, ē_ℓ,i, |Â_{C_r}|, |Ĝ|, |Ŷ|, |Ẑ| and |Ẑ_full|.

## 6. Oracle bounds (§15.3.6–15.3.7)

- **Main route (P1 holds).** r_h = max_v |q̂(v) − q^ref(v)|/q^ref(v), exactly. ρ_h = ρ̄_ref(32, N, d) + r_h/(1 − r_h), stored as up(ρ_h).
- **Route F (P1 fails).**
  - b̃ comes from the 60-digit Decimal posterior (the provenance replica of `error_bound._reference_posterior`), with β = `posterior_envelope(32, N)`.
  - q̃ is the 60-digit Decimal predictive, with β_q = (1+β)(1+`gamma_digits(2N+2, 60)`) − 1.
  - r = max_v |q̂ − q̃|/q̃ and x = (1 + r)(1 + β_q) − 1. P4 requires x ≤ 1/2, and then ρ_F = x/(1 − x).
- **M-ln.** In `trapping_context(40)`, 𝓛 = Decimal(q̂(v)).ln(). e = |Fraction(ℓ̂(v)) − Fraction(𝓛)| + 10⁻³⁸·|Fraction(𝓛)|, and ē_ℓ,i = up(max e) over the row's 72 values. Every certificate Decimal context is K4's `trapping_context(prec)`. After each Decimal block its flags are inspected, and a set watched flag raises `CertificateFlag`.

## 7. Row bounds as implemented (§15.3.8–15.3.10; L5 counts)

Each bound is evaluated in float64, with every constant replaced by up(c), exactly in the displayed shape below:
- sums are left to right in the index order shown;
- ρ̄ = ρ + ρ·ρ is evaluated as written;
- (γ_V + u′), (u′ĉ₁ + δ₁) and (u′ĉ₃ + δ₃) are evaluated as displayed: one addition, or one multiplication and one addition.

The displayed bounds:
- ε^d_v = u′·|d̂_v| + ρ̄⁺·q̂⁺_v + ρ̄⁻·q̂⁻_v
- ε^λ_v = u′·|λ̂_v| + 2·ē_ℓ + ρ⁺ + ρ⁻
- b^G = ½·Σ_v [ε^d_v·|λ̂_v| + (|d̂_v| + ε^d_v)·ε^λ_v + γ_V·|d̂_v|·|λ̂_v|] + ζ
- b^A = ½·[(γ_V + u′)·Σ_v |d̂_v|·|Δ̂_v| + (1/(1−u))·(Σ_v ε^d_v·|Δ̂_v| + ω_TE·max_v|Δ̂_v|)] + ζ
- b^Y = u′·|Ŷ| + b^A_T + (1/32)·Σ_r b^A_{C_r} + (γ_31/32)·Σ_r |Â_{C_r}| + ζ
- b^Z = u′·|Ẑ| + b^Y + (u′ĉ₁ + δ₁)·|Ĝ| + (1/10)·b^G + ζ
- b^Zf = u′·|Ẑ_full| + b^A_full + (u′ĉ₃ + δ₃)·|Ĝ| + (3/10)·b^G + ζ

The node, monomial and degree counts of these shapes must not exceed the §15.3.5 table:

| Bound | Nodes | Monomials | Degree |
|---|---|---|---|
| b^G | 1,117 | 1,081 | 6 |
| b^A | 474 | 254 | 6 |
| b^Y | 15,711 | 8,416 | 7 |
| b^Z | 16,837 | 9,501 | 7 |
| b^Zf | 1,600 | 1,339 | 7 |

`c1_bounds.Sym` lets the tests recompute these counts by evaluating the same functions on counting leaves.

**Counting conventions.**
- A leaf has 0 nodes, 1 monomial and degree 1. Constants are leaves.
- For a + b: nodes = n_a + n_b + 1, monomials = m_a + m_b, degree = max.
- For a·b: nodes = n_a + n_b + 1, monomials = m_a·m_b, degree = d_a + d_b.
- Shared subexpressions are replicated, which follows from evaluating the tree.

## 8. Constants, guards and the decision theorem (§15.3.11)

The constants are evaluated as exact Fractions, with n the eligible-row count of the gated split:
- B_num,j = OUT(max_i b̂^Z_{j,i}) + γ_{d_n+1}·Fraction(max_i |Ẑ_{j,i}|) + ζ;
- B^H uses b̂^G and Ĝ in the same way;
- B^V3_j uses b̂^Zf and Ẑ_full in the same way.

The guards (exact rationals; floor 10⁻⁹):
- **(E)** F_j = max(B_num,j, 10⁻⁹). INCONCLUSIVE/NUMERICAL if |L_j| ≤ F_j or |U_j| ≤ F_j for any j.
- **(H)** Γ = lower − 1/100 and g = max(B^H, 10⁻⁹). PASS iff Γ > g; INCONCLUSIVE/HEADROOM iff Γ ≤ −g; else INCONCLUSIVE/NUMERICAL.
- **(V)** Γ_j = L^V3_j and g_j = max(B^V3_j, 10⁻⁹). PASS iff Γ_j > g_j for all j; INCONCLUSIVE/MODEL_HEADROOM iff Γ_j ≤ −g_j for some j; else INCONCLUSIVE/NUMERICAL.

A rank-check failure is FAIL_TECHNICAL/NUMERICAL.

## 9. Placement and records (§15.3.15)

**Placement:**
- P0 and the A1 self-test at H1.
- H3: the reference rows, with C0, P1, route F, r_h, M-ln and b^G.
- N0 (row 4a): validation eligible rows, with C0, P1, route F, r_h, P4, M-ln, P2 for q̂/ℓ̂/Ĝ, b^G and B^H.
- V3: b^A_full, b^Zf and B^V3.
- T-PRE: fresh N0, B^H and B^V3.
- NUM: b^A for the primary and control pairs, b^Y, b^Z and B_num.

**Records (immutable):**
- per history: ν_min, the route flag, r_h or (r, x), and ρ;
- per row: ē_ℓ, b^G, b^A_T, the mean b^A_C, b^A_full, b^Y, b^Z and b^Zf;
- per gate, as exact rational strings: the P0 constants, ρ̄_ref, B_num,j, B^H, B^V3_j, the ranks and rank-check counts, and the guard outcome;
- the E_canon digests, the A1 self-test record, and the numpy, Python and libmpdec versions.
