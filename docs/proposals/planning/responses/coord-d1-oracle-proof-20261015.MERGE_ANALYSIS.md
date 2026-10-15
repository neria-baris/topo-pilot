# D-1 oracle proof: merge analysis of track X (Codex) and track L (Claude)

This is a clean-context comparison for the coordinator. It is read-only: I ran no Python and opened no scientific data. Every number below was recomputed by hand.

**Inputs**
- The request `planning/requests/coord-d1-oracle-proof-20261015.md`.
- X = `coord-d1-oracle-proof-20261015.codex.md`, cited as X§n.
- L = `coord-d1-oracle-proof-20261015.claude.md`, cited as L§n.

**Code checked** at topo-pilot main @4f219d6:
- `world/{lattice,metrics,registry,identification,config}.py`;
- `process/{transition,_geometry}.py`;
- `oracle/{_common,_filter,_futures}.py`;
- `dataset/sampler.py`;
- `contracts/_schemas_world.py` (TransitionSpec);
- `analysis/x4f_scores.py::kl_rows`;
- `tests/oracle_profile/independent_reference.py`;
- `tests/world/test_world.py` (the flipped/Klein fixture).

**Bottom line**
- Both main theorems are correct, and every exact witness value I recomputed is correct.
- Neither plan has a mathematical error. The defects are minor: one statistical margin is overstated, a few sentences are overbroad, and X overclaims "no open choice".
- **X** is the simpler and more auditable existence proof. It alone gives a *reachable* pair of histories that differ only in the world posterior. The request defines the distinction as that posterior, so this is the witness the request literally asks for.
- **L** supplies the general theory that X lacks:
  - a gap formula valid on the whole decision phase;
  - a common-support lemma;
  - the holonomy coupling, which proves non-degeneracy and makes "topological" precise.
- **Recommendation:** freeze X's 4×3 construction, with L's theorems ported to it (§7), L's controls, and exhaustive exact enumeration in place of L's sampled stage. L's 12×12 is recorded as the candidate for a later downstream study.

---

## 1. Synopses

**X**
- **World.** Z ∈ {C, M}, prior ½. The lattice is 4×3: x is glued, y is not. M glues (3,y)~(0,2−y).
- **Walk.** The existing lazy max-degree walk with p_stay = 1/5, so a = 1/5 and the x-hold probability is c = 3/5.
- **Band.** B = {2,3,0}, an asymmetric band whose interior I = {3} is adjacent to the seam. The outside region is column 1 only.
- **Alphabet.** (σ0, σ2, σ3, A, B), with V = 5.
- **Outside emission.** Column 1 emits A with probability 3/4, 1/2, 1/4 at y = 0, 1, 2.
- **Start.** Fixed at (1,0) in both worlds, which is non-stationary. There are 24 mixture states.
- **Witnesses.**
  - h* = (A,σ2,σ3): two-step TV = 1/50 for both the joint and the distant-symbol marginal.
  - Pair h_A / h_B, 11 symbols each: identical coordinate beliefs, posteriors 1/4 and 3/4, pair TV = 1/100.
  - h_edge: one-step TV = 1/10, showing the band edge.
- **Checks.** Exact rationals, the float oracle and four controls. There is no sampling.

**L**
- **World.** F ∈ {C, M}, prior ½. The lattice is 12×12, and M glues (11,y)~(0,11−y).
- **Walk.** The same walk, with a = 1/5.
- **Band.** B = {10,11,0,1}, with interior {11,0}. The outside region is O = {2..9}.
- **Alphabet and emission.** V = 16. Outside, the emission is x-blind: it reads y with Ẽ = (3/4)I + (1/48)J.
- **Start.** Uniform. There are 288 mixture states.
- **Theory.**
  - Lemma 0: common support.
  - Lemma 1: x-autonomy.
  - Theorem 1: horizon-1 identity on the decision phase H_int.
  - Theorem 2: TV₂ = a²(1−ε)·TV(ρ_C, ρ_M) for every h ∈ H_int.
  - Theorem 3: holonomy coupling.
  - A chain identity with X's sufficiency lemma.
