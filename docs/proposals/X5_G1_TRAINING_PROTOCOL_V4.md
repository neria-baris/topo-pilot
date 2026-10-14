# X5 G1 six-model training — protocol v4 (x5g1-train-v4)

14 October 2026, handoff job 0010.

**IMPLEMENTATION CONTRACT PENDING FINAL EXECUTION FREEZE.**

* No scientific sampling, training or evaluation is authorised by this document.
* The root must review the implementation and the concrete pending `StudyConfig`, then freeze this contract (sha256 in DECISIONS) in a separate job.

**Relation to v3.** [v3](X5_G1_TRAINING_PROTOCOL_V3.md) and earlier drafts are preserved byte-identically.

* §1–§7 below are **unchanged in substance** from v3: scope, sources, lineage, endpoint, uncertainty, decision rule and secondary outcomes. The only addition is the world artifact's full hash.
* v4 changes only the runtime, budget and resource wording (§8–§9), the production configuration and environment (§10), the stage integration (§11) and the protocol identifier.
* No estimate, budget, reserve, threshold or scientific criterion changes.

## 1. Hypothesis, estimand and scope (unchanged from v2)

* **H5 (G1).** For the defined process pair, the conductance kernel a020 delays the **grid-defined** regret-threshold event by ≥ 250 steps compared with the flat kernel a0, in each of three paired models.
* **Estimand.** Per pair p, Δ_p = τ_grid(a020, p) − τ_grid(a0, p).
* **What a positive result means.** Slower learning by this algorithm on this process pair. It is **not** a curvature effect: the gate showed a large movement-speed confound.
* **Excluded:** a third arm, PH, G2, density, X6, optimizer or architecture search, and evaluation-driven tuning.

## 2. Fixed inputs and configuration (unchanged; asserted from metadata at every stage start)

**Process.**

| Item | Value |
|---|---|
| World | `21feee1d8ee5422e`, WorldSpec sha b6f0746e46d20d202c1a74220f96357a0a80375d57046ffea69b03f3f354f77f (verified read-only) |
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

**Order and locking (unchanged from v3).**

* Order: masters 310001 → 310002 → 310003, a0 then a020 within each. One model and one process at a time.
* An exclusive run lock is taken before each model. An existing lock or recorded outcome refuses a second start.
* No retry, restart, replacement or reseeding.
* **Pre-start convention (accepted in review 0009).** A STOP or budget stop after the lock is taken, even before the first update, records an INCOMPLETE outcome and consumes that model's single attempt.

**Live-process usage hold (unchanged policy).**

* A hold pauses the live process inside the experiment callback; the optimizer, scheduler and batch RNG stay in memory.
* The hold record is audit-only (`AUDIT_ONLY_NOT_A_RESUME_CHECKPOINT`).
* There is no mid-process restore.
* If the process dies, the model is INCOMPLETE and the cohort INCONCLUSIVE.

**Control sources and precedence: STOP > HOLD > CONTINUE.**

| Source | STOP | HOLD | Continue / missing |
|---|---|---|---|
| owner `STOP` file | present | — | — |
| `request.json` | command `STOP`; missing, malformed or unknown | — | `RUN_NEXT` |
| `worker_control.json` | `STOP`; malformed or unknown | `WAIT_USAGE_RESET` (until the coordinator releases it) | `CONTINUE`; missing |
| `runtime_state.json` `mode` (allow-list) | malformed, non-string or unknown | `WAIT_USAGE_RESET`, `RUNTIME_BLOCKED`, `NEEDS_USAGE_INFO` | `WORKING`, `WAITING`, `USAGE_READY`; missing file |
| worker usage evidence `claude_usage.json` | malformed or unknown values | an OBSERVED relevant limit with `used_percent ≥ threshold` (85), or a non-null warning; this holds even under a stale `CONTINUE` | `UNAVAILABLE` (alone never a hold); missing file |
| self-hold latch `usage_hold_latch.json` | malformed | present | absent |

**Self-hold latch.**

* An observed blocking condition **sets** a persistent latch that records the blocking limits.
* The latch **clears** only on NEW evidence: `claude_usage.json` must have `observability = OBSERVED`, a non-`unavailable` source, and an `observed_at_utc` strictly after the latch time. Every previously blocking limit kind must be present, relevant, numeric, below the threshold and without a warning, and no relevant limit may be blocking.
* None of these clears it: editing the runtime mode, elapsed or reset times, `UNAVAILABLE`, or missing limit evidence.
* On clearing, the latch is archived with the evidence.
* A coordinator `WAIT_USAGE_RESET` still holds until the coordinator releases it.
* No quota or reset time is ever invented.

**Check points.** Controls are checked:

* at every grid checkpoint, at an **expected** latency of about 2 min at the measured 1-thread rate (≤ 250 updates plus dev CE);
* while held;
* before and after every scientific save and bulk export step (JSON or npz);
* before and after every 512-row scoring batch and every oracle batch;
* before every fresh pool or test draw, and after it.

