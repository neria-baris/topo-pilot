# X5 G1 — six-model training protocol DRAFT v2 (x5g1-train-draft-2)

14 October 2026, handoff job 0008.

**NOT FROZEN. NOT AUTHORISED.**

* This supersedes [draft-1](X5_G1_TRAINING_PROTOCOL_DRAFT.md), which is kept byte-identical, and applies the job-0007 review.
* Inputs: the gate (FEASIBLE, D-066), the verification (CONSISTENT, D-067) and the [technical benchmark](X5_G1_TECHNICAL_BENCHMARK_REPORT.md) (B1 RESOLVED at 1 thread).
* Changes from draft-1 are listed in §11.

## 1. Hypothesis, estimand and scope

* **H5 (G1).** For the defined process pair, the conductance kernel a020 delays the **grid-defined** regret-threshold event by **≥ 250 steps** compared with the flat kernel a0, in each of the three paired models.
* **Estimand.** Per pair p, Δ_p = τ_grid(a020, p) − τ_grid(a0, p), where τ_grid is defined in §4.
* **What a positive result means.** Slower learning by this algorithm on this process pair. It is **not** a curvature effect: the gate showed a large movement-speed confound, since a rate-matched flat kernel nearly reproduces a020's mixing summaries.
* **Excluded:** a third training arm, PH, G2, density, X6, an optimizer or architecture search, and any evaluation-driven tuning.

## 2. Fixed inputs and configuration (asserted at run start from metadata)

**Process.**

| Item | Value |
|---|---|
| World | `21feee1d8ee5422e` |
| T a0 | `e4dafc7b9785c172`, payload sha f94340a6…68dd |
| T a020 | `08a22a03727d2295`, sha 663d0011…6b7b |
| E | `3633ac27dab50cf4` (sha f5b6197c…b1fb), with its stored `symbol_perm`, for all six models |
| π | uniform |
| Fixed normalizers (D-066) | G_C(a0) = 0.27133797235249024 and G_C(a020) = 0.2939268960103646. Uncertainty is conditional on them; they are not re-estimated. |

**Model.** `ModelConfig` equal to the stored E3 metadata (checkpoint c3358e3cb9c352fb):

* vocab_in 37 and vocab_out 36; n_ctx 33;
* 4 layers, d_model 128, 4 heads, d_mlp 512;
* GELU, dropout 0, untied embeddings.

**Training.** `TrainConfig`, stored values: steps 5000, batch 128, lr 1e-3, warmup 200, cosine, weight decay 0.1, clip 1.0. **Fields changed from the stored literal:**

* `checkpoint_steps` → the §4 grid (stored: the 12-point E3 grid);
* `device` → `"cpu"` (stored: `"auto"`, which resolves to CPU with the installed CPU-only torch). Making it explicit prevents a silent device change; the computation is identical.

**Process setting (not a config field).** `torch.set_num_threads(1)`, as chosen by the benchmark. Interop threads are left at the default and recorded.

**Exposure.** 5,000 × 128 × 33 = **21,120,000 target tokens per model**, from 131,072 unique training histories per arm and master.

## 3. Lineage (public only; latents discarded)

**Masters, frozen.** 310001, 310002, 310003.

* Deterministic ID inspection was already done (job 0008, metadata only, no sampling).
* All 819,200 planned sequence IDs, across 14 distinct process codes, are unique and collide with **none** of the 3,440,640 stored main-store, calibration and B2 IDs.

**Generators.** Every pool is drawn with one `HMMSampler(T_arm, E[:, perm], π, SequenceLayout())` call per arm, and named = perm[canon]. The two arms of a pair use two **separately initialised** generators from the same seed.

| Pool | Stream | Size | Code |
|---|---|---|---|
| train (master m, arm) | `SeedTree(m).generator("x5g1-train-v1", "train", "cylinder", "overlap", "1.25")` | 131,072 | 9 |
| dev (master m, arm) | `SeedTree(m).generator("x5g1-train-v1", "dev", "cylinder", "overlap", "1.25")` | 4,096 | 10 |
| fresh test (arm; shared across masters) | `SeedTree(0).generator("x5g1-train-v1", "test", "cylinder", "overlap", "1.25")` | 4,096 | 11 |

**Sequence IDs.** `(process_code("cylinder", "overlap", "1.25", f"x5g1-train-v1:{split}:{arm}:{m}") << 32) | (code << 28) | index`. The test pool uses m = "shared".

**Persistence.**

* `ObservationSet` with split train / dev / test and config {role, protocol, arm, master, stream, namespace_code}, in an independent X5 training store.
* `DatasetStage` is not used. Its defaults stay unchanged.

**Learner input.** The learner sees only `topo_pilot.dataset.PublicTokenDataset`. (Draft-1 referred to it imprecisely; it is exported by `dataset`, not by `learner`.)