- **Witnesses.** W2 (TV₂ = 9/400), W3 (first gap at horizon 3, TV₃ = 9/2000), h_inf (π = 7/122, TV₂ = 333/20125) and the band edge (9/80).
- **Checks.** Gates G0 to G4, including 16,384 sampled sequences and null and positive controls.

## 2. Hand verification

### 2.1 X (all claims recomputed)

**Structure**
- 12 states, 20 edges (9 horizontal, 3 seam, 8 vertical) and 8 squares, so χ = 0.
- Degree is 3 on rows y = 0 and y = 2, and 4 on row y = 1. D_max = 4.
- The builder's `_wrap` maps (4,y) to (0, n_y−1−y) = (0, 2−y), which matches X§3.2.
- With n_y = 3, the M seam contains exactly one straight edge, at y = 1. So `is_x_periodic` finds 1 of 3 wrap edges and raises INVALID_GLUE. X's warning in §3.5 is correct.
- Both metrics pass `check_flat_bounds`: only deck copies with k ∈ {−1, 0, 1} can attain the L1 minimum.

**x-autonomy.** At a boundary row, the x-hold probability is 2/5 + 1/5 = 3/5. At y = 1 it is 1/5 + 2/5 = 3/5. ✓

**Theorem 1.** From column 3, the next column is 2, 3 or 0 with probabilities a, c, a. All three are band columns, so the next-symbol law is (σ0, σ2, σ3, A, B) = (1/5, 1/5, 3/5, 0, 0) for every y and both worlds. ✓

**Theorem 2 at h***
- P(h*) = (3/4)a² = 3/100 in each world. S_3 = (3,0) in both worlds, and π = ½.
- Rows of J_C:

  | First symbol | Entries | Row sum |
  |---|---|---|
  | σ0 | (ac, 0, a², a²·3/4, a²·1/4) = (3/25, 0, 1/25, 3/100, 1/100) | 1/5 |
  | σ2 | (0, 3/25, 1/25, 3/100, 1/100) | 1/5 |
  | σ3 | (ca, ca, c², 0, 0) = (3/25, 3/25, 9/25, 0, 0) | 3/5 |

- J_M differs only in the σ0 row: there, (A, B) = (1/100, 3/100), because (0,2) steps to (1,2). This matches X§5 entrywise.
- TV(J) = ½(2/100 + 2/100) = 1/50 = a²/2. ✓
- Q₂,C = (6/25, 6/25, 11/25, 3/50, 1/50) and Q₂,M = (…, 1/25, 1/25), so TV = 1/50. ✓

**Pair h_A / h_B**
- The x path is 1,2,3,0,1,2,3,0,1,2,3: ten x-moves and two seam crossings. M has y = 2 at the middle visit to column 1 and y = 0 at the end.
- Likelihoods: P(h_A | C) = (3/4)³a¹⁰ = 27/64·a¹⁰ and P(h_A | M) = 9/64·a¹⁰, so ρ = 1/4. For h_B the two likelihoods swap, so ρ = 3/4.
- P(h_r) = ½·(36/64)·a¹⁰ = 9/32·a¹⁰ = 9/312,500,000 = 2.88e-8. ✓
- Q₂(h_A) has (A, B) = (3/4)(3/50) + (1/4)(1/25) = 11/200 and 5/200.
- Q₂(h_B) has (A, B) = 9/200 and 7/200.
- Pair TV = (1/2)(1/50) = 1/100. The merged-predictor bound 1/200 follows from the triangle inequality. ✓

**h_edge.** At the endpoint, C has y = 0 and M has y = 2. The one-step TV is a·½(|3/4 − 1/4| + |1/4 − 3/4|) = a/2 = 1/10. ✓

