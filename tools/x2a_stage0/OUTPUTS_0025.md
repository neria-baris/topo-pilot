# X2a stage 0: outputs of job 0025 (X2A-FROZEN-v1)

**Protocol:** `agent-handoff/planning/responses/X2A-FROZEN-v1.md`, sha256 C80808CB7F22D9A171385FCB1AB7D03973E80DAFE638DFA758B6A84CA8341939.
**Run:** HEAD 218b02b9e5142d9d95321f20488e25fc01c9bf7b on branch x2a-0025; one metered run; frozen seeds (MASTER_X2A0 = 20261015).
**Store:** `X:/Downloads/projects/topo-pilot/x2a-stage0-oracle-store/`.
**Scope:** oracle only. There is no model, no training and no activations. Every value below is an oracle fact about this one frozen construction.

## Verdict

| Item | Result |
|---|---|
| Validity | **PASS**: PF, S0 and G0–G5 all PASS |
| Scientific outcome | **GO_P1_NONADDITIVE** |
| P3 | **PASS**: D3 = acc_32 − acc_8^win = 0.19118 (SE 0.00032; 99% interval [0.19036, 0.19200]); the PASS rule L99 − τ ≥ 0.10 holds |
| P4 | **PASS**: U99(I_8^win) = 0.06763 ≤ ½·L99(I_32) = 0.16232 |
| A3 | **NONADDITIVE**: D_add = acc_32 − acc_add = 0.05666 (SE 0.00017; 99% interval [0.05621, 0.05710]); L99 ≥ 0.03 |
| Bound robustness (Hoeffding, δ = 0.01) | P3, P4 and A3 unchanged |
| P5 (descriptive) | V_32 = 0.009828 nats (99% interval [0.009799, 0.009858]): **INCENTIVE_BELOW_0.01** |
| PH Q1 | **PASS**: β̂₁(B_PH) = 2 in 8/8 panels for both A and B; P-ref = 2 in 0/8 panels |
| PH Q2 | **NOT_SEPARATED** (the forecast outcome): full-history mixture beliefs form one retained cluster in 8/8 panels |
| N-local reading rule | **EXPECTED_BELOW_0.03**: U99(acc_32^N − acc_add^N) = 0.0079 < 0.03, so no qualifier |

**Licensed sentence (§1.4, GO_P1_NONADDITIVE):** "In a T²⊔T² process with exactly equal symbol statistics, where component B is component A's emission field pulled back by a Dehn twist, the last symbol carries no component information (exact). The last k symbols carry I_2 = 0.00207 and I_4 = 0.01617 nats (exact) and I_8 = 0.0674 nats (validated Monte Carlo), and the full 32-symbol history carries I_32 = 0.3252 nats. Bayes accuracy rises from acc_8 = 0.639 to acc_32 = 0.830, and the full history beats the specified product of four disjoint 8-symbol block likelihood ratios by 0.0567 (lower 99% bound 0.0562 ≥ 0.03). This does not establish that no other aggregation of short-window evidence could reproduce the advantage." "This concerns component identity, not the circular coordinate. Short windows are not blind: I_2 > 0. All pre-run information-size estimates were forecasts; decisions use computed quantities."

The N-local reading rule did not trigger, so the qualifier sentence is not added. A3 concerns only this frozen four-block comparator; block boundaries fall between symbols 8/9, 16/17 and 24/25 (§1.4, §5.6).

## Information curves (nats; bits in parentheses)

**Exact, k ≤ 4 (G2):**

| k | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| I_k | 2.8e-32 (≈ 0) | 0.0020737 (0.0029918) | 0.0074388 (0.0107319) | 0.0161669 (0.0233239) |
| acc_k | 0.5 | 0.523787 | 0.545949 | 0.566791 |

**Monte Carlo (n = 2²⁰ stratified rows):**
- Hoeffding half-widths at δ = 1e-6: 0.001823 for I, 0.001315 for max-posterior accuracy, 0.002630 for credits.
- Î_t:

| t | 1 | 2 | 4 | 8 | 16 | 24 | 32 |
|---|---|---|---|---|---|---|---|
| Î_t | 0 | 0.002078 | 0.016175 | 0.067559 | 0.170454 | 0.255175 | 0.325239 (SE 0.00023; 0.4692 bits) |

- âcc_t at t = 2, 4, 8, 16, 32: 0.5238, 0.5668, 0.6390, 0.7302, 0.8304.
- **Windows at t\*:**

| k | Î^win_k (SE) | âcc^win_k (max form) |
|---|---|---|
| 2 | 0.0020731 (4.4e-6) | 0.52377 |
| 4 | 0.016149 (3.1e-5) | 0.56678 |
| 8 | 0.067374 (1.0e-4) | 0.63872 |

  The gate-form credit âcc_8 is 0.63923. I_8/I_32 = 0.207.
- **Additive tier:**
  - acc_add = 0.77376;
  - I_add^LB = 0.22721;
  - ρ_add (KL share) = 0.572;
  - acc_add − acc_8 = 0.1345;
  - paired I_32 − 2I_8 = 0.1905.
- **Concentration and LLR:**
  - share of rows with max(π, 1 − π) ≥ 0.9 at t = 32: 0.398; with ≥ 0.99: 0.111;
  - LLR slopes over t ∈ [16, 32]: −0.0708 (A) and +0.0839 (B) per symbol.
- **Context gains:** the last-symbol context gain at t\* is 0.2965 nats; the full-history gain over the 8-window is 0.0069 nats. These mix position and component information.
- **Long horizon** (descriptive; 2¹⁶ rows; reliability **RELIABLE**: stencil 7.9e-14, Decimal 8.3e-17):

