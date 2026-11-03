# `tests/hwsg/test_b_streams.py`

- Source: [tests/hwsg/test_b_streams.py](../../../../../tests/hwsg/test_b_streams.py)
- Kind: python
- Lines: 128

## Module docstring

> Author B: streams carry the world key; seeds; disjointness (protocol 2.4, G4, KG2, DRG4).

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, TAGS, mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 12, via same directory)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root) (inside a function)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 18, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 8)
- `pytest` (lines 9)

### Standard library

- `__future__` (lines 2)
- `importlib` (lines 4)
- `pathlib` (lines 6)
- `sys` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 31: `hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md)
- `import_module` line 45: `hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md)
- `import_module` line 60: `hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md)
- `import_module` line 71: `hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md)
- `import_module` line 82: `hwsc_data` -> [tools/hwsc/hwsc_data.py](../../tools/hwsc/hwsc_data.py.md)

### sys.path additions

- line 11: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `_lib`** [L15-19]: `def _lib()`
- **function `_draw`** [L22-23]: `def _draw(g, n=8)`
- **test `test_train_dev_generators_carry_world_key`** [L27-37]: `def test_train_dev_generators_carry_world_key(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_block_generators_and_ids`** [L41-54]: `def test_block_generators_and_ids(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_train_dev_sequence_ids_follow_scope_role_master`** [L57-66]: `def test_train_dev_sequence_ids_follow_scope_role_master()`
- **test `test_cal_draws_differ_across_worlds_and_from_stage_c`** [L69-77]: `def test_cal_draws_differ_across_worlds_and_from_stage_c()`
- **test `test_lgate_cal_val_id_sets_pairwise_disjoint_across_worlds`** [L80-91]: `def test_lgate_cal_val_id_sets_pairwise_disjoint_across_worlds()`
- **test `test_planted_shared_sigma_pair_collides_under_sigma_only_tags`** [L94-104]: `def test_planted_shared_sigma_pair_collides_under_sigma_only_tags()`
- **test `test_seeds_masters_and_run_keys_equal_contract`** [L108-119]: `def test_seeds_masters_and_run_keys_equal_contract(tag)` decorators: @pytest.mark.parametrize('tag', TAGS)
- **test `test_dry_seeds_and_masters_do_not_touch_real_ones`** [L122-128]: `def test_dry_seeds_and_masters_do_not_touch_real_ones()`

