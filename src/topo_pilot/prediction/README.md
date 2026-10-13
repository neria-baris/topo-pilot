# `prediction`

## Purpose

Predictive evaluation without PH and without the model: n-gram baselines (a), predictive metrics and the learning gate (b), and the ridge probe (c). All quantities are in nats.

## Logic

- **n-gram.** Order 1 is the unigram over all 33 positions of the train tokens. Order 2 conditions on the last token. Bigram counts are taken within sequences only, so contexts never cross sequences and there is no BOS context.
  - Additive: `p(w|c) = (n(c,w)+a)/(n(c)+aV)`. With `a = 0` this is the exact MLE; a context unseen in train backs off to the unigram distribution with the same `a`.
  - Kneser-Ney (order 2, interpolated, discount `d = a`, default 0.75): `p(w|c) = max(n(c,w)-d,0)/n(c) + d N1+(c,.)/n(c) * p_cont(w)`, with `p_cont(w) = N1+(.,w)/N1+(.,.)`. An unseen context uses `p_cont`. Order 1 is the MLE.
  - `select_smoothing(dev, grid)` scores each alpha by dev cross-entropy of `w_33` given `w_1..w_32` (D-021), keeps the best (earliest on ties), refits nothing, and returns it.
- **Metrics.** `kl` uses `0 log 0 = 0`; `p > 0` with `q = 0`, or rows not summing to 1 within 1e-6, raise `NUMERICAL_FAILURE`. `regret` is the exact mean `KL(q_C || p_model)`. `captured = 1 - regret/G_C`, `nan` if `G_C <= 1e-6`.
- **Gate.** `LearningGate.evaluate(captured)` returns `GateCheck("learning_gate", passed, value, 0.8)`. `evaluate_with_status` also returns the `Status`: `INCONCLUSIVE` for NaN (check has `passed=False, value=None`), else `OK`.
- **Bootstrap.** Resamples whole groups with replacement using the injected `rng`, averages all rows of the drawn groups, and returns the 2.5/97.5 percentiles.
- **Join.** `join_by_history_id(a, b)` returns `idx` with `b[idx] == a`; any length, duplicate, or id-set mismatch raises `JOIN_CARDINALITY`.
- **Ridge.** Closed form on centred data with an unpenalised intercept. `lambda` is chosen by validation MSE. `fit(..., splits=("dev_fit","dev_val"))` raises `LEAKAGE` (check `probe_split`) if `"test"` is listed. `score` returns `mse` and `r2`.

## Data

Reads `ObservationSet` (train, dev, test) and `HistoryIndex`. Writes `BaselineOutputs(ngram_order, smoothing="additive:<alpha!r>", history_id, probs)` with parents `[train, dev, test, history_index]`, one per order 1 and 2. The grid is `(1e-3, 1e-2, 1e-1, 0.5, 1.0)`. `run_metrics` (W4) and `run_probes` (W5) raise `NotImplementedError`: the learning metrics and the probe I/O run in `experiment` (S3/S4 and S7, D-047), which calls `PredictiveMetrics`, `LearningGate` and `RidgeProbe`.

## Public API

`NGramBaseline`, `PredictiveMetrics`, `LearningGate`, `RidgeProbe`, `PredictionStage`, `join_by_history_id` (see SPEC.md and the docstrings). Only `stage.py` touches the store.

## How to test

```bash
python -m pytest tests/prediction -q
```