| t | 32 | 48 | 64 | 96 | 128 |
|---|---|---|---|---|---|
| Î_t | 0.3247 | 0.4311 | 0.5047 | 0.5947 | 0.6405 |
| âcc_t | 0.830 | 0.887 | 0.922 | 0.961 | 0.980 |

  Î^win_8 is 0.06731 at t = 128 and 0.06739 at t = 32.

## Validation

**G0–G2 (exact):**
- 144 / 288 / 144 cells; χ = 0; Betti (1,2,1) over GF(2) and GF(3); ∂₁∂₂ = 0.
- Fraction error of T: 4.4e-17.
- E_A against the minimum-image brute force: abs error 2.2e-16, rel error 1.5e-15.
- Equivariance: 1.1e-16.
- Δ_rep closed form 0.0102670 = trace difference (error < 1e-17).
- Lemma U: 3.5e-18.
- Symbol translations: rel error 2.5e-15.
- I_2 against JS of the pair laws: rel error 4.2e-16.
- Every hand value [W] agrees with the computed value at its quoted precision.

**G3 (oracle cross-checks on 2¹⁴ rows):**
- stencil beliefs 4.1e-15; π 1.7e-14;
- per-component expit 1.7e-14;
- mixture predictive 3.6e-16;
- evidence (rel) 7.1e-14;
- `suffix_posterior` 0 (exact equality);
- **80-digit Decimal reference on 24 histories: 8.3e-17**.

**G4 (Monte Carlo against exact):** all 49 four-SE comparisons pass. For example:
- Î_2 = 0.002078 vs I_2 = 0.0020737 (SE 4.4e-6);
- Î_4 = 0.016175 vs 0.016167 (SE 3.1e-5);
- âcc_4 = 0.566826 vs 0.566791 (SE 1.5e-4).

**G5 (required controls):**

| Control | Result |
|---|---|
| N-iso | exact I_k ≤ 3.8e-32; MC \|π − ½\| ≤ 4.4e-16 |
| N-same | exact 0; MC 3.9e-16 |
| N-id | beliefs exactly uniform; π 1.1e-16 |
| N-swap | \|π′ − (1 − π)\| ≤ 6.7e-16; estimates unchanged ≤ 2.2e-16 |

## Descriptive controls

**N-local (2¹⁸ rows):**
- I_32 = 0.2406, I_8 = 0.0678;
- acc_32 = 0.7858, acc_8 = 0.6442, acc_add = 0.7781;
- D_add^N = 0.0077 (99% interval [0.0075, 0.0079]);
- ρ_add = 0.933.

**P-ref (2¹⁸ rows):**
- exact I_2 = 0.1050 and I_4 = 0.3091;
- I_8 = 0.526, I_32 = 0.691;
- acc_32 = 0.9993, acc_add = 0.9982.

  The original X2a design exposed most component information to short windows.

## PH route

- **K1:** band B_PH = [0.6611, 0.7850], from S = [0.5991, 0.8470).
- **K2:** two H1 bars with persistence ≥ 1.0.
- **K3:** m = 0.6371, h₀\* = 0.8185.
- **C-emis:** β̂₁ = 2.
- **Q1:** A and B give β̂₁ = 2 in 8/8 panels.
  - P-ref's β̂₁ in the 8 panels is 23, 20, 27, 22, 29, 19, 23, 24, never 2. So Q1-spec holds by the frozen rule (β̂₁ = 2 not reached). **Note:** the P-ref counts are far *above* 2, not below; the rule is literal.
  - Noise floor: 40 covariance-matched surrogates, all with β̂₁ = 0, so no "not distinguished from a Gaussian null" qualifier.
- **Q2:**
  - full: one retained cluster in 8/8 panels;
  - window-8: one cluster in 8/8;
  - X¹: two clusters with purity 1 in 8/8;
  - N-iso: one cluster in 8/8;
  - N-id: COLLAPSED in 8/8;
  - retained fraction 1.0 everywhere.

  Q2-curve β̂₀ = 1 at every t ∈ {1, 2, 4, 8, 16, 24, 32}.

## Files

| File | sha256 |
|---|---|
| report.json | 285bc6ca317a73a7678e9e0d3328c1351837ef893c2bb70ab3aacfefbedda028 |
| model.npz | 68cdf36fe75b32c2141d3e476737b4a28d4247012fb64500c53f55b99b70118b |
| ph_diagrams.npz | 0e21b058b0e8654abbbb85aefc76d891114a8ecdc3b80434b35913a179b7807b |
| preflight.json | 6dcf74bac0647da52d431b22ef5cc50c6990a35363a536830076134f010ed6b8 |
| cpu_ledger.json | f077afef57b09f943a00588753e3d049b98e3c11cb19039dd6d3fc538179ba2c |

**Array hashes in model.npz (sha256 of the array bytes):**

| Array | sha256 |
|---|---|
| T | 4a6c9159… |
| e | 690cece1… |
| E_A | e9195fbc… |
| E_B | cd40a3f1… |
| E_N | ce5e3a67… |
| E_P | 246fd1d2… |

The full values are in report.json.

**Seeds:**
- The main tree's issued map is in report.json under `seeds`.
- P-ref helper: SeedTree(0) stream ("axis_permutation", "_x2a_torus_local"), seed 1606601844618191212, with:
  - sx = [8, 1, 5, 3, 11, 0, 2, 9, 4, 10, 6, 7];
  - sy = [7, 10, 5, 9, 2, 8, 11, 4, 3, 0, 6, 1].
- **Exposure rule:** these stage-0 histories are oracle-only and must not be reused by a trained stage.

**CPU:** run 1750.5 CPU s, 1740.9 s wall, one thread, peak job commit 3.7 GB. Preflight 18.5 CPU s.