**Other claims**
- P(X_3 = 3) = 2a², via 1→2→3 and 1→0→3. ✓
- The scaling (1−p)²/32. ✓
- The likelihood-ratio bound 3^{±m}. ✓
- Stationary P(A) = 1/8. ✓

**Extra values for the record (analyst-derived; must be independently re-derived)**
- At h*: KL(J_C‖J_M) = (1/50)·ln 3 ≈ 0.02197 nats.
- At h*: I(Z; W_{t+1:t+2} | h*) = ln(27/16)/100 ≈ 0.00523 nats. The next-symbol mutual information is 0.

### 2.2 L (all claims recomputed)

**Structure**
- 144 states, 276 edges (144 x-edges and 132 y-edges) and 132 squares, so χ = 0.
- R(y) = 11 − y has no fixed row. It is an automorphism of both C and M.
- The degree-3 subgraph is two 12-cycles in C and one 24-cycle in M. ✓
- Flat bounds: a k = ±2 copy shifts x by 24, so its L1 distance is at least 13 + |Δy|, which exceeds the k = 0 distance. L§3.7 is therefore correct. ✓

**Lemma 1, Lemma 0 and Theorem 1.** All correct. Lemma 0 uses the fact that Ẽ has full support (ε > 0) and that the x-path law is world-free.

**Theorem 2**
- From x₀ ∈ {11, 0}, the only two-step path into O is 0→1→2 (respectively 11→10→9), and it uses no seam edge.
- So the exit slice is a²·ρ_f·Ẽ.
- (ρ_C − ρ_M)·J = 0, hence TV₂ = a²(1−ε)·TV(ρ_C, ρ_M) ≤ 3/100. ✓
- The KL formula, the mixture slope and the Pinsker bound 2π(1−π)TV² are all correct.

**Theorem 3 (coupling Ψ)**
- Correct. Off-seam steps commute with R because R preserves degree and the boundary self-loops. Seam steps map to M-seam edges.
- c(h) is a function of h, because both seam columns are band columns that pin x.
- Note: Ψ is the identity at s = 1, so the coupling needs only *equal* initial laws in the two worlds, not R-invariant ones. This is what lets it port to X's fixed start (§7).

**W2**
- Pr_f = (1/144)·a³·Σ_y e_y(η_{y0}) = a³/144 = 1/18000. Summed over the 24 histories this gives 1/750.
- ρ_C = (37/48)δ_{y0} + (1/48) elsewhere, and TV(ρ_C, Rρ_C) = 36/48 = 3/4.
- TV₂ = (1/25)(3/4)(3/4) = 9/400. ✓
- ρ_C·Ẽ = (9/16)δ_{y0} + 7/192, so A = 115/192 and u = 7/192.
- KL = a²(A − u)·ln(A/u) = (9/400)·ln(115/7) ≈ 0.06298. ✓
- I = a²[A·ln(2A/(A+u)) + u·ln(2u/(A+u))] = (1/25)[0.37979 − 0.07893] = 0.01203. ✓

**Band edge.** 9/80 = a(1−ε)², and the chain identity 9/400 = a·9/80 holds. ✓

**W3**
- c = 0, so b_M = b_C and TV₂ = 0.
- The only three-step path that is η-emitting and crosses the seam is 11→0→1→2, because the prefix (β0, β1) forces it.
- TV₃ = a³(1−ε)·(3/4) = 9/2000. ✓

**h_inf**
- The x path is 9,10,11,0,1,2,1,0, which is 7 x-moves.
- C likelihood: Σ_y e_y(η)² = (1369 + 11)/2304 = 115/192.
- M likelihood: Σ_y e_y(η)·e_{11−y}(η) = (74 + 10)/2304 = 7/192.
- Hence π = 7/122.
- ρ_C′ = 1369/1380 at y₀ and 1/1380 elsewhere. ρ_M′ = 37/84 at y₀ and at 11−y₀, and 1/84 elsewhere.
- TV(ρ_C′, ρ_M′) = 9583/9660 − 4255/9660 = 5328/9660 = 444/805.
- TV₂ = (1/25)(3/4)(444/805) = 333/20125. ✓

