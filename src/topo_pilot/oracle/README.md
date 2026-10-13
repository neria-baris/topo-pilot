# `oracle`

## Purpose

Exact Bayesian quantities for a known HMM `(T, E, pi)` given only the visible tokens: filtered beliefs, next-symbol and two-symbol futures, the last-symbol posterior, context gain and observability. It never sees latent states, checkpoints or activations; its consumer name `"oracle"` has no `EvalSidecar` access, so the store raises `LEAKAGE` if it tried.

## Logic

Notation (RESEARCH_SUMMARY §5): `T [N,N]`, `E [N,V]`, `pi [N]`, row vectors, `w_t = tokens[:, t-1]`.

**Filter.** `a_1 = pi`; `b_t = a_t ⊙ E[:, w_t] / (a_t E[:, w_t])`; `a_{t+1} = b_t T`. Every row restarts from `pi`.

**Derivation of `q_t`.** `a_{t+1}[z] = P(z_{t+1} = z | w_{1:t})`, because `b_t[z] = P(z_t = z | w_{1:t})` and the chain moves by `T` (emit-then-transition). Then
`q_t[v] = P(w_{t+1} = v | w_{1:t}) = Σ_z a_{t+1}[z] E[z, v] = (b_t T E)[v]`. With no history, `q_0 = pi E`. The normaliser `Z_t = a_t E[:, w_t] = q_{t-1}[w_t]` is the predictive probability of the observed symbol, so
`log p(w_{1:P}) = Σ_t log Z_t` (`log_evidence`) and `ce[:, t-1] = -log q_{t-1}(w_t) = -log Z_t`.

**Derivation of `F2`.** The joint law of the next two symbols (i, j) is
`F2[i,j] = Σ_{m,k} (bT)[m] E[m,i] T[m,k] E[k,j] = Σ_m (bT)[m] E[m,i] (TE)[m,j]`,
computed by one `einsum("rm,mi,mj->rij")`. Summing over `j` uses `Σ_j (TE)[m,j] = 1`, giving `Σ_m (bT)[m] E[m,i] = (bTE)[i] = F1[i]`. The code checks this to 1e-12.

**Last-symbol baseline.** `r_w = pi ⊙ E[:, w] / (pi E[:, w])` (the filter after one symbol); `q_last = r_w T E`. `b^(1) = r_{w_32}`, `b^(32) = b_32`.

**Context gain.** `G_C = mean_r KL(q_C || q_last)` in nats. Terms with `q_C = 0` add 0; `q_last = 0` where `q_C > 0` raises `NUMERICAL_FAILURE` (impossible for a correct filter).

**Observability.** `G_1 = T E`; `G_j = [T diag(E[:, s]) G_{j-1}]_s` (columns blocked by the first symbol s). Then `b G_j` is the vector of `P(next j symbols = s)` over all strings of length j. `O_k` stacks `G_j^T` for `j ≤ k` (rows = strings, cols = N). Singular values are reported unthresholded.

**Literature mapping.** Shai et al.'s `η` equals our `a_{p+1} = b_p T`, with `T^{(x)} = diag(E[:,x]) T`.

**Edge cases.** A zero normaliser raises `IMPOSSIBLE_HISTORY`; no epsilon is ever added. Beliefs and predictives must sum to 1 within 1e-10 (`NUMERICAL_FAILURE`). `P > 33`, a symbol `>= V`, or non-integer tokens raise `ALIGNMENT_ERROR`. Float64 with per-step normalisation avoids underflow.

## Data

`OracleStage` loads `TransitionSpec`, `EmissionSpec`, `ObservationSet` (test) and `HistoryIndex`. It checks `end == 32` for each row (`ALIGNMENT_ERROR`), maps `sequence_id` to its test trajectory and verifies `tokens_hash` (`SAMPLE_ID_MISMATCH`). It writes one `OracleOutputs` over all HistoryIndex rows in index order (`b32, b1, q, q_last, F2` as float32, `belief_entropy` in nats, `log_evidence` of `w_1..w_32`) plus `ce_oracle_all_positions [R_test, 33]` float32 over all test trajectories, and one `ProcessDiagnostics` (`G_C`, `mean_H_b1`, `O_singular_values` for k ≤ 3, `sigma`, `world_family` from the nearest `WorldSpec` ancestor of the emission). Both have parents `[transition, emission, obs_test, history_index]`.

## Public API

`BayesFilter(T, E, pi).run(tokens) -> FilterResult(b, q, log_evidence, ce)`, `.belief_at(tokens, p)`; `LastSymbolPosterior.r / q_last`; `FutureOperator.F1 / F2 / observability_singular_values`; `context_gain(q_C, q_last)`; `OracleStage.run(transition_id, emission_id, obs_test_id, history_index_id, store) -> {"oracle", "diagnostics"}`.

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/oracle -q
```
