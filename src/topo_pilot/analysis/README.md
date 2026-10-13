# analysis (part a, wave W2)

## Purpose
Project-aware analysis. Part (a) builds the reference comparison spaces on the same histories,
applies the pre-registered sigma rule, and computes the discriminability table (S per space).
Parts (b) and (c) (F1 rule, Delta-geom, baselines, dynamics, sensitivity) are not implemented yet.
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

## Data
`PointSet(space, X, D, ids, metric)` (frozen); `SigmaRow`, `SigmaDecision` (frozen);
`MetricRecords` output of the table. No artifacts are written here.

## Public API
`PointSet, SpaceBuilder, SigmaRow, SigmaDecision, SigmaCalibrator, DiscriminabilityTable,
ph_summary, require_same_ids`.

## How to test
`.venv\Scripts\python.exe -m pytest tests/analysis -q`; `python tools/check_imports.py`;
`python tools/check_file_sizes.py`.
