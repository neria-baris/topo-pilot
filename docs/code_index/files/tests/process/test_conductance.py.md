# `tests/process/test_conductance.py`

- Source: [tests/process/test_conductance.py](../../../../../tests/process/test_conductance.py)
- Kind: python
- Lines: 258

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, MemoryBackend, StageFailure, TransitionSpec, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `from topo_pilot.contracts.testing import tiny_world_spec` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 26, via package root)
- `from topo_pilot.process import ConductanceConfig, ProcessStage, TransitionBuilder, TransitionConfig, conductance_kernel, warp_profile` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 27, via package root)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 35, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)
- `scipy` (lines 16)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)
- `json` (lines 11)
- `math` (lines 12)

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

- `R12`

## Classes and functions

- **function `world`** [L43-45]: `def world()` decorators: @pytest.fixture(scope='module') - 12 x 12 cylinder from the world package (state id = x * 12 + y).
- **function `k020`** [L49-50]: `def k020(world)` decorators: @pytest.fixture(scope='module')
- **function `_lh`** [L53-54]: `def _lh(y: int, a: float, ny: int) -> float`
- **function `_edge_classes`** [L57-62]: `def _edge_classes(world)`
- **test `test_warp_profile_hand_values_12x12`** [L68-81]: `def test_warp_profile_hand_values_12x12()`
- **test `test_warp_profile_exact_mid_row_when_ny_odd`** [L84-91]: `def test_warp_profile_exact_mid_row_when_ny_odd()`
- **test `test_warp_profile_a0_is_flat`** [L94-97]: `def test_warp_profile_a0_is_flat()`
- **test `test_warp_profile_rejects_abs_a_ge_1`** [L101-104]: `def test_warp_profile_rejects_abs_a_ge_1(a)` decorators: @pytest.mark.parametrize('a', [1.0, -1.0, 1.5, -3.0])
- **test `test_warp_profile_rejects_ny_below_2`** [L107-110]: `def test_warp_profile_rejects_ny_below_2()`
- **test `test_conductance_config_defaults`** [L113-117]: `def test_conductance_config_defaults()`
- **test `test_a0_equals_max_degree_lazy_walk`** [L124-131]: `def test_a0_equals_max_degree_lazy_walk(source, world)` decorators: @pytest.mark.parametrize('source', ['build_world', 'tiny_world_spec'])
- **test `test_a020_kernel_validity`** [L137-150]: `def test_a020_kernel_validity(world, k020)`
- **test `test_a020_support_only_edges_and_diagonal`** [L153-161]: `def test_a020_support_only_edges_and_diagonal(world, k020)`
- **test `test_a020_connected`** [L164-168]: `def test_a020_connected(k020)`
- **test `test_a020_c_max_closed_form_and_entries`** [L171-182]: `def test_a020_c_max_closed_form_and_entries(world, k020)`
- **test `test_edge_classification_counts`** [L185-193]: `def test_edge_classification_counts(world, k020)`
- **test `test_wrap_edges_carry_horizontal_conductance`** [L196-201]: `def test_wrap_edges_carry_horizontal_conductance(world, k020)`
- **test `test_metadata_matches_warp_profile`** [L204-213]: `def test_metadata_matches_warp_profile(k020)`
- **test `test_kernel_rejects_bad_state_order`** [L216-232]: `def test_kernel_rejects_bad_state_order()`
- **test `test_kernel_rejects_abs_a_ge_1`** [L235-237]: `def test_kernel_rejects_abs_a_ge_1(world)`
- **test `test_process_stage_saves_with_world_parent`** [L243-258]: `def test_process_stage_saves_with_world_parent(world, k020)`

