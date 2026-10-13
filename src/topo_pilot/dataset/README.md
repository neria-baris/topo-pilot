# `dataset`

## Purpose

Samples trajectories from (T, E, pi) in the emit-then-transition order, splits them by trajectory, writes the public observations and the privileged latent sidecar as separate artifacts, and builds the fixed analysis panels. This module is the leakage boundary.

## Logic

**Sampling** (`sampler.py`). `z_1 ~ pi`; for t = 1..33 emit `w_t ~ E[z_t]`, then (t < 33) `z_{t+1} ~ T[z_t]`. All trajectories are drawn together; every categorical draw is an inverse CDF on the cumulative row with one `rng.random(n)` per step (order: initial state, then per step emission, transition). Cumulative rows are set to exactly 1 from the last positive entry on, so zero-probability symbols or states are never drawn despite round-off.

**Canonical symbol order (D-019).** The stage samples from `E_canon = E[:, symbol_perm]`, gets canonical index `j`, and emits token `symbol_perm[j]`. With the identity permutation this is plain sampling. Replicates that differ only in the symbol renaming therefore share the same test latent paths, and their test tokens differ by the relabelling.

**Seed scheme** (D-012, D-019; `sigma` is `repr(float)` or `"none"`):

| Stream | Generator |
|---|---|
| test split | `SeedTree(0).generator("data", "test", family, mode, sigma)` |
| panels | `SeedTree(0).generator("panels", family, mode, sigma)` |
| train, dev | `seeds.generator("data", split, family, mode, sigma, seeds.master)` |

`mode`, `sigma` come from `store.meta(emission_id).config`; `family` from the config of the emission's first parent (the world).

**Sequence-id rule.** `sequence_id = (process_code << 32) | (split_code << 28) | index`, int64.
`process_code` is the first 31 bits of `sha256(canonical_json([family, mode, sigma, replicate]))` (big-endian top bits of the first 4 bytes, shifted right by 1). `replicate` is `seeds.master` for train and dev and the string `"shared"` for test, so test ids are equal across replicates. `split_code`: train 1, dev 2, test 3. Ids are non-negative and unique across splits (distinct split codes); `index < 2^28`.

**Panels** (`panels.py`). `perm = rng.permutation(R)`; panel k takes `perm[(k-1)S : kS]`, so panels are disjoint and each holds S distinct trajectories. Rows are ordered by (panel, drawn position). `tokens_hash = tokens_hash(tokens[row, :32])`, `history_id = make_history_id(dataset_id, sequence_id, 32, tokens_hash)`, with `dataset_id` the test ObservationSet artifact id. No latent information is used. `n_test >= n_panels * panel_size` is required.

**Checks** (`checks.py`). Token >= V or state >= N: `ALIGNMENT_ERROR`. Shared `sequence_id` between splits: `SPLIT_OVERLAP`. First-token chi-square against `n * (pi E)` (cells with expected count < 5 pooled; skipped for n < 200): p < 1e-4 gives `NUMERICAL_FAILURE` with detail `sampler_bias`. A non-`ObservationSet` or one with a non-public field given to `PublicTokenDataset`: `LEAKAGE`. Identical windows across splits are not an error.

## Data

Reads `TransitionSpec`, `EmissionSpec` (consumer `dataset`) and the metadata of the emission and its world. Writes, all with consumer `dataset`:

- `ObservationSet` train/dev/test, parents `[transition_id, emission_id]`; the test config has no `replicate`, train/dev do;
- `EvalSidecar` dev and test only (train latents are never persisted), same parents;
- `HistoryIndex`, parent `[obs_test_id]`.

## Public API

`DatasetConfig`, `HMMSampler`, `PanelBuilder`, `PublicTokenDataset`, `DatasetStage` (see `SPEC.md`).
`PanelBuilder.build(test, cfg, rng, *, dataset_id="")` takes the extra keyword `dataset_id` (the test artifact id, needed for `history_id`).

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/dataset -q
```
