STATUS: REVIEW_READY (not frozen)

# D1-MERGED-v1: cylinder versus Möbius with a y-blind seam band (oracle-only proof and check)

| Field | Value |
|---|---|
| Protocol id | D1-MERGED-v1 |
| Role | Protocol writer for the merged protocol. Planning only: no Python run, no data opened, no git write. |
| Date | 2026-10-15 |
| Binding decisions | `planning/responses/coord-d1-oracle-proof-20261015.MERGE.md` (cited as MERGE §n) |
| Other inputs | Request `planning/requests/coord-d1-oracle-proof-20261015.md`; track X `…codex.md` (cited X§n); track L `…claude.md` (cited L§n); analyst `…MERGE_ANALYSIS.md` (cited AN§n) |
| Code read for reuse claims | topo-pilot main @ `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`: `src/topo_pilot/world/{lattice,identification,registry,complex,metrics,config}.py`, `src/topo_pilot/process/{transition,_geometry}.py`, `src/topo_pilot/oracle/{_common,_filter,_futures}.py`, `src/topo_pilot/contracts/_schemas_world.py`, `tools/x4_oracle_profile/{validation,oracle_profile}.py`, `tests/oracle_profile/independent_reference.py`, `tests/world/test_world.py`, `tools/SPEC.md` |
| Arithmetic | Every number below was recomputed by hand by the protocol writer (W). Values that W derived and that appear in no input are marked **[W]**; the reviewer must re-derive them. |

## Summary (≤ 300 words)

**Construction (X).** One hidden-Markov process with a hidden world bit Z ∈ {C, M}, prior ½. Z selects how a 4×3 lattice is glued along x: the cylinder seam (3,y)~(0,y) or the Möbius seam (3,y)~(0,2−y). The y axis is not glued. Both worlds use the existing lazy max-degree walk with p_stay = 1/5, so every x-move has probability a = 1/5. The seam band is the three columns {2,3,0}. It emits one symbol per column and says nothing about y. Column 3 is the decision column. Column 1 emits A or B, reading y with probabilities 3/4, 1/2 and 1/4. Both worlds share one literal 12×5 emission array and the fixed start (1,0).

**Theorems.**
- (a) At every reachable history ending in σ3, the next-symbol law is (1/5, 1/5, 3/5, 0, 0) in both worlds.
- (b) Both worlds give positive probability to exactly the same histories.
- (c) A path coupling shows that the world bit changes the likelihood only through column-1 observations made after an odd number of seam crossings (Z₂ orientation holonomy).
- (d) The chain identity places the two-step gap at the band edge, one step later.
- (e) Exact witnesses:
  - h* = (A, σ2, σ3): two-step TV 1/50.
  - A reachable pair h_A, h_B with identical coordinate beliefs and world posteriors 1/4 and 3/4: next-symbol laws equal, two-step TV 1/100.
  - Band edge: one-step TV 1/10.
- (f) A general gap formula on the decision phase, stated as a conjecture.

**Check.** No sampling. Every reachable history up to length 8 (37,190 histories [W]) is enumerated in exact rationals. The existing BayesFilter and FutureOperator, used unchanged, cross-check the enumeration at 1e-12, and the existing Decimal reference cross-checks it at 1e-45. Further gates: structure, a surface check, an orientability certificate, and null and leak controls. Cost: about 3 CPU-min, ceiling 20.

**Licence.** An existence result for an orientability distinction only.

**Footprint.** One module and one test file. No production change, and WORLD_REGISTRY is not touched.

---

## 0. Notation and conventions

| Symbol | Meaning |
|---|---|
| Z ∈ {C, M} | Hidden world bit, drawn once per episode, P(Z = C) = P(Z = M) = ½ |
| S_t = (X_t, Y_t) | Coordinate state, X_t ∈ {0,1,2,3} (glued axis 0), Y_t ∈ {0,1,2} (unglued axis 1) |
| i(x,y) = 3x + y | State index within a world (equals `check_state_order`'s x·dims[1] + y) |
| 12z + 3x + y | Mixture index, z = 0 for C and z = 1 for M; 24 states |
| a = 1/5, c = 3/5 | x-move probability and column-hold probability (c = 1 − 2a) |
| e(y) | P(A ∣ state (1,y)) = (3/4, 1/2, 1/4) for y = 0, 1, 2 |
| R | Reflection R(y) = 2 − y; (Rρ)(y) := ρ(2 − y) |
| 𝓑 = {2, 3, 0}, I = {3} | Seam band and its interior (decision column). The outside region is {1} |
| Alphabet | (σ0, σ2, σ3, A, B), token ids 0, 1, 2, 3, 4 in this order |
| h = w_{1:t} | A history; P_f(h) := P(h ∣ Z = f) |
| π(h) | World posterior P(Z = M ∣ h). **This is X's ρ(h)**, renamed so that ρ can denote y-beliefs as in L, AN and MERGE §2 |
| b_f(h) | Filtered coordinate belief over S_t given h and Z = f |
| ρ_f(h) | y-marginal of b_f(h); δ_f(h) := ρ_f(h)(0) − ρ_f(h)(2) |
| Q_k(h, f) | Law of (W_{t+1}, …, W_{t+k}) given h and Z = f. Q₁ is the next-symbol law; J_f(h) := Q₂(h, f) is the two-step joint |
| Q₂^dist(h, f) | Law of W_{t+2} alone (the distant-symbol marginal), i.e. J_f summed over the first symbol |
| Q_k(h) | Mixture predictive (1 − π(h))·Q_k(h, C) + π(h)·Q_k(h, M) |
| par(h) | Seam parity: the number of indices s < t with {w_s, w_{s+1}} = {σ3, σ0}, mod 2 |
| μ | Start law: μ(C,1,0) = μ(M,1,0) = ½, zero elsewhere |
| TV(p, q) | ½ Σ_v ∣p_v − q_v∣. Logarithms are natural |

Event order: emit W_1 from S_1, then transition, then emit, and so on (`emit_then_transition`, as in BayesFilter).

---

## 1. Question, scope and licence

### 1.1 Question (owner B3-D; charter priority 3)

Does a finite process exist in which a topological distinction is:
- unnecessary for next-symbol prediction at a reachable, observable decision phase; but
- necessary for a longer horizon,

with the gap proven by construction?

The distinction is formulated as the posterior over a hidden world bit (request item 1).

### 1.2 Scope

- Oracle-only mathematics and checking. No training, no model, no sampling, no activations.
- One frozen construction (§2). No parameter search.
- B2 / D-055 is not reopened. No frozen result is altered.
- Dropped from the frozen scope (MERGE §6):
  - L's horizon-3 even-parity witness. It may appear only as optional descriptive output; it is not gated.
  - L's 12×12 construction. It stays on record (L§1–2, with AN's corrections L1–L3) as the named starting point for any later trained-model study. It is not frozen or run here.

### 1.3 Licence (MERGE §7, verbatim in substance)

A PASS is an **existence result** for an **orientability** distinction. Cylinder and Möbius have equal Betti numbers (1,1,0) over every field; they differ in orientability (w₁) and in their number of boundary circles. At a reachable decision phase, this distinction is:
- unnecessary at horizon 1;
- necessary at horizon 2.

A PASS says **nothing** about:
- the square/cylinder pilot. An x-reader sees the square's x-boundary already at horizon 1: from column 3, a cylinder can emit σ0 and a square never can. The gadget cannot be transplanted;
- β₁;
- B2 (and D-055);
- trained models: representation geometry, causal use or learnability.

**L's caveat stands.** A next-symbol-trained transformer need not carry the bit at decision-phase positions: position t + 1 can re-read the context. Lemma D shows that the bit is one-step relevant at band-edge positions one step later, which is where such a model must use it.

