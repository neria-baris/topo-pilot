STATUS: DESIGN FREEZE (coordinator 9c3d4140, 2026-11-03; reviews coord-hws-gen-review-20261103 and .v3confirm; owner addendum 45)

# HWSG-DESIGN-v1: generality across worlds, the full beyond-four test repeated in three more worlds

**Merged plan** of planning round coord-hws-gen-20261103 (track L Claude, track X Codex; merge note `coord-hws-gen-20261103.MERGE.md`). Request sha256 88dfbbcdf021d0fe7027562b460905bbd7ed696c6370e7d51939587a982d46e6 (both tracks verified). Base topo-pilot main 764b5af. Planning only.

**Labels.** **[V]** checked against code or a record (file:line or JSON key). **[H]** an inherited record value. **[W]** desk arithmetic or reasoning. **[R]** a constant registered by this plan; it becomes a gate value only when written into `tools/hwsg/CONTRACT.json` at design freeze, and every gate reads it from there. No [W] or [H] value is a gate; where a gate needs an earlier record value, the run re-reads it from the hashed record.

Paths: `tp/` = `X:/Downloads/projects/topo-pilot/topo-pilot`; `ah/` = `X:/Downloads/projects/topo-pilot/agent-handoff`; `root/` = `X:/Downloads/projects/topo-pilot`; `scratch/` = `X:/Downloads/topo-scratch`.

---

## Summary
Stage C found SUPPORT in 3/3 new models in w\* = W12-q1-s1.75-p0.2 (Δ4_orc ≈ 0.047, capture 0.89–0.93) [H, `ah/jobs/0196/review.md`]. HWSG repeats stage C **unchanged** (E4 recipe, K4b estimand, certificate, ladder, decision rule, M = 1/100, α = 0.05/3 per world) in **three new worlds** chosen by a rule fixed here from stage-A oracle quantities only: the lowest, highest and geometric-middle Δ4_orc lower bound among stage-A finalists whose emission logits terminate in Decimal, so the law bound is exact and already recorded by stage A. The rule gives **W12-q1-s1.25-p5/6** (L3 0.0362), **W12-q1-s2.0-p0.2** (0.0864) and **W12-q1-s2.5-p0.5** (0.2324), a 6.4× span around w\* (0.0457) [V/W, §3]. (Owner question Q1: default three; alternative the two stage-A fallback worlds, which are lo and mid.)

Three new models per world train side by side, one thread each; nine models. No separate pilot: its roles move to an oracle-only first stage **O** (fail-fast) and to the stage-C gates inside E1. Registries are built once for all worlds per phase and also cover `hwsc-store`, `hwsu-store`, `hwsd-store` and their scratch.

**Estimands.** Primary: the per-world stage-C outcome. Secondary: the per-model capture ratio ρ = E X− / Δ4_orc on the same test rows with joint-bootstrap bounds. **Cross-world:** GENERAL iff every new world is SUPPORT; NOT_GENERAL iff at least one world passed P1 and at least one model in that world has endpoint status EXCLUDE (a MIXED world with no EXCLUDE does not establish NOT_GENERAL); GENERAL_UNAVAILABLE whenever neither GENERAL nor NOT_GENERAL holds. CAPTURE_AT_LEAST_HALF iff every model's ratio lower bound ≥ 1/2 (registered default, owner Q2); "similar fraction" is described, not claimed.

**CPU:** about 42,000 CPU-s (11.7 CPU-h) at k = 1 including expected correction repeats; about 51,000 (14 CPU-h) if every world needs the largest test; about 9–10 h run wall.

---

## 1. The question

### 1.1 Where things stand [H]
- K4b (w0): EXCLUSION; the oracle's own comparator (0.0085) lay below the margin; models reached 83–95 % of it.
- Stage A (`ah/planning/responses/HWS-FROZEN-v1.md`): 16 ordinary finalists, every one with Δ4_orc one-sided lower bound L3 ≥ 3M (`hws-store/stages/FINAL/REPORT.json` keys `finalists.ordinary`, `floors.D4`, `s3`) [V].
- Stage B: two-model pilot in w\*, HWSB_PASS. Stage C: SUPPORT 3/3, lower bounds 0.0395–0.0406, Δ4_orc 0.0473, N = 3,072, k = 1.

### 1.2 What HWSG asks
In worlds whose oracle carries clearly different amounts of beyond-four phase information, do three models trained by the same recipe (a) each carry a chart coordinate whose beyond-four alignment is certified above the margin, and (b) capture at least a stated fraction of, and a similar fraction of, the oracle comparator?

### 1.3 Explanations HWSG separates [W]
| Explanation | Prediction | Reading |
|---|---|---|
| E-gen: training generally yields beyond-four phase in proportion to availability | SUPPORT everywhere; ρ similar | GENERAL + CAPTURE_AT_LEAST_HALF, compatible fractions |
| E-world: w\* is special | a model with endpoint status EXCLUDE in a P1-passed world although Δ4_orc ≥ 3M | NOT_GENERAL with power certificate |
| E-scale: capture varies with Δ4_orc, σ or p | SUPPORT everywhere, ρ differs | GENERAL, fractions not compatible (descriptive) |
| E-learn: recipe fails in a world | L1 fails | INCONCLUSIVE/NOT_LEARNED; GENERAL_UNAVAILABLE |
| E-chart: chart method fails off w\* | C0 fails | INCONCLUSIVE/CHART_UNAVAILABLE |
| E-power: endpoint lacks precision | P1 fails | INCONCLUSIVE/UNDERPOWERED, never EXCLUSION |

[W] σ and p change together across worlds; this is replication across selected environments, not a factorial mechanism study.

---

## 2. The design

### 2.1 Unchanged from stage C and K4b [V]
Everything in `ah/planning/responses/HWSC-DESIGN-v1.md` §2.1:
- the bounded estimand [E X−, E X+] with every row kept (`tools/k4b/k4b_scores.py:68-86`): on supported rows X± = u·r4, on unsupported rows ∓‖r4‖;
- the chart rule and `k4b_config.chart_cfg()` with its equality check (`k4b_config.py:84-97`);
- certificate F± = max(B±_num, 10⁻⁹) + Z_bound (`k4b_cert.py:133-144`);
- 5,000-draw joint bootstrap, ranks 84 / 4,917 / 250 / 125 / 4,875 (`k4b_config.py:52-53`); α = 0.05/3 (`:61`); M = 1/100 (`:58`);
- per-model rule SUPPORT L− − F− > M; EXCLUDE U+ + F+ < M and L− − F− > −M; else UNRESOLVED; world SUPPORT/EXCLUSION only if all three agree, else MIXED/INCONCLUSIVE (`k4b_stats.py:61-89`);
- ladder, sealing, controls, stop rules.

Further unchanged:
- **E4 recipe** (`tools/hwsb/CONTRACT.json` `recipe`, `:109-173`): 4 layers, d_model 128, 4 heads, d_mlp 512, GELU, no dropout, untied; 5,000 steps, batch 128, AdamW 1e-3, warmup 200 + cosine, wd 0.1, clip 1.0; n_train 131,072, n_dev 4,096; context 33; vocab in/out 37/36; checkpoint steps as in the contract; one torch/OMP/MKL thread; CPU device.
- **Site** `resid_post_3`, index 32, BOS 36.
- **Training code** `hwsb_train.train`.
- **Learning gate L1** captured ≥ 0.8, finite, G_C > 1e-6 (`hwsc_gates.l1`, `tools/hwsc/API.md:386`).
- **Sizes:** lgate 4,096; cal 3,072 (512 lowest-ID landmarks, 2,560 decoder rows); val 3,072; test 3,072·k, k ∈ {1, 2, 4} (`k4b_config.py:40-44`).

All chosen worlds are tier 0, W = 12, q = 1 (`tools/hws/hws_worlds.py:109`) [V]: 144 states, V = 36, period 12, decoder width 144, `S_ENVELOPE` 144 unchanged.

### 2.2 What changes, and why
| # | Change | Why |
|---|---|---|
| G1 | Three worlds, each a cohort with its own models, histories, charts, P1, ENDPOINT, outcome | the question |
| G2 | No stage-B pilot; its roles go to stage O (oracle) and E1 gates (§2.6) | stage C used HANDOFF only for identity values, N_C (= first ladder value), model count, forecasts and exclusions [V, HWSC §6.4]; all are oracle-computable or measured |
| G3 | World-parametrised binding `hwsg_bind.world(key)` for every world-specific constant of `hwsb_config`/`hwsc_config` (§2.3) | these hard-code w\* [V] |
| G4 | Stream tags carry the full world key (σ and p) | stage C's tag `("cylinder","overlap","1.75")` lacks p (HWSC §2.4) [V]; worlds sharing σ would share streams [W] |
| G5 | Per-world law bound with exact stage-A σ and neighbour Fractions | §2.3 row 3; §6 O2 |
| G6 | One registry pass per phase for all worlds, extended to hwsc/hwsu/hwsd | cost (D-0192-1) and cross-world disjointness |
| G7 | Three metered training children per world in one TRAIN job | 6 cores; 1,799–1,892 CPU-s per model [H, `ah/HWSC_CPU_LEDGER.json` jobs 0187–0189] |
| G8 | Secondary estimand ρ and cross-world rule (§2.7) | the question |
| G9 | Runaway safeguards replace pause lines (§10.3) | addenda 41–43 |

