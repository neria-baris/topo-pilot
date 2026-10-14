# X5 G1 training — implementation plan v4 (for x5g1-train-v4)

14 October 2026, handoff job 0010.

**IMPLEMENTATION CONTRACT PENDING FINAL EXECUTION FREEZE.** Synthetic fixtures only; no study execution. Plans 1–3 are preserved.

## 1. Changes from plan v3 (narrow; the six review-0009 gaps)

| Gap | Change |
|---|---|
| 1. Exports | `x5g1t_exports.study_export`: full `StudyControls` (all STOP sources, live holds, budget, resources) before and after every JSON or npz write; complete-status record; a stopped export writes only a small status record |
| 2. Batch guards | guards before and after every 512-row scoring batch (`x5g1t_score`, optional `guard`) and every oracle batch; a boundary before and after every fresh draw and save; a fresh-ID collision check before the test draw |
| 3. Production config | `x5g1t_config`: exact `StudyConfig` keys; `ProductionSpec` frozen values; read-only validation of sources, stored checkpoint metadata, environment, lineage and roots before any computation; an explicit synthetic-fixture mode that cannot masquerade as production |
| 4. Prerequisites and identity | `verify_export_complete` (status plus manifest); `x5g1t_checks.validate_checkpoints` (ordered grid, run_key and configs, parents, observation and run IDs, payload hash); full-hash verification before and after of every used pool and checkpoint plus world, T and E |
| 5. Usage hold | `x5g1t_usage`: an allow-listed runtime mode; an evidence-based self-hold latch (set on observed ≥ 85% or a warning; cleared only by new OBSERVED evidence for every latched limit); fail-closed parsing |
| 6. Protocol wording | protocol v4 §8–§9: expected latency only, no guaranteed overshoot bound, training RAM unmeasured and checked at runtime |

**Unchanged:**

* the public `Trainer` loop and the checkpoint callback identity;
* the live-process hold;
* the no-retry policy;
* the endpoint, lineage and oracle maths, estimates and reserve.

No framework or daemon is added.

## 2. Independent tests (separate test-writer agents, from API v4 only)

| Writer | Area | Gaps |
|---|---|---|
| (D) | usage latch and v4 controls | 5 |
| (E) | config validation, prerequisites and checkpoint identity | 3, 4 |
| (F) | actual-driver integration | 1, 2 |

(F) reproduces the root's STOP probes through `x5g1t_stages` and the CLI. All tests use tiny N4/V3 fixtures and temporary stores.

## 3. Pending production configuration

`jobs/0010/STUDY_CONFIG_PENDING.json` (mode `production`) is validated read-only with the `validate` stage. **It is not executed.** Execution needs a separate root review and freeze job.
