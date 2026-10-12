# TEST_PLAN: prediction

Marker: `pytest.mark.prediction`. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| R01 | `kl(q, q) = 0`; KL ≥ 0 on random pairs; hand value for a 2-symbol example | known answer + property |
| R02 | `nll` of a constant uniform model equals log V | known answer |
| R03 | Unigram fit on hand-made tokens gives exact frequencies (additive α = 0) | known answer |
| R04 | Bigram on a deterministic cycle sequence predicts the successor with probability → 1 (small α) | known answer |
| R05 | Smoothing selection uses dev only (spy on inputs); test is never passed to `fit` or `select` | contract |
| R06 | `captured` and `LearningGate`: hand values; G_C ≈ 0 gives status INCONCLUSIVE | known answer |
| R07 | `bootstrap_ci` resamples groups: a constant within-group array gives a CI that reflects between-group variance only | property |
| R08 | Join with mismatched `history_id` sets raises `JOIN_CARDINALITY` | error path |
| R09 | RidgeProbe: recovers a planted linear map (R² > 0.99); shuffled labels give R² ≈ 0 on held-out | property |
| R10 | A probe given test rows at fit time raises `LEAKAGE` | error path |