### 2.3 World-specific parts of reused code [V], and how HWSG supplies them
| Location | Hard-coded for w\* | HWSG supply |
|---|---|---|
| `tools/hwsb/hwsb_config.py:60-67` | KEY, PROCESS, MASTERS, SEEDS, SIGMA, NEIGHBOUR from hwsb CONTRACT `world` | rebound by `hwsg_bind.world(key)`, restored in `finally` |
| `hwsb_config.py:69-71` | `WORLD_CFG`, `TRANS_CFG = TransitionConfig(p_stay=0.2)`, `EMIS_CFG = EmissionConfig("overlap", 36, 1.75, "grid")` | passed explicitly: `hwsb_data.build_process(store, masters, emission_cfg, world_cfg, transition_cfg)` accepts all three (`hwsb_data.py:98-104`); also rebound so no default leaks |
| `hwsb_data.py:115-116` | `proc["sigma"] = Fraction(repr(float(σ)))`, `proc["neighbour"] = (1 − Fraction(repr(float(p))))/4` | **overridden** with stage A's exact Fractions: stage A used `(1 − Fraction(p))/4`, p = Fraction from its CONTRACT levels (`hws_exact.py:226`, `hws_worlds.py:60`). For p = 5/6, repr(float) gives 0.8333333333333334, not 5/6, so the neighbour would not be 1/24 [V/W]. O1 asserts proc σ, neighbour = stage-A values exactly |
| `hwsb_law.py:120` | `law_bound(…, sigma=hc.SIGMA, neighbour=hc.NEIGHBOUR)` defaults | always called with explicit per-world Fractions |
| `tools/hwsc/hwsc_config.py:36-43, 55, 77-78` | STORE, DRY_STORE, STUDY_LEDGER, `HANDOFF_PATH = hwsb-store/HANDOFF.json`, KEY, SIGMA, NEIGHBOUR | rebound to `hwsg-store/worlds/<key>/`, `ah/HWSG_CPU_LEDGER.json`, the stage-O `WORLD_HANDOFF.json` |
| `hwsc_config.load_handoff` (`:115-129`), `hwsc_gates.law_identity` (`:66`) | HANDOFF key set; w\* identity | `hwsg_handoff.load(key)` validates WORLD_HANDOFF with its own key set; adapters for law identity. No HWSB_PASS record is fabricated |
| `hwsc_data.py:86` | process cfg `"sigma": plan.process[2]` | per-world plan carries σ and p |
| `hwsc_gates.py:69,77` | `cc.SIGMA`, `cc.NEIGHBOUR` | rebound |
| `hwsc_known.py:207`, `hwsc_dry2.py:155` | literal `"1.75"`, `Fraction(5,4)`, `Fraction(1,5)` | not reused for new worlds; HWSG known cases live in `tools/hwsg` |
| `hwsc_registry_build.py:17-45` | fixed source tag list without later studies | composition adapter `hwsg_registry` (§6) |
| `hwsb_gates.ladder_pilot` (`hwsb_gates.py:141-186`), `hwsc_gates.py:174-176` | captured stage-C seed defaults | called with explicit `models`, `seeds`, `ladder`; a stale-default trap test (DRG3) |
| KC1 identity references | WorldSpec 21feee1d…, TransitionSpec e4dafc7b… (HWSC §4 KC1) | WorldSpec unchanged (same W12 cylinder) [W, asserted in O1]; TransitionSpec differs for p ≠ 0.2 and is recorded per world |

**Copied-name hazard.** Modules that did `from hwsb_config import SIGMA` keep the old value after rebinding. `hwsg_bind` runs the HWSC audit pattern (`tools/hwsc/hwsc_bind.py` `check_old`, `bound_stage_c`, `audit`; `API.md:78-89`) over every reused module: every global, function default and dataclass field equal to a w\* constant (1.75, 7/4, 1/5, 0.2, "W12-q1-s1.75-p0.2", 6203xx, 6202xx) is rebound or allowlisted with a reason. Never two world bindings in one process; parallel training uses separate processes.

### 2.4 Worlds, models, seeds and scopes
| World | key | σ | p | neighbour (1−p)/4 | Masters | Bootstrap seeds (val_sd, val_b4, endpoint, fresh_b4, val_projection) |
|---|---|---|---|---|---|---|
| lo | W12-q1-s1.25-p0.8333333333333334 | 5/4 | 5/6 | 1/24 | 620611–620613 | 620614–620618 |
| mid | W12-q1-s2.0-p0.2 | 2 | 1/5 | 1/5 | 620621–620623 | 620624–620628 |
| hi | W12-q1-s2.5-p0.5 | 5/2 | 1/2 | 1/8 | 620631–620633 | 620634–620638 |
| CROSS | — | — | — | — | — | 620640 |
| DRY | synthetic | — | — | — | 620901–620909 | 620911–620915 |

- **Seed blocks [V].** A whole-token grep of `tools src tests` at 764b5af found no 6206xx–6209xx. Both tracks' first DRY proposals (629961–629989) collide with `tools/hwsd/CONTRACT.json`, `hwsd_dry*.py`, `tools/hwsu/CONTRACT_OF.json`, so DRY uses 6209xx. Gate KG0 repeats the search over the full tree at run time; a collision is FAIL_TECHNICAL/BINDING (no silent substitution).
- **Scope** `hwsg-v1`. **Run key** `("hwsg-v1", KEY_w, master)`. **Process tag** `PROC_w = ("cylinder", "overlap", σ_str, p_str, KEY_w)`.
- **Streams:** train/dev `SeedTree(m).generator("data", "hwsg-v1", KEY_w, role, m)`; lgate/cal/val/test block b `SeedTree(0).generator("data", "hwsg-v1", KEY_w, role, b)`; sequence IDs `make_sequence_ids(process_code(*PROC_w, f"hwsg-v1/{KEY_w}/{role}/b{b}"), split, n)`. Process-code uniqueness and sequence-ID disjointness are checked explicitly (KG2); scope strings alone do not prove history disjointness.
- **Symbol names and EmissionSpec** per master by the E4 mechanism (`tools/hwsb/CONTRACT.json:91`; `PROTOCOL_HWSC_v1.md:80-87`) with `EmissionConfig("overlap", 36, σ_w, "grid")`.
- **Exclusions:** the 24 stage-B ids (HANDOFF `stage_c_exclusions`) and the 6 stage-C checkpoint ids (names in `hwsc-store/stages/TRAIN/`). No earlier checkpoint enters; run keys differ anyway.

### 2.5 Histories and sizes per world (all new)
| Role | Rows | Use |
|---|---|---|
| train, dev (per master) | 131,072 × 33; 4,096 × 33 | training; enter K-REG1 |
| lgate b0 | 4,096 | L1 only |
| cal b0 | 3,072 | calibration (landmarks, decoder rows, 4 Decimal rows) |
| val b0 | 3,072 | validation (512-row panel, B4-VAL, CERT-VAL, P1) |
| test b0…b(k−1) | 3,072·k | endpoint, drawn only under that world's release B |

- **Ladder rule (per world):** N_w = max(3,072, N_P1,w), N_P1,w the first of {3,072, 6,144, 12,288} passing K4b's rule (K4B §7.2: SD-upper-bound/MDE condition; centred projection at effect 0.02 for SUPPORT and 0 for EXCLUSION; ≥ 4,000/5,000 successes per model and jointly) on world w's validation arrays. No qualifying value → INCONCLUSIVE/UNDERPOWERED before any test draw. Raise-only.
- **Registry-risk check:** (4,096 + 3,072 + 3,072 + N_w)·p_D2a(w) ≤ 1/100 in exact rationals (HWSC §3.4; `API.md:392`).

