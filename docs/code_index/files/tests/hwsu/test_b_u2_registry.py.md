# `tests/hwsu/test_b_u2_registry.py`

- Source: [tests/hwsu/test_b_u2_registry.py](../../../../../tests/hwsu/test_b_u2_registry.py)
- Kind: python
- Lines: 297

## Module docstring

> Author B (job 0223, phase 2): the registry readers with planted defects (protocol 8.2-8.3;
> API_U2 3; DRU-REG). Synthetic stores under tmp_path; history tables are made with the K4b table
> builder (canon32, seq_ids, digest, ...); access hooks record every file open.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 21, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 22, via unique basename)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 5)
- `builtins` (lines 7)
- `copy` (lines 8)
- `hashlib` (lines 9)
- `importlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 28: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 29: `hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](../../tools/hwsu/u2/hwsu_registry.py.md)

### sys.path additions

- line 19: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `INC`
- `REPO`

## Classes and functions

- **function `_r`** [L27-29]: `def _r()`
- **function `_sha`** [L32-33]: `def _sha(b: bytes) -> str`
- **function `_table`** [L36-42]: `def _table(path: Path, seed: int, n: int = 8, split='val', block=0) -> list`
- **function `_stages`** [L45-48]: `def _stages(store: Path, entries: dict) -> None`
- **function `opens`** [L52-77]: `def opens(monkeypatch)` decorators: @pytest.fixture
- **function `_hwsc`** [L80-104]: `def _hwsc(tmp_path, extra=True)` - hwsc-store fixture: u2_hist tables listed in S3/S7 STAGE_COMPLETE, OBS_INVENTORY, plus a
- **function `_first_hist`** [L107-108]: `def _first_hist(c)`
- **test `test_source_hwsc_reads_planted_tables_by_the_k4b_reader`** [L112-117]: `def test_source_hwsc_reads_planted_tables_by_the_k4b_reader(tmp_path)`
- **test `test_source_hwsc_sha_differs_from_stage_complete_entry`** [L120-124]: `def test_source_hwsc_sha_differs_from_stage_complete_entry(tmp_path)`
- **test `test_source_hwsc_missing_listed_file`** [L127-130]: `def test_source_hwsc_missing_listed_file(tmp_path)`
- **test `test_source_hwsc_unlisted_array_file`** [L133-136]: `def test_source_hwsc_unlisted_array_file(tmp_path)`
- **test `test_source_hwsc_digest_column_differs_from_canon32`** [L139-153]: `def test_source_hwsc_digest_column_differs_from_canon32(tmp_path)`
- **test `test_source_hwsc_checkpoint_payload_and_sealed_never_opened`** [L156-161]: `def test_source_hwsc_checkpoint_payload_and_sealed_never_opened(tmp_path, opens)`
- **function `_kreg2`** [L165-174]: `def _kreg2(tmp_path, n=12)`
- **test `test_source_kreg2_c_reads_digest_file`** [L177-181]: `def test_source_kreg2_c_reads_digest_file(tmp_path)`
- **test `test_source_kreg2_c_sha_mismatch_refused`** [L184-187]: `def test_source_kreg2_c_sha_mismatch_refused(tmp_path)`
- **test `test_source_kreg2_c_missing_file_refused`** [L190-193]: `def test_source_kreg2_c_missing_file_refused(tmp_path)`
- **function `_sorted_union`** [L197-199]: `def _sorted_union(n=40, seed=1)`
- **test `test_superset_diagnostic_counts_and_lists_missing`** [L202-207]: `def test_superset_diagnostic_counts_and_lists_missing()`
- **test `test_superset_diagnostic_chunk_size_invariant_and_empty_case`** [L210-216]: `def test_superset_diagnostic_chunk_size_invariant_and_empty_case()`
- **test `test_superset_diagnostic_head_is_capped_at_100`** [L219-223]: `def test_superset_diagnostic_head_is_capped_at_100()`
- **function `_own`** [L227-234]: `def _own(tmp_path, names=('stages/OF/HIST_OF_eval_a1_b0.npz', 'stages/OF/HIST_OF_eval_a2_b0.npz'))`
- **test `test_source_own_u_reads_listed_tables`** [L237-240]: `def test_source_own_u_reads_listed_tables(tmp_path)`
- **test `test_source_own_u_unlisted_history_file_refused`** [L243-246]: `def test_source_own_u_unlisted_history_file_refused(tmp_path)`
- **test `test_source_own_u_sha_mismatch_and_missing_expected_refused`** [L249-255]: `def test_source_own_u_sha_mismatch_and_missing_expected_refused(tmp_path)`
- **test `test_source_own_dry_store_without_obligation_refused`** [L259-261]: `def test_source_own_dry_store_without_obligation_refused(tmp_path)`
- **test `test_source_own_dry_test_root_with_history_file_refused`** [L264-266]: `def test_source_own_dry_test_root_with_history_file_refused(tmp_path)`
- **test `test_source_own_dry_empty_or_array_free_roots_pass`** [L269-273]: `def test_source_own_dry_empty_or_array_free_roots_pass(tmp_path)`
- **test `test_inventory_u_flags_unlisted_top_level_dir_with_history_file`** [L277-281]: `def test_inventory_u_flags_unlisted_top_level_dir_with_history_file(tmp_path)`
- **test `test_inventory_u_table_rows_of_root_table_u2_are_known`** [L284-290]: `def test_inventory_u_table_rows_of_root_table_u2_are_known(tmp_path)`
- **test `test_root_table_u_hwsc_store_is_a_reader_row`** [L293-297]: `def test_root_table_u_hwsc_store_is_a_reader_row()`

