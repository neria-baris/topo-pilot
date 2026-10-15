STATUS: REVIEW_READY (not frozen)

# X2A-MERGED-v1: corrected X2a stage 0, T²⊔T² with a Dehn-twisted emission (oracle only, no training)

| Field | Value |
|---|---|
| Protocol id | X2A-MERGED-v1 |
| Role | Protocol writer (W) for the merged protocol. Planning only: no Python run, no test run, no data opened, no git write. |
| Date | 2026-10-15 |
| Binding decisions | `planning/responses/coord-x2a-stage0-20261015.MERGE.md`, decisions 1–10 (cited as **MD n**) |
| Analyst amendments | `planning/responses/coord-x2a-stage0-20261015.MERGE_ANALYSIS.md`, amendments A1–A5 (cited as **AN §n / An**) |
| Other inputs | Request `planning/requests/coord-x2a-stage0-20261015.md` (cited RQ); track L `…claude.md` (base protocol; cited L§n); track X `…codex.md` (cited X§n); style reference `D1-FROZEN-v1.md` |
| Next step | MD 10: an independent Codex review, including a re-derivation of T1–T7, Lemma U, Lemmas R/C/A/P and Proposition N, before freeze |
| Code read for reuse claims | topo-pilot main @ `c364f95e5573940cdc24b569b0fb7c6a16c97ab8` (HEAD of main; also contained in d1-seam-0019 and int-0021). `src/topo_pilot/oracle/{__init__,_common,_filter,_futures}.py`; `process/{__init__,transition,_geometry,centers,emission}.py`; `world/{__init__,lattice,metrics,config,identification,registry}.py` and `complex.py` signatures; `dataset/{__init__,sampler}.py`; `contracts/{layout,ids}.py`; `topology/{__init__,metrics,distance,persistence,shapes,summaries}.py`; `tools/x4_oracle_profile/oracle_profile.py`; `tests/oracle_profile/{independent_reference.py,AUTHORSHIP.md}`; `tools/d1_seam/{API.md,d1_seam.py (header, imports),d1_seam_checks.py (s0_check, run),OUTPUTS_0020.md}`; `tests/d1_seam/AUTHORSHIP.md`; `tests/world/test_world.py` (`_t_torus`); `tools/check_file_sizes.py`; `docs/proposals/X6_TOPOLOGICAL_INVARIANTS.md` (the Z₂ transport lines). Every function named in §8.2 was checked against its signature at this commit. |
| Arithmetic | Every hand value was recomputed by W with a desk calculator (awk floating-point arithmetic; no Python, no repository code). Values that appear in no input are marked **[W]**. Analyst approximations are marked **[H]** (Gaussian/Whittle, good to about a factor of 2). **No [W] or [H] value is a gate**; every gated quantity is computed by the run. Discrepancies with the inputs are listed in §10.2. |

## Summary (≤ 300 words)

**Question (charter priority 1).** In a two-torus process whose components have exactly equal single-symbol statistics, how much component information is available from the last symbol, from the last k = 2, 4, 8 symbols, and from the full 32-symbol history, and how much of the full-history gain is merely a sum of short-window evidence?

**Construction (MD 1).** Two 12×12 tori (N = 288), the pilot's lazy walk (p_stay = 0.2) on each, no inter-component transitions, uniform start. A emits the pilot's O field (V = 36, σ = 1.25) on the doubly periodic flat metric as an explicit array. B emits A's field pulled back by the Dehn twist φ(x,y) = (x+y mod 12, y): a smooth, non-isometric warp that is a row permutation of E_A.

**Theorems.** T1: every symbol has probability exactly 1/36 in both components, so I_1 = 0. T2: the repeat probability differs by 0.010267 [W], so I_2 > 0 under any symbol relabelling. T3: window information is position-free. T5: a function of the last k symbols cannot beat acc_k.

**Computation.** Exact enumeration for k ≤ 4. Monte Carlo with 2²⁰ stratified sequences and the unchanged BayesFilter, validated against exact values, a stencil filter, `suffix_posterior` and the Decimal reference.

**GO/STOP (fixed now; MD 2–3).** GO_P1 requires P3 (acc_32 − acc_8 ≥ 0.10) and P4 (I_8 ≤ ½·I_32), both judged by 99% intervals. GO_P1_NONADDITIVE additionally requires that the lower 99% bound of acc_32 − acc_add is ≥ 0.03, where acc_add is the accuracy of the product of four disjoint 8-block likelihood ratios. Otherwise the label is GO_P1_ADDITIVE. P5 (incentive), the PH route and the blur comparator are reported, not gated.

**Cost.** About 30–45 CPU-min, one thread, uncapped.

**Licence.** Oracle facts about component identity in this one construction. It cannot show exact short-window blindness. Every information size quoted before the run is a forecast.

---

## 0. Notation and conventions

