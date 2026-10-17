STATUS: FROZEN (X6-FROZEN-v1, 2026-10-17; coordinator 75dcd488; Claude review 2026-10-15 + Codex review coord-x6-review-20261017 + v3 confirmation, its one residual fix applied verbatim)

# X6-MERGED-v3: X6 stage 0, exact observability of non-abelian holonomy on a 4×4 torus with one flux face (oracle only, no training)

| Field | Value |
|---|---|
| Protocol id | X6-MERGED-v3 |
| Role | Protocol writer (W) for the merged protocol; v2 was the fix round after the result-blind review, v3 the fix round after the Codex review of v2 (§12.7). Planning only: no Python run, no test run, no repository code run, no scientific data or store payload opened, no git write (read-only `git log/show/diff/grep` only). Two files written: this one and `X6-MERGED-v3.sha256`. v1 and v2 are left untouched |
| Date | 2026-10-17 (v1: 2026-10-15) |
| Review applied (v1→v2) | `planning/responses/coord-x6-review-20261015.claude-reviewer.md` (sha256 6571AE43…E0C6), a clean-context Claude reviewer standing in for Codex (the Codex attempt exited on its usage limit), of X6-MERGED-v1 (sha256 12DBB22C32678156408D4C04840E1D6CD423EB158FE12077806974231EE7CADD, re-checked by W against `X6-MERGED-v1.sha256`): VERDICT APPROVE_WITH_REQUIRED_CHANGES, RC1–RC6 (cited **RC n**), optional suggestions 1–9 (cited **OS n**), re-derivations Part B (cited **RV Bn**). Coordinator rulings `…/coord-x6-review-20261015.rulings.md` (sha256 356369AE…ECF6; cited **RU**): RC1–RC6 adopted as written; OS 1–9 adopted; coordinator additions (a) code binding, (b) tolerance attainability, (c) rerun and lineage rule, (d) scratch outside the project root (cited **RU (a)–(d)**). The mapping of every change to its location is in §12; the places where a reviewer text was extended are listed in §12.5; open items are in §12.6 |
| Review applied (v2→v3) | `planning/responses/coord-x6-review-20261017.codex.md` (sha256 39E64B70…7E5F), the Codex result-blind review of X6-MERGED-v2 (sha256 43550626CBBACF0B254A75CF4C9343179944F1DE616061CAF77082D96A4BD069): VERDICT APPROVE_WITH_REQUIRED_CHANGES, required changes 1–3 (cited **Codex RC n**), recommendations on O1–O6, four optional suggestions (cited **Codex OS**). Rulings `…/coord-x6-review-20261017.rulings.md` (sha256 A24CB01E…2975): RC1–RC3 adopted as written; O1–O6 accepted as recommended; all four optional suggestions adopted. Mapping in §12.7 |
| Authority | Owner addendum 11 (order: K4b, then X6); addenda 3 and 9 (as cited by RU) |
| Binding decisions | `planning/responses/coord-x6-stage0-20261015.MERGE.md`, decisions 1–11 (cited **MD n**). They are followed exactly; the mapping is in the table at the end of this header |
| Analyst | `planning/responses/coord-x6-stage0-20261015.MERGE_ANALYSIS.md` (cited **AN §n**) |
| Other inputs | Request `planning/requests/coord-x6-stage0-20261015.md` (cited **RQ**); track L `…claude.md` (skeleton, MD 1; cited **L§n**); track X `…codex.md` (grafts, MD 2; cited **X§n**); the draft `docs/proposals/X6_NONABELIAN_HOLONOMY_PROTOCOL_DRAFT.md` (cited **DR§n**); style references `D1-FROZEN-v1.md`, `X2A-FROZEN-v1.md`; the D5 commit-binding rule of `D2A-FROZEN-v1.md` §11.3 and `d2a-v2-rulings.md` (MD 11); v2 style and K4b lessons: `K4B-FROZEN-v1.md` (sha256 957F0D5E…B485) §5.6 (tolerance attainability), §11.5–§11.8 (binding, worktree, store/meter/TEMP, rerun and lineage); the scratch rule R24/R27 (`agent-handoff/archive/scratch-move-20261016/MOVE_RECORD.md`, `COORDINATOR_STATE.md`) |
| Code read for reuse claims | topo-pilot main @ `978e17f04b15b45025f5ecddf729b9b617037fa6`. W ran `git diff --name-status c364f95e5573940cdc24b569b0fb7c6a16c97ab8 978e17f -- src tools/x4_oracle_profile tests/oracle_profile`: **empty**. `tools/d1_seam` and `tools/x2a_stage0` are present on main (X's provenance note is stale, AN §0.4). Every function named in §10.3 was checked against its signature at this commit (list in §10.3). While this file was written, main advanced to `7c8da1fc2e59e4e4ed52f51531fb2c8291fc8c4b` (the C1′ merge, job 0026); W checked that its diff from 978e17f over the §8.1 protected paths is **empty** (only `docs/c1prime`, `tests/c1prime`, `tools/c1prime` and `state/` changed), so R = 978e17f remained a valid reviewed reference under the D5 rule at v1. **v2 (RU (a)):** main has since moved to **`f8e5f12b2f83ecf8b6a32189705a03ff98afa28d`** (the D-2a merge, docs, the licence commit c460e24, the K4b merge). W ran, read-only, `git diff --name-status 978e17f f8e5f12 -- <the §8.1 protected paths of v1> pyproject.toml`: **non-empty**, three entries (`M pyproject.toml`, `A src/topo_pilot/learner/multihorizon.py`, `M src/topo_pilot/learner/trainer.py`), none in a function X6 reuses (§8.1, "Review-base record"). The reviewed reference is therefore re-recorded as **R = f8e5f12** (§8.1). Every reused file is byte-identical at 978e17f, 7c8da1f (the reviewer's HEAD) and f8e5f12, so the signatures of §10.3 and the code facts of RV B14 hold at R. W also verified at f8e5f12: `winjob.MEMORY_CAP = 8 * 1024**3`; `process/emission.py` imports `point_distances` by name from `._geometry`; `is_x_periodic` is defined and called only in `process/_geometry.py`; `tools/check_file_sizes.py` walks the repository tree (`os.walk`) |
| Arithmetic | Every hand value was recomputed by W with a desk calculator (awk floating point; no Python, no repository code, no data). Values that appear in no input are marked **[W]**; v2's new hand values are in §8.7 and §11.4 C24, all marked [W]. Forecasts are marked **[H]** (L's and AN's reasoning, good to about a factor of 2). **No [W] or [H] value is a gate**: every gated quantity is computed by the run. Discrepancies with the inputs are flagged in §11.4 |
| Next step | The result-blind review (RC1–RC6, OS 1–9, RU (a)–(d)) was applied in v2; the Codex review of v2 (Codex RC1–RC3, O1–O6, four optional suggestions) is applied here (§12.7). Next: the Codex confirmation (resume of the review thread), then the freeze as X6-FROZEN-v1. Execution only after coordinator dispatch. X6 is secondary |

**Merge decisions as applied.**

| MD | Decision | Where |
|---|---|---|
| 1 | L's skeleton: W1–W3, ladder (∅, parity, counts, H1, Parikh) from one integer DP, ZC/TRIV/GAUGE/ETA1, short-window gate, β table, PF/S0/G0–G7, enumeration t ≤ 6 | §3, §4, §5, §7, §8 |
| 2 | From X: W3 at t = 32; certified enclosures with INCONCLUSIVE_NATURAL; Decimal inputs by high-precision rational division; the 4×8 static-label block comparator on the challenge family; emission-covariant gauge, no-cue null, token permutation | §4.4, §5.6, §8.4, §9.5, §6.1, §7 |
| 3 | X's second (eight-block) partition dropped; X2a analogue = X's 4×8 on the challenge + L's K-blk on the natural law; PoE descriptive only | §6 |
| 4 | O1 = the draft's: TV ≥ 0.3 per family, exact constancy, exact zero abelian spread | §8.3 |
| 5 | O2 = G_Parikh(32) ≥ 1e-3 nats **and** M_32(0.01) ≥ 1/32. No split, no lowering. GO_X6_CHALLENGE_ONLY is a legitimate outcome | §8.3, §8.4 |
| 6 | η = 1/50 frozen; 1/100 is not run | §2.5, §8.6 |
| 7 | ZC and the GAUGE arms are required controls | §7, G7 |
| 8 | W3 secondary; balanced weighting (β_rev = 0) descriptive only | §4.9 |
| 9 | Bag-of-tokens gap: designed families only; natural gap stated as not tractable | §5.5 |
| 10 | CPU measure-only (`--max-cpu inf`), one thread, TEMP on X: | §10.5 (v2: TEMP and pytest basetemp under `X:/Downloads/topo-scratch/<job>`, on X: and outside the project root, RU (d)) |
| 11 | Execution commit pinned at dispatch; S0 checks an allowlisted diff over the reused paths (D2A D5 rule) | §8.1 (v2: review base re-recorded as R = f8e5f12, RU (a); `pyproject.toml` protected, OS 7) |

**v2 additions (RU; they change no science).** Tolerance attainability (§8.7, RU (b)); rerun and lineage rule (§10.8, RU (c)); scratch outside the project root (§10.5, RU (d)); clean execution worktree (§10.7, OS 6).

## Summary (≤ 300 words)

**Question (RQ 2).** In a world whose transport is an S₃ local system that is flat on every face but one, does the exact next-symbol law at reachable histories inside the 32-symbol context depend on the **order** in which seam crossings are composed, beyond every commutative summary (parity, counts, H1, Parikh vector) and, on designed sets, beyond the bag of tokens? How large and how frequent is that dependence under the natural law?

**Construction (MD 1).** A 4×4 torus with the pilot's lazy walk (1/5 per move and stay). Arm NA: a = (01) on the x-seam, b = (12) on the y-seam; the corner face carries a 3-cycle flux. A 48-state lift redraws the fibre at rate η = 1/50. Every vertex emits its own token except the anchor (2,2), which emits the fibre. The base path is observed exactly; the fibre only through cues.

**Theorems.** A closed-form oracle; order-dependence ⟺ non-trivial flux; exact short-window blindness (no window of ≤ 7 symbols carries next-symbol order information; tight); exact zeros in the abelian arms AB and ZC.

**Witnesses.** W1 (local detour, t = 8), W2 (AB versus BA, t = 18), W3 (24 loop orderings, t = 32, multiplicities 16/4/4). Cue-normalised TVs 0.851, 0.695, 0.524 [W]; every commutative competitor is exactly constant on each set.

**Computation.** Natural quantities are exact (one integer DP), with certified log enclosures; validated by Fraction enumeration (t ≤ 6), the unchanged BayesFilter, the Decimal reference and Monte Carlo (validation only).

**Outcomes (fixed now).** GO_X6_NATURAL needs O1 and O2 (G_Parikh(32) ≥ 1e-3 nats and M_32(0.01) ≥ 1/32, certified); GO_X6_CHALLENGE_ONLY if O2 is certified to fail; INCONCLUSIVE_NATURAL if it cannot be certified; STOP_X6 if O1 fails.

**Cost.** About 15–45 CPU-min, measured only, one thread.

**Licence.** Oracle facts about one construction. Nothing about trained models; no natural bag-of-tokens claim.

---

## 0. Notation and conventions

