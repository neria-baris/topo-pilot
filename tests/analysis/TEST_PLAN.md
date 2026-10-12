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