### 2.6 Stage O: oracle feasibility first (addendum 25), replacing the per-world pilot
One metered oracle-only job; trains nothing; draws no evaluation row. Per world:
- **O0** recompute the selection rule (§3) from the sha256-bound `REPORT.json`; require the registered list.
- **O1** build the process with explicit configs into `hwsg-store/worlds/<key>/artifacts`; override and assert σ, neighbour (§2.3); check T equals the max-degree lazy walk with p_w (`src/topo_pilot/process/transition.py:54`), E_canon equal across masters, `validate_process(…, 1e-12)`; record T/E/π/coords sha256 as the world's identity. Stage A recorded no T/E/π hashes (S3 world-record key list) [V], so the identity anchor is O4.
- **O2** `hwsb_law.law_bound(T, E, π, coords, σ_w, neighbour_w)` → BOUNDED, κ < 1, δ = 0 (terminating logits, §3.2); Z_bound must equal the exact law bound stage A recorded for that world (`hws-store/stages/S3/worlds/<key>.json` `law_bound`) [V, field present]; F_plan = `k4b_cert.F_plan(Z_bound)` ≤ M/10 [R].
- **O3** `hws_exact.p_d2a` and the registry-risk check at N = 12,288.
- **O4** regenerate stage A's S3 oracle sample for the world (HWSB KB5 code) and require its history sha256 = the recorded `hist_sha256` (e.g. `S3/worlds/W12-q1-s1.5-p0.5.json:569`) and the D4, G_C, G4, G4A means within 1e-12 of `s3.<key>`.
- **O5** assert the stage-A S3 record is `at_3x` (L3.D4 ≥ 3M, above the addendum-25 2M floor). No new oracle-feasibility draw: stage A certified it on its own fresh rows.

Writes `WORLD_HANDOFF.json` per world: `{key, sigma, p, neighbour, Z_bound, F_plan, p_D2a, N_C: 3072, model_count: 3, process identities, exclusions}`, hashed into the O STAGE_COMPLETE. **Fail-fast:** a world failing any O gate is dropped before training with its outcome; never replaced.

**Why no pilot [W].** Stage B's pilot (1) measured training cost (now measured five times, world-independent at fixed architecture); (2) checked learnability and chart formation, which stage C repeats as L1 and C0 before any test draw; (3) set N_C, equal to the first ladder value; (4) produced Z_bound, F_plan, p_D2a, which are oracle quantities computed in O. A two-model pilot per world adds six trainings (≈ 11,400 CPU-s) to move the same gates earlier; the residual risk, a world that does not learn, costs one world's training (≈ 5,700 CPU-s) and is reported as NOT_LEARNED. Stage B's effect-dependent capture gate is not reproduced, so small learned alignment is not screened out. (Owner Q3 offers X's first-model-first gate.)

### 2.7 Registered estimands and cross-world rule
**Primary (per world w).** O_w ∈ {SUPPORT, EXCLUSION, MIXED, INCONCLUSIVE(/reason), FAIL_TECHNICAL(/reason)} by the unchanged rule: per model L−_wj = rank 84 and U+_wj = rank 4,917 of the joint bootstrap, F = max(B_num, 10⁻⁹) + Z_bound(w), outcome from `k4b_stats.model_status`/`overall`.

**Secondary (per model): capture ratio.**
- ρ_wj = mean(X−_wj)/mean(D_w) over the N_w test rows, D_w the oracle comparator array (`delta4_orc`, `vector_phase(m32)` scored against r4, `k4b_scores.py:39-64`).
- **Joint resampling is already in the endpoint [V]:** `delta4_orc` is a control (`k4b_fresh.py:37`), in the single ordered bootstrap dict (`:181-196`), resampled by the one `joint_bootstrap` with the endpoint seed (`:244`); indices depend only on seed and n (`c1prime/c1_means.py:37-41`). RESULT stores only point ratios (`k4b_fresh.py:280`). `hwsg_ratio` re-runs `joint_bootstrap(bootstrap_inputs(arrays, controls), seed_endpoint_w)` on the same arrays, recovers identical draws (asserted: L, U equal RESULT bitwise), and forms ρ*_wj = X−* / D* per draw. ρL_wj = rank 84, ρU_wj = rank 4,917; X+ ratio and central intervals are reported.
- Defined only when the world's B4-VAL passed and the D* rank-84 bound > 0; otherwise RATIO_UNRESOLVED. Never clipped; may exceed 1 or be negative (the oracle comparator is not an upper bound for every learned field).

**Cross-world readings** (worlds that reached ENDPOINT; w\* is descriptive context only):
| Reading | Rule [R] |
|---|---|
| **GENERAL** | all three new worlds SUPPORT |
| **NOT_GENERAL** | at least one world passed P1 and at least one model in that world has endpoint status EXCLUDE, whatever the others. A MIXED world with no EXCLUDE does not establish NOT_GENERAL (`k4b_stats.py:79-89` returns MIXED for SUPPORT plus unresolved models) |
| **GENERAL_UNAVAILABLE** | whenever neither GENERAL nor NOT_GENERAL holds (e.g. a world INCONCLUSIVE, FAIL_TECHNICAL, dropped or MIXED without an EXCLUDE model) |
| annotation ALL_EXCLUSION | every world at ENDPOINT is EXCLUSION (≥ 2 worlds) |
| **CAPTURE_AT_LEAST_HALF** (default, Q2) | every ρL_wj ≥ 1/2 [R] over all models of all worlds at ENDPOINT (≥ 2 worlds); the licence names the worlds covered and the unavailable ones |
| **CAPTURE_BELOW_HALF** | some ρU_wj < 1/2 |
| CAPTURE_UNRESOLVED | neither |
| descriptive similarity | world-mean ratios ρ̄_w with paired central intervals; COMMON_FRACTION_COMPATIBLE iff the six-to-nine lower-capture central intervals intersect; spread S = max ρ̄ − min ρ̄ with its rank-4,917 bound over index-paired draws (worlds independent; seed 620640 orders the pairing). Labels only; no claim |

