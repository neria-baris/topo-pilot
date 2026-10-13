# TEST_PLAN: analysis

Marker: `pytest.mark.analysis`. The F1 and Δgeom tests are written by an **independent** test writer. Budget: under 45 s.

| ID | Test | Kind |
|---|---|---|
| N01 | `F1Decision.contrasts`: hand-made S table gives the hand-computed D_i | known answer |
| N02 | `noise_envelope`: hand-made panel values give the hand-computed q95 of \|S_i − S_j\| maximised over cells | known answer |
| N03 | Verdict SUPPORTED: 3 replicates with D > 0 in 8/8 and median > u | known answer |
| N04 | Verdict REJECTED: one replicate with only 6/8 positive (all gates passed) | known answer |
| N05 | Verdict INCONCLUSIVE: any learning gate False, or any input status not OK; the reason is named | known answer |
| N06 | Edge: exactly 7/8 positive counts as passing; median exactly equal to u fails (strict inequality) | known answer |
| N07 | `delta_geom`: planted geometry (D_A = D_B32 plus noise, D_B1 random) gives > 0; swapping gives < 0 | property |
| N08 | Same-last-symbol pairs: the count is correct on a hand-made array; fewer than 200 pairs gives INCONCLUSIVE | known answer |
| N09 | `SigmaCalibrator`: tables where the first, second, or no candidate passes; the fallback ≥ 0.03 path and the stop path | known answer |
| N10 | Space alignment: mismatched id lists raise `SAMPLE_ID_MISMATCH` | error path |
| N11 | R2 baseline: with a ring-shaped symbol transition matrix (hand-built), R2 points lie on a loop (S above null) — documents why R2 is needed | property |
| N12 | Checkpoint-order null: a monotone early-jump sequence gives a small p; a random sequence gives p ≈ uniform | property |
| N13 | Privileged reads are labelled `privileged_eval` in the output records | contract |
| N14 | `ln_gauge_free`: `U(αZ + c·1) == U(Z)` to 1e-6 for α ∈ {0.3, 1, 7.5} and random per-row shifts c, with eps = 0; the shift alone is exact for eps = 1e-5; with eps = 1e-5 scaling is NOT an invariance: test the exact identity `U_eps(αZ) = U_{eps/α²}(Z)` and a visible difference for rows with variance ≪ eps (D-040); rows have mean 0; a hand-computed 1×4 row matches | known answer + property |
| N15 | `readout_projector`: P symmetric and idempotent (1e-10), trace(P) = rank = numpy `matrix_rank(A)` for full-rank A (V < d) and for a rank-deficient W_U (duplicate rows) and a gamma with zeros; `P A = A` | property |
| N16 | `split_readout`: `U_visible + U_null == U`; row-wise dot products ≈ 0; U already in range(A) gives `U_null ≈ 0` | property |
| N17 | Tiny random numpy model (Z → `ln_gauge_free` → `gamma ⊙ u + beta` → `@ W_U^T`): logits from U_visible equal logits from U to 1e-10 (float64) | known answer |
| N18 | `predictive_pointset`: rows sum to 1, metric `hellinger`, ids kept; equals a hand softmax; adding a constant to a logits row changes nothing | known answer |
| N19 | Error paths of part (d): 1-D Z → `ALIGNMENT_ERROR`; eps < 0 → `INVALID_CONFIG`; NaN → `NUMERICAL_FAILURE`; mismatched gamma / W_U / P / ids → `ALIGNMENT_ERROR` | error path |

| N20 | `Sensitivity.activation_D`: `euclidean` equals `scipy cdist`; `chord` equals cdist of row-normalised X and is invariant to positive row scaling; `pca` with `pca_dims = d` on full-rank `X_fit` equals `euclidean` (rotation), with `pca_dims = 1` equals `|((x_i − x_j)·v₁)|` for the hand-computed top singular vector of a 2-D example; the fit set, not X, defines the projection | known answer + property |
| N21 | `Sensitivity.distribution_D`: hand values for two 2-point distributions (Hellinger and √JSD, natural log); bounds `[0, 1]` and `[0, √ln 2]`; disjoint supports reach the upper bound; `head(5, 3) = [0, 1, 2]` | known answer |
| N22 | `circular_agreement`: `A(θ, θ) = 1`; `A(θ + c, θ) = 1`; `A(−θ, θ) = 1`; a hand-computed 4-point value; independent uniform angles (M = 4000) give A < 0.1 | known answer + property |
| N23 | `lattice_angle` / `belief_angle`: hand values on a 3×2 coordinate grid; a delta belief returns the state's angle (mod 2π); a belief split equally on angles 0 and π/2 returns π/4 | known answer |
| N24 | `CircularCorrespondence.compare` on a noisy circle (M = 120, ℝ⁸, noise 0.05) with θ the true angle: status ok, agreement > 0.9, p_value ≤ 0.02 (n_perm = 50); with θ replaced by an independent uniform draw: p_value > 0.02 in at least 4 of 5 draws; on 3 collinear points: status `no_h1_class` and every value None | property (`slow` if > 5 s) |
| N25 | Error paths of part (c): unknown variant, `pca` without `X_fit`, chord zero row, non-distribution rows, mismatched angle lengths, `n_perm = 0` | error path |
| N26 | Part (e) `tests/analysis/test_horizon.py` (X4 Phase B §8): Helmert basis; constant emissions → FACTORIZES; four-state path Q1(δ0) = Q1(δ1), Q2(δ0)[AA] = 1, Q2(δ1)[AB] = .16, ALLOWS_STABLE; constructed G2 = G1 L → FACTORIZES; certificate and tolerance rows; symbol-permutation invariance; joint order and marginals catch bT²E and transposed order; Hellinger bounds and error path; deterministic anchors; self/duplicate/symbol exclusion; screen, 2-of-3 rule, overall and strict verdicts | known answer + property + error path |
| N27 | Part (f) `test_circular_bound.py`: bound = 1 when the symbol determines θ; hand value 1/3; dominates every symbol function (both branches) and is attained by group means; rotation/relabelling invariance; error paths | known answer + property + error path |
| N28 | Part (g) `test_x4f_targets.py`, `test_x4f_erasure*.py`, `test_x4f_scores.py` (independent): targets, retained-range whitening, oblique eraser rank/idempotence/exactness, batch convention, random families in span(U_keep), every degeneracy status, R²/KL/RBF/Ledoit–Wolf/support/verdict rules | known answer + property + error path |
| N29 | Part (h) `test_x5_kernel.py`, `test_x5_context.py` (independent): rate, spectrum, ceil mixing bound, IAT, statuses, rate-matched validity, context equality/zero rules, verdict precedence | known answer + property |
