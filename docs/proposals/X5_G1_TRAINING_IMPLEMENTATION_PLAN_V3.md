# X5 G1 training — implementation plan v3 (for x5g1-train-v3)

14 October 2026, handoff job 0009.

**IMPLEMENTATION CONTRACT PENDING FINAL EXECUTION FREEZE.**

* This job implements and tests the plan with **synthetic fixtures only**. It runs no study sampling, training or evaluation.
* Plans 1 and 2 are preserved. The API detail, which is the contract for the independent tests, is in [X5_G1_TRAINING_API.md](X5_G1_TRAINING_API.md).

## 1. Modules (experiment unless stated; ≤ 400 lines each)

| Module | Role |
|---|---|
| `learner/__init__` | public export of `serialise_state` (authorised by review 0008; no behaviour change) |
| `analysis/x5_endpoint.py` | pure endpoint maths: grid event, bounds, infinity-safe quantiles, paired whole-curve bootstrap, pair and cohort verdict, dev AUC |
| `x5g1t_lineage.py` | masters, streams, codes, sequence IDs, paired pool draws (reusing `x5g1_lineage.sample_named`), ObservationSet configs, disjointness |
| `x5g1t_oracle.py` | `oracle_q32`: BayesFilter q at p32 from w1..w32 only |
| `x5g1t_score.py` | batched-512 float64 p32 log-probs and stable KL (already used by the scoring correction) |
| `x5g1t_runtime.py` | control reading with STOP precedence and fail-closed parsing; live hold with ≤ 45 s polls; audit-only hold record; run lock and outcome records; boundary budget planner; resource checks |
| `x5g1t_train.py` | study `TrainConfig`; checkpoint callback mirroring the `LearnerStage` identity with guarded saves; one-model driver recording COMPLETE or INCOMPLETE |
| `x5g1t_stages.py` | stage functions `pools`, `train`, `dev_analysis` and `final_test` over a study config (sources with full hashes, sizes, grid, normalizers, roots) |
| `x5g1t_main.py` | CLI with sub-commands per stage; `final-test` requires `--authorized-final` |

## 2. Independent tests (separate test-writer agents, from the API contract only)

Three test authors each work from the API contract only:

* **(A) endpoint statistics;**
* **(B) lineage, oracle and training composition;**
* **(C) runtime safety.**

All use tiny models and N4/V3 processes in temporary stores, never real pools or models. The required fixtures are listed in the API contract, §8.

## 3. Execution sequence (later, separately authorised)

1. Root review of the implementation; freeze v3 (sha256 in DECISIONS); add a real study config with full hashes.
2. Run `pools` (scientific ledger).
3. Run `train` for the six models in the fixed order.
4. Run `dev-analysis`.
5. Run `final-test` only after explicit authorisation.
6. Report and STOP.