| Symbol | Meaning |
|---|---|
| v = (x, y) ∈ Z₄² | Base vertex. Index i(v) = 4x + y (equals `QuotientLatticeBuilder`'s `x·dims[1] + y`). `divmod(i, 4) = (x, y)` |
| a★ = (2,2), i = 10 | Anchor. N(a★) = {(1,2), (3,2), (2,1), (2,3)} = indices {6, 14, 9, 11} |
| f★ | The corner face with vertex set {0, 3, 12, 15}; its local-lexicographic row in `spec.cells[2]` is (15, 12, 3, 0) |
| Fibre x ∈ {0,1,2} | Permutations are arrays g = (g[0], g[1], g[2]). Composition (g∘h)[x] = g[h[x]] |
| e, a, b, c, c², t | (0,1,2), (1,0,2), (0,2,1), (1,2,0), (2,0,1), (2,1,0). Hence a∘b = c (x ↦ x+1) and b∘a = c² = c⁻¹ |
| Lifted state | s = state(i, x) = 3i + x, 48 states. Anchor states 30, 31, 32. The 16-vertex and 48-state indexings are never conflated |
| tok(i) | i for i < 10; i − 1 for 11 ≤ i ≤ 15 (vertex tokens 0..14). The cue for fibre x is token 15 + x. V = 18 |
| η, λ_m | η = 1/50; λ_m = (1 − η)^m = (49/50)^m (rational) |
| u | Uniform law on {0,1,2} |
| Event order | Emit, then transition (`emit_then_transition`), as in BayesFilter and HMMSampler. Row vectors. t counts observed symbols; t* = 32; horizon 1 (w_33) |
| s, n, y | Time of the last cue, n = t − s its age (X's d), y its value |
| Segment γ | The base path v_s..v_t (v_s = a★), avoiding a★ at s+1..t |
| ρ(γ) | Holonomy g_{e_n}∘⋯∘g_{e_1}: edge labels in path order, the latest applied last (X's H) |
| seam letters | x⁺: (3,y)→(0,y); x⁻: (0,y)→(3,y); y⁺: (x,3)→(x,0); y⁻: (x,0)→(x,3) |
| κ(γ) = π_P(γ) | Parikh vector (k_x⁺, k_x⁻, k_y⁺, k_y⁻) of seam crossings (X's C) |
| H1(γ) | (m_x, m_y) = (k_x⁺ − k_x⁻, k_y⁺ − k_y⁻) |
| μ_m(z) | λ_m·δ_z + (1 − λ_m)·u (a "point law" of age m at image z) |
| q*_t(h) | Exact law of w_{t+1} given w_{1:t} (BayesFilter `q[:, t]`) |
| TV, KL, H | ½Σ\|p − q\|; Σ p ln(p/q); −Σ p ln p. Natural logarithms; nats |
| "cue-normalised" | Restricted to the three cue tokens and renormalised (their total is 1/5 at N(a★)) |

---

## 1. Question, motivation, scope and licence

### 1.1 Question (RQ 2a–2d)

In a world whose transport is a flat-except-one-face S₃ local system:
1. **(a) Exact observability.** Are there reachable histories with the same loop multiset, H1 class and crossing counts but different holonomy (composition order), whose next-symbol laws differ inside the 32-symbol context?
2. **(b) Competitors.** Which commutative competitors fail (∅, parity, counts, H1, Parikh; bag and bigram bag on designed sets), with what exact gap, and in which abelian arm (AB, ZC) does the order effect vanish exactly?
3. **(c) Windows and blocks.** How is the information distributed over windows k ∈ {1, 2, 4, 8} versus the full history at t ≤ 32, and what do X2a-style block comparators retain?
4. **(d) Coverage.** How frequent, under the natural law, are histories whose next-symbol law is order-sensitive?

### 1.2 Motivation (secondary programme; competing explanations)

X6 is a **secondary** programme under the owner charter ("topology richer than H1; local versus global"; owner D7; authorisation B3-E: "X6 transport starts with an exact-observability audit, not speculative training"). X2a showed that a component label could not be made exactly invisible to short windows (X2A-FROZEN-v1 Remark H); RQ notes that a locally invisible label twist (holonomy) is a route to exact short-window blindness, and that non-abelian holonomy is what separates order-dependence from H1-class dependence. Stage 0 checks, by exact computation, whether this construction delivers both before any trained stage is designed.

| Explanation for a later model's success on order-sensitive histories | Discriminating oracle observation (this protocol) |
|---|---|
| E-bag: the token multiset suffices | On W2 and W3, token and bigram multisets are equal across members while q* differs (Theorem 5; designed sets only, §5.5) |
| E-H1: the signed crossing numbers (H1 class) suffice | G_H1 > 0 in NA; G_H1 = 0 exactly in ZC (Theorem 2) |
| E-count/parity: unsigned counts or the S₃/A₃ quotient (Zhang & Li, DR§11) suffice | G_counts, G_parity > 0 in NA and ZC; G_parity = 0 in AB |
| E-Parikh: the strongest commutative statistic of the crossing word suffices | G_Parikh > 0 in NA (Theorem 2); O2 measures its natural size |
| E-short: a short window suffices | J_k = 0 exactly for k ≤ 7 (Theorem 4) |
| E-block: an order-blind aggregation of block evidence suffices | X's 4×8 comparator on W3 (§6.1); K-blk on the natural law (§6.2) |
| E-gauge: edge-label non-commutativity, not holonomy, drives the effect | GAUGE-TRIV has non-commuting edge labels and equals TRIV (Theorem 6) |

### 1.3 Scope

- Oracle only: no model, no training, no activations, no checkpoints.
- One frozen construction (§2), with no parameter search (η = 1/50, MD 6).
- Sampling is used only to validate exact computations (§9.6).
- No frozen result (D-1, X2a, B2/D-055, D2A) is reopened.

### 1.4 Licence and limits (L§9 + X§13, merged)

**Licensed sentences** (numbers in brackets are inserted from the run's exact values; exactly one outcome paragraph applies).
- *Designed sentence (GO_X6_NATURAL, GO_X6_CHALLENGE_ONLY, INCONCLUSIVE_NATURAL):* "In a 4×4-torus lazy walk carrying an S₃ local system that is flat on 15 faces with a 3-cycle flux on one, observed exactly in its base and only through anchor cues in its fibre, the exact next-symbol law depends on the order in which seam crossings are composed. Reachable histories with identical token and directed-bigram multisets, H1 class, crossing counts, permutation parity and last 8 symbols have cue-normalised next-symbol TV [0.695] (AB versus BA, t = 18) and [0.524] (24 orderings of a null-homologous commutator, t = 32). On the commutator family, with the 24 orderings equally likely, every predictor that is a function of the token bag, the directed-bigram bag, the H1 class or the crossing counts (together with the cue and the shared scaffolding) has expected excess log-loss at least [Δ_challenge] nats per readout, with equality for the optimal one. In abelian controls with the same counts (AB: a on both seams; ZC: 3-cycles) every such order effect is exactly zero. No window of at most 7 symbols carries any order information about the next symbol." (Under S8 the last clause is kept only as §8.5 S8 states.)
- *Natural sentence (GO_X6_NATURAL only; X§13):* "Under the stationary natural-history distribution, the Bayes predictor given the last cue, its age, the current vertex and the four directed seam-crossing counts since the cue (the finest commutative statistic of the crossing word; it refines parity, unsigned counts and the H1 class) has excess log-loss G_Parikh(32) = [ ] nats at t = 32, and a fraction [M_32] of histories have full-vocabulary row-KL to it of at least 0.01 nats (certified enclosures). Every predictor that is a function of that statistic has excess log-loss at least G_Parikh(32)."
- *GO_X6_CHALLENGE_ONLY adds:* "The natural non-commutative signal did not meet the preregistered screen (certified); any trained claim is restricted to the designed distribution."
- *INCONCLUSIVE_NATURAL adds:* "The natural screen could not be decided [at the certified precision | within the resource limits]; no natural claim is made."
- *STOP_X6:* "This construction did not meet the preregistered designed-observability criteria O1: [reason]."

**Stage 0 cannot establish** (union of L§9 and X§13):
- anything about trained models: learnability, representation, causal use, or whether a model composes in order;
- that a neural representation has the topology of the base or of the cover; or that a model "knows" the surface is punctured. The base is visible by design and the topology lies in the connection; a small finite-state automaton composing S₃ in order solves the task (DR§12);
- the natural-distribution gap of bag-of-tokens or bigram-bag predictors (designed-only, MD 9);
- exclusion, under the natural law, of order-blind mechanisms that are not functions of R_Parikh (for example a bag of tokens); only the designed sets exclude those;
- that all H1-related or short-block algorithms fail; that non-abelian transport is necessary for every form of long memory; that local flux is evidence of a learned sheaf obstruction;
- that order-dependence persists under other η, L, anchors, emission rules or noisy bases; any population claim over seeds;
- anything about the original square/cylinder pilot question.

Further limits:
- Designed templates are individually rare (§4.6) and are never presented as natural.
- Zhang & Li are checked against their abstract only (DR§11); stage 0 computes only the parity (S₃/A₃) competitor exactly.
- Stage-0 Monte Carlo histories are oracle-only and must not serve as a trained-stage test set.
- A GO supports designing a later trained-stage protocol. It does **not** authorise training.

---

## 2. Exact construction (MD 1; L§2 = X§3, identical model, AN §0.1)

### 2.1 Base world: local, unregistered torus builder (D-1 / X2a pattern)

```python
class _X6TorusBuilder(QuotientLatticeBuilder):            # deliberately NOT @register_world
    family: ClassVar[str] = "_x6_torus_local"
    expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
    identifications: ClassVar[tuple] = (Identification(0, "periodic"), Identification(1, "periodic"))
```

Validation mirrors `build_world`, as in X2a §2.1:
1. `spec = _X6TorusBuilder().build(WorldConfig("_x6_torus_local", (4, 4), "flat"))`. The builder raises BETTI_MISMATCH unless the Betti numbers are (1,2,1) over GF(2) and GF(3).
2. `spec.validate()`.
3. `check_boundary_closed(CubicalComplex(spec.n_states, spec.cells))`.
4. `check_flat_bounds(spec.dist, spec.dist_graph, 2)`.

At dims (4,4) this is the lattice that `tests/world/test_world.py` already builds as `_t_torus` (16/32/16 cells). WORLD_REGISTRY is never mutated; `process._geometry.point_distances` and `is_x_periodic` are never called.

### 2.2 Punctured complex (the transport complex; the walk stays on the full torus)

```python
f_star = [r for r in range(len(spec.cells[2])) if sorted(spec.cells[2][r]) == [0, 3, 12, 15]]   # one row: (15, 12, 3, 0)
punct = CubicalComplex(16, {0: spec.cells[0], 1: spec.cells[1], 2: np.delete(spec.cells[2], f_star, axis=0)})
```

Expected: cell counts (16, 32, 15); χ = −1; Betti (1, 2, 0) over GF(2) and GF(3); ∂₁∂₂ = 0; the four edges of f★ are the only edges lying in exactly one 2-cell, and they form one cycle (one boundary component, X§3.1). No second `WorldSpec` is built; only the public `CubicalComplex` is used.

### 2.3 S₃ arrays (X§3.2)

```text
e = (0,1,2)   a = (1,0,2)  # (01)    b = (0,2,1)  # (12)
c = (1,2,0)   c2 = (2,0,1)           t = (2,1,0)  # (02)
compose(g, h)[x] = g[h[x]]      inverse(g)[g[x]] = x
S3_LIST = (e, a, b, c, c2, t)   # listing order used by the gauge arrays
```

For successive edge maps g₁, …, g_n, ρ = g_n∘⋯∘g₁. A row-vector point law δ_y moved by P_g becomes δ_{g[y]}, so this is exactly the order in which a forward filter applies them.

### 2.4 Seams, connection arrays and arms (explicit)

```python
def seam_letter(i, j):                  # directed base edge i -> j, i != j
    (xi, yi), (xj, yj) = divmod(i, 4), divmod(j, 4)
    if yi == yj and (xi, xj) == (3, 0): return "x+"
    if yi == yj and (xi, xj) == (0, 3): return "x-"
    if xi == xj and (yi, yj) == (3, 0): return "y+"
    if xi == xj and (yi, yj) == (0, 3): return "y-"
    return None                         # interior edge: label e
```

Directed seam edges in the + direction: x-seam 12→0, 13→1, 14→2, 15→3; y-seam 3→0, 7→4, 11→8, 15→12. Every other edge and every self-loop carries e in the seam-supported arms.

| Arm | x⁺ / x⁻ | y⁺ / y⁻ | Role |
|---|---|---|---|
| **NA** | a / a | b / b | Experiment. Non-abelian; flux c at f★ |
| **AB** | a / a | a / a | Abelian control with the same counts (RQ 2b). Flat on all 16 faces |
| **ZC** | c / c² | c / c² | Abelian control where H1 is sufficient but parity and unsigned counts are not |
| **TRIV** | e / e | e / e | Null |
| **ETA1** | NA labels, η = 1 | | Null: fibre redrawn at every step (X's ε = 1) |
| **GAUGE-NA** | g′_{u→v} = h_fix(v)∘g^{NA}_{u→v}∘h_fix(u)⁻¹ | | Gauge-equivalent to NA, anchor not relabelled; must equal NA |
| **GAUGE-TRIV** | g′_{u→v} = h_fix(v)∘h_fix(u)⁻¹ | | Pure gauge with non-commuting edge labels; must equal TRIV |
| **GAUGE-COV** | g′_{u→v} = h_cov(v)∘g^{NA}_{u→v}∘h_cov(u)⁻¹, with the emission transformed (§2.6) | | X§8's emission-covariant gauge, h_cov(a★) ≠ e; must equal NA |

Positive-direction label arrays for NA, rows indexed by x, columns by y (X§3.3): `G_plus_x[x][y]` labels (x,y)→(x+1,y); `G_plus_y[x][y]` labels (x,y)→(x,y+1); reverse edges carry the inverse.

```text
G_plus_x = [[e,e,e,e],[e,e,e,e],[e,e,e,e],[a,a,a,a]]
G_plus_y = [[e,e,e,b],[e,e,e,b],[e,e,e,b],[e,e,e,b]]
```

AB replaces b by a. ZC puts c in place of every seam entry of both arrays (so the reverse edges carry c²).

Gauge arrays (index i = 0..15), from S3_LIST[i mod 6]:

```text
h_cov = (e, a, b, c, c2, t, e, a, b, c, c2, t, e, a, b, c)     # h_cov(10) = c2
h_fix = h_cov with h_fix(10) = e                               # anchor never relabelled
```

Self-loops carry h(i)∘e∘h(i)⁻¹ = e in every gauge arm, so the lift's convention g_{i→i} = e is consistent.

**Seam-supported arms** are NA, AB, ZC, TRIV (and ETA1, which has NA's labels). The competitor ladder and K-blk (§5, §6.2) are defined only for these: in the gauge arms, the holonomy of an open segment is gauge-dependent, so only their observation laws are compared (§7).

### 2.5 Kernel and 48-state lift (η = 1/50 frozen, MD 6)

`T_base = TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T` (16×16). Every degree is 4, so T(v, v′) = 1/5 for each neighbour and for the stay. The exact model uses Fraction(1, 5). Neighbour table (X§3.1, re-checked by W):

| v | +x | −x | +y | −y | stay | | v | +x | −x | +y | −y | stay |
|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 12 | 1 | 3 | 0 | | 8 | 12 | 4 | 9 | 11 | 8 |
| 1 | 5 | 13 | 2 | 0 | 1 | | 9 | 13 | 5 | 10 | 8 | 9 |
| 2 | 6 | 14 | 3 | 1 | 2 | | 10 | 14 | 6 | 11 | 9 | 10 |
| 3 | 7 | 15 | 0 | 2 | 3 | | 11 | 15 | 7 | 8 | 10 | 11 |
| 4 | 8 | 0 | 5 | 7 | 4 | | 12 | 0 | 8 | 13 | 15 | 12 |
| 5 | 9 | 1 | 6 | 4 | 5 | | 13 | 1 | 9 | 14 | 12 | 13 |
| 6 | 10 | 2 | 7 | 5 | 6 | | 14 | 2 | 10 | 15 | 13 | 14 |
| 7 | 11 | 3 | 4 | 6 | 7 | | 15 | 3 | 11 | 12 | 14 | 15 |

  T_lift[3i + x, 3j + x′] = T_base[i, j]·((1 − η)·1{x′ = g_{i→j}[x]} + η/3),  g_{i→i} = e.

- Exact entries at η = 1/50: (1/5)(49/50 + 1/150) = **74/375** on the transported fibre and (1/5)(1/150) = **1/750** on each other fibre; 0 off the base support. ETA1 (η = 1): 1/15 on each of the three fibres.
- Row sums 5·(74/375 + 2/750) = 1. Column sums Σ_i T_base[i, j] = 1, so T_lift is doubly stochastic.
- Start π = 1/48, stationary.
- The float64 arrays handed to the production kernels are the Fractions converted once (`float(Fraction)`); they are the inputs of BayesFilter and HMMSampler. The rational model is the reference (§9).

### 2.6 Emissions

| Array | Definition | Use |
|---|---|---|
| E [48, 18] | E[3i + x, tok(i)] = 1 for i ≠ 10; E[30 + x, 15 + x] = 1 (cue reveals x with r = 1) | All arms except NOCUE and GAUGE-COV |
| E_cov [48, 18] | E_cov[3i + x′, ·] = E[3i + h_cov(i)⁻¹[x′], ·]; the anchor state (10, x′) emits cue 15 + c[x′] (since h_cov(10)⁻¹ = c) | GAUGE-COV |
| E_nc [48, 16] | E_nc[3i + x, i] = 1 (one token per vertex, anchor included; the alphabet change is explicit) | NOCUE null |
| E_σ [48, 18] | E_σ[s, σ_tok(w)] = E[s, w], with σ_tok(w) = (w + 7) mod 15 for w ≤ 14 and σ_tok(w) = w for w ∈ {15, 16, 17} | TOKPERM control |

Every observation identifies its base vertex. The fibre is hidden away from the anchor.

### 2.7 Local model record (no registry, no `src/` change)

A local record per arm holds `T_base`, `T_lift`, `E` (or variant), `pi`, the labels, the state map `state(i, x) = 3i + x`, and the puncture metadata. It is assembled by small local functions (`edge_labels(arm)`, `lift(T_base, labels, eta)`, `emission(kind)`), never as a registered world. The 48 hidden states are not presented as vertices of a base world (X§3.6).

### 2.8 Why this design (AN §2)

- The base path is exactly readable, so ρ(γ) is a deterministic function of the observations, and "same Parikh class, different holonomy" is a well-defined event on observations. This gives the closed form, exact class matching and the exact natural DP. An aliased base would lose all three.
- It is **not degenerate** for the order question (MD "Verified"): a learner must recognise seam crossings as specific anonymous bigrams among 32 edges plus stays, compose S₃ in order over up to 31 steps, and apply the λ decay. It **does** trivialise base-geometry learning and any "topology inference" reading (§1.4).
- The realism limiter for a later stage is readout sparsity (cue entry only from N(a★), total cue mass 1/5, mean return time to a★ 16 steps), not the emission alphabet. η changes λ, not the ambiguity mass (AN §2).

---

## 3. Theorems and proofs (each is checked exactly by the run)

**Lemma 0 (structure).** In every seam-supported arm with seam labels g_x (x⁺; x⁻ carries g_x⁻¹) and g_y:
1. the 15 faces other than f★ are flat;
2. the flux of f★, traversed 15→3→0→12→15 (letters x⁺, y⁺, x⁻, y⁻), is g_y⁻¹∘g_x⁻¹∘g_y∘g_x.

Under NA it is b∘a∘b∘a = (c²)² = **c**. Under AB it is a⁴ = e; under ZC c²∘c²∘c∘c = e; under TRIV e.

*Proof.* A face with base (3, y), y ≤ 2, has edges (3,y)→(0,y) [x⁺, g_x], (0,y)→(0,y+1) [e], (0,y+1)→(3,y+1) [x⁻, g_x⁻¹], (3,y+1)→(3,y) [e]; its holonomy is g_x⁻¹∘g_x = e. Faces with base (x, 3), x ≤ 2, give g_y⁻¹∘g_y = e by the same argument. Interior faces carry only e. The corner face crosses both seams once in each direction in the stated order. ∎

**Lemma 0′ (cover certificate).** Let the cover be the 3-sheeted cover of the punctured complex T° defined by the arm's labels: vertices (i, x), edges (i, x)–(j, g_{i→j}[x]) for the 32 base edges, and, for each of the 15 retained faces and each x, the lifted square obtained by transporting x from the face's first corner (flatness makes it close). Then:
- counts (48, 96, 45), χ = 3·χ(T°) = −3, β₂ = 0, so β₁ = β₀ + 3;
- β₀ = the number of orbits of the monodromy group on {0,1,2}: NA 1 (S₃), ZC 1 (A₃), AB 2 ({0,1}, {2}), TRIV 3;
- boundary circles = orbits of the flux on {0,1,2}: NA 1 (3-cycle); ZC, AB, TRIV 3.

| Arm | Betti (GF(2) and GF(3)) | Surface |
|---|---|---|
| NA | (1,4,0) | genus 2, 1 boundary circle (χ = 2 − 2·2 − 1) |
| ZC | (1,4,0) | genus 1, 3 boundary circles (χ = 2 − 2·1 − 3) |
| AB | (2,5,0) | two components |
| TRIV | (3,6,0) | three components |

*Proof.* A finite cover multiplies χ. A cover of a connected surface with non-empty boundary is a surface with boundary, hence homotopy-equivalent to a graph: torsion-free, β₂ = 0. Components correspond to orbits of the monodromy; boundary circles over ∂f★ to cycles of the flux permutation. ∎

NA and ZC have **equal** cover Betti numbers; only the boundary count (the flux) and the order test separate them (L D10).

**Lemma 1 (observed base, no leak).** In every seam-supported arm using the standard emission E of §2.6:
1. the base path v_{1:t} is a deterministic function of w_{1:t} (tokens identify vertices; any cue identifies a★);
2. the base process is the lazy walk with uniform start: the base marginal of each T_lift row is T_base whatever x is;
3. off the anchor, emissions do not depend on the fibre;
4. given the base path, the fibre is a time-inhomogeneous Markov chain with kernels K_g = (1 − η)P_g + ηU (U has every row u), started from u.

Hence I(X_t; W_{1:t}) = 0 on histories with no cue, and all fibre information comes from cue values transported along the observed path. *Proof.* Σ_{x′} T_lift[3i + x, 3j + x′] = T_base[i, j]. uP_g = u and βU = u for every probability vector β, so the fibre law stays u until the first cue. ∎

**Theorem 1 (closed-form oracle).** For a seam-supported arm using the standard emission E, let s be the last cue time, y its value, n = t − s ≥ 0, and ρ = ρ(γ). Then

  P(x_t = · | w_{1:t}) = μ_n(ρ[y]) = λ_n·δ_{ρ[y]} + (1 − λ_n)·u,

and the fibre posterior is u if there is no cue. If v_t ∈ N(a★), the next-symbol law gives 1/5 to each of the three non-anchor moves and the stay (vertex tokens), and gives cue token 15 + z the probability (1/5)·μ_{n+1}(ρ[y])(z). If v_t = a★ (n = 0), the stay gives cue law (1/5)·μ_1(y). Otherwise q* does not depend on the fibre.

The history probability is

  P(h) = (1/16)·5^{−(t−1)}·(1/3)·Π_{j≥2} [λ_{Δ_j}·1{y_j = ρ_j[y_{j−1}]} + (1 − λ_{Δ_j})/3]

over the successive cues j (gaps Δ_j, segment holonomies ρ_j), and (1/16)·5^{−(t−1)} with no cue.

*Proof.* At s the hidden state is exactly (a★, y) (r = 1). By the Markov property and Lemma 1(4), the fibre at t has law δ_y K_{g_1}⋯K_{g_n}. Since δ_z K_g = (1 − η)δ_{g[z]} + ηu and uK_g = u, induction gives δ_y K_{g_1}⋯K_{g_k} = λ_k δ_{(g_k∘⋯∘g_1)[y]} + (1 − λ_k)u. Anchor-avoidance is a base event, independent of the fibre given the base path. The edge from N(a★) into a★ is interior, so it carries e and adds one factor λ. The history probability multiplies the base-path probability (uniform start, 1/5 per step), the first cue's 1/3, and each later cue's transported law. ∎

**Theorem 2 (characterisation of order-dependence).** For a seam-supported arm with labels g_x, g_y, standard emission E and η = 1/50, the following are equivalent:
1. g_x∘g_y = g_y∘g_x;
2. the flux of f★ is e;
3. for every n, end vertex v and H1 class, all anchor-based segments in the class have the same holonomy, namely g_y^{m_y}∘g_x^{m_x};
4. q* = q_H1 at every reachable history;
5. q* = q_Parikh at every reachable history (competitors as in §5.1).

If they fail, W1 (§4.1) is a reachable witness with TV(q*(W1-U), q*(W1-D)) = (λ_8/5)·1{ρ_U[y] ≠ ρ_D[y]}; under NA this is λ_8/5 for every y.

*Proof.*
- 1 ⟺ 2: Lemma 0(2).
- 1 ⇒ 3: ρ is the product of the seam letters in path order (interior edges carry e). Commuting letters collect into g_x^{k_x⁺ − k_x⁻}∘g_y^{k_y⁺ − k_y⁻}.
- 3 ⇒ 4: by Theorem 1, q* depends on the segment only through ρ, which by 3 is a function of R_H1; so q* is R_H1-measurable and q_H1 = E[q* | R_H1] = q*.
- 4 ⇒ 5: R_Parikh refines R_H1, so q* is also R_Parikh-measurable.
- ¬1 ⇒ ¬5: W1-U and W1-D share n, end vertex, prefix and Parikh vector (one x⁺, one y⁺), with holonomies g_y∘g_x and g_x∘g_y. If these differ, their quotient is a non-identity permutation, which moves some y; by Theorem 1 the cue laws differ there, so q* is not R_Parikh-measurable. Under NA the quotient is a 3-cycle, which moves every y. ∎

The restriction η < 1 is essential for the predictive equivalences: ETA1 has NA’s non-trivial flux but q* = q_H1 = q_Parikh everywhere because every transition redraws the fibre uniformly. The tightness and positive order-information statements below concern NA at η = 1/50. Gauge-arm oracle laws are obtained by the state and emission relabellings of Theorem 6; NOCUE is treated separately in §7.

**Corollaries.**
- AB: ρ = a^{k_x + k_y}, a function of the parity statistic, so q_parity = q* and G_parity = G_counts = G_H1 = G_Parikh = 0.
- ZC: ρ = c^{m_x + m_y}. H1 is sufficient. Parity and unsigned counts are not. Witness (L, AN §1.5): two n = 7 segments ending at (1,2) = 6, both with k_x = 1, k_y = 0:
  - 10→14→2→6, then 4 stays (the crossing 14→2 is x⁺, holonomy c);
  - 10→9→5→1→13→9→5→6 (the crossing 1→13 is x⁻, holonomy c²).
- NA: q* ≠ q_Parikh at W1.
- The parity statistic is (k_x⁺ + k_x⁻ + k_y⁺ + k_y⁻) mod 2. It equals sign ρ in NA and AB; in ZC every holonomy is even (§11.4 C6).

**Lemma I (image-level ambiguity).** A competitor class is *ambiguous at y* if its members' images ρ[y] take at least two values with positive weight (X§7.5: distinct permutations need not give distinct predictions). In NA, for S ∈ {parity, counts, H1, Parikh}, a class is ambiguous at y iff it contains two distinct holonomies, for every y. For S = ∅ this fails (example: AB, holonomies e and a, y = 2, since a fixes 2).
*Proof.* Each of these statistics fixes the parity of k = k_x + k_y (H1: m ≡ k mod 2), and in NA sign ρ = (−1)^k. Two distinct holonomies of equal sign differ by a non-identity even permutation, a 3-cycle, which has no fixed point; so their images differ at every y. ∎ The run uses the image-level definition everywhere.

**Theorem 3 (π₁ reading; remark, not separately gated).** Under NA the representation factors through π₁(T°, p) ≅ F₂ = ⟨A, B⟩ with A ↦ a, B ↦ b. Its image is S₃, and the commutator, null in H₁, maps to (b∘a)^{±2} ≠ e. Every arm flat on all 16 faces factors through π₁(T²) = Z², so its image is abelian and Theorem 2 applies. The order-dependence of long loops (W3) and of the single local detour (W1) are the same object, the flux of one face, seen globally and locally (non-abelian Stokes); the commutator holonomy c is conjugate to the flux.

**Theorem 4 (exact short-window blindness to order; L Theorem 4, verified tight by AN §1.4).**
- **(a) Windows without a cue** give exactly the uniform fibre posterior under stationary restart (Lemma 1).
- **(b) Fibre level.** A Parikh class contains more than one holonomy only if its segments cross **both** seams (one-letter words commute). Crossing both seams from a★ needs ≥ 2 x-moves (2→3→0) and ≥ 2 y-moves, so n ≥ 4. *Attained:* 10→14→2→3→0 (letters a, b; ρ = c²) versus 10→11→8→12→0 (letters b, a; ρ = c), both avoiding a★, same Parikh vector and end vertex. Hence **no window with k ≤ 4 symbols carries non-commutative fibre information** (J^fib_k = 0 for k ≤ 4).
- **(c) Next-symbol level (horizon 1).** The end vertex must lie in N(a★), where exactly one coordinate is ≢ 2 (mod 4). Lift the path to Z² from (2,2). A coordinate whose seam is crossed needs ≥ 3 moves to end ≡ 1 or 3 (2→3→4→5, 2→3→4→3, 2→1→0→−1) and ≥ 4 moves to end ≡ 2 (2→3→4→5→6, 2→3→4→3→2). So n ≥ 3 + 4 = 7; stays only lengthen n. *Attained by W1:* 10→14→15→3→0→4→5→6 (x: 2→3→4→5; y: 2→3→4→5→6).

  **No window of ≤ 7 symbols carries any non-commutative next-symbol information (J_k = 0 for k ≤ 7); windows with k = 8 can, but only through n = 7 segments.** ∎

**Corollary 4′ (k-gram locality; G1).** The stationary k-gram laws of NA, AB, ZC and TRIV are identical for k ≤ 4 and differ for k = 5. *Proof.* A k-gram's law can depend on the arm only through two or more cues in the window. Two cues ≤ 4 symbols apart are joined by an anchor-to-anchor path of ≤ 3 transitions. By bipartiteness (parity of x + y) such a path has 0 or 2 moves; both edges at a★ are interior, and reaching a seam edge and returning needs ≥ 4 moves. So its holonomy is e in every arm, and λ is the same. For k = 5, the path 10→11→8→9→10 (crossing 11→8, y⁺) gives the 5-gram [15+y, 10, 8, 9, 15+y′] with weight (1/48)·5⁻⁴·[λ_4·1{y′ = g_y[y]} + (1 − λ_4)/3]. The y-seam labels b, a, c, e of NA, AB, ZC, TRIV are pairwise distinct, so every pair of arms differs at some y, with probability ratio (λ_4 + (1 − λ_4)/3)/((1 − λ_4)/3) ≈ 36.6 [W] (λ_4 = 0.9223682 [W]). ETA1 differs from NA already at k = 2 (cue, stay, cue) and is excluded from the equality. ∎

**Theorem 5 (designed sets; §4 for the families).** Within each family, for fixed y and prefix:
1. all members have equal probability, P(prefix ending at (a★, y))·5^{−n};
2. all members share length, n, end vertex, Parikh vector, H1 class, unsigned counts and parity, and a common tail (W1: 4 tokens; W2: 8; W3: 9);
3. **W2 and W3:** the token multisets are equal and so are the **directed-bigram multisets**, because swapping closed loops at a common vertex permutes whole edge lists (L D3; AN §1.5). The trigram multisets differ at the joints;
4. hence every competitor that is a function of the matched statistics is constant on the set. That includes every Bayes k-window predictor with k ≤ n, blind by Theorem 4(a);
5. the oracle cue laws are μ_{n+1}(ρ[y]). Different holonomies give different images (3-cycles have no fixed point), and the cue-normalised TV between members of different holonomy is λ_{n+1}·TV(δ_z, δ_{z′}) = **λ_{n+1}**; the full-vocabulary TV is λ_{n+1}/5;
6. in AB, ZC, TRIV and GAUGE-TRIV the within-set spread of q* is exactly 0 (Theorem 2; AB: every family's words reduce to a^{even} = e).

*Proof.* 1–2: by construction (§4) and Theorem 1. 3: each loop starts and ends at p, so concatenations in any order contain the same directed edges. 4: immediate. 5: Theorem 1. 6: Theorem 2 and Theorem 6. ∎

**Theorem 6 (gauge).**
- *(a) Anchor-fixed gauge (L).* For h with h(a★) = e, let P_h map (i, x) ↦ (i, h(i)[x]). Then T′ = P_h⁻¹T_lift P_h is the lift of the labels h(v)∘g∘h(u)⁻¹; E′ = P_h⁻¹E = E (rows off the anchor are constant across the fibre, and h(a★) = e); π′ = π. The observation laws are identical. GAUGE-NA ≡ NA; GAUGE-TRIV ≡ TRIV although its edge labels do not commute (for example the edge 0→1 carries a and the edge 1→2 carries b∘a = c², which do not commute).
- *(b) Emission-covariant gauge (X§8).* For any h, the same state relabelling with E′(i, x′) = E(i, h(i)⁻¹[x′]) is a relabelling of hidden states, so the observation law is unchanged. GAUGE-COV ≡ NA with h_cov(a★) = c² ≠ e.
- Changing only the connection and not the emission is a different model, not a gauge test (X§8).

*Proof.* T′[(u, h_u[x]), (v, h_v[x′])] = T[(u, x), (v, x′)] = T_base(u, v)[(1 − η)1{h_v⁻¹[y′] = g[h_u⁻¹[y]]} + η/3], and 1{h_v⁻¹[y′] = g[h_u⁻¹[y]]} = 1{y′ = (h_v∘g∘h_u⁻¹)[y]}; the uniform redraw is invariant under conjugation by permutations; π is uniform. The observation law is the image of the hidden-path law under the emission, and the relabelling is a bijection on hidden paths that preserves each path's emission. ∎

**Theorem 7 (exact natural law; basis of the DP).** Under the stationary process at time t, for 1 ≤ n ≤ t − 1, each (y, segment γ) with γ anchor-avoiding of length n from a★ has probability (1/48)·5^{−n}. The case n = 0 (v_t = a★) has probability 1/16. The remaining mass is P(no cue in 1..t). Let A_n be the number of anchor-avoiding n-step paths from a★ and D_m(v) the number of m-step paths from v ≠ a★ avoiding a★ entirely. Then (total-mass identity)

  1/16 + Σ_{n=1}^{t−1} A_n/(16·5^n) + Σ_{v ≠ a★} D_{t−1}(v)/(16·5^{t−1}) = 1.

Every predictive and fibre quantity is a function of (n, y, v_t, segment statistic, ρ); contributions with n ≤ t − 1 do not depend on t, so every natural gap G(t) is a cumulative sum Σ_{n=1}^{t−1} g(n).
*Proof.* P(v_s = a★, x_s = y) = 1/48 by stationarity. The segment is independent of everything before s given (a★, y), each step has probability 1/5, and anchor avoidance makes s the last cue. The three cases (last cue at n ≥ 1, at n = 0, no cue) partition the histories. ∎ Small values [W] (exact; below 2⁵³): A_1..A_8 = 4, 16, 76, 352, 1684, 7984, 38236, 182464. A_31 ≈ 7.9 × 10²⁰ [W] > 2⁶⁴, so fixed-width integers would overflow (X§7.4): exact Python integers are mandatory.

**Theorem 8 (block-commutative comparator; L Theorem 8).** K-blk (§6.2) knows R_∅ and the **unordered multiset** of the segment's block holonomies. In every abelian seam-supported arm, D_blk = 0, because the product of a multiset of commuting elements does not depend on the order. Under NA, D_blk(32) > 0.
*Witness [W, explicit].* Cue at s = 16 (positions 17–24 form block 3; 25–32 block 4). Path U: 10→14→15→3 (landing at 17, 18, 19; 15→3 is x⁺, a), 5 stays at 3 (20–24), 3→0 (25; y⁺, b), 0→4→5→6 (26–28), 4 stays at 6 (29–32). Path D: the same, with 15→12 (19; y⁺, b), stays at 12, and 12→0 (25; x⁺, a). Both have n = 16, end at 6 ∈ N(a★), avoid a★, share the prefix, and have block multiset {a, b}; their holonomies are b∘a = c² and a∘b = c. So the K-blk class is ambiguous at every y and has positive mass. ∎

**Remark B (bipartiteness; AN §1.5).** Z₄×Z₄ without stays is bipartite by the parity of x + y; p = (1,1) is even and N(a★) is odd, so no **stay-free** 8-step path joins them. The draft never forbids stays: W3's suffix (7 stays, then p→u) is legal. This is a remark, not a draft error.

---

## 4. Witness families (MD 1, MD 2, MD 8)

The cue at t = 1 has value y ∈ {0,1,2}. Each family is instantiated for all three y (y-balanced) and checked per y. Vertex sequences are listed after the cue; tokens follow from tok.

### 4.1 W1: local detour round f★ (the shortest possible; n = 7, readout t = 8)

- W1-U: 14, 15, **3**, 0, 4, 5, 6. Crossings 15→3 (x⁺) then 3→0 (y⁺). ρ_U = b∘a = c².
- W1-D: 14, 15, **12**, 0, 4, 5, 6. Crossings 15→12 (y⁺) then 12→0 (x⁺). ρ_D = a∘b = c.
- Tokens: [15+y, 13, 14, **3**, 0, 4, 5, 6] versus [15+y, 13, 14, **11**, 0, 4, 5, 6]. The two members differ by one face. Common tail: 4 tokens. Not bag-matched (token 3 versus 11).

### 4.2 Loops at p = (1,1) = 5 (X§5.1 = L§2.4)

| Loop (X / L name) | Vertices | Tokens | Crossing | NA letter |
|---|---|---|---|---|
| A⁺ / A | 9, 13, 1, 5 | 9, 12, 1, 5 | 13→1 (x⁺) | a |
| A⁻ / A′ | 1, 13, 9, 5 | 1, 12, 9, 5 | 1→13 (x⁻) | a |
| B⁺ / B | 6, 7, 4, 5 | 6, 7, 4, 5 | 7→4 (y⁺) | b |
| B⁻ / B′ | 4, 7, 6, 5 | 4, 7, 6, 5 | 4→7 (y⁻) | b |

No loop visits a★. Under NA, A± both carry a and B± both carry b (involutions; L D4).

### 4.3 W2: AB versus BA (n = 17, readout t = 18; L)

Approach a★→9→5; then XY with {X, Y} = {A⁺, B⁺}; then S7 = 1, 2, 3, 7, 11, 15, 14 (seam-free, avoids a★, ends at (3,2) ∈ N(a★)).
- ρ_AB = b∘a = c²; ρ_BA = a∘b = c.
- AB tokens: [15+y, 9, 5, 9, 12, 1, 5, 6, 7, 4, 5, 1, 2, 3, 7, 10, 14, 13]; BA swaps the two 4-token loop blocks. Common tail: 8 tokens (p, then S7).

### 4.4 W3: the null-homologous commutator, canonical at t = 32 (X§5; MD 2)

Positions: 1 cue at a★; 2 u = (1,2) = 6; 3 p = 5; 4–8 five stays at p; 9–24 the four loops {A⁺, A⁻, B⁺, B⁻} in one of the 24 orders; 25–31 seven stays at p; 32 p→u = 6 ∈ N(a★). n = 31, readout uses λ_32.
- Tokens: [15+y, 6, 5, 5, 5, 5, 5, 5, ⟨16 loop tokens⟩, 5, 5, 5, 5, 5, 5, 5, 6].
- The seam word in path order is one of aabb, abba, baab, bbaa (holonomy e; 16 orderings), abab (b∘a∘b∘a = c; 4 orderings) or baba (a∘b∘a∘b = c²; 4 orderings) (AN §1.1). Examples: A⁺B⁺A⁻B⁻ ↦ c; B⁺A⁺B⁻A⁻ ↦ c². The draft's "ABA⁻¹B⁻¹ ↦ c²" uses the opposite product convention; it is not an error.
- Common tail: the last **9** tokens (positions 24–32). No path revisits a★ after the cue. Each member has probability (1/48)·5^{−31}.
- **W3′ cross-check (L's t = 26 instance; exact, reported, not part of O1):** approach 9, 5; the 24 orderings; S7. n = 25, TV λ_26.

### 4.5 Prefixes (prefix invariance on W1 and W2; L)

Token sequences placed before the family's cue (each ends adjacent to a★):
- Π0 = ∅; Π1 = [10] (vertex (2,3)); Π3 = [6, 5, 9] (vertices 6, 5, 9);
- Π6 = [15+y₀, 13, 12, 9, 5, 9]: an earlier cue y₀ ∈ {0,1,2}, then the seam-free path 14, 13, 9, 5, 9.

With Π6, W1 reads out at t = 14 and W2 at t = 24. By Theorem 1, q* at the readout is unchanged under every prefix.

### 4.6 Exact values ([W], all reproduced from L, X and AN; §11.4)

| Family | Readout t | n | Cue-normalised TV = λ_{n+1} | Full TV = λ_{n+1}/5 | Set gap of the best set-constant predictor (nats, full vocabulary) | P(one member), Π0 |
|---|---|---|---|---|---|---|
| W1 | 8 | 7 | 49⁸/50⁸ = **0.8507630** | 0.1701526 | 0.092701 | (1/48)·5⁻⁷ = 2.6667e-7 |
| W2 | 18 | 17 | **0.6951353** | 0.1390271 | 0.061119 | 2.7307e-14 |
| W3 (t = 32) | 32 | 31 | **0.5238831** | 0.1047766 | **Δ_challenge = 0.037832** (16/4/4 mixture) | 4.4739e-24 |
| W3′ (t = 26) | 26 | 25 | 0.5913954 | 0.1182791 | 0.048459 | 6.9905e-20 |

- Set gap = mean over members of KL(q*_member ‖ q̄) = (1/5)[H(μ̄) − H(μ_{n+1})], with μ̄ the members' mixture. Two-member families: μ̄ = ((1−L)/3, (1−L)/3 + L/2, (1−L)/3 + L/2) in coordinates (y, y+1, y+2). The 16/4/4 family: μ̄ = q̄ = ((1+L)/3, (2−L)/6, (2−L)/6), and every member's law is a permutation of q_L = ((1+2L)/3, (1−L)/3, (1−L)/3) (X§6.1). At L = λ_32: H(q̄) = 1.034076, H(q_L) = 0.844915, Δ_cue = 0.189160, Δ_challenge = Δ_cue/5 = 0.037832 [W].
- Natural template frequencies (any y and member, template ending at t = 32): W1 6/(48·5⁷) = 1.6e-6; W2 6/(48·5¹⁷) = 1.638e-13; W3′ 72/(48·5²⁵) = 5.03e-18; W3 72/(48·5³¹) = 24/(16·5³¹) = 3.22e-22 [W]. Among the 72 canonical W3 histories, the non-identity fraction is exactly 1/3.
- Every member of each family is reachable in every arm (support is common because η > 0).
- **Posterior isolation (D-1 pattern).** Within a pair, the base beliefs are the same δ_v and the fibre posteriors have the same shape; they differ only by the permutation ρ_U∘ρ_D⁻¹, a 3-cycle conjugate to the flux.

### 4.7 Matched statistics and competitor constancy (Theorem 5)

| Statistic or competitor | W1 | W2 | W3 (t = 32) |
|---|---|---|---|
| length, n, end vertex, prefix, cue y | equal | equal | equal |
| Parikh vector, H1, unsigned counts, parity | equal (1,0,1,0) | equal (1,0,1,0) | equal (1,1,1,1); H1 = 0 |
| token multiset (bag) | **differs** | equal | equal |
| directed-bigram multiset | **differs** | equal | equal |
| loop multiset | — | equal | equal |
| last-k tokens (any function) | equal for k ≤ 4 | k ≤ 8 | k ≤ 9 |
| Bayes k-window predictor | constant for k ≤ 7 | k ≤ 17 | k ≤ 31 |
| ladder competitors q_∅, q_parity, q_counts, q_H1, q_Parikh (natural classes, §5) | constant | constant | constant |
| trigram multiset | differs (listed) | differs (listed) | differs (listed) |

Each family's **matched list** for O1(ii) is every row marked equal or constant in its column.

### 4.8 Challenge quantities on W3 (X§6.1–6.2)

The challenge distribution is uniform over the 24 orderings within each cue stratum. Every challenge competitor receives the cue and the common scaffolding.
- The optimal bag, bigram-bag and H1/count predictors (and the loop-multiset predictor) all equal q̄; their exact excess log-loss is Δ_challenge (§4.6). In AB the corresponding gaps are exactly 0.
- Holonomy information: with Z ∈ {e, c, c²} the challenge holonomy (prior 2/3, 1/6, 1/6), I(Z; W_{1:32}) = H(2/3, 1/6, 1/6) = 0.867563 nats [W], and I(Z; W_{33−k:32}) = 0 for every k ≤ 9 (common tail). Bag, bigram-bag and H1/count statistics carry exactly zero information about Z.
- The holonomy is determined by the observed base path; the physical fibre is not (its uncertainty remains in q_L).

### 4.9 β table, FAMILY label and stage-1 roles (L§4.2; AN §1.3; MD 8)

β_alt = Σ⟨q̃_alt, q̃*⟩ / Σ‖q̃*‖², centred within sets, pooled over the three y (DR§6). Competitors' laws use the same λ_{n+1}, so λ cancels and every β is rational (computed exactly by the run in G3).

| Competitor | W1 | W2 | W3 (equal ordering weights) | W3, holonomy-balanced weights (descriptive, MD 8) |
|---|---|---|---|---|
| every set-constant competitor | 0 | 0 | 0 | 0 |
| rev (ρ composed in reversed order) | −1 | −1 | **+1/3** | 0 |
| last crossing (ρ ≈ last seam letter) | 0 pooled; per y ½, −1, ½ | 0 pooled; per y ½, −1, ½ | 0 pooled; per y −1/6, 1/3, −1/6 [W] | run |
| first crossing (ρ ≈ first seam letter) | 0 pooled; per y −½, 1, −½ [W] | 0 pooled; per y −½, 1, −½ | 0 pooled; per y 1/6, −1/3, 1/6 [W] | run |

- W3 rev (AN §1.3): with m = (2/3, 1/6, 1/6), ‖δ̃_e‖² = 1/6, ‖δ̃_c‖² = 7/6, ⟨δ̃_c, δ̃_{c²}⟩ = 1/6; reversal maps identity words to identity words and swaps c and c²; numerator 16/6 + 8/6 = 4, denominator 16/6 + 56/6 = 12; β_rev = 1/3. Balanced weights (each identity ordering weighted ¼): m = u, numerator ∝ 2/3 − 1/3 − 1/3 = 0.
- **FAMILY** (DR G0.5 rule): DISCRIMINATING iff every listed competitor has pooled β ≤ 0.25. Forecast from the theorems: W1 and W2 DISCRIMINATING; W3 NOT (rev = 1/3). The balanced-weight value is reported beside it and never changes the label (MD 8).
- **Stage-1 roles (recorded now, decided by a later protocol):** W2 primary (β_rev = −1; bag- and bigram-matched); W3 secondary, the null-homologous family (MD 8); W1 the local-Stokes and window-tightness witness (not bag-matched).

---

## 5. Competitor ladder and the natural-gap DP (MD 1; L§4.2–4.4; X§7)

### 5.1 Bayes competitors

Each competitor K_S is the Bayes predictor given R_S = (no-cue flag, prefix, n, y, v_t, S(γ)): it knows everything except the segment beyond S. Its law is the class average of q* with weights proportional to the integer path counts of Theorem 7. Its natural gap is

  G_S(t) := E KL(q*_t ‖ q_S,t) = I(W_{t+1}; W_{1:t} | R_S),

and any predictor that is a function of R_S has excess log-loss ≥ G_S (Pythagorean identity for conditional expectations). Defined for the seam-supported arms.

| S | Statistic of the segment | Note |
|---|---|---|
| ∅ | none | knows the cue value and its age |
| parity | (k_x⁺ + k_x⁻ + k_y⁺ + k_y⁻) mod 2 | = sign ρ in NA and AB: the S₃/A₃ outcome (DR A4) |
| counts | (k_x⁺ + k_x⁻, k_y⁺ + k_y⁻) | unsigned |
| H1 | (m_x, m_y) | the request's H1-class predictor |
| Parikh | κ = (k_x⁺, k_x⁻, k_y⁺, k_y⁻) | **the strongest commutative statistic of the crossing word**; = X's C. Refines all of the above |

Refinement ladder: ∅ ⊃ parity ⊃ counts ⊃ Parikh and parity ⊃ H1 ⊃ Parikh (coarser on the left).

### 5.2 The single exact integer DP

Per seam-supported arm (or once, carrying the tuple of arm holonomies; both are exact), for n = 0..31:
- layer n holds integer counts N_n(v, κ, g) of n-step paths from a★ avoiding a★ at steps 1..n, ending at v, with Parikh vector κ and ordered holonomy g;
- initial N_0(a★, 0, e) = 1;
- for each state and each of the 5 successors j of v: reject j = a★; update κ by `seam_letter(v, j)`; set g ← L(v→j)∘g (compose on the left: the latest applied last); add the count;
- counts are **exact Python integers** (A_31 > 2⁶⁴); numpy fixed-width integer arrays are forbidden for counts;
- only adjacent layers are kept; per-n summaries (class tables) are retained for the gated computations.

Every ladder statistic is a function of κ, so C_n(v, σ_S, g) for every S is obtained by **aggregation** of the one Parikh DP (MD 1: "one exact integer DP"). The upper bound on keys per layer is 16·6·C(n+4, 4) ≈ 5.0 × 10⁶ at n = 31 (X§11.3, re-checked [W]); reachable keys are far fewer.

For a class (n, y, v, σ) with weights w(z) = Σ_{g: g[y] = z} C_n(v, σ, g)/Σ_g C_n(v, σ, g):
- oracle cue law μ*_{n,g,y} = μ_{n+1}(g[y]); competitor μ_S = λ_{n+1}·w + (1 − λ_{n+1})·u;
- natural mass of (n, y, v, κ, g): (1/48)·5^{−n}·N_n(v, κ, g);
- full-vocabulary row-KL at v ∈ N(a★): (1/5)·KL(μ*‖μ_S); 0 elsewhere (and at n = 0, and with no cue).

A second integer recursion gives D_m(v) for the no-cue mass (Theorem 7 identity).

### 5.3 Natural quantities (all exact; every t ≤ 32 unless stated)

| Quantity | Definition / formula |
|---|---|
| G_S(t), S in the ladder | Σ_{n=1}^{t−1} Σ_{y, v∈N(a★), κ, g} (1/48)·5^{−n}·N_n·(1/5)·KL(μ*‖μ_S) |
| I^fib_k(t), k ∈ {1,2,4,8}; I^fib(t) = I^fib_t(t) | I(X_t; W_{t−k+1:t}) = Σ_{n=0}^{min(k,t)−1} P(n)·(ln 3 − H(μ_n)), P(0) = 1/16, P(n) = A_n/(16·5^n). Order-free; identical in NA, AB, ZC, TRIV (X§7.1) |
| G_k(t), k ∈ {1,2,4,8} | I(W_{t+1}; W_{1:t}) − I(W_{t+1}; W_{t−k+1:t}) = Σ_{n=k}^{t−1} (B_n/(16·5^n))·(1/5)·(ln 3 − H(μ_{n+1})), B_n = number of avoiding paths ending in N(a★). Transport memory, not order; identical across the η = 1/50 seam-supported arms (X§7.2) |
| J_k(t) (order information inside a k-window) | Σ_{n ≤ min(k,t)−1} [masses at v ∈ N(a★)]·(1/5)·KL(μ*‖μ_Parikh); J_k = 0 for k ≤ 7 (Theorem 4c); J_full = G_Parikh |
| J^fib_k(t) | Σ_{n ≤ min(k,t)−1} masses·KL(μ_n(g[y]) ‖ λ_n·w + (1 − λ_n)·u) over all v ≠ a★; 0 for k ≤ 4 (Theorem 4b) |
| J^fib_full(t) (v2, OS 8) | J^fib_full(t) := J^fib_t(t), the full-history fibre-level order information; used by G6's label-based fibre check at t = 32 |
| Horizon | Only horizon 1 is gated; horizon-2 laws are not computed (AN §5) |

### 5.4 Coverage masses (RQ 2d; L§4.4 ∪ X§7.5)

At every t ≤ 32 and at t* = 32, as exact rationals rendered to 20 significant digits:

| Event | Definition |
|---|---|
| E_cue | some cue in w_{1:t} (= 1 − no-cue mass) |
| last-cue age law | P(n) for n = 0..t−1, and P(no cue) |
| E_nb | v_t ∈ N(a★); exactly 1/4 for every t |
| E_amb,S | the class (n, y, v_t, σ_S) is ambiguous at y (Lemma I), S ∈ {∅, parity, counts, H1, Parikh} |
| E_amb,S ∧ E_nb | horizon-1 order sensitivity |
| M_t(θ) | P(row-KL(q*_t ‖ q_Parikh,t) ≥ θ), θ = 0.01 nats, full vocabulary; with certified membership (§5.6): reported as [M_lower, M_upper] |
| n_min | smallest n with E_amb,Parikh: at any v, and at N(a★). Theorem values 4 and 7 |
| INCENTIVE input | mean over t = 1..32 of G_Parikh(t) |
| prospective counts | expected qualifying histories in 131,072 natural histories (X§7.5 item 7), descriptive only |

### 5.5 Bag of tokens: designed families only (MD 9)

On W2 and W3, with the members equally likely, every bag and bigram-bag predictor has expected excess loss at least the set gap, with equality for the optimal one (0.061119 and 0.037832 nats per readout [W]; W3′ 0.048459; v2, conformed to RC3). **The natural-distribution bag gap is not tractable** and is not computed: E[q* | bag] aggregates over all histories sharing a 15-to-18-dimensional count vector, which is neither DP-tractable nor estimable by Monte Carlo at the required precision. No natural lower bound is claimed.

### 5.6 Certified enclosures (X§9.3, §10.2; MD 2)

Every gated or labelled comparison of a logarithmic quantity uses a certified enclosure.
1. Weights are exact rationals; every input to a logarithm is an exact rational converted to Decimal by **high-precision rational division** (§9.5).
2. Each KL or entropy is evaluated in `decimal` with Python's correctly rounded `Decimal.ln`, at 80 and at 120 significant digits.
3. For a value v (sum of N terms with absolute sum Σ|·|), the enclosure is [v₈₀ − ε, v₈₀ + ε] with ε = 10^{−60}·max(1, Σ|·|). This exceeds the rounding bound (N + 10)·10⁻⁷⁸·max(1, Σ|·|) (80-digit arithmetic, correctly rounded `Decimal.ln`, inputs from 90-digit rational division) by many orders of magnitude for every N ≤ 10¹⁷. The run records N for every enclosed value and asserts (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹. The consistency check |v₈₀ − v₁₂₀| ≤ ε is part of G4.
4. A comparison "v ≥ θ" is **certified PASS** iff v₈₀ − ε ≥ θ, **certified FAIL** iff v₈₀ + ε < θ, otherwise **uncertified**.
5. A mass such as M_32(θ) is reported as [M_lower, M_upper]: M_lower counts rows certified ≥ θ, M_upper counts rows not certified < θ. "M ≥ 1/32" is certified PASS iff M_lower ≥ 1/32 (exact rational comparison), certified FAIL iff M_upper < 1/32.
6. **Memoisation (v2, OS 3).** A class's KL term KL(μ_{n+1}(z) ‖ λ_{n+1}w + (1 − λ_{n+1})u) depends only on n, the class's exact rational weight vector w and the image z (and, for the fibre-level J^fib terms, on n, w and z with λ_n in place of λ_{n+1}). Each Decimal evaluation is memoised under the exact key (precision, quantity kind, n, w as reduced Fractions, z); a cached value is the identical Decimal that recomputation in the same context returns, so memoisation changes no value. Each enclosed value's N still counts every summed term (item 3), not the distinct evaluations. The cache is per precision and is never shared between the 80- and 120-digit runs.

### 5.7 Hand values and forecasts (not gates)

Hand values [W] (awk, floating point; the run computes the exact values):
- E_cue(32) ≈ 0.7641; I^fib_1 = (1/16)ln 3 = 0.068663; I^fib_2(32) ≈ 0.11959; I^fib_4(32) ≈ 0.19235; I^fib_8(32) ≈ 0.29752; I^fib(32) ≈ 0.51234.
- G_1(32) ≈ 0.027232; G_2(32) ≈ 0.017649; G_4(32) ≈ 0.013432; G_8(32) ≈ 0.008855; G_8/G_1 ≈ 0.325.
- **Upper bounds [W].** In each Parikh class all members' cue laws have entropy H(μ_{n+1}), so the class-average KL is H(μ_Parikh) − H(μ_{n+1}) ≤ ln 3 − H(μ_{n+1}); and ambiguity at N(a★) needs n ≥ 7 (Theorem 4c). Hence G_Parikh(32) ≤ G_7(32) ≈ **0.00984**, mean_t G_Parikh(t) ≤ 0.0053, and M_32(0.01) ≤ P(n ≥ 7, v_32 ∈ N(a★)) ≈ **0.102**.

Forecasts [H] (L, AN): G_Parikh(32) ≈ 0.5–5 × 10⁻³ (AN: ≈ 5 × 10⁻³); M_32(0.01) ≈ 0.01–0.06; E_amb,Parikh ∧ E_nb ≈ 0.02–0.08; J_8/G_Parikh ≲ 10⁻²; D_blk(32) ≈ 0.2–0.6 × G_Parikh. **O2 is genuinely uncertain at the frozen thresholds; that is acceptable because the thresholds are fixed first (MD 5; AN §4.2).**

---

## 6. X2a-analogue comparators (MD 3)

X2a's comparator was a static-label product of disjoint 8-block evidence. Two analogues are frozen: X's 4×8 static-label comparator on the **challenge** family, and L's K-blk on the **natural** law. PoE is descriptive only.

### 6.1 Challenge: the 4×8 static-label block comparator on W3 (X§6.3, first partition only)

- Label Z ∈ {e, c, c²} with challenge prior (2/3, 1/6, 1/6) within each cue stratum.
- Blocks B₁ = w_{1:8}, B₂ = w_{9:16}, B₃ = w_{17:24}, B₄ = w_{25:32}. P(B_j = b | Z = z) by exact enumeration of the 24 orderings.
- r_add(z | h) ∝ P(z)·Π_j P(B_j | Z = z), normalised; the predictor mixes the holonomy-conditioned readout laws: q_add = Σ_z r_add(z | h)·q*(z).
- Expected exact values (X; verified by W and AN §1.6):
  - identity histories: r_add(e) = 1 (every non-identity alternative is killed by B₂ or B₃);
  - non-identity histories: r_add(true rotation) = 4/5, r_add(e) = 1/5 (for A⁺B⁺A⁻B⁻: e ∝ (2/3)(1/16)(1/16), c ∝ (1/6)(1/4)(1/4); ratio c : e = 4 : 1);
  - holonomy log-loss (1/3)·ln(5/4) = 0.0743812 [W]; holonomy argmax accuracy 1, equal to the oracle;
  - full-vocabulary predictive regret Δ_add,8 = (1/15)·KL(q_rot ‖ ⅘q_rot + ⅕q_id) = **0.0022197** [W] at L = λ_32 (q_rot, q_id the normalised cue laws); Δ_add,8/Δ_challenge ≈ 0.0587 [W].
- Blocks B₁ and B₄ are identical across the family and carry no evidence; only B₂ and B₃ do.
- **Reading rule (X§6.3, fixed now).** Report calibration (regret, log-loss) and classification (accuracy) separately. Perfect classification together with positive predictive regret does **not** prove that the aggregate carries less mutual information, nor that no recalibration or other short-block aggregation could succeed. Static-label block likelihoods are not transplanted onto the changing physical target X_t.

### 6.2 Natural: K-blk, exact (L§4.3; Theorem 8)

- Blocks are as above. Each transition belongs to the block of its destination position.
- K-blk knows R_∅ (no-cue flag, prefix, n, y, v_t) and the **unordered multiset** of the exact holonomies of the segment's parts inside each block (blocks that contain at least one segment transition). Commutative aggregation of exact block evidence is precisely abelianisation across blocks.
- Exact DP per cue position s = 1..31 (n = 32 − s): state (v, current-block product, tuple of completed block products), at most 15·6·6³ = 19,440 states; integer counts; at t = 32 the tuple is reduced to a multiset.
- D_blk(32) = E KL(q*_32 ‖ q_blk,32), with a certified enclosure. Computed for NA, AB, ZC and TRIV.
- G4 checks: D_blk = 0 exactly in AB, ZC, TRIV (integer statement: no K-blk class ambiguous at any y); the Theorem 8 witness class is present and ambiguous in NA.
- Label **BLOCK**: BLOCK_ORDER_NEEDED iff D_blk(32) ≥ 1e-3 nats (certified), BLOCK_ORDER_SMALL iff certified < 1e-3, otherwise BLOCK_UNRESOLVED. Descriptive; never changes the outcome.

### 6.3 PoE (descriptive only; MD 3)

Literal X2a product of experts on the hidden state X_32: each block β's posterior is `BayesFilter(T_lift, E, π).run(tokens[:, 8β−8:8β]).b[:, 7]` propagated without conditioning by T_lift^{32−8β}; the four are multiplied, renormalised (uniform prior) and pushed one step (`FutureOperator.F1`). D_PoE(32) = mean KL(q*_32 ‖ q_PoE) on the first 2¹⁴ rows of NA, AB and TRIV (Monte Carlo; no gate, no label beyond the reading).
- **Reading rule (L, fixed now).** If D_PoE(AB) and D_PoE(NA) are both clearly positive while D_PoE(TRIV) ≈ 0, the literal comparator measures cross-block transport, which every non-trivial arm needs; only K-blk and the Parikh ladder speak to order.

---

## 7. Controls (MD 1, MD 2, MD 7; all required, G7)

| Id | Model | Required outcome (exact unless a tolerance is stated) |
|---|---|---|
| AB | a on both seams | Every W-family spread 0; no parity class ambiguous (integer); G_parity = G_counts = G_H1 = G_Parikh = 0; D_blk = 0; closed form = BayesFilter within 1e-12 on 2¹⁶ rows |
| ZC | c / c² on both seams | Every W-family spread 0; no H1 class ambiguous (integer); G_H1 = G_Parikh = 0; G_parity > 0 and G_counts > 0 with the §3 ZC witness class present; D_blk = 0; closed form = BayesFilter within 1e-12 on 2¹⁶ rows |
| TRIV | e everywhere | Every spread 0; G_∅ = 0 (and so every ladder gap); D_blk = 0; closed form = BayesFilter within 1e-12 on 2¹⁶ rows |
| ETA1 | NA labels, η = 1 | Every cue law uniform (λ_m = 0 for m ≥ 1); every G_S = G_k = J_k = 0 exactly; closed form = BayesFilter within 1e-12 on 2¹⁶ rows |
| GAUGE-NA | §2.4, h_fix | On the NA rows, every q_t (t ≤ 32) equals NA's within 1e-12; W-family q* equal to NA's exactly (Fractions) |
| GAUGE-TRIV | §2.4, h_fix | On the TRIV rows, every q_t equals TRIV's within 1e-12; its edge labels are checked to include a non-commuting pair |
| GAUGE-COV | §2.4/§2.6, h_cov, E_cov | On the NA rows, every q_t equals NA's within 1e-12; W-family q* equal exactly |
| NOCUE | NA and TRIV lifts with E_nc (16 tokens) | On 2¹⁴ rows sampled from (T_NA, E_nc): BayesFilter q_t of NA and TRIV agree within 1e-12; every belief's fibre marginal is uniform within 1e-12; q_t equals the base-walk law of v_t within 1e-12 |
| TOKPERM | E_σ, σ_tok of §2.6 | On the first 2¹⁴ NA rows: `BayesFilter(T, E_σ, π).run(σ(tokens)).q[:, t, σ(w)]` equals `BayesFilter(T, E, π).run(tokens).q[:, t, w]` within 1e-12 for all t ≤ 32 and all w |
| FIXED-POINT (X§8) | AB under ∅ | At y = 2 no ∅ class is ambiguous (a fixes 2), so its contribution to G_∅(AB) is exactly 0, while y ∈ {0,1} contribute > 0: the DP treats ambiguity at the image level (Lemma I) |
| SAME-HOLONOMY (X§8) | NA | The 16 identity orderings of W3 (equal cue age and end vertex) have identical q*, exactly |

No "all short windows match across arms" assertion is made beyond Corollary 4′: a single winding loop followed by a cue distinguishes seam actions without testing commutator order (X§8).

---

## 8. Gates, criteria, outcomes and stop rules (fixed before any computation)

### 8.0 Order and statuses

**Execution order:** PF → S0 → G0 → G1 → G2 → G3 → G4 → G5 → G6 → G7 → D (O1, O2, outcome, labels).
- Every gate records PASS, FAIL, INVALID or NOT_RUN.
- The run stops at the first FAIL or INVALID in PF, S0 or G0–G7 and records every later gate as NOT_RUN. D values computed earlier (in G3 and G4) are **sealed**; the outcome and labels are released only if G0–G7 all pass. Otherwise they are WITHHELD, with the values preserved for diagnosis.
- Exception: the resource rule S8 (§8.5).
- Any rerun or technical correction follows the rerun and lineage rule (§10.8, v2). Tolerances are fixed with their attainability argument (§8.7, v2).
- All gates are deterministic given the frozen seeds. Every history-dependent decision uses at most w_1..w_32; w_33 is used only as the label target of the G6 label-based checks.

### 8.1 PF and S0

**PF (mandatory preflight).** A metered run (§10.5), **in the clean execution worktree at H** (§10.7; v2, OS 6), of:
- the unchanged regression suites `tests/world`, `tests/process`, `tests/oracle`, `tests/oracle_profile`, `tests/dataset`, `tests/d1_seam`, `tests/x2a_stage0`;
- the new `tests/x6_stage0` (§10.4), including registry hygiene and the `point_distances` / `is_x_periodic` guards;
- `tools/check_file_sizes.py` (every .py ≤ 400 lines). It walks every `.py` under the repository root, tracked or not, so it runs only in that clean worktree, never in the main worktree (whose untracked `output/` and `research_audit_export/` and uncommitted edits would be counted).

The record is `preflight.json`, which also records: `git rev-parse HEAD` of the worktree (must equal H); `git status --porcelain --untracked-files=all` of the worktree (must be empty before PF starts); `tempfile.gettempdir()` as seen inside a metered child (it must lie under `X:/Downloads/topo-scratch/<job>/`, §10.5); the pytest `--basetemp` used. Any failure or inability to complete gives INVALID with every gate NOT_RUN (D-1 coordinator ruling 8).

**S0 (MD 11; the D2A D5 allowlisted-diff rule).** Run only if all hold:
1. the protocol is frozen and its SHA256 matches the freeze record;
2. the request SHA256 equals `18E77F7E5BAE48AACC08C8A48560DEEDC0A543531C11B2E09D8684B36C9EFBE1` (W re-hashed the request file; it matches the `.sha256` record);
3. **commit binding.** The reviewed reference is R = `f8e5f12b2f83ecf8b6a32189705a03ff98afa28d` (v2, RU (a); v1's R = 978e17f is superseded, see the review-base record below). At dispatch the exact execution commit H is pinned and recorded. Across the protected paths, the R→H diff may contain only the allowlisted additions. Unrelated main changes outside the protected paths do not invalidate the binding. (In this rule R and H name commits.)
   - **Protected paths (the reused and run paths):** `src`; `tools/x4_oracle_profile`; `tools/d1_seam`; `tools/x2a_stage0`; `tools/check_file_sizes.py`; `tools/x6_stage0`; `tests/world`, `tests/process`, `tests/oracle`, `tests/oracle_profile`, `tests/dataset`, `tests/d1_seam`, `tests/x2a_stage0`, `tests/x6_stage0`; **`pyproject.toml`** (v2, OS 7: its `[tool.pytest.ini_options]` `addopts` (`--import-mode=importlib -m 'not slow and not gpu and not integration'`) decide which tests PF runs).
   - **Allowlist:** new `tools/x6_stage0/API.md`, `tools/x6_stage0/x6_model.py`, `tools/x6_stage0/x6_exact.py`, `tools/x6_stage0/x6_run.py`; **optional** new `tools/x6_stage0/x6_dp.py` (v2, OS 9; §10.1); new `tests/x6_stage0/test_x6_stage0.py`, optional `tests/x6_stage0/test_x6_stage0_dp.py`, and `tests/x6_stage0/AUTHORSHIP.md`.
   - **Mechanical check:** `git diff --no-renames --name-status R H -- <protected paths>` lists only `A` entries for allowlisted files. Any `M`, `D` or other entry fails S0.
4. the kernel-compatibility condition of X2a, restated against R (v2): `git diff --no-renames --name-status c364f95e5573940cdc24b569b0fb7c6a16c97ab8 H -- src tools/x4_oracle_profile tests/oracle_profile` lists **exactly** `A src/topo_pilot/learner/multihorizon.py` and `M src/topo_pilot/learner/trainer.py` (the D-2a learner changes already present at R; W verified this list at R). Any other entry fails S0. (Implied by 3, because R→H adds nothing under these paths; checked anyway. v1 required this diff to be empty, which no descendant of current main can satisfy; open item §12.6 O1.)
5. **dispatch record (v2, OS 4).** The dispatch record holds the sha256 of the store-local `x6_meter_bind.py` and the absolute directory from which it imports `meter`, `controls` and `winjob`; that directory must be `<execution worktree at H>/tools/x4_oracle_profile` (§10.5, §10.7). At launch the binding file's sha256 and its import directory are re-checked against the record.
6. **store lineage (v2, RU (c); v3 conformed to Codex RC3).** The pre-PF lineage check of §10.8 item 7 passed and is recorded in `preflight.json`; S0 re-checks the recognised archived lineage (every listed archived file present with its recorded sha256), and `run/` holds nothing but this attempt's `preflight.json` (no PF or S0 gate marker, gate directory or gate-log entry, §10.8 item 1).

A violation gives INVALID ("do not run").

**Review-base record (v2, RU (a); W, read-only git in `X:/Downloads/projects/topo-pilot/topo-pilot`).**
- `git diff --name-status 978e17f f8e5f12 -- src tools/x4_oracle_profile tools/d1_seam tools/x2a_stage0 tools/check_file_sizes.py tools/x6_stage0 tests/world tests/process tests/oracle tests/oracle_profile tests/dataset tests/d1_seam tests/x2a_stage0 tests/x6_stage0 pyproject.toml` (v1's §8.1 protected paths plus `pyproject.toml`; identical output with `--no-renames`), exactly:

  ```text
  M	pyproject.toml
  A	src/topo_pilot/learner/multihorizon.py
  M	src/topo_pilot/learner/trainer.py
  ```
- The same three entries, and nothing else, appear from 7c8da1f (the reviewer's HEAD) to f8e5f12. 978e17f is an ancestor of f8e5f12 (65 commits). The changes come from 34f8312 (Trainer injection, D-2a job 0029), 7f8f5b8 (MultiHorizonLM, job 0029) and c460e24 (licence).
- **Under v1's rule this binding fails:** the two `M` entries are not allowlisted, so any H descending from current main would be INVALID at S0 item 3 (and at v1's item 4). Hence the new review base.
- **No change touches a function X6 reuses.**
  - `trainer.py`: `Trainer.__init__(self, model_cfg, train_cfg, seeds, run_key)` becomes `Trainer.__init__(self, model_cfg, train_cfg, seeds, run_key, *, model_factory=None, loss_fn=None)`, and `fit` uses them when given (default behaviour unchanged). X6 never trains.
  - `multihorizon.py`: a new D-2a learner module (139 lines).
  - `pyproject.toml`: one added line, `license = {text = "MIT"}`, under `[project]`. `[tool.pytest.ini_options]` (testpaths, addopts, markers) is unchanged, so PF's test selection is unchanged. sha256 of the committed blob (`git show <commit>:pyproject.toml | sha256sum`): 978e17f `b4536291…25df`, f8e5f12 `de31a5d9…a994`.
  - X6 imports nothing from `topo_pilot.learner`. At f8e5f12, `git grep` finds imports of `topo_pilot.learner` only under `src/topo_pilot/activations` and `src/topo_pilot/experiment`. No reused package (`world`, `process`, `oracle`, `dataset`, `contracts`), no reused tool (`tools/x4_oracle_profile`, `tests/oracle_profile/independent_reference.py`, `tools/check_file_sizes.py`) and no PF suite imports it (`contracts/store.py` names "learner" only as a string in `MODULES`). There is no root `conftest.py`; the PF suites' own `conftest.py` files are inside unchanged protected directories.
  - Every other file under the protected paths is byte-identical at 978e17f and f8e5f12 (the diff lists nothing else), so every signature of §10.3 and every code fact of RV B14 holds at R.
- **New review base:** R = `f8e5f12b2f83ecf8b6a32189705a03ff98afa28d` (main, the K4b merge). The D5 rule then reads as stated in item 3, with `pyproject.toml` added (OS 7). The Codex v2 review re-checks this record (§12.6 O1).

### 8.2 Validity gates G0–G7

| Gate | Content | Tolerance |
|---|---|---|
| **G0 structure** | Builder steps 1–4 (§2.1); counts 16/32/16; torus Betti (1,2,1) over GF(2), GF(3). Punctured complex: (16,32,15), χ = −1, Betti (1,2,0), ∂₁∂₂ = 0, one boundary cycle (§2.2). T_base equals the Fraction neighbour table (§2.5) and its support. Each arm's T_lift equals the Fraction formula entrywise; row and column sums (exact, on the Fraction arrays; v2 reading, §8.7 T2, §12.6 O3); `validate_process(T_lift, E, π)` returns. Per arm: the 16 face holonomies and the flux (Lemma 0; GAUGE-NA's f★ holonomy is a 3-cycle, GAUGE-TRIV's 16 faces are flat). Per seam-supported arm: the cover (48, 96, 45), its Betti numbers via unchanged `CubicalComplex(48, cover_cells).betti(p)` for p = 2, 3 (which uses `rank_mod_p`), `check_boundary_closed`, and the boundary-circle count (components of the edges lying in exactly one lifted square) per Lemma 0′ | floats 1e-15; otherwise exact |
| **G1 emission and locality** | E, E_cov, E_nc, E_σ are one-hot as in §2.6; tok is a bijection onto 0..14. Stationary k-gram laws (forward recursion over **reachable** strings, prefix-shared DFS; unreachable strings have probability 0 in every arm) of NA, AB, ZC, TRIV are equal for k ≤ 4. For k = 5, every pair of these arms differs at the named 5-gram [15+y, 10, 8, 9, 15+y′] for some (y, y′), with probability ratio > 2 (theorem ≈ 36.6) | equality rel 1e-12 |
| **G2 exact enumeration** | Every history with t ≤ 6, for NA, AB, ZC and TRIV (DFS with shared prefixes; a generic sparse 48-state Fraction forward filter that never uses ρ): Theorem 1 belief, q* and P(h) agree **exactly**; Σ_h P(h) = 1 for each t; anchor-avoiding path counts and every ladder class table for n ≤ 5 equal the DP's; A_1..A_5 reported beside the [W] values | exact |
| **G3 witnesses and challenge** | In exact Fractions, for all y and for Π0, Π1, Π3, Π6 (all y₀) on W1 and W2, and Π0 on W3 and W3′: membership probabilities and equality within sets; the matched statistics of §4.7 (token and bigram multisets for W2, W3; tails; Parikh, H1, counts, parity; length), with the differing trigrams listed; q*; cue-normalised TVs equal λ_{n+1} exactly; set gaps equal the closed forms (Decimal, 1e-40); W3 multiplicities (16, 4, 4) in NA and (24, 0, 0) in AB; competitor constancy (§4.7), where constancy of each ladder competitor q_S is checked by **equality of the R_S keys** (no-cue flag, prefix, n, y, v_t, S(γ)) across the members, which implies equal q_S by definition (§5.1), so G3 needs no DP class table (v2, OS 2); the β table (§4.9, exact rationals, including the balanced W3 value); prefix invariance; within-set spread 0 in AB, ZC, TRIV, GAUGE-TRIV; the challenge quantities of §4.8 (Z-information H(2/3,1/6,1/6) and 0 for k ≤ 9); the 4×8 comparator values of §6.1 (posteriors exactly 1 and 4/5; logs to 1e-40) | exact; logs 1e-40 |
| **G4 exact DP** | The integer DP (§5.2) per seam-supported arm, n ≤ 31. The total-mass identity of Theorem 7 for every t ≤ 32 (exact rationals). Ladder: for every t ≤ 32 and arm, G_∅ ≥ G_parity ≥ G_counts ≥ G_Parikh and G_parity ≥ G_H1 ≥ G_Parikh, and the Pythagorean identities G_∅ − G_Parikh = E KL(q_Parikh‖q_∅) and G_H1 − G_Parikh = E KL(q_Parikh‖q_H1), within the summed enclosure half-widths. Theorem 4: J_k = 0 for k ≤ 7 and J^fib_k = 0 for k ≤ 4 as integer statements (no Parikh class ambiguous at N(a★) with n ≤ 6, or at any v with n ≤ 3); n_min = 4 and 7. Abelian nulls as integer statements (AB under parity; ZC under H1; TRIV under ∅). I^fib_k and G_k identical across NA, AB, ZC, TRIV. K-blk: D_blk = 0 in AB, ZC, TRIV; the Theorem 8 class ambiguous in NA. Every gated or labelled log value: |v₈₀ − v₁₂₀| ≤ ε, and its recorded term count N satisfies (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹ (§5.6 item 3; Decimal evaluations memoised per §5.6 item 6). Values of G_S, J_k, I^fib_k, G_k, D_blk, the masses of §5.4 and M_32 bounds are computed here and sealed | exact; enclosures per §5.6 |
| **G5 numerical cross-checks** | On the first 2¹⁴ NA Monte Carlo rows: unchanged `BayesFilter` b_t and q_t against Theorem 1 for all t ≤ 32; `FutureOperator.F1(b_32)` against q_32; `suffix_posterior(T_lift, E, π, tokens[:, :32], K)` for K ∈ {1, 2, 4, 8} against the window closed form (the cue inside the window, else uniform fibre at v_t). Decimal reference (§9.5): Decimal against Fractions within 1e-45; BayesFilter against Fractions within 1e-12; BayesFilter log-evidence against the Fraction ln P(h) within 1e-10; the 120-digit repeat agrees with the 80-digit run within 1e-45. `enumerate_posterior` (Fraction inputs) on 30 histories with t ≤ 2 (all 18 unigrams, then the first 12 reachable bigrams in lexicographic token order) equals the Fraction forward filter exactly. No non-finite or negative value anywhere | as stated |
| **G6 Monte Carlo validity** | NA 2¹⁸ rows (33 symbols, unchanged `HMMSampler`). Each within 4·SE + 2e-12 of the exact value: mean per-row KL(q*_32 ‖ q_S) for S ∈ {∅, parity, counts, H1, Parikh} and the Bayes 8-window (6 comparisons; q* from BayesFilter, q_S from the DP class of the row's observed segment); the masses E_cue, E_amb,Parikh ∧ E_nb and M_32 (with the row-KL membership taken from the exact class) (3); Î^fib(32) (1); label-based: mean ln q*(w₃₃) − ln q_Parikh(w₃₃) against G_Parikh(32), and mean ln post*(x₃₂) − ln post_Parikh(x₃₂) against J^fib_full(32) (§5.3; true fibres from HMMSampler states) (2). Total 12 comparisons. **SE (v2, OS 1):** for the three indicator masses the SE is computed from the exact p, SE = sqrt(p(1 − p)/2¹⁸), not from the sample variance: p = E_cue(32) and p = P(E_amb,Parikh ∧ E_nb) at t = 32 from the DP; for M_32 the Monte Carlo indicator is "the row's exact class is certified ≥ 0.01" and p = M_lower (§5.6 item 5), even if the interval does not collapse; membership retains the row's image z = ρ[y], i.e. the class key is (n, y, v_32, κ, z) (v3, O4 resolved). For the other nine comparisons the SE is the sample SD of the row-level statistic over √(2¹⁸) | 4·SE + 2e-12 |
| **G7 controls (required)** | Every row of §7 | as stated |

G6 diagnostics: with 12 four-SE comparisons, the union-bound false-FAIL probability is about 12 × 6.334e-5 ≈ 7.6e-4 (0.076%) [W]; an asymptotic diagnostic, not a guarantee. Hoeffding half-widths are reported, not gated (range 1 nat: 0.00526 at δ = 1e-6 for 2¹⁸ rows [W], too wide to validate). A G6 failure invokes S5: no reseed and no increase of n. With the exact-p SE, an indicator mass with p = 0 passes only with zero hits (which is then certain), and a mass with zero sample hits fails only if p > 16/(2¹⁸ + 16) ≈ 6.10e-5, where the probability of zero hits is (1 − p)^{2¹⁸} ≤ e⁻¹⁶ ≈ 1.13e-7 [W] (v2).

### 8.3 Scientific criteria D (released only under validity PASS; all inputs exact)

- **O1 (designed exact observability; MD 4).** For each family W1, W2 and W3 (canonical, t = 32):
  1. the cue-normalised TV between members of different holonomy is ≥ **0.3** (exact rational comparison; theorem values 0.8507630, 0.6951353, 0.5238831);
  2. every competitor in the family's matched list (§4.7) is exactly constant on the set;
  3. the within-set spread is exactly 0 in AB, ZC, TRIV and GAUGE-TRIV.
- **O2 (natural non-commutative signal at t* = 32; MD 5).** Both of:
  1. G_Parikh(32) ≥ **1e-3 nats**;
  2. M_32(0.01) ≥ **1/32** (full-vocabulary row-KL ≥ 0.01 nats).

  O2 is **certified PASS** iff both are certified PASS (§5.6); **certified FAIL** iff at least one is certified FAIL; otherwise **uncertified**. Parikh refines parity, counts and H1, so G_Parikh(32) ≤ G_H1(32), G_counts(32), G_parity(32), and O2(i) implies the same inequality for those competitors. O2(ii) is a statement about q_Parikh only: row-level KL is not monotone under refinement, so no M_32 statement is implied for the coarser competitors. O2 is not split, and its thresholds are not changed after the forecast or the result (MD 5). These are DR§7.2's values (0.001 nat; 512 of 16,384 histories) applied to exact quantities; X's 1/256 is rejected (MD 5).

### 8.4 Outcomes and labels

| Outcome | Condition | Meaning for a later trained stage |
|---|---|---|
| **GO_X6_NATURAL** | O1 ∧ O2 certified PASS | A trained-stage protocol may make natural and designed claims |
| **GO_X6_CHALLENGE_ONLY** | O1 ∧ O2 certified FAIL | A legitimate pre-registered outcome (MD 5). Training only by explicit owner decision; every claim restricted to the designed distribution; natural training is not presented as supported by the rare canonical witnesses |
| **INCONCLUSIVE_NATURAL** | O1 ∧ O2 uncertified, or the natural DP could not complete within the memory limit (S8, with every completed G4 check passing). Never after a wall-limit kill (S7) | The designed result stands (under S8 its window clause only as §8.5 S8 states); the unresolved natural calculation is identified. No natural claim |
| **STOP_X6** | ¬O1 | No trained stage in this formulation |

**Reported labels** (fixed now; they never change the outcome):
- **P1-link:** LONG_HISTORY iff J_8(32) ≤ ½·G_Parikh(32) (certified), SHORT_HISTORY if certified otherwise, else UNRESOLVED. Forecast LONG.
- **BLOCK** (§6.2).
- **INCENTIVE:** ABOVE iff mean_{t=1..32} G_Parikh(t) ≥ 1e-3 (certified), BELOW if certified otherwise, else UNRESOLVED. Compare X2a's V_32 = 0.0098. Descriptive only; it is not part of O2 (MD 5).
- **HEADROOM (X§9.3):** G_8(32) ≥ 1e-3 (certified). Long-context predictive headroom, not specific to non-abelian transport.
- **FAMILY** per family (§4.9), with the balanced-W3 value beside it.
- **PoE reading** (§6.3).

A GO supports designing a trained-stage protocol. It does **not** authorise training. A later trained stage is informative only after its own protocol freezes the task, the comparators, natural versus challenge evaluation, replication, the **cue-mass gate** (DR§6, carried into stage 1 per AN §2) and success criteria. Its sharp natural criterion (data processing): a model whose natural excess log-loss at t = 32 is credibly below G_Parikh(32) is not a function of R_Parikh or of any coarser statistic (parity, S₃/A₃, counts, H1). Stage 1 needs new seeds.

### 8.5 Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S0 | Protocol not frozen; request, protocol or commit mismatch; a protected-path entry outside the allowlist; a kernel diff other than the two recorded entries (§8.1 item 4); a meter-binding sha256 or import-directory mismatch (item 5); a store file outside this lineage (item 6) | INVALID; do not run |
| PF | Preflight failure or inability to complete | INVALID; every gate NOT_RUN |
| S2 | Builder or validation exception in G0 | INVALID; escalate. No registry change, no production edit |
| S3 | Any exact identity, tolerance, count or required control fails (G0–G5, G7) | FAIL at the first failed criterion; later gates NOT_RUN; D WITHHELD. Preserve the failing object. No post-hoc edit of a theorem or tolerance. A documented implementation or environment defect may be corrected only under §10.8 |
| S5 | A G6 comparison fails | FAIL; G7 and D NOT_RUN; escalate as a possible DP or oracle defect. No reseed, no increase of n. A documented defect may be corrected only under §10.8 |
| S6 | The implementation needs a production change, a module file beyond the three planned files and the one optional allowlisted `x6_dp.py` (§10.1), or a file over 400 lines | Stop before coding; escalate |
| S7 | Owner STOP, usage limit, disk thresholds (C: < 2 GB, X: < 30 GB), or a kill by the meter's wall limit (`--max-wall`, §10.5) | INVALID (interrupted). Resume only under the same frozen specification, reproducing identical values. After a wall-limit kill the rerun may use a larger `--max-wall` (an environment parameter, recorded in the ledger); nothing scientific changes, and a wall-limit kill never yields INCONCLUSIVE_NATURAL |
| S8 | The natural DP or its certification cannot complete within the memory limit (a MemoryError inside G4, including one raised under the Job Object memory limit) | G4 records RESOURCE_LIMIT, the step at which it occurred, and every G4 check that completed; **every completed G4 check must pass** (a completed check that fails is S3, not S8). G6 and the DP-dependent items of G7 (the G_S, D_blk and class-ambiguity items of the AB, ZC, TRIV and ETA1 rows, and the FIXED-POINT row) are NOT_RUN; G5 and the other G7 items still run. If PF, S0, G0–G3, the completed G4 checks, G5 and the remaining G7 items pass and O1 holds, the outcome is INCONCLUSIVE_NATURAL (X§11.3); otherwise the usual FAIL/INVALID applies. Under S8 the designed sentence (§1.4) keeps its last clause ("No window of at most 7 symbols …") only if the Theorem 4 integer checks (no Parikh class ambiguous at N(a★) for n ≤ 6, or at any v for n ≤ 3) completed and passed; otherwise that clause is omitted. No change of definition, precision or threshold to obtain a GO. The memory limit is the unchanged Job Object limit of 8 GiB, `winjob.MEMORY_CAP` (§10.5) |

There is **no CPU ceiling** (MD 10): CPU is measured only. Owner caps: one scientific task at a time, ≤ 12 GiB, threads pinned to 1; the hard per-job memory limit is the unchanged 8 GiB `winjob.MEMORY_CAP`, inside the owner's 12 GiB. The pipeline is deterministic, so a rerun after an environment-caused INVALID (S7) under the same specification and seeds is legitimate and must reproduce identical values; it follows §10.8 (archive the interrupted attempt, regenerate bit-identically) and is not counted as a technical correction.

### 8.6 Threshold register (all fixed before any data)

| Item | Value |
|---|---|
| L, p_stay, η, anchor, r | 4; 0.2; **1/50 (frozen; 1/100 not run, MD 6)**; (2,2); 1 |
| t*; windows; blocks | 32; {1, 2, 4, 8}; positions 1–8, 9–16, 17–24, 25–32 (by destination position) |
| O1 | cue-normalised TV ≥ 0.3 per family (W1, W2, W3 at t = 32); exact constancy; exact zero spread in AB, ZC, TRIV, GAUGE-TRIV |
| O2 | G_Parikh(32) ≥ 1e-3 nats ∧ M_32(0.01) ≥ 1/32, both certified |
| Labels | J_8 ≤ ½·G_Parikh; D_blk ≥ 1e-3; mean_t G_Parikh ≥ 1e-3; G_8(32) ≥ 1e-3; β ≤ 0.25 |
| Enclosures | 80 and 120 digits; ε = 10⁻⁶⁰·max(1, Σ\|terms\|); asserted (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹ per enclosed value (RC6) |
| Enumeration depth | histories t ≤ 6; counts n ≤ 5 |
| DP depth | n ≤ 31; every t ≤ 32 |
| Monte Carlo | NA 2¹⁸; AB, ZC, TRIV, ETA1 2¹⁶ each; NOCUE 2¹⁴; 33 symbols; validity 4·SE + 2e-12 (12 comparisons; indicator-mass SE from the exact p, OS 1) |
| Decimal | inputs by rational division at 90 digits (130 for the 120-digit repeat); 80-digit context; set of §9.5 |
| Tolerances | structure 1e-15; numerical cross-checks and controls 1e-12; log-evidence 1e-10; Decimal 1e-45; logs in G3 1e-40; G1 rel 1e-12; G2–G4 exact. Each with its attainability argument in §8.7 (v2) |
| Resources (environment, not science) | `--max-cpu inf`; `--max-wall 21600` (S7 allows a larger value on rerun); Job Object memory 8 GiB (`winjob.MEMORY_CAP`, unchanged); `OUTPUT_CAP` 128 MiB (unchanged) |
| Seeds | `SeedTree(420700)` (DR's base seed); streams ("x6s0_mc", arm) for arm ∈ {NA, AB, ZC, TRIV, ETA1, NOCUE}; one `sample` call per stream. GAUGE-NA, GAUGE-COV, TOKPERM and PoE reuse NA rows; GAUGE-TRIV reuses TRIV rows |

### 8.7 Tolerance attainability, fixed before data (v2, RU (b); the R13 lesson, K4b §5.6 pattern)

C1′'s M1 tolerance of 1e-10 for a cho_solve versus lstsq comparison was not attainable at κ ≈ 1e9 (job 0042), and changing it after data needed retroactive owner ratification (addendum 10). Every numeric tolerance and identity in PF, S0, G0–G7 and D is listed here with its conditioning and the reason it is attainable. **No X6 gate compares two linear solvers, and no X6 gate solves a linear system.** Every float comparison is between an unchanged production kernel and exact rationals (or exact Decimal), or between two runs of the same kernel on relabelled models. All error bounds below are hand bounds [W] (u = 2⁻⁵³ ≈ 1.11e-16), not gates.

| # | Gate: identity or comparison | Tolerance | Conditioning and error bound [W] | Why attainable |
|---|---|---|---|---|
| T1 | G0: float `T_base` (from `TransitionBuilder`) against Fraction(1, 5) entries; support | 1e-15; support exact | Each entry comes from a few (≤ 4) correctly rounded operations on values in [0, 1]: \|error\| ≤ 4u ≈ 4.4e-16; expected ≤ 1 ulp of 0.2 = 2.8e-17. Zero entries are exact zeros | Bound below the tolerance; no cancellation |
| T2 | G0: float `T_lift`, `E`, `π` against the Fraction formula entrywise | 1e-15 | The float arrays are defined as `float(Fraction)` (§2.5): each entry is the correctly rounded value, \|error\| ≤ ½ ulp ≤ 1.4e-17 for entries ≤ 0.2; E is 0/1, exact. Row sums, column sums and stationarity are checked **exactly on the Fraction arrays** (W reading of G0; §12.6 O3) | By construction; the float sums are covered by T3 |
| T3 | G0: `validate_process(T_lift, E, π, tol=1e-12)` (production default) | 1e-12 | Each float row sum has 15 non-zero entries: \|error\| ≤ 14u ≈ 1.55e-15; πT − π has the same order | Margin ≥ 600 |
| T4 | G0: `check_flat_bounds(dist, dist_graph, 2, tol=1e-9)` (production default) | 1e-9 | Distances of the unchanged builder on the 4×4 flat torus (small integers and their square-root combinations): error ≲ 1e-15 | Margin ≥ 10⁵; the same lattice `tests/world` builds as `_t_torus` |
| T5 | G0: cell counts, Betti numbers (`rank_mod_p`), ∂₁∂₂ = 0, boundary cycle, face holonomies, flux, cover | exact | Integers mod p and permutation arrays | No rounding |
| T6 | G1: k-gram laws equal across NA, AB, ZC, TRIV for k ≤ 4 | rel 1e-12 | Forward recursion over reachable strings: each probability is a sum of positive terms over ≤ 3 fibre states, with ≤ 5 factors; relative error ≤ ~20u ≈ 2.2e-15 per arm, ≤ 4.4e-15 between arms (exact if computed in Fractions) | No cancellation; margin ≥ 200 |
| T7 | G1: the named 5-gram ratio between arms | > 2 | Theorem value (1 + 2λ_4)/(1 − λ_4) = 36.64 | Margin ≥ 18× (a ratio threshold, not a tolerance) |
| T8 | G2: Theorem 1 belief, q*, P(h), Σ P(h) = 1, counts and class tables (t ≤ 6) | exact | Fractions and Python integers | No rounding |
| T9 | G3: TVs = λ_{n+1}, constancy (R_S key equality), multiplicities, β, prefix invariance, spreads, 4×8 posteriors 1 and 4/5 | exact | Fractions; keys compared by equality | No rounding |
| T10 | G3: set gaps against the closed forms; Z-information; 4×8 logs | 1e-40 | 80-digit Decimal from 90-digit rational division; ≤ 72·18 = 1,296 summed terms of magnitude ≲ 10: error ≲ (N + 10)·10⁻⁷⁸·max(1, Σ\|·\|) ≲ 10⁻⁷⁰ | Margin > 10²⁹ |
| T11 | G4: DP counts, total-mass identity, ambiguity statements, abelian nulls, Theorem 4 integer checks, n_min, K-blk zeros | exact | Python integers (A_31 ≈ 7.9e20 > 2⁶⁴) and Fractions | No rounding; fixed-width integers forbidden |
| T11′ | G4: I^fib_k and G_k identical across NA, AB, ZC, TRIV | identical | Order-free: their inputs are the arm-independent integer counts A_n, B_n and the rational λ_n (§5.3), checked equal as integers; the Decimal evaluations are then the same operations on the same inputs, hence identical | By construction |
| T12 | G4: the RC6 assertion (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹, i.e. N ≤ 10¹⁷ − 10 | assertion | Upper bound N ≤ 9·96·Σ_{n=1}^{31} C(n + 4, 4) = 9·96·376,991 = 325,720,224 ≈ 3.3e8 (3 values of y × 3 KL coordinates × at most 16·6·C(n + 4, 4) keys at layer n; Σ_{n=0}^{31} C(n + 4, 4) = C(36, 5) = 376,992). K-blk: ≤ 31·19,440·9 = 5,423,760. Then (N + 10)·10⁻⁷⁸ ≤ 3.3e-70 | Margin ≈ 3·10⁸ |
| T13 | G4: \|v₈₀ − v₁₂₀\| ≤ ε | ε = 10⁻⁶⁰·max(1, Σ\|·\|) | By T12, \|v₈₀ − v\| ≤ 10⁻⁶¹·max(1, Σ\|·\|); \|v₁₂₀ − v\| is smaller by about 40 orders | Margin ≥ 10 from the asserted bound alone; ≥ 10⁹ with the T12 bound on N |
| T14 | G4: ladder inequalities (G_∅ ≥ G_parity ≥ …) and Pythagorean identities | within the summed enclosure half-widths | Each computed side lies within 10⁻⁶¹·max(1, Σ\|·\|) of its exact value (T12); the exact relations hold, with equality where a gap is exactly 0 (for example every gap in TRIV) | The computed residual is ≤ 3·10⁻⁶¹ against an allowance of ≥ 2·10⁻⁶⁰ |
| T15 | D and labels: certified comparisons v ≥ θ (O2, P1-link, BLOCK, INCENTIVE, HEADROOM) | PASS iff v − ε ≥ θ; FAIL iff v + ε < θ | ε ≈ 10⁻⁶⁰·max(1, Σ\|·\|) | A decision rule, not a tolerance: either outcome is certified unless \|v − θ\| < ε; "uncertified" is a legitimate pre-registered outcome (INCONCLUSIVE_NATURAL or UNRESOLVED), RV B12 |
| T16 | G5 and G7: unchanged `BayesFilter` b_t and q_t against the closed form (Fractions), t ≤ 32; `FutureOperator.F1`; `suffix_posterior` (K ≤ 8) | 1e-12 | The base is observed, so after the first symbol each belief has ≤ 3 non-zero entries. Normalised positive maps are not in general immune to conditioning amplification; here the structure is special (v3, Codex OS): at every cue the posterior resets to a point mass, so earlier error is discarded, and between cues the normalised fibre update is a stochastic permutation/redraw map (K_g = (1 − η)P_g + ηU), not conditioning on an increasingly rare hidden event. Each step therefore adds its own rounding (no cancellation) and does not amplify inherited relative error: ≤ 32·50u ≈ 1.8e-13 including the rounding of the float model (T2) | Margin ≥ 5 (typical error ~1e-15) |
| T17 | G7: GAUGE-NA, GAUGE-COV against NA; GAUGE-TRIV against TRIV; NOCUE (NA against TRIV, uniform fibre marginal, base-walk law) | 1e-12 | Two float filters on relabelled models, each within 1.8e-13 of the exact law (T16): difference ≤ 3.6e-13 | Margin ≥ 2.7 by the crude bound (typical ~1e-15) |
| T18 | G7: TOKPERM | 1e-12 | Columns of E and token ids permuted; per-column arithmetic unchanged: expected bit-identical (RV B13); any BLAS blocking difference is within T16 | Margin ≥ 5 |
| T19 | G5: `BayesFilter` log-evidence against the Fraction ln P(h) (evaluated in Decimal) | 1e-10 | Σ of ≤ 33 logs of normalisers; the step-t normaliser carries relative error ≤ (t + 1)·50u: Σ ≤ 50u·594 ≈ 3.3e-12; summation rounding ≤ 33·209·u ≈ 7.7e-13 (\|ln P(h)\| ≤ ln 16 + 31 ln 5 + ln 3 + 31 ln(150) ≈ 209) | Margin ≥ 20 |
| T20 | G5: Decimal reference against Fractions; 120-digit against 80-digit | 1e-45 | 80-digit forward sums, ≤ 32 steps of ≤ 48² operations, inputs from 90-digit division: relative error ≲ 32·50·10⁻⁷⁹ ≈ 1.6e-76 | Margin > 10³⁰ |
| T21 | G5: `enumerate_posterior` (Fraction inputs kept) against the Fraction forward filter, t ≤ 2 | exact | Both exact rationals (RV B14) | No rounding |
| T22 | G5: no non-finite or negative value | exact predicate | Sums and products of non-negative floats are never negative; the zeros of T and E are exact | By construction |
| T23 | G6: Monte Carlo against the exact values (12 comparisons) | 4·SE + 2e-12 | The n ≥ 7 bound applies to next-symbol Parikh order information, not to all twelve comparisons. Uniformly over positive entries needed here, cue and fibre probability ratios are bounded by (1 + 2λ_1)/(1 − λ_1) = 148; matching zero entries contribute zero. With r = 32·50u < 1.8e-13 from T16, first-order perturbation of KL when both probability vectors have relative error at most r is bounded by (ln 148 + 2)r < 1.3e-12. Entropy-based fibre information has error at most (ln 150 + 1)r < 1.1e-12, and a difference of two label log-probabilities has error at most 2r + O(r²). Exact class probabilities are converted directly from Fractions, and row and sample reductions use stable summation; elementary evaluation and reduction error fit inside the remaining 2e-12 allowance. Indicator membership comes from exact certified classes, and indicator SEs use the exact p. The four-SE false-FAIL figure remains an asymptotic diagnostic, not a guarantee. | The 2e-12 floor covers numerical evaluation for all twelve statistics; 4·SE carries sampling variation |
| T24 | O1: TV ≥ 0.3; constancy; zero spreads | exact | Exact rationals; theorem margins 0.851, 0.695, 0.524 | No rounding |
| T25 | FAMILY: pooled β ≤ 0.25 | exact | Exact rationals (label only) | No rounding |
| T26 | PF, S0, file sizes, RC6 N record | mechanical | Test outcomes, git name-status lists, line counts | — |

**Rule (fixed now).** No threshold or tolerance changes after any X6 gate value (G0 onward) has been computed. If a frozen tolerance proves unattainable, the gate's status stands (FAIL under S3 or S5), and any change needs an **owner** decision, never a coordinator ruling alone (K4b §5.6; addendum 10). The rerun and lineage rule (§10.8) never changes a tolerance.

---

## 9. Verification design (RQ 4)

### 9.1 Layers

| Layer | What it checks | Why it is independent |
|---|---|---|
| Fraction enumeration, t ≤ 6 (G2) | Theorem 1, P(h), the DP's counts and classes | A generic 48-state forward filter; it never uses ρ |
| Integer DP, n ≤ 31 (G4) | Every natural quantity | Exact integers; total-mass identity against 1; Pythagorean ladder identities |
| Witnesses in Fractions (G3) | §4 values exactly | Direct forward filtering of named histories |
| Unchanged BayesFilter, FutureOperator, `suffix_posterior` (G5) | The float pipeline against the closed form | Production kernels, used unchanged |
| Decimal reference (G5) | Float error; closed form at high precision | `tests/oracle_profile/independent_reference.py`, an independent unnormalised forward sum |
| Certified enclosures (§5.6) | Every gated log comparison | Two precisions, correctly rounded `ln`, explicit ε |
| Monte Carlo (G6) | DP expectations and masses; label-based estimators against true fibres | A sampling path independent of the DP |
| Controls (G7) | Nulls, gauge equivalence, relabellings | Theorems 2 and 6 |

**Monte Carlo is not the source of any decision value.** Every gated number is exact. This is the main difference from X2a: the observed base reduces everything to path counting.

### 9.2 Exhaustive enumeration (t ≤ 6)

About 1.3 × 10⁵ history nodes per arm [H] (L). The DFS shares prefixes; the forward filter keeps the 48-entry Fraction belief (support ≤ 3 states because the base is observed). For every node: the belief equals Theorem 1's, q* equals the closed form, P(h) equals the product formula. Σ P(h) = 1 per t.

### 9.3 The DP

§5.2. Additionally: A_n and B_n from the DP equal the independent anchor-avoidance recursion of the total-mass identity; for n ≤ 5 the class tables equal the enumeration's (G2).

### 9.4 Certified enclosures

§5.6. The enclosure arithmetic, the recorded term count N with its assertion (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹ (RC6), the memoisation key (§5.6 item 6) and the PASS/FAIL/uncertified logic are unit-tested by the independent author (§10.4, test 11). Attainability: §8.7 T12–T15.

### 9.5 Decimal reference (X§10.2; MD 2)

- **Function:** unchanged `decimal_suffix_posterior(T, E, pi, suffix, digits)` (≥ 60 digits). W verified that it keeps `Decimal` inputs unchanged (`_as_decimal` returns a `Decimal` as is; `_matrix` and `_vector` read object arrays), and converts any other input by `Decimal(float(x))`.
- **Input rule:** T_lift, E and π are passed as nested lists of `Decimal` values produced by **high-precision rational division** (`Decimal(p) / Decimal(q)` in a 90-digit context; 130 digits for the 120-digit repeat). Their precision is recorded. They are not claimed to be finite exact representations of 1/48 or 1/750, and binary floats are never passed and described as the rational model.
- **Comparisons** (no float conversion): Decimal posteriors against the Fraction posterior (Theorem 1, and the Fraction forward filter where t ≤ 6) within 1e-45 (all 48 entries); BayesFilter (the float model) against Fractions within 1e-12; BayesFilter log-evidence against the Fraction ln P(h) (evaluated in Decimal) within 1e-10.
- **Reference set:**
  1. every reachable single-symbol history (18) and every reachable two-symbol history;
  2. W1 and W2 (2 members × 3 y each, Π0), 12 histories (L's minimum);
  3. all 72 canonical W3 histories;
  4. frozen edge cases, also run at 120 digits: (i) no cue: [5]·32; (ii) repeated cues: 32 symbols at the anchor with cue values cycling 15, 16, 17; (iii) return-to-anchor update: Π6 + W2 with y₀ = 0, y = 1 (t = 24); (iv) transport then entry: W1-U (y = 0) followed by cue 17 (t = 9); (v) the first NA Monte Carlo row, in row order, with at least three cues;
  5. the first 64 NA Monte Carlo rows (w_1..w_32).
- **enumerate_posterior** (48^K paths): only t ≤ 2 (G5).

### 9.6 Monte Carlo (validation only)

- Unchanged `HMMSampler(T_lift, E, π, SequenceLayout()).sample(n, rng)` returns tokens uint8 [n, 33] and states int16 [n, 33]. Seeds per §8.6, recorded from `SeedTree.issued`.
- Rows are the independent units; positions within a row are not. Row-level statistics are computed before SEs (X§10.3).
- Filtering uses `tokens[:, :32]`; w_33 is the label target only. BayesFilter runs in batches of 2,048 rows, in row order.
- For each row, the observed segment (n, y, v_32, κ) is read off the tokens and its exact class looked up in the DP tables (q_S and the row-KL).
- Exact DP results remain the gate authority; Monte Carlo alone cannot justify any GO.

---

## 10. Implementation, reuse and cost

### 10.1 Files (S6: three module files plus one optional allowlisted fourth, each ≤ 400 lines; no production change)

| File | Contents | Budget |
|---|---|---|
| `tools/x6_stage0/API.md` | Written contract, committed **before** any module code. Names every function, its inputs, outputs, report keys and seeds; changes no scientific choice; the protocol wins on conflict | — |
| `tools/x6_stage0/x6_model.py` | Constants and seed names; `_X6TorusBuilder`, `build_world`, the punctured complex; S₃ helpers; `seam_letter`, `edge_labels(arm)`, gauge arrays; `lift(T_base, labels, eta)` (Fractions, then float); `emission(kind)`; closed-form oracle (Theorem 1); face holonomies, flux, cover cells and certificate; k-gram recursion; gates G0, G1 | ≤ 400 |
| `tools/x6_stage0/x6_exact.py` | Fraction enumeration (G2); templates, witnesses, matched statistics, β table, challenge and 4×8 comparator (G3); `segment_dp(arm, n_max)` with Python integers, aggregation to the ladder; K-blk DP; G_S, G_k, J_k, J^fib_k, I^fib_k, masses; Decimal enclosures and the certification logic (G4); O1/O2 | ≤ 400 |
| `tools/x6_stage0/x6_run.py` | Monte Carlo and per-row statistics (G6); numerical and Decimal cross-checks (G5); controls (G7); PoE; labels and outcome (D); `s0_check` (the allowlist rule, the dispatch-record check and the store-lineage check); `run(out_dir, preflight)`; report and NPZ writing (the `d1_seam_checks.run` / `x2a_ph.run` pattern); the per-gate artifact records of §10.8 | ≤ 400 |
| `tools/x6_stage0/x6_dp.py` (**optional**, allowlisted in v2, OS 9) | If used: `segment_dp`, the ladder aggregation, the K-blk DP and the Decimal enclosures with the certification logic and the memo of §5.6 item 6, moved out of `x6_exact.py` (which then keeps G2, G3 and O1/O2). Whether it exists, and which functions it holds, is fixed in `API.md` before the tests are written (§10.2, §10.4). K4b's file footprint had to be split twice (RC12 at its review; an added `k4b_registry_k.py` under ruling R28 during implementation); allowlisting this one file now is cheaper than an S6 escalation later (OS 9) | ≤ 400 |
| `tests/x6_stage0/test_x6_stage0.py` (+ optional `test_x6_stage0_dp.py`) | Independent tests (§10.4) | ≤ 400 each |
| `tests/x6_stage0/AUTHORSHIP.md` | Independence record | — |

- No change to `src/`. No new sampler, filter, runner, registered world or generic bundle/sheaf framework. No import from `tools/d1_seam` or `tools/x2a_stage0` (patterns only; X§11.1).
- If any module file would exceed 400 lines, or a module file other than the three planned files and the optional `x6_dp.py` is needed, stop and escalate (S6).

### 10.2 Contract first

`API.md` is committed before any module code (D-1 / X2a pattern). It fixes function names and signatures, array shapes and dtypes (16 versus 48 indexing via `state(i, x)`), the seed map, the report keys (`protocol`, `protocol_sha256`, `verdict`, `first_failed`, `gates`, `exact`, `natural`, `challenge`, `blocks`, `controls`, `mc`, `decimal`, `outcome`, `labels`, `seeds`, `model_sha256`, `cpu_s`), and the S0 allowlist. v2 additions: whether the optional `x6_dp.py` exists and what it holds (§10.1); the per-gate artifact files and their records (§10.8); which report fields are volatile (`cpu_s`, timestamps, absolute paths) and are therefore excluded from the bit-identical comparisons of §10.8. v3 addition (Codex OS): oracle quantities computed with Fractions or Python integers are tagged **exact**; logarithmic oracle quantities computed under §5.6 are tagged **enclosure**, with v₈₀, ε, recorded N and, where applicable, certification status. Monte Carlo estimates, floating-point validation diagnostics and resource measurements retain their own report types and are not labelled exact or certified enclosures. It changes no scientific choice.

### 10.3 Six-field reuse assessment (signatures verified at 978e17f; v2: every reused file is byte-identical at R = f8e5f12, §8.1 review-base record)

| Field | Assessment |
|---|---|
| **1. Existing, reused unchanged** | **World:** `QuotientLatticeBuilder` (ClassVar `family`, `expected_betti`, `identifications`; `.build(WorldConfig) -> WorldSpec`; vertex id `x·dims[1] + y`; local-lexicographic cells from `lattice_cells`), `Identification(axis, kind)`, `WorldConfig(family, dims, metric)`, `WorldSpec.validate()`, `CubicalComplex(n_vertices, cells)` (`betti(p)`, `boundary_matrix(k)`, `euler_characteristic()`, `one_skeleton()`), `world.complex.check_boundary_closed(cx)`, `world.complex.rank_mod_p(matrix, p)`, `world.metrics.check_flat_bounds(dist, dist_graph, n_axes, tol=1e-9)`. **Process:** `TransitionBuilder().build(world, TransitionConfig(p_stay=0.2)) -> TransitionSpec(T, pi, p_stay, d_max)`. **Dataset/contracts:** `HMMSampler(T, E, pi, layout).sample(n, rng) -> (tokens uint8 [n, 33], states int16 [n, 33])`; `SequenceLayout()` (n_obs = 33, analysis_position = 32); `SeedTree(master).generator(name, *scope)` and `.issued`. **Oracle:** `BayesFilter(T, E, pi).run(tokens) -> FilterResult(b, q, log_evidence, ce)` (P ≤ 33; `q[:, t] = b_t T E`; raises StageFailure on an impossible history); `FutureOperator(T, E).F1(b)`. **Oracle profile:** `validate_process(T, E, pi, tol=1e-12) -> dict` (raises ProfileError); `suffix_posterior(T, E, pi, tokens, K)` (stationary restart, 1 ≤ K ≤ L). **Reference:** `tests/oracle_profile/independent_reference.decimal_suffix_posterior(T, E, pi, suffix, digits)` and `enumerate_posterior(T, E, pi, suffix)` (Fraction inputs kept). **Meter:** `tools/x4_oracle_profile/meter.py` with `controls.py` and `winjob.py` (`MEMORY_CAP = 8 * 1024**3`, verified at f8e5f12), unchanged, store-local binding. **Patterns:** D-1 / X2a local unregistered builder, first-failure gates, `s0_check`, API-first contract, clean-context tests with AUTHORSHIP.md, store-local meter binding, `report.json` + `model.npz` |
| **2. Genuinely missing** | The seam-labelled local system and its 48-state lift with typed indexing; the anchor-cue emission and its variants; the closed-form transport oracle; the cover certificate; the segment DP over (v, κ, g) and its ladder aggregation; K-blk; the witness templates, β and challenge tables; certified Decimal enclosures |
| **3. Smallest change** | One new tool directory with three files and one test directory, on public interfaces only (§10.1). No registered world, no `src/` edit |
| **4. Stable interfaces and invariants** | `src/` and the oracle kernels byte-identical (S0); WORLD_REGISTRY untouched; P ≤ 33; vertex (16) and lift (48) indexings never conflated; emit-then-transition; stationary start; privileged quantities (fibre, holonomy, labels) never leave the analysis; exact zeros preserved as integer statements |
| **5. Relevant regression checks** | The PF list (§8.1), including the unchanged `tests/d1_seam` and `tests/x2a_stage0` |
| **6. Next plausible extension (not built now)** | Stage 1 reuses the template generator, the DP competitor tables and the closed-form readout. X6-II (in-context flux inference) would reuse `lift` with a mixture over NA and ZC, which have equal cover Betti numbers and differ only by the flux and the order. Promote anything into `src/` only when a second consumer exists |

### 10.4 Independent test author (D-1 / X2a pattern, binding)

- The tests are written by an agent **other than the module author**, **after** the protocol is frozen and `API.md` is committed, and **before** the module exists.
- The author may read the frozen protocol, `API.md`, the production and reference code the tests call (§10.3 field 1) and `pyproject.toml`; must **not** read, list or search `tools/x6_stage0/*.py`; executes nothing. The worker runs the tests in PF.
- `AUTHORSHIP.md` records what was read, not read and executed.
- Corrections to a test file are made only by its author. No formatter is ever run over `tests/x6_stage0` (the module author formats module files by name only; v2, W, after K4b §11.4).
- Required tests (each with an independent reference importing nothing from the module's kernels):
  1. literal conventions: the neighbour table, S₃ arrays and composition order, tok, `state(i, x)`;
  2. T_base and T_lift from Fractions (74/375, 1/750); G0 counts and Betti numbers; the punctured complex (1,2,0); cover Betti numbers and boundary-circle counts per arm by independently coded lifting;
  3. face holonomies, the flux per arm, f★'s local-lexicographic row (15, 12, 3, 0);
  4. an independent Fraction path-sum for W1 and W2 (TVs, probabilities, set gaps) and the W3 multiplicities 16/4/4 with the 1/3 non-identity fraction;
  5. k-gram equality for k ≤ 4 and the named 5-gram difference;
  6. the ZC witness; the AB fixed-point case (y = 2 never ambiguous under ∅);
  7. gauge equivalence (GAUGE-NA, GAUGE-TRIV, GAUGE-COV), NOCUE, TOKPERM and ETA1 on a few short histories;
  8. the DP against exhaustive short paths (n ≤ 6), the total-mass identity for t ≤ 8 by brute force, and count types: Python ints, with an n = 31 count exceeding 2⁶⁴ represented exactly;
  9. the 4×8 comparator by independent enumeration of the 24 orderings: posteriors 1 and 4/5, accuracy 1, and the classification-versus-calibration distinction;
  10. Decimal input handling: Decimal inputs from rational division pass through `decimal_suffix_posterior` unchanged in type;
  11. the enclosure and certification logic on hand-made values (PASS, FAIL, uncertified; M_lower and M_upper); v2: the recorded term count N and the assertion (N + 10)·10⁻⁷⁸ ≤ 10⁻⁶¹ (RC6), and the memo key (precision, kind, n, w, z) returning values identical to recomputation (OS 3);
  12. the outcome logic (GO_X6_NATURAL, GO_X6_CHALLENGE_ONLY, INCONCLUSIVE_NATURAL including the S8 path, STOP_X6, WITHHELD). v2 cases: under S8 a completed G4 check that fails gives S3 (FAIL), not INCONCLUSIVE_NATURAL; under S8 the designed sentence keeps its window clause only when the Theorem 4 integer checks completed and passed; the S8 NOT_RUN set is exactly G6 plus the DP-dependent G7 items named in §8.5; a wall-limit kill gives INVALID (S7), never INCONCLUSIVE_NATURAL;
  13. registry hygiene (WORLD_REGISTRY unchanged after import and run) and the geometry guards: `is_x_periodic` and `point_distances` monkeypatched to raise, with `point_distances` patched under **both** names, `topo_pilot.process._geometry.point_distances` and `topo_pilot.process.emission.point_distances` (`emission` imports it by name; v2, OS 5), and `topo_pilot.process._geometry.is_x_periodic`;
  14. the 400-line limit;
  15. (v2) G6's indicator-mass SE from the exact p (OS 1) on hand-made values, including p = 0 with zero hits (PASS) and p > 16/(2¹⁸ + 16) with zero hits (FAIL); the R_S key-equality constancy check of G3 (OS 2) on hand-made keys;
  16. (v2, §10.8) the rerun and lineage rule on a temporary store under the §10.5 scratch root: the run refuses a store holding an unrecorded file; a superseded attempt is archived with a `SHA256SUMS` manifest; a rerun whose unaffected per-gate artifact differs by one byte is INVALID/LINEAGE; volatile report fields are excluded from the comparison;
  17. (v3, Codex OS) ETA1's distinction between non-trivial flux and predictive zero: its f★ flux is NA's 3-cycle, yet q* = q_H1 = q_Parikh at every reachable history (§3, note after Theorem 2); an S0 marker collision: a PF or S0 gate marker, gate directory or gate-log entry present in `run/` at S0's lineage check gives INVALID (§10.8 item 1, §8.1 S0 item 6); manifest acceptance without self-hashing: a recorded superseded attempt's `SHA256SUMS` is accepted although it does not list or hash itself, while a missing listed file or a hash mismatch gives INVALID/LINEAGE (§10.8 item 7).

  The store-local meter binding is not in the repository, so it is not covered by these tests; it is bound by S0 item 5 (sha256 and import directory in the dispatch record) and PF's record of the child environment (§8.1).

### 10.5 Meter, TEMP on X: outside the project root, store and freeze bindings (MD 10; v2, RU (d), OS 4)

- **Store:** `X:/Downloads/projects/topo-pilot/x6-stage0-oracle-store/` (outside the repository). v2 layout (§10.8): at the root, the meter's own bookkeeping (`x6_meter_bind.py`, the CPU ledger, its emergency file and locks, `logs/`); `run/` with the scientific outputs of the active attempt (`preflight.json`, `gates/<gate>/` per-gate artifacts, `GATES.jsonl`, `report.json`, `model.npz` with T_base, T_lift per arm, E, E_cov, E_nc, E_σ and their SHA256); `superseded/<job>-a<k>/` for archived attempts, one unique directory per attempt (§10.8 item 4). **No `tmp/` in the store** (RU (d)).
- **Meter:** the unchanged job-0014 meter through a store-local binding `x6-stage0-oracle-store/x6_meter_bind.py` that rebinds module names only (the `x2a_meter_bind.py` pattern): `meter.OUT`, `LEDGER`, `LOCK`, `EMERGENCY`, `ACTIVE`, `LOG_DIR` to the store; `meter.CAP_S = meter.STOP_NEW_S = inf`; `controls.JOB_ID`, `controls.TASK_SHA256` and `meter.WORKER_SESSION` filled in at dispatch (the inherited job-0014 identities are never used). `OUTPUT_CAP` (128 MiB) and the Job Object memory limit, **8 GiB, `winjob.MEMORY_CAP`** (v2, OS 4), stay at their job-0014 defaults and are not rebound; the forecast output is far below 128 MiB and the memory forecast below 2 GiB, within both the 8 GiB limit and the owner's 12 GiB. A MemoryError under this limit inside G4 is S8 (§8.5).
- **Meter import path (v2, OS 4).** The binding inserts `<execution worktree at H>/tools/x4_oracle_profile` (§10.7) into `sys.path` and imports `controls`, `meter` (and through it `winjob`) from there, never from the main worktree or another checkout (the X2a binding hard-coded `REPO`). The dispatch record holds the binding file's sha256 and this directory; S0 item 5 re-checks both at launch.
- **Launch:** `python -I x6_meter_bind.py --label <stage>__<label> --max-cpu inf --max-wall 21600 -- CMD`. Measure-only; one thread (the meter sets OPENBLAS/MKL/OMP/NUMEXPR/VECLIB thread variables to 1). CMD runs the venv interpreter with `-s` and `PYTHONPATH=<execution worktree>/src` (§10.7). A kill at `--max-wall` is S7 (RC5).
- **TEMP and pytest basetemp outside the project root (MD 10; v2, RU (d), rulings R24 and R27).** Every metered command, and the worker's own shell, is launched with `TEMP`, `TMP` and `TMPDIR` set to `X:/Downloads/topo-scratch/<job>/tmp` (on X:, outside `X:/Downloads/projects/topo-pilot/`). Every pytest run gets `--basetemp X:/Downloads/topo-scratch/<job>/pt-<label>`. Nothing temporary is written under the project root (the store holds no `tmp/`). W verified that the meter passes the parent environment to the child (`env = dict(os.environ, …)` in `meter.py`). PF records the resolved `tempfile.gettempdir()` and the basetemp, and fails if either lies outside `X:/Downloads/topo-scratch/<job>/`. Nothing is written to C: beyond the interpreter's own needs; S7's disk floors are checked before each stage.
- **Freeze bindings (S0):** R = `f8e5f12b2f83ecf8b6a32189705a03ff98afa28d` (v2; v1's 978e17f superseded, §8.1); H pinned at dispatch; kernel base `c364f95e5573940cdc24b569b0fb7c6a16c97ab8`; request SHA256 `18E77F7E5BAE48AACC08C8A48560DEEDC0A543531C11B2E09D8684B36C9EFBE1`; the protocol SHA256 in the freeze record; `SeedTree(420700)`; the paths of §10.1, §10.5 and §10.7; the sha256 and import directory of `x6_meter_bind.py` (S0 item 5).

### 10.6 Cost (forecast, not benchmarked; measured only; one thread)

| Part | Forecast |
|---|---|
| PF (regression suites, new tests, file sizes) | 3–5 min (X2a: 18.5 s of suites plus its tests) |
| G0–G1 (build, covers, k ≤ 5 reachable strings for 4 arms) | < 1 min |
| G2 enumeration, t ≤ 6, 4 arms | 2–8 min |
| G3 witnesses, β, challenge | < 1 min |
| G4 Parikh DP per seam-supported arm (dict DP; reachable keys ≪ 5 × 10⁶ per layer), K-blk, Decimal enclosures at 80 and 120 digits (v2: memoised by (precision, kind, n, w, z), §5.6 item 6, which cuts the Decimal work by orders of magnitude, OS 3; not benchmarked) | 5–20 min |
| G5 cross-checks and the Decimal reference (≈ 200–300 histories) | 1–4 min |
| Monte Carlo (2¹⁸ + 4·2¹⁶ + 2¹⁴ rows; BayesFilter 32 steps × 48²), G6, G7, PoE | 3–8 min |
| **Total** | **≈ 15–45 CPU-min** (L 10–20; X 10–45), peak < 2 GiB |

Forecasts only [H]. The `--max-wall 21600` limit is an environment parameter; a kill there is S7, and the rerun may raise it (RC5).

### 10.7 Execution worktree (v2, OS 6; K4b §11.6 pattern)

- A new worktree `X:/Downloads/projects/topo-pilot/topo-pilot-x6` on branch `x6-<job>`, created from R; the implementation commits on it give H. PF, S0 and every stage run **in this worktree at H**, never in the main worktree (which currently carries untracked `output/`, `research_audit_export/`, `tmp/` and uncommitted edits under `src/`; `tools/check_file_sizes.py` would count untracked files, and the uncommitted edits would not be H).
- Before PF, `git -C <worktree> rev-parse HEAD` equals H and `git -C <worktree> status --porcelain --untracked-files=all` is empty; both are recorded in `preflight.json` (§8.1).
- `PYTHONPATH=<worktree>/src` is set and the venv interpreter runs with `-s`; the editable install would otherwise import main's `src` (C1′ R9).
- The store-local meter binding imports the meter from `<worktree>/tools/x4_oracle_profile` (§10.5).

### 10.8 Rerun and lineage rule (fixed in advance; v2, RU (c); K4b §11.8 pattern)

1. **Per-gate artifacts.** For G0–G7 and D, the run writes every payload by exclusive create into `run/gates/<gate>/` and appends to `run/GATES.jsonl`, per gate, a record with its status and the sha256 of every file it wrote. A marker is written before each of these gates starts. PF and S0 create no gate marker, gate directory or gate-log entry before S0 validation has finished: at S0’s lineage check, `run/` contains only this attempt’s `preflight.json`. PF and S0 statuses may subsequently be copied into the gate log. Volatile fields (`cpu_s`, timestamps, absolute paths; named in `API.md`) are kept out of the per-gate files and out of the comparisons below.
2. **Final outcomes.** A PASS gate, and a valid scientific outcome of D (O1, O2, the outcome and the labels, including a certified FAIL, STOP_X6, GO_X6_CHALLENGE_ONLY and INCONCLUSIVE_NATURAL), are final and are never rerun to obtain another outcome. A validity FAIL (S3, S5) or an incomplete attempt stays stopped unless item 3 or item 6 applies.
3. **Technical correction.** A coordinator may authorise a technical correction only for a documented X6 implementation or environment defect. The ruling names the defect, the correction commit (a new H, still inside the S0 allowlist), the affected gates, the exact artifacts to supersede, and evidence that the correction is independent of the scientific outcome. **At most two correction jobs are allowed per defect.** A failure that shows a theorem, construction or protocol statement to be wrong is not a defect: it stops X6 and returns to planning (owner). This item also covers an interrupted attempt without a terminal gate record when the interruption is attributable to the documented defect.
4. **Supersede, append-only.** The complete failed or interrupted attempt's `run/` moves to `superseded/<job>-a<k>/`, a destination unique to that attempt (its job identifier plus an attempt suffix k = 1, 2, …, never reused; repeated S7 interruptions within one job therefore never collide; v3, Codex OS), together with copies of the ledger entries and logs it produced, under a `SHA256SUMS` manifest; nothing is deleted or edited, and the meter ledger at the store root stays append-only. The rerun recomputes from G0 with the frozen seeds (the run is one deterministic pass). Every per-gate artifact of a gate that the correction does not affect must regenerate **bit-identically**, compared against the archived sha256 values; any mismatch is INVALID/LINEAGE.
5. **Owner escalation.** If the correction would change an already computed outcome-bearing quantity, or the failed attempt computed such a quantity at or after its declared failure point, a coordinator ruling is insufficient: an owner decision is required. Outcome-bearing here means the O1 inputs (TVs, constancy, spreads), the O2 inputs (G_Parikh(32), M_lower and M_upper of M_32(0.01), their enclosures and certification), the label inputs (J_8, D_blk, mean G_Parikh, G_8, β) and every sealed D value of G3 and G4. No owner escalation is needed solely because an unchanged outcome-bearing quantity was computed before that point. No threshold or tolerance may change under this rule (§8.7).
6. **Environment reruns (S7).** An attempt interrupted by owner STOP, the usage limit, a disk floor or the wall limit is archived and rerun under items 4 and 7 with the same frozen specification; such a rerun is not a technical correction and does not count against item 3's limit. Its values must reproduce bit-identically wherever the interrupted attempt computed them. After a wall-limit kill the rerun may use a larger `--max-wall` (RC5).
7. **The store recognises lineage.** Before PF writes anything, `run/` must be absent. Every existing file elsewhere in the store must be explicitly recognised meter bookkeeping, a `SHA256SUMS` manifest belonging to a recorded superseded attempt of this lineage, or an archived file listed in such a manifest. Recognised manifests are lineage metadata and need not list or hash themselves. Every listed archived file must exist and match its recorded sha256. The pre-check is recorded in `preflight.json`; S0 item 6 re-checks the recognised archived lineage and requires `run/` to contain only this attempt’s `preflight.json`. Any other file, missing listed file or hash mismatch is INVALID/LINEAGE.
8. Monte Carlo reruns use the frozen seed streams (§8.6); a rerun never reseeds and never changes n (S5).

---

## 11. Risks, open points and changelog

### 11.1 Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | O2 borderline (G_Parikh(32) ≤ 0.00984 and M_32 ≤ 0.102 [W]; forecasts straddle the thresholds) | GO_X6_CHALLENGE_ONLY is a legitimate outcome (MD 5). No threshold change, no η switch (MD 6), no O2 split |
| R2 | DP memory or time | Adjacent layers only; summaries exported; Decimal memo (§5.6 item 6). S8 (memory, 8 GiB `winjob.MEMORY_CAP`) gives INCONCLUSIVE_NATURAL only if every completed G4 check passed, never a changed definition; a wall-limit kill is S7 (INVALID, rerun with a larger `--max-wall`), never INCONCLUSIVE_NATURAL |
| R3 | Fixed-width integer overflow (A_31 ≈ 7.9 × 10²⁰ > 2⁶⁴) | Python ints mandatory; test 8 |
| R4 | Ambiguity counted at the holonomy level (wrong for ∅) | Image-level definition (Lemma I); FIXED-POINT control; test 6 |
| R5 | Decimal inputs from binary floats described as the rational model | §9.5 input rule; test 10 |
| R6 | Uncertified log comparisons near a threshold | §5.6 enclosures; INCONCLUSIVE_NATURAL |
| R7 | Conflating 16-vertex and 48-state indices | `state(i, x)`; G0; test 1 |
| R8 | Ladder or K-blk applied to gauge arms (gauge-dependent open holonomy) | Defined only for seam-supported arms (§2.4); gauge arms compared by observation law |
| R9 | PoE read as an order test | Descriptive; reading rule (§6.3) |
| R10 | 4×8 classification read as information equivalence | Reading rule (§6.1) |
| R11 | Overclaim: "topology inference", trained models, natural bag gap | §1.4 non-claims; MD 9 |
| R12 | Forecasts or [W] values treated as findings | Labelled; never gates |
| R13 | W3 not discriminating against rev (β = 1/3) | W3 secondary (MD 8); W2 primary in stage 1 |
| R14 | Spurious float failures | Tolerances 1e-12 on float paths; G6 allowance 2e-12; exact paths in Fractions/integers |
| R15 | Registry pollution; geometry traps | Unregistered builder; guard tests |
| R16 | Code over 400 lines per file | Three files planned with budgets; S6 |
| R17 | TEMP on C: filling the system drive; scratch inside the project root polluting later inventories (K4b R24/R27) | TEMP/TMP/TMPDIR and pytest `--basetemp` under `X:/Downloads/topo-scratch/<job>` (§10.5); PF records and checks it |
| R18 | Stage-0 histories reused in a trained stage | Exposure rule (§1.4) |
| R19 | Self-assessed readiness | Result-blind review done (RC1–RC6); Codex result-blind review of v2 before freeze |
| R20 (v2) | Main moves under the binding (it moved from 978e17f to f8e5f12, with `M` entries for `pyproject.toml` and `src/topo_pilot/learner/trainer.py`) | Review base re-recorded with disclosure (§8.1); `pyproject.toml` protected; the Codex v2 review re-checks it (§12.6 O1) |
| R21 (v2) | A frozen tolerance proves unattainable (C1′ R13) | Attainability table before data (§8.7); any later change needs the owner |
| R22 (v2) | An aborted attempt's files block or contaminate a rerun (C1′ job 0039) | Rerun and lineage rule (§10.8); store pre-check |
| R23 (v2) | PF counts untracked or uncommitted files of the main worktree | Clean worktree at H (§10.7) |

### 11.2 Open points for the result-blind review (writer's readings, not new decisions)

1. **X's extra controls as required.** MD 2 adds GAUGE-COV, NOCUE and TOKPERM; MD 7 makes ZC and the GAUGE arms required. W made all of them required (G7) because X§8 lists them as required and they cost seconds.
2. **W3′ (t = 26)** is kept as an exact cross-check (AN §3), reported and not part of O1.
3. **S8** integrates X§11.3's resource rule with L's first-failure semantics as stated in §8.5.
4. **PoE scope:** NA, AB and TRIV on 2¹⁴ rows each (the reading rule needs exactly these).
5. **Decimal reference set:** the union in §9.5 (L's minimum, X's set, frozen edge cases).
6. **Enclosure width** ε = 10⁻⁶⁰·max(1, Σ|terms|) (§5.6).

**Review result (v2).** The reviewer agreed with readings 1, 2, 4 and 5; with 3 subject to RC4 (S8) and RC5 (the wall limit); and with 6 subject to RC6 (the N assertion). All three RCs are applied (§12.1). These points are closed.

### 11.3 Section sources

| Section | Source |
|---|---|
| §1 | RQ; L§1, §9; X§2, §13; AN §2; X2A-FROZEN-v1 §1 (format) |
| §2 | L§2 = X§3 (AN §0.1); X's neighbour and label arrays; L's gauge arms; X§8 GAUGE-COV, NOCUE, TOKPERM; AN §2 |
| §3 | L§3 (Lemmas 0, 0′, 1; Theorems 1–8), re-proved by W; Lemma I and Corollary 4′'s explicit 5-gram from W, after X§7.5 and AN §1.4; Theorem 8's explicit witness from W |
| §4 | L§2.4, §4.1–4.2; X§5 (W3 at t = 32, MD 2); X§6.1–6.2; AN §1.1–1.3; MD 8 |
| §5 | L§4.2–4.4 (ladder, MD 1); X§7 (DP, coverage, enclosures, MD 2); MD 5, MD 9; W bounds |
| §6 | X§6.3 first partition (MD 2–3); L§4.3 K-blk and PoE; AN §1.6 |
| §7 | L§2.2, §5.1 G7; X§8; MD 7 |
| §8 | L§5 (gates, O1, O2, labels); X§9 (INCONCLUSIVE_NATURAL); MD 4, 5, 11; D2A §11.3 D5; X2A-FROZEN-v1 §5 |
| §9 | L§6; X§10 (Decimal input rule, edge cases, enclosures) |
| §10 | L§7; X§11; X2A-FROZEN-v1 §8; job-0025 meter binding; MD 10; v2: OS 3, 4, 6, 9; RU (c), (d); K4B-FROZEN-v1 §11.4, §11.6–§11.8 |
| §8.7 (v2) | RU (b); K4B-FROZEN-v1 §5.6; W's error bounds |
| §8.1 review-base record (v2) | RU (a); W's read-only git at f8e5f12 |
| §12 (v2) | The review (RC1–RC6, OS 1–9) and RU |

### 11.4 Corrections, flags and arithmetic re-checks

| # | Item | Status |
|---|---|---|
| C1 | **X§6.3: the second (eight-block) partition claim** "each individual loop block is independent of Z" | **Error** (AN §1.6; MD 3). Single-loop blocks are strongly dependent on Z; that comparator reproduces the 4×8 values, not Δ_challenge. **Dropped**; it appears nowhere in this protocol |
| C2 | X§1 provenance ("the worktree lacks the tools") | Stale (AN §0.4). main @978e17f contains both; the binding was R = 978e17f with the D5 allowlist (MD 11). v2: R = f8e5f12 (C21) |
| C3 | L's code state d244e17 | Superseded by R = 978e17f (v1), then by R = f8e5f12 (v2, C21). W re-ran the kernel diff from c364f95 at v1: empty. d244e17→978e17f changed only `reports/he_summary/*`; 978e17f→7c8da1f (C1′ merge) changed only `docs/c1prime`, `tests/c1prime`, `tools/c1prime` and `state/`, none of them protected |
| C4 | L§4.2 β cell for W1 "last crossing, first crossing: per y ½, −1, ½" | **Incomplete (W).** ½, −1, ½ is the last-crossing row; first-crossing is the negation, −½, 1, −½ (two-member family: q̃_first = −q̃_last). Pooled 0 for both; no label changes |
| C5 | L§4.2 W3 first/last "computed by run" | W derived: first per y (1/6, −1/3, 1/6), last per y (−1/6, 1/3, −1/6), both pooled 0. The run computes them exactly (G3); not gates |
| C6 | L§4.2 "parity: (k_x + k_y) mod 2 = sign ρ" | True in NA and AB only; in ZC every holonomy is even. The parity competitor is defined as the count statistic (§5.1) |
| C7 | L§4.4 E_amb at the holonomy level | Replaced by the image level (X§7.5). Lemma I proves the two coincide for parity, counts, H1 and Parikh in NA; they differ for ∅ (FIXED-POINT control) |
| C8 | L D2 (bipartite suffix) and D5 (λ index) as "draft corrections" | Wording only: a stay-free remark and a convention (AN §1.5). Remark B |
| C9 | W3's canonical instance | t = 32 per MD 2: TV λ_32 = 0.5238831, set gap 0.037832 [W]. L's licence value 0.591 is replaced by 0.524; t = 26 is kept as W3′ |
| C10 | L's descriptive η = 1/100 sensitivity | **Removed** (MD 6: 1/100 is not run) |
| C11 | X's mass threshold 1/256; AN's optional O2a/O2b split | Rejected (MD 5). INCENTIVE remains a descriptive label only |
| C12 | X§9.2's extra challenge thresholds (full TV ≥ 0.06; gap ≥ 1e-3) | Not gates (MD 4: O1 is the draft's). The quantities are computed and reported; their identities are gated in G3 |
| C13 | L's Decimal set (24 histories) and its 1e-12 comparison | Superseded by the §9.5 union, rational-division inputs and the 1e-45 Fraction comparison (MD 2; AN §4.1) |
| C14 | L's G1 "every arm is indistinguishable by every statistic of ≤ 4 consecutive symbols" | Holds for the η = 1/50 seam-supported arms; ETA1 differs already at k = 2 (cue, stay, cue). Made explicit in Corollary 4′ |
| C15 | Ladder and K-blk for gauge arms | Undefined (gauge-dependent open holonomy); restricted to seam-supported arms (W) |
| C16 | L's [H] forecasts against W's hand values | E_cue(32): L 0.80–0.90, [W] ≈ 0.764 (**outside L's range**); I^fib(32): L 0.3–0.5, [W] ≈ 0.512 (slightly above); G_8/G_1: L 0.4–0.7, [W] ≈ 0.325 (**below**); I^fib_8 ≈ 0.298 and G_1(32) ≈ 0.0272 inside L's ranges. Forecasts only; no decision depends on them |
| C17 | AN §1.2 cross-checks "0.24229/5 = 0.048458" and "(0.85644 − 0.39293)/5 = 0.092702" | Rounding of the inputs only: W gets 0.242297/5 = 0.048459 and 0.463506/5 = 0.092701, matching L |
| C18 | Values re-checked and confirmed | λ_8, λ_18, λ_26, λ_32 and /5; set gaps 0.092701, 0.061119, 0.048459, 0.037832; H(q̄) 1.034076, H(q_L) 0.844915; member probabilities 2.6667e-7, 2.7307e-14, 6.9905e-20, 4.4739e-24; templates 1.6e-6, 1.638e-13, 5.03e-18, 3.22e-22; 16/4/4; β_rev +1/3 and balanced 0; 4×8 posterior 4/5, (1/3)ln(5/4) = 0.0743812, Δ_add,8 = 0.0022197; I(Z) = 0.867563; I^fib_1 = 0.068663; DP bound ≈ 5.03 × 10⁶; Hoeffding 0.00526; false-FAIL 7.6e-4; short-window bounds 4 and 7 with their attaining pairs; ZC witness; cover Betti numbers; flux words; the neighbour table |
| C19 | X§6.2 "I(Z; W_{33−k:32}) = 0 for k ∈ {1, 2, 4, 8}" | Correct; it extends to every k ≤ 9 (the common 9-token tail) |
| C20 | X's Monte Carlo sizes (65,536 per arm) | L's sizes adopted (AN §3); X's simultaneous-interval wording is covered by the 4·SE family with its stated union-bound diagnostic |
| C21 (v2) | v1's R = 978e17f under the D5 rule | **Superseded.** The protected-path diff 978e17f→f8e5f12 is non-empty (`M pyproject.toml`, `A src/topo_pilot/learner/multihorizon.py`, `M src/topo_pilot/learner/trainer.py`); none touches a reused function; R = f8e5f12 recorded with disclosure (§8.1). v1's S0 item 4 ("kernel diff from c364f95 empty") is restated as an exact two-entry list (§8.1 item 4; §12.6 O1) |
| C22 (v2) | v1 §8.3 "O2 implies the same for H1, counts and parity" (carried over from L§5.2) | **Error** for O2(ii) (RC1): row-level KL is not monotone under refinement. Replaced |
| C23 (v2) | v1 §1.4 "the strongest commutative predictor"; "every commutative predictor … loses [Δ_challenge]" | **Overclaims** (RC2, RC3). Replaced by the finest commutative statistic of the crossing word, with the Bayes/any-function lower bound; and by "at least Δ_challenge, with equality for the optimal one" for functions of the bag, bigram bag, H1 class or counts |
| C24 (v2) | New hand values [W] | N ≤ 9·96·376,991 = 325,720,224 ≈ 3.3e8, so (N + 10)·10⁻⁷⁸ ≤ 3.3e-70 ≤ 10⁻⁶¹ (§8.7 T12); K-blk ≤ 5,423,760 terms; zero-hit threshold 16/(2¹⁸ + 16) = 6.10e-5 and e⁻¹⁶ = 1.13e-7 (§8.2); float error bounds of §8.7 (14u = 1.55e-15; 32·50u = 1.78e-13; log-evidence ≤ 3.3e-12 + 7.7e-13; \|ln P(h)\| ≤ 209.1; min non-zero next-symbol probability 1.33e-3; ln 18.10 = 2.896; per-row KL error ≤ 1.38e-12; v3: these last three T23 figures are superseded by Codex RC2's T23 text). None is a gate |

---

## 12. v1→v2 changes

### 12.1 Required changes (all adopted as written, RU)

| RC | Change | Location in v2 (text) | Conformed cross-references |
|---|---|---|---|
| RC1 | O2(ii) implies nothing for coarser competitors | §8.3, O2 paragraph: the sentence replaced verbatim | §11.4 C22 |
| RC2 | Natural sentence: finest commutative statistic of the crossing word, Bayes predictor, any-function lower bound | §1.4, natural sentence: the text after "Under the stationary natural-history distribution, " replaced verbatim | §11.4 C23 |
| RC3 | Designed sentence: "at least [Δ_challenge] … with equality for the optimal one", functions of bag, bigram bag, H1 class or counts | §1.4, designed sentence: the clause replaced verbatim | §5.5 conformed; §11.4 C23 |
| RC4 | S8: completed G4 checks must pass; DP-dependent G7 items named; window clause | §8.5, S8 row replaced verbatim, plus one appended sentence (§12.5 item 1) | §1.4 (parenthetical after the designed sentence); §8.4 INCONCLUSIVE_NATURAL row; §10.4 test 12; §11.1 R2; §11.2 review result |
| RC5 | S7: wall-limit kill | §8.5, S7 row replaced verbatim | §8.4 INCONCLUSIVE_NATURAL row; §8.5 closing paragraph; §8.6 resources row; §10.5 launch bullet; §10.6 note; §10.8 item 6; §10.4 test 12; §11.1 R2 |
| RC6 | Enclosure premise: N ≤ 10¹⁷ and the recorded-N assertion | §5.6 item 3, sentence replaced verbatim | §8.2 G4 row; §8.6 enclosures row; §8.7 T12–T14; §9.4; §10.4 test 11; §11.4 C24 |

### 12.2 Optional suggestions adopted (RU)

| OS | Change | Location in v2 |
|---|---|---|
| 1 | G6 SE for the indicator masses from the exact p | §8.2 G6 row ("SE (v2, OS 1)") and the G6 diagnostics paragraph; §8.6 Monte Carlo row; §8.7 T23; §10.4 test 15 |
| 2 | G3 constancy by R_S key equality | §8.2 G3 row; §8.7 T9; §10.4 test 15 |
| 3 | Decimal KL memoised by (n, class weight vector, z) | §5.6 item 6 (key made exact: precision, kind, n, w, z); §8.2 G4 row; §9.4; §10.1 `x6_dp.py` row; §10.4 test 11; §10.6 G4 row |
| 4 | Dispatch record: sha256 of `x6_meter_bind.py` and its meter import path; 8 GiB `winjob.MEMORY_CAP` named | §8.1 S0 item 5; §8.5 S0 row; §10.5 meter bullet, new "Meter import path" bullet, freeze-bindings bullet; MEMORY_CAP named in §10.5 and §8.5 S8 (appended sentence) and the §8.5 closing paragraph; §8.6 resources row; §10.3 field 1 |
| 5 | Guard test 13 patches both names of `point_distances` | §10.4 test 13 |
| 6 | PF in a clean worktree at H | §8.1 PF; new §10.7; §11.1 R23 |
| 7 | `pyproject.toml` in the S0 protected paths | §8.1 item 3 (protected paths); §8.1 review-base record |
| 8 | J^fib_full(t) := J^fib_t(t) | §5.3 table (new row); §8.2 G6 row (reference) |
| 9 | One optional fourth module file allowlisted | §8.1 allowlist (`tools/x6_stage0/x6_dp.py`); §10.1 heading, table row and S6 bullet; §8.5 S6 row; §10.2 |

### 12.3 Coordinator additions (RU (a)–(d))

| Addition | Location in v2 |
|---|---|
| (a) Code binding: diff 978e17f→f8e5f12 over the protected paths plus `pyproject.toml`; new review base | Header "Code read" row; MD table row 11; §8.1 item 3 (R = f8e5f12), item 4 (restated), "Review-base record"; §10.3 heading; §10.5 freeze bindings; §11.1 R20; §11.4 C2, C3, C21; §12.6 O1, O2 |
| (b) Tolerance attainability, owner rule for any post-data change | New §8.7 (T1–T26 and the rule); §8.0 bullet; §8.6 tolerances row; §9.4; §11.1 R21; §12.6 O3 |
| (c) Rerun and lineage rule (append-only supersede with `SHA256SUMS`, bit-identical regeneration, ≤ 2 correction jobs per defect, owner escalation) | New §10.8; §8.0 bullet; §8.1 S0 item 6; §8.5 S0, S3 and S5 rows and closing paragraph; §10.1 `x6_run.py` row; §10.2; §10.5 store layout; §10.4 test 16; §11.1 R22; §12.6 O5 |
| (d) Every pytest basetemp and TEMP under `X:/Downloads/topo-scratch/<job>` | §10.5 TEMP bullet (and no `tmp/` in the store bullet); §8.1 PF record; MD table row 10; §11.1 R17; §10.4 test 16 |

### 12.4 Other v2 edits

Title and header (protocol id, role, date, review applied, authority, other inputs, code read, arithmetic, next step); the "v2 additions" line under the MD table; §10.4 author bullet (corrections by the file's author only; no formatter over `tests/x6_stage0`; W, after K4b §11.4); §10.6 forecast note; §11.1 R19; §11.2 "Review result (v2)"; §11.3 v2 rows; §11.4 C22–C24. No threshold, construction, gate value, seed or theorem changed.

### 12.5 Where v2 extends a reviewer replacement text

1. **RC4.** The S8 row is the reviewer's text verbatim, with one sentence appended at the end of the cell: "The memory limit is the unchanged Job Object limit of 8 GiB, `winjob.MEMORY_CAP` (§10.5)." OS 4 asks for the limit to be named in S8; appending keeps the reviewer's wording intact.

RC1, RC2, RC3, RC5 and RC6 are verbatim at the stated locations. The parenthetical "(Under S8 the last clause is kept only as §8.5 S8 states.)" after the designed sentence in §1.4 lies outside the licensed sentence and conforms §1.4 to RC4.

### 12.6 Open items (all resolved in v3)

**Resolution (v3).** The Codex result-blind review of v2 (`coord-x6-review-20261017.codex.md`) recommended accepting O1–O6, and the coordinator's rulings (`coord-x6-review-20261017.rulings.md`) accepted all six as recommended. Every item below is **closed**:
- **O1 resolved:** R = f8e5f12 and the restated S0 item 4 are accepted. Git confirms the disclosed changes and the unchanged reused code. This is a disclosed new review binding, not a claim that the old empty-diff condition passed.
- **O2 resolved:** execution only from the clean H worktree, with the specified import paths (§10.7, §10.5).
- **O3 resolved:** row sums, column sums and stationarity are exact Fraction checks; float validation belongs under `validate_process`'s 1e-12 tolerance (§8.2 G0, §8.7 T2–T3).
- **O4 resolved:** certified lower membership and p = M_lower, even if the interval does not collapse; membership retains the row's image z (§8.2 G6).
- **O5 resolved:** full deterministic recomputation with comparison of unchanged artifacts, after Codex RC3 (§10.8); environment reruns do not consume the technical-correction allowance.
- **O6 resolved:** the chosen module, worktree and scratch names are accepted.

The table records the items as raised in v2.

| # | Item | W's reading or recommendation (v2) |
|---|---|---|
| O1 | **New review base R = f8e5f12** (RU (a)). The reviewer read code at 7c8da1f; the protected-path diff to f8e5f12 has three entries (§8.1). S0 item 4 changes from "kernel diff from c364f95 empty" (unsatisfiable for any descendant of current main) to "exactly the two recorded learner entries" | Accept. Codex re-checks the diff, the absence of `topo_pilot.learner` imports in every reused module and PF suite, and the restated item 4. An alternative item 4 (narrow the kernel paths to `src/topo_pilot/{world,process,oracle,dataset,contracts}`, still empty) is equivalent today; W kept v1's path set with an exact list because it is mechanical and stricter |
| O2 | The main worktree carries uncommitted edits under `src/` (`analysis/x4f_erasure.py`, `experiment/x4f_*.py`), modified `README*.md`, `state/*` and `tools/d2a/d2a_train.py`, and untracked directories. They are on no commit, so they do not affect the binding | Informational. §10.7 requires execution in a clean worktree at H, so they cannot reach X6 |
| O3 | G0's "row and column sums" of T_lift. W reads them as exact checks on the Fraction arrays (§8.7 T2). If they were float sums under the 1e-15 tolerance, the worst-case bound 14u ≈ 1.55e-15 exceeds 1e-15 (typical error ≤ 2 ulp) | Accept W's reading now, before data. Otherwise the float-sum tolerance must be set before the freeze (for example 1e-14); never after data (§8.7 rule) |
| O4 | OS 1 for the interval-valued M_32: the Monte Carlo indicator is "the row's exact class is certified ≥ 0.01", and p = M_lower | Accept (in practice M_lower = M_upper, §5.6, RV B12) |
| O5 | §10.8 recomputes from G0 on every rerun (X6 is one deterministic pass) instead of K4b's restart of only the affected stage; unaffected per-gate artifacts must match bit-identically. S7 environment reruns do not count against the two-correction limit | Accept |
| O6 | Names chosen by W: the optional module `tools/x6_stage0/x6_dp.py` and its contents; the worktree `topo-pilot-x6` on branch `x6-<job>`; scratch `X:/Downloads/topo-scratch/<job>/tmp` and basetemp `pt-<label>` (R24's `pt-*` form) | Accept, or rename before the freeze |

### 12.7 v2→v3 changes (Codex review of v2, VERDICT APPROVE_WITH_REQUIRED_CHANGES; coordinator rulings: RC1–RC3 adopted as written, O1–O6 accepted as recommended, all four optional suggestions adopted)

| Item | Change | Location in v3 |
|---|---|---|
| Codex RC1 | Lemma 1, Theorem 1 and Theorem 2 restricted to seam-supported arms with the standard E (Theorem 2 also η = 1/50); note on ETA1, the gauge arms and NOCUE | §3: Lemma 1 opening, Theorem 1 first sentence, Theorem 2 first sentence (verbatim); new paragraph after Theorem 2's proof (verbatim) |
| Codex RC2 | T23 conditioning argument replaced; tolerance 4·SE + 2e-12 unchanged | §8.7 T23 row (verbatim); §11.4 C24 conformed (old T23 figures marked superseded) |
| Codex RC3 | No PF/S0 gate marker before S0 validation; recognised manifests need not hash themselves | §10.8 items 1 and 7 (verbatim); §8.1 S0 item 6 conformed |
| O1–O6 | Closed as the reviewer recommends | §12.6 resolution list; O4 also conformed in §8.2 G6 (p = M_lower even if the interval does not collapse; membership keeps z) |
| OS: T16 | Explanation cites cue resets and the stochastic fibre update | §8.7 T16 row (conditioning cell) |
| OS: archive | Unique archive destination per attempt, `superseded/<job>-a<k>/` | §10.8 item 4; §10.5 store bullet |
| OS: tests | ETA1 flux versus predictive zero; S0 marker collision; manifest acceptance without self-hashing | §10.4 test 17 |
| OS: reports | Exact oracle quantities and certified logarithmic enclosures distinguished in reports; numerical diagnostics retain their own types. | §10.2 |
| Identity | Title, protocol id, role, review row (v2→v3), next step | Header |

No reviewer text was adapted in v3. Nothing else changed: no threshold, tolerance, construction, gate, seed or theorem content beyond the RC1 scope restriction.

## Freeze record (coordinator)
- **Source:** X6-MERGED-v3.md (sha256 DFBEED1E21EE96E5E631B15BF5DEDE0506925F63BA367F52F890C31C9562C234). Three things differ from it: the STATUS line, this record, and the Codex v3-confirmation residual fix (§10.2 reporting-tag sentence and the §12.7 "OS: reports" row), applied verbatim by the coordinator. The stray trailing "6" in the reviewer text was omitted.
- **History:**
  - **v1** (12DBB22C): writer, from MD 1–11.
  - **Claude clean-context review** (Codex was unavailable on 2026-10-15): RC1–RC6 and OS1–OS9.
  - **Coordinator rulings** coord-x6-review-20261015.rulings.md: everything adopted, plus K4b lessons (a)–(d).
  - **v2** (43550626).
  - **Codex result-blind review** coord-x6-review-20261017.codex.md: APPROVE_WITH_REQUIRED_CHANGES, RC1–RC3.
  - **Rulings** coord-x6-review-20261017.rulings.md: everything adopted, O1–O6 accepted, and 4 optional suggestions adopted.
  - **v3** (DFBEED1E): diff v2→v3 has 22 hunks (X6-MERGED-v2-v3.diff).
  - **Codex v3 confirmation:** CONFIRM_WITH_REQUIRED_CHANGES (one wording fix, applied here).
- **Authority:**
  - OWNER_DECISIONS.v1-a73c869.md (5BD1FDB0…37CD);
  - addendum 3;
  - addendum 9;
  - addendum 11 (order: K4b, then X6).
- **Code reference:** R = main f8e5f12. The protected diff 978e17f→f8e5f12 is `M pyproject.toml` (licence line only), `A learner/multihorizon.py` and `M learner/trainer.py` (training-only). Every reused file is byte-identical. **Execution runs only from a clean worktree at H.** The main working tree may carry another session's uncommitted edits.
- **Execution:**
  - first an implementation job: contract first, independent test authors A/B, modules ≤ 400 lines (up to one optional fourth module), PF in a clean worktree, a coordinator full suite, then the code freeze;
  - then the stage-0 run, measure-only, one thread, with TEMP and basetemp under X:/Downloads/topo-scratch/<job>.
- **Post-data changes:** any change to a threshold or tolerance after X6 data exist needs the owner.
