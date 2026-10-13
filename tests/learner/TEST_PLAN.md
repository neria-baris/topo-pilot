# TEST_PLAN: learner

Marker: `pytest.mark.learner`. Uses a tiny config (2 layers, d = 16, 2 heads) on CPU. Budget: under 45 s.

| ID | Test | Kind |
|---|---|---|
| L01 | Causality: perturbing input position j leaves logits at positions < j unchanged (to 1e-6) | contract |
| L02 | Shapes: logits `[B, 33, V]`; each hook `[B, 33, d]`; `HOOK_NAMES` matches the config depth | contract |
| L03 | `resid_post_{L-1}` → final LN → unembed reproduces the logits exactly | known answer |
| L04 | Overfit: 8 fixed sequences reach CE < 0.05 within 300 steps | property |
| L05 | Step-0 checkpoint equals the initial weights; the same seeds give identical weights and loss curves on CPU | contract |
| L06 | Save → load of a checkpoint reproduces logits to 1e-6 | contract |
| L07 | `Trainer.fit` given a non-`PublicTokenDataset` raises `LEAKAGE` | error path |
| L08 | A forced NaN (monkeypatched loss) raises `NONFINITE_LOSS` | error path |
| L09 | Static: the module source contains no import of world, process, oracle, analysis, or prediction (parse the AST) | contract |
| L10 | The checkpoint schedule is respected exactly; the optimizer state exists only at the final step | contract |
| L11 | X4-F `test_patch.py` (independent): identity at all positions, causality, resid_post_k and ln_final_out sites, non-uniform γ / non-zero β without a second LayerNorm, hooks after the patch, unchanged weights, error paths, no science imports | contract + known answer + error path |
