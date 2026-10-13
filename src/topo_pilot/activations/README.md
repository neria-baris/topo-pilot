# `activations`

## Purpose

Deterministic, gradient-free extraction of hook activations and logits at the analysis position for the fixed analysis histories, from a saved checkpoint. It never pools, averages or joins with latent information (joins with beliefs happen later, in `analysis`, by `history_id`).

## Logic

**Position convention.** A trajectory stores `w_1..w_33` as `tokens[:, 0..32]`. `SequenceLayout().model_inputs(tokens, V)` returns `[BOS=V, w_1..w_32]`: 33 positions `p = 0..32`. Position `p` holds token `w_p` (BOS at `p = 0`), sees the history `w_1..w_p`, and its logits predict `w_{p+1}`. The analysis position is `p = end = 32`.

Worked example (V = 3, tokens `w = [2, 0, 1, ..., w_32, w_33]`): the input is `[3, 2, 0, 1, ..., w_32]`. Position 1 holds `w_1 = 2`; position 32 holds `w_32` and sees all of `w_1..w_32`. We take `hooks[name][:, 32]` and `logits[:, 32]`; those logits predict `w_33`. Token `w_33` is not in the input, so changing it cannot change the output (test A03).

**Algorithm.**
1. Validate hook names against `embed, resid_post_0..resid_post_{L-1}, ln_final_out` (`L = model.cfg.n_layers`): `UNKNOWN_HOOK`.
2. Select index rows (`panels` filter, index order preserved); map to observation rows by `sequence_id`; require `end == 32` and `contracts.tokens_hash(tokens[:32]) == index.tokens_hash`: otherwise `ALIGNMENT_ERROR`.
3. Batch in index order under `eval()` and `torch.no_grad()`; the output is concatenated in the same order, so row `i` is index row `i` for any batch size.
4. On the first batch, compare the hooked logits with a plain forward pass: more than 1e-5 apart gives `NUMERICAL_FAILURE`.

Edge cases: an empty panel selection returns empty arrays of the right rank; device `"auto"` is CUDA if available, else CPU.

## Data

Reads `Checkpoint`, `ObservationSet` (test split), `HistoryIndex` (consumer `"activations"`). Writes `ActivationSet(source="model")` with parents `[checkpoint, observations, index]` and config `{hooks, panels (sorted list or "all"), checkpoint_id}`. Never loads `EvalSidecar` (the store raises `LEAKAGE`).

## Public API

- `ActivationExtractor(hooks, batch_size=256, device="auto").extract(model, obs_test, index, panels=None) -> (A [M, K, d] float32, logits [M, V] float32, history_ids)`.
- `ActivationStage().run(checkpoint_id, obs_test_id, history_index_id, hooks, panels, store) -> ActivationSet id`.

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/activations -q
```
