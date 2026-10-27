STATUS: HWSB-DESIGN-v1, design freeze candidate (HWSB-v2 af8772b8 + NEW-1..4 of the v2 confirmation applied verbatim)

# HWSB-v2: the world-sweep stage B, a short training pilot in w\* = W12-q1-s1.75-p0.2

**Round:** `coord-hws-stage-b-20261027` (request sha256 `498a607b754d8f2985415d3bdc10cbe0ddaf7d04486e0776b77759f11c1a1538`, verified). **Track:** L only (Codex frozen, addendum 28; PLANNING_PROTOCOL rule 5). **Writer:** clean-context Claude subagent of coordinator db858736, 2026-10-27.
**Revision v2.** Applies RC-1..RC-18 of the result-blind review (`coord-hws-stage-b-20261027.claude-reviewer.md`, sha256 ee406c3c…, verdict CONFIRM_AFTER_MINOR_FIXES) verbatim, as accepted in `coord-hws-stage-b-20261027.rulings.md` (d4e2d8f5…), and folds in the OPEN rulings of `coord-hws-stage-b-20261027.open-rulings.md` (7be74779…), amended by RC-7 and RC-15. v1 is `coord-hws-stage-b-20261027.claude.md` (sha256 3467d41f…), unchanged. Where a fix left a choice, the stricter option was taken. Every change is listed in §14 "Change log v1 → v2".
**Base code:** topo-pilot main `fab0499dddbbffb466be28e4084c6343f21a1941`; HWS code branch `hws-impl` `6101eae0a090ff5ef9da75caee84e5047e356e3f` (worktree `topo-pilot-hws`). `.venv/Scripts/python.exe tools/build_code_index.py --check` at fab0499 printed "code index is current" (exit 0) [V].
**Planning only.** The writer ran no training, sampling, tests or oracle computation, changed no store or repository and made no git write. No `payload.npz`, `state.pt`, `sealed/` file or `hist/` array was opened or hashed. Only JSON/YAML/Markdown records, `meta.json`/`extra.json` artifact metadata and code were read. The public research-summary paths were not opened or searched. No other output of this round was read, except (for v2, as the coordinator authorised) the review and the two rulings files named above.

**Labels.** **[V]** checked by the writer against code or a record (file:line, or JSON key for one-line JSON records). **[H]** an inherited record value. **[W]** the writer's desk arithmetic or design reasoning. **No [W] or [H] value is a gate threshold.** Every gated quantity is computed by the run. Known-case references are read by the run from the cited record files at run time.

Paths: `tp/` = `X:/Downloads/projects/topo-pilot/topo-pilot` (main, fab0499); `hws/` = `X:/Downloads/projects/topo-pilot/topo-pilot-hws` (6101eae); `ah/` = `X:/Downloads/projects/topo-pilot/agent-handoff`; `store:` = `X:/Downloads/projects/topo-pilot/hws-store`.

---

## Summary (≤ 300 words)

**Question.** In w\*, the world that stage A selected (12 × 12 cylinder, stay probability 0.2, emission width σ = 1.75), does the unchanged E4 training recipe produce models that (i) learn next-symbol prediction, (ii) form a circle that the K4b chart rule accepts on fresh histories, and (iii) carry enough of the oracle's beyond-four information that a stage C at the K4b margin 0.01 would have 80% planned power? Stage B answers this on two pilot models and fresh pilot histories, and fixes the stage-C size, model count and budget by frozen rules.

**Design.** Two pilot models (new masters 620201, 620202), E4 recipe unchanged except σ = 1.75 (and new, unissued seed scopes; one torch thread). Pilot histories: a 4,096-row learning block, a 3,072-row calibration block and a 3,072-row validation block, all fresh and never used by stage C. Pilot models never enter stage C (default of owner question Q1).

**Gates.** Decision-bearing for "stage C may be planned": B1 (captured ≥ 0.8), B4 (C0-cal and C0-val), B5 (pilot capture ≥ c_min at 80% planned power), B6 (a K4b-ladder N exists), and the technical preconditions B8a (a reviewed Decimal enclosure gives Z_bound BOUNDED for σ = 7/4) and B9a (stage-B store registrable; N_C·p_D2a ≤ 0.01). Report-only: B2, B3, B7. Deferred to stage-C implementation: B8b, B9b.

**Outcomes.** HWSB_PASS, HWSB_NOT_LEARNED, HWSB_NO_CIRCLE, HWSB_UNDERPOWERED, INCONCLUSIVE/RESOURCE_OR_AUTHORITY, FAIL_TECHNICAL. No outcome licenses the next world or a recipe change automatically.

**Schedule.** Implementation and the synthetic dry run may run now, writing no `.npz`/`.npy` file or ArtifactStore artifact under the project root (§6.4 rule 1). All real history generation into `hwsb-store` waits until the coordinator has accepted C2ND's S5 with no pending S5 rerun, or C2ND is terminal, because C2ND's fail-closed inventory would otherwise see an unlisted history store.

**Cost.** About 6,650 CPU-s (1.85 CPU-h) central, of which training is 4,850 CPU-s; 3× pauses per stage and cumulatively. All stage-B CPU is recorded in its own ledger `agent-handoff/HWSB_CPU_LEDGER.json`, outside the 12 CPU-h line of addendum 29.

---

## 1. The question

### 1.1 Where stage A left things
- **w\* = W12-q1-s1.75-p0.2**, tier 0, outcome HWS_SELECTED/T0 (`ah/jobs/0136/review.md:3-5`) [V]. The configs in the hand-off are `WorldConfig(cylinder, (12, 12), flat)`, `TransitionConfig(max_degree_lazy_walk, p_stay 0.2)`, `EmissionConfig(overlap, V 36, σ 1.75, grid, flat)` (`store:SELECTION.json` key `configs`) [V].
- S3 on 32,768 fresh rows (`store:stages/S3/worlds/W12-q1-s1.75-p0.2.json`, sha256 164c6038…) [V]: D4 mean 0.04701, L3 0.04575, per-row SD 0.08230 (lines 14, 35, 37); G_C mean 0.28719 (line 86); G4 mean 0.031687 (line 52); G4^A mean 0.018927 (line 69); V4 mean 0.039796 (line 455) [H].
- Stage-C implications: D4/M = 4.70, δ_max = 0.01525 (`store:SELECTION.json:540`) [H]. The transport bound was **UNAVAILABLE/NONTERMINATING_LOGIT** for w\* in stage A (`store:stages/S3/worlds/W12-q1-s1.75-p0.2.json:571-573`) [V], so the RC-3 reviewed enclosure (HWS-FROZEN-v1 §8, §11 row 5) is required.
- The current world w0 has σ = 1.25; the E4 models reached 0.83–0.95 of the oracle comparator there (`ah/jobs/0057/report.md:44`) [H], but the comparator itself (0.00854) was below the margin.

### 1.2 What stage B must decide
Stage A licensed oracle properties of w\* only (HWS-FROZEN-v1 §7.2, `ah/planning/responses/HWS-FROZEN-v1.md:433-439`) [V]. Stage B asks, of trained models and fresh histories:
1. **Learning.** Does the E4 recipe still meet the existing learning gate in w\*?
2. **Circle.** Does the K4b chart rule (LCC ≥ 95 %, C0-cal, C0-val) still find a circle?
3. **Power.** Is the pilot's share of D4 large enough, at its measured row variance, for a stage C at margin M = 0.01 to have 80 % planned power within the K4b ladder?
4. **Hand-off.** What stage-C N, model count, budget, Z_bound and registry inputs follow by frozen rules (HWS-FROZEN-v1 §10.3, lines 559-573) [V].

Competing explanations stage B can separate [W]: the recipe does not learn w\* (B1); it learns prediction but the circle is not legible to the K4b rule (B4); the circle exists but captures too little of D4 to measure at the margin (B5/B6); everything passes. Stage B never infers model success from oracle qualification (HWS-FROZEN-v1 line 573) [V]: every gate reads model outputs on pilot histories.

---

## 2. The pilot design

### 2.1 The E4 recipe, and exactly what changes

**Unchanged (the E4 recipe as recorded).**

| Item | Value | Source |
|---|---|---|
| World and dynamics | cylinder 12 × 12, flat metric, lazy max-degree walk, p_stay 0.2 | `tp/configs/base.yaml:9-16` [V] |
| Emission | overlap Gaussian, V = 36, grid centres (0.5 + 2a, 0.5 + 2b), symbols renamed per master by `SeedTree(master).generator("symbol_names", family, master)` | `base.yaml:18-20`; `tp/src/topo_pilot/process/emission.py:83-102` [V] |
| Sequences | n_obs 33, context 32, analysis position 32, BOS | `base.yaml:29-33` [V] |
| Data sizes | n_train 131,072, n_dev 4,096 per model | `base.yaml:36-37` [V] |
| Model | 4 layers, d_model 128, 4 heads, d_mlp 512, GELU, dropout 0, untied; vocab_in 37 (BOS = 36), vocab_out 36, n_ctx 33 | `base.yaml:42-51`; E4 step-5000 checkpoint `c3358e3cb9c352fb` `extra.json` `model_config` [V] |
| Training | 5,000 steps, batch 128 drawn with replacement, AdamW lr 1e-3, warmup 200 + cosine, weight decay 0.1 on matrices, grad clip 1.0, loss over all 33 positions, deterministic algorithms | `base.yaml:53-62`; `tp/src/topo_pilot/learner/trainer.py:45-55, 70-72, 106-113, 141-146, 177-189` [V]; checkpoint `extra.json` `train_config` [V] |
| Checkpoint grid | 0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000; primary 5000 | `base.yaml:61-62` [V] |
| Site | `resid_post_3`, index 32 (token w32 of [BOS, w1..w32]) | `base.yaml:51`; `tp/tools/k4b/k4b_config.py:37` [V] |
| Learning gate | captured = 1 − regret/G_C at p = 32, regret = mean KL(q32 ‖ p_model), G_C = mean KL(q32 ‖ q_last) on the same rows, pass iff captured ≥ 0.8 | `base.yaml:64-65`; `tp/src/topo_pilot/prediction/metrics.py:66-76, 107-115`; `tp/src/topo_pilot/experiment/s3.py:239-251`; `tp/src/topo_pilot/oracle/stage.py:93-103` [V] |
| Training code | `Trainer.fit` unchanged, with checkpoints serialised exactly as `LearnerStage.run` does (same config, parents, seed map, `serialise_state`) | `tp/src/topo_pilot/learner/stage.py:29-43, 75-106`; `trainer.py:129-194` [V] |

**What w\* forces.** Only `EmissionConfig.sigma` 1.25 → 1.75. W, q, p, V and the vocabulary (36 + 1) are unchanged at tier 0 (HWS-FROZEN-v1 §11 row 16, line 602) [V]. The w\* process is built by the same `src` builders that built E4 (`WorldStage`, `ProcessStage.run_transition`, `ProcessStage.run_emission`; `tp/src/topo_pilot/process/stage.py:43-65`) [V], so its WorldSpec and TransitionSpec are E4's own (ids 21feee1d8ee5422e and e4dafc7b9785c172, checked in KB1).