**Frequencies.** The frequency of H_int is 1/6 at every t (uniform stationary x). About 655 W2 occurrences are expected (30 positions × 16,384 / 750). ✓

## 3. Errors found

### X
- **X1 (overclaim).** "No scientific construction choice remains open" (X Open questions). This is not true:
  - The meaning of "topological distinction" is a true owner question (§8).
  - The non-stationary fixed start is a substantive modelling choice. X's own open questions ask the reviewer to accept it.
- **X2 (omission, not error).** X proves the gap only at its witnesses.
  - It gives no formula over all of 𝓗_I.
  - It gives no theorem that the world bit enters only through holonomy. §11.4 asserts this informally ("only world-dependent operation is the seam gluing").
  - Both results are true for X's lattice (§7.2).
- **X3 (provenance label).** It cites the repo as "topo-pilot-circle-history-k4". The hash matches main @4f219d6, so this is harmless.

### L
- **L1 (overstated margin, G3(g)).** L claims ">10 sequence-clustered SE". I computed the variance of the H_int occupancy over 33 steps by spectral decomposition, using the κ eigenvalues 0.6 + 0.4·cos(2πk/12) and the weights cos²(πk/12)/36.
  - Var(S) ≈ 48.9, so the per-sequence SD is ≈ 0.21 and the SE is ≈ 0.0017.
  - The tolerance 0.01 is therefore ≈ 6 SE, not more than 10. The gate is still safe (p ≈ 1e-9), but the stated margin is wrong.
- **L2 (overbroad wording, Theorem 3(b)).** "No statistic of outside-only segments carries information about F" is true only for a segment's *own* law, under the stationary start. Jointly with earlier history, an outside segment at odd parity is exactly where F appears. The theorem statement itself, "only through odd outside observations", is correct.
- **L3 (overstatement, open question 2).** L says Theorems 1–3 "hold unchanged" for a pilot-like Gaussian outside emission.
  - Theorems 1 and 3 do hold.
  - Theorem 2(iii)'s factor (1−ε) depends on A4, which a Gaussian overlap violates. The formula would become a²·TV(ρ_C·E_{x*}, ρ_M·E_{x*}).
- **L4 (ambiguity).** "Expect about 540,000 positions" refers to all positions (16,384 × 33). H_int has about 90,000.
- **Both (certificate gap).** "χ = 0 with non-empty boundary implies annulus or Möbius" presupposes that the complex is a 2-manifold with boundary.
  - Neither plan gates the manifold condition: every edge lies in 1 or 2 squares, and every vertex link is an arc or a circle.
  - A cheap direct w₁ test is also available, and the merged design adds it: either a sign vector s with ∂₂s supported on boundary edges exists, or it does not.

**Code claims.** All the code claims I checked are accurate:
- `as_model` accepts a π with zeros, so X's point-mass start is valid in BayesFilter, HMMSampler and the Decimal reference.
- `TransitionSpec.validate` enforces πT = π, so X is right to keep π_start separate.
- `_as_decimal` keeps Decimal inputs as they are and converts every other value through float. L's "pass Decimals made at prec ≥ 60" is right, and X's "binary values" caveat is right.
- `FutureOperator._beliefs` requires row sums within 1e-10.
- F2 checks its first-symbol marginal at 1e-12.
- In `observability_matrices`, G_j is blocked by the first symbol, so L's index s₁V² + s₂V + s₃ is right.
- `check_tokens` max_len is 33.
- `kl_rows` lives in `analysis.x4f_scores`, and `validate_process` does not exist.
- The existing flipped test is the 4×4 Klein bottle. The unglued-y Möbius path is untested in both plans.

