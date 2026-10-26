STATUS: MERGED v2, design freeze candidate (pending confirmation)

# HWS-MERGED-v2: an oracle-only world sweep for the history-source question (stage A, no training)

**Round:** `coord-history-world-sweep-20261026`. **Writer:** clean-context Claude, for coordinator 243a611b, 2026-10-26.
**Revision:** v2 applies review items RC-1..RC-9 (`coord-hws-review-20261026.codex.md`, all accepted in `….rulings.md`) and the coordinator rulings on OPEN-1..4; the per-item list is the final section "Change log v1 → v2" (§19).
**Base code:** topo-pilot main @ `0a67c5a77d57a6ea325b25360d1b8b09e2e55904` (code index checked current with `build_code_index.py --check`).
**Inputs (sha256, first 16 hex):** request `7a1cca2bcb7d76a3`; track L `….claude.md` `08769617ce4a3ff3` (base text); track X `….codex.md` `ca8f821342a4e8c1`; comparison `….COMPARISON.md` `b5d5ea739b216a90`; merge decisions `….MERGE.md` `9fd25b801782d7e4`. The MERGE decisions and rulings R-HWS-1..7 override everything else.
**This document is planning only.** The writer ran no Python, tests, sampling or oracle computation. No store payload (`payload.npz`, `state.pt`, `sealed/`) was opened or hashed; only JSON files, configs and code were read. The public research-summary paths were not opened or searched. No git writes.

**Labels.** **[V]** = checked by the writer against the code at 0a67c5a or the cited record (file:line given). **[H]** = an inherited record value. **[W]** = the writer's desk arithmetic. No [W] or [H] value is a gate. Every gated quantity is computed by the run.

---

## Summary (≤ 300 words)

**Question.** Find a cylinder world where (i) the beyond-four history information that the K4b measure can see is at least 3× its margin, and (ii) context helps next-symbol prediction enough that a model could plausibly learn it.

**Target.** The phase-only oracle comparator D4 = E[v32·(m32 − m4)], v32 = m32/‖m32‖: K4b's own `delta4_orc` (0.00854 in the current world). Gate: a one-sided lower bound D4 ≥ 0.03 = 3 × the K4b margin 0.01. Information measures in nats and bits are report-only.

**Grid.** Stay probability p ∈ {0.2, 0.5, 0.75, 0.875, 0.9375}; emission width σ ∈ {1.25, 1.5, 2, 2.5, 3}; anchored circular aliasing q ∈ {1, 2, 3}; circumference W ∈ {8, 12, 16}; height 12; length 32. 225 grid worlds; exact symmetry and registry filters leave at most 150 to sample.

**Frozen rule.** Eligibility filters, then four criteria: D4 ≥ 0.03; context gain ≥ 0.10 nat; beyond-four gain ≥ max(its current-world value, 0.0078 nat); circular-symbol beyond-four gain ≥ its current-world value. Worlds confidently qualified on screening come first, then the smallest departure from the current world.

**Stages.** S0 known cases (gating, freezes two floors); S1 coarse screen at 4,096 rows; one conditional range extension; one conditional refinement; S3 confirmation of ≤ 16 finalists on 32,768 fresh rows at α = 0.05/16.

**Outcomes.** SELECTED (tier 0/1/2), BELOW_3X, NO_WORLD_CONFIRMED, NO_SUITABLE_WORLD (only if every stage completed), INCONCLUSIVE/RESOURCE_OR_AUTHORITY, FAIL_TECHNICAL.

**Cost.** About 1.5 CPU-h central (1.8 h with the extension), plus 0.15 h implementation; pause when one stage passes 3× its forecast or the cumulative total passes 3× the cumulative forecast.

**Licence.** Oracle properties of one world only; nothing about learning, capture or stage C.

---

## 0. Scope, conventions and notation

### 0.1 Authority and scope
- Owner addendum 25 adopted the working rules (oracle feasibility first, at least 2× the margin; learning pilot; margins from pilot variance; synthetic dry run before freeze; every control checked on a known case; a registered "positive but below margin" licence). This plan is §3.1 stage A of `docs/proposals/NEXT_ROUND_SHARPER_ANSWERS_HE.md`.
- Addendum 26: adaptive budget, extension rules frozen in advance, 3× pause.
- Addendum 27: planning go-ahead only. **No run, sampling or CPU spend is authorised by this document.** Execution needs the final execution freeze and a separate owner AUTH (§15 Q6).
- **Authorisation sequence (RC-4).** Design review acceptance is distinct from the final execution freeze. A separate owner AUTH may authorize J1 implementation, tests and synthetic-only dry runs before that freeze; it authorizes no S0 or sweep sampling. Final HWS execution freeze requires coordinator acceptance of DR1–DR13 and a committed report bound to the implementation hash. S0–S3 require a subsequent owner AUTH. In order: (1) design review acceptance ("design freeze candidate", this document after confirmation); (2) owner AUTH for J1; (3) J1 implementation, tests and the synthetic-only dry run (§13); (4) coordinator acceptance of DR1–DR13 and the final execution freeze bound to the implementation hash; (5) owner AUTH for S0–S3. The review that produced v2 does not authorize J1.
- Stage A trains nothing, runs no model and draws no conclusion about any model. Earlier verdicts (X4 history origin COMPLETE_ORACLE_HEADROOM_FAIL_NO_CONFIRMATION, K4, K4b EXCLUSION, C1′, D-2a, E4) are not reopened or pooled.

### 0.2 Notation

| Symbol | Meaning |
|---|---|
| w = (W, q, σ, p) | World key: circumference W (axis 0 periodic), alias level q, emission width σ, lazy-walk stay probability p. Height H = 12, length L = 32, flat metric, overlap emission throughout |
| N = 12W | Latent states; state id = x·12 + y (`WorldSpec` docstring, `contracts/_schemas_world.py:28`) [V] |
| V = 3W | Emission centres (W/2 circular × 6 axial), centre index j = 6i + b |
| n_A(W, q) | Circular labels after aliasing (§4.3); V′ = 6·n_A public symbols; canonical symbol v = 6g + b (g circular label, b axial index) |
| c(z) | (cos 2πx/W, sin 2πx/W), x = coords[z, 0]: the first harmonic of the circle |
| b_K, m_K, q_K | Posterior of z32 given the last K symbols (stationary restart, §2.1); m_K = b_K·c; next-symbol law q_K = b_K T E. K = 32 is the full history |
| q_K^A | Circular-label marginal of q_K: q_K^A(g) = Σ_b q_K(6g + b) |
| b_K^x | x-marginal of b_K: b_K^x(x) = Σ_y b_K(x·12 + y) |
| r_K | m32 − m_K |
| v32 | m32/‖m32‖, with phase 0 at an exact zero (K4b `vector_phase`, `k4b_scores.py:35-38`) [V] |
| SE | sample standard deviation / √n |
| w0 | (12, 1, 1.25, 0.2): the current ("E4") cylinder-O world of the K4b models |
| M | stage-C margin = `k4b_config.MARGIN` = 1/100 (`k4b_config.py:58`) [V] |

---

## 1. The question

In the current world w0 the last four symbols nearly fix the position on the circle:
- B4 = E‖r4‖ ≈ 0.068 and B8 ≈ 0.0093 (job 0014) [H];
- the phase-only oracle comparator is 0.00854 [0.00791, 0.00933] (job 0057, `report.md:81`) [H], below the registered margin 0.01, while the three models reached 0.83–0.95 of it (`report.md:44`) [H].

So K4b could not tell "the learned circle carries history" from "history adds too little to see". The same lesson stopped the X4 history-origin study before any model was examined: its oracle headroom failed.

Stage A asks, with the exact oracle only: **is there a cylinder world, reachable from w0 by changing world parameters, in which the beyond-four information the K4b measure sees is ≥ 3× its margin, and in which context helps prediction enough to be plausibly learnable?** The selection rule is frozen here, before any sweep data.

The competing explanations a sweep can separate (from track X): too little endpoint headroom; too little predictive incentive; difficult inference (diffuse or lopsided belief phase); or a promising design where all pass. These are world-design conclusions, not conclusions about any model.

---

## 2. Quantities and definitions

### 2.1 Population and suffix posteriors

All quantities are population expectations under the stationary law of world w: z1 ~ π, emit w_t ~ E(z_t, ·), then transition z_{t+1} ~ T(z_t, ·); π is uniform because T is symmetric (`transition.py:54-55, 84`) [V]. History H = w1..w32, suffix S_K = w_{33−K}..w32.

- b_K(z) = P(z32 = z | S_K), computed by `oracle_profile.suffix_posterior(T, E, π, tokens, K)` (`oracle_profile.py:128-152`) [V]: the filter restarts from π at the window start, emits first, transitions only between emissions, takes no trailing transition, and normalises after every emission.
- Every suffix filter restarts from π. It never inherits the full-history belief at the suffix boundary.
- K grid: S1, X1, S2 and S0 use K ∈ {1, 2, 4, 8, 16, 32}; S3 adds {6, 12, 24}.
- Each row's value is computed exactly up to float64 rounding (§8). The population mean is estimated by Monte Carlo over n independent stationary histories. No filtering of histories by support, residual size, phase or confidence.

### 2.2 Primary quantity, in the units of the stage-C measure

| Id | Definition | Per-row value | Role |
|---|---|---|---|
| **D4** | E[v32·r4] | `k4b_scores.phase_scores(k4b_scores.oracle_phase(m32), m32, m4)` (`k4b_scores.py:45-46, 54-55`) [V] | **criterion C1** |
| D_K | E[v32·r_K] | same, with m_K | profile, descriptive |
| B_K | E‖r_K‖ | `scores.r4_norms(m32, m_K)` (`scores.py:90-92`) [V] | profile; B4 is K4b's B4-VAL quantity |
| V_K | E‖r_K‖² | | profile |

**Why D4 and not B4.** K4b's estimand is Δ4 = E[ũ·r4] for a learned unit coordinate ũ, with margin M = 0.01.
- B4 bounds |Δ4| for every coordinate (Cauchy–Schwarz). It is attained only by ũ = r4/‖r4‖, which is not a coordinate on the circle.
- D4 is the value of the ideal circle coordinate, the phase of the full-history belief. It is exactly K4b's `delta4_orc` control: the same functions on the same arrays (`k4b_scores.py:148`) [V]; K4B-FROZEN-v1 §9 item 6.
- The K4b models reached 0.83–0.95 of D4 but only 0.10–0.12 of B4 (job 0057 `report.md:44`) [H].
- So D4 is the best-case effect a belief-tracking circle can show in the stage-C measure, which is what addendum 25 rule 1 asks for. D4 is not an upper bound for other coordinates.

**Identities (from K4b; reused, not re-proved).**
- (I1) Stationarity and the tower property give m_K = E[m32 | S_K]. Hence E[g(S_K)·r_K] = 0 for every bounded suffix function g (K4B-FROZEN-v1 §1.2 Proposition 1).
- (I2) 0 ≤ D4 ≤ B4 in the population (K4B-FROZEN-v1 §9 item 6).
- (I3) V_K = E‖m32‖² − E‖m_K‖², non-increasing in K (job 0014).
- (I4) Row-wise v32·r4 ≤ ‖r4‖, so the sample D4 never exceeds the sample B4.

### 2.3 Cross-checks in nats (bits = nats / ln 2)

**Row form (R-HWS-5).** Every gain and information quantity is estimated from **per-row KL values**, which are non-negative row by row and whose mean equals the conditional mutual information. The entropy-difference form is computed on the same rows and reported as a cross-check only.