## 9. Budget and resources (revised wording; same numbers)

**Projection** (job 0009, 1 thread): **13,400.25 CPU s** of the remaining 21,582.984; limit 17,266.39.

**Ledger.** A single cumulative X5 ledger (prior 17.016 s), with a hard cumulative cap of 21,600 CPU s.

**Boundary rule (unchanged).** Work proceeds only if:

```text
cumulative_now + 1.5 × estimate(next unit) + evaluation_reserve ≤ 21,600
```

The estimates (per update 0.383 s, dev CE 3.92 s, score 3.906 s) and the reserve are unchanged.

**Not a hard kill.**

* These checks are **periodic safety checks, not an exact instruction-level CPU kill**.
* An atomic unit (a checkpoint interval, a 512-row scoring batch, an oracle batch, a sampler call or a save) can take longer than its estimate, and then the cap can be exceeded by however long that unit actually runs.
* **No guaranteed overshoot bound is claimed.** The about-2-minute checkpoint latency is an expectation from measured throughput, not a guarantee.

**Resources.**

* Peak working set and new-output storage are **checked at runtime** at every boundary, and the run fails at 8 GB RAM or 2 GB storage. An unknown peak fails closed.
* **Measured:** batched scoring peak of 456 MB (job 0009).
* **Not measured:** full training RAM; it is checked at runtime, and no bound is claimed.
* Expected storage is about 0.7 GB, based on measured checkpoint sizes.

**Unknown CPU.** CPU of a hard-killed process is unknown, so no cap-compliance claim can be made for it.

## 10. Production configuration and environment

**Validation.** The concrete production `StudyConfig` (mode `production`) is validated **before any sampler, model or output computation**:

* **Protocol.** `x5g1-train-v4`, with this document's sha256.
* **Sources.** World, T a0, T a020 and E IDs with **full** payload sha256 and artifact types, verified read-only. Source producer versions are recorded and must match.
* **Stored model.** The metadata (not the weights) of checkpoint `c3358e3cb9c352fb` (payload bcd024efc2ff30f76940d459dba95a693f536fb7cc3b2441c4ee5145dcf8596b). `ModelConfig` must equal it. `TrainConfig` must equal it except `checkpoint_steps` = the grid and `device = "cpu"`.
* **Design constants.**

  | Item | Value |
  |---|---|
  | masters | 310001–310003 |
  | arms | a0 and a020 |
  | sizes | 131,072 / 4,096 / 4,096 |
  | grid | 27 points |
  | steps | 5,000 |
  | fixed G_C values | as in §2 |
  | bootstrap draws | 2,000 |
  | threads | 1 |
  | CPU caps | 21,600 |
  | namespace and stream construction | exactly as in §3 |

* **Process environment** (set before Python starts): `OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = OMP_NUM_THREADS = 1` and torch intra-op threads 1. Interop threads are recorded unchanged. This matches the feasibility execution and bounds numpy and oracle CPU overhead. The values are recorded in the config and every run manifest. It is not an optimizer, architecture or budget change. The earlier technical benchmark (environment unset) is not rerun.
* **Roots.**

  | Role | Path |
  |---|---|
  | read (read-only) | `topo-pilot/artifacts`, `x5g1-research-store/store`, `x4b2-research-store/store` |
  | new study root (the only write root) | `x5g1t-research-store` |
  | ledger | `x5g1-research-store/cpu_ledger.json` |

  The write root must not equal or lie inside a read root, the main repository or the research worktree.
* **Fail closed.** An unknown key, a missing value or a malformed config is refused.
* **Synthetic fixture mode.** It is explicit and distinct (`mode = synthetic-fixture`), uses a SYNTHETIC protocol label, and may not use production roots, the production ledger or production source IDs.

## 11. Stage integration

| Stage | What it does |
|---|---|
| `validate` | read-only; no writes |
| `pools` | train and dev pools |
| `train` | one model per invocation |
| `dev-analysis` | curves, events, bootstrap and verdict |
| `final-test` | the fresh test; explicit authorisation, after a complete dev-analysis export |

**Every stage:**

* validates the config first;
* verifies the full hashes of world, T, E and every **used** pool and checkpoint before and after use;
* verifies the checkpoint identity:
  - the ordered full grid of steps;
  - run_key and the model and train configs;
  - parents = [train, dev] pool IDs;
  - `observation_id`;
* refuses to advance unless prerequisite exports are **complete**: an `EXPORT_STATUS.json` with status COMPLETE and every `MANIFEST.json` hash matching, with no extra or missing file;
* makes a failed integrity check prevent the scientific result export.

**Fresh-test IDs.** They are collision-checked against the stored main, B2 and calibration IDs and the new train and dev pools **before** the fresh draw.

**After a STOP during export.** Only a small status record and the ledger entry are written; no scientific file.