## 4. Degeneracy check

| Question | X | L |
|---|---|---|
| World-conditional laws undefined (zero likelihood in one world)? | **No.** The column-1 rows have full support on {A, B}, and the x-path law is world-free (same kernel and same start), so supports are common (X§11.3). | **No.** Lemma 0, from ε > 0. L correctly notes that ε = 0 would break this. |
| Identifiable from x-path or band statistics? | **No.** The projected x-chain and every band emission are world-free. | **No** (Theorem 3). |
| Identifiable from outside-band statistics? | **Only via holonomy, but with one subtlety.** The start fixes a y-frame, so the *single-time marginal* of an outside symbol differs between worlds. For example, P(W_5 = A) differs by 2a⁴·(1/2) = 1/625, through the hidden winding paths 1→2→3→0→1 and 1→0→3→2→1. This is topology-mediated and vanishes under the cylinder-seam control, so it is not a label leak. Still, a population outside-symbol statistic is world-dependent. X§11.4 acknowledges this only obliquely. | **Cleaner.** Under the uniform start, every window's own law is world-free unless the window contains an odd outside observation (Theorem 3 with stationarity). |
| Is the posterior ever trivially 0 or 1? | No. The likelihood ratio is within 3^{±m}. | No. It is bounded by ((1−ε+ε/12)/(ε/12))^{±m}. |
| Does the gap trivialise? | No. The gap needs a seam crossing between a y-reference and a readout. | Same. |

Neither plan is degenerate. L's stationary start makes the non-degeneracy statement stronger and simpler. After the port in §7.2, X's non-degeneracy is equally provable; the only difference is that the start acts as an even-parity observation at time 0.

## 5. Conflicts

| Topic | X | L | Better, and why |
|---|---|---|---|
| Lattice size; closeness to pilot | 4×3, 24 states | 12×12, 288 states (pilot dims, p_stay and length 33) | **X for D-1.** The request says "prefer the simplest", and every array is hand-checkable. L is closer to the pilot, but that matters only for a downstream test that both plans say would be retuned anyway. |
| Emission in the band | One symbol per column, deterministic | Same | Tie. |
| Emission outside the band | One column; A/B read y at 3/4, 1/2, 1/4. The middle row is reflection-fixed. | 8 x-blind columns; noisy 12-way y-readout (37/48, 1/48) | **X for exactness** (two outcomes, a literal 12×5 array, as the request asks). L's A4 structure gives a cleaner general formula, but X admits an equally clean one (§7.2). |
| Noise ε | Implicit; rows strictly inside (0,1) | ε = 1/4, frozen with a rationale | **L's explicit rationale** (Lemma 0) should be adopted as the stated reason for X's rows. |
| World-bit formulation | Z, prior ½, mixture diag(T_C, T_M), fixed start | F, prior ½, block-diagonal mixture, uniform start | Tie on formulation. **On the start law, L is cleaner** (stationary, πT = π, sampler default). X's fixed start is what buys the posterior-isolation pair. **Keep X's**, with L-style disclosure. |
| Decision phase | Ends in σ3 (I = {3}); one-step neighbours in B | Ends in β11/β0; frequency 1/6 for every t | Both are precise and correct. L states the frequency. For X it depends on t (e.g. 0.08 at t = 3, 1/4 stationary); the merged design must report it per t. |
| Proof technique | Row identity plus explicit path sums at witnesses | General lemmas, the Theorem 2 formula on all of H_int, the coupling Ψ, and the X-lemma chain identity | **L.** It proves the gap and non-degeneracy for every history, not only for witnesses. Port it to X (§7.2). |
| Witness set | h* (1/50); h_A/h_B (posterior-only, 1/100); h_edge (1/10) | W2 (9/400), W3 (horizon 3), h_inf (π = 7/122), band edge (9/80) | **X's h_A/h_B is decisive.** It is a *reachable* pair with identical coordinate beliefs that differs only in ρ. The request defines the distinction as the posterior, and L can show this only counterfactually (Theorem 2(iv)). L's W3 has no direct analogue on a 4-column lattice; drop it (L itself marks it optional). |
| Gates and tolerances | Exact equality; float 1e-12; evidence rel 1e-10; log-evidence 1e-10; 4 controls; NOT_COMPLETED status | G0–G4; Fraction equality; float 1e-12; π 1e-11; Decimal 1e-45 with Decimal inputs; sampled identity checks; null and positive controls | **Merge.** Use X's tolerances, add L's π and Decimal rules, and use L's control set. Replace L's sampled G3 with exhaustive exact enumeration, which is feasible only at X's size. |
| New code; reuse correctness | Fixture, unregistered local Möbius builder validated explicitly, check entry and independent rational reference | One module plus a test file; `d1_mobius` registered globally on import | **X on registry hygiene.** The existing tests register and then pop. Both reuse lists are accurate (§3). |
| Orientability certificate | Betti numbers over GF(2)/GF(3); boundary graph 2 cycles vs 1 | The same, plus the edge symmetric difference, degree multisets and χ | **L**, plus the manifold check and the direct w₁ sign test that both omit. |
| Cost | Under 300 CPU-s (forecast) | About 5 CPU-min, ceiling 20 | Both trivial. X has no sampled histories and so no exposure-registry entry. |
| Licence and non-claims | Narrow claim; no pilot, B2 or H1 claim; a trained model may retain Z | The same, plus: not transplantable to square vs cylinder; Transformer vs recurrent framing; orientability (w₁) named | **L** on substance. Its claim "Local statistics cannot identify it" needs Theorem 3, which the port provides. |

