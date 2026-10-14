# X5 G1 — six-model training protocol DRAFT (x5g1-train-draft-1)

14 October 2026, handoff job 0007.

**NOT FROZEN. NOT AUTHORISED.**

* This is a freeze-ready draft for coordinator review. No sampling, training or evaluation has occurred under it.
* It builds on the [X5 G1 feasibility gate](X5_G1_FEASIBILITY_REPORT.md) (FEASIBLE, D-066) and its [verification](X5_G1_COORDINATOR_VERIFICATION_ADDENDUM.md) (CONSISTENT), the X5 outline, and the coordinator notes in jobs/0007/TRAINING_REVIEW_NOTES.md (adopted except where marked).
* **Blocking open issue B1 (§9.1) must be resolved before freeze.**

## 1. Hypothesis and scope (unchanged)

**H5 (G1).** For the defined process pair, the metric-coupled conductance kernel (a020) increases the steps needed to reach the oracle-relative regret threshold by **at least 250 steps** compared with the flat kernel (a0), under the same topology, stationary occupancy, emissions, architecture and optimizer.

**What a positive result would show.** Slower learning by this algorithm on this process pair. It would **not** show a curvature effect:

* the gate showed a large movement-speed confound, since a speed-matched flat kernel nearly reproduces a020's mixing summaries;
* curvature attribution would need a separately approved speed-matched arm, which is not part of this study.

**Excluded:** a third training arm, PH, G2, density, X6, an optimizer or architecture search, and evaluation-driven tuning.

## 2. Fixed inputs

**Process inputs.**

| Item | Value |
|---|---|
| World | `21feee1d8ee5422e` |
| a0 kernel | T `e4dafc7b9785c172` |
| a020 kernel | T `08a22a03727d2295` |
| E | `3633ac27dab50cf4` with its stored `symbol_perm`; the same numeric E and symbol names for all six models |
| π | uniform; the initial law equals π |
| Normalizers (fixed) | G_C(a0) = 0.27133797235249024 and G_C(a020) = 0.2939268960103646, the calibration point estimates (D-066), never re-estimated |

**Model.** The current `ModelConfig`, to be read from the stored E3 checkpoint metadata and asserted equal at run start, not assumed:

* vocab_in 37 and vocab_out 36;
* 33 positions;
* 4 layers, d_model 128, 4 heads, d_mlp 512;
* GELU, dropout 0, untied embeddings.

**Training.** The current `TrainConfig`:

* AdamW, lr 1e-3, warmup 200, cosine schedule, weight decay 0.1 with the existing matrix-only decay, clip 1.0;
* **5,000 updates, batch 128, CPU**;
* `checkpoint_steps` = the §4 grid. This is the only TrainConfig field changed from the defaults, and it changes no optimisation semantics.

**Exposure.** 5,000 × 128 × 33 = **21,120,000 target tokens per model**, drawn from 131,072 unique training histories per arm and master.

## 3. Data lineage (new; public only; latents discarded)

**Masters.** 310001, 310002 and 310003, the coordinator's candidates. Before freeze, check that they collide with no stored replicate scope.

**Generators.** Every pool is drawn with one `HMMSampler(T_arm, E[:, perm], π)` call, and named = perm[canon]. The two arms of a pair use **two separately initialised generators from the same seed** (common randomness).

| Pool | Stream | Size | Shared? | Namespace code |
|---|---|---|---|---|
| train (per master, per arm) | `SeedTree(master).generator("x5g1-train-v1", "train", "cylinder", "overlap", "1.25")` | 131,072 | per pair | 9 |
| dev (per master, per arm) | `SeedTree(master).generator("x5g1-train-v1", "dev", "cylinder", "overlap", "1.25")` | 4,096 | per pair | 10 |
| fresh test (per arm) | `SeedTree(0).generator("x5g1-train-v1", "test", "cylinder", "overlap", "1.25")` | 4,096 | shared across the three masters | 11 |

**Why these sharing choices.**

* Per-pair dev sets make each pair's endpoint uncertainty its own.
* A single shared fresh test, evaluated once at the end, is a secondary outcome for which all models face identical histories.
* Neither the dev nor the test pool ever selects anything.

