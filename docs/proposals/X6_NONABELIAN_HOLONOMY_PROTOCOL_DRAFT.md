# X6 protocol draft: non-abelian holonomy — can a next-token learner see π₁ beyond H₁?

14 October 2026. **Proposal only. Nothing in this document was executed:** no world was built, no history was sampled, no oracle was run, and no model was trained or evaluated. The only computation behind it is a scratch check of the group algebra and the Betti numbers of the covering space (§3). That check is mathematics, not an experimental result, and it is not a project artifact.

Governance: the [owner research charter](../../../agent-handoff/NEXT_RESEARCH_AND_WORKFLOW.md#owner-research-charter) applies. X6 is a secondary programme and does not displace priorities 1–3. Running anything requires a frozen task from Codex and owner approval. [PROTOCOL.md](../../../agent-handoff/PROTOCOL.md) requires that "X6 transport starts with an exact-observability audit, not speculative training", so Stage 0 below is oracle-only. Labels [R/M/L/H/S] follow [RESEARCH_LANDSCAPE](RESEARCH_LANDSCAPE.md).

Relation to [X6_TOPOLOGICAL_INVARIANTS](X6_TOPOLOGICAL_INVARIANTS.md): this draft keeps that document's identifiability ladder, its four levels of local-to-global evidence, and its stop rules. It proposes replacing the Z₂ sign transport over a cylinder as X6's **primary** transport formulation. The reason is that Z₂ is abelian, so any Z₂ holonomy factors through H₁. It therefore cannot answer the charter's question about structure *richer than H₁*. The Z₂ case reappears inside this design as Level 1 (§4). Boundary study H6-B remains an optional, separate low-cost study (Appendix A).

**Revision 2 (14 October 2026): merged with the parallel Hebrew draft `x6-plan-1`.** That draft (X6-T: Z₂ sign transport on a 6×4 cylinder, with a T0 gate and a T1 plan) lies outside the repository and was compared to this one. This revision keeps the S₃ design as the primary hypothesis and adopts the following from x6-plan-1:
- the feasibility categories FEASIBLE_NATURAL / FEASIBLE_CHALLENGE / CHALLENGE_ONLY, and a natural suffix-gain statistic G_K (§7);
- full-vocabulary KL and a J ratio as a secondary endpoint, plus a gate on cue mass (§6);
- explicit seeds, splits and sizes (§8);
- a 1,800 CPU-s cap on Stage 0 that includes overhead (§9);
- the H6-B corrections (Appendix A);
- two sources: Zhang & Li 2026 (cosets) and Paluzo-Hidalgo & Ike 2026 (atlases and w₁) (§11).

The prediction of Zhang & Li is now a named competing hypothesis (§4, A4/A9). The det/w₁ part of S2 is toned down: as a method it is not new.

The separate trivial-arm control in x6-plan-1 (2×3 models) is not adopted. The within-model order control (§6) gives the null for H6-NC at half the cost.

---

## 1. Question

**Charter question (X6):** Can models learn topological structures richer than H₁? Can they detect or resolve inconsistencies between local information and global structure, perhaps with sheaf-theoretic methods?

**Operational formulation:**
> A world carries a flat non-abelian transport (a local system of G-sets) over a base complex. Is the next-token prediction of a standard Transformer, trained only on observations, consistent with the transport *composed in path order* (a function of the path class in π₁)? Or is it explained by a mechanism that depends only on counts or on the H₁ class: a bag of tokens, seam-crossing counts, a short context, or the parity of the permutation?

Why this is a test of "beyond H₁" **[M]**: π₁ of a punctured torus is the free group F₂, and its H₁ is Z². The commutator loop [A,B] is null-homologous, so its H₁ class is 0, but it is not null-homotopic. For a representation ρ: F₂ → S₃ with non-commuting images, ρ([A,B]) ≠ e. Every predictor whose dependence on the path passes through H₁, or through any commutative statistic of the path, is constant on a set of loop orderings that share the same multiset of loops. The exact Bayes predictor is not constant on such a set. The test is therefore built so that **every commutative explanation predicts exactly zero**.

Two further points that reinforce the "richer than H₁" interpretation:
- The **closed** torus and the punctured torus have the **same H₁ (Z²)** but different π₁ (Z² versus F₂).
- The base random walk in this design is a walk on the complete torus. The puncture exists only as a non-zero **flux** of the transport through a single face, in the manner of an Aharonov–Bohm solenoid or a lattice-gauge-theory plaquette.

So the "hole" is defined by transport alone, not by anything visible in the walk.

## 2. World and process (proposed values; the Stage 0 audit freezes them)

- **Base:** an L×L torus lattice, L=4, with 16 vertices, 32 edges and 16 faces. The x-seam is the set of edges (3,y)–(0,y); the y-seam is the set of edges (x,3)–(x,0). The **flux face** f★ is the corner face with vertices (3,3),(0,3),(0,0),(3,0), the only face that straddles both seams. The complex used for transport is the torus without the open face f★: χ = 16 − 32 + 15 = −1 and β = (1,2,0).
- **Base walk:** a lazy max-degree walk with probability 0.2 for each of the four neighbours and 0.2 for a self-loop. Every base path of length n has the same probability, 0.2ⁿ **[M]**. The base walk is symmetric, so the stationary distribution over vertices is uniform.
- **Fiber:** X = {0,1,2} with an action of S₃.
- **Connection, arm NA (primary):**
  - Each x-seam edge carries a = (01).
  - Each y-seam edge carries b = (12).
  - Every other edge carries e.
  - Both elements are involutions, so the two directions of an edge carry the same element.
  - Every face except f★ is flat (holonomy e). The holonomy around f★ is a 3-cycle (verified in §3).
- **Connection, arm AB (optional control, not in the first protocol):** a on both seams. Every face is flat, and the world is a Z₂ bundle over the closed torus.
- **Hidden state:** z = (v, x), 48 states.
- **Lifted transition:** T((v,x),(v′,x′)) = T_base(v,v′)·[(1−η)·1{x′ = g_{vv′}x} + η/3]. Here η is the rate at which the fiber is redrawn uniformly; η = 0.02 is proposed. Each T_lift row is a doubly stochastic mixture of permutations, so the stationary distribution π is uniform over 48 states.
- **Emissions:**
  - Each vertex emits its own anonymous symbol w_v. This is the U-type design of the existing draft: the base path is visible and the fiber is hidden.
  - The anchor a = (2,2) instead emits a fiber cue c_x with probability r. Proposed r = 1, so the anchor always reveals x.
  - Alphabet: 15 base symbols plus 3 cues, 18 symbols in total.
  - Because r = 1, a history determines the base path exactly. The time since the last anchor visit is also known exactly.
  - Uncertainty remains only in the fiber, through the noise η.
  - Why r=1 and not r=0.5 as in x6-plan-1: with r=0.5, a specific Z₂ witness there has stationary probability of about (1/48)·0.5·0.2⁶·0.5 ≈ 3·10⁻⁷. With r=1 every visit to the anchor is a cue, so the training signal is denser (to be verified in G0.6). The cost: the witness histories must avoid the anchor in the middle of the path. This is a constraint on how witness sets are built, not on the process.
- **Training:** unchanged from the pilot. A 4-block, width-128 decoder; context BOS+32; 5000 updates; batch 128 (subject to the Stage 1a rule); natural sequences from `HMMSampler`. Only the vocabulary size changes.

**Closed-form oracle readout [M]:** at a position t where the current vertex is a neighbour of the anchor, the next token is a cue only if the walk enters the anchor. Normalising the probabilities of the three cue tokens gives the predicted fiber distribution:

q*(h) = (1−η)^{n}·δ_{ρ(γ)·x₀} + (1−(1−η)^{n})·u

Here:
- x₀ is the last cue observed;
- γ is the base path since that cue;
- n is the number of transitions from the cue to the next state;
- u is the uniform distribution on X.

ρ(γ) is the product of the edge elements **in path order**. The model's analogue is q_m(h), the model's normalised probabilities of the three cue tokens. This is a behavioural readout with O(1) effect size and no dependence on a probe.

## 3. Facts checked (scratch script, mathematics only)

- **[M] Flatness:** in arm NA the only non-flat face is f★, with holonomy a 3-cycle. In arm AB every face is flat.
- **[M] Orderings:** take loops A± (around row y=1) and B± (around column x=1), all based at p = (1,1). Of the 24 orderings of {A+, A−, B+, B−}, arm NA gives 16 with holonomy e, 4 with c, and 4 with c², where c = ab. Arm AB gives e for all 24. Example: A B A⁻¹ B⁻¹ ↦ c² and B A B⁻¹ A⁻¹ ↦ c. These two are the same commutator traversed in opposite directions.
- **[M] Covering space:** the total space of the local system is a 3-sheeted cover of the punctured torus with χ = −3. Over Q, the cover's Betti numbers are:
  - NA: (1,4,0), a connected genus-2 surface with one boundary component;
  - AB: (2,5,0);
  - trivial connection: (3,6,0).

  These were computed from boundary matrices of the lifted complex, with ∂∂ = 0 verified. The number of components equals the number of orbits of the monodromy on X.
- **[M] Abelian part:** the transpositions a and b act on the fiber simplex (in the 2-dimensional standard representation of S₃) as reflections, with determinant −1. det∘ρ factors through H₁ and is the w₁ class of the associated plane bundle, the "orientation" part. The commutator acts as a rotation by 120°, invisible to det and to H₁. The design therefore separates the **abelian/H₁ part** (Level 1) from the **non-abelian part** (Level 2) inside a single world.

## 4. Hypotheses (one primary)

Level 0 is a learning gate (technical): oracle-relative regret at cue-eligible positions, using a regret/G_C formula as in X5, frozen in Stage 0. A failure here is INCONCLUSIVE.

**H6-1 (Level 1, a gate for the interpretation of Level 2):** on "single loop" sets, where one 4-step loop is chosen from {A±, B±, F±} (F is a flat face next to p) and followed by a common suffix, the model's slope β₁ of q_m on q* (defined below) has a one-sided 95% lower bound ≥ 0.5 in each of the three models. This tests transport at the H₁/abelian level: the "Z₂ parity" of the existing draft.

**H6-NC (primary):** on "ordering" sets (§5), the non-commutativity slope β_NC has a one-sided 95% lower bound ≥ 0.5 in **each** of the three models, together with the spurious-order control in §6.

**A competing hypothesis from the literature (stated in advance):** Zhang & Li (2026) report that standard Transformers trained on running products of group elements learn only **cosets of normal subgroups**. Recurrent networks also pass through cosets of non-normal subgroups. The normal subgroups of S₃ are {e}, A₃ and S₃, so their account predicts one of two outcomes:
- the full state, giving β_NC ≈ 1;
- the parity quotient S₃/A₃ only, giving β_NC = 0 exactly, because every ordering is even.

Note the following:
- What the cue reveals is the point x ∈ X ≅ S₃/S₂, a coset of a **non-normal** subgroup. That point is available only from the full state.
- H6-NC therefore directly tests their account in a different setting: words that are implicit (edges between anonymous symbols), generated by a walk on a topological space, observed partially and noisily, and learned from next-token prediction only.
- In this setting, "NOT SUPPORTED with β_NC ≈ 0 while H6-1 passes partially" is a prediction their account allows. It is an informative result, not a technical failure.

Secondary and exploratory, not part of the primary decision:
- **S1, local-to-global consistency (a non-abelian Stokes check).** Compare the implied holonomy of the long commutator (16 steps, around the whole torus) with that of a short lasso around f★ (4 steps). The two are homotopic and must agree under flatness. Also report the disagreement index of the model.
- **S2, a calibrated learned sheaf.** Fit a fiber-posterior probe on the fit split, then estimate an edge transport map M̂_e per edge. Report:
  - face curvature ‖∏M̂ − I‖, whose prediction is ≈0 on the 15 flat faces and large on f★;
  - det M̂ on the standard plane, predicted −1 on seams;
  - the dimension of the near-null space of the sheaf Laplacian, predicted to be the number of orbits (NA = 1), with the tolerance calibrated on exact oracle maps with the same noise.

  The stalks here are a defined physical quantity (the fiber posterior) on both sides of each edge. This answers the existing draft's objection that disagreement between local fits is not cohomology.

  **Novelty limit:** reading w₁ from the determinant signs of transition maps is an existing method (Paluzo-Hidalgo & Ike 2026, learned atlases). Building an atlas, or det = −1 in itself, is not a contribution here. What is new is only the **calibration against a known local system** (exact oracle maps), and the separation of curvature on f★ from the abelian sign. Each theorem's applicability is checked separately: the result is a cellular sheaf on the base, not a smooth manifold.
- **S3, causal (link to priority 2).** Interchange interventions with `forward_with_patch`: swap residual activations between members of a c/c² pair at the position right after the loops, for each layer, and measure how far q_m moves toward the donor's q*. These are natural activations, without random erasers, which avoids X4-F's damage-matching failure. This is in the spirit of the coset-component swap of Zhang & Li (2026), but on implicit words. Report support distances as in Grant et al. (ICLR 2026).
- **S4, positive control for the priority 1 instruments.** By construction, the ordering effect lies more than 8 tokens before the readout. Run the existing K-suffix profile instruments on this world as a known positive control for "dependence on earlier history". This calibrates the priority 1 tools; it does not answer priority 1 about the pilot world.
- **S5, dynamics.** Using checkpoints, record when Level 1 passes and when Level 2 passes. Li et al. (2025) report a parity-associative mechanism that resolves parity first. Here every ordering has even parity, so a parity-only stage predicts β_NC = 0.
- **S6, geometry of the cover (exploratory).** Representational similarity between activation distances and cover-graph distances versus base-graph distances, on histories with a nearly certain fiber. PH of the activations is allowed only after calibration. The oracle belief cloud is discrete here (the base is observed), so it is **not** a PH positive control.

## 5. Evaluation sets (designed; generated only after the freeze)

**An ordering set s** consists of:
- a natural prefix ending in a cue at a;
- a fixed 2-step path a→p;
- one ordering o of {A+, A−, B+, B−} (16 steps);
- a common 8-step suffix S that avoids a and the seam edges and ends at a neighbour of a.

Total length ≤ 32. The prefix of length 1–6 is sampled **backward** from a with the same kernel, which is exact because the walk is symmetric and the stationary distribution is uniform. Within a set, all 24 orderings share:
- the prefix, the cue, the length, and the cue-to-readout distance;
- the **multiset of tokens**;
- the seam-crossing counts and the H₁ class (zero);
- the **last ≥ 9 tokens**;
- the parity of the permutation.

Their bigram multisets differ only at the joints at p. Stage 0 reports the exact list of differing bigrams.

Family variants (frozen in Stage 0):
- different basepoints p and generator representatives;
- long commutators versus short lassos around f★ (S1);
- control sets with commuting multisets, where the oracle is constant: {A+, A+, A−, A−}, and {A±, F±} with F a flat face.

**Single-loop sets (Level 1):** one 4-step loop from {A±, B±, F±}, followed by a common 12-step contractible padding and the suffix S.

**Natural evaluation (secondary, S-nat):** fresh natural histories. At readout positions where TV(q*, q_comm) ≥ 0.1, report agreement of q_m with q* versus q_comm. Here q_comm is the commutative surrogate (§6, A3). This covers the risk that a designed challenge distribution is mistaken for the natural one. Results on designed sets are never presented as natural generalisation.

## 6. Estimands, alternatives and decision rules

For a set s and an ordering o, centre within the set: q̃ = q − mean_o q. Then

**β_NC = Σ_{s,o} ⟨q̃_m, q̃*⟩ / Σ_{s,o} ‖q̃*‖²**, pooled over sets, per model.

β₁ is defined the same way on the single-loop sets. A perfectly faithful model gives β = 1. Any order-insensitive mechanism gives β = 0 exactly.

**Named alternatives, with β_alt computed exactly in Stage 0 (no training):**

| Mechanism | β_NC (predicted) |
|---|---|
| A1: a suffix of ≤ 8 tokens / last symbol | 0 |
| A2: bag of tokens / unigram counts | 0 |
| A3: abelianised transport (counts of a and b crossings) | 0 |
| A4: permutation parity, i.e. the normal quotient S₃/A₃ (the Zhang & Li outcome when the full state is not learned) | 0 (on Level 1 sets β₁ > 0 is partial; computed exactly in Stage 0) |
| A5/A6: last / first crossing only | computed exactly in Stage 0 |
| A7: composition in **reversed** order | −1 (c ↔ c²) |
| A8: a local flux rule only (lasso around f★, no seam rules) | 0 on long sets |

**Design gate G0.5:** every alternative except the oracle has β_alt ≤ 0.25 on the frozen family. Otherwise the family is redesigned before freezing.

**Spurious order sensitivity:** ρ_spur = (mean within-set variance of q_m on the control sets) / (mean within-set variance of q* on the ordering sets). This is required to be ≤ 0.25 per model, and is reported for all models.

**Decisions** (per model; the primary verdict requires all three):

| Outcome | Condition |
|---|---|
| SUPPORTED | Level 0 and H6-1 pass; lower(β_NC) ≥ 0.5; ρ_spur ≤ 0.25 |
| NOT SUPPORTED (at this level) | Level 0 and H6-1 pass, and upper(β_NC) < 0.5 in at least one model. Report β_NC and its proximity to 0 (commutative) or to −1 (reversed order). |
| INCONCLUSIVE | A Level 0 or Level 1 failure; ρ_spur > 0.25; or an interval that straddles 0.5 |

**Cue-mass gate (adopted from x6-plan-1, for the fragility of a normalised readout):** q_m is defined only through renormalisation over the three cue tokens. If the model gives these tokens little total mass, q_m is noisy. Requirement: for each model, the median of Σ_x p_m(c_x | h) over the evaluation sets is ≥ 0.5 × the oracle's total cue mass at the same positions. Otherwise the outcome is INCONCLUSIVE (a readout failure), not NOT SUPPORTED.

**Secondary endpoint on the full vocabulary (adopted from x6-plan-1):**
- L = mean KL(p_oracle ‖ p_model) over all 18 symbols at the readout positions.
- J = 1 − L_model / L_comm, where L_comm is the loss of the commutative surrogate (A3) against the same oracle.
- Report J and paired intervals for each model and for each family of sets. J does not replace β_NC in the primary decision.

**Multiplicity:** the primary decision is an intersection–union test (each of the three models must pass), so it does not inflate the error of a positive claim. The secondary endpoints (J, S1–S6) are reported with family-adjusted intervals (Bonferroni over the predeclared family) or as descriptive results.

Intervals: 2000 bootstrap draws over **sets** (independent constructions), with `inverted_cdf` percentiles, as in X5/X4. The thresholds 0.5, 0.25 and 0.1 are practical design choices, not noise floors. The number of sets is chosen in Stage 0 so that the projected SE(β_NC) ≤ 0.05 under a conservative residual variance, starting from 512 sets × 24 orderings per model. Inference cost is negligible.

## 7. Stage 0: exact observability audit (oracle only, no training)

| Gate | Content | NO-GO / revision |
|---|---|---|
| G0.1 Complex | Punctured-torus builder: β over F₂ and F₃, χ, ∂∂ = 0; flatness of 15 faces and holonomy of f★; cover Betti numbers as in §3 | Any mismatch: stop |
| G0.2 Oracle | BayesFilter on T_lift/E against an **independent** closed-form reference (§2), and against a 60-digit Decimal check on a sample; gauge invariance: a random gauge transformation, with the cues transformed accordingly, leaves the law of the observations unchanged | Discrepancy > 1e−12: stop |
| G0.3 Observability | TV(q*_c, q*_{c²}) = (1−η)^n ≥ 0.3 at the frozen readout. Nulls give zero: η = 1, the AB arm, and r = 0 (where the cues disappear) | Fail: revise η/L before freezing; otherwise NO-GO |
| G0.4 Local matching | Equality within a set of the token multiset, the last ≥ 9 tokens, length and parity; exact list of differing bigrams | Fail: redesign the family |
| G0.5 Discrimination | β_alt ≤ 0.25 for A1–A8 | Fail: redesign |
| G0.6 Training signal (natural) | Statistics on a natural sample (§7.1): G_K and G_NC | Determined by the categories in §7.2 |
| G0.7 Cost | Technical benchmark of 50 updates; projection of the CPU cost of the cohort | Above the cap: request a decision, do not trim silently |

### 7.1 Natural feasibility screen (adopted from x6-plan-1 and adapted to S₃)

**Sample:**
- 16,384 trajectories of length 33.
- Base seed 420700, stream `x6nc/t0/natural`. This is a separate namespace from x6-plan-1's 4206xx.
- No resampling to enlarge the screen, and no "sampling until success".

**Per history at p32, compute:**
- b32 and q32 (the oracle);
- q_K, the posterior from a K-token suffix only, with a uniform stationary prior, for a fixed K = 8. K = 8 matches the suffix equality in the sets. There is no scan over K;
- q_comm, the commutative surrogate (A3) with full history.

**Statistics:**
- **G_K** = E·KL(q32 ‖ q_K): the gain from history beyond the suffix.
- **G_NC** = E·KL(q32 ‖ q_comm): the natural non-commutative information, the quantity H6-NC requires.
- Also report:
  - the frequency of cue positions;
  - the distribution of the time since the last cue;
  - the mass of histories with row-KL ≥ 0.01 nat under each statistic.

**Bootstrap:** 2,000 resamples of whole trajectories, seed 420704, `inverted_cdf`, both central 95% and one-sided lower 95%.

### 7.2 Feasibility categories

| Status | Rule (practical design choices, frozen before the data) |
|---|---|
| INVALID | An error in structure, oracle, gauge, null or lineage (G0.1–G0.4): no claim at all |
| FEASIBLE_CHALLENGE | G0.1–G0.5 pass and the oracle gap on the designed sets ≥ 0.3 TV (G0.3) |
| FEASIBLE_NATURAL | In addition: lower95%(G_NC) ≥ 0.001 nat **and** at least 512 trajectories with row-KL(q32 ‖ q_comm) ≥ 0.01 |
| CHALLENGE_ONLY | The designed sets are valid but the natural screen failed. If training goes ahead, every claim is restricted to the designed distribution and is not presented as natural generalisation |
| INCONCLUSIVE | Precision, power or resources do not allow a decision; no threshold relaxation or alternative collection |

If FEASIBLE_NATURAL fails at the base point, a predeclared small grid is checked (L ∈ {4,5}, η ∈ {0.01, 0.02}). The selection rule is fixed in advance: the first point in lexicographic order that passes. If no point passes, the status is CHALLENGE_ONLY or INCONCLUSIVE, and the owner decides whether there is any training at all.

Stage 0 produces an audit report, a gate.json with a reason, a frozen configuration, and one sentence: is "natural" justified, "challenge only", or stop. It does not authorise training.

## 8. Stage 1 (only after owner approval of the Stage 0 report)

- **1a, learnability pilot (optional):** one seed, excluded from confirmation. It is evaluated on Level 0/1 and on dev sets only, **blind to Level 2**. Predeclared rule: if Level 1 fails on dev at 5000 updates, the cohort uses 10000; if it fails at 10000 as well, NO-GO (technical).
- **1b, confirmation cohort:** three new master seeds and 131072 natural training histories per model. Data and test sets are generated from separate seed streams after the freeze. Test sets are touched once. No reseeding, no retuning, no replacement of a failed run. Censored results and failures are reported.

**Seeds, splits and sizes (proposed; frozen at the end of Stage 0):**

| Item | Value |
|---|---|
| Masters 1b | 420701 / 420702 / 420703; the symbol permutation and init are seeded from the master |
| Pilot 1a | 420709 (excluded from confirmation) |
| Training | 131072 natural histories per model; architecture and optimiser of the pilot (4 blocks, width 128, 4 heads, MLP 512, GELU, pre-LN, n_ctx 33, AdamW, 5000 updates, pilot checkpoint schedule); V_out = 18, V_in = 19, untied readout |
| Natural dev | 4096 per model (dev and probe fitting only); fit 3072 / val 1024 for S2 |
| Natural test | 4096, a new lineage shared across models through a canonical vocabulary |
| Designed sets | dev: 128 sets per family (1a only); test: 512 ordering sets × 24, plus 512 control sets, plus 512 Level-1 sets, stream `x6nc/test/designed` |
| Bootstrap | 2000 draws, seed 420710; a set is the cluster for all its orderings |
| Primary checkpoint | 5000 (or 10000 under the 1a rule); no choice of the best checkpoint on test |
- Arm AB (three more models) is a separate, later decision. It would test whether non-commutative composition is learned only when it is needed. It is not needed for H6-NC, because the control sets supply an order null within each model.

## 9. Budget and stopping (proposed, not granted)

| Stage | CPU cap |
|---|---|
| Stage 0 | ≤ 1800 CPU-s, including startup, tests, supervision and export (as in x6-plan-1); one native thread, 8 GiB peak, 128 MiB of outputs. This is an unmeasured planning estimate |
| 1a | ≤ 3600 CPU-s |
| 1b | ≤ 10800 CPU-s (estimated by analogy with X5, about 2700 CPU-s per model including evaluation, to be confirmed by G0.7) |

Further limits: 8 GB RAM, 2 GB of outputs, CPU only, no installations. The existing meter is reused (`tools/x4_oracle_profile/meter.py`, fail-closed). The unallocated X5 balance is not assumed to be available. STOP, usage and integrity controls take precedence. A practical NO-GO is a scoped negative, not a proof of impossibility.

## 10. Reuse assessment (six fields)

1. **Existing:**
   - `BayesFilter(T,E,pi)` and `FutureOperator` (generic);
   - `HMMSampler(T,E,pi,layout)`;
   - `CubicalComplex` (boundaries, F_p ranks, χ);
   - `QuotientLatticeBuilder` (periodic gluing);
   - the trainer and the model with a configurable vocabulary;
   - the activation extractor;
   - `learner/patch.forward_with_patch`;
   - store, MetricRecords and lineage;
   - the bootstrap conventions of X4/X5;
   - the meter.
2. **Missing:**
   - a torus builder (periodic on both axes) with a removed face;
   - lifting the base walk to (v,x) with typed metadata for base and fiber (24 vs 48 must not be conflated, as in the draft);
   - a cue-emission constructor;
   - generation of designed sets;
   - a closed-form reference oracle;
   - the β estimators.
3. **Smallest change:** a registered builder `torus_punctured` (extension through `WorldBuilder`); a pure function `lift_local_system(T_base, edge_group_elements, η)`; an analysis module `x6_holonomy` with no change to frozen code.
4. **Stable invariants:**
   - existing worlds/processes are byte-identical;
   - privileged definitions (fiber, holonomy) stay outside learner and activations and are joined only in analysis;
   - the alphabet, seeds and splits are frozen in the store.
5. **Regression checks:** existing tests for world/process/oracle/dataset/learner; new independent tests written by a separate author (complex, flatness, cover, closed-form oracle, gauge, β on synthetic predictors with known β).
6. **Next plausible extension:**
   - in-context topology inference (§12) reuses the same lift with a mixture over connections;
   - a noisy base (O-type) reuses EmissionModel;
   - a general sheaf engine and a generic G-bundle framework are not built.

## 11. Comparison with existing research (focused check, 14 October 2026)

| Work | Their finding | What differs here |
|---|---|---|
| Shai et al., NeurIPS 2024; Piotrowski et al., ICML 2025 | Belief geometry in the residual stream; constrained updates | Here the hidden quantity is a global transport whose composition order matters; the test is behavioural with an exact oracle, not only geometric |
| Liu et al., *Transformers Learn Shortcuts to Automata*, ICLR 2023 ([arXiv](https://arxiv.org/abs/2210.10749)) | Shallow shortcuts for automata; O(1) depth for solvable groups; brittle out of distribution | S₃ is solvable, so it is expressible. Here the group word is **generated by a walk on a topological space with partial and noisy observations**, and the test asks whether the model uses π₁ structure rather than commutative shortcuts |
| Merrill, Petty & Sabharwal, *The Illusion of State*, ICML 2024 ([arXiv](https://arxiv.org/abs/2404.08819)) | Limits of TC⁰ for state tracking (S₅ is NC¹-complete) | Possible extension: A₅ holonomy as the expressivity boundary inside a topological world; not in this protocol |
| Li, Guo & Andreas, *(How) Do Language Models Track State?*, ICML 2025 ([arXiv](https://arxiv.org/abs/2503.02854)) | Associative and parity-associative mechanisms for permutation composition | In their setting the permutations are given explicitly as tokens. Here they are **implicit** (edges between anonymous symbols), learned only from next-token prediction, and constrained by flatness (locally consistent). The orderings are even, so parity alone predicts β = 0 |
| Chughtai, Chan & Nanda, ICML 2023 ([PMLR](https://proceedings.mlr.press/v202/chughtai23a.html)) | Group composition through matrix representations | Concrete mechanistic prediction for S2: reflections with det −1 on the standard plane at the seams, rotation by 120° around f★ |
| Park et al., ICLR 2025 ([arXiv](https://arxiv.org/abs/2501.00070)); George et al. 2021 (CSCG, [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8062558/)); Raju et al. ([arXiv](https://arxiv.org/abs/2212.01508)) | Recovery of a graph or topology from walks and aliased observations | Here the base graph is visible on purpose; the question is the **connection** over it (a local system), which is invisible to base statistics |
| Grant & Wang, ICLR 2026 workshop ([page](https://iclr.cc/virtual/2026/10022164)) | A cellular sheaf over paraphrase graphs decomposes LLM activations into H⁰/H¹ | There, the sheaf is defined by the analyst on activations. Here, the sheaf of the world is known exactly, and the instrument (S2) is calibrated against it |
| Hansen & Ghrist 2019; Bodnar et al. 2022 | Sheaf Laplacians and sheaf diffusion as architecture | Used only as a measurement instrument; this is not a sheaf network |
| Sung, preprint 2026 ([arXiv](https://arxiv.org/abs/2601.05240)) | An architecture that imposes a path-ordered product ("Holonomic Network"); claims not independently verified | The question here is whether a **standard** Transformer learns this, not what can be built in |
| Zhang & Li, *Tracking States or Tracking Cosets?*, preprint, September 2026 ([arXiv](https://arxiv.org/abs/2609.29951)); found through x6-plan-1, abstract checked | Partial accuracy follows the quotient; standard Transformers learn only cosets of normal subgroups, while RNNs also learn non-normal ones; component swaps transfer coset state | **The most direct competing hypothesis** (§4, A4): for S₃ it predicts full state or parity. The readout here is S₃/S₂, a non-normal coset, with implicit words generated topologically. The claims are checked against the abstract only, not against the whole paper or its experiments |
| Paluzo-Hidalgo & Ike, *Learning Tangent Bundles and Characteristic Classes with Autoencoder Atlases*, preprint v2, May 2026 ([arXiv](https://arxiv.org/abs/2602.22873)); found through x6-plan-1 | w₁ from the determinant signs of transitions in a learned atlas | Determinant signs are not a contribution here (§4, S2); only the calibration against a known local system is. The theorem's assumptions (smooth manifold, matching dimension) are not assumed for history clouds |
| Penrose 1992 (cohomology of impossible figures); Abramsky & Brandenburger 2011 (sheaf structure of contextuality); Wilson 1974; Aharonov–Bohm 1959 | Local consistency with global obstruction; Wilson loops; flux | The source of the framing: a flux face is a hole defined by transport |

**Working novelty (not a priority claim):** the focused search found no study in which a next-token model trained on a stochastic world is tested for the use of **non-abelian holonomy** with a set design in which every H₁ or commutative explanation predicts exactly zero, and with an exact Bayes oracle. The search should be refreshed before any publication.

Specific contributions, if the study succeeds:
1. An operational, falsifiable test of π₁ beyond H₁.
2. A hole defined by flux (torus versus punctured torus, same H₁).
3. Separation of the abelian part (w₁ of the plane bundle) from the non-abelian part within one world.
4. A sheaf instrument with physically defined stalks, calibrated against ground truth (not a new method for w₁).
5. A positive control by construction for the history-attribution instruments of priority 1.
6. Natural causal interventions without matched erasers (priority 2).
7. A test, in a new setting, of the 2026 normal-coset claim (Zhang & Li). Either outcome is informative.

## 12. Claim boundaries, risks and later steps

- **Not claimed:**
  - that the model "knows" that the surface is a punctured torus;
  - that its activations form a genus-2 surface (S6 is exploratory);
  - that a finite automaton is not a sufficient explanation (it is; non-commutative composition **is** such an automaton, and the claim concerns which composition is learned, not a geometric embedding);
  - anything about natural-language LLMs;
  - anything about a population of seeds.
- **Risks:**
  - a small transport signal in natural data (G0.6);
  - the designed sets lie outside the training distribution in structure, even though their likelihood is the same (S-nat and support measurements are reported);
  - the visible base turns the study into "state tracking" rather than topology learning. This is intentional and must be stated: the topology lies in the connection, not in the base.
- **Later steps, conditional on the outcome:**
  - **SUPPORTED:** X6-II, **in-context topology inference**. Each sequence draws a connection (flux versus no flux) at random, and the oracle posterior P(flux | h) increases when a cue observed after a commutator contradicts the abelian expectation. This is a direct operationalisation of "detecting an inconsistency between local and global", noise η versus genuine obstruction. A noisy base is a further option.
  - **NOT SUPPORTED** with β₁ passing: a scoped result. In this setting the learner is H₁-faithful and π₁-blind, consistent with the normal-coset account (§4) if β_NC ≈ 0. The next step is S5 (checkpoints, longer training) or an expressivity question (layers), not an immediate rescue.
  - **CHALLENGE_ONLY in Stage 0:** training is possible only under a claim restricted to the designed distribution, by explicit owner decision. Otherwise, close with a feasibility report.
  - **NO-GO at Stage 0:** document it and stop. No training "anyway".

## 13. Decisions for the owner

1. Approve Stage 0 only (≤ 1800 CPU-s, no training), or postpone it. Recommendation: do not preempt the K4 decision (priority 1, awaiting approval). Stage 0 is cheap and independent of K4's artefacts, and can run before or after it, one task at a time.
2. Should arm AB be part of the plan from the start, or wait until after H6-NC? Recommendation: wait. The trivial arm of x6-plan-1 is not needed either.
3. Approve the practical thresholds, or revise them before the freeze:
   - β: 0.5;
   - ρ_spur: 0.25;
   - TV: 0.1 and 0.3;
   - cue mass: 0.5;
   - G_NC: 0.001 nat, with 512 qualifying trajectories.
4. What happens to x6-plan-1: it is incorporated here (Z₂ as Level 1, together with its gates and procedures). There is no separate Z₂ T1 campaign.

## Appendix A — H6-B (boundary), corrections before any freeze (adopted from x6-plan-1)

An optional, low-cost route using the existing models; it does not run in parallel with X6-NC and does not replace it after the fact. Hypothesis, as in [X6_TOPOLOGICAL_INVARIANTS](X6_TOPOLOGICAL_INVARIANTS.md#minimal-x6-experiment-boundary-organization-without-training): conditional organisation into two components on the two boundary circles, better than R0/R1. This is not a test of orientability.

**Selection and pool:**
- Selection uses B(h) = Σ_{y∈{0,11}} b32 ≥ 0.8, from the oracle only, labelled `privileged_eval:boundary`.
- Fix a pool cap of 32768 per process and split. There is no sampling until success. Keep the counts of rejected histories.
- Effective coverage for each boundary component is N_eff = (Σw)²/Σw², with w the posterior mass on that component. Require N_eff ≥ 32 in each panel, in addition to total mass. If there are not enough histories: INCONCLUSIVE, and 0.8 is not relaxed.
- Distinguish source panels from conditional panels built after selection. Panels of 128 are not equivalent to the primary M512 design.

**Spaces and baselines:**
- A = ln_gauge_free(resid_post_3, eps=1e−5) with Euclidean distance; b32 and b1 with Hellinger distance.
- Baselines: R1 (the same token + position embedding), one-hot of the last symbol, exact b1.
- Calibrate every space that receives a score, including R0 and R1. A baseline whose estimator fails (duplicate embeddings, coverage) does not count as pass-count 0 and is not proof of an advantage.

**Scale and endpoint:**
- Choose the scale band on calibration only, with a deterministic rule defined in advance, requiring ≥ 19/20 correct synthetic draws. If there is no valid normalised rule for comparing oracle, model and baselines: INCONCLUSIVE.
- Primary endpoint: H0 only. Two components across the whole band; each component ≥ 20% of the rows; ≥ 7/8 panels in every seed; the oracle ≥ 7/8; the model's pass count strictly above R0 and R1 in every seed.
- H1 per component is secondary and is not added afterwards to change the verdict.

**Controls and scope:**
- Square-O, P and density-matched thinning are comparison controls, not a rescue.
- The E4 data are already exposed, so they are exploratory only.
- Even success does not show that the cloud is a manifold with boundary.