## 6. Unique catches

**X only**
1. A reachable posterior-isolation pair (identical b_C, b_M and coordinate beliefs; ρ = 1/4 vs 3/4), with the merged-representation lower bound 1/200.
2. An asymmetric band that puts the seam on the decision column's two-step exit. The gap therefore arises from a *future* crossing at uninformed histories (π = ½, b_C = b_M). The common witness has probability 0.03.
3. The full normative 5×5 J_C/J_M arrays, and both horizons reported (joint F2 vs distant marginal bT²E), with a cancellation warning (§11.5).
4. `TransitionSpec.pi` must stay stationary, so π_start is passed only to BayesFilter.
5. `is_x_periodic` raises on a partial wrap for odd n_y.
6. Controls: a reflection-fixed start y = 1, and a symmetric readout.
7. NOT_COMPLETED is distinct from FAIL. Critical tests are to be authored before production code by an independent author.

**L only**
1. Lemma 0 (common support) and the ε = 0 failure mode.
2. Lemma 1's dependence on max-degree normalisation: a degree-normalised walk breaks x-autonomy.
3. The Theorem 2 formula on all of H_int, plus KL and mutual information.
4. The holonomy coupling: F enters only through odd outside observations (w₁).
5. The chain identity TV₂(h) = a·TV₁(hβ†): where the gap lives, under X's lemma.
6. Band dwell blurs the gap and never creates one (R-equivariant column kernel).
7. Non-transplantability to square vs cylinder: an x-reader sees the square's x-boundary at horizon 1.
8. Downstream framing: a Transformer need not carry the bit at H_int, because it can re-read the context.
9. Controls: the null C⊕C, the local-leak positive control, and the band-too-narrow control.
10. Decimal inputs must be passed as Decimal objects. The meaning of "topological" is raised as an owner question.

## 7. Recommended merged D-1

### 7.1 Construction: X's, frozen as written