**What changes besides σ, and why none of it is a recipe change [W].**
1. **Seeds and scopes are new** (stage B is a new study, and the request requires unissued scopes): new masters 620201 and 620202; run_key `("hwsb-v1", "W12-q1-s1.75-p0.2", master)`; data scopes in §2.3. The sampling law, the sampler, the sizes, the canonical-to-named mapping and the init/batch-order mechanisms are E4's. Using E4's own run keys would re-issue E4's init and batch-order streams (`trainer.py:151, 160`) [V], and E4's DatasetStage test scope does not contain p_stay or the study (`tp/src/topo_pilot/dataset/stage.py:90-92`) [V], so it would be shared by any later σ = 1.75 study.
2. **One torch thread** instead of `physical_cores` (6 on this 12-logical-core machine; `tp/configs/stages.yaml:21`, `s3.py:50-59`; S8 record `cpu_count` 12, MetricRecords `f6c43ab3567c578f`) [V]. Measured cost per update: 0.383 CPU-s at 1 thread against 1.148 at 6 threads (`ah/jobs/0008/report.md:66-68`) [H]. This is a floating-point-order change, not a recipe change; KB2/KB3 (§3) check it on a known case.
3. **Composition.** A new driver calls the unchanged `Trainer.fit` on ObservationSets in a stage-B ArtifactStore, with a checkpoint callback that mirrors `LearnerStage.run`'s `save` (`learner/stage.py:94-102`) [V] and adds only the §8.2 hold. This is the X5 G1 precedent ("the public `Trainer` with an experiment-side checkpoint callback that mirrors the `LearnerStage` identity", `tp/src/topo_pilot/experiment/x5g1t_train.py` docstring) [V]. DRB2 checks that the mirrored callback gives checkpoint ids and checksums bitwise equal to `LearnerStage.run` on the same inputs. It does not use the experiment stages S3/S4, which read `base.yaml` and the S2 σ decision and would raise CONFIG_DRIFT (`base.yaml:1-2`) [V].
4. **The learning-gate rows** are a fresh 4,096-row block in stage B's own scope (E4 used its 4,096-row test split = 8 panels × 512, `base.yaml:38-40`) [V]: the same size and estimator.

**Not used:** the E4 cut-path ladder (`stages.yaml:94-96`: 3,000 steps, 10,000 steps, a larger model, the next σ) [V]. HWS-FROZEN-v1 §10.4 forbids a recipe change as the first remedy (lines 575-577) [V].

### 2.2 Models and seeds

| Choice | Value | Rationale [W] |
|---|---|---|
| Number of pilot models | **2** | Shared rule 1 makes the trained model the replication unit (`tp/docs/proposals/GAP_CLOSING_EXPERIMENTS_HE.md` §2 rule 1) [V]. One model cannot show seed-to-seed variation in learning, chart or capture; two can, at half the cost of three. Stage C still plans 3 (§11 row 4 of HWS-FROZEN-v1) |
| Masters | 620201, 620202 | Unissued (G0 checks); the 6202xx block is next to HWS's 6201xx bootstrap seeds (`HWS-FROZEN-v1.md:406`) [V], so it is recognisable as this lineage |
| Run key | `("hwsb-v1", "W12-q1-s1.75-p0.2", master)` | Gives new `init/…` and `batch_order/…` scopes (`trainer.py:151, 160`) [V] |
| Symbol names | `SeedTree(master).generator("symbol_names", "cylinder", master)` via the unchanged `OverlapGaussian` | E4's mechanism (`emission.py:83-85`) [V]; new names per master as in E4's O condition |
| EmissionSpec per master | `ProcessStage.run_emission(world_id, EmissionConfig("overlap", 36, 1.75, "grid"), SeedTree(master), store)` | The E4 serialisation envelope (`process/stage.py:55-61`) [V] |
| Pilot models in stage C | **never** (default of owner Q1) | Their pilot capture (B5) is computed and reported in `REPORT.json` only (§6.1, RC-6). If they were stage-C models, B5 would preview the stage-C endpoint and break blindness (§6) |

### 2.3 Histories, streams and scopes (all new; G0 verifies no prior issuance)

| Role | Rows | Stream | Sequence IDs | Kept as |
|---|---|---|---|---|
| Train, per master m | 131,072 × 33 | `SeedTree(m).generator("data", "hwsb-v1", "train", KEY, m)` | `make_sequence_ids(process_code("cylinder", "overlap", "1.75", f"hwsb-v1/train/{m}"), "train", n)` | ObservationSet in `hwsb-store/artifacts` (named tokens uint8 [n, 33]) |
| Dev, per master m | 4,096 × 33 | `…("data", "hwsb-v1", "dev", KEY, m)` | `…f"hwsb-v1/dev/{m}"…, "dev"` | ObservationSet |
| LGATE (learning gate, B1–B3) | 4,096 × 32 | `SeedTree(0).generator("data", "hwsb-v1", "LGATE", KEY)` | `…f"hwsb-v1/LGATE"…, "test"` | `hwsb-store/hist/LGATE.npz` (keys `canon32`, `seq_ids`, `digest_canon32`; §6.3) |
| CAL (chart calibration, B4) | 3,072 × 32 | `…("data", "hwsb-v1", "CAL", KEY)` | `…f"hwsb-v1/CAL"…, "test"` | `hist/CAL.npz` |
| VAL (C0-val, extension, B5, B6) | 3,072 × 32 | `…("data", "hwsb-v1", "VAL", KEY)` | `…f"hwsb-v1/VAL"…, "test"` | `hist/VAL.npz` |
| DRY (synthetic dry run only) | small | `…("data", "hwsb-v1", "DRY", …)`, masters 629901/629902 | — | `X:/Downloads/topo-scratch/hwsb-dry/` (no file named `HIST_*.npz`) |

KEY = `"W12-q1-s1.75-p0.2"`. `process_code` and `make_sequence_ids` are from `tp/src/topo_pilot/dataset/checks.py:17-32` [V].

The dry run never issues masters 620201/620202, seeds 620212–620214 or the TRAIN/dev/LGATE/CAL/VAL keys. It uses masters 629901/629902 and the `DRY` key only. (RC-3)

**Sampling.** Each table comes from one call to `HMMSampler(T, E_canon, π, SequenceLayout()).sample(n, rng)` on the canonical emission. Train and dev tokens are then named per master: `named = perm[canonical]`, mirroring `DatasetStage._sample_all` (`dataset/stage.py:84-99`) [V]. DRB4 and KB2 test this path bitwise. For the evaluation blocks, w33 and the latent states are dropped in memory at once, as in `k4b_data.sample_block` (`tp/tools/k4b/API.md:50`) [V]. The model input is `[BOS = 36, perm_j[canonical w1..w32]]` per model (`c1_model.model_inputs`, `tp/tools/c1prime/c1_model.py:41-44`) [V]. Oracle work is canonical and shared by both models. Each table runs `check_ranges` and `check_first_token` as `_sample_all` does. A failure is FAIL_TECHNICAL/SAMPLER, with no resampling. (RC-12 d)

**Separation (gate H2-B, before evaluation).** Sequence IDs of all tables are pairwise disjoint (`check_disjoint`, `checks.py:44-51`) [V]. Canonical 32-symbol digests (`scores.history_digests`, `tp/tools/x4_circle_history/scores.py:49`) [V] of LGATE ∪ CAL ∪ VAL are pairwise disjoint and disjoint from both masters' train and dev rows (train/dev canonicalised by the inverse perm, w1..w32). Any collision is FAIL_TECHNICAL/LINEAGE, with no replacement sampling. Duplicates within a table are kept and counted. Collisions with `hws-store` w\* histories are counted and reported only (the pilot models never saw them).

**Separation from stage C.** Stage C will use its own new scope. Its registry must contain `hwsb-store` and `hwsb-dry` (§6.3), so no stage-B history can become a stage-C history.

### 2.4 Checkpoints, site and position
- All 12 E4 checkpoints are saved (dev CE at each, the E4 grid). Every gate reads **step 5000** only. **Step 0** is used only for the descriptive initialisation-chart control.
- The site is `resid_post_3` at index 32, float64 activations via `c1_model.load_model64` and `c1_model.activations` (`c1_model.py:28-38, 52-59`), the K4b site (`k4b_config.py:37`) [V].
- The B1–B3 logits are the float32 plain forward at position 32, softmaxed in float64. This is E4's path (`tp/src/topo_pilot/activations/_extractor.py:116-129`; `s3.py:246-249` [V lines 246-248 softmax]) [V], mirrored in three lines and tested bitwise against `ActivationExtractor` (DRB6, KB6).

### 2.5 Pilot evaluation sizes, with rationale [W]
- **LGATE 4,096:** the E4 test size, so B1 is E4's gate on the same number of rows. With G_C ≈ 0.287 and per-row SD 0.236 [H, `store:SELECTION.json` `effects.G1.sd`], SE(G_C) ≈ 0.0037. G_C's sampling error moves captured by about ±0.0003 at captured ≈ 0.98; the regret's own spread is reported by the run.
- **CAL 3,072, VAL 3,072:** the K4b block size (`k4b_config.py:40`) [V]. The 512 lowest IDs are the landmarks and the C0-val panel (K4B-FROZEN-v1 §3.1, `K4B-FROZEN-v1.md:206-210`) [V]. The K4b ladder rule (B6) resamples size-3,072 validation arrays (`K4B-FROZEN-v1.md:452`) [V], so VAL keeps that size. At SD(X) ≈ 0.08 [W from H, D4 row SD], SE(mean X−) ≈ 0.0014 and SE(capture) ≈ 0.031.

---

## 3. Known-case checks (addendum 25 rule 5; stage KB, gating, before any training)

KB runs as its own metered job after the execution freeze and the scheduling precondition (§6.4). Any failure is **FAIL_TECHNICAL/KNOWN_CASE**: stop for coordinator review, with no tolerance or reference changed after data (a change needs an owner decision, as in HWS addendum 30). References are read by the run from the cited files.

