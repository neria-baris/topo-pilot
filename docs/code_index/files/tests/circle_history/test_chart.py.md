# `tests/circle_history/test_chart.py`

- Source: [tests/circle_history/test_chart.py](../../../../../tests/circle_history/test_chart.py)
- Kind: python
- Lines: 374

## Module docstring

> Independent synthetic tests, author A (spec v2.3): chart bar selection, cocycle mapping,
> fit_chart and gauge (TEST_PLAN A8, A9, A10; A13 is in test_chart_arrays.py).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 26, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)
- `ripser` (lines 19)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 11)
- `json` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `ARRAY_FIELDS`
- `CHART_KEYS`
- `CIRCLE_THETA`
- `CIRCLE_X`
- `INF`
- `INT_FIELDS`
- `P`
- `PKG`
- `REPO_ROOT`
- `TWO_PI`

## Classes and functions

- **function `make_cfg`** [L45-50]: `def make_cfg(**overrides)`
- **function `make_ids`** [L53-54]: `def make_ids(n)`
- **function `circle_points`** [L57-61]: `def circle_points(theta)` - Deterministic circle in R^4 with small, symmetry-breaking offsets.
- **function `distance_matrix`** [L64-66]: `def distance_matrix(X)`
- **function `eighth_neighbour`** [L69-70]: `def eighth_neighbour(dist)`
- **function `my_select_bar`** [L73-80]: `def my_select_bar(dgm)`
- **function `edge_index`** [L83-84]: `def edge_index(edges)`
- **function `clique_triangles`** [L87-92]: `def clique_triangles(edges, n)`
- **function `triangle_sums`** [L95-98]: `def triangle_sums(c, edges, triangles)`
- **function `unit_columns`** [L101-102]: `def unit_columns(angle, scale=1.0)`
- **function `circle_chart`** [L110-111]: `def circle_chart()` decorators: @pytest.fixture(scope='module')
- **function `dup_fit`** [L115-120]: `def dup_fit()` decorators: @pytest.fixture(scope='module')
- **test `test_select_h1_bar`** [L136-139]: `def test_select_h1_bar(dgm, expected)` decorators: @pytest.mark.parametrize('dgm, expected', [([[0.0, 0.5], [0.25, 1.5], [0.125, 0.25]], 1), ([[0.5, 1.25], [0.25, 1.0], [0.0, 0.25]], 1), ([[0.5, 1.0], [0.25, 0.75], [0.375, 0.875]], 1), ([[0.25, 1.0], [0.25, 1.0], [0.0, 0.125]], 0), ([[0.0, INF], [0.25, 0.5]], 1), ([[0.5, 0.5], [0.25, 0.375]], 1), ([[0.5, 0.25], [0.0, 0.125]], 1)])
- **test `test_select_h1_bar_none`** [L143-145]: `def test_select_h1_bar_none(dgm)` decorators: @pytest.mark.parametrize('dgm', [[[0.0, INF], [0.5, 0.5]], np.zeros((0, 2))])
- **test `test_cocycle_to_edges_sign_centring_and_unknown_edges`** [L148-159]: `def test_cocycle_to_edges_sign_centring_and_unknown_edges()`
- **test `test_fit_chart_exists`** [L163-172]: `def test_fit_chart_exists(circle_chart)`
- **test `test_fit_chart_bar_radius_and_edges`** [L175-189]: `def test_fit_chart_bar_radius_and_edges(circle_chart)`
- **test `test_fit_chart_cocycle_matches_ripser_rows`** [L192-203]: `def test_fit_chart_cocycle_matches_ripser_rows(circle_chart)`
- **test `test_fit_chart_certificates_explicit`** [L206-217]: `def test_fit_chart_certificates_explicit(circle_chart)`
- **test `test_fit_chart_phi_ascending_up_to_reflection`** [L220-229]: `def test_fit_chart_phi_ascending_up_to_reflection(circle_chart)`
- **test `test_fit_chart_extension_scale_recomputed`** [L232-238]: `def test_fit_chart_extension_scale_recomputed(circle_chart, dup_fit)`
- **test `test_fit_chart_duplicate_counts_at_distance_zero`** [L241-249]: `def test_fit_chart_duplicate_counts_at_distance_zero(dup_fit)`
- **test `test_fit_chart_invalid_inputs`** [L253-269]: `def test_fit_chart_invalid_inputs(case)` decorators: @pytest.mark.parametrize('case', ['unsorted', 'duplicate', 'length', 'few', 'nan', 'inf'])
- **function `hexagon_clusters`** [L272-275]: `def hexagon_clusters(spread)`
- **test `test_fit_chart_zero_bandwidth_unresolved`** [L278-284]: `def test_fit_chart_zero_bandwidth_unresolved()`
- **test `test_fit_chart_spread_clusters_positive_bandwidth`** [L287-291]: `def test_fit_chart_spread_clusters_positive_bandwidth()`
- **function `explicit_c`** [L295-296]: `def explicit_c(phi, m32, s)`
- **test `test_fit_gauge_sign_shift_alignment`** [L300-311]: `def test_fit_gauge_sign_shift_alignment(circle_chart, s0, t0)` decorators: @pytest.mark.parametrize('s0, t0', [(-1, 0.7), (1, -2.0)])
- **test `test_apply_gauge_known_values`** [L314-318]: `def test_apply_gauge_known_values()`
- **test `test_fit_gauge_exact_tie_chooses_plus`** [L321-326]: `def test_fit_gauge_exact_tie_chooses_plus(circle_chart)`
- **test `test_fit_gauge_alignment_zero_unresolved`** [L329-331]: `def test_fit_gauge_alignment_zero_unresolved(circle_chart)`
- **test `test_fit_gauge_invalid_inputs`** [L335-346]: `def test_fit_gauge_invalid_inputs(circle_chart, bad)` decorators: @pytest.mark.parametrize('bad', ['nan', 'inf', 'cols', 'rows'])
- **function `snapshot`** [L349-352]: `def snapshot(c)`
- **function `assert_same`** [L355-359]: `def assert_same(c, snap)`
- **test `test_gauge_isolation_from_validation_arrays`** [L362-374]: `def test_gauge_isolation_from_validation_arrays(circle_chart)`

