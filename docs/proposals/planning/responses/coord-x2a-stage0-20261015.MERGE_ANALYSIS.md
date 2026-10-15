# Merge analysis: coord-x2a-stage0-20261015 (X = Codex, L = Claude)

Analyst: clean-context comparison subagent (coordinator c351b245). Read-only; no Python, no runs, no git writes.
Inputs: the request, `coord-x2a-stage0-20261015.codex.md` (X, FREEZE_READY), `coord-x2a-stage0-20261015.claude.md` (L, DRAFT).
Code checked at main @ c364f95: `process/{transition,emission,centers,_geometry}.py`, `contracts/layout.py`,
`oracle/_common.py`, `tools/x4_oracle_profile/oracle_profile.py`, `tools/d1_seam/`, `docs/proposals/X6_TOPOLOGICAL_INVARIANTS.md`.
Labels: **[V]** verified by hand in this note. **[H]** is a hand estimate from a Gaussian/Whittle approximation (§2.1), good to
about a factor of 2. No [H] value should become a gate.

**Bottom line.** Recommendation (i): merge and freeze one protocol on **L's Dehn-twist construction** with L's P3/P4 gates at
t* = 32 and five amendments (§4). STOP is not nearly certain: by [H] estimates P3 and P4 are likely to pass, and only L's P5
(an un-derived 0.01-nat constant) is a coin flip. X's blur is mathematically valid, but it is a local noise-level
difference (exactly A followed by an i.i.d. symbol channel). Its information grows almost additively from k = 2, so it is the
weaker priority-1 instrument. X's 512-step gate also passes for almost any small-rate pair.

---

## 1. Mathematical verification

### 1.1 Facts shared by both plans (both correct) [V]
- Each component's T is symmetric and doubly stochastic, and the start is uniform. Given c, the hidden chain is stationary,
  so (c, W_{t−k+1:t}) has the same law as (c, W_{1:k}). **L's T3 holds**: I(c; window_k) = I_k = JS(P_A^(k), P_B^(k)) at
  every t ≥ k, and the window Bayes accuracy is acc_k. X's "independent of t ≥ k" is the same statement.
- Restarting the window filter from π̃ = 1/288 is exact. The state law at the window start is uniform given either component,
  so it does not depend on c. Both `suffix_posterior` (verified: batched, any length, stationary restart) and
  BayesFilter-on-a-slice give the exact window posterior.
- The pilot defaults are verified in code: p_stay = 0.2 with each of 4 moves at 1/5 (`transition.py`), centres
  (0.5+2a, 0.5+2b) (`SPEC.md`/`GridCenters`) and σ = 1.25. `check_tokens` caps the oracle at 33 symbols, and
  `analysis_position = 32` means w_1..w_32.

### 1.2 L: Dehn twist E_B[z] = E_A[φz], with φ(x,y) = (x+y, y)
| Claim | Check | Status |
|---|---|---|
| Factorised field, Z = 1.566642 for every x, and the p(d) table | All x share the distance multiset {0.5,…,5.5}. e^{−d²/3.125} = .92312, .48675, .13534, .01984, .00153, .0000626, with sum 1.56664 | correct [V] |
| T1: column sums are 4, so P(W_t=j given c) = 1/36 | Shift-by-2 equivariance e[x+2,a+1] = e[x,a]; Z₆² is transitive; E_B is a row permutation | correct [V] |
| φ is a non-isometric SL(2,Z) automorphism; operator norm = golden ratio | Edge (0,0)–(0,1) maps to (0,0)–(1,1) | correct [V] |
| Lemma U: in emission coordinates B steps 0, ±(1,0), ±(1,1) | φ is linear, so T(z,z′)=K(z′−z) pushes forward | correct [V] |
| T2: Δ_rep = (a/2)G(1)(G(0)−G(1)) | H(d)=6G(d) by equivariance. Difference (1/720)(2H0H1−2H1²) = 0.1·G1(G0−G1) | correct [V] |
| G(0)=0.902700, G(1)=0.769233, Δ_rep=0.010267, P_A=0.17962, P_B=0.16935 | Recomputed: 0.90270, 0.76923, 0.01027, 0.179621, 0.169354 | correct [V] |
| Repeat-indicator bound I_2 ≥ 9×10⁻⁵ nats | Δ²/(8 p̄(1−p̄)) = 1.054e−4/1.152 | correct, but loose (full I_2 [H] ≈ 1–3×10⁻³ nats) |
| Σ_A = 0.4I, Σ_B = [[.8,.4],[.4,.4]]; det = 0.16 for both; KL = 0.5 nats per noise-free step | tr(Σ_B⁻¹Σ_A)=3 | correct [V] |
| T4: I_t → ln 2 (distinct ergodic laws are mutually singular) | Standard | correct |
| T6: grid automorphism gives identical laws | It is a path bijection that preserves π and T | correct |
| Hoeffding ≈ 3×10⁻³ nats at n = 2¹⁹ per stratum, δ = 1e−6 | ln2·√(ln(2e6)/2²⁰) = 2.6e−3 | correct [V] |

