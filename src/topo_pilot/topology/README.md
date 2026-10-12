# topology

## Purpose
Generic, model-agnostic toolbox for distances and Vietoris-Rips persistent homology. It receives
arrays and returns arrays, summaries and statuses; it knows nothing about HMMs, worlds or models.
Imports: stdlib, numpy, scipy, ripser, `topo_pilot.contracts` (errors and statuses only).

## Logic
- **Metrics** (`metrics.py`): Euclidean; chord (Euclidean on L2-normalised rows, zero row ->
  `NUMERICAL_FAILURE`, check `zero_vector`); Hellinger `||sqrt p - sqrt q|| / sqrt 2`; sqrt-JS with
  `JS = H((p+q)/2) - (H(p)+H(q))/2`, natural log, `0 log 0 = 0`. Hellinger/JS require non-negative
  rows summing to 1 within 1e-9, else `NUMERICAL_FAILURE`. Outputs are symmetrised with an exactly
  zero diagonal.
- **Deduplication** (`distance.py`): points at distance <= 1e-12 are merged (first occurrence is the
  representative) *before* PH, because zero-length edges would create bars of zero length and
  duplicate vertices and change nothing topologically. `dedup_map[i]` is the row of original point
  `i` in `D`. One surviving point -> status `COLLAPSED`, `scale_s = 0`, S = 0.
- **Scale** `s` = 95th percentile of the positive off-diagonal distances, raw units. Normalisation
  by `s` happens only in `Summaries.S`, so `S` is invariant to rescaling `D` (births and deaths
  scale with `c`, so does `s`).
- **Ripser wrapper** (`persistence.py`): `ripser(D, distance_matrix=True, coeff=p, maxdim, thresh)`.
  `D` is validated (finite, square, symmetric, >= 0, zero diagonal, else `NON_METRIC`). Threshold
  `"auto"` is `max(D)`: every edge is present, so the complex is a full simplex at the end and every
  H1 bar dies by `max(D)`. A finite threshold below that leaves bars open: in dim >= 1 a death of
  inf is flagged `censored = 1` (never dropped) and the result status is `CENSORED`. The H0
  essential bar keeps death = inf with `censored = 0`. A 1-point or all-zero `D` returns only the
  H0 essential bar, status `COLLAPSED`.
- **Timeout**: if `n <= 600`, `maxdim <= 1` and `timeout_s >= 1`, ripser runs in-process (fast path,
  seconds at M = 512; the timeout cannot interrupt it). Otherwise ripser runs in a `spawn`ed
  process (Windows safe) with a pipe and `poll(timeout_s)`; on timeout the worker is terminated and
  the result is status `CENSORED` with the H0 diagram only (from a minimum spanning tree). Worker
  failure or `MemoryError` -> `PH_RESOURCE_LIMIT`. Callers that spawn must sit under the usual
  `if __name__ == "__main__":` guard (pytest does).
- **Landmarks**: only when `cfg.landmarks` is set (needs `maxdim >= 2`); `maxmin_landmarks` is greedy
  farthest-point sampling from an `rng`-chosen start. `diagrams` then starts at point 0 and flags
  `APPROXIMATE`. No k-NN graph distances anywhere.
- **S**: max over finite H_dim bars of `(death - birth)/s`; 0.0 if none. `pi_max` = max death/birth
  over finite bars with birth > 0 (0.0 if none). Betti curve counts `birth <= t < death`.
- **Circular coordinates** (`circular.py`, de Silva-Morozov-Vejdemo-Johansson): Rips persistence
  over `F_p` (p odd prime, default 47) with cocycles; take the finite H1 bar of maximal
  persistence `(b, d)` and its cocycle; set `r = (b + d)/2`; lift cocycle values to integers in
  `(-p/2, p/2]`, zero on edges outside the support; on the graph `{D <= r}` solve the least
  squares `min_f sum (f_j - f_i - alpha_ij)^2` (Laplacian normal equations, minimal-norm); angle
  `2 pi (f mod 1)`. Why it works: `alpha - delta f` is the harmonic representative of the class;
  `f mod 1` is the circle-valued map whose pull-back of the generator is that class. Angles are
  defined up to rotation/reflection. Dense `M x M` solve: fine for M <= ~1000.
- **Shapes**: unit circle, unit disk, Clifford torus (R^4), sphere S^dim, placed in the first
  coordinates of R^ambient; Gaussian noise of std `noise` **per ambient coordinate**. `rng` is
  required (None -> `INVALID_CONFIG`). Null clouds: isotropic `N(0, I)`; covariance-matched via the
  SVD of the centred data (no F x F matrix).

## Data
Pure results: `DistanceResult(D, point_ids, dedup_map, scale_s, status)` and
`DiagramResult(rows [n,4] float64 (dim, birth, death, censored), coeff_p, maxdim, threshold,
library_version, status)`; both frozen. Persisting as `DistanceArtifact` / `Diagrams` is done by
`analysis`. `status` is a `contracts.Status`.

## Public API
`DistanceMetric, Euclidean, Chord, Hellinger, SqrtJS, METRIC_REGISTRY, PHConfig, DistancePipeline,
DistanceResult, PersistenceComputer, DiagramResult, Summaries, NullClouds, SyntheticShapes,
CircularCoordinates` (see `SPEC.md`).

## How to test
`.venv\Scripts\python.exe -m pytest tests/topology -q` (add `-m "topology or slow"` for the slow
items); `python tools/check_imports.py`; `python tools/check_file_sizes.py`.