**Dev-set use.** The same dev pool serves both the trainer's dev-CE monitoring and the endpoint. This is allowed because neither selects anything.

## 4. Grid-defined endpoint

**Grid G**, 27 evaluation checkpoints: t_0 = 0, then 100, 200, …, 1000, then 1250, 1500, …, t_26 = 5000.

**PASS at checkpoint t.**

* Regret per dev history h: reg_t(h) = KL(q_C(h) ‖ p_model,t(h)) at p32, in nats.
  - q_C comes from `BayesFilter` with the arm's own T and the stored E, computed in experiment, never in the learner.
  - p_model,t comes from the stored checkpoint at step t.
* ratio_t = mean_h reg_t(h) / G_C(arm).
* **PASS_t** iff ratio_t ≤ 0.05 (threshold unchanged).

**Primary event.** τ_grid = t_j for the **smallest j ≤ 24** such that PASS holds at j, j+1 and j+2.

* An observed τ_grid is **exactly t_j**, with degenerate bounds [t_j, t_j].
* The prior-grid band (t_{j−1}, t_j] is a **descriptive resolution note only**. Without monotonicity it identifies no latent first-crossing time, and nothing is interpolated.

**Right-censoring.**

* The event is defined only on the observed window: a qualifying j must have j + 2 ≤ 26, i.e. t_j ≤ 4500. No extra runs or checkpoints beyond step 5,000 exist or are imagined.
* If no j ≤ 24 qualifies, τ_grid is **censored**, meaning "the event did not occur at any checkpoint where it could be observed". The valid one-sided statement is **τ_grid > 4500**: bounds (4500, ∞).
* A trailing PASS at 4,750 and/or 5,000 is reported descriptively as unconfirmed. Nothing is imputed, in particular not 5,000.

**Hand examples.**

| PASS pattern | τ_grid | Bounds |
|---|---|---|
| PASS from 1,000 onward | 1000 | [1000, 1000] |
| PASS 2,000; FAIL 2,250; PASS 2,500, 2,750, 3,000 … (non-monotone) | 2500 | [2500, 2500] (the 2,000 PASS is unconfirmed) |
| PASS 1,000, 1,250, 1,500; FAIL 1,750; PASS later | 1000 | [1000, 1000]; the later FAIL is descriptive (non-monotone after the event) |
| first PASS 4,750, PASS 5,000 | censored | (4500, ∞); trailing PASS reported |
| first PASS only at 5,000 | censored | (4500, ∞) |
| FAIL at 5,000, never confirmed | censored | (4500, ∞) |

**Difference bounds per pair.** With a020 bounds [Lc, Uc] and a0 bounds [Lf, Uf] (open at 4,500 when censored):

* D_low = Lc − Uf and D_high = Uc − Lf, with ±∞ allowed and never NaN (Uf = ∞ gives D_low = −∞; Uc = ∞ gives D_high = ∞).
* **Both observed:** D_low = D_high = Δ, a point.
* **a020 censored, a0 observed:** D_low = 4500 − t_f, as a strict bound Δ > 4500 − t_f; D_high = ∞.
* **a0 censored:** D_low = −∞.

## 5. Uncertainty: paired whole-curve bootstrap

* **Draws.** 2,000 per master, stream `SeedTree(m).generator("x5g1-train-v1", "endpoint_bootstrap")`.
* **Resampling.** Each draw resamples the dev indices i ∈ {0..4095} with replacement, **shared by both arms** (index i pairs the arms under common randomness). It applies the indices to **whole per-history regret curves**; checkpoints are never resampled independently.
* **Per draw.** Recompute both ratio curves, PASS sequences, τ_grid with its bounds, and D_low* and D_high*.
* **Quantiles.** `np.quantile(·, q, method="inverted_cdf")` at q = 0.025 and 0.975. These are order statistics, so they are valid with ±∞ and never interpolate.
* **Censored replicates** are kept and their fraction reported. Nothing is conditioned on crossing.
* **Scope.** The intervals are conditional on the fixed normalizers, the six trained models and the two processes. They do not express model-population or normalizer uncertainty.

## 6. Decision rule (all three pairs required; no replacement)

| Verdict | Condition |
|---|---|
| **SUPPORTED** | in **every** pair, D_low ≥ 250 (equality satisfies ≥ 250) **and** the bootstrap 2.5% quantile of D_low* > 0 |
| **REJECTED** | in **some** pair, the bootstrap 97.5% quantile of D_high* < 250, a valid upper-evidence bound |
| **INCONCLUSIVE** | anything else, including: contradictory evidence (the SUPPORTED and REJECTED conditions both hold); any failed, crashed or incomplete model; unresolved censoring; a failed check; a budget or STOP stop |

