# analysis (parts a and b, waves W2 and W4)

## Purpose
Project-aware analysis. Part (a) builds the reference comparison spaces on the same histories,
applies the pre-registered sigma rule, and computes the discriminability table (S per space).
Part (b) adds the F1 rule, Delta-geom, baselines R0-R3, the checkpoint-order null and a minimal
layer sweep. Part (c) (sensitivity, circular correspondence) is not implemented yet.
Imports: stdlib, numpy, `topo_pilot.contracts`, `topo_pilot.topology` (package roots).

## Logic
- **Spaces** (`spaces.py`, consumer `"analysis"`). `world` = the world distance matrix `d_M` over
  the N states (metric `flat`, D given). `emission` = the N rows of E (Hellinger). For an
  `OracleOutputs` artifact, rows are in `HistoryIndex` order over all panels (D-020); the index is
  the parent of type `HistoryIndex` (else `MISSING_PARENT`) and its ids must equal the oracle's
  (else `SAMPLE_ID_MISMATCH`). A panel selects its rows and ids. `belief32` / `belief1` are
  b^(32) / b^(1); `future1` = q (= q_32 = b32 T E); `future2` = F2 flattened to `[M, V*V]`
  (renormalised only if every row sum is within 1e-4 of 1, else `NUMERICAL_FAILURE`).
  `null(like, kind, rng)` draws an isotropic or covariance-matched Gaussian cloud of the same
  M and F.
- **Same histories.** `require_same_ids(a, b)` raises `SAMPLE_ID_MISMATCH` unless the ordered id
  lists are identical.
- **PH summary** (`ph_summary`). D = Hellinger (distributions) or Euclidean, duplicates merged,
  `s` = 95th percentile of positive distances, `S = max finite H1 persistence / s`. A collapsed
  cloud gives `S = 0`, status `collapsed`; other statuses (e.g. `censored`) propagate.
- **Sigma rule** (`sigma.py`, RESEARCH_SUMMARY section 4). Candidates in order of first appearance
  in `rows` (callers pass 1.25, 0.75, 2.0). A candidate passes iff in every world
  `mean_H_b1 >= log 2`, `G_C >= 0.10`, `min_p_w >= 0.5/V`; the first passing one wins (`ok`).
  Otherwise the candidate with the highest min-over-worlds `G_C` (earliest on ties) is chosen if
  that value is >= 0.03 (`weak_context`); else `stop_H3` with `sigma = None`. Thresholds are
  constructor parameters.
- **Discriminability table** (`discriminability.py`). Rows `run_id="S2"`, metric ids `S_H1` and
  `scale_s`: world (once per world, condition and panel None), emission (per world and condition),
  belief32 / belief1 / future1 / future2 (per world, condition, panel). The result is not saved.

### Worked toy sigma table (V = 36, so `0.5/V = 0.0139`; log 2 = 0.693)
| sigma | world | mean_H_b1 | G_C | min_p_w | verdict |
|---|---|---|---|---|---|
| 1.25 | cyl | 0.80 | 0.08 | 0.02 | fails G_C |
| 1.25 | sq | 0.80 | 0.15 | 0.02 | |
| 0.75 | cyl | 0.90 | 0.12 | 0.02 | passes |
| 0.75 | sq | 0.85 | 0.11 | 0.02 | passes |
| 2.0 | both | 0.70 | 0.20 | 0.02 | not reached |

Result: `sigma = 0.75`, status `ok`. If instead 0.75 had `G_C = 0.05` in a world and 2.0 `0.02`,
nothing passes; min-world `G_C` is 0.08 / 0.05 / 0.02 so 1.25 is chosen as `weak_context`. If all
three were below 0.03 the status is `stop_H3` (checkpoint H3).

## Part (b) logic
- **F1 rule** (`f1.py`, RESEARCH_SUMMARY 7.4). `contrasts(S)` gives
  `D_i = (S[cyl,final,i]-S[cyl,init,i]) - (S[sq,final,i]-S[sq,init,i])` over sorted panel ids;
  `noise_envelope(S)` gives `u = max over the 4 cells of percentile95{|S_i-S_j|: i<j}`.
  `verdict(...)`: INCONCLUSIVE if any learning gate is False, any input status is not `ok`, or
  fewer than 3 replicates (reasons name `learning_gate`, `status`, `replicates`); else cond1 =
  at least 7 panels with `D>0`, cond2 = `median(D) > u` strictly; SUPPORTED iff both hold in every
  replicate, else REJECTED with reasons naming replicate and condition.
