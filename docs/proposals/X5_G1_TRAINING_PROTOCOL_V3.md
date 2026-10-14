# X5 G1 six-model training — protocol v3 (x5g1-train-v3)

14 October 2026, handoff job 0009.

**IMPLEMENTATION CONTRACT PENDING FINAL EXECUTION FREEZE.**

* No scientific sampling, training or evaluation is authorised by this document.
* The root must review the implementation, then freeze this contract (sha256 recorded in DECISIONS) in a separate job before any study run.

**Lineage.** [draft-1](X5_G1_TRAINING_PROTOCOL_DRAFT.md) and [draft-2](X5_G1_TRAINING_PROTOCOL_V2.md) are preserved byte-identically. The accepted scientific scope is the job-0008 review. v3 changes only:

* the censoring wording (§4);
* the both-censored difference (§4);
* the runtime, budget and resource controls (§8–§9);
* the corrected scoring projection (§9).

## 1. Hypothesis, estimand and scope (unchanged from v2)

* **H5 (G1).** For the defined process pair, the conductance kernel a020 delays the **grid-defined** regret-threshold event by ≥ 250 steps compared with the flat kernel a0, in each of three paired models.
* **Estimand.** Per pair p, Δ_p = τ_grid(a020, p) − τ_grid(a0, p).
* **What a positive result means.** Slower learning by this algorithm on this process pair. It is **not** a curvature effect: the gate showed a large movement-speed confound.
* **Excluded:** a third arm, PH, G2, density, X6, optimizer or architecture search, and evaluation-driven tuning.

## 2. Fixed inputs and configuration (unchanged; asserted from metadata at every stage start)

**Process.**

| Item | Value |
|---|---|
| World | `21feee1d8ee5422e` |
| T a0 | `e4dafc7b9785c172`, payload sha f94340a64769df1c89935c1767a58d2f764b0f31a49e675bd43d8484eeba68dd |
| T a020 | `08a22a03727d2295` (X5 research store), sha 663d0011c7f9b541a436359c885a9f367dda280b20b594e484ff1492b8686b7b, parent world |
| E | `3633ac27dab50cf4`, sha f5b6197c22e3613f12a29feb9dec2ccd357749928032f4dc844364d6884bb1fb, with stored `symbol_perm` |
| π | uniform |
| Fixed normalizers (D-066) | G_C(a0) = 0.27133797235249024 and G_C(a020) = 0.2939268960103646. Uncertainty is conditional on them. |

**Model.** `ModelConfig` exactly equal to the metadata of `c3358e3cb9c352fb`, asserted at run start; job 0009 verified it read-only:

* vocab_in 37 and vocab_out 36; n_ctx 33;
* 4 layers, d_model 128, 4 heads, d_mlp 512;
* GELU, dropout 0, untied embeddings.

**Training.**

* `TrainConfig` uses the stored values: steps **5000**, batch 128, lr 1e-3, warmup 200, cosine, weight decay 0.1, clip 1.0.
* Only two fields change: `checkpoint_steps` = the §4 grid, and `device = "cpu"`.
* Process setting: `torch.set_num_threads(1)`.

**Learner input and pairing.**

* The learner sees only `topo_pilot.dataset.PublicTokenDataset`. No oracle quantity, target, belief or latent ever reaches it.
* **Seeds:** `SeedTree(m)` with run_key `("x5g1", "cylinder", m)` for both arms. This gives identical initial weights and batch order; checkpoint IDs differ through their ObservationSet parents.

## 3. Lineage (unchanged)

**Masters:** 310001, 310002, 310003, frozen.

**Generators.** For each pool, two separately initialised generators from the same seed, one per arm. Each arm makes one `HMMSampler(T_arm, E[:, perm], π)` call, and the tokens are named = perm[canon]. Latents are discarded.

| Pool | Stream | Size | Code |
|---|---|---|---|
| train (m, arm) | `SeedTree(m).generator("x5g1-train-v1", "train", "cylinder", "overlap", "1.25")` | 131,072 | 9 |
| dev (m, arm) | `SeedTree(m).generator("x5g1-train-v1", "dev", "cylinder", "overlap", "1.25")` | 4,096 | 10 |
| fresh test (arm) | `SeedTree(0).generator("x5g1-train-v1", "test", "cylinder", "overlap", "1.25")` | 4,096 | 11 |

