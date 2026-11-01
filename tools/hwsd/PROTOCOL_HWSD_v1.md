STATUS: HWSD-DESIGN-v1: design freeze candidate (HWSD-v2 + F-1..F-4, J9, J10, suggestions)

# HWSD-DESIGN-v1: track D, when does the beyond-four information appear during training?

**Round:** `coord-hws-dyn-20261101`. Request `agent-handoff/planning/requests/coord-hws-dyn-20261101.md`, sha256 `1f8db403b1aafd9e7a8e1750b7397533905600d829efc394f7be243d65c44fca` (verified by the writer with `sha256sum` before reading). **Track:** L only (Codex frozen, addendum 28; PLANNING_PROTOCOL rule 5). **Writer:** clean-context Claude subagent of coordinator d9a66698, 2026-11-01.
**Revision v2.** It applies five inputs, each verified by `sha256sum` before reading:
- RC-1..RC-9 of the result-blind review `coord-hws-dyn-20261101.claude-reviewer.md` (sha256 5e2bc7eb…78df; VERDICT CONFIRM_AFTER_MINOR_FIXES), with the reviewer's replacement or insertion text verbatim and the refinements named in the rulings;
- the coordinator rulings `coord-hws-dyn-20261101.rulings.md` (184eb32f…8f5b), including S1–S9 as ruled;
- the joint rulings J1–J7 binding both tracks, `coord-hws-ud-20261101.joint-rulings.md` (641502e8…546f), and J8 of `coord-hws-ud-20261101.joint-rulings-addendum-1.md` (241040fb…c22b);
- the mailbox records `ah/records/HWSC_W2_END.json` (2390e29d…6cb) and `ah/records/HWS_UD_NAMESPACE.json` (b4c6d6ff…7b5e).

