# `tests/process/test_overlap.py`

- Source: [tests/process/test_overlap.py](../../../../../tests/process/test_overlap.py)
- Kind: python
- Lines: 160

## Module docstring

> P04, P05, P09, P10 (and the dead-symbol / sigma error paths) for the overlap emission.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.process import CENTER_REGISTRY, CenterStrategy, EmissionConfig, GridCenters, OverlapGaussian` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 11, via package root)
- `from topo_pilot.process._diagnostics import check_symbols_alive` -> [src/topo_pilot/process/_diagnostics.py](../../src/topo_pilot/process/_diagnostics.py.md) (line 18, via package root)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 147)
- `math` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `_build`** [L23-25]: `def _build(world, seed=1729, **kw)`
- **function `_centers`** [L28-29]: `def _centers()`
- **test `test_P04_rows_sum_to_one_and_direct_formula_square`** [L32-43]: `def test_P04_rows_sum_to_one_and_direct_formula_square(square12)`
- **test `test_P04_cylinder_x_distance_is_periodic`** [L46-56]: `def test_P04_cylinder_x_distance_is_periodic(cylinder12, square12)`
- **test `test_logsumexp_no_underflow_nan_with_tiny_sigma`** [L59-62]: `def test_logsumexp_no_underflow_nan_with_tiny_sigma(square12)`
- **test `test_P05_factorizes_on_core_worlds`** [L66-76]: `def test_P05_factorizes_on_core_worlds(family, square12, cylinder12)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder'])
- **test `test_diagnostics_values`** [L79-86]: `def test_diagnostics_values(square12)`
- **test `test_P09_symbol_names_permute_columns_only`** [L89-99]: `def test_P09_symbol_names_permute_columns_only(square12)`
- **test `test_symbol_perm_uses_replicate_seed_stream`** [L102-107]: `def test_symbol_perm_uses_replicate_seed_stream(square12)`
- **test `test_P10_nonpositive_sigma_raises`** [L111-114]: `def test_P10_nonpositive_sigma_raises(square12, sigma)` decorators: @pytest.mark.parametrize('sigma', [0.0, -1.0, None, float('nan')])
- **test `test_P10_center_outside_chart_raises`** [L117-123]: `def test_P10_center_outside_chart_raises(square3)`
- **test `test_P10_dead_symbol_helper_and_constructed_build`** [L126-143]: `def test_P10_dead_symbol_helper_and_constructed_build(square12, monkeypatch)`
- **test `test_error_state_order_and_unknown_strategy`** [L146-154]: `def test_error_state_order_and_unknown_strategy(square12)`
- **test `test_graph_metric_uses_manhattan`** [L157-160]: `def test_graph_metric_uses_manhattan(square12)`