### 1.3 X: symmetric blur E_B = K E_A, with K = ¾I + ⅛R₊₂ + ⅛R₋₂ along x
| Claim | Check | Status |
|---|---|---|
| Valid emission | Rows are convex combinations of rows of E_A, so they sum to 1 and every entry is > 0 | correct [V] |
| Exact marginals 1/36 | K is doubly stochastic (each R is a permutation). E_A column sums are equal by shift-by-2 equivariance with integer centres (2a,2b) | correct [V] |
| Not a P-world | ‖KE_A‖_F < ‖E_A‖_F strictly, because κ_m = ¾+¼cos(4πm/12) < 1 off m ∈ {0,6} and E_A columns are not 2-periodic. Row permutations preserve the Frobenius norm | correct [V] |
| Two-symbol witness S_A − S_B = (1/12)gᵀ(L − KLK)g ≥ 0, strict | Fourier: (1/144)Σ_m ĝ_m² λ_m(1−κ_m²). λ_m ∈ [½,1], since T₀ has stay ½ so L is positive definite. g(0)=0.638 > g(2)=0.177 rules out a pure {0,6} spectrum | correct [V]; magnitude S_A ≈ 0.0725, S_B ≈ 0.0583 [H] |
| Wrapped Gaussian is smooth; the min-distance field has cut-locus kinks | True for the continuum field. Immaterial on the lattice | correct, minor |

**Key identity that X does not state** [V]. Equivariance gives E_A(z+2e_x,(a,b)) = E_A(z,(a−1,b)), so
E_B(z,(a,b)) = ¾E_A(z,(a,b)) + ⅛E_A(z,(a−1,b)) + ⅛E_A(z,(a+1,b)).
**B is A's output passed through a memoryless symbol channel a ↦ a+ξ (mod 6)**, with ξ ∈ {0,±1} drawn i.i.d. each step
with probabilities ¾, ⅛, ⅛. B is therefore a garbling of A. The components differ in per-emission x-noise (variance about
1.56 for A and 2.56 for B), not in geometry or dynamics. This is the "different σ" alternative that L rejected, in another
form. It is not a P-world, but it is also not the "smooth non-isometric warp" that the request asked for.

### 1.4 Errors and defects found
**X**
1. *Conceptual (major for priority 1).* Because B is A plus i.i.d. symbol noise (§1.3), the evidence lives at short
   timescales and accumulates almost additively (§2). X notes the noise difference (§3.7) but does not draw this conclusion.
2. *Gate horizon (major).* All information gates are at t = 512. The pilot context is 32 and BayesFilter is capped at 33.
   X concedes that a pass at 512 "does not justify a 32-token model study". Any pair with a per-step KL rate r satisfying
   8r ≪ 1 ≪ 512r passes I_512 ≥ 0.8 and G_8 ≥ 0.6, so the gate mostly screens r. It does not screen long-range structure.