**Sequence IDs.** `(process_code("cylinder", "overlap", "1.25", f"x5g1-train-v1:{split}:{arm}:{master}") << 32) | (code << 28) | index`. The test pool uses master "shared".

**Required checks** (failure → FAILED):

* disjointness from every stored ObservationSet, from the calibration (8), B2 (5) and X4-F (6) namespaces, and across arms, splits and masters.

**Persistence.**

* ObservationSets with `split` train / dev / test and config {role, protocol, arm, master, stream, namespace_code}, in an **independent X5 training store**.
* `DatasetStage` is **not** used: its world-scoped test stream would reproduce the old, unblinded test set, and its IDs would collide across arms. Its defaults stay unchanged.

**Learner input.** The learner sees only public `ObservationSet`s through `PublicTokenDataset`.

## 4. Evaluation grid and endpoint

**Grid (27 points).** [0, 100, 200, …, 1000, 1250, 1500, …, 5000]. There are no repeated confirmations at step 5,000.

**Regret at grid step t.** For each model and each dev history h:

reg_t(h) = KL(q_C(h) ‖ p_model,t(h)) at p32, in nats.

* q_C comes from `BayesFilter` with the arm's own T and the stored E. The oracle runs in experiment, never in the learner.
* p_model,t is computed from the stored checkpoint at step t.
* ratio_t = mean_h reg_t(h) / G_C(arm), using the fixed normalizer.
* **PASS_t** iff ratio_t ≤ 0.05 (threshold unchanged).

**Crossing τ.** The first grid index j such that PASS holds at j, j+1 and j+2. The observed τ then lies in **(t_{j−1}, t_j]**, and τ = 0 is the degenerate [0, 0].

**Censoring** (no confirmed crossing; never substitute 5,000):

* If the trailing suffix of the grid is entirely PASS, starting at index k with fewer than 3 points (an unconfirmed late candidate), then τ ∈ (t_{k−1}, ∞).
* Otherwise τ ∈ (5000, ∞).

**Hand examples.**

| Curve (PASS at …) | τ interval | Status |
|---|---|---|
| 1,000, 1,250, 1,500, … onward | (900, 1000] | observed |
| first PASS at 4,750, then PASS at 5,000 | (4500, ∞) | censored, unconfirmed |
| first PASS only at 5,000 | (4750, ∞) | censored |
| FAIL at 5,000, no earlier confirmed run | (5000, ∞) | censored |
| PASS at 2,000, FAIL at 2,250, PASS from 2,500 onward | (2250, 2500] | observed (the first confirmed run) |

**Paired difference bounds** (a020 minus a0), for a pair with intervals (Lc, Uc] and (Lf, Uf]:

* D_low = Lc − Uf;
* D_high = Uc − Lf.

Infinities are allowed and propagate (∞ − x = ∞; x − ∞ = −∞). Neither bound is ever NaN, because ∞ − ∞ cannot occur in D_low (Uf is finite or ∞, and Lc is finite) or in D_high (Lf is finite).

Example: curved observed in (900, 1000] and flat in (600, 700] give D_low = 200 and D_high = 400.

## 5. Uncertainty (paired dev-trajectory bootstrap)

* **Draws.** 2,000 per master, using a new stream `SeedTree(master).generator("x5g1-train-v1", "endpoint_bootstrap")`.
* **Joint resampling.** Each draw resamples dev indices i ∈ {0..4095} with replacement, **jointly for both arms**, because index i pairs the arms' dev histories under common randomness. Resampling covers whole per-history regret curves; checkpoints are never resampled independently.
* **Per draw.** Recompute both arms' ratio curves, PASS sequences, τ intervals, and D_low* and D_high*.
* **Quantiles.** `np.quantile(·, q, method="inverted_cdf")` at q = 0.025 and 0.975. This is an order statistic, so it is well-defined with ±∞ values and never interpolates them.
* **Censored replicates** are kept, never dropped, and their fraction is reported.
* **What the intervals are conditional on:** the fixed G_C normalizers, the six trained models and the chosen processes. They are not model-population or normalizer uncertainty.

## 6. Decision rule (all three pairs required)

**SUPPORTED** iff, in **every** pair:

* the point D_low ≥ 250 (equality satisfies ≥ 250);
* and the bootstrap 2.5% quantile of D_low* is > 0.

