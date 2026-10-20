# `tests/world/test_world.py`

- Source: [tests/world/test_world.py](../../../../../tests/world/test_world.py)
- Kind: python
- Lines: 324

## Module docstring

> Independent tests W01-W13 for `topo_pilot.world`, written from SPEC.md / TEST_PLAN.md only.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 10, via package root)
- `from topo_pilot.world import WORLD_REGISTRY, CubicalComplex, FlatQuotientMetric, Identification, QuotientLatticeBuilder, WorldBuilder, WorldConfig, WorldStage, build_world, register_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 6)
- `pytest` (lines 7)

### Standard library

- `__future__` (lines 2)
- `typing` (lines 4)

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

- `PRIMES`

## Classes and functions

- **function `_rank_mod_p`** [L30-46]: `def _rank_mod_p(mat: np.ndarray, p: int) -> int`
- **function `_own_boundary`** [L49-64]: `def _own_boundary(cells: dict[int, np.ndarray], k: int) -> np.ndarray` - Independent cubical boundary: d = sum_i (-1)^i (upper_i - lower_i); edges canonical (lo,hi).
- **function `_own_betti`** [L67-71]: `def _own_betti(cells: dict[int, np.ndarray], p: int) -> tuple[int, ...]`
- **function `_cx`** [L74-75]: `def _cx(spec: WorldSpec) -> CubicalComplex`
- **function `_cfg`** [L78-79]: `def _cfg(family: str, n: int, metric: str = 'flat') -> WorldConfig`
- **function `_vid`** [L82-83]: `def _vid(x: int, y: int, n: int = 12) -> int`
- **function `_assert_metric`** [L86-91]: `def _assert_metric(d: np.ndarray) -> None`
- **function `registered`** [L95-105]: `def registered()` decorators: @pytest.fixture - Register in-test builders under unique names; always clean the registry afterwards.
- **function `_make_builders`** [L108-129]: `def _make_builders(registered)`
- **test `test_w01_boundary_squared_is_zero_over_integers`** [L135-145]: `def test_w01_boundary_squared_is_zero_over_integers(family, n)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder']) @pytest.mark.parametrize('n', [3, 4, 12])
- **test `test_w02_betti_known_answers`** [L151-156]: `def test_w02_betti_known_answers(family, expected, p)` decorators: @pytest.mark.parametrize('family,expected', [('square', (1, 0, 0)), ('cylinder', (1, 1, 0))]) @pytest.mark.parametrize('p', PRIMES)
- **test `test_w03_cell_counts_n12`** [L162-168]: `def test_w03_cell_counts_n12(family, counts, chi)` decorators: @pytest.mark.parametrize('family,counts,chi', [('square', (144, 264, 121), 1), ('cylinder', (144, 276, 132), 0)])
- **test `test_w03_vertex_ids_and_coords`** [L171-176]: `def test_w03_vertex_ids_and_coords()`
- **test `test_w04_graph_cycle_rank_differs_from_surface_betti1`** [L180-183]: `def test_w04_graph_cycle_rank_differs_from_surface_betti1()`
- **test `test_w05_flat_metric_cylinder_known_and_axioms`** [L187-194]: `def test_w05_flat_metric_cylinder_known_and_axioms()`
- **test `test_w05_flat_metric_class_matches_built_dist`** [L197-201]: `def test_w05_flat_metric_class_matches_built_dist()`
- **test `test_w06_flat_vs_graph_sandwich`** [L206-210]: `def test_w06_flat_vs_graph_sandwich(family, registered)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder', '_t_torus', '_t_klein'])
- **test `test_w06_graph_metric_option_is_graph_geodesic`** [L213-218]: `def test_w06_graph_metric_option_is_graph_geodesic()`
- **test `test_w07_betti_invariant_under_vertex_relabelling`** [L223-234]: `def test_w07_betti_invariant_under_vertex_relabelling(family)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder'])
- **test `test_w08_face_repeating_a_vertex_raises_invalid_glue`** [L238-244]: `def test_w08_face_repeating_a_vertex_raises_invalid_glue()`
- **test `test_w09_wrong_expected_betti_raises`** [L248-252]: `def test_w09_wrong_expected_betti_raises(registered)`
- **test `test_w10_registry_dispatch_and_unknown_family`** [L256-276]: `def test_w10_registry_dispatch_and_unknown_family(registered)`
- **test `test_w11_torus_extension`** [L280-289]: `def test_w11_torus_extension(registered)`
- **test `test_w12_klein_extension`** [L292-302]: `def test_w12_klein_extension(registered)`
- **test `test_w13_world_stage_saves_valid_spec_with_stable_id`** [L306-318]: `def test_w13_world_stage_saves_valid_spec_with_stable_id()`
- **test `test_builds_are_deterministic`** [L321-324]: `def test_builds_are_deterministic()`

