# `tests/contracts/test_ids.py`

- Source: [tests/contracts/test_ids.py](../../../../../tests/contracts/test_ids.py)
- Kind: python
- Lines: 141

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SCHEMA_VERSION, ErrorCode, SeedTree, StageFailure, canonical_json, make_artifact_id` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 5)
- `pytest` (lines 6)

### Standard library

- `hashlib` (lines 1)
- `json` (lines 2)
- `random` (lines 3)

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

- `CFG`

## Classes and functions

- **function `_shuffled`** [L22-25]: `def _shuffled(d, rng)`
- **test `test_C01_id_known_answer_and_shape`** [L28-35]: `def test_C01_id_known_answer_and_shape()`
- **test `test_C01_id_independent_of_key_order`** [L38-42]: `def test_C01_id_independent_of_key_order()`
- **test `test_C01_id_independent_of_parent_order_and_container`** [L45-47]: `def test_C01_id_independent_of_parent_order_and_container()`
- **test `test_C02_id_changes_with_each_input`** [L50-66]: `def test_C02_id_changes_with_each_input()`
- **test `test_C03_canonical_json_known_answers`** [L69-80]: `def test_C03_canonical_json_known_answers()`
- **test `test_C03_canonical_json_floats_and_numpy`** [L83-96]: `def test_C03_canonical_json_floats_and_numpy()`
- **test `test_C03_canonical_json_rejects_nonfinite`** [L101-104]: `def test_C03_canonical_json_rejects_nonfinite(bad)` decorators: @pytest.mark.parametrize('bad', [float('nan'), float('inf'), float('-inf'), np.float32('nan'), [1, {'a': float('nan')}], np.array([1.0, np.inf])])
- **function `_ref_seed`** [L107-109]: `def _ref_seed(*a)`
- **test `test_C09_seed_known_answers`** [L112-118]: `def test_C09_seed_known_answers()`
- **test `test_C09_seed_sensitivity`** [L121-125]: `def test_C09_seed_sensitivity()`
- **test `test_C10_generator_streams`** [L128-141]: `def test_C10_generator_streams()`