- **Toy F1 table.** Per panel i=1..8: cyl-init 0.1, cyl-final 0.5+0.01i, sq-init 0.1, sq-final
  0.12. Then `D_i = 0.40+0.01i-0.02 = 0.39..0.46` (all positive), `median D = 0.425`. The cell
  spreads: cyl-final differs by 0.01 steps, so `q95{|S_i-S_j|}` = 0.06; other cells are constant
  so `u = 0.06`. cond1 (8 >= 7) and cond2 (0.425 > 0.06) hold, so 3 such replicates give
  SUPPORTED. If one replicate had only 6 positive panels: REJECTED (cond1). If `median D == u`
  exactly: REJECTED (strict). If any gate failed: INCONCLUSIVE regardless of D.
- **Delta-geom** (`geometry.py`). Inputs are `[M, M]` distance matrices; Spearman over `i<j`;
  `all = rho(dA,dB32) - rho(dA,dB1)`; same-last-symbol restricts to pairs with equal `w_32`;
  fewer than 200 such pairs gives `None` and `status_same="inconclusive"`. Because
  `b1 = r_{w32}` depends on `w_32` only, `dB1` is identically 0 on those pairs; a constant `dB1`
  term counts as 0, so the restricted value is `rho(dA,dB32)` (D-031). A non-finite restricted
  value (e.g. constant `dA`) gives `None` / inconclusive, never NaN.
- **Baselines** (`baselines.py`, `SpaceBuilder.baseline`). R0: step-0 activations (hook default
  `resid_post_3`). R1: the `embed` hook of the final checkpoint at position 32; positional
  embedding is a constant shift at a fixed position, so Euclidean distances equal
  token-embedding distances. R2 / R3 are labelled process-level (they use E, T, pi, the same
  knowledge as the oracle): `phi` = spectral embedding of `M = E^T diag(pi) T E` (symmetrised),
  normalised Laplacian `L = I - D^-1/2 M D^-1/2`, eigenvectors of the `k` smallest eigenvalues
  excluding the trivial one, scaled by `D^-1/2` (`k = 12` by default, `refs["k"]`);
  R2 = `1/2[phi(w_32)+phi(w_31)]`, R3 = mean of `phi(w_t)`, t=1..32. Tokens come from the
  `ObservationSet` joined to the `HistoryIndex` by `sequence_id`; all histories need `end == 32`.
  If R2 / R3 show `D>0` of similar size, F1 under O is explained by simple mixing.
- **Activations**. `SpaceBuilder.activations` takes the panel's ids from the ActivationSet's
  parent `HistoryIndex`; the set may cover only some panels but must contain all ids of the panel.
- **Checkpoint-order null** (`dynamics.py`). `stat` = share of total `|dS|` in the first
  `ceil((n-1)/3)` consecutive differences; `p = (1+#{perm >= obs})/(1+n_perm)`; zero total gives
  `nan` and `p=1`. Descriptive only. `Dynamics.curves` is not implemented.
- **LayerSweep**. `S_H1` (Euclidean, via `ph_summary`) per hook plus `concat`.

## Part (d) logic
Readout-geometry helpers (`readout.py`, wave WX4), all float64.
- `ln_gauge_free`: row-wise LayerNorm without gamma/beta, `u = (z - mean(z)) / sqrt(var(z)+eps)`
  (ddof 0). Invariant to per-row shifts, and to positive scaling when `eps = 0`.
- Why the split is exact: with no unembedding bias, `logits = LN_f(z) W_U^T = u A + beta W_U^T`
  where `A = diag(gamma) W_U^T` (`d x V`) and `beta` is the LayerNorm shift. `readout_projector`
  returns `P = Q_r Q_r^T`, the orthogonal projector onto `range(A)` (thin SVD, singular values
  above `tol = max(d,V) * eps * sigma_max`, the `matrix_rank` convention), so `(I - P) A = 0`.
  Hence `u A = u P A + u (I - P) A = u P A`: only `U_visible = u P` reaches the logits, and
  `U_null = u (I - P)` (dimension at least `d - V`) is invisible to the next-token output.
  `split_readout` is therefore exact, up to float rounding, and the two parts are orthogonal
  row by row because `P` is symmetric idempotent.
- `predictive_pointset`: max-subtracted softmax of the logits as a Hellinger `PointSet`.
- Edge cases: `A = 0` gives `P = 0`; zero entries in `gamma` or duplicate rows of `W_U` lower the
  rank (and `trace(P)`); a zero-variance row with `eps = 0` raises `NUMERICAL_FAILURE`.

## Data
`PointSet(space, X, D, ids, metric)` (frozen); `SigmaRow`, `SigmaDecision` (frozen);
`MetricRecords` output of the table. No artifacts are written here.

## Public API
`PointSet, SpaceBuilder, SigmaRow, SigmaDecision, SigmaCalibrator, DiscriminabilityTable,
ph_summary, require_same_ids, ln_gauge_free, readout_projector, split_readout,
predictive_pointset`.

## How to test
`.venv\Scripts\python.exe -m pytest tests/analysis -q`; `python tools/check_imports.py`;
`python tools/check_file_sizes.py`.