Proposed licensed sentence (X§12 plus L's holonomy clause):

> In the frozen D-1 process, a hidden bit selects a cylinder or a Möbius gluing of a 4×3 lattice that carries one shared emission array and a fixed start. At every reachable history ending in the band-interior symbol σ3, the bit is exactly irrelevant to next-symbol prediction. At reachable histories in the same phase, it is needed for two-step prediction: world-conditional TV 1/50 at h*, and TV 1/100 between two reachable histories that differ only in the world posterior (1/4 vs 3/4). The bit affects the likelihood only through outside observations made at odd seam parity (w₁ holonomy). This was established by proof and checked by exhaustive exact enumeration and by the existing oracle kernels.

What a later trained-model protocol would have to add (request item 4; **not now**) is listed in §7.3.

---

## 2. Exact construction (X§3, frozen as written; MERGE §1)

### 2.1 Worlds

| Item | C (cylinder) | M (Möbius) |
|---|---|---|
| Lattice | 4×3; x ∈ Z₄ glued; y ∈ {0,1,2} unglued | same |
| Ordinary horizontal edges | (x,y)–(x+1,y), x = 0, 1, 2 (9 edges) | same |
| Vertical edges | (x,y)–(x,y+1), y = 0, 1 (8 edges) | same |
| Seam edges | (3,y)–(0,y), y = 0, 1, 2 | (3,y)–(0,2−y), y = 0, 1, 2 |
| Counts | 12 vertices, 20 edges, 8 squares, χ = 0 | same |
| Degrees | 3 on rows y ∈ {0,2}; 4 on row y = 1; D_max = 4 | same |
| Betti over GF(2) and GF(3) | (1,1,0) | (1,1,0) |
| Boundary | two 4-cycles (rows 0 and 2) | one 8-cycle: row 0, then seam (3,0)–(0,2), then row 2, then seam (3,2)–(0,0) |
| Builder | existing `CylinderBuilder` via `build_world(WorldConfig(family="cylinder", dims=(4,3)))` | **local, unregistered** subclass, §2.6 |

The Möbius seam has exactly one straight edge, (3,1)–(0,1). So `process._geometry.is_x_periodic` finds 1 of 3 wrap edges and raises `INVALID_GLUE` (X§3.5, AN§2.1). D-1 never calls it.

### 2.2 Transitions (existing kernel, unchanged)

`TransitionBuilder().build(world, TransitionConfig(p_stay=0.2))` gives, in each world:
- T_f(s, s′) = a = (1 − p_stay)/D_max = 1/5 for every edge neighbour s′;
- T_f(s, s) = 1 − deg(s)/5, which is 2/5 on rows 0 and 2 and 1/5 on row 1.

T_f is symmetric, so the uniform law is stationary. `TransitionSpec.pi` stays uniform and validated. **The start law μ is never written into TransitionSpec** (its validator enforces πT = π at 1e-12).

### 2.3 Band and alphabet

- Band 𝓑 = {2, 3, 0}: two columns on one side of the seam and one on the other. Interior I = {3}: both x-neighbours of column 3 (columns 2 and 0) lie in 𝓑.
- Column 1 is the only outside column.
- Alphabet (σ0, σ2, σ3, A, B). Every symbol identifies x exactly. A and B also give a noisy reading of y.

### 2.4 Literal emission array (identical in both worlds by construction)

Rows are ordered by 3x + y; columns follow the alphabet order.

```
row  (x,y)   σ0   σ2   σ3   A     B
 0   (0,0)   1    0    0    0     0
 1   (0,1)   1    0    0    0     0
 2   (0,2)   1    0    0    0     0
 3   (1,0)   0    0    0    3/4   1/4
 4   (1,1)   0    0    0    1/2   1/2
 5   (1,2)   0    0    0    1/4   3/4
 6   (2,0)   0    1    0    0     0
 7   (2,1)   0    1    0    0     0
 8   (2,2)   0    1    0    0     0
 9   (3,0)   0    0    1    0     0
10   (3,1)   0    0    1    0     0
11   (3,2)   0    0    1    0     0
```

E_C = E_M = E. This is one source array used for both blocks, not two generated arrays. It is not built from `point_distances` or from any emission builder: those ignore the flipped gluing, and the odd y-dimension trips `is_x_periodic`.

**Why the column-1 rows lie strictly inside (0,1)** (L's Lemma 0 rationale, adopted per AN§5): full support on {A, B} makes the two worlds' supports common (Lemma B). It also keeps every finite-history posterior strictly between 0 and 1. With an exact y-readout (rows 1/0), one world could rule out a history and the world-conditional laws would be undefined there.

### 2.5 Start law and the single mixture process

- μ(C,1,0) = μ(M,1,0) = ½. The fixed start is the same in both worlds and is non-stationary.
- Mixture: T̃ = blockdiag(T_C, T_M) [24×24]; Ẽ = vstack(E, E) [24×5], built from the same source array; start μ [24].
- μ is passed only to BayesFilter, to the Decimal reference and to the exact enumerator. It is never passed to TransitionSpec.
- The time-homogeneous chain has no reset or clock gadget.
- The distinction is π(h) = P(Z = M ∣ h).

The fixed y = 0 start supplies an orientation reference (a y-frame at time 1). It supplies no information about Z, because P_C and P_M agree on every history whose outside observations all occur at even seam parity (Theorem C). Its one side effect, the start-law artefact, is stated and quantified in §4.

### 2.6 Local, unregistered Möbius builder (MERGE §1)

The builder lives inside the D-1 module. It is **not** decorated with `@register_world`, and WORLD_REGISTRY is never mutated.

```python
class _D1MobiusBuilder(QuotientLatticeBuilder):          # no @register_world
    family: ClassVar[str] = "_d1_mobius_local"
    expected_betti: ClassVar[dict] = {2: (1, 1, 0), 3: (1, 1, 0)}
    identifications: ClassVar[tuple] = (Identification(0, "flipped", flip_axis=1),)
```

It is validated explicitly, in the same order as `build_world`:
1. `spec = _D1MobiusBuilder().build(WorldConfig(family="_d1_mobius_local", dims=(4, 3), metric="flat"))`. `build` uses `self.family` and never consults the registry.
2. `spec.validate()`.
3. `check_boundary_closed(CubicalComplex(spec.n_states, spec.cells))`.
4. `check_flat_bounds(spec.dist, spec.dist_graph, 2)`.

**Expected to pass (W re-check).**
- `_wrap` maps corner (4,y) to (0, 2 − y), which is the M seam.
- The seam squares with bases (3,0) and (3,1) have the 4 distinct vertices {(3,0),(3,1),(0,2),(0,1)} and {(3,1),(3,2),(0,1),(0,0)}. So no cell repeats a vertex, and no cell is listed twice.
- Flat bounds:
  - FlatQuotientMetric is the Euclidean minimum over the deck copies g^k, k ∈ {−1, 0, 1}, of the glide g(x,y) = (x + 4, 2 − y).
  - Any graph path has length at most 4 (the diameter), so it lifts to a strip path ending at a k ∈ {−1, 0, 1} copy. Hence dist ≤ dist_graph.
  - Each included copy has L1 distance at least the graph distance, and L2 ≥ L1/√2. Hence dist ≥ dist_graph/√2.
  - Copies with k = ±2 sit at ∣Δx∣ ≥ 5, which exceeds √13, the largest k = 0 distance. So the truncation is exact, and the triangle inequality holds.

If any step raises an exception, the outcome is INVALID with escalation (stop rule S2). There is no metric switch and no registry workaround.

---

## 3. Theorems and proofs (on this construction)

### 3.0 Lemma 1 (x-autonomy; L Lemma 1 ported)

For f ∈ {C, M} and every state (x, y):
- P(X_{t+1} = x + 1 mod 4 ∣ S_t = (x,y), Z = f) = a;
- P(X_{t+1} = x − 1 mod 4 ∣ S_t = (x,y), Z = f) = a;
- P(X_{t+1} = x ∣ S_t = (x,y), Z = f) = c = 3/5.

So X_t is a Markov chain with the world-free, y-free kernel κ(x, x ± 1) = a and κ(x, x) = c.

*Proof.*
1. Every vertex has exactly one neighbour in column x + 1 and exactly one in column x − 1 (mod 4; these columns are distinct because 4 ≥ 3). In M, the neighbour of (3,y) in column 0 is (0, 2 − y), and the neighbour of (0,y) in column 3 is (3, 2 − y).
2. Each edge carries probability a.
3. All remaining mass stays in column x: vertical moves plus the self-loop.
   - On boundary rows: self-loop 2/5 + one vertical move 1/5 = 3/5.
   - On row 1: self-loop 1/5 + two vertical moves 2/5 = 3/5. ∎

This needs the max-degree normalisation (L): a degree-normalised walk would give x-moves probability 1/3 on boundary rows and 1/4 on row 1.

**Lemma 1′ (column dwell is R-equivariant).** Restricted to a column, the in-column kernel K (an unnormalised 3×3 matrix with row sums c) is:
- K(0,·) = (2/5, 1/5, 0);
- K(1,·) = (1/5, 1/5, 1/5);
- K(2,·) = (0, 1/5, 2/5).

It is the same in every column and in both worlds, and K(Ry, Ry′) = K(y, y′).

### 3.1 Theorem A: next-symbol identity on the decision phase (request item 2; X Theorem 1)

**Decision phase.** 𝓗_I := {h = w_{1:t} : P(h) > 0, w_t = σ3}, for t ≥ 1. The decision is taken immediately after observing the terminal σ3, before the next transition. The earliest member has t = 3.

**Theorem A.** For every h ∈ 𝓗_I and each f ∈ {C, M}:

  Q₁(h, f) = (σ0: a, σ2: a, σ3: c, A: 0, B: 0) = (1/5, 1/5, 3/5, 0, 0).

Hence Q₁(h) = (1/5, 1/5, 3/5, 0, 0) for every value of π(h), and I(Z; W_{t+1} ∣ h) = 0.

*Proof.*
1. w_t = σ3 forces X_t = 3 (column 3 alone emits σ3), so b_f(h) is supported on {(3,0), (3,1), (3,2)}. Both worlds have positive probability by Lemma B.
2. By Lemma 1, from any (3,y), X_{t+1} is 2, 0 or 3 with probabilities a, a and c, in both worlds.
3. All three columns lie in 𝓑 and emit σ2, σ0 and σ3 deterministically, whatever y is. A Möbius crossing reflects y but cannot change a band emission.
4. So every row δ_{(3,y)} T_f E equals (a, a, c, 0, 0). Every belief supported on column 3 is a convex combination of these rows, and the mixture predictive is a convex combination of two equal vectors. ∎

**Matrix form (what is checked, G1).** δ_{(3,y)} T_f E = (1/5, 1/5, 3/5, 0, 0) for y = 0, 1, 2 and f = C, M: six exact rows.

**Remark (strength; L).** On 𝓗_I, the last symbol alone is one-step sufficient. Not only Z, but every other feature of the history, is irrelevant at horizon 1. What makes Z special is that it changes the two-step law at the same histories (Theorem E).

### 3.2 Lemma B: common support (L Lemma 0 ported; AN§7.2)

**Lemma B.** For every finite string h, P_C(h) > 0 ⟺ P_M(h) > 0. Consequently, for every reachable h:
- both Q_k(h, f) are defined;
- 0 < π(h) < 1;
- the likelihood ratio obeys 3^{−m} ≤ P_M(h)/P_C(h) ≤ 3^{m}, where m is the number of A/B symbols in h. Theorem C sharpens m to the number of odd-parity outside observations.

*Proof.*
1. Write ξ(h) for the column sequence that h forces (each symbol fixes its column).
2. The x-path law is world-free: the start column is 1 in both worlds, and the kernel κ is world-free (Lemma 1). So P(X_{1:t} = ξ ∣ Z = f) = 1{ξ_1 = 1}·Π_s κ(ξ_s, ξ_{s+1}) is the same for f = C and f = M.
3. Conditional on X_{1:t} = ξ, every band emission has probability 1. Each A/B emission has probability in [1/4, 3/4] whatever y is, because every column-1 row has both entries in [1/4, 3/4].
4. So P_f(h) = P(ξ)·L_f(h ∣ ξ), with L_f(h ∣ ξ) ∈ [(1/4)^m, (3/4)^m]. Hence P_f(h) > 0 ⟺ P(ξ) > 0, a world-free condition.
5. The ratio bound follows from the same interval. ∎

**Reachable set (used by G2) [W].**
- Every column sequence starting at 1 with steps in {−1, 0, +1} (mod 4) has positive probability, since κ > 0 on all three moves.
- Each visit to column 1 offers both A and B.
- So the number N_t of reachable histories of length t is Σ_ξ 2^{#visits of ξ to column 1}. This equals Σ_x v_t(x) for the recursion v_1 = (0,2,0,0) and v_{t+1}(x′) = w(x′)·Σ_{x ∈ {x′−1, x′, x′+1}} v_t(x), with w(1) = 2 and w(x′) = 1 otherwise.

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | total |
|---|---|---|---|---|---|---|---|---|---|
| N_t (all reachable histories) | 2 | 8 | 32 | 124 | 480 | 1,852 | 7,144 | 27,548 | **37,190** |
| ∣𝓗_I ∩ length t∣ (= v_t(3)) | 0 | 0 | 4 | 16 | 68 | 264 | 1,028 | 3,968 | **5,348** |

### 3.3 Theorem C: path coupling, where the world bit acts only through odd-parity seam crossings (L Theorem 3 ported; AN§7.2)

**Visibility of crossings.**
- A seam crossing is a transition between columns 3 and 0. In this lattice, those columns are adjacent only through the seam.
- Both columns are band columns that emit σ3 and σ0 deterministically. So a crossing at step s → s + 1 occurs **iff** {w_s, w_{s+1}} = {σ3, σ0}.
- Hence par(w_{1:s}) is a function of the history.

An index s is an **odd outside observation** if w_s ∈ {A, B} and par(w_{1:s}) = 1. A history is **uninformed** if it has no odd outside observation, and **informed** otherwise.

**Theorem C.**
- **(a) Uninformed histories.** If h is uninformed, then:
  - P_M(h) = P_C(h), hence π(h) = ½ exactly;
  - b_M(h)(x, y) = b_C(h)(x, R^{par(h)} y), hence ρ_M(h) = R^{par(h)} ρ_C(h) and δ_M(h) = (−1)^{par(h)} δ_C(h).
- **(b) All histories.** P_M(h) equals the probability of h under a modified world-C process. That process is identical to C except that at each odd outside observation time s, state (1, y) emits with the row of (1, 2 − y).

  Consequently Z enters the likelihood only through outside observations made at odd seam parity. Equivalently, it enters only through observations that close a loop of odd winding around the core circle.
- **(c) Futures.** For every reachable h and string u, Q_k(h, M)(u) = P_M(h·u)/P_M(h). Both factors are given by (b), with the parity continuing from par(h). In particular, at an uninformed h with par(h) = 0 (for example h*), b_M = b_C and π = ½. Yet Q₂(h, M) can differ from Q₂(h, C), because a **future** crossing followed by a column-1 read is an odd outside observation of the extended string.

*Proof.*
1. **Coupling map.** For a world-C state path ζ = (x_s, y_s)_{s ≤ t}, let par_s(ζ) be the parity of the seam crossings among its first s − 1 transitions. Define Ψ(ζ)_s := (x_s, R^{par_s(ζ)} y_s).
2. **Start.** par_1 = 0, so Ψ(ζ)_1 = ζ_1. Both worlds start at (1,0) with the same probability. Only *equal* initial laws are needed, not R-invariant ones (AN§2.2).
3. **Off-seam steps** (a non-seam x-move, a vertical move or a stay). The map (x,y) ↦ (x, Ry) is an automorphism of the off-seam graph:
   - it preserves the horizontal edges (x,y)–(x+1,y) for x ≤ 2;
   - it swaps the vertical edges (x,0)–(x,1) and (x,2)–(x,1);
   - it preserves degree, since R swaps the two boundary rows;
   - it therefore preserves the self-loops 1 − deg/5.

   Also T_M = T_C on every off-seam pair, because both worlds have the same off-seam graph and the same D_max. Hence T_M((x, R^p y), (x′, R^p y′)) = T_C((x, y), (x′, y′)) for p ∈ {0, 1}.
4. **Seam steps.** The C-step (3, y) → (0, y) maps to (3, R^p y) → (0, R^{p+1} y). Since R^{p+1} y = 2 − R^p y, this is the M-seam edge (3, y′)–(0, 2 − y′) with y′ = R^p y, and it has probability a. The step (0, y) → (3, y) is symmetric.
5. **Bijection.** Ψ is a bijection from C-paths onto M-paths (the inverse unfolds an M-path the same way), and it preserves μ(z₁)·Π T.
6. **Emissions.**
   - At band times, the emission depends only on x, which Ψ preserves.
   - Seam crossings occur only between two consecutive band times. So for every C-path compatible with h, par_s(ζ) = par(w_{1:s}).
   - At an outside time s, the M-path sits at (1, R^{par(w_{1:s})} y_s).
7. Summing over ζ gives (b).
8. If h is uninformed, every outside factor coincides, so P_M(h) = P_C(h). Reading off the time-t marginal under Ψ gives the belief relation in (a). Part (c) is (b) applied to h·u. ∎

**Topological reading (L).**
- Column 1 is a contractible 1×3 patch on which the outside emission fixes a y-frame; the band is y-blind.
- A history that leaves column 1, travels through the band and returns to column 1 closes a loop. Its winding number around the core circle is congruent to the number of seam crossings, mod 2.
- The y-frame transported around the loop comes back reflected exactly when w₁ of the loop is non-zero: never in C (orientable), and iff the winding is odd in M (non-orientable).
- So Z is revealed only through w₁. This is what makes the bit topological rather than a label: a label leak (control L1) produces π ≠ ½ at an uninformed history, which Theorem C forbids in the frozen construction.

**Wording correction (AN L2).** "No statistic of outside-only segments carries information about Z" is true only of a segment's own law under an R-symmetric start. Jointly with earlier history, an outside segment at odd parity is exactly where Z appears. Under the fixed start, population single-time marginals are world-dependent through hidden windings (§4). The theorem statement (b) is the correct one.

### 3.4 Lemma D: chain identity and sufficiency (X's round-1 lemma; L §2.7; AN§7.2)

**Lemma D (X, sufficiency).** Let S be a statistic of histories with:
- a deterministic closed update S(hw) = u(S(h), w); and
- S(h) determining Q₁(h) at **every** reachable h.

Then S(h) determines Q_k(h) for every k.

*Proof.* By the chain rule, Q_k(h)(w_{1:k}) = Π_{j=1}^{k} Q₁(h·w_{1:j−1})(w_j). Each S(h·w_{1:j−1}) is obtained from S(h) and w_{1:j−1} by iterating u. ∎

**Corollary D1 (no global version).** Suppose Q₁(g, C) = Q₁(g, M) held at every reachable g. Then the world-conditional chain rule would give P_C = P_M on all strings, and Z would be irrelevant at every horizon. Theorem E exhibits a two-step gap, so horizon-1 irrelevance of Z can hold only on a **phase**, and Z must be one-step relevant at some reachable history (for example h_edge, Theorem E(iii)).

**Corollary D2 (chain identity; "where the gap lives").** For every h ∈ 𝓗_I:

  TV(J_C(h), J_M(h)) = a·TV(Q₁(hσ0, C), Q₁(hσ0, M)) + a·TV(Q₁(hσ2, C), Q₁(hσ2, M)).

The same holds with KL in place of TV.

*Proof.*
1. J_f(h)(w, w′) = Q₁(h, f)(w)·Q₁(hw, f)(w′).
2. By Theorem A, Q₁(h, f) = ν := (a, a, c, 0, 0) for both f. So TV(J_C, J_M) = Σ_w ν(w)·TV(Q₁(hw, C), Q₁(hw, M)).
3. The continuations hσ0, hσ2 and hσ3 have probability a, a and c in both worlds, so they are reachable.
4. hσ3 ∈ 𝓗_I, so its term vanishes by Theorem A. ∎

This replaces L's single-exit version: X's interior has two exits.

**Reading in X's terms.** Take S(h) := (b_C(h), b_M(h)), the world-conditional beliefs with π discarded. S is recursively updatable. It is one-step sufficient on 𝓗_I (Theorem A) but not at the band edges hσ0 and hσ2 (Theorem E(iii)). So:
- π is one-step unnecessary on 𝓗_I;
- π is two-step necessary there (Theorem E(ii));
- π is one-step necessary one step later.

The projection "current column only" is locally sufficient at the decision phase but not recursively sufficient (X§7.1).

### 3.5 Theorem E: the gap at the witnesses (exact values, all recomputed by W)

**(i) h* = (A, σ2, σ3), t = 3 (X Theorem 2).**
- **Path and probability.** The forced column path is 1 → 2 → 3: two non-seam x-moves, so y = 0 throughout. P_f(h*) = (3/4)·a² = 3/100 in each world, so P(h*) = 3/100.
- **State.** h* is uninformed with par = 0, so π(h*) = ½ and b_C = b_M = δ_{(3,0)}.
- **First step from (3,0)** (degree 3):
  - to (2,0) with a, emitting σ2;
  - to the seam neighbour with a, emitting σ0: (0,0) in C, (0,2) in M;
  - to (3,1) with a, or stay with 2/5: together c, emitting σ3.
- **Second step:**
  - From (2,0): to (1,0) with a, which emits A/B as 3/4 / 1/4; to (3,0) with a (σ3); hold in column 2 with c (σ2).
  - From the σ0 state:
    - In C, (0,0) → (1,0) with a, reading 3/4 / 1/4.
    - In M, (0,2) → (1,2) with a, reading 1/4 / 3/4.
    - In both worlds, to column 3 with a (σ3) and hold with c (σ0).
  - From column 3: (a, a, c) on (σ0, σ2, σ3).

Rows are the first symbol and columns the second symbol, in the order (σ0, σ2, σ3, A, B):

| J_C(h*) | σ0 | σ2 | σ3 | A | B | row sum |
|---|---|---|---|---|---|---|
| σ0 | 3/25 | 0 | 1/25 | 3/100 | 1/100 | 1/5 |
| σ2 | 0 | 3/25 | 1/25 | 3/100 | 1/100 | 1/5 |
| σ3 | 3/25 | 3/25 | 9/25 | 0 | 0 | 3/5 |
| A, B | 0 | 0 | 0 | 0 | 0 | 0 |

J_M(h*) equals J_C(h*) except for the σ0 row, whose (A, B) entries are (1/100, 3/100).

- **Joint.** TV(J_C, J_M) = ½(2/100 + 2/100) = **1/50** = a²/2.
- **Distant marginals.**
  - Q₂^dist(h*, C) = (6/25, 6/25, 11/25, 3/50, 1/50).
  - Q₂^dist(h*, M) = (6/25, 6/25, 11/25, 1/25, 1/25).
  - TV = ½(1/50 + 1/50) = **1/50**.
- **Logarithmic quantities** (AN extras, re-derived by W):
  - KL(J_C ‖ J_M) = KL(J_M ‖ J_C) = (3/100)ln 3 + (1/100)ln(1/3) = **(1/50)·ln 3 ≈ 0.0219722** nats.
  - I(Z; W_{t+1:t+2} ∣ h*) = ½KL(J_C ‖ J̄) + ½KL(J_M ‖ J̄), where J̄ has 2/100 on both (σ0, A) and (σ0, B). This equals (1/100)[3 ln(3/2) − ln 2] = **ln(27/16)/100 ≈ 0.0052325** nats.
  - I(Z; W_{t+1} ∣ h*) = 0 (Theorem A).
- **Chain identity check.**
  - TV₁(h*σ0): the column-1 read from (0,0) in C versus (0,2) in M gives a·½(∣3/4 − 1/4∣ + ∣1/4 − 3/4∣) = a/2 = 1/10.
  - TV₁(h*σ2) = 0, since both worlds sit at (2,0).
  - So TV₂ = a·(1/10) + a·0 = 1/50 ✓.
- **Scaling.** For other p_stay < 1 (same max-degree construction), this gap is a²/2 = (1 − p)²/32. At p = 1 it vanishes. No parameter search is part of D-1.

**(ii) The posterior-isolation pair h_A / h_B, t = 11 (X§6; MERGE §3; the decisive witness).**

```
h_A = (A, σ2, σ3, σ0, A, σ2, σ3, σ0, A, σ2, σ3)
h_B = (A, σ2, σ3, σ0, B, σ2, σ3, σ0, A, σ2, σ3)
```

- **Path.** Both force the column path 1,2,3,0,1,2,3,0,1,2,3. Each consecutive pair of columns differs, so all 10 transitions are x-moves, contributing a^10. There are two seam crossings (t = 3→4 and t = 7→8).
- **y-tracks.**
  - In C, y = 0 throughout.
  - In M, y = 0 for t ≤ 3, y = 2 for 4 ≤ t ≤ 7, and y = 0 for t ≥ 8.
  - So S_11 = (3,0) with probability 1 in both worlds and for both histories.
- **Readouts.** The readouts at t = 1 and t = 9 are at even parity and have likelihood 3/4 in both worlds. The readout at t = 5 is at odd parity.

| History | P(h ∣ C) | P(h ∣ M) | π(h) |
|---|---|---|---|
| h_A | (27/64)·a^10 | (9/64)·a^10 | **1/4** |
| h_B | (9/64)·a^10 | (27/64)·a^10 | **3/4** |

- **Probability.** P(h_r) = ½·(36/64)·a^10 = (9/32)·a^10 = **9/312,500,000 ≈ 2.88 × 10⁻⁸** for each r ∈ {A, B}. Here a^10 = 1/9,765,625.
- **Beliefs.** b_C(h_A) = b_C(h_B) = b_M(h_A) = b_M(h_B) = δ_{(3,0)}. The 24-state mixture beliefs are (1 − π)·δ_{(C,3,0)} + π·δ_{(M,3,0)}, so they differ **only** in π.
- **Next symbol.** Q₁(h_A) = Q₁(h_B) = (1/5, 1/5, 3/5, 0, 0) (Theorem A).
- **Two-step.** J(h_r) = (1 − π(h_r))·J_C + π(h_r)·J_M, with J_C and J_M the arrays of (i), since the conditional states are the same δ_{(3,0)}.
  - TV(J(h_A), J(h_B)) = ∣3/4 − 1/4∣·(1/50) = **1/100**.
  - Q₂^dist(h_A) = (6/25, 6/25, 11/25, 11/200, 5/200).
  - Q₂^dist(h_B) = (6/25, 6/25, 11/25, 9/200, 7/200).
  - The distant-marginal TV is also **1/100**.
- **Necessity.** Any representation that maps h_A and h_B to the same two-step prediction q has TV(q, J(h_A)) + TV(q, J(h_B)) ≥ 1/100. So it errs by at least **1/200** in TV on one of them (triangle inequality).
- **Licence limit.** This shows that the predictive information carried by the world posterior is necessary. It does not establish an internal encoding or a representation shape.

**(iii) Band edge h_edge = (A, σ2, σ3, σ0, A, σ2), t = 6 (X§7.2).**
- **State.** The endpoint is column 2, an outer band edge, not in 𝓗_I. C has y = 0; M has y = 2 (one crossing).
- **Probability [W].** P_C = (9/16)·a⁵ and P_M = (3/16)·a⁵. So π(h_edge) = 1/4 and P(h_edge) = (3/8)·a⁵ = 3/25,000.
- **World-conditional next-symbol laws:**
  - Q₁(h_edge, C) = (0, 3/5, 1/5, 3/20, 1/20);
  - Q₁(h_edge, M) = (0, 3/5, 1/5, 1/20, 3/20);
  - TV = **1/10** = a/2.
- **Mixture next-symbol law [W].** (0, 3/5, 1/5, 1/8, 3/40).
- **Role.** This must be in the verification, to catch any "whole band" overclaim: one-step equality fails at outer band edges.

**Theorem E (statement).** h*, h_A, h_B ∈ 𝓗_I and h_edge are reachable. The values above hold exactly. In particular:
- the world-conditional two-step gap at h* is 1/50 in both the joint and the distant marginal;
- the mixture pair (h_A, h_B), with identical coordinate beliefs and equal next-symbol laws, differs by TV 1/100 at horizon 2;
- the one-step gap at the band edge is 1/10.

*Proof.* The direct path sums above, together with Theorems A and C and Corollary D2. ∎

### 3.6 Conjecture F: the decision-phase gap formula (analyst-derived; MERGE §2: NOT adopted until the independent reviewer re-derives it)

**Conjecture F.** For every h ∈ 𝓗_I, with δ_f := δ_f(h) = ρ_f(h)(0) − ρ_f(h)(2) in chart coordinates:

- (F1) TV(J_C(h), J_M(h)) = (a²/2)·max(∣δ_C∣, ∣δ_M∣);
- (F2) TV(Q₂^dist(h, C), Q₂^dist(h, M)) = (a²/2)·∣δ_C∣;
- (F3) for the mixture: if h, h′ ∈ 𝓗_I have equal (b_C, b_M), then TV(J(h), J(h′)) = ∣π(h) − π(h′)∣·TV(J_C(h), J_M(h)).

**Consequences (if adopted).**
- At uninformed h (Theorem C(a)), ∣δ_M∣ = ∣δ_C∣, so F1 and F2 coincide.
- Column dwell multiplies δ_f by exactly 2/3 per band-dwell step (from Lemma 1′: δ′ = (2/5)δ/(3/5)) **[W]**. Dwell therefore blurs the gap and never creates one (L).
- If δ_C = 0 ≠ δ_M, the joint gap is positive while the distant-marginal gap is zero (X's cancellation warning §11.5).

**Consistency with the witnesses.**
- h*: δ_C = δ_M = 1, giving 1/50 ✓.
- h_A/h_B: (F3) gives (1/2)·(1/50) = 1/100 ✓.

**Probe of the max branch [W; not a PASS witness].** h_max = (A, σ2, σ3, σ0, A, B, σ0, σ3), t = 8.
- Column path 1,2,3,0,1,1,0,3: six x-moves, plus one column-1 dwell between t = 5 and t = 6.
- Odd outside observations at t = 5 and t = 6.
- In C: ρ_C = (1/2, 1/2, 0), so δ_C = 1/2.
- In M: ρ_M = (3/4, 1/4, 0) in chart coordinates (after the second crossing), so δ_M = 3/4.
- P_C = (9/80)·a⁶ and P_M = (3/40)·a⁶, so π(h_max) = 2/5 and P(h_max) = (3/32)·a⁶ = 3/500,000.
- Direct path sums:
  - (σ2, A): C 5a²/8, M 11a²/16;
  - (σ0, A): C 5a²/8, M 5a²/16;
  - joint TV = **3/200**;
  - distant-marginal TV = **1/100**.
- These match F1 = (1/50)·(3/4) and F2 = (1/50)·(1/2). The enumeration (G2) must reach h_max and report these values.

**Status and check.** Conjecture F is checked at every 𝓗_I node of the exhaustive enumeration (§5, gate CONJ). Its outcome (CONFIRMED / REFUTED) is reported separately and does not enter the PASS criteria. Theorems A–E do not depend on it.

**For the reviewer, after an independent re-derivation: derivation outline.**
1. From column 3, the only two-step paths that reach column 1 are 3 → 2 → 1 (first symbol σ2) and 3 → seam → 1 (first symbol σ0). Each has probability a² (two x-moves; y unchanged except for the reflection by the M seam).
2. Using Σρ = 1, (ρ·e)(A) = ½ + δ/4.
3. So J_C(σ2, A) = J_C(σ0, A) = a²(½ + δ_C/4), J_M(σ2, A) = a²(½ + δ_M/4) and J_M(σ0, A) = a²(½ − δ_M/4).
4. All band entries are world-free (Lemma 1). Using ∣u − v∣ + ∣u + v∣ = 2·max(∣u∣, ∣v∣) gives F1. Summing over the first symbol gives F2: Q₂^dist(h, M) puts exactly **a²** on each of A and B, whatever δ_M is.
5. This outline was re-derived by W and agrees with AN, except for one correction: AN wrote (a²/2, a²/2). See the changelog, entry C1.

### 3.7 Edge cases (request item 2)

1. **Band entry.**
   - Entry from column 1 lands at column 0 or 2, an outer edge, never directly at column 3. Every 𝓗_I history has passed through an outer edge, and no history starts inside the band (the start is fixed at column 1).
   - At outer edges, Q₁ may depend on Z (h_edge: 1/10).
   - An uninformed history that has just entered the band (from column 1, without crossing) has even parity: if the preceding read had been at odd parity, the history would be informed. So ρ_M = ρ_C there, and Q₁(h, C) = Q₁(h, M) **[W]**.
   - The band-edge gap arises at outer-edge histories reached through a crossing (for example h*σ0) or at informed ones.
2. **Lazy stay.**
   - Theorem A holds for every p_stay ∈ [0, 1), because each x-move has probability a = (1 − p)/4 from every state (Lemma 1).
   - The gap events at the witnesses consist of two x-moves, so stays never enter them. Their probability is exactly a².
   - Stays and vertical moves enter other entries of the full arrays.
   - Column dwell acts by the R-equivariant kernel K (Lemma 1′), the same in both worlds. It preserves ρ_M = R^{par} ρ_C (Theorem C) and multiplies δ by 2/3 per step.
3. **Boundary rows of the unglued y axis.**
   - Rows 0 and 2 have degree 3. The missing vertical mass goes to the self-loop, so the hold probability is 2/5 + 1/5 = 3/5, the same as on row 1 (1/5 + 2/5).
   - R swaps the boundary rows. This is what makes R a degree-preserving automorphism of the off-seam graph, which Theorem C needs.
   - The M seam joins row 0 to row 2. That join is the topological difference: one boundary circle instead of two.
   - Row y = 1 is R-fixed. A start at y = 1 removes all named-witness gaps and the start-law artefact (control N3).
4. **Short histories.**
   - Every gated history has t ≤ 11 ≤ 33, within `check_tokens` (max_len 33).
   - The futures are computed from beliefs, so no token sequence longer than the history is ever passed.

### 3.8 Reachability of the decision phase (AN§5: report per t) [W]

The x-chain from X_1 = 1 on Z₄ has eigenvalues 1, 3/5, 1/5, 3/5. This gives P(X_t = 3) = ¼·[1 − 2(3/5)^{t−1} + (1/5)^{t−1}]:

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | ∞ |
|---|---|---|---|---|---|---|---|---|---|
| P(h ∈ 𝓗_I) | 0 | 0 | 2/25 = 0.08 | 18/125 = 0.144 | 116/625 = 0.1856 | 132/625 = 0.2112 | 3542/15625 = 0.226688 | 18438/78125 = 0.2360064 | 1/4 |

At t = 3, all four 𝓗_I histories, (A/B, σ2/σ0, σ3), have world-conditional two-step TV 1/50. With the fixed start, the first read carries no y-information.

---

## 4. The start-law artefact (MERGE §5)

**Statement.** Because the start is fixed at (1,0), not R-symmetric, the single-time marginal law of an outside symbol differs between worlds.

*Derivation.* Let D_t := P_C(W_t = A) − P_M(W_t = A). Then:
- the band-symbol marginals are world-free (Lemma 1);
- by Theorem C(b) applied to marginals, D_t = Σ over C-paths ζ with X_t = 1 and odd par_t(ζ) of P(ζ)·[e(y_t) − e(2 − y_t)];
- e(y) − e(2 − y) = ½·(1{y = 0} − 1{y = 2});
- y starts at 0 and changes only during column dwell, which follows Lemma 1′. The weight after j dwell steps is ½·(K^j(0,0) − K^j(0,2)) = ½·(2/5)^j;
- an odd winding back to column 1 needs net x-displacement ±4, that is, 2·C(k, (k+4)/2) x-move sign patterns for k x-moves (k even, k ≥ 4).

Then TV(P_C(W_t ∈ ·), P_M(W_t ∈ ·)) = ∣D_t∣.

| t | Contributions | D_t | Value |
|---|---|---|---|
| 1–4 | no odd winding fits | 0 | 0 |
| 5 | k = 4, j = 0: 2·a⁴·½ | **1/625** (MERGE, AN) | 0.0016 |
| 6 | k = 4, j = 1: 2·5·a⁴·(1/5) | **2/625 [W]** | 0.0032 |
| 7 | k = 4, j = 2: 2·15·a⁴·(2/25); k = 6, j = 0: 12·a⁶·½ | **66/15625 [W]** | 0.004224 |
| 8 | k = 4, j = 3: 2·35·a⁴·(4/125); k = 6, j = 1: 12·7·a⁶·(1/5) | **364/78125 [W]** | 0.0046592 |

The two t = 5 paths are 1→2→3→0→1 and 1→0→3→2→1. In both, D_t > 0: the cylinder reads A more often, because a single winding returns M's frame reflected.

**Interpretation.**
- The artefact is the topological channel itself, not a label leak. It arises only through hidden odd windings followed by a column-1 read; per history, those are exactly the informed histories of Theorem C. It vanishes:
  - under the cylinder-seam null C⊕C (N1);
  - under the symmetric readout (N2);
  - under any R-symmetric start, for example y = 1 (N3; the sum is antisymmetric under the path involution ζ ↦ Rζ);
  - under L's uniform stationary start.
- At every uninformed history, π(h) = ½ exactly (Theorem C(a)).
- **Disclosure for downstream use.** Population-level outside-symbol frequencies at a fixed time are world-dependent. A downstream study must not present "world identifiable from per-time outside frequencies" as a non-topological leak, and must not use such frequencies as an unconditional null.

**Quantified in the enumeration (G2).** For t = 1, …, 8, the enumeration sums P_f(h) over the histories of length t that end in each symbol. It reports P_f(W_t ∈ ·) and D_t exactly, and requires:
- D_t to equal the table values;
- D_t = 0 under N1, N2 and N3.

---

## 5. Verification plan (oracle-only; nothing here has been executed)

### 5.1 Overview and order

All checks are deterministic. There are no seeds, no sampled histories and so no exposure-registry entry (MERGE §4). The gates run in the order G0, G0S, G0O, G1, G2 (+ CONJ), G3, G4, G5, G6, and stop at the first INVALID.

### 5.2 Gates and exact criteria

**G0: structure (both worlds; exact unless stated).**
1. Builds succeed: C through `build_world`; M through the local builder with the explicit validation of §2.6.
2. Counts: 12 states, 20 edges and 8 squares. χ = 0. Betti numbers (1,1,0) over GF(2) and GF(3). ∂₁∂₂ = 0.
3. The edge sets equal the lists in §2.1 exactly. The symmetric difference of the C and M edge sets is exactly the 3 C-seam edges plus the 3 M-seam edges.
4. Degrees are 3, 4, 3 on rows 0, 1, 2. D_max = 4. The degree multisets are equal.
5. Exact T_f is built independently from the coordinate formulas of §2.2 (Fraction a = 1/5).
   - It is stochastic and symmetric.
   - Its support equals the production support exactly.
   - The production float T equals it entrywise within **1e-15**.
   - T_C = T_M on every off-seam pair.
6. E equals the literal array of §2.4 exactly. The mixture blocks satisfy Ẽ[:12] ≡ Ẽ[12:] bitwise (`np.array_equal`), and both are the same source object.
7. μ has entries ½ at indices 3 (C,1,0) and 15 (M,1,0), and zero elsewhere. `TransitionSpec.pi` is uniform.

**G0S: surface check (links; AN "manifold check").**
1. Edge links: each edge lies in exactly 1 or 2 squares. Expected in each world: 8 boundary edges in exactly 1 square and 12 interior edges in exactly 2.
2. Vertex links: for each vertex v, form the graph whose nodes are the edges incident to v and whose edges are the squares containing v (joining the square's two edges at v). It must be connected and either a path (an arc) or a cycle (a circle).
   - Expected: arcs with 3 nodes and 2 edges at rows 0 and 2; 4-cycles at row 1.
   - W hand-checked M's seam vertices. For example, the link of (0,1) is the cycle (0,0)–(1,1)–(0,2)–(3,1)–(0,0), and the link of (0,0) is the arc (1,0)–(0,1)–(3,2).
3. Pass ⟺ every link is as stated. This makes the complex a compact connected 2-manifold with boundary, which the certificate below presupposes (AN "certificate gap").

**G0O: orientability certificate.**
1. **Boundary components.**
   - Boundary edges are those in exactly one square, read from the rows of ∣∂₂∣ (`CubicalComplex.boundary_matrix(2)`) with one non-zero entry.
   - Count the connected components of the boundary graph: **C = 2 (two 4-cycles) and M = 1 (one 8-cycle)**.
   - Together with G0S and χ = 0: a compact connected surface with χ = 0 and non-empty boundary is an annulus (2 boundary circles) or a Möbius band (1).
2. **Orientation cocycle (direct w₁ test).**
   - For each interior edge e shared by squares i and j, with incidence signs ε_i(e), ε_j(e) ∈ {±1} from ∂₂, set ω(e) := −ε_i(e)·ε_j(e).
   - Propagate a sign s by breadth-first search over the dual graph (8 squares, 12 interior edges), using s_j = ω(e)·s_i.
   - Expected:
     - **C**: consistent on all 12 interior edges. The resulting s ∈ {±1}⁸ satisfies (∂₂ s)_e = 0 on every interior edge, verified in integers.
     - **M**: inconsistent: some dual cycle has ∏ω = −1.
   - Rank corroboration:
     - the rank over GF(3) of the 12×8 interior-edge submatrix of ∂₂ is 7 for C and 8 for M (`rank_mod_p`). Full column rank for M means no non-zero rational s exists;
     - over GF(2) the nullity is 1 for both: the sum of all squares is a mod-2 relative cycle.
3. Pass ⟺ all expected values hold.

**G1: exact kernel identities (Fraction).**
1. Lemma 1: for all 24 (state, world) rows, the column sums of T_f equal κ exactly.
2. Lemma 1′: the in-column kernel equals K in every column and world, and K is R-equivariant.
3. Theorem C ingredients:
   - T_M((x, Ry), (x′, Ry′)) = T_C((x, y), (x′, y′)) on all off-seam pairs;
   - T_M((3, Ry), (0, R²y)) = T_C((3, y), (0, y)) = a, and likewise for the reverse direction.
4. Theorem A, matrix form: δ_{(3,y)} T_f E = (1/5, 1/5, 3/5, 0, 0) for all 6 (y, f).
5. Two-step kernel rows from each (3,y), f (6 exact 5×5 arrays):
   - the band block does not depend on (y, f);
   - (σ2, A) = a²·e(y) and (σ0, A) = a²·e(y) in C, or a²·e(2 − y) in M;
   - for y = 0 they equal the J arrays of §3.5(i).

**G2: exhaustive exact enumeration (Fraction; MERGE §4).** A depth-first forward recursion over every reachable history up to length **K = 8**.
- Each node carries the unnormalised world-conditional forward vectors α_C and α_M. These are supported on the observed column, at most 3 states each.
- Each node also carries a third pass: the "reflected-C" forward vector of Theorem C(b).
- A child is created for every symbol with positive one-step probability.

At every node:
1. **Counts.** The number of nodes at depth t equals N_t (§3.2 table), and the number of σ3-ending nodes equals ∣𝓗_I ∩ t∣.
2. **Lemma B.** P_C(h) > 0 and P_M(h) > 0 at every node. 3^{−m_odd} ≤ P_M/P_C ≤ 3^{m_odd}, where m_odd is the number of odd outside observations.
3. **Theorem C(b).** P_M(h) equals the reflected-C likelihood exactly.
4. **Theorem C(a).** At uninformed nodes, P_M(h) = P_C(h) (so π = ½) and b_M = (id × R^{par(h)}) b_C exactly.
5. **Mixture consistency.** The 24-state normalised belief equals ((1 − π)·b_C, π·b_M) exactly.

At every 𝓗_I node (5,348 of them):

6. **Theorem A.** Q₁(h, C) = Q₁(h, M) = Q₁(h) = (1/5, 1/5, 3/5, 0, 0) exactly.
7. **Corollary D2.** TV(J_C, J_M) = a·[TV₁(hσ0) + TV₁(hσ2)] exactly, with the continuations computed by one further exact filter step.
8. **Named nodes.** h*, h_max and the prefixes of h_A, h_B and h_edge are reached, and their exact values equal §3.5 and §3.6.

Population and artefact outputs:

9. **Start-law artefact (§4).** P_f(W_t ∈ ·) and D_t for t = 1..8 equal the §4 table exactly.
10. **Descriptive outputs (not gated).** Per t: the 𝓗_I probability mass, which must also equal the §3.8 table (gated); the informed/uninformed split; the distribution of world-conditional TV₂ and of mixture π at 𝓗_I nodes; and the count of 𝓗_I nodes with a positive joint gap but a zero distant-marginal gap.

**CONJ: Conjecture F check (reported, not gating).** At every 𝓗_I node, compare TV(J_C, J_M) and TV(Q₂^dist) with F1 and F2 exactly.
- Report CONFIRMED (all 5,348 equal) or REFUTED (list the nodes).
- Report the count of nodes with ∣δ_M∣ ≠ ∣δ_C∣. It must be ≥ 1, because h_max is one; otherwise the max branch is not exercised, and this is recorded.
- REFUTED triggers stop rule S4.

**G3: named witnesses (Fraction; independent path-sum reference in the test file).**
Every value in §3.5(i)–(iii) is checked exactly:
- the probabilities;
- π;
- the conditional and mixture beliefs;
- Q₁ (world-conditional and mixture);
- the full J_C and J_M arrays;
- Q₂^dist;
- the TVs 1/50, 1/100, 1/10 and the bound 1/200;
- the chain identity at h*.

The logarithmic quantities at h* (KL and I) are computed in `decimal` at precision 80 from the exact Fractions. They must equal (1/50)·ln 3 and ln(27/16)/100, evaluated in the same context, within **1e-45**.

**G4: float oracle cross-check (existing kernels, unchanged).**
1. **Filters.** For each length t ≤ 8, stack all N_t enumerated histories as `tokens [N_t, t]` (int64). Run:
   - `BayesFilter(T̃, Ẽ, μ).run(tokens)` on the mixture;
   - `BayesFilter(T_f, E, μ_f).run(tokens)` per world, with μ_f = δ_{(1,0)}. This must raise no `IMPOSSIBLE_HISTORY` (Lemma B).

   Run the witnesses h_A, h_B and h_edge the same way.
2. **Futures.** At every 𝓗_I node and every named witness, run `FutureOperator(T̃, Ẽ).F1/.F2` on the mixture belief and `FutureOperator(T_f, E).F1/.F2` on each world belief. Q₂^dist := F2.sum(axis=1), where axis 1 is the first symbol. FutureOperator.F2 is the **joint**; it is not b·T²·E.
3. **Compare against the exact values from G2 and G3:**

| Quantity | Tolerance |
|---|---|
| Beliefs b (mixture and per world), F1, F2 and Q₂^dist entries | max abs error ≤ **1e-12** |
| π (the M-block sum of the mixture belief) | abs error ≤ **1e-11** |
| π via expit(logev_M − logev_C) | abs error ≤ **1e-10** |
| Every TV (world-conditional, pair, band edge) against its exact value | abs error ≤ **1e-12** |
| One-step differences at 𝓗_I nodes, max_v ∣F1(b_C) − F1(b_M)∣ | ≤ **1e-12** |
| Mixture futures against (1 − π)·F(b_C) + π·F(b_M) | ≤ **1e-12** |
| Evidence exp(log_evidence) against the exact P(h) | relative error ≤ **1e-10** |
| log_evidence against the exact ln P(h) | abs error ≤ **1e-10** |
| Distribution sums | ≤ 1e-12 |
| Non-finite values or negative probabilities | none allowed |

There is no smoothing and no epsilon. The oracle's own internal checks (1e-10 sums, the F2 marginal at 1e-12) stay as they are.

**G5: Decimal reference (existing, unchanged).**
- Function: `tests/oracle_profile/independent_reference.py::decimal_suffix_posterior`, the job-0014 reference that `tools/x4_oracle_profile/validation.py` uses. It is imported by `sys.path` insertion, as in `tests/oracle_profile/test_oracle_profile.py`.
- **Inputs are passed as `Decimal` objects** created from the strings "0.2", "0.4", "0.75", "0.5", "0.25", "1", "0" and "0.5" (start). Every entry of T, E and μ is a terminating decimal, so the inputs are exact.
- Float inputs would be converted through `Decimal(float(x))` and would test the binary model instead (L; AN§3). The 0016 lesson about the default 28-digit context applies, so digits = 80.
- Called on the 24-state mixture with suffix = the whole history. With pi = μ, this gives the full-history posterior.
- Applied to all 646 reachable histories with t ≤ 5, plus h*, h_A, h_B, h_edge and h_max.
- Criterion: every one of the 24 posterior entries, and π (the M-block sum), agrees with Fraction within **1e-45**.

**G6: controls.** Each control is a separate synthetic variant; the frozen construction is not changed.

| Id | Variant | Required outcome (exact) | Purpose |
|---|---|---|---|
| N1 | **Null C⊕C** (= X's "cylinder seam" control): T̃ = blockdiag(T_C, T_C), same Ẽ and μ | Full K = 8 enumeration: π(h) = ½ at every node; every world-conditional TV₁ and TV₂ = 0; D_t = 0 for all t; h_A and h_B both have π = ½ and pair TV 0 | Detects spurious gaps from the pipeline or from indexing |
| N2 | **Symmetric readout:** column-1 rows (½, ½) in both blocks; M seam kept | Full enumeration: π = ½ everywhere; all world-conditional TV₂ at 𝓗_I = 0; D_t = 0 | The gap needs a y-readout |
| N3 | **Start y = 1** (R-fixed): μ′(C,1,1) = μ′(M,1,1) = ½ | Named-witness gaps vanish: h* TV₂ = 0; h_A and h_B have π = ½ and pair TV 0; h_edge TV₁ = 0. D_t = 0 for t ≤ 8. Theorem C(a) still holds at uninformed nodes. Informed histories may still have π ≠ ½ (for example (A, A, σ2, σ3, σ0, A), with C/M likelihood ratio 7/5 [W]), so "all gaps vanish" is **not** required | Certifies the role of the orientation reference and the origin of the §4 artefact |
| L1 | **Local leak** (positive control): M block's column-1 rows reflected, E_M′(1,y) = E(1, 2 − y); C block unchanged | G0.6 must report E_C ≠ E_M. G2.4 must report the uninformed node (A) with π = 1/4 ≠ ½ (likelihoods 3/4 vs 1/4). The control passes iff **both** are detected | The check can see a label leak |
| L2 | **Narrow interior** (positive control): column-2 rows replaced by the column-1 rows (A/B readout) in both blocks | G1.4 (Theorem A matrix form) must fail: δ_{(3,0)} T_f E ≠ δ_{(3,2)} T_f E. The control passes iff detected | G1.4 is not vacuous |
| P1 | **Band edge** (positive control) | h_edge world-conditional TV₁ = 1/10 (G3) | Catches a whole-band overclaim |

For N1 and N2, the "world-conditional" laws are those of the two blocks of the variant mixture.

### 5.3 Verdicts

- **PASS** ⟺ G0, G0S, G0O, G1, G2, G3, G4, G5 and G6 all pass. In particular, PASS requires:
  - the Theorem A identity at every 𝓗_I node;
  - the reachable **posterior-isolation pair** (π = 1/4 vs 3/4, identical coordinate beliefs, pair TV 1/100), as required by MERGE §3 and X§8.8.

  A PASS on h* alone is insufficient. The CONJ outcome is reported alongside and is not a PASS condition.
- **FAIL** ⟺ the run completed on the frozen inputs, and any exact identity, witness value, count, artefact value, tolerance or control outcome deviates. FAIL means that the theorem as stated or its implementation is wrong. Preserve the discrepancy. Never edit a theorem, value or tolerance after seeing the result.
- **INVALID** ⟺ some gate could not be evaluated for a reason unrelated to the checked property. Examples:
  - an environment or import error;
  - an interrupted run (X's NOT_COMPLETED);
  - a builder or validation exception in G0, which is **escalated**, never worked around;
  - a mismatch in the input or protocol hash;
  - the cost ceiling being reached.

  The pipeline is deterministic, so a rerun after a logged fix under the same frozen specification is legitimate.

### 5.4 Cost estimate (forecast, not benchmarked)

| Part | Estimate |
|---|---|
| G0–G1 (builds, links, certificate, 6 kernel rows) | < 5 s |
| G2: 37,190 nodes × 3 passes × ≤ 3 states × ≤ 3 in-column successors, in Fractions; plus futures at 5,348 𝓗_I nodes (≤ 3 × 5 × 5 two-step paths per world) | ≈ 10–30 s |
| G3 witnesses and the Decimal logarithms | < 2 s |
| G4: BayesFilter over 37,190 rows (8 length groups, 24 states) plus F1/F2 at ≈ 5,400 beliefs | < 5 s |
| G5: 651 histories × 24² × ≤ 11 Decimal multiply-adds at precision 80 | ≈ 10–30 s |
| G6: N1, N2 full enumerations; N3, L1, L2 partial | ≈ 30–90 s |
| **Total** | **≈ 3 CPU-min forecast; planning ceiling 20 CPU-min** (stop rule S1); memory < 1 GB |

- Run on one thread (`OMP_NUM_THREADS = MKL_NUM_THREADS = OPENBLAS_NUM_THREADS = 1`). Owner limits apply: at most 4 threads, 12 GiB RAM, existing usage/STOP controls, disk thresholds and CPU accounting.
- Outputs are written outside the repository, to a store bound by the coordinator (proposed: `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`):
  - the report JSON: gate statuses; exact values as Fraction strings; 30-digit Decimal renderings; maximum discrepancies; per-t tables; CPU time; commits and hashes;
  - a small NPZ with T_C, T_M, E and μ, plus sha256 hashes.

---

## 6. Reuse assessment and minimal new code footprint

### 6.1 Six-field reuse assessment

| Field | Assessment |
|---|---|
| **1. Existing functions and artefacts (used unchanged)** | **World:** `QuotientLatticeBuilder`, `CylinderBuilder`, `build_world`, `WorldConfig`, `Identification('flipped', flip_axis=1)`, `CubicalComplex` (`boundary_matrix`, `betti`, `euler_characteristic`, `one_skeleton`), `WorldSpec.validate`. Also the internals `world.complex.check_boundary_closed`, `world.complex.rank_mod_p` and `world.metrics.check_flat_bounds`. These are not in `world.__all__`; importing them from `tools/` is outside `check_imports.py`'s scope, which covers `src/` only, and `tests/process` already imports internals this way. **Process:** `TransitionBuilder`, `TransitionConfig`, `check_support` (called inside `build`). **Oracle:** `BayesFilter`, `FutureOperator` (F1, F2). **Reference:** `tests/oracle_profile/independent_reference.py::decimal_suffix_posterior`. No scientific payload or oracle cache applies. |
| **2. Genuinely missing capability** | A local Möbius builder (no registered Möbius family exists). An explicit table emission (no builder produces one, and `point_distances` is wrong for flipped gluing). The mixture assembly with a separate start law. Surface and orientability certificates (Betti numbers cannot separate C from M). Seam-parity bookkeeping. An exact-rational history enumerator with the reflected-C pass. |
| **3. Smallest change** | One module and one test file (§6.2). No change to `world`, `process`, `oracle`, `dataset`, `contracts` or any production file. No new sampler, filter, future engine, runner or generic "table emission" mode. |
| **4. Stable interfaces and invariants** | Row-vector convention; `T [N,N]`, `E [N,V]`, `pi [N]`; `emit_then_transition`; state id 3x + y and mixture id 12z + 3x + y; token ids σ0 = 0, σ2 = 1, σ3 = 2, A = 3, B = 4; P ≤ 33; belief rows normalised within 1e-10; one shared E object; Fraction parameters are the definitions and floats derive from them; μ never enters TransitionSpec; WORLD_REGISTRY untouched; `point_distances` and `is_x_periodic` never called. `tools/x4_oracle_profile/oracle_profile.py::validate_process` **exists** but enforces πT = π at 1e-12, so it must not be called with μ (see changelog C2). |
| **5. Relevant regression checks** | Existing `tests/world`, `tests/process`, `tests/oracle` and `tests/oracle_profile` run once, unchanged, and must pass. New tests (§6.2): registry hygiene (WORLD_REGISTRY identical before and after import and run); guards that monkeypatch `process._geometry.point_distances` and `is_x_periodic` to raise; the Decimal-input trap; all controls; the 400-line file limit (`tools/check_file_sizes.py`). |
| **6. Next plausible extension (no premature generalisation)** | If a trained-model study is approved: promote a Möbius builder to `world/lattice.py` with its own tests, starting from L's 12×12 record. Expose the band width only if a k > 2 study is commissioned. No generic table-emission mode until a second consumer exists. |

### 6.2 Minimal new code

**Module: `tools/d1_seam/d1_seam.py`** (one file, ≤ 400 lines, the repository limit). The location follows the `tools/x4_*` convention and keeps `src/` untouched; the coordinator binds the final location (AN C6). Contents:
1. Constants: dims, band, alphabet, token map, the literal E as Fractions, μ, and the witness histories.
2. `_D1MobiusBuilder`, unregistered, plus `_validated(spec)`, which mirrors `build_world` (§2.6).
3. Exact T_f from the coordinate formulas, plus mixture assembly (float and Fraction).
4. Structure, link and orientability-certificate functions (G0, G0S, G0O).
5. The exact enumerator with the reflected-C pass, and futures up to 2 steps (G1, G2, CONJ).
6. Float and Decimal cross-check drivers (G4, G5).
7. Control variants, parameterised by seam, E variant and start (G6).
8. `run(out_dir)`, which writes the report.

If the module cannot fit in 400 lines, stop and escalate (S6). Do not split it silently.

**Test file: `tests/d1_seam/test_d1_seam.py`.**
- Authored **independently, from the frozen protocol only, before the module** (X§9): critical tests first, by an author other than the module's.
- Contains a small independent Fraction path-sum reference for the named witnesses. It does not import the module's exact kernels.
- Tests:
  - the closed-form values of §3.5, §3.6 (h_max) and §4;
  - the N_t counts;
  - registry hygiene;
  - the `point_distances` / `is_x_periodic` guards;
  - the Decimal trap (float inputs agree only to about 1e-17, Decimal inputs to 1e-45);
  - each G6 control's expected outcome.

**No production change.** No exposure registry. No sampler.

---

## 7. Risks, mitigations and stop rules

### 7.1 Risks (request item 5)

| # | Risk | Mitigation |
|---|---|---|
| R1 | **Degeneracy: Z identifiable from local or outside-band statistics** (a label leak would trivialise the gap) | One literal E shared bitwise (G0.6). T_C = T_M off the seam (G0.5, G1.3). Theorem C: π = ½ exactly at every uninformed history, checked at all 37,190 nodes (G2.4). L1 shows the check detects a leak. |
| R2 | **Start-law artefact mistaken for a leak, or hidden** | Stated and quantified (§4). It is gated against exact values for t ≤ 8 and against zero under N1, N2 and N3. |
| R3 | **Reachability.** The decisive pair is rare (2.88 × 10⁻⁸ each) | An existence proof needs only positive, exactly computed probability. 𝓗_I itself has mass 0.08 at t = 3, rising toward 1/4 (§3.8). h* has 0.03. No claim is made about typical natural histories; a downstream study needs its own coverage analysis. |
| R4 | **Identifiability in the other direction** (the gap is zero everywhere) | Excluded by the exact witnesses (G3) and by the N1 contrast. |
| R5 | **Posterior collapses to 0 or 1** | Lemma B: the likelihood ratio stays within 3^{±m_odd}. The pair has π = 1/4 and 3/4. |
| R6 | **`point_distances` / `is_x_periodic` trap** (flipped gluing is not x-periodic; odd n_y gives a partial wrap and raises) | E is literal; guard tests (§6.2). |
| R7 | **Registry pollution** | Unregistered local builder; registry-hygiene test. |
| R8 | **The Möbius build path is untested at 4×3** (the existing flipped test is the 4×4 Klein bottle) | G0 runs first, and an exception gives INVALID with escalation (S2). Cell generation is certified independently by G0.3, G0S and G0O. Flat bounds are argued in §2.6. |
| R9 | **The Decimal reference silently tests the float model** | Decimal string inputs at digits = 80 (G5); trap test. |
| R10 | **The start law leaks into TransitionSpec**, or `validate_process` is applied to μ | μ is passed only to BayesFilter, the reference and the enumerator (G0.7). `validate_process` is not called with μ. |
| R11 | **Joint versus distant-marginal confusion, or cancellation** | Both horizons are gated separately. F2 is the joint and Q₂^dist = F2.sum(axis=1). CONJ reports joint-positive, marginal-zero nodes. |
| R12 | **Conjecture F adopted prematurely** | It is labelled a conjecture, does not enter PASS, and needs independent re-derivation (MERGE §2). |
| R13 | **Overclaim** (topology, H1, pilot, models) | §1.3 licence and non-claims. Lemma D's phase restriction. L's transformer caveat. |
| R14 | **Self-assessed readiness** | Status is REVIEW_READY, not frozen. The independent clean-context reviewer must re-derive: Lemma 1, Theorem A, Lemma B, the coupling Ψ (Theorem C), Corollary D2, every Theorem E value, the [W] values (N_t, the §3.8 and §4 tables, h_max, h_edge's π) and Conjecture F. |

### 7.2 Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S0 | Protocol not frozen, or input/protocol/commit hash mismatch | Do not run. |
| S1 | Cost ceiling of 20 CPU-min reached, or memory above 2 GB | Stop. INVALID. Report partial gate statuses. |
| S2 | Any builder or validation exception in G0 (including M's flat bounds) | Stop. INVALID. Escalate. No metric switch, registry change or production edit. |
| S3 | Any exact identity, witness, count, artefact or control deviation | Stop at the first failing gate. FAIL. Preserve the failing node or array. No post-hoc theorem or tolerance edit. |
| S4 | CONJ = REFUTED | Complete the remaining gates, then **hold** the verdict until the reviewer diagnoses it as an implementation defect (then FAIL and fix) or a false conjecture (then withdraw Conjecture F by a logged amendment; the verdict rests on G0–G6). |
| S5 | A float or Decimal tolerance is exceeded while the exact gates pass | FAIL of G4 or G5. Escalate as a possible oracle or implementation defect. Never loosen the tolerance. |
| S6 | Implementation needs a production change, a second module, or more than 400 lines | Stop and escalate before writing it. |
| S7 | Owner STOP, usage limits, or disk thresholds | Stop. INVALID (interrupted). Resume only under the same frozen specification. |

### 7.3 What a later trained-model protocol would have to add (request item 4; not now)

1. A separate pre-registered protocol:
   - architecture, objective, data size, seeds, fresh histories and CPU binding;
   - review, then freeze, then an oracle-only gate.
2. A treatment of the fixed start and of the §4 artefact in its training and evaluation distributions, and a coverage plan for rare 𝓗_I⁺ histories (oracle-only enrichment).
3. A framing that respects Lemma D:
   - a recurrent model must carry π at 𝓗_I positions;
   - a transformer need not.

   Pick an architecture contrast, or a multi-step objective that makes the bit necessary at 𝓗_I itself.
4. Readouts:
   - the model's two-step law via the chain rule;
   - regret against the oracle;
   - probes of π and of the R-asymmetry of ρ at 𝓗_I versus band-edge positions;
   - C⊕C and label-permuted controls;
   - causal forcing with matched controls, if use is claimed.
5. An effect-size and power plan. The gap is small: a²/2 = 1/50 world-conditional. Parameter retuning, done only within that protocol, requires rerunning this check.

The recommended starting point is L's 12×12 record (MERGE §6).

---

## 8. Changelog: sources and corrections

### 8.1 Section sources

| Section | Source |
|---|---|
| Header, summary, §0 notation | W; notation mapping X's ρ(h) → π(h) per L, AN and MERGE §2 |
| §1.1–1.2 Question and scope | Request; X§1; MERGE §6 |
| §1.3 Licence | MERGE §7 (verbatim in substance); licensed sentence from X§12 plus L§4.1 clause 3; L§4.3 non-claims |
| §2.1–2.5 Construction | **X§3** as written (MERGE §1); counts and boundary from AN§2.1 and X§8.3 |
| §2.4 rationale for full-support rows | **L** Lemma 0 rationale (AN§5) |
| §2.6 Local builder and validation | MERGE §1; AN§7.1; flat-bounds argument restated by W |
| §3.0 Lemma 1, Lemma 1′ | **L** Lemma 1 ported; Lemma 1′ from L§2.8(2), made explicit for 4×3 by W |
| §3.1 Theorem A | **X** Theorem 1; matrix form from L Theorem 1 |
| §3.2 Lemma B | **L** Lemma 0 ported (AN§7.2); X§11.3 ratio bound; N_t table W |
| §3.3 Theorem C | **L** Theorem 3 ported (AN§7.2, MERGE §2); part (c) W; wording correction AN (L2) |
| §3.4 Lemma D, Corollaries | **X** round-1 lemma (X§7.1); L§2.7; two-exit form AN§7.2 |
| §3.5 Theorem E | **X**§5–7 witnesses; AN§2.1 KL and MI extras; h_edge probabilities and mixture law W |
| §3.6 Conjecture F | **Analyst** AN§7.2 (MERGE §2: conjecture); h_max probe and dwell factor W |
| §3.7 Edge cases | X§7.2–7.4; L§2.8; band-entry parity remark adapted by W |
| §3.8 Reachability table | AN§5 (report per t); values W |
| §4 Start-law artefact | MERGE §5; AN§4 (t = 5); t = 6–8 values and derivation W |
| §5 Verification | MERGE §4; **X**§8 tolerances; **L**§3.3–3.4 π and Decimal rules and controls N1/L1/L2; AN§7.4 G0–G4, manifold and w₁ tests; X§8.6 controls N2/N3/P1; enumeration specifics W |
| §5.3 Verdicts | X§8.8 (pair required); L§3.7 (INVALID); X's NOT_COMPLETED folded into INVALID |
| §5.4 Cost | W (supersedes X§10 and L§3.6) |
| §6 Reuse and footprint | X§9 and L§3.8 merged; re-checked against code by W |
| §7 Risks and stop rules | X§11; L§5; AN§4; stop rules W |
| §7.3 Downstream | X§12; L§4.2 |
| Open questions | MERGE "Owner questions"; AN§8 |

### 8.2 Corrections and clarifications (every item re-checked by W)

| Id | Where | Was | Now |
|---|---|---|---|
| **C1** | AN§7.2 (general gap) | "Q₂,M is always (a²/2, a²/2) on {A, B}" | **(a², a²)**. In M, the two exits carry reflected readouts that sum to a²·(½ + δ/4) + a²·(½ − δ/4) = a² for each of A and B. At h*, Q₂^dist(M) gives A = B = 1/25 = a². The TV formula (a²/2)·∣δ_C∣ is unaffected. |
| **C2** | L§3.1/R7; AN§3 "validate_process does not exist" | Function said not to exist | True only within `src/topo_pilot`. `tools/x4_oracle_profile/oracle_profile.py::validate_process(T, E, pi, tol=1e-12)` exists. It enforces πT = π, so it would reject μ. D-1 must not call it with μ. |
| C3 | Coordinator task wording "tools/x4_oracle_profile (the Decimal reference)" | Location ambiguous | The function is `tests/oracle_profile/independent_reference.py::decimal_suffix_posterior`. `tools/x4_oracle_profile/validation.py` imports it by `sys.path`. |
| C4 | AN§2.1 "only deck copies with k ∈ {−1,0,1} can attain the L1 minimum" | Argued in L1 | FlatQuotientMetric is Euclidean (L2). The conclusion (flat bounds pass) holds; the argument is restated in §2.6. |
| C5 | AN§7.4 G2 size "upper bound 3⁷·2⁸ ≈ 5.6e5, in practice of order 10⁴" | Estimate | Exact count **37,190** reachable histories up to t = 8, of which 5,348 end in σ3 [W] (§3.2). |
| C6 | X status line FREEZE_READY; X "no scientific construction choice remains open" (AN X1) | Overclaim | REVIEW_READY (not frozen). The owner question on the meaning of "topological" and the fixed-start choice are disclosed (§4, open questions). |
| C7 | X§11.4 "the only world-dependent operation is the seam gluing" | Incomplete disclosure | True of the kernels. The per-time outside-symbol marginals still differ, through hidden windings (§4: 1/625 at t = 5 …). |
| C8 | L Theorem 3(b) "no statistic of outside-only segments carries information" (AN L2) | Overbroad | Restricted to a segment's own law under an R-symmetric start (§3.3). |
| C9 | X§8.4 "enumerating every possible history is unnecessary"; X§8.2 "do not use exhaustive enumeration" | Sampling-free witness checks only | Superseded by MERGE §4. Theorem A's proof needs no enumeration, but the check enumerates all 37,190 histories, not 24^t state paths. |
| C10 | X verdict NOT_COMPLETED | Separate status | Folded into INVALID (interrupted run); distinct from FAIL. |
| C11 | X and AN notation ρ(h) for the world posterior | Collided with ρ_f for y-beliefs | π(h) for the posterior; ρ_f and δ_f for y-beliefs (§0). |
| C12 | X§10 forecast "under 300 CPU-s"; L "≈ 5 CPU-min" | Pre-enumeration | ≈ 3 CPU-min forecast, 20 CPU-min ceiling (§5.4). |
| C13 | AN§7.3 "add one informed max-branch witness, coordinator picks" | Open (AN C5) | Not added as a PASS witness (MERGE §3 lists the witnesses). h_max is an enumeration probe for Conjecture F only, with values [W]. |
| C14 | AN§7.4 control "Start y = 1: witness gaps vanish" | Scope unstated | Only the named witnesses' gaps and D_t vanish. Informed histories can still have π ≠ ½ under the y = 1 start (§5.2 N3). |
| C15 | L G3(g) margin "> 10 SE" (AN L1) | Overstated | Moot: sampling is dropped (MERGE §4). |
| — | Values re-verified and unchanged | — | P(h*) = 3/100; J_C, J_M; TV 1/50 (joint and marginal); KL = (1/50)·ln 3; I = ln(27/16)/100; π(h_A) = 1/4 and π(h_B) = 3/4; P(h_r) = (9/32)·a^10 = 9/312,500,000; Q₂^dist(h_A) and Q₂^dist(h_B); pair TV 1/100; bound 1/200; h_edge TV 1/10; P(X_3 = 3) = 2a² = 0.08; gap scaling (1 − p)²/32; likelihood-ratio bound 3^{±m}; stationary P(A) = 1/8; D_5 = 1/625. |

---

## Open questions

**Owner questions** (MERGE; for the morning report, not blocking):
1. **What "topological distinction" means.** D-1 delivers orientability (w₁; equal Betti numbers). If the owner meant β₁ (square vs cylinder) or the pilot's own distinction, a different construction is needed (§1.3).
2. **Downstream.** Whether a PASS should lead to a trained-model study, and at what scale (L's 12×12 record; recurrent vs transformer; multi-step objective).

**For the coordinator or reviewer before freeze:**
3. Re-derive Conjecture F independently. Adopt it as a theorem only after that (MERGE §2).
4. Re-derive every [W] value: N_t, the §3.8 and §4 tables, h_max, and h_edge's π and mixture law.
5. Bind the module and test locations (`tools/d1_seam/`, `tests/d1_seam/` proposed), the output store, the base commit, and the protocol and request hashes.
6. Confirm K = 8 as the enumeration depth (MERGE §4) and the Decimal subset (all t ≤ 5 plus the named witnesses).
