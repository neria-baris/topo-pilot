# X4-F implementation plan — addendum for x4f-exec-v1

14 October 2026. Branch `x4f-execution-contract`. Handoff job 0001.

**This addendum amends [X4F_IMPLEMENTATION_PLAN.md](X4F_IMPLEMENTATION_PLAN.md), which stays unchanged.** Where they differ, [X4F_EXECUTION_PROTOCOL.md](X4F_EXECUTION_PROTOCOL.md) (x4f-exec-v1) governs. It is a plan only: nothing here has been implemented or run.

## A1. Scope of the first execution job

The first execution job does only three things:

1. Implement the frozen-forward adapter, the pure analysis functions and the gate orchestration, with independent tests.
2. Extract dev activations into an independent store.
3. Run G1–G5 on calibration (panels 1–6) and outer validation (panels 7–8), write the gate report, and STOP.

It does **not** do any of the following:

* fresh-test sampling;
* test-time ΔR (regret change), or validation regret;
* the natural-donor patch;
* the refitted readout;
* the dose curve;
* the PH manipulation check.

## A2. Adapter (learner) — replaces the `resume_from_site` sketch

`learner.forward_with_patch(model, inputs, site, index, replacement) -> PatchedOutput(logits [R, 33, V], hooks)`. Its semantics, tolerances and fixture tests are those of x4f-exec-v1 §7.

* **Exports.** It is exported through `learner.__init__`.
* **Imports.** It imports only `torch` and `contracts`.
* **Tests.** An independent test writer writes `tests/learner/test_patch.py` from the protocol §7 before reading the implementation (ORCHESTRATOR §2).

## A3. Analysis functions (pure; new `analysis/x4f_*.py`, each ≤ 400 lines)

| Function | Protocol § | Independent known-answer / property tests |
|---|---|---|
| `circle_expectation(b, x, period)` | §2 | delta belief → unit vector; uniform x → 0; rotation covariance |
| `two_symbol_posterior` | §2 | not in analysis: computed in experiment with `BayesFilter` on (w31, w32); tested there against brute-force enumeration on a tiny HMM |
| `nested_ridge(X_cal, Y_cal, panel_cal, X_val, Y_val, grid)` | §4 | leave-one-panel-out picks λ without touching the validation rows (asserted by passing NaN validation rows during selection); R² definition; ties → larger λ |
| `shuffled_q95(...)` | §4 | uses the same pipeline; seeded determinism; the shuffle scores about 0 on an independent target |
| `rbf_features(X, n, rng_omega, rng_bandwidth)` | §4 | deterministic given seeds; median-bandwidth rule; shape |
| `fit_oblique_eraser(X, Z, eig_floor, rank_tol)` | §5 | post-erasure cross-covariance ≤ 1e-8 relative; a planted target is erased while orthogonal signal is kept; rank ≤ dim Z; α = 1 is idempotent |
| `random_matched_erasers(X, W, W_pinv, mu, rank, target_mean_disp, n_accept, max_draws, seed_fn)` | §6 | acceptance rule; draw indices recorded; exhausting draws yields `accepted < 20` |
| `displacement_report(X, X_a, X_b)` | §6 | quantiles; per-history mismatch on hand values |
| `final_null_replacement(z3, gamma, beta, W_U)` | §5 | reuses `readout_projector(gamma, C·W_U)`; centred logits unchanged ≤ 1e-8; never applied to y |
| `support_report(X_cal, X_patch, X_val)` | §9 | identity patch → about 1% beyond q99; a planted shift is flagged; 10-NN ratio about 1 for the identity |
| `damage_profile(...)` | §8 | units kept separate: R² quantities vs nats |
| `gate_verdict(g1 … g5)` | §10 | FEASIBLE / NOT_FEASIBLE / INCONCLUSIVE truth table |

## A4. Experiment orchestration (not a registered stage; no `stages.yaml` change)

| Module | Role |
|---|---|
| `x4f_inputs.py` | resolve the 3 step-5000 checkpoints (and optionally step 0), the dev HistoryIndex / ObservationSets, and T/E/π via the existing resolvers; check against frozen IDs; record provenance rows |
| `x4f_extract.py` | `ActivationStage.run(..., hooks=[embed, resid_post_1, resid_post_3, ln_final_out], panels=[1..8])` into an independent store (`topo-pilot/x4f-research-store/`). Reads from main pass through `ReadThroughBackend`; the main listing hash is checked before and after. |
| `x4f_targets.py` | b32, b2 and b1 with the oracle kernels; m32, m2, m1, r2, the y-target, local position and Q1, on the dev tokens |
| `x4f_gates.py` | G1–G5 per model; budget (`Budget`, cap 1 CPU h for this task); peak memory; gate report JSON/CSV with `MANIFEST`; MetricRecords in the independent store |

The adapter runs under consumer `experiment`. Checkpoints load via `learner.load_model`. Analysis receives numeric arrays only.

## A5. Provenance recorded by the gate job

* the protocol doc sha256 (x4f-exec-v1) and the producer commit (clean tree required);
* checkpoint, dev ActivationSet, HistoryIndex, ObservationSet and T/E/π IDs;
* every seed stream and the accepted random draw indices;
* eraser parameters (μ, the W eigen-floor count, the P rank and the map checksum), exported as checksummed npz;
* λ per inner selection, and the RBF bandwidth;
* gate values and statuses;
* CPU-s and peak working set, plus the main-store listing hashes.

## A6. Cost (planning estimate, unchanged order of magnitude)

* **Extraction:** about 1 CPU min for 3 models, 4,096 histories and 4 hooks.
* **G1:** nested ridge with 6 folds × 5 λ × 21 runs (target plus 20 shuffles), for several targets and 3 models. Each 128-dimensional ridge solve is milliseconds, so a few CPU min in all. The RBF probe adds a few CPU min.
* **G3–G5:** eraser fits; random families of up to 10,000 draws × 2 ranks × 3 models, each draw being one matrix product on 3,072×128 rows (< 1 CPU min); adapter passes for about 30 replacements × 1,024 validation histories × 3 models (a few CPU min).
* **Expected total:** ≤ 0.3 CPU h against the 1 CPU h first-task cap. The cumulative X4-F cap stays at 3 CPU h.
* **Engineering:** about 2 working days, including the independent tests.

## A7. Deferred items (listed, not dropped)

These remain hypotheses or controls for future, separately issued jobs:

* the natural-donor patch;
* the frozen-vs-refitted readout comparison;
* the dose curve α ∈ {0.25, 0.5, 0.75};
* the PH manipulation check;
* the fresh-test lineage (stream and namespace recorded in protocol §11), together with every test-time ΔR comparison: primary, randoms, controls and S2–S4.