**REJECTED** iff, in **some** pair, the bootstrap 97.5% quantile of D_high* is < 250.

**INCONCLUSIVE** otherwise. This includes censoring that leaves the bounds unresolved, a crashed or failed model, a failed check, or a budget stop.

* No pair is dropped or replaced.
* Three pairs give sign-level evidence at best (p = 0.125); there is no population claim.

**Relation to the original outline.**

* *Same as the outline:* the 250-step practical threshold and the "positive under paired resampling" requirement.
* *Made explicit here:* the interval form (D_low), the censoring rule (where the outline said "never substitute 5,000"), and equality.
* *Rejection rule:* "upper bound < 250" now uses a valid bootstrap upper bound on the conservative D_high.

## 7. Execution controls

* **Order.** Masters run in the order 310001, 310002, 310003, and a0 before a020 within a pair. No retries; a failed model is recorded and kept.
* **Training composition.** The existing public `Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, save)` is used through an **experiment-side `save` callback**. The callback stores checkpoints with the LearnerStage identity rule and polls STOP and budget at each grid step, which bounds the poll interval to ≤ 250 updates.
  - **No learner API change.** Identical pairing keys (run_key = ("x5g1", "cylinder", master) for both arms) give identical initial weights and batch order. Checkpoint IDs still differ because the parents (obs_train, obs_dev) differ, as verified in `LearnerStage` (config {run_key, step, model_config, train_config} plus parents).
  - The arm is recorded explicitly in an experiment manifest and in every report.
* **Stopping mid-model.** If STOP or the budget triggers mid-model, that model is incomplete. Its partial checkpoints are kept, the ledger records the cause, and the cohort is INCONCLUSIVE.
* **Dense evaluation.** Regret curves are computed after each model finishes, from stored checkpoints, in batches with guards.
* **Fresh test.** Untouched until the frozen final evaluation at step 5,000 for all six models. It is a secondary outcome only: final regret in nats, normalized regret, and AUC of regret/G_C. There is no early stopping, seed replacement, tuning or endpoint selection.
* **Ledger and repairs.** Every cost is charged to the X5 ledger. The job-0007 repairs apply: full-hash before/after source checks, guarded exports, the atomic ledger and immutable outputs. A hard kill's CPU stays unknown.

## 8. Storage and outputs

* **Checkpoints.** 27 per model: 26 × 3.24 MB + 1 × 9.74 MB (final, with optimizer) ≈ 94 MB per model, **≈ 0.57 GB for six**. Sizes measured from stored E3 checkpoints.
* **Data.** Train ObservationSets 6 × 131,072 × 33 B ≈ 26 MB; dev and test about 1 MB.
* **Regret curves.** Per-history curves, 6 × 27 × 4,096 float64 ≈ 5.3 MB.
* **Total.** ≤ 0.7 GB, within 2 GB. No logits or activations are stored.

## 9. Open issues to resolve before freeze

1. **B1 — CPU budget feasibility (BLOCKING).**
   - The remaining X5 budget is 21,600 − 17.016 = **21,582.98 CPU s** (≈ 5.995 h).
   - E2/E3 training took about 16 **wall** minutes per model on 6 threads (D-030: 22k tokens/s).
   - If the cap counts process CPU time (as the ledger does), six models could cost far more: very roughly 6 × 16 × (threads used), up to about 9.6 CPU h, before evaluation.
   - **Proposal:** before freeze, a separately authorised *technical* throughput probe (not scientific; on synthetic tokens; about 20 updates; single-threaded and 6-threaded torch) measures process CPU per update.
   - Freeze only if the projected training, evaluation and bootstrap cost fits the remaining budget with a ≥ 20% reserve. Otherwise the coordinator must change the budget or the scope; there is no partial cohort.
2. **Thread setting.** Recommended: `torch.set_num_threads(1)` and single-threaded BLAS, so that ledger CPU ≈ wall time and runs are deterministic. To be confirmed after B1.
3. **Master seeds.** 310001–310003 are subject to the collision check.
4. **Single dev pool for both CE and endpoint.** The same dev pool would serve both the trainer's dev CE and the endpoint. This is acceptable, because dev CE selects nothing, but the alternative of separate pools could be preferred.
5. **Normalizer scope.** Normalizer uncertainty is excluded (conditional intervals). Confirm that this is acceptable.
