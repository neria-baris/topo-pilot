# learner

## Purpose

Model definition, training loop, checkpoint save/restore. It sees only public tokens
(`PublicTokenDataset`) and never loads `EvalSidecar`, `TransitionSpec` or `EmissionSpec`.

## Logic

**Architecture** (RESEARCH_SUMMARY section 6): decoder-only, pre-LN, learned positional embeddings,
GELU MLP, final LayerNorm, untied unembedding without bias, dropout 0. Input vocabulary `V+1`
(BOS = `V`), output vocabulary `V`, 33 positions. Attention is
`F.scaled_dot_product_attention(..., is_causal=True)`.

One block and the hook positions (`x` is `[B, 33, d]`):

```
 tokens -> tok_emb + pos_emb ----> [embed] -----------------------------+
                                                                        v
   block k:   x --+--> LN1 -> causal MHA -> proj --(+)--> x' --+--> LN2 -> fc_in -> GELU -> fc_out --(+)--> x''
                  |________________ residual _______________|   |_____________ residual ______________|
                                                                  x'' = [resid_post_k]   (before any final LN)
 after last block:  x'' -> LN_final -> [ln_final_out] -> unembed (no bias) -> logits [B, 33, V]
```

Hooks: `embed`, `resid_post_0 .. resid_post_{L-1}`, `ln_final_out` (`HOOK_NAMES` is the
4-layer list; `model.hook_names` follows the config depth). `forward(..., return_hooks=names)`
returns them in `ModelOutput.hooks`; unknown names raise `UNKNOWN_HOOK`.

**Init.** N(0, 0.02) for embeddings and matrices (residual output projections scaled by
`1/sqrt(2L)`), zero biases. Built inside `torch.random.fork_rng(devices=[])` after
`manual_seed(seeds.seed("init", *run_key))`, so the global RNG is untouched.

**Causality check.** At construction a random batch (local `torch.Generator`) is run with one
position perturbed; logits at earlier positions must change by at most 1e-6, else
`CAUSAL_MASK_FAILED`.

**Optimiser.** AdamW; weight decay (0.1) on weight matrices only (all `Linear` weights including
the unembedding); biases, LayerNorm and both embeddings are excluded. LR multiplier after `s`
updates: `(s+1)/warmup` for `s < warmup`, then `0.5(1+cos(pi (s-warmup)/(steps-warmup)))`, which is
0 at `s = steps`. Global-norm gradient clipping 1.0.

**Loss and batches.** Mean cross-entropy over every position. Each step draws `batch_size`
trajectory indices with replacement from `seeds.generator("batch_order", *run_key)`. All training
items are materialised once into tensors.

**Checkpoints.** Step 0 is saved before any update; later steps right after the update. Dev CE
(full dev set, batched, eval mode, no grad) is computed at every checkpoint step and passed to
`on_checkpoint(step, model, info)` (`info`: `dev_ce`, `train_loss`, `is_final`, and at the final
step `optimizer_state`, `scheduler_state`). `state` = `torch.save({"model": ...[, "optimizer",
"scheduler"]})`; this is byte-deterministic (test L06b), so re-running a stage yields the same
artifact ids. `LearnerStage` saves `Checkpoint` artifacts with parents `[obs_train_id,
obs_dev_id]` and config `{run_key, step, model_config, train_config}`.

**Edge cases.** `checkpoint_steps` must lie in `0..steps`, `steps >= 1`, `warmup >= 1`
(`INVALID_CONFIG`). If `steps` is not a checkpoint step, no optimizer state is stored at all.
Determinism: `torch.use_deterministic_algorithms(True, warn_only=True)` during `fit`; CPU runs
with equal seeds are bit-identical; GPU runs are not guaranteed to be.

## Data

In: two `ObservationSet` artifacts (loaded with consumer `learner`). Out: one `Checkpoint` per
checkpoint step. `TrainSummary`: `steps_done, final_train_loss, dev_ce_by_step,
tokens_per_second` (target tokens / wall time, excluding the step-0 evaluation and callback),
`wall_time_s, device, torch_version, checkpoint_ids` (filled by `LearnerStage.last_summary`).

## Public API

`ModelConfig`, `TrainConfig`, `HOOK_NAMES`, `TransformerLM`, `ModelOutput`, `Trainer`,
`TrainSummary`, `LearnerStage` (`run(...) -> list[str]`, `last_summary`), `load_model(checkpoint)`.

Errors: `CAUSAL_MASK_FAILED`, `NONFINITE_LOSS`, `LEAKAGE` (non-`PublicTokenDataset`),
`UNKNOWN_HOOK`, `INVALID_CONFIG`.

## How to test

```
.venv\Scripts\python.exe -m pytest tests/learner -q
```

Tests L01-L10 use a 2-layer, d = 16 model on CPU (about 5 s). L04 note: distinct sequences cannot
be memorised below `ln(n_distinct)/33` nats (first divergence has identical prefix), so the test
uses 8 sequences made of 2 distinct ones.
