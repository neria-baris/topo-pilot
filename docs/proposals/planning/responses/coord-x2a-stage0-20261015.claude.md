STATUS: DRAFT

The protocol is complete as written. Two things stand between it and a freeze: the independent re-derivation of T1–T7 (as in D-1), and coordinator ratification of the items listed under Open questions (OQ1–OQ4).

# X2a-S0 (track L): corrected T²⊔T², stage 0, oracle only

| Field | Value |
|---|---|
| Request | `planning/requests/coord-x2a-stage0-20261015.md` (coordinator c351b245; owner authorisation B3-E) |
| Track | Claude planning track L. Planning only: no Python run, no test run, no data opened, no git write. The Codex response was not read. |
| Code read | Main @ c2046fc (`src/topo_pilot/{world,process,oracle}`, `topology/{persistence,summaries,distance,metrics,shapes}.py`, `dataset/sampler.py`, `contracts/layout.py`, `tests/world/test_world.py` (`_t_torus`), `tests/oracle_profile/independent_reference.py`). Branch d1-seam-0019 @ c364f95 (`tools/d1_seam/{API.md,d1_seam.py,d1_seam_checks.py,OUTPUTS_0020.md}`). |
| Docs read | `docs/EXTENSIONS.md` §3; `docs/RESEARCH_SUMMARY.md` §3–7; `docs/STAGES.md` (G-A); `D1-FROZEN-v1.md`; charter (`NEXT_RESEARCH_AND_WORKFLOW.md`, "Owner research charter") |
| Arithmetic | Every value marked **[L]** was derived by hand in this response and is not yet checked by any computation. Every gated quantity is computed by the run; no gate uses an [L] value. |

## Summary (≤ 300 words)

**Construction.**
- Two 12×12 tori (N = 288), no inter-component transitions, uniform start, the pilot's lazy walk (p_stay = 0.2) on a local unregistered torus builder.
- A emits the pilot's O field (V = 36, σ = 1.25), Gaussian on the doubly periodic flat metric, as an explicit array.
- B emits A's field pulled back by the Dehn twist φ(x,y) = (x+y mod 12, y), a smooth non-isometric diffeomorphism. E_B is a row permutation of E_A, so every one-state statistic is identical.

**Theorems.**
- T1: in both components, every symbol has probability exactly 1/36 at every t, so the last symbol carries no component information.
- T2: the repeat probability differs by (a/2)·G(1)(G(0)−G(1)) > 0 (≈ 0.0103 [L]). The laws differ under any relabelling of B's symbols.
- T3: under the stationary start, the last k symbols carry exactly I_k = JS(P_A^(k), P_B^(k)) at any position. One curve answers (a) and (c).
- T5: any function of the last k symbols decodes the component with accuracy at most acc_k.
- T6: an isometric copy gives π ≡ ½.

**Computation.**
- I_k: exact float64 enumeration for k ≤ 4.
- Monte Carlo: 2^20 stratified sequences, unchanged BayesFilter, checked against exact values, a stencil filter, the Decimal reference and Hoeffding bounds.
- PH: Vietoris–Rips/F₂ on Hellinger belief clouds, 8×512, G-A-style calibration; isometric, identical-emission and P-world controls.

**GO/STOP (fixed now).**
- GO_P1 iff acc_32 − acc_8 ≥ 0.10, I_8 ≤ ½·I_32 and V_32 ≥ 0.01 nats (V is the incentive to track the component).
- The PH routes are graded separately.
- Forecast, not a criterion: the posterior is only partly concentrated at t = 32, so β̂₀ = 2 is unlikely.

**Cost:** ≈ 25 CPU-min (range 15–60), one thread, uncapped.

**Licence:** oracle facts about this one construction only.

---

## 0. Notation