| # | Check | Reference (read at run time) | Pass |
|---|---|---|---|
| **KB0 (G0)** | Authority and freeze: addendum 32 and the stage-B FREEZE bound by sha256; `store:SELECTION.json` sha256 = 243f7324… and `store:stages/FINAL/REPORT.json` = bd460cee… (`ah/jobs/0136/review.md:7`) [V]. Scopes and seeds: needles `hwsb-v1`, 620201, 620202, 620212–620214 in no earlier seed map, generation manifest or execution record (`hws_driver.seed_search` and `_needle_in` reused unchanged; classification by a new `hwsb_known.classify_hits`, a mirror of `classify_seed_hits` whose declaration fragments and job-scratch roots come from `tools/hwsb/CONTRACT.json`; tested bitwise against `classify_seed_hits` with the HWS fragments in DRB15) (`hws/tools/hws/hws_driver.py:57-92`) [V]. KB2's E4 regeneration and KB6's E4 test regeneration are declared "authorised deterministic regeneration" (the K4b G0 class, `K4B-FROZEN-v1.md:226`) [V]. The scheduling record of §6.4 is present | records | exact; unresolved hit fails closed |
| **KB1** | Process identity without payload access. Build the w\* process with the `src` builders into `hwsb-store/artifacts`. (a) WorldSpec id = 21feee1d8ee5422e and TransitionSpec id = e4dafc7b9785c172, with `payload_checksum(spec.to_payload())` (`tp/src/topo_pilot/contracts/base.py:170-184`) [V] equal to the `payload_sha256` in E4's `meta.json` (b6f0746e…, f94340a6…) [V]. (b) For each master, `oracle_profile.canonical_emission(E, perm)` bytes sha256 = `SELECTION.json` sha256 `E` 4d7b8e56…, and T, π, coords sha256 = d55d1024…, 5ab26711…, 81468d18… (`store:SELECTION.json:532-535`) [V]; the hash is the float64 C-order bytes (`hws/tools/hws/hws_records.py:318-319, 338`) [V]. (c) `validate_process(T, E_canon, π, 1e-12)` returns; E_canon is bitwise identical for both masters | E4 meta.json; SELECTION.json | exact |
| **KB2** | **E4 recipe reproduction, 100 steps, E4 threads (6).** Regenerate in memory (never persisted) the E4 train and dev sets of master 1729 with E4's own streams (`SeedTree(1729).generator("data", split, "cylinder", "overlap", "1.25", 1729)`, `dataset/stage.py:90-91`) [V] through the stage-B sampling path. Require `payload_checksum` equal to the `payload_sha256` of ObservationSets `38358227133898a2` (train, n 131,072) and `096f9b6dbe8536cd` (dev) [V meta.json]. Then run `Trainer.fit` with E4's exact ModelConfig/TrainConfig, run_key `("cylinder", "O", 1729)` and `SeedTree(1729)`, stopping by a sentinel exception in the checkpoint callback after step 100. Within warm-up the LR multiplier does not depend on the total step count (`trainer.py:51-53`) [V]. Require `payload_checksum` of the steps 0, 50 and 100 Checkpoints equal to `bd8813115bbd970b` (d49284f5…), `67e173f07b6b2908` (ae93135b…) and `eb0f9e9c8e3a6e1f` (7625c1c1…) [V meta.json], and dev CE at steps 50 and 100 equal to MetricRecords `37657d8490ba9e17` rows (2.7369381487369537, 2.4262474477291107) [V]. Checkpoints are built with `run_id` = "cylinder-O-1729" and `observation_id` = "38358227133898a2", exactly as `LearnerStage.run`. Threads are set by `torch.set_num_threads(6)` for KB2 and `torch.set_num_threads(1)` with `OMP_NUM_THREADS=MKL_NUM_THREADS=1` for KB3 and TRAIN. `torch.get_num_threads()`, `torch.__version__` and the E4 version found (OPEN-5) are recorded. The KB record also states which reading (bitwise or the secondary reading) applies (OPEN-5 ruling). | E4 metadata | bitwise. **Pre-registered secondary reading** (only if bitwise fails while both ObservationSet checksums pass): PASS_WITH_NUMERIC_DRIFT iff \|ΔdevCE\| ≤ 1e-3 nats at steps 50 and 100 against the MetricRecords `37657d8490ba9e17` values; the step-0 checksum must still be bitwise equal (initialisation does not depend on threads or BLAS); recorded as a deviation flag. No E4 checkpoint payload is opened. |
| **KB3** | **The one-thread setting.** The same 100 steps at `torch.set_num_threads(1)`: \|devCE − E4\| ≤ 1e-3 nats at steps 50 and 100. Determinism: a second 1-thread run to step 50 gives a bitwise-identical step-50 checksum. Report whether the 1-thread checkpoints equal the 6-thread ones bitwise. If KB3 fails while KB2 passes, the outcome is FAIL_TECHNICAL/KNOWN_CASE before any training. The coordinator may rule (procedural) that training uses E4's six threads, with the TRAIN central re-frozen as 2 × 5,800 CPU-s and the per-model hold at 17,400 CPU-s, before training starts. No other change is permitted. | E4 dev CE | ≤ 1e-3 nats; bitwise |
| **KB4** | **Law enclosure known case (B8a).** With the reviewed enclosure (§4, B8a) bound at σ = 5/4 and neighbour 1/5 on the w0 process built by the `src` builders (σ = 5/4, master 1729) with WorldSpec, TransitionSpec and EmissionSpec `payload_checksum` equal to the E4 `meta.json` `payload_sha256`, and E = `oracle_profile.canonical_emission(E, perm)` (K4b's `E_canon_shared`): status BOUNDED and the exact Z_bound equal to K4b's recorded `2116763197780003590583470649/10^39` (`ah/jobs/0057/report.md:40`; `k4b-store/stages/S8/RESULT.json`, sha256 1571b08b…) [H]. At σ = 5/4 every logit terminates, so δ (defined in B8a as the exact rounding error) is computed as 0 and the enclosure equals `softmax_enclosure` bit for bit (RC-1). Then at σ = 7/4, on the shared canonical E of KB1(b): BOUNDED, κ < 1, Z_bound recorded | K4b RESULT.json | exact rational equality; BOUNDED |
| **KB5** | **Stage-A oracle reproduction.** Verify the sha256 of `store:hist/S3/W12-q1-s1.75-p0.2.npz` = c000a224… (S3 world record line 569) [V], then recompute with `hws_oracle` on the stage-B canonical arrays the S3 means of D4, G1 (= G_C), G4 and G4^A. A history table is read; no payload | S3 world record lines 35, 52, 69, 86 | \|Δ\| ≤ 1e-12 each |
| **KB6** | **Learning-gate machinery at w0.** Regenerate the E4 test split in memory (`SeedTree(0).generator("data", "test", "cylinder", "overlap", "1.25")`), checksum = ObservationSet `2a67b2c947e293ba`, and its panels = HistoryIndex `afb6e7120c9477b1` [V meta.json]. (a) Stage-B G_C on those 4,096 rows = recorded G_C 0.2648737252067266 (MetricRecords `37657d8490ba9e17`) [V]. (b) With the KB2 step-100 model, the stage-B B1 code and the `src` path (`ActivationExtractor` logits; `BayesFilter`, `LastSymbolPosterior`; `PredictiveMetrics.regret`, `captured`) agree | MetricRecords | ≤ 1e-12 |
| KB7 (report only) | Decimal `error_bound.reference_moments` on the 4 lowest-ID VAL rows at K ∈ {4, 32}, as the HWS S3 spot check (S3 record line 937, passed at w\*) [V]; m4-phase and SHA-of-suffix null scores on VAL (oracle-only, mean ≈ 0) | — | report |

**Not run (default):** a full 5,000-step E4 reproduction. The S8 rerun already reproduced all 12 E4 cylinder-O-1729 checkpoints bitwise on a fresh clone (`checksum_equal` 12, MetricRecords `f6c43ab3567c578f`) [H]. KB2 re-tests the same composition in today's environment for 100 steps, at about 1/30 of the cost [W]. The environment is pinned: `requirements.lock:38` torch 2.14.1+cpu, committed 2026-10-13 00:19 +0300, before E4's first checkpoint at 05:07Z (b21fa93; checkpoint `bd8813115bbd970b` `created_utc`) [V]. KB2's secondary reading covers residual drift.

**Chart rule on a known case.** The K4b chart code is reused unchanged. Its known cases are K4b's own passes at w0 (C0-cal and C0-val PASS in all three E4 models, `ah/jobs/0055/report.md:35-36`) [H] and the planted-circle cases of the dry run (DRB7). An optional rebuild of K4b's E4 chart would need an explicit AUTH for checkpoint payload reads (HWS MD-11 precedent) and is not planned.

---

## 4. The gates B1–B9, frozen before training

Common conventions: models j ∈ {620201, 620202}, step 5000. Arrays are float64. Means are `c1_means.tree_mean`. Bootstraps use `c1_means.bootstrap_means` (one index stream shared by every array) and ranks use `c1_means.quantile_with_rank`. z constants come from `statistics.NormalDist().inv_cdf` on exact arguments; the decimals below are [W]. Every gate is computed for both models even after a failure, except where its input does not exist: a model without a production chart has C0-val, extension, B5 and B6 recorded NOT_RUN/NO_CHART, and B6 is then reported (not gated) on the charted model only. The outcome follows the precedence of §5.

| Gate | Exact computation | Data | Pass reading | Numerical tolerance | On failure | Role |
|---|---|---|---|---|---|---|
| **H2-B** | §2.3 separation and sequence-ID disjointness | all stage-B tables | 0 collisions | exact | FAIL_TECHNICAL/LINEAGE | precondition |
| **B1** learning | p_j = softmax(float32 logits at index 32) in float64, re-indexed to canonical: p_canon[:, v] = p_named[:, perm_j[v]]. q32, q1 from `hws_oracle.beliefs` and `predictive` (`hws/tools/hws/hws_oracle.py:51-60`) [V] (q1 = E4's q_last, checked in KB6). r_j = mean `kl_rows`(q32, p_j) (`hws_oracle.py:72-84`) [V]; G_C = mean `kl_rows`(q32, q1); captured_j = `PredictiveMetrics.captured`(r_j, G_C); `LearningGate(0.8).evaluate_with_status` | LGATE, 4,096 | captured_j ≥ 0.8 for **both** j (equality passes, `metrics.py:114`) [V] | p rows sum to 1 within 1e-6 (`metrics.py:13, 21-28`) [V]; NaN → INCONCLUSIVE (`metrics.py:112-113`) [V] | HWSB_NOT_LEARNED (k of 2 recorded) | **decision** |
| **B2** forcing beyond four | Ĝ4 = mean kl_rows(q32, q4); d_i = kl(q32, q4)_i − kl(q32, p_j)_i; L = d̄ − z_{1−0.05/4}·SE(d), z ≈ 2.2414 (family: 2 models × B2, B3) | LGATE | report r_j/Ĝ4; "predictions not suffix-4-only" (Proposition F, `HWS-FROZEN-v1.md:133`) [V] iff L > 0 | — | annotation only | report |
| **B3** circular forcing | the same on `circ_marginal`(·, 6) (`hws_oracle.py:63-65`) [V] of q32, q4 and p_j | LGATE | report r_j^A/Ĝ4^A; L > 0 reading as B2 | — | annotation only | report |
| **B4** circle | Per model, independently. **C0-cal:** `k4b_charts.build_chart(X_cal[512 lowest-ID CAL rows], ids, m32_land, trained_ledger, j, "production", cfg)` with cfg = `k4b_config.chart_cfg()` (the C1′/K4b kernel cfg; `tp/tools/k4b/API.md:38`) [V]: GIANT \|C\*\| ≥ 487 of 512, exact integer lift, primitive class, smoothing residual ≤ 1e-8, gauge alignment finite and > 0 (`K4B-FROZEN-v1.md:299-305`; `tp/tools/k4b/k4b_charts.py:65-88`) [V]. Then the step-0 control `init_charts` on the step-0 CAL landmark activations (descriptive; INIT_UNAVAILABLE non-gating, a shared-code FAIL_TECHNICAL stops at once, `k4b_charts.py:107-121`) [V]. Then `freeze_production(out, {j: res for passing j}, init, {})` (`k4b_charts.py:128-153`) [V], before any VAL activation. **C0-val:** `k4b_charts.c0_val_gate([j], …)` (`k4b_charts.py:176-197`) [V] on the 512 lowest-ID VAL rows: own direct chart GIANT ≥ 487; support ≥ 507/512; fidelity ≥ 0.80; every one of 12 bins ≥ 8; resultant ≤ 0.30 (`K4B-FROZEN-v1.md:313`) [V]. **Held-out extension:** `k4b_charts.extend` (`k4b_charts.py:168-173`) [V] of the frozen production chart to all 3,072 VAL rows gives φ_j and A_j (reported: support fraction, reasons, d8 and resultant summaries via `k4b_scores.support_report`). | CAL 512 landmarks; VAL 512 panel; VAL 3,072 | C0-cal and C0-val PASS for **both** j | inherited exact integer criteria; smoothing 1e-8 | INCONCLUSIVE/CHART_UNAVAILABLE → HWSB_NO_CIRCLE; FAIL_TECHNICAL as mapped by `c1_records` (`K4B-FROZEN-v1.md:323`) [V] | **decision** |
| **B6** stage-C N (computed before B5) | On VAL: m = `k4b_scores.oracle_moments` (K ∈ {1, 2, 4, 32}); `endpoint_arrays(φ_j, A_j, m32, m4)` → X−_j, X+_j, r4n (`tp/tools/k4b/API.md:93`) [V]. SD^U_{j,s} = rank-4,917 of 5,000 `precision.sd_b4_draws` SDs (seed **620212**, size 3,072). F_plan = `k4b_cert.F_plan(Z_bound(w*))` (`tp/tools/k4b/k4b_cert.py:141`) [V]. For N in (3,072, 6,144, 12,288): N qualifies iff (1) `precision.mde(SD^U, {delta: 0.01 + F_plan, alpha: 0.05/3, power: 0.80, projected_N: N})` ≤ 0.02 for every j and side, and (2) in the SUPPORT and EXCLUSION scenarios of K4B-FROZEN-v1 §7.2(2) (`K4B-FROZEN-v1.md:464-468`) [V], with centred draws `precision.centered_draws` (seed **620213**, 5,000 draws, size N) over the four (j, s) columns, every per-model count and the **two-model joint** count is ≥ 4,000 of 5,000. N_C = the smallest qualifying N | VAL, 3,072 | N_C exists | ranks checked by `quantile_with_rank`; exact F_plan | HWSB_UNDERPOWERED/LADDER | **decision**; fixes N_C |
| **B5** pilot capture | D̂4 = tree mean of `phase_scores(oracle_phase(m32), m32, m4)` (K4b `delta4_orc`, `HWS-FROZEN-v1.md:93, 100`) [V]; ĉ_j = mean(X−_j)/D̂4 (X− carries the missing mass, since X− = −‖r4‖ on unsupported rows, `K4B-FROZEN-v1.md:140-142`) [V]. **c_min,j = (M + F_plan + (z_{1−α} + z_{0.80})·SD^U_{j,−}/√N_C) / D̂4**, with M = 1/100, α = 0.05/3 (stage-C 3-model multiplicity), z-sum ≈ 2.969666 (`K4B-FROZEN-v1.md:463`) [H], N_C from B6 (12,288 if B6 failed, report only). Also reported: the §10.2 literal c_min (z_{1−α} only) and a bootstrap 95 % CI of ĉ_j (seed **620214**, ratio of the two tree means per draw) | VAL, 3,072 | ĉ_j ≥ c_min,j for **both** j (equality passes) | float64; reported to 6 digits | HWSB_UNDERPOWERED/CAPTURE, annotation POSITIVE_BELOW_PLANNING iff the rank-125 value of the mean-X−_j column of the seed-620214 draws is > 0 | **decision** |
| **B7** cost and model count | Measured meter CPU per pilot model (one meter job per model, §8). Stage-C training forecast = 3 × max_j(measured CPU_j). Stage-C evaluation forecast = K4b measured E1 1,280.5 + E2 1,720.1 × N_C/3,072 CPU-s (`ah/jobs/0055/report.md:63`; `ah/jobs/0057/report.md:102`) [H]. Model count for stage C = **3** (HWS-FROZEN-v1 §11 row 4, line 590; §10.3 B7, line 569) [V] | meter ledger | — | — | — | report (feeds the stage-C budget) |
| **B8a** law bound (stage B) | The reviewed enclosure `hwsb_law.softmax_enclosure_rounded(states, digits=60)`: each logit q = −d²/(2σ²) is an exact Fraction, with d² as in `process_law.py:112-113`. It is converted once to q̃ = Decimal(q.numerator)/Decimal(q.denominator) in `error_bound.trapping_context(60)` (Inexact and Rounded not trapped, every other trap kept). **δ := max_{s,j} \|Fraction(q̃_{s,j}) − q_{s,j}\|, computed exactly.** The run asserts δ ≤ u·Q_max, with u = `u_digits(60)` = ½·10⁻⁵⁹ and Q_max = max_{s,j} \|q_{s,j}\|, and asserts 2δ < 1. It returns (E_dec, lo·(1 − 2δ), hi/(1 − 2δ)), where E_dec, lo and hi are computed from q̃ exactly as `process_law.py:117-124`. When every logit terminates (σ = 5/4), δ = 0 and the result equals `softmax_enclosure` bit for bit. Proof (reviewed note in `tools/hwsb/`): (1) the existing analysis applies to the exact inputs q̃, so softmax(q̃)_j ∈ [E_dec/hi, E_dec/lo]; (2) with θ = q − q̃, softmax(q)_j/softmax(q̃)_j = e^{θ_j}/Σ_k w_k e^{θ_k} ∈ [e^{−2δ}, e^{2δ}]; (3) e^{−2δ} ≥ 1 − 2δ and e^{2δ} ≤ 1/(1 − 2δ); hence E*_j ∈ [E_dec(1 − 2δ)/hi, E_dec/(lo(1 − 2δ))]. A context manager binds `process_law.LAW["sigma"]` = 7/4, `LAW["neighbour"]` = 1/5 and `process_law.softmax_enclosure`, and restores all three in `finally`. (This is the `hws_exact.law_bound_report` pattern, `hws/tools/hws/hws_exact.py:220-235`) [V]. `process_law_bound` itself is unchanged (`process_law.py:222`) [V]. Round-to-nearest holds in `trapping_context` (ROUND_HALF_EVEN, `error_bound.py:54-65`, per the review). Obligations (OPEN-3 ruling): the result-blind reviewer checked the argument before the design freeze (sound after RC-1); at implementation, an independent author-B test and the reviewed proof note in `tools/hwsb/`, with δ as defined here | w\* arrays | KB4 passes and status BOUNDED for w\* | exact rationals | FAIL_TECHNICAL/LAW_BOUND (correction ≤ 2 per defect); B6 then uses the frozen stand-in Z_bound = 10⁻⁶ for report only | **decision (technical precondition)** |
| **B8b** K4b tier-0 binding (deferred) | The versioned stage-C K4b binding of HWS-FROZEN-v1 §11 rows 1, 5, 10, 11, 12, 13, 15 and 16 (lines 587-602) [V] passes its own synthetic dry run | — | before any stage-C data | — | stage C cannot start | stage-C precondition |
| **B9a** registry (stage B) | (i) Every stage-B history file (artifacts ObservationSets; `hist/*.npz`; `superseded/**`) is listed with its sha256 in `HANDOFF.json`. (ii) The reader `hwsb_data.registry_digests(store)` returns canonical digests for 100 % of recorded rows, fail-closed on any missing or unreadable file. (iii) (3,072 + 3,072 + N_C)·p_D2a(w\*) ≤ 0.01, with p_D2a recomputed by `hws_exact.p_d2a` (`hws_exact.py:52-60`) [V] on the stage-B arrays and equal to `SELECTION.json:409` (5.4162868151717785e-15) [V] within 1e-12 relative. (iv) Sealed-D-2a predicate hits on stage-B evaluation rows: report | store | all hold | exact counts | FAIL_TECHNICAL/REGISTRY | **decision (technical precondition)** |
| **B9b** stage-C registry (deferred) | The stage-C registry covers `hws-store` (HWS §11 row 10 reader, line 596) [V], `hwsb-store` and `topo-scratch/hwsb-dry` with frozen readers | — | before any stage-C data | — | stage C cannot start | stage-C precondition |

**Refinements of HWS-FROZEN-v1 §10.3, with justification.**
1. **B5 at 80 % planned power** instead of §10.2's z_{1−α} form (`HWS-FROZEN-v1.md:556`) [V]. The §10.2 form is 50 % power at the pilot capture. Shared rule 3 requires 80 % planned power (`GAP_CLOSING_EXPERIMENTS_HE.md` §2 rule 3) [V], as does the K4b MDE rule (`K4B-FROZEN-v1.md:463`) [V]. F_plan is added for consistency with K4b's planning allowance. §10.2's capture definition is internally loose ("c = E X−/D4" and "c·D4 − missing mass"); here capture is mean X−/D4, which already contains the missing mass. Flagged as owner Q3; the default is this refinement. B5 is not an extension decision (addendum 26 item 3). It is the registered futility check of HWS §10.3 B5, computed on pilot models that never enter stage C. Stage-C size comes only from variance (B6).
2. **B6 with two pilot models.** The joint projection covers two models, not three; the per-model rule is K4b's verbatim. This is a planning approximation, and stage C may keep its own validation precision check that can only raise N along the ladder. That choice is left to stage-C planning, which is not approved (OPEN-2 ruling).
3. **B8 and B9 split** into a stage-B part (a, decision-bearing technical) and a stage-C part (b, deferred). The §10.3 wording ("before any stage-C data", lines 570-571) [V] places them at the stage-C boundary, while B6 needs Z_bound now.
4. **"Both models"** for B1, B4 and B5. Stage C needs every model to pass (K4b overall SUPPORT needs all three, `K4B-FROZEN-v1.md:67`) [V], so a 1-of-2 pilot is a real risk signal. The next step then goes to the owner (Q4).

**Expected values (orientation only, never thresholds) [W from H].** Regret at w0 was 0.0036–0.0039 nats (`tp/reports/E2/summary.md:12-14`) [V], so B1 has a wide margin (it needs regret ≤ 0.2·0.287 ≈ 0.057). With SD^U ≈ 0.09 and N_C = 3,072: c_min ≈ (0.0101 + 2.9697·0.09/55.43)/0.0470 ≈ 0.32, or 0.29 in the §10.2 form, against w0 captures of 0.83–0.95. SD(X) ≤ √V4 ≈ 0.20 [W], so N_C = 3,072 is likely unless the support is poor.

---

## 5. Outcomes and licences (registered now; addendum 25 rule 6 included)

### 5.1 Precedence
| # | Outcome | Condition |
|---|---|---|
| 1 | **FAIL_TECHNICAL/<reason>** | a KB failure; H2-B LINEAGE; NONFINITE loss; B8a or B9a unresolved after ≤ 2 corrections per defect; an integrity, identity or numerical defect; B1 INCONCLUSIVE (G_C ≤ 1e-6, impossible after KB5) → FAIL_TECHNICAL/NUMERICAL |
| 2 | **INCONCLUSIVE/RESOURCE_OR_AUTHORITY** | a scheduled stage did not complete: a 3× hold the owner does not continue, a lost training process (never restarted from weights), a disk or memory safe-STOP, missing or expired authority, or the §6.4 scheduling precondition not met |
| 3 | **HWSB_NOT_LEARNED** (k/2) | B1 fails in ≥ 1 model |
| 4 | **HWSB_NO_CIRCLE/<criterion>** | B1 passes in both; B4 fails in ≥ 1 model |
| 5 | **HWSB_UNDERPOWERED/LADDER or /CAPTURE** (+ POSITIVE_BELOW_PLANNING annotation) | B1 and B4 pass; B6 has no N, or B5 fails in ≥ 1 model |
| 6 | **HWSB_PASS** ("stage C may be planned") | B1, B4, B5, B6, B8a, B9a all pass |

Every gate value is reported whatever the outcome. B2, B3 and B7 never change it.

### 5.2 Licences
- **HWSB_PASS.** "In w\* (12 × 12 cylinder, p 0.2, σ 1.75), two transformers trained by the E4 recipe (masters 620201, 620202, step 5000) each reached captured ≥ 0.8 on 4,096 fresh pilot histories. In each, the K4b LCC chart rule built a circle that passed C0-cal on 512 fresh landmarks and C0-val on 512 fresh validation rows. On 3,072 fresh validation rows each pilot capture ratio reached the frozen c_min (80 % planned stage-C power at margin 0.01 with N_C rows, α = 0.05/3). Stage C may be planned with N_C = …, 3 models and a training forecast of … CPU-s; Z_bound(w\*) = … ." It does **not** license: that any circle carries beyond-four information (pilot statistics are uncertified, multiplicity-uncontrolled and on pilot models); that stage C will reach SUPPORT; that new stage-C models will pass their gates; anything about the E4 models, K4b's EXCLUSION or any earlier verdict; that w\* is optimal.
- **HWSB_NOT_LEARNED.** "With the E4 recipe unchanged, k of 2 pilot models did not reach captured 0.8 in w\*." Not licensed: that w\* is unlearnable, or that a longer or larger recipe would fail; any statement about the circle.
- **HWSB_NO_CIRCLE.** "Both pilot models learned the prediction task, but in model(s) … the K4b LCC chart rule did not yield a chart passing C0-cal/C0-val (criterion …) on fresh pilot histories." Not licensed: that no circular structure exists (another chart method might find it); anything about E4.
- **HWSB_UNDERPOWERED.** "The pilot models learned and charted, but the pilot capture or its row variance implies that a stage C at margin 0.01 within the K4b ladder (≤ 12,288 rows) would not have 80 % planned power." The rule-6 annotation POSITIVE_BELOW_PLANNING reads: "the pilot circles covary positively with r4 on pilot histories (bootstrap lower bound > 0), below what stage C could detect at the margin." Not licensed: absence of the effect; an effect below the margin as a finding.
- **FAIL_TECHNICAL, INCONCLUSIVE:** no scientific statement.

### 5.3 The fallback rule (HWS-FROZEN-v1 §10.4, lines 575-577) [V]
No outcome licenses the next world (W12-q1-s2.0-p0.2, then W12-q1-s1.25-p0.8333; `store:SELECTION.json:394`) [V], a recipe change, extra seeds or a larger pilot automatically. After any outcome other than HWSB_PASS, the coordinator reports in plain language and the owner decides (Q4). Stage B never infers model success from oracle qualification.

---

## 6. Blindness and data hygiene

### 6.1 What may shape stage C, and by which frozen rule
| Stage-B quantity | Shapes | Rule |
|---|---|---|
| SD^U_{j,s}, support, missing mass (VAL) | stage-C N | B6 (K4b §7.2 on pilot arrays) |
| ĉ_j, c_min,j | whether stage C is planned at all | B5 (pass/fail only) |
| measured CPU per model | stage-C budget | B7: 3 × max_j CPU_j plus the K4b evaluation scaling |
| model count | stage C | 3 (HWS §11 row 4); a change needs a reviewed generalisation |
| Z_bound(w\*) | stage-C margin allowance F | B8a |
| p_D2a(w\*), N_C | stage-C registry risk | B9a(iii) |
| the margin M | nothing | M stays 1/100 (HWS §11 row 14, line 600) [V]; never lowered after pilot data; δ_max = 0.01525 ≥ M is reported |
| chart parameters, recipe, site | nothing | unchanged K4b cfg and E4 recipe; no tuning on pilot data |

`HANDOFF.json` (the only stage-B input to stage-C planning) holds: the outcome; N_C; the model count; the stage-C training and evaluation forecasts (B7); Z_bound(w\*) and F_plan; p_D2a and the B9a(iii) value; the store inventory and sha256 list; and the pilot checkpoint ids listed as stage-C exclusions. It holds no mean of X±, ĉ_j, c_min,j, CI, regret, captured value or chart-fidelity value. Those stay in `REPORT.json`, which goes to the coordinator and the owner. It is never attached to or quoted in a prompt to a stage-C writer, test author or reviewer. (RC-6)

### 6.2 What is sealed or never computed
- Pilot models never enter stage C (Q1 default), so their pilot X± means are pilot data, not a preview of the stage-C endpoint, and are reported in `REPORT.json` only, never in `HANDOFF.json` or to stage-C roles (§6.1, RC-6). **If the owner chooses to reuse them (Q1 alternative):** B5 is not computed; every VAL mean of X±, the supported contribution and every ratio that reconstructs them are written only by a sealing writer (`k4b_stats.write_sealed` pattern, `K4B-FROZEN-v1.md:492-500`) [V]; only B6 (variance-only) is gated.
- Stage B never computes a K4b decision (`model_status`, `overall`) or certified bounds on pilot data, never draws in any stage-C scope, never reads `k4b-store/SEALED_VALIDATION.json`, any `sealed/` file or any C2ND file, and never opens E4 checkpoint payloads.
- No stage-A history becomes stage-B data (HWS-FROZEN-v1 §6.4, line 392) [V]. KB5 reads the S3 w\* table only to reproduce stage-A numbers.
- The execution AUTH names the `hws-store` history reads: KB5 (S3 w\* table, sha256 checked) and the H2-B digest count over `hws-store/hist/**` w\* tables (identity only). (RC-16)

### 6.3 Registry entry of stage-B histories
- **Formats.** Train and dev are ObservationSet artifacts (named uint8 [n, 33]) in `hwsb-store/artifacts`, with each master's EmissionSpec perm in the same store, so a K4b-style `source_a`/`source_f` reader canonicalises them (`tp/tools/k4b/API.md:72, 77`) [V]. LGATE, CAL and VAL are canonical histories under `hwsb-store/hist/`. `hist/{LGATE,CAL,VAL}.npz` keys are exactly `canon32` (uint8 [n, 32]), `seq_ids` (int64 [n]) and `digest_canon32`. Superseded attempts are kept under `superseded/`.
- **Reader.** `hwsb_data.registry_digests(store)` (tested, B9a) inventories every file recursively and fails closed. `HANDOFF.json` freezes the file list and sha256s.
- **Obligation recorded in the hand-off.** Every later registry, stage C first, must list `hws-store` (HWS §11 row 10), `hwsb-store` and `X:/Downloads/topo-scratch/hwsb-dry` as READER sources. The dry store holds synthetic tiny-world histories only (§7); it is listed so that a fail-closed inventory finds it classified.
- **Merge and exclusions (RC-16).** After the stage-B report is accepted, `hwsb-impl` is merged into main (--no-ff, with its `docs(index)` commit) so later registries import `hwsb_data.registry_digests`. HANDOFF lists every pilot Checkpoint id (24) as stage-C exclusions.

### 6.4 Scheduling relative to C2ND (precondition P-SCHED)
- **The hazard [V].** C2ND's registry inventory treats any unlisted top-level directory under the project root that holds a history file, identity reference or ObservationSet root as a violation, which makes the registry INCOMPLETE (`tp/tools/c2_readout/c2_registry.py:173-210`; C2ND's own inventory is `topo-pilot-c2nd/tools/c2_nd/nd_registry.py:232-257`, frozen table in its `CONTRACT.json` `registry.inventory`, per the review). C2ND rebuilds its registry at S5 (REG2) before its DTEST draw, and history generation of the rounds must never overlap (`ah/planning/responses/C2ND-DESIGN-v1.md:456-472`) [V]. C2ND is now at dry run 0158, before its freeze and S1–S5 (`ah/COORDINATOR_STATE.md:8-12`) [V].
- **Rule.**
  1. Stage-B implementation, tests and the synthetic dry run may run at any time. Until P-SCHED rule 3 is met, they write no `.npz`/`.npy` file and no ArtifactStore artifact anywhere under `X:/Downloads/projects/topo-pilot/` (including `topo-pilot-hws`, `hwsb-store` and `k4b-store`). No `.npz`/`.npy` is committed under `tools/hwsb` or `tests/hwsb`. For J-B1 and DRY, `hwsb_meter_bind` sets the meter `out` and `TEMP_ROOT` to `X:/Downloads/topo-scratch/test_hwsb-<job>/`, and every pytest run uses `--basetemp X:/Downloads/topo-scratch/test_hwsb-<job>/pytest`. The dry store is `X:/Downloads/topo-scratch/hwsb-dry/`, and no file in it is named `HIST_*.npz`. After each of J-B1 and DRY, a read-only header inventory (`k4b_registry.inventory` over the project root) must show no new history file, identity reference, ObservationSet root or unreadable file in any directory compared with the record taken before the job; any difference stops for coordinator review. (RC-5; C2ND's scratch reader reads only `HIST_*.npz` outside `test_*` directories, `C2ND-DESIGN-v1.md:458` [V], so `hwsb-dry` and `test_hwsb-<job>` are ignored, as the review verified, OPEN-4 ruling.)
  2. Real-process histories in memory (the DRY integration smoke, KB2, KB6) and every persisted stage-B history are generated only when no other study holds a live history-generation reservation.
  3. `hwsb-store` receives no history file or ObservationSet before the coordinator has accepted C2ND's S5 with no pending S5 rerun, or C2ND is terminal. If C2ND later needs a registry rebuild, its registry must add a `hwsb-store` reader first. It may exist earlier holding only JSON. If C2ND stalls for more than a day, the coordinator asks the owner (OPEN-4 ruling).
- **Record.** KB0 checks the coordinator's dated record of C2ND's state and of any other reservations (the K4b §3.5 W3 attestation pattern, `K4B-FROZEN-v1.md:278-280`) [V].
- **Worktree.** Stage-B code is developed in the existing `topo-pilot-hws` worktree on a new branch `hwsb-impl`, not in a new top-level directory. A new worktree after C2ND's freeze would be an unlisted directory, and main tracks an `.npz` file (`docs/proposals/X5_G1_VERIFICATION_OUTPUTS/verification_arrays.npz`) [V].

---

## 7. Synthetic dry run (addendum 25 rule 4; before the execution freeze)

The real driver, records, gates and report run end to end in `X:/Downloads/topo-scratch/hwsb-dry/` under the DRY scope. Persisted histories come only from synthetic tiny worlds. The real-architecture smoke keeps its w\* rows in memory and runs under P-SCHED rule 2. Planted fixtures are labelled as fixtures. Any defect is fixed before the freeze; no threshold is tuned.

| # | Case | Expected |
|---|---|---|
| DRB1 | Tiny world (HWS DR1 world: W = 6, H = 2, 3 centres, σ = 1, p = 0.5, but L = 32), a tiny model (1 layer, d_model 16, 2 heads, d_mlp 32), 200 steps, 4,096 train rows; driver TRAIN → EVAL | runs; records complete; all gate functions return values |
| DRB2 | Real E4 architecture, 20 steps (TrainConfig checkpoints 0, 10, 20), 2,048 in-memory w\* DRY rows | shapes, BOS 36, vocab 37/36, checkpoint artifacts and records valid; the stage-B callback's checkpoint ids and checksums equal `LearnerStage.run`'s on the same inputs, bitwise; both runs use a `MemoryBackend` ArtifactStore; nothing is persisted |
| DRB3 | Config identity: the frozen stage-B ModelConfig/TrainConfig `asdict` equal E4 checkpoint `c3358e3cb9c352fb` `extra.json` field by field | equal; a planted change in any field is refused |
| DRB4 | The stage-B sampling path with E4 scopes equals `DatasetStage` tokens bitwise (small `DatasetConfig`, MemoryBackend store) | bitwise |
| DRB5 | B1–B3 on planted predictives: p = q32 → regret 0, captured 1; p = q4 → d̄ = 0, L ≤ 0; p = q1 → captured 0; permuted naming → canonical re-indexing exact; marginals sum | exact (≤ 1e-12) |
| DRB6 | Stage-B logits equal `ActivationExtractor.extract` logits on a tiny model and in-memory ObservationSet/HistoryIndex | bitwise |
| DRB7 | Charts: planted 128-d activations of a known phase (noisy circle) → C0-cal and C0-val PASS; scrambled → GIANT failure → NO_CIRCLE; ledger claims, freeze and re-hash; step-0 INIT_UNAVAILABLE path | as stated |
| DRB8 | Partial planted support → X±, missing mass and width exact; X− ≤ X+ | exact |
| DRB9 | `hwsb_gates.ladder_pilot` with K4b's three MODELS keys and K4b's seeds equals `k4b_stats.ladder` (`k4b_stats.py:159`) [V] bitwise; with two keys it follows the §4 rule; MDE boundary equality | bitwise / exact |
| DRB10 | B5: planted mean X− giving ĉ = c_min passes, one ulp below fails; the 12,288 fallback when B6 fails | exact |
| DRB11 | Outcomes: every row of §5.1, the precedence and every licence filled from synthetic numbers | exact |
| DRB12 | Law enclosure: σ = 5/4 equals the old enclosure exactly (δ computed as 0, lo/hi and every returned Fraction identical); σ = 7/4 and 3/2 BOUNDED; at σ = 7/4, δ > 0 and δ ≤ u·Q_max; a planted narrower enclosure caught by an independent 200-digit Decimal check on sampled entries; module state restored after every call | as stated |
| DRB13 | Registry reader on a synthetic hwsb-store: every file found; a missing, renamed or unreadable file fails closed; digests = `scores.history_digests`; named → canonical inversion exact | as stated |
| DRB13b | Meter binding and pytest placement (RC-5) | the meter binding's effective TEMP_ROOT and basetemp are under a `test_`-prefixed topo-scratch folder |
| DRB14 | Records and budget: exclusive-create refusals; the 3× hold at a training callback (planted CPU function) holds with ~0 CPU, continues on CONTINUE, ends INCONCLUSIVE on STOP; a lost process is never restarted from weights; per-stage and cumulative triggers; a run held at step 10 and continued gives checkpoint checksums bitwise equal to an unheld run (RC-14) | as stated |
| DRB15 | G0 needles: planted true and false hits classified (the D-0127-1 whole-token rule); `hwsb_known.classify_hits` equals `classify_seed_hits` bitwise with the HWS fragments (RC-3) | as stated |
| DRB16 | H2-B: a planted eval/train collision → FAIL_TECHNICAL/LINEAGE | as stated |

**Pass:** every expected result exactly. The report is committed and bound to the implementation hash, and the coordinator accepts DRB1–DRB16 (with DRB13b) before the execution freeze. **Cost:** about 300 CPU-s [W] (HWS dry 18 s and X6ZC dry 245 s measured, `ah/jobs/0126/review.md:9-10`, `ah/jobs/0132/review.md:3`) [H]; DRB1 and DRB2 dominate.

---

## 8. Budget stages and cost (addendum 26; all stage-B CPU outside the 12 CPU-h line of addendum 29, addendum 32 item 4 and the OPEN-1 ruling)

### 8.1 Measured basis
- **Training at 1 thread [H].** X5 G1 trained six models of this exact architecture and TrainConfig (5,000 steps, batch 128, 27 checkpoints with dev CE) at 1 thread on this machine: `cpu_s` 2,345.0; 2,352.5; 2,820.9; 2,321.3; 2,317.6; 2,614.6, mean 2,462.0 [W]; peak memory 0.70 GB (`X:/Downloads/projects/topo-pilot/x5g1t-research-store/tables/train/*/run.json`, keys `cpu_s`, `threads` 1, `peak_memory_bytes`) [V]. E4's grid has 15 fewer dev-CE evaluations (about 3.9 CPU-s each at 1 thread, `ah/jobs/0008/report.md:69`) [H], so the per-model central is **2,425 CPU-s** including data generation (about 8 CPU-s per 131,072-row draw, `x5g1t-research-store/tables/pools/run.json` steps) [H/W]. Range 2,300–2,900.
- **E4 itself** was not metered: wall 863.7–957.1 s per model at 6 threads (MetricRecords `408845d2a8be6779`, `a60ce9a530a2ad0f`, `37657d8490ba9e17`) [V]. At 1.148 CPU-s/update (6 threads) that is about 5,740 CPU-s per model [W from H]. The 6-thread fallback would be 2.4× the 1-thread cost.
- **Evaluation [H/W].** Scoring 4,096 rows at float32 1 thread costs about 7 CPU-s (x5g1t dev-analysis steps) [H]. Six float64 activation passes of 3,072 rows, PH on 512 points (~0.4 s each, `K4B-FROZEN-v1.md:291`) [H], oracle moments on 10,240 rows, two 5,000-draw bootstrap families and the separation digests of 280,576 rows sum to **≈ 400 CPU-s** [W]. There is no Decimal certificate and no 6-million-digest registry, which dominated K4b E1/E2.
- **Preflight [H].** The HWS J1 preflight (1,390 tests) took 332.8 CPU-s (`ah/jobs/0126/review.md:7`) [V].

### 8.2 Stage forecast and 3× thresholds [W]
| Stage | Content | Central CPU-s | Range | Stage 3× | Cumulative central | Cumulative 3× |
|---|---|---|---|---|---|---|
| P0 | merge `hws-impl` into main (--no-ff), docs(index), branch `hwsb-impl` | 0 | — | — | 0 | — |
| J-B1 IMPL | metered tests: tests/hwsb, preflight `tests/{world, process, dataset, oracle, oracle_profile, circle_history, k4b, hws, learner}`, `check_file_sizes` | 600 | 350–1,200 | 1,800 | 600 | 1,800 |
| DRY | DRB1–DRB16 | 300 | 100–900 | 900 | 900 | 2,700 |
| KB | KB0 (G0 ≈ 90, `ah/jobs/0129/review.md`) + KB1–KB7 (KB2 ≈ 165: 100 updates × 1.148 + 3 dev CE at 6 threads + data) | 500 | 250–1,200 | 1,500 | 1,400 | 4,200 |
| TRAIN | 2 sequential meter jobs × 2,425 | 4,850 | 4,600–5,800 | 14,550 (per model 7,275) | 6,250 | 18,750 |
| EVAL | H2-B, B1–B9, report, HANDOFF | 400 | 150–1,200 | 1,200 | 6,650 | 19,950 |
| **Total** | | **6,650 (1.85 h)** | 5,450–10,300 | | | |

**Pauses (addendum 26 item 5; addendum 32 item 3).** CPU is measure-only (`--max-cpu inf --max-wall inf`). Both triggers are checked at every item boundary (each KB check, each model, each gate group):
- **per stage:** running stage CPU > 3× its central;
- **cumulative:** running total > 3× the cumulative central through the current stage.

Training cannot be paused and resumed from weights (the Trainer has no restore; the X5 review rule, `ah/jobs/0008/review.md:9`) [V]. Instead, the checkpoint callback **holds** the live process, keeping its in-memory state at ≈ 0 CPU, when either holds:
- from step 1000 on, the projected CPU (CPU so far × 5000/step) exceeds 7,275 s;
- the CPU so far exceeds 7,275 s.

The coordinator then asks the owner: CONTINUE resumes, STOP ends that model as INCONCLUSIVE/RESOURCE_OR_AUTHORITY. A process lost while holding is never restarted from weights. The hold report contains the step, CPU so far and the projection only; dev-CE values are not shown until the model's training is complete. Meter flags `--max-cpu inf --max-wall inf`. (RC-14)

**Frozen extension rules.**
- (X-1) No stage grows on a scientific reading. B1, B4, B5 and B6 failures go to the owner: no extra seeds, rows, steps or larger model.
- (X-2) A technical correction is allowed only for a documented implementation or environment defect, at most two per defect (HWS §9.4 pattern, lines 536-540) [V]. An interrupted training job is rerun from scratch with identical seeds (never resumed from weights). Checkpoints the interrupted attempt already wrote must re-appear bitwise, and the attempt is archived under `superseded/`. A correction made after any decision-bearing gate value (B1, B4, B5, B6) has been computed needs an owner decision if it could change that value. Chart construction ledgers are never reset or edited. A rerun that would need a second claim for a (model, role) pair is a new attempt in a fresh store under `superseded/` lineage and needs an owner decision. Every original gate value stays in the report. (RC-4)
- (X-3) KB2's pre-registered secondary reading is the only tolerance alternative.
- (X-4) The stage-C N, model count and budget come from B6 and B7, which is the adaptive link of addendum 26 item 2.

**Ledgers.** The per-job meter ledgers stay in each job's `out` (`test_hwsb-<job>/` for J-B1/DRY, `hwsb-store/` for KB/TRAIN/EVAL). The study ledger of record is `agent-handoff/HWSB_CPU_LEDGER.json` (OPEN-1). It is appended after each job and written atomically (temp file in the same directory, then `os.replace`). The cumulative trigger reads it. It is never summed into the addendum-29 ledger. (RC-7)

**Wall and resources [W].** KB ≈ 10 min; training ≈ 45 min per model at 1 thread, run sequentially as separate meter jobs so per-model CPU is exact (the D-2a launcher trap, `ah/jobs/0033/report.md:114-118`) [V]; evaluation ≈ 10 min, about 2–2.5 h in all. RAM < 1 GB per process. Store < 150 MB (24 checkpoints of 3.2–9.7 MB, `ah/jobs/0008/report.md:71`) [H]. TEMP/TMP/TMPDIR and the meter `TEMP_ROOT` under `X:/Downloads/topo-scratch/test_hwsb-<job>/` for J-B1 and DRY, and under `hwsb-store/tmp/` for KB/TRAIN/EVAL (after P-SCHED rule 3; covered by the B9a(i) recursive inventory and the HANDOFF file list, as in the HWS pattern); disk floors C: ≥ 2 GB, X: ≥ 30 GB; meter memory cap 8 GiB; `PYTHONPATH=<worktree>/src`, venv interpreter with `-s`.

### 8.3 Plain-language forecast for the owner (when training starts)
"We are now training two small models in the new world that the sweep chose. It is the same recipe as before, with only the observation noise changed. Each model should take about 40 minutes of computer time, one after the other. The training and the checks after it should come to about an hour and a half of processor time, roughly the same on the clock. This is counted separately from the 12-hour line. If any part runs past three times its estimate, I will stop and ask you before going on. At the end I will tell you whether the models learned, whether the circle formed, and whether a full test would be large enough to give a clear answer. If so, I will also say how big that test would need to be and roughly what it would cost."

---

## 9. Reuse and footprint

### 9.1 New code: `tools/hwsb/` on branch `hwsb-impl` (from main after P0; each .py ≤ 400 lines; no existing file edited)
| File | Contents | Lines [W] |
|---|---|---|
| `PROTOCOL_HWSB_v1.md` (byte copy of the frozen plan), `API.md`, `CONTRACT.json`, `TEST_PLAN.md` | committed first: names, scopes, seeds, sizes, thresholds, references, rates, store layout | — |
| `hwsb_config.py` | constants, scopes, masters, seeds, paths, rates, reference record paths and hashes | ≈ 120 |
| `hwsb_data.py` | process build into the store via `WorldStage`/`ProcessStage`; train/dev ObservationSets; evaluation blocks; sequence IDs; H2-B; `registry_digests` | ≈ 290 |
| `hwsb_train.py` | `Trainer.fit` composition with the `LearnerStage`-mirroring callback; thread setting; hold rule; per-model records; the KB2/KB3 sentinel-stop harness | ≈ 220 |
| `hwsb_eval.py` | logits; B1–B3; activations; oracle moments; X± and support | ≈ 280 |
| `hwsb_gates.py` | B4 orchestration (`k4b_charts`), `ladder_pilot`, B5, B8a/B9a checks, outcome precedence, licence fill, HANDOFF | ≈ 320 |
| `hwsb_law.py` | the reviewed enclosure and the binding context manager | ≈ 140 |
| `hwsb_known.py` | G0 needles; `classify_hits` (mirror of `classify_seed_hits`, fragments from `CONTRACT.json`); KB0–KB7 | ≈ 330 |
| `hwsb_driver.py` | stages KB, TRAIN (one model per job), EVAL, REPORT; GATES/STAGES records; ledger; CLI | ≈ 330 |
| `hwsb_dry.py` | DRB1–DRB16, DRB13b | ≈ 350 |
| `hwsb_meter_bind.py` | thin main over `k4b_meter_bind` (the `hws_meter_bind` pattern), MEMORY_CAP 8 GiB; meter `out` and `TEMP_ROOT` under `X:/Downloads/topo-scratch/test_hwsb-<job>/` for J-B1/DRY (§6.4 rule 1), `out` = `hwsb-store` and `TEMP_ROOT` = `hwsb-store/tmp/` for KB/TRAIN/EVAL | ≈ 80 |

About 2.4k lines [W]. Tests (≈ 1.4k lines) in `tests/hwsb/` are written by two independent authors who never read `tools/hwsb/*.py`:
- **Author A:** B1–B6 maths on planted arrays, the ladder mirror, c_min, outcomes and licences, the enclosure proof checks.
- **Author B:** data streams and IDs, the E4-path equalities, records, registry reader, hold rule, meter binding, basetemps outside the project root, and the independent test of the B8a enclosure (OPEN-3 ruling).

`AUTHORSHIP_A.md` and `AUTHORSHIP_B.md` record what each author read. No formatter is run over `tests/` (project lesson). After acceptance, `tools/build_code_index.py` is run and its output committed in its own `docs(index): …` commit. Store: `X:/Downloads/projects/topo-pilot/hwsb-store/` with `FREEZE.json`, `AUTH_*.json`, `GATES.jsonl`, `STAGES.jsonl`, `cpu_ledger.json`, `artifacts/`, `hist/`, `stages/{KB, TRAIN, EVAL, S4a}/`, `REPORT.json`, `HANDOFF.json`, `superseded/`, `logs/`. `stages/S4a/PRODUCTION_FROZEN.json` is required by the reused `k4b_charts.FROZEN` (`k4b_charts.py:22`) [V].

### 9.2 Six-field reuse assessment (existing · missing · smallest change · invariants · regression checks · next extension)
| Part | Existing (reused unchanged) | Missing | Smallest change | Invariants | Regression checks | Next extension (not built) |
|---|---|---|---|---|---|---|
| Learner | `LearnerStage.run`, `Trainer`, `ModelConfig`, `TrainConfig`, `serialise_state`, `load_model` (`learner/stage.py:29-106`) [V] | a hold hook, per-model CPU | composition in `hwsb_train`: `Trainer.fit`'s `on_checkpoint` callback mirrors `LearnerStage`'s `save` and adds the hold; tested bitwise against `LearnerStage.run` (DRB2) | deterministic algorithms; init and batch order from SeedTree(master) | `tests/learner`; KB2, KB3; DRB2 | a `steps` extension only by a new protocol |
| Data | `HMMSampler`, `SequenceLayout`, `PublicTokenDataset`, `process_code`, `make_sequence_ids`, `check_disjoint`; `DatasetStage` and `PanelBuilder` as references (KB2, KB6) | stage-B scopes; evaluation blocks without w33 | ≈ 40-line sampling path mirroring `_sample_all` | named = perm[canonical]; one `sample` call per table | `tests/dataset`; DRB4; KB2 | — |
| World/process | `WorldStage`, `ProcessStage.run_transition`/`run_emission`, `OverlapGaussian`, `EmissionConfig`, `TransitionConfig` | none (tier 0) | none | σ is the only change; envelope as E4 | `tests/world`, `tests/process`; KB1 | tier 1/2 builders (HWS Q2) |
| Contracts | `ArtifactStore`, `LocalFSBackend`, `ObservationSet`, `Checkpoint`, `SeedTree`, `payload_checksum`, `make_artifact_id` | none | none | content-addressed ids; exclusive writes | KB1, KB2 | — |
| Oracle | `oracle_profile.{suffix_posterior, canonical_emission, circle_features, validate_process}`; `hws_oracle.{beliefs, predictive, circ_marginal, kl_rows}`; `k4b_scores.{oracle_moments, oracle_phase, phase_scores, endpoint_arrays, m4_phase, sha_phase, support_report}`; `PredictiveMetrics`, `LearningGate`; `BayesFilter`, `LastSymbolPosterior` (KB6) | none | none; `k4b_scores.control_arrays`/`support_entries` are **not** used (bound to `k4b_config.MODELS`, `k4b_scores.py:144-159`) [V] | canonical arrays shared by models | `tests/oracle*`, `tests/hws`; KB5, KB6 | — |
| Model evaluation | `c1_model.{load_model64, model_inputs, activations}`; `ActivationExtractor` as reference | float32 logits at index 32 | 3-line forward mirror, tested bitwise (DRB6) | logits never mixed with float64 activations | KB6; DRB6 | — |
| Charts | `k4b_charts.{build_chart, InitLedger, open_ledgers, freeze_production, require_frozen, extend, c0_val_gate, init_charts}`; `c1_chart`; `k4b_config.chart_cfg` | per-model independence (`c0_cal` stops at the first failure, `k4b_charts.py:95-104`) [V] | call `build_chart` per model | each construction claimed once, never retried; production frozen before VAL activations | `tests/k4b`; DRB7 | — |
| Statistics | `c1_means.{bootstrap_means, quantile_with_rank, rank_for, tree_mean}`; `precision.{sd_b4_draws, mde, centered_draws}` (`tp/tools/x4_circle_history/precision.py:22, 39, 52`) [V]; `k4b_cert.F_plan` | a ladder keyed by pilot models (`k4b_stats.ladder`/`sd_upper` bind `MODELS`, `k4b_stats.py:20, 92-101, 159`) [V] | `ladder_pilot` mirror (≈ 40 lines), bitwise equal to `k4b_stats.ladder` on K4b keys (DRB9) | one index stream per bootstrap; ranks checked | `tests/k4b`; DRB9 | 3-model stage-C P1 uses `k4b_stats` directly |
| Law bound | `process_law.process_law_bound` (`process_law.py:222`), `LAW` (`:25-33`) [V]; `hws_exact.law_bound_report` pattern | an enclosure for non-terminating logits | `hwsb_law` (new, reviewed) bound in a restoring context | the transport proof unchanged except lo/hi widening | KB4; DRB12; independent review | stage-C binding row 5/12 reuses it |
| HWS exact/G0 | `hws_exact.{p_d2a, exact_world, expected_envelope}`; `hws_driver.{seed_search, _needle_in}` (`classify_seed_hits` as bitwise reference only) | a stage-B hit classifier | `classify_hits` mirror (≈ 15 lines) | whole-token needle rule; requires P0 (merge) | `tests/hws`; DRB15 | — |
| Records/meter | `stage_records.{write_new, save_npz, record_gate, sha256}`; `k4b_meter_bind` via the `hws_meter_bind` pattern; `winjob` | per-model meter jobs | `hwsb_meter_bind` | exclusive create; measure-only CPU | DRB14 | — |
| Registry | `scores.history_digests`; `k4b_registry.inventory`/`classify` for the self-check | the stage-B reader | `registry_digests` | fail closed | DRB13; B9a | stage-C reader `hwsb` |

---

## 10. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Wider emissions make beliefs less sharp (‖m32‖ quantiles 0.035 … 0.90, median about 0.88, `store:SELECTION.json:400`) [H] | GIANT or C0-val failure | B4 on fresh data; NO_CIRCLE outcome; owner decides the fallback |
| C2ND's fail-closed inventory sees a new history store | C2ND REG2 INCOMPLETE | P-SCHED; JSON-only store until C2ND's S5 is accepted with no pending rerun; reuse the existing worktree |
| Thread count changes the floating-point order | non-reproducible models | KB2 (E4 threads, bitwise), KB3 (1 thread, determinism) |
| Environment drift since E4 | KB2 bitwise failure | the pinned lock; the pre-registered secondary reading |
| The reviewed enclosure is wrong or unreviewable | no Z_bound for w\* | B8a review; KB4 exact known case; DRB12 independent check; ≤ 2 corrections |
| Two pilot models under-represent the seed spread | stage-C models fail gates | "both" rule; stage C keeps its own gates; Q4 |
| Two-model joint projection is weaker than three | N_C too small | stage C may keep a raise-only P1 (OPEN-2 ruling: stage-C planning) |
| Pilot numbers read as findings, or reaching stage-C roles | overclaiming; loss of result-blindness | the licence wording of §5.2; report labels "pilot, uncertified"; HANDOFF carries no effect estimate (RC-6) |
| Training process lost during a hold | incomplete model | INCONCLUSIVE; no restart from weights; per-model jobs |
| Venv launcher hides child CPU | wrong per-model CPU | the meter job per model, not a supervisor |
| Worktree imports main's `src` | wrong code under test | `PYTHONPATH=<worktree>/src`; `-s`; import check in preflight |
| Pytest basetemps, meter temp files or fixtures under the project root | registry INCOMPLETE elsewhere | §6.4 rule 1 (RC-5): basetemp and `TEMP_ROOT` under `topo-scratch/test_hwsb-<job>/`; no `.npz`/`.npy` committed; before/after header inventory; DRB13b |
| Non-finite loss in w\* | a model lost | FAIL_TECHNICAL/NONFINITE; owner review; no seed swap |
| HWS code unmerged | missing imports | P0 merge before branching |
| Late technical corrections steer an outcome | biased result | X-2 (RC-4): owner decision after a decision-bearing value exists; ledgers never reset |

---

## 11. Owner questions (science and risk only; each with a registered default)

1. **Stage-C models.** Should stage C train its own three models, so that the pilot models never enter stage C and their capture can be read by the coordinator and the owner (never by stage-C writers, test authors or reviewers, RC-6)? **Default: yes** (alternative: reuse the pilots, with B5 dropped and validation means sealed, §6.2).
2. **Pilot size.** Two pilot models. **Default: two.**
3. **The power standard of B5.** 80 % planned power at the pilot capture (shared rule 3, K4b MDE), stricter than the 50 % implied by HWS §10.2's formula. **Default: 80 %**, with the §10.2 value reported.
4. **A one-model failure** (B1 or B4 in 1 of 2) or any non-PASS outcome. **Default: stop with that outcome and ask; nothing automatic** (no third seed, no fallback world, no recipe change).
5. **Prediction-forcing checks B2/B3.** **Default: report-only** (B5 measures the representation directly).
6. **Stage-C model count.** **Default: 3** (HWS §11 row 4); 5 only with a reviewed generalisation.

Decided by the coordinator (procedural, registered here): one thread (with the RC-9b six-thread fallback ruling); KB2/KB3 tolerances; P-SCHED; the single stage-B ledger `agent-handoff/HWSB_CPU_LEDGER.json`; reading the S3 w\* table in KB5; no full E4 reproduction; reuse of the `topo-pilot-hws` worktree.

---

## 12. OPEN items (all closed by coordinator rulings)

- **OPEN-1. Ledger line. CLOSED.** All stage-B CPU (implementation tests, dry run, known-case checks, training, evaluation) goes in its own ledger, `agent-handoff/HWSB_CPU_LEDGER.json`, outside the 12 CPU-h line of addendum 29. Addendum 32 item 4 puts stage B outside that line and under the adaptive rules of addendum 26. The ledger is reported beside the addendum-29 ledger and never summed into it. It is written atomically (RC-7, §8.2).
- **OPEN-2. "K4b ladder rule 3". CLOSED.** The reading is K4b §7.2 under addendum 25 rule 3 (B6). Whether stage C keeps its own raise-only precision check is left to stage-C planning, which is not approved.
- **OPEN-3. The B8a enclosure. CLOSED as a design question; an implementation obligation remains.** The result-blind reviewer found the argument sound and fixed the definition of δ (RC-1, applied in §4 B8a, KB4, DRB12). At implementation it needs an independent author-B test and a reviewed proof note in `tools/hwsb/`, with δ defined as in RC-1. B8a stays a gate.
- **OPEN-4. Scheduling against C2ND. CLOSED.** Implementation, the tests and the synthetic dry run may start now, under §6.4 rule 1 (RC-5). The reviewer verified that `X:/Downloads/topo-scratch/hwsb-dry/` with non-`HIST_` names and `test_`-prefixed scratch folders are ignored by C2ND's inventory, and that a JSON-only `hwsb-store` is no violation. No history file enters `hwsb-store` until the coordinator has accepted C2ND's S5 with no pending S5 rerun, or C2ND is terminal (RC-15). If C2ND stalls for more than a day, the coordinator asks the owner.
- **OPEN-5. Torch version. CLOSED.** Accepted with the registered fallback. KB2 records the torch version actually found in the E4 metadata or lock, the version in use, the thread count, and which reading (bitwise or the secondary reading of RC-2) applies.

---

## 13. Provenance

| Input | Identity |
|---|---|
| Request | `ah/planning/requests/coord-hws-stage-b-20261027.md` sha256 498a607b…1c1a1538 (verified) |
| v1 and its review (v2 inputs) | v1 `coord-hws-stage-b-20261027.claude.md` 3467d41f1f604989…; review `….claude-reviewer.md` ee406c3c665cff1d…; rulings `….rulings.md` d4e2d8f5b72e1bb8…; OPEN rulings `….open-rulings.md` 7be74779fd6c5869… |
| Protocols | `HWS-FROZEN-v1.md` (§2, §7, §9, §10, §11, §12.3 read); `K4B-FROZEN-v1.md` (§1.4, §3, §4, §5.5, §7, §8 read); `C2ND-DESIGN-v1.md` §6.2–§6.5 |
| Owner addenda | 25, 26, 28, 29, 30, 31, 32 (`ah/archive/owner-decisions-20261015/`) |
| Rules | `GAP_CLOSING_EXPERIMENTS_HE.md` §2; `NEXT_RESEARCH_AND_WORKFLOW_EN.md` (reuse-first) |
| Stage-A records | `store:SELECTION.json` (243f7324…), `store:stages/FINAL/REPORT.json` (bd460cee…), `store:stages/S3/worlds/W12-q1-s1.75-p0.2.json` (164c6038…), `store:worlds/W12-q1-s1.75-p0.2.json`; `ah/jobs/0126`–`0136` reviews |
| E4 records (metadata only) | `tp/artifacts/{Checkpoint, ObservationSet, HistoryIndex, EmissionSpec, WorldSpec, TransitionSpec, MetricRecords}/*/meta.json` and `extra.json`; `tp/reports/E2/summary.md` |
| CPU records | `ah/jobs/0007`, `0008` (X5 benchmark); `x5g1t-research-store/tables/*/run.json`; `ah/jobs/0033` (D-2a); `ah/jobs/0055`, `0057` (K4b) |
| Code | `tp/` at fab0499 (learner, dataset, process, oracle, prediction, experiment/s3, activations, contracts, tools/k4b, tools/c1prime/c1_model, tools/x4_circle_history/process_law, precision, scores, tools/c2_readout/c2_registry); `hws/tools/hws/` at 6101eae |
| Code index | `--check` current at fab0499 |
| Not read | the public research-summary paths; any payload, `state.pt`, `sealed/` or `hist/` array; any other output of this round besides the three v2 inputs above |

---

## 14. Change log v1 → v2

Base: v1 `coord-hws-stage-b-20261027.claude.md` (sha256 3467d41f…, unchanged). Every RC fix below is the reviewer's exact text, applied verbatim (RC-1..RC-18 accepted in `….rulings.md`). "Choice" records where a fix left an option and the stricter one was taken; "adaptation" records a purely editorial join.

| Item | Where applied | Choice or adaptation |
|---|---|---|
| Header | status line `STATUS: v2, pending confirmation`; title HWSB-v2; revision paragraph; reading statement | — |
| RC-1 (MAJOR) | §4 B8a computation cell replaced from "The reviewed enclosure" to "restores all three in `finally`"; DRB12 "(δ = 0)" replaced and "at σ = 7/4, δ > 0 and δ ≤ u·Q_max" added; KB4's σ = 5/4 sentence restated with the exact δ | Adaptation: the v1 parenthetical after the replaced range now starts "(This is the `hws_exact.law_bound_report` pattern …)"; the round-to-nearest citation (`error_bound.py:54-65`) and the OPEN-3 obligations were added to the cell |
| RC-2 (MAJOR) | §3 KB2 Pass cell: secondary reading replaced | — |
| RC-3 (MAJOR) | §3 KB0 parenthetical replaced; §9.2 row "HWS exact/G0" Missing and Smallest change set; §2.3 dry-run seed sentence added; DRY row names masters 629901/629902; DRB15 and the `hwsb_known.py` row mention `classify_hits` | "requires P0 (merge)" kept, moved to the Invariants column |
| RC-4 (MAJOR) | §8.2 X-2 appended; §10 new risk row | — |
| RC-5 (MAJOR) | §6.4 rule 1 replaced; DRB13b added; §8.2 resources; §9.1 `hwsb_meter_bind.py` row; §10 basetemp risk row | **Choice:** — |
| RC-6 (MAJOR) | §6.1 HANDOFF paragraph added; §2.2, §6.2 and §11 Q1 now say pilot effect numbers go to `REPORT.json` only; §10 risk row | — |
| RC-7 | §8.2 "Ledgers" paragraph replaced; summary "Cost"; §8 heading; §11 decided list; OPEN-1 closed | — |
| RC-8 | §4 B4: step-0 control and `freeze_production(out, {j: res for passing j}, init, {})` inserted after C0-cal; the separate "Step-0 control" sentence deleted; §4 preamble replaced | Adaptation: the inserted step-0 sentence keeps v1's descriptive status and citation (`k4b_charts.py:107-121`) |
| RC-9 | (a) §5.1 row 1; (b) §3 KB3 appended | — |
| RC-10 | §3 KB2 appended | The KB record also states which reading applies (OPEN-5 ruling) |
| RC-11 | §3 KB4 "on the KB2-identical E4 arrays" replaced | — |
| RC-12 | (a) DRB2 appended; (b) CAL and VAL sequence-ID cells; (c) §6.3 keys, also used in the LGATE row of §2.3; (d) §2.3 Sampling | — |
| RC-13 | §4 B5 "On failure"; §3 KB0 needles | **Choice (stricter):** 620211 dropped (needles 620212–620214), leaving no seed without a stated use |
| RC-14 | §8.2 hold paragraph appended; DRB14 extended; pauses line now `--max-cpu inf --max-wall inf` | — |
| RC-15 | §6.4 rule 3 replaced; hazard bullet citation added; summary "Schedule"; §10 C2ND risk row; OPEN-4 closed | — |
| RC-16 | §6.3 merge-and-exclusions bullet; §6.2 AUTH bullet | — |
| RC-17 | §4 refinement 1 appended | — |
| RC-18 | (a) §2.5 LGATE sentence; (b) §8.3 owner paragraph | — |
| OPEN rulings | §12 rewritten: OPEN-1..5 closed with the ruling text, amended by RC-7 (single atomic ledger) and RC-15 (C2ND completion condition). OPEN-3's implementation obligation is kept (B8a cell; author B in §9.1). The OPEN-4 "more than a day" owner rule is in §6.4 rule 3. The OPEN-2 ruling is in §4 refinement 2 and §10 | — |
| Provenance | §13: v2 inputs with sha256; the "not read" row updated | — |

No RC item was left unapplied. No scientific threshold, gate, outcome rule or forecast changed except where an RC fix says so (RC-9b registers a six-thread fallback forecast of 2 × 5,800 CPU-s with a 17,400 CPU-s per-model hold, usable only by a coordinator ruling before training).