| Id | Definition (KL rows) | Identity | Role |
|---|---|---|---|
| I_Z(K) | E KL(b32 ‖ b_K) | = I(z32 ; w_{1..32−K} \| S_K), since b_K = E[b32 \| S_K] | report |
| I^x_4 | E KL(b32^x ‖ b4^x) | = I(x32 ; w_{1..28} \| S4) | report |
| **G_K** | E KL(q32 ‖ q_K) | = I(w33 ; w_{1..32−K} \| S_K) = E H(q_K) − E H(q32) | profile; G4 is criterion C3 |
| **G_C** ≡ G_1 | the repository's context gain, `oracle._futures.context_gain` semantics (`_futures.py:80-107`) [V] | = H(w33 \| w32) − H(w33 \| w_{1..32}) | criterion C2 |
| **G4^A** | E KL(q32^A ‖ q4^A) | = I(g33 ; w_{1..28} \| S4), g33 the circular label of w33 | criterion C4 |
| G_0 | E KL(q32 ‖ π T E) | context gain against the stationary marginal | report |
| H* | E H(q32) | oracle next-symbol cross-entropy (stage B's learning floor) | report |

Also reported: the perplexity ratio e^{G4}; the entropy-difference estimates of I_Z(4), I^x_4, G4 and G4^A with the difference from the KL estimate and its SE.

**Pinsker consistency (report only, never a gate).** Because ‖c(z)‖ = 1 and m depends on b only through b^x, row-wise ‖r4‖ ≤ ‖b32^x − b4^x‖₁ ≤ √(2 KL(b32^x ‖ b4^x)). So ‖r4‖² ≤ 2·KL(b32^x‖b4^x) holds on every row, and V4 ≤ 2·I^x_4 in the population and in every sample. The run reports the number of rows violating it by more than 1e-12; a nonzero count is an integrity flag for coordinator review (§5.1 E6), not a gate. The chain D4 ≤ B4 ≤ √V4 ≤ √(2 I^x_4) ≤ √(2 I_Z(4)) is a population note.

I_Z(4) covers every harmonic and y, so I_Z(4) > 0 can hold with D4 small, but not the reverse.

### 2.4 Context benefit and learnability proxies

1. **G_C, context benefit (C2).** Floor **0.10 nats**, the project's registered σ-calibration floor (`PREREGISTRATION.md:205`, `min_context_gain_nats: 0.10`) [V].
2. **G4, beyond-four predictive incentive (C3).** *Proposition F:* for every predictor f that depends only on the last four symbols, E KL(q32 ‖ f(S4)) = G4 + E KL(q4 ‖ f) ≥ G4, because q4 = E[q32 | S4] (tower property). So **a model whose regret E KL(q32 ‖ p_model) is below G4 cannot be predicting from the last four symbols alone.** E2 recorded cylinder-O regrets of 0.0036–0.0039 nats at p = 32 on test panels (`reports/E2/summary.md:7-14`) [V].
   - Floor g4* = max(Ĝ4(w0), 2 × 0.0039) = max(Ĝ4(w0), **0.0078**) nats, with Ĝ4(w0) frozen at S0.
   - Reading: at least as much beyond-four incentive as the world where models captured most of D4, and a model with up to twice E4's regret could not be suffix-only. A proxy, not a guarantee of learning.
3. **G4^A, circular-symbol beyond-four gain (C4; track X).** Floor **g4A* = Ĝ4^A(w0)**, the S0 value, frozen in the S0 stage record before any non-baseline world is evaluated (R-HWS-3). It closes a loophole: a world could otherwise pass C3 mainly because older context helps predict the axial coordinate.
4. **Report-only proxies.**
   - Horizon profile: B_K, D_K, V_K, G_K over K.
   - Track X's proxies: R2 = E‖m32‖²; p_weak = P(‖m32‖ < 0.1); p_gain = P(KL(q32^A ‖ q4^A) ≥ 0.005). None is a gate.
   - Effective aliasing A_eff = exp(Σ_w p(w) H(r_w)), r_w the one-symbol state posterior: the mean number of states a single symbol leaves open (exact, by enumerating symbols).
   - **Path-dependence index** P4 = E‖m32(h) − m32(h̃)‖² / V4, where h̃ applies a uniformly random permutation to w1..w28 and keeps w29..w32 (S3 only; stream §6.6). P4 ≈ 0 means the beyond-four information is order-free averaging; a large P4 means the order of the path matters. Permuted histories always have positive probability because the emissions have full support.

### 2.5 Circle legibility (eligibility E5)

On the S3 rows for decisions (on S1/X1/S2 rows as point estimates for screening):
- the fraction of rows with ‖m32‖ ≥ 0.2 is ≥ 0.95;
- each of 12 equal bins of arg m32 holds ≥ n/64 rows;
- |mean v32| ≤ 0.30.

These mirror the K4b chart rules: support resultant ≥ 0.2 (`PROTOCOL_K4B_v1.md:86`) and C0-val's "every one of 12 bins ≥ 8 of 512" and "overall resultant ≤ 0.30" (`PROTOCOL_K4B_v1.md:313`) [V]. Here they apply to the oracle belief, not to a chart; they are an analogy and a design filter on point estimates. They exclude worlds where the belief phase is too diffuse or too lopsided for "the circle is the latent coordinate" to stay meaningful. The 12 phase bins are kept at every W, including W ≠ 12 (coordinator ruling OPEN-3, closed); the bin profile is reported.

### 2.6 The sealed-D-2a registry probability (exact; MD-12)

K4b's registry treats every history whose 32 canonical symbols all lie in {0, …, 4} as a potential overlap with the sealed D-2a pools (`k4b_data.py:178-180`) [V]. One such row anywhere in the cal, val or test tables makes the whole K4b study INCONCLUSIVE/REGISTRY_INCOMPLETE (`predicate_check`, `k4b_data.py:186-190`; applied at `k4b_driver.py:235` and `k4b_fresh.py:107`) [V]. Per world, under the frozen canonical label order of §4.3:

  p_D2a(w) = π · D_S · (T · D_S)^31 · 1,  D_S = diag(Σ_{v ≤ 4} E[:, v]),

a masked forward recursion: exact up to float64 and cheap. It replaces track L's i.i.d. (5/V′)^32 argument, which understates the rate for correlated histories (R-HWS-6). Its eligibility threshold is fixed in §5.1 E4.

### 2.7 Reduction to the K4b values at w0

At w0 these definitions are the K4b and job-0014 definitions, computed by the same functions: D4 = `delta4_orc`, B4 = B4-VAL, B_K the job-0014 profile, G_C the E2 context gain. S0 (§3) checks this numerically against the records (addendum 25 rule 5).

---

## 3. Known-case checks (stage S0, gating; addendum 25 rule 5)

S0 runs before any other world, as its own job, using the sweep's own code. It draws n0 = 32,768 fresh rows of w0 (stream §6.6) and runs the exact computations. The coordinator ACCEPTs the S0 record before S1 is dispatched, because g4* and g4A* are frozen there.

**Tolerance for a sampled quantity x against a reference r recorded on n_r rows:** |x̂ − r| ≤ 4·s·√(1/n0 + 1/n_r), s the sweep's own per-row sample SD. Any failure gives **FAIL_TECHNICAL/KNOWN_CASE** and stops the study. No tolerance or reference is changed after data; a change needs an owner decision.

| # | Check | Reference | Tolerance |
|---|---|---|---|
| **KC1** | **Process identity without payload access (R-HWS-2).** Rebuild w0 with the `src` builders: `build_world(WorldConfig("cylinder", (12, 12), "flat"))`, `TransitionBuilder().build(world, TransitionConfig(p_stay=0.2))`, and `OverlapGaussian().build(world, EmissionConfig("overlap", 36, 1.25, "grid"), SeedTree(s))` for s ∈ {1729, 2718, 3141}. For each rebuilt spec: (a) **config identity**: from the artifact's `meta.json` (JSON) take `config`, `parent_ids`, `schema_version`; require that `meta.config` equals the expected config of (d) (the rebuild config field by field plus the envelope additions), that `make_artifact_id(type, meta.config, meta.parent_ids, meta.schema_version)` (`contracts/ids.py:73-84`) equals the recorded id, and that `meta.seed_map` equals the expected seed map of (d); (b) **content identity**: `payload_checksum(rebuilt_arrays, stored_extra)` (`contracts/base.py:170-184`), with `rebuilt_arrays` from `spec.to_payload()` and `stored_extra` read from the artifact's `extra.json` (JSON), must equal both `meta.payload_sha256` and the manifest entry `artifacts["<kind>/<id>"]["sha256"]` in `x4-history-feas-store/INPUT_IDENTITIES.json`. The manifest's own file hash is checked against `tools/x4_oracle_profile/config.json` `inputs_sha256["INPUT_IDENTITIES.json"]` = b0edd2e3…5d3d. (c) The rebuilt extra is compared with the stored extra field by field and differences are reported (report only; (b) decides). (d) **Serialization envelope (RC-2; `ProcessStage.run_emission`, `process/stage.py:55`, adds `replicate`, `world_scope_master` and `world_scope/centers/cylinder`).** Reconstruct the serialization envelope without calling any stage or store loader. For emission seed s, expected config is `asdict(emission_cfg)` plus `replicate=s` and `world_scope_master=0`. Expected seed_map combines the rebuild tree’s issued entries with `world_scope/`-prefixed entries from a fresh `SeedTree(0)` after issuing `seed("centers", "cylinder")`. World and transition seed maps are empty; their expected parent lists are respectively `[]` and `[world_id]`, with the same parent for each emission. Require complete status, expected artifact type/id, and the metadata-file SHA256 recorded in the pinned manifest before comparing config, seed map and rebuilt content checksum. **No `payload.npz` is opened or hashed. `inputs.load_artifact`, `inputs.load_process`, `k4b_data.load_process` and `inputs.verify_input_hashes` are never called** (the first three open `payload.npz`, `inputs.py:70-78`; the last hashes the history files `calibration.npz` and `validation.npz`, `inputs.py:42-48`) [V] | WorldSpec 21feee1d8ee5422e, TransitionSpec e4dafc7b9785c172, EmissionSpec 3633ac27dab50cf4 / 97838b9e13a26f74 / 8c29c329c197c79e (`x4_oracle_profile/config.json`) [V] | exact equality of ids, configs and checksums |
| KC2 | Exact symbol law: min_w p(w), p = π E | 0.0268 (`PREREGISTRATION.md:49`) [V] | \|x − 0.0268\| ≤ 5e-5 |
| KC3 | Mean last-symbol entropy Σ_w p(w) H(r_w), exact | 3.140 nats (same table) | ≤ max(5e-4, 4·s/√4096) |
| KC4 | B1, B2, B4, B8, B16 | job 0014 pooled (3·cal + val)/4, n_r = 4096: 0.37097, 0.19761, 0.06769, 0.009258, 1.7875e-4 [W from H, `jobs/0014/report.md:149-153`] | rule above |
| KC5 | B4 | K4b fresh 0.0688849, n_r = 3072 (`jobs/0057/report.md:41`) [H] | rule above |
| KC6 | **D4** | K4b `delta4_orc` 0.00854213, n_r = 3072 (`jobs/0057/report.md:81`) [H] | rule above |
| KC7 | G_C | E2 0.2649 (`reports/E2/summary.md:7-14`); n_r = 4096 (8 panels × 512, `PREREGISTRATION.md:219-221`). The executor confirms n_r from E2 metadata JSON without opening arrays; if it cannot, n_r = 4096 stands and the fact is recorded | rule above |
| KC8 | Suffix-only nulls at K = 4: m4-phase (`k4b_scores.m4_phase`) and SHA-of-suffix (`k4b_scores.sha_phase`) scores against r4; orthogonality means ⟨m_K, r_K⟩ for K ∈ {1, 2, 4, 8, 16} | 0 (I1) | the study-wide null rule of §5.3 (z_null ≈ 4.58, fresh-row re-check) |
| KC9 | Exact enumeration: for K ∈ {1, 2, 3}, E‖m_K‖² and E H(q_K) over all 36^K suffixes with exact stationary probabilities, against the MC means | exact | ≤ 4·SE |
| KC10 | Numerics: Decimal `error_bound.reference_moments` (`error_bound.py:236-265`) on the 16 lowest-index rows at K ∈ {1, 2, 4, 32}, gap ≤ `MOMENT_TOL_EXACT` = 1e-10 (`error_bound.py:287`) by exact Fraction comparison; `suffix_posterior` b32 against `topo_pilot.oracle.BayesFilter` (`oracle/_filter.py:30`) b32 on 1,024 rows | — | ≤ 1e-10; ≤ 1e-12 |
| KC11 | Known-zero worlds at w0 geometry: U (`Unique`, E = I, V = 144) and N (`Identical`, E = 1/36) (`emission.py:191-213`) [V], 4,096 rows each | r_K = 0 ⇒ D_K = B_K = G_K = I_Z = G4^A = 0 | \|x\| ≤ 1e-12 |
| KC12 | Rule consistency: w0 classified by §5 | must **fail** C1 (U_w(D4) < 0.03) | exact |
| KC13 | Row-form cross-check (R-HWS-5): KL-row and entropy-difference estimates of G4, G4^A and I_Z(4) | agreement | report only (difference and its SE) |
| KC14 | p_D2a(w0), exact (§2.6), and the Pinsker violation count | — | report only |

**Outputs frozen in the S0 stage record before S1:** Ĝ4(w0), hence g4*; Ĝ4^A(w0) = g4A*; the per-row SDs at w0 (reporting only); the S0 store hash.

**Contingency (not a tolerance change).** If KC1 (b) fails, S0 stops with FAIL_TECHNICAL/KNOWN_CASE and the coordinator reviews. A plausible cause is code drift between the artifacts' producer (`meta.producer_version` "84152ab27e91+dirty" [V]) and 0a67c5a. A bitwise array comparison against the stored payload would then need an explicit AUTH that names the process-artifact payload reads (MD-11); this plan does not include one.

---

## 4. Sweep design

### 4.1 Factors and levels

| Factor | Levels | w0 | Why |
|---|---|---|---|
| p (stay probability) | 0.2, 0.5, 0.75, 0.875, 0.9375 | 0.2 | Interior mean dwell 1/(1−p) = 1.25, 2, 4, 8, 16 steps: geometric spacing. A slower walk keeps older symbols informative: the most direct lever on beyond-four information. Neighbour weight (1−p)/D_max with D_max = 4 (`transition.py:77-81`) [V]: 1/5, 1/8, 1/16, 1/32, 1/64; exact binary from 0.5 up, so the float T equals the documented law exactly (useful for the stage-C law bound). `TransitionConfig.p_stay` unchanged |
| σ (emission width, "observation noise") | 1.25, 1.5, 2.0, 2.5, 3.0 | 1.25 | A wider emission makes each symbol less informative, so evidence must accumulate. σ = 2.0 met every pre-registered calibration criterion (G_C 0.2657, mean H(b¹) 3.978, min p(w) 0.0248; `PREREGISTRATION.md:49-53`) [V]. Levels below 1.25 sharpen symbols and lower history value (σ = 0.75: G_C 0.1589) [V], so they stay out. `EmissionConfig.sigma` unchanged |
| q (anchored circular aliasing) | 1, 2, 3 | 1 | Distant places on the circle share a public symbol, so local evidence becomes ambiguous along the circle and long history must resolve it. Track X's anchored, circular-only map (§4.3). New code (§12) |
| W (circumference) | 8, 12, 16 (H = 12) | 12 | First-harmonic sensitivity scales like (2π/W)². A smaller circle turns the same positional uncertainty into more angular residual; a larger one has more distinct places. Rectangular centre grid (0.5 + 2i, 0.5 + 2b), i < W/2, b < 6, so V = 3W and the local observation geometry is the same at every W (MD-5). New code; at W = 12 it must equal `GridCenters` bitwise (`centers.py:47-68`) [V] |

**Caveat on p (MD-4).** p is a floor, not the stay probability of every state. Boundary rows (y = 0 and y = 11, degree 3) stay with probability 1 − 3(1 − p)/4 > p (`transition.py:81`) [V]. "Mean dwell 1/(1 − p)" describes interior states only.

**Held fixed, with reasons.**
- **L = 32.** The K4b site (`INDEX = 32`, `k4b_config.py:37`) [V], the model input [BOS, w1..w32] and the training recipe are built on it. D4 is defined relative to m32, so information beyond 32 does not enter the stage-C measure. The S3 horizon profile (K up to 32) tells stage B where the information lies.
- **H = 12.** y is not the circle. Keeping H fixed isolates the circumference.
- **Flat metric, max-degree lazy walk, overlap emission.**
- **Out of the grid (MD-4):** W = 24 (288 states, about 4× the cost per row, farthest from K4b portability; W = 16 already tests the larger-circle direction), σ = 0.75 (low history value), symbol-flip noise and the conductance kernel (new families).

### 4.2 Why the centre grid is new code

`GridCenters` requires V to be a perfect square and places centres at 0.5 + 2a for a < √V whatever the world size (`centers.py:59-68`) [V]. At W = 8 with V = 36 a centre at x = 10.5 lies outside the chart and the build fails with INVALID_SIGMA (`centers.py:28-30`) [V]; at W = 16 the centres would cluster in part of the circle. Track X's scaled centres ((W/12)(0.5 + 2a), …) would tie centre spacing to circumference and so confound W with observation noise. The rectangular spacing-2 grid keeps the local observation geometry fixed and changes only the angular scale (MD-5). It lives inside `tools/hws` and is **not** registered in `CENTER_REGISTRY`, a module dict in `src` (`centers.py:99`) [V], so no `src` edit or runtime mutation is needed.

### 4.3 The anchored circular alias map (MD-6, R-HWS-4)

**Map.** Circular centres i = 0 … W/2 − 1 at x = 0.5 + 2i. Let m(W, q) = ⌈(W/2 − 1)/q⌉. The circular label is
- g(0) = 0 (the anchor, always its own label);
- g(i) = 1 + ((i − 1) mod m) for i ≥ 1.

The axial index b stays visible. Canonical public symbol v = 6·g + b, so n_A = 1 + m circular labels and V′ = 6·n_A. Merged emission: E′[:, 6g + b] = Σ_{i : g(i) = g} E_centres[:, 6i + b]. Probabilities are summed, never averaged or renormalised. At q = 1, g(i) = i and v = 6i + b, which at W = 12 is exactly the `GridCenters` index j = a·k + b (`centers.py:48`) [V].

**Groups and alphabet sizes [W].**

| W | q = 1 | q = 2 | q = 3 |
|---|---|---|---|
| 8 (4 circ. centres) | 4 labels, V′ = 24 | {0}, {1, 3}, {2}: V′ = 18 | {0}, {1, 2, 3}: V′ = 12 |
| 12 (6) | V′ = 36 | {0}, {1, 4}, {2, 5}, {3}: V′ = 24 | {0}, {1, 3, 5}, {2, 4}: V′ = 18 |
| 16 (8) | V′ = 48 | {0}, {1, 5}, {2, 6}, {3, 7}, {4}: V′ = 30 | {0}, {1, 4, 7}, {2, 5}, {3, 6}: V′ = 24 |

At W = 12 this reproduces track X's partitions (q = 2: {1, 4}, {2, 5}, {3}; q = 3: {1, 3, 5}, {2, 4}). The labels depend on (W, q) only, so σ and p vary over identical maps. Every V′ ≥ 12.

**Symmetry check (E3; generalised by the writer).** An exact label-preserving symmetry of the observation process constrains the oracle belief on every history:
- an **x-translation** s ∈ 1..W−1 with E′(z + s·e_x, v) = E′(z, v) for all z, v forces b to be s-periodic and hence m_K ≡ 0 (this is why the anchor exists; track L's check);
- an **x-reflection** x → c − x (mod W), c ∈ 0..W−1, with E′(R z, v) = E′(z, v) forces b to be reflection-symmetric on every history, so m32 always lies on one line through the origin and its phase takes only two values. The observable quotient of the circle is then an interval and the topology question loses its meaning.

A world is **ineligible (E3/SYMMETRY)** if any translation or reflection satisfies max_{z,v} |E′(Tz, v) − E′(z, v)| ≤ 1e-9. T commutes with both on the cylinder lattice, so E′ decides. The check is exact and runs before any sampling.

**Finding [W] (not in either track or the comparison).** Under the map above, three (W, q) cells are exactly reflection-symmetric about the anchor (x → 1 − x, i → −i mod W/2), because each group maps onto itself: (8, 2) {1, 3}; (8, 3) {1, 2, 3}; and (12, 3) {1, 5}, {3}, {2, 4} inside {1, 3, 5}, {2, 4}. The cells (12, 2), (16, 2), (16, 3) and every q = 1 cell are not (for example at (12, 2) the reflection sends 1 → 5, from {1, 4} to {2, 5}). The run confirms this by the exact check. These three cells are recorded as ineligible (INELIGIBLE/SYMMETRY) and not sampled; no substitute reflection-breaking map is used (coordinator ruling OPEN-1, closed).

The unanchored periodic map (g(i) = i mod (W/(2q)) where it divides) is used **only** as a dry-run negative control (§13).

### 4.4 Grid count

Full factorial 5 (p) × 5 (σ) × 3 (q) × 3 (W) = **225 grid worlds**. Excluded before sampling by E3/SYMMETRY: the 75 worlds of the cells (8, 2), (8, 3), (12, 3). **At most 150 worlds are sampled in S1:** 25 at W = 8 (q = 1), 50 at W = 12 (q ∈ {1, 2}), 75 at W = 16 (q ∈ {1, 2, 3}). The exact filters E1, E2 and E4 may exclude more before sampling; every excluded world is recorded with its reason. w0 is one of the sampled worlds.

### 4.5 Portability tiers (how far the K4b tool must move for stage C)

| Tier | Worlds | Stage-B build | K4b changes for stage C (§11) |
|---|---|---|---|
| 0 | W = 12, q = 1 (σ and/or p changed) | existing `src` configs only | process tag and contract; documented-law constants (`process_law.LAW` sigma, neighbour); **not always constants only (RC-3):** tier 0 may require a reviewed law-enclosure change when rational logits do not terminate in Decimal (§8, §11 rows 5 and 12) |
| 1 | W = 12, q = 2 | new `src` emission mode (anchored aliased overlap) | tier 0 + V′ = 24 (BOS, permutation checks, decoder width), a merged-column softmax enclosure (today `process_law_bound` returns UNAVAILABLE when V ≠ 36, `process_law.py:226-227, 240`) [V] |
| 2 | W ∈ {8, 16} | new `src` centre strategy (+ alias mode if q ≥ 2) | tier 1 + period-W features, N = 12W envelope, law dims/period/grid |

### 4.6 World construction (per key, in memory; no artifact-store writes)

1. `world.registry.build_world(WorldConfig("cylinder", (W, 12), "flat"))` (`registry.py:41`; `CylinderBuilder`, `lattice.py:173-178`) [V]. The builder checks Betti (1, 1, 0).
2. `TransitionBuilder().build(world, TransitionConfig(p_stay=p))` (`transition.py:49-86`) [V].
3. Centre emission E_centres [N, 3W]:
   - **W = 12:** `OverlapGaussian().build(world, EmissionConfig("overlap", 36, σ, "grid"), SeedTree(1729))` (`emission.py:130-144`), then `oracle_profile.canonical_emission(E, spec.symbol_perm)` (`oracle_profile.py:58-66`) [V], which returns the centre-ordered matrix (`emission.py:110-111`: E[:, perm] = E_centres) [V]. Symbol names are irrelevant to every quantity.
   - **W ≠ 12:** E_centres[z, j] = softmax_j(−d(z, c_j)²/2σ²) with `process._geometry.point_distances(world, centres, "flat")` (`_geometry.py:67`) and log-sum-exp. This mirrors `_overlap_core` (`emission.py:88-102`) [V]; the private function is not imported.
4. Aliasing (q ≥ 2): merge columns by §4.3. Then the symmetry check (E3).
5. Validity: `oracle_profile.validate_process(T, E′, π, tol=1e-12)` (`oracle_profile.py:69-91`) [V]. Features c(z) = (cos, sin)(`2.0*np.pi*x/W`), bitwise equal to `oracle_profile.circle_features` at W = 12 (`oracle_profile.py:40-55`, PERIOD = 12 at `:21`) [V] (tested, DR5).
6. Exact per-world values before sampling: p(w), min p(w), A_eff, p_D2a, V′, the symmetry record, tier, number of changed factors, distance (§5.5). E1–E4 are decided here.

### 4.7 Per-row computation (one pass per world)

1. **Sampling.** `HMMSampler(T, E′, π, SequenceLayout()).sample(n, rng)` (`sampler.py:33-80`) [V] returns tokens [n, 33] and states. For each world-look, `HMMSampler.sample(n, rng)` is called exactly once (RC-5; it draws all initial states, then emission and transition uniforms by time step, `sampler.py:74`). w33 and the states are dropped in memory at once; canonical tokens w1..w32 are kept as uint8 [n, 32] (V′ ≤ 48; U uses V = 144 ≤ 255).
2. **Filtering.** For each K: b_K = `suffix_posterior(T, E′, π, tok, K)`; m_K = b_K @ c (bitwise equal to `posterior_means`, tested); q_K = b_K @ T @ E′; q_K^A and b_K^x by summation. Sampling, filtering and numerical aggregation use the frozen whole-world call shapes; variable numerical chunking is disabled in HWS-v1.
3. **Per-row arrays.** D_K and ‖r_K‖ for every K; KL(q32‖q_K) for every K; KL(q32^A‖q4^A); KL(b32‖b4) and KL(b32^x‖b4^x); the entropy terms H(q_K), H(q_K^A), H(b_K), H(b_K^x) for K ∈ {4, 32}; ‖m32‖ and arg m32; the seven null rows (§5.3); the Pinsker slack; in S3 only, the P4 row value and the extra K.
4. Aggregates per world: means, SEs, the bounds of §5.3, the E5 statistics, the annotations of §7.3.

### 4.8 Expectations, for range-setting only

A Gaussian/Kalman desk heuristic (Appendix A [W], calibrated to the w0 D4) puts D4 ≈ 0.03–0.05 at p ≥ 0.875 or σ ≥ 2 (tier 0) and about 0.005–0.017 for W ∈ {16, 8} at w0's other values. It says nothing about aliasing, can be wrong by 2× and gates nothing.

---

## 5. The frozen selection rule

### 5.1 Eligibility (every filter must pass; failures are recorded, never repaired)

| # | Filter | Computed |
|---|---|---|
| E1 | `validate_process` passes; the world builder passes (Betti (1, 1, 0)) | exact, before sampling |
| E2 | Symbols alive: min_w p(w) ≥ 0.5/V′ (the registered rule, `PREREGISTRATION.md:206`, `min_symbol_prob_factor: 0.5`) [V]. For q ≥ 2 the threshold is scaled by the number of centres merged into a symbol: p(v) ≥ 0.5·\|v\|/V, where \|v\| is the number of centres merged into v; it equals 0.5/V′ at q = 1 (coordinator ruling OPEN-4, closed) | exact, before sampling |
| E3 | No exact x-translation or x-reflection symmetry of E′ (§4.3) | exact, before sampling |
| E4 | **Registry-safe alphabet:** p_D2a(w) ≤ **τ_D2a = 5 × 10⁻⁷** (§2.6, justification below) | exact, before sampling |
| E5 | Circle legibility, §2.5 | S1/X1/S2 point estimates for screening; S3 rows for decisions |
| E6 | Numerical integrity: every row finite; posteriors normalised within 1e-12; the null rule of §5.3 in every world; the S3 spot checks of §8; Pinsker violation count reported (a nonzero count is a review flag, not a stop) | every stage |

**Why τ_D2a = 5 × 10⁻⁷ (R-HWS-3, fixed by the writer).** The sealed-D-2a predicate is fail-closed for the whole study: a single satisfying row in the cal, val or test tables makes K4b INCONCLUSIVE/REGISTRY_INCOMPLETE and rows are never removed or replaced (`k4b_data.py:186-190`; `PROTOCOL_K4B_v1.md:243`) [V]. Under the K4b contract the most rows stage C can check are cal 3,072 + val 3,072 + test 12,288 (the largest ladder step) = **18,432** (`tools/k4b/CONTRACT.json` `splits` and `ladder`; `k4b_config.py:40-41`) [V]. These tables are shared by all models (`k4b_data.sample_block`, `k4b_data.py:83-92`) [V], so the model count does not change the number. By the union bound, P(any stage-C row satisfies the predicate) ≤ 18,432 · p_D2a ≤ 18,432 × 5e-7 = **0.0092 < 0.01** [W]. So a selected world carries at most a 1 % risk that stage C ends INCOMPLETE through this predicate alone. If stage C's binding changes the ladder or the canonical label order, it re-checks N_C · p_D2a ≤ 0.01 (§11 row 9). The label order is frozen in §4.3 and not optimised.

An E6 failure is FAIL_TECHNICAL for that world and stops the study for coordinator review (§9.4). It is never a scientific exclusion.

### 5.2 Criteria (all four required)

| # | Criterion | Threshold (equality passes) |
|---|---|---|
| **C1** | 3× the stage-C margin | bound on D4 ≥ **0.03** = 3M |
| **C2** | Context benefit | bound on G_C ≥ **0.10** nats |
| **C3** | Beyond-four predictive incentive | bound on G4 ≥ **g4*** = max(Ĝ4(w0), 0.0078) nats |
| **C4** | Circular-symbol beyond-four incentive | bound on G4^A ≥ **g4A*** = Ĝ4^A(w0) nats |

All comparisons are in float64 on the reported bounds. Rows for C3 and C4 are the KL rows (R-HWS-5).

### 5.3 Bounds and error control (MD-2, R-HWS-3)

All bounds are nominal normal or percentile-bootstrap approximations and are reported as such (shared rule 4). The z constants are computed by the implementation as `statistics.NormalDist().inv_cdf(·)` from the exact frozen arguments below; the decimals here are [W].

1. **Nominal screening bounds (S1, X1, S2).** L1 = x̂ − 2.326·SE and U1 = x̂ + 2.326·SE (one-sided 1 %). Used only for the "confident" class and for ranking (§5.4, §5.5).
2. **Widened exclusion and candidacy bound.** U_w = x̂ + z_w·SE and L_w = x̂ − z_w·SE with **z_w = z_{1 − 0.05/(4·N_slots)}**, N_slots = **308** = the frozen maximum of statistically evaluated world-looks: S1 150 + X1 102 + S2 40 + S3 16. z_w ≈ **3.94** [W]. A world is **excluded** iff U_w fails at least one of C1–C4 on its latest look (S3 data for finalists). Bonferroni over every world-look and the four criteria gives P(any truly qualifying world is wrongly excluded) ≤ 0.05. The same U_w decides candidacy, which makes screening more liberal, never less. N_slots stays 308 even if fewer worlds are evaluated (conservative).
3. **Decision bound (S3, fresh rows).** Per finalist and criterion, L3 = min(x̂ − 2.7344·SE, the rank-16 order statistic of 5,000 bootstrap means). α_f = 0.05/16 = 0.003125; rank 16 = ⌈5000 · 0.003125⌉ by `c1_means.rank_for` (`c1_means.py:57-60`) [V]; one bootstrap index stream per world, shared by every array (`c1_means.bootstrap_means`, `c1_means.py:31-43`) [V]. α_f stays 0.05/16 even with fewer finalists.
4. **Error control for selection.** Qualification is an intersection test: a non-qualifying finalist falsely qualifies only if each of its truly failing criteria passes, so the probability is ≤ α_f per finalist and ≤ 0.05 over ≤ 16 finalists. Fresh S3 rows make the screening-stage selection irrelevant to this guarantee.
5. **Null checks (E6, KC8; R-HWS-3).** Per world-look, seven suffix-only nulls are tested: m4-phase score, SHA-of-suffix score (both against r4), and ⟨m_K, r_K⟩ for K ∈ {1, 2, 4, 8, 16}; each has population mean 0 by I1. The family is every null check in the study: N_null = 7 × (1 S0 world + 292 screening worlds + 16 S3 looks) = **2,163**. Two-sided Bonferroni threshold at family level 0.01: **z_null = z_{1 − 0.01/(2·2163)} ≈ 4.58** [W]. A world-look with |x̂|/SE > z_null is **reported** and re-checked once on fresh rows (stream `NULLCHK`, §6.6, same n). It **halts** the study (FAIL_TECHNICAL/NULL for coordinator review; FAIL_TECHNICAL/KNOWN_CASE at S0) only if the same null exceeds z_null again. A non-reproduced exceedance stays on the record and does not change the world's status.

### 5.4 Classification after screening (S1, then X1 and S2)

Each evaluated world receives exactly one class on its screening data:

| Class | Condition |
|---|---|
| INELIGIBLE/<filter> | fails E1–E4 (exact) or E5 (point estimates) |
| EXCLUDED/<criterion> | eligible, and U_w fails at least one of C1–C4 |
| CANDIDATE/CONFIDENT | eligible, and L1 passes all of C1–C4 (so its coarse lower bound already clears 0.03) |
| CANDIDATE/POSSIBLE | eligible, U_w passes all of C1–C4, not CONFIDENT, and **D̂4 ≥ 0.03** (R-HWS-1) |
| CANDIDATE/MARGINAL | eligible, U_w passes all of C1–C4, not CONFIDENT, D̂4 < 0.03 |

MARGINAL candidates can never fill an ordinary finalist slot (R-HWS-1); they may appear only in the fallback-only 2× set of §5.6 (RC-1). They are not excluded either, so they block the no-world licence (§7).

### 5.5 Ranking (lexicographic, deterministic)

1. Confidence class: CONFIDENT before POSSIBLE (track X's "confidently qualified first").
2. Tier, 0 < 1 < 2.
3. Number of factors changed from w0, counting σ (0–4). (Track X left σ out of its count without a reason; σ changes the documented law, `process_law.LAW["sigma"]`, `process_law.py:30`.)
4. Distance: Σ over factors of |level index − w0 index|. p and σ indices 0–4 (X1 levels: p 0.96875 → 5; σ 3.5 → 5, 4.0 → 6); q index q − 1; W: 8 → 1, 16 → 1. S2 midpoints count as half steps.
5. Larger L1(G4) (the learning incentive).
6. World key, lexicographic.

Steps 2–6 use no D4 value. **Why minimal departure ranks after confidence.** The training recipe, the chart rule and the K4b tool were validated near w0, so the fewer and smaller the changes, the less stage B and C must newly establish. But a slot spent on a near-w0 world whose true D4 is about 0.03 is likely wasted (it needs a point estimate ≥ 0.031 on 32,768 rows), so worlds already confidently above 0.03 are confirmed first (MD-8, R-HWS-1).

### 5.6 Finalists, selection and fallback

1. **Ordinary finalists.** The first 16 CONFIDENT or POSSIBLE candidates in the §5.5 order, after S1, X1 and S2 have run as triggered (§6.2). MARGINAL worlds cannot fill ordinary finalist slots.
2. **If there is no CONFIDENT or POSSIBLE candidate:** the finalists are the fallback-only "2× set": eligible worlds with U_w(D4) ≥ 0.02 and U_w passing C2–C4, the 16 with the largest D̂4 (ties by key). If no CONFIDENT or POSSIBLE candidate exists, the 2× set receives fallback-only confirmation. These worlds cannot produce HWS_SELECTED or enter its fallback list. They may produce HWS_BELOW_3X under §7.1. (RC-1)
3. **S3** runs every finalist (ordinary or fallback-only) on 32,768 fresh rows. An ordinary finalist **qualifies** if it passes E1–E6 and C1–C4 on S3 data with L3. A fallback-only world is evaluated against the BELOW_3X condition of §7.1 only; it never qualifies.
4. **Selected** = the first qualifier among the ordinary finalists in the frozen finalist order (no re-ranking on S3 data). The next two ordinary qualifiers in that order are recorded as the **fallback list**; using one needs an owner decision (§10.4). The selection clauses of this section apply to ordinary finalists only.

---

## 6. Stages and sample sizes

### 6.1 Stage table

| Stage | Worlds | Rows per world | Purpose |
|---|---|---|---|
| S0 | w0, U, N | 32,768 (U, N: 4,096) | §3; gating; freezes g4*, g4A*; its own job |
| S1 | ≤ 150 (§4.4) | n1 = 4,096 | coarse screen |
| X1 (conditional) | ≤ 102 | 4,096 | one frozen range extension |
| S2 (conditional) | ≤ 40 midpoints | 4,096 | one refinement round |
| S3 | ≤ 16 finalists | n3 = 32,768 fresh | confirmation and selection |

S1 → (X1) → (S2) → S3 run as one job under the frozen rules after the coordinator's S0 ACCEPT.

**Precision [W from H].** K4b's D4 interval implies a per-row SD of about 2.3× the mean (SE ≈ 0.00036 at n = 3,072, mean 0.0085). If the SD scales with the mean, at D4 = 0.03 it is about 0.07: SE ≈ 0.0011 at 4,096 rows and ≈ 0.00039 at 32,768 rows. Then a world is a candidate on D4 if D̂4 ≳ 0.0257, CONFIDENT if D̂4 ≳ 0.0326, and a finalist confirms C1 if D̂4 ≳ 0.0311.

### 6.2 Frozen extension and refinement rules (addendum 26 item 3)

The quantities here are oracle design targets with no sealed test outcome, so using point estimates in the triggers is allowed (MD-9). Every rule is fixed now, so the adaptive budget cannot become "run until it comes out".

1. **X1, range extension, at most once.**
   - **Trigger:** after S1 there is no CANDIDATE (any subclass), and the eligible world with the largest point estimate D̂4 has p = 0.9375 or σ = 3.0. For X1, choose the largest-D̂4 eligible world, breaking exact ties by ascending world key; if none exists, skip X1. (RC-6)
   - **Added levels:** p = 0.96875 (dwell 32) if that world has p at its top; σ ∈ {3.5, 4.0} if it has σ at its top. Each added level is crossed with every level of the other factors in every eligible (W, q) cell. Counts [W]: p only 30, σ only 60, both 102 (6 cells × (6·7 − 25)).
   - X1 worlds join the S1 table and the §5.4 classification. No circumference or aliasing extension is automatic.
2. **S2, refinement, at most once.**
   - **Trigger:** at least one CANDIDATE exists after S1 (and X1 if it ran).
   - Take the lowest tier that contains a candidate. Within it, take every grid edge along p or σ (adjacent levels, other factors equal, both endpoints eligible) whose endpoints differ in candidate status.
   - Evaluate each edge's midpoint world. σ midpoints 1.375, 1.75, 2.25, 2.75 (and 3.25, 3.75 if X1 added σ levels). The p-edge refinement values are explicitly frozen as 0.375, 2/3, 5/6, 11/12, and 23/24 for the extension edge; use these values rather than computing dwell midpoints. (RC-6)
   - Cap 40, chosen by (changed factors, distance, key). S2 worlds join the classification.
3. **S3 runs once.** Its sample size is fixed. No top-up, no resampling of a finalist, no second batch.
4. **Nothing else grows:** no new factors, levels, rows, thresholds or rounds. Cost measurements may change scheduling only.

### 6.3 Every scheduled stage

S0 and S1 are always scheduled; X1 and S2 are scheduled iff their triggers fire; S3 is scheduled iff there is at least one finalist (with no finalist it is complete by definition). "Every scheduled stage completed" (R-HWS-1, §7) refers to this list.

### 6.4 Stage-A rows are design data

No stage-A history ever becomes stage-B or stage-C test data (addendum 25 rule 3). Stage C's registry must cover `hws-store` (§11 row 10).

### 6.5 Records

Stage records use `stage_records.write_new`, `save_npz`, `record_gate` and `sha256` (`stage_records.py:31-69`) [V], with exclusive create. Every evaluated world is reported; none is dropped.

### 6.6 Seeds and streams (MD-17; G0 verifies no prior issuance)

- Histories: `SeedTree(0).generator("data", "hws-v1", stage, key)` with stage ∈ {S0, S1, X1, S2, S3, NULLCHK, DRY}. For NULLCHK the scope is ("data", "hws-v1", "NULLCHK", stage_of_the_exceedance, key). The same pattern as K4b (`k4b_data.py:75`) [V].
- Key: the canonical world string `W{W}-q{q}-s{σ!r}-p{p!r}`; U and N: `U-W12`, `N-W12`.
- Synthetic (DRY), discovery (S1, X1, S2), confirmation (S3) and re-check (NULLCHK) streams are separate; stages never share a stream, so S3 rows are fresh relative to every screening row.
- No stream is extended. For each world-look, call `HMMSampler.sample(n, rng)` exactly once. Sampling, filtering and numerical aggregation use the frozen whole-world call shapes; variable numerical chunking is disabled in HWS-v1. Cost measurements may change scheduling only. Resume occurs at world boundaries and regenerates an interrupted world from its original stream. (RC-5)
- Prefix permutation for P4: `SeedTree(0).generator("hws-v1", "prefix_perm", key)`.
- Alias labels are deterministic (§4.3) and need no seed.
- Bootstrap: PCG64 seeds 620101 (S0) and 620103 (S3) via `c1_means.bootstrap_means`.
- G0 records that the scope "hws-v1" and the two bootstrap seeds appear in no earlier seed map, generation manifest or execution record (the K4b G0 pattern; text search is a discovery aid, every hit is classified, unresolved prior use fails closed).

---

## 7. Outcomes and licences (registered now; addendum 25 rule 6 included)

### 7.1 Outcomes, in order of precedence

| Outcome | Condition |
|---|---|
| **FAIL_TECHNICAL/<reason>** | an S0 known-case failure; a reproduced null; a numerical, integrity, identity or lineage defect not resolved under §9.4 |
| **INCONCLUSIVE/RESOURCE_OR_AUTHORITY** | some scheduled stage did not complete: a disk safe-STOP or memory stop that cannot be resumed, a 3× pause the owner does not continue, or missing or expired authority |
| **HWS_SELECTED/T0, /T1, /T2** | ≥ 1 ordinary-finalist qualifier (§5.6); the tier of the selected world. Fallback-only worlds never produce this outcome |
| **HWS_BELOW_3X** | no ordinary finalist qualified for selection, and ≥ 1 S3 world (ordinary finalist or fallback-only) passes E1–E6 and C2–C4 at L3 with L3(D4) ≥ 0.02 |
| **HWS_NO_WORLD_CONFIRMED** | no earlier outcome applies and at least one unresolved world remains. An unresolved world passes E1–E6 on its latest look and has U_w satisfying C1–C4 (RC-7) |
| **HWS_NO_SUITABLE_WORLD/HEADROOM or /FILTER** | none of the above: every evaluated world is INELIGIBLE or EXCLUDED, **and every scheduled stage completed** (R-HWS-1). HEADROOM applies iff at least one eligible evaluated world exists and every eligible evaluated world is excluded by C1 (U_w(D4) < 0.03). Otherwise use FILTER. |

A paused or unauthorised search can never receive the no-world licence (track X; MD-10).

### 7.2 Licences

**HWS_SELECTED (filled at run time).** "In world w* = (W, q, σ, p) on a 12-high cylinder, under its documented law, on 32,768 fresh oracle-only histories:
- the phase-only oracle comparator D4 (the ideal belief-phase coordinate's covariance with r4 = m32 − m4, in the units of the K4b measure) has a one-sided lower bound ℓ ≥ 0.03, 3× the K4b margin;
- the context gain G_C has lower bound ≥ 0.10 nats;
- the beyond-four predictive gain G4 has lower bound ≥ g4*, and its circular-symbol part G4^A has lower bound ≥ g4A*.

These are nominal bounds at α = 0.05/16. The world is the first qualifier in the frozen order (confidence class, then minimal departure)." It does **not** license:
1. that any model learns it, captures any share of D4 or passes a learning gate;
2. that stage C will reach SUPPORT;
3. that D4 bounds a model's coordinate;
4. anything about the E4 models or any earlier verdict;
5. that w* is optimal, unique or the world where history matters most;
6. anything outside the grid.

A T1 or T2 selection adds: "requires new emission/centre code and the K4b changes of §11; owner go-ahead needed before stage B" (§15 Q2).

**HWS_BELOW_3X ("positive but below 3×", rule 6).** "Within the swept range, the beyond-four first-harmonic information confirmed on fresh rows reaches at least 2× the K4b margin (the addendum-25 rule-1 floor) in worlds …. No ordinary finalist qualified for selection. Any fallback-only world whose L3(D4) also reaches 0.03 is explicitly reported; no upper bound below 0.03 is implied. 3× absence among all evaluated worlds: shown / not shown." ("Shown" iff every evaluated world is excluded by C1–C4 under U_w.) Nothing is selected automatically; the owner may choose one of these worlds or ask for an extension (§15 Q5). It does not license a claim that 3× is unreachable.

**HWS_NO_WORLD_CONFIRMED.** "No evaluated world was confirmed at the frozen criteria; candidates remained that were not finalists or not confirmed (listed), so the absence of a suitable world in the grid is **not** shown." It licenses no absence claim.

**HWS_NO_SUITABLE_WORLD (R-HWS-1).** "No world in the swept grid (§4.4, plus the registered X1 and S2 worlds that ran) met the frozen criteria at the stated levels: every evaluated world failed an exact eligibility filter, the E5 point-estimate legibility filter, or at least one of C1–C4 under the widened bound (z_w ≈ 3.94, family error ≤ 0.05 for wrongly excluding a qualifying world). Sub-reason … The maximum observed D̂4 is … at …." It does **not** license:
- anything about grid points not evaluated, other alias maps, other families, lengths, harmonics, y, or nonlinear readouts;
- that history is unimportant, or that models do not use history;
- any change to K4b's verdict.

The next step would be to change the question or the family (owner decision).

**INCONCLUSIVE/RESOURCE_OR_AUTHORITY and FAIL_TECHNICAL** license no scientific statement.

### 7.3 Descriptive annotations (track X; per world, never decision-bearing)

On each world's latest look, with L_w and U_w on D4:
- `ORACLE_POSITIVE_BELOW_C_MARGIN` when 0 < L_w ≤ U_w < 0.01;
- `ORACLE_POSITIVE_BELOW_SWEEP_REQUIREMENT` when L_w > 0 and U_w < 0.03.

They distinguish detectable positive covariance from adequate headroom. They do not revise K4b's historical status.

---

## 8. Numerics and exactness (MD-3)

- **Exact per row, sampled across rows.** Each row's b_K, m_K and q_K are the exact Bayes filter in float64: a normalised forward recursion with positive entries. K4b certified per-row moment gaps ≤ 8.5e-16 and row bounds ≤ 9e-16 on this kernel [H]. Expectations over histories cannot be enumerated (at least 8^32 ≈ 8e28 histories at W = 8 even at q = 3 with V′ = 12: 12^32), so Monte Carlo over independent stationary histories is the only route.
- **MC error dominates float error.** SE ≈ 1e-4 to 1e-3 against float error ≈ 1e-15, a factor ≥ 10^10. **No new numerical certificate is built in stage A** (MD-3): stage A selects a design and decides no scientific claim; stage C re-measures `delta4_orc` on its own fresh rows under its own certificate. Track X's certificate list (construction, filtering, features, phase, validated logarithms, law transport) moves to the stage-C binding work (§11). There is no 1e-6 allowance and no 80/160-digit fallback.
- **Underflow is not a realistic risk.** `suffix_posterior` normalises after every emission (`oracle_profile.py:141-149`) [V]. The smallest relative emission entry is about e^−50 at σ = 1.25 [W from the comparison], far above the float64 minimum. Full-support softmax emissions keep every q and b entry positive, so every KL term is finite. U and N go through the `context_gain` zero-support convention (`_futures.py:100-107`) [V].
- **Exact pieces.** Every world: p(w), min p(w), A_eff, p_D2a, the symmetry checks. S0: suffix enumeration for K ≤ 3 (46,656 suffixes). Dry run: all histories of the tiny world.
- **Spot checks in S3 (E6).**
  - W = 12 finalists: Decimal `reference_moments` on 4 rows × K ∈ {4, 32}, gap ≤ 1e-10. Valid for any T, E at W = 12, because only `exact_features` (12-gon table, `error_bound.py:146-173`) is period-specific and `_checked_histories` needs only length 32 and symbols < V′ (`error_bound.py:225-233`) [V].
  - W ≠ 12 finalists: `suffix_posterior` against `BayesFilter` on 256 rows, ≤ 1e-12.
- **Phase convention.** Exactly K4b's: an exact zero maps to phase 0; phases wrapped to [0, 2π) (`k4b_scores.py:27-38`) [V].
- **Tier-0 de-risking (report only).** For each tier-0 finalist, `process_law.process_law_bound(T, E, π, coords)` (`process_law.py:222`) runs with `LAW["sigma"]` and `LAW["neighbour"]` rebound in process (the functions read the module dict at call time, `process_law.py:64, 105`) [V]. Status and Z_bound are recorded so stage C knows the transport bound is available. Tier 0 may require a reviewed law-enclosure change when rational logits do not terminate in Decimal. In stage A, the report-only wrapper catches `decimal.Inexact` from the unchanged enclosure and records `UNAVAILABLE/NONTERMINATING_LOGIT`, without changing eligibility, ranking or selection. Other exceptions retain their normal technical-failure treatment. Before stage C, an independently reviewed enclosure must bound rational-to-Decimal logit conversion error and return BOUNDED; disabling the trap alone is insufficient. (RC-3: `softmax_enclosure`, `process_law.py:106`, traps on inexact Decimal division; for example at σ = 1.5 the logit at squared distance 1/2 is −1/9, and σ = 3 and several refinement widths also give repeating decimals; `process_law_bound` catches only `Mismatch`.) The reviewed enclosure change is J1/J2 implementation work, not a protocol change.
- **Statistical approximation.** All bounds are nominal (§5.3) and reported as such.

---

## 9. Adaptive budget (addendum 26)

### 9.1 Forecast basis (single thread, measure-only, never a cap)

- **Reference:** job 0014's profile run took **2.87 CPU s** for 4,096 rows × K ∈ {1, 2, 4, 8, 16, 32} at N = 144 (`jobs/0014/report.md:254`) [V]. (Track L's "56.75 s" is that job's whole measured total, including tests, snapshots, meter checks and a 24.21 s validate, `report.md:232-256`, not the profile; R-HWS-6.)
- Work per row: Σ K = 63 belief steps of 2N² flops, about 1.07e10 flops for 4,096 rows at N = 144, i.e. job 0014 ran at about 3.7 GFLOP/s effective [W].
- HWS adds the predictives q_K (about +12 %), the KL and entropy rows, the nulls and Python overhead. The frozen central rates below carry about 2.4× slack over the job-0014 rate and scale with N² [W].

**Frozen per-world central rates (CPU s) [W].**

| Stage type | W = 8 (N = 96) | W = 12 (N = 144) | W = 16 (N = 192) |
|---|---|---|---|
| Screening world (S1, X1, S2; 4,096 rows; incl. ≈ 1 s build and exact pieces) | 4 | 8 | 13 |
| S3 finalist (32,768 rows, 9 K + P4 = 137 steps, 5,000-draw bootstrap, spot checks) | 70 | 190 (tier 0, incl. `process_law_bound`) / 160 (tier 1) | 235 |

The forecast of a conditional stage is the sum of these frozen rates over the worlds it actually schedules; this is computed when the worklist is fixed and is not a re-estimate.

### 9.2 Stage forecast

| Stage | Content | Central | Range |
|---|---|---|---|
| J1 IMPL (separate job) | API.md, CONTRACT, tests A/B, modules, preflight suites, the synthetic dry run (§13) | 540 s (0.15 h) | 0.1–0.4 h |
| S0 | w0 at 32,768 rows; U and N; enumeration K ≤ 3; 16 Decimal rows; 1,024-row cross-implementation; KC1 rebuild | 360 s (0.1 h) | 0.05–0.3 h |
| S1 | 25 × 4 + 50 × 8 + 75 × 13 | 1,475 s (0.41 h) | 0.2–1.2 h |
| X1 (if triggered; maximal 102 worlds) | 17 × 4 + 34 × 8 + 51 × 13 | 1,003 s (0.28 h) | 0.15–0.8 h |
| S2 (if triggered; cap 40) | 40 × ≈ 9 (mixed) | 360 s (0.1 h) | 0.03–0.3 h |
| S3 | 16 finalists × ≈ 200 (mixed) | 3,200 s (0.89 h) | 0.4–2.0 h |
| **Study total (S0–S3)** | without X1 / with X1 | **5,395 s (1.50 h) / 6,398 s (1.78 h)** | 0.8–3.8 h / 1.0–4.6 h |

- RAM: < 1 GB (a 32,768 × 192 float64 belief array is 50 MB); whole-world call shapes, no variable numerical chunking (RC-5). Track X's 8 GiB memory cap and the meter's limits stay. After calling `k4b_meter_bind.bind`, the HWS wrapper explicitly sets `winjob.MEMORY_CAP = 8 * 1024**3` and rebinds `TEMP_ROOT` to the HWS job’s store. DR12 verifies the effective child settings. (RC-9: `bind` sets 12 GiB, `k4b_meter_bind.py:43`.)
- Store: < 100 MB (§12.3). TEMP, TMP and TMPDIR on X:, disk floors C: ≥ 2 GB and X: ≥ 30 GB (`k4b_meter_bind.py:25`) [V], as in K4B-FROZEN-v1 §11.7.

### 9.3 The 3× pauses (MD-16; both triggers apply)

The meter measures every run and never stops one on CPU (`--max-cpu inf --max-wall inf`). The study ledger (`hws-store/cpu_ledger.json`, never reset) starts at S0; J1 has its own ledger and its own stage trigger (1,620 s).

- **Per-stage trigger.** A stage's running measured CPU exceeds 3× that stage's central forecast (§9.1 rates on its actual worklist).
- **Cumulative trigger.** Cumulative study CPU exceeds 3× the cumulative central forecast through the end of the current stage.
- **When checked:** at every world boundary and every stage boundary. Once a trigger fires, no new world starts; the stage is paused in a resumable state and the coordinator reports to the owner in plain language (measured CPU, work done, causes, a revised forecast that never erases the original). Continuation needs the owner's decision. The pause is checked at every world boundary (coordinator ruling OPEN-2, closed). If the owner does not continue, the outcome is INCONCLUSIVE/RESOURCE_OR_AUTHORITY.

Cumulative 3× thresholds for the maximal worklists [W] (the run computes them from its actual worklists):

| Boundary | Cumulative central | 3× threshold |
|---|---|---|
| after S0 | 360 s | 1,080 s |
| after S1 | 1,835 s | 5,505 s |
| after X1 (if run) | 2,838 s | 8,514 s |
| after S2 (no X1 / X1) | 2,195 / 3,198 s | 6,585 / 9,594 s |
| after S3 (no X1 / X1) | 5,395 / 6,398 s | 16,185 / 19,194 s |

Per-stage 3× thresholds at the forecasts above: S0 1,080 s; S1 4,425 s; X1 ≤ 3,009 s; S2 ≤ 1,560 s (40 W = 16 worlds); S3 ≤ 11,280 s (16 W = 16 finalists), 9,600 s at the central mix.

### 9.4 Jobs, review and technical correction

- **Jobs (RC-4 sequence).** Design review acceptance → separate owner AUTH for J1 (implementation, tests and synthetic-only dry runs; it authorizes no S0 or sweep sampling) → J1 → coordinator acceptance of DR1–DR13 with a committed report bound to the implementation hash → final HWS execution freeze → owner AUTH for S0–S3 → S0 job → coordinator ACCEPT (g4*, g4A* frozen) → one job S1 → (X1) → (S2) → S3 → report. Each job binds the meter through `hws_meter_bind` (§12.1).
- **Technical correction (the K4B-FROZEN-v1 §11.8 pattern).**
  - Only for a documented implementation or environment defect; at most two corrections per defect.
  - Completed worlds must regenerate bit-identically; the failed attempt is archived under `superseded/`.
  - Correcting a world whose criteria were already computed needs an owner decision if the correction would change any reported bound.
  - A disk safe-STOP or memory stop that cannot be resumed is INCONCLUSIVE/RESOURCE_OR_AUTHORITY.

---

## 10. Hand-off to stage B

### 10.1 What the selected world passes on (`hws-store/SELECTION.json`, hashed; one immutable package)

- **Configs and identity.** `WorldConfig`, `TransitionConfig`; `EmissionConfig` (tier 0) or the centre list, the alias map and its hash (tiers 1–2); the **canonical label order** v = 6g + b (binding for stage C: p_D2a is computed under it); sha256 of T, E′, π and coords bytes; the world key and tier; the source commit and the HWS FREEZE hash; discovery and confirmation stream identities.
- **Expected effect sizes** (S3 point, central 95 % interval, L3): D_K, B_K, V_K for K ∈ {1, 2, 4, 6, 8, 12, 16, 24}; G_K, G_C, G_0, G4^A, I_Z(4), I^x_4 (nats and bits) and H*; the ‖m32‖ distribution, phase bins, R2, p_weak, p_gain, A_eff and P4; the per-row SDs of D4 and ‖r4‖; p_D2a.
- **Search record.** Every evaluated world with its class, bounds and annotations; measured oracle cost per stage; the fallback list.

### 10.2 Implied stage-C numbers (formulae; run values filled in)

- Margin M = 0.01 (K4b) and the ratio D4/M.
- **δ_max = L3(D4)/3** (track X): the largest stage-C margin this world supports at 3×. If later planning proposes a margin above δ_max, the headroom gate must be revisited. The margin is never lowered after model results.
- A model at capture c (= E X−/D4) is expected at about c·D4 − (missing mass) (K4B-FROZEN-v1 §1.4). SUPPORT needs L(E X−) − F > M, so the planned minimum capture is c_min ≈ (M + z_{1−α}·SD_X/√N + missing mass)/D4, with α = 0.05/n_models.
- Illustration [W]: D4 = 0.03, SD_X = 0.07, N = 3,072, α = 0.05/3 (z ≈ 2.128) give c_min ≈ 0.42 plus the missing-mass share; with 5 models (α = 0.01, z ≈ 2.326), ≈ 0.43.

### 10.3 What stage B must check (pilot histories only; never stage-C test data)

| # | Check | Pass reading |
|---|---|---|
| B1 | Learning gate with the E4 recipe (1–2 models): captured = 1 − regret/G_C | ≥ 0.8 (existing gate) |
| B2 | Forcing, beyond the four-symbol baseline: pilot regret r_B against G4 (Proposition F) | r_B < G4 means predictions are not suffix-4-only; report r_B/G4 |
| B3 | Forcing on the circular component: pilot regret on the circular-label marginal against G4^A | r_B^A < G4^A; report the ratio |
| B4 | A circle in the representation: the LCC ≥ 95 % chart rule with C0-cal- and C0-val-type criteria on pilot activations, and held-out phase extension | as in K4B-FROZEN-v1 §4 |
| B5 | Pilot capture ratio: the K4b-type E X− on pilot histories / D4 | ≥ c_min (§10.2), else stage C is underpowered at M |
| B6 | Pilot SDs of X± and the support and missing mass (unsupported-row completion width) | fix stage-C N by the K4b ladder (rule 3) |
| B7 | Measured CPU per model in the new world; model count | stage-C budget; prefer 3 models unless a reviewed generalisation to 5 is justified (§11 row 4) |
| B8 | The §11 K4b changes implemented, versioned and passing their own synthetic dry run, including Z_bound BOUNDED for w* | before any stage-C data |
| B9 | Registry: the stage-C registry covers `hws-store` and the stage-B store; N_C · p_D2a ≤ 0.01 under the stage-C ladder and label order | before any stage-C data |

Stage B must not infer model success from oracle qualification.

### 10.4 Fallback

If B1 or B4 fails, the first remedy considered is the next fallback world, **but only by an owner decision** (both tracks). A stage-B failure never automatically licenses the next world (track X), and no recipe change is made first.

---

## 11. K4b binding table for stage C (MD-13; stage-C work, outside stage A)

The estimand, the support completion (Theorem A), the bootstrap, F, the decision rule and the licences are world-generic and stay unchanged. The world-specific pieces, with the tiers that need a change:

| # | Item | Where (0a67c5a) [V] | Current value | Needed for |
|---|---|---|---|---|
| 1 | Process tag, seed scope, models, site | `k4b_config.py:36-40` (MODELS :36; SITE, INDEX, BOS, D_MODEL :37; SCOPE :38; PROCESS :39); `tools/k4b/CONTRACT.json` | ("cylinder", "overlap", "1.25"), k4b-sf-v1, 1729/2718/3141 | every tier: a new versioned contract |
| 2 | BOS id and alphabet size | `k4b_config.BOS = 36` (:37); `k4b_data.load_process` permutation check `range(36)` (`k4b_data.py:54`) | 36 | every world with V′ ≠ 36 (tier 1; tier 2: W = 8 q = 1 gives 24, W = 16 q = 1 gives 48) |
| 3 | Suffix decoder width | `k4b_decoder.one_hot_suffix` 4 × 36 = 144 columns (`k4b_decoder.py:25-30`); `rbf_map(144, …)` (:57) | 144 | every world with V′ ≠ 36: 4·V′ |
| 4 | Model count and multiplicity | `ALPHA = c1_means.P_THIRD` = 5/300 (`k4b_config.py:61`; `c1_means.py:63`); `RANKS` alpha 84, one_minus_alpha 4917 (`k4b_config.py:51-57`); CONTRACT ladder alpha "5/300" | 3 models, α = 0.05/3 | any model count ≠ 3: α = 0.05/n, ranks recomputed by `rank_for`, overall-status binding reviewed |
| 5 | Documented law | `process_law.LAW` (`process_law.py:25-33`): dims, x_period, neighbour 1/5, grid 6, sigma 5/4, L 32; `softmax_enclosure` (:97); V check (:226-227) → UNAVAILABLE (:240) | w0 | tier 0: rebind neighbour (exact (1 − p)/4) and sigma, **and, where rational logits do not terminate in Decimal (e.g. σ = 1.5, σ = 3, several refinement widths), the independently reviewed enclosure of §8 that bounds the rational-to-Decimal logit conversion error and returns BOUNDED (RC-3; disabling the trap alone is insufficient)**; tier 1: a merged-column enclosure; tier 2: dims, period, grid shape |
| 6 | Exact features | `error_bound.exact_features` 12-gon table (`error_bound.py:146-173`) | period 12 | tier 2 (W = 8: √2/2 values; W = 16: cos π/8 = √(2+√2)/2, with a re-proved envelope) |
| 7 | Float features | `oracle_profile.PERIOD = 12` (`oracle_profile.py:21`), `circle_features` (:40-55) | 12 | tier 2 |
| 8 | Posterior envelope state count | `k4b_cert.S_ENVELOPE = 144` (`k4b_cert.py:24`) | 144 | tier 2 (12W) |
| 9 | Sealed-D-2a predicate | `k4b_data.sealed_d2a_predicate`, `predicate_check` (`k4b_data.py:178-190`); applied at `k4b_driver.py:235`, `k4b_fresh.py:107` | {0..4}^32 on canonical tokens | kept unchanged; stage C uses the HWS canonical label order and re-checks N_C · p_D2a ≤ 0.01 |
| 10 | Registry coverage | `k4b_registry` sources and fail-closed inventory (`PROTOCOL_K4B_v1.md` §3.4) | K4b's sources | every tier: add a token reader (uint8 [n, 32]) that recursively inventories and reads every `hws-store/hist/**/*.npz`, including S0, discovery, S3 and NULLCHK histories, and includes retained histories from superseded attempts; missing or unreadable registered files fail closed (RC-8: histories are nested under `hist/<stage>/`); plus the stage-B store |
| 11 | Process loading and identity | `k4b_data.load_process` → job-0014 `inputs.load_process` (`k4b_data.py:36-71`), which opens process-artifact payloads | E4 artifacts | every tier: a process source for w* under the stage-C protocol's own access rules |
| 12 | Numerical certificate | K4b `CERTIFICATE.md`, `k4b_cert.py` | w0 constants | tiers 1–2: track X's list (construction, filtering, features, phase, logarithms, law transport); tier 0 too where the Decimal logit enclosure of row 5 is needed (RC-3: a reviewed enclosure change, not constants only) |
| 13 | Records defect D6 | `k4b_fresh` export of SEALED_OPENED outside STAGE_COMPLETE (jobs/0057 R29, `review.md:53`) | — | every tier: include the opened-validation copy in the completed-stage record |
| 14 | Margin | `k4b_config.MARGIN` (:58) | 1/100 | unchanged (coordinator ruling); bounded above by δ_max |
| 15 | Ladder N | `k4b_config.LADDER` (:41) | 3,072 / 6,144 / 12,288 | set from stage-B variance (rule 3); re-check row 9 |
| 16 | Learner vocabulary (stage B) | model input [BOS, w1..w32] with BOS = V (`contracts/layout.py:22`) | 36 + 1 | tiers 1–2 and V′ ≠ 36: vocabulary V′ + 1 |

The historical K4B-FROZEN-v1 implementation and records stay as they are.

---

## 12. Reuse and footprint (MD-15)

### 12.1 New code: `tools/hws/` (each .py ≤ 400 lines; no edit to any existing file)

| File | Contents | Lines [W] |
|---|---|---|
| `API.md`, `CONTRACT.json`, `TEST_PLAN.md` | Committed first: names, signatures, grid, levels, alias map, thresholds (incl. τ_D2a, z_w, z_null arguments), seeds, n per stage, the S0 references and tolerances, the frozen CPU rates, store layout, report keys | — |
| `hws_worlds.py` | Grid enumeration, keys, tiers, distance; world/transition/emission build via `src`; rectangular centres; anchored alias map; translation and reflection symmetry checks; features 2πx/W; E1–E3 | ≈ 240 |
| `hws_oracle.py` | Sampling; suffix posteriors, m_K, q_K, q_K^A, b_K^x; per-row arrays (D_K via `k4b_scores`, B_K, KL and entropy rows, ‖m32‖, phase); nulls; Pinsker slack; P4 | ≈ 230 |
| `hws_exact.py` | p(w), A_eff, p_D2a (E4), suffix enumeration K ≤ 3, tiny-world full enumeration, Decimal spot check, BayesFilter cross-check, the KC1 rebuild-and-checksum identity check including the serialization envelope of KC1 (d) (JSON reads only) | ≈ 220 |
| `hws_stats.py` | Means, SEs, L1/U1, U_w/L_w, L3; z constants via `statistics.NormalDist`; bootstrap via `c1_means`; E5 bins; the null family | ≈ 150 |
| `hws_select.py` | Eligibility, criteria, classification, ranking, finalists, outcomes, annotations, X1 and S2 rules, pause rule, licence fill | ≈ 250 |
| `hws_driver.py` | Stages S0, S1, X1, S2, S3, NULLCHK, DRY; records; report; `SELECTION.json` | ≈ 340 |
| `hws_meter_bind.py` | Thin main over `k4b_meter_bind.bind`, `make_limiter`, `disk_reason`, `child_env`, `classify_stop` (`k4b_meter_bind.py:30-112`) [V] with the store rebound; `--max-cpu inf --max-wall inf`; single thread. After calling `k4b_meter_bind.bind`, the HWS wrapper explicitly sets `winjob.MEMORY_CAP = 8 * 1024**3` and rebinds `TEMP_ROOT` to the HWS job’s store (RC-9) | ≈ 90 |

About 1.5k lines of Python [W]. There is no `hws_numerics.py` (MD-3, MD-15). Tests (about 1.2k lines) in `tests/hws/` by two independent authors who never read `tools/hws/*.py`:
- **Author A:** identities on the tiny world by exact Fractions, Proposition F, the Pinsker inequality, bounds and z constants, ranks, every classification and outcome branch.
- **Author B:** builders, rectangular-grid and feature equality, alias map and symmetry checks, p_D2a against brute force, streams and keys, KC1 on a synthetic artifact store, records, meter binding, basetemp outside the project root.

No formatter is run over `tests/hws` (project lesson). `AUTHORSHIP.md` records what each author read. After the accepted implementation, `.venv/Scripts/python.exe tools/build_code_index.py` is run and `docs/code_index/` committed in its own `docs(index): …` commit (CLAUDE.md rule).

### 12.2 Reused unchanged (six-field assessment, short)

1. **Existing.**
   - World and process: `build_world`, `WorldConfig`, `TransitionBuilder`, `TransitionConfig`, `OverlapGaussian`, `EmissionConfig`, `Identical`, `Unique` (`emission.py:191-213`), `GridCenters` (`centers.py:47-68`), `point_distances`.
   - Contracts: `payload_checksum` (`contracts/base.py:170`), `make_artifact_id` (`contracts/ids.py:73`), `Artifact.to_payload` (`contracts/base.py:125`).
   - Sampling and seeds: `HMMSampler`, `SequenceLayout`, `SeedTree` (`contracts/ids.py:99`).
   - Oracle: `oracle_profile.{suffix_posterior, posterior_means, canonical_emission, validate_process, circle_features}`; `oracle.BayesFilter` (`_filter.py:30`); `context_gain` semantics.
   - Scoring: `k4b_scores.{oracle_phase, m4_phase, sha_phase, phase_scores, vector_phase}`, so D4 is K4b's own definition; `scores.{unit_vectors, scores, r4_norms, sha256_phase}` (`scores.py:65-100`). All are period-agnostic [V].
   - Numerics: `error_bound.reference_moments`, `MOMENT_TOL_EXACT`; `process_law.process_law_bound`.
   - Statistics and records: `c1_means.{bootstrap_means, rank_for, tree_mean}` (`c1_means.py:15-60`); `stage_records.{write_new, save_npz, record_gate, sha256}`.
   - Meter: the job-0014 meter through the K4b binding functions.
2. **Missing.** The grid and keys, the rectangular centres, the anchored alias map and symmetry checks, the multi-K predictive and KL arrays, G4^A, P4, p_D2a, the exact suffix enumeration, the payload-free identity check, the selection rule, the stage driver and the report.
3. **Smallest change.** A new `tools/hws/` that imports frozen modules unchanged. The only mirrored code is the 4-line softmax of `_overlap_core` (private, and it needs non-registry centres); it is tested bitwise against the original at W = 12. No `src` edit; no `CENTER_REGISTRY` entry.
4. **Invariants.** Stationary restart at the suffix boundary; w33 and states never stored; one bootstrap index stream per world; stages never share streams; the rules frozen before S0; every evaluated world reported; no payload opened.
5. **Regression checks.** Preflight runs the unchanged `tests/{world, process, dataset, oracle, oracle_profile, circle_history, k4b}` plus `tests/hws`, and `tools/check_file_sizes.py`.
6. **Next extension, not built.** If T1 or T2 is selected: a `src` aliased-overlap emission mode and a rectangular `CenterStrategy`, each a separate reviewed change (§15 Q2).

### 12.3 Store, registry hygiene and preconditions

- **Store:** `X:/Downloads/projects/topo-pilot/hws-store/` (verified absent at writing): `FREEZE.json`, `stages/<S>/`, `GATES.jsonl`, `STAGES.jsonl`, `worlds/<key>.json` (aggregates), `hist/<stage>/<key>.npz`, `SELECTION.json`, `superseded/`, `logs/`, `cpu_ledger.json`.
- **Histories are kept (nested under `hist/<stage>/`; reader specification in §11 row 10, RC-8) as uint8 [n, 32] canonical tokens** (w1..w32 only), about 60 MB in total [W], so any later exposure registry can cover them with a plain token reader (the K4b/C2 fail-closed inventory rule).
- **Dry-run scratch** outside the project tree: `X:/Downloads/topo-scratch/hws-dry/` (verified absent), and pytest basetemps outside it too (the K4b registry trap).
- **Precondition before S0 (R-HWS-7).** S0 draws w0 (E4-process) histories. Before S0 the coordinator records, with the concurrent round `coord-c2-necessity-decoy-20261026`, that no other study holds a live history-generation reservation or a frozen registry awaiting a fresh draw that would not include `hws-store` (the K4B-FROZEN-v1 §3.5 W3 rule), and that any later study drawing E4-process histories lists `hws-store` in its registry. This is a scheduling step, not a review blocker.

---

## 13. Synthetic dry run (addendum 25 rule 4; before the final execution freeze)

The dry run is implementation and synthetic-only work under the separate J1 AUTH (§0.1, RC-4); it authorizes no S0 or sweep sampling. The full pipeline runs end to end with the real driver, records, report and selection code, in the scratch store of §12.3, on synthetic worlds only. Expected answers are known exactly, so nothing about a real sweep world is revealed. Synthetic decision fixtures may supply planted row values directly; they are labelled as fixtures, not findings. Any defect is fixed before the freeze, never after data; the dry run may not tune any threshold or range.

| # | Case | Expected |
|---|---|---|
| DR1 | Tiny cylinder W = 6, H = 2, three centres (0.5 + 2i, 0.5), σ = 1, p = 0.5, L = 8 (`SequenceLayout(n_obs=9, context=8, analysis_position=8)`; the sampler reads only `n_obs`, `sampler.py:69-80`) [V]. All 3^8 = 6,561 histories enumerated with exact probabilities: exact D_K, B_K, V_K, G_K, G4^A, I_Z and I^x for K ∈ {1, 2, 4} against L = 8; a broken-symmetry positive case | MC on 20,000 rows within 4·SE of exact for every quantity; I1–I4, Proposition F and row-wise Pinsker hold exactly on the enumeration |
| DR2 | U and N emissions on the tiny world | every beyond-K quantity 0 (≤ 1e-12) |
| DR3 | Unanchored periodic alias (translation-symmetric) | rejected by E3; when forced through a test-only flag, m_K ≡ 0 and D_K = 0 (≤ 1e-12) |
| DR4 | Anchored maps: the (12, 3) map and the tiny-world reflection-symmetric map | rejected by E3 as reflection-symmetric; the (12, 2) map accepted; group sizes, V′ and labels as in §4.3; deterministic |
| DR5 | Rectangular grid at W = 12 | equals `OverlapGaussian`/`GridCenters` E bitwise; `circle_features` equality; `posterior_means` equality |
| DR6 | p_D2a | the masked recursion equals brute-force enumeration on the tiny world (with labels 0..4 replaced by the tiny alphabet's analogue) to 1e-15; a planted world just above τ_D2a is rejected, one at τ_D2a passes |
| DR7 | KC1 on a synthetic artifact store (meta.json, extra.json, a manifest with metadata-file checksums; `payload.npz` absent or unreadable), including the serialization envelope of KC1 (d): emission config additions `replicate` and `world_scope_master`, `world_scope/`-prefixed seed-map entries, empty world and transition seed maps, parent lists `[]` and `[world_id]`, complete status, artifact type/id (RC-2) | identity passes without touching the payload; a tampered extra, config, envelope field, seed map, metadata-file checksum or manifest checksum fails; the test proves no `payload.npz` is opened |
| DR8 | Formula bridge | HWS D4 rows equal `k4b_scores.phase_scores(oracle_phase(m32), m32, m4)` exactly on deterministic histories at W = 12 |
| DR9 | Planted tables fed to `hws_select` | every outcome branch (SELECTED/T0, T1, T2; BELOW_3X with absence shown / not shown; NO_WORLD_CONFIRMED; NO_SUITABLE_WORLD/HEADROOM and /FILTER; INCONCLUSIVE/RESOURCE_OR_AUTHORITY; FAIL_TECHNICAL); equality exactly at 0.03, 0.10, g4*, g4A* and τ_D2a passes; NaN gives FAIL_TECHNICAL; every class of §5.4 and every tie-break level; the R-HWS-1 slot rule (a MARGINAL world never fills an ordinary slot); the fallback-only 2× set (it can produce BELOW_3X but never SELECTED or a fallback-list entry, RC-1); NO_WORLD_CONFIRMED needs an unresolved world that passes E1–E6 and has U_w satisfying C1–C4, and HEADROOM with no eligible evaluated world becomes FILTER (RC-7); the X1 trigger fires only on its condition, with exact-tie breaking by ascending world key and skipping when no eligible world exists (RC-6); the S2 edge set and cap; the annotations of §7.3; a paused search never receives NO_SUITABLE_WORLD |
| DR10 | Null rule | a planted exceedance that does not reproduce is reported and the run continues; one that reproduces halts with FAIL_TECHNICAL/NULL |
| DR11 | Alignment traps | a transposed T, a wrong symbol map, a prefix instead of a suffix, an inherited suffix belief and a trailing transition are each detected by a test |
| DR12 | Records, budget and resume | exclusive-create refusals; stage records and hash manifest; the licence text filled from synthetic numbers; meter binding with `--max-cpu inf --max-wall inf` and child TEMP on X:, and the effective child settings verified (memory cap 8 GiB, `TEMP_ROOT` in the HWS store; RC-9); both 3× triggers at a world boundary and at a stage boundary; one `HMMSampler.sample(n, rng)` call per world-look; the resume rule: an interrupted stage resumes at a world boundary, regenerates the interrupted world from its original stream, and reproduces identical streams, rows, ledger and decisions (RC-5) |
| DR13 | Tier-0 law-enclosure traps (RC-3) | at σ = 1.5 (logit −1/9 at squared distance 1/2) and at a refinement width, the report-only wrapper records `UNAVAILABLE/NONTERMINATING_LOGIT` and eligibility, ranking and selection are unchanged; other exceptions are technical failures; the reviewed enclosure, when present, returns BOUNDED for those cases |

The dry run is synthetic-only; its report is committed, bound to the implementation hash, and is a precondition of the final execution freeze (RC-4).

---

## 14. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| A more ambiguous world is harder to learn | Stage B fails | Confidence-then-minimal-departure ranking; C3 and C4 forcing floors; fallback list by owner decision; stage B before stage C |
| Slow-walk worlds make beyond-four information order-free averaging | A stage-C SUPPORT would show "earlier symbols matter", not path integration | P4 reported; the reading stated in the hand-off; §15 Q3 |
| Winner's curse from screening up to 292 worlds | A finalist's D4 is overstated | Fresh S3 rows; α = 0.05/16; ranking after the class uses no D̂4 |
| Wasted finalist slots | Qualifying worlds left unconfirmed | CONFIDENT first; MARGINAL worlds cannot fill ordinary finalist slots (R-HWS-1); NO_WORLD_CONFIRMED instead of a false absence claim |
| Desk heuristics are wrong | Grid ranges miss the 3× region | Full factorial; one frozen extension X1; registered BELOW_3X and no-world outcomes |
| Reflection- or translation-symmetric alias maps | Phase confined to a line or erased | Exact E3 check before sampling; three cells excluded (OPEN-1, closed) |
| E2 under aliasing | The registered 0.5/V′ rule would exclude anchored labels at (16, 3) by construction (anchor mass ≈ 1/48 against a threshold of 1/48 [W]) | OPEN-4 ruling: threshold scaled by the number of centres merged into a symbol (§5.1 E2) |
| Lumpy belief phase at W = 8 | E5's 12 bins may exclude sharp W = 8 worlds | OPEN-3 ruling: 12 bins kept at every W (§2.5); stage C's C0-val would apply the same 12 bins to a chart |
| KC1 checksum drift (artifacts produced by `84152ab27e91+dirty`) | S0 FAIL_TECHNICAL although the process is right | Field-by-field extra diff reported; stop and review; a payload read needs its own AUTH (§3) |
| Spurious null stops over about 2,163 null checks | A false study halt | Bonferroni z_null ≈ 4.58 and a fresh-row re-check (R-HWS-3) |
| K4b tool hard-wiring | Stage-C rework | Tiers, tier-0 preference, §11 table, the Z_bound check for tier-0 finalists |
| Registry hazards (sealed-D-2a predicate; a new history store) | A stage-C or other study's registry INCOMPLETE | Exact p_D2a ≤ 5e-7; tokens persisted in a readable store; the R-HWS-7 scheduling step |
| The circle may not form in representations of new worlds | Stage C cannot measure | E5 is necessary, not sufficient; B4 |
| CPU forecast off by 3× | Overrun | Measure-only meter; per-stage and cumulative 3× pauses |

---

## 15. Owner questions (each with a registered default)

Procedural and binding matters were decided by the coordinator (§17). These are the science and risk questions:

1. **What "reuse K4b unchanged" means for stage C.** Keep the K4b measurement and chart method unchanged, with a versioned, reviewed binding of the world-specific constants (§11). **Default: yes; prefer a tier-0 world.**
2. **New observation code for stage A.** Approve the anchored circular aliasing and the spacing-2 centres inside `tools/hws` for stage A. If only a tier-1 or tier-2 world qualifies, stop and ask before stage B. **Default: approve for stage A; stop and ask before stage B if the winner needs new code.**
3. **Slow, nearly order-free worlds.** Does beyond-four information that is mostly an average of earlier symbols (high stay probability) answer "does the circle come from long history"? **Default: yes, with the path-dependence index P4 reported and the reading stated in the hand-off.**
4. **The meaning of "learnable enough".** Context gain ≥ 0.10 nat; beyond-four gain at least the current world's and at least twice its recorded regret; circular-symbol beyond-four gain at least the current world's. **Default: yes.**
5. **Confirmed ≥2× without ordinary selection (BELOW_3X).** Accept the best world at ≥ 2× (the owner's own oracle floor) or extend the search. **Default: ask at that point; nothing is chosen automatically.**
6. **Execution authorisation (RC-4; two steps).** (a) After design review acceptance: a separate AUTH for J1 implementation, tests and synthetic-only dry runs (about 0.15 h implementation; it authorizes no S0 or sweep sampling). (b) After the final execution freeze (coordinator acceptance of DR1–DR13 and a committed report bound to the implementation hash): AUTH for S0–S3 with the staged plan, its forecast (about 1.5–1.8 CPU-h central) and the two 3× pause triggers. **Default: request (a) and (b) at those points.**

Decided by the coordinator, not the owner: the margin stays 0.01; whether X1 runs (frozen rule); W = 24 and σ = 0.75 stay out; aliasing crosses all circumferences (R-HWS-4).

---

## 16. OPEN items (all closed by coordinator rulings)

- **OPEN-1. Reflection-symmetric alias cells. CLOSED.** The anchored map is exactly reflection-symmetric at (8, 2), (8, 3) and (12, 3) (§4.3), which confines the belief phase to two values. **Ruling:** exclude the three mirror-symmetric cells; apply E3 as written; record the 75 worlds as INELIGIBLE/SYMMETRY; no substitute map (aliasing is then sampled at (12, 2), (16, 2), (16, 3)). The counts in §4.4, §5.3, §6.2 and §9 stand unchanged.
- **OPEN-2. Granularity of the 3× pause. CLOSED.** **Ruling:** check both triggers at every world boundary and pause there (stricter, never later than a stage boundary; §9.3).
- **OPEN-3. E5 phase bins at W ≠ 12. CLOSED.** **Ruling:** keep 12 bins for every W, because stage C's C0-val would apply the same 12 bins to a learned chart; report the bin profile (§2.5).
- **OPEN-4. E2 under anchored aliasing. CLOSED.** The registered rule min p(w) ≥ 0.5/V′ assumed equal-mass symbols; anchored labels hold one centre while merged labels hold several, so the rule would exclude (16, 3) by construction [W]. **Ruling:** scale the symbols-alive threshold by the number of centres merged into a symbol: p(v) ≥ 0.5·|v|/V (identical to the registered rule at q = 1; §5.1 E2).

---

## 17. Provenance

| Element | Source |
|---|---|
| Base text, structure, notation, identities I1–I4, Proposition F, KC table, factor levels for p and σ, W ∈ {8, 12, 16}, spacing-2 centres, portability tiers, stages S0/S1/X1/S2/S3 and their sizes, frozen X1 and S2 rules, outcome structure and 2× band, E5 legibility, P4, A_eff, seed pattern, footprint `tools/hws/`, store and registry hygiene, desk heuristic | track L (MD-4, MD-5, MD-7, MD-9, MD-10, MD-15, MD-17) |
| D4 as the single gate; information measures report-only | both tracks (MD-1) |
| I^x_4, entropy-difference cross-checks, Pinsker note | track X (MD-1) |
| Anchored circular-only alias map; unanchored map as negative control | track X, generalised by the comparison's rule (MD-6, R-HWS-4) |
| G4^A and criterion C4 | track X; floor = S0 value (MD-7, R-HWS-3) |
| R2, p_weak, p_gain report-only | track X (MD-7) |
| Confidence-first finalist ordering; σ counted as a departure | track X + track L (MD-8, R-HWS-1) |
| NO_WORLD_CONFIRMED; paused search never earns the no-world licence; below-margin annotations | track X (MD-10, R-HWS-1) |
| Nominal screening and fresh-row S3 decision; widened exclusion bound | track L, repaired by the comparison (MD-2) |
| No stage-A certificate; certificate list moved to stage C | track L; track X's list relocated (MD-3) |
| KC1 by rebuild and recorded fingerprints, no payload | track X's principle, ruling R-HWS-2 |
| Null family Bonferroni with fresh re-check | comparison + R-HWS-3 |
| Exact p_D2a filter | comparison (MD-12); threshold by the writer (R-HWS-3) |
| K4b binding table with decoder and model-count rows | track L + track X (MD-13) |
| Hand-off union, δ_max, stage-B list, fallback by owner decision | both tracks (MD-14) |
| Forecast on the 2.87 s reference; per-stage and cumulative 3× triggers | track L corrected; track X's triggers (MD-16, R-HWS-6) |
| Separate synthetic/discovery/confirmation streams | track X (MD-17) |
| Reservation coordination before S0 | R-HWS-7 |
| Reflection-symmetry filter; τ_D2a value; z_w with the four criteria and S3 looks; z_null value; KC1 details (meta/extra JSON, artifact-id recomputation, the never-call list); X1 counts for the new grid; forecast recomputation; OPEN-1..4 | the writer [W] |

---

## 18. Changes from track L

1. **KC1 rewritten (R-HWS-2):** no `inputs.load_process`; rebuild from the recorded config and compare `make_artifact_id`, the seed map and `payload_checksum(rebuilt arrays, stored extra.json)` with the JSON manifest and `meta.json`. `verify_input_hashes` (which hashes history payloads) is also never called.
2. **Aliasing replaced (MD-6):** track L's balanced random labelling over all centres (a ∈ {1, 2, 3, 4}) is replaced by track X's anchored circular-only map, q ∈ {1, 2, 3}, crossed with every W (R-HWS-4). Canonical order v = 6g + b frozen.
3. **Symmetry check generalised:** x-reflections added to track L's x-translation check; three (W, q) cells are reflection-symmetric and excluded (OPEN-1).
4. **Grid size:** 225 grid worlds, ≤ 150 sampled (was 300 / 275). The (W = 8, a = 4) exclusion is gone.
5. **E4 replaced (MD-12, R-HWS-6):** the V′ ≥ 8 argument from i.i.d. (5/V′)^32 is replaced by the exact p_D2a recursion with τ_D2a = 5e-7, justified by the 18,432-row stage-C maximum.
6. **E2 under aliasing flagged** (OPEN-4).
7. **New criterion C4** on G4^A with floor g4A* frozen at S0; S0 freezes both floors.
8. **Gains use KL rows (R-HWS-5);** entropy differences are cross-checks; KC13 added.
9. **Cross-check set extended (MD-1):** I^x_4, the row-wise Pinsker count, R2, p_weak, p_gain (report only).
10. **Widened exclusion bound (MD-2):** z_w = z_{1−0.05/(4·308)} ≈ 3.94 decides exclusion and candidacy (track L's candidacy used U1 = x̂ + 2.326·SE). The comparison's "z_{1−0.05/N_eval}, about 3.9 for 300 worlds" was inconsistent (that formula gives ≈ 3.59); the writer's form includes the four criteria and gives ≈ 3.94.
11. **Null gate (MD-11, R-HWS-3):** ±4·SE per world replaced by a study-wide Bonferroni z_null ≈ 4.58 over 2,163 checks, with a fresh-row re-check; halt only if it reproduces.
12. **Finalists (MD-8, R-HWS-1):** classes CONFIDENT / POSSIBLE / MARGINAL; confidence first; MARGINAL worlds (D̂4 < 0.03) cannot fill a slot; σ counted as a departure.
13. **Selection** is the first S3 qualifier in the frozen finalist order (track L re-ranked with L3).
14. **Outcomes (MD-10):** HWS_NO_WORLD_CONFIRMED added; INCONCLUSIVE/RESOURCE became RESOURCE_OR_AUTHORITY and includes an uncontinued 3× pause; NO_SUITABLE_WORLD needs every evaluated world excluded under U_w and every scheduled stage complete; its licence wording narrowed to the frozen criteria at the stated levels; BELOW_3X states whether 3× absence is shown; track X's below-margin annotations added.
15. **Forecast corrected (MD-16, R-HWS-6):** reference is job 0014's 2.87 s profile, not the 56.75 s job total; recomputed for the new grid (1.50 h / 1.78 h central for S0–S3, J1 separate).
16. **Two 3× triggers (MD-16):** per stage and cumulative, checked at world and stage boundaries (OPEN-2), with threshold tables.
17. **X1 count** recomputed: ≤ 102 worlds (was ≤ 187); S2 midpoints for X1 levels added.
18. **Numerics (MD-3):** unchanged in substance; the stage-C certificate list from track X recorded in §11 row 12.
19. **K4b binding table (MD-13):** decoder width (`k4b_decoder.py:25-30, 57`), model-count multiplicity (`c1_means.py:63`, `k4b_config.py:51-61`), registry coverage, process loading, learner vocabulary and ladder rows added; row 9 now uses p_D2a.
20. **Hand-off (MD-14):** δ_max = L3(D4)/3; canonical label order, alias map, G4^A, p_D2a and the full search record added; stage-B checks B3 (circular regret) and B9 (registry) added; fallback only by owner decision and never automatic.
21. **Seeds (MD-17):** alias seeds removed (map is deterministic); NULLCHK stream added; separate stream families stated; no stream extension.
22. **Footprint:** `hws_exact.py` gains p_D2a and KC1; no numerics module; code-index regeneration step added; `docs/RESEARCH_SUMMARY.md` is no longer cited (the 0.10 floor is cited from `PREREGISTRATION.md:205`).
23. **Reservation step (R-HWS-7)** before S0, coordinated with `coord-c2-necessity-decoy-20261026`.
24. **Dry run extended:** DR3 (unanchored control), DR4 (reflection), DR6 (p_D2a), DR7 (payload-free KC1), DR8 (formula bridge), DR10 (null re-check), DR11 (alignment traps), DR12 (both pause triggers, resume).
25. **Owner questions** replaced by the six of the merge; the margin, X1, W = 24 and σ = 0.75 moved to coordinator decisions; OPEN-1..4 added.
26. **Citations corrected:** `lattice.py:173-178`, `sampler.py:33-80`, `oracle_profile.py:141-149`, `k4b_meter_bind.py:30-112`, K4B-FROZEN-v1 "§9 item 6".

---

## Appendix A. Desk heuristic used to set the ranges [W] (not a prediction, not a gate)

Model x as a Gaussian random walk with per-step variance s² = (1 − p)/2, observed once per step with noise τ² ≈ σ² + 1/3 (spacing-2 centres). Kalman posterior variances follow: P∞ is the steady state and P4 the value after four observations from a flat prior; D = P4 − P∞. With angular scale α = (2π/W)² and concentration ρ ≈ exp(−αP∞/2) (capped at the lattice value 0.946), the concentration-gain and phase-correction terms are each about ρ·α·D/2, so D4 ≈ ρ·α·D. Scaled by 0.70 to match w0's 0.00854 (raw 0.0122):

| World (others at w0) | P∞ | D | D4 heuristic |
|---|---|---|---|
| w0 (p 0.2, σ 1.25, W 12) | 0.694 | 0.049 | 0.0085 (anchor) |
| p 0.75 | 0.429 | 0.146 | ≈ 0.026 |
| p 0.875 | 0.315 | 0.212 | ≈ 0.039 |
| p 0.9375 | 0.229 | 0.273 | ≈ 0.050 |
| σ 1.5 | 0.836 | 0.095 | ≈ 0.016 |
| σ 2.0 | 1.131 | 0.259 | ≈ 0.043 |
| W 8 | 0.694 | 0.049 | ≈ 0.017 |
| W 16 | 0.694 | 0.049 | ≈ 0.005 |

At σ ≥ 2.5 the approximation breaks down (wide posteriors, wrap-around, discreteness), and it says nothing about aliasing. The table only justifies the ranges: the 3× region plausibly lies inside the tier-0 plane, the circumference has a modest effect, and aliasing is the open lever.

---

## 19. Change log v1 → v2

Each entry lists the sections changed and the text inserted or replaced. RC texts are the reviewer's exact fixes (`coord-hws-review-20261026.codex.md`), applied verbatim where given; the OPEN items follow the coordinator rulings. Unchanged sections are not listed. One consistency adaptation: the reviewer's "DR1–DR12" reads "DR1–DR13" here because RC-3 adds DR13.

**RC-1 (§5.4, §5.6, §7.1, §7.2, §13 DR9).**
- §5.6 items 1–4 replaced: item 1 "Ordinary finalists ... MARGINAL worlds cannot fill ordinary finalist slots"; item 2 gains "If no CONFIDENT or POSSIBLE candidate exists, the 2× set receives fallback-only confirmation. These worlds cannot produce HWS_SELECTED or enter its fallback list. They may produce HWS_BELOW_3X under §7.1."; item 3: ordinary finalists qualify, fallback-only worlds are evaluated for BELOW_3X only; item 4 and closing sentence restrict the selection clauses to ordinary finalists. The v1 sentence "They can at most support BELOW_3X" was replaced.
- §5.4 note: "can never fill a finalist slot" became "an ordinary finalist slot ... only in the fallback-only 2× set".
- §7.1: SELECTED row "≥ 1 ordinary-finalist qualifier ... Fallback-only worlds never produce this outcome"; BELOW_3X row "no ordinary finalist qualified for selection, and ≥ 1 S3 world (ordinary finalist or fallback-only) passes ...".
- §7.2 BELOW_3X licence: "but no finalist confirmed the 3× target." replaced by "No ordinary finalist qualified for selection. Any fallback-only world whose L3(D4) also reaches 0.03 is explicitly reported; no upper bound below 0.03 is implied."
- §13 DR9: fallback-only 2× set case added.

**RC-2 (§3 KC1, §12.1, §13 DR7).**
- §3 KC1 (a) now compares `meta.config` and `meta.seed_map` with the expected values of new item (d); new item (d) "Serialization envelope (RC-2)" inserted with the reviewer's text: "Reconstruct the serialization envelope without calling any stage or store loader. For emission seed s, expected config is `asdict(emission_cfg)` plus `replicate=s` and `world_scope_master=0`. ... Require complete status, expected artifact type/id, and the metadata-file SHA256 recorded in the pinned manifest before comparing config, seed map and rebuilt content checksum."
- §12.1 `hws_exact.py` row: "including the serialization envelope of KC1 (d)". DR7 rewritten to cover the envelope fields, the metadata-file checksum and their tampering.

**RC-3 (§4.5 tier 0, §8, §11 rows 5 and 12, §13 DR13).**
- §4.5 tier 0 cell: "constants only" replaced by "not always constants only (RC-3): tier 0 may require a reviewed law-enclosure change when rational logits do not terminate in Decimal".
- §8 tier-0 de-risking bullet: reviewer's paragraph inserted ("In stage A, the report-only wrapper catches `decimal.Inexact` ... records `UNAVAILABLE/NONTERMINATING_LOGIT` ... disabling the trap alone is insufficient."), with the σ = 1.5, σ = 3 and refinement-width evidence; the enclosure change is stated to be J1/J2 implementation work (ruling).
- §11 rows 5 and 12: "Needed for" cells extended with the qualification. New DR13 (σ = 1.5 and a refinement width).

**RC-4 (§0.1, §9.4, §13, §15 Q6; status).**
- Status line now "MERGED v2, design freeze candidate (pending confirmation)".
- §0.1: Addendum 27 bullet says "final execution freeze"; new bullet "Authorisation sequence (RC-4)" with the reviewer's text and the five-step order. §9.4 Jobs bullet rewritten to the same sequence. §13 heading "before the final execution freeze", opening sentence on the J1 AUTH, closing sentence "The dry run is synthetic-only; its report is committed, bound to the implementation hash, and is a precondition of the final execution freeze". §15 Q6 split into (a) J1 AUTH and (b) S0–S3 AUTH.

**RC-5 (§4.7, §6.2 item 4, §6.6, §9.2, §13 DR12).**
- §4.7 step 1: "called exactly once per world-look"; step 2: "Chunking is allowed; results must be bitwise independent of chunk size." replaced by "Sampling, filtering and numerical aggregation use the frozen whole-world call shapes; variable numerical chunking is disabled in HWS-v1."
- §6.2 item 4: "scheduling and chunk size" became "scheduling only". §6.6: chunking bullet replaced by the reviewer's text ("For each world-look, call `HMMSampler.sample(n, rng)` exactly once. ... Resume occurs at world boundaries and regenerates an interrupted world from its original stream."). §9.2 RAM bullet: "chunking allowed" removed. DR12 resume rule rewritten.

**RC-6 (§6.2).** X1 trigger: appended "For X1, choose the largest-D̂4 eligible world, breaking exact ties by ascending world key; if none exists, skip X1." S2: "p midpoints by dwell ..." replaced by "The p-edge refinement values are explicitly frozen as 0.375, 2/3, 5/6, 11/12, and 23/24 for the extension edge; use these values rather than computing dwell midpoints." DR9 extended.

**RC-7 (§7.1, §13 DR9).** NO_WORLD_CONFIRMED condition replaced by "no earlier outcome applies and at least one unresolved world remains. An unresolved world passes E1–E6 on its latest look and has U_w satisfying C1–C4." HEADROOM clause added: "HEADROOM additionally requires at least one eligible evaluated world; otherwise use FILTER."

**RC-8 (§11 row 10, §12.3).** Reader specification replaced by: recursively inventory and read every `hws-store/hist/**/*.npz`, including S0, discovery, S3 and NULLCHK histories, and retained histories from superseded attempts; missing or unreadable registered files fail closed. §12.3 histories bullet cross-refers.

**RC-9 (§9.2, §12.1, §13 DR12).** Inserted "After calling `k4b_meter_bind.bind`, the HWS wrapper explicitly sets `winjob.MEMORY_CAP = 8 * 1024**3` and rebinds `TEMP_ROOT` to the HWS job’s store. DR12 verifies the effective child settings." in §9.2 and the §12.1 `hws_meter_bind.py` row; DR12 verifies the effective settings.

**OPEN-1 (§4.3 Finding, §14, §16).** "Default: ... **OPEN-1** asks whether to substitute ..." replaced by "These three cells are recorded as ineligible (INELIGIBLE/SYMMETRY) and not sampled; no substitute reflection-breaking map is used (coordinator ruling OPEN-1, closed)." §14 marker "(OPEN-1, closed)"; §16 item closed.

**OPEN-2 (§9.3, §16).** "(see **OPEN-2** on the granularity)" replaced by "The pause is checked at every world boundary (coordinator ruling OPEN-2, closed)." §16 item closed.

**OPEN-3 (§2.5, §14, §16).** "(See OPEN-3 on the 12 bins at W ≠ 12.)" replaced by "The 12 phase bins are kept at every W, including W ≠ 12 (coordinator ruling OPEN-3, closed); the bin profile is reported." §14 and §16 updated.

**OPEN-4 (§5.1 E2, §14, §16).** "see **OPEN-4** (default: the anchor-aware form ...)" replaced by "the threshold is scaled by the number of centres merged into a symbol: p(v) ≥ 0.5·|v|/V ... (coordinator ruling OPEN-4, closed)". §14 and §16 updated.

**Not changed by design:** §17 Provenance and §18 "Changes from track L" keep their v1 wording (history of v1 against track L); the numeric forecasts, thresholds and counts are unchanged because no ruling altered them.

## 20. Confirmation and design freeze candidate (coordinator 243a611b, 2026-10-26)

- Codex confirmation round on v2 (`coord-hws-review-20261026.v2confirm.codex.md`): **CONFIRM_AFTER_MINOR_FIXES**; RC-1..RC-9 applied; both writer adaptations correct.
- NEW-1 and NEW-2 applied verbatim by the coordinator (§14 "Wasted finalist slots", §15 Q5 heading, §7.1 NO_SUITABLE_WORLD row). No other change from v2.
- This document is the **HWS design freeze candidate (HWS-DESIGN-v1)**. The final execution freeze binds the implementation hash and the accepted DR1–DR13 dry-run report, after a separate owner AUTH for J1 (implementation, tests, synthetic-only dry runs). S0–S3 need a later owner AUTH.