- dims (4,3); x glued; y unglued.
- M: `Identification(0, "flipped", flip_axis=1)` in a fixture-local `QuotientLatticeBuilder` subclass. It is not registered globally. It is validated explicitly, mirroring `build_world`: `spec.validate`, `check_boundary_closed`, flat bounds. **Reason:** registry hygiene; the existing tests pop test families after use.
- C: `CylinderBuilder`.
- T: `TransitionBuilder(p_stay=0.2)`, so a = 1/5 and c = 3/5.
- B = {2,3,0}, decision column I = {3}.
- Alphabet (σ0, σ2, σ3, A, B), with the literal 12×5 array E from X§3.5, used identically in both blocks. **Reason:** the request asks for a literal array.
- π_start = δ(1,0) in each world; Z prior ½. Passed to BayesFilter, HMMSampler and the reference, and **never** to TransitionSpec. **Reason:** this enables the posterior-isolation pair, which is the request's own definition of the distinction.
- Disclosure: per-t single-symbol marginals are world-dependent through hidden windings (§4).
- State the rationale for full-support readout rows as L's Lemma 0.

### 7.2 Theorems: X's, plus L's theory ported (analyst-derived; must be re-derived independently)

**Theorem 1 (X).** For every h ending in σ3, the next-symbol law is (1/5, 1/5, 3/5, 0, 0).

**Lemma 0 (L, ported).**
- Supports are common, so 0 < ρ(h) < 1 at every reachable h.
- Reason: the x-path law is world-free, and the column-1 rows have full support.

**Theorem 3 (L, ported).**
- With R(y) = 2 − y and seam parity c(h) = parity of consecutive σ3/σ0 pairs, Pr_M(h) equals the C-likelihood with the column-1 rows reflected at odd-parity times.
- For uninformed h: ρ(h) = ½ and b_M = R^c·b_C.
- Validity: Ψ is the identity at s = 1, and R is a degree-preserving automorphism off the seam. Both hold here.

**General gap on 𝓗_I (new; replaces witness-only proofs).**
- Let δ_f = ρ_f(0) − ρ_f(2). Then (ρE₁)(A) = ½ + δ/4.
- Only the (σ2, ·) and (σ0, ·) slices differ. M's σ0 slice uses Rρ_M, so:
  - TV(J_C, J_M) = (a²/4)(|δ_C − δ_M| + |δ_C + δ_M|) = **(a²/2)·max(|δ_C|, |δ_M|)**;
  - TV(Q₂,C, Q₂,M) = **(a²/2)·|δ_C|**, because Q₂,M is always (a²/2, a²/2) on {A, B}.
- At uninformed h both equal (a²/2)|δ_C|.
- Check at h*: δ = 1 gives 1/50 ✓.
- Mixture pair: TV = |Δρ|·TV(J_C, J_M). At h_A/h_B this gives 1/100 ✓.

**L's chain identity.** TV₂(h) = a·[TV₁(h·σ2) + TV₁(h·σ0)]. It replaces L's single-exit version, because X's interior has two exits.

### 7.3 Witnesses (exact; all verified in §2.1)

- h*: J_C/J_M arrays, TV 1/50, KL (1/50)·ln 3, mutual information ln(27/16)/100.
- h_A/h_B: ρ = 1/4 and 3/4, P = 9/32·a¹⁰, pair TV 1/100, Q₂ values as in X§6.
- h_edge: TV₁ = 1/10.
- Add one informed decision-phase witness whose b_C ≠ b_M, to exercise the max(|δ_C|, |δ_M|) branch. The coordinator picks one, e.g. h_A extended by (σ0, A, σ2, σ3), and its values are derived by the independent reference author before implementation.

### 7.4 Checks

**G0: structure.**
- 12 states, 20 edges and 8 faces; degrees; Betti numbers over GF(2) and GF(3).
- Boundary graph: two 4-cycles in C, one 8-cycle in M.
- Edge symmetric difference: exactly the 3 + 3 seam edges.
- **Manifold check:** every edge lies in 1 or 2 squares.
- **Direct w₁:** C admits a sign vector s with ∂₂s supported on the boundary edges; M admits none.
- E_C = E_M bitwise.

