# X5 G1 — training implementation plan (for x5g1-train-draft-1)

14 October 2026, handoff job 0007. **Plan only; NOT authorised.** Nothing here is implemented, sampled or trained.

## 1. Minimal composition: existing APIs reused, no learner or contract change

| Need | Reuse | New (experiment only) |
|---|---|---|
| Pools | `dataset.HMMSampler`; the named-token remap, generator pairing, namespaces and disjointness from `x5g1_lineage` | `x5g1t_lineage.py`: train/dev/test streams per the draft §3, namespace codes 9/10/11, ObservationSet split and role config |
| Training | `learner.Trainer(model_cfg, train_cfg, seeds, run_key).fit(train, dev, save)` and `learner.PublicTokenDataset` | `x5g1t_train.py`: a save callback mirroring the `LearnerStage` checkpoint identity ({run_key, step, model_config, train_config}, parents [obs_train, obs_dev]), with STOP and budget polling at each grid step |
| Model and config | `ModelConfig` and `TrainConfig` (only `checkpoint_steps` = the 27-point grid); asserted equal to the stored E3 metadata | none |
| Regret curves | `learner.load_model`, model forward at index 32, `oracle.BayesFilter` per arm, `analysis.kl_rows` | `x5g1t_endpoint.py`: per-history regret curves → ratio, PASS, τ intervals |
| Endpoint statistics | — | pure analysis `x5_endpoint.py`: `crossing_interval(pass_seq, grid)`, `difference_bounds`, `paired_bootstrap_endpoint`, `cohort_verdict` (§6 of the draft) |
| Controls | `x5g1_controls` and `x5g1_safety` (repaired in job 0007) | none |

**Learner boundary.** The learner never receives targets, beliefs, world data or latents. The save callback carries compute and STOP controls only. If B1 (draft §9) recommends single-threading, it is set in the experiment process (`torch.set_num_threads`), not inside the learner.

## 2. Independent tests (separate test-writer agent, from the frozen draft)

* **`x5_endpoint`:**
  - every hand example in the draft §4 (observed, late unconfirmed, only at 5,000, FAIL at 5,000, a broken run);
  - τ = 0 handled as degenerate;
  - D_low and D_high with infinities and no NaN;
  - `inverted_cdf` quantiles with ±∞;
  - the cohort rule truth table, including equality at 250, a censored pair, and a failed model giving INCONCLUSIVE;
  - the bootstrap resampling indices shared across arms (pairing).
* **Lineage:**
  - frozen seeds and namespace codes;
  - identical first symbols across the arms of a pair;
  - disjointness across splits, arms and masters, and against stored IDs;
  - the test stream differs from the original test and calibration streams.
* **Training composition** (tiny model fixture):
  - identical run_key gives identical step-0 weights across arms, while checkpoint IDs differ by their parents;
  - the save callback raises on STOP and on budget, and partial checkpoints are kept;
  - default `LearnerStage` behaviour is unchanged.

## 3. Execution sequence (a later, separately authorised task)

1. Resolve B1 with the technical throughput probe, which is not scientific. Then freeze the protocol (DECISIONS, sha256) and commit the code and tests.
2. Run the integrity check (full hashes, before and after).
3. Draw the pools for all masters and arms, then run the disjointness checks.
4. Train six models in the fixed order, keeping all 27 checkpoints per model.
5. Compute dense regret curves, then the τ intervals and the paired bootstrap.
6. Evaluate the fresh test once on all six final models (secondary outcome).
7. Write the report and STOP.

## 4. Budget

The remaining X5 budget is 21,582.98 CPU s. The required costs are recorded in the ledger:

* training, which dominates; see B1;
* dense evaluation: 27 × 4,096 histories × 6 models, plus the oracle;
* bootstraps: 2,000 × 3 pairs × 2 × 27-point curve means. This is cheap, because per-history regret is precomputed.

The plan is not executable until B1 shows that it fits with a reserve.
