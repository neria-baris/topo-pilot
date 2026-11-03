# `tests/hwsu/test_b_u2_binding.py`

- Source: [tests/hwsu/test_b_u2_binding.py](../../../../../tests/hwsu/test_b_u2_binding.py)
- Kind: python
- Lines: 246

## Module docstring

> Author B (job 0223, phase 2): stage-C binding and identity (protocol 3.1; API_U2 1.1; DRU8).
> Synthetic hwsc-store fixtures under tmp_path; chart 'files' are random bytes (never np.load-ed).
> The 'real' checks read JSON/hash only (no payload, no blinded path).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 20, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 21, via unique basename)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `hashlib` (lines 8)
- `importlib` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 28: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 29: `hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](../../tools/hwsu/u2/hwsu_model.py.md)

### sys.path additions

- line 18: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `HANDOFF`
- `IDENT`
- `MASTERS`
- `REPO`

## Classes and functions

- **function `_m`** [L27-29]: `def _m()`
- **function `_sha`** [L32-33]: `def _sha(b: bytes) -> str`
- **function `_get`** [L36-37]: `def _get(d, j)`
- **function `_set`** [L40-41]: `def _set(d, j, v)`
- **function `_fail`** [L44-47]: `def _fail(fn, *a, **k)`
- **function `_record`** [L50-54]: `def _record(j, **over)`
- **function `_stage_store`** [L57-75]: `def _stage_store(tmp_path, rec_over=None, stage_sha_over=None)` - hwsc-store fixture with three TRAIN_RECORDs, STAGES.jsonl and a CONTRACT copy.
- **function `_charts`** [L78-99]: `def _charts(tmp_path, bad_gauge=False)`
- **test `test_read_train_record_drops_dev_ce_and_everything_else`** [L103-109]: `def test_read_train_record_drops_dev_ce_and_everything_else(tmp_path)`
- **test `test_read_train_record_dev_ce_dropped_whatever_its_shape`** [L112-118]: `def test_read_train_record_dev_ce_dropped_whatever_its_shape(tmp_path)` - A dev_ce value of any shape (here nested) is dropped; a UTF-8 BOM is accepted.
- **test `test_read_train_record_missing_whitelisted_key_refused`** [L122-127]: `def test_read_train_record_missing_whitelisted_key_refused(tmp_path, drop)` decorators: @pytest.mark.parametrize('drop', ['checkpoint_ids', 'checksums', 'run_key', 'status'])
- **test `test_stage_complete_sha_last_record_wins`** [L131-140]: `def test_stage_complete_sha_last_record_wins(tmp_path)`
- **test `test_identity_c_train_record_differs_from_contract`** [L147-150]: `def test_identity_c_train_record_differs_from_contract(tmp_path)`
- **test `test_identity_c_train_record_differs_from_stage_complete`** [L153-155]: `def test_identity_c_train_record_differs_from_stage_complete(tmp_path)`
- **test `test_identity_c_status_not_complete_refused`** [L158-160]: `def test_identity_c_status_not_complete_refused(tmp_path)`
- **test `test_identity_c_checkpoint_id_differs_from_contract`** [L163-166]: `def test_identity_c_checkpoint_id_differs_from_contract(tmp_path)`
- **test `test_identity_c_excluded_checkpoint_id_refused`** [L169-173]: `def test_identity_c_excluded_checkpoint_id_refused(tmp_path)`
- **test `test_charts_identity_pass_without_np_load`** [L177-185]: `def test_charts_identity_pass_without_np_load(tmp_path, monkeypatch)`
- **test `test_chart_off_by_one_byte_refused`** [L188-194]: `def test_chart_off_by_one_byte_refused(tmp_path)`
- **test `test_gauges_differ_from_contract_refused`** [L197-199]: `def test_gauges_differ_from_contract_refused(tmp_path)`
- **test `test_production_frozen_rehash_mismatch_refused`** [L202-206]: `def test_production_frozen_rehash_mismatch_refused(tmp_path)`
- **test `test_chart_record_hash_differs_from_contract_copy`** [L209-213]: `def test_chart_record_hash_differs_from_contract_copy(tmp_path)`
- **test `test_load_stage_c_requires_one_torch_thread`** [L217-222]: `def test_load_stage_c_requires_one_torch_thread(tmp_path, monkeypatch)`
- **test `test_real_stage_c_hashes_equal_contract`** [L226-246]: `def test_real_stage_c_hashes_equal_contract()`