**IDs.** `(process_code("cylinder", "overlap", "1.25", f"x5g1-train-v1:{split}:{arm}:{m}") << 32) | (code << 28) | index`, with m = "shared" for test. All 819,200 planned IDs are unique, with 0 collisions against the 3,440,640 stored IDs (job 0008).

**ObservationSets.**

* splits train / dev / test, with config {role, protocol, arm, master, stream, namespace_code};
* parents [T_arm, E].

**Fresh test.** It is generated **only** in the separately authorised final stage. One dev pool serves both trainer monitoring and the endpoint; neither selects anything.

## 4. Grid-defined endpoint

**Grid G**, 27 points: t_0 = 0, 100, …, 1000, 1250, …, t_26 = 5000.

**PASS.** reg_t(h) = KL(q_C(h) ‖ p_model,t(h)) at p32, in nats.

* **Oracle row.** q_C comes from `BayesFilter(T_arm, E_stored, π)` run on the **public history w1..w32 only**. The target w33 is excluded. Tokens are named, so the stored (named) E is the right emission matrix.
* **Model row.** p_model comes from the stored checkpoint: batched (512) float64 `log_softmax` at index 32.
* **Test.** ratio_t = mean_h reg_t(h) / G_C(arm); **PASS_t** iff ratio_t ≤ 0.05.

**Event.** τ_grid = t_j for the smallest j ≤ 24 with PASS at j, j+1 and j+2.

* An observed τ_grid is **exactly** t_j; its bounds are [t_j, t_j]. τ_grid = 0 is allowed.
* Any prior-grid band is descriptive only.

**Right-censoring (conservative bound).** If no j ≤ 24 qualifies, τ_grid is censored, with lower bound **4500 (strict)** and upper bound +∞.

* This bound means only that **no qualifying event was observable within the finite 27-point window**. A qualifying event needs t_{j+2} ≤ 5000.
* It does **not** assert that a finite event or crossing would occur later, nor estimate one. No extended experiment is implied.
* A trailing PASS at 4,750 or 5,000 is reported as unconfirmed. Nothing is imputed.

**Hand examples.**

| PASS pattern | τ_grid |
|---|---|
| PASS 2000, FAIL 2250, PASS from 2500 | 2500 |
| PASS 1000/1250/1500, FAIL 1750 | 1000 |
| PASS at 0, 100, 200 | 0 |
| PASS from 4500 (4500, 4750, 5000) | 4500, observed |
| first PASS 4750 | censored |

**Difference bounds per pair.** With a020 bounds [Lc, Uc] and a0 bounds [Lf, Uf]:

* D_low = Lc − Uf and D_high = Uc − Lf.
* Every L is finite (t_j or 4500), so ∞ − ∞ never occurs and nothing is NaN.

| Case | Bounds |
|---|---|
| both observed | D_low = D_high = Δ |
| a020 censored, a0 observed | D_low = 4500 − t_f (strict: Δ > D_low), D_high = +∞ |
| a0 censored, a020 observed | D_low = −∞, D_high = t_c − 4500 (strict) |
| **both censored** | **[−∞, +∞]**: no information on Δ |

## 5. Uncertainty (unchanged)

* **Draws.** 2,000 per master, stream `SeedTree(m).generator("x5g1-train-v1", "endpoint_bootstrap")`, in 4 batches of 500 with guards.
* **Resampling.** Dev indices are resampled with replacement and **shared** by both arms. They are applied to **whole** per-history regret curves.
* **Per draw.** Recompute both ratio curves, PASS sequences, τ_grid with bounds, and D_low* and D_high*.
* **Quantiles.** Order statistics with `inverted_cdf` (the ⌈qn⌉-th smallest value) at q = 0.025 and 0.975; ±∞ are allowed.
* **Censoring.** Censored draws are kept and their fraction reported.
* **Scope.** Conditional on the fixed normalizers, models and processes.

## 6. Decision rule (unchanged; all three pairs required, no replacement)

| Verdict | Condition |
|---|---|
| **SUPPORTED** | every pair has point D_low ≥ 250 (equality counts) **and** a 2.5% quantile of D_low* > 0 |
| **REJECTED** | some pair has a 97.5% quantile of D_high* < 250 |
| **INCONCLUSIVE** | otherwise, including both conditions holding (contradiction), any model failed, incomplete or lost, any failed integrity check, and any STOP or budget stop |

No pair, seed or model is replaced, and no significance level is attached.