3. *Unforced departures from the pilot:* p_stay = ½ instead of 0.2, and integer centres instead of 0.5+2a. They are not
   errors, but they break like-for-like comparison with E-series worlds. The ½ stay also raises same-state repeats, which
   feeds the local noise signal.
4. *Stale provenance:* "the research checkout does not contain tools/d1_seam". It does now: main = c364f95.
5. *Cost overstated:* `suffix_posterior` is batched (n×288 @ 288×288). 1.4×10¹² MAC is roughly minutes to tens of minutes
   single-thread with BLAS, not 2–6 h. This is harmless.

**L**
1. *G1 tolerance is ambiguous and could fail as written.* "Brute-force 2-D softmax over the 9 deck images" must mean
   **minimum over images**. If the images are summed (a wrapped Gaussian), the farthest centre (d = 5.5, p ≈ 4.0e−5) gets an
   extra image term of relative size e^{−(42.25−30.25)/3.125} ≈ 0.021. That is an absolute difference of about 8.6e−7,
   far above the 1e−15 tolerance. Specify min-image.
2. *Overclaim in the Remark/OQ5.* "This class always leaks at k = 2" is **proved only for the Dehn twist (T2)**. For other
   smooth warps it is generic but unproven: the pair law is a local functional, and cancellation is non-generic. Reword it.
