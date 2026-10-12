# TEST_PLAN: integration (runs at gates only)

Marker: `pytest.mark.integration`, excluded by default. Run with:

```bash
python -m pytest tests/integration -m integration -q
```

| ID | Test | When |
|---|---|---|
| I01 | `test_s1.py`: S1 on the real core config produces WorldSpec, TransitionSpec, and EmissionSpec; G-A checks 1–2 pass (check 3, the synthetic calibration, comes from topology T11) | end of W1 |
| I02 | `test_s2_mini.py`: S2 on a scaled-down config (n = 4, V = 4, 2k trajectories) runs end to end; the oracle, baselines, σ table, and discriminability table are written | end of W2 |
| I03 | `test_mini_pipeline.py`: S1→S4 on a mini config (n = 4, V = 4, 2 seeds, 2-layer d = 16 model, 200 steps, M = 64, 2 panels), CPU, under 5 minutes; F1Decision returns some verdict; the report renders | end of W4 |
| I04 | `test_leakage_end_to_end.py`: shuffling `EvalSidecar.z` leaves every learner and activations artifact id unchanged (proof the learner never read it) | end of W3 |
| I05 | `test_bundle_roundtrip.py`: run the mini S4 job via `BundleExecutor` in a temp dir; the imported artifact ids equal those of the local run | end of W4 |
| I06 | `test_rerun_identity.py` (S8): rerunning one mini run from scratch reproduces the artifact ids | S8 |