## 7. Secondary outcomes (descriptive, unchanged)

* **Dev curves:** the dev-curve AUC of ratio_t (trapezoid rule on the actual steps), the per-checkpoint ratios, and the censored-replicate fractions.
* **Fresh test:** only in the final stage, step 5,000 only: regret in nats and regret/G_C.

## 8. Runtime controls (revised)

**Order and locking.**

* Order: masters 310001 → 310002 → 310003, a0 then a020 within each. One model and one process at a time.
* A **run lock** file is created exclusively before a model starts. If a lock, or a recorded outcome for the same (arm, master), exists, a second start is refused, whether the earlier run is live or of unknown state.
* No retry, restart, replacement or reseeding.

**Usage hold of a live process.** The existing `Trainer.fit` has no mid-run restore API, and intermediate checkpoints hold weights only. A hold therefore **pauses the live process inside the experiment checkpoint callback**. The optimizer, scheduler and batch RNG stay in that process's memory.

* **While held,** the process:
  - writes an **audit-only** hold record with PID, run identity, the completed checkpoint IDs and payload hashes, the current CPU snapshot and the time;
  - polls the runtime controls in waits of **≤ 45 s**.
* **It resumes the same callback only when:**
  - the coordinator hold is released (worker_control no longer `WAIT_USAGE_RESET`), **and**
  - the worker's own usage hold has cleared on actual blocking usage evidence (runtime_state no longer `WAIT_USAGE_RESET`).
* **Elapsed time or a scheduled reset alone never resumes.** Usage observability `UNAVAILABLE` is not itself a hold.
* **If the held process dies,** its outputs are retained, the model is marked INCOMPLETE and the cohort becomes INCONCLUSIVE. It is not restarted from weights, and no seed is replaced or resampled.
* **Wording.** An intermediate weights-only artifact is never called a "resume checkpoint".
* **No learner change.** No learner-loop or API change is needed.

**STOP and control precedence.** The owner `STOP` file, `worker_control.command == "STOP"` and `request.json command == "STOP"` each stop the run. They are checked:

* at every grid checkpoint (≤ 250 updates plus dev CE ≈ **2 min** at 1 thread; documented latency);
* while held;
* before and after every scientific write and every evaluation, bootstrap and export batch.

STOP always wins over hold and continue. A malformed or unreadable critical control file **fails closed**, i.e. it is treated as STOP.

## 9. Budget and resources (revised)

**Projection** (corrected, job 0009, 1 thread): **13,400.25 CPU s** of the remaining 21,582.984; limit 17,266.39.

**Scientific ledger.** A single cumulative X5 ledger (prior 17.016 s), validated and atomic, with a hard cumulative cap of **21,600 CPU s**.

**Boundary accounting.** At every checkpoint boundary and before every model or stage, the run proceeds only if:

```text
cumulative_now + 1.5 × estimate(next unit of work) + evaluation_reserve ≤ 21,600
```

**Estimates.**

| Quantity | Value |
|---|---|
| per update | 0.383 s |
| dev CE | 3.92 s |
| scoring + load per checkpoint | 3.91 s |
| evaluation_reserve = 1.5 × (remaining scoring + fresh test + bootstrap 120 s + exports 60 s) | ≈ 1.43 ks while nothing is scored |

Otherwise the run stops **before** starting that work, with status `budget`.

**Overshoot disclosure.** Checks are periodic, not an instruction-level CPU kill. A unit that runs over its estimate can overshoot by at most that unit: one checkpoint interval of about 100 CPU s, or one evaluation batch of about 1 s.

**Resources.** The process peak working set and the new-output storage are checked at the same boundaries. The run fails at **8 GB RAM** or **2 GB storage**. Expected peaks are about 0.5 GB RAM and 0.7 GB storage.

**Unknown CPU.** If a process is killed hard, its CPU is unknown, so no cap-compliance claim can be made.

## 10. Stage separation

| Stage | What it does |
|---|---|
| `pools` | generate train and dev pools for all masters and arms, plus collision checks |
| `train` | one (arm, master) per invocation |
| `dev-analysis` | curves, τ, bounds, bootstrap and verdict |
| `final-test` | generate the fresh test pool and score the six step-5,000 models; only with explicit later authorisation, after dev-analysis is final |

**Common to every stage:**

* immutable output directories;
* full-hash read-through parents verified before and after;
* guarded scientific saves and exports.
