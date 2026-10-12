# `process`

## Purpose

Builds the two halves of the hidden Markov model **separately**: the transition kernel `T` with `pi` (`TransitionSpec`), and the emission matrix `E` (`EmissionSpec`). The emission builder never receives `T`, and the transition builder never receives `E`. It does not choose sigma (that is `analysis` S2).

## Logic

**Transition (RESEARCH_SUMMARY §3).** With adjacency `A` from `world.edges`, `deg = A 1`, `D_max = max deg`:
`T_ij = (1 - p_stay)/D_max` for neighbours, `T_ii = 1 - deg(i)(1 - p_stay)/D_max`, `pi = 1/N`.
`T` is symmetric, so rows and columns sum to 1 and `pi T = pi`. The support check (edges plus diagonal) runs at build time because contracts cannot see the world (D-011). State order is checked first (`coords[x*dims[1]+y] == (x, y)`, else `STATE_ORDER_MISMATCH`).

**Overlap O (§4).** `E[z, j] = softmax_j(-d(z, c_j)^2 / 2 sigma^2)`, float64, via `logsumexp`, no truncation. `d` is the flat distance from the chart coordinates of `z` to the (non-vertex) center, with the x difference wrapped to `min(|dx| mod P, P - |dx| mod P)`, `P = dims[0]`, on the cylinder. `metric="graph"` uses the Manhattan analogue (the graph geodesic extended to points). Centers: `GridCenters` gives `c_ab = (0.5+2a, 0.5+2b)`, `j = a*k + b`, `k = sqrt(V)`; a center outside `[0, dims-1]` raises `INVALID_SIGMA`. Centers are world-scoped (`SeedTree(WORLD_SCOPE_MASTER)`), so they never vary by replicate.

**Symbol names.** `symbol_perm[j]` is the public id of center `j`: `E_public[:, symbol_perm[j]] = E_centers[:, j]`, drawn from `rng_tree.generator("symbol_names", family, rng_tree.master)`. `EmissionSpec.centers[j]` is center `j` in generation order, so it pairs with `symbol_perm`. Renaming permutes columns only; every scalar diagnostic is unchanged and `p_w` is permuted.

**Product structure.** With `E4 = E_centers.reshape(n0, n1, k, k)`, `Ex = sum_{y,b} E4 / n1`, `Ey = sum_{x,a} E4 / n0`; `factorizes` is `max|E4 - Ex Ey| < 1e-12`. It is computed numerically, in center order, for every mode (False if the shape does not admit the reshape).

**Axis-permuted P.** `sx`, `sy` are drawn from `SeedTree(WORLD_SCOPE_MASTER = 0).generator("axis_permutation", family)` (D-012): per world, **not** per replicate. `state_perm[x*n1 + y] = sx[x]*n1 + sy[y]` and `E_P[z] = E_O[state_perm[z]]`, i.e. `E_P[(x,y)] = E_O[(sx(x), sy(y))]`. P reuses O's symbol names for the same replicate. Row multiset, `p_w`, `H(W|Z)` and the factorisation are preserved because permuting rows of a product matrix by a product permutation keeps it a product. The row multiset is verified at build time. `FullPermuted` (extension) permutes all N states and breaks the product.

**N / U.** `E = 1/V`; `E = I` renamed by `symbol_perm` (needs `V = N`).

**Diagnostics** (uniform `pi`, natural log): `p_w = pi E`, `H_W`, `H_W_given_Z = sum pi_z H(E[z])`, `coverage_radius = max_z min_j d(z, c_j)`, `row_entropy_quantiles` at 0, .25, .5, .75, 1, and `factorizes`. For P the coverage radius is the source's. For N it is the world diameter and for U it is 0 (no centers).

**Errors.** `NONSTOCHASTIC` (`illegal_support`, `row_multiset`, and rows/symmetry via contracts), `STATIONARITY_FAILURE`, `INVALID_SIGMA` (sigma not > 0, center outside chart, `dead_symbol` when some `p_w < 1e-4`), `STATE_ORDER_MISMATCH`, `INVALID_CONFIG`.

### Worked example, n = 3 square (ids `x*3+y`, `p_stay = 0.2`, `D_max = 4`, step `(1-0.2)/4 = 0.2`)

| vertex | id | deg | `T_ii` | neighbours (each 0.2) |
|---|---|---|---|---|
| corner (0,0) | 0 | 2 | 1 - 2(0.2) = 0.6 | 1, 3 |
| edge (0,1) | 1 | 3 | 1 - 3(0.2) = 0.4 | 0, 2, 4 |
| interior (1,1) | 4 | 4 | 1 - 4(0.2) = 0.2 | 1, 3, 5, 7 |

Each row sums to 1 (0.6+0.2+0.2, 0.4+3(0.2), 0.2+4(0.2)). On the 3x3 cylinder (x periodic) there is no corner: rows with `y = 0` or `2` have `T_ii = 0.4`, and `x = 0` and `x = 2` are neighbours (0.2).

Axis-wise permutation with `sx = (1, 2, 0)`, `sy = (2, 0, 1)`: state `(x, y)` takes the row of `(sx(x), sy(y))`, so `state_perm = [5, 3, 4, 8, 6, 7, 2, 0, 1]`. For example `E_P[(0,0)] = E_O[(1,2)]` (id 5) and `E_P[(2,1)] = E_O[(0,0)]` (id 0). In production, `sx`, `sy` are the seeded draws above.

## Data

Reads `WorldSpec` (consumer `process`). Writes `TransitionSpec` and `EmissionSpec` with parent = the world id. The emission artifact config is the `EmissionConfig` fields plus `replicate` (master seed) and, for world-scoped modes, `world_scope_master`. `seed_map` holds the issued seeds and the world-scoped seed of the centers.

## Public API

`TransitionConfig`, `TransitionBuilder`, `CenterStrategy`, `GridCenters`, `FPSCenters`, `CENTER_REGISTRY`, `EmissionConfig`, `EmissionModel`, `OverlapGaussian`, `AxisPermuted`, `FullPermuted`, `Identical`, `Unique`, `EMISSION_REGISTRY`, `ProcessStage` (`run_transition`, `run_emission`). `WORLD_SCOPE_MASTER = 0` lives in `process.emission` (not exported). `FPSCenters` starts at vertex 0 and is deterministic.

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/process -q
```
