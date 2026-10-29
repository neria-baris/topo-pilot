STATUS: HWSC-v2, track L plan (planning only; RC-1..RC-13 and S1–S3 applied; pending the reviewer's confirmation read).

# HWSC-v2: the world-sweep stage C, the full beyond-four test with three new models in w\* = W12-q1-s1.75-p0.2

**Round:** `coord-hws-stage-c-20261029`. Request `agent-handoff/planning/requests/coord-hws-stage-c-20261029.md`, sha256 `4299ce6afe50bd5c6a1363e9b097a858edc72810781fff51d40a2b25e9b7b639` (verified by the writer before reading). **Track:** L only (Codex frozen, addendum 28; PLANNING_PROTOCOL rule 5). **Writer:** clean-context Claude subagent of coordinator 08ad4eaf, 2026-10-29.
**Revision v2.** Applies RC-1..RC-13 of the result-blind review (`coord-hws-stage-c-20261029.claude-reviewer.md`, sha256 59f68390c4c80f08ff8a019935662800dc97b9ae24190b7bfbade7fdeae7d2fc, verified; VERDICT CONFIRM_AFTER_MINOR_FIXES) with the reviewer's replacement or insertion text verbatim, and suggestions S1–S3 as ruled in `coord-hws-stage-c-20261029.rulings.md` (sha256 c705d155635f760097ee735df72ff3b1f0261bcf9bb5d2e6fba7e3e88842b942, verified). v1 is `coord-hws-stage-c-20261029.claude.md` (sha256 e7718bff…3f8e), unchanged. Every change is listed in the final section "Change log v1 → v2". Nothing else was changed.
**Authority:** owner addendum 34 (sha256 `7207564a…3941`, verified): planning, result-blind review, design freeze candidate, implementation with independent tests and a synthetic dry run, up to an execution freeze. **Running stage C (training or any real-scope draw) is not approved by this plan or by addendum 34.**
**Base code:** topo-pilot main `af5e7b48615de5acebfb47fa3e98aa69130c3c3a` (clean apart from untracked `.claude/`, `output/`, `research_audit_export/`, `tmp/`). `.venv/Scripts/python.exe tools/build_code_index.py --check` printed "code index is current" (exit 0) [V].
**Planning only.** The writer ran no training, sampling, tests, drivers or oracle computation and wrote no file except this one. No `payload.npz`, `state.pt`, `sealed/` file, `hist/` array or checkpoint payload was opened or hashed. The only stage-B result input read is `hwsb-store/HANDOFF.json` (§9.1). The files on the request's "Do not read" list were not opened.

**Labels.** **[V]** checked by the writer against code or a record (file:line, or JSON key). **[H]** an inherited record value. **[W]** the writer's desk arithmetic or design reasoning. **No [W] or [H] value is a gate threshold.** Every gated quantity is computed by the run; identity references (HANDOFF values, record hashes) are read by the run at run time and compared exactly.

Paths: `tp/` = `X:/Downloads/projects/topo-pilot/topo-pilot` (main af5e7b4); `ah/` = `X:/Downloads/projects/topo-pilot/agent-handoff`; `root/` = `X:/Downloads/projects/topo-pilot`; `scratch/` = `X:/Downloads/topo-scratch`. Protocols: **K4B** = `ah/planning/responses/K4B-FROZEN-v1.md` (sha256 957f0d5e…b485 [V]); **HWS** = `HWS-FROZEN-v1.md` (d9690609…63a9 [V]); **HWSB** = `HWSB-FROZEN-v1.md` (db0db31a…577e705 [V], equal to HANDOFF `protocol_sha256` [V]).

---

## Summary (≤ 300 words)

**Question.** In the world w\* selected by stage A (12 × 12 cylinder, stay probability 0.2, emission width σ = 1.75), do three **new** transformers trained by the unchanged E4 recipe carry, in the gauged phase of a K4b-rule chart, first-harmonic belief information that the last four symbols do not determine, at the K4b margin 0.01? This is K4b's question asked again where the oracle comparator is ≈ 4.7× the margin [H].

**Design.** K4b's estimand, support completion (Theorem A), bootstrap, F, decision rule and licences, unchanged. New: three masters 620301–620303 trained in w\* (one per metered job, E4 recipe, one thread); scope `hwsc-v1`; fresh learning-gate, calibration, validation and test blocks; test size N = max(N_C from HANDOFF = 3,072, the K4b validation ladder), raise-only; Z_bound(w\*) from the reviewed `hwsb_law` enclosure, required equal to HANDOFF.

**Gates.** S0 binding, preflight, known cases (stage-B KB set reused plus a binding-identity case and a registry rehearsal before training), per-model training completion, G0c, H1-C identity and law bound (Z_bound equal to HANDOFF), REG1, H2 (lgate, cal, val), L1 learning gate (captured ≥ 0.8 in all three), ORACLE-VAL, B4-VAL, C0-cal, C0-val, CERT-VAL, P1, release B with K-REG2, H2-FRESH, T-PRE, ENDPOINT. First non-PASS ends the cohort.

**Outcomes.** SUPPORT, EXCLUSION, MIXED, INCONCLUSIVE/<reason> (including NOT_LEARNED and CHART_UNAVAILABLE, with no replacement seed), FAIL_TECHNICAL; per-model POSITIVE_BELOW_MARGIN annotation (addendum 25 rule 6).

**Cost.** ≈ 13,300 CPU-s (3.7 CPU-h) central at N = 3,072, of which training 6,007 s; ≈ 18,500 s (5.1 h) at N = 12,288 [W from H]; E1/E2 centrals re-set from the measured registry rehearsal before the run approval; 3× pauses per stage and cumulative; a per-model training hold at 6,007 s.

---

## 1. The question

### 1.1 Where things stand
- **K4b** asked whether the learned chart phase of the three E4 models covaries with r4 = m32 − m4 beyond what a suffix-only field can (K4B §1.2–§1.4, lines 104–159) [V]. It ended EXCLUSION in 3/3 models (`ah/jobs/0057`) [H], but its margin M = 0.01 lies above the oracle's own phase-only comparator in that world, 0.00854 (HWS §1, line 68) [H]. So K4b could not separate "the circle carries no beyond-four information" from "there is too little to see".
- **Stage A (HWS)** selected w\* = W12-q1-s1.75-p0.2, HWS_SELECTED/T0: D4 mean 0.04701, L3 0.04575 on 32,768 fresh rows; D4/M = 4.70; δ_max = 0.01525 (`ah/jobs/0136/review.md:5`) [H]. Tier 0: no new observation code; the K4b tool moves by the §11 binding rows (HWS lines 581–604) [V].
- **Stage B (HWSB)** trained two pilot models in w\* and ended **HWSB_PASS** (HANDOFF `outcome`) [V]. Its only input to this plan is `hwsb-store/HANDOFF.json` (§9.1).

### 1.2 What stage C asks
Per K4B §1.1 with the objects replaced: in each of three new E4-recipe models trained in w\* (masters 620301, 620302, 620303; step 5000; `resid_post_3`; position 32), does the gauged phase of a chart built by the LCC ≥ 95 % rule on fresh calibration histories covary with the first-harmonic oracle residual r4 = m32 − m4 on fresh test histories, with the identified-set lower bound above M = 0.01 after the certified margin F?

Stage C is a new study. It is not K4b, not a rescue of K4b and not part of stage B. Its results are never pooled with K4b, K4, C1′, E4 or stage-B results, and it changes no earlier verdict (K4b stays EXCLUSION for the E4 models in w0).

### 1.3 Competing explanations stage C can separate [W]
| Explanation | What discriminates it |
|---|---|
| E1 short-context statistics only | E X− ≤ 0 under P\* for any suffix-only field (K4B Corollary A1, line 155) [V] |
| E2 belief formation over history | Δ4 > 0; ideal comparator 0 ≤ Δ4^orc ≤ B4 (K4B §9 item 6) [V]; D4(w\*) ≈ 0.047 gives room above M [H] |
| E3 chart or architecture artifact | step-0 control charts of the same three runs; m4-phase and SHA-of-suffix nulls (K4B §9) |
| E4 selection through support | ruled out by Theorem A (all completions) |
| E5 numerics or stored law | row certificate, B_num, Z_bound(w\*) via the reviewed enclosure |
| E6 reuse or leakage | fresh histories; K-REG1/K-REG2 covering every store including stage A, stage B and the stage-C training sets |
| E7 learning failure in w\* | the per-model learning gate L1 (new; §5) — a failure is INCONCLUSIVE/NOT_LEARNED, never EXCLUSION |

---

## 2. The design

### 2.1 What is unchanged from K4B-FROZEN-v1
Unchanged, by reuse of the frozen K4b code under the binding of §3: the estimand Δ4 and the bounded estimand [E X−, E X+] (K4B §1.2–§1.4); every row kept, no support conditioning; the chart rule and its code (K4B §4, cfg `k4b_config.chart_cfg()` equal to C1′'s, `k4b_config.py:84-97`) [V]; nine constructions at most (3 production, 3 direct, 3 step-0) with the two ledgers; the row certificate and Lemma N (K4B §5.2–§5.3); B_num, F = max(B_num, 10⁻⁹) + Z_bound and Theorem B′ (K4B §5.4–§5.5, lines 365–394) [V]; tolerances (K4B §5.6); the 5,000-draw joint bootstrap and ranks 84/4,917/250/125/4,875 (`k4b_config.py:51-57`, checked at import, :71-73) [V]; the precision ladder rule (K4B §7.2) and the width diagnostic (§7.6); sealing (K4B §7.5); the per-model and overall decision rule (K4B §8.1–§8.2; `k4b_stats.py:61-89`) [V]; α = 0.05/3 (`k4b_config.py:61`) [V]; the error-rate statement (K4B §8.3); the licence templates and the "does not establish" list (K4B §8.4, adapted only in their object names, §6.2); the controls and descriptive analyses (K4B §9); support reporting (K4B §10); the rerun and lineage rule (K4B §11.8); the stop rules (K4B §13).

### 2.2 What changes, and why (every change is forced by w\* or by "three new models")
| # | Change | Why | K4b binding row (HWS §11) |
|---|---|---|---|
| C1 | Models: three new masters trained in w\* instead of the fixed E4 checkpoints | addendum 33 Q1/Q6 defaults (`OWNER_DECISIONS.addendum-33.md`, items 1 and 6) [V]; HANDOFF `model_count` = 3 [V] | 1 |
| C2 | Seed scope `hwsc-v1`, process tag ("cylinder", "overlap", "1.75"), new bootstrap seeds 620311–620315 | K4b's scope and seeds are issued; the process tag must name σ | 1 |
| C3 | Process source: the w\* process built by the `src` builders into the stage-C store (`hwsb_data.build_process` pattern), not `k4b_data.load_process` (E4 payloads) | E4 artifacts are σ = 1.25; payload reads of other studies are not authorised | 11 |
| C4 | Z_bound(w\*) computed inside `hwsb_law.bound_law(7/4, 1/5)` with the reviewed rounded-logit enclosure | at σ = 7/4 logits do not terminate in Decimal and `process_law_bound` alone fails (HWS §8, line 476; HWSB §4 B8a, line 158) [V] | 5, 12 |
| C5 | A learning gate L1 per model (captured ≥ 0.8, E4's gate) before any chart | K4b's models were fixed E4 objects that had already passed this gate; new models have not | — (new gate; HWS §10.3 B1 pattern, line 563) |
| C6 | Test size N = max(N_C, N_P1) on the K4b ladder, raise-only | HANDOFF N_C = 3,072, k_C = 1 from two pilot models (HWSB §4 refinement 2, line 165, leaves a raise-only stage-C check to this plan) [V] | 15 |
| C7 | Registry: K4b's sources plus every store since K4b (C2, C2ND, X6 stage 0/1, X6ZC, HWS, HWSB, the dry stores) and the stage-C training sets | HWS §11 row 10; HANDOFF `registry_obligation` [V] | 9, 10 |
| C8 | Records defect D6 fixed: the opened-validation copy (`SEALED_OPENED.json`) is written and hashed inside the ENDPOINT stage's STAGE_COMPLETE record | K4b R29 (`ah/jobs/0057/review.md:53`) [V] | 13 |
| C9 | Step-0 control checkpoints: the step-0 checkpoint of each new run | K4B §9 item 3 uses "the step-0 checkpoints of the same runs" | — |
| C10 | Disclosure sentence: replaces K4B §4.5's C1′ disclosure by the K4b/HWS/HWSB lineage disclosure (§6.4) | the inherited context changed | — |

Unchanged rows of the binding table, re-verified for tier 0 [V]: row 2 (BOS 36, alphabet 36: V = 36 at w\*, HWSB API §1.1 `EMIS_CFG`); row 3 (decoder width 144 = 4 × 36, `k4b_decoder.py:57`); row 4 (3 models, α = 0.05/3); row 6 (exact features, period 12); row 7 (`oracle_profile.PERIOD = 12`); row 8 (`k4b_cert.S_ENVELOPE = 144`, `k4b_cert.py:24`; N = 144 at W = 12); row 14 (M = 1/100, `k4b_config.py:58`); row 16 (vocabulary 37).

### 2.3 Models, seeds and training (C1, C2)
| Item | Value | Rationale [W unless marked] |
|---|---|---|
| Masters | **620301, 620302, 620303** | Unissued; the 6203xx block follows HWSB's 6202xx (HWSB §2.2, line 85) [V]. A read-only text search found no whole-token use of 620301–620315 under `tp/tools`, `tp/src` (the only hits are hexadecimal substrings of sha256 values in `tools/c2_readout/c2_config.py:45` and `CONTRACT.json:25`) [V]. G0 repeats this search over the full tree and classifies every hit (K4B §6 row 0 rule) |
| Run key | `("hwsc-v1", "W12-q1-s1.75-p0.2", master)` | new `init/…` and `batch_order/…` streams (the HWSB §2.2 reasoning, line 86) [V] |
| Symbol names | `SeedTree(master).generator("symbol_names", "cylinder", master)` via the unchanged `OverlapGaussian` | E4's mechanism (HWSB §2.2) |
| EmissionSpec | `ProcessStage.run_emission(world_id, EmissionConfig("overlap", 36, 1.75, "grid"), SeedTree(master), store)` | E4 envelope |
| Recipe | E4 recipe exactly as HWSB §2.1 (lines 55–78) [V]: 4 layers, d_model 128, 4 heads, d_mlp 512; 5,000 steps, batch 128, AdamW 1e-3, warmup 200 + cosine, wd 0.1, clip 1.0; n_train 131,072, n_dev 4,096; checkpoints 0, 50, …, 5,000 | addendum 33 Q4: no recipe change |
| Threads | one torch thread, `OMP_NUM_THREADS = MKL_NUM_THREADS = 1` | stage B's KB3 found one-thread training deterministic and within 3e-8 nats of E4 at 100 steps (`ah/jobs/0172/review.md:9`) [H] |
| Training code | `hwsb_train.train` unchanged (Trainer composition and checkpoint callback mirroring `LearnerStage.run`, bitwise-tested in stage B's DRB2) with the hold rule of §8.3 | reuse |
| Training data | per master: train 131,072 × 33 and dev 4,096 × 33 drawn from `SeedTree(m).generator("data", "hwsc-v1", role, KEY, m)`; sequence IDs `make_sequence_ids(process_code("cylinder", "overlap", "1.75", f"hwsc-v1/{role}/{m}"), role, n)`; saved as ObservationSets in `hwsc-store/artifacts` | the HWSB §2.3 pattern with the new scope; see the `hwsb_data.py:176` finding in §3.2 |
| Gate checkpoint | step 5000; step 0 for the initialisation control only | K4B §2.2 |

The 24 stage-B pilot checkpoints (HANDOFF `stage_c_exclusions`, 24 ids [V]) never enter stage C. H1-C (§5) refuses any stage-C checkpoint id in that list, and no stage-C code path takes a checkpoint id from outside `hwsc-store/artifacts`. The pilot models are excluded by run key as well (`hwsb-v1` versus `hwsc-v1`).

### 2.4 Histories, streams, scopes and sizes (all new)
KEY = `"W12-q1-s1.75-p0.2"`, PROC = `("cylinder", "overlap", "1.75")`.

| Role | Rows | Stream | Sequence IDs | Use |
|---|---|---|---|---|
| train, dev (per master) | 131,072 × 33; 4,096 × 33 | §2.3 | §2.3 | training only; enter K-REG1 as an own-lineage source |
| **lgate b0** | 4,096 | `SeedTree(0).generator("data", "hwsc-v1", "lgate", 0, *PROC)` | `make_sequence_ids(process_code(*PROC, "hwsc-v1/lgate/b0"), "test", 4096)` | learning gate L1 only (E4's test size, HWSB §2.5 line 118) [V] |
| **cal b0** | 3,072 | `SeedTree(0).generator("data", "hwsc-v1", "cal", 0, *PROC)` (= `k4b_data.history_generator` under the binding, `k4b_data.py:74-75`) [V] | `process_code(*PROC, "hwsc-v1/cal/b0")`, "test", 3,072 (`k4b_data.py:78-80`) [V] | K4B §3.1 calibration role exactly: 512 lowest IDs = production landmarks; 2,560 decoder rows; 4 Decimal reference rows |
| **val b0** | 3,072 | same pattern, split "val" | same pattern | K4B §3.1 validation role exactly: 512-row direct-comparator panel; B4-VAL, CERT-VAL, P1 on all rows |
| **test b0…b(k−1)** | 3,072·k, k ∈ {1, 2, 4} | same pattern, split "test", block b | same pattern | the single endpoint, drawn only under release B |
| DRY | small | `("data", "hwsc-v1", "DRY", case, …)`, masters 629911–629913 | — | `scratch/hwsc-dry/` only (§7) |

Blocks are fixed 3,072-row streams (K4B §3.1, line 204) [V]; the lgate block is its own stream and never a chart, validation or test row. Every block is drawn by one `HMMSampler.sample` call on the canonical emission, w33 and states dropped at once (`k4b_data.py:83-92`) [V]. Rows ordered by sequence ID; landmark IDs are 20-digit strings (K4B §3.1).

**Sizes and the ladder rule (C6).** Calibration and validation are 3,072 rows each (K4B MD 3). The test size is decided at P1 (§5 gate P1) as **N = max(N_C, N_P1)**, where N_C is HANDOFF `N_C` = 3,072 (`k_C` = 1) [V], read at run time, and N_P1 is the smallest ladder value {3,072, 6,144, 12,288} that passes K4b's rule (K4B §7.2) on the stage-C validation arrays of the three stage-C models. If no ladder value passes, the outcome is INCONCLUSIVE/UNDERPOWERED before any fresh draw (K4b unchanged). The rule can only raise N above the stage-B planning value; it never lowers it below N_C and never uses an endpoint mean (the projection uses centred draws, K4B line 472) [V]. With N_C = 3,072 = the ladder's first value, N = N_P1 in practice [W]; the max() is kept so that a later HANDOFF with a larger N_C would bind.

### 2.5 Checkpoints, site, position and chart configuration (unchanged K4b cfg)
- Site `resid_post_3`, index 32, d_model 128, BOS 36 (`k4b_config.py:37`) [V]; input `[BOS, perm_j[canonical w1..w32]]`; float64 activations via `c1_model.load_model64` and `c1_model.activations` (K4B §2.2, line 192) [V]; logits for L1 only, by the stage-B float32 path (`hwsb_eval.model_predictive`, HWSB API §4) and never mixed with the float64 activations.
- Checkpoints: step 5000 (trained) and step 0 (control) of each master, loaded from `hwsc-store/artifacts` only.
- Chart cfg: `k4b_config.chart_cfg()` unchanged; `check_chart_equality()` must return equal (`k4b_config.py:89-97`) [V]. GIANT ≥ 487/512; C0-val support ≥ 507/512, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30; extension support at resultant ≥ 0.2 and 8th-NN ≤ R (K4B §4.2, lines 299–313) [V]. No chart parameter is tuned on pilot data (§9.2).

### 2.6 Sealing plan
| Object | Sealed by | Opened | Who may open |
|---|---|---|---|
| Validation means of X±, controls, step-0 arrays, decoder scores, Δ1, Δ2, Δ4^orc, the supported contribution, the conditional supported mean and endpoint ratios | `k4b_stats.write_sealed` (the only writer, exclusive create, `k4b_stats.py:185-192`) [V] into `hwsc-store/SEALED_VALIDATION.json` at P1; the validation report is checked by `check_unsealed` (`:195-204`) [V] | after the fresh ENDPOINT record is written | the ENDPOINT stage code; then the coordinator and owner. Writers, test authors and reviewers of later rounds see it only through the final report |
| `SEALED_OPENED.json` (the opened copy) | ENDPOINT stage | — | written and hashed **inside** the ENDPOINT STAGE_COMPLETE record (C8; K4b R29 fix) |
| Stage-B `REPORT.json`, `stages/EVAL/`, `GATES.jsonl`, `CHART_CONSTRUCTIONS_*.json`, `ah/jobs/0175/` | not a stage-C object | never by stage-C code or stage-C roles | coordinator and owner only (HWSB §6.1 RC-6, line 213) [V] |
| Stage-C L1 values (captured, regret) | not sealed (learning, not endpoint) | in the E1 report | coordinator; they do not shape any stage-C threshold |

The validation report contains chart diagnostics, support counts, missing mass and width, B4, SD bounds, projection summaries and certificate bounds, and no endpoint-reconstructing quantity (K4B §7.5, lines 494–500) [V].

---

## 3. The K4b binding for tier 0 (HWS §11 rows 1, 5, 9, 10, 11, 12, 13, 14, 15, 16)

### 3.1 Binding table
| Row | Item | K4b value and place [V] | Stage-C value | Mechanism |
|---|---|---|---|---|
| 1 | Models, scope, process tag, site | `MODELS = (1729, 2718, 3141)`, `SCOPE = "k4b-sf-v1"`, `PROCESS = ("cylinder", "overlap", "1.25")`, site/index/BOS/d_model (`k4b_config.py:36-39`); `SEEDS` 610101–610105 (`:44-50`); `STORE = ROOT/"k4b-store"` (`:34`); `CONTRACT` (`:81`) | `(620301, 620302, 620303)`; `"hwsc-v1"`; `("cylinder", "overlap", "1.75")`; site unchanged; seeds val_sd 620311, val_b4 620312, endpoint 620313, fresh_b4 620314, val_projection 620315; `STORE = root/"hwsc-store"`; `CONTRACT` = `tools/hwsc/CONTRACT.json` (K4b's chart section byte-equal) | the versioned binding `hwsc_bind` (§3.2) |
| 5 | Documented law | `process_law.LAW` sigma 5/4, neighbour 1/5; `softmax_enclosure` traps on inexact division (HWS line 476) | sigma 7/4, neighbour 1/5 (= (1 − 0.2)/4), the reviewed `hwsb_law.softmax_enclosure_rounded` | `hwsb_law.bound_law(7/4, 1/5)` (`tp/tools/hwsb/hwsb_law.py:99`), restoring in `finally`; `hwsb_law.law_bound` (`:120`) for H1-C |
| 9 | Sealed-D-2a predicate | `k4b_data.sealed_d2a_predicate`, `predicate_check` (`k4b_data.py:178-190`) | unchanged, on every stage-C evaluation row (lgate, cal, val, test) before any activation of those rows; plus the exact registry-risk check (§3.4) | reused unchanged |
| 10 | Registry coverage | `k4b_registry` sources (a)–(f), (k) | K4b's sources, every source C2ND covered, plus `c2nd-store`, `hwsb-store`, the dry stores and the stage-C training sets (§3.4) | new `hwsc_registry` composing frozen readers |
| 11 | Process loading and identity | `k4b_data.load_process` → job-0014 `inputs.load_process`, which opens E4 payloads (`k4b_data.py:36-71`) | the w\* process built by `hwsb_data.build_process(store, masters=(620301, 620302, 620303))` into `hwsc-store/artifacts`; WorldSpec 21feee1d8ee5422e and TransitionSpec e4dafc7b9785c172; E_canon, T, π, coords sha256 equal to `hws-store/SELECTION.json` (file sha256 243f7324…f087 [V]) | reused builder; identity in KC1 and H1-C |
| 12 | Numerical certificate | K4b `CERTIFICATE.md`, `k4b_cert.py` | unchanged row bound, Lemma N, B_num and F; the transport term from the reviewed enclosure (`tools/hwsb/ENCLOSURE_PROOF.md`; KB4 PASS, `ah/jobs/0172/review.md:10`) [H]. `k4b_cert.transport_bound` (`k4b_cert.py:158-168`) is called only inside `bound_law` | binding + reused proof |
| 13 | Records defect D6 | `SEALED_OPENED` exported outside STAGE_COMPLETE (`ah/jobs/0057/review.md:53`) | inside the ENDPOINT STAGE_COMPLETE record | replaced by `hwsc_driver.export_c`, which writes `RESULT.json` and `SEALED_OPENED.json` and then makes one `complete_stage(out, "S8", [RESULT.json, SEALED_OPENED.json])` (D6 fix, C8) (`k4b_fresh.export` is not edited) |
| 14 | Margin | `MARGIN = Fraction(1, 100)` (`k4b_config.py:58`) | **unchanged, 1/100** (δ_max = 0.01525 ≥ M [H]; never changed after any data) | not rebound; S0 checks it |
| 15 | Ladder | `LADDER = (3072, 6144, 12288)` (`:41`) | unchanged values; N = max(N_C, N_P1) (§2.4) | `hwsb_gates.ladder_pilot` with the stage-C models and seeds, via `hwsc_gates.p1c` (§3.2), then the max() in `hwsc_gates` |
| 16 | Learner vocabulary | 36 + 1 | unchanged (tier 0) | — |

### 3.2 The versioned binding, and a finding about copied names [V]
The K4b modules read most constants as **copies made at import**, not through `k4b_config` at call time:
- `k4b_data.py:16` `from k4b_config import BLOCK, MODELS, PANEL, PROCESS, SCOPE`;
- `k4b_stats.py:20` `from k4b_config import ALPHA, DRAWS, LADDER, MARGIN, MODELS, RANKS, SEEDS`;
- `k4b_driver.py:28` `from k4b_config import MODELS, SEEDS, …`, and `ARTIFACTS = ROOT/"topo-pilot"/"artifacts"` (`:37`), used by `load_checkpoint` (`:137-142`);
- `k4b_fresh.py:30` `from k4b_config import MODELS, SEEDS`;
- `k4b_decoder.py:12` `from k4b_config import SCOPE` (decoder seed scopes at `:53-57`);
- `k4b_scores.py:144-159` reads `k4b_config.MODELS` at call time; `k4b_release.py:115` reads `k4b_config.SCOPE`; `k4b_meter_bind.py:134` reads `k4b_config.STORE`.

Rebinding `k4b_config.MODELS` alone would leave `k4b_stats`, `k4b_data`, `k4b_driver` and `k4b_fresh` on the E4 seeds: a silent partial binding. Likewise `hwsb_data.sequence_ids` hard-codes the literal `"hwsb-v1"` (`hwsb_data.py:176`) and cannot be rebound, while `hwsb_data._check_role` and `stream_record` read `hc.MASTERS` and `hc.SCOPE` at call time (`:152`, `:163`), and `hwsb_train.train` uses `hc.run_key` (`hwsb_train.py:272`; `hwsb_config.py:189-190`).

**Rule (no edit to any existing file).** All of this is handled in one new module, `tools/hwsc/hwsc_bind.py`, the versioned binding:
1. A frozen **binding table** in `tools/hwsc/CONTRACT.json` lists every (module, name, old value, stage-C value): `k4b_config.{MODELS, SCOPE, PROCESS, SEEDS, STORE, CONTRACT, CONTRACT_PATH, PROTOCOL_PATH}`, `k4b_data.{MODELS, PROCESS, SCOPE}`, `k4b_stats.MODELS`, `k4b_driver.{MODELS, SEEDS, ARTIFACTS}`, `k4b_fresh.{MODELS, SEEDS}`, `k4b_decoder.SCOPE`, `hwsb_config.{SCOPE, MASTERS, DRY_MASTERS}` (hwsb's KEY and PROCESS are already w\*'s). The implementation job completes the table by the audit below; any addition is a contract erratum reviewed before the freeze.

   **Default arguments are not rebound.** `k4b_stats.sd_upper` and `k4b_stats.centered` hold the seeds 610101 and 610105 as definition-time defaults (`k4b_stats.py:92, 110`), and `k4b_stats.ladder` calls them without a seed (`:166, :169`). Hence `k4b_stats.ladder` and `k4b_driver.p1` are never called under stage C. P1 is `hwsc_gates.p1c`, a line-for-line mirror of `k4b_driver.p1` (`k4b_driver.py:346-371`). Its only change is the ladder call `hwsb_gates.ladder_pilot(X−, X+, r4n, F_plan, models=(620301, 620302, 620303), seeds=(620311, 620315), D_bar=D, ladder=(3072, 6144, 12288))` (`hwsb_gates.py:141-183`; bitwise-tested against `k4b_stats.ladder` in HWSB DRB9). `write_sealed`, `check_unsealed` and the validation-report keys are unchanged. Every reused function with a stage-B or K4b default (`hwsb_train.train(plan=)`, `hwsb_driver.running_cpu`/`pause_or_raise(ledger_path=)`, `hwsb_gates.ladder_pilot(models=, seeds=)`) is called with the argument given explicitly.
2. `bound_stage_c()` is a context manager: it asserts that every listed name holds its recorded old value (else FAIL_TECHNICAL/BINDING: code drift), sets the new values, and restores all of them in `finally` (the `hwsb_law.bound_law` pattern).
3. **Binding audit** (in PF, in the dry run and at the start of every stage-C job, inside the binding): scan the module globals **and the `__defaults__` and `__kwdefaults__` of every function and method**, recursing into tuples, lists, dicts, Paths and frozen-dataclass fields (e.g. `hwsb_config.REAL_PLAN`), of every loaded module from `tools/k4b`, `tools/hwsb`, `tools/hws`, `tools/c1prime*`; any value equal to a K4b- or HWSB-only constant (the tuple (1729, 2718, 3141) or that key set; `"k4b-sf-v1"`; `("cylinder", "overlap", "1.25")`; the K4b SEEDS dict or any of 610101–610105; the K4b store or main `artifacts` path; `"hwsb-v1"`; the masters 620201/620202; the HWSB seeds 620212–620214; `hwsb_config.STORE`, `DRY_STORE`, `STUDY_LEDGER`; `k4b_meter_bind.TEMP_ROOT`) that is not on the table's "left unchanged, with reason" list fails (FAIL_TECHNICAL/BINDING).
4. **Functions never called under stage C** (they hard-code a value that cannot be rebound, or open foreign payloads): `hwsb_data.sequence_ids`, `hwsb_data.make_train_dev` (literal `"hwsb-v1"`), `k4b_data.load_process` (E4 payloads), `k4b_driver.h1` (E4 checkpoints; unwrapped `transport_bound`), `k4b_driver.g0` (K4b authority list), `k4b_cert.transport_bound` outside `bound_law`. `hwsc_data` mirrors `make_train_dev` and `sequence_ids` (≈ 40 lines) with the `hwsc-v1` replicate string; the dry run checks that the mirror with `"hwsb-v1"` equals `hwsb_data.make_train_dev` bitwise on a memory store (DRC4).
5. **Identity known case** (KC7, §4): with a binding table whose new values equal the old ones, every bound stage function returns bitwise what the unbound call returns on synthetic inputs; with the stage-C table, `hwsc_gates.p1c`'s ladder result equals `hwsb_gates.ladder_pilot(models=(620301, 620302, 620303), seeds=(620311, 620315))` on synthetic arrays, and the audit lists `k4b_stats.sd_upper`/`centered` defaults as 'left unchanged: never called under stage C' (`ladder_pilot` is already bitwise-tested against `k4b_stats.ladder`, HWSB DRB9, line 252) [V].

### 3.3 What stage C reuses from the K4b driver, and what it replaces
| K4b stage function | Stage C | Reason |
|---|---|---|
| `k4b_driver.g0` | replaced by `hwsc_known.g0c` | different authority files, needles and window evidence |
| `k4b_driver.h1` | replaced by `hwsc_gates.h1c` | stage-C checkpoints and process; Z_bound inside `bound_law`; pilot-exclusion check |
| `oracle_val`, `b4_val`, `c0_cal_stage`, `c0_val_stage`, `cert_val` | reused unchanged under `bound_stage_c()`, called by `hwsc_driver` in K4b's order | the K4b computations exactly |
| `k4b_driver.p1` | replaced by `hwsc_gates.p1c` | default-argument seeds (§3.2) |
| `k4b_fresh.require_release_b`, `sample_test`, `t_pre`, `endpoint` | reused unchanged under the binding | — |
| `k4b_fresh.export` | replaced by `hwsc_driver.export_c`, which writes `RESULT.json` and `SEALED_OPENED.json` and then makes one `complete_stage(out, "S8", [RESULT.json, SEALED_OPENED.json])` (D6 fix, C8) | records only |
| `k4b_driver.reg1`, `k4b_fresh.kreg2_step` | replaced by `hwsc_registry.build("K-REG1" \| "K-REG2", store, extra=…)` | `k4b_registry.build` has only K4b's readers (its `classify` marks every post-K4b store INCOMPLETE); `nd_registry.build` drops `c2nd-store` and checks C2ND's inventory |
| `k4b_driver.h2`, `k4b_fresh.h2_fresh` | replaced by `hwsc_data.h2c`, `h2_fresh_c` | K4b's versions take the registry as an in-memory string set |

**Registry format (fixed now, not an implementation choice).** `hwsc_registry.build` composes, unchanged, `c2_registry.token_sources(root)`, `c2_registry.x6_source(root/"x6-stage1-store", <store>/registry/runs/<version>)`, C2ND's row-2–9 readers (`nd_registry.source_c2`, `source_c2_superseded`, `source_scratch`, `source_parallel(hws-store, "hws")`, `source_parallel(x6zc-store, "x6zc")`) and the new readers R2–R7, with its own inventory adapter over the R8 table. It writes the C2 manifest and digest-file format with the x6 runs (C2 API §16.3, as `nd_registry.build` does), so `c2_registry.Registry.load(hwsc-store, version)` loads it unchanged. `h2c` and `h2_fresh_c` mirror `k4b_driver.h2` and `k4b_fresh.h2_fresh` line for line, with two changes: registry membership is `Registry.contains` (the `c2_registry.separation` pattern, `c2_registry.py:360-389`), and lgate is a third block. `k4b_data.seq_disjoint`, `predicate_check`, `duplicates` and the sealed ranges are reused unchanged. The E1 and E2 meter memory cap is 12 GiB, fixed in the CONTRACT now.

### 3.4 The stage-C exposure registry (row 10) and how it fails closed
**K-REG1** (frozen after the three TRAIN jobs, before any evaluation draw) is the union of:

| # | Source | Reader | Basis |
|---|---|---|---|
| R1 | Everything C2ND's registry covered: K4b sources (a)–(f), (k); the X6 stage-1 registry and arrays; C2's stores, its superseded name scan; C2 and C2ND scratch histories | C2ND's frozen readers (`tp/tools/c2_nd/CONTRACT.json` `registry.sources` rows 1–9, `c2_readers` a–f, k, x6) [V], unchanged | the newest frozen registry before stage C |
| R2 | `c2nd-store`: `hist/HIST_{fit_b0, fit_b1, feas_b0, val_b0, test_b0}.npz` (names [V]); `superseded/` name scan; `decoys/`, `fits/`, `oracle/`, `manifests/` classified as history or non-history from C2ND's API | the C2 digest-column reader pattern (`nd_registry.source_c2`; columns `digest_H, digest_Hp, digest_Hm, digest_HY`, C2ND contract `c2_table_format`) [V] applied to `c2nd-store`; the format of C2ND's own tables is verified from its API.md at implementation; unresolved → REGISTRY_INCOMPLETE. **`sealed/` is never opened**. Every array file under `c2nd-store` outside `sealed/` is assigned. `hist/HIST_*.npz` goes to this reader. `decoys/HEAD_*`, `fits/{DEC,REFIT}_*`, `oracle/ORACLE_*`, `stages/S2/ACT_FIT_*`, `stages/S5/{ACT_TEST,ENDPOINT_NR,ENDPOINT_D,ENDPOINT_NM}_*` and `registry/**` are classed non-history by C2ND API §14 (`tools/c2_nd/API.md:363-366`). `sealed/` is listed by name only and classed non-history by C2ND API line 230 (activation and readout arrays). Any other array file is REGISTRY_INCOMPLETE. **(S3)** The `sequence_id` columns of the C2ND tables are added to the frozen sequence-ID union if C2ND's API confirms the column per table at implementation; otherwise this is recorded as a known gap in the registry record (not a failure) | C2ND was "OWN" in its own inventory (contract `inventory.c2nd-store`) [V], so no frozen reader for it exists |
| R3 | `hws-store`: every `hist/**/*.npz` (uint8 [n, 32] canonical tokens; all stages and superseded) | C2ND reader `hws` (`source_parallel(hws-store, 'hws')`, contract `parallel.hws`) [V], which also reads `scratch/hws-dry/hist/**` (R-0116-3) | HWS §11 row 10; HANDOFF obligation |
| R4 | `hwsb-store`: the 4 ObservationSets (train/dev of 620201, 620202), `hist/{LGATE, CAL, VAL}.npz`, `superseded/**` | `hwsb_registry.registry_digests(store, expected=HANDOFF["store_inventory"])` (`tp/tools/hwsb/hwsb_registry.py:126`) [V]: fail closed on any missing, renamed, extra or unreadable file. Files outside R4's three subtrees are classed without opening. `artifacts/{WorldSpec, TransitionSpec, EmissionSpec, Checkpoint}` go by artifact type. `stages/S4a/CHART_*.npz` are charts. `stages/EVAL/` holds JSON only per the frozen code (`hwsb_stages.py:135-136`) and is neither listed nor opened. Any other array file found by a name-only listing outside `stages/EVAL/` is REGISTRY_INCOMPLETE | HANDOFF `store_inventory` (32 entries) and `registry_obligation` [V] |
| R5 | Dry stores of stages A, B and C: `scratch/hws-dry/**` outside `hist/` (e.g. `DR12/<utc>/superseded/DRY-<utc>/hist/DRY/DR12.npz`, which C2ND's hws reader does not read, `nd_registry.py:224-229`); `scratch/hwsb-dry/`, `scratch/hwsb-dry-0169/`, `scratch/hwsb-dry-0171/`; `scratch/hwsc-dry*/` | A file-level token reader. Non-artifact `.npz` files are read with `allow_pickle=False` (uint8 [n, 32] / `canon32` members digested). ObservationSet payloads are read for tokens only. WorldSpec, TransitionSpec, EmissionSpec and Checkpoint payloads (`payload.npz`, `state.pt`) are classed by the artifact type in their `meta.json` and never opened. `stages/S4a/CHART_*.npz` are classed non-history by name. **Planted fixtures:** the CONTRACT lists every DRB13 planted file (the three `-unreadable/hist/VAL.npz` files, 10 bytes `not an npz`, `hwsb_dry2.py:201-210`) by path, size and sha256. A file that matches is class PLANTED_FIXTURE (no history). Any other unreadable file is REGISTRY_INCOMPLETE. The `-missing` and `-renamed` copies are read file by file. | HANDOFF obligation plus the re-run stores |
| R6 | Every other array file (`*.npz`, `*.npy`, `*.pt`) under `scratch/` outside `test_*` components (≈ 10,100 files in 45 top-level directories on 2026-10-29) | (a) C2ND row 9 unchanged (`HIST_*.npz`; C2-format tables read). (b) A frozen **scratch inventory table** in `tools/hwsc/CONTRACT.json`, built at implementation by a read-only header scan with `k4b_registry.inventory` semantics (history-bearing members by `HISTORY_KEYS`, identity references, ObservationSet roots, unreadable files; `.pt` by name only), and reviewed before the freeze. It has one row per top-level scratch directory, with decision READER (a named reader, e.g. the R5 token reader for copied stores) or EXCLUSION (with the reason, e.g. 'pytest fixtures, every file ≤ 1,024 history rows'). (c) At REG1 and REG2 the scan is repeated. A new directory, or a history-bearing, identity-bearing or unreadable file that its row does not cover, is REGISTRY_INCOMPLETE | generalises C2ND row 9 |
| R7 | Stage-C own lineage: the six ObservationSets (train, dev × 3 masters) in `hwsc-store/artifacts` | `hwsb_registry.registry_digests(hwsc-store, expected=<TRAIN inventory>)` | the trained models saw them; no evaluation row may equal one |
| R8 | Every top-level directory of `root/` | `k4b_registry.inventory` and `classify` (`k4b_registry.py:43, 92`) [V] against a frozen stage-C inventory table extending C2ND's (contract `registry.inventory`, dated 2026-10-26) [V] by `c2nd-store` (READER R2), `hwsb-store` (READER R4) and `hwsc-store` (OWN). The deep scan excludes C2ND's `deep_scan_exclude` list plus `hwsb-store` and `hwsc-store` (`k4b_registry.inventory(root, exclude=…)`). Each excluded store is covered file by file by its reader below. | an unlisted directory holding any history file, identity reference or ObservationSet root is REGISTRY_INCOMPLETE (K4B lines 252–262) [V]. The project-root listing of 2026-10-29 shows exactly one top-level directory not in C2ND's table, `hwsb-store` [V] |

**Fail-closed rules (K4b and C2ND, unchanged).** An unreadable, unlisted or unclassifiable history-bearing source makes the registry INCONCLUSIVE/REGISTRY_INCOMPLETE; handoff JSON is validated before the unchanged handoff reader; NOT_SCANNED needs a recorded inventory reason; foreign `payload.npz` files are read only for ObservationSet tokens by the frozen identity readers, never a checkpoint `state.pt`, never a `sealed/` path. The coordinator certifies completeness in release A.

**K-REG2** is rebuilt from scratch after the coordinator's ACCEPT of the validation report, inside the W2 reservation, and adds the stage-C lgate, cal and val blocks (K4B lines 266–280) [V].

**Requirements (K4B line 268, unchanged).** U_lgate, U_cal, U_val disjoint from K-REG1 and from each other; U_test disjoint from K-REG2; sequence IDs disjoint from every frozen union; every evaluation row fails the sealed-D-2a predicate. A collision is FAIL_TECHNICAL/LINEAGE; a predicate hit is INCONCLUSIVE/REGISTRY_INCOMPLETE; no replacement sampling.

**Registry-risk check (row 9).** The run computes p_D2a(w\*) with `hws_exact.p_d2a` on the stage-C arrays and requires agreement with HANDOFF `p_D2a` = 5.4162868151717785e-15 [V] within 1e-12 relative (the HWSB B9a(iii) rule), then (4,096 + 3,072 + 3,072 + N)·p_D2a ≤ 1/100 in exact rationals for the chosen N. Desk values [W]: 7.2e-11 at N = 3,072, 1.2e-10 at N = 12,288. HANDOFF `registry_value` = 30896816545173375/2⁸⁹ ≈ 4.99e-11 = 9,216·p_D2a [W], the stage-B formula without the lgate block.

---

## 4. Known-case checks (addendum 25 rule 5; stage KC, gating, before any training)

KC runs as its own metered job after the execution freeze and the owner's run approval. Any failure is **FAIL_TECHNICAL/KNOWN_CASE**: stop for coordinator review; no tolerance or reference changes after data (a change needs an owner decision). References are read by the run from the cited records at run time. Stage B's KB functions are reused unchanged (`hwsb_known`, HWSB §3, lines 125–140) [V] wherever the check is the same.

| # | Check | Code | Reference (read at run time) | Pass |
|---|---|---|---|---|
| **KC0 (G0c)** | Authority and freeze: addenda 25, 26, 33, 34 and the owner's stage-C run approval bound by sha256; the stage-C FREEZE; HANDOFF.json sha256 = a4d9a0c9…4353 [V, the writer's hash of the file] and its `freeze_sha256` = the stage-B FREEZE 4b84b320…b3a4 (`ah/jobs/0171/review.md:3`) [V]; `hws-store/SELECTION.json` = 243f7324…f087 [V]. Scopes and seeds: needles `hwsc-v1`, 620301–620303, 620311–620315, 629911–629913 in no earlier seed map, generation manifest or execution record (`hws_driver.seed_search` and the whole-token classification as in HWSB KB0); unresolved hits fail closed; `hwsc-store` absent or holding only this lineage's recorded files; the W3 scheduling record (§9.4) | new `hwsc_known.g0c` over reused search code | records | exact |
| **KC1** | Process identity without payload access: `hwsb_data.build_process(hwsc-store, masters=(620301, 620302, 620303))`; WorldSpec 21feee1d8ee5422e and TransitionSpec e4dafc7b9785c172 with `payload_checksum` equal to E4's `meta.json` values; E_canon, T, π, coords sha256 equal to SELECTION.json; E_canon bitwise identical for the three masters; `validate_process(…, 1e-12)` returns | HWSB KB1 code with the masters argument | E4 `meta.json`; SELECTION.json | exact |
| **KC2** | E4 recipe reproduction, 100 steps at 6 threads, bitwise (with HWSB's pre-registered secondary reading PASS_WITH_NUMERIC_DRIFT) | HWSB KB2, unchanged | E4 metadata, MetricRecords `37657d8490ba9e17` | as HWSB KB2 |
| **KC3** | One-thread setting: \|devCE − E4\| ≤ 1e-3 nats at steps 50 and 100; second one-thread run bitwise equal at step 50 | HWSB KB3, unchanged | E4 dev CE | as HWSB KB3 |
| **KC4** | Law bound: (a) w0 BOUNDED with Z_bound equal to K4b's recorded value and δ = 0; (b) w\* BOUNDED, κ < 1, and the exact Z_bound **equal to HANDOFF `Z_bound`** (87876736540276863476307541/78125·10³³ [V]); (c) `k4b_cert.F_plan(Z_bound)` (`k4b_cert.py:141-144`) [V] **equal to HANDOFF `F_plan`** (exact Fraction) | HWSB KB4 + two exact comparisons | K4b RESULT.json; HANDOFF | exact rational equality |
| **KC5** | Stage-A oracle reproduction at w\*: the S3 means of D4, G_C, G4, G4^A within 1e-12 | HWSB KB5, unchanged (reads the hash-checked S3 w\* table of `hws-store`; the run AUTH must name this read, as HWSB §6.2 RC-16, line 219) [V] | S3 world record | ≤ 1e-12 |
| **KC6** | Learning-gate machinery at w0 (the E4 test split regenerated in memory; G_C equal to the recorded 0.2648737252067266) | HWSB KB6, unchanged | MetricRecords | ≤ 1e-12 |
| **KC7** | **Binding identity** (§3.2 item 5): (a) identity binding → every bound K4b stage function bitwise equal to the unbound call on a synthetic fixture; (b) stage-C binding → binding audit clean; `hwsc_gates.p1c`'s ladder result equals `hwsb_gates.ladder_pilot(models=(620301, 620302, 620303), seeds=(620311, 620315))` on synthetic arrays, and the audit lists `k4b_stats.sd_upper`/`centered` defaults as 'left unchanged: never called under stage C'; `k4b_data.history_generator("cal", 0)` equals `SeedTree(0).generator("data", "hwsc-v1", "cal", 0, "cylinder", "overlap", "1.75")` (first 64 draws); the binding is fully restored after exit | new | — | bitwise / exact |
| **KC8** | K4b's own known cases at the bound constants: Proposition 1 by exact enumeration, Theorem A, Lemma N, decision boundaries and ranks (the cases of K4b's independent tests, K4B §11.4, lines 705–713) [V], re-implemented in `tests/hwsc` and run inside the binding | `tests/hwsc/test_a_k4b_known_bound.py` (author A): Proposition 1 by exact enumeration, Theorem A, Lemma N, the §8.1 decision boundaries and the ranks 84/4,917/250/125/4,875, re-run inside `bound_stage_c()` with the stage-C model keys and seeds. `tests/k4b` runs unbound only, because it hard-codes K4b's models and seeds. | — | all pass |
| **KC9** | Registry rehearsal before any training: `hwsc_registry.build` of R1–R6 and R8 against the real root into `hwsc-store/registry/rehearsal/` (not a K-REG; no stage-C table) | `hwsc_registry` | the frozen inventory tables | status PASS; CPU and peak memory recorded |

**Not run (default):** a K4b E1 reproduction on E4 models (it would open E4 checkpoint payloads and `k4b-store` history arrays, which need an explicit AUTH; HWSB §3 line 140 precedent) [V]; a full 5,000-step E4 reproduction (the S8 rerun reproduced all 12 E4 checkpoints bitwise, HWSB line 138) [H].

**Known cases inside the scientific stages (reported, unchanged from K4b).** ORACLE-VAL's Decimal moment check on every validation row (≤ 1e-10); the m4-phase and SHA-of-suffix population-zero nulls on the test rows; the step-0 control. These are the K4b controls (K4B §9) and stay non-gating except where K4b gates them.

---

## 5. Gates, frozen before any training or draw

**Convention.** Exact quantities are Fractions; strict inequalities as in K4b. The first non-PASS gate ends the cohort; later gates are NOT_RUN (K4B §6, line 417) [V], with the narrow technical-correction rule of K4B §11.8 (§8.4 here). Every gate value computed is reported. Jobs: one metered stage per job (§8.2).

| # | Job | Gate | Computation | Data | Pass reading | Tolerance | On failure |
|---|---|---|---|---|---|---|---|
| S0 | dispatch | BINDING | protocol sha256 = freeze record; request sha256; R_ref → H_exec diff over protected paths only allowlisted `A` entries (protected: `src`, `tools/{k4b, hwsb, hws, c1prime, c1prime_registry, x4_circle_history, x4_oracle_profile, c2_nd, c2_readout, x6_stage1}`, their test directories, `tools/check_file_sizes.py`; allowlist: new `tools/hwsc/*`, `tests/hwsc/*`); every reused file's sha256 = the freeze table; C1′ chart section equal; `k4b_config.MARGIN == 1/100` | git, files | all hold | exact | INVALID: do not run |
| PF | J-C1 (once; its record bound in FREEZE). Each later job's dispatch runs S0 and the binding audit only | PREFLIGHT | unchanged suites `tests/{k4b, hwsb, hws, c1prime, oracle, oracle_profile, circle_history, dataset, world, process, learner, contracts}` + `tests/hwsc`; `tests/k4b` unbound; the bound known cases of KC8 in `tests/hwsc`; binding audit; `check_file_sizes` (≤ 400 lines); `tempfile.gettempdir()` inside a metered child on X:; basetemps outside the project root | code | all pass | — | INVALID |
| KC | KC job | KC0–KC9 | §4 | §4 | all PASS | §4 | FAIL_TECHNICAL/KNOWN_CASE |
| T1–T3 | one TRAIN job per master | TRAIN_j | `hwsb_train.train(hwsc-store, obs_ids, j, plan=HWSC_PLAN, hold=HoldRule(…))` under `bound_stage_c()` (run key `("hwsc-v1", KEY, j)`); train/dev by the `hwsc_data` mirror | train, dev of j | status COMPLETE, 5,000 steps, 12 checkpoints saved in `hwsc-store/artifacts`, finite loss | — | NONFINITE → FAIL_TECHNICAL/NONFINITE (no seed swap); owner STOP at a hold, or a lost process → INCONCLUSIVE/RESOURCE_OR_AUTHORITY (never restarted from weights) |
| 0 | E1 | G0c (window) | KC0's authority and seed checks repeated; release A present with the W3 attestation, the K-REG1 reservation and the seed-hit classification (K4B §6 row 0) | records | all hold | exact | INCONCLUSIVE/AUTHORITY; FAIL_TECHNICAL on hash/seed defects |
| 1 | E1 | **H1-C IDENTITY** | the 6 checkpoints (step 5000 and step 0 of each master), whose ids and checksums are read from the three `stages/TRAIN/<master>/TRAIN_RECORD.json` files bound by sha256 in their STAGE_COMPLETE records and in release A, by `meta.json` checks before loading: artifact id, artifact type, run key `("hwsc-v1", KEY, master)`, step, status, init seed key and value (equal between step 0 and 5000), and `payload_sha256` equal to the TRAIN record (the `k4b_config.check_checkpoint_meta` field set); none of their ids in HANDOFF `stage_c_exclusions`; `c1_model.load_model64` round trip exact; process rebuilt (KC1 identity again); E_canon bitwise identical; `validate_process`; **Z_bound = `hwsb_law.law_bound(T, E_canon_shared, π, coords, 7/4, 1/5)`**, status BOUNDED and equal to HANDOFF `Z_bound`; `c1_cert.a1_selftest()`; one torch thread | checkpoints, process | all hold | exact | FAIL_TECHNICAL/IDENTITY; Z_bound unavailable or unequal → FAIL_TECHNICAL/LAW_BOUND |
| 2 | E1 | REG1 | K-REG1 built (§3.4), manifest classifies every directory; coordinator completeness certificate in release A | §3.4 sources | complete | exact | INCONCLUSIVE/REGISTRY_INCOMPLETE |
| — | E1 | sampling S3 | reservation verified; lgate b0 (4,096), cal b0, val b0 (3,072 each) drawn (§2.4) | — | — | — | reservation breach before the first row: cancel release A, rebuild; after: stop for lineage review (K4B §3.5 W2) |
| 3 | E1 | H2 SEPARATION | `hwsc_data.h2c` (the `k4b_driver.h2` mirror with `Registry.contains` and lgate as a third block, §3.3): every row's digest ∉ K-REG1, the three blocks pairwise disjoint, sequence IDs disjoint from the frozen union, sealed-D-2a predicate false on every row; duplicates counted | lgate, cal, val | 0 collisions, 0 predicate hits | exact | collision → FAIL_TECHNICAL/LINEAGE; predicate → INCONCLUSIVE/REGISTRY_INCOMPLETE |
| 4 | E1 | **L1 LEARNING** (new) | per master j at step 5000: `hwsb_eval.model_predictive` (float32 logits at index 32, float64 softmax, canonical re-indexing), oracle predictives q32, q1 (`hwsb_eval.oracle_predictives`), `hwsb_eval.b1` → captured_j = 1 − regret_j/G_C with `LearningGate(0.8)` (E4's gate; HWSB B1, line 151) [V]; computed for all three before the gate decides | lgate b0, 4,096 rows | captured_j ≥ 0.8 for **all three** (equality passes, `metrics.py:114` per HWSB) | probability rows sum to 1 within 1e-6; NaN → FAIL_TECHNICAL/NUMERICAL | **INCONCLUSIVE/NOT_LEARNED (k of 3)**; no replacement seed, no recipe change (§6.3) |
| 5 | E1 | ORACLE-VAL | m1, m2, m4, m32 on cal and val; Decimal references on all 3,072 validation rows and 4 calibration rows; moment check ≤ 1e-10 (K4B §6 row 4) | cal, val | all rows | 1e-10, exact Fraction comparison | FAIL_TECHNICAL/ORACLE |
| 6 | E1 | B4-VAL | `guard_H5(lower, B^H + Z_bound(w*))`, lower = rank-250 of 5,000 tree means of ‖r4‖ (seed 620312) (K4B §6 row 5) | val | PASS (certified one-sided 95 % lower bound of B4 > 0.01) | exact | INCONCLUSIVE/HEADROOM or /NUMERICAL |
| 7 | E1 | C0-CAL | per model `fit_chart_lcc` on the 512 cal landmarks (GIANT ≥ 487, lift, primitive class, smoothing ≤ 1e-8), gauge alignment finite and > 0; trained ledger 3 claims; then the three step-0 production charts (INIT_UNAVAILABLE non-gating; shared-code FAIL_TECHNICAL stops) and the suffix decoder; production artifacts frozen before any validation activation (K4B §6 row 6) | cal | all three PASS | inherited exact integer criteria; 1e-8 | INCONCLUSIVE/CHART_UNAVAILABLE or FAIL_TECHNICAL (C1′ §14 taxonomy) |
| 8 | E1 | C0-VAL | direct chart per model (GIANT ≥ 487); `c0_val`: support ≥ 507/512, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30 (K4B §6 row 7) | val panel 512 | all three PASS | exact counts | as row 7 |
| 9 | E1 | CERT-VAL | production extension on all validation rows; for every row and primary array: B ≤ 1e-4, \|X̂\| ≤ 4 (K4B §6 row 8) | val | all rows | cap 1e-4 exact | INCONCLUSIVE/NUMERICAL (cap) or FAIL_TECHNICAL/NUMERICAL |
| 10 | E1 | **P1 PRECISION** | `hwsb_gates.ladder_pilot` with the stage-C models and seeds, via `hwsc_gates.p1c`: SD^U by `sd_b4_draws` (seed 620311, rank 4,917), MDE rule with delta 0.01 + F_plan, projection with centred draws (seed 620315), per-model and **three-model joint** counts ≥ 4,000/5,000 in the SUPPORT and EXCLUSION scenarios (K4B §7.2) [V]; N_P1 = first qualifying ladder value; **N = max(HANDOFF `N_C`, N_P1)**, k = N/3,072; width diagnostic reported; `SEALED_VALIDATION.json` written and hashed | val, 3,072 | N_P1 exists | ranks checked; F_plan exact | INCONCLUSIVE/UNDERPOWERED (before any fresh draw) |
| 11 | release | ACCEPT, K-REG2, release B | coordinator ACCEPT of the validation report; W2 reservation; K-REG2 rebuilt from scratch and frozen; release B binds N, k, the K-REG2 sha256 and inventory, reservation, worker session, W3 record (K4B §6 row 10) | — | all present | exact | no release, no fresh data |
| — | E2 | sampling S7 | test b0…b(k−1) under release B | — | — | — | as K4B §6 S7 row |
| 12 | E2 | H2-FRESH | `hwsc_data.h2_fresh_c` (§3.3): U_test ∩ K-REG2 = ∅; IDs disjoint; predicate false (K4B §6 row 11) | test | 0 | exact | LINEAGE / REGISTRY_INCOMPLETE / lineage review |
| 13 | E2 | T-PRE | oracle and Decimal references on every test row; landmark determinism (all 3,072 cal activations recomputed bitwise for 3 trained + 3 step-0 models); extension by the frozen charts; row certificate ≤ 1e-4; fresh B4 reported only (seed 620314) (K4B §6 row 12) | test, cal | all hold | bitwise; 1e-10; 1e-4 | FAIL_TECHNICAL/ORACLE, /DETERMINISM, /NUMERICAL; INCONCLUSIVE/NUMERICAL |
| 14 | E2 | **ENDPOINT** | joint bootstrap (seed 620313, 5,000 draws) over X±_j and every control array; L−_j = rank 84 of X−_j, U+_j = rank 4,917 of X+_j; F_{j,s} = max(B_num, 10⁻⁹) + Z_bound(w\*); per-model status and overall outcome by `k4b_stats.model_status`/`overall` (`k4b_stats.py:69-89`) [V] under the binding; POSITIVE_BELOW_MARGIN annotation (§6); validation file opened and `SEALED_OPENED.json` hashed inside STAGE_COMPLETE | test | — | ranks checked | rank-check failure → FAIL_TECHNICAL/NUMERICAL |

**Decision (unchanged, K4B §8.1).** SUPPORT_j iff L−_j − F_{j,−} > 0.01; EXCLUDE_j iff U+_j + F_{j,+} < 0.01 and L−_j − F_{j,−} > −0.01; otherwise UNRESOLVED_j (UNRESOLVED/NUMERICAL if F alone blocks; NEGATIVE_ALIGNMENT if U+_j + F_{j,+} < −0.01). Overall: SUPPORT or EXCLUSION only in all three; MIXED if some definite status but not all the same; INCONCLUSIVE otherwise.

**Expected magnitudes (orientation only, never thresholds) [W from H].** F ≈ 10⁻⁹ + 1.12e-12 (Z_bound(w\*) ≈ 1.1248e-12 [W from the HANDOFF fraction]); F_plan ≈ 1.0000000112e-4 [W]. Stage A's per-row D4 SD at w\* was 0.0823 and V4 ≈ 0.0398 (HWSB line 36) [H], so SD(X±) ≤ √V4 ≈ 0.20 [W]; the MDE rule passes at N = 3,072 iff SD^U ≤ (0.01 − F_plan)·√3072/2.9697 ≈ 0.185 [W], so N_P1 = 3,072 is likely but N = 6,144 is possible if support is poor. These numbers do not use any pilot statistic.

---

## 6. Outcomes and licences (registered now; addendum 25 rule 6 included)

### 6.1 Outcomes, in order of precedence
| # | Outcome | Condition |
|---|---|---|
| 1 | **FAIL_TECHNICAL/<reason>** | S0/PF invalid is "do not run", not an outcome; a KC failure (KNOWN_CASE); NONFINITE training loss; IDENTITY, LAW_BOUND, LINEAGE, ORACLE, DETERMINISM, NUMERICAL, BINDING, SEALING defects not resolved under §8.4 |
| 2 | **INCONCLUSIVE/RESOURCE_OR_AUTHORITY** | a scheduled stage did not complete: a 3× pause or a training hold the owner does not continue, a lost training process, a disk or memory safe-STOP, missing or expired authority, or the window/scheduling precondition not met |
| 3 | **INCONCLUSIVE/NOT_LEARNED (k/3)** | L1: captured < 0.8 in k ≥ 1 models |
| 4 | **INCONCLUSIVE/<K4b reason>** | REGISTRY_INCOMPLETE, HEADROOM, CHART_UNAVAILABLE (with the failing model and criterion), NUMERICAL, UNDERPOWERED: the first non-PASS K4b gate |
| 5 | **SUPPORT / EXCLUSION / MIXED / INCONCLUSIVE(/NUMERICAL)** | the ENDPOINT rule (§5) |

**Annotations (never change the outcome).**
- **POSITIVE_BELOW_MARGIN_j** (addendum 25 rule 6): L−_j − F_{j,−} > 0 and status_j ∈ {UNRESOLVED, UNRESOLVED/NUMERICAL, EXCLUDE}. With EXCLUDE_j it reads 'positive, and certified below the margin'. With an UNRESOLVED status it reads 'positive, not resolved against the margin'. The overall annotation POSITIVE_BELOW_MARGIN applies iff L−_j − F_{j,−} > 0 in all three models and the overall outcome is not SUPPORT.
- NEGATIVE_ALIGNMENT_j, UNRESOLVED/NUMERICAL (K4B §8.1); the step-0 qualifier and INIT_UNAVAILABLE (K4B §9 item 3); FRESH_B4_LOW (K4B §6 notes).
- Every per-model result is published; no model is selected post hoc (K4B §8.2).

**Levels.** Unchanged (K4B §8.3): α = 0.05/3 per one-sided bound; ≤ 2α per model for a false definite claim; 6α = 0.10 over three models; 0.05 per directional family; nominal bootstrap levels conditional on the three trained weight sets, charts and gauges. The POSITIVE_BELOW_MARGIN annotation is a one-sided bound at the same nominal α against 0, per model; it is a description, with no added family claim.

### 6.2 Licences
All are nominal percentile-bootstrap statements conditional on the three trained models and their frozen charts and gauges; documented-law transport assumes idealised uniform sampler draws and does not bound PCG64 bias (K4B §8.4, line 552) [V].

**SUPPORT (filled at run time).** "In each of three transformers trained by the E4 recipe in world w\* (12 × 12 cylinder, stay probability 0.2, emission width 1.75; masters 620301/620302/620303, step 5000, resid_post_3, position 32), the gauged phase of a chart built by the LCC ≥ 95 % rule on fresh calibration histories covaries with the first-harmonic oracle residual r4 = m32 − m4 on N fresh stationary test histories. For every assignment of unit coordinates to the unsupported rows (a/N, b/N, c/N), the one-sided (1 − 0.05/3) lower bound of E[u·r4] under the documented law exceeds 0.01 after the certified margin F (values …; B4 = …; oracle comparator Δ4^orc = … on the same rows). Every function of the last four observations has zero population covariance with r4 under that law, so on its supported rows this coordinate is not a function of the last four observations: it depends on earlier observations, in a direction aligned with the oracle belief residual." Qualifiers when triggered: the step-0 qualifier; "initialisation control unavailable (reason)"; the lineage disclosure (§6.4).

**EXCLUSION.** "For this chart rule, site and world, in each of the three models the covariance of the chart phase with r4 lies within (−0.01, 0.01) for every completion of unsupported rows, under the documented law, at the stated nominal levels (bounds …; B4 = …; Δ4^orc = … on the same rows). Covariance of either sign at or beyond 0.01 is excluded." If the oracle comparator Δ4^orc on the same test rows is certified and its one-sided (1 − 0.05/3) lower bound exceeds 0.01 (the `delta4_orc` entry of the control summary), the report adds: 'these learned circles did not carry, in the measured direction, beyond-four information that the belief carried on these rows'. Otherwise the sentence is omitted. In either case EXCLUSION still does not establish suffix-only dependence (K4B line 574) [V].

**POSITIVE_BELOW_MARGIN (rule 6).** 'In model(s) …, the chart phase covaries positively with r4 for every completion (one-sided (1 − 0.05/3) lower bound > 0 after F). [EXCLUDE_j:] Its upper bound after F is below the registered margin 0.01: a positive effect, certified smaller than the margin. [UNRESOLVED_j:] Its lower bound does not exceed 0.01: a positive finding below the margin, neither SUPPORT nor evidence of a negligible effect.'

**MIXED / INCONCLUSIVE.** Only the recorded per-model results and the identified limitations.

**INCONCLUSIVE/NOT_LEARNED.** "Under the unchanged E4 recipe, k of 3 new models did not reach captured 0.8 on 4,096 fresh histories in w\*. The beyond-four question was not tested." Not licensed: that w\* is unlearnable; any statement about circles or about the pilot models.

**INCONCLUSIVE/CHART_UNAVAILABLE.** "The models learned (L1 PASS), but in model … the K4b chart rule did not yield a chart passing C0-cal/C0-val (criterion …) on fresh histories." Not licensed: that no circular structure exists.

**What a positive result does not establish.** K4B §8.4 items 1–10 (lines 562–572) [V], with "E4 models" read as "the three stage-C models", plus:
11. **The E4 models and K4b.** Nothing about the E4 models in w0; K4b's EXCLUSION stands, and a stage-C SUPPORT does not imply that K4b's models lacked the information (their world had too little of it to see).
12. **Training-seed population.** Three trained seeds are three draws of the training process, not a sample large enough to estimate how often the recipe produces this; the claim is "in each of these three models".
13. **Pilot models and other worlds.** Nothing about the stage-B pilot models, the fallback worlds or any world outside w\*.
14. **Oracle qualification.** Stage A's oracle numbers are motivation, not part of the evidence; stage C's own Δ4^orc on the test rows is the reported comparator.

**FAIL_TECHNICAL, INCONCLUSIVE/RESOURCE_OR_AUTHORITY:** no scientific statement.

### 6.3 What happens if a model fails to learn, or to form a chart
- The cohort stops at the failing gate with its outcome (§6.1). Every computed value is reported.
- **No replacement seed, no fallback world, no recipe change, no extra training steps, no larger model and no other chart method** without a new owner decision (addendum 33 Q4 pattern; HWS §10.4, lines 575–577; HWSB §5.3) [V]. A rerun with other seeds would be a new versioned protocol with its own review; its histories would enter its registry.
- The coordinator reports the outcome in plain language and asks the owner (default: stop, §12 Q2).
- A technical defect is handled only by the K4b technical-correction rule (§8.4).

### 6.4 Disclosure carried by every report
"Stage C follows K4b (EXCLUSION in the E4 models in w0, where the oracle comparator was below the margin), stage A (w\* selected on oracle criteria only) and stage B (a two-model pilot in w\*, HWSB_PASS). Stage C's models, histories, charts and decision are its own; stage-B results entered stage C only through HANDOFF.json (test size floor, model count, budget forecasts, Z_bound and F_plan identity values, the registry inputs and the pilot exclusions). No threshold, margin, chart parameter or recipe setting was changed in response to any earlier result."

---

## 7. Synthetic dry run (addendum 25 rule 4; before the execution freeze)

The real `hwsc_driver`, binding, records, gates, registry composition and report run end to end in `scratch/hwsc-dry/` under the DRY scope (masters 629911–629913). Persisted histories come only from synthetic tiny worlds; the real-architecture smoke keeps its w\* rows in memory. Planted fixtures are labelled as fixtures. Any defect is fixed before the freeze; no threshold is tuned; the dry run never issues a real-scope stream, master or seed.

| # | Case | Expected |
|---|---|---|
| DRC1 | Full pipeline on the HWSB DRB1 tiny world (W = 6, H = 2, L = 32): three tiny models (1 layer, d_model 16), 200 steps; KC-style identity on the tiny process; L1; REG1 on a synthetic project tree (S2: every dry-run registry case, here and in DRC9, runs on a synthetic root only, never on the real project or scratch root); S3; H2; ORACLE-VAL; B4-VAL; charts; CERT-VAL; P1; release B; S7; H2-FRESH; T-PRE; ENDPOINT; report | runs; every record complete; every gate function returns a value |
| DRC2 | Real E4 architecture, 20 steps, three masters, 2,048 in-memory w\* DRY rows: training through `hwsb_train.train` under the binding; checkpoint run keys `("hwsc-v1", "DRY", …)`; logits, activations, BOS 36, vocab 37/36 | shapes and identities valid; nothing persisted |
| DRC3 | Binding: identity table bitwise (KC7 a); stage-C table audit clean; a planted extra copied constant (a module global equal to (1729, 2718, 3141)) is caught; restore after an exception; a planted function default equal to 610101 and a planted dataclass field equal to (620201, 620202) are caught | as stated |
| DRC4 | `hwsc_data` train/dev mirror with replicate `"hwsb-v1"` equals `hwsb_data.make_train_dev` bitwise on a memory store; with `"hwsc-v1"` the IDs and streams differ and are disjoint | as stated |
| DRC5 | Planted endpoint fixtures (arrays with known means and widths): SUPPORT in all three; EXCLUSION in all three; MIXED; UNRESOLVED/NUMERICAL; NEGATIVE_ALIGNMENT; POSITIVE_BELOW_MARGIN (L − F exactly 0 is not positive; one ulp above is); the boundaries L − F = 0.01 and U + F = 0.01 unresolved; EXCLUDE with L − F one ulp above 0 → annotated; EXCLUDE with L − F = 0 → not annotated | exact |
| DRC6 | Ladder: N = max(N_C, N_P1) with N_C ∈ {3,072, 6,144} and N_P1 ∈ {3,072, 6,144, 12,288, none}; "none" → UNDERPOWERED regardless of N_C; projection invariant to mean shifts; `hwsc_gates.p1c` draws with 620311/620315 (a seed-sensitive fixture distinguishes them from 610101/610105) | exact |
| DRC7 | L1 on planted predictives: p = q32 → captured 1; p = q1 → captured 0; 0.8 exactly passes; one model failing → INCONCLUSIVE/NOT_LEARNED (1/3) and no later gate runs | exact |
| DRC8 | Law and identity: σ = 5/4 enclosure equals the old one (δ = 0); σ = 7/4 BOUNDED; H1-C refuses a planted Z_bound differing from a fixture HANDOFF in the last digit; H1-C refuses a checkpoint id listed in a fixture `stage_c_exclusions` | as stated |
| DRC9 | Registry: synthetic stores for each reader R1–R8, including a DRB13-style store with a missing and a renamed file (read file by file, PASS), an unreadable `.npz` (INCOMPLETE), an unlisted top-level directory with a history file (INCOMPLETE), a `sealed/` directory (never opened: an access hook records zero opens), a C2-format digest table; a scale case: a synthetic DigestSet base of ≥ 20 M digests with one planted collision, built and queried under the 12 GiB cap | as stated |
| DRC10 | Sealing: a validation report that would allow X̄± = C ± D to be reconstructed is refused; `SEALED_OPENED.json` appears in the ENDPOINT STAGE_COMPLETE file list with its sha256 (D6) | as stated |
| DRC11 | Blindness hooks: any attempt by stage-C code to open `hwsb-store/REPORT.json`, `stages/EVAL/`, `GATES.jsonl`, `CHART_CONSTRUCTIONS_*.json` or any path under `ah/jobs/0175/` raises FAIL_TECHNICAL/BLINDNESS (a path guard in `hwsc_config`, tested with fixture paths) | as stated |
| DRC12 | Records, rerun and budget: exclusive-create refusals; an interrupted stage archived under `superseded/` and regenerated bit-identically; per-stage and cumulative 3× triggers; the training hold (planted CPU function) holds at ≈ 0 CPU, CONTINUE resumes, STOP ends INCONCLUSIVE; a held-and-continued run gives bitwise-equal checkpoints | as stated |
| DRC13 | Meter binding and placement: effective TEMP_ROOT and pytest basetemp under `scratch/test_hwsc-<job>/`; single thread; `--max-cpu inf --max-wall inf`; disk safe-STOP and op-guard precedence (K4B §11.7) | as stated |
| DRC14 | G0c needles: planted true and false hits classified by the whole-token rule | as stated |

**Pass:** every expected result exactly; the report is committed, bound to the implementation hash, and accepted by the coordinator before the execution freeze. **Cost:** about 600 CPU-s central [W] (HWSB DRY 161 s and 159 s measured, `ah/jobs/0169/review.md:10`, `0171/review.md:9`) [H]; DRC1 and DRC2 dominate.

After the dry run, a read-only header inventory of `root/` must show no new history file, identity reference or ObservationSet root compared with the record before the job (HWSB §6.4 rule 1 pattern, line 230) [V].

---

## 8. Adaptive budget (addendum 26; outside the addendum-29 line, addendum 34 item 4)

### 8.1 Measured basis [H]
- **Training at one thread in w\*:** 1,964.8 and 2,002.1 meter CPU-s for the two pilot models (`ah/jobs/0173/review.md:3`, `0174/review.md:3`); wall 1,923 and 1,949 s. HANDOFF `training_forecast_s` = 6,006.6282 = 3 × 2,002.2094 [V, W].
- **Evaluation:** K4b E1 1,280.5 CPU-s (`ah/jobs/0055/report.md:63`) and E2 1,720.1 CPU-s at N = 3,072 (`ah/jobs/0057/report.md:102`); HANDOFF `evaluation_forecast_s` = 3,000.6 = 1,280.5 + 1,720.1·N_C/3,072 [V, W].
- **Known cases and tests:** HWSB KB 407.3 CPU-s (`ah/jobs/0172/review.md:4`); HWSB J-B1 preflight 417.0 and 410.4 CPU-s (`0169/review.md:8`, `0171/review.md:7`); the C1′ suite ≈ 12 min [H, K4B line 702].
- **Registry growth [W]:** C2ND's frozen X6 base alone has 19,420,831 digests (`tp/tools/c2_nd/CONTRACT.json` `registry.x6_reg2_n`) [V], far more than K4b's E1 registry; K-REG1 and K-REG2 builds are the main uncertainty in E1 and E2.

### 8.2 Stage forecast and 3× thresholds [W] (single thread, measure-only, never a cap)
| Stage (one job each) | Content | Central CPU-s | Range | Stage 3× | Cumulative central | Cumulative 3× |
|---|---|---|---|---|---|---|
| J-C1 IMPL | metered tests: `tests/hwsc` + PF suites (incl. C1′ ≈ 720 s) + binding audit + sizes | 1,200 | 800–2,400 | 3,600 | 1,200 | 3,600 |
| DRY | DRC1–DRC14 | 600 | 200–1,500 | 1,800 | 1,800 | 5,400 |
| KC | KC0–KC9 (KC2 ≈ 165 at 6 threads; KC9 the registry rehearsal) | 1,500 | 800–3,500 | 4,500 | 3,300 | 9,900 |
| TRAIN ×3 | three sequential meter jobs × 2,002.2 (HANDOFF) | 6,006.6 | 5,800–7,500 | 18,020 (per model hold 6,006.6) | 9,306.6 | 27,920 |
| E1 (release A) | G0c, H1-C, REG1, S3, H2, L1, ORACLE-VAL, B4-VAL, C0-CAL, C0-VAL, CERT-VAL, P1 | 2,000 | 1,300–4,500 | 6,000 | 11,306.6 | 33,920 |
| E2 (release B) | K-REG2 (cost R = KC9's measured registry CPU), S7, H2-FRESH, T-PRE, ENDPOINT: R + 1,720.1·k | planning value with R = 300 [W]: 2,020 (k = 1); 3,740 (k = 2); 7,180 (k = 4) | ×0.6–×2 | 3× its central at the released k | 13,327 / 15,047 / 18,487 | 39,980 / 45,140 / 55,460 |
| **Total** | | **≈ 13,300 CPU-s (3.7 h) at N = 3,072**; 15,000 (4.2 h) at 6,144; 18,500 (5.1 h) at 12,288 | | | | |

Before the run approval, the E1 and E2 centrals are re-set from KC9's measured registry CPU (cost, not data; addendum 26 item 2) and written into the CONTRACT. The owner forecast (§8.5) is restated if the total changes by more than 20 %.

E2's central is fixed by this formula at release B, from the released k, before any test row; it is not re-estimated afterwards. The difference from HANDOFF's 3,000.6 evaluation forecast is the registry growth, L1, the process build and the law bound [W].

### 8.3 Pauses and the training hold (addendum 26 item 5)
- `--max-cpu inf --max-wall inf`; CPU is measured, never a stop. Disk floors C: ≥ 2 GB, X: ≥ 30 GB; meter memory cap 8 GiB for TRAIN; the KC (KC9 builds the registry), E1 and E2 meter memory cap is 12 GiB, fixed in the CONTRACT now (RC-2); native-operation wall 600 s per operation (K4B §11.7).
- **Per-stage trigger:** running stage CPU > 3× its central. **Cumulative trigger:** running total > 3× the cumulative central through the current stage. Checked at every item boundary (each KC check, each model, each gate). On a trigger no new item starts; the coordinator reports in plain language; continuation needs the owner. Not continued → INCONCLUSIVE/RESOURCE_OR_AUTHORITY.
- **Training hold** (HWSB §8.2, lines 289–293) [V]: the checkpoint callback holds the live process at ≈ 0 CPU when, from step 1,000, the projected CPU (CPU so far × 5,000/step) exceeds 6,006.6 s, or the CPU so far exceeds 6,006.6 s; CONTINUE resumes, STOP ends the model INCONCLUSIVE/RESOURCE_OR_AUTHORITY; a lost process is never restarted from weights. The hold report shows step, CPU and projection only; dev CE is not shown before the model completes.
- **Pause and hold reports (S1).** Every 3× pause report and every training-hold report carries CPU, step (or item) and projection only, and no gate value, so that the owner's continue/stop decision cannot be conditioned on intermediate scientific readings. Gate statuses stay in `GATES.jsonl`.
- **Study ledger:** `ah/HWSC_CPU_LEDGER.json`, appended atomically after each job, with unique labels per attempt (the HWSB ledger-label lesson, `ah/jobs/0172/review.md:5`) [V]; never summed into the addendum-29 ledger.

### 8.4 Frozen extension rules
- **X-1.** No stage grows on a scientific reading. L1, chart, headroom or endpoint results never add seeds, rows, steps or models.
- **X-2.** The only growth is the test size N, chosen once at P1 from blind quantities (validation SDs and centred draws, never a validation mean) by the frozen ladder, raise-only above HANDOFF N_C (addendum 26 item 3).
- **X-3.** Technical correction: only the K4B §11.8 rule (lines 751–767) [V]: a documented implementation or environment defect; at most two correction jobs per defect; PASS stages immutable; superseded archive with SHA256SUMS; bit-identical regeneration; an owner decision if a correction would change an already computed outcome-bearing quantity (L1 values, B4 bounds, chart criteria, SD bounds, N, endpoint means). An interrupted TRAIN job is rerun from scratch with identical seeds; its already written checkpoints must reappear bitwise (HWSB X-2, line 297) [V]. A valid failed chart construction is never re-attempted.
- **X-4.** KC2's pre-registered secondary reading is the only tolerance alternative. No threshold or tolerance changes after any stage-C data (K4B §13 item 8).

### 8.5 Plain-language forecast for the owner (to be said when asking for the run approval)
"This is the full test. We would train three new small models in the world the sweep chose, the same recipe as the pilot, one after the other; each takes a little over half an hour of computer time, so about an hour and forty minutes for all three. Before that, a short set of checks makes sure nothing in the setup has drifted. After training, the main measurement on fresh data takes roughly another hour. In all it should be a little under four hours of processor time, close to that on the clock, and about five hours if the data turn out noisier and the test has to be at its largest size. These are estimates, not limits. This is counted separately from the 12-hour line, and if any part runs past three times its estimate, I stop and ask you. At the end I will tell you, for each of the three models, whether its learned circle carries information from further back than the last four symbols, clearly does not, or whether the test could not decide."

---

## 9. Blindness and data hygiene

### 9.1 Stage-B quantities enter only through HANDOFF.json
`hwsb-store/HANDOFF.json` (sha256 a4d9a0c9…4353, 5,668 bytes; keys `F_plan, N_C, Z_bound, evaluation_forecast_s, freeze_sha256, k_C, model_count, outcome, p_D2a, protocol_sha256, registry_obligation, registry_value, report_sha256, stage_c_exclusions, store_inventory, training_forecast_s`) [V]. It holds no X± mean, capture ratio, c_min, confidence interval, regret, captured value or chart-fidelity value (HWSB §6.1, line 213) [V, and checked by the writer's key listing].

| HANDOFF key | Value [V] | Use in stage C | Rule |
|---|---|---|---|
| `outcome` | HWSB_PASS | precondition for planning | addendum 34 |
| `N_C`, `k_C` | 3,072; 1 | floor of the test size | §2.4, P1: N = max(N_C, N_P1) |
| `model_count` | 3 | three models | addendum 33 Q6 |
| `training_forecast_s`, `evaluation_forecast_s` | 6,006.63; 3,000.6 | budget forecast and holds | §8 |
| `Z_bound` | 87876736540276863476307541/78125·10³³ | identity check against the run's own law bound | KC4, H1-C (exact equality; the run's own value enters F) |
| `F_plan` | (exact fraction) | identity check against `k4b_cert.F_plan(Z_bound)` | KC4 |
| `p_D2a`, `registry_value` | 5.4163e-15; 4.99e-11 | registry-risk check | §3.4 |
| `registry_obligation`, `store_inventory` | text; 32 file hashes | registry sources R3–R5 | §3.4 |
| `stage_c_exclusions` | 24 checkpoint ids | refused at H1-C | §2.3 |
| `freeze_sha256`, `protocol_sha256`, `report_sha256` | hashes | identity only; `REPORT.json` is never opened | KC0 |

The writer did not open `REPORT.json`; its hash is used only to bind HANDOFF to the stage-B record.

### 9.2 No tuning on pilot data; the margin
- **M stays 1/100** (HWS §11 row 14, line 600; HWSB §6.1 line 210) [V]. It is not raised toward δ_max = 0.01525 [H] and not lowered after any data.
- Chart cfg, recipe, site, position, gates, ranks, α, the ladder values, the certificate cap and every tolerance are K4b's or E4's unchanged. No pilot activation, chart or capture value informs any choice here.
- Stage-B pilot values (in `REPORT.json`) go to the coordinator and the owner only, and are never attached to or quoted in prompts to stage-C writers, implementers, test authors or reviewers (RC-6). The dry-run guard DRC11 makes stage-C code refuse to open them.
- Stage-C roles: the implementation author and the two test authors read this protocol, `API.md`, `CONTRACT.json`, `TEST_PLAN.md` and the reused frozen code; never the public research summary paths, stage-B `REPORT.json`, `stages/EVAL/`, `GATES.jsonl`, `CHART_CONSTRUCTIONS_*.json`, `ah/jobs/0175/`, or any `sealed/` file.

### 9.3 How stage-C histories enter every later registry
- **Store** `root/hwsc-store/` (new; verified absent before creation, or holding only this lineage's recorded files): `FREEZE.json`, `AUTH_*.json`, `RESERVATION_*.json`, `registry/`, `artifacts/` (WorldSpec, TransitionSpec, three EmissionSpecs, six ObservationSets, 36 Checkpoints), `stages/<stage>/` (K4b layout: `stages/S3/HIST_{lgate, cal, val}_b0.npz`, `stages/S7/HIST_test_b<k>.npz` with K4b's columns), `GATES.jsonl`, `STAGES.jsonl`, the two chart ledgers, `SEALED_VALIDATION.json`, `SEALED_OPENED.json`, `superseded/`, `logs/`, `cpu_ledger.json`, `tmp/`.
- **Final record** `hwsc-store/REGISTRY_OBLIGATION.json`, hashed in the final report: every later registry must list `hwsc-store` (ObservationSets by the `hwsb_registry` reader; `HIST_*.npz` by the K4b history-table reader; superseded attempts included), `scratch/hwsc-dry/` and any `scratch/hwsc-dry-<job>/` re-run (§3.4 R5 lesson), with the full file inventory and sha256 list, fail closed.
- Dry stores never use `HIST_*` names; pytest basetemps and meter temp folders live under `scratch/test_hwsc-<job>/` (K4b registry-trap lesson).
- **Set-aside rule for repeated dry runs (S2; R-0157-1, `ah/jobs/0157/review.md:7`) [V].** A repeated dry run re-draws the identical DRY rows. When a `hwsc-dry*` store is superseded by a later dry run, its `hist/` is set aside by renaming it to `test_superseded-hist/` inside the same store, with a `SET_ASIDE.json` record of each file's sha256; nothing is deleted or rewritten. Dry-run registry cases never read the real scratch root (DRC1).

### 9.4 Window and scheduling (K4B §3.5, lines 270–280) [V]
- W2/W3 apply from the first stage-C history generation, which is the first TRAIN job (train/dev draws). The coordinator records that no other study holds a live history-generation reservation or a frozen registry awaiting a draw that would not include `hwsc-store` (today none is running, per the request) and keeps an exclusive reservation from the start of TRAIN through the last test block, renewed per job.
- Any later study's registry lists `hwsc-store` (§9.3).

---

## 10. Reuse and footprint

### 10.1 New code: `tools/hwsc/` (one new module; each `.py` ≤ 400 lines; no existing file edited)
Developed on branch `hwsc-impl` in the existing worktree `topo-pilot-hws` (listed in every frozen inventory; a new top-level worktree would be an unlisted directory), from main af5e7b4. `PYTHONPATH=<worktree>/src`, venv interpreter with `-s`.

No `.npz`/`.npy` file is committed under `tools/hwsc` or `tests/hwsc`. Implementation, tests and the dry run write no array file anywhere under `root/`. Meter `TEMP_ROOT` and pytest basetemps are under `scratch/test_hwsc-<job>/` (HWSB §6.4 rule 1 pattern).

| File | Contents | Lines [W] |
|---|---|---|
| `PROTOCOL_HWSC_v1.md` (byte copy of the frozen plan), `API.md`, `CONTRACT.json` (incl. the binding table and the inventory table), `TEST_PLAN.md` | committed first | — |
| `hwsc_config.py` | constants, scope, masters, seeds, paths, plan object, HANDOFF loader with key whitelist, blindness path guard | ≈ 160 |
| `hwsc_bind.py` | binding table load, `bound_stage_c()`, binding audit | ≈ 180 |
| `hwsc_data.py` | process build wrapper, train/dev mirror (`hwsc-v1` replicate), lgate block, `h2c` and `h2_fresh_c` (RC-2) | ≈ 260 |
| `hwsc_registry.py` | `build("K-REG1" \| "K-REG2" \| rehearsal)` in the C2 manifest/digest format: C2/C2ND readers, R2 c2nd-store reader, R4/R7 hwsb reader, R5/R6 scratch readers and scratch inventory table, R8 inventory adapter (RC-2, RC-3, RC-4) | ≈ 380 |
| `hwsc_known.py` | G0c, KC0–KC9 (calls `hwsb_known` KB functions) | ≈ 290 |
| `hwsc_gates.py` | H1-C, L1, `p1c` (RC-1) and N = max(N_C, N_P1), POSITIVE_BELOW_MARGIN, outcome precedence, licences | ≈ 290 |
| `hwsc_driver.py` | jobs KC, TRAIN, E1, E2; stage records; `export_c` (D6); ledger; CLI | ≈ 380 |
| `hwsc_dry.py` | DRC1–DRC14 | ≈ 380 |
| `hwsc_meter_bind.py` | thin main over `k4b_meter_bind` (the `hwsb_meter_bind` pattern) | ≈ 100 |

About 2.4k lines [W]. Tests (≈ 1.5k lines) in `tests/hwsc/` by **two independent authors** who never read `tools/hwsc/*.py`: **A** (decision rule with the annotation, ladder max-rule, L1 maths, law identity, outcome precedence and licences, KC8 under the binding in `tests/hwsc/test_a_k4b_known_bound.py`); **B** (binding table and audit, streams and IDs, the mirror equality, registry readers R1–R8 with planted defects, blindness guard, records, sealing and D6, hold and pauses, meter binding, basetemps outside the root). `AUTHORSHIP_A.md`, `AUTHORSHIP_B.md`. No formatter over `tests/`. After acceptance, `.venv/Scripts/python.exe tools/build_code_index.py` and a separate `docs(index): …` commit (CLAUDE.md rule).

### 10.2 Six-field reuse assessment
| Part | 1 Existing (unchanged) | 2 Missing | 3 Smallest change | 4 Invariants | 5 Regression checks | 6 Next extension (not built) |
|---|---|---|---|---|---|---|
| K4b pipeline | `k4b_driver.{oracle_val, b4_val, c0_cal_stage, c0_val_stage, cert_val}`, `k4b_fresh.{require_release_b, sample_test, t_pre, endpoint}`, `k4b_stats` (except `ladder`, `sd_upper`, `centered`), `k4b_cert`, `k4b_scores`, `k4b_charts`, `k4b_decoder`, `k4b_release` | constants for new models and scope; P1 seeds held as default arguments; registry format and scale | `hwsc_bind` binding table + audit (§3.2); mirrors `p1c`, `h2c`, `h2_fresh_c`, `export_c` (§3.3) | every K4b invariant (K4B §11.3 field 4); first non-PASS stops | `tests/k4b` unbound; the bound known cases in `tests/hwsc`; KC7, KC8; DRC1, DRC3, DRC5 | a generic K4b config object only by a new reviewed protocol |
| Training | `hwsb_train.{train, HoldRule, CheckpointSaver, set_threads}`, `Trainer`, `LearnerStage` (reference) | — | plan object with stage-C masters; run key via bound `hc.SCOPE` | deterministic algorithms; one thread; per-model meter job | `tests/hwsb`, `tests/learner`; KC2, KC3; DRC2, DRC12 | — |
| Data and process | `hwsb_data.{build_process, sample_observations, sample_block, canonical32}`, `k4b_data.{sample_block, history_table, separation_*, seq_disjoint, predicate_check}` | `hwsc-v1` train/dev IDs (`hwsb_data.py:176` literal) | 40-line mirror, bitwise-tested (DRC4) | one `sample` call per table; w33 never stored | `tests/dataset`, `tests/hwsb`; KC1; DRC4 | — |
| Learning gate | `hwsb_eval.{model_predictive, oracle_predictives, b1}`, `PredictiveMetrics`, `LearningGate` | an all-three gate | `hwsc_gates.l1` (≈ 30 lines) | logits never mixed with float64 activations | KC6; DRC7 | — |
| Law bound | `hwsb_law.{bound_law, law_bound}`, `ENCLOSURE_PROOF.md`, `process_law.process_law_bound` | — | none | module state restored in `finally` | KC4; DRC8 | — |
| Known cases | `hwsb_known` KB0–KB6 functions; `hws_driver.seed_search` | stage-C needles, KC7 | `hwsc_known` | whole-token rule | DRC14 | — |
| Registry | `k4b_registry.{inventory, classify}`, C2ND `nd_registry` readers, `c2_registry.{token_sources, x6_source, Registry}`, `x6s1_registry`, `hwsb_registry.registry_digests`, `k4b_data.{seq_disjoint, predicate_check, duplicates}` | R2, R5, R6 readers; the extended root and scratch inventory tables; a C2-format build | `hwsc_registry` | fail closed; never `sealed/`, never `state.pt` | DRC9; KC9 | — |
| Meter | `k4b_meter_bind` (via the `hwsb_meter_bind` pattern), job-0014 meter, `op_guard` | stage-C store binding | `hwsc_meter_bind` | measure-only CPU; STOP/INVALID precedence | DRC13 | — |

---

## 11. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Partial binding of copied constants (§3.2) | silent use of E4 seeds or K4b scope | binding table + audit in PF, dry run and every job; KC7 |
| A new model fails L1 or a chart gate | INCONCLUSIVE, no test | registered outcomes; owner decides (Q2); stage B's two pilots passed (HANDOFF outcome) [H], which is not evidence for new seeds |
| Wider emissions give a lower support fraction | wide identified set; larger N or UNRESOLVED | the ladder up to 12,288; width reported, never gated (K4B F5) |
| Registry build cost with ≈ 19 M digests | E1/E2 above forecast; a registry failure after training | C2-format DigestSet with `Registry.contains` (§3.3); 12 GiB cap fixed now; KC9 rehearsal before any training, its measured cost re-sets the E1/E2 centrals; 3× pauses |
| Unlisted or unreadable history store (incl. the stage-B dry re-runs) | REGISTRY_INCOMPLETE | §3.4 R5/R6; inventory tables frozen in the CONTRACT before the execution freeze; re-scanned at REG1 and REG2; DRC9 |
| C2ND's own table format differs from C2's | R2 unresolved | verified from C2ND API at implementation; unresolved is INCOMPLETE, never NOT_SCANNED |
| Z_bound or F_plan differs from HANDOFF | stop | FAIL_TECHNICAL/LAW_BOUND; coordinator review; no tolerance |
| Training nondeterminism or environment drift | non-reproducible models | KC2, KC3; locked torch 2.14.1+cpu [H] |
| Lost training process during a hold | model lost | INCONCLUSIVE; no restart from weights |
| Pilot values reaching stage-C roles | loss of result-blindness | HANDOFF-only rule; path guard DRC11; prompts never cite REPORT.json |
| Overreading an EXCLUSION as "no history use" or a SUPPORT as "the recipe always learns it" | overclaiming | licences §6.2 items 11–14 |
| Late technical corrections steering the outcome | bias | §8.4 X-3: owner decision once an outcome-bearing value exists |
| Worktree imports main's `src`; basetemps under the root | wrong code; registry INCOMPLETE elsewhere | `PYTHONPATH`, `-s`; basetemps under `scratch/test_hwsc-<job>/` |
| Interaction of the max() rule with a future HANDOFF | none today (N_C = first ladder value) | the rule is fixed now and tested (DRC6) |

---

## 12. Owner questions (science and risk only; each with a registered default)

1. **Test size.** Use N = max(stage-B N_C = 3,072, the K4b validation ladder on the stage-C models), so the stage-C check can only enlarge the test? **Default: yes (raise-only).** Alternative: N fixed at N_C with no stage-C check.
2. **A model fails to learn or to form a chart.** **Default: stop with that outcome and ask; nothing automatic** (no replacement seed, no fallback world, no recipe change, no other chart method).
3. **The learning gate.** Add E4's own learning gate (captured ≥ 0.8) for each new model, all three required, before any chart is built? **Default: yes.** Alternative: report-only.
4. **The "positive but below margin" licence.** Register the per-model annotation POSITIVE_BELOW_MARGIN with the §6.1 definition: the lower bound after F is above 0 and the model is not SUPPORT. It covers both "positive, not resolved against the margin" (UNRESOLVED) and "positive, and certified below 0.01" (EXCLUDE), the latter being the likeliest informative result if the learned circles carry only part of the oracle signal. Never a SUPPORT. **Default: yes.**
5. **The margin.** Keep M = 0.01 (K4b's margin) even though the world would allow up to about 0.015 at three-fold headroom? **Default: keep 0.01.**
6. **Running stage C.** Not approved (addendum 34 item 3). After the execution freeze the coordinator asks for an explicit run approval with the §8.5 forecast (about 3.7 CPU-h central, about 5.1 CPU-h at the largest test size, re-set from KC9's measured registry cost before the request; 3× pauses). **Default: no run until the owner says so.**

**Decided by the coordinator (procedural, registered here):** one torch thread with KC2/KC3; the KC set (stage B's KB checks reused; no E4 payload reads); covering the stage-B dry re-run stores in the registry (§3.4 R5); the worktree and branch; the study ledger `ah/HWSC_CPU_LEDGER.json`; the binding-table completion by the audit (as a reviewed contract erratum before the freeze); the seeds 620301–620315 and DRY masters 629911–629913.

---

## 13. Provenance

| Input | Identity |
|---|---|
| Request | `ah/planning/requests/coord-hws-stage-c-20261029.md` sha256 4299ce6a…7b639 (verified) |
| v2 inputs | v1 `coord-hws-stage-c-20261029.claude.md` (e7718bff…3f8e); review `….claude-reviewer.md` (59f68390…d2fc, verified); rulings `….rulings.md` (c705d155…b942, verified). For v2 the writer additionally verified at main af5e7b4 the code lines it newly cites or relies on: `k4b_driver.py:346` (`p1`), `hwsb_gates.py:141` (`ladder_pilot`), `hwsb_driver.py:148, 155` (ledger defaults), `k4b_meter_bind.py:26` (`TEMP_ROOT`), `hwsb_train.py:265` (`plan=hc.REAL_PLAN`), `k4b_fresh.py:288-298` (`export`), `c2_registry.py:99, 132, 306, 350, 360` (`x6_source`, `token_sources`, `Registry`, `contains`, `separation`), `nd_registry.py:78, 106, 127, 210, 224-229, 283`, `hwsb_dry2.py:201-210`, `hwsb_stages.py:135-136`, `tools/c2_nd/API.md:230, 363-366`, `ah/jobs/0157/review.md:7` (R-0157-1) |
| Rules | `tp/CLAUDE.md` (public-summary prohibition; code index); `ah/planning/PLANNING_PROTOCOL.md` |
| Owner addenda | 25, 26, 28, 32, 33 (6e253f92…d1c6), 34 (7207564a…3941) in `ah/archive/owner-decisions-20261015/` |
| Protocols | K4B-FROZEN-v1 (957f0d5e…, read in full except §11.1–§11.3 detail tables skimmed); HWS-FROZEN-v1 (d9690609…; §0–§4.6, §6, §7, §8, §9, §10, §11, §12, §20 read); HWSB-FROZEN-v1 (db0db31a…; read in full) |
| Stage-B input | `hwsb-store/HANDOFF.json` (a4d9a0c9…4353), read in full |
| Stage-A records | `ah/jobs/0136/review.md`; `hws-store/SELECTION.json` hashed (243f7324…), not read beyond its hash |
| Stage-B execution records | `ah/jobs/0168`–`0174` `review.md` (all), `0172/task.md`, `0173/task.md` |
| K4b records | `ah/jobs/0055/report.md:63`, `0057/report.md:102`, `0057/review.md:53` (single lines) |
| Code (main af5e7b4) | `tools/k4b/{k4b_config, k4b_data, k4b_stats}.py` (full), `k4b_driver.py` (28–40, 100–240), `k4b_cert.py` (1–60 and signatures), `k4b_fresh.py`, `k4b_registry.py` (signatures), `k4b_scores.py`, `k4b_decoder.py`, `k4b_release.py`, `k4b_meter_bind.py` (grep lines); `tools/hwsb/API.md` (§0–§7), `hwsb_data.py` (140–200), `hwsb_config.py`, `hwsb_train.py` (grep lines), `hwsb_law.py`, `hwsb_registry.py`, `hwsb_records.py` (signatures), `CONTRACT.json` (head); `tools/c2_nd/CONTRACT.json` key `registry` |
| Code index | `--check`: current at af5e7b4 |
| Directory listings (names only) | `root/`, `scratch/` (hws/hwsb entries), `c2nd-store`, `c2nd-store/hist`, `hwsb-store/{artifacts, hist, stages}`, `k4b-store/stages` |
| Arithmetic | desk Python on literal numbers only (no repository code, no data): Z_bound decimal, registry values, CPU sums |

**Not read:** the public research-summary paths; `hwsb-store/REPORT.json`, `stages/EVAL/`, `GATES.jsonl`, `CHART_CONSTRUCTIONS_*.json`; `ah/jobs/0175/`; any `payload.npz`, `state.pt`, `sealed/` file, `hist/**` array or checkpoint payload (the HANDOFF file lists sha256 values of some payloads; those are recorded hashes, not the writer's access). No other output of this round was read.

**Pilot statistics.** The writer saw no stage-B pilot statistic. The stage-B job reviews read (0168–0174) contain CPU, identity and known-case values only (0173 and 0174 state "Dev CE not read"); stage-A oracle values (job 0136) are oracle design data, not pilot data, and are used only as [H] orientation, never as gates.

**Changes from the inputs.** Findings of this plan not in the inputs: (1) the copied-constant hazard of the K4b and HWSB modules and the binding audit (§3.2); (2) the stage-B dry re-run stores `hwsb-dry-0169` and `hwsb-dry-0171` outside HANDOFF's registry obligation (§3.4 R5); (3) `c2nd-store` has no frozen reader yet (§3.4 R2); (4) the lgate block raises the registry-risk sum above HANDOFF's `registry_value` formula (§3.4). The review added further findings (P1 seeds as default arguments; registry format and scale; planted-fixture and scratch coverage; deep-scan exclusions; `tests/k4b` constants), applied in v2.

---

## Change log v1 → v2

Base: v1 `coord-hws-stage-c-20261029.claude.md` (sha256 e7718bff…3f8e, unchanged). Every RC text below is the reviewer's replacement or insertion text, applied verbatim (RC-1..RC-13 accepted in `….rulings.md`). "Merge" records where two changes met in one place; "conforming" records a wording change elsewhere that only keeps the document consistent with an applied RC (no new content); "join" records a purely editorial join.

| Item | Where applied | Merge, conforming edit or join |
|---|---|---|
| Header | STATUS line; title HWSC-v2; new "Revision v2" paragraph | — |
| RC-1 (MAJOR) | §3.2 item 1 (`k4b_stats.SEEDS` removed from the table list; "Default arguments are not rebound" paragraph inserted after item 1); §3.2 item 3 (audit scans globals and `__defaults__`/`__kwdefaults__`, recursive; constants appended); §3.3 (`p1` moved to its own row "replaced by `hwsc_gates.p1c`"); §4 KC7(b) replaced; §5 row 10 P1 computation replaced; §7 DRC3 appended, DRC6 replaced | **Merge:** §3.2 item 5 carried v1's KC7(b) sentence; the KC7(b) replacement text was applied there too. **Conforming:** §3.1 row 15 mechanism now "`hwsb_gates.ladder_pilot` … via `hwsc_gates.p1c`"; §10.1 `hwsc_gates.py` row names `p1c`; §10.2 K4b-pipeline row no longer lists `p1`, `ladder`, `sd_upper`, `centered` as reused |
| RC-2 (MAJOR) | §3.3: rows for `reg1`/`kreg2_step` and `h2`/`h2_fresh` replaced by the two reviewer rows; the `k4b_registry.build` row and the sentence after the table replaced by the "Registry format (fixed now …)" paragraph; §7 DRC9 scale case appended; 12 GiB E1/E2 cap | **Merge:** the reviewer's two rows and RC-1's `p1` row and RC-9's `export` row combined in one §3.3 table; the remaining reused rows keep v1's text. **Conforming:** §5 row 3 (H2) and row 12 (H2-FRESH) name `hwsc_data.h2c`/`h2_fresh_c`; §8.3 memory-cap clause now states the fixed 12 GiB E1/E2 cap; §10.1 `hwsc_data.py` and `hwsc_registry.py` rows; §10.2 Registry row; §11 registry-cost risk row |
| RC-3 (MAJOR) | §3.4 R5 and R6 rows replaced; §4 new KC9 row; §8.2 KC row set to "KC0–KC9 … \| 1,500 \| 800–3,500 \| 4,500" and every cumulative column recomputed (cumulative central 3,300 / 9,306.6 / 11,306.6 / 13,327 – 15,047 – 18,487; cumulative 3× 9,900 / 27,920 / 33,920 / 39,980 – 45,140 – 55,460; totals ≈ 13,300 / 15,000 / 18,500 CPU-s) | **Conforming:** §5 KC gate row "KC0–KC9"; Summary "Gates" and "Cost"; §8.5 "a little under four hours"; §12 Q6 hours (3.7 / 5.1 CPU-h); §10.1 `hwsc_known.py` row. The v1 R5 "Finding" basis text is replaced by the reviewer's basis; the finding stays in §13 |
| RC-4 (MAJOR) | §3.4 R2, R4 and R8 rows: the reviewer's texts appended | — |
| RC-5 (MAJOR) | §4 KC8 Code cell replaced; §5 PF row computation ("`tests/k4b` unbound; the bound known cases of KC8 in `tests/hwsc`") | **Merge:** the PF row also carries RC-11. **Conforming:** §10.1 author-A list names `tests/hwsc/test_a_k4b_known_bound.py`; §10.2 K4b-pipeline regression cell |
| RC-6 (MAJOR) | §6.1 POSITIVE_BELOW_MARGIN bullet replaced; §6.2 POSITIVE_BELOW_MARGIN licence replaced; §7 DRC5 appended | **Conforming:** §12 Q4 states the RC-6 definition (as the rulings require) |
| RC-7 (MINOR) | §6.2 EXCLUSION, second sentence replaced | **Join:** the reviewer's text ends "In either case EXCLUSION" and v1's continuation began "it still does not establish"; joined as "In either case EXCLUSION still does not establish …" |
| RC-8 (MINOR) | §5 row 1 (H1-C) computation cell | — |
| RC-9 (MINOR) | §3.1 row 13 mechanism; §3.3 row `k4b_fresh.export` | v1's parenthetical "(`k4b_fresh.export` is not edited)" kept after the RC-9 text in §3.1. **Conforming:** §10.1 `hwsc_driver.py` row names `export_c` |
| RC-10 (MINOR) | §8.2 E2 row ("K-REG2 (cost R = KC9's measured registry CPU) … R + 1,720.1·k"); note after the table | v1's numeric E2 centrals kept, labelled "planning value with R = 300 [W]". **Conforming:** Summary "Cost", §11 registry risk row, §12 Q6 |
| RC-11 (MINOR) | §5 PF row "Job" cell | — |
| RC-12 (MINOR) | §8.5 sentence replaced | **Join:** the reviewer's text ends "These are estimates, not limits:"; v1's next sentence "This is counted separately …" continues in lower case after the colon. **Conforming:** "about three and a half hours" → "a little under four hours" (RC-3 cost change) |
| RC-13 (MINOR) | §10.1 paragraph inserted after the first paragraph | — |
| S1 (ruled ADOPTED) | §8.3 new bullet "Pause and hold reports (S1)": CPU, step and projection only, no gate value; gate statuses stay in `GATES.jsonl` | — |
| S2 (ruled ADOPTED, both parts) | §7 DRC1: dry-run registry cases on a synthetic root only; §9.3 new bullet: the R-0157-1 set-aside rule for `hwsc-dry*` stores (`ah/jobs/0157/review.md:7`, verified) | — |
| S3 (ruled ADOPTED, conditional) | §3.4 R2: C2ND `sequence_id` columns enter the frozen sequence-ID union if C2ND's API confirms the column per table; otherwise a known gap recorded in the registry record, not a failure | — |
| Provenance | §13: "v2 inputs" row with the newly verified code lines; closing sentence of "Changes from the inputs" | — |

No other text changed. The scientific design (estimand, completion, bootstrap, F, decision rule, levels, margin) is unchanged, as the review required.

## Design freeze candidate (coordinator, 2026-10-29)
HWSC-DESIGN-v1 = HWSC-v2 (80e99bc1…) with the confirmation read's V2-1, V2-2 and V2-3 applied verbatim and its optional §11 wording adopted (`coord-hws-stage-c-20261029.v2confirm.claude-reviewer.md`, a2abc799…, VERDICT: CONFIRM_AFTER_MINOR_FIXES; "no further review is needed before the design freeze candidate"). No other change. Owner questions Q1–Q6 (§12) go to the owner with their defaults; running stage C is not approved (addendum 34).
