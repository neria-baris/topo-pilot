# `tools/x4_circle_history/cochain.py`

- Source: [tools/x4_circle_history/cochain.py](../../../../../tools/x4_circle_history/cochain.py)
- Kind: python
- Lines: 250

## Module docstring

> Integer cochains on the Vietoris-Rips 1- and 2-skeleton (API.md, cochain.py).

## Imports

### Internal (repo files)

- `from errors import Invalid, Unresolved` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 22, via same directory)

### External (third-party)

- `numpy` (lines 21)
- `scipy` (lines 23, 24, 25)

### Standard library

- `__future__` (lines 14)
- `collections` (lines 19)
- `math` (lines 16)
- `time` (lines 17)
- `warnings` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 36, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 32, import)
- [tests/c1prime/test_a_chart_lcc512.py](../../tests/c1prime/test_a_chart_lcc512.py.md) (line 34, import)
- [tests/circle_history/test_cochain.py](../../tests/circle_history/test_cochain.py.md) (line 24, import)
- [tests/circle_history/test_cochain_chart_v24.py](../../tests/circle_history/test_cochain_chart_v24.py.md) (line 32, import)
- [tests/circle_history/test_cochain_lift.py](../../tests/circle_history/test_cochain_lift.py.md) (line 35, import)
- [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 15, import)
- [tools/chart_diag/chart_diag.py](../chart_diag/chart_diag.py.md) (line 33, import)
- [tools/x4_circle_history/chart.py](chart.py.md) (line 17, import)

## Top-level constants

- `HIGHS_PINNED`

## Classes and functions

- **function `edge_list`** [L28-35]: `def edge_list(D, radius: float) -> np.ndarray` - All i < j with D[i, j] <= radius, lexicographic order; int64 [E, 2].
- **function `triangle_system`** [L38-60]: `def triangle_system(edges, n: int) -> tuple[csr_matrix, np.ndarray]` - D1 (int64 sparse [T, E]) and triangles (int64 [T, 3]) of the clique 2-skeleton.
- **function `_edge_values`** [L63-64]: `def _edge_values(values, edges) -> dict`
- **function `check_closure`** [L67-72]: `def check_closure(alpha, edges, triangles) -> None` - Invalid unless alpha(j,k) - alpha(i,k) + alpha(i,j) == 0 for every triangle.
- **function `check_congruence`** [L75-79]: `def check_congruence(alpha, a, p: int) -> None` - Invalid unless alpha == a (mod p) on every edge.
- **function `_milp_correction`** [L85-118]: `def _milp_correction(D1, b, bound, cfg, remaining_s)` - One bounded zero-objective feasibility MILP; HiGHS pinned to one thread (fail closed).
- **function `_local_passes`** [L121-137]: `def _local_passes(z, edges, n, cfg, over_cap)`
- **function `integer_lift`** [L140-202]: `def integer_lift(a, D1, edges, triangles, n, cfg, guard=None, clock=time.process_time)` - Exact integer lift alpha = a - p z of a mod-p cocycle a (API.md integer_lift).
- **function `primitive_class`** [L205-235]: `def primitive_class(alpha, edges, triangles, n, p)` - Primitive integer class beta with alpha = g*beta + delta q (API.md primitive_class).
- **function `smooth_phase`** [L238-250]: `def smooth_phase(beta, edges, n)` - Least squares f (f[0] = 0) of ||beta + B f||; phi = 2 pi f mod 2 pi (API.md).