* No pair, seed or model is dropped or replaced.
* No significance level is attached. With three pairs the result is descriptive cohort evidence, and no population-level claim follows.
* **Relation to the outline.** The original "τ_curved − τ_flat ≥ 250, positive under paired resampling" is kept, with τ now the grid-defined event. This draft does **not** claim that the grid rule equals a latent continuous crossing time.

## 7. Secondary outcomes (descriptive)

* **From the dev curves:**
  - the area under ratio_t over the 27-point grid, using the trapezoid rule on the actual step spacing;
  - per-checkpoint ratios;
  - the fraction of censored bootstrap replicates.
* **Fresh test,** one evaluation per model at **step 5,000 only**, after all training and dev endpoints are final: regret in nats and regret/G_C.
* The fresh test provides no curve and no AUC. It selects nothing.

## 8. Execution controls

* **Order.** Masters 310001 → 310002 → 310003; a0 then a020 within each pair. **Never** two models at once. No retries; a failed model is recorded and kept, which makes the cohort INCONCLUSIVE.
* **Training composition.** The public `Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, on_checkpoint)` with an experiment-side `on_checkpoint`. It stores each grid checkpoint with the LearnerStage identity: config {run_key, step, model_config, train_config}, parents [obs_train, obs_dev].
* **Pairing.** run_key = ("x5g1", "cylinder", m) for **both** arms, which gives identical initial weights and batch order. Checkpoint IDs differ through their ObservationSet parents. The arm is recorded in an experiment manifest and every report.
* **Smallest learner change: export `serialise_state`.** The callback needs the existing serialiser, `learner.stage.serialise_state`, which is not exported today. Exporting it from `topo_pilot.learner` is a public-surface addition only, with no behaviour change. Its independent test must show bytes identical to `LearnerStage`. The alternative, duplicating the serialiser in experiment, risks identity drift and is not preferred. **Needs review.**
* **STOP and budget polling** happens at every grid checkpoint inside the callback. At the measured 0.389 s wall per update (1 thread), that is at most 250 updates ≈ 97 s plus about 4 s of dev CE, so **≤ about 2 min between polls**. Polling also happens between models and in every evaluation, bootstrap and export batch.
  - A STOP mid-model ends that model, keeps its checkpoints, and makes the cohort INCONCLUSIVE.
  - A usage hold during training means: let the current checkpoint interval finish at the next poll, persist the resume state, and never start a duplicate model.
* **Ledger and repairs.** All costs go to the X5 scientific ledger, with the job-0007/0008 repairs (full-hash before/after checks, guarded exports with the scientific save inside the guards, the atomic validated ledger, immutable outputs). If a process is killed hard, its CPU is unknown, and cap compliance cannot be claimed.

## 9. Budget and storage

**Remaining X5 scientific budget:** 21,582.984 CPU s.

**Projected cost at 1 thread** (benchmark), ≈ **13,429 CPU s** (62%; reserve about 38%):

| Term | CPU s |
|---|---|
| training | 11,484 |
| dev CE | 635 |
| scoring | 721 |
| generation and oracle (allocated) | 360 |
| bootstrap (allocated) | 120 |
| fresh test | 85 |
| exports and checkpoint I/O | about 60 |

**Hard caps:** cumulative 21,600 CPU s, 8 GB RAM, ≤ 2 GB storage.

**Storage:** 27 checkpoints per model (26 × 3.24 MB + 9.74 MB) ≈ 94 MB, so ≈ 0.57 GB for six. Data and curves add ≤ 0.1 GB, for a total ≤ 0.7 GB.

## 10. Open choices for review

1. Export `serialise_state` from `learner` (preferred), or duplicate it in experiment.
2. Whether one dev pool for both monitoring and the endpoint is acceptable (proposed: yes).
3. Censoring at τ_grid > 4,500, the observed window, versus any extended-grid convention (proposed: the observed window only).

## 11. Changes from draft-1

* **τ.** τ is now the grid-defined event (exactly t_j); draft-1's bracket was a latent-crossing interval, now descriptive only. A non-monotone hand example is added.
* **Censoring.** Censoring is defined on the observed window, as (4500, ∞). Draft-1 used candidate-specific lower bounds that relied on unobserved checkpoints.
* **Decision rule.** Contradiction and failure cases are explicit, and the p = 0.125 language is removed.
* **AUC.** It is defined from the dev curves; the fresh test is a single step-5,000 point.
* **Config fields.** checkpoint_steps and an explicit device "cpu"; the thread setting comes from the benchmark.
* **`PublicTokenDataset`.** It is now attributed to the correct module (`dataset`).
* **Masters.** Frozen, with the collision check done.
* **STOP interval and budget.** Both now come from measured throughput.
* **`serialise_state`.** Its export is identified as the smallest needed change.
