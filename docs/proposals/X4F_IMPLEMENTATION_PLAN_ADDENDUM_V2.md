# X4-F implementation plan — addendum v2 (for x4f-exec-v2)

14 October 2026. Branch `x4f-execution-contract`. Handoff job 0002.

**This addendum amends [addendum v1](X4F_IMPLEMENTATION_PLAN_ADDENDUM.md) and [the plan](X4F_IMPLEMENTATION_PLAN.md).** Both are kept unchanged; where they differ, [x4f-exec-v2](X4F_EXECUTION_PROTOCOL_V2.md) governs. It is a plan only: nothing here has been implemented or run.

## B1. Scope of the first execution job (narrowed from v1)

The first execution job does only three things:

1. Implement the adapter, the analysis functions and the gate orchestration, with independent tests.
2. Extract dev activations at step 5000: `embed`, `resid_post_1`, `resid_post_3` and `ln_final_out`, plus logits.
3. Run G1–G5 on calibration and validation; then STOP.

It does **not** build or run:

* F-circlePC1, F-y or F-r2;
* the r2 eraser;
* step-0 extraction;
* fresh sampling or ΔR.

## B2. Analysis function changes (versus addendum v1, section A3)

| Function | Change | Required independent fixtures |
|---|---|---|
| `whiten(X, floor=1e-10)` | **new**. Returns μ, U_keep, Λ_k, W, W⁺ and k, or the status FEATURES_DEGENERATE. | (i) anisotropic correlated data (condition number ≥ 1e4): W·Σ·Wᵀ = I_k within 1e-8; (ii) rank-deficient data (d = 8 with exact rank 5): k = 5 and W W⁺ = I_5; (iii) all-zero X gives FEATURES_DEGENERATE |
| `fit_oblique_eraser(X, Z, whitening)` | rank r from G = WΣ_xz with tolerance 1e-8 · σ_max; returns M, E, r and the statuses TARGET_ZERO_VARIANCE / TARGET_UNCORRELATED / ERASER_INVALID; batch application X′ = (X − μ)Mᵀ + μ | (i) correlated anisotropic X with a planted 2-D target: cross-covariance after erasure ≤ 1e-8 relative, M² = M, rank(E) = 2, and orthogonal signal kept; (ii) a target lying in only one direction (q = 2 but rank 1): r = 1, **not 2**; (iii) a constant target gives TARGET_ZERO_VARIANCE; (iv) a target independent of X, constructed so that the exact cross-covariance is 0: TARGET_UNCORRELATED; (v) rank-deficient X: the erasure stays within span(U_keep), and the component in discarded directions is unchanged |
| `random_family(whitening, rank, target_disp, X, family, seed, n_accept=20, max_draws=10_000)` | draws in R^k and embeds via U_keep; same μ/W/W⁺ as the target; DRAW_DEGENERATE rejection; RANK_EXCEEDS_RETAINED; ZERO_DISPLACEMENT; FAMILY_UNMATCHED; accepted indices recorded | (i) rank-deficient X: every accepted E_j has a range inside span(U_keep) and rank r; (ii) anisotropic X: the acceptance window (5%) is applied to the mean displacement; (iii) zero target displacement gives ZERO_DISPLACEMENT; (iv) a draw budget too small gives FAMILY_UNMATCHED; (v) determinism given the seed tuple |
| `r2_score(Y_pred, Y_val, mean_cal)` | **new**. Pooled, around the calibration mean; R2_UNDEFINED_ZERO_VARIANCE when SST ≤ 1e-12·n·q | hand values; a zero-variance target gives the status |
| `nested_ridge` | calls `RidgeProbe([λ])` per λ and fold; standardisation with a 1e-12 std floor; ties → larger λ | validation rows untouched during selection (NaN-poison test); known λ selection on a planted fixture |
| `displacement_report` | excludes histories with d_i(t) ≤ 1e-12·mean‖x − μ‖ from the mismatch ratio and counts them | a zero-displacement row is excluded and counted |
| `support_report` | SUPPORT_DEGENERATE; RATIO_UNDEFINED; the literal zero-median rule | an identity patch gives about 1% beyond q99; median-zero fixture; duplicate rows give RATIO_UNDEFINED |
| `kl_rows(p, q)` | **new**. Rows in nats; KL_UNDEFINED on a zero-vs-positive entry; no clipping | hand values; a zero entry gives the status |
| `gate_verdict` | status precedence per the v2 §10 table; an optional-family failure never fails the primary | truth table, including control degeneracy |

**Unchanged from addendum v1:** `circle_expectation`, `rbf_features` (now with RBF_DEGENERATE), `final_null_replacement` (now with READOUT_DEGENERATE), `damage_profile`.

**Adapter unchanged:** `learner.forward_with_patch`, with its fixture tests as in v1.

## B3. Independence of tests

The learner tests (adapter) and the analysis tests (whitening, erasers, families, statuses, verdict) are written by a separate test writer from the v2 protocol sections 5, 6, 7, 9 and 11, before the implementation is read. Fixtures are synthetic only; no real artifacts are used.

## B4. Cost

The cost estimate is unchanged from addendum v1 (≤ 0.3 CPU h expected, against the 1 CPU h first-task cap). Building only F-primary removes about one third of the random-draw work.

## B5. Deferred (listed, not dropped)

The following are deferred:

* F-circlePC1 and F-y, together with S4;
* F-r2, with an r2 causal-support rule;
* the natural-donor patch;
* the frozen-vs-refitted readout comparison;
* the dose curve;
* the PH manipulation check;
* the fresh test lineage and all test-time ΔR comparisons.

Each requires its own reviewed task, and the families need frozen rules before any fresh sampling.