| Symbol | Meaning |
|---|---|
| c ∈ {A, B} | Component (hidden world), drawn once per sequence, P(c = A) = P(c = B) = ½ |
| z = (x, y) ∈ Z₁₂² | State within a component. Index i(x, y) = 12x + y, which equals `check_state_order`'s x·dims[1] + y. Mixture index 144·[c = B] + 12x + y |
| j = (a, b) ∈ Z₆² | Symbol with centre (0.5 + 2a, 0.5 + 2b). Token id 6a + b, which equals `GridCenters`'s j = a·k + b. No symbol renaming is applied; both components use one alphabet |
| a = (1 − p_stay)/4 = 1/5 | Probability of each of the 4 lattice moves; the stay probability is also 1/5 |
| K_c | Step law of component c in emission coordinates (§2.3) |
| P_c^(k) | Stationary law of k consecutive symbols given c |
| π_t(h) | P(c = B ∣ w_{1:t}): the component posterior, the "belief about the world" |
| π_t^(k)(h) | P(c = B ∣ w_{t−k+1:t}): the posterior from the window of the last k symbols |
| H_b(p) | −p ln p − (1−p) ln(1−p). All logarithms are natural; all information is in nats |
| I_t | I(c; W_{1:t}) = ln 2 − E[H_b(π_t)] |
| acc_t | E[max(π_t, 1 − π_t)], the Bayes accuracy of the component from w_{1:t} |
| b_c(h) | World-conditional belief over the 144 states of c, equal to the c-block of the 288-state mixture belief, renormalised |
| q_c(h), q(h) | b_c T E_c (world-conditional next-symbol law); q = (1−π)q_A + π q_B (mixture) |
| t* = 32 | Primary analysis position (the pilot's `SequenceLayout.analysis_position`) |
| k_s = 8 | Short-window cutoff for GO/STOP (largest k in the request) |

Event order: emit, then transition (`emit_then_transition`, as in BayesFilter and HMMSampler).

---

## 1. Question and scope

**Question (charter priority 1, applied to the world-identity variable).** In a T²⊔T² process whose components have exactly equal single-symbol statistics, how much information about the component is available:
- from the last symbol;
- from the last k = 1, 2, 4, 8 symbols;
- from the full history?

Supporting questions:
- How fast does the posterior concentrate?
- Do the exact belief clouds carry each torus's H1 and separate the components, at a calibrated scale band?

**Scope.**
- Oracle only: no model, no training, no activations.
- One frozen construction (§2): no search over parameters.
- Sampling is used only for Monte Carlo estimates of oracle quantities. It uses new stage-0 seeds (§4.3).
- No frozen result is altered. B2/D-055 and D-1 are not reopened.

---

## 2. Construction (frozen)

### 2.1 World and dynamics

- **World.** One 12×12 lattice, periodic in both axes. It is built by a local, unregistered builder that copies the existing `_t_torus` test pattern:

  ```python
  class _X2aTorusBuilder(QuotientLatticeBuilder):          # deliberately NOT @register_world
      family: ClassVar[str] = "_x2a_torus_local"
      expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
      identifications: ClassVar[tuple] = (Identification(0, "periodic"), Identification(1, "periodic"))
  ```

  Validation follows the order of `build_world`, as in D-1 §2.6:
  1. `spec = _X2aTorusBuilder().build(WorldConfig("_x2a_torus_local", (12, 12), "flat"))`;
  2. `spec.validate()`;
  3. `check_boundary_closed(CubicalComplex(spec.n_states, spec.cells))`;
  4. `check_flat_bounds(spec.dist, spec.dist_graph, 2)`.

  WORLD_REGISTRY is never mutated.
- **Kernel.** `T = TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T` (144×144). Every vertex has degree 4, so D_max = 4. T(z, z ± e_i) = 1/5 and T(z, z) = 1/5.
  - T is symmetric and doubly stochastic, so the uniform law u₁₄₄ is stationary.
  - Both components use this **same** T. The components differ only in emission.
- **Disjoint union.** T̃ = blockdiag(T, T) (288×288). Start π̃ = 1/288, uniform over all 288 states. It is stationary for T̃, so each component has probability ½ and, given the component, the state law is uniform at every t.
  - A disjoint union is not a QuotientLatticeBuilder family, so it is assembled here as the block matrix (request code fact).

### 2.2 Emission A: the pilot's O field on the torus, as an explicit array

`process._geometry.point_distances` wraps axis 0 only, so the registered O mode would compute a field that is non-periodic in y. It is never called (guard test, §7.2).

The flat torus distance is d² = δ₁₂(x, c_x)² + δ₁₂(y, c_y)², where δ₁₂(u, c) = min(|u − c| mod 12, 12 − |u − c| mod 12). Since the deck group is a product, the softmax over the 6×6 centre grid factorises **exactly**:

  e[x, a] := exp(−δ₁₂(x, 0.5+2a)²/2σ²) / Σ_{a′=0}^{5} exp(−δ₁₂(x, 0.5+2a′)²/2σ²), with σ = 1.25 (12×6);

  E_A[12x + y, 6a + b] := e[x, a] · e[y, b] (144×36).

The array is literal, built once from `e`, and every entry is strictly positive.

**Independent check (G1).** The brute-force 2-D softmax over the 9 deck images (m, n ∈ {−1, 0, 1}), computed with log-sum-exp, must match: absolute error ≤ 1e-15 and relative error ≤ 1e-12.

**Hand values [L]** (σ = 1.25, so 2σ² = 3.125). Every x has the same multiset of distances to the six centres, {0.5, 1.5, 2.5, 3.5, 4.5, 5.5}. Hence:
- the normaliser is Z = 1.566642 for every x;
- the probability of the centre at distance d is p(d):

| d | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 5.5 |
|---|---|---|---|---|---|---|
| p(d) | 0.589230 | 0.310699 | 0.086385 | 0.012665 | 0.000979 | 0.0000399 |

Column 0 of e (centre 0.5) is (p.5, p.5, p1.5, p2.5, p3.5, p4.5, p5.5, p5.5, p4.5, p3.5, p2.5, p1.5) for x = 0..11.

### 2.3 Emission B: A's field pulled back by a Dehn twist

  φ(x, y) := ((x + y) mod 12, y),  E_B[12x + y, :] := E_A[12·((x+y) mod 12) + y, :].

**Properties of φ.**
1. φ is a group automorphism of Z₁₂² with determinant 1: a linear Dehn twist, a smooth and area-preserving diffeomorphism of the torus.
2. φ is **not** an automorphism of the grid graph: it maps the edge (0,0)–(0,1) to (0,0)–(1,1), which is not an edge.
3. φ is Lipschitz in d_M, with constant √2 on lattice steps (the operator norm of the matrix [[1,1],[0,1]] is the golden ratio, ≈ 1.618).

Hence:
- E_B is a smooth, non-isometric warp of the emission field;
- E_B is a **row permutation** of E_A, so the row multiset, H(W ∣ Z) and the distribution of one-symbol posteriors are identical.

**Emission coordinates (Lemma U).** Put u = φ(z). Then B is the walk on Z₁₂² with step law:
- K_B: 0 and ±(1,0) and ±(1,1), each with probability 1/5;

observed through the **unchanged** E_A. A is the same walk with:
- K_A: 0 and ±(1,0) and ±(0,1), each with probability 1/5.

*Proof.* T(z, z′) = K_A(z′ − z), and φ is linear: φ(e₁) = (1,0) and φ(e₂) = (1,1). ∎

So the components share one emission geometry and one walk graph. They differ only in how the walk's moves sit in the emission geometry: B's "vertical" moves are diagonal.

### 2.4 Mixture and literal model

| Item | Value |
|---|---|
| T̃ | blockdiag(T, T), 288×288 |
| Ẽ | `np.vstack((E_A, E_B))`, 288×36, built once |
| π̃ | uniform 1/288 |
| Tokens | ids 0..35; sequences of 33 symbols (`SequenceLayout()` default) |

Neither the mixture nor E_A, E_B is written into any production spec. TransitionSpec is used only per component, from TransitionBuilder.

### 2.5 Why this B (alternatives rejected)

| Alternative | Why rejected |
|---|---|
| Translation or reflection of E_A (any grid automorphism) | Identical sequence laws: π ≡ ½ at every history (T6). This is the request's core defect; it is used here as null N-iso |
| Axis-wise permutation (original X2a, P) | Equal marginals, but not smooth. Kept only as the specificity control P-ref |
| Different σ in B | Marginals are still exactly uniform, but per-state emission entropy differs. The components would then differ by a purely local noise statistic, not by geometry |
| Twisted-lattice torus Z²/⟨(12,0),(6,12)⟩ | Needs a non-square fundamental domain and new metric code. Because symbol labels are global, it changes the symbol-adjacency graph (label (a,5) borders (a−3,0)), so pairs detect it anyway. Not simpler, and not sharper |

---

## 3. Theorems (for this construction)

### T1. Exactly equal symbol marginals

**Statement.** For c ∈ {A, B}, every t ≥ 1 and every symbol j: P(W_t = j ∣ c) = 1/36. Hence P(c ∣ W_t) = ½ for every single position, and I_1 = 0.

*Proof.*
1. **Equivariance.** δ₁₂(x+2, 0.5 + 2(a+1)) = δ₁₂(x, 0.5+2a), and the normaliser is a sum over all six centres, which is re-indexed by a ↦ a+1 (mod 6, since 2·6 = 12). So e[x+2, a+1] = e[x, a], and E_A[z + (2,0), (a+1, b)] = E_A[z, (a,b)]. The same holds for y.
2. **Equal column sums.** Z₆² acts transitively on the symbols, so all column sums Σ_z E_A[z, j] are equal. They sum to 144, so each equals 4.
3. E_B is a row permutation of E_A, so it has the same column sums.
4. **Stationarity.** Given c, the state law is uniform at every t (T is doubly stochastic and the start is uniform). So P(W_t = j ∣ c) = 4/144 = 1/36. ∎

### T7. Full support

Every entry of E_A and of E_B is positive, and T is irreducible. Therefore:
- every finite string has positive probability under both components;
- 0 < π_t(h) < 1 at every history;
- BayesFilter can never raise IMPOSSIBLE_HISTORY.

### T2. Distinguishability (exact witness)

**Statement.** Let G(d) := Σ_{x∈Z₁₂} e[x,0]·e[x+d,0]. Then

  Δ_rep := P_A(W_{t+1} = W_t) − P_B(W_{t+1} = W_t) = (a/2)·G(1)·(G(0) − G(1)) > 0.

Consequences:
- P_A^(2) ≠ P_B^(2), so I_2 > 0.
- The repeat probability is invariant under any relabelling of symbols and under any relabelling of states by a grid automorphism. So **no** symbol permutation ψ makes P_B = P_A∘ψ: B is not A up to naming or isometry.

*Proof.*
1. **Pair sum.** By Lemma U, for each c:

   P_c(repeat) = (1/144) Σ_u Σ_δ K_c(δ) Σ_j E_A[u,j] E_A[u+δ,j].

2. **Factorisation.** By §2.2,

   Σ_u Σ_j E_A[u,j] E_A[u+δ,j] = H(δ_x)·H(δ_y), with H(d) := Σ_a Σ_x e[x,a] e[x+d,a].

   By equivariance (T1, step 1), each a contributes equally, so H = 6G. Also H(−d) = H(d).
3. **Difference.** K_A − K_B puts +a on (0, ±1) and −a on ±(1,1). So

   Δ_rep = (a/144)·[2H(0)H(1) − 2H(1)²] = (2a/144)·H(1)(H(0) − H(1)) = (a/2)·G(1)(G(0) − G(1)).

4. **Sign.** G(1) > 0, because every entry is positive. For the second factor, Cauchy–Schwarz gives G(1) = ⟨e₀, S e₀⟩ ≤ ‖e₀‖² = G(0), where S is the cyclic shift. Equality would force e₀ to be shift-invariant, i.e. constant. It is not constant: e[0,0] = p(0.5) ≠ e[6,0] = p(5.5). ∎

**Hand values [L]** (from the p(d) table):

| Quantity | Value |
|---|---|
| G(0) | 0.902700 |
| G(1) | 0.769233 |
| Δ_rep | 0.1 × 0.769233 × 0.133467 ≈ **0.010267** |
| P_A(repeat) = ¼[0.2·G(0)² + 0.8·G(0)G(1)] | ≈ 0.17962 |
| P_B(repeat) = ¼[0.2·G(0)² + 0.4·G(0)G(1) + 0.4·G(1)²] | ≈ 0.16935 |

By data processing, the repeat indicator alone gives I_2 ≥ JS(Bern(0.17962), Bern(0.16935)) ≈ Δ_rep²/(8 p̄ q̄) ≈ **9 × 10⁻⁵ nats [L]** (a second-order approximation). The pair-level signal is therefore small.

### T3. Window reduction

**Statement.** For every t ≥ k: I(c; W_{t−k+1:t}) = I(c; W_{1:k}) = I_k = JS(P_A^(k), P_B^(k)), the Jensen–Shannon divergence with weights ½, ½. Likewise, the window posterior π_t^(k) has the same law as π_k, and the window Bayes accuracy equals acc_k.

*Proof.*
1. Given c, the hidden chain is stationary: uniform start and doubly stochastic T.
2. The emission is time-homogeneous, so (c, W_{t−k+1:t}) has the same joint law as (c, W_{1:k}).
3. I(c; W) with c ~ Bern(½) equals the JS divergence of the two conditional laws. ∎

**Consequences.**
- Knowing the position adds nothing.
- At position t, the information requiring history older than k is I(c; W_{1:t−k} ∣ W_{t−k+1:t}) = I_t − I_k.
- The entropy curve of (a) is E[H_b(π_t)] = ln 2 − I_t: one curve answers both (a) and (c).

### T4. Monotonicity and limit

- I_k ≤ I_{k+1} ≤ ln 2 and acc_k ≤ acc_{k+1}, by data processing.
- I_t → ln 2 as t → ∞.

*Proof of the limit.*
1. Each component's output process is a stationary ergodic factor of a finite, irreducible, aperiodic chain, so it is ergodic.
2. By T2 the two output processes are distinct. Distinct stationary ergodic measures are mutually singular.
3. So π_t → 1{c = B} almost surely, by martingale convergence. ∎

### T5. Data-processing bound (what makes a later trained test sharp)

For any measurable f of the last k symbols at position t:
- I(c; f(W_{t−k+1:t})) ≤ I_k;
- any classifier of c based on f has accuracy ≤ acc_k.

**Contrapositive.** If a representation at position t decodes c (on held-out histories) with accuracy significantly above acc_k, then it is not a function of the last k symbols.

### T6. Isometric null

**Statement.** Let g be any automorphism of the 12×12 torus grid graph (a translation, or one of the dihedral maps about any point). Then B′ with E_{B′} = E_A∘g has P_{B′} = P_A on all strings, so π_t ≡ ½ and I_k = 0 for all k.

*Proof.* The map g is a bijection of state paths that preserves the uniform start and T, so it carries P_A onto P_{B′}. ∎

**Remark (not gated).** Within this class (one T, an emission row permutation, stationary start), I_1 = 0 always, and T2 makes the pair window informative. A process that is blind to short windows would need a holonomy-type mechanism, like D-1's Theorem C. For flat tori with translation-invariant walks and periodic emission patterns, labelled lifts that agree everywhere force a common quotient and hence identical laws. So this class cannot provide such a mechanism (OQ5). The priority-1 sharpness of this stage therefore rests on the **size** of I_t − I_k and acc_t − acc_k (T5), not on zero short-window information.

### Identities used as checks

**Increment identity.**
- i_{t+1} := I_{t+1} − I_t = E_h[(1−π)·KL(q_A‖q) + π·KL(q_B‖q)], where q_c = b_c T E_c.
- Hence I_t = Σ_{s<t} i_{s+1}, since I_1 = 0.

**Incentive.**
- V_t := E_h[KL(q(h) ‖ q^{½}(h))], where q^{½} = ½q_A + ½q_B.
- V_t is the next-symbol excess log-loss of a predictor that knows both world-conditional beliefs but not the component posterior. It measures the training incentive to represent π.

---

## 4. Oracle questions: quantities, estimators, PH

### 4.1 Exact quantities (float64, deterministic, no sampling)

1. **Pair laws.** M_c = (1/144)·E_cᵀ T E_c (36×36), so I_2 = JS(M_A, M_B) in closed form. Also trace(M_A) − trace(M_B), which T2 gives in closed form.
2. **Block laws for k ≤ 4**, by forward recursion per component.
   - α₁ = u₁₄₄ ⊙ E_c[:, w₁], then α_{s+1} = (α_s T) ⊙ E_c[:, w_{s+1}].
   - Level 3 has 46,656 rows × 144 states; the leaves are (α₃ T) E_c, giving 36⁴ = 1,679,616 probabilities per component.
   - JS is accumulated in the stable form ½(P_A + P_B)·[(1+r)·log1p(r) + (1−r)·log1p(−r)], with r = (P_A − P_B)/(P_A + P_B), summed with `math.fsum` per level-3 block.
3. **Exact outputs:**
   - I_1, I_2, I_3, I_4;
   - acc_1..acc_4 (= Σ_h max(P_A, P_B)/2);
   - the exact entropy curve ln 2 − I_t for t ≤ 4.
4. **Variants:** the same for N-iso (all values must be 0) and for P-ref (descriptive).

### 4.2 Monte Carlo (validated)

**Sampling** (existing `HMMSampler`, unchanged).
- n = 2^20 sequences of 33 symbols: 2^19 from each component. Sampling is exactly stratified, using `HMMSampler(T, E_c, u₁₄₄, SequenceLayout())`.
- Seeds: `SeedTree(MASTER_X2A0)` with streams ("x2a0_mc", c). MASTER_X2A0 = 20261015 is a new master, bound at freeze. All seeds are recorded in the store manifest (OQ7).

**Filtering** (existing `BayesFilter`, unchanged).
1. **Full history.** `BayesFilter(T̃, Ẽ, π̃).run(tokens)` in batches of 2,048 gives b̃_t and q_t for t = 1..33. Then:
   - π_t is the sum of the B block;
   - b_c is the renormalised c-block;
   - q_c = b_c T E_c.
2. **Windows at t*.** For k ∈ {1, 2, 4, 8}, `BayesFilter(T̃, Ẽ, π̃).run(tokens[:, 32−k:32])` gives π^(k) at the final position. Starting from π̃ is exact for a window, because the state law at the window start is uniform (T3).
3. **Per component** (first 2^14 rows, cross-check only). `BayesFilter(T, E_c, u₁₄₄)` gives the log-likelihood ratio LLR_t = Σ_{s≤t}(ce^A_s − ce^B_s), and π_t = expit(LLR_t).

**Estimators.** Each is a mean over all n sequences; with equal strata this equals the ½/½ mixture expectation.
- Î_t = ln 2 − mean H_b(π_t). This is the Rao–Blackwellised form.
- Second estimator, for validation: Î′_t = mean[ln 2 + ln P(c_true ∣ h)].
- âcc_t = mean max(π_t, 1−π_t).
- Window versions Î^win_k and âcc^win_k at t*.
- î_{t+1} and V̂_t, by the identities of §3.

**Uncertainty.**
- SE from the stratum-wise sample variance; 99% intervals with z = 2.576.
- Differences used in GO/STOP are **paired**: computed per sequence, on the same rows.
- Distribution-free check: H_b(π) ∈ [0, ln 2], so Hoeffding over the two strata (δ = 10⁻⁶) bounds |Î_t − I_t| ≤ 3 × 10⁻³ nats **[L]**. This bound is reported next to every Î_t.

**Reported for (a) and (c)**, for t = 1..33 and for windows k ∈ {1, 2, 4, 8} at t*:
- I, SE, acc;
- the share I_k/I_32 and the older-history information I_32 − I_k;
- E[H_b(π_t)] and its 5/25/50/75/95 % quantiles;
- the fractions of histories with max(π, 1−π) ≥ 0.9 and ≥ 0.99;
- the per-component mean LLR and its slope over t ∈ [16, 32] (an estimate of the relative-entropy rate);
- î_t and V_t.

**Descriptive extras (not gated):**
1. The pilot's context gain G_C at t*, from the existing `LastSymbolPosterior` and `context_gain`.
2. A curve extension to t = 128. It uses n = 2^16 sequences, sampled by `HMMSampler` with `SequenceLayout(n_obs=129)` (the sampler uses only `n_obs`), and filtered by the independent stencil filter of §6 (G4). BayesFilter is capped at 33 symbols. The extension only tells a later protocol what context length would be needed (OQ8).

### 4.3 PH (question b): estimator, scale rule, calibration, nulls (all frozen)

**Estimator.**
- Points are belief vectors. The metric is **Hellinger** (`topology.metrics.Hellinger`), the pilot's primary belief metric (RESEARCH_SUMMARY §7.2); √JS is descriptive only.
- Distances, deduplication and scale come from `DistancePipeline(Hellinger(), pca_dims=None).compute`. The scale s is the 95th percentile of the positive distances (`scale_of`).
- Vietoris–Rips over F₂: `PersistenceComputer(PHConfig(maxdim=1, coeff_p=2, threshold="auto"))`, or `maxdim=0` for clouds that need only H0.
- **H1 count:** β̂₁(τ) := #{finite H1 bars with death − birth ≥ τ·s}.
- **H0 count:** β̂₀(h) := the number of single-linkage clusters at Hellinger height h (cutting MST/H0 edges longer than h) that contain ≥ 0.05·M points. The size filter stops one outlier from counting as a cloud.
- Also stored, per the pilot: S, π_max, the top-3 persistences and the full diagrams. Reported: the H0 gap statistic g₀ = d₍₁₎/d₍₂₎ (the two largest finite H0 deaths) against E[H_b(π_t)], which is the EXTENSIONS §3 measure.

**Panels.**
- 8 disjoint panels of M = 512, taken as fixed slices of the MC sample: no extra sampling.
- Per-component clouds use 512 rows of that component's stratum.
- Mixture clouds use 256 + 256 rows.

**Scale-band calibration**, run before any belief cloud is evaluated:
1. **C-syn.** `SyntheticShapes.flat_torus`, `circle` and `disk`: M = 512, ambient 128, noise 0.05, Euclidean metric, 20 draws each (stream "x2a0_cal").
   - The τ grid is G = {0.02, 0.04, …, 0.60}.
   - B₁ := the largest contiguous run of τ ∈ G at which every shape is classified correctly (torus 2, circle 1, disk 0) in ≥ 19/20 draws.
   - τ₁* := the lower median of B₁.
2. **C-world.** Vietoris–Rips on the torus's own flat metric `spec.dist` (144 points): β̂₁(τ₁*) = 2.
3. **C-emis.** The emission-row cloud {E_A[z]} (144 points, Hellinger) gives β̂₁(τ₁*) = 2. This one cloud serves both components, because E_B's rows are the same multiset.
4. **C-H0.** At t*, on the same panel histories, build two oracle controls:
   - X¹: π replaced by the true label (fully concentrated). Its two clouds are at Hellinger distance exactly 1.
   - X^½: π replaced by ½ (unconcentrated).

   Let m be the maximum over panels of: the largest finite H0 death of X^½, and the second-largest finite H0 death of X¹. Then h₀* := (m + 1)/2. The band (m, 1) must be wider than 0.05.
5. **Failure handling.** If any of C-syn, C-world, C-emis or C-H0 fails or is empty, then every PH outcome is INVALID. The information outcomes (§5) are unaffected.

**Clouds and decisions** (each decision uses β̂ at τ₁* or h₀* and ≥ 7/8 panels, per the pilot's convention).

| Id | Cloud | Decision |
|---|---|---|
| Q1-A, Q1-B | b_c(h) at t*, h ~ P_c (Δ¹⁴³) | β̂₁ = 2 |
| Q1-spec (P-ref) | b_{B_P}(h) at t*, from the mixture A ⊔ B_P, where E_{B_P} = E_A[axis_state_perm(draw_axis_permutation(spec))] (existing helpers) | must **not** reach β̂₁ = 2 in ≥ 7/8 panels |
| Q2-full | mixture beliefs at t*, 256 + 256 | β̂₀(h₀*) = 2, with split purity ≥ 0.95 (both clusters ≥ 95 % one label, labels differ) |
| Q2-win | window-8 mixture beliefs at t* (posterior from w_{25:32}), same histories | β̂₀(h₀*) = 1 |
| Q2-curve (descriptive) | mixture beliefs at t ∈ {1, 2, 4, 8, 16, 24, 32} | β̂₀, g₀ and purity reported |

**Outcomes.**
- Q1 = PASS ⟺ Q1-A, Q1-B and Q1-spec all hold.
- Q1 = NON_SPECIFIC ⟺ A and B pass but P-ref also reaches 2.
- Q1 = FAIL ⟺ otherwise.
- Q2 = SEPARATED_FULL_ONLY ⟺ Q2-full and Q2-win hold.
- Q2 = SEPARATED_BOTH ⟺ Q2-full holds and Q2-win fails.
- Q2 = NOT_SEPARATED ⟺ Q2-full fails.

**Null and positive controls** (validity; required, §6 G5).

| Id | Variant | Required |
|---|---|---|
| N-iso | E_{B′} = E_A translated by (1,0) | Exact I_k = 0 to 1e-12 for k ≤ 4. MC (2^16 sequences): max ∣π_t − ½∣ ≤ 1e-12 for all t. Mixture cloud at t*: β̂₀(h₀*) = 1 in 8/8 panels |
| N-id | E = 1/36 in both blocks | All beliefs uniform; PH status COLLAPSED; π ≡ ½ |
| N-swap | Labels A and B exchanged | π ↦ 1 − π exactly (1e-15); every Î unchanged (1e-15) |
| X¹ | Concentrated oracle cloud (C-H0) | β̂₀(h₀*) = 2 with purity 1 in 8/8 panels (pipeline check) |
| P-ref (descriptive) | Original X2a B | Exact I_1..I_4 and MC I_t reported. Shows how much component information the original design exposed to short windows |
| Noise floor (descriptive) | `NullClouds` isotropic and covariance-matched, 20 draws | S reported as context, never as a threshold (pilot rule) |

---

## 5. GO/STOP criteria (fixed before any computation)

All statistical decisions use the 99 % interval:
- a criterion **passes** if the interval lies on the passing side;
- it **fails** if the interval lies on the failing side;
- otherwise it is **THRESHOLD_INCONCLUSIVE**, which counts as not passed.

There is no rerun, no change of n, and no parameter change after results are seen.

**Priority-1 criteria** (the information route; the decisive part):

| Id | Criterion | Rationale |
|---|---|---|
| P3 | acc_32 − acc_8^win ≥ 0.10 (paired, at t*) | By T5, a later probe can show use of history older than 8 symbols only if acc_32 − acc_8 is clearly positive. With 4,096 test histories, the probe's SE is about 0.007, so a 0.10 margin leaves room for an imperfect model (≈ 60 % capture still gives ≈ 8 SE) |
| P4 | I_8^win ≤ 0.5·I_32 (conservative form: upper 99 % bound of I_8 ≤ 0.5 × lower 99 % bound of I_32) | At least half the component information at t* needs history older than 8 symbols |
| P5 | V_32 ≥ 0.01 nats per symbol | One tenth of the pilot's minimum context gain (0.10). Below this, a trained model has too little incentive to track the component, and a null result would be uninterpretable (OQ3) |

**Stage-0 outcome** (only if the overall validity verdict is PASS, §6.3):

| Outcome | Condition | Meaning for a later trained stage |
|---|---|---|
| **GO_P1_PH** | P3 ∧ P4 ∧ P5 ∧ Q1 = PASS ∧ Q2 = SEPARATED_FULL_ONLY | Informative for priority 1 by both the probe route (T5) and the original X2a PH route |
| **GO_P1** | P3 ∧ P4 ∧ P5, and not GO_P1_PH | Informative for priority 1 by the probe route only. PH separation would either not occur at t*, or would also be available from 8-symbol windows |
| **PH_NOT_P1** | ¬(P3 ∧ P4 ∧ P5) ∧ Q1 = PASS ∧ Q2 ∈ {SEPARATED_FULL_ONLY, SEPARATED_BOTH} | A PH-based X2a stage is feasible but **not** informative for priority 1 |
| **STOP_P1** | ¬(P3 ∧ P4 ∧ P5), and not PH_NOT_P1 | Not informative for priority 1 on this construction. The I_t / acc_t curves are the finding |

**Forecast** (recorded now, not a criterion; marked [L]).
- T2's pair signal is small (I_2 ≳ 10⁻⁴ nats from the repeat indicator).
- In a Gaussian-displacement picture (Lemma U), Σ_A = 0.4·I and Σ_B = [[0.8, 0.4], [0.4, 0.4]] have equal determinants. One fully resolved displacement is then worth at most KL = 0.5 nats [L].
- On a 12-torus with σ = 1.25 noise, only a few such displacements resolve within 32 steps.
- So I expect only partial concentration at t* (an order of magnitude: acc_32 ≈ 0.7–0.8), with P4 plausible and P3 and P5 uncertain.
- Q2-full (β̂₀ = 2) would need nearly every one of the 512 histories to be confident. Under roughly linear evidence accumulation, that much concentration at 32 implies acc_8 > 0.9, which would fail P3. So **GO_P1_PH is unlikely by construction of the criteria, not by accident**.

This tension is itself a priority-1 point. The original X2a prediction ("β̂₀ = 2 at late positions") cannot by itself demonstrate long-history use; the window contrast (Q2-win) is required.

---

## 6. Verification plan

Order:
1. mandatory preflight (§7.2);
2. S0 (hashes and commit);
3. G0, G1, G2, G4, G3, G5, G6;
4. the scientific outputs (§4–§5).

All gates are deterministic given the frozen seeds.

### 6.1 Gates and criteria

**G0: structure.**
1. The builder validates (§2.1).
2. 144 vertices, 288 edges and 144 squares. χ = 0. Betti numbers (1,2,1) over GF(2) and GF(3). ∂₁∂₂ = 0.
3. Every degree is 4, so D_max = 4.
4. T against an independent Fraction formula (1/5 on each of the 4 neighbours and on the diagonal): max error ≤ 1e-15. T is symmetric. T̃ is block-diagonal with both blocks bitwise equal to T.
5. π̃T̃ = π̃ within 1e-15.

**G1: emission.**
1. The factorised E_A matches the brute-force 2-D deck-image softmax (abs ≤ 1e-15, rel ≤ 1e-12).
2. Rows sum to 1 within 1e-15; every entry is positive.
3. Z₆² equivariance holds within 1e-15.
4. E_B equals E_A[φ] **bitwise**. `np.array_equal(np.sort(E_A, 0), np.sort(E_B, 0))` holds.
5. φ is a bijection and not a graph automorphism (witness edge, §2.3).
6. Ẽ is built once, and its blocks are bitwise equal to E_A and E_B.

**G2: theorem identities (exact enumeration).**
1. T1: every column sum equals 4 within 1e-12. At t = 1, ∣π − ½∣ ≤ 1e-14 for all 36 symbols. I_1 ≤ 1e-15.
2. T2: trace(M_A) − trace(M_B) equals (a/2)·G(1)(G(0) − G(1)), computed from `e`, within 1e-14, and is > 0.
3. The [L] hand values of §2.2 and §3 are reported next to the computed values. They are not gated.
4. The enumerated laws for k ≤ 4 are invariant under the 36 symbol translations (relative error 1e-13).
5. I_1 ≤ I_2 ≤ I_3 ≤ I_4 (exact, up to 1e-15). I_2 > 0. I_2 from the enumeration equals JS(M_A, M_B) within 1e-13.
6. N-iso: I_k ≤ 1e-12 for k ≤ 4.
7. N-swap: holds within 1e-15.

**G4: oracle cross-checks** (on the first 2^14 MC rows, all t ≤ 33).
1. **Independent stencil filter.** It never forms T; it applies the rule of §2.1 with `np.roll` on 12×12 arrays, per component, and combines the components by log-evidence. Against BayesFilter:
   - beliefs within 1e-12;
   - π within 1e-11.
2. π via expit(LLR) from the per-component BayesFilters: within 1e-10.
3. q = (1−π)q_A + π q_B: within 1e-12.
4. exp(log_evidence) against the stencil evidence: relative error ≤ 1e-10.
5. **Decimal reference.** `independent_reference.decimal_suffix_posterior` (digits 80) on 16 histories (the first 8 rows of each stratum), length 33, on the mixture with π̃. All 288 entries agree with BayesFilter within 1e-12.
   - Here the float64 model **is** the model, so the reference's `Decimal(float(x))` conversion is the right one. This differs from D-1's rational model, so D-1's Decimal trap does not apply.
6. No non-finite values; no negative probabilities.

**G3: Monte Carlo validity.**
1. For k = 2, 3, 4: ∣Î_k − I_k∣ ≤ 4·SE_k, and ≤ the Hoeffding bound.
2. Î_1 equals 0 within 1e-14: every π₁ is ½.
3. **Stationarity identity (T3).** For k ∈ {2, 4, 8}, the window estimate at t* (Î^win_k) and the prefix estimate (Î_k) agree within 4 paired SE. The same holds for acc.
4. Î_t and Î′_t agree within 4 SE of their difference, for t ∈ {4, 8, 16, 32}.
5. **Chain identity.** Σ_{s<32} î_{s+1} agrees with Î_32 within 4 SE.
6. Î_t is non-decreasing in t within 4 SE of each step difference.

**G5: controls.** N-iso, N-id, N-swap and X¹ as specified in §4.3.

**G6: PH calibration.** C-syn, C-world, C-emis and C-H0 (§4.3). A failure here makes every PH outcome INVALID. It does not affect the overall verdict, and it does not affect P3–P5.

### 6.2 Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S0 | Protocol not frozen; a mismatch in the request, protocol or commit hash; a non-empty diff against the bound commit in `src/`, `tests/oracle_profile/` or `tools/x4_oracle_profile/` | Do not run |
| S2 | Any builder or validation exception in G0 | INVALID; escalate. No metric switch, registry change or production edit |
| S3 | Any exact identity or tolerance in G0, G1, G2, G4 or G5 violated | FAIL at the first failed criterion; record the remaining gates as NOT_RUN; preserve the failing array or row. No post-hoc edit of a theorem or tolerance |
| S5 | A G3 Monte Carlo validity criterion fails | FAIL of G3; the scientific outcomes are NOT_RUN; escalate as a possible estimator or oracle defect. No increase of n and no reseed |
| S6 | Implementation needs a production change, a third module file, or more than 400 lines per file | Stop and escalate before writing the code |
| S7 | Owner STOP, usage limits, or the disk thresholds (C: < 2 GB, X: < 30 GB) | INVALID (interrupted); resume only under the same frozen specification |

There is **no CPU ceiling** (owner B4): CPU is measured only.

### 6.3 Verdict

- **Overall PASS** ⟺ the preflight passes, S0 passes, and G0–G5 all pass. G6 may independently be PASS or INVALID.
- **FAIL** ⟺ S3 or S5.
- **INVALID** ⟺ S2, S7, an environment error, or a gate that cannot be evaluated.
- The scientific outcome (§5) is reported only under overall PASS. A STOP_P1 is a valid scientific outcome, **not** a FAIL.

---

## 7. Reuse, footprint and cost

### 7.1 Six-field reuse assessment

| Field | Assessment |
|---|---|
| **1. Existing functions and artefacts (used unchanged)** | **World:** `QuotientLatticeBuilder`, `Identification('periodic')`, `WorldConfig`, `WorldSpec.validate`, `CubicalComplex`, and the internals `check_boundary_closed` and `check_flat_bounds` (imported from `tools/` as D-1 does). **Process:** `TransitionBuilder`, `TransitionConfig`; `draw_axis_permutation` and `axis_state_perm` for P-ref. **Dataset:** `HMMSampler`, `SequenceLayout`. **Oracle:** `BayesFilter`, `LastSymbolPosterior`, `context_gain`. **Topology:** `Hellinger`, `DistancePipeline`/`scale_of`, `PersistenceComputer`/`PHConfig`, `Summaries`, `SyntheticShapes`, `NullClouds`. **Contracts:** `SeedTree`. **Reference:** `tests/oracle_profile/independent_reference.decimal_suffix_posterior`. **D-1 pattern:** a local unregistered builder; an explicit E array; API.md written before the module; an independent test file with AUTHORSHIP.md; mandatory preflight; S0 hashes; `report.json` and `model.npz`; a store-local binding of the job-0014 meter in measure-only mode; at most two module files of ≤ 400 lines (addendum-2 split) |
| **2. Genuinely missing capability** | An explicit doubly periodic Gaussian emission (`point_distances` wraps only axis 0, so the registered O mode is wrong on a torus). The Dehn-twist variant. The disjoint-union assembly (not a builder family). Exact block-law JS enumeration for k ≤ 4. Monte Carlo MI and accuracy estimators with SE, Hoeffding bounds and paired differences. A stencil reference filter: an independent numerical reference, and the only filter for the descriptive t > 33 extension, since BayesFilter's `check_tokens` caps sequences at 33 symbols. The PH band rule for β̂₀ and β̂₁ (new because the pilot gated S, not counts) |
| **3. Smallest change** | `tools/x2a_stage0/x2a_stage0.py` (construction, exact enumeration, Monte Carlo, G0–G4) and `tools/x2a_stage0/x2a_stage0_ph.py` (calibration, clouds, controls, G5–G6, `run`), each ≤ 400 lines. Plus `tools/x2a_stage0/API.md`, `tests/x2a_stage0/test_x2a_stage0.py` and `tests/x2a_stage0/AUTHORSHIP.md`. No change to `src/`; no new sampler, production filter, runner or generic table-emission mode |
| **4. Stable interfaces and invariants** | Row vectors; `emit_then_transition`. State id 12x + y; mixture id 144·[B] + 12x + y; token id 6a + b. Ẽ = `vstack((E_A, E_B))`, built once. T̃ = blockdiag(T, T). π̃ uniform and stationary. Sequences of 33 symbols (`check_tokens` max_len). float64, no epsilon. WORLD_REGISTRY untouched. `point_distances` and `is_x_periodic` never called. Seeds come only from `SeedTree(MASTER_X2A0)` |
| **5. Relevant regression checks** | Unchanged `tests/world`, `tests/process`, `tests/oracle`, `tests/oracle_profile`, `tests/topology` and `tests/dataset`. New tests: registry hygiene; guards (monkeypatch `point_distances` and `is_x_periodic` to raise); closed forms T1/T2 from an independent `e` implementation; an independent k = 2, 3 enumeration; N-iso and N-swap; `tools/check_file_sizes.py` |
| **6. Next plausible extension (no premature generalisation)** | After GO_P1 or GO_P1_PH: a separate trained-stage protocol reusing this module's construction. Promote a torus builder and a table-emission mode into `src/` only when that second consumer exists. The non-abelian X6 is the route to short-window-blind distinctions (OQ5) |

### 7.2 Preflight, store and bindings

- **Preflight:** a metered run of the regression suites listed in field 5, `tests/x2a_stage0` and `tools/check_file_sizes.py`. Its record is `preflight.json`. Any failure gives INVALID with every gate NOT_RUN (the D-1 coordinator's ruling 8).
- **Store:** `X:/Downloads/projects/topo-pilot/x2a-stage0-oracle-store/` (on X:, per owner B4). It holds:
  - `report.json`: verdict; gate statuses; every curve with its SE and Hoeffding bound; the PH diagrams' summaries; seeds; CPU; hashes;
  - `model.npz`: T, E_A, E_B, e;
  - `ph_diagrams.npz`;
  - the CPU ledger.
- **Bindings at freeze:**
  - base commit (OQ1);
  - request SHA256;
  - protocol SHA256 (recorded in the freeze record);
  - MASTER_X2A0;
  - module, test and store paths.

### 7.3 Cost (forecast, not benchmarked; one thread, uncapped)

| Part | Estimate |
|---|---|
| G0–G2: build, kernels, k ≤ 4 enumeration × 3 variants (≈ 46,656 × 144² flops per level-3 product) | ≈ 1 min |
| Sampling 2^20 × 33 symbols (HMMSampler, inverse CDF over 36 + 144 entries per step) | 1–3 min |
| BayesFilter on 2^20 × 33 symbols (288² matrix products, 512 batches) plus window filters | 5–10 min |
| G4: stencil filter on 2^14 rows; Decimal reference on 16 histories × 32 steps × 288² operations at 80 digits | 2–4 min |
| Controls: N-iso (2^16) and P-ref (2^18 Monte Carlo plus enumeration) | 2–4 min |
| PH: 60 calibration clouds, 2 world clouds and 24 per-component H1 clouds at M = 512, plus about 100 H0-only clouds | 5–15 min |
| Descriptive extension to t = 128 (2^16 sequences, stencil filter) | 1–2 min |
| **Total** | **≈ 25 CPU-min (range 15–60)**, plus a preflight of about 3 min (as in D-1) |

- Memory is below 2 GB: BayesFilter batches of 2,048 × 33 × 288 doubles take about 160 MB, and the level-3 enumeration about 110 MB.
- Threads are pinned to 1 (`OMP`/`MKL`/`OPENBLAS_NUM_THREADS = 1`).
- Owner safety caps apply: ≤ 4 threads, 12 GiB, one scientific task at a time.

---

## 8. Licence and limits

**Stage 0 can establish (for this frozen construction only):**
1. The components have exactly equal symbol marginals (T1), and they are distinguishable even up to symbol renaming (T2). The isometric correction (T6) would not have worked.
2. The exact component-information curve I_t and acc_t: exact for t ≤ 4, Monte Carlo with stated error for t ≤ 33, and descriptive to 128. By T3 the same curve gives the window information I_k at every position, so it splits the information at t* into last-symbol (0), ≤ k-window and older-history parts.
3. The incentive V_t.
4. Whether exact beliefs show each torus's H1, and whether full-history beliefs (and not 8-symbol window beliefs) separate the components, at a calibrated scale band ("reproduced / not reproduced at the band", as in EXTENSIONS §2).
5. Whether a later trained stage would be informative for priority 1 (§5), with T5 as the sharp criterion.

**Proposed licensed sentence** (completed with the numbers after the run):

> In a T²⊔T² process with exactly equal symbol statistics (component B is component A's emission field pulled back by a Dehn twist), the last symbol carries no component information. The last k symbols carry I_k = … nats (k = 2, 4, 8), and the full 32-symbol history carries I_32 = … nats (Bayes accuracies …). This was established by exact enumeration for k ≤ 4 and by validated Monte Carlo with the unchanged oracle.

**Stage 0 cannot establish:**
- anything about trained models: representation geometry, learnability, causal use (priority 2), or whether a model actually uses older history;
- anything about other σ, p_stay, twists, torus sizes or contexts;
- any general claim that tori with equal marginals need long history.

Further limits:
- PH counts are statements at the calibrated band only. Hellinger belief clouds are not the activation space.
- The [L] forecasts are not findings.
- The Remark under T6 is a proof sketch about a class of constructions and is not gated.
- Stage-0 Monte Carlo histories are oracle-only. They must not serve as a trained-model test set unless a later protocol declares them (OQ7).

**What a later trained stage must add (not now).**
1. Its own frozen protocol: data and seeds disjoint from MASTER_X2A0; the uniform stationary start, without which T3 fails; and t* inside its context.
2. The **paired T5 test**: per held-out history, compare the probe's correctness with the 8-window Bayes classifier's correctness, against a pre-registered margin.
3. Controls:
   - an N-iso model, whose probe must stay at chance;
   - a model or probe fed only the last 8 symbols, whose accuracy must be ≤ acc_8;
   - label permutation.
4. A learning gate relative to V_32.
5. Optionally, the PH route, but only if the outcome is GO_P1_PH.

---

## Open questions

1. **Base commit (OQ1).** The request says "main @c364f95 or later". But c364f95 is the HEAD of branch d1-seam-0019 and is **not** on main (main is c2046fc). The D-1 pattern exists only on that branch. Bind either main after D-1 is promoted, or a new branch from c364f95. The src kernels needed here appear unchanged; S0 checks this by diff at freeze.
2. **Thresholds to ratify (OQ2):**
   - t* = 32;
   - k_s = 8;
   - P3 margin 0.10;
   - P4 share 0.5;
   - the 99 % intervals with the THRESHOLD_INCONCLUSIVE rule;
   - the 7/8 panel rule;
   - the 5 % cluster-size filter;
   - purity 0.95;
   - the τ grid and the 19/20 rule;
   - the H0 band width 0.05;
   - n = 2^20;
   - MASTER_X2A0.
3. **P5 (OQ3).** Should the incentive criterion (V_32 ≥ 0.01 nats) gate GO, or be descriptive? I propose gating: without incentive, a trained-model null is uninterpretable. The 0.01 value is a judgment (one tenth of the pilot's G_C floor).
4. **Follow-up after STOP_P1 (OQ4)**, if the cause is too little information at t* (P3 or P5). Each candidate below would be a **new** protocol, never a stage-0 rerun:
   - a stronger twist (s = 2, so a vertical move becomes (2,1); KL per resolved displacement 2 nats [L]);
   - σ = 0.75;
   - a longer context, guided by the descriptive t ≤ 128 curve.

   Owner or coordinator choice.
5. **Short-window-blind distinctions (OQ5).** By T2, this class always leaks some information at k = 2. A distinction that only long windows can see needs label holonomy (D-1-style, or the non-abelian X6), not a smooth torus pair. This affects whether X2a or X6 better serves priority 1.
6. **Independent re-derivation (OQ6)** of T1–T7, Lemma U, the identities, and the [L] values (G(0), G(1), Δ_rep, the JS lower bound, the KL = 0.5 and 2 nats, the Hoeffding bound) before freeze, as was done for D-1.
7. **Exposure (OQ7).** Should stage-0 sequences be entered in an exposure or seed registry? They are oracle-only, but the trained stage must avoid reusing them silently.
8. **Descriptive extension (OQ8).** Is it acceptable to use `SequenceLayout(n_obs=129)` purely as the sampler's length parameter, with the stencil reference filter as the only filter beyond 33 symbols, for a non-gated curve? If not, drop the extension; nothing gated depends on it.
