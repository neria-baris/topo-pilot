# X5 G1 — training implementation plan v2 (for x5g1-train-draft-2)

14 October 2026, handoff job 0008.

**Plan only; NOT authorised.** Nothing here is implemented, sampled or trained.

* This supersedes [plan 1](X5_G1_TRAINING_IMPLEMENTATION_PLAN.md), which is kept byte-identical.
* It follows the [draft v2](X5_G1_TRAINING_PROTOCOL_V2.md).

## 1. Composition: existing APIs plus one learner export

| Need | Reuse | New (experiment only, unless stated) |
|---|---|---|
| Pools | `dataset.HMMSampler`; the named-token remap, generator pairing and namespaces from `x5g1_lineage` | `x5g1t_lineage.py`: streams, codes 9/10/11, masters 310001–3, ObservationSet split and role config (draft §3) |
| Learner input | `topo_pilot.dataset.PublicTokenDataset` | none |
| Training | `learner.Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, on_checkpoint)` | `x5g1t_train.py`: a callback storing grid checkpoints with the `LearnerStage` identity; STOP, budget and usage-hold polling at each grid step |
| Serialisation | `learner.stage.serialise_state` | **learner (review needed):** export `serialise_state` from `topo_pilot.learner.__init__`. Public surface only; no behaviour change. |
| Config | `ModelConfig` as stored; `TrainConfig` as stored, except checkpoint_steps = the 27-point grid and device = "cpu" | `torch.set_num_threads(1)` in the experiment process, recorded in the run manifest |
| Regret curves | `learner.load_model`, the forward at index 32, `oracle.BayesFilter` per arm, `analysis.kl_rows` | `x5g1t_endpoint.py`: per-history regret curves [4096 × 27] per model, then ratio and PASS |
| Endpoint statistics | — | pure analysis in `analysis/x5_endpoint.py`: `grid_event(pass_seq, grid)` returns (τ, bounds, censored); also `difference_bounds`, `paired_bootstrap_endpoint` and `cohort_verdict` (draft §4–§6) |
| Controls | `x5g1_controls` and `x5g1_safety`, with the job-0007/0008 repairs (guarded scientific saves, validated atomic ledger) | none |

**Learner boundary.**

* The learner never receives targets, beliefs, world data or latents.
* The callback carries compute and STOP controls only.
* The one learner change is the `serialise_state` export. The preferred option avoids a duplicated serialiser that could drift in checkpoint identity. It needs coordinator or owner review before any implementation.

## 2. Independent tests (a separate test-writer agent, working from the frozen draft)

**`x5_endpoint`:**

* every hand example in draft §4, including the non-monotone ones (PASS 2000 / FAIL 2250 / PASS from 2500 gives 2500; PASS 1000–1500 then FAIL gives 1000);
* censoring at the window edge: first PASS at 4,500 counts as observed, first PASS at 4,750 is censored;
* τ = 0 handled as degenerate;
* D_low and D_high with ±∞ and never NaN;
* `inverted_cdf` quantiles with ±∞;
* the cohort truth table: equality at 250; a censored a020 with a strict bound; contradictory evidence → INCONCLUSIVE; a failed model → INCONCLUSIVE; no replacement;
* bootstrap indices shared across the two arms of a pair, applied to whole curves.

**Lineage:**

* the frozen masters, streams and codes;
* identical first symbols across the arms of a pair;
* disjointness across splits, arms and masters, and against the stored and B2 IDs. This is a regression of the job-0008 check: 819,200 IDs, 0 collisions.

**`serialise_state` export:**

* the bytes produced through the public import are identical to those `LearnerStage` stores for the same model and config;
* the default `LearnerStage` behaviour is unchanged.

**Training composition** (tiny model fixture):

* the same run_key gives identical step-0 weights across arms, while checkpoint IDs differ through their parents;
* the callback raises on STOP and on budget, and partial checkpoints are kept;
* no model starts while another is recorded as RUNNING.

## 3. Execution sequence (a later, separately authorised task)

1. Review draft v2. Then freeze it (sha256 in DECISIONS), implement, run the independent tests, and commit on a clean tree.
2. Run the integrity check with full hashes, before and after.
3. Draw the pools for all masters and arms; check disjointness against the stored IDs.
4. Train six models sequentially in the fixed order at 1 thread, keeping all 27 checkpoints per model. A run of about 0.54 h per model gives about 3.3 h wall in total.
5. Compute the dense dev regret curves, then τ_grid, the bounds and the paired bootstrap.
6. Evaluate the fresh test once, on the six step-5,000 models only (secondary outcome).
7. Write guarded exports with an immutable output directory, then the report, then STOP.

## 4. Budget

* **Projected cost** (benchmark, 1 thread): 13,428.8 CPU s of the 21,582.984 remaining, against a frozen 80% limit of 17,266.4.
* **Recording.** All costs go to the X5 scientific ledger, with cumulative hard guards.
* **Unknown CPU.** CPU from a hard-killed process is unknown and blocks any claim of cap compliance.
* **Storage:** ≈ 0.7 GB, within the ≤ 2 GB cap.
