# world

## Purpose

Builds latent worlds: states (lattice vertices), the cubical complex that defines the surface (not just the transition graph), gluings, metrics, and exact homology over GF(p). It knows nothing about symbols, sequences, or models. Output is a `WorldSpec` (contracts). Building is deterministic (no RNG).

## Logic

**Vertices and cells.** Vertex `x = (x_0, .., x_{D-1})` has C-order id (`x * dims[1] + y` for D = 2); `coords` holds the float lattice coordinates. A k-cube is determined by a base vertex and a set `S` of k direction axes; its 2^k corners `base + sum_t eps_t e_{S_t}` (eps in {0,1}) are listed in local lexicographic order (first direction axis most significant, i.e. corner index `j` has axis-`t` bit `(j >> (k-1-t)) & 1`). Corners reaching `x_a = n_a` on a glued axis are wrapped: periodic subtracts `n_a`; flipped additionally maps `y_f -> n_f - 1 - y_f`. Each cube is listed once; a repeated vertex or a duplicate cube raises `INVALID_GLUE` (e.g. a periodic axis shorter than 3). Edges are stored canonical `(lo, hi)` and sorted.

**Boundary signs.** For a k-cube `c` with axes `i = 0..k-1`:
`d c = sum_i (-1)^i ( face_{i,1} - face_{i,0} )`, where `face_{i,s}` keeps the corners with axis-i bit `s` (in order). Each facet is matched (by vertex set) to the stored (k-1)-cell; if the facet's vertex order differs from the stored order, the sign is multiplied by the sign of the cube symmetry relating them (axis-permutation sign times `(-1)^{#reflections}`; for edges simply -1 when `(hi, lo)` appears). Hence `d_{k-1} d_k = 0` over Z, which `build_world` checks.

Worked example, n = 3 cylinder (ids 3x+y). The square at base (0,0) is `(0,1,3,4)`:
`d = [3,4] - [0,1] - [1,4] + [0,3]` (a closed loop 0->3->4, 1->4 reversed, 0->1 reversed). The seam square at base (2,0) is `(6,7,0,1)` (x wraps to 0):
`d = [0,1] - [6,7] + [1,7] - [0,6]`; the facets `(7,1)` and `(6,0)` are reversed relative to the canonical edges `(1,7)`, `(0,6)`, which is why their signs are flipped. The loop is 0->1->7->6->0, closed.

**Homology.** `beta_k = n_k - rank_p d_k - rank_p d_{k+1}` with `rank_p` by Gaussian elimination on dense `int64 mod p` (pivots inverted with `pow(a, -1, p)`). `betti(p)` returns `(beta_0..beta_K)`. Core worlds: square (1,0,0), cylinder (1,1,0), for p = 2, 3. The graph cycle rank `E - V + 1` is not beta_1 (square n = 12: 121 vs 0), since 2-cells kill cycles.

**Flat metric (lift-based).** Each glued axis contributes a deck generator, an affine map `x -> a*x + b`: periodic axis i: `b = n_i e_i`; flipped axis i with flip axis f: `b = n_i e_i + (n_f - 1) e_f`, `a_f = -1`. The set `G'` consists of all products of generators with exponents in {-1,0,1} (3^r copies, r = number of glued axes), and `d(p,q) = min_{g in G'} ||p - g(q)||_2`, then symmetrised by `min(d, d^T)`.
Worked example, n = 3 cylinder, p = vertex 0 = (0,0), q = vertex 8 = (2,2). Lifts of q: (2,2) -> distance sqrt(8); (-1,2) (shift by -3 in x) -> sqrt(1+4) = sqrt(5) = 2.236; (5,2) farther. So `dist = sqrt(5)`, while the graph geodesic is 1 + 2 = 3. Sandwich: `dist <= dist_graph + 1e-9` and `dist >= dist_graph / sqrt(D)` (checked in `build_world`, `NON_METRIC`). For n = 12, d((11,y),(0,y)) = 1 and d((0,0),(6,0)) = 6.

**Errors.** unknown family -> `INVALID_CONFIG`; `d d != 0` -> `BETTI_MISMATCH` (`boundary_not_closed`); computed beta != expected -> `BETTI_MISMATCH`; repeated vertex / inconsistent gluing -> `INVALID_GLUE`; asymmetric / nonzero diagonal / triangle violation / disconnected graph geodesic -> `NON_METRIC`.

## Data

Input: `WorldConfig(family, dims=(12,12), metric="flat"|"graph", params)`. Output: `WorldSpec` with `coords [N,D]`, `cells {k: int32[n_k, 2^k]}` (`cells[0]` = 0..N-1), `edges` (= `cells[1]`), `dist` (chosen metric), `dist_graph`, `betti_expected` / `betti_computed` keyed by p in {2,3}, `identifications` (strings such as `"x periodic"`), `metric`. Persisted by `WorldStage` with `config` = the dataclass fields of the config, no parents, empty seed map, consumer `world`.

## Public API

`WorldConfig`, `CubicalComplex` (`boundary_matrix`, `betti`, `euler_characteristic`, `one_skeleton`), `Identification`, `Metric`, `FlatQuotientMetric`, `GraphGeodesicMetric`, `WorldBuilder`, `QuotientLatticeBuilder`, `SquareBuilder`, `CylinderBuilder`, `WORLD_REGISTRY`, `register_world`, `build_world`, `WorldStage`.

Adding a family: subclass `QuotientLatticeBuilder`, set `family`, `expected_betti` and the class attribute `identifications` (tuple of `Identification`), decorate with `@register_world`.

## How to test

```
.venv\Scripts\python.exe -m pytest tests/world -q
.venv\Scripts\python.exe tools/check_imports.py
.venv\Scripts\python.exe tools/check_file_sizes.py
```
