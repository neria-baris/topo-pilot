STATUS: FREEZE_READY (self-assessed; the owner-mandated independent review, Codex first, is still required before any freeze)

# D-1: cylinder versus Möbius with a y-blind seam band. Oracle-only proof and check (Claude planning track L)

Request: `planning/requests/coord-d1-oracle-proof-20261015.md`. Repository read at main @4f219d6. Planning only: nothing was executed. Every number below was derived by hand and is stated in exact closed form. The check in §3 recomputes all of them.

## Summary (≤ 300 words)

**Construction.** One HMM with a hidden world bit F, prior ½. F glues a 12×12 lattice along x periodically (cylinder C, existing builder) or with the flip (11,y)~(0,11−y) (Möbius M, a five-line subclass). Both worlds use the existing lazy max-degree walk with p_stay = 1/5, so each x-move has probability a = 1/5. The band B = {10,11,0,1} emits β_x: x exactly, nothing about y. Outside it, η_y has probability 37/48 and each other η 1/48 (V = 16); one explicit array E serves both worlds. The 288-state mixture uses the existing oracle unchanged.

**Theorems.**
- On the decision phase H_int (histories ending in β_11/β_0; 1/6 of positions), Q₁(h, C) = Q₁(h, M) exactly, for every h.
- For every h in H_int, the two-step TV gap equals a²(1−ε)·TV(ρ_C, ρ_M), where ρ_f is the y-belief in world f.
- The reachable witness (η_y0, β_10, β_11, β_0) has π = ½, TV₂ = 9/400 and KL₂ = (9/400)·ln(115/7) ≈ 0.063 nats. Mutual information with F: 0 for the next symbol, ≈ 0.012 nats for the next two.
- An even-parity witness first differs at horizon 3.
- A path coupling shows that F changes the likelihood only after an odd number of net seam crossings, which is the Z₂ orientation holonomy. Local statistics therefore cannot identify the bit.
- X's sufficiency lemma explains why the claim is scoped to a phase: the gap at h equals the band-edge one-step gap, discounted by a.

**Check.**
- Exact Fraction identities that imply the theorems for every history.
- Exact witnesses, with Decimal and float cross-checks.
- 16,384 sampled sequences, checked row by row.
- Null and positive controls.
- About 5 CPU-minutes.

**Scope.** The distinction is orientability (w₁): the Betti numbers are equal. A PASS says nothing about the square/cylinder pilot, about B2, about H1 or about trained models.

---

## 0. Request item map

| Request item | Section |
|---|---|
| 1 Exact construction (lattice, band, rows, alphabet, explicit E, one process with a hidden bit) | §1 |
| 2 Theorem and proof; reachable phase via X's lemma; edge cases | §2 (Thms 1–4, §2.7 phase, §2.8 edge cases) |
| 3 Oracle-only verification (reuse, new code, six fields, tolerances, exact cross-check, cost, PASS/FAIL) | §3 |
| 4 What a PASS licenses; what is not claimed about the pilot | §4 |
| 5 Risks and mitigations | §5 |
| Corrections to the round-1 L sketch | §6 |

---

## 1. Exact construction (frozen objects)

### 1.1 Worlds

