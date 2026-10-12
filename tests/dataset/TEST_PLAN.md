# TEST_PLAN: dataset

Marker: `pytest.mark.dataset`. Uses `contracts.testing.tiny_hmm`. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| D01 | Deterministic HMM (T = permutation cycle, E = identity): the sampled sequence equals the hand-derived one for a fixed start | known answer |
| D02 | Over 20k samples from `tiny_hmm`: empirical z-transition, w\|z, and first-token frequencies match T, E, πE (χ² test, p > 1e-3) | property |
| D03 | Emission happens *before* the transition: with E = identity, `tokens[:, t] == states[:, t]` | contract |
| D04 | Splits have disjoint `sequence_id`s; the test split is identical across replicate seeds, and train differs | contract |
| D05 | Panels: 8 disjoint sets of 512 distinct trajectories, end = 32; `history_id` is reproducible | contract |
| D06 | `ObservationSet` has no latent field; `PublicTokenDataset` built from an `EvalSidecar` raises `LEAKAGE` | error path |
| D07 | `PublicTokenDataset[i]` returns inputs `[V, w1..w32]` and targets `[w1..w33]` (via `SequenceLayout`) | known answer |
| D08 | No train sidecar is persisted (store listing after `DatasetStage.run`) | contract |
| D09 | A biased sampler (monkeypatched) is caught by the first-token χ² check | error path |
