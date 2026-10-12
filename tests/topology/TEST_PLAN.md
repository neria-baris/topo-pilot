# TEST_PLAN: topology

Marker: `pytest.mark.topology`. Written by an **independent** test writer. Items marked `slow` are excluded by default. Budget for the default set: under 60 s.

| ID | Test | Kind |
|---|---|---|
| T01 | Metrics: hand values for Euclidean, chord, Hellinger, and √JS on 3 small vectors; metric axioms on random inputs | known answer + property |
| T02 | Hellinger on non-distributions raises; chord on a zero row raises | error path |
| T03 | Square of 4 points with unit sides: one H₁ bar, birth 1, death √2 | known answer |
| T04 | Scale covariance: multiplying D by c multiplies births and deaths by c; S is invariant | property |
| T05 | Permuting the points leaves the diagrams unchanged | property |
| T06 | Noisy circle (M = 200, ambient 128): S is clearly above the isotropic Gaussian floor (≥ 3× the mean of 10 Gaussian draws) | property |
| T07 | Disk and Gaussian clouds: S below a documented threshold derived in the test from 10 null draws | property |
| T08 | Deduplication: duplicated points give the same diagrams as the unique set; an all-zero D gives `COLLAPSED` and S = 0 | contract |
| T09 | Censoring: with a too-small threshold, H₁ bars are marked censored, not dropped | contract |
| T10 | `coeff_p = 3` is passed through: an RP²-like synthetic sample (antipodal sphere quotient) differs in β̂₁ between p = 2 and p = 3 | known answer, `slow` |
| T11 | **G-A calibration** (`slow`): circle vs disk at M = 512 in ℝ¹²⁸ with noise, 20 draws each; correct ordering (S_circle > max S_disk) in ≥ 19/20 | calibration |
| T12 | Circular coordinates on a noisy circle: circular correlation with the true angle > 0.95 | known answer, `slow` |
| T13 | PCA fitted on one set and applied to another; the dimension is respected; `pca_dims = None` is a no-op | contract |