3. *Stale OQ1:* c364f95 is now on main, so bind main @ c364f95.
4. *P5 threshold is un-derived and sits on the forecast.* §2 gives V_32 ≈ 0.004–0.012 nats [H]. A gate at 0.01 would decide
   GO/STOP on an arbitrary constant (L's own OQ3).
5. *Reuse-first:* the t ≤ 128 extension makes a new stencil filter the *only* filter beyond 33 symbols, although the unchanged
   `suffix_posterior` already handles any length. Keep the stencil filter as an independent reference only.
6. *Minor:* the min-distance Gaussian is called "smooth". It has cut-locus kinks, but no lattice state lies on the cut locus
   (d ≤ 5.5 < 6), so this is harmless.

No error was found in either plan's marginal-equality proof, distinguishability proof or stationarity argument.

---

## 2. The decisive priority-1 issue

### 2.1 Approximation used [H]
Treat each symbol as a noisy position reading, y_t = z_t + n_t. For L's field the per-axis noise variance is
s² = Σ_d p(d)d² = 1.5625 [V]. For X, s_A² ≈ 1.56 and s_B² ≈ 2.56. Difference the readings: Δy_t = ε_t + n_t − n_{t−1}.
The spectral density is S_c(ω) = Σ_c + 2s²(1−cos ω)·I. The KL per frequency bin is ½[tr(S_B⁻¹S_A) − d + ln det S_B/det S_A].
Get the window KL from Whittle bins ω_j = 2πj/(k−1), then convert KL to I and acc with a Gaussian-LLR (EXIT J-function)
approximation. The approximation ignores lattice quantisation and torus wrap. Wrap matters for L at k = 32: B's x-displacement
has std ≈ 5 after 31 steps on a 12-cycle, so I_32 should sit at the low end of its range.

### 2.2 Where the evidence lives (the qualitative point)
- **L:** with ν = 2s²(1−cos ω), f(ν) = 0.50, 0.16, 0.09, 0.04, 0.008 and 0.0025 at ν = 0, 0.25, 0.5, 1, 3.1 and 6.25.
  Discrimination is concentrated at **ω ≲ 0.6, i.e. timescales of about 10 steps or more**: the anisotropic diffusion
  becomes visible only once accumulated displacement beats the reading noise. I_k is **superlinear** in small k.
- **X:** f(0) = 0, rising to about 0.05–0.07 at ω = π. Discrimination is at **ω ≳ 1, i.e. timescales of 2–6 steps**.
  I_k grows **roughly linearly from k = 2**; this is i.i.d. evidence accumulating.

### 2.3 Orders of magnitude [H] (bits unless marked)
| Quantity | L (twist, p_stay 0.2) | X (blur, p_stay ½) |
|---|---|---|
| I_1 | 0 (exact) | 0 (exact) |
| I_2 | 2–5×10⁻³ (repeat indicator alone ≥ 1.3×10⁻⁴) | 1.5–3×10⁻² |
| I_4 | 1–3×10⁻² | 4–8×10⁻² |
| I_8 | 0.04–0.10 | 0.07–0.20 |
| I_32 | 0.25–0.45 | 0.30–0.50 |
| I_512 | → about 1 (wrap-limited rate) | > 0.99 |
| I_8 / I_32 | about 0.1–0.25 | about 0.25–0.4 |
| acc_8, acc_32 | about 0.62, 0.75–0.85 | about 0.65, 0.78–0.85 |
| Additive share: KL of 4 disjoint 8-blocks ÷ KL_32 | about 0.55 | about 0.9 |
| V_32 (nats) ≈ per-step increment i_32 | 0.004–0.012 | 0.004–0.010 |

### 2.4 Are the gates attainable?
- **L at t* = 32.**
  - P3 (acc_32 − acc_8 ≥ 0.10): [H] gap ≈ 0.13–0.21. Likely PASS.
  - P4 (I_8 ≤ ½ I_32, conservative bounds): ratio ≈ 0.1–0.25. Likely PASS.
  - P5 (V_32 ≥ 0.01 nats): ≈ 0.004–0.012. Coin flip, leaning FAIL. This is the binding gate.
  - Q2-full (β̂₀ = 2 at 32) is near-impossible, because acc_32 is about 0.8 and unconcentrated histories bridge the clouds.
    L forecasts this correctly. **STOP is not nearly certain. It is likely only if P5 stays gating.**
- **X at t = 512.**
  - I_512 ≥ 0.8: near-certain.
  - G_8 ≥ 0.6: near-certain if U[I_8] ≤ 0.2.
  - U[I_8] ≤ 0.2: likely, but within the factor-2 error. The discrete ±1-symbol jitter may beat the Gaussian estimate.
  - GO is therefore likely. But under L's t = 32 lens X also roughly passes P3/P4 (ratio ≈ 0.3). X's gate does not separate
    the two mechanisms.

### 2.5 The confound neither plan gates: additive evidence accumulation
Priority 1 asks how much depends on earlier history. Both plans treat I_32 − I_8 > 0 as long-history information. That is
true, but it does not distinguish **(E1) summing many independent short-window evidences**, which a bag-of-n-grams counter
can do, from **(E2) long-timescale structure that no sum of short-window scores captures**. A trained probe that beats acc_8
(L's T5) is consistent with E1.

Oracle baseline, nearly free from posteriors already planned: the product-of-experts over the 4 disjoint 8-windows of
w_1..w_32, giving π_add ∝ Π_b LR_8(block b) with acc_add and I_add. By [H], L keeps roughly 45% of KL beyond additive.
That is an acc_32 − acc_add gap of about 0.05–0.07. X keeps only about 10% (gap ≲ 0.02). **This is the observation that
discriminates the two constructions, and it favours L.**

### 2.6 Is L's claim correct that k = 2 leakage is unavoidable and holonomy is needed?
- *Exact window-blindness needs locally identical, globally different labelled structure.* Correct.
  - If both components carry the same label field ℓ and the field descends to both quotients, then ℓ descends to the common
    coarser quotient. Both components are covers of it, and a covering projection preserves the walk-plus-emission law, so
    the laws are identical. With equal 144-state 12×12 tori and label period 12Z², the quotients simply coincide.
  - Differences therefore require a **label twist (holonomy) at a gluing**. An ordinary relabelling twist creates new
    symbol adjacencies at the seam that are visible at k = 2; L's twisted-lattice row makes this point.
  - Blindness also needs the twist to be locally invisible, i.e. a gauge or hidden-fibre construction such as X6's
    anchor-sign transport.
- *"Smooth torus pairs always leak at k = 2":* proved for the twist and generic otherwise. As a universal statement it is not
  a theorem (§1.4 L2). It also matters less than its framing suggests. Exact I_8 = 0 is not needed for a T5-style test; a
  measured I_8 ≪ I_32 is enough.
- *"Non-abelian" is not required.* The documented X6 transport task uses **Z₂ (abelian)** flat transport and equalises only
  unigram and bigram laws. Its six-edge winding means windows of about 8 symbols or more (reveal, wind, reveal) are
  informative. So X6 also needs its own I_k curve and is not automatically 8-window-blind.

---

## 3. Conflicts table

| Axis | X (Codex) | L (Claude) | Merge ruling |
|---|---|---|---|
| Construction of B | ¾/⅛/⅛ blur along x by ±2 = A + i.i.d. symbol channel. Noise-level difference | Dehn-twist pullback (row permutation). Geometry/diffusion-anisotropy difference | **L.** Optionally keep X-blur as a descriptive "local-evidence" comparator (A4) |
| Dynamics / field | p_stay ½, integer centres, wrapped Gaussian | Pilot p_stay 0.2, pilot centres, min-image δ₁₂ | **L** (pilot-consistent). Fix G1 to min-image |
| Marginals | Exact: K doubly stochastic | Exact: row permutation plus equivariance (T1) | Both correct. L also equalises H(W∣Z) and the one-symbol posterior law |
| Distinguishability proof | Fourier two-symbol a-correlation. Strict via g(0)>g(2) | T2 repeat probability. Invariant under symbol and isometry relabelling | Both correct. L's is stronger (rules out "B = A up to naming") |
| Window stationarity | Stated | T3 theorem | Both correct |
| Computation | MC only above k=2: 16,384 × 512, `suffix_posterior`, 64-claim Hoeffding | Exact for k ≤ 4. MC 2²⁰ × 33, BayesFilter, 99% CLT plus Hoeffding, chain and Rao–Blackwell checks | **L** for gating. X's `suffix_posterior` for the descriptive long horizon (A5) |
| Primary position | t = 512 (outside the pilot context) | t* = 32 (pilot analysis position) | **L** |
| GO criteria | L[I_512] ≥ 0.8 b, U[I_8] ≤ 0.2 b, L[G_8] ≥ 0.6 b, plus PH | P3 acc gap ≥ 0.10, P4 I_8 ≤ ½I_32, P5 V_32 ≥ 0.01 nats | **L P3+P4.** P5 becomes descriptive. Add the additive tier (A3) |
| PH route | Hellinger VR at 512. Band from in-space reference families q^{(ρ)}. 3/4 panels. 19 Gaussian-null surrogates | Hellinger VR at 32. τ from Euclidean synthetic shapes. h₀ band from X¹/X^½. 7/8 panels. P-ref specificity | **L's positions and controls, plus X's in-space reference calibration** for the H1 band (Euclidean C-syn transfers poorly to the probability simplex) |
| Units | bits | nats | Report both. Gates in the unit frozen |
| Cost | 2–6 CPU-h (overstated) | about 25 CPU-min | About 30–45 CPU-min with A3–A5 [H] |
| Licence | Statement at 512. Explicitly not a 32-token study | Oracle facts for one construction. T5 contrapositive for later probes | L, plus the additive-tier wording (A3) |
| Status | FREEZE_READY | DRAFT (needs OQ re-derivation) | Merge to L-based v1, then independent re-derivation, then freeze |

---

## 4. Recommendation: (i) merge and freeze one stage-0 protocol on L's construction

**Construction (frozen):** L §2 unchanged: Dehn twist φ(x,y) = (x+y, y), p_stay 0.2, σ = 1.25, pilot centres, min-image
δ₁₂, uniform start, N = 288, V = 36.

**Amendments:**
- **A1 (fixes):**
  - G1 compares against the **minimum over the 9 images**, not their sum.
  - Bind main @ c364f95.
  - Reword the Remark/OQ5 per §2.6 ("proved for the twist; generic otherwise"; abelian holonomy suffices for blindness;
    X6 is not automatically 8-blind).
- **A2 (gates):** GO_P1 ⟺ **P3 ∧ P4**, both with L's 99%-interval and THRESHOLD_INCONCLUSIVE rule. **P5 becomes descriptive**:
  report V_32 with a trained-stage feasibility flag at 0.01 nats. Reason: its threshold is a judgment that the [H] forecast
  straddles, and stage 0 authorises no training.
- **A3 (priority-1 sharpening, required):**
  - Add the oracle **additive baseline** π_add, the product of the 4 disjoint 8-window likelihood ratios over w_1..w_32
    (equal prior). Report acc_add, I_add and the paired acc_32 − acc_add.
  - Split GO_P1 into **GO_P1_NONADDITIVE**, if the lower 99% bound of acc_32 − acc_add is ≥ 0.03, and
    **GO_P1_ADDITIVE** otherwise. The licensed sentence must state which.
  - This adds no new STOP route. It only prevents E1 from being reported as long-range structure.
- **A4 (optional, recommended):** add X's blur, applied to L's field and dynamics, as a descriptive comparator **N-local**.
  It needs no gates and costs about 5 CPU-min. It is the positive control for A3, expected to show acc_add ≈ acc_32.
- **A5 (reuse-first):** run the descriptive horizon curve (t ≤ 128, and optionally 512 as X proposed) with the unchanged
  `tools/x4_oracle_profile.suffix_posterior`. L's stencil filter stays only as the independent numerical reference
  (G4 subset).
- **PH:** keep L's clouds, controls and panel rule. Replace C-syn with X's in-space reference families q_{c,z}^{(ρ)} to set
  the H1 band (§6.2 of X, applied at t* = 32). Keep C-emis and C-H0. PH outcomes stay graded separately and do not enter
  GO_P1.

**Why not (ii).**
- STOP is not nearly certain: P3 and P4 are forecast to pass with margin, and only P5 was marginal.
- Cost is under an hour of CPU.
- The result is a needed calibrated decomposition: symbol statistics (0), short-context, additive, and non-additive
  long-history information for a topological β₀ distinction. The T5/additive machinery transfers directly to X6.
- L's OQ5 remains a **scoping limit**: X2a can show a quantitative gap, never exact short-window blindness. If the owner's
  target is blindness, X6 (abelian Z₂ transport suffices) is the next one-at-a-time stage 0. It needs its own I_k curve.

**Charter justification.**
- *Priority 1* asks to "distinguish symbol statistics, short-context information, full-history beliefs". L at t* = 32
  with A3 measures exactly those layers, at the pilot's own position.
- *Competing explanations with discriminating observations*: A3 and the N-local comparator separate E1 from E2. Neither
  plan's original gates did.
- *Reuse-first*: unchanged BayesFilter, `suffix_posterior`, HMMSampler, PH stack and the D-1 local-builder pattern.
- *Quality over speed / scoped negatives*: a GO_P1_ADDITIVE or STOP is reported as a scoped finding for this construction.
- *Caveat to carry into the licence*: X2a concerns **component identity**, not the learned circular coordinate itself.
  Within-component circular structure under O stays largely last-symbol-decodable. Its relevance to priority 1 is
  therefore by analogy (a topological distinction that history must supply), and that should be stated.

## 5. Items for the coordinator before freeze
1. Independent re-derivation of L's T1–T7 and Lemma U (L's OQ6). §1.2 already confirms the closed forms and the hand values.
2. Ratify A2 (P5 descriptive) and the A3 margin of 0.03. The margin is a judgment, set below the [H] L-gap of about
   0.05–0.07 and above the X-gap of ≲ 0.02.
3. Decide whether A4 (the N-local comparator) is in scope. It is cheap, and it is the only empirical positive control for
   the additive tier.
4. Record the [H] forecasts of §2.3 in the frozen protocol as forecasts. They are not criteria.
