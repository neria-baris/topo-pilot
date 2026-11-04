# `tests/hwsg/test_b_registry.py`

- Source: [tests/hwsg/test_b_registry.py](../../../../../tests/hwsg/test_b_registry.py)
- Kind: python
- Lines: 275

## Module docstring

> Author B: registry fixtures, class-to-reader table, inventory fail-closed (protocol 6, N6, DRG9).

## Imports

### Internal (repo files)

- `from test_b_common import CONTRACT, expect_fail, is_incomplete, mod` -> [tests/hwsg/test_b_common.py](test_b_common.py.md) (line 16, via same directory)

### External (third-party)

- `numpy` (lines 12)
- `pytest` (lines 13)

### Standard library

- `__future__` (lines 2)
- `builtins` (lines 4)
- `hashlib` (lines 5)
- `json` (lines 6)
- `os` (lines 7)
- `pathlib` (lines 10)
- `sys` (lines 8)
- `time` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 27: `k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md)
- `__import__` line 138: `stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md)

### sys.path additions

- line 15: `str(Path(__file__).resolve().parent)` -> `tests/hwsg`

## Imported by

- none

## Top-level constants

- `SCHEMA`

## Classes and functions

- **function `_sha`** [L21-22]: `def _sha(p)`
- **function `_table`** [L25-34]: `def _table(path, seed, n=6)`
- **function `_entry`** [L37-39]: `def _entry(store, f, cls, reader)`
- **function `_store`** [L42-53]: `def _store(tmp_path, name='s-store')`
- **function `_write`** [L56-57]: `def _write(store, obl, name='REGISTRY_OBLIGATION.json')`
- **test `test_class_to_reader_table_matches_contract`** [L60-66]: `def test_class_to_reader_table_matches_contract()`
- **test `test_matching_listing_passes_and_returns_digests`** [L69-75]: `def test_matching_listing_passes_and_returns_digests(tmp_path)`
- **test `test_new_missing_resized_array_is_incomplete`** [L78-89]: `def test_new_missing_resized_array_is_incomplete(tmp_path)`
- **test `test_array_listing_includes_subfolders_and_is_stat_only`** [L92-107]: `def test_array_listing_includes_subfolders_and_is_stat_only(tmp_path, monkeypatch)`
- **test `test_history_sha_mismatch_is_lineage`** [L110-120]: `def test_history_sha_mismatch_is_lineage(tmp_path)`
- **test `test_unknown_class_or_reader_is_incomplete`** [L124-130]: `def test_unknown_class_or_reader_is_incomplete(tmp_path, which)` decorators: @pytest.mark.parametrize('which', ['class', 'reader'])
- **test `test_non_history_is_never_opened`** [L133-151]: `def test_non_history_is_never_opened(tmp_path, monkeypatch)`
- **test `test_metadata_files_listed_separately`** [L154-162]: `def test_metadata_files_listed_separately(tmp_path)`
- **test `test_missing_obligation_is_incomplete`** [L165-175]: `def test_missing_obligation_is_incomplete(tmp_path)`
- **test `test_latest_obligation_by_written_utc`** [L178-188]: `def test_latest_obligation_by_written_utc(tmp_path)`
- **test `test_hwsc_like_store_sealed_never_opened_and_unassigned_array`** [L191-207]: `def test_hwsc_like_store_sealed_never_opened_and_unassigned_array(tmp_path, monkeypatch)`
- **test `test_scratch_unmatched_top_level_dir_is_incomplete`** [L210-217]: `def test_scratch_unmatched_top_level_dir_is_incomplete(tmp_path)`
- **test `test_scratch_to_freeze_row_is_incomplete`** [L220-227]: `def test_scratch_to_freeze_row_is_incomplete(tmp_path)`
- **test `test_root_unlisted_dir_with_history_file_is_incomplete`** [L230-236]: `def test_root_unlisted_dir_with_history_file_is_incomplete(tmp_path)`
- **test `test_cross_world_collision_is_lineage`** [L239-252]: `def test_cross_world_collision_is_lineage(tmp_path)`
- **test `test_recheck_after_root_change_is_incomplete`** [L255-270]: `def test_recheck_after_root_change_is_incomplete(tmp_path)`
- **test `test_all_outputs_under_tmp_path`** [L273-275]: `def test_all_outputs_under_tmp_path(tmp_path)`