**Design freeze candidate.** HWSD-DESIGN-v1 = HWSD-v2 (`HWSD-v2.md`, sha256 28202282…824a, unchanged) with the following applied, each verified by sha256 before reading:
- F-1..F-4 of the confirmation read `coord-hws-dyn-20261101.v2confirm.claude-reviewer.md` (dd3b846b…086b; VERDICT CONFIRM_AFTER_MINOR_FIXES), with the reviewer's exact text;
- the rulings `coord-hws-dyn-20261101.v2confirm.rulings.md` (67216e08…03b9), whose four suggestions are adopted;
- joint ruling J9 (`coord-hws-ud-20261101.joint-rulings-addendum-2.md`, 6644433a…d9b5), in its symmetric form with t = `hwsd`, o = `hwsu`;
- joint ruling J10 (`coord-hws-ud-20261101.joint-rulings-addendum-3.md`, 127d08fe…c053c092; the reviewer's F-1).

Both G0s bind the sha256 of joint addenda 1–3. The changes are listed in the final section, "Change log HWSD-v2 → HWSD-DESIGN-v1". v1 is `coord-hws-dyn-20261101.claude.md` (07e5f761…6e97), unchanged. Every change is listed in the final section, "Change log v1 → v2". Track U's reserved tokens are read only from `HWS_UD_NAMESPACE.json` and treated as declared needles (J3).
**Authority:** owner addendum 37 (`OWNER_DECISIONS.addendum-37.md`, sha256 475f0540…a2a [V]): planning, result-blind review, design freeze candidate, implementation with independent tests and a synthetic dry run, up to an execution freeze. **No real-scope run is approved** by addendum 37 or by this plan: no draw of protected histories and no scoring of real checkpoints. Addendum 26 budget rules apply; no CPU line is set. **No training.**
**Base code:** topo-pilot main `8f894623900ce52dfea91db5e934dfb63f7c360c` (clean apart from untracked `.claude/`, `output/`, `research_audit_export/`, `tmp/`). `.venv/Scripts/python.exe tools/build_code_index.py --check` printed "code index is current" (exit 0) [V].
**Planning only.** The writer ran no sampling, training, test, driver, oracle or model computation, made no commit and changed no store. No `payload.npz`, `state.pt`, `sealed/` file, `hist/` array, `HIST_*.npz`, chart/activation array or checkpoint payload was opened or hashed. Stage-C training logs and per-step metrics were not read (provenance, §15, lists two accidental exposures, neither a per-step training metric). For v2, the writer read `hwsc-store/stages/TRAIN/OBS_INVENTORY.json` (relative paths and sha256 only) under the J1 blindness exception; nothing else under `stages/TRAIN/**` was opened. No file of the parallel round `coord-hws-use-20261101` and no `HWSU-*` file was opened. One file was written: this one.

**Labels.** **[V]** checked by the writer against code or a record (file:line, or JSON key). **[H]** an inherited record value. **[W]** the writer's desk arithmetic or design reasoning. **No [W] or [H] value is a gate threshold.** Every gated quantity is computed by the run; identity references (record hashes, HANDOFF and stage-C values) are read by the run at run time and compared exactly.

Paths: `tp/` = `X:/Downloads/projects/topo-pilot/topo-pilot` (main 8f89462); `ah/` = `X:/Downloads/projects/topo-pilot/agent-handoff`; `root/` = `X:/Downloads/projects/topo-pilot`; `scratch/` = `X:/Downloads/topo-scratch`; `hwsc/` = `root/hwsc-store`; `hwsd/` = `root/hwsd-store` (new). Protocols: **HWSC** = `ah/planning/responses/HWSC-DESIGN-v1.md` = `tp/tools/hwsc/PROTOCOL_HWSC_v1.md` (both sha256 f0f2396c…00a9 [V]); **K4B** = `ah/planning/responses/K4B-FROZEN-v1.md`; **HWSB** = `HWSB-FROZEN-v1.md`.

---

## Summary (≤ 300 words)

**Question.** Stage C found, at step 5000, that the gauged chart phase of each of three w\* models covaries with the beyond-four oracle residual r4 above the margin 0.01 (SUPPORT 3/3). Track D asks, over the 12 saved checkpoints per model (steps 0–5000), how this covariance evolves relative to learning (the captured context gain of the stage-C learning gate) and to chart formation (the stage-C chart gates).

**Design.** Descriptive and preregistered. For each of the 36 checkpoints: the stage-C chart rule on fresh calibration rows, the stage-C chart gates (C0-CAL, C0-VAL) as a registered chart status, the K4b estimand with support completion, the 5,000-draw joint bootstrap and the certified margin F (Z_bound equal to stage C), and the stage-C learning measure on fresh rows. One fresh scope `hwsd-v1` (13,312 rows: lgate 4,096, cal, val, test 3,072 each) serves all checkpoints, so comparisons across checkpoints are paired.

**Statements.** Each has an evaluation rule and readings TRUE / FALSE / NOT_EVALUABLE(reason):
- D1, final-step replication;
- D2, "no earlier than the chart": the owner's example, made falsifiable, and TRUE only with an INFORMATIVE pre-chart measurement;
- D3, "after the chart";
- D4, "after the learning landmark";
- D5, relative to the first checkpoint whose predictions beat every last-four predictor;
- D6, "no certified loss" on validated charts.

A circle already present at step 0 does not count as formed during training (CHART_AT_INIT). Readings that claim "some checkpoint" use Bonferroni-strength bounds: ranks 70 / 49,931 of a separate 50,000-draw bootstrap. There is no decision claim.

**Chartless checkpoints.** Every checkpoint gets a registered status (SCORED, SCORED_UNVALIDATED/<criterion>, CHART_UNAVAILABLE/<criterion>, UNCERTIFIED/<reason>); none is dropped, none is imputed, and each status enters the statements by a fixed rule (§5.5).

**Cost.** Scoring ≈ 4,100 CPU-s (1.1 CPU-h) central. With tests, the dry run, known cases, four expected test/dry repeats and one KD repeat, ≈ 9,750 CPU-s (2.7 CPU-h) [W from H]. 3× pauses per stage and cumulative.

---

## 1. The question

### 1.1 Where things stand
- **Stage C** (HWSC) trained three new E4-recipe models in w\* = W12-q1-s1.75-p0.2 (masters 620301–620303) and tested at step 5000, site `resid_post_3`, position 32, whether the gauged phase of the K4b-rule chart covaries with r4 = m32 − m4 above M = 0.01 for every completion of the unsupported rows. Outcome **SUPPORT** in 3/3 (`hwsc/stages/S8/RESULT.json` `outcome`, `overall` [V]; `ah/jobs/0196/review.md:8-22` [V]). Per-model L (rank 84 of X−) 0.04063, 0.03946, 0.04025; U (rank 4,917 of X+) 0.04758, 0.04543, 0.04689; Δ4^orc on the same rows 0.0473; fresh B4 0.151; N = 3,072 [V RESULT.json `per_model`, `N`; H for the review's rounded values]. Annotations INIT_UNAVAILABLE_620302 and INIT_UNAVAILABLE_620303 (RESULT.json `annotations` [V]).
- Stage C saved 12 checkpoints per model at steps 0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000 (every `hwsc/artifacts/Checkpoint/*/meta.json` `config.train_config.checkpoint_steps` [V]; 36 directories [V]). It scored only step 5000, plus a step-0 chart control.
- Stage A's oracle values at w\* [H, `ah/jobs/0136/review.md:5`]: G_C lower bound 0.2834 and G4 lower bound 0.03093. So a predictor that uses only the last four symbols already reaches captured ≈ 1 − 0.031/0.283 ≈ 0.89 [W]. **The stage-C learning landmark (captured ≥ 0.8) can therefore be reached by short-context learning alone.** This is why the plan adds a predictive beyond-four measure (§2.4 a) beside it.
- **Oracle feasibility (addendum 25 rule 1; S8).** Stage C's Δ4^orc on its test rows was 0.0473 ≈ 4.7× the margin [H]. The run's B4-TEST and the Δ4^orc control report it again on the hwsd test rows. No new feasibility stage is needed, because the world and process are unchanged.

### 1.2 What track D asks
For each model j ∈ {620301, 620302, 620303} and each saved checkpoint t, measure on fresh histories:
1. the stage-C beyond-four covariance of the chart phase, as the identified set [E X−_j(t), E X+_j(t)] with its certified bounds;
2. the stage-C learning measure, captured_j(t) = 1 − regret_j(t)/G_C, and the predictive beyond-four gain (HWSB's B2);
3. the stage-C chart gates, as a per-checkpoint chart status.

Then report, by preregistered rules, **how the covariance evolves relative to chart formation and to learning**. Track D is descriptive. It is not stage C, does not revisit stage C's decision, and is never pooled with stage C, K4b, stage B or any other study.

### 1.3 What the design can and cannot separate [W]
| Description of the trajectory | What discriminates it |
|---|---|
| T1 "the circle comes first, history later": the chart passes its gates while the covariance is still certified below 0.01, and later rises above it | D3 TRUE (ORDER AFTER in all models) |
| T2 "circle and history together": the first validated chart already carries it | ORDER WITH; D3 FALSE |
| T3 "history before a validated circle": an unvalidated proto-chart already carries it | ORDER BEFORE; D2 FALSE |
| T4 "learn the short context first, history later" | D4 TRUE (AFTER the learning landmark) |
| T5 "the circle carries it before / after the predictions use it" | D5 TRUE / FALSE |
| T6 a transient: present, then certified lost | D6 FALSE |
| T7 an initialisation artifact (an untrained network is a function of the whole history, K4B §9 item 3, line 596 [V]) | the step-0 checkpoint is a full row of every sequence; a validated chart at step 0 reads CHART_AT_INIT; σ at step 0 and the ORDER at k_C^+ are reported |
| T8 numerics, row reuse | certified F per checkpoint; fresh rows disjoint from every store (§4) |

It cannot separate anything finer than the checkpoint grid, and it says nothing about use (track U), mechanism, or other seeds and worlds (§8.3).

---

## 2. The design

### 2.1 Unchanged from stage C (by reuse of the frozen code)
- **Estimand and completion:** Δ4,j(t) = E[ũ·r4] with ũ = u on the supported set; the identified set [E X−, E X+], with X± = u·r4 on supported rows and ∓‖r4‖ on unsupported rows; every row kept, no support conditioning (K4B §1.2–§1.4, lines 108–159 [V]). Theorem A and Corollary A1 apply to any chart field frozen before the scored rows (K4B lines 146–155 [V]), so they apply to every checkpoint's chart.
- **Chart rule:** `c1_chart.fit_chart_lcc` with `k4b_config.chart_cfg()` unchanged (HWSC §2.5, line 111 [V]): PH over F47 on the 512 lowest-ID calibration landmarks, GIANT ≥ 487/512, exact integer lift, primitive class, smoothing ≤ 1e-8, production gauge fitted to m32 on the calibration landmarks, alignment finite and > 0 (`k4b_charts.py:65-88` [V]; `c1_chart.py:90-144` [V]); extension by 8 nearest charted landmarks, support iff resultant ≥ 0.2 and 8th-NN ≤ R (K4B §4.2, line 304 [V]).
- **Chart gates:** C0-CAL (the production construction above) and C0-VAL (a direct chart on the 512 lowest-ID validation rows, then `c1_chart.c0_val`: support ≥ 507/512, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30; `c1_chart.py:161-176` [V]).
- **Row certificate, Lemma N, B_num, F:** F_{j,s}(t) = max(B_num, 10⁻⁹) + Z_bound(w\*) in exact rationals (K4B §5.5, lines 372–394 [V]); cap 1e-4 and the P2 analogue |X̂| ≤ 4 (K4B line 363 [V]).
- **Bootstrap:** `c1_means.bootstrap_means` with 5,000 draws, one `rng.integers(0, n, n)` per draw shared by every array (`c1_means.py:31-43` [V]). Ranks 84 / 4,917 (one-sided α = 0.05/3), 125 / 4,875 (central 95 %), `k4b_stats.bounds` with rank checks (`k4b_stats.py:44-51` [V]; `k4b_config.py:51-57, 71-73` [V]).
- **Per-checkpoint status rule:** `k4b_stats.model_status` (SUPPORT iff L − F− > 0.01; EXCLUDE iff U + F+ < 0.01 and L − F− > −0.01; else UNRESOLVED, with UNRESOLVED/NUMERICAL and NEGATIVE_ALIGNMENT labels; `k4b_stats.py:61-76` [V]). **M = 1/100** (`k4b_config.py:58` [V]).
- **Site and inputs:** `resid_post_3`, index 32, BOS 36, float64 activations via `c1_model`; logits for learning by the stage-B float32 path (`hwsb_eval.model_predictive`, `hwsb_eval.py:70-73` [V]), never mixed with the float64 activations.
- **Controls (reported, never gated, never subtracted):** m4-phase null, SHA-of-suffix null, suffix decoder, Δ1, Δ2, Δ4^orc, naive completion (K4B §9, lines 590–617 [V]).
- **Learning measure:** `hwsb_eval.b1` (captured = 1 − mean KL(q32‖p)/mean KL(q32‖q1), `LearningGate(4/5)`; `hwsb_eval.py:88-105` [V]; HWSB line 151 [V]).

### 2.2 What changes, and why
| # | Change | Why |
|---|---|---|
| D-C1 | Objects: all 36 saved stage-C checkpoints instead of step 5000 only | the question |
| D-C2 | Scope `hwsd-v1`, store `hwsd/`, new seeds (§2.5) | stage-C scope and seeds are issued |
| D-C3 | The chart gates become a **per-checkpoint status**, not a cohort stop. A C0-CAL or C0-VAL failure at a checkpoint is recorded and scoring continues with the next checkpoint. Only FAIL_TECHNICAL in shared code stops the run | early checkpoints are expected to lack a chart (request) |
| D-C4 | A checkpoint whose production chart passes C0-CAL but fails C0-VAL is **still scored**, labelled SCORED_UNVALIDATED, and is never a chart onset (owner Q1) | without it, "beyond-four before the chart" is impossible by construction and the owner's example statement could not fail |
| D-C5 | The step-0 checkpoint gets the full treatment (production and direct charts, C0-VAL, estimand) like every other checkpoint. The K4b "init" control family is dropped, because step 0 is a row of the sequence | stage C ran step 0 as a production-only control on a separate ledger (K4B §4.3, lines 315–319 [V]) |
| D-C6 | Per-checkpoint construction ledgers: one `c1_chart.ConstructionLedger` file per checkpoint (≤ 2 claims: production, direct; never retried) | the class allows at most 6 claims per file and keys claims by `int(model)` (`c1_chart.py:21, 28-50` [V]); 36 checkpoints need 72 claims |
| D-C7 | Test size fixed at **N = 3,072** (one block), no precision ladder, no P1, no validation sealing, no CERT-VAL on validation rows | no decision and no N choice; the certificate that matters is on the scored test rows; stage C's N, so the step-5000 bands are comparable |
| D-C8 | All four blocks (lgate, cal, val, test) drawn in one job under one registry (K-REG-D) and checked pairwise disjoint | there is no release-B decision between validation and test |
| D-C9 | The B4 headroom guard moves from validation rows to the test rows (B4-TEST, run-level) | val rows carry no oracle work in track D |
| D-C10 | Added learning measure: HWSB B2 (predictive gain over the four-symbol oracle), per checkpoint, report-only plus statement D5 | §1.1: captured ≥ 0.8 is reachable with last-four information |
| D-C11 | No new estimand, chart parameter, margin, rank rule or tolerance. One new rank pair for existential readings only (§5.6): 70 / 49,931, from a separate 50,000-draw bootstrap of the 72 X± arrays (S2). The 84 / 4,917 bands are unchanged | multiplicity across checkpoints |

### 2.3 The 36 checkpoints (all; ids from `meta.json` [V])
| step | 620301 | 620302 | 620303 |
|---|---|---|---|
| 0 | 900fcd1d61111734 | 5badf5dec11c6087 | 05a201f784b64167 |
| 50 | 287fea7157944e1a | 73d24bcac17b6867 | 1f30c4d7cd8037d3 |
| 100 | f1cb8f6942eeea99 | ea353e05124dc136 | a180e77c1e8d2521 |
| 200 | 9ccd945c6130ca19 | af2d7d4fccdb1112 | 3b07606cba5ba113 |
| 400 | e5a51e752b40841d | 25e1148656beacd4 | 06cab8fad231b69c |
| 700 | e1b07bb29e63fc87 | f9577f908ec93557 | cc401bc627d21def |
| 1000 | 7148e1cf6a9fc2a4 | 5dcc7cd54265c820 | 851b783350db083f |
| 1500 | 511b88b0fbd4db33 | 2bc52ca12927fab4 | ae8d7ef312cc24bf |
| 2000 | 5e69bcc46cede2c6 | d7e002074d228f8d | b7e31d0fea9cf437 |
| 3000 | 478b6f5b58695bb7 | 22d9f24961239758 | 1646ecfc1cf277bb |
| 4000 | a8ac852658f59486 | 2cd5ed58eeaf2dba | c6ff3007a548bf22 |
| 5000 | a4cb0279bee92f52 | 71b118ba2c5e12cc | 69c86a578ae8c1bc |

Every `meta.json` has status `complete`, run key `["hwsc-v1", "W12-q1-s1.75-p0.2", master]`, and seed-map keys `init/…` and `batch_order/…` only. No metric field is present (key listing of `meta.json` and `extra.json` [V]). The implementation copies the 36 (master, step, id, `payload_sha256`) rows from `meta.json` into `tp/tools/hwsd/CONTRACT.json`. The run checks them against the stage-C TRAIN records (§3.2).

### 2.4 Per-checkpoint measures
For each (j, t), in this order inside the job of model j (production chart frozen before any validation or test activation of that checkpoint: the K4b "no peeking" order, K4B line 311 [V]):

**(a) Learning (lgate rows, 4,096).** p_j(t) = `hwsb_eval.model_predictive(ckpt, lgate, perm_j)`. q = `hwsb_eval.oracle_predictives(proc, lgate, Ks=(1, 4))` is computed once per run and gives q1, q4, q32 (`hwsb_eval.py:75-79` [V]).
- captured_j(t), regret_j(t), G_C from `hwsb_eval.b1(q, p)`, and the stage-C gate reading `captured ≥ 4/5` (equality passes). The gate is a **landmark here, not a stop**.
- B2: `hwsb_eval.forcing(q[32], q[4], p, z)` (`hwsb_eval.py:108-127` [V]), reported at HWSB's z = z_{1−0.05/4} ≈ 2.2414 (HWSB line 152 [V]) and at the strong z_S = z_{1−1/720} ≈ 2.9913 [W] used for the onset k_P (§5.2). The run computes z_S as `NormalDist().inv_cdf(1 − 1/720)`.

**(b) Chart formation.** Cal activations of all 3,072 cal rows, as in `k4b_driver.c0_cal_stage` (`k4b_driver.py:282-308` [V]).
- **C0-CAL:** `k4b_charts.build_chart(X_land, ids, m32_land, ledger_jt, j, "production", cfg)` (`k4b_charts.py:65-88` [V]).
- If C0-CAL passes, extend to the 2,560 non-landmark rows and fit the suffix decoder `k4b_decoder.fit(canon, ids, phase, j)`. Freeze the chart, gauge and decoder (`c1_chart.serialise`, sha256 into the checkpoint's FROZEN record).
- Then val activations of all 3,072 val rows, as in `k4b_driver.c0_val_stage` (`k4b_driver.py:311-321` [V]), and **C0-VAL** on the 512-row panel: the direct chart `build_chart(…, "direct")`, then `c1_chart.c0_val` (the `k4b_charts.c0_val_gate` body for one key, `k4b_charts.py:176-197` [V]).
- If C0-CAL fails, there is no direct chart, no decoder and no estimand.

**(c) Beyond-four estimand (test rows, 3,072),** whenever a production chart exists:
- test activations; `k4b_charts.extend`;
- `k4b_scores.endpoint_arrays` (X±);
- `secondary_arrays` (Δ1, Δ2), `naive_scores`, the decoder phase (`k4b_decoder.predict_phase`) and the decoder agreement (`k4b_decoder.agreement`);
- the row bounds `k4b_cert.endpoint_bounds` / `control_bounds`, then `k4b_cert.certify` (cap 1e-4, P2) (`k4b_cert.py:77-133` [V]);
- `k4b_scores.support_report` (sealed = False).

Arrays and maxima are written per checkpoint. Bounds are computed only in the SUMMARY job (§2.7).

**(d) Shared, once per run:** oracle moments m1, m2, m4, m32 on cal and test; Decimal references on all 3,072 test rows and 4 cal rows, with the moment check ≤ 1e-10 (`k4b_cert.references`, `moment_check`, `k4b_cert.py:38-53` [V]); m4-phase, SHA-of-suffix and Δ4^orc arrays (`k4b_scores.py:41-57` [V]); B4-TEST; q1, q4, q32 on lgate.

### 2.5 Histories, streams, scope, sizes (all new; drawn once, used for all 36 checkpoints)
KEY = `"W12-q1-s1.75-p0.2"`, PROC = `("cylinder", "overlap", "1.75")`.

| Block | Rows | Stream | Sequence IDs | Use |
|---|---|---|---|---|
| lgate b0 | 4,096 | `SeedTree(0).generator("data", "hwsd-v1", "lgate", 0, *PROC)` | `make_sequence_ids(process_code(*PROC, "hwsd-v1/lgate/b0"), "test", 4096)` | learning measures only |
| cal b0 | 3,072 | `SeedTree(0).generator("data", "hwsd-v1", "cal", 0, *PROC)` | `process_code(*PROC, "hwsd-v1/cal/b0")` | 512 lowest IDs = landmarks; 2,560 decoder rows; 4 Decimal reference rows |
| val b0 | 3,072 | same pattern, `"val"` | same pattern | 512-row C0-VAL panel only |
| test b0 | 3,072 | same pattern, `"test"` | same pattern | the estimand, controls, B4-TEST |
| DRY | small | `("data", "hwsd-dry-v1/<case>", …)` | — | `scratch/hwsd-dry*/` only (§10) |

Each block is one `HMMSampler.sample` call on the canonical emission, with w33 and the states dropped at once and rows ordered by sequence ID. This is `hwsc_data.block_generator(split, 0, scope="hwsd-v1", process=PROC)` and `block_ids(…)` with the scope passed explicitly (`hwsc_data.py:98-116` [V]); `sample_block_c` is not used because it takes the bound default scope. Tables use the K4b history-table format (`k4b_data.history_table`).

**Seeds (new; G0d checks that each is unissued):**
- k4b seed names under the binding: val_sd 620411, val_b4 620412, endpoint 620413 (the joint bootstrap), fresh_b4 620414 (B4-TEST), val_projection 620415. Only 620413 and 620414 of these are used; the others are set so that no stage-C or K4b seed remains bound.
- **Strong-bound bootstrap (S2): seed 620416.** The reviewer proposed 620413 + 1 = 620414, which is inside D's block but already used by fresh_b4. Per the ruling, the next free seed inside the block is taken.
- Decoder maps: `SeedTree(0).generator("hwsd-v1", "suffix_rbf_bw" | "suffix_rbf", master)`, the K4b decoder under the bound `k4b_decoder.SCOPE`. So every checkpoint of a model uses the same suffix-feature family.
- DRY: masters 629951–629953, seeds 629961–629965, scope `hwsd-dry-v1/<case>` (the dry scope of `HWS_UD_NAMESPACE.json`, J3).
- **Namespace reserved for track D** (`ah/records/HWS_UD_NAMESPACE.json`, J3; S9 satisfied):
  - scopes `hwsd-v1` and `hwsd-dry-v1`;
  - the store `hwsd-store`;
  - the globs `scratch/hwsd-dry*` and `scratch/test_hwsd-*`;
  - the seed blocks 620400–620499 and 629950–629999.

  Track U's reserved tokens (scopes `hwsu-of-v1`, `hwsu-v1`, `hwsu-dry-v1`; blocks 640101–640120 and 649901–649920) are declared needles in G0d (§4.3).

**Same rows for every checkpoint: right, with consequences [W].** Using one row set for all 36 checkpoints (and across the three models, as stage C did) is correct:
1. The rows are drawn independently of every checkpoint and before any is scored.
2. Each per-checkpoint estimand is a population quantity conditional on that checkpoint's frozen chart.
3. Nothing is selected after scoring.

The consequences:
- (i) Row-sampling noise is common to all checkpoints. Differences between checkpoints are therefore paired and more precise than with independent rows, and the joint bootstrap keeps this dependence because it resamples rows jointly for every array.
- (ii) The per-checkpoint bands are positively dependent. A whole trajectory can shift together, so agreement across checkpoints is not independent confirmation. Existential readings use Bonferroni, which is valid under any dependence.
- (iii) Every checkpoint's chart uses the same 512 landmarks, so differences between charts are conditional on one shared landmark set; landmark-set variability is not assessed.
- (iv) The statement anchors k_C (from cal and val rows), k_L and k_P (from lgate rows) do not use the test rows. A bound evaluated at an anchor is therefore a single pre-specified test (§5.6).

### 2.6 Per-checkpoint status (registered; never dropped, never imputed)
| Status | Condition | Estimand | Enters statements as |
|---|---|---|---|
| **SCORED** | C0-CAL PASS, C0-VAL PASS, test certificate PASS | reported, certified | a validated-chart checkpoint ("OK") |
| **SCORED_UNVALIDATED/<criterion>** | C0-CAL PASS; C0-VAL failed (direct chart GIANT, lift or smoothing, or support / fidelity / bins / resultant, with the failing criteria); certificate PASS | reported, labelled | pre-chart evidence for D2's BEFORE test only; never an onset; NA in every anchored reading |
| **CHART_UNAVAILABLE/<criterion>** | C0-CAL failed: GIANT_BELOW_0.95, unresolved lift, "not a cocycle", smoothing residual, NO_H1_BAR or other kernel Unresolved, or "gauge alignment not positive" (C1′ §14 taxonomy via `adapt_chart_exception`, K4B §4.4, line 323 [V]); also any other non-PASS construction status that does not start with FAIL_TECHNICAL, by the §7 row 9 mapping (RC-8) | none: there is no chart phase | "no chart, no estimand": cannot cross, cannot be an onset; counted and listed |
| **UNCERTIFIED/<reason>** | a production chart exists, but a primary test-row bound exceeds 1e-4 or the P2 analogue fails (INCONCLUSIVE/NUMERICAL in the K4b taxonomy) | values reported with the label "uncertified" | NA in every reading |
| FAIL_TECHNICAL/<reason> | non-finite phase, shared-code exception, identity, lineage or determinism defect | — | stops the run (§7) |

**Construction wall (RC-8).** Each construction runs with `timed = op_guard.timed_factory(<job dir>, 600)`. An operation that completes past the wall gives CHART_UNAVAILABLE/NATIVE_WALL (C0-CAL) or SCORED_UNVALIDATED/NATIVE_WALL (direct chart), never retried. If the supervisor kills a SCORE job during a construction, X-3 archives the attempt. The rerun records that (checkpoint, role) as …/NATIVE_WALL from the archived ledger claim and operation marker, without re-attempting it, and scores every other checkpoint.

Each row of the 36-row report carries: status; chart diagnostics (GIANT size, bar birth and death, components, lift kind, g, residual, gauge alignment; C0-VAL support, fidelity, bins, resultant); learning measures; and, when an estimand exists, point means, L, U, central 95 %, strong bounds, F±, status, labels, support fraction, width, missing mass, the controls and the decoder agreement.

### 2.7 No peeking before the summary (rule H-1)
- The three SCORE jobs write per-checkpoint arrays and records (hashed into STAGE_COMPLETE). Their printed output and the records the coordinator reads for acceptance carry **only counts per status, any FAIL_TECHNICAL, hashes and CPU** (S5): no per-checkpoint status list, no X± mean, bound, learning value or control value. The per-checkpoint chart statuses fix k_C, so they are value-bearing for D2 and D3; the per-checkpoint list stays in the unopened files.
- Learning values and arrays go to npz/JSON files that the coordinator does not open before the SUMMARY job. A recursive key check, the `k4b_stats.check_unsealed` pattern with a hwsd key list, refuses value keys in acceptance records (DRD10).
- All bounds, statuses, onsets and statement readings are computed only in the SUMMARY job.

**Why:** a technical correction to model 2's job must not be informed by model 1's values (the K4B §11.8 rule, extended by the stage-C S1 pause-report rule, HWSC line 362 [V]).

---

## 3. Binding to stage C

### 3.1 Identity references (bound in the hwsd CONTRACT now; compared exactly by G0d and H1-D at run time)
| Record | sha256 [V, writer's hash of the JSON or MD file] | Role |
|---|---|---|
| `hwsc/FREEZE.json` | 17c5b574…9800 | the stage-C execution freeze, final, equal to `ah/jobs/0196/review.md:6` |
| HWSC protocol (`PROTOCOL_HWSC_v1.md` = HWSC-DESIGN-v1) | f0f2396c…00a9 | equals RESULT.json `protocol_sha256` [V] |
| `hwsc/stages/S8/RESULT.json` | f2b8a678…7048 | Z_bound identity; D1 reference values (report only) |
| `hwsc/RELEASE_B.json` | 7a000410…7a79 | `train_records`: TRAIN record sha256 per master (D-0187-3) |
| `hwsc/STAGES.jsonl` | 8eb6cec9…596 | STAGE_COMPLETE hashes of the TRAIN records, S3/S7 tables, S4a charts |
| `hwsc/registry/K-REG2.json` | ff455ed3…bf99 | superset check of K-REG-D (§4.1 R9) |
| `root/hwsb-store/HANDOFF.json` | a4d9a0c9…4353 | Z_bound, F_plan, p_D2a, `stage_c_exclusions` |
| `tp/tools/hwsc/CONTRACT.json` | af669ac2…af88 | world ids, the reused registry tables |
| `hwsc/stages/TRAIN/OBS_INVENTORY.json` | bd385a96…11a8 [V], equal to `RELEASE_A.json` `obs_inventory_sha256` and to the `TRAIN_INVENTORY` STAGE_COMPLETE entry of `STAGES.jsonl` [V] | R9(a) `expected=`; read only through reader (b′) (J1); 51 entries: 6 ObservationSets × 3 files, `superseded/0181-a1/` 9 files, `superseded/0184-a1/` 24 files [V] |
| `ah/records/HWSC_W2_END.json` | 2390e29d…6cb (verified) | stage C's W2 reservation counts as ended (J2, RC-2) |
| `ah/records/HWS_UD_NAMESPACE.json` | b4c6d6ff…7b5e (verified) | both tracks' namespaces, history format, obligation rule and globs (J3) |
| `ah/planning/responses/coord-hws-ud-20261101.joint-rulings-addendum-1.md`, `-addendum-2.md`, `-addendum-3.md` | 241040fb…c22b; 6644433a…d9b5; 127d08fe…c053c092 (verified) | J8 (reservation end), J9 (declaration fragments), J10 (obligation contents; supersedes namespace rule 3 where they differ). Both G0s bind all three |

hwsc-store must not change during track D; J1: the stage-C obligation record is not written. G0d rehashes every row above and fails closed on any difference.

### 3.2 Checkpoint identity (H1-D, per checkpoint, metadata before any load)
For each of the 36 rows of the CONTRACT table:
- The TRAIN record `hwsc/stages/TRAIN/<j>/TRAIN_RECORD.json` must have sha256 equal to RELEASE_B `train_records[j]` and to its STAGE_COMPLETE entry (the `hwsc_gates.h1c` check, `hwsc_gates.py:95-103` [V]).
- It is read by a **key-whitelisting reader** that returns only `status`, `run_key`, `checkpoint_ids`, `checksums` and `process_ids`. `dev_ce` (`hwsc_driver.py:121` [V]) and every other key are dropped unread into memory and never logged (DRD9).
- The CONTRACT id and `payload_sha256` must equal the record's `checkpoint_ids[step]` and `checksums[step]`.
- `k4b_config.check_checkpoint_meta(meta, hwsc_gates.expected_meta_c(j, step, record))` must PASS (artifact id and type, run key `("hwsc-v1", KEY, j)`, step, status, init seed key and value; `hwsc_gates.py:52-58` [V]; `k4b_config.py:140-168` [V]), and the init seed must be equal across the 12 checkpoints of a master.
- None of the 36 ids may appear in HANDOFF `stage_c_exclusions` (`hwsc_gates.exclusion_check`, `:61-63` [V]).
- The checkpoint is loaded read-only: `ArtifactStore(LocalFSBackend(hwsc/artifacts)).load(Checkpoint, id, consumer="experiment")` verifies the stored checksum and writes nothing (`src/topo_pilot/contracts/store.py:185-199` [V]). Then `c1_model.load_model64` round trip exact.
- One torch thread.

### 3.3 The versioned binding `hwsd_bind` (no existing file edited)
The K4b modules hold copied constants (HWSC §3.2, lines 141–159 [V]). Track D reuses the stage-C mechanism: `hwsc_bind.bound_stage_c(table=<hwsd table>)` takes any table (`hwsc_bind.py:112` [V]), checks the old values, sets the new ones and restores them in `finally`. `hwsc_bind.audit(modules, left_unchanged, forbidden)` is parametrised (`hwsc_bind.py:247` [V]).

| Module.name | Old (K4b) | hwsd value |
|---|---|---|
| `k4b_config.{SCOPE, PROCESS, SEEDS, STORE, CONTRACT, CONTRACT_PATH, PROTOCOL_PATH, MODELS}` | K4b values | `"hwsd-v1"`; PROC; the §2.5 seed dict; `hwsd/`; a CONTRACT view whose chart section is byte-equal to K4b's (`check_chart_equality` equal); hwsd paths; `(620301, 620302, 620303)` |
| `k4b_data.{MODELS, PROCESS, SCOPE}` | K4b | as above |
| `k4b_stats.MODELS`, `k4b_fresh.{MODELS, SEEDS}`, `k4b_driver.{MODELS, SEEDS}` | K4b | as above |
| `k4b_driver.ARTIFACTS` | main `artifacts` | `hwsc/artifacts` (read-only loads) |
| `k4b_decoder.SCOPE` | `"k4b-sf-v1"` | `"hwsd-v1"` |

- **Left unchanged, with reason:** `hwsc_config.SCOPE = "hwsc-v1"`, because it is the run-key scope of the checkpoints and is used only for identity. The `k4b_stats.sd_upper` / `centered` default seeds, because they are never called (no P1).
- **Audit forbidden list:** the stage-C list (HWSC §3.2 item 3), plus the stage-C history seeds 620311–620315 and the paths `hwsc/stages/S3`, `hwsc/stages/S7` as data sources. The audit runs in PF, in the dry run and at the start of every job.
- **Never called under hwsd:** `k4b_driver.{g0, h1, reg1, h2, p1, c0_cal_stage, c0_val_stage, cert_val}`; `k4b_fresh.{sample_test, h2_fresh, t_pre, endpoint, export}`; `k4b_charts.{c0_cal, init_charts, freeze_production}`; `k4b_scores.control_arrays`; `hwsc_data.{sample_block_c, sample_lgate, sample_eval}`. Each of these either iterates over `MODELS` for one cohort, keeps one ledger per store, or takes a bound default scope.
- **Mirrors (each small, and bitwise-tested against the original on the step-5000 checkpoints under the stage-C binding in KD-REPRO and DRD14):**
  - `hwsd_score.chart_one`: the per-key bodies of `c0_cal_stage` and `c0_val_gate`, with the checkpoint ledger;
  - `hwsd_score.controls_one`: `control_arrays` for one key, without `init`;
  - `hwsd_score.arrays_one`: the per-key body of `t_pre`.

### 3.4 Process, law bound and F (equal to stage C)
- The process is built into `hwsd/artifacts` by `hwsc_data.build_process_c(store)` (= `hwsb_data.build_process`, `hwsc_data.py:33-34` [V]). `hwsc_data.process_identity` (`:37-56` [V]) checks the WorldSpec and TransitionSpec ids and payloads, the SELECTION sha256 and E_canon per master. The EmissionSpec ids must equal the record's `process_ids`.
- `Z_bound = hwsc_gates.law_identity(proc, handoff)` (`hwsb_law.law_bound(T, E, π, coords, 7/4, 1/5)`, BOUNDED and equal to HANDOFF `Z_bound`; `hwsc_gates.py:66-77` [V]). Track D adds: **equal to `hwsc/stages/S8/RESULT.json` `Z_bound`** = 87876736540276863476307541/78125·10³³ [V]. `k4b_cert.F_plan(Z_bound)` must equal HANDOFF `F_plan` exactly. F per checkpoint and side follows §2.1.
- `hwsc_data.p_d2a_check(proc, HANDOFF p_D2a)` must hold (rel ≤ 1e-12; `:236-239` [V]). The registry risk is 13,312 · p_D2a ≤ 1/100 in exact rationals; the desk value is 7.2e-11 [W].

### 3.5 Exposure of the reused checkpoints (what stage C opened, and what that affects)
- **Opened in stage C for representation analysis:**
  - step 5000 of each master: production chart on stage-C cal landmarks, C0-VAL, test endpoint (SUPPORT);
  - step 0 of each master: a production chart on the same landmarks (on the step-0 ledger, without C0-VAL); available for 620301, INIT_UNAVAILABLE for 620302 and 620303 (RESULT.json `init_qualifier`, `annotations` [V]); extended to the test rows for 620301.
  - L1 evaluated step 5000 on stage-C lgate rows.
- **Not opened for representation:** the 10 intermediate checkpoints. During training, dev CE was evaluated at every checkpoint (`hwsc_driver.py:121` `dev_ce` [V]); those values sit in the TRAIN records, the logs and the job 0187–0189 reviews, and the writer read none of them.
- **What the exposure does not affect:**
  - the validity of any hwsd measurement: fresh rows disjoint from every store, the estimand conditional on fixed weights, nothing tuned (§9.3);
  - the 10 intermediate checkpoints, whose representation nobody has measured.
- **What it does affect:**
  - **D1 is not blind.** The step-5000 SUPPORT is known, so D1 is a replication on fresh rows (same weights, new rows), not a prediction, and it carries no evidence about timing.
  - **The planners know that a step-0 production chart could pass C0-CAL** in one model (and that it was not above the margin, §15). This shaped the design: step 0 is a full row, and a validated chart at step 0 makes D2 and D3 NOT_EVALUABLE/CHART_AT_INIT for that model (§5.3 rule 1a, §5.4).
  - **The coordinator may have seen dev CE trajectories.** The statements are fixed here without them, and no hwsd quantity uses dev CE.

---

## 4. Registry and scope disjointness

### 4.1 K-REG-D (built in the SAMPLE job before any draw; fails closed)
**Mechanism:**
- `hwsc_registry_build.build` composes every source through a `sources=` dictionary that callers may replace (`hwsc_registry_build.py:34-52, 60-79` [V]). `hwsd_registry.build_d` calls it with version `"K-REG1"` into `hwsd/registry/inner/`, with these sources replaced:
  - `inventory` → the hwsd root table;
  - `scratch` → `hwsd_registry.scratch_check_d`, a mirror of `hwsc_scratch.scratch_check` with two changes. (i) `_row_for` also matches the pattern rows `hwsd-dry-<job>`, `hwsd-kd-<job>` and `hwsu-*`. (ii) The D-0178-1 dry type rule (`hwsc_drystore.check_store`) is applied, with the prefix `hwsd-dry`, to `hwsd-dry*` stores. (J3: the patterns are the globs of `HWS_UD_NAMESPACE.json`.)
  - `dry` → `source_dry()` ∪ `source_dry(paths=<hwsd-dry*>)`;
  - `own` → the composite R9 + R10.
- It then writes the wrapper record `hwsd/registry/K-REG-D.json`. The wrapper binds the inner manifest sha256 and states `registry_version "hwsd-reg-v1"` and the hwsd protocol sha256. The inner manifest's own `registry_version`/`protocol_sha256` fields name hwsc (`:132, :141` [V]); this is recorded as a known label, not a defect.
- **Why not a plain call:** `inventory_c` reads the stage-C table frozen at import (`hwsc_registry.py:28, 307-326` [V]) and drops `hwsc-store` (`:311` [V]).

| # | Source | Reader | Basis |
|---|---|---|---|
| R1 | Everything stage C's K-REG1/K-REG2 covered: C2ND rows 1–9, the K4b sources, the X6 base, `c2nd-store`, `hws-store`, `hwsb-store` (HANDOFF inventory) | the stage-C sources unchanged (`hwsc_registry_build.py:34-52` [V]) | K-REG2 PASS, 8,348,018 digests, inventory PASS (K-REG2.json `status`, `n_digests`, `inventory` [V]) |
| R5′ | Dry stores: `hws-dry`, `hwsb-dry*`, every `hwsc-dry*` (now `hwsc-dry-0177` … `hwsc-dry-0194`, names [V]) and every `hwsd-dry*` | `source_dry()` (globs `hwsc-dry*`, `hwsc_registry.py:149-152` [V]) plus `source_dry(paths=hwsd-dry*)`; planted fixtures of the hwsd dry run listed in the CONTRACT by path, size and sha256 | stage-C R5 rule |
| R6′ | Every other array file under `scratch/` | `scratch_check_d` (RC-1; the Mechanism bullet) against a **new frozen scratch inventory table** in the hwsd CONTRACT: the stage-C table (181 rows [V]) extended by every directory created since (`test_hwsc-0177…0194`, `hwsc-job-0181…0196`, `hwsc-dry-*`, …). The table is built at implementation by the read-only header scan (array headers only; no text file is opened) and reviewed before the freeze. Rows: `hwsd-dry` and `hwsd-dry-<job>`: READER_IF_PRESENT, reader R5′. `hwsd-kd-<job>`: READER_IF_PRESENT; KD writes no history-bearing, identity or `.pt` file, and any listed file → INCOMPLETE. `hwsu-*`: READER_IF_PRESENT, reader R10 | stage-C R6 |
| R8′ | Every top-level directory of `root/` | the hwsd root table = the stage-C table (68 rows [V]) with `hwsc-store` READER R9, `hwsd-store` OWN, `hwsu-store` READER_IF_PRESENT R10, `topo-pilot-hwsc-fix` and any other directory present at implementation listed with its decision; deep-scan exclusions = stage C's plus `hwsd-store` | an unlisted directory holding a history file, identity reference or ObservationSet root → INCOMPLETE (K4B lines 252–262 [V]) |
| **R9** | **`hwsc-store`** (new; stage C left no `REGISTRY_OBLIGATION.json` [V], and by J1 none is written; this layout reader covers the store, §4.4) | (a) the six ObservationSets by `hwsb_registry.registry_digests(hwsc, expected=<hwsc OBS_INVENTORY.json, sha256 bound by STAGES.jsonl TRAIN_INVENTORY>)`. (b) `stages/S3/HIST_{lgate,cal,val}_b0.npz` and `stages/S7/HIST_test_b0.npz` by the K4b history-table reader (canon32, seq_ids, digest; digest recomputed from canon32 as in `source_own`, `hwsc_registry.py:289-302` [V]), each file's sha256 equal to its STAGE_COMPLETE entry. (b′) `stages/TRAIN/OBS_INVENTORY.json` is read by a dedicated reader that returns only its relpath → sha256 map. Its sha256 must equal RELEASE_A `obs_inventory_sha256` and the `TRAIN_INVENTORY` STAGE_COMPLETE entry. (c) `superseded/**` read file by file with the same readers. (d) Classed non-history without opening a payload: `registry/**`; `stages/S4a/{CHART_*, INIT_CHART_*, DECODER_*}.npz` and `ACTS_cal_b0.npz`; `stages/S4/ORACLE_{cal,val}.npz` (oracle moment tables, hwsc API.md:294); every `payload.npz`/`state.pt` whose sibling `meta.json` names WorldSpec, TransitionSpec, EmissionSpec or Checkpoint, anywhere in the store, `superseded/<job>/artifacts/` included. These are not read as histories, but the files listed in OBS_INVENTORY are sha256-checked by `history_inventory` under (a), and the EmissionSpec parents of the ObservationSets are loaded for `symbol_perm` only (stage C's R7 behaviour). No Checkpoint payload is opened or hashed. (e) `stages/TRAIN/**` is listed by name only. `<m>/TRAIN_RECORD.json` is read only through the §3.2 whitelist reader and `OBS_INVENTORY.json` only through reader (b′). Any array file there is INCOMPLETE; other files are not opened. (e′) Any other array file, `tmp/**` included → INCOMPLETE. (f) **Superset check:** every digest of `hwsc/registry/K-REG2_digests.npz` must be in K-REG-D (missing → INCOMPLETE), and the S7 test digests must be present | own-lineage and fresh-block coverage of stage C |
| **R10** | **`hwsu-store` and the `hwsu-*` scratch directories** (track U), if present | `hwsu-store`: the obligation reader. Its closed classes are those of `HWS_UD_NAMESPACE.json` (J3): ObservationSet → `hwsb_registry.registry_digests`; K4b history table → the R9(b) reader. It reads every `REGISTRY_OBLIGATION*.json` present. The newest by `written_utc` must list every array file then in the store, each with relpath, sha256 and one class: **ObservationSet** or **K4b history table** (read as stated), or **NON_HISTORY** with one closed basis: (i) WorldSpec, TransitionSpec, EmissionSpec or Checkpoint by its sibling `meta.json` (a Checkpoint `state.pt`/`payload.npz` is classed by `meta.json` only, never opened or hashed); (ii) a file under `registry/**`; (iii) a chart, decoder, activation, oracle-moment, score, bootstrap or certificate array matched by a name rule frozen in the owning track's CONTRACT and copied into the obligation. NON_HISTORY files are checked by sha256 only. Present without an obligation, a sha mismatch, an unlisted array file, or an unknown class or basis → INCOMPLETE. (J10 item 1; the obligation names include `REGISTRY_OBLIGATION_OF.json` after track U's oracle-only stage, J6, and `REGISTRY_OBLIGATION.json` at study end.) Every top-level `hwsu-*` scratch directory (dry stores, job folders): the R5′ token reader `source_dry(paths=…)` file by file. ObservationSets are read canonically and spec or checkpoint payloads are classed by artifact type; an unreadable file → INCOMPLETE. **J4 refinement (replaces the reviewer's "No obligation is needed for these directories"):** each `hwsu-dry*` store must also carry its own `REGISTRY_OBLIGATION.json` in the closed format, written at the end of its dry run, and that obligation must list every array file the token reader finds; a `hwsu-dry*` store without one → INCOMPLETE, with no exception. `test_hwsu-*` roots are test roots (no history; skipped by the scratch scan as every `test_*` directory is) | the later registry covers the earlier store (§4.3) |
| R11 | hwsd's own blocks | not in K-REG-D; H2-D checks them against K-REG-D and pairwise | — |

**Fail-closed rules (unchanged from K4b, C2ND and stage C).**
- An unreadable, unlisted or unclassifiable history-bearing source makes the registry INCONCLUSIVE/REGISTRY_INCOMPLETE.
- NOT_SCANNED needs a recorded inventory reason.
- `sealed/` is never opened; a `state.pt` is never opened.
- The coordinator certifies completeness in the SAMPLE job's AUTH record.
- An INCOMPLETE registry stops the SAMPLE job **before any draw**. A contract erratum (table row) is reviewed, and the job is rerun under the technical-correction rule (§11.4). Because no row is drawn before the registry passes, track D runs no separate registry rehearsal (stage C's KC9); the cost is in §11.

### 4.2 Requirements (K4B line 268, extended to four blocks)
- U_lgate, U_cal, U_val, U_test are each disjoint from K-REG-D and pairwise disjoint.
- Sequence IDs are disjoint from every frozen union.
- Every row fails the sealed-D-2a predicate (`hwsc_data.separation_c` with four tables, `hwsc_data.py:166-188` [V]).
- A collision → FAIL_TECHNICAL/LINEAGE; a predicate hit → INCONCLUSIVE/REGISTRY_INCOMPLETE; no replacement sampling.

### 4.3 Track U: disjoint whichever runs first
1. **Namespace reservation (done: `ah/records/HWS_UD_NAMESPACE.json`, sha256 b4c6d6ff…7b5e; J3, S9).**
   - Track D holds the scopes `hwsd-v1` and `hwsd-dry-v1`, the store `hwsd-store`, the globs `hwsd-dry*` and `test_hwsd-*`, and the seed blocks 620400–620499 and 629950–629999.
   - Track U holds `hwsu-of-v1`, `hwsu-v1`, `hwsu-dry-v1`, `hwsu-store`, `hwsu-dry*`, `test_hwsu-*`, and 640101–640120 and 649901–649920.
   - Both G0s bind the sha256 of this record and of `HWSC_W2_END.json`.
   - G0d treats track U's tokens as declared needles in its whole-token search (`hwsd_known.seed_search_d`, the J5 mirror of `hwsc_known.seed_search_c`/`classify_hits_c`, `hwsc_known.py:51-75` [V]). **J9 (symmetric form, t = `hwsd`, o = `hwsu`):** a hit of **either track's** reserved tokens is a declaration if and only if its path contains one of these fragments:
     - **own:** `/tools/hwsd/`, `/tests/hwsd/`, `/agent-handoff/`, `/hwsd-store/`, `/coord-scratch/`, `/docs/code_index/`, `/topo-scratch/hwsd-dry`, `/topo-scratch/test_hwsd-`;
     - **the other track's declaration sites:** `/tools/hwsu/`, `/tests/hwsu/`, `/topo-scratch/hwsu-dry`, `/topo-scratch/test_hwsu-`, `/hwsu-store/`. Under `/hwsu-store/`, only its `REGISTRY_OBLIGATION*.json` and `reservations/*.END.json` files and its reservation files are searched; everything else there is pruned unsearched as blinded.

     Track U's round files under `/agent-handoff/planning/` stay on the blinded list and are pruned unsearched. A hit anywhere else is unclassified, giving FAIL_TECHNICAL/SEED_SCOPE.
   - Any overlap between the two tracks' reserved tokens **fails closed**. Track U's round files are pruned before any open (J5). The sequence-ID replicate strings `hwsd-v1/<split>/b0` and `hwsu-v1/…` differ, so the IDs differ by construction, and H2-D checks them anyway.
2. **Serial history generation.** Only one live history-generation reservation may exist at a time (the K4b W2 rule, K4B §3.5; `k4b_release.start_reservation`/`verify_reservation`, `k4b_release.py:124-143` [V]). Track D's reservation covers only the SAMPLE job. The SCHED record of that job must attest W2 (no live reservation of another study) and W3 (no other study holds a frozen registry awaiting a draw that would not include `hwsd-store`). If track U holds such a registry, track D does not draw until track U has drawn and written its obligation, or has rebuilt its registry.
   - **Stage C's live reservation (RC-2, J2).** Stage C left `hwsc-store/RESERVATION_W2.json` ACTIVE (`end_utc` null) and `RUN.lock` (job 0196); hwsc-store is not edited.
   - The coordinator has written the mailbox record `ah/records/HWSC_W2_END.json` (sha256 2390e29d…6cb). It holds the sha256 of `RESERVATION_W2.json`, `RUN.lock` and `OPERATION_ACTIVE.json`; "ended with S8 STAGE_COMPLETE 2026-10-30T00:30:48Z"; and the sha256 of the S8 RESULT and of `jobs/0196/review.md`. The hwsd CONTRACT binds it.
   - **W2 attestation (J8 item 4, both tracks).** A history-generation reservation counts as ended if and only if one of these holds:
     - (a) it is `RES-HWSC-W2` and `records/HWSC_W2_END.json` (sha256 2390e29d…) is bound and matches;
     - (b) an end record of schema `hws-reservation-end-v1` exists whose `reservation_sha256` equals the current reservation file's sha256 and whose `obligation_sha256` equals the current obligation file's sha256.

     Any other ACTIVE reservation is live, so the attestation is INCONCLUSIVE/AUTHORITY. This applies to W2 and §9.5.
   - **Ending track D's reservation (J8, replacing the reviewer's "rewrites only its own reservation file" clause).** A reservation file is never edited after creation. Track D ends its own reservation with `hwsd_data.end_reservation(store, reservation_id, utc, obligation_path)` (new code), called right after `hwsd/REGISTRY_OBLIGATION.json` is written.
     - It writes, by exclusive create, `hwsd/reservations/<reservation_id>.END.json` with the fields `schema` "hws-reservation-end-v1", `reservation_id`, `reservation_file`, `reservation_sha256`, `end_utc`, `obligation_file`, `obligation_sha256` and `written_by`.
     - It writes only after the obligation file exists.
     - It refuses when the reservation is not ACTIVE, when the obligation is absent, or when the end record already exists.
   - **Stopped drawing job (F-1 item 3, J10 item 3).** If SAMPLE stops after `start_reservation` and before its first row, it writes `hwsd/REGISTRY_OBLIGATION_<job>-a<k>.json` (no history file) and calls `end_reservation` with that obligation before exiting. A rerun starts a new reservation `RES-HWSD-W2-a<k+1>` in a new file. If the stop comes after the first row, it is a lineage stop (§7) and the obligation is still written before exit. The J8 end record binds the obligation of the job that drew (J10 item 2).
3. **The later registry covers the earlier store.**
   - If track U draws first, `hwsu-store` must carry its obligation record, and hwsd's R10 reads it (present without one → INCOMPLETE, no draw).
   - Every hwsd job that writes into `hwsd/` (KD, SAMPLE, SCORE, SUMMARY, including a stopped attempt) ends by writing, by exclusive create, an obligation listing every array file then in the store with the classes of R10: `hwsd/REGISTRY_OBLIGATION.json` for SAMPLE after sampling (J3, J8), `hwsd/REGISTRY_OBLIGATION_<job>-a<k>.json` for every other job and attempt.
   - Both tracks use the same closed-class obligation reader (J3).
   - **Order (J6).** Whichever track the owner approves first draws first. Track U's oracle-only stage (OF) is its own metered stage with its own freeze and approval, and it may come before both model phases. Its rows enter track D's registry through `hwsu-store/REGISTRY_OBLIGATION_OF.json` (R10).
   - **Dry stores (J4).** Each dry run (`hwsd-dry*`, `hwsu-dry*`) writes its own `REGISTRY_OBLIGATION.json` in the closed format at its end. A dry store without one is REGISTRY_INCOMPLETE for the other track. **J10 item 4:** dry stores follow J10 items 1–3. A dry run that aborts before writing its obligation is recovered by a recorded coordinator step: an obligation listing every array file present, written before any other track's registry build. Until then the dry store is REGISTRY_INCOMPLETE for both tracks.
4. **Inventory.** Both stores are listed READER_IF_PRESENT in the other's root table, together with both tracks' dry and test globs (J3). Any third new directory is unlisted, so it is INCOMPLETE if it holds history.

### 4.4 Finding: stage C left no obligation record (ruled by J1)
HWSC §9.3 (line 404 [V]) requires `hwsc-store/REGISTRY_OBLIGATION.json`; it is absent (store listing [V]).

**Ruling J1 (replaces v1's default; RC-9).** The coordinator does **not** call `hwsc_registry_build.obligation()` and does not write into `hwsc-store`. Calling it would hash ObservationSet and history-table payloads outside any authorised job and write into a closed store. Instead, track D's registry covers `hwsc-store` by its own layout reader (R9):
- the inventory is taken from `STAGES.jsonl` STAGE_COMPLETE entries and `stages/TRAIN/OBS_INVENTORY.json`, both sha256-bound;
- ObservationSets are read by `hwsb_registry.registry_digests(expected=OBS_INVENTORY)`;
- `HIST_*.npz` files are read by the K4b history-table reader (the `hwsc_registry.source_own` pattern);
- `superseded/**` is read file by file with the same readers;
- Checkpoint, WorldSpec, TransitionSpec and EmissionSpec arrays, `stages/S4/ORACLE_*.npz`, `stages/S4a/*` and `registry/**` are classed non-history by artifact type or by a frozen name rule, without opening;
- any other array file → REGISTRY_INCOMPLETE.

The superset check against `K-REG2_digests.npz` stays. Track D does not depend on the record, and the hwsd CONTRACT does not bind it. The gap is recorded in the joint rulings and in the stage-C round; it is not an outcome defect.

---

## 5. The registered summary statements

### 5.1 Notation (model j; checkpoint index k = 1…12 ↔ steps 0, 50, …, 5000)
- OK_j(k): status SCORED. EST_j(k): status SCORED or SCORED_UNVALIDATED (a production chart and a certified estimand).
- L_j(k), U_j(k): ranks 84 / 4,917 of the X− / X+ tree-mean draws of the main joint bootstrap (seed 620413, 5,000 draws).
- **Strong bounds** L^S_j(k), U^S_j(k) (S2): ranks **70 / 49,931** of a **separate 50,000-draw bootstrap** over the 72 X± arrays only. It uses `c1_means.bootstrap_means` (the same index rule) with seed 620416. The ranks are `c1_means.rank_for(1/720, 50000)` and `rank_for(719/720, 50000)`: ⌈50000/720⌉ = 70 and ⌈50000·719/720⌉ = 49,931 [W]. The run checks them at import, like `k4b_config.py:71-73`.
- F−_j(k), F+_j(k) as in §2.1.
- σ_j(k) = `k4b_stats.model_status(L, U, F−, F+)` if OK_j(k), else **NA**.
- ABOVE^S_j(k) := EST_j(k) ∧ L^S − F− > 1/100. BELOW^S_j(k) := OK_j(k) ∧ U^S + F+ < 1/100. Exact rationals, strict inequalities; equality is "not above" and "not below".
- ABOVE^S_OK_j(k) := OK_j(k) ∧ L^S − F− > 1/100. This is the validated-chart version used by D6 (S3).
- captured_j(k), B2 lower bounds at z and z_S.

### 5.2 Onsets (no tuning: the first index satisfying a fixed predicate)
- **Chart onset** k_C(j) = min{k : C0-CAL and C0-VAL PASS at k}, from the cal and val rows only. The stable onset k_C\*(j) = min{k : chart OK at k and at every later k} is reported, not used in statements.
- **Learning onset** k_L(j) = min{k : captured_j(k) ≥ 4/5} (the stage-C gate value, equality passes), from lgate rows only.
- **Predictive beyond-four onset** k_P(j) = min{k : B2 lower bound at z_S > 0}, from lgate rows only.
- Each is "undefined" if no k qualifies. **Reported only:** k_B(j) = min{k : σ = SUPPORT} and k_B^S(j) = min{k : ABOVE^S}, the first above-margin checkpoints at the per-checkpoint and strong levels.
- k_C^+(j) = min{k ≥ 2 : C0-CAL and C0-VAL PASS at k and not at k − 1} (the same gate predicate as k_C; suggestion adopted), the first validated chart that forms during training. When k_C = 1, the report gives σ at step 0 and the ORDER at k_C^+ (report-only, labelled 'chart present at initialisation'), and no statement uses them.
- **Onset-order line (S1; report-only, registered).** Per model, k_L vs k_C and k_P vs k_C, each read as <, = or > (or "undefined" if an onset is undefined). This gives the "relative to learning" half of the question a plain registered answer in every case.

### 5.3 ORDER classifications (per model; anchor A ∈ {chart: k_C, learning: k_L})
Evaluated in this order; the first match applies:
1. **NO_ANCHOR** if the anchor is undefined (NO_CHART for k_C; NO_LEARNING for k_L).
1a. **CHART_AT_INIT** if A = k_C and k_C(j) = 1 (step 0).
2. **BEFORE** if ∃ k < A with ABOVE^S_j(k).
3. If σ_j(A) = NA (S1 split):
   - **LEARNING_BEFORE_CHART** if A = k_L and no validated chart exists yet at k_L (k_C undefined or k_C > k_L);
   - **UNCERTIFIED_AT_ANCHOR** otherwise: the anchor checkpoint is UNCERTIFIED, or for k_L the chart is not OK at k_L although k_C < k_L.
4. **WITH** if σ_j(A) = SUPPORT.
5. **AFTER** if σ_j(A) = EXCLUDE and σ_j(12) = SUPPORT.
6. **NEVER** if σ_j(12) = EXCLUDE.
7. Otherwise (S6): **FINAL_NA** if σ_j(12) = NA (no validated chart, or uncertified, at step 5000); **UNRESOLVED** in every remaining case.

Also reported: n_pre(j) = #{k < k_C : EST_j(k)} (pre-chart checkpoints that could show BEFORE), and the maximum U^S + F+ over them.

### 5.4 Statements D1–D6
"All three" is required for TRUE; any per-model FALSE gives FALSE; everything else is NOT_EVALUABLE with the reason(s). Per-model readings are always published.

| # | Statement | Per-model rule | TRUE | FALSE | NOT_EVALUABLE (reasons) | Nominal error of a wrong reading [W] |
|---|---|---|---|---|---|---|
| **D1** | **Final replication.** On fresh rows, at step 5000, the chart phase carries beyond-four covariance above the margin | σ_j(12) | SUPPORT in all three | EXCLUDE in some model | UNRESOLVED, NA (no validated chart or uncertified at 5000) | false TRUE ≤ α per model (= stage C's SUPPORT level); false FALSE ≤ α per model |
| **D2** | **No earlier than the chart** (the owner's example). The covariance is not certified above the margin at any checkpoint before the first validated chart, and it is above the margin at the end | CHART_AT_INIT_j iff k_C(j) = 1. It is evaluated first and excludes TRUE_j and BY_CONSTRUCTION_j (FALSE_j cannot occur, since no k < 1 exists); the model then reads NOT_EVALUABLE/CHART_AT_INIT. TRUE_j iff k_C defined, not BEFORE, σ_j(12) = SUPPORT and n_pre(j) ≥ 1, with the qualifier INFORMATIVE iff some k < k_C with EST_j(k) has U^S_j(k) + F+_j(k) < 1/100 (exact rationals, strict), else UNINFORMATIVE. FALSE_j iff BEFORE. BY_CONSTRUCTION_j iff not BEFORE, σ_j(12) = SUPPORT, n_pre(j) = 0 | every model TRUE_j or BY_CONSTRUCTION_j, and at least one TRUE_j with qualifier INFORMATIVE | some model BEFORE | NO_CHART; CHART_AT_INIT (in that model); final not SUPPORT; BY_CONSTRUCTION in all three ("could not have failed": no pre-chart checkpoint had a chart phase); UNINFORMATIVE_PRE_CHART (no TRUE_j is INFORMATIVE) | false FALSE ≤ α per model (Bonferroni over ≤ 11 pre-chart checkpoints at 1/720 each), ≤ 0.05 over three. TRUE rests on the absence of strong pre-chart evidence: the report states n_pre and max U^S + F+ before the onset |
| **D3** | **After the chart (lag).** At the first validated chart the covariance is certified below the margin, and at the end it is above | ORDER at k_C | AFTER in all three | WITH or BEFORE in some model | NO_CHART, CHART_AT_INIT (in that model), UNCERTIFIED_AT_ANCHOR, NEVER, FINAL_NA, UNRESOLVED | false TRUE ≤ 2α (one false EXCLUDE at k_C or one false SUPPORT at 5000, intersection–union over models); false FALSE ≤ α per model per route |
| **D4** | **After the learning landmark.** When captured first reaches 0.8, the covariance is still certified below the margin, and at the end it is above | ORDER at k_L | AFTER_L in all three | WITH_L or BEFORE_L in some model | NO_LEARNING, LEARNING_BEFORE_CHART (no validated chart yet at k_L: then D3 and the onset-order line speak), UNCERTIFIED_AT_ANCHOR, NEVER, FINAL_NA, UNRESOLVED | as D3 |
| **D5** | **Circle no later than prediction (secondary).** When the model's predictions first beat every last-four predictor (B2 at z_S), the chart phase already carries the covariance above the margin | TRUE_j iff k_P, k_C defined, k_C ≤ k_P, σ_j(k_P) = SUPPORT. FALSE_j iff k_P defined and (k_C undefined or k_C > k_P or σ_j(k_P) = EXCLUDE) | all three TRUE_j | some FALSE_j ("prediction first") | k_P undefined; σ_j(k_P) = NA with k_C ≤ k_P (chart lost or uncertified); UNRESOLVED | false early k_P ≤ α per model (Bonferroni via z_S); σ at k_P ≤ α per side |
| **D6** | **No certified loss (validated charts).** No model shows a validated-chart checkpoint certified below the margin after a validated-chart checkpoint certified above it | LOSS_j iff ∃ k1 < k2 with ABOVE^S_OK_j(k1) ∧ BELOW^S_j(k2) (both sides on OK checkpoints, S3). FALSE_j iff LOSS_j. TRUE_j iff not LOSS_j and ∃ k1 < 12 with ABOVE^S_OK_j(k1). The same pair test with ABOVE^S on an unvalidated (EST-only) k1 is reported as the labelled diagnostic "EST-based loss", never a reading | all three TRUE_j | some LOSS_j | no strong crossing before step 5000 in some model (vacuous) | false FALSE ≤ 2α per model (one false strong bound on either side). TRUE means "no certified loss", not "monotone" |

### 5.5 How each checkpoint status enters the statements
- **SCORED:** everywhere.
- **SCORED_UNVALIDATED:** only in BEFORE (D2, and ORDER at either anchor), through ABOVE^S, and in D2's INFORMATIVE qualifier, through U^S + F+ < 1/100 (RC-5). It is never an onset, and σ = NA there, so it cannot make WITH or AFTER. It never enters D6, except in the labelled "EST-based loss" diagnostic (S3). Its curve values are reported with the label.
- **CHART_UNAVAILABLE:** has no chart phase, so it cannot be ABOVE^S or BELOW^S, and σ = NA. It is counted in n_unavailable and listed with its criterion. In D2 it does not count toward n_pre: the chart-phase covariance does not exist there, which is exactly why D2 has the BY_CONSTRUCTION reading. In D4, a learning onset before any validated chart gives LEARNING_BEFORE_CHART (S1).
- **UNCERTIFIED:** NA everywhere; reported with its label. If it falls at an anchor, the reading is UNCERTIFIED_AT_ANCHOR.
- **A validated chart at step 0 (k_C = 1):** D2 and D3 read NOT_EVALUABLE/CHART_AT_INIT for that model (RC-4). σ at step 0 and the ORDER at k_C^+ are reported, labelled 'chart present at initialisation'.
- **A chart lost after k_C** (OK, then not OK): k_C is still the first OK; the loss is shown by k_C\* and the status row.

### 5.6 Confidence levels and multiplicity
- **Per-checkpoint bands** (ranks 84 / 4,917; central 95 % at 125 / 4,875): nominal one-sided (1 − 0.05/3) percentile-bootstrap bounds for each (model, checkpoint). They are conditional on the weights, the chart and the gauge, as in K4B §8.3 (lines 538–546 [V]). **They are descriptive, with no family-wise claim over the 36 bands**, and the curves are drawn from them.
- **Anchored readings** (σ at k_C, k_L, k_P and at step 5000) use the per-checkpoint bounds. Each anchor is fixed by rows disjoint from the test rows (cal and val, or lgate) or by design (step 5000), so the bound there is a single pre-specified test conditional on the anchor. No correction is needed.
- **Existential readings over checkpoints** (BEFORE; D2's INFORMATIVE qualifier; D6 LOSS; the onset k_P) use the strong bounds at 1/720 per side. By Bonferroni over at most 12 checkpoints this gives a per-model family-wise level of 12/720 = 1/60 = 0.05/3 per side, valid under the dependence induced by the shared rows; over three models ≤ 0.05 per side.
- **Monte Carlo error of the strong bounds (S2).** The strong bounds come from the separate 50,000-draw bootstrap (ranks 70 / 49,931, seed 620416) rather than from rank 7 of the main 5,000 draws, so each sits on about 70 draws. The bootstrap seed is fixed. The 84 / 4,917 bands are unchanged. Seeds 620413 and 620416 give the 1/60 and 1/720 quantiles from different index streams, so L^S > L or U^S < U can occur by Monte Carlo near the boundary. Every such checkpoint is reported as a labelled diagnostic (suggestion adopted).
- **Statement level:** each statement carries the error statements in its table row. No correction is applied across the six statements. They are descriptive summaries of one data set, partly nested (D2 and D3 share k_C), and **they must not be counted as independent confirmations**.
- **Learning landmark:** captured ≥ 0.8 is read on point estimates, as the stage-C gate does; its sampling error is reported (regret SE, `hwsb_eval.b1` `regret_se`).
- **Expected magnitudes (orientation only, never thresholds) [W from H]:**
  - From stage C's step 5000 (U − L ≈ 0.0070 at full support), SE(X̄) ≈ 0.0016, per-row SD ≈ 0.09.
  - At full support: SUPPORT needs a point above ≈ 0.0135 and EXCLUDE a point below ≈ 0.0065; ABOVE^S needs ≈ 0.015 and BELOW^S ≈ 0.005.
  - Lower support widens [E X−, E X+] by 2·E[(1 − A)‖r4‖].
  - At step 5000, E X− / Δ4^orc ≈ 0.92 (RESULT.json `ratios` [V]).

### 5.7 Descriptive curves (reported for every model and checkpoint; no statement, no smoothing, no fitted curve)
- captured, regret and B2 (d̄, L at z and at z_S);
- chart status and diagnostics;
- support fraction, width and missing mass;
- the point means of E X− and E X+, L, U, central 95 %, strong bounds and F;
- E X−/Δ4^orc and E X−/B4 (`k4b_stats.ratios`);
- the decoder agreement and the decoder, Δ1, Δ2, naive, m4-phase and SHA controls with their certified flags;
- the "positive" annotation (L − F− > 0), the analogue of POSITIVE_BELOW_MARGIN, report-only;
- the onset-order line (k_L vs k_C, k_P vs k_C; S1), k_C^+ with σ at step 0 when k_C = 1 (RC-4), D2's per-model qualifier (RC-5), and the EST-based loss diagnostic (S3);
- the stage-C step-5000 values, labelled "stage C, other rows", beside the hwsd step-5000 row.

### 5.8 No decision claim
Track D registers **no** SUPPORT/EXCLUSION-type study verdict:
- stage C already answered the decision question;
- a new decision would need its own power plan, sealing and P1 gate;
- the request asks how the covariance evolves, which a decision cannot express.

D1 uses the stage-C rule at step 5000 as a replication reading. It is reported beside stage C, never as a second SUPPORT.

---

## 6. Known-case checks (addendum 25 rule 5)
Gating. KD runs as its own metered job after the execution freeze and the owner's run approval; the synthetic sequences also run in the dry run before the freeze (DRD4, DRD5). Any failure is **FAIL_TECHNICAL/KNOWN_CASE**: stop for coordinator review, with no tolerance or reference change after data (an owner decision is needed for that). References are read at run time from the cited records.

| # | Check | Code | Reference (run time) | Pass |
|---|---|---|---|---|
| **KD0 (G0d)** | Authority and freeze: addenda 25, 26, 37 and the owner's track-D run approval by sha256; the hwsd FREEZE; every §3.1 identity row. Scope and seed needles `hwsd-v1`, `hwsd-dry-v1`, 620411–620416, 629951–629953, 629961–629965 found in no earlier seed map, manifest or execution record (whole-token rule). Track U's reserved tokens from `HWS_UD_NAMESPACE.json` are declared needles, and the two reservations must not overlap (§4.3, J3). The sha256 of `HWS_UD_NAMESPACE.json` and `HWSC_W2_END.json` are bound. `hwsd/` must be absent or hold only this lineage's recorded files; W2/W3 SCHED record. Blinded paths are pruned before any open | `hwsd_known.seed_search_d`, a mirror of `hwsc_known.seed_search_c` whose only change is the prune predicate `hwsd_config.blinded` (the stage-C set plus the §9.2 paths and `ah/jobs/0187\|0188\|0189/review.md`), and `hwsc_known.classify_hits_c(hits, fragments=<the J9 list of §4.3 item 1: own /tools/hwsd/, /tests/hwsd/, /agent-handoff/, /hwsd-store/, /coord-scratch/, /docs/code_index/, /topo-scratch/hwsd-dry, /topo-scratch/test_hwsd-; other /tools/hwsu/, /tests/hwsu/, /topo-scratch/hwsu-dry, /topo-scratch/test_hwsu-, /hwsu-store/ (obligation, END and reservation files only)>, job_scratch=<CONTRACT list>)`, applied to hits of either track's tokens (J9 replaces the RC-7 fragment list) (J5: the blinded list includes track U's round files `*coord-hws-use-20261101*` and `HWSU-*`). G0d also binds the sha256 of joint addenda 1–3 | records | exact; unresolved hit fails closed |
| **KD1** | Checkpoint identity, metadata only, for all 36 rows (§3.2) | `hwsd_known.ident` (reuses `expected_meta_c`, `check_checkpoint_meta`, `exclusion_check`) | CONTRACT table; TRAIN records via the whitelist reader; RELEASE_B; STAGES.jsonl | exact |
| **KD2 (binding)** | (a) The identity table gives bitwise-equal results for every mirror and bound function on a synthetic fixture (HWSC KC7(a) pattern). (b) The hwsd table: audit clean; `k4b_data.history_generator("cal", 0)` equals `SeedTree(0).generator("data", "hwsd-v1", "cal", 0, *PROC)` for the first 64 draws and differs from the `hwsc-v1` stream; restore after exit | `hwsd_bind` | — | bitwise / exact |
| **KD3 (REPRO-C; the step-5000 result and the step-0 control)** | Inside the **stage-C binding** (`hwsc_bind.bound_stage_c()`, default table), the hwsd per-checkpoint scorer is applied read-only to stage-C data: the stored `hwsc/stages/S4a/ACTS_cal_b0.npz` activations, the S3 cal, val and S7 test tables, and the six step-0/5000 checkpoints. **S4:** the cal m32 used for the gauges is recomputed from the S3 cal table (`k4b_scores.oracle_moments`); stage C's `stages/S4/ORACLE_cal.npz` is not read. (a0) **Activation path:** the hwsd activation path on the six step-0/5000 checkpoints, applied to the S3 cal table, must be bitwise equal to the stored `ACTS_cal_b0.npz`. This is a run-time check; planners and test authors never open that file. (a) Refit charts: `CHART_j.npz` and `INIT_CHART_620301.npz` bitwise equal to the frozen stage-C files; 620302 and 620303 at step 0 give CHART_UNAVAILABLE with the reasons recorded in `PRODUCTION_FROZEN.json` `init_status`; decoders bitwise equal `DECODER_j.npz`. (b) C0-VAL at step 5000: per-model fidelity, support, bins and resultant equal the stage-C C0-VAL gate record (`hwsc/GATES.jsonl` gate C0-VAL, key `c0_val`). (c) Estimand: X± arrays on the S7 rows with the joint bootstrap (seed 620313, 5,000 draws) → L, U (ranks 84 / 4,917) bitwise equal RESULT.json `per_model.<j>.L`, `.U`; for 620301 at step 0, L and U equal `controls.init.620301` `alpha_bound` and `one_minus_alpha_bound`. F is not recomputed (no Decimal references); the certificate path is tested in DRD1 and DRD14 | `hwsd_known.repro_c` (opens only the stage-C files named; a write guard refuses any write under `hwsc/`) | RESULT.json; `PRODUCTION_FROZEN.json`; GATES.jsonl C0-VAL line; S4a chart and decoder files | bitwise / exact |
| **KD4 (SEQ)** | Synthetic checkpoint sequences through the real scorer and summary, on 3,072 in-memory w\* DRY rows (never persisted). The activations are planted, with fixed isotropic noise. (i) **No circle:** every row on a 1-dimensional segment in two of the 128 dimensions (position a fixed function of the row's sequence ID) plus isotropic noise ≤ 1e-6; expected CHART_UNAVAILABLE (NO_H1_BAR or GIANT). (ii) A circle in two of 128 dimensions carrying the m4 phase. (iii) The same circle carrying the m32 phase. (iv) **Unvalidated circle:** a full circle whose angle is the m32 angle pushed through a fixed monotone circle map g that puts about 1 % of the population mass into one 30° arc. g is chosen so that the production extension on the 512-row val panel leaves a phase bin with fewer than 8 rows. Expected: C0-CAL PASS, C0-VAL FAIL with criterion bins or resultant, and ABOVE^S. (v) **History-free circle:** a full circle with uniform angle independent of the history; expected C0-CAL PASS (alignment > 0 by construction), status SCORED, EXCLUDE. This documents that the gauge check does not screen out circles unrelated to the history. Sequences: **AFTER** (i, ii, ii, iii, iii), **WITH** (i, i, iii, iii), **BEFORE** (i, iv, iii, iii), **NEVER** (i, ii, ii), **NO_CHART** (i, i, i), and the **step-0 control** sequence (ii at step 0, then iii), which reads CHART_AT_INIT. F is planted as 10⁻⁹. Expected: (ii) point within ±4 SE of 0 and EXCLUDE (suffix-only field, Proposition 1); (iii) point within ±4 SE of the Δ4^orc mean on the same rows, SUPPORT; (i), (iv) and (v) as stated; the ORDER categories and D2/D3/D6 readings as named. The implementer fixes g, the noise scales and the seeds in the dry run (DRD4) and records the measured status of every case before the execution freeze. A case whose status under the unmodified chart code differs from its expectation is redesigned before the freeze, never after. If no planted fixture yields SCORED_UNVALIDATED through the unmodified chart code, the BEFORE route is checked by DRD5's planted status tables only, and §6 states that. | `hwsd_dry.seq_cases` | constructed | categorical exact; numeric ±4 SE |
| **KD5 (learning machinery)** | HWSC KC6 unchanged: the E4 test split regenerated in memory at w0, G_C equal to the recorded 0.2648737252067266; planted p = q32 → captured 1, p = q1 → 0, p = q4 → B2 d̄ = 0 | `hwsb_known` KB6 (reused) + a planted case | MetricRecords `37657d8490ba9e17` (HWSB line 135 [V]) | ≤ 1e-12 |
| **KD6** | K4b known cases at the hwsd constants: Proposition 1 by exact enumeration, Theorem A, Lemma N, the status boundaries, ranks 84/4,917/125/4,875 at 5,000 draws and the new 70/49,931 at 50,000 draws | `tests/hwsd/test_a_known_bound.py` (author A), run inside `hwsd_bind` | — | all pass |

**Not run (default):**
- Stage C's training reproductions KC2 and KC3 (no training in track D).
- KC9's registry rehearsal (the SAMPLE job builds the registry before any draw and stops on INCOMPLETE; §4.1).
- A recomputation of stage C's F, which would need about 700 CPU-s of Decimal references on stage-C test rows [W].

**Known cases inside the run (reported, as in K4b):** the moment check on every test row; the m4-phase and SHA-of-suffix population-zero nulls on the test rows, for every checkpoint's chart through the shared arrays; the step-0 checkpoint as the first row of every sequence.

---

## 7. Gates, frozen before any draw
**Convention.** Exact Fractions and strict inequalities, as in K4b. **Run-level** gates stop the run at the first non-PASS (later gates NOT_RUN). **Per-checkpoint** statuses (§2.6) never stop the run. Every computed value is reported. Jobs: one metered stage per job (§11.2).

| # | Job | Gate | Computation | Data | Pass reading | Tolerance | On failure |
|---|---|---|---|---|---|---|---|
| S0 | dispatch | BINDING | protocol sha256 = freeze record; request sha256; R_ref → H_exec diff over protected paths shows only allowlisted additions. Protected: `src`, `tools/{k4b, hwsb, hws, hwsc, c1prime, c1prime_registry, x4_circle_history, x4_oracle_profile, c2_nd, c2_readout, x6_stage1}`, their test directories, `tools/check_file_sizes.py`. Allowlist: `tools/hwsd/*`, `tests/hwsd/*`, `docs/code_index/*`. Every reused file's sha256 = the freeze table; chart section equal; `MARGIN == 1/100` | git, files | all hold | exact | INVALID: do not run |
| PF | J-D1 (once, bound in FREEZE; later jobs: S0 + audit) | PREFLIGHT | the stage-C PF suites unchanged + `tests/hwsc` + `tests/hwsd`; `tests/k4b` unbound; KD6 inside the binding; hwsd binding audit; file sizes ≤ 400 lines; `tempfile.gettempdir()` on X: inside a metered child; basetemps under `scratch/test_hwsd-<job>/` | code | all pass | — | INVALID |
| KD | KD | KD0–KD6 | §6 | §6 | all PASS | §6 | FAIL_TECHNICAL/KNOWN_CASE |
| 0 | SAMPLE | G0D | KD0 repeated at job start; AUTH names the stage and the coordinator's completeness certificate | records | all hold | exact | INCONCLUSIVE/AUTHORITY; FAIL_TECHNICAL on hash or seed defects |
| 1 | SAMPLE | **H1-D IDENTITY, LAW, F** | KD1 for 36 rows; process build and `process_identity` (EmissionSpec ids = TRAIN `process_ids`); `law_identity`: Z_bound BOUNDED, = HANDOFF `Z_bound` = stage-C RESULT `Z_bound`; `F_plan(Z_bound)` = HANDOFF `F_plan`; `p_d2a_check`; `c1_cert.a1_selftest()`; one thread | records, process | all hold | exact | FAIL_TECHNICAL/IDENTITY or /LAW_BOUND |
| 2 | SAMPLE | REG-D | K-REG-D (§4.1) incl. the R9 superset check | §4.1 | PASS | exact | INCONCLUSIVE/REGISTRY_INCOMPLETE (before any draw) or FAIL_TECHNICAL/LINEAGE |
| — | SAMPLE | sampling S3-D | W2 reservation verified; lgate, cal, val, test drawn (§2.5); tables saved and hashed; then `hwsd/REGISTRY_OBLIGATION.json`; reservation ended (`hwsd_data.end_reservation`) | — | — | — | reservation breach before the first row: cancel, rebuild; after: stop for lineage review |
| 3 | SAMPLE | H2-D SEPARATION | `separation_c(K-REG-D, {lgate, cal, val, test})`; registry risk 13,312·p_D2a ≤ 1/100 | 4 blocks | 0 collisions, 0 predicate hits, IDs disjoint | exact | FAIL_TECHNICAL/LINEAGE; INCONCLUSIVE/REGISTRY_INCOMPLETE |
| 4 | SAMPLE | ORACLE-D | m1, m2, m4, m32 on cal and test; Decimal references on all test rows and 4 cal rows; moment check | cal, test | every checked row ≤ 1e-10 | exact Fraction comparison | FAIL_TECHNICAL/ORACLE |
| 5 | SAMPLE | B4-TEST | `k4b_cert.b4_guard(r4n, max B_N, Z_bound, 620414, n)` (`k4b_cert.py:147` [V]) | test | PASS (certified one-sided 95 % lower bound of B4 > 0.01) | exact | INCONCLUSIVE/HEADROOM: curves still produced, statements not evaluated |
| 6 | SAMPLE | LGATE-ORACLE | q1, q4, q32 on lgate; rows sum to 1 | lgate | finite, sums within 1e-6 | 1e-6 | FAIL_TECHNICAL/NUMERICAL |
| 7 | SCORE_j (×3) | SCORE-IDENT | S0, audit; KD1 for the 12 rows of j; the SAMPLE records re-hashed against STAGES (`k4b_fresh.load_recorded` pattern, `k4b_fresh.py:306-316` [V]) | records | all hold | exact | FAIL_TECHNICAL/IDENTITY or /LINEAGE |
| 8 | SCORE_j | per checkpoint: LRN | §2.4 a | lgate | recorded (not a gate) | p rows within 1e-6; NaN → FAIL_TECHNICAL/NUMERICAL | — |
| 9 | SCORE_j | per checkpoint: CH-CAL, CH-VAL | §2.4 b, one ledger per checkpoint, never retried | cal, val panel | recorded status (§2.6) | inherited integer criteria; 1e-8 | the `k4b_charts.init_charts` rule (`k4b_charts.py:116-119`): a status starting with FAIL_TECHNICAL stops the run; every other non-PASS status (INCONCLUSIVE, INCONCLUSIVE/CHART_UNAVAILABLE, INCONCLUSIVE/RESOURCE) gives CHART_UNAVAILABLE/<status>: <reason> (C0-CAL) or SCORED_UNVALIDATED/<status>: <reason> (C0-VAL direct chart) |
| 10 | SCORE_j | per checkpoint: CERT | §2.4 c; cap B ≤ 1e-4 on every primary test row; \|X̂\| ≤ 4; finite phases in [0, 2π) | test | recorded status | cap exact | cap → UNCERTIFIED; non-finite → FAIL_TECHNICAL/NUMERICAL |
| 11 | SCORE_j | DETERMINISM | at job end, the cal activations of the first and last checkpoints with a production chart are recomputed bitwise | cal | equal | bitwise | FAIL_TECHNICAL/DETERMINISM |
| 12 | SCORE_j | H-1 RECORD | the acceptance record passes the no-value key check (§2.7) and carries only counts per status, any FAIL_TECHNICAL, hashes and CPU (S5) | records | no value key, no per-checkpoint status list | exact | FAIL_TECHNICAL/SEALING |
| 13 | SUMMARY | BOOTSTRAP | (a) one `joint_bootstrap` (seed 620413, 5,000 draws) over every array in the registered order (per model, checkpoint ascending: X−, X+, decoder, Δ1±, Δ2±, naive; then m4-phase, SHA, Δ4^orc), ranks 84/4,917/125/4,875; (b) the strong-bound bootstrap (S2): `c1_means.bootstrap_means` over the 72 X± arrays only (seed 620416, 50,000 draws), ranks 70/49,931. All ranks are rank-checked (`k4b_stats._q` pattern, `k4b_stats.py:34-41` [V]) | all arrays | finite, rank checks pass | exact ranks | FAIL_TECHNICAL/NUMERICAL |
| 14 | SUMMARY | STATEMENTS | B_num and F per checkpoint and side (`k4b_cert.b_num`, `margin`); σ; onsets; ORDER; D1–D6; the report (§8) | — | report written | exact | — |

**Stop rules:** the first non-PASS run-level gate ends the run with its outcome. A per-checkpoint status never ends it. A SCORE job's FAIL_TECHNICAL stops all later jobs until it is resolved under §11.4.

---

## 8. Outcomes

### 8.1 Report and technical outcomes (precedence)
| # | Outcome | Condition |
|---|---|---|
| 1 | FAIL_TECHNICAL/<reason> | KD failure (KNOWN_CASE), IDENTITY, LAW_BOUND, LINEAGE, ORACLE, DETERMINISM, NUMERICAL, BINDING, SEALING, BLINDNESS not resolved under §11.4 |
| 2 | INCONCLUSIVE/RESOURCE_OR_AUTHORITY | a 3× pause the owner does not continue, a lost process, a disk or memory safe-STOP, missing authority or a failed window precondition. If one or two SCORE jobs completed, their curves are reported as PARTIAL and every statement is NOT_EVALUABLE/RESOURCE |
| 3 | INCONCLUSIVE/REGISTRY_INCOMPLETE | REG-D or H2-D predicate (before or at sampling) |
| 4 | INCONCLUSIVE/HEADROOM | B4-TEST: curves reported, statements not evaluated |
| 5 | **HWSD_REPORT** | the 36-row table, the curves (§5.7), the onsets, the ORDER classifications, D1–D6 with their readings and reasons, the multiplicity and error statements (§5.6), the disclosure (§8.4) and the "does not establish" list (§8.3) |

### 8.2 Reading templates (filled at run time; plain words)
- **D2 TRUE:** "In each model, no checkpoint before the first validated chart showed a chart phase certified above the margin (n_pre = …; largest upper bound …). The covariance was above the margin at the end." (qualifier per model: INFORMATIVE / UNINFORMATIVE / BY_CONSTRUCTION)
- **D2 FALSE:** "In model …, at step … (before the first validated chart at step …), a chart that had not passed validation already carried beyond-four covariance certified above 0.01 at the strong level."
- **D3 TRUE:** "In each model, at the first checkpoint with a validated chart (steps …), the covariance was certified below 0.01, and it was above 0.01 at step 5000: at this checkpoint resolution, the circle formed before it carried the beyond-four information." A model whose validated chart is already present at step 0 is NOT_EVALUABLE/CHART_AT_INIT, because a circle present in the untrained network does not count as formed during training (RC-4).
- **D3 FALSE (WITH):** "In model …, the first validated chart (step …) already carried it above 0.01."
- **D4 TRUE:** "When captured first reached 0.8 (steps …), the covariance was still certified below 0.01; it rose above 0.01 later." Always add: "captured 0.8 can be reached with last-four information alone in this world."
- **D5 TRUE / FALSE:** "when the predictions first beat every last-four predictor (steps …), the chart phase already did / did not carry it."
- **D6 TRUE:** "No model showed a certified loss after a certified gain"; this does not mean monotone.
- **NOT_EVALUABLE:** name the reason and the models.

### 8.3 What the report does not establish (registered)
1. **Use.** No claim that the readout or the predictions use the beyond-four component of the chart phase, causally or otherwise; that is track U's question. D5 compares two onsets; it is not a use test.
2. **Training as a cause.** Checkpoints of one run are not independent experiments, and there is no counterfactual. Nothing about what training "causes" (K4B §8.4 item 6, line 568 [V]).
3. **Timing finer than the grid.** Timing is at the checkpoint grid 0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000 only. WITH means "within the same grid interval".
4. **Chart formation.** It is measured by the stage-C gate rule on these rows. "No chart" means the rule's gates failed, not that no circular structure exists. Beyond-four information outside the chart phase is not measured.
5. **Learning.** Captured ≥ 0.8 is a registered landmark, not a phase transition, and it is reachable with last-four information (§1.1). B2 is a normal-approximation lower bound.
6. **Population.** Three runs of one recipe in one world; not the training-seed population; not other worlds, sites, positions, layers, harmonics or the y-coordinate.
7. **Mechanism.** No claim about how the circle or the history dependence is computed.
8. **Simultaneity.** The 36 bands are not simultaneous. Curve shapes include shared-row noise, and the six statements are not independent confirmations.
9. **Unvalidated charts.** Their bounds are valid for that fixed field (Theorem A), but the field did not pass validation.
10. **Step 0.** An untrained network is a function of the whole history. Covariance at step 0 is not learned (K4B line 596 [V]).
11. **Earlier verdicts.** No new decision. Stage C's SUPPORT, K4b's EXCLUSION and every earlier verdict stand. D1 is a replication on fresh rows with the same weights, not a fourth model.
12. **D6.** No certified loss is not monotone growth.
13. **Licence conditions.** All bounds are nominal percentile-bootstrap statements conditional on weights, charts and gauges. The documented-law transport assumes idealised sampler draws (K4B line 552 [V]).

### 8.4 Disclosure carried by every report
"Track D follows stage C (SUPPORT 3/3 at step 5000 in w\*). It reuses stage C's 36 saved checkpoints; stage C had opened step 5000 and a step-0 chart control, and training had evaluated dev CE at every checkpoint. Track D's histories, charts and bounds are its own. No threshold, margin, chart parameter, rank rule or statement was set or changed in response to any stage-C quantity beyond the step-5000 result and the step-0 chart availability disclosed in its plan."

---

## 9. Blindness and hygiene

### 9.1 Roles
Planners, the implementer, the two test authors and the reviewers of track D read this plan, the reused code and its API/CONTRACT, the JSON records named in §3.1 and checkpoint `meta.json`. **J1 exception:** `hwsc/stages/TRAIN/OBS_INVENTORY.json` (file paths and sha256 only, no training metric) may be read by track-D planners, implementers and test authors. Everything else under `stages/TRAIN/**` stays blinded.

**They never open:**
- the public research-summary paths (`tp/00_READ_ME_FIRST_*`, `tp/docs/research_summary/`);
- `hwsc/stages/TRAIN/**` (except `OBS_INVENTORY.json`, J1), `hwsc/logs/**`, `scratch/hwsc-job-*/**`, and `ah/jobs/0187|0188|0189/review.md`;
- `hwsc/stages/E1/L1.json` and the L1 line of `hwsc/GATES.jsonl` (step-5000 learning values: not per-checkpoint, but not needed);
- any `payload.npz`, `state.pt`, `sealed/` file, `hist/` array or `HIST_*.npz`;
- the files of the parallel round `coord-hws-use-20261101` and `HWSU-*`;
- the stage-B blinded files (HWSC §9.2).

Prompts to them never quote these paths' contents.

### 9.2 Code guard
`hwsd_config` extends the stage-C path guard (`hwsc_config.blinded`, `guard`, `hwsc_config.py:161-203` [V]):
- the TRAIN directory except through the whitelisting TRAIN-record reader (§3.2);
- `hwsc/logs/**`; `scratch/hwsc-job-*/**`;
- the public-summary paths;
- the stage-B blinded set.

Any other open → FAIL_TECHNICAL/BLINDNESS (DRD9). The scratch header scan opens array files only, never text files. The TRAIN-directory guard exempts exactly two readers: the TRAIN_RECORD whitelist reader and the OBS_INVENTORY reader (b′). The blinded list also holds `ah/jobs/0187|0188|0189/review.md` (RC-7) and track U's round files `*coord-hws-use-20261101*` and `HWSU-*` (J5); the seed-search mirror `seed_search_d` prunes with this list before any open. Under `/hwsu-store/`, everything except its `REGISTRY_OBLIGATION*.json`, `reservations/*.END.json` and reservation files is pruned unsearched as blinded (J9).

### 9.3 No tuning on stage-C data
Unchanged from stage C:
- the chart cfg, gauge rule, site, position, ranks 84/4,917/125/4,875, α, M, the certificate cap and every tolerance;
- the learning gate value 4/5 and B2's z;
- N = 3,072, the stage-C value, chosen before any track-D data.

New and fixed here without data: the strong ranks 70/49,931 at 50,000 draws, z_S, the onsets, the ORDER rules, the D2 qualifier, CHART_AT_INIT and D1–D6. No stage-C activation, chart, bound or learning value informs any choice, except the disclosed step-5000 result and the step-0 chart availability (§3.5).

### 9.4 How track-D histories enter later registries
- `hwsd/REGISTRY_OBLIGATION.json` is written right after sampling and listed in the final report. It lists every array file of `hwsd/` with sha256 and R10 class (S3 tables as K4b history tables; everything else NON_HISTORY with its basis), names the dry stores (each carrying its own obligation, J4), and states 'fail closed'.
- Dry stores never use `HIST_*` names. Pytest basetemps and meter temp folders live under `scratch/test_hwsd-<job>/`.
- **J4:** every hwsd dry store (`hwsd-dry`, `hwsd-dry-<job>`) writes its own `REGISTRY_OBLIGATION.json` at the end of its dry run. It uses the closed format of `HWS_UD_NAMESPACE.json` as extended by J10 item 1: every array file, with its sha256 and class (ObservationSet, K4b history table, or NON_HISTORY with its basis). A dry store without one is REGISTRY_INCOMPLETE for track U. An aborted dry run is recovered by the J10 item 4 coordinator step.
- The stage-C set-aside rule for repeated dry runs applies (HWSC line 406 [V]).

### 9.5 Window
W2/W3 (K4B §3.5) apply to the SAMPLE job only (§4.3). Stage C's RES-HWSC-W2 counts as ended by `ah/records/HWSC_W2_END.json` (RC-2, J2). Every other reservation counts as ended only through the J8 item-4 rule (§4.3 item 2). In-memory w\* DRY rows (DRD2, KD4) are generated only when no other study holds a live history-generation reservation (HWSB §6.4 rule 2, line 231 [V]).

---

## 10. Synthetic dry run (addendum 25 rule 4; before the execution freeze)
The real `hwsd_driver`, binding, records, registry composition, per-checkpoint scorer, summary and report run end to end in `scratch/hwsd-dry/` (first run) or `scratch/hwsd-dry-<job>/` (repeats); meter temp roots and pytest basetemps are under `scratch/test_hwsd-<job>/`. They run under the DRY scope `hwsd-dry-v1`. This is the one dry location, `hwsd-dry*` (J3). Each dry run ends by writing its store's `REGISTRY_OBLIGATION.json` (J4). Persisted histories come only from synthetic tiny worlds; real-architecture and w\* cases keep their rows in memory. The dry run never issues a real-scope stream or seed, and never opens a real stage-C payload.

| # | Case | Expected |
|---|---|---|
| DRD1 | Full pipeline in the HWSB tiny world (W = 6, H = 2, L = 32): three tiny models (masters 629951–629953, 1 layer, d_model 16) trained 200 steps with checkpoints 0, 50, 100, 200 by `hwsb_train.train` under a dry plan. Then: registry on a synthetic root; SAMPLE (four blocks); H2-D; ORACLE-D with Decimal references; B4-TEST; three SCORE jobs; SUMMARY | runs; every record complete; every status and statement reading produced |
| DRD2 | Real E4 architecture: two 20-step checkpoints of one master on 2,048 in-memory w\* DRY rows through the scorer (logits path, activations, BOS 36, vocab 37/36, per-checkpoint ledgers) | shapes and identities valid; nothing persisted |
| DRD3 | Binding: identity table bitwise; hwsd table audit clean; planted leftover constants caught (`k4b_data.SCOPE = "hwsc-v1"`; a SEEDS value 620313; a function default 610101); restore after an exception | as stated |
| DRD4 | KD4 sequences (AFTER, WITH, BEFORE, NEVER, NO_CHART, step-0 control) and cases (i)–(v); g, the noise scales and the seeds are fixed here and every measured status is recorded before the freeze (RC-3) | as KD4 |
| DRD5 | Statement logic on planted per-checkpoint bound tables. Every ORDER category at both anchors; D1–D6 TRUE / FALSE / each NOT_EVALUABLE reason; BY_CONSTRUCTION in one, two and three models; equality cases (L^S − F = 1/100 exactly is not ABOVE; one ulp above is); k_C, k_L, k_P undefined; chart lost after k_C; UNCERTIFIED at an anchor; SCORED_UNVALIDATED never an onset; D6 vacuous; a seed-sensitive fixture confirms seeds 620413 and 620416 and the ranks 70/49,931 at 50,000 draws (S2). CHART_AT_INIT in one model with AFTER in the others → D3 NOT_EVALUABLE; with WITH in another model → D3 FALSE (RC-4). D2 qualifier boundaries: U^S + F+ = 1/100 exactly is UNINFORMATIVE (RC-5). D2 with CHART_AT_INIT in one model and TRUE/INFORMATIVE in the other two → NOT_EVALUABLE/CHART_AT_INIT (F-2). LEARNING_BEFORE_CHART vs UNCERTIFIED_AT_ANCHOR (S1); FINAL_NA vs UNRESOLVED (S6); D6 on OK checkpoints only, with an EST-only crossing giving the labelled diagnostic and not FALSE (S3); the onset-order line (S1) | exact |
| DRD6 | Ledgers: one file per checkpoint; production then direct; a second claim refused; C0-CAL failure → no direct claim and no estimand; 72-claim total for 36 checkpoints. RC-8: one case for each mapping of §7 row 9 — FAIL_TECHNICAL → stop; bare INCONCLUSIVE (kernel Unresolved, e.g. NO_H1_BAR), INCONCLUSIVE/CHART_UNAVAILABLE and INCONCLUSIVE/RESOURCE → CHART_UNAVAILABLE/<status>: <reason> at C0-CAL or SCORED_UNVALIDATED/<status>: <reason> at the direct chart; an operation past the 600 s wall → …/NATIVE_WALL; a killed construction recorded as …/NATIVE_WALL on rerun from the archived claim and marker, not re-attempted | as stated |
| DRD7 | Learning: p = q32 → captured 1; p = q1 → 0; 0.8 exactly is reached; p = q4 → B2 d̄ = 0 and L ≤ 0; z_S reproduces `inv_cdf(1 − 1/720)` | exact (≤ 1e-12) |
| DRD8 | Registry on synthetic stores: an R9-like store (ObservationSets, S3/S7 tables, superseded, registry digests, S4a charts and ACTS) passes. Fails closed: an unknown array in `tmp/` → INCOMPLETE; a K-REG2 fixture digest missing from the build → INCOMPLETE; R10 with a valid obligation → PASS; R10 store present without an obligation → INCOMPLETE; R10 unlisted file → INCOMPLETE; R10 unknown class → INCOMPLETE; an unlisted top-level directory with a history file → INCOMPLETE; `sealed/` never opened (access hook: zero opens). A store with the hwsc-store layout holding `stages/S4/ORACLE_*.npz`, `superseded/<job>/artifacts/EmissionSpec/<id>/{meta.json, payload.npz}` and `stages/TRAIN/OBS_INVENTORY.json` → PASS, with the spec payloads opened only by the (a) sha256 check and the EmissionSpec `symbol_perm` load, zero opens of any Checkpoint payload, and zero opens of TRAIN files other than the two allowed. A `hwsd-dry-<job>` repeat store, and a `hwsu-dry` store with no `hwsu-store`, → PASS. An unreadable array in a `hwsu-*` scratch directory → INCOMPLETE. J4: a `hwsu-dry*` fixture store without its own `REGISTRY_OBLIGATION.json` → INCOMPLETE (so the `hwsu-dry` PASS case carries its obligation); a `hwsu-store` fixture with `REGISTRY_OBLIGATION_OF.json` only → PASS if it lists every array file (J6). F-1, J10 item 5: a `hwsu-store` fixture whose newest obligation lists NON_HISTORY artifact payloads, `registry/**` files and named arrays → PASS; with one unlisted chart array → INCOMPLETE; a store holding only KD records and its KD obligation → PASS | as stated |
| DRD9 | Blindness: opens of a fixture TRAIN directory file other than through the whitelist reader, `logs/`, `hwsc-job-*`, public-summary paths → FAIL_TECHNICAL/BLINDNESS. The whitelist reader returns exactly its five keys from a fixture record that also holds `dev_ce`. The OBS_INVENTORY reader (b′) returns only the relpath → sha256 map and refuses a fixture whose sha256 differs from the bound value | as stated |
| DRD10 | H-1: a SCORE acceptance record with a value key (mean, bound, captured) is refused; the SUMMARY is the only writer of bounds | as stated |
| DRD11 | Records, rerun, budget: exclusive-create refusals; an interrupted SCORE job archived under `superseded/` and regenerated bit-identically (charts, arrays); per-stage and cumulative 3× triggers. J8 item 5 (replaces RC-2's test sentence): `end_reservation` ends an ACTIVE reservation; it refuses one that is not ACTIVE, one without its obligation, and a second call; the attestation treats a reservation without a valid end record as live, and a reservation whose file changed after its end record as live; the attestation accepts the other track's end record in this schema (fixture). SAMPLE stopped by REG-D INCOMPLETE ends its reservation with a no-history obligation; a rerun opens a new reservation id (F-1, J10 item 5). | as stated |
| DRD12 | Meter binding and placement: TEMP_ROOT and basetemps under `scratch/test_hwsd-<job>/`; one thread; `--max-cpu inf --max-wall inf`; output cap from the CONTRACT; disk safe-STOP precedence | as stated |
| DRD13 | G0d needles: planted true and false hits classified by the whole-token rule; an overlap with a fixture track-U reservation fails closed; a track-U token outside track U's declared locations fails closed (J3). A planted needle inside a fixture `stages/TRAIN/<m>/TRAIN_RECORD.json` and inside `hwsc-job-x/log.txt` is not reported, and the access hook records zero opens under them (RC-7); likewise inside a fixture `*coord-hws-use-20261101*` file (J5). J9 fixtures: own-token hits in a fixture `hwsd-store` freeze record, a `docs/code_index/files/tools/hwsd/*.md` page and a `tools/hwsu/CONTRACT.json`, classified as declarations; other-track-token hits in `tools/hwsd/CONTRACT.json`, classified as declarations; the same tokens in `topo-pilot/src/x.py`, unclassified | as stated |
| DRD14 | REPRO machinery on a stage-C **dry** store (a `hwsc-dry-*` case store, or a fresh hwsc DRC1 case generated under the hwsc dry binding): `repro_c` reproduces that store's charts and L/U bitwise; the mirrors `chart_one`, `controls_one`, `arrays_one` equal the K4b originals bitwise | as stated |

**Pass:** every expected result exactly. The report is committed, bound to the implementation hash, and accepted by the coordinator before the execution freeze.
**Cost:** ≈ 250 CPU-s central [W]. Stage-C DRY measured 121.5–142.1 CPU-s (`ah/HWSC_CPU_LEDGER.json`, jobs 0177–0194 [V]); DRD1's 12-checkpoint loop and DRD4's in-memory oracle add ≈ 100 s [W].
After the dry run, a read-only header inventory of `root/` must show no new history file, identity reference or ObservationSet root (stage-C rule).

---

## 11. Adaptive budget (addendum 26; addendum 37 item 7)

### 11.1 Measured basis [V, from `ah/HWSC_CPU_LEDGER.json` and `hwsc/registry/*.json`; H where inherited]
- **Stage-C E1** (job 0191): 1,578.2 CPU-s. Wall split from `hwsc/STAGES.jsonl` [V]:
  - REG1 325 s (23:11:19–23:16:44);
  - S4 (oracle moments on cal and val plus Decimal references on 3,072 val rows) 742 s (23:17:18–23:29:40);
  - S4a (six cal activation sets, six charts, three decoders) 71 s;
  - C0-VAL + CERT-VAL + P1 49 s.
- **Stage-C REG2:** 313.3 CPU-s (job 0195; an earlier attempt, 0192, 269.1 CPU-s). Registry build CPU inside the manifests: 290.97 (K-REG1) and 286.88 (K-REG2) [V `cpu_s`].
- **Stage-C E2** (job 0196, N = 3,072): 900.1 CPU-s, of which S7 → E2_GATES 849 s wall, dominated by the test-row Decimal references [W].
- **J-C1 preflight:** 559.8–604.0 CPU-s with the four standard labels; 1,048–1,173 with extra labels. **DRY:** 121.5–142.1. **KC:** 858.98 (job 0186).
- **Repeats in stage C:** 9 completed J-C1 + DRY pairs (jobs 0177, 0178, 0179, 0180, 0183, 0185, 0190, 0193, 0194) and one aborted (0182) [V ledger].
- **Desk per-checkpoint cost:** ≈ 70 s per checkpoint with a production chart (cal ≈ 17, val ≈ 10, test ≈ 38, lgate ≈ 5), ≈ 20 s per CHART_UNAVAILABLE checkpoint; ≈ 800 s per model [W from the stage-C shares]. The basis: stage-C per-model shares ≈ 37 s (E1) and ≈ 46 s (E2) beyond the shared oracle work, ≈ 70 s without CERT-VAL and P1.
- **Stage-C non-training CPU [W from the ledger, review RC-6]:** 13,023 s against a non-training forecast of about 5,500 s, about 2.4×. The ledger shows 11 J-C1 entries (one estimate, one abort), 9 DRY, 4 KC and 2 REG2 runs.
- **Strong-bound bootstrap (S2):** 50,000 draws × 72 arrays (3.6 M tree means plus the gathers) ≈ 200–250 CPU-s in SUMMARY [W]. This is the reviewer's estimate, adopted. It stays inside SUMMARY's 200–800 range, so the central (350) and the totals are not changed.
- **Decimal references** on 3,072 rows ≈ 700 s [W from the S4 wall time].

### 11.2 Stage forecast and 3× thresholds [W] (single thread, measure-only, never a cap)
| Stage (one job each) | Content | Central CPU-s | Range | Stage 3× | Cumulative central | Cumulative 3× |
|---|---|---|---|---|---|---|
| J-D1 | metered tests: stage-C PF suites + `tests/hwsc` + `tests/hwsd` + audit + sizes | 700 | 500–1,400 | 2,100 | 700 | 2,100 |
| DRY | DRD1–DRD14 | 250 | 120–600 | 750 | 950 | 2,850 |
| J-D1 + DRY repeats | expected after post-freeze code corrections: **4 pairs** central (stage C needed 8; hwsd reuses more frozen code) | 3,800 | 0–7,600 (0–8 pairs) | 11,400 | 4,750 | 14,250 |
| KD | KD0–KD6 (seed search ≈ 90; REPRO ≈ 150; SEQ ≈ 60; KD5 ≈ 20) | 450 | 250–1,000 | 1,350 | 5,200 | 15,600 |
| KD repeat | one expected repeat after a post-freeze correction | 450 | 0–900 | 1,350 | 5,650 | 16,950 |
| SAMPLE | G0d, H1-D (law bound), K-REG-D ≈ 320, sampling, H2-D, ORACLE-D (references ≈ 700), B4-TEST, lgate oracle | 1,350 | 900–2,700 | 4,050 | 7,000 | 21,000 |
| SCORE ×3 | 12 checkpoints each, ≈ 800 per model | 2,400 | 1,200–4,500 | 2,400 per model; 7,200 stage | 9,400 | 28,200 |
| SUMMARY | main bootstrap over ≈ 291 arrays × 5,000 draws ≈ 100–150; strong-bound bootstrap over 72 arrays × 50,000 draws ≈ 200–250 (S2; within this stage's range); statements and report | 350 | 200–800 | 1,050 | 9,750 | 29,250 |
| **Total** | | **≈ 9,750 CPU-s (2.7 CPU-h)**; scoring (SAMPLE + SCORE + SUMMARY) ≈ 4,100 (1.1 CPU-h); without repeats ≈ 5,500 (1.5 CPU-h) | | | | |

The scoring central is a little above the request's 'well under 1 CPU-h'; the test-row Decimal references (≈ 700 s) and the per-checkpoint test work are the largest items. (RC-6 gives a SUMMARY central of 200 and totals of 9,600 / 3,950 / 5,350; S2 adds 150 to SUMMARY, giving 9,750 / 4,100 / 5,500.) Before the run approval, the coordinator restates the forecast if J-D1, DRY or KD measured differ from these centrals by more than 20 % (cost only, not data).

### 11.3 Pauses, caps and ledger
- `--max-cpu inf --max-wall inf`; CPU is measured, never a stop. Disk floors C: ≥ 2 GB and X: ≥ 30 GB. Native-operation wall 600 s per operation (K4B §11.7).
- **Memory caps (CONTRACT):** J-D1 8 GiB; DRY, KD, SAMPLE 12 GiB (registry); SCORE 8 GiB; SUMMARY 8 GiB.
- **Output cap (CONTRACT `resources.output_cap_bytes`): 8 GiB.** The meter compares it with the whole out directory (stage-C defect D-0192-1, `tp/tools/hwsc/API.md:672-678` [V]). Sizing [W]:
  - K-REG-D digests ≈ 0.4 GB, with x6 runs ≈ 1.0 GB (stage-C K-REG1 sizes, API.md:673 [V]; `K-REG2_digests.npz` 395 MB [V listing]);
  - a superseded registry after one correction ≈ 1.4 GB;
  - process artifacts and tables < 0.01 GB;
  - per checkpoint, chart + decoder + arrays + cal activations ≈ 8 MB × 36 ≈ 0.3 GB;
  - total ≈ 3.2 GB, so 8 GiB leaves 2.5× headroom.
  - J-D1 writes under `scratch/test_hwsd-<job>/`; DRY writes its store as §10 states. KD writes its records into `hwsd/stages/KD/` (the stage-C KC pattern, job 0186) and writes no history-bearing, identity or `.pt` file. A `scratch/hwsd-kd-<job>/` directory is therefore not expected; R6′ keeps its fail-closed row. Each job runs with the same cap.
- **Per-stage trigger:** running stage CPU > 3× its central. **Cumulative trigger:** running total > 3× the cumulative central through the current stage. Both are checked at every item boundary (each KD check, each checkpoint, each gate).
- **On a trigger:** no new item starts and the coordinator reports in plain language; continuation needs the owner. If the owner does not continue → INCONCLUSIVE/RESOURCE_OR_AUTHORITY.
- **Pause reports** carry CPU, item and projection only, never a value (rule H-1).
- **Study ledger:** `ah/HWSD_CPU_LEDGER.json`, with unique labels `<job>-<stage>[-<master>]-a<k>` (the HWSB ledger-label lesson). It is never summed into another study's ledger.

### 11.4 Frozen extension rules
- **X-1.** Nothing grows on a scientific reading: chart statuses, learning values, bounds and statement readings never add rows, checkpoints, draws or models.
- **X-2.** N is fixed at 3,072. There is no ladder and no adaptive growth.
- **X-3.** Technical correction follows K4B §11.8 only:
  - a documented implementation or environment defect; at most two correction jobs per defect;
  - PASS stages stay immutable; superseded archive with SHA256SUMS; bit-identical regeneration;
  - **an owner decision if a correction would change an already computed value-bearing quantity** (chart status, learning value, any array or bound).
  - A valid failed chart construction is never re-attempted.
  - A SCORE job interrupted before its record is rerun from scratch; its already written charts and arrays must reappear bitwise.
- **X-4.** No threshold, tolerance, rank or statement rule changes after any track-D data.

### 11.5 Plain-language forecast for the owner (to be said when asking for the run approval)
"This one needs no training. We take the 36 snapshots that the last test saved while it trained the three models, twelve per model from the very start to the end. We look at each of them on about thirteen thousand new histories. For each snapshot we check three things: whether the model has learned to predict well yet, whether the circle has formed yet, and how much the circle carries from further back than the last four symbols. First comes a short set of checks that redo a piece of the last test exactly. The measuring itself should take a little over an hour of processor time. With the code tests, the practice run and their likely repeats, it comes to about three hours in all. These are estimates, not limits. If any part runs past three times its estimate, I stop and ask you. At the end I will tell you, for each model, when the circle appeared, when the information from further back showed up in it, and whether that came with the circle, after it, or after the model had already learned to predict well."

---

## 12. Reuse and footprint

### 12.1 New code: `tp/tools/hwsd/` (one new module; each `.py` ≤ 400 lines; no existing file edited)
Branch `hwsd-impl` from main 8f89462, in an existing listed worktree (`topo-pilot-hws`), with `PYTHONPATH=<worktree>/src` and the venv interpreter with `-s`. No `.npz`/`.npy` is committed. Implementation, tests and the dry run write no array file under `root/`.

| File | Contents | Lines [W] |
|---|---|---|
| `PROTOCOL_HWSD_v1.md` (byte copy of the frozen plan), `API.md`, `CONTRACT.json` (binding table, checkpoint table, seeds, identity rows, registry tables R6′/R8′/R10, resources), `TEST_PLAN.md` | committed first | — |
| `hwsd_config.py` | constants, scope, seeds, paths, CONTRACT loader, the TRAIN whitelist reader, the OBS_INVENTORY reader (b′), the blindness guard (§9.2, incl. J5 list) | ≈ 200 |
| `hwsd_bind.py` | the hwsd table on `hwsc_bind.bound_stage_c(table=…)`; audit lists | ≈ 120 |
| `hwsd_data.py` | blocks in scope `hwsd-v1`, H2-D, ORACLE-D, B4-TEST, lgate oracle, obligation record (store and dry stores, J4), `end_reservation` and the W2 attestation rule (RC-2, J8) | ≈ 250 |
| `hwsd_registry.py` | `build_d` via `hwsc_registry_build.build(sources=…)`; `scratch_check_d` (RC-1); R9 and R10 readers; superset check; wrapper record | ≈ 360 |
| `hwsd_score.py` | per-checkpoint scorer: identity, LRN, `chart_one` (ledger per checkpoint), freeze, C0-VAL, `arrays_one`, `controls_one`, certificates, determinism | ≈ 360 |
| `hwsd_summary.py` | joint bootstrap, bounds, σ, strong bounds, onsets, ORDER, D1–D6, report | ≈ 330 |
| `hwsd_known.py` | G0d with `seed_search_d` (RC-7, J5, J9 fragments), KD1, KD2, KD3 `repro_c` (with the S4 activation check), KD5, KD6 runner | ≈ 340 |
| `hwsd_driver.py` | jobs J-D1, DRY, KD, SAMPLE, SCORE, SUMMARY; records (stage-C `hwsc_records` functions reused: `preflight`, `run_gates_c`, `pause_or_raise_c`, `ledger_append`, `freeze_c` pattern); CLI | ≈ 340 |
| `hwsd_dry.py` (+ `hwsd_dry2.py` if needed) | DRD1–DRD14 and `seq_cases` | ≈ 380 + 200 |
| `hwsd_meter_bind.py` | thin main over `hwsc_meter_bind`'s pattern, hwsd caps | ≈ 100 |

About 2.8k lines [W]. Tests (≈ 1.4k lines) live in `tp/tests/hwsd/` and are written by **two independent authors**, neither of them the implementer, who never read `tools/hwsd/*.py`:
- **A:** onsets (incl. k_C^+ and the onset-order line); ORDER at both anchors (incl. CHART_AT_INIT, LEARNING_BEFORE_CHART, FINAL_NA); D1–D6 with every reading and reason (incl. the D2 qualifier and D6 on OK only); ranks 70/49,931 at 50,000 draws; z_S; the error-table arithmetic; learning measures; KD6 inside the binding (`test_a_known_bound.py`).
- **B:** the binding table and audit; scopes, streams and IDs; registry readers R9/R10, `scratch_check_d`, the superset check and fail-closed cases; dry-store obligations (J4); `end_reservation` and the W2 attestation (J8 item 5); the seed-search mirror and its pruning; the blindness guard, whitelist reader and OBS_INVENTORY reader; H-1; per-checkpoint ledgers; records and reruns; pauses; meter placement and caps.

`AUTHORSHIP_A.md` and `AUTHORSHIP_B.md`. No formatter over `tests/`. After acceptance, `.venv/Scripts/python.exe tools/build_code_index.py` and a separate `docs(index): …` commit (CLAUDE.md rule).

### 12.2 Six-field reuse assessment
| Part | 1 Existing (unchanged) | 2 Missing | 3 Smallest change | 4 Invariants | 5 Regression checks | 6 Next extension (not built) |
|---|---|---|---|---|---|---|
| Chart rule and gates | `c1_chart.{fit_chart_lcc, fit_production_gauge, serialise, extend_phase, c0_val, ConstructionLedger}`, `k4b_charts.{build_chart, extend, determinism_check}`, `k4b_config.chart_cfg` | a per-checkpoint loop; more than 6 constructions; non-stopping statuses | `hwsd_score.chart_one` (mirror of the per-key bodies) with one ledger file per checkpoint | one construction per (checkpoint, role), never retried; production frozen before val/test activations | KD3(a, b) bitwise vs stage C; DRD6, DRD14 | — |
| Estimand, certificate, controls | `k4b_scores.{endpoint_arrays, secondary_arrays, naive_scores, m4_phase, sha_phase, oracle_phase, phase_scores, support_report}`, `k4b_cert.{references, moment_check, endpoint_bounds, control_bounds, certify, b_num, margin, b4_guard, F_plan, envelopes}`, `k4b_decoder.{fit, predict_phase, agreement}` | per-checkpoint calls (`control_arrays` iterates `MODELS`) | `controls_one`, `arrays_one` mirrors | every row kept; cap 1e-4; F formula | KD3(c); DRD14 bitwise; `tests/k4b` unbound | — |
| Bootstrap and statuses | `c1_means.{bootstrap_means, rank_for, quantile_with_rank, rank_check, tree_mean}`, `k4b_stats.{joint_bootstrap, bounds, model_status, ratios}` | strong ranks; onsets; ORDER; statements | `hwsd_summary` (new logic only) | ranks rank-checked; exact Fractions; strict inequalities | KD6; DRD5 | a simultaneous max-type band only by a new protocol |
| Binding | `hwsc_bind.{bound_stage_c(table), load_table, check_old, audit(…)}` | the hwsd table and lists | `hwsd_bind` | restore in `finally`; old values checked | KD2; DRD3 | — |
| Data, process, law | `hwsc_data.{build_process_c, process_identity, block_generator, block_ids, separation_c, p_d2a_check}`, `k4b_data.{history_table, seq_disjoint, predicate_check, duplicates}`, `hwsc_gates.{law_identity, expected_meta_c, exclusion_check}`, `hwsb_law.law_bound` | explicit scope for four blocks | `hwsd_data` | one `sample` call per block; w33 never stored; Z_bound exact | KD1; H1-D; DRD1 | — |
| Learning | `hwsb_eval.{model_predictive, oracle_predictives, b1, forcing}`, `hwsb_known` KB6 | per-checkpoint loop; z_S | calls with `z` explicit | logits never mixed with float64 activations | KD5; DRD7 | — |
| Registry | `hwsc_registry_build.{build(sources=…), obligation}`, `hwsc_registry.{source_c2nd, source_hwsb, source_dry, source_own, scratch_check, _walk_arrays, _meta_type}`, `c2_registry.Registry`, `hwsb_registry.registry_digests`, `k4b_registry.{inventory, classify}`, `k4b_release.{start_reservation, verify_reservation}` | R9 (hwsc-store), R10 (obligation reader), extended tables, superset check | `hwsd_registry` | fail closed; never `sealed/`, never `state.pt` | DRD8; REG-D | the obligation reader as a shared component for track U and later studies |
| Records, meter, known | `hwsc_records.{preflight, run_gates_c, pause_or_raise_c, ledger_append, lineage_c, auth_ok, sched_ok, s0}`, `hwsc_known.{seed_search_c, classify_hits_c}`, `hwsc_meter_bind` pattern, `k4b_meter_bind`, job-0014 meter | hwsd stages and caps | `hwsd_driver`, `hwsd_meter_bind` | measure-only CPU; STOP/INVALID precedence | DRD11–DRD13 | — |

---

## 13. Risks (each with a registered default)
| Risk | Effect | Mitigation / default |
|---|---|---|
| Charts absent at most early checkpoints | D2 BY_CONSTRUCTION, ORDER mostly from late checkpoints | registered readings; D-C4 scoring of unvalidated charts; curves always reported |
| A chart already at step 0 (stage C's step-0 C0-CAL pass in 620301) | D2 and D3 read NOT_EVALUABLE/CHART_AT_INIT for that model; the ORDER at k_C^+ is reported | step 0 is a full row; BY_CONSTRUCTION reported; T7 in §1.3 |
| Low support at early checkpoints | wide identified sets, UNRESOLVED at anchors | widths reported, never gated (K4B F5); NOT_EVALUABLE reasons |
| Coarse grid (50 → 5000) | WITH absorbs short lags | §8.3 item 3; no interpolation |
| Copied constants left bound to stage C or K4b | wrong scope or seeds | hwsd binding audit in PF, DRY, every job; KD2 |
| Registry inventory drift (new scratch or root directories since the stage-C table; track U stores) | INCOMPLETE at SAMPLE | tables rebuilt at implementation and reviewed; failure before any draw; contract erratum |
| `hwsc-store` lacks its obligation record | uncovered stage-C lineage | J1: the record is not written; R9 layout reader + superset check (§4.4) |
| Track U concurrency | overlapping draws or uncovered store | `HWS_UD_NAMESPACE.json` (J3); serial W2 with `end_reservation`; obligation reader incl. `REGISTRY_OBLIGATION_OF.json` (J6) and dry-store obligations (J4); W3 attestation |
| Stage C's reservation still ACTIVE | W2 attestation impossible | `HWSC_W2_END.json` (RC-2, J2) |
| A slow chart construction at an early checkpoint | run stop by the native wall | RC-8 mapping to …/NATIVE_WALL per checkpoint |
| KD4 fixtures not giving their expected statuses | untested chart route | RC-3: statuses measured in DRD4 before the freeze; redesign before the freeze; DRD5 fallback |
| Output cap reached by the registry | killed job (D-0192-1 lesson) | 8 GiB cap sized in §11.3; X: floor unchanged |
| Strong-bound Monte Carlo variability (rank 70 of 50,000) | unstable strong readings near the margin | fixed seed 620416; stated in the report; only existential readings use it |
| Unvalidated-chart estimands over-read | overclaiming | label; used only for BEFORE; §8.3 item 9 |
| Leakage of dev CE or step-5000 learning values to roles | statements shaped by data | whitelist reader; path guard; §9.1 role list; H-1 |
| KD3 mismatch from environment drift | stop before scoring | FAIL_TECHNICAL/KNOWN_CASE; coordinator review; no tolerance change |
| Decoder fit fails at some checkpoints | missing control | "unavailable" (non-gating), as K4b |
| A SCORE job dies mid-way | partial arrays | X-3 rerun from scratch, bitwise regeneration of written files |
| D-statements read as independent evidence | overclaiming | §5.6 and §8.3 item 8 in every report |

---

## 14. Owner questions (science and risk only; each with a registered default)
1. **Scoring unvalidated charts.** Should a checkpoint whose circle passes the calibration test but fails validation still be measured, labelled, and used only to detect "history before a validated circle"? **Default: yes.** Without it, the statement "no earlier than the circle" cannot fail.
2. **Test size.** Keep 3,072 test histories, as in stage C, for every snapshot? **Default: yes.** Alternative: 6,144, at about +0.6 CPU-h, for sharper timing.
3. **Learning landmarks.** Use the stage-C learning gate (captured ≥ 0.8) as the learning landmark, and add "first snapshot whose predictions beat every last-four predictor" as a second landmark? **Default: yes** (both are reported; D5 is marked secondary).
4. **Re-opening stage C's step-0 and step-5000 snapshots** and stage C's histories for an exact reproduction check before measuring anything new (no new information). **Default: yes.**
5. **The six summary statements as written, and no decision claim.** **Default: yes.** Asked with RC-4 and RC-5 applied, in plain words: a circle already present in the untrained network does not count as formed during training. "Nothing before the circle" is claimed only when an earlier, unvalidated circle was measured precisely enough.
6. **Running track D.** Not approved (addendum 37 item 2). After the execution freeze the coordinator asks for an explicit run approval with the §11.5 forecast (about 1.1 CPU-h of measuring, about 2.7 CPU-h with tests and repeats; 3× pauses). **Default: no run until the owner says so.**

J7: the defaults stand as registered, and the coordinator asks the owner at the run approval, in plain language.

**Decided by the coordinator (procedural, registered here; J1–J6 under the owner's standing "keep running" instruction):**
- the namespace reservation with track U (done: `HWS_UD_NAMESPACE.json`, J3) and the order of the runs (J6: whichever track the owner approves first draws first; never concurrently; track U's oracle-only stage may come first, with its own approval);
- `hwsc-store/REGISTRY_OBLIGATION.json` is not written (J1; not a track-D precondition), and stage C's W2 reservation is ended by the mailbox record `HWSC_W2_END.json` (J2);
- the worktree and branch; the study ledger `ah/HWSD_CPU_LEDGER.json`;
- the seeds 620411–620416 and DRY 629951–629965; the output cap;
- the completion of the registry tables at implementation as a reviewed contract erratum.

---

## 15. Provenance
| Input | Identity |
|---|---|
| Request | `ah/planning/requests/coord-hws-dyn-20261101.md` sha256 1f8db403…4fca (verified) |
| Rules | `tp/CLAUDE.md` (public-summary prohibition; code index); `ah/planning/PLANNING_PROTOCOL.md` (aca4dedd…49c1) |
| Owner addenda | 25 (22f13022…37f4), 26 (23ab23f9…f602), 37 (475f0540…a2a) in `ah/archive/owner-decisions-20261015/` |
| Model of depth and style | `ah/planning/requests/coord-hws-stage-c-20261029.md`; `ah/planning/responses/HWSC-DESIGN-v1.md` (read in full) |
| Protocols (sections) | K4B-FROZEN-v1 §1.2–§1.4 (lines 102–159), §4 (284–335), §5.1–§5.6 (338–411), §8 (514–586), §9 (590–617); HWSB-FROZEN-v1 by search only (lines 22, 67, 74, 106, 115, 118, 129–138, 151–153, 185–189, 213, 231, 245–262) |
| Stage-C execution records | `ah/jobs/0186, 0187, 0190, 0191, 0192, 0193, 0194, 0195, 0196/task.md`; `ah/jobs/0196/review.md`; `hwsc/stages/S8/RESULT.json` (read); `hwsc/STAGES.jsonl` (stage names, events, utc and key names only); `hwsc/registry/K-REG1.json`, `K-REG2.json` (status, counts, cpu, inventory, source summaries); `hwsc/FREEZE.json`, `RELEASE_B.json`, `STAGES.jsonl`, `CONTRACT.json` hashed only; checkpoint `meta.json` (all 36: id, master, step, status, `payload_sha256` prefix, `created_utc`) and one `extra.json` (keys only); `ah/HWSC_CPU_LEDGER.json` (CPU entries) |
| Other records | `ah/jobs/0136/review.md:1-30`; `root/hwsb-store/HANDOFF.json` hashed only |
| Code (main 8f89462) | `tools/hwsc/{hwsc_driver.py (full), hwsc_gates.py (full), hwsc_registry.py (full), hwsc_registry_build.py (full), hwsc_data.py (25–245), hwsc_bind.py (1–120 and signatures), hwsc_config.py, hwsc_scratch.py, hwsc_drystore.py, hwsc_known.py, hwsc_records.py, hwsc_jobs.py, hwsc_outcome.py, hwsc_meter_bind.py (signatures), API.md (headings, §28 lines 672–678), CONTRACT.json (top-level keys, masters, seeds, sizes, resources, registry key summary, cpu)}`; `tools/k4b/{k4b_driver.py (137–376), k4b_fresh.py (1–345), k4b_stats.py (full), k4b_config.py (full), k4b_charts.py (full), k4b_data.py (60–110), k4b_scores.py (120–159, signatures), k4b_cert.py, k4b_decoder.py (signatures, 40–70), k4b_release.py (signatures)}`; `tools/c1prime/c1_chart.py (1–27, 68–177)`, `c1_means.py (15–69)`; `tools/hwsb/hwsb_eval.py (1–30, 70–140)`, `hwsb_config.py`, `hwsb_registry.py` (signatures), `tools/hws/hws_oracle.py:72-75`; `src/topo_pilot/contracts/store.py:185-214`; code index page for `tools/hwsc/hwsc_jobs.py` (header) |
| Code index | `--check`: current at 8f89462 |
| Directory listings (names only) | `root/`; `hwsc/` and its `registry/`, `stages/{S3, S4a, S5, S7, S8, E1, E2, KC}`, `superseded/`, `logs/` (file names only), `artifacts/Checkpoint/`; `scratch/` (names matching hws\*, and the count) |
| v2 inputs | review `coord-hws-dyn-20261101.claude-reviewer.md` (5e2bc7eb…78df), rulings `coord-hws-dyn-20261101.rulings.md` (184eb32f…8f5b), joint rulings `coord-hws-ud-20261101.joint-rulings.md` (641502e8…546f), records `ah/records/HWSC_W2_END.json` (2390e29d…6cb) and `ah/records/HWS_UD_NAMESPACE.json` (b4c6d6ff…7b5e): all hashes verified and all read in full. `hwsc/stages/TRAIN/OBS_INVENTORY.json` (bd385a96…11a8) read under J1 (51 relpath → sha256 entries; no metric), with its binding checked in `STAGES.jsonl` (TRAIN_INVENTORY line) and `RELEASE_A.json` `obs_inventory_sha256` (grep of that key only). Nothing else under `stages/TRAIN/**` was opened |
| Desk arithmetic | Python on literal numbers only: ranks 7 / 4,994 (v1; v2 uses 70 / 49,931 at 50,000 draws), z_S = 2.99132, z_{1−0.05/3} = 2.12805, registry risk 7.21e-11, SE ≈ 0.00163, CPU sums |

**Accidental exposures (declared).**
1. Printing RESULT.json fields showed `init_qualifier` 620301 = false. The step-0 chart of 620301 did not have its lower bound above the margin on stage-C test rows. The same fact is in `ah/jobs/0196/review.md:21` ("available and needs no qualifier"), an allowed record. This is a step-0 status, not a training-time metric. It did not change any rule here: step 0 is treated as any other checkpoint, and D2/D3 handle every step-0 case.
2. The name listing of `hwsc/logs/` showed the log file names, including the three TRAIN logs. The writer opened none.

The checkpoint `created_utc` timestamps (wall time per checkpoint) were seen in `meta.json`. They are not a learning metric and are not used. **No per-checkpoint training metric (dev CE, loss, learning value at an intermediate step) was seen.**

**Observation for the coordinator.** `ah/jobs/0196/review.md:18` says "Support is 3,072/3,072 per model". RESULT.json `per_model.620301.support.fraction` = 0.99967 (3,071/3,072), while 620302 and 620303 are 1.0 [V]. This is immaterial to the outcome.

**Not read:** the public research-summary paths; `hwsc/stages/TRAIN/**`; `hwsc/logs/**` contents; `scratch/hwsc-job-*/`; `ah/jobs/0187|0188|0189/review.md`; `hwsc/stages/E1/L1.json`; the values of `hwsc/GATES.jsonl` (gate names, statuses and key names only were printed); every `payload.npz`, `state.pt`, `sealed/` file, `hist/` array, `HIST_*.npz`, chart, decoder and activation array; the stage-B blinded files; the files of `coord-hws-use-20261101` and every `HWSU-*` file.

**Findings of this plan not in the inputs:**
1. `hwsc-store/REGISTRY_OBLIGATION.json` is missing (§4.4).
2. The construction ledger's 6-claim and int-key limits force per-checkpoint ledgers (D-C6).
3. Without scoring unvalidated charts, the owner's example statement is true by construction (D-C4, D2 BY_CONSTRUCTION).
4. The stage-C learning landmark is reachable by last-four information in w\*, so a predictive beyond-four landmark is added (§1.1, D5).
5. `hwsc_registry.inventory_c` drops `hwsc-store` and reads its table at import, so a later registry must inject its own inventory, scratch and dry sources (§4.1).
6. Anchors from cal, val and lgate rows allow single-test readings at onsets, with Bonferroni needed only for existential readings (§5.6).

---

## Change log v1 → v2

Base: v1 `coord-hws-dyn-20261101.claude.md` (sha256 07e5f761…6e97, unchanged).
- The RC texts are the reviewer's replacement or insertion texts, applied verbatim except where a row below says otherwise (the joint-ruling refinements named in the rulings).
- "Merge" records where two changes met in one place.
- "Conforming" records a wording change elsewhere that keeps the document consistent with an applied change and adds no new content.

### Required changes
| Item | Where applied | Merge, conforming edit or departure from verbatim |
|---|---|---|
| RC-1 (MAJOR) | (1) §4.1 R9: (b′) inserted; (d) and (e) replaced by the reviewer's (d), (e), (e′); §9.2 sentence appended. (2) §4.1 Mechanism bullet `scratch` replaced; R6′ rows appended; §10 first paragraph sentence replaced; §11.3 sentence replaced. (3) §4.1 R10 cell replaced. (4) DRD8 appended | **(b) per ruling / J3:** §10 keeps the reviewer's text and adds "This is the one dry location, `hwsd-dry*` (J3)". **(d) per ruling / J4:** the reviewer's R10 sentence "No obligation is needed for these directories" is replaced by the J4 rule, and DRD8 gains a J4 case. **J6:** R10 also reads `REGISTRY_OBLIGATION_OF.json`. **§11.3:** the reviewer's sentence is applied. v1's KD location (`scratch/hwsd-kd-<job>/`) moves to `hwsd/stages/KD/` (the stage-C KC pattern), so that every scratch name stays inside J3's globs. The reviewer's `hwsd-kd-<job>` rows (R6′, `scratch_check_d`, the RC-7 fragments) are kept verbatim as fail-closed guards. **Conforming:** the R6′ reader cell names `scratch_check_d`; the R9 header cites J1; §3.1 OBS_INVENTORY row; §9.1 J1 exception; DRD9 OBS reader case; §12.1 file rows; test author B list |
| RC-2 (MINOR) | §4.3 item 2 (inserted bullets); §7 sampling row; DRD11 appended; §9.5 | **Superseded in part by J8 (ruled):** RC-2's "a reservation … named in such a record counts as ended" sentence, its `end_reservation(path, utc)` clause ("rewrites only its own reservation file …") and its DRD11 sentence are replaced by J8 items 4, 2–3 and 5. The §7 sampling-row text stands (J8 item 6). **Departure from verbatim (ruled):** the record already exists, so "Before the hwsd freeze, the coordinator writes the mailbox record …" becomes "The coordinator has written the mailbox record `ah/records/HWSC_W2_END.json` (sha256 2390e29d…6cb)". Its contents are stated as written: J2 adds the `OPERATION_ACTIVE.json` sha256 and the S8 RESULT sha256. **Conforming:** §3.1 identity row; §9.5 sentence; §13 risk row; §12.1 `hwsd_data` row |
| RC-3 (MAJOR) | §6 KD4: items (i) and (iv) replaced, (v) added, the paragraph appended | **Merge:** the change lands inside a table cell, so the reviewer's list is written inline as "(i) … (v)". The step-0 control sequence is annotated "which reads CHART_AT_INIT" (RC-4). **Conforming:** DRD4 cell; §13 risk row |
| RC-4 (MAJOR) | §5.3 rule 1a; §5.2 k_C^+ appended; §5.4 D2 and D3 NOT_EVALUABLE cells; §13 row 2 replaced; DRD5 appended | **Merge:** the D2 row also carries RC-5, and the D3 row also carries the S1/S6 reasons. **Conforming:** §5.5 bullet; §5.7 curve list; §8.2 D3 sentence; KD4 step-0 sequence; §14 Q5 wording; summary |
| RC-5 (MINOR) | §5.4 D2 rule (insertion), TRUE cell (replaced), NOT_EVALUABLE cell (added); §8.2 D2 TRUE template appended; DRD5 qualifier boundary | **Merge:** in the D2 row, with RC-4. **Conforming:** §5.5 SCORED_UNVALIDATED bullet; §5.6 existential list; §9.3; summary |
| RC-6 (MINOR) | §11.1 per-checkpoint bullet replaced (plus the reviewer's ledger basis as a [W] bullet); §11.2 rows replaced and inserted, cumulative columns recomputed; the note's first sentence replaced; §11.5 sentence replaced; §14 Q2 | **Merge with S2:** S2 adds ≈ 150 CPU-s to SUMMARY (central 350, range 200–800, 3× 1,050). The reviewer's totals of 9,600 / 3,950 / 5,350 therefore become 9,750 / 4,100 / 5,500, and the last cumulative values become 9,750 / 29,250; the note says so. **Conforming:** summary cost; §14 Q6 hours (1.1 / 2.7) |
| RC-7 (MINOR) | §6 KD0 code cell replaced; DRD13 appended | **Merge with J3/J5:** KD0 also binds the two records, declares track U's tokens as needles, and adds 620416 and `hwsd-dry-v1` to the needles. The J5 blinded list (track U round files) is added to §9.2 and to DRD13. **Conforming:** §4.3 item 1; §12.1 `hwsd_known` row |
| RC-8 (MINOR) | §7 row 9 failure cell replaced; §2.6 paragraph inserted; DRD6 cases added | **Conforming:** the §2.6 CHART_UNAVAILABLE row points to the row-9 mapping; §13 risk row |
| RC-9 (MINOR) | §4.4, §3.1 last paragraph, §14 coordinator list | **Superseded by J1 (ruled):** §4.4's default is replaced by J1's text (the record is not written). §3.1 reads "hwsc-store must not change during track D; J1: the stage-C obligation record is not written" instead of the reviewer's erratum-job wording. §14 states J1 instead of the reviewer's "whether and when to write" item |

### Joint rulings
| Item | Where applied |
|---|---|
| J1 | §4.4 (replaced by J1's text); §4.1 R9 header; §3.1 OBS_INVENTORY row; §9.1 blindness exception and list; header "Planning only" paragraph; §15 v2 inputs (the writer read OBS_INVENTORY under J1); §13 row |
| J2 | §4.3 item 2 (RC-2 text with the record's path and hash); §3.1 identity row; §9.5; §14 |
| J3 | §2.5 (dry scope `hwsd-dry-v1`, namespace bullet, track U's tokens); §4.1 Mechanism bullet note; §4.3 items 1 and 4; §6 KD0; §10 first paragraph; §3.1 identity row; DRD13 |
| J4 | §4.1 R10 (replaces the reviewer's "no obligation" sentence); §4.3 item 3; §9.4; §10 first paragraph; DRD8 |
| J5 | §6 KD0 (the mirror `seed_search_d`); §9.2 blinded list (track U round files); DRD13 |
| J6 | §4.3 item 3 (order of runs; `REGISTRY_OBLIGATION_OF.json`); §4.1 R10; DRD8; §14 |
| J7 | §14 (defaults stand; Q2 cost; Q5 plain words) |
| J8 (addendum 1, `coord-hws-ud-20261101.joint-rulings-addendum-1.md`, sha256 241040fb…c22b, verified) | §4.3 item 2: the W2 attestation rule (item 4) and the end record by exclusive create, `hwsd/reservations/<reservation_id>.END.json`, schema `hws-reservation-end-v1`, with its fields and refusals (items 1–3); these replace RC-2's attestation sentence and its "rewrites only its own reservation file" clause. DRD11: RC-2's appended test sentence is replaced by item 5. §9.5 sentence. Test author B list. §7 sampling row unchanged (item 6) |

### Suggestions (as ruled)
| Item | Ruling | Where applied |
|---|---|---|
| S1 | ADOPTED | §5.3 rule 3 split (LEARNING_BEFORE_CHART, UNCERTIFIED_AT_ANCHOR); §5.4 D4 reasons; §5.2 onset-order line (report-only); §5.5; §5.7; DRD5 |
| S2 | ADOPTED | §5.1 strong bounds (50,000 draws over the 72 X± arrays, ranks 70 / 49,931); §2.2 D-C11; §2.5 seed; §5.6; §7 row 13; §11.1; §11.2 SUMMARY; KD0 needles; KD6; DRD5; summary. **Seed:** the reviewer's 620413 + 1 = 620414 is inside D's block but already used by fresh_b4, so the ruling's "next free seed inside the block", 620416, is used |
| S3 | ADOPTED | §5.1 ABOVE^S_OK; §5.4 D6 (validated checkpoints only; EST-based loss as a labelled diagnostic); §5.5; §5.7; DRD5 |
| S4 | ADOPTED | §6 KD3: cal m32 recomputed (stage-C `ORACLE_cal.npz` not read); (a0) bitwise activation check against `ACTS_cal_b0.npz`, at run time only |
| S5 | ADOPTED | §2.7 first bullet; §7 row 12 |
| S6 | ADOPTED | §5.3 rule 7 (FINAL_NA vs UNRESOLVED); §5.4 D3/D4 reasons; DRD5 |
| S7 | ADOPTED verbatim | §2.5 consequence (iii) |
| S8 | ADOPTED | §1.1 oracle-feasibility bullet |
| S9 | Done by the coordinator (`HWS_UD_NAMESPACE.json`) | §2.5; §4.3 item 1 |

### Other
- Header: STATUS line, title, the "Revision v2" paragraph, and the J1 sentence in "Planning only".
- Summary, §11.2 and §11.5 now agree:
  - scoring ≈ 4,100 CPU-s (1.1 CPU-h, "a little over an hour");
  - total ≈ 9,750 CPU-s (2.7 CPU-h, "about three hours").
- §15: a v2 inputs row is added.
- No other text changed. As the review required, these are unchanged: the estimand, completion, the bootstrap bands (84 / 4,917), F, the per-checkpoint use of the stage-C chart rule, the shared rows and the anchored single tests.

---

## Change log HWSD-v2 → HWSD-DESIGN-v1

Base: `HWSD-v2.md` (sha256 28202282…824a, unchanged). F-texts are the confirmation reviewer's exact texts. J9 and J10 are the joint addenda 2 and 3. The four suggestions are applied as ruled in `coord-hws-dyn-20261101.v2confirm.rulings.md`.

| Item | Where applied | Merge or note |
|---|---|---|
| Header | STATUS line; title; a "Design freeze candidate" paragraph listing the inputs and their hashes | — |
| F-1 (MAJOR; issued as joint ruling J10) | (1) §4.1 R10 reader cell: the reviewer's replacement text. (2) §4.3 item 3: the second bullet (v2's "If track D draws first …") is replaced; §9.4 first bullet, sentence replaced. (3) §4.3 item 2: the stopped-SAMPLE text appended. DRD11 and DRD8: the reviewer's cases appended | **Merge:** the R10 cell keeps v2's opening sentence ("`hwsu-store`: the obligation reader …") and its J4 dry-store refinement. After the replacement text, a parenthesis records the obligation names of J6 (`REGISTRY_OBLIGATION_OF.json`, `REGISTRY_OBLIGATION.json`), which the replaced sentence had carried. The §4.3 item 2 insertion also cites J10 item 2 ("the J8 end record binds the obligation of the job that drew"). The §9.4 J4 bullet is made consistent with J10 item 1 (conforming) |
| J10 (addendum 3) | as F-1, plus: item 4 (aborted dry run, the recorded coordinator recovery step) in §4.3 item 3 "Dry stores" and §9.4; item 5 tests in DRD8 and DRD11; the sha256 binding in §3.1 and KD0 | J10 supersedes namespace rule 3 where they differ (§3.1 row) |
| F-2 (MINOR) | §5.4 row D2, per-model rule cell (prepended); DRD5 appended | — |
| F-3 (MINOR) | §4.1 R9 (d) (sentence replaced by the reviewer's longer text); DRD8 (clause replaced) | — |
| F-4 (MINOR, conforming) | §3.5 second "affect" bullet; §1.3 row T7; §13 risk row (name and seed) | — |
| J9 (addendum 2), symmetric form t = `hwsd`, o = `hwsu` | §4.3 item 1 (the declaration rule, replacing v2's track-U location list); §6 KD0 code cell (the fragment list, replacing the RC-7 list); §9.2 (`/hwsu-store/` pruning); DRD13 (J9's fixtures, with t and o substituted) | **Non-verbatim:** J9 is written for both tracks with placeholders, so t and o are substituted. J9's own list omits RC-7's fragment `/topo-scratch/hwsd-kd-`; J9 binds, so it is dropped. No `hwsd-kd-<job>` directory is expected (KD writes into `hwsd/stages/KD/`), and R6′ keeps that row as a fail-closed guard |
| Joint addenda 1–3 bound by G0 | §3.1 new identity row; KD0 code cell | — |
| Suggestion: k_C^+ predicate | §5.2 (the same gate predicate as k_C) | report-only; no reading changes |
| Suggestion: two bootstrap streams | §5.6 (labelled diagnostic when L^S > L or U^S < U) | report-only |
| Suggestion: S2 cost | §11.1 bullet and §11.2 SUMMARY content cell: 200–250 CPU-s | **Note:** the ruling places this within the SUMMARY range, so the SUMMARY central (350), its range (200–800) and every total (9,750 / 4,100 / 5,500 CPU-s; 2.7 / 1.1 CPU-h) are unchanged. The summary, §11.2, §11.5 and §14 still agree |
| Suggestion: J4 recovery | J10 item 4 (§4.3 item 3, §9.4) | — |

No other text changed. The science is unchanged, as the confirmation read states: the estimand, the chart rule per checkpoint, the shared rows, the anchored tests, the strong bounds and statements D1–D6.
