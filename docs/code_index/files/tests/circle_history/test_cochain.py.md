# `tests/circle_history/test_cochain.py`

- Source: [tests/circle_history/test_cochain.py](../../../../../tests/circle_history/test_cochain.py)
- Kind: python
- Lines: 267

## Module docstring

> Independent synthetic tests, author A (spec v2.3): cochain complexes, explicit checks,
> primitive class and smoothing (TEST_PLAN A1, A3, A6, A7).

## Imports

### Internal (repo files)

- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 24, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 25, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)
- `scipy` (lines 17)

### Standard library

- `__future__` (lines 8)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `C4_EDGES`
- `EXPECTED_CHART_CFG`
- `K4_EDGES`
- `K4_TRIS`
- `NO_TRIANGLES`
- `P`
- `PKG`
- `REPO_ROOT`
- `TWO_PI`

## Classes and functions

- **function `as_int`** [L41-42]: `def as_int(values)`
- **function `edge_index`** [L50-51]: `def edge_index(edges)`
- **function `triangle_sums`** [L54-59]: `def triangle_sums(c, edges, triangles)` - Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints.
- **function `coboundary`** [L62-63]: `def coboundary(f, edges)`
- **test `test_contract_chart_keys_match_job_values`** [L66-70]: `def test_contract_chart_keys_match_job_values()`
- **function `hand_distance_matrix`** [L74-81]: `def hand_distance_matrix()`
- **test `test_edge_list_hand_graph_inclusive_and_lexicographic`** [L84-91]: `def test_edge_list_hand_graph_inclusive_and_lexicographic()`
- **test `test_triangle_system_hand_graph_rows`** [L94-109]: `def test_triangle_system_hand_graph_rows()`
- **test `test_triangle_system_k4_and_tree`** [L112-124]: `def test_triangle_system_k4_and_tree()`
- **test `test_check_closure_explicit`** [L128-143]: `def test_check_closure_explicit()`
- **test `test_check_congruence_explicit`** [L146-152]: `def test_check_congruence_explicit()`
- **function `primitive`** [L156-158]: `def primitive(alpha, edges, n, triangles=NO_TRIANGLES)`
- **function `assert_decomposition`** [L161-163]: `def assert_decomposition(alpha, edges, beta, q, g)`
- **test `test_primitive_class_cycle_known_period`** [L166-176]: `def test_primitive_class_cycle_known_period()`
- **test `test_primitive_class_bfs_not_dfs_order`** [L179-188]: `def test_primitive_class_bfs_not_dfs_order()`
- **test `test_primitive_class_gcd_of_two_periods`** [L191-200]: `def test_primitive_class_gcd_of_two_periods()`
- **test `test_primitive_class_unresolved_cases`** [L203-213]: `def test_primitive_class_unresolved_cases()`
- **test `test_primitive_class_non_closed_alpha_invalid`** [L216-221]: `def test_primitive_class_non_closed_alpha_invalid()`
- **function `assert_phases`** [L225-230]: `def assert_phases(phi, expected, tol=1e-09)`
- **function `smooth`** [L233-237]: `def smooth(beta, edges, n)`
- **test `test_smooth_phase_cycle_four`** [L240-247]: `def test_smooth_phase_cycle_four()`
- **test `test_smooth_phase_cycle_five_winding_two`** [L250-254]: `def test_smooth_phase_cycle_five_winding_two()`
- **test `test_smooth_phase_path_is_exact`** [L257-261]: `def test_smooth_phase_path_is_exact()`

