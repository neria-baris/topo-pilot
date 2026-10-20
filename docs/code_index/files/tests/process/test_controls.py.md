# `tests/process/test_controls.py`

- Source: [tests/process/test_controls.py](../../../../../tests/process/test_controls.py)
- Kind: python
- Lines: 186

## Module docstring

> P06, P07, P08, P11, P12 and the ProcessStage I/O round trip.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import EmissionSpec, ErrorCode, SeedTree, StageFailure, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 18, via package root)
- `from topo_pilot.process import EMISSION_REGISTRY, AxisPermuted, EmissionConfig, EmissionModel, FPSCenters, FullPermuted, Identical, OverlapGaussian, ProcessStage, TransitionConfig, Unique` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 19, via package root)
- `from topo_pilot.process._diagnostics import check_row_multiset` -> [src/topo_pilot/process/_diagnostics.py](../../src/topo_pilot/process/_diagnostics.py.md) (line 32, via package root)
- `from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 7)
- `pytest` (lines 8)

### Standard library

- `__future__` (lines 3)
- `inspect` (lines 5)

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

- **function `_o_and_p`** [L38-42]: `def _o_and_p(world, seed=1729, sigma=1.25)`
- **function `_sorted_rows`** [L45-46]: `def _sorted_rows(E)`
- **test `test_P06_axis_permuted_preserves_rows_and_structure`** [L50-63]: `def test_P06_axis_permuted_preserves_rows_and_structure(family, square12, cylinder12)` decorators: @pytest.mark.parametrize('family', ['square', 'cylinder'])
- **test `test_P06_full_permutation_keeps_rows_but_not_product`** [L66-71]: `def test_P06_full_permutation_keeps_rows_but_not_product(square12)`
- **test `test_axis_state_perm_n3_hand_example`** [L74-77]: `def test_axis_state_perm_n3_hand_example()`
- **test `test_P06_row_multiset_check_error_path`** [L80-87]: `def test_P06_row_multiset_check_error_path()`
- **test `test_P07_permutations_depend_on_world_not_replicate`** [L90-99]: `def test_P07_permutations_depend_on_world_not_replicate(square12, cylinder12)`
- **test `test_P08_identical_all_rows_equal`** [L102-107]: `def test_P08_identical_all_rows_equal(square3)`
- **test `test_P08_unique_is_permutation_matrix`** [L110-120]: `def test_P08_unique_is_permutation_matrix(square3)`
- **test `test_P11_emission_builder_does_not_accept_transition`** [L123-131]: `def test_P11_emission_builder_does_not_accept_transition()`
- **test `test_P12_fps_greedy_maxmin_by_hand`** [L134-145]: `def test_P12_fps_greedy_maxmin_by_hand(square3)`
- **test `test_fps_overlap_builds_on_tiny_world`** [L148-153]: `def test_fps_overlap_builds_on_tiny_world(square3)`
- **test `test_stage_round_trip_and_lineage`** [L156-177]: `def test_stage_round_trip_and_lineage(square12)`
- **test `test_stage_unknown_mode`** [L180-186]: `def test_stage_unknown_mode(square12)`