| Symbol | Meaning |
|---|---|
| c ∈ {A, B} | Component, drawn once per sequence with P(A) = P(B) = ½ |
| z = (x, y) ∈ Z₁₂² | State within a component. Index i(z) = 12x + y (equals `check_state_order`'s x·dims[1] + y) |
| s = 144·[c = B] + 12x + y | Mixture state index (0..287) |
| j = (a, b) ∈ Z₆² | Symbol with centre (0.5 + 2a, 0.5 + 2b). Token id 6a + b (equals `GridCenters`' j = a·k + b with k = 6). One alphabet, no symbol renaming |
| α = (1 − p_stay)/4 = 1/5 | Probability of each of the four lattice moves. The stay probability is also 1/5 |
| δ₁₂(u, v) | min(\|u − v\| mod 12, 12 − (\|u − v\| mod 12)) |
| e[x, a] | 1-D field (§2.3), 12×6 |
| P_c^(k) | Stationary law of k consecutive symbols given c |
| π_t(h) | P(c = B ∣ w_{1:t}), the component posterior |
| π_t^(k)(h) | P(c = B ∣ w_{t−k+1:t}), the window posterior (stationary restart) |
| π^blk_β(h), β = 1..4 | P(c = B ∣ w_{8β−7:8β}), the block posterior (stationary restart) |
| H_b(p) | −p ln p − (1 − p) ln(1 − p). Logarithms are natural; information is in nats (bits in parentheses where useful) |
| I_t | I(c; W_{1:t}) = ln 2 − E[H_b(π_t)] |
| I_k (window) | I(c; W_{t−k+1:t}); by T3 equal to I(c; W_{1:k}) for every t ≥ k |
| acc_t, acc_k | Bayes accuracy of c from w_{1:t}, or from a k-window |
| b_c(h) | World-conditional belief over the 144 states of c: the c-block of the 288-state mixture belief, renormalised |
| q_c(h), q(h) | b_c T E_c (world-conditional next-symbol law); q = (1 − π)q_A + π q_B |
| t* = 32 | Primary analysis position (`SequenceLayout.analysis_position`); w_1..w_32 |
| k_s = 8 | Short-window cutoff of the gates |
| L99(·), U99(·) | Lower and upper ends of the two-sided 99% normal interval, estimate ∓ 2.576·SE |

Event order: emit, then transition (`emit_then_transition`), as in BayesFilter, HMMSampler and `suffix_posterior`. Row vectors throughout.

---

## 1. Question, motivation, scope and licence

### 1.1 Question

In a T²⊔T² process whose components have exactly equal single-symbol statistics, how much information about the component is available:
1. from the last symbol;
2. from the last k = 2, 4, 8 symbols;
3. from the full history at t* = 32;
4. from a sum of independent short-window evidence (four disjoint 8-blocks) rather than from the joint history?

Supporting questions (RQ 2a, 2b):
- How fast does the component posterior concentrate (entropy curve)?
- Do the exact belief clouds show each torus's H1 at a calibrated band, and do they separate the components (β̂₀ = 2)?

### 1.2 Motivation: charter priority 1, competing explanations

Charter priority 1 asks how much structure needs long history versus the last symbol or a short context, and asks that symbol statistics, short-context information and full-history beliefs be distinguished. A trained model's separation of the two components would be informative about long-history use only if the oracle shows that the component is not recoverable from short windows. Stage 0 measures that decomposition at the pilot's own position.

| Explanation for a later model's component separation | Discriminating oracle observation (this protocol) |
|---|---|
| E0: symbol frequencies leak the component | I_1 = 0 exactly (T1); G2.1 |
| E-short: short windows already identify the component | I_8 large relative to I_32 (P4), or acc_32 − acc_8 small (P3) |
| E1: many independent short-window evidences, summed | acc_32 − acc_add small (A3 tier: GO_P1_ADDITIVE) |
| E2: long-timescale structure that no sum of 8-window scores captures | acc_32 − acc_add ≥ 0.03 at the lower 99% bound (GO_P1_NONADDITIVE) |
| The A3 tier cannot separate E1 from E2 in this setting | The N-local positive control (A4) also shows a large non-additive gap (§5.8, reading rule) |

### 1.3 Scope

- Oracle only: no model, no training, no activations, no payload or checkpoint access.
- One frozen construction (§2), with no search over parameters.
- Sampling is used only for Monte Carlo estimates of oracle quantities, under new stage-0 seeds (§6.2).
- No frozen result is altered. B2/D-055, D-1 (D-080) and earlier E-series results are not reopened.

### 1.4 Licence and limits (MD 9, binding)

**Mandatory caveats (MD 9).** The report and every licensed sentence must carry all three:
1. **X2a concerns which component produced the history, not the circular coordinate itself.** Within a component, the circular structure under O stays largely last-symbol-decodable. The relevance to priority 1 is by analogy: a topological distinction (β₀ of the union, a geometric difference of the emission field) that history must supply.
2. **It cannot show exact blindness to short windows.** T2 proves I_2 > 0 for this construction. The finding is a measured gap, never I_8 = 0 (Remark H).
3. **All information sizes in the analysis are forecasts** (accurate to about a factor of 2), not gates. Only quantities computed by the run enter decisions.

**Stage 0 can establish, for this frozen construction only:**
1. Exactly equal symbol marginals (T1) and distinguishability that survives any symbol relabelling (T2). The isometric correction would not have worked (T6).
2. The component-information curve: exact I_k and acc_k for k ≤ 4; validated Monte Carlo I_t and acc_t for t ≤ 33, and window values I_8, acc_8 at t*; descriptive values to t = 128.
3. The decomposition at t*: last symbol (0), ≤ 8-window, additive four-block, and the remainder (A3).
4. The incentive V_32 (descriptive).
5. Whether exact beliefs show each torus's H1 at the calibrated band, and whether full-history beliefs separate the components while 8-window beliefs do not ("reproduced / not reproduced at the band").
6. Whether a later trained stage at context 32 would be informative for priority 1 (§5.9), with T5 as the sharp criterion.

**Licensed sentences** (numbers filled after the run; exactly one applies):
- *GO_P1_NONADDITIVE:* "In a T²⊔T² process with exactly equal symbol statistics, where component B is component A's emission field pulled back by a Dehn twist, the last symbol carries no component information (exact). The last k symbols carry I_k = … nats (k = 2, 4 exact; k = 8 by validated Monte Carlo) and the full 32-symbol history carries I_32 = … nats. Bayes accuracy rises from acc_8 = … to acc_32 = …, and the full history beats the product of four 8-symbol block likelihood ratios by … (lower 99% bound ≥ 0.03). This concerns which component produced the history, not the circular coordinate; short windows are not blind (I_2 > 0)."
- *GO_P1_ADDITIVE:* the same first three sentences, then: "Within the 0.03 margin, the full-history gain over 8-symbol windows is reproduced by summing independent 8-block evidence, so a later trained stage could show use of more than 8 symbols but not long-timescale structure beyond additive short-window evidence." Same caveats.
- *STOP_P1:* "On this construction at t* = 32, the full history does not carry enough component information beyond 8-symbol windows to make a trained-model study informative for priority 1 (P3 = …, P4 = …)." The I_t and acc_t curves are the finding.
- If the N-local reading rule (§5.8) triggers, the sentence must add: "The additive tier did not separate a local-noise comparator from the twist in this setting."

**Stage 0 cannot establish:**
- anything about trained models: representation geometry, learnability, causal use (priority 2), or whether a model actually uses older history;
- anything about other σ, p_stay, twists, torus sizes, or contexts;
- any general claim that tori with equal marginals need long history;
- exact short-window blindness (caveat 2);
- the world's H2, or an exact characterisation of the whole reachable belief space.

Further limits:
- PH counts are statements at the calibrated band only. Hellinger belief clouds are not an activation space.
- Remark H is a scoping statement and is not gated.
- Stage-0 Monte Carlo histories are oracle-only. They must not serve as a trained-model test set (§6.2).

---

## 2. Exact construction (MD 1; L§2 with A1)

### 2.1 World: local, unregistered torus builder (D-1 pattern)

```python
class _X2aTorusBuilder(QuotientLatticeBuilder):          # deliberately NOT @register_world
    family: ClassVar[str] = "_x2a_torus_local"
    expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
    identifications: ClassVar[tuple] = (Identification(0, "periodic"), Identification(1, "periodic"))
```

Validation mirrors `build_world` (as in D-1 §2.6):
1. `spec = _X2aTorusBuilder().build(WorldConfig("_x2a_torus_local", (12, 12), "flat"))`. The builder itself raises BETTI_MISMATCH unless the Betti numbers are (1,2,1) over GF(2) and GF(3).
2. `spec.validate()`.
3. `check_boundary_closed(CubicalComplex(spec.n_states, spec.cells))` (from `topo_pilot.world.complex`).
4. `check_flat_bounds(spec.dist, spec.dist_graph, 2)` (from `topo_pilot.world.metrics`).

WORLD_REGISTRY is never mutated. `spec.dist` is the flat quotient metric, the minimum over the 9 deck images (`FlatQuotientMetric`); on integer lattice points it equals √(δ₁₂(x,x′)² + δ₁₂(y,y′)²).

### 2.2 Kernel and disjoint union

- `T = TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T` (144×144). Every vertex has degree 4, so D_max = 4: T(z, z ± e_i) = (1 − 0.2)/4 = 1/5 and T(z, z) = 1/5.
  - In float64 the off-diagonal entries are 0.8/4 = 0.2000000000000000111 and the diagonal is 1 − 0.8 = 0.1999999999999999556 [W]. Both are within 6×10⁻¹⁷ of 1/5. G0 compares against the exact Fraction with tolerance 1e-15.
  - T is symmetric, hence doubly stochastic, so the uniform law u₁₄₄ is stationary.
- Both components use this **same** T; they differ only in emission.
- T̃ = blockdiag(T, T) (288×288). Start π̃ = 1/288 on all 288 states. π̃ is stationary for T̃: each component has probability ½ and, given the component, the state law is uniform at every t.
- A disjoint union is not a QuotientLatticeBuilder family, so it is assembled as the block matrix (RQ code fact).

### 2.3 Emission A: the pilot's O field on the torus, as an explicit array (A1: minimum image)

`process._geometry.point_distances` wraps axis 0 only, so the registered O mode would be non-periodic in y on a torus. It is **never called** (guard test, §8.4).

Define the 12×6 one-dimensional field, with 2σ² = 3.125:

  e[x, a] := exp(−δ₁₂(x, 0.5 + 2a)²/2σ²) / Σ_{a′=0}^{5} exp(−δ₁₂(x, 0.5 + 2a′)²/2σ²),

and the 144×36 array

  E_A[12x + y, 6a + b] := e[x, a] · e[y, b].

**Why the product is exact.** The minimum-image squared distance on the torus is δ₁₂(x, c_x)² + δ₁₂(y, c_y)², because the minimum over the 9 deck images (m, n ∈ {−1, 0, 1}) of (x − c_x + 12m)² + (y − c_y + 12n)² separates into independent minima over m and n. The logits are therefore a sum of an x-term and a y-term, and the softmax over the 6×6 centre grid is the product of the two 1-D softmaxes.

**G1 reference (A1).** The independent check computes, for every state and centre, the **minimum** over the 9 images of the squared distance, then a 2-D softmax over the 36 centres with log-sum-exp. It must match E_A within abs ≤ 1e-15 and rel ≤ 1e-12. **The images must not be summed:** a wrapped (summed) Gaussian differs at the farthest centre (d = 5.5) by a relative e^{−(6.5² − 5.5²)/3.125} = e^{−3.84} = 0.0215 [W re-derived], an absolute ≈ 8.6 × 10⁻⁷, far above the tolerance (AN §1.4 L1).

**Smoothness (minor, AN §1.4 L6).** The minimum-distance Gaussian has cut-locus kinks at per-axis distance 6 from a centre. No lattice state lies there: per-axis distances from the half-integer centres are 0.5, 1.5, …, 5.5. The lattice array is therefore unaffected.

**Hand values [W]** (recomputed; σ = 1.25). For every x the six centre distances are the multiset {0.5, 1.5, 2.5, 3.5, 4.5, 5.5}, so the normaliser is Z = 1.566641 for every x and the probability of the centre at distance d is p(d):

| d | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 5.5 |
|---|---|---|---|---|---|---|
| exp(−d²/3.125) | 0.923116 | 0.486752 | 0.135335 | 0.019841 | 0.0015338 | 0.0000625 |
| p(d) | 0.589233 | 0.310698 | 0.0863856 | 0.0126647 | 0.000979 | 0.0000399 |

Column 0 of e (centre 0.5) is (p.5, p.5, p1.5, p2.5, p3.5, p4.5, p5.5, p5.5, p4.5, p3.5, p2.5, p1.5) for x = 0..11. The smallest entry of E_A is p(5.5)² ≈ 1.6 × 10⁻⁹ [W]; every entry is strictly positive. The per-axis reading variance Σ_d p(d)d² = 1.56246 [W].

### 2.4 Emission B: A's field pulled back by a Dehn twist

  φ(x, y) := ((x + y) mod 12, y),  E_B[12x + y, :] := E_A[12·((x + y) mod 12) + y, :].

**Properties of φ.**
1. φ is a group automorphism of Z₁₂² with matrix [[1, 1], [0, 1]] (determinant 1). It is induced by a linear map of R² that preserves the lattice 12Z², so it is an area-preserving smooth diffeomorphism of the flat torus (a linear Dehn twist).
2. φ is **not** an automorphism of the grid graph: the edge (0,0)–(0,1) maps to (0,0)–(1,1), which is not an edge.
3. φ is Lipschitz for the flat torus metric with constant ‖[[1,1],[0,1]]‖ = (1 + √5)/2 ≈ 1.618 (the largest singular value). A lattice step e₂ maps to (1, 1), of length √2.

Hence E_B is a smooth, non-isometric warp of the emission field and a **row permutation** of E_A: the row multiset, H(W ∣ Z), and the law of one-symbol posteriors are identical in both components.

**Lemma U (emission coordinates).** Put u = φ(z). Under c = B, u is a stationary walk on Z₁₂² with step law K_B: 0, ±(1, 0), ±(1, 1), each with probability 1/5, observed through the **unchanged** E_A. Under c = A, z is the walk with K_A: 0, ±(1, 0), ±(0, 1), each 1/5, observed through E_A.

*Proof.* T(z, z′) = K_A(z′ − z). Since φ is a linear bijection, u′ − u = φ(z′ − z), so u has step law K_A∘φ⁻¹, which puts 1/5 on φ(0) = 0, φ(±e₁) = ±(1, 0) and φ(±e₂) = ±(1, 1). u is uniform at t = 1 because φ is a bijection and z is uniform. The emission is E_B[z] = E_A[φz] = E_A[u]. ∎

So the two components share one emission geometry and one walk graph; they differ in how the walk's moves sit in that geometry. B's "vertical" moves are diagonal.

### 2.5 Mixture and literal model

| Item | Value |
|---|---|
| T̃ | blockdiag(T, T), 288×288 |
| Ẽ | `np.vstack((E_A, E_B))`, 288×36, built once |
| π̃ | uniform 1/288 |
| Tokens | ids 0..35; sequences of 33 symbols (`SequenceLayout()` default) for all gated quantities |

Neither the mixture nor any emission array is written into a production spec. TransitionSpec is used only per component.

### 2.6 Variants (controls; built in the same module, never registered)

| Id | Second block E₂ (first block is always E_A) | Role |
|---|---|---|
| main | E_B (Dehn twist) | The experiment |
| N-iso | E_A translated by (1, 0): E₂[12x + y] = E_A[12((x+1) mod 12) + y] | Required null (T6) |
| N-same | E₂ = E_A | Required null (T6 with g = id; X's identical-component null) |
| N-id | E = 1/36 in **both** blocks (the codebase's `Identical` mode) | Required null |
| N-swap | Ẽ′ = vstack(E_B, E_A) | Required label-exchange identity |
| P-ref | E₂ = E_A[axis_state_perm(*draw_axis_permutation(spec), (12, 12))] (existing helpers in `topo_pilot.process.emission`) | Descriptive; PH specificity control (the original X2a's P-world) |
| N-local | E₂ = K E_A with K = ¾I + ⅛R₊ + ⅛R₋, R± shifting the state by ±2e_x (X's blur on L's field and dynamics; A4, MD 5) | Descriptive positive control for the additive mechanism |

### 2.7 Why this B (alternatives rejected)

| Alternative | Why rejected |
|---|---|
| Translation or reflection of E_A (any grid automorphism) | Identical sequence laws, π ≡ ½ (T6): the request's core defect. Used as N-iso |
| Axis-wise permutation (original X2a) | Equal marginals, but not smooth, and E1 found no belief H1 under P. Kept as P-ref |
| X's blur E_B = K E_A (X§3.5) | Valid and marginal-preserving, but it is exactly A's output passed through an i.i.d. symbol channel a ↦ a + ξ (Proposition N): a noise-level difference, not a geometric warp. Its evidence is local and accumulates almost additively (AN §1.3, §2.2). X's gates at t = 512 also sit outside the pilot's 33-symbol context (MD 1 rationale). Kept as the N-local comparator |
| Different σ in B | Marginals are still uniform, but per-state emission entropy differs: again a local noise statistic |
| Twisted-lattice torus Z²/⟨(12,0),(6,12)⟩ | Needs a non-square fundamental domain and new metric code. Global symbol labels change the symbol-adjacency graph, so pairs detect it anyway (L§2.5) |

---

## 3. Theorems and proofs (for this construction)

### T1. Exactly equal symbol marginals

**Statement.** For c ∈ {A, B}, every t ≥ 1 and every symbol j: P(W_t = j ∣ c) = 1/36. Hence P(c ∣ W_t) = ½ at every single position, and I_1 = 0.

*Proof.*
1. **Equivariance.** δ₁₂(x + 2, 0.5 + 2(a + 1)) = δ₁₂(x, 0.5 + 2a). The normaliser at x + 2 is the sum over a′ of exp(−δ₁₂(x + 2, 0.5 + 2a′)²/2σ²). Re-index a′ = a″ + 1 (mod 6; valid because 0.5 + 2·6 ≡ 0.5 mod 12): it equals the normaliser at x. So e[x + 2, a + 1] = e[x, a].
2. **Column sums of e.** By step 1, Σ_x e[x, a + 1] = Σ_x e[x + 2, a + 1] = Σ_x e[x, a], so the six column sums are equal. Every row of e sums to 1, so they total 12 and each equals 2.
3. **Column sums of E_A.** Σ_z E_A[z, (a, b)] = (Σ_x e[x, a])(Σ_y e[y, b]) = 4.
4. E_B is a row permutation of E_A, so it has the same column sums.
5. **Stationarity.** Given c, the state is uniform at every t (uniform start, doubly stochastic T). So P(W_t = j ∣ c) = 4/144 = 1/36 for both c. Bayes' rule with prior ½ gives P(c ∣ W_t) = ½, and I(c; W_t) = 0. ∎

### T7. Full support

**Statement.** Every finite string has positive probability under both components. Hence 0 < π_t(h) < 1 at every history, and neither BayesFilter nor `suffix_posterior` can raise an impossible-history error.

*Proof.* Every entry of E_A (and so of E_B, E_N, E_P) is ≥ p(5.5)² > 0 and π̃ > 0. The path that stays at its start state has probability π̃(z)·Π E(z, w_s)·(1/5)^{t−1} > 0 for any string w_{1:t}. ∎

### T2. Distinguishability (exact witness)

**Statement.** Let G(d) := Σ_{x∈Z₁₂} e[x, 0] e[x + d, 0]. Then

  Δ_rep := P_A(W_{t+1} = W_t) − P_B(W_{t+1} = W_t) = (α/2)·G(1)·(G(0) − G(1)) > 0.

Consequences:
- P_A^(2) ≠ P_B^(2), so I_2 > 0, and by T4 I_k > 0 for all k ≥ 2.
- The repeat probability is invariant under any relabelling of symbols (applied to both positions) and under any grid automorphism of the states. So no symbol permutation ψ gives P_B = P_A∘ψ: B is not A up to naming or isometry.

*Proof.*
1. **Pair sum.** By Lemma U, for each c the pair (u_t, u_{t+1}) is uniform u_t with an independent step δ ~ K_c, both observed through E_A:

   P_c(repeat) = (1/144) Σ_u Σ_δ K_c(δ) Σ_j E_A[u, j] E_A[u + δ, j].

2. **Factorisation.** Σ_u Σ_j E_A[u, j] E_A[u + δ, j] = H(δ_x)·H(δ_y), where H(d) := Σ_a Σ_x e[x, a] e[x + d, a]. By T1 step 1, e[x, a] = e[x − 2a, 0], so each a contributes G(d): H = 6G. Also G(−d) = G(d).
3. **Both repeat probabilities.** (1/144)·36 = ¼, so
   - P_A(repeat) = ¼[α G(0)² + 2α G(1)G(0) + 2α G(0)G(1)] = ¼[0.2 G(0)² + 0.8 G(0)G(1)];
   - P_B(repeat) = ¼[α G(0)² + 2α G(1)G(0) + 2α G(1)G(1)] = ¼[0.2 G(0)² + 0.4 G(0)G(1) + 0.4 G(1)²].
4. **Difference.** Δ_rep = ¼ · 2α · (G(0)G(1) − G(1)²) = (α/2) G(1)(G(0) − G(1)).
5. **Sign.** G(1) > 0 because every entry of e is positive. Let S be the cyclic shift and e₀ = e[·, 0]. Cauchy–Schwarz gives G(1) = ⟨e₀, S e₀⟩ ≤ ‖e₀‖‖S e₀‖ = ‖e₀‖² = G(0), with equality only if S e₀ = e₀, i.e. e₀ constant. It is not: e[0, 0] = p(0.5) ≠ e[6, 0] = p(5.5). ∎

**Hand values [W]** (recomputed):

| Quantity | Value |
|---|---|
| G(0), G(1), G(2) | 0.902705, 0.769235, 0.475989 |
| G(3), G(4), G(5), G(6) | 0.213878, 0.069815, 0.016887, 0.005687 |
| Δ_rep = 0.1 × 0.769235 × 0.133470 | **0.010267** |
| P_A(repeat) | 0.179622 |
| P_B(repeat) | 0.169355 |
| JS(Bern(P_A), Bern(P_B)) (exact), repeat indicator alone | 9.149 × 10⁻⁵ nats (1.320 × 10⁻⁴ bits) |

By data processing, I_2 ≥ 9.1 × 10⁻⁵ nats from the repeat indicator alone. This bound is loose; the full I_2 is forecast at 2–5 × 10⁻³ bits [H] (§4.4). The pair-level signal is small.

### T3. Window reduction

**Statement.** For every t ≥ k: I(c; W_{t−k+1:t}) = I(c; W_{1:k}) = I_k = JS(P_A^(k), P_B^(k)), the Jensen–Shannon divergence with weights ½, ½. The window posterior π_t^(k) has the same law as π_k, and the window Bayes accuracy equals acc_k.

*Proof.*
1. Given c, the hidden chain is stationary (uniform start, doubly stochastic T), and the emission is time-homogeneous. So (c, W_{t−k+1:t}) has the same joint law as (c, W_{1:k}).
2. For c ~ Bern(½), I(c; W) = ½KL(P_A‖M) + ½KL(P_B‖M) with M = ½(P_A + P_B), which is the JS divergence. ∎

**Lemma R (stationary restart is exact).** For a window w_{t−k+1:t}, the posterior over (c, z_t) equals the BayesFilter output started from π̃ on that window alone.

*Proof.* Without conditioning on earlier symbols, the joint law of (c, z_{t−k+1}) is ½ × uniform = π̃ (stationarity given c). From there the window is generated by the same HMM (T̃, Ẽ). ∎

**Consequences.**
- Knowing the position adds nothing.
- At position t, the information that needs history older than k is I(c; W_{1:t−k} ∣ W_{t−k+1:t}) = I_t − I_k.
- The entropy curve of RQ (a) is E[H_b(π_t)] = ln 2 − I_t, so one curve answers both (a) and (c).
- The four blocks of w_{1:32} each have the law of P_c^(8) given c, so each block posterior is an exact 8-window posterior.

### T4. Monotonicity and limit

**Statement.** I_k ≤ I_{k+1} ≤ ln 2 and acc_k ≤ acc_{k+1}; I_t → ln 2 and acc_t → 1 as t → ∞.

*Proof.*
1. Monotonicity: W_{1:k} is a function of W_{1:k+1} (data processing for I; a classifier of the shorter string is a classifier of the longer).
2. Ergodicity: the pair process (z_t, W_t) is a stationary Markov chain on 144 × 36 states with transition T(z, z′)E(z′, w′). It is irreducible (T irreducible, E > 0) and aperiodic (T(z, z) E(z, w) > 0 gives a self-loop), hence mixing. W is a factor of it, so each component's output process is stationary and mixing, hence ergodic.
3. By T2 the two output laws differ. Distinct stationary ergodic measures are mutually singular: some cylinder event has different frequencies, and by Birkhoff's theorem the two sets of sequences with each limiting frequency have full measure under one law and zero under the other.
4. π_t is a bounded martingale, so π_t → P(c = B ∣ W_{1:∞}) almost surely (Lévy). By step 3, c is a.s. a function of W_{1:∞}, so the limit is 1{c = B}. Then H_b(π_t) → 0 a.s. and, by bounded convergence, I_t → ln 2; likewise max(π_t, 1 − π_t) → 1. ∎

### T5. Data-processing bound (what makes a later trained test sharp)

**Statement.** For any measurable (possibly randomised, independently of c given the window) function f of the last k symbols at position t:
- I(c; f(W_{t−k+1:t})) ≤ I_k;
- any classifier of c based on f has accuracy ≤ acc_k.

*Proof.* c → W_{t−k+1:t} → f(W) is a Markov chain; apply data processing and T3. A classifier of f(W) is a classifier of W, and acc_k is the Bayes optimum over classifiers of W. ∎

**Contrapositive.** If a representation at position t decodes c on held-out histories with accuracy significantly above acc_k, it is not a function of the last k symbols.

### T6. Isometric null

**Statement.** Let g be any automorphism of the 12×12 torus grid graph (a translation, or a dihedral map about any point). If E_{B′}[z] = E_A[g z], then P_{B′} = P_A on all strings, so π_t ≡ ½ and I_k = 0 for every k.

*Proof.* T depends only on adjacency (max-degree lazy walk with constant degree), so T(gz, gz′) = T(z, z′), and the uniform start is g-invariant. The map (z_1, …, z_t) ↦ (g z_1, …, g z_t) is a bijection of state paths that preserves path probabilities and carries emission probabilities E_{B′}[z_s, w_s] to E_A[g z_s, w_s]. Summing over paths gives P_{B′}(w) = P_A(w). ∎

N-iso (g = translation by (1, 0)) and N-same (g = identity) are instances.

### Lemma C (credit form of accuracies; W)

Let d(h) ∈ {A, B, tie} be any decision computed from w_{1:32}. Define its **credit**

  cr_d(h) := π_32(h) if d = B; 1 − π_32(h) if d = A; ½ if d = tie,

where π_32 is the exact full-history posterior. Then:
1. E[cr_d] = P(d is correct), with ties counted as a fair coin.
2. cr_32 := max(π_32, 1 − π_32) ≥ cr_d pointwise, and cr_32 − cr_d = |2π_32 − 1|·(1[d ≠ ĉ_32, d ≠ tie] + ½·1[d = tie]) ∈ [0, 1].
3. Hence acc_8 ≤ acc_32 and acc_add ≤ acc_32, with per-row differences in [0, 1].

*Proof.* Equal priors and Bayes' rule give E[1{c = B} ∣ w_{1:32}] = π_32. Because d is a function of w_{1:32}, conditioning on the history gives (1), and (2) is immediate from the definitions. (3) follows from (1) and (2). ∎

**Note.** acc_add ≥ acc_8 is **not** guaranteed: the additive rule is not Bayes-optimal for anything.

**Tie rule (fixed now).** d = tie iff |π_d − ½| ≤ 1e-12, where π_d is the decision's posterior or pseudo-posterior. It matters for k = 1, where π^(1) = ½ up to rounding (T1), so acc_1 is exactly ½ by construction.

### Lemma A (additive four-block score; A3)

Define s_add(h) := Σ_{β=1}^{4} logit π^blk_β(h) and π_add := expit(s_add). Then:
1. By Lemma R and equal priors, logit π^blk_β = ln[P_B(block β)/P_A(block β)], so s_add = ln Π_β LR_β: the product of experts over the four disjoint 8-blocks (AN §2.5).
2. s_add is the exact full-history log-likelihood ratio iff the four blocks are conditionally independent given c. They are not, because the hidden state carries across block boundaries. π_add is therefore not a calibrated posterior.
3. By T3, given c all four blocks have the law P_c^(8), so E_c[s_add] = 4·E_c[logit π^(8)].

*Proof.* (1) and (3) follow from Lemma R and T3. (2): the full likelihood is the product of block likelihoods exactly when the joint law factorises over blocks. ∎

Consequences for estimation (§4.2): acc_add must be computed as a **classification accuracy** (Lemma C credit), never as E[max(π_add, 1 − π_add)], which would be biased because π_add is uncalibrated. The information-type summary is the cross-entropy lower bound I_add^LB (§4.2), not ln 2 − E[H_b(π_add)].

### Proposition N (the N-local comparator; A4)

With K = ¾I + ⅛R₊ + ⅛R₋ acting on states (R± shifts by ±2e_x):
1. E_N = K E_A is a valid emission with every entry positive.
2. Its column sums equal those of E_A (K is doubly stochastic, since each R± is a permutation matrix), so T1 holds for the mixture A ⊔ N.
3. **Symbol channel.** By T1 step 1, E_A[z + 2e_x, (a, b)] = E_A[z, (a − 1, b)]. So E_N[z, (a, b)] = ¾E_A[z, (a, b)] + ⅛E_A[z, (a − 1, b)] + ⅛E_A[z, (a + 1, b)]: N's output is A's output passed through an i.i.d. channel a ↦ a + ξ (mod 6), ξ ∈ {0, ±1} with probabilities ¾, ⅛, ⅛ (AN §1.3).
4. **Not a row permutation.** In Fourier modes m of the x-axis, K has eigenvalues κ_m = ¾ + ¼cos(4πm/12) ∈ [½, 1], equal to 1 only for m ∈ {0, 6}. A column x ↦ e[x, a]e[y, b] is not 2-periodic in x (e[0, 0] = p(0.5) ≠ e[2, 0] = p(1.5)), so it has a mode with κ_m < 1 and ‖E_N‖_F < ‖E_A‖_F strictly. Row permutations preserve the Frobenius norm, so E_N is neither a P-world nor any pullback of E_A.
5. **Two-symbol witness.** Let g(x) := e[x, 0] = P(a(W) = 0 ∣ z) under A, and (Kg)(x) the same under N. On functions of x the walk acts as L = 0.6I + 0.2R₊₁ + 0.2R₋₁ (x is unchanged with probability 0.2 + 0.4), with eigenvalues λ_m = 0.6 + 0.4cos(2πm/12) ∈ [0.2, 1] > 0. Then S_A := P_A(a(W₁) = 0, a(W₂) = 0) = (1/12)gᵀLg and S_N = (1/12)gᵀKLKg. In Fourier, S_A − S_N = (1/144)Σ_m |ĝ_m|² λ_m (1 − κ_m²) > 0, strictly by (4).

*Proof.* (1)–(4) as stated. (5): K and L are circulant, so they commute and diagonalise in the same Fourier basis. ∎

**Hand values [W]** (no input supplies them, because X's hand values were for p_stay ½ and integer centres): S_A = 0.0707764, S_N = 0.0573220, difference 0.0134544. ‖e₀‖² = 0.902705 versus ‖Ke₀‖² = 0.716659. Repeat probabilities 0.179622 (A) versus 0.145669 (N). The N-local repeat gap, 0.0340, is 3.3 times the twist's Δ_rep: N-local is far more visible to pairs, as intended for a local-evidence positive control.

### Lemma P (pooled reference clouds; W)

If two finite clouds X_A, X_B ⊂ Δ²⁸⁷ have supports in disjoint blocks, every cross pair is at Hellinger distance exactly 1. Hence for r < 1, VR_r(X_A ∪ X_B) = VR_r(X_A) ⊔ VR_r(X_B), and the Betti numbers add.

*Proof.* The Bhattacharyya coefficient of distributions with disjoint supports is 0, so H = √(1 − 0) = 1. No VR simplex at scale r < 1 contains a cross pair. ∎

So X's pooled calibration requirement (β₀ = 2, β₁ = 4 for the union, X§6.2) holds automatically on [0, 1) once each component reference has β₀ = 1, β₁ = 2. The band search is restricted to [0, 0.99].

### Remark H (holonomy; reworded per A1, not gated)

- Within this class (one shared T, an emission that is a row permutation of E_A, stationary start), I_1 = 0 always (T1's argument).
- For the Dehn twist, T2 **proves** I_2 > 0. For other smooth warps in the class, k = 2 leakage is generic, because the pair law is a local functional of the field and exact cancellation is non-generic, but it is **not proved**. "This class always leaks at k = 2" is a theorem only for the twist.
- Exact blindness to short windows needs locally identical but globally different labelled structure. If both components carry the same label field and it descends to both quotients, the field descends to their common coarser quotient. Both components then cover that quotient, and a covering projection preserves the walk-plus-emission law, so the laws coincide. A difference therefore needs a **label twist (holonomy) at a gluing**, and the twist must also be locally invisible (a gauge or hidden-fibre construction). An ordinary relabelling twist creates new symbol adjacencies at the seam, which pairs detect.
- **The holonomy need not be non-abelian.** The documented X6 transport task (`docs/proposals/X6_TOPOLOGICAL_INVARIANTS.md`) uses flat Z₂ (abelian) edge transport and equalises only unigram and bigram laws. Its witness is a six-edge winding between two reveals, about 8 symbols, so X6 is not automatically 8-window-blind either and needs its own I_k curve.
- This stage's priority-1 sharpness therefore rests on the **size** of I_32 − I_8 and acc_32 − acc_8 (T5), and on the A3 tier, not on zero short-window information.

### Identities used as checks or descriptive values

- **Increment.** i_{t+1} := I_{t+1} − I_t = I(c; W_{t+1} ∣ W_{1:t}) = E_h[(1 − π)·KL(q_A‖q) + π·KL(q_B‖q)], with q_c = b_c T E_c and q = (1 − π)q_A + πq_B the mixture predictive. Since I_1 = 0, I_32 = Σ_{s=1}^{31} i_{s+1}.
- **Incentive (P5, descriptive).** V_t := E_h[KL(q(h) ‖ q^½(h))], with q^½ = ½q_A + ½q_B. It is the next-symbol excess log-loss of a predictor that knows both world-conditional beliefs but not the component posterior, i.e. the training incentive to represent π.

---

## 4. Quantities

### 4.1 Exact quantities (float64, deterministic, no sampling)

1. **Pair laws.** M_c = (1/144)·E_cᵀ T E_c (36×36). trace(M_A) − trace(M_B) is checked against T2's closed form. Lemma U is checked by computing M_B a second way, as (1/144)·E_Aᵀ T_u E_A with T_u the K_B walk.
2. **Block laws for k ≤ 4**, by forward recursion per component: α₁ = u₁₄₄ ⊙ E_c[:, w₁], α_{s+1} = (α_s T) ⊙ E_c[:, w_{s+1}]. Level 3 has 46,656 rows × 144 states; P_c(w_{1:4}) = (α₃ T E_c)[w_{1:3}, w₄], giving 36⁴ = 1,679,616 probabilities per component.
3. **Jensen–Shannon, corrected form (W; see §10.2 C1).** With M(h) = ½(P_A(h) + P_B(h)) and r(h) = (P_A − P_B)/(P_A + P_B):

   I_k = Σ_h M(h)·φ(r(h)), φ(r) = ½[(1 + r)ln(1 + r) + (1 − r)ln(1 − r)].

   (Check: disjoint point masses give 2 × ½ × ln 2 = ln 2.) For |r| < 10⁻³ use the series φ(r) = Σ_{n=1}^{4} r^{2n}/(2n(2n − 1)) (truncation error below r¹⁰/90 < 10⁻³²); otherwise use log1p. Accumulate with `math.fsum` per level-3 block. T7 guarantees |r| < 1.
4. **Exact accuracy:** acc_k = Σ_h max(P_A(h), P_B(h))/2 = Σ_h M(h)(1 + |r(h)|)/2.
5. **Exact outputs:** I_1..I_4, acc_1..acc_4, ln 2 − I_t for t ≤ 4, in nats and bits.
6. **Variants:** the same for N-iso and N-same (must be 0) and for P-ref and N-local (descriptive).

### 4.2 Monte Carlo estimands (per-row statistics, averaged over the stratified sample of §6)

All are equal-weight means over 2¹⁹ rows per component, which are unbiased for the ½/½ mixture.

| Quantity | Per-row statistic | Notes |
|---|---|---|
| Î_t, t = 1..33 | ln 2 − H_b(π_t) | Rao–Blackwellised (uses the true posterior) |
| Î′_t (validation) | ln 2 + ln P(c_true ∣ h_{1:t}) | Label-based; same expectation |
| Î^win_k, k ∈ {1, 2, 4, 8}, at t* | ln 2 − H_b(π^(k)_32) | Window w_{33−k}..w_32 |
| âcc_t | max(π_t, 1 − π_t) | Rao–Blackwellised |
| âcc_k^win (gate form) | cr_k = credit of d_k = argmax π^(k)_32 (Lemma C) | Paired with âcc_32 |
| âcc_k^win (validation form) | max(π^(k), 1 − π^(k)) | Same expectation (π^(k) is calibrated) |
| âcc_add | cr_add = credit of d_add = sign(s_add) (Lemma C) | Classification accuracy of the additive rule |
| Î_add^LB (descriptive) | ln 2 + π_32 ln π_add + (1 − π_32) ln(1 − π_add) | Rao–Blackwellised cross-entropy bound: I_add^LB ≤ I(c; s_add) ≤ I_32, and per row I_32-term − I_add^LB-term = KL(Bern(π_32)‖Bern(π_add)) ≥ 0 |
| ρ_add (descriptive) | KL share: [E_A(−s_add) + E_B(s_add)] / [E_A(−logit π_32) + E_B(logit π_32)] | = 4(KL₈^AB + KL₈^BA)/(KL₃₂^AB + KL₃₂^BA) by Lemma A(3); estimated per stratum |
| î_{t+1}, t = 1..31 | (1 − π_t)KL(q_A‖q) + π_t KL(q_B‖q) | Increment identity |
| V̂_t, t ∈ {1..32}; V_32 (P5) | KL(q ‖ ½q_A + ½q_B) | Descriptive |
| Concentration | fractions with max(π_t, 1 − π_t) ≥ 0.9 and ≥ 0.99; quantiles 5/25/50/75/95% of H_b(π_t) | RQ (a) |
| LLR slope | per-component mean logit π_t and its least-squares slope over t ∈ [16, 32] | Estimate of the relative-entropy rate |

**Paired gate statistics** (computed per row on the same histories):
- D3 := cr_32 − cr_8 (P3), with values in [0, 1];
- D_add := cr_32 − cr_add (A3), with values in [0, 1];
- descriptively, I_32 − 2I_8 per row = 2H_b(π^(8)) − H_b(π_32) − ln 2 (paired form of P4) and acc_add − acc_8.

**Descriptive extras (not gated).**
1. The pilot's context gain at t*: `context_gain(q_32, LastSymbolPosterior(T̃, Ẽ, π̃).q_last(w_32))`.
2. The predictive gain of the full history over the 8-window: `context_gain(q_32, q^(8)_32)` with q^(8) = b^(8) T̃ Ẽ (X§7.5). It mixes position and component information.
3. The long-horizon curve to t = 128 (§6.5, A5).

### 4.3 P5 (descriptive only; A2, MD 2)

Report V_32 with its 99% interval and the trained-stage feasibility flag: INCENTIVE_ABOVE_0.01 if L99(V_32) ≥ 0.01 nats; INCENTIVE_BELOW_0.01 if U99(V_32) < 0.01; otherwise INCENTIVE_STRADDLES. The flag informs a later protocol's learning gate and never changes the stage-0 outcome.

### 4.4 Forecasts (recorded now; not criteria; MD 9 caveat 3)

From AN §2.3 [H], in bits unless marked. L's twist (this protocol); X's blur column is for X's own construction (p_stay ½), not for N-local.

| Quantity | Twist [H] | X's blur [H] |
|---|---|---|
| I_1 | 0 (exact, T1) | 0 (exact) |
| I_2 | 2–5 × 10⁻³ (repeat indicator alone ≥ 1.32 × 10⁻⁴ [W]) | 1.5–3 × 10⁻² |
| I_4 | 1–3 × 10⁻² | 4–8 × 10⁻² |
| I_8 | 0.04–0.10 | 0.07–0.20 |
| I_32 | 0.25–0.45 | 0.30–0.50 |
| I_8/I_32 | ≈ 0.1–0.25 | ≈ 0.25–0.4 |
| acc_8, acc_32 | ≈ 0.62; 0.75–0.85 | ≈ 0.65; 0.78–0.85 |
| Additive KL share | ≈ 0.55 | ≈ 0.9 |
| acc_32 − acc_add | ≈ 0.05–0.07 | ≲ 0.02 |
| V_32 (nats) | 0.004–0.012 | 0.004–0.010 |

Forecast verdicts [H]: P3 gap ≈ 0.13–0.21 (likely PASS); P4 ratio ≈ 0.1–0.25 (likely PASS); A3 gap ≈ 0.05–0.07, so NONADDITIVE is plausible but not certain; P5 about a coin flip (descriptive now); Q2-full near-impossible at t* (acc_32 ≈ 0.8, so unconcentrated histories bridge the clouds). In the Gaussian-displacement picture (Lemma U), Σ_A = 0.4I and Σ_B = [[0.8, 0.4], [0.4, 0.4]] have equal determinants 0.16, and one fully resolved displacement is worth KL = 0.5 nats in either direction [re-derived by W]. Discrimination concentrates at timescales of about 10 steps or more (AN §2.2), which is why I_k is superlinear in small k.

---

## 5. Gates, criteria, verdicts and stop rules

### 5.0 Order and statuses

**Execution order:** PF (preflight) → S0 → G0 → G1 → G2 → G3 → G4 → D (P3, P4, A3; values sealed) → PH (calibration and readings) → G5 (controls) → verdict.

- Every gate records PASS, FAIL, INVALID or NOT_RUN. D, PH and the descriptive items record values and labels.
- The run stops at the first FAIL or INVALID in PF, S0 or G0–G4, and records every later gate as NOT_RUN.
- D and PH values are computed before G5 but **sealed**: the outcome labels are released only if G5's required controls pass. If G5 fails, the overall verdict is FAIL and the D and PH labels are WITHHELD, with their values preserved for diagnosis.
- All gates are deterministic given the frozen seeds.

### 5.1 PF (mandatory preflight) and S0

**PF.** A metered run (the job-0014 meter, store-local binding, measure-only, as in D-1) of:
- the unchanged regression suites `tests/world`, `tests/process`, `tests/oracle`, `tests/oracle_profile`, `tests/topology`, `tests/dataset`;
- the new `tests/x2a_stage0` (§8.4), including registry hygiene and the `point_distances` / `is_x_periodic` guards;
- `tools/check_file_sizes.py` (every .py ≤ 400 lines).

The record is `preflight.json`. Any failure, or inability to complete, gives overall INVALID with every gate NOT_RUN (D-1 coordinator ruling 8). PF takes precedence over S3–S5.

**S0.** Run only if all of the following hold:
- the protocol is frozen and its SHA256 matches the freeze record;
- the request SHA256 equals `4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595`;
- `git diff c364f95e5573940cdc24b569b0fb7c6a16c97ab8 HEAD -- src tools/x4_oracle_profile tests/oracle_profile` is empty (the `d1_seam_checks.s0_check` pattern).

A violation gives INVALID ("do not run").

### 5.2 G0: structure

1. The builder validates per §2.1. An exception invokes S2.
2. Counts: 144 vertices, 288 edges, 144 squares; χ = 0; Betti numbers (1, 2, 1) over GF(2) and GF(3); ∂₁∂₂ = 0.
3. Every degree is 4 and D_max = 4.
4. T equals the independent Fraction formula (1/5 on each of the 4 neighbours and on the diagonal) within 1e-15 entrywise. T is exactly symmetric, and its support equals the edges plus the diagonal.
5. T̃ is block-diagonal, with both blocks bitwise equal to T and zero off-diagonal blocks.
6. π̃T̃ = π̃ within 1e-15, and `validate_process(T̃, Ẽ, π̃)` (oracle_profile, tol 1e-12) returns without error.

### 5.3 G1: emission construction; G2: exact identities

**G1.**
1. E_A matches the brute-force **minimum-image** 2-D softmax (§2.3, A1): abs ≤ 1e-15 and rel ≤ 1e-12.
2. Rows of E_A, E_B, E_N, E_P sum to 1 within 1e-14; every entry is > 0; the minimum entry is reported (expected p(5.5)² ≈ 1.6e-9 [W]).
3. Z₆² equivariance: |E_A[z + (2, 0), (a + 1, b)] − E_A[z, (a, b)]| ≤ 1e-15, and likewise in y.
4. E_B equals E_A[φ] **bitwise**, and `np.array_equal(np.sort(E_A, 0), np.sort(E_B, 0))` holds.
5. φ is a bijection and not a grid automorphism (witness edge (0,0)–(0,1) ↦ (0,0)–(1,1)).
6. Ẽ is built once, and its blocks are bitwise equal to E_A and E_B.
7. E_P is bitwise E_A[state_perm] and has the same column-sorted multiset. E_N equals ¾E_A[z] + ⅛E_A[z + 2e_x] + ⅛E_A[z − 2e_x] within 1e-15 and matches the symbol-channel form of Proposition N(3) within 1e-15.

**G2** (exact enumeration, §4.1).
1. T1: every column sum of E_A, E_B, E_N, E_P equals 4 within 1e-12. At t = 1, |π − ½| ≤ 1e-14 for all 36 symbols. I_1 ≤ 1e-15.
2. T2: trace(M_A) − trace(M_B) equals (α/2)·G(1)(G(0) − G(1)), computed from `e`, within 1e-14, and is > 0.
3. Lemma U: M_B computed from E_B and T equals (1/144)E_Aᵀ T_u E_A within 1e-15.
4. The k ≤ 4 laws of both components are invariant under the 36 symbol translations (a, b) ↦ (a + α′, b + β′), within relative 1e-12. (For B, a symbol translation corresponds to the state translation z ↦ z + (2α′ − 2β′, 2β′), a grid automorphism.)
5. I_1 ≤ I_2 ≤ I_3 ≤ I_4 (each step ≥ −1e-15). I_2 > 0. I_2 from the enumeration equals JS(M_A, M_B) within relative 1e-10.
6. The hand values of §2.3, T2 and Proposition N are reported next to the computed values. They are not gated.

### 5.4 G3: numerical oracle cross-checks

On the first 2¹³ rows of each stratum (2¹⁴ rows), for all t ≤ 33 unless stated.
1. **Independent stencil filter.** It never forms T: it applies the §2.2 rule with `np.roll` on 12×12 arrays per component and combines the components by log-evidence. Against BayesFilter: beliefs within 1e-12 (abs) and π within 1e-11.
2. π from the per-component filters, expit(LLR_t) with LLR_t = log_evidence_B − log_evidence_A from `BayesFilter(T, E_c, u₁₄₄)`: within 1e-10 of the mixture π.
3. The mixture predictive equals (1 − π)q_A + πq_B within 1e-12.
4. The mixture `exp(log_evidence)` equals the stencil evidence within relative 1e-10.
5. `suffix_posterior(T̃, Ẽ, π̃, tokens[:, :32], K)` for K ∈ {1, 2, 4, 8}, and on each 8-block, equals the BayesFilter window/block posterior within 1e-12 (abs, all 288 entries).
6. **Decimal reference.** `independent_reference.decimal_suffix_posterior(T̃, Ẽ, π̃, w_{1:32}, digits=80)` on 24 histories: the first 8 rows of each stratum, plus the 4 rows with the largest |logit π_32| among the first 2¹³ rows of each stratum (selection rule fixed now). All 288 entries agree with BayesFilter b_32 within 1e-12. The float64 arrays **are** the model, so the reference's `Decimal(float(x))` conversion is the correct one; D-1's rational-model Decimal trap does not apply (L G4.5).
7. No non-finite values and no negative probabilities anywhere.

### 5.5 G4: Monte Carlo validity

SE is the stratified standard error, √(¼(s_A²/n_A + s_B²/n_B)), of the per-row statistic or per-row difference; ε_H is the Hoeffding half-width of §6.3.
1. Î_1 ≤ 1e-14; every |π_1 − ½| ≤ 1e-14.
2. For k = 2, 3, 4: |Î_k − I_k| ≤ 4·SE and ≤ ε_H(I); |âcc_k − acc_k| ≤ 4·SE and ≤ ε_H(acc), against the exact G2 values.
3. **Stationarity (T3).** For k ∈ {2, 4, 8}: |Î^win_k − Î_k| ≤ 4·SE of the paired difference, and the same for âcc (max form).
4. Î_t and Î′_t agree within 4·SE of their paired difference, for t ∈ {4, 8, 16, 32}.
5. **Chain identity.** Σ_{s=1}^{31} î_{s+1} agrees with Î_32 within 4·SE of the paired difference.
6. **Monotonicity.** Î_{t+1} − Î_t ≥ −4·SE of the paired step difference, for t = 1..32.
7. **Calibration of the window posterior.** The credit form and the max form of âcc_8^win agree within 4·SE of their paired difference.

There are about 50 four-SE claims. If the implementation is correct, the chance of a false FAIL is at most about 50 × 6.3 × 10⁻⁵ ≈ 0.3% [W]. A G4 failure invokes S5: no increase of n, no reseed.

### 5.6 D: priority-1 decision criteria (P3, P4, A3; MD 2–3, A2–A3)

All decisions use the two-sided 99% normal interval (z = 2.576). There is no rerun, no change of n and no parameter change after results are seen.

| Id | Criterion | PASS | FAIL | Otherwise |
|---|---|---|---|---|
| **P3** | acc_32 − acc_8^win ≥ 0.10 (paired D3 at t*) | L99(D3) ≥ 0.10 | U99(D3) < 0.10 | THRESHOLD_INCONCLUSIVE |
| **P4** | I_8^win ≤ ½·I_32 (L's conservative form, separate bounds) | U99(I_8^win) ≤ ½·L99(I_32) | L99(I_8^win) > ½·U99(I_32) | THRESHOLD_INCONCLUSIVE |
| **A3** | acc_32 − acc_add (paired D_add at t*) | NONADDITIVE iff L99(D_add) ≥ 0.03 | — | ADDITIVE |

THRESHOLD_INCONCLUSIVE counts as not passed (L§5).

**Rationale (recorded).**
- P3: by T5, a later probe can show use of history older than 8 symbols only if acc_32 − acc_8 is clearly positive. With 4,096 held-out test histories a probe's SE is about 0.006–0.007 [W re-derived], so a 0.10 margin leaves room for an imperfect model (60% capture is still about 8.6 SE).
- P4: at least half of the component information at t* needs history older than 8 symbols.
- A3 margin 0.03 (MD 3, ratified before computation): set below the [H] twist gap of about 0.05–0.07 and above the [H] blur gap of ≲ 0.02.

**Bound robustness (descriptive).** For each of P3, P4 and A3, the report also states whether the label is unchanged when the 99% normal interval is replaced by the Hoeffding interval at δ = 0.01 (§6.3). A difference is reported as BOUND_SENSITIVE and never changes the label.

### 5.7 PH route (MD 7; reported, not in GO_P1)

The PH route is specified in §7. Its calibration results (K1–K3) and readings (Q1, Q2) are recorded with statuses PASS/FAIL/INVALID per item. A PH failure, timeout or exception affects **only** the PH outcome. It never affects the overall verdict, D or P5.

### 5.8 G5: controls

**Required (validity; any violation invokes S3):**

| Id | Criterion |
|---|---|
| N-iso | Exact I_k ≤ 1e-12 for k ≤ 4. Monte Carlo on 2¹⁶ rows: max over rows and t ≤ 33 of \|π_t − ½\| ≤ 1e-12 |
| N-same | Exact I_k ≤ 1e-15 for k ≤ 4 (identical arrays). Monte Carlo on 2¹⁴ rows: \|π_t − ½\| ≤ 1e-12 |
| N-id | Monte Carlo on 2¹³ rows: every 288-entry belief within 1e-15 of 1/288, and π ≡ ½ within 1e-15 |
| N-swap | On the first 2¹³ main rows of each stratum: the swapped-model π′ satisfies \|π′ − (1 − π)\| ≤ 1e-12 per row and t, and every Î and âcc on those rows is unchanged within 1e-12 |

**Descriptive (reported, never gating):**
- **N-local (A4, MD 5)**, the positive control for the additive mechanism. Exact I_1..I_4 and acc_1..acc_4. A Monte Carlo run of 2¹⁸ rows through the full D pipeline gives I_t, acc_t, acc_8^win, acc_add, I_add^LB, ρ_add, and the P3/P4/A3 statistics as values only.
  - **Pre-registered reading rule.** If U99(acc_32^N − acc_add^N) < 0.03, the control behaves as expected: the A3 tier labels a local-noise mechanism ADDITIVE. If L99(acc_32^N − acc_add^N) ≥ 0.03, the A3 tier does not separate local from long-timescale mechanisms at t = 32 in this setting, and any GO_P1_NONADDITIVE sentence must carry that qualifier (§1.4). Otherwise the control is INDETERMINATE and the report says so.
- **P-ref.** Exact I_1..I_4, plus a 2¹⁸-row Monte Carlo of I_t, acc_t and acc_add: how much component information the original X2a design exposed to short windows. Its beliefs feed Q1-spec (§7).
- **Noise floor.** `NullClouds.covariance_matched` surrogates of the panel-0 Q1-A and Q1-B clouds in the √b/√2 embedding, 20 draws each, Euclidean metric (equal to Hellinger in that embedding): β̂₁(B_PH) and S per draw. Context only (pilot rule).

### 5.9 Verdict semantics

**Overall validity verdict.**
- **PASS** ⟺ PF, S0 and G0–G5 (required controls) all pass.
- **FAIL** ⟺ S3 (G0–G3 or G5) or S5 (G4).
- **INVALID** ⟺ PF failure, S0 violation, S2, S7, an environment or import error, or a gate (or the D computation) that cannot be evaluated.

**Scientific outcome** (released only under overall PASS):

| Outcome | Condition | Meaning for a later trained stage |
|---|---|---|
| **GO_P1_NONADDITIVE** | P3 = PASS ∧ P4 = PASS ∧ L99(D_add) ≥ 0.03 | Informative for priority 1 at context 32, including evidence beyond a sum of 8-window evidence (T5 plus the A3 tier) |
| **GO_P1_ADDITIVE** | P3 = PASS ∧ P4 = PASS ∧ L99(D_add) < 0.03 | Informative for use of more than 8 symbols, but a model's gain could be explained by summing short-window evidence (E1) |
| **STOP_P1** | otherwise; the report gives the reason (which of P3, P4 FAILed or was THRESHOLD_INCONCLUSIVE) | Not informative for priority 1 on this construction. The curves are the finding. A STOP is a valid scientific outcome, **not** a FAIL |

**PH outcome** (separately, under overall PASS): Q1 ∈ {PASS, NON_SPECIFIC, FAIL, INVALID} and Q2 ∈ {SEPARATED_FULL_ONLY, SEPARATED_BOTH, NOT_SEPARATED, INVALID}. These are never combined with the GO_P1 labels (MD 7).

**Descriptive flags:** P5 flag (§4.3), N-local reading (§5.8), BOUND_SENSITIVE (§5.6), long-horizon reliability (§6.5).

A GO supports designing a later trained-stage protocol. It does **not** authorise training.

### 5.10 Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S0 | Protocol not frozen; request, protocol or commit mismatch; non-empty kernel diff (§5.1) | Do not run (INVALID) |
| PF | Preflight failure or inability to complete | INVALID; every gate NOT_RUN |
| S2 | Any builder or validation exception in G0 | INVALID; escalate. No metric switch, registry change or production edit |
| S3 | Any exact identity, tolerance, count or required-control criterion violated in G0, G1, G2, G3 or G5 | FAIL at the first failed criterion; remaining gates NOT_RUN (for G5: D and PH labels WITHHELD). Preserve the failing array or row. No post-hoc edit of a theorem or tolerance |
| S5 | A G4 criterion fails | FAIL of G4; D, PH and G5 NOT_RUN; escalate as a possible estimator or oracle defect. No increase of n, no reseed |
| S6 | The implementation needs a production change, a fourth module file, or a file over 400 lines (§8.1) | Stop and escalate before writing the code |
| S7 | Owner STOP, usage limits, or the disk thresholds (C: < 2 GB, X: < 30 GB) | INVALID (interrupted); resume only under the same frozen specification |
| S8 | A PH computation times out (`PHConfig.timeout_s` = 600), is CENSORED, or raises | The affected PH item is INVALID; the overall verdict and D are unaffected |

There is **no CPU ceiling** (owner B4, MD 8): CPU is measured only. Owner caps apply: at most 4 threads (this run uses 1), 12 GiB, one scientific task at a time. Because the pipeline is deterministic, a rerun after an environment-caused INVALID, under the same frozen specification and seeds, is legitimate and must reproduce identical values.

### 5.11 Threshold register (all fixed before any data)

| Item | Value |
|---|---|
| t*, k_s, window set | 32; 8; {1, 2, 4, 8} |
| P3 margin; P4 share; A3 margin | 0.10; ½; 0.03 |
| Decision interval | Two-sided 99% normal, z = 2.576; paired where stated |
| P5 flag | 0.01 nats (descriptive) |
| Tie tolerance (Lemma C) | 1e-12 |
| Main sample | n = 2²⁰ (2¹⁹ per component), 33 symbols |
| Control samples | N-iso 2¹⁶; N-same 2¹⁴; N-id 2¹³; N-swap 2¹⁴ main rows; P-ref 2¹⁸; N-local 2¹⁸ |
| Long horizon | 2¹⁶ rows × 128 symbols; t ∈ {32, 48, 64, 96, 128} |
| Hoeffding | δ = 1e-6 per reported quantity (validity); δ = 0.01 for the bound-robustness flag |
| Validity rule | 4·SE (G4) |
| Tolerances | G0: 1e-15. G1: abs 1e-15 / rel 1e-12; row sums 1e-14. G2: column sums 1e-12; T2 closed form 1e-14; Lemma U 1e-15; translations rel 1e-12; JS rel 1e-10. G3: beliefs 1e-12, π 1e-11, expit 1e-10, q 1e-12, evidence rel 1e-10, suffix 1e-12, Decimal 1e-12. G5: N-iso 1e-12, N-same 1e-15/1e-12, N-id 1e-15, N-swap 1e-12 |
| Decimal | 80 digits; 24 histories (selection rule in §5.4) |
| PH | ρ ∈ {0.75, 1.0, 1.25}; band search on [0, 0.99]; minimum plateau width 0.08; B_PH = central half; C-world: exactly two H1 bars with persistence ≥ 1.0 lattice units; M = 512; 8 panels; panel rule ≥ 7/8 (8/8 for PH controls); cluster-size filter ⌈0.05·M⌉ = 26 points; purity 0.95; H0 band (m, 1) wider than 0.05; surrogates 20 per cloud |
| Seeds | MASTER_X2A0 = 20261015; stream map in §6.2 |

---

## 6. Monte Carlo design

### 6.1 Samples and stratification

- **Main.** Exactly 2¹⁹ sequences of 33 symbols from each component, sampled by the unchanged `HMMSampler(T, E_c, u₁₄₄, SequenceLayout())` with one `sample(2**19, rng)` call per component. The component label is known by construction (exact stratification). Every estimator is the equal-weight mean over all 2²⁰ rows, which is unbiased for the ½/½ mixture expectation.
- **Controls:** the same procedure with the variant's E₂ (sizes in §5.11). N-swap reuses main rows and draws no new samples.
- **Rows are the independent units.** Positions within a row are not treated as independent.
- **Filtering.**
  - Full history: `BayesFilter(T̃, Ẽ, π̃).run(tokens)` in batches of 2,048 rows, in row order. It gives b_t and q_t for t = 1..33; π_t is the B-block mass, b_c the renormalised c-block, and q_c = b_c (T E_c).
  - Windows at t*: `BayesFilter(T̃, Ẽ, π̃).run(tokens[:, 32−k:32]).b[:, k−1]` for k ∈ {1, 2, 4, 8}.
  - Blocks: `run(tokens[:, 8(β−1):8β]).b[:, 7]` for β = 1, 2, 3. Block 4 is the k = 8 window.
  - Per row, only the statistics of §4.2 are retained, plus beliefs for the PH panel rows (§7.1).

### 6.2 Seed map (all from `SeedTree(20261015)`; recorded from `SeedTree.issued` in the report)

| Stream (name, *scope) | Use | Size |
|---|---|---|
| ("x2a0_mc", "main", "A"), ("x2a0_mc", "main", "B") | Main sample | 2¹⁹ each |
| ("x2a0_mc", "N-iso", c) | N-iso | 2¹⁵ each |
| ("x2a0_mc", "N-same", c) | N-same | 2¹³ each |
| ("x2a0_mc", "N-id", c) | N-id | 2¹² each |
| ("x2a0_mc", "P-ref", c) | P-ref | 2¹⁷ each |
| ("x2a0_mc", "N-local", c) | N-local | 2¹⁷ each |
| ("x2a0_long", c) | Long horizon, `SequenceLayout(n_obs=128)` | 2¹⁵ each |
| ("x2a0_null", c, draw) | Covariance-matched surrogates, draw = 0..19 | 512 points each |

Each generator feeds exactly one sampling call, so results do not depend on batching. Stage-0 histories are oracle-only. A later trained stage must use a different master seed and must not reuse these sequences (exposure rule; OQ7).

### 6.3 Uncertainty

- **SE** is the stratified standard error (§5.5). Every difference used in a gate or validity check is **paired**: computed per row on the same histories.
- **Hoeffding (validity and disclosure).** Each per-row statistic lies in a known range R: R = ln 2 for H_b-based quantities, R = ½ for max-form accuracies, R = 1 for credits and paired credit differences. The estimator is the mean of n = 2²⁰ independent (non-identically distributed) bounded variables, so
  ε_H = R·√(ln(2/δ)/(2n)). At δ = 1e-6: ε_H(I) = 1.823 × 10⁻³ nats, ε_H(acc) = 1.315 × 10⁻³, ε_H(credit difference) = 2.630 × 10⁻³ [W].
  (The analyst's 2.6 × 10⁻³ nats for I is the per-stratum bound with n = 2¹⁹. It is valid but conservative; see §10.2.)
  The bound is reported next to every Î and âcc. It is required in G4.2.
- **Bound robustness:** the Hoeffding interval at δ = 0.01 for D3, I_8, I_32 and D_add (§5.6).
- **Forecast precision [W]:** the per-row SDs are at most ≈ 0.35, so SE ≲ 3.4 × 10⁻⁴. The THRESHOLD_INCONCLUSIVE band around each gate threshold is therefore narrower than about ±10⁻³.

### 6.4 Cross-validation against exact values and references (summary)

| Reference | What it validates | Gate |
|---|---|---|
| Exact enumeration, k ≤ 4 | Sampler, filter and estimators (Î_k, âcc_k) | G4.2 |
| Closed forms T1, T2, Lemma U | Emission arrays and pair laws | G2 |
| Stencil filter (never forms T) | BayesFilter beliefs, π and evidence | G3.1, G3.4 |
| Per-component filters | Mixture π via log-evidence | G3.2 |
| `suffix_posterior` (unchanged) | Window and block posteriors; the tool used for the long horizon | G3.5 |
| Decimal reference, 80 digits | Float error of the filter, including extreme posteriors | G3.6 |
| Identities (T3 stationarity, increment chain, label-based Î′, credit vs max) | Internal consistency of the estimators | G4.3–G4.7 |

### 6.5 Long-horizon descriptive curve (A5, MD 6)

- 2¹⁶ sequences of 128 symbols (`HMMSampler` with `SequenceLayout(n_obs=128)`; the sampler reads only `n_obs`).
- The **unchanged** `tools/x4_oracle_profile/oracle_profile.suffix_posterior(T̃, Ẽ, π̃, tokens[:, :t], K=t)` at t ∈ {32, 48, 64, 96, 128}, plus the K = 8 window at t = 128. No new filter is introduced. BayesFilter stays capped at 33 symbols.
- Reported: Î_t, âcc_t, max(π, 1 − π) ≥ 0.9 and ≥ 0.99 fractions, and Î^win_8(128) against Î^win_8(32) (descriptive stationarity).
- Reliability checks (descriptive): the stencil filter on 2¹⁰ rows (π within 1e-10), and the Decimal reference on 4 histories of length 128 (all entries within 1e-10). A failure marks the curve UNRELIABLE and changes nothing else.
- Purpose: tell a later protocol what context length would be needed. Not gated.

---

## 7. PH route (MD 7: L's clouds and controls, X's in-space reference band)

### 7.1 Clouds (all fixed slices of existing samples; no extra sampling)

| Id | Points | Rows |
|---|---|---|
| Q1-A, Q1-B | b_c(h) at t* (Δ¹⁴³), h from component c | Panel p = 0..7: rows [512p, 512p + 512) of stratum c |
| Q1-spec | b_{B_P}(h) at t*, from the mixture A ⊔ B_P, h from B_P | P-ref stratum B_P, rows [512p, 512p + 512) |
| Q2-full | Mixture beliefs at t* (Δ²⁸⁷) | Rows [512p, 512p + 256) of each main stratum (256 + 256) |
| Q2-win | Window-8 mixture beliefs at t* (from w_25..w_32), same histories | As Q2-full |
| Q2-curve (descriptive) | Mixture beliefs at t ∈ {1, 2, 4, 8, 16, 24, 32}, same histories | As Q2-full |
| X¹ | Mixture belief with the block masses (1 − π, π) replaced by the true label: [b_A, 0] or [0, b_B] | As Q2-full |
| X^½ | Block masses replaced by (½, ½): [½b_A, ½b_B] | As Q2-full |
| N-iso cloud | N-iso mixture beliefs at t* | N-iso rows [256p, 256p + 256) of each stratum |
| N-id cloud | N-id mixture beliefs at t* | N-id rows [256p, 256p + 256) of each stratum |

### 7.2 Metric and estimator

- Hellinger distance (`topology.metrics.Hellinger`, ‖√p − √q‖₂/√2), the pilot's primary belief metric (L§4.3).
- `DistancePipeline(Hellinger(), pca_dims=None).compute(X, ids)` for distances and deduplication (≤ 1e-12). Cluster sizes count the original points via `dedup_map`.
- Vietoris–Rips over F₂: `PersistenceComputer(PHConfig(maxdim=1, coeff_p=2, threshold="auto"))` for H1 clouds and `maxdim=0` for H0-only clouds. `threshold="auto"` = max D, so every H1 bar closes. All clouds have ≤ 600 points and run in-process.
- **H1 reading:** β̂₁(B) := #{H1 bars with birth ≤ inf B and death ≥ sup B}, the bars that span the band.
- **H0 reading:** β̂₀(h) := the number of single-linkage clusters at height h (cut the MST edges longer than h; scipy `minimum_spanning_tree` + `connected_components`) with at least 26 points.
- Also stored: the full diagrams, S (`Summaries.S`), the top-3 persistences, and g₀ = d₍₁₎/d₍₂₎ (the two largest finite H0 deaths) against E[H_b(π_t)] (the EXTENSIONS §3 measure).

### 7.3 H1 scale band from X's reference families (K1; replaces L's C-syn)

For ρ ∈ {0.75, 1.0, 1.25}, the reference cloud R_ρ has 144 points q_z^(ρ)(s) ∝ exp(−spec.dist[z, s]²/2ρ²) (minimum-image flat torus distance, the same convention as E_A), one per lattice state z. These are known toroidal families of localised distributions in the same space as b_c (X§6.2). By Lemma P, the 288-coordinate pooled version adds nothing below Hellinger distance 1.
1. Compute each R_ρ's diagram (Hellinger, maxdim 1).
2. For each ρ, let S_ρ := {r ∈ [0, 0.99] : β₀(r) = 1 and β₁(r) = 2}, where β_k(r) = #{bars with b ≤ r < d}, evaluated exactly between consecutive diagram endpoints (`Summaries.betti_curve` at endpoint midpoints).
3. S := ∩_ρ S_ρ. Take its longest connected interval [l, u); on ties choose the smaller l.
4. Require u − l ≥ 0.08. Then B_PH := [l + (u − l)/4, u − (u − l)/4] (the central half; width ≥ 0.04).
5. If no interval qualifies, record CALIBRATION_INCONCLUSIVE: Q1 is INVALID. Do not choose another width, metric or rule.

**Forecast [W]** (continuous-Gaussian approximation; flat-VR torus classes assumed alive from the diagonal scale |Δ| = √2 until |Δ| = 4): H_ρ(√2) = 0.599, 0.470, 0.385 and H_ρ(4) = 0.986, 0.930, 0.850 for ρ = 0.75, 1.0, 1.25. So S ≈ [0.599, 0.850), width ≈ 0.25, and B_PH ≈ [0.66, 0.79]. The steady-state per-axis posterior SD of the exact filter is ≈ 0.78 lattice units [W, scalar Kalman approximation], inside the ρ range.

**K2 (C-world).** VR on `spec.dist` (144 points, lattice units) must have exactly two H1 bars with persistence ≥ 1.0. Forecast [W]: the two torus classes span [1, 4), because projection to the 12-cycle shows they survive below 4 and row triangles kill them at 4. The square cycles live on [1, √2), persistence 0.41. Failure makes Q1 INVALID.

**C-emis (descriptive; W).** The emission-row cloud {E_A[z]} (144 points in Δ³⁵) is reported with its diagram, β̂₁(B_PH) and the number of H1 bars with persistence ≥ 0.25·s (s = its `scale_s`). It is not a calibration requirement, because a band calibrated in belief space does not transfer to the 36-symbol simplex (§10.2).

### 7.4 H0 threshold from oracle clouds (K3; L's C-H0)

On each panel's X¹ and X^½ clouds, let m be the maximum over the 8 panels of: the largest finite H0 death of X^½, and the second-largest finite H0 death of X¹ (X¹'s largest is the cross merge at exactly 1, Lemma P). Require 1 − m > 0.05, then set h₀* := (m + 1)/2. Otherwise Q2 is INVALID.

### 7.5 Readings (≥ 7/8 panels)

| Id | Decision |
|---|---|
| Q1-A, Q1-B | β̂₁(B_PH) = 2 |
| Q1-spec | P-ref must **not** reach β̂₁(B_PH) = 2 in ≥ 7/8 panels |
| Q2-full | β̂₀(h₀*) = 2 with split purity ≥ 0.95 (both clusters ≥ 95% one label, and the labels differ) |
| Q2-win | β̂₀(h₀*) = 1 |
| Q2-curve | β̂₀, g₀ and purity per t (descriptive) |

**Outcomes.**
- Q1 = PASS ⟺ Q1-A, Q1-B and Q1-spec all hold. Q1 = NON_SPECIFIC ⟺ A and B pass but P-ref also reaches 2. Q1 = FAIL ⟺ otherwise. Q1 = INVALID ⟺ K1 or K2 fails, or a required Q1 cloud is censored or raises (S8).
- Q2 = SEPARATED_FULL_ONLY ⟺ Q2-full and Q2-win hold. Q2 = SEPARATED_BOTH ⟺ Q2-full holds and Q2-win fails. Q2 = NOT_SEPARATED ⟺ Q2-full fails. Q2 = INVALID ⟺ K3 or a PH control (§7.6) fails, or a required Q2 cloud is censored or raises.

### 7.6 PH-level null controls (required for PH validity only)

| Id | Requirement |
|---|---|
| N-iso cloud | β̂₀(h₀*) = 1 in 8/8 panels (isometric copy: π ≡ ½) |
| N-id cloud | Status COLLAPSED (all beliefs uniform) in 8/8 panels |
| X¹ | β̂₀(h₀*) = 2 with purity 1 in 8/8 panels (pipeline check) |
| P-ref | Specificity, through Q1-spec |
| Noise floor | Descriptive (§5.8) |

### 7.7 Pre-registered reading rule

- **Q1 = PASS:** "At the calibrated Hellinger band, exact world-conditional beliefs at t = 32 show two H1 classes in ≥ 7/8 panels for both components, and the P-world control does not": reproduced at the band. If any noise-floor surrogate also reaches β̂₁ = 2, the sentence adds "not distinguished from a covariance-matched Gaussian null at this band".
- **Q1 = NON_SPECIFIC:** the count does not discriminate smooth from P emission and is not interpreted as world H1.
- **Q1 = FAIL:** not reproduced at the band. This is a statement about the band and the estimator, not about the world.
- **Q2 = SEPARATED_FULL_ONLY:** full-history beliefs separate the components at the calibrated height while 8-window beliefs do not: the original X2a prediction holds with the window contrast that priority 1 requires.
- **Q2 = SEPARATED_BOTH:** separation is already available to 8-symbol windows, so PH separation is not evidence of long-history use.
- **Q2 = NOT_SEPARATED (forecast):** expected, because acc_32 < 1 leaves unconcentrated histories bridging the clouds. It is not evidence against long-history information, which D measures.
- The original X2a prediction ("β̂₀ = 2 at late positions") cannot by itself show long-history use; only the window contrast can.

---

## 8. Implementation footprint, reuse, cost and independence

### 8.1 Files and line budgets (planned split from the start; S6)

D-1 needed 735 lines in two files for a smaller scope, and its single-file plan blocked. This stage is planned as **three** module files from the start (OQ1):

| File | Contents | Budget |
|---|---|---|
| `tools/x2a_stage0/API.md` | Written contract, committed **before** any module code (D-1 pattern). Names every function, its inputs, outputs and report keys; changes no scientific choice; the protocol wins on conflict | — |
| `tools/x2a_stage0/x2a_model.py` | Constants and seed names; `_X2aTorusBuilder` and its validation; `e`, E_A, E_B and the variants (§2.6); mixture assembly; exact enumeration k ≤ 4 with the corrected JS; closed forms; stencil filter; gates G0, G1, G2 | ≤ 400 (≈ 330) |
| `tools/x2a_stage0/x2a_mc.py` | Seeded sampling; batched filter pass and per-row statistics; windows, blocks and the additive score; credits; SE, intervals and Hoeffding; G3, G4, D, G5 required controls; N-local, P-ref and the long horizon | ≤ 400 (≈ 380) |
| `tools/x2a_stage0/x2a_ph.py` | Reference band (K1), C-world (K2), C-H0 (K3); cloud assembly; β̂ readings; PH controls; surrogates; `s0_check`; `run(out_dir, preflight)`; report and NPZ writing (the `d1_seam_checks.run` pattern) | ≤ 400 (≈ 340) |
| `tests/x2a_stage0/test_x2a_stage0.py` (+ optional `test_x2a_stage0_ph.py`) | Independent tests (§8.4) | ≤ 400 each |
| `tests/x2a_stage0/AUTHORSHIP.md` | Independence record | — |

- No change to `src/`. No new sampler, production filter, runner, registered world, or generic table-emission mode.
- If any module file would exceed 400 lines, or a fourth module file is needed, stop and escalate (S6). Do not split silently.

### 8.2 Six-field reuse assessment (signatures verified at c364f95)

| Field | Assessment |
|---|---|
| **1. Existing functions and artefacts (used unchanged)** | **World:** `QuotientLatticeBuilder` (subclass with ClassVar `family`, `expected_betti`, `identifications`; `.build(WorldConfig) -> WorldSpec`), `Identification(axis, kind)`, `WorldConfig(family, dims, metric)`, `WorldSpec.validate()`, `CubicalComplex(n_vertices, cells)` (`betti`, `euler_characteristic`, `boundary_matrix`, `one_skeleton`), and the internals `world.complex.check_boundary_closed(cx)` and `world.metrics.check_flat_bounds(dist, dist_graph, n_axes)`, imported from `tools/` as D-1 does. **Process:** `TransitionBuilder().build(world, TransitionConfig(p_stay=0.2)) -> TransitionSpec(.T, .pi)`; `process.emission.draw_axis_permutation(world)` and `axis_state_perm(sx, sy, dims)` (module-level, not in `process.__all__`) for P-ref. **Dataset/contracts:** `HMMSampler(T, E, pi, layout).sample(n, rng) -> (tokens uint8 [n, n_obs], states)`; `SequenceLayout(n_obs=…)`; `SeedTree(master).generator(name, *scope)` and `.issued`. **Oracle:** `BayesFilter(T, E, pi).run(tokens) -> FilterResult(b, q, log_evidence, ce)` (P ≤ 33); `LastSymbolPosterior(T, E, pi).q_last(w)`; `context_gain(q_C, q_last)`. **Oracle profile:** `suffix_posterior(T, E, pi, tokens, K)` (any length, stationary restart, normalised output) and `validate_process(T, E, pi, tol)`. **Reference:** `tests/oracle_profile/independent_reference.decimal_suffix_posterior(T, E, pi, suffix, digits)` (≥ 60 digits, `Decimal(float(x))` inputs). **Topology:** `Hellinger`, `Euclidean`, `DistancePipeline(metric, pca_dims=None).compute(X, ids) -> DistanceResult(D, point_ids, dedup_map, scale_s, status)`, `PersistenceComputer(PHConfig(maxdim, coeff_p, threshold, timeout_s)).diagrams(D) -> DiagramResult(rows, status)`, `Summaries.S`, `.top_k_persistence`, `.betti_curve`, `NullClouds.covariance_matched(X, rng)`. **Meter:** the job-0014 meter, store-local binding, measure-only. **D-1 pattern:** local unregistered builder, explicit E array, API.md first, independent test file with AUTHORSHIP.md, mandatory preflight, S0 hashes and kernel diff, `report.json` + `model.npz`, split module files |
| **2. Genuinely missing capability** | A doubly periodic Gaussian emission array (`point_distances` wraps axis 0 only). The Dehn-twist and N-local variants. Disjoint-union assembly (not a builder family). Exact k ≤ 4 block-law JS enumeration. Monte Carlo MI and accuracy estimators with credits, paired SEs and Hoeffding bounds. The additive four-block score. A stencil reference filter (an independent numerical reference only; A5). The band rule for β̂₀ and β̂₁ and the reference families (new, because the pilot gated S, not counts) |
| **3. Smallest change** | The three module files and the test files of §8.1. Nothing in `src/` |
| **4. Stable interfaces and invariants** | Row vectors; `emit_then_transition`. State id 12x + y; mixture id 144·[B] + 12x + y; token id 6a + b. Ẽ = `vstack((E_A, E₂))` built once; T̃ = blockdiag(T, T); π̃ uniform and stationary. Gated sequences have 33 symbols (`check_tokens` max_len). float64, no epsilon. WORLD_REGISTRY untouched. `point_distances` and `is_x_periodic` never called. Seeds come only from `SeedTree(20261015)` |
| **5. Relevant regression checks** | Unchanged `tests/world`, `tests/process`, `tests/oracle`, `tests/oracle_profile`, `tests/topology`, `tests/dataset`. New tests (§8.4). `tools/check_file_sizes.py` |
| **6. Next plausible extension (no premature generalisation)** | After a GO: a separate trained-stage protocol reusing this module's construction. Promote a torus builder and a table-emission mode into `src/` only when that second consumer exists. For exact short-window blindness, X6 (abelian Z₂ transport suffices; Remark H), one at a time, with its own I_k curve |

`SyntheticShapes` (L's C-syn) is no longer used (MD 7).

### 8.3 Store, outputs and freeze bindings

- **Store** (on X:, per owner B4): `X:/Downloads/projects/topo-pilot/x2a-stage0-oracle-store/`. It did not exist on 2026-10-15.
  - `report.json`: verdict, gate statuses, every curve with SE and Hoeffding bound, D values and labels, P5 flag, PH summaries, seeds (`SeedTree.issued`), CPU, hashes;
  - `model.npz`: T, e, E_A, E_B, E_N, E_P, with sha256 hashes;
  - `ph_diagrams.npz`; `preflight.json`; the CPU ledger.
- **Freeze bindings** (S0):
  - base commit `c364f95e5573940cdc24b569b0fb7c6a16c97ab8` (main);
  - request SHA256 `4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595` (W checked it against the request file);
  - protocol SHA256, recorded in the freeze record (a protocol cannot contain its own hash);
  - MASTER_X2A0 = 20261015;
  - the module, test and store paths of §8.1 and §8.3.

### 8.4 Test-author independence requirement (D-1 pattern, binding)

- The test file(s) are written by an agent **other than the module author**, **after** the protocol is frozen and API.md is committed, and **before** the module exists.
- The author may read the frozen protocol, API.md, the production and reference code the tests call (§8.2 field 1), and `pyproject.toml`. The author must **not** read, list or search `tools/x2a_stage0/*.py`.
- The author executes nothing (no Python, no pytest). The worker runs the tests in PF.
- AUTHORSHIP.md records what was read, what was not read and what was executed, as in `tests/d1_seam/AUTHORSHIP.md`.
- Required tests, each with an independent reference that imports nothing from the module's kernels:
  1. E_A from an independent minimum-image 9-image 2-D softmax (and a negative test showing that a summed-image field differs by more than 1e-7 at d = 5.5);
  2. T from Fraction coordinate formulas; G0 counts and Betti numbers;
  3. T1 column sums and T2's closed form from an independently coded `e` (G(0), G(1), Δ_rep against the §3 values at 1e-5);
  4. an independent k = 2 and k = 3 enumeration of I_k and acc_k by explicit loops;
  5. the JS accumulation on toy laws, including disjoint point masses (must give ln 2: this catches the factor-2 error of §10.2 C1);
  6. Lemma C credits and the tie rule on hand-made posteriors;
  7. the additive score on a toy HMM with i.i.d. hidden states (every row of T equal to π), where blocks are conditionally independent and s_add must equal the full log-likelihood ratio;
  8. N-iso, N-same and N-swap identities on short histories;
  9. registry hygiene (WORLD_REGISTRY unchanged after import and run);
  10. guards (monkeypatch `process._geometry.point_distances` and `is_x_periodic` to raise);
  11. the band selector and β̂ readings on hand-made diagrams (plateau intersection, tie rule, the spanning rule, the 26-point filter);
  12. the verdict logic (P3/P4/A3 interval cases, including THRESHOLD_INCONCLUSIVE and the WITHHELD path).

### 8.5 Cost (forecast, not benchmarked; one thread, uncapped; MD 8)

| Part | Estimate |
|---|---|
| PF (regression suites, new tests, file sizes) | 3–6 min |
| G0–G2: build, kernels, k ≤ 4 enumeration for 5 second-block variants (level 3: 46,656 × 144² MAC each) | ≈ 1–2 min |
| Sampling: 2²⁰ × 33 main, ≈ 2¹⁹ × 33 controls, 2¹⁶ × 128 long | 3–5 min |
| Main BayesFilter, full history: 2²⁰ rows × 33 steps × 288² ≈ 2.9 × 10¹² MAC | 4–8 min |
| Windows (k = 1, 2, 4, 8) and blocks 1–3: 39 steps × 2²⁰ × 288² ≈ 3.4 × 10¹² MAC | 4–8 min |
| G3: stencil, per-component filters and `suffix_posterior` on 2¹⁴ rows; Decimal on 24 × 32 steps × 288² operations at 80 digits | 3–5 min |
| G5 and descriptive Monte Carlo: P-ref and N-local (each ≈ ¼ of main), N-iso, N-same, N-id | 4–8 min |
| Long horizon: 2¹⁶ × 368 steps × 288² ≈ 2.0 × 10¹² MAC, plus checks | 2–4 min |
| PH: 3 reference clouds and C-world (144 points), ≈ 64 H1 clouds and ≈ 120 H0 clouds at ≤ 512 points | 3–8 min |
| **Total** | **≈ 30–45 CPU-min (range 25–75)** |

- Memory is below 2 GB. A BayesFilter batch of 2,048 × 33 × 288 doubles is about 156 MB; the level-3 enumeration about 54 MB per component; retained PH beliefs about 150 MB.
- Threads are pinned to 1 (`OMP_NUM_THREADS = MKL_NUM_THREADS = OPENBLAS_NUM_THREADS = 1`). Total process-tree CPU is metered.
- The dense 288² products waste the block-diagonal zeros (a factor of 2); this is accepted to keep the oracle unchanged (reuse-first).

---

## 9. Risks and open questions

### 9.1 Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | Too little information beyond 8 symbols at t* (STOP_P1) | A valid scoped finding. Follow-ups need a new protocol (OQ8); no rerun |
| R2 | A3 straddles 0.03 | The default label is the conservative GO_P1_ADDITIVE; the values and the bound-robustness flag are reported |
| R3 | acc_add computed as E[max(π_add, ·)] (biased, since π_add is uncalibrated) | Lemma A/C; credit estimator; test 7 |
| R4 | JS accumulated with the factor-2 error of L§4.1 | Corrected formula (§4.1); test 5; G4.2 compares exact against Monte Carlo |
| R5 | Spurious float failures at tight tolerances | Tolerances set from float-error bounds (§10.2 C13); the 4-SE family has a ≈ 0.3% false-FAIL budget |
| R6 | PH band empty, or the C-world forecast wrong | Q1 becomes INVALID; GO_P1 is unaffected (MD 7) |
| R7 | `point_distances` / `is_x_periodic` trap | Explicit array; guard tests |
| R8 | Registry pollution | Unregistered builder; registry-hygiene test |
| R9 | Code exceeds 400 lines per file | Three files planned with budgets; S6 |
| R10 | B-block indexing error (rows of E_B indexed by z, not u = φz) | G1.4 bitwise check; Lemma U check G2.3 |
| R11 | Stage-0 sequences silently reused as a trained-stage test set | Seed-map record; exposure rule (§6.2, OQ7) |
| R12 | Overclaim: circular coordinate, blindness, or forecasts as findings | MD 9 caveats in every licensed sentence (§1.4) |
| R13 | P-ref reaches β̂₁ = 2, contradicting E1 | Q1 = NON_SPECIFIC, reported; no reinterpretation |
| R14 | The N-local control also shows a large non-additive gap | Pre-registered reading rule (§5.8) adds a qualifier |
| R15 | Self-assessed readiness | Status is REVIEW_READY; MD 10 Codex review with re-derivation before freeze |

### 9.2 Open questions (for the coordinator and the MD 10 review)

1. **Three module files (OQ1).** The instruction suggests planning two. W plans three (§8.1) because the scope (exact enumeration, Monte Carlo, the additive tier, five variants, PH calibration and readings) exceeds D-1's 735 lines over two files. Ratify three, or name what to cut.
2. **Writer-introduced estimators (OQ2).** Ratify the Lemma C credit form for acc_8^win and acc_add (gate statistics), I_add^LB in place of "I_add", and the tie rule (1e-12).
3. **Tolerances (OQ3).** N-iso and N-swap were loosened from L's 1e-15 to 1e-12, and G1 row sums to 1e-14, on float-error grounds (§10.2 C13). Ratify.
4. **P4 form (OQ4).** L's conservative separate-bounds form is kept as the gate (A2, "L's 99%-interval rule"); the paired form is descriptive. Confirm.
5. **PH calibration details (OQ5).** C-emis demoted to descriptive; C-world uses an absolute rule (two bars with persistence ≥ 1.0 lattice units); the reference kernel uses minimum-image `spec.dist` rather than X's wrapped kernel. Ratify.
6. **Control sample sizes and Decimal selection (OQ6).** The sizes in §5.11 and the 24-history Decimal set (including 8 extreme-posterior rows) are W's choices. Ratify.
7. **Exposure (OQ7).** Should stage-0 seeds be entered in an exposure or seed registry? This protocol records them and forbids reuse by a trained stage.
8. **Follow-ups after STOP_P1 (OQ8; owner or coordinator choice; each a new protocol):** a stronger twist s = 2 (vertical move (2, 1): Σ_B = [[2.0, 0.8], [0.8, 0.4]], det 0.16, KL per resolved displacement 2 nats [re-derived by W]); σ = 0.75; or a longer context guided by the t ≤ 128 curve.
9. **X6 next (OQ9).** If the owner's target is exact short-window blindness, X6 (abelian Z₂ transport suffices) is the next one-at-a-time stage 0 and needs its own I_k curve (Remark H).
10. **Independent review (MD 10).** Codex re-derives T1–T7, Lemma U, Lemmas R, C, A, P, Proposition N, the [W] values (§2.3, T2, Proposition N, Hoeffding, forecasts) and the corrections of §10.2 before freeze.

---

## 10. Changelog: sources and corrections

### 10.1 Section sources

| Section | Source |
|---|---|
| §1 question, scope | RQ; L§1; AN §2.5 (competing explanations E1/E2); X§2 (explanation table format) |
| §1.4 licence | L§8; MD 9 caveats (verbatim in substance); AN §4 charter caveat; A3 wording |
| §2 construction | L§2 (MD 1); A1 minimum image; AN §1.4 L6 (smoothness note); X§3.5 → N-local (A4) |
| §3 T1–T7, Lemma U | L§3, re-derived and completed by W (T4 ergodicity, T5 randomised f, T6 kernel invariance) |
| §3 Lemma R | L§4.2 / AN §1.1 (restart exactness), stated as a lemma by W |
| §3 Lemmas C, A, P; Proposition N | W (C, P); AN §2.5 and A3 (A); AN §1.3 and X§3.6–3.8 adapted to L's field and dynamics (N) |
| §3 Remark H | L Remark/OQ5 reworded per A1 and AN §2.6; X6 facts checked in `docs/proposals/X6_TOPOLOGICAL_INVARIANTS.md` |
| §4 quantities | L§4.1–4.2; A3 additive baseline; A2 P5; X§7.5 (window predictive gain); AN §2.3 forecasts |
| §5 gates | L§5–6 restructured in the requested order; MD 2–3; A2–A4; D-1 PF ruling 8 and S0 pattern |
| §6 Monte Carlo | L§4.2; A5 (MD 6); X§5.3 seed-namespace idea |
| §7 PH | L§4.3 clouds, controls, panel rule; X§6.2 reference families and band rule (MD 7); X§6.6 surrogates (descriptive) |
| §8 footprint | L§7; D-1 OUTPUTS_0020 and AUTHORSHIP; code at c364f95 |

### 10.2 Corrections and clarifications (every item re-checked by W)

| # | Item | Change |
|---|---|---|
| C1 | **L§4.1 JS accumulation formula (error found by W).** L wrote "½(P_A + P_B)·[(1+r)log1p(r) + (1−r)log1p(−r)]" summed over h. That sum equals **2·JS**: for disjoint point masses it gives 2 ln 2 instead of ln 2. | Corrected to I_k = Σ_h ¼(P_A + P_B)[(1+r)ln(1+r) + (1−r)ln(1−r)] = Σ M·φ(r), with a small-r series (§4.1); test 5 |
| C2 | G1 compared against summed images (ambiguous) | Minimum over the 9 images (A1, MD 4); re-derived: the summed form differs by ≈ 8.6e-7 at d = 5.5 |
| C3 | Base commit (L OQ1 said c364f95 was not on main) | main @ c364f95 (A1, MD 4); W confirmed that `git rev-parse HEAD` on main is c364f95e… |
| C4 | L Remark/OQ5: "this class always leaks at k = 2"; "non-abelian X6" | Proved only for the twist; generic otherwise; abelian holonomy suffices; X6 is not automatically 8-blind (A1, MD 4) |
| C5 | L P5 gated | Descriptive with a flag (A2, MD 2) |
| C6 | L outcomes GO_P1_PH and PH_NOT_P1 | Removed; the PH outcome is reported separately (MD 7) |
| C7 | A3 "acc_add" (unspecified estimator) | Classification accuracy via Lemma C credits; E[max(π_add, ·)] would be biased because π_add is uncalibrated (W) |
| C8 | A3 "I_add" | ln 2 − E[H_b(π_add)] is not a mutual information; replaced by the Rao–Blackwellised cross-entropy lower bound I_add^LB (W) |
| C9 | L: the stencil filter was the only filter beyond 33 symbols | Unchanged `suffix_posterior` for t ≤ 128; stencil is a reference only (A5, MD 6) |
| C10 | L C-syn (Euclidean synthetic shapes) set τ₁* | X's in-space reference families set an absolute Hellinger band (MD 7). Reference kernel on minimum-image `spec.dist` for consistency with E_A (W) |
| C11 | L C-emis at τ₁* | Descriptive; the belief-space band does not transfer to Δ³⁵ (W) |
| C12 | L C-world at τ₁* (τ₁* no longer exists) | Absolute rule: exactly two H1 bars with persistence ≥ 1.0 lattice units (W) |
| C13 | L tolerances 1e-15 for N-swap and N-iso | 1e-12: a 288-term float dot product has worst-case relative error ≈ 287u ≈ 3e-14 per step, so 1e-15 over 33 steps risks spurious failures. G1 row sums 1e-14 for the same reason (36-term sums) (W) |
| C14 | Hoeffding values | L's "≤ 3e-3" and AN's "2.6e-3 nats" are the per-stratum bound (n = 2¹⁹), valid but conservative. The pooled bound for the stratified mean is 1.823e-3 at δ = 1e-6 (W) |
| C15 | Hand-value rounding (L, AN) | p(0.5) = 0.589233 (L 0.589230); p(1.5) = 0.310698 (L 0.310699); G(0) = 0.902705 (L 0.902700); G(1) = 0.769235 (L 0.769233); P_A(rep) = 0.179622 (AN 0.179621); P_B(rep) = 0.169355 (L 0.16935, AN 0.169354). Δ_rep = 0.010267 and the JS bound 9.15e-5 nats are confirmed. **No claim is affected** |
| C16 | AN s² "= 1.5625" | 1.56246 (approximately equal; forecast input only) |
| C17 | L's T2 notation used "a" for both the move probability and a symbol coordinate | Move probability renamed α = 1/5 |
| C18 | T4 limit proof (L sketch) | Completed: pair-chain mixing, Birkhoff singularity, Lévy convergence |
| C19 | X's t = 512 gates, 64-claim simultaneous Hoeffding, p_stay ½, integer centres, wrapped Gaussian | Not adopted (MD 1–2). X's blur is kept as N-local on L's field and dynamics (A4); its reference band and surrogate idea are kept (MD 7) |
| C20 | Cost (L ≈ 25 min; X 2–6 h) | ≈ 30–45 CPU-min (MD 8); X's estimate was overstated (AN §1.4 X5) |
| C21 | Gate order | Restructured to the requested order, with execution order and sealing rules explicit (§5.0) |
| C22 | Module files (L: two) | Three, planned from the start (§8.1; OQ1) |
| C23 | Q2 cluster-size filter "≥ 0.05·M" | Made exact: ⌈0.05 × 512⌉ = 26 original points (counted through `dedup_map`) |
| C24 | Analyst forecasts | Recorded as forecasts (§4.4), never gates (MD 9) |
| C25 | N-local hand values (absent from every input) | Derived by W: S_A = 0.0707764, S_N = 0.0573220, repeat 0.179622 versus 0.145669 |
