# `tests/contracts/test_store.py`

- Source: [tests/contracts/test_store.py](../../../../../tests/contracts/test_store.py)
- Kind: python
- Lines: 342

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 9, via package root)
- `from topo_pilot.contracts import testing` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 5)
- `pytest` (lines 6)

### Standard library

- `collections` (lines 3)
- `dataclasses` (lines 1)
- `json` (lines 2)

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

- `ALL_TYPES`
- `CONSUMER`

## Classes and functions

- **function `_norm`** [L18-27]: `def _norm(v)`
- **function `_same_array`** [L30-34]: `def _same_array(a, b, where)`
- **function `assert_same`** [L37-52]: `def assert_same(a, b)`
- **function `_snapshot`** [L55-57]: `def _snapshot(root)`
- **function `_save`** [L60-62]: `def _save(store, art, cfg=None, parents=())`
- **function `_dir`** [L65-66]: `def _dir(root, art_type, aid)`
- **function `_failure`** [L69-73]: `def _failure(fn, code)`
- **test `test_C04_all_16_classes_covered`** [L83-90]: `def test_C04_all_16_classes_covered(builders)`
- **test `test_C04_roundtrip_memory`** [L94-106]: `def test_C04_roundtrip_memory(name, builders)` decorators: @pytest.mark.parametrize('name', ALL_TYPES)
- **test `test_C04_roundtrip_localfs`** [L110-129]: `def test_C04_roundtrip_localfs(name, builders, fs_store)` decorators: @pytest.mark.parametrize('name', ALL_TYPES)
- **test `test_C04_find_filters_by_config`** [L132-138]: `def test_C04_find_filters_by_config(builders)`
- **test `test_C04_save_validates_first`** [L141-145]: `def test_C04_save_validates_first(builders)`
- **test `test_C05_second_save_is_noop`** [L149-157]: `def test_C05_second_save_is_noop(builders, fs_store)`
- **test `test_C05_same_id_different_content_is_checksum_mismatch`** [L160-167]: `def test_C05_same_id_different_content_is_checksum_mismatch(builders)`
- **function `_tamper_rewrite`** [L170-174]: `def _tamper_rewrite(path)`
- **function `_tamper_flip`** [L177-180]: `def _tamper_flip(path)`
- **test `test_C05_tampered_payload_detected`** [L184-191]: `def test_C05_tampered_payload_detected(tamper, builders, fs_store)` decorators: @pytest.mark.parametrize('tamper', [_tamper_rewrite, _tamper_flip], ids=['rewrite', 'flip'])
- **test `test_C05_tampered_checkpoint_blob_detected`** [L194-200]: `def test_C05_tampered_checkpoint_blob_detected(builders, fs_store)`
- **function `_edit_meta`** [L204-208]: `def _edit_meta(root, art_type, aid, **changes)`
- **test `test_C06_incomplete_refused`** [L211-216]: `def test_C06_incomplete_refused(builders, fs_store)`
- **test `test_C06_unknown_id_is_missing`** [L219-224]: `def test_C06_unknown_id_is_missing(fs_store)`
- **test `test_C07_schema_version`** [L227-235]: `def test_C07_schema_version(builders, fs_store)`
- **test `test_C08_learner_cannot_load_evalsidecar`** [L239-244]: `def test_C08_learner_cannot_load_evalsidecar(builders)`
- **test `test_C08_policy_checked_before_existence`** [L247-249]: `def test_C08_policy_checked_before_existence()`
- **function `_allowed`** [L252-258]: `def _allowed(art_type, consumer)`
- **test `test_C08_default_policy_table`** [L261-278]: `def test_C08_default_policy_table()`
- **test `test_C08_custom_policy`** [L281-288]: `def test_C08_custom_policy()`
- **function `_chain`** [L292-295]: `def _chain(store, builders)`
- **test `test_C12_missing_parent_on_save`** [L298-301]: `def test_C12_missing_parent_on_save(builders)`
- **test `test_C12_bundle_roundtrip`** [L304-320]: `def test_C12_bundle_roundtrip(builders, tmp_path)`
- **test `test_C12_bundle_into_memory_store`** [L323-329]: `def test_C12_bundle_into_memory_store(builders, tmp_path)`
- **test `test_C12_bundle_without_parents_needs_parents`** [L332-342]: `def test_C12_bundle_without_parents_needs_parents(builders, tmp_path)`