| Object | Value |
|---|---|
| Chart | x ∈ Z₁₂ (axis 0, glued), y ∈ {0,…,11} (axis 1, not glued). State id z = 12x + y (the world module's vertex order, `check_state_order`). N = 144 per world. |
| World C | `CylinderBuilder`, family `"cylinder"`, `Identification(0, "periodic")`. Seam edges (11,y)–(0,y). |
| World M | New subclass `D1MobiusBuilder(QuotientLatticeBuilder)`, family `"d1_mobius"`, `identifications = (Identification(0, "flipped", flip_axis=1),)`, `expected_betti = {2: (1,1,0), 3: (1,1,0)}`. Seam edges (11,y)–(0,11−y) (the `Identification` docstring convention). |
| Off-seam structure | Identical in both worlds: x-edges (x,y)–(x+1,y) for x ≠ 11, and y-edges (x,y)–(x,y+1). There are 276 edges and 132 squares in each world, so χ = 144 − 276 + 132 = 0. |
| Reflection | R(y) = 11 − y; (Rρ)(y) := ρ(11−y). n_y = 12 is even, so R fixes no row. |
| Metric | `WorldConfig(dims=(12,12), metric="flat")` for both. D-1 never uses `dist`; the field exists only because `build_world` validates it. |

### 1.2 Transitions (existing kernel, unchanged)

`TransitionBuilder().build(world, TransitionConfig(p_stay=0.2))` gives the following for each world f:
- T_f[z,z′] = a for each graph neighbour;
- T_f[z,z] = 1 − deg(z)·a;
- a := (1 − p)/D_max = (1 − 1/5)/4 = **1/5**, with D_max = 4 in both worlds;
- deg = 4 for y ∈ {1..10} and deg = 3 for y ∈ {0, 11}, in both worlds;
- π_f uniform (1/144).

The exact reference uses p = Fraction(1,5). The float `T_f` agrees entrywise within 1e-15 (gate G1).

### 1.3 Alphabet and emission (explicit array, identical rows by construction)

Band B = {10, 11, 0, 1}; band interior B° = {11, 0}; outside O = {2,…,9}.

| Symbol | Id | Emitted by |
|---|---|---|
| η_y, y = 0..11 | y | states with x ∈ O |
| β_10, β_11, β_0, β_1 | 12, 13, 14, 15 | x = 10, 11, 0, 1 respectively |

V = 16. The array is built once, from the chart, with no call to `process` emission builders or `_geometry.point_distances`:

```
E = zeros((144, 16))                       # float64; an exact twin uses Fraction
BETA = {10: 12, 11: 13, 0: 14, 1: 15}
for x in range(12):
    for y in range(12):
        z = 12 * x + y
        if x in BETA:                        # band: reveals x exactly, nothing about y
            E[z, BETA[x]] = 1
        else:                                # outside: reads y with noise, ignores x
            E[z, 0:12] = eps / 12            # = 1/48
            E[z, y]    = 1 - eps + eps / 12  # = 37/48
```

**Frozen parameter values:**
- ε = **1/4**.
- Write e_y for row y of the 12×12 outside block Ẽ = (1−ε)I + (ε/12)J. Ẽ is doubly stochastic: Σ_y e_y(η_y′) = 1.
- Stationary symbol frequencies: each β has frequency 1/12 and each η has 1/18.

**Conditions the proofs use** (§2 is stated for any E satisfying them):
- **(A1)** band rows: E((x,y),·) = δ_{β_x} for x ∈ B;
- **(A2)** outside rows are supported on the η symbols and are the **same array** in both worlds;
- **(A3)** outside rows have full support on the η symbols, which holds because ε > 0;
- **(A4)** gap condition: (ρ − ρ′)Ẽ = (1−ε)(ρ − ρ′) for distributions ρ, ρ′ on y, with 1 − ε > 0.

### 1.4 One process with a hidden world bit

- **State:** (F, z), N = 288.
- **Kernels:** T_mix = blockdiag(T_C, T_M), E_mix = vstack(E, E) (the same source array), π_mix = 1/288 everywhere.
- **Sampling:** this is F ~ Bernoulli(½), fixed for the whole sequence, followed by the world-F walk with "emit, then transition" (the oracle's event order). It is an ordinary HMM, so `BayesFilter`, `FutureOperator` and `HMMSampler` apply unchanged.

**Notation.**
- h = w_{1:t}; Pr_f(h) := Pr(h | F = f).
- b_f(h) ∈ Δ(Z): the filtered belief over z_t given h and F = f.
- ρ_f(h) ∈ Δ({0..11}): its y-marginal.
- π(h) := Pr(F = M | h).
- Q_k(h, f): the law of (w_{t+1}, …, w_{t+k}) given h and F = f.
- Q_k(h) = (1 − π)Q_k(h, C) + πQ_k(h, M): the Bayes predictive of the mixture.
- TV(P, Q) = ½Σ|P − Q|. Logarithms are natural.

The "topological distinction" is F. At a history h it enters the predictor in two ways:
1. through the posterior π(h);
2. through the world-conditional beliefs b_f(h).

---

## 2. Theorems and proofs

### 2.1 Basic lemmas

**Lemma 1 (x-autonomy).** For f ∈ {C, M} and every state z = (x, y):
- Σ_{z′ in column x+1} T_f[z,z′] = a;
- Σ_{z′ in column x−1} T_f[z,z′] = a;
- Σ_{z′ in column x} T_f[z,z′] = 1 − 2a.

So the column process x_t is a Markov chain with kernel κ: κ(x, x±1) = a and κ(x, x) = 1 − 2a. κ is the same in both worlds and does not depend on y.

*Proof.* In both worlds, (x, y) has exactly one neighbour in column x+1 and exactly one in column x−1. In M at x = 11, that neighbour is (0, 11 − y). Each neighbour carries mass a = (1 − p)/D_max. Every other transition (a y-move, or the self-loop) stays in column x. At the boundary rows y ∈ {0, 11}, the missing y-neighbour's mass a is added to the self-loop, which also stays in column x. ∎

This is where the lazy max-degree normalisation matters: Lemma 1 holds for every p ∈ [0, 1). A degree-normalised walk would give x-moves probability 1/3 at boundary rows and 1/4 elsewhere, and Lemma 1 would fail.

**Lemma 2 (band readout).** If w_t = β_x, then z_t lies in column x almost surely. If w_t is an η symbol, then z_t ∈ O. *(This is A1 plus A2: the band and outside alphabets are disjoint.)*

**Lemma 0 (common support).** For every finite string h, Pr_C(h) > 0 ⟺ Pr_M(h) > 0. Hence, whenever Pr(h) > 0, both Q_k(h, f) are defined and 0 < π(h) < 1.

*Proof.*
1. Let X(h) be the set of column sequences ξ_{1:t} such that:
   - |ξ_{s+1} − ξ_s| ≤ 1 (mod 12);
   - ξ_s = x when w_s = β_x;
   - ξ_s ∈ O when w_s is an η symbol.

   X(h) does not depend on the world.
2. If X(h) = ∅, every state path is incompatible with h (Lemma 2 and the light cone), so Pr_f(h) = 0.
3. If ξ ∈ X(h), then:
   - Pr_f(x_{1:t} = ξ) = (1/12)·Π κ(ξ_s, ξ_{s+1}) > 0, by Lemma 1, the uniform start, and 1 − 2a = (1+p)/2 > 0;
   - conditional on x_{1:t} = ξ, the emission likelihood is at least (ε/12)^{#η in h} > 0, using A1 and A3.

   So Pr_f(h) > 0 in both worlds. ∎

With ε = 0 (exact y-readout), Lemma 0 fails: one world can rule a history out. This is why ε > 0 is frozen.

### 2.2 Theorem 1: horizon-1 irrelevance on the band interior

**Definition (decision phase).** H_int := {h = w_{1:t} : Pr(h) > 0, w_t ∈ {β_11, β_0}}, for any t ≥ 1. For h ∈ H_int, write x₀ = x(w_t) ∈ {11, 0}.

**Theorem 1.** For every h ∈ H_int and f ∈ {C, M}:

  Q₁(h, f) = ν_{x₀} := a·δ_{β_{x₀−1}} + (1 − 2a)·δ_{β_{x₀}} + a·δ_{β_{x₀+1}}.

Hence:
- Q₁(h, C) = Q₁(h, M) = Q₁(h) = ν_{x₀};
- I(F; W_{t+1} | H = h) = 0;
- Q₁(h) does not depend on π(h), on b_C(h) or on b_M(h).

Concretely:
- ν_11 = (β_10: 1/5, β_11: 3/5, β_0: 1/5);
- ν_0 = (β_11: 1/5, β_0: 3/5, β_1: 1/5).

**Matrix form, which is what is checked.** For both f, every row of T_f E indexed by a state in column 11 equals ν_11, and every such row in column 0 equals ν_0.

*Proof.*
1. By Lemma 2, b_f(h) is supported on column x₀.
2. By Lemma 1, starting from any (x₀, y), x_{t+1} = x₀ − 1, x₀ or x₀ + 1 with probabilities a, 1 − 2a and a.
3. All three columns lie in B, because x₀ ∈ B° = {11, 0}.
4. So w_{t+1} = β_{x_{t+1}} deterministically (A1).
5. Therefore b_f(h)·T_f·E = ν_{x₀} for every belief supported on column x₀.

The mixture predictive is a convex combination of two equal vectors. ∎

**Remark (honest strength).** On H_int the last symbol alone is one-step sufficient. Not only F, but every other part of the history (including ρ) is irrelevant at horizon 1. What makes F special is §2.3: F changes the two-step law at the same h.

### 2.3 Theorem 2: exact horizon-2 law and gap

For h ∈ H_int, define the exit column and the intermediate band symbol:
- x* = 2 and β† = β_1 if x₀ = 0;
- x* = 9 and β† = β_10 if x₀ = 11.

**Theorem 2.** For every h ∈ H_int and f:
- **(i) Band block.** For band symbols w, w′: Q₂(h, f)[w, w′] = Σ κ(x₀, i)·κ(i, j) over the column pairs (i, j) with β_i = w and β_j = w′. This does not depend on f or on h beyond x₀.
- **(ii) Exit slice.** Q₂(h, f)[β†, η_{y′}] = a²·(ρ_f(h)·Ẽ)(y′). Every other entry that contains an η symbol is 0.
- **(iii) Gaps.**
  - TV(Q₂(h, C), Q₂(h, M)) = a²·TV(ρ_C Ẽ, ρ_M Ẽ) = a²(1−ε)·TV(ρ_C(h), ρ_M(h)) ≤ a²(1−ε) = 3/100.
  - KL(Q₂(h, C) ‖ Q₂(h, M)) = a²·KL(ρ_C Ẽ ‖ ρ_M Ẽ).
- **(iv) Mixture.** Q₂(h) = Q₂(h, C) + π(h)·(Q₂(h, M) − Q₂(h, C)).
  - Replace π(h) by any π′ while keeping b_C and b_M. Then Q₁ is unchanged, and TV(Q₂^{π′}, Q₂) = |π′ − π(h)|·TV(Q₂(h, C), Q₂(h, M)).
  - Also I(F; W_{t+1:t+2} | h) ≥ 2π(1−π)·TV(Q₂(h, C), Q₂(h, M))², by Pinsker applied to π·KL(Q_M ‖ Q̄) + (1−π)·KL(Q_C ‖ Q̄).

*Proof.*
1. Two steps from x₀ ∈ B°, the column path either stays in B or is the single path x₀ → x† → x*, where x† is the band-edge column next to x*. The steps 0→1→2 and 11→10→9 both use only off-seam x-edges.
2. **(i)** Band-only column paths have world-free probabilities (Lemma 1), and their symbols depend only on the columns (A1).
3. **(ii)** The exit path consists of two x-moves. An x-move leaves y unchanged, and each has probability a regardless of y and f (Lemma 1). So Pr(x_{t+2} = x*, y_{t+2} = y | h, f) = a²·ρ_f(h)(y), and state (x*, y) then emits according to e_y (A2). The symbol β† occurs before an η only on this path.
4. **(iii)**
   - The band blocks are equal, so the TV and KL sums run over the exit slice only.
   - (ρ_C − ρ_M)·Ẽ = (1−ε)(ρ_C − ρ_M), because (ρ_C − ρ_M)·J = 0 (A4).
5. **(iv)** This is linearity in π. Q₁ is independent of π by Theorem 1. The Pinsker bound is the standard decomposition of the mutual information with a binary F. ∎

The 2-step exit does not cross the seam. The whole difference between ρ_C(h) and ρ_M(h) is created by the past, through the world-specific filter. §2.4 says exactly how.

### 2.4 Theorem 3: holonomy coupling (non-degeneracy; F is identifiable only through topology)

**Seam parity.** c(h) := #{s < t : {w_s, w_{s+1}} = {β_11, β_0}} mod 2.
- A seam crossing is a step 11↔0. Both endpoints are band columns, so the crossing is visible as consecutive β_11/β_0 symbols.
- Conversely, consecutive β_11, β_0 (in either order) force a crossing.
- So c is a function of h.

An index s is an **odd outside observation** if w_s is an η symbol and c(w_{1:s}) = 1. A history is **uninformed** if it has no odd outside observation.

**Theorem 3.**
- **(a)** For uninformed h:
  - Pr_M(h) = Pr_C(h), hence π(h) = ½ exactly;
  - b_M(h)(x, y) = b_C(h)(x, R^{c(h)} y), so ρ_M(h) = R^{c(h)} ρ_C(h).
- **(b)** For every h: Pr_M(h) equals the probability of h under a modified world-C process. In that process, the emission at each odd outside time s is replaced by E∘(id × R), so state (x, y) emits like (x, 11 − y).

  Consequently F changes the likelihood only through odd outside observations. In particular:
  - no statistic of outside-only segments carries information about F;
  - no statistic of band x-paths carries information about F;
  - no history without a net seam transit followed by an outside observation carries information about F.

*Proof.*
1. **Coupling map.** For a world-C state path ζ = (x_s, y_s)_{s≤t}, let c_s(ζ) be the parity of the number of seam crossings before time s. Define Ψ(ζ)_s := (x_s, R^{c_s(ζ)} y_s).
2. **Ψ maps C-paths bijectively onto M-paths and preserves π(z₁)·Π T.**
   - At s = 1, c = 0, and the initial law is uniform in both worlds.
   - Off-seam C-step (x, y) → (x′, y′), meaning an x-move with x ≠ 11↔0, a y-move, or a stay. The M-step is (x, R^c y) → (x′, R^c y′), with T_M[(x, R^c y), (x′, R^c y′)] = T_C[(x, y), (x′, y′)]. This holds because T_M = T_C off the seam and R is an automorphism of the off-seam graph that preserves degrees: it swaps the boundary rows 0 ↔ 11.
   - Seam C-step (11, y) → (0, y). The M-step is (11, R^c y) → (0, R^{c+1} y) = (0, 11 − R^c y), which is an M-seam edge, so both have probability a. The step 0 → 11 is symmetric.
   - The inverse map unfolds an M-path in the same way.
3. **Band times.** The emission depends only on x, which Ψ preserves.
4. **Outside times.** Seam crossings happen only between consecutive band times, and the band times pin x (Lemma 2). So c_s(ζ) = c(w_{1:s}) for every path ζ consistent with h. At an outside time, the M-path emits from (x_s, R^{c(w_{1:s})} y_s).
5. Summing over ζ gives (b). For uninformed h, every outside emission factor coincides, so the likelihoods are equal. Reading off the time-t marginal under Ψ gives the belief relation in (a). ∎

**Topological reading.**
- O is a contractible 8×12 rectangle, on which the outside emission fixes a global y-frame. The band is y-blind.
- Close a band path from column 9 to column 2 by a path back through O. The resulting loop γ has winding number ≡ c (mod 2) around the core circle.
- The y-frame transported around γ comes back reflected exactly when w₁(γ) ≠ 0: never in C (orientable), and iff the winding is odd in M (non-orientable).
- Theorem 3 therefore says that F is revealed only by observations that close odd-winding loops. Equivalently, the orientation character w₁ of the world is the only channel.
- C and M have the same Betti numbers over every field, because both are homotopy equivalent to S¹. They are distinguished by orientability, equivalently by their number of boundary circles (2 versus 1). They are not isomorphic as graphs: the induced subgraph on degree-3 vertices is two 12-cycles in C and one 24-cycle in M.

### 2.5 Witnesses (exact, reachable)

All values below follow from Theorems 2 and 3 with a = 1/5 and ε = 1/4. The check reproduces each one in Fractions (§3).

**W2, odd parity (two-step gap).** h_w(y₀) = (η_{y₀}, β_10, β_11, β_0) for y₀ ∈ {0..11}, plus the mirrors h′_w(y₀) = (η_{y₀}, β_1, β_0, β_11). That is 24 histories with t = 4.
- **Probability.** z₁ must be (9, y) (or (2, y) for the mirror), followed by three x-moves. Then Pr_f(h_w) = (1/144)·a³·Σ_y e_y(η_{y₀}) = a³/144 = **1/18000** in both worlds. The total over W2 at t = 4 is 1/750.
- **Posterior.** The history is uninformed, so π = ½.
- **Beliefs.** Each step is an x-move, so y never moves. ρ_C = (1−ε)δ_{y₀} + (ε/12)·1 = (3/4)δ_{y₀} + 1/48. Here c = 1, so ρ_M = Rρ_C, and TV(ρ_C, ρ_M) = 1 − ε = 3/4, because y₀ ≠ 11 − y₀.
- **Gaps.**
  - TV(Q₁(h,C), Q₁(h,M)) = 0.
  - TV(Q₂(h,C), Q₂(h,M)) = a²(1−ε)² = **9/400** = 0.0225.
  - **Exit-slice law.** ρ_C Ẽ = (1−ε)²·δ_{y₀} + u·1, with u := ε(2−ε)/12 = 7/192. The entry at y₀ is A := (1−ε)² + u = 115/192.
  - KL(Q₂C ‖ Q₂M) = KL(Q₂M ‖ Q₂C) = a²(A − u)·ln(A/u) = **(9/400)·ln(115/7) ≈ 0.06298 nats**.
  - I(F; W_{t+1} | h) = 0.
  - I(F; W_{t+1:t+2} | h) = a²·[A·ln(2A/(A+u)) + u·ln(2u/(A+u))] = **(1/25)·[(115/192)·ln(115/61) + (7/192)·ln(7/61)] ≈ 0.01203 nats**. This exceeds the Pinsker bound 2π(1−π)TV² ≈ 2.5e-4.
- **Mixture.** A predictor that replaces π = ½ by 0 or 1 makes a two-step TV error of 9/800 and a one-step error of 0.

**Band edge, the one-step gap one step later.** g = h_w(y₀)·β_1 (column 1, not in H_int).
- TV(Q₁(g,C), Q₁(g,M)) = a(1−ε)² = **9/80**.
- This shows the chain identity of §2.7: 9/400 = a·9/80.

**W3, even parity (gap first at horizon 3).** h_e(y₀) = (η_{y₀}, β_10, β_11), plus the mirrors (η_{y₀}, β_1, β_0). That is 24 histories with t = 3, each with probability a²/144 = 1/3600.
- c = 0, so ρ_M = ρ_C. Hence:
  - TV(Q₁) = 0;
  - TV(Q₂) = 0, by Theorem 2(iii).
- At horizon 3, the only η-emitting three-step path that crosses the seam is 11→0→1→2, with symbols (β_0, β_1, η). This prefix arises from no other path, because β_0 at t+1 forces the crossing. Every other path uses only off-seam edges, starting from the common belief b_M = b_C.
- So TV(Q₃(h,C), Q₃(h,M)) = a³·TV(ρ_C Ẽ, (Rρ_C) Ẽ) = a³(1−ε)² = **9/2000**.

**Informed witness, where the posterior over the bit is non-trivial.** h_inf(y₀) = (η_{y₀}, β_10, β_11, β_0, β_1, η_{y₀}, β_1, β_0), with t = 8, plus its mirror.
- **Likelihood ratio.** The η at s = 6 is an odd outside observation. Its likelihood is A = 115/192 under C and u = 7/192 under M, so π(h_inf) = 7/122.
- **Probabilities.** Pr_C = (1/144)·a⁷·(115/192) and Pr_M = (1/144)·a⁷·(7/192).
- **Posterior y-beliefs (chart coordinates).**
  - ρ_C′ = (1369/1380)·δ_{y₀} + (1/1380) elsewhere.
  - ρ_M′ = 37/84 at both y₀ and 11 − y₀, and 1/84 at each of the other ten rows.
- **Gaps.**
  - TV(ρ_C′, ρ_M′) = 1369/1380 − 37/84 = 444/805.
  - TV(Q₁) = 0.
  - TV(Q₂) = a²(1−ε)·444/805 = **333/20125 ≈ 0.01655**.
  - The mixture slope Q₂(h) = Q₂(h,C) + (7/122)·Δ is non-trivial.

### 2.6 Remark: k-step version (not frozen)

Widen the band to half-width m: B = {12−m, …, m−1}, keeping O non-empty. A history ending in a band column at distance d ≥ 2 from O then has Q_j(h,C) = Q_j(h,M) for every j < d. The argument is that of Theorem 1: within d − 1 steps, only band symbols can occur, and the column law is world-free.

With an odd-parity witness, the horizon-d gap is a^d·(1−ε)²; the proof is that of Theorem 2, with d consecutive x-moves. The frozen design uses m = 2. W3 already shows a horizon-3 first gap inside m = 2.

### 2.7 The reachable decision phase and X's sufficiency lemma

**Lemma X** (round 1, X§15, in chain-rule form). For each f and each history h with Pr(h) > 0:

  Q_k(h, f)(w_{1:k}) = Π_{j=1}^{k} Q₁(h·w_{1:j−1}, f)(w_j).

Consequences:
- **(i) No global version.** If Q₁(g, C) = Q₁(g, M) at **every** history g with Pr(g) > 0, then Pr_C = Pr_M on all strings. Then F would be irrelevant at every horizon, and the two worlds would be a single process.
  - The equivalent X§15 form: suppose S(h) is one-step sufficient everywhere and S(hw) = u(S(h), w). Then S determines every Q_k.
  - The W2 witness shows that the D-1 worlds differ. So horizon-1 irrelevance of F can only hold on a **phase**, and F must be one-step relevant at some reachable history.
- **(ii) Where the gap lives.** For h ∈ H_int, Q₁(h, ·) does not depend on F. So:

    TV(Q₂(h,C), Q₂(h,M)) = Σ_w ν_{x₀}(w)·TV(Q₁(hw,C), Q₁(hw,M)) = a·TV(Q₁(hβ†,C), Q₁(hβ†,M)).

  The horizon-2 relevance at h is exactly the horizon-1 relevance at the band-edge history hβ†, discounted by a. The y-belief carries over unchanged, because the step is an x-move.
- **(iii) In X's terms.**
  - S(h) := (b_C(h), b_M(h)), i.e. the full belief with π discarded, is recursively updatable.
  - On H_int it is one-step sufficient (Theorem 1). At hβ† it is not (9/80 at the witness).
  - So the lemma is respected: π is one-step unnecessary on H_int, two-step necessary, and one-step necessary one step later.

**Precise phase statement.**
- **Decision phase.** H_int = {h : Pr(h) > 0, w_t ∈ {β_11, β_0}}, for t ≥ 1. The pilot layout evaluates 1 ≤ t ≤ 33.
- **Frequency.** Pr(H_t ∈ H_int) = **1/6** for every t. The start is uniform and T_mix is doubly stochastic, so x_t is uniform on Z₁₂.
- **Gap-positive subphase.** H_int⁺ := {h ∈ H_int : ρ_C(h) ≠ ρ_M(h)}.
  - For uninformed h: h ∈ H_int⁺ ⟺ c(h) = 1 and ρ_C(h) ≠ Rρ_C(h).
  - H_int⁺ is reachable: W2 ⊂ H_int⁺, with total probability 1/750 at t = 4.
  - The informed witness h_inf is also in H_int⁺.
- **Where Theorem 1 does not hold.** Outside H_int, the guarantee is withdrawn. The positive-probability witness of failure is hβ†.

### 2.8 Edge cases (as requested)

1. **Band entry.**
   - A history whose last symbol is the entry symbol (β_10 from 9, or β_1 from 2) is at the band edge, not in H_int. Q₁ may depend on F there.
   - For uninformed entry histories, c is necessarily even, because any odd transit would have been followed by the outside observation that preceded the entry. So ρ_M = ρ_C and Q₁ coincides. For informed entry histories it need not.
   - A history that begins inside the band starts with c = 0 and a uniform y-belief, which is R-symmetric. It stays symmetric until the first outside observation, so its gap is 0. This is consistent with H_int⁺ being a proper subphase.
2. **Lazy stay.**
   - Theorem 1 holds for every p ∈ [0, 1), because the x-moves have probability a = (1−p)/4 at every state.
   - Theorems 2 and 3 need a > 0, i.e. p < 1.
   - Inside the band, a column-stay (a self-loop or a y-move, indistinguishable to an x-reader) updates the y-belief by the column kernel K = T_f|_column / (1 − 2a). K is the same in both worlds and R-equivariant, so ρ_M = R^c ρ_C is preserved.
   - TV(ρK, RρK) ≤ TV(ρ, Rρ). Long band dwell blurs ρ and shrinks the gap, but never creates one.
   - The gap scales as a²(1−ε)². At p = 0, a = 1/4.
3. **Boundary rows y ∈ {0, 11}.**
   - They have degree 3. The missing y-move goes to the self-loop, so the x-move probabilities are unchanged (Lemma 1).
   - R swaps the two boundary rows. This is why R is a degree-preserving automorphism of both worlds, which Theorem 3 needs.
   - In M, the seam joins row 0 to row 11. This is exactly the topological difference: one boundary circle instead of two.
   - n_y is even, so R has no fixed row, and the W2 gap is the same for every y₀. With odd n_y, the middle row would give a zero gap.
4. **Short histories.** All witnesses have t ≤ 8 ≤ 33, so `check_tokens` (max_len = 33) is respected.
5. **ε = 0 limit.**
   - Theorems 1 and 2 still hold where they are defined.
   - Lemma 0 fails, so world-conditional laws are undefined on histories that one world rules out, and π ∈ {0, ½, 1}.
   - This is why ε = 1/4 is frozen.

---

## 3. Oracle-only verification plan

No training and no model. All objects are deterministic, apart from one seeded sampling stage whose outputs are either gated by exact identities or reported descriptively.

### 3.1 Reused code (exact signatures, verified at @4f219d6)

| Use | Existing function (unchanged) |
|---|---|
| World C | `build_world(WorldConfig(family="cylinder", dims=(12,12)))` → `WorldSpec` (validates Betti, ∂∂ = 0, metric bounds) |
| World M | `QuotientLatticeBuilder` subclass plus `register_world`, then the same `build_world` |
| Topology certificates | `CubicalComplex(spec.n_states, spec.cells)`: `.betti(p)`, `.euler_characteristic()`, `.boundary_matrix(2)` (scipy CSR, shape [n₁, n₂]) |
| Transitions | `TransitionBuilder().build(world, TransitionConfig(p_stay=0.2))` → `TransitionSpec.T`, `.d_max`, `.pi` |
| Filtering | `BayesFilter(T, E, pi).run(tokens[R, P≤33])` → `FilterResult(b [R,P,N], q [R,P+1,V], log_evidence [R], ce)`; `q[:, t] = b_t T E` |
| Futures | `FutureOperator(T, E).F1(b)`, `.F2(b)` → [R, V, V] (internal check: marginal = F1 within 1e-12; belief rows must sum to 1 within 1e-10); `.observability_matrices(3)[2]` → O₃ [V+V²+V³, N]. G₃ = O₃[-V³:].T, with string index s₁V² + s₂V + s₃ |
| Sampling | `HMMSampler(T, E, pi, SequenceLayout()).sample(n, rng)` → tokens uint8 [n, 33], states int16 [n, 33] |
| Seeds | `SeedTree(master).generator(name, *scope)` |
| KL | `topo_pilot.analysis.kl_rows(P, Q)` → (values or None, status) |
| Decimal reference | `tests/oracle_profile/independent_reference.py::decimal_suffix_posterior(T, E, pi, suffix, digits≥60)`, imported by `sys.path` insertion as in `tests/oracle_profile/test_oracle_profile.py`. **Inputs must be passed as `Decimal`s created inside a `localcontext(prec ≥ 60)`.** Non-Decimal inputs are converted through `float`, which would test the float model rather than the exact one. The 0016 lesson about the default 28-digit context applies. |

Not reused, deliberately:
- `OverlapGaussian` and `point_distances`: they use unwrapped x for flipped gluing, and are a different emission anyway.
- `EmissionSpec`: its `mode` must be one of the registered modes, and the oracle kernels take raw arrays.

The round-1 sketch named `validate_process`. **No such function exists.** Its role is taken by `TransitionSpec.validate()` (called inside `build`) and by gates G1 and G3.

### 3.2 Minimal new code

**One module, `src/topo_pilot/experiment/d1_seam.py` (about 250 lines):**
1. `D1MobiusBuilder` (5 lines; `@register_world`; family `"d1_mobius"`, prefixed so it cannot collide with a future production Möbius).
2. `seam_emission(eps: Fraction, exact: bool) -> (E, symbols)`: the §1.3 array, either float64 or an object array of Fractions.
3. `mixture(T_C, T_M, E) -> (T_mix, E_mix, pi_mix)`.
4. `boundary_component_count(world) -> int`: the rows of |∂₂| with exactly one non-zero entry are the boundary edges; their components are counted with union-find.
5. `seam_parity(tokens) -> (c [R,P] int8, informed [R,P] bool)`: a vectorised scan for consecutive β_11/β_0 pairs and for η at odd parity.
6. `exact_filter(nbrs, E_frac, tokens)`. This is a sparse Fraction forward pass over each world, using lists of at most 5 successors. It returns:
   - the unnormalised α_t;
   - b_f, Pr_f(h) and π;
   - an exact Q₁ / Q₂ / Q₃ from a belief, by sparse path enumeration up to 3 steps.

   This is the **independent exact reference**, justified under the charter's "independent numerical references" clause. The float oracle cannot represent 1/5 or 1/48 exactly.
7. `run_d1_check(cfg, out_dir)`. It runs the gates, then writes `d1_seam_report.json` and `d1_seam_arrays.npz`, which hold T_C, T_M, E and the tokens with their sha256 hashes.

**One test file, `tests/experiment/test_d1_seam.py`:**
- fast unit tests of items 1–6;
- the exact identities;
- the witness closed forms;
- the controls of §3.4;
- a guard test that monkeypatches `topo_pilot.process._geometry.point_distances` to raise, and asserts that the D-1 path never calls it.

**No change to `world`, `process`, `oracle` or `dataset`.**

### 3.3 Stages and gates

**Frozen configuration:**
- dims (12,12); B = {10,11,0,1}; p = 1/5; ε = 1/4;
- master seed 20261015; sampling stream `SeedTree(20261015).generator("d1_seam", "sample")`;
- R = 16,384 sequences of length 33; chunk size 1,024;
- exact subset: the first 64 rows; Decimal subset: the first 8 rows plus 8 witnesses.

**Threads.** `OMP_NUM_THREADS = MKL_NUM_THREADS = OPENBLAS_NUM_THREADS = 1`.

**G0: Worlds and topology certificate.**
- Both builds succeed.
- Betti (1,1,0) over GF(2) and GF(3) for both worlds, and χ = 0.
- |edges| = 276 for both.
- The edge symmetric difference is exactly the 12 C-seam edges {(11,y),(0,y)} plus the 12 M-seam edges {(11,y),(0,11−y)}.
- Boundary-component count: **C = 2, M = 1**. This is the orientability certificate: a compact connected surface with χ = 0 and non-empty boundary is an annulus or a Möbius band, and the two are told apart by this count.
- Degree multisets are equal, and D_max = 4.

**G1: Exact kernel identities (Fraction; together with §2 these prove Theorems 1–3 for every history).**
- (a) T_f is stochastic, symmetric and supported on edges plus the diagonal. The float T from `TransitionBuilder` equals the exact T within 1e-15 entrywise.
- (b) Lemma 1: for all z and both f, the column sums equal κ exactly.
- (c) T_C = T_M on every non-seam entry. T_M[(11,y),(0,11−y)] = T_C[(11,y),(0,y)] = a. Both are R-equivariant.
- (d) E: the band rows are δ_{β_x}; the outside rows equal e_y with full support; Ẽ is doubly stochastic; the two blocks of E_mix are identical. Each world's 144-row block equals the single source array.
- (e) **Theorem 1, matrix form:** (T_f E)[z] = ν_{x₀} for all z in columns 11 and 0, for both f.
- (f) **Theorem 2, matrix form:** for z = (x₀, y) with x₀ ∈ {11, 0}, the two-step row T_f·diag(E_w)·T_f·E_{w′} has:
  - exit slice a²·e_y;
  - all other η entries 0;
  - a band block that does not depend on y or f.

**G2: Exact witnesses.** These are W2 (24 histories), the 24 band-edge extensions, W3 (24) and h_inf with its mirror.
- **Fraction values** must **equal** the closed forms of §2.5: Pr_f, π, Q₁ equality, TV₂ (and TV₃ for W3), TV₁ at the band edge, the TV₂ of h_inf, and the chain identity TV₂(h) = a·TV₁(hβ†).
- **Logarithmic quantities** (KL, I) are computed with Decimal at prec 60 from the exact Fractions and must agree with the closed-form expressions within 1e-45.
- **Decimal reference** (`decimal_suffix_posterior` on the 288-state mixture, applied to 8 witnesses): the posterior and π must agree with Fraction within 1e-45.
- **Float oracle** (`BayesFilter`, `FutureOperator.F2`, and G₃ from `observability_matrices(3)`): the beliefs, π, Q₁, Q₂ and Q₃ must agree with Fraction within **1e-12**, and within 1e-11 for π.

**G3: Sampled identity checks (float, every row and every position).**
- Run three filters: the mixture, world C alone, and world M alone.
- (a) The per-world filters raise no `IMPOSSIBLE_HISTORY` (Lemma 0).
- (b) At every H_int position, max_v |Q₁(h,C) − Q₁(h,M)| ≤ 1e-12, and Q₁ = ν_{x₀} within 1e-12.
- (c) At every H_int position, |TV₂ − a²(1−ε)·TV(ρ_C, ρ_M)| ≤ 1e-12.
- (d) **Mixture consistency on unnormalised blocks**, to avoid division when π is near 0 or 1:
  - |b_mix[:144] − (1−π)·b_C| ≤ 1e-12 and |b_mix[144:] − π·b_M| ≤ 1e-12;
  - π from the M-block sum agrees with expit(logev_M − logev_C) within 1e-10.
- (e) **Theorem 3 on every uninformed position:** |π − ½| ≤ 1e-11 and max|b_M − (id × R^c)b_C| ≤ 1e-12.
- (f) Fraction filter on the exact subset: float agreement within 1e-12 (1e-11 for π). Exact ΔQ₁ = 0 at every H_int position.
- (g) Smoke check on the sampler: the fraction of positions in H_int is within 0.01 of 1/6. Expect about 540,000 positions, so 0.01 is more than 10 sequence-clustered standard errors.

**G4: Controls (the check must be able to fail).**
- **Null control C⊕C.** Use the G3 tokens with T_mix = blockdiag(T_C, T_C). Both supports are equal, so the tokens are valid. Then every TV₁ and TV₂ ≤ 1e-12, and π = ½ within 1e-11 at every position. This detects spurious gaps from the numerics or the pipeline.
- **Positive control, local leak.** Build E′ by replacing the column-2 outside rows of the M block only with their R-reflections. This is a local, non-topological label change. Then G1(d) must flag that the rows are not identical, and G3(e) must find at least one uninformed position with |π − ½| > 1e-6, among sampled rows that pass through column 2. Otherwise the check is blind to local identifiability.
- **Positive control, band too narrow.** With B′ = {11, 0} as both band and "interior", G1(e) must fail (an exit is reachable in one step). This shows G1(e) is not vacuous.
- **Positive control, the gap itself.** The band-edge TV₁ = 9/80 and the W2 TV₂ = 9/400 are detected (G2).
- **Documented trap (a unit test, not a gate).** `is_x_periodic(M_world)` is False, so an `OverlapGaussian` built on M would use unwrapped x distances. The test asserts that rows in columns 2 and 9 then differ from C's. This records why §1.3 is explicit.

### 3.4 Tolerances (rationale)

| Comparison | Tolerance | Expected size |
|---|---|---|
| Exact identities | equality in Fractions | 0 |
| Float vs exact T | 1e-15 | ≈ 5e-17 (fl(0.2), 1 − 4·fl(0.2)) |
| Float predictive identities and float vs exact | 1e-12 | ≲ 1e-15 (scaled filter over ≤ 33 steps) |
| π equalities | 1e-11; 1e-10 for the log-evidence route | ≲ 1e-13 |
| Decimal vs Fraction | 1e-45 | ≲ 1e-55 at prec 60 |

**Attainability.** Every gated quantity is a theorem-implied identity with a tolerance at least 100× the expected float error. The only statistical gate is G3(g), with a margin above 10 SE. None of the gates is a fraction threshold on a scientific effect, so no gate can become INCONCLUSIVE by chance.

### 3.5 Descriptive outputs (reported, not gated)

At the H_int positions of the 16,384 sampled sequences:
- the distribution of TV₂ and KL₂: quantiles, plus the fractions with TV₂ = 0, > 1e-3, > 5e-3 and > 1e-2;
- I(F; W_{t+1:t+2} | h);
- π;
- the fraction uninformed;
- the parity split;
- all of the above by position t;
- TV₃ at even-parity positions;
- the occurrences of the exact W2 pattern; about 650 are expected, given probability 1/750 per position for t ≥ 4.

Outside H_int: the distribution of TV₁ at band-edge and outside positions, for the X-lemma contrast.

### 3.6 Cost

- G0–G2: under 2 CPU-min. The Decimal reference dominates: 288² × length per history, for 16 histories.
- G3: sampler about 1 s; the three filters over 16 chunks about 30 s; F2 and G₃ only at H_int rows, about 1 min; the Fraction subset (64 × 33 steps × at most 1,440 sparse products, with integers of about 100 digits) about 1 min.
- G4: about 1 min.
- **Forecast: about 5 CPU-min. Planning ceiling: 20 CPU-min. Memory under 2 GB** (chunks of 1,024: b is 1,024 × 33 × 288 float64, about 78 MB).

### 3.7 Verdict of the check

- **PASS** iff G0–G4 all pass.
- **FAIL** if any exact identity, witness value or sampled theorem identity fails, or if a control does not behave as specified. FAIL means that either the theorem as stated or its implementation is wrong. Stop, report the failing item, and do not modify the theorem after the fact.
- **INVALID** if a gate cannot be evaluated for a reason unrelated to the checked property, such as an environment error or a builder exception in G0.
  - A G0 builder failure is **escalated**, not worked around. In particular, the metric is not silently switched.
  - The analysis in §5 R8 predicts that the flat bounds hold. That analysis takes the 3 deck copies of the glide g(x,y) = (x+12, 11−y): every k = ±2 image is farther away in Manhattan distance than the k = 0 image.
  - The pipeline is deterministic and exact, so a rerun after a code fix under the same frozen specification is legitimate. It must be logged.

**Outputs, kept outside the repository** in `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`:
- the report JSON: gate statuses; exact values as Fraction strings; 30-digit Decimal values; maximum discrepancies; descriptive statistics; seeds; commit; CPU time;
- the NPZ of arrays, with sha256 hashes.

**Exposure registry entry.** These 16,384 histories become oracle-exposed. A later trained-model test must use fresh histories from a different seed scope.

### 3.8 Six-field reuse assessment

1. **Existing functions and artifacts:**
   - World: `build_world`, `QuotientLatticeBuilder`, `Identification('flipped')`, `register_world`, `CylinderBuilder`, `CubicalComplex` (betti, euler_characteristic, boundary_matrix).
   - Process: `TransitionBuilder` / `TransitionConfig`.
   - Oracle: `BayesFilter`, `FutureOperator` (F1, F2, observability_matrices).
   - Data and analysis: `HMMSampler`, `SequenceLayout`, `SeedTree`, `analysis.kl_rows`, and the Decimal reference from job 0014.
   - All are used unchanged. The mixture is an ordinary HMM, so no oracle change is needed.
2. **Genuinely missing capability:**
   - a registered Möbius family;
   - an emission given as an explicit table (the existing builders only produce distance-based or fixed-mode matrices, and `point_distances` is wrong for flipped gluing);
   - an orientability certificate (Betti numbers cannot separate C from M);
   - seam-parity bookkeeping;
   - an exact-rational reference for this model.
3. **Smallest change:** one experiment module and one test file. The Möbius builder is a 5-line subclass registered under the prefixed family; the emission is a 15-line array constructor. No production module is edited.
4. **Stable interfaces and invariants:**
   - vertex order z = 12x + y;
   - `TransitionSpec` invariants (symmetric, doubly stochastic, support on edges);
   - the oracle event order `emit_then_transition` and P ≤ 33;
   - the oracle's row-sum tolerance of 1e-10;
   - E is built once and shared by both blocks;
   - the exact parameters (Fraction 1/5 and 1/4) are the definitions, and the floats are derived from them;
   - `point_distances` is never called.
5. **Relevant regression checks:**
   - the existing `tests/world`, `tests/process`, `tests/oracle` and `tests/oracle_profile` must pass unchanged;
   - new tests: registering `d1_mobius` leaves the `square`/`cylinder` builds byte-identical; the `point_distances` guard; the controls of G4.
6. **Next plausible extension, without premature generalisation:**
   - if a trained-model D-1 test is approved, promote the Möbius builder to `world/lattice.py` with its own tests;
   - expose the band half-width m (§2.6) only when a k > 2 study is commissioned;
   - a Klein-bottle variant (y periodic plus flipped x) only for X6.
   - No generic "table emission" mode in `process` until a second consumer exists.

---

## 4. What a PASS licenses, and what it does not

### 4.1 Licensed claim (exact wording proposed)

> In the frozen D-1 process, the hidden bit selecting a cylinder or a Möbius world is a 12×12 lazy max-degree walk with p_stay = 1/5. A y-blind band of width 4 reads x exactly; outside it, y is read with noise ε = 1/4. The rows are identical in both worlds, and the prior on the bit is ½.
>
> 1. The world bit is exactly irrelevant to next-symbol prediction at every history ending in the band interior, which is one sixth of positions.
> 2. It is relevant to two-step prediction at reachable histories. At the witness (η_y, β_10, β_11, β_0), the world-conditional two-step laws differ by TV = 9/400 and KL = (9/400)·ln(115/7) nats. There, I(bit; next symbol) = 0 and I(bit; next two symbols) ≈ 0.0120 nats.
> 3. The bit affects the likelihood only through observations made after an odd number of net seam crossings, the Z₂ orientation holonomy. Local statistics cannot identify it.
>
> This was verified by exact rational arithmetic and the existing float oracle. It answers owner item D in the affirmative for the orientability distinction, by construction.

It also licenses a methodological claim: the existing oracle kernels compute these quantities correctly on a non-orientable world assembled as a mixture HMM.

### 4.2 What a later trained-model test would have to add (not now)

1. **A separate pre-registered protocol:**
   - architecture, objective, training-set size and seeds;
   - fresh histories with an exposure registry, never the G3 tokens;
   - CPU binding;
   - the C-path review, then freeze, then an oracle-only gate.
2. **The key design point, which follows from Lemma X.** A model that is optimal for the next symbol must still use the bit at band-edge positions hβ†, where it is one-step relevant. The scientific question is therefore **where** the information lives, not **whether** it is learned:
   - In a **recurrent** model, the state at an H_int position must carry π and F·c, because it is the only channel to t+1.
   - In a **Transformer**, position t+1 can re-read the context, so the representation at an H_int position is **not** required to carry the bit.

   The protocol must pick one of the following and state it:
   - an architecture contrast; or
   - a multi-step objective that makes the bit necessary at H_int itself.
3. **Readouts:**
   - the model's own two-step law at H_int, via the chain rule (feed β† and read Q₁);
   - regret against the oracle Q₂;
   - probes of π and of the R-asymmetry of ρ at H_int positions versus band-edge positions;
   - controls: a C⊕C-trained model (bit absent) and a label-permuted probe.
   - For a causal use claim, C1-style forcing with its matched random controls.
4. **An effect-size and power plan.**
   - The two-step gap is capped at a²(1−ε) = 3/100 in TV and concentrated on the event w_{t+1} = β†, which has probability a = 1/5.
   - Expect parameter tuning before that freeze: a smaller p raises a, a smaller ε raises the readout, a wider band raises the horizon.
   - Enrich the evaluation sets by oracle-only selection of H_int⁺ histories from long sampled pools.
   - Any parameter change requires rerunning this oracle check, at a cost of about 5 CPU-min.

### 4.3 What this construction does **not** say

- **Nothing about the original square/cylinder pilot.** That pilot uses a Gaussian overlap emission over the whole lattice: no band, no exact x-readout, and Q₁ depends on the full belief everywhere.
  - D-1's gadget cannot be transplanted to square versus cylinder. An x-reader at the band sees the square's x-boundary at horizon 1: from x = 11, the cylinder emits β_0 with probability a, and the square never does. That distinction is immediately visible.
  - The square/cylinder version needs a different gadget (X's round-1 D1 or L's D-2 double cover).
- **Nothing about B2 or D-055.** The NO-GO for the pilot's horizon-2 screen at p32 is untouched and is not reopened.
- **Nothing about H1.** C and M have identical Betti numbers. The distinction is orientability (w₁, a Z₂ class), and what a predictor needs is one bit, F·c(h), together with the y-belief. It does not need a circle-shaped representation.
- **Nothing about trained models**, representation geometry, causal use, or learnability. It is an existence result in one frozen parameterisation, with a small gap.
- **No separation of "topological" from "history" needs** in the B2 sense. At H_int all history except w_t is one-step irrelevant, and Q₂ needs both ρ (history) and F (topology).

---

## 5. Risks and mitigations

| # | Risk | Mitigation |
|---|---|---|
| R1 | **Degeneracy: F identifiable from outside-band or local statistics**, which would make the "topological" bit a mere label and trivialise the gap | Rows are identical by construction (one array), and T_C = T_M off the seam (G1 c, d). **Theorem 3** proves that the likelihood ratio is 1 unless an odd outside observation occurs. G3(e) checks π = ½ exactly on every uninformed sampled position. The G4 local-leak control proves the check would catch a violation. |
| R2 | **The `point_distances` trap** (flipped gluing is not x-periodic, so rows near the seam would differ between worlds) | E is built explicitly from the chart and never from `point_distances` (a guard test). A documented unit test shows the trap. Theorems 1–3 depend only on A1–A4. |
| R3 | **Reachability.** Gap-positive histories are rare: W2 has probability 1/750 per position, and the gap is at most 0.03 | Theorem 2 only needs one reachable witness, and W2/W3/h_inf are exact with positive probability. H_int itself has frequency 1/6. The sampled TV₂ distribution is reported (§3.5). For the downstream study: power planning, oracle-only enrichment, and parameter retuning before that freeze (§4.2). |
| R4 | **Informed histories dominate long sequences** (π drifts toward 0 or 1) | This is not a degeneracy: at informed h ∈ H_int, Q₁ is still F-free and Q₂ still depends on π (h_inf: π = 7/122, TV₂ = 333/20125). The position-wise fraction uninformed and the π distribution are reported. |
| R5 | **Identifiability failure in the other direction** (F never revealed, gap zero everywhere) | Excluded by the W2 witness and the informed witness (exact). The C⊕C null control shows the zero-gap baseline is distinguishable. |
| R6 | **Numerics:** tiny path probabilities; π near 0 or 1 | Use the scaled filter (existing). Mixture consistency is compared on unnormalised blocks (G3 d). Exact Fraction and Decimal references are used. |
| R7 | **Code-reuse mismatch** (a round-1 lesson) | Signatures are listed in §3.1 and were checked at @4f219d6. `validate_process` does not exist. The G₃ block ordering is stated. `FutureOperator` requires normalised beliefs (1e-10). The Decimal reference needs Decimal inputs in a prec-60 context. |
| R8 | **The Möbius build path is untested at 12×12** (the existing flipped test is the Klein bottle at 4×4) | G0 runs first and stops as INVALID on failure, with escalation and no silent metric switch. The flat-bounds argument for the glide copies is given in §3.7. Cell-generation correctness is certified independently by the edge symmetric difference and the boundary count. |
| R9 | **Interpretation and overclaim** | §4.1 wording; §4.3 non-claims; §2.2 remark on what H_int makes irrelevant. |
| R10 | **Self-assessed readiness** (a round-1 lesson) | An independent review is required: Codex first, then a clean-context Claude reviewer after 60 minutes without a reply. The reviewer should re-derive Lemma 1, Theorem 2(ii), the coupling Ψ, and the four witness values. |

---

## 6. Corrections to the round-1 L sketch

1. The outside emission is changed from the 36-symbol overlap emission (σ = 1.25) to an explicit x-blind noisy y-readout (V = 16).
   - Reason: the overlap rows would have come from `point_distances` (defect (a) in MERGE_ANALYSIS §7).
   - The y-readout also gives closed-form gaps and full support, which Lemma 0 needs.
   - The pilot-like alternative remains an option for the owner (open question 2). Theorems 1–3 hold for it unchanged.
2. The construction is now one mixture process with a hidden bit, as defect (b) required.
3. Q₁ equality is scoped to the band-interior phase H_int, and X's lemma is used to show why it must be (defect (c)).
4. The sketch's claim (ii) required "no earlier band visit, a y-belief that is not R-symmetric, odd crossings". It is replaced by:
   - the exact formula TV₂ = a²(1−ε)·TV(ρ_C, ρ_M), valid for all of H_int;
   - the coupling theorem, which says when ρ_M = R^c ρ_C.
5. F1 of the sketch ("R preserves E with b → 5−b") no longer applies to the new E, which is R-equivariant under η_y ↔ η_{11−y}. `validate_process` is replaced as described in §3.1.
6. The sketch's 1,600-entry Q₂ (V = 40) becomes 256 entries (V = 16).

---

## Open questions

1. **Owner: the meaning of "topological distinction".**
   - D-1 delivers **orientability** (cylinder vs Möbius, equal Betti numbers).
   - If the owner means square vs cylinder (β₁ differs), D-1 does not apply (§4.3), and X's D1 gadget or L's D-2 double cover is needed.
   - If the owner means a continuous circle of predictive states, X's D2 applies.
2. **Outside emission.** Keep the frozen y-readout, with exact closed forms? Or use the pilot-like Gaussian overlap restricted to O as an explicit array, with the gap computed numerically? The theorems are unchanged; only the witness numbers become numeric.
3. **Parameters.** p = 1/5, ε = 1/4 and m = 2 suffice for the oracle claim. Should the oracle freeze already use the values a later trained-model test would want (larger gap)? This document recommends freezing the oracle as specified and retuning only inside a downstream protocol, with a rerun of this check.
4. **Location of the Möbius builder.** Keep it in the experiment module (recommended now) or promote it to `world/lattice.py` (recommended only when a trained-model test is approved)?
5. **The W3 horizon-3 witness** is included as a gated exact witness. The reviewer may judge it out of scope for "two-step"; removing it does not affect Theorems 1–3.
6. **Downstream framing (not now).** Recurrent versus Transformer, or a multi-step objective. Lemma X implies that a next-symbol-trained Transformer need not carry the bit at H_int positions, so a representation test must be framed accordingly.