- **Error rates [W].** GENERAL is intersection–union: false-claim rate ≤ the largest per-world rate (≤ 0.10 over three models, as stage C). NOT_GENERAL rests on per-world EXCLUDE claims in P1-passed worlds, three families at ≤ 0.10 each (union ≤ 0.30 nominal); every NOT_GENERAL report states this. Capture readings are nominal bootstrap statements, no family claim. No new simultaneous nine-model region is claimed.
- **Null vs lack of power.** P1 certifies ≥ 4,000/5,000 joint projected power in both SUPPORT and EXCLUSION scenarios before any test draw; otherwise UNDERPOWERED. EXCLUSION means U+ + F < M in a world whose oracle comparator is certified ≥ 3M (O5).
- **Why 1/2 [W].** Stage C's capture was 0.89–0.93 and K4b's 0.83–0.95 [H]; "at least half" is a one-sided claim far from both, fixed before any HWSG data and not tuned (stage C has one world, no spread information). A spread threshold (track L's 1/4) would be an equivalence claim without a power design; it stays descriptive unless the owner chooses otherwise.

### 2.8 Sealing plan (per world, as stage C §2.6)
- Validation means of X±, controls, step-0 arrays, decoder scores, Δ1, Δ2, Δ4_orc, endpoint ratios and every ρ-related validation quantity are sealed by `k4b_stats.write_sealed` (`k4b_stats.py:185-204`) into `worlds/<key>/SEALED_VALIDATION.json` at P1. Exposed: gate status, SD bounds, chosen N, numerical bounds, permitted support diagnostics, identity and registry records.
- Opened only by that world's ENDPOINT; `SEALED_OPENED.json` hashed inside the ENDPOINT STAGE_COMPLETE (D6 fix).
- **Release barrier:** before any E2, every registered world must have either an accepted terminal pre-endpoint outcome or an accepted E1 validation. K-REG2 includes all histories already drawn, including histories from failed worlds. Every world eligible for E2 must have its release B fixed before the first E2. Terminal worlds require no release B and remain in the CROSS report. E2 results cannot shape any release; later E2 jobs have no free parameter (N_w, k, registry, seeds bound in release B).
- Every world stopped before ENDPOINT writes a sha256-bound terminal RESULT.json. CROSS reads the outcomes of all registered worlds from their RESULT.json files and re-derives draws per §2.7 only for endpoint worlds.

---

## 3. World selection

### 3.1 Rule [R] (oracle quantities only)
**Pool:** `REPORT.json` `finalists.ordinary` (16, all at_3x and qualifying) [V], minus w\*, restricted to worlds whose stage-A S3 `law_bound` is an exact bound (not `UNAVAILABLE/NONTERMINATING_LOGIT`), i.e. σ with terminating Decimal logits. Ordering key `s3.<key>.L3.D4`.
- W_lo = argmin L3.D4; W_hi = argmax L3.D4.
- W_mid = argmin over the rest of |ln L3.D4 − ½(ln L3_lo + ln L3_hi)|; ties by stage A's frozen order.
- O0 recomputes this from the hashed REPORT.json and S3 world records and must obtain the registered list.

### 3.2 Inputs and result [V values, W arithmetic]
L3.D4 of the 16 finalists (`FINAL/REPORT.json`), with law status from `hws-store/stages/S3/worlds/<key>.json` `law_bound`:
| key | L3.D4 | exact law |
|---|---|---|
| s1.5-p0.5 | 0.032118 | no |
| **s1.25-p0.8333…** | 0.036222 | yes |
| s1.375-p0.75 | 0.037603 | no |
| s1.25-p0.875 | 0.042658 | yes |
| (w\*) s1.75-p0.2 | 0.045749 | no |
| s1.5-p0.75 | 0.051217 | no |
| s1.25-p0.9375 | 0.057829 | yes |
| s1.5-p0.875 | 0.072283 | no |
| **s2.0-p0.2** | 0.086396 | yes |
| s1.5-p0.9375 | 0.090750 | no |
| s2.0-p0.5 | 0.113304 | yes |
| s2.0-p0.75 | 0.147579 | yes |
| s2.5-p0.2 | 0.179171 | yes |
| s2.0-p0.875 | 0.182021 | yes |
| **s2.5-p0.5** | 0.232354 | yes |
| s3.0-p0.2 | 0.246704 | no |

- Geometric midpoint √(0.036222 × 0.232354) ≈ 0.09174 [W]; s2.0-p0.2 at ln-distance 0.060, runner-up s2.0-p0.5 at 0.211 [W].
- Chosen: lo **s1.25-p5/6**, mid **s2.0-p0.2**, hi **s2.5-p0.5**; span 6.4× in L3.D4, w\* between lo and mid; σ ∈ {5/4, 2, 5/2}, p ∈ {1/5, 1/2, 5/6}.
- The pair lo + mid is exactly stage A's fallback list (`SELECTION.json` `fallback_list`; `REPORT.json:48-49`) [V].

### 3.3 Why this rule [W]
- Extremes plus geometric middle maximise the spread of Δ4_orc on a log-even design; a single contrary world among three can be told from a trend better than among two.
- Restricting to terminating σ means the law bound is the original exact enclosure (δ = 0), already recorded by stage A for these worlds, so no new proof is needed (§4). The unrestricted rule (s1.5-p0.5, s1.5-p0.9375, s3.0-p0.2) spans 7.7× but all three need the rounded enclosure re-argued and reviewed for σ = 3/2 and 3. The price of the restriction is a slightly narrower span; the restricted pool still contains 9 of the 15 eligible worlds.
- Every pool world is oracle-certified ≥ 3M, so a model EXCLUSION would be informative everywhere.
- Disclosure: the rule was written by planners who knew stage C's SUPPORT; it uses no model, stage-B or stage-C quantity.

### 3.4 Noted risks [W]
- **lo** (p = 5/6, lazy walk, σ = 5/4 sharp emissions): smallest Δ4_orc; at about 3.6M the endpoint needs more precision than in w\*, so P1 may require k = 2 or 4.
- **hi** (σ = 5/2, broad emissions): largest Δ4_orc but noisier symbols; L1 is relative to G_C, so the absolute regret tolerance shrinks.
These are the generality risks the study probes; they are reported, not designed away.

---

## 4. Binding to stages A–C
| Item | Source | Binding in HWSG |
|---|---|---|
| World candidates, oracle bounds, law status, `hist_sha256` | stage A `REPORT.json`, `SELECTION.json`, `S3/worlds/<key>.json` (sha256 bound at O0) | O0 selection; O2 law equality; O4 reproduction |
| Law enclosure | `hwsb_law.bound_law`, `softmax_enclosure_rounded` (`hwsb_law.py:72-108`), `ENCLOSURE_PROOF.md` | reused unchanged. **Proof scope [V]:** `ENCLOSURE_PROOF.md:10,18,42` argues σ = 5/4 (terminating, δ = 0, returns objects equal to `process_law.softmax_enclosure`) and σ = 7/4 (δ ≤ u·Q_max, asserted exactly). The chosen σ ∈ {5/4, 2, 5/2} have 2σ² = 25/8, 8, 25/2, denominators of the form 2^a5^b, so q terminates and the δ = 0 argument (`:42`) applies verbatim [W]; O2 asserts δ = 0 and equality with stage A's exact record. **A new non-terminating σ** would need: Q_max computed from max d² (≤ 5.5² + 10.5² = 140.5 on W12), the δ ≤ u·Q_max and 2δ < 1 line restated for it, the 200-digit independent check (`hwsb_law.py:151-169`, slack 1/10¹⁹⁰), and a clean-context review before freeze |
| Training | `hwsb_train.train` | unchanged, under `hwsg_bind.world`, separate processes |
| Measurement | `tools/hwsc` stage functions (E1/E2 gates, `hwsc_gates.p1c`, `hwsc_data.h2c/h2_fresh_c`, `hwsc_outcome`), `k4b_fresh.endpoint` | reused under `hwsg_bind.world`, with `bound_stage_c` nested inside and the world's seeds/masters |
| Registry | `hwsc_registry`, `hwsc_registry_build`, `hwsb_registry.registry_digests`, `k4b_registry.inventory/classify`, C2ND readers | reused through the `hwsg_registry` composition adapter plus readers for hwsc/hwsu/hwsd (§6) |
| Decision | `k4b_stats.model_status`/`overall` | unchanged |

---

## 5. Known-case checks (addendum 25 rule 5), before any real draw
One metered KC job after the execution freeze; stage O follows before any training. Failure → FAIL_TECHNICAL/KNOWN_CASE (all worlds), stop, coordinator review; no tolerance change. References are read at run time. No KC job opens earlier checkpoints or sealed objects.

| # | Check | Reuse | Pass |
|---|---|---|---|
| KG0 | Authority (addenda 25, 26, 37, 43, 44, HWSG FREEZE by sha256); needles `hwsg-v1`, 620611–620640, 620901–620915 absent from every seed map, manifest, execution record (whole-tree, KB0 classification); `hwsg-store` absent or this lineage only; no other `OPERATION_ACTIVE.json` active | `hws_driver.seed_search` + HWSB KB0 | exact |
| KG1 | Binding is a no-op at w\*: under `hwsg_bind.world("W12-q1-s1.75-p0.2")` every rebound constant equals stage C's and `build_process` reproduces stage C's process identities | HWSB KB1 | exact |
| KG2 | Stream separation: first 64 cal draws differ across the three worlds and from stage C; lgate/cal/val sequence-ID sets pairwise disjoint (64 rows each, in memory); σ-only tags would collide on a planted shared-σ pair | new | exact |
| KG3 | E4 recipe 100 steps bitwise (KB2) and one-thread (KB3) | HWSB | as KB2/KB3 |
| KG4 | Parallel = sequential: three one-thread 100-step DRY-master trainings as concurrent metered children equal the same run sequentially, bitwise | new | bitwise |
| KG5 | Law: w0 Z_bound = K4b's recorded value with δ = 0; w\* Z_bound and F_plan = HANDOFF exactly (HWSC KC4); for each chosen world, the δ = 0 path equals stage A's recorded exact `law_bound` (oracle computation in KC on the world process, not a draw) | HWSB KB4 | exact rational |
| KG6 | K4b known cases inside `hwsg_bind.world(hi)` ∘ `bound_stage_c`: Proposition 1 (`tests/k4b/test_a_prop1.py`), Theorem A support trap (`test_a_theorem_a.py`), Lemma N and transport (`test_a_lemma_n.py`, `test_a_transport_bound.py`), decision boundaries incl. equality (`tests/hwsc/test_a_decision.py`), POSITIVE_BELOW_MARGIN cases (`tools/hwsc/API.md:174-175`), bound suite (`tests/hwsc/test_a_k4b_known_bound.py`) | port of HWSC KC8 | all pass |
| KG7 | Ratio: planted X− = c·D gives ρ = c and bounds bracketing c; re-derived draws equal the endpoint's (L, U bitwise) on a seed-sensitive fixture; zero/negative denominator → RATIO_UNRESOLVED; ratio > 1 and negative numerator not clipped | new | exact |
| KG8 | Registry rehearsal: `hwsg_registry.build` of every source (§6) against the real root into `hwsg-store/registry/rehearsal/`; CPU, peak memory and bytes recorded | new + reused | PASS |

Not run (default): a stage-C reproduction on stage-C models (it would open `hwsc-store` checkpoints and sealed objects).

---

## 6. Registry (one pass per phase, all worlds) and fail-closed inventory
**K-REG1**, once, after all TRAIN jobs and before any E1 draw, is the union of:
- **(a)** every source of stage C's K-REG2 (HWSC §3.4 R1–R8) with frozen readers;
- **(b) `hwsc-store`** as READER: the 6 train/dev ObservationSets via `hwsb_registry.registry_digests(hwsc-store, expected=<stage-C TRAIN inventory>)`; lgate/cal/val/test history files by the token reader; `registry/**`, chart and checkpoint artifacts classed non-history by name or type; `SEALED_*.json` and `sealed/` listed by name only; subfolders such as `hwsd-dry-*`, `hwsu-dry-of-*`, `hwsd-run-*` under `stages/` assigned to the hwsu/hwsd readers or the token reader; any unassigned array file → REGISTRY_INCOMPLETE;
- **(c) `hwsu-store` and `hwsd-store`:** each store's latest `REGISTRY_OBLIGATION*.json` (per file `relpath, bytes, sha256, class, reader, basis`) [V, files exist; hwsu `REGISTRY_OBLIGATION_OF.json`, hwsd `REGISTRY_OBLIGATION.json`]. The complete array-file listing must equal the obligation's array-file list (new, missing or resized → INCOMPLETE); metadata files are classified separately; Entries are read through the class-to-reader table bound at N6: (`K4b history table`, `k4b_history_table`) maps to the existing history-table reader, every other accepted history class is enumerated explicitly, and an unknown class or reader fails REGISTRY_INCOMPLETE (the class is not literally `HISTORY`); NON_HISTORY entries are never opened. Obligation entries are compared with the complete array-file inventory, including superseded and scratch arrays; metadata files are classified separately. Contract paths: hwsu base contract is `tools/hwsu/CONTRACT_OF.json` (store and dry/test globs `:147-149`, hwsd globs `:168-170`, real/dry/temp paths `:958-963`, reservations `:717-732`); hwsd `tools/hwsd/CONTRACT.json:450-453` [V, track X]. Track U phase 2 runs first; its final obligation is used; if absent or not final at REG1, HWSG waits (window gate);
- **(d) scratch inventory** (HWSC R6) re-scanned with a refreshed frozen table: every top-level scratch directory since 2026-10-29 (`test_hwsc-*`, `hwsu-dry-*`, `hwsd-dry-*`, `hwsg-dry*`, `test_hwsg-*`) gets a row (READER, or EXCLUSION with reason) in `tools/hwsg/CONTRACT.json`;
- **(e) root inventory:** stage C's table (complete, including U/D worktrees and dry/run/test folders) plus `hwsc-store` (b), `hwsu-store`/`hwsd-store` (c), `hwsg-store` (OWN);
- **(f) HWSG lineage:** 18 train/dev ObservationSets, superseded and interrupted attempts included.

**K-REG2** rebuilt from scratch once every registered world has an accepted terminal pre-endpoint outcome or an accepted E1 validation, in one reservation; includes all histories already drawn (failed worlds included) and adds every world's lgate, cal, val blocks drawn so far.

**Requirements:** every evaluation block disjoint from K-REG1 and from every other block of every world; U_test,w disjoint from K-REG2; sequence IDs disjoint from every frozen union; sealed-D-2a predicate false on every row. Collision → FAIL_TECHNICAL/LINEAGE; predicate hit → INCONCLUSIVE/REGISTRY_INCOMPLETE; no replacement sampling.

**Fail closed [V pattern, K4B lines 252–262]:** an unlisted top-level directory with a history file, identity reference or ObservationSet root; an unreadable history-bearing file; an obligation/listing mismatch; an unresolved reservation; or a wildcard non-history classification → INCONCLUSIVE/REGISTRY_INCOMPLETE for **all** worlds. Inventory and reader versions are bound into the registry certificate and rechecked immediately before each draw; a changed root invalidates the certificate. Registry readers never open `state.pt`, `sealed/`, foreign checkpoints or effect reports.

**Hygiene:** pytest basetemps, TEMP/TMP/TMPDIR under `scratch/test_hwsg-<job>/`, never under the root; registry outputs in `hwsg-store/registry/`, metered separately (§10.3); the full needle search at most once per job, result cached in-job, rerun only when source or inventory changes; marker files by retried atomic replace, written only by the coordinator-side stage driver.

---

## 7. Gates, outcomes and licences

### 7.1 Gates (frozen before any draw or training; thresholds read from CONTRACT)
| # | Stage | Gate | Computation / data | Pass | Tol. | Failure action |
|---|---|---|---|---|---|---|
| S0 | every dispatch | BINDING | protocol sha256 = FREEZE; request sha256; R_ref→H_exec diff only `tools/hwsg/*`, `tests/hwsg/*`, `docs/code_index/*`; reused files' sha256 = freeze table; `k4b_config.MARGIN == 1/100`; chart cfg equal; recipe equal to HWSB and HWSC | all hold | exact | INVALID, do not run |
| PF | J-G1 | PREFLIGHT | HWSC PF suites + `tests/hwsc` + `tests/hwsg`; binding audit; file sizes ≤ 400 lines; TEMP/basetemp under scratch | all pass | — | INVALID |
| KG | KC | KG0–KG8 | §5 | all PASS | §5 | FAIL_TECHNICAL/KNOWN_CASE (all) |
| WIN | before KC, REG1, every draw | WINDOW | no other `OPERATION_ACTIVE.json`; track U real stages finished; no foreign registry awaiting its draw | holds | exact | refuse stage (no outcome) |
| O0 | O | SELECTION | §3 on hashed records | registered list | exact | FAIL_TECHNICAL/BINDING (all) |
| O1 | O per w | PROCESS IDENTITY | §2.6 O1 | all hold | exact / 1e-12 | FAIL_TECHNICAL/IDENTITY (w dropped) |
| O2 | O per w | LAW BOUND | BOUNDED, κ < 1, δ = 0, Z_bound = stage-A exact record, F_plan ≤ 1/1000 [R] | all hold | exact rational | FAIL_TECHNICAL/LAW_BOUND (w dropped) |
| O3 | O per w | D2a RISK | (10,240 + 12,288)·p_D2a ≤ 1/100 | holds | exact | INCONCLUSIVE/REGISTRY_RISK (w dropped) |
| O4 | O per w | ORACLE REPRODUCTION | hist sha256 = stage A; D4, G_C, G4, G4A means | equal; ≤ 1e-12 | 1e-12 | FAIL_TECHNICAL/ORACLE (w dropped) |
| O5 | O per w | HEADROOM | S3 record `at_3x` | true | exact | INCONCLUSIVE/ORACLE_FEASIBILITY (w dropped) |
| T | TRAIN-w | TRAINING | three children; finite loss; all checkpoint steps; TRAIN_RECORD per master; run keys and recipe exact | all hold | — | NONFINITE → FAIL_TECHNICAL/TRAINING (model); runaway → FAIL_TECHNICAL/RESOURCE (§10.4) |
| R1 | REG1 | K-REG1 | §6; coordinator completeness certificate | complete | exact | INCONCLUSIVE/REGISTRY_INCOMPLETE (all) |
| 0–10 | E1-w | stage-C gates unchanged: G0c window, H1 IDENTITY (Z_bound and p_D2a = WORLD_HANDOFF, p_D2a rel. ≤ 1e-12, `API.md:127`), H2 SEPARATION incl. cross-world blocks, **L1 all three**, ORACLE-VAL (Decimal moments ≤ 1e-10), B4-VAL (`lower − 0.01 > max(B_H + Z, 1e-9)`, `c1_bounds.py:93-97`), C0-CAL (one production chart, no retries), C0-VAL (≥ 507/512 support, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30), CERT-VAL (row bound ≤ 1e-4, |X̂| ≤ 4), **P1** with N_C = 3,072 and explicit seeds | HWSC §5 rows 0–10 [V] | as stage C | as stage C | as stage C, world w only |
| R2 | REG2 | every world terminal-accepted or E1-ACCEPTed, K-REG2, release B for each E2-eligible world | each release B binds N_w, k_w, K-REG2 sha256, reservation, session, seeds | all present | exact | no release, no fresh data |
| 12–14 | E2-w | H2-FRESH, T-PRE (bitwise landmark activations), ENDPOINT + ρ bounds | HWSC §5 rows 12–14 + `hwsg_ratio` | as stage C; KG7 identity | ranks checked | as stage C |
| X | CROSS | cross-world rule | §2.7 on the sha256-bound RESULT files of all registered worlds (terminal RESULT for worlds stopped before ENDPOINT; draws re-derived only for endpoint worlds) | — | exact | FAIL_TECHNICAL/NUMERICAL on rank-check failure |

### 7.2 Outcomes per world (precedence order), then the cross-world reading
1. **FAIL_TECHNICAL/<reason>:** KNOWN_CASE (all); IDENTITY, LAW_BOUND, ORACLE (world dropped at O); TRAINING, RESOURCE, LINEAGE, DETERMINISM, NUMERICAL, BINDING, SEALING not resolved under §10.4.
2. **INCONCLUSIVE/RESOURCE_OR_AUTHORITY:** lost process, disk/memory safe-STOP, missing authority.
3. **INCONCLUSIVE/REGISTRY_RISK** (O3), **/ORACLE_FEASIBILITY** (O5), **/REGISTRY_INCOMPLETE** (shared).
4. **INCONCLUSIVE/NOT_LEARNED (k/3).**
5. **INCONCLUSIVE/<K4b reason>:** HEADROOM, CHART_UNAVAILABLE (model, criterion), NUMERICAL, UNDERPOWERED.
6. **SUPPORT / EXCLUSION / MIXED / INCONCLUSIVE(/NUMERICAL)** by the ENDPOINT rule.

**Annotations (never change an outcome):** POSITIVE_BELOW_MARGIN_wj (addendum 25 rule 6): L−_wj − F > 0 with status EXCLUDE ("positive, certified below the margin") or UNRESOLVED ("positive, not resolved against the margin"); world-level when true for all three models and the world is not SUPPORT. NEGATIVE_ALIGNMENT, INIT_UNAVAILABLE, FRESH_B4_LOW (stage C). CROSS adds POSITIVE_EVERYWHERE when every model at ENDPOINT has L− − F > 0, and ALL_EXCLUSION (§2.7). Every per-model and per-world value is published; nothing is selected post hoc.

### 7.3 If a model or a world fails a gate
- The world stops at its failing gate with its outcome; computed values are reported. **Other worlds continue** [R] (owner Q4).
- **No replacement** model, seed, world, recipe, step count, model size or chart method without a new owner decision. Runner-up worlds are not substitutes. No model is omitted to make a three-model result.
- A shared failure (KG, R1, R2) stops all worlds.
- CROSS is computed on what reached ENDPOINT; with fewer than two worlds there, capture readings are UNAVAILABLE.

### 7.4 Licences
- **World SUPPORT:** "In world w, under its documented law, on N_w fresh histories, for each of three newly trained E4-recipe models, the gauged chart phase at resid_post_3 is not a function of the last four observations on its supported rows; it depends on earlier observations, aligned with the oracle belief residual, with a certified lower bound above the margin 0.01."
- **GENERAL:** "This held in each of three new worlds chosen by an oracle-only spanning rule (Δ4_orc lower bounds 0.036 to 0.232), as it did in the stage-C world."
- **World EXCLUSION** (power certified): "In world w, whose oracle comparator is ≥ 3M, the three models' completion-protected beyond-four alignment is certified below the margin." It does not establish zero alignment or absence elsewhere in the representation.
- **NOT_GENERAL** names the world(s) and the EXCLUDE model(s) with the per-world error statement. A MIXED world without an EXCLUDE model is reported as MIXED and supports no NOT_GENERAL claim.
- **CAPTURE_AT_LEAST_HALF:** "Each of the [n] models reaching ENDPOINT in [named worlds] captured at least half of the oracle comparator on the same rows (nominal one-sided bounds). This reading makes no claim about [named unavailable worlds/models]."
- **Similarity sentence (only permitted form):** "The observed capture estimates are [compatible / not compatible] with a common fraction at the reported descriptive precision."
- **POSITIVE_BELOW_MARGIN:** a description, not a SUPPORT claim.

**Does not establish (registered):** K4B §8.4 items 1–10 and HWSC items 11–14 (object names adapted); 15 anything outside the three chosen worlds or the stage-A grid; 16 any functional dependence of capture on Δ4_orc, σ or p; 17 that the recipe is optimal or that other recipes, sizes, sites, lengths behave alike; 18 anything about w0 or the E4 models (K4b stands); 19 causal use of the coordinate (use study); 20 training dynamics; 21 that a world dropped or failing L1/C0 lacks beyond-four information in models; 22 a pooled estimate across worlds or with stage C/w0; 23 a success probability over training seeds; 24 ratio equivalence from overlapping intervals; 25 that the oracle comparator bounds every learned phase field; 26 that the coordinate holds all beyond-four information.

### 7.5 Disclosure in every report
"HWSG follows K4b (EXCLUSION in w0, comparator below the margin), stage A (worlds by oracle criteria), stage B (pilot in w\*) and stage C (SUPPORT 3/3 in w\*). HWSG's worlds were chosen by a rule fixed before any HWSG data, from stage-A oracle records only; the planners knew stage C's result. HWSG's models, histories, charts and decisions are its own. No threshold, margin, chart parameter or recipe setting was changed in response to any earlier result; the capture floor 1/2 was set at planning."

---

## 8. Blindness and data hygiene
- HWSG code and roles never read stage-B `REPORT.json`, `stages/EVAL/`, `CHART_CONSTRUCTIONS_*`, stage-C `SEALED_*.json`, `stages/S4*`, `S5`, `S7`, `S8` arrays, or any hwsu/hwsd report. A path guard in `hwsg_config` raises FAIL_TECHNICAL/BLINDNESS (DRG11), pruning before traversal.
- Stage-C Δ4_orc(w\*) and ratios appear only in the disclosure and as CROSS context; no gate reads them.
- Test authors (two, independent, neither the implementer) get the API and this plan's §2–§7, not stage-C results; the implementer does not edit their assertions.
- Track U and D stores are read (listings and obligations), never written.
- The public research-summary paths are never read by any HWSG role (CLAUDE.md).

---

## 9. Stage order (one metered stage per job)
`J-G1 + DRY` (repeatable) → execution FREEZE → **KC** → **O** → **TRAIN-lo**, **TRAIN-mid**, **TRAIN-hi** (three parallel children each) → **REG1** → **E1-lo**, **E1-mid**, **E1-hi** → coordinator ACCEPT of every world's terminal outcome or E1 → **REG2** (+ release B for each E2-eligible world) → **E2** for each eligible world (lo, mid, hi) → **CROSS** → result review.

TRAIN-w is skipped for a world dropped at O; E1 skipped when its TRAIN failed. Each stage writes `<job>.accepted.json` before the next. Real sampling, registry builds and endpoints are serial; a registry job is never combined with training or tests. Parallel children write only their own model subdirectories and attempt-specific meter records; the coordinator aggregates after all terminate.

---

## 10. Dry run and budget

### 10.1 Synthetic dry run (before execution freeze; `scratch/hwsg-dry*/` only; no real master or stream)
| # | Scope | Pass |
|---|---|---|
| DRG1 | Full pipeline on three tiny synthetic worlds (W = 6 cylinder, L = 32; two share σ with different p): O, three tiny models per world (1 layer, d_model 16, 200 steps, parallel children), REG1 on a synthetic root, E1, ACCEPT, REG2, release B, E2, CROSS (plus DRG14). Geometry-dependent K4b gates the tiny process cannot pass (HWSC dry limitation, `tools/hwsc/API.md:416`) use a planted adapter; the record lists kernels run directly vs inputs planted, and does not call this "whole pipeline PASS" | every record complete; every gate returns a value |
| DRG2 | Real E4 architecture, 20 steps, 3 DRY masters per real world, in memory: shapes, BOS 36, vocab 37/36, run keys | valid; nothing persisted |
| DRG3 | Binding: identity at w\*; every §2.3 constant changes per world; planted copied constants (module global 1.75, default `p_stay=0.2`, dataclass field (620301, 620302, 620303)) caught; stale `ladder_pilot` seed defaults caught; restore after exception; nested bindings refused | as stated |
| DRG4 | Streams: σ-only tags collide on the planted shared-σ pair; key-bearing tags disjoint | exact |
| DRG5 | Endpoint fixtures per world: SUPPORT, EXCLUSION, MIXED, UNRESOLVED/NUMERICAL, POSITIVE_BELOW_MARGIN boundaries | exact |
| DRG6 | Ladder with N_P1 ∈ {3,072, 6,144, 12,288, none} | exact |
| DRG7 | One world NOT_LEARNED, the others continue; CROSS gives GENERAL_UNAVAILABLE; a missing world never becomes EXCLUSION | exact |
| DRG8 | Law: σ = 5/4 δ = 0 equals the original enclosure; σ = 7/4 equals HANDOFF Z_bound; a neighbour from repr(float(5/6)) is refused by O1; F_plan > 1/1000 fixture drops a world | as stated |
| DRG9 | Registry: synthetic hwsu/hwsd-like stores with obligations (matching PASS; extra, missing, resized file INCOMPLETE; accepted history classes read via the bound class-to-reader table, including (`K4b history table`, `k4b_history_table`); unknown class or reader INCOMPLETE; NON_HISTORY never opened, access hook); hwsc-like store with `sealed/` (zero opens); unlisted top-level dir INCOMPLETE; missing phase-2 obligation INCOMPLETE; cross-world collision LINEAGE | as stated |
| DRG10 | Ratio and CROSS: planted ρ for every reading; ρL = 1/2 exactly passes; joint-index identity; RATIO_UNRESOLVED path; RC-1 boundaries: SUPPORT + UNRESOLVED without EXCLUDE → GENERAL_UNAVAILABLE, and a P1-passed MIXED world containing EXCLUDE → NOT_GENERAL | exact |
| DRG11 | Blindness guard on §8 paths | FAIL_TECHNICAL/BLINDNESS |
| DRG12 | Records: exclusive create; superseded archive + bit-identical regeneration; a TRAIN child killed mid-run → that model FAIL_TECHNICAL/RESOURCE, siblings complete, rerun reproduces bitwise; retried atomic marker replace; reservation survives a pre-draw interruption | as stated |
| DRG13 | Meter: per-child caps, aggregate-RAM check before launch, TEMP/basetemp under scratch, one thread per child, `registry/` metered separately (D-0192-1 regression) | as stated |
| DRG14 | Early-failure release path: world A NOT_LEARNED at TRAIN (terminal), world B fails an E1 gate (terminal), world C passes E1; REG2 runs with accepted terminal outcomes for A and B, K-REG2 includes the histories already drawn for A and B, release B exists for C only, C's E2 proceeds, CROSS reports A and B as terminal and gives GENERAL_UNAVAILABLE; a variant with a world neither terminal nor E1-accepted blocks the first E2 | exact |

Every code correction touching the executable binding invalidates the dry acceptance and needs a new accepted run at the corrected hash. Cost ≈ 300–600 CPU-s per dry attempt [W] (stage-C DRY 121–142 [H], ×2–4 for three worlds, children and planted adapters).

### 10.2 Budget (CPU-s)
**Measured basis [H]** (`ah/HWSC_CPU_LEDGER.json`): J-C1 559–1,172 per run, ≈ 6,600 over 10 runs; DRY 121–142 per run (8 runs); KC 305–859 per attempt, 4 attempts ≈ 2,220; TRAIN 1,799.3 / 1,872.4 / 1,891.8; E1 incl. REG1 1,578.2; REG2 269.1 and 313.3; E2 900.1 at k = 1; total 18,586.6 against a planned central ≈ 13,300. Stage B TRAIN 1,964.9 and 2,002.2 (`ah/HWSB_CPU_LEDGER.json`). Stage A S3 578 s (`SELECTION.json` `cpu`). Full needle search 30–35 CPU-min (request).

| Stage | Central | Expected repeats | Expected total | Range |
|---|---|---|---|---|
| J-G1 + DRY | 700 + 400 | ×6 (stage C ran 10 J-C1) | 6,600 | 4,000–10,000 |
| KC (KG4 ≈ 450, KG5 law ≈ 300, KG8 ≈ 600) | 1,500 | ×2 | 3,000 | 1,500–5,000 |
| Extra full seed/inventory searches | 2,100 | ×2 | 4,200 | 2,100–8,400 |
| O (3 worlds: build, law, p_D2a, S3 reproduction) | 900 | ×1.3 | 1,200 | 500–3,000 |
| TRAIN ×3 (3 children × 1,900) | 5,700 / world | ×1 | 17,100 | 16,200–20,000 |
| REG1 | 800 | ×1.5 | 1,200 | 600–2,500 |
| E1 ×3 | 1,400 / world | ×1.2 | 5,000 | 3,600–8,000 |
| REG2 | 600 | ×1.5 | 900 | 400–2,000 |
| E2 ×3 (900·k + ratio ≈ 100) | 1,000 at k = 1 | ×1.1 | 3,300 (k = 1) / 12,200 (k = 4 everywhere) | ×0.6–×2 |
| CROSS | 30 | ×1 | 30 | — |
| **Total** | | | **≈ 42,500 (11.8 CPU-h) at k = 1; ≈ 51,400 (14.3 CPU-h) at k = 4 everywhere** | |

Two-world alternative (Q1): ≈ 33,600 at k = 1. With X's first-model gate (Q3): +≈ 200 CPU-s and two jobs per world; saves ≈ 3,800 only in a world that fails to learn. The forecast does not assume any world fails.

**Wall [W]:** training 3 × 35–45 min (three children, 1.2× contention); evaluation, registries, tests single-threaded ≈ 6–7 h; ≈ 9–10 h of run wall over jobs, plus coordination gaps.

**Memory and disk [W]:** training children capped at 8 GiB each (stage C, `tools/hwsc/CONTRACT.json` `resources.memory_cap_bytes`) [V], expected ≈ 1.5 GiB; three are launched only after an aggregate free-RAM check. KC/REG/E jobs 12 GiB. Disk: hwsg-store ≈ 6 GB (registries ≈ 1.5 GB each ×3, 18 ObservationSets, 9 models' checkpoints); X: floor 30 GB, C: floor 2 GB.

### 10.3 Runaway safeguards (no pause lines; defect protection only)
- **Per-model hold** inherited from stage C: 6,006.6282 CPU-s with its checkpoint-callback projection from step 1,000 (`tools/hwsc/CONTRACT.json` `cpu.per_model_hold_s`, `hold_rule`) [V]. A hold is FAIL_TECHNICAL/RESOURCE for that model, never a scientific failure; the report shows step, CPU and projection only, never dev CE.
- **Meter caps per job [R]:** `--max-cpu` = 5 × the job's central (a TRAIN job: per child the hold above); `--max-wall` = 4 × central wall. A kill → FAIL_TECHNICAL/RESOURCE under §10.4.
- **Output cap:** stage C's 16 GiB whole-directory cap (`resources.output_cap_bytes`; D-0192-1) [V] per world directory; `hwsg-store/registry/` metered separately with its own 20 GiB cap [R]. Before freeze, projected registries, artifacts and an interrupted-attempt allowance are checked to fit.
- **Disk:** safe-STOP at C: < 2 GB or X: < 30 GB; native-operation wall 600 s (`resources`) [V].
- **Ledger:** `ah/HWSG_CPU_LEDGER.json`, one unique label per attempt (HWSB label lesson), each process charged once; children write attempt-specific records and the coordinator appends. Actual CPU is reported to the owner after each stage; no approval step (addendum 43 item 2).

### 10.4 Frozen extension and correction rules
- X-1 no growth on a scientific reading. X-2 the only growth is N_w at P1 (raise-only).
- X-3 technical correction by K4B §11.8: at most two corrections per defect; PASS stages immutable; superseded archive with SHA256SUMS; bit-identical regeneration; owner decision if an outcome-bearing quantity would change. An interrupted TRAIN child reruns from scratch with identical seeds. Unaffected expensive stages are reused only with explicit dependency evidence.
- X-4 no tolerance change after HWSG data. A defect found after unsealing cannot yield a fresh confirmatory rerun under this protocol; the owner decides.

### 10.5 Plain-language forecast for the owner (English; the coordinator translates)
"This study repeats the full test from the last stage in three more simulated worlds, picked only from the earlier sweep's numbers: one where looking further back helps a little, one where it helps a lot, and one in between. We chose worlds whose maths can be checked exactly, so no new proof is needed. In each world we train three new small models with exactly the same recipe, three at a time side by side, about forty minutes per world. Then we run the same measurement on fresh data. Before anything is trained, a short check confirms each world matches the earlier sweep; a world that fails is dropped without training and not replaced. I expect about twelve hours of processor time and roughly nine to ten hours on the clock, spread over a day or two of jobs; it could reach about fourteen processor hours if the data need the largest test size. Most of the uncertainty is the usual repeat of tests after small code fixes; the last stage used about forty percent more than planned for that reason, and this forecast already includes it. These are estimates, not limits; safety cut-offs only stop runaway defects. At the end I will tell you, world by world, whether the models carry information from further back than the last four symbols, and whether each captures at least half of what is available."

---

## 11. Reuse and footprint

### 11.1 New code: `tools/hwsg/` (each `.py` ≤ 400 lines; no existing file edited)
- `hwsg_config.py` (CONTRACT, worlds, seeds, paths, blindness guard); `hwsg_bind.py` (world rebinding, audit); `hwsg_handoff.py`; `hwsg_oracle.py` (stage O, WORLD_HANDOFF); `hwsg_train.py` (parallel-children orchestrator over `hwsb_train.train`); `hwsg_registry.py` (composition adapter, readers b–d, inventory); `hwsg_ratio.py`; `hwsg_cross.py`; `hwsg_known.py` (KG0–KG8); `hwsg_jobs.py`, `hwsg_records.py`, `hwsg_dry*.py`.
- Documents: `API.md`, `CONTRACT.json`, `PROTOCOL_HWSG_v1.md`, `TEST_PLAN.md`.
- Tests `tests/hwsg/`: author A (spec-derived known cases, KG6 port, law, ratio), author B (black-box: binding, streams, registry fixtures, CROSS, marker ordering); neither is the implementer.
- Code index regenerated in its own `docs(index)` commit. No new sampler, oracle filter, chart kernel or statistics engine; each adapter that mirrors existing code says why direct reuse is unsafe and is tested for equivalence on synthetic input.

### 11.2 Six-field reuse assessment
| Part | Existing functions/artifacts | Missing capability | Smallest addition | Stable invariants | Regression checks |
|---|---|---|---|---|---|
| `tools/hws` | world builders, S3 sampler, `hws_exact.p_d2a`, `law_bound_report`, `seed_search` | per-world reproduction and handoff | manifest adapter in `hwsg_oracle` | canonical law; exact Fraction σ, p | O4 hist sha256; KG5 law equality |
| `tools/hwsb` | `hwsb_train`, `build_process`, `hwsb_law`, `hwsb_eval`, `hwsb_registry`, `ladder_pilot`, KB1–KB5 | world arguments; exact neighbour | explicit kwargs + rebinding; σ/neighbour override | E4 recipe; δ check exact | KG1, KG3, KG5, DRG3, DRG8 |
| `tools/hwsc` | binding audit, E1/E2 gates, `p1c`, `h2c`, `hwsc_outcome`, registry build | three-world manifests; later-study sources | HWSG adapters; no HWSC edit | binding restored; lineage exact | KG1, KG6, DRG1, DRG3 |
| `tools/k4b` | estimand, chart, scores, certificate, bootstrap, `k4b_fresh.endpoint` | ratio bounds from the same draws | `hwsg_ratio` re-running `joint_bootstrap` | all rows kept; M, α, ranks unchanged | KG6, KG7 |
| `tools/c2_*` | canonical registry readers, digest sets | obligation-store composition | `hwsg_registry` sources | canonical unions; fail closed | DRG9, KG8 |
| `src/topo_pilot` | world/process, sampler, SeedTree, learner, artifacts | none | reuse unchanged | exact configs | PF suites |
| meter / records | process accounting, exclusive writes | parallel children | attempt-specific ledgers, coordinator aggregation | one charge per process | DRG12, DRG13 |

### 11.3 Footprint
One new module and test folder; new store `root/hwsg-store/` (`FREEZE.json`, `registry/`, `worlds/<key>/{artifacts,stages,reservations,logs,tmp}`, `STAGES.jsonl`, `GATES.jsonl`); scratch `scratch/hwsg-dry*`, `scratch/test_hwsg-*`; ledger `ah/HWSG_CPU_LEDGER.json`. No change to any existing file except through the runtime binding restored in `finally`.

---

## 12. Points settled at merge (code-checked) and remaining implementation notes
- **N1 settled:** the endpoint resamples Δ4_orc jointly with the model arrays (`k4b_fresh.py:37, 181-196, 244`); ratio bounds come from re-derived identical draws (§2.7).
- **N2 settled:** `build_process` accepts `transition_cfg` (`hwsb_data.py:98-104`); its σ/neighbour come from float repr (`:115-116`) and are overridden with stage A's Fractions.
- **N3 settled:** stage A recorded `hist_sha256` and an exact `law_bound` per world, not T/E/π hashes; O4 and O2 anchor identity on those.
- **N4 settled for the default worlds:** terminating σ, δ = 0 path (`ENCLOSURE_PROOF.md:42`). Open only if the owner picks a non-terminating world.
- **N5 settled:** 6206xx/6209xx free at 764b5af; re-checked at KG0.
- **N6 (replaced in v3):** Before design freeze, bind an explicit class-to-reader table from the permitted obligation JSON. Map (`K4b history table`, `k4b_history_table`) to the existing history-table reader. Enumerate every additional accepted history class explicitly; unknown classes or readers fail REGISTRY_INCOMPLETE. Compare obligation entries with the complete array-file inventory, including superseded and scratch arrays; separately classify metadata files. NON_HISTORY entries are never opened. Freeze the complete root and scratch directory tables, including U/D worktrees and dry/run/test folders.
- **Open N7:** confirm the exact key of the `delta4_orc` entry in the bootstrap dict (one-sided `delta4_orc:all` or two-sided pair) and use its lower-side array as D.
- **Open N8:** confirm `hws_exact.law_bound_report` output fields map to `hwsb_law.law_bound`'s Z_bound for the O2/KG5 equality (same quantity, possibly different field name).

---

## 13. Risks
| # | Risk | Effect | Mitigation / default |
|---|---|---|---|
| R1 | lo world (Δ4_orc ≈ 3.6M) needs a large test | k = 4, more CPU | budgeted; P1 decides before any draw |
| R2 | hi world (σ = 5/2) or lazy lo world (p = 5/6) not learned / no chart | NOT_LEARNED / CHART_UNAVAILABLE | reported; others continue; no recipe change |
| R3 | neighbour or σ taken from float repr | wrong law bound | O1 override + assert; DRG8 |
| R4 | registry misses hwsu/hwsd outputs | lineage blind spot | obligation reader + listing equality; fail closed |
| R5 | cross-world stream collision | duplicate histories | key-bearing tags; KG2; H2 across worlds |
| R6 | parallel non-determinism or RAM contention | irreproducible or killed | KG4 bitwise; aggregate RAM check; per-child caps |
| R7 | post-freeze correction loops | CPU, calendar | ×6 test/dry repeats budgeted; positive paths exercised in DRG1 |
| R8 | output cap on a store holding registries | job killed | registry metered separately |
| R9 | track U phase 2 overruns | HWSG cannot start KC/REG1 | window gate; wait |
| R10 | small mean(D) makes ρ unstable | wide bounds | all worlds D ≥ 3M; RATIO_UNRESOLVED path |
| R11 | multiplicity across worlds | over-read NOT_GENERAL | per-world error statement |
| R12 | folded pilot judged insufficient by the reviewer | redesign | return design before freeze; never add models during execution |

---

## 14. Owner questions (science and risk; each with a registered default)
1. **How many worlds, and which?** Default: **three**, lowest/middle/highest among worlds with an exact law bound (s1.25-p5/6, s2.0-p0.2, s2.5-p0.5). Reason: widest spread checkable without new maths. Alternatives: (a) the two stage-A fallback worlds only (lo, mid; saves ≈ 8,900 CPU-s); (b) the unrestricted three (s1.5-p0.5, s1.5-p0.9375, s3.0-p0.2; wider span, needs a reviewed proof extension for two new σ).
2. **Capture ratio: registered threshold or description?** Default: **register "at least half captured" for every model; describe similarity only.** Reason: the floor is a one-sided claim the bounds support; "similar" needs an equivalence margin and power design no one has fixed. Alternatives: also register a spread ≤ 1/4 (track L); or fully descriptive (track X).
3. **Learnability check before training the other two models?** Default: **no; all three train together, the learning gate runs before any measurement.** Reason: saves about 40 minutes per world and two jobs; a check first saves CPU only if a world fails to learn. Alternative: train the first model alone, gate it, then the other two.
4. **If one world fails before its endpoint, do the others continue?** Default: **yes**; the cross-world reading becomes "unavailable", never "not general".

---

## 15. Provenance
- Request sha256 88dfbbcd…82d46e6 (tracks L and X); base 764b5af.
- Sources: track L plan (`coord-hws-gen-20261103.claude.md`), track X plan (`coord-hws-gen-20261103.codex.md`), merge note.
- Merge checks (read-only grep/sed, no Python): `tools/hwsb/hwsb_config.py:55-80`, `hwsb_data.py:98-130`, `ENCLOSURE_PROOF.md` σ lines, `tools/hws/hws_exact.py:215-232`, `hws_worlds.py:50-70`, `tools/hws/CONTRACT.json` p levels, `src/topo_pilot/process/transition.py` p_stay lines, `tools/k4b/k4b_stats.py:25-60`, `k4b_fresh.py:37, 181-300`, `tools/c1prime/c1_means.py:31-43`, `hwsc_gates.py` def list; `hws-store/stages/FINAL/REPORT.json` (D4 L3 per finalist, `:553-572`), `hws-store/stages/S3/worlds/*.json` (key list, `hist_sha256`, `law_bound` status); whole-token seed grep over `tools src tests`.
- Not read: public-summary paths; U/D round files, reports, jobs 0197–0223; any payload, `hist/**`, sealed or checkpoint file.

## Change log v2 → v3 (design review coord-hws-gen-review-20261103, all four items accepted as written)
- **RC-1 (NOT_GENERAL rule):** Summary (Estimands), §1.3 E-world row, §2.7 cross-world table (NOT_GENERAL, GENERAL_UNAVAILABLE) and error-rate bullet, §7.4 NOT_GENERAL licence. Rule: NOT_GENERAL iff a P1-passed world has a model with endpoint status EXCLUDE; MIXED alone never suffices.
- **RC-2 (release barrier):** §2.8 release barrier, §6 K-REG2, §7.1 gate R2, §9 stage order, DRG1 and new dry fixture DRG14 (early-failure release path).
- **RC-3 (registry reader):** §6(c) and (e), DRG9, §12 N6 replaced by the class-to-reader table rule; class is `K4b history table`, not literal HISTORY.
- **RC-4 (capture licence):** §2.7 CAPTURE_AT_LEAST_HALF row and §7.4 capture licence now name covered and unavailable worlds/models.

## Change log HWSG-v3 → HWSG-DESIGN-v1 (confirmation review coord-hws-gen-review-20261103.v3confirm: CONFIRM_AFTER_MINOR_FIXES)
- §6(c): the array-file listing is compared with the obligation's array-file list; metadata classified separately.
- §2.8 and §7.1 X: every world stopped before ENDPOINT writes a sha256-bound terminal RESULT; CROSS reads all registered worlds' outcomes and re-derives draws only for endpoint worlds.
- DRG10: explicit RC-1 boundary fixtures; change log RC-2 now names DRG14.
- Owner questions: all four defaults accepted (owner addendum 45).