**G1: exact kernel identities (Fraction).**
- x-autonomy, Theorem 1 for all six rows, both F2 slices, and the R-equivariance of T off the seam.

**G2: exhaustive exact enumeration.**
- Enumerate *every* positive-probability history up to length K = 8 by depth-first forward recursion in Fractions. The upper bound is 3⁷·2⁸ ≈ 5.6e5 leaves, in practice of order 10⁴. It replaces L's 16,384-sample stage and needs no exposure registry.
- At every node, assert:
  - common support;
  - ρ = ½ and b_M = R^c·b_C when uninformed;
  - at σ3 endpoints, ΔQ₁ = 0 and the §7.2 TV formulas.

**G3: witnesses against the float oracle.**
- BayesFilter (mixture and per-world), F1, F2, and the distant marginal.
- Tolerances:
  - float 1e-12 absolute;
  - π 1e-11;
  - evidence 1e-10 relative;
  - `decimal_suffix_posterior` with Decimal inputs at prec ≥ 60 against Fraction, 1e-45.

**G4: controls.**
- Cylinder seam: gaps vanish.
- Symmetric readout: gaps vanish.
- Start y = 1: witness gaps vanish.
- h_edge one-step TV = 1/10.
- **Local leak:** reflect the column-1 rows of the M block only. Then ρ ≠ ½ already at the uninformed history (A), with likelihood 3/4 vs 1/4. G0 and G2 must flag it.
- **Narrow interior:** make column 2 y-revealing. Then G1's Theorem 1 identity must fail.

**Verdicts.** PASS, FAIL or NOT_COMPLETED, as in X§8.8. PASS requires the posterior-isolation pair.

### 7.5 Footprint, licence and record

**Footprint**
- One fixture/check module and one independently authored rational reference plus tests.
- No change to world, process, oracle or dataset.
- Cost: under 5 CPU-min with 1 thread.

**Licence.** Use X§12 wording, plus L's clause: "the bit affects the likelihood only through odd-parity outside observations (w₁ holonomy)".

**Non-claims.** Add L§4.3 in full: pilot, B2/D-055, H1, trained models, and square vs cylinder not transplantable. Add L's Transformer caveat to the downstream list.

**Record.** Record L's 12×12 construction (L§1–2, with L1–L3 corrected) as the named starting point for any downstream trained-model protocol. It is not frozen or run now.

## 8. Open questions

### True owner questions
- **O1. What does "topological distinction" (B3-D) mean?**
  - D-1 delivers orientability (w₁; equal Betti numbers; cylinder vs Möbius).
  - If the owner meant β₁ (square vs cylinder) or the pilot's own distinction, D-1 does not answer it, and a different gadget is needed (L§4.3).
  - Only the owner can say whether an orientability existence result discharges item D.
- **O2. What follows a PASS?** Whether it should lead to a trained-model D-1 test, and whether that test should be at pilot scale, is a programme decision.

### Coordinator- or reviewer-settleable
- **C1. Base lattice.** 4×3 (recommended) vs 12×12.
- **C2. Start law.** Fixed δ(1,0), recommended because it enables the posterior-isolation pair, vs uniform.
- **C3. What "necessary" means.** World-conditional gap only, or a reachable posterior-isolation pair as well? Settle this from the request text: it defines the distinction as the posterior. Recommend requiring the pair.
- **C4.** The enumeration depth K (8 proposed). Replace sampling with enumeration.
- **C5.** The choice of the informed-witness extension in §7.3, and its frozen values.
- **C6.** Registry handling (unregistered builder, recommended), the module location (tools/ vs `src/topo_pilot/experiment`), and the output store.
- **C7.** The W3/horizon-3 witness: drop it. L marks it optional, and a width-4 analogue is not straightforward.
- **C8.** The reviewer order, and adoption of the §7.2 formulas only after independent re-derivation. They are analyst-derived here and have not been checked by a second party.
