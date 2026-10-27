# `tests/hwsb/test_b_records.py`

- Source: [tests/hwsb/test_b_records.py](../../../../../tests/hwsb/test_b_records.py)
- Kind: python
- Lines: 359

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_records.py`: pause check (section 8.2), study
> ledger (RC-7), AUTH/SCHED rules, store inventory snapshot/diff (section 6.4 rule 1), the G0
> needle classification and search (RC-3, DRB15), FREEZE fields, and the dry-run refusal.
> tools/hwsb/*.py unread; everything under pytest tmp_path.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 26, via sys.path edit)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../../tools/hwsb/hwsb_driver.py.md) (line 27, via sys.path edit)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 28, via sys.path edit)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 29, via sys.path edit)
- `import hws_driver` -> [tools/hws/hws_driver.py](../../tools/hws/hws_driver.py.md) (line 30, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 6)
- `builtins` (lines 8)
- `copy` (lines 9)
- `hashlib` (lines 10)
- `io` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 17)
- `shutil` (lines 14)
- `subprocess` (lines 15)
- `sys` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `CPU`
- `HWS_CONTRACT`
- `HWS_FRAGS`
- `HWS_JOBS`
- `OWNER_SHA`
- `P`
- `PLANTED`
- `REPO`
- `STAGES`

## Classes and functions

- **test `test_pause_check_is_strictly_greater_than_three_times`** [L42-53]: `def test_pause_check_is_strictly_greater_than_three_times(stage)` decorators: @pytest.mark.parametrize('stage', ['J-B1', 'DRY', 'KB', 'TRAIN', 'EVAL'])
- **test `test_pause_check_numbers_from_the_protocol`** [L56-62]: `def test_pause_check_numbers_from_the_protocol()`
- **test `test_ledger_read_default`** [L66-68]: `def test_ledger_read_default(tmp_path)`
- **test `test_ledger_append_entries_sum_and_atomic_replace`** [L71-92]: `def test_ledger_append_entries_sum_and_atomic_replace(tmp_path, monkeypatch)`
- **test `test_ledger_duplicate_job_is_refused`** [L95-101]: `def test_ledger_duplicate_job_is_refused(tmp_path)`
- **function `auth`** [L105-108]: `def auth(**kw)`
- **test `test_auth_ok_for_every_stage`** [L112-115]: `def test_auth_ok_for_every_stage(stage)` decorators: @pytest.mark.parametrize('stage', STAGES)
- **function `sched`** [L118-123]: `def sched(**kw)`
- **test `test_sched_rule2_and_rule3`** [L127-139]: `def test_sched_rule2_and_rule3(stage)` decorators: @pytest.mark.parametrize('stage', STAGES)
- **test `test_missing_sched_record_is_refused`** [L142-144]: `def test_missing_sched_record_is_refused()`
- **function `put_npz`** [L148-151]: `def put_npz(path, **arrays)`
- **function `synthetic_root`** [L154-161]: `def synthetic_root(tmp_path)`
- **function `flat`** [L164-165]: `def flat(snap)`
- **test `test_inventory_snapshot_lists_kinds`** [L168-174]: `def test_inventory_snapshot_lists_kinds(tmp_path)`
- **test `test_inventory_diff_unchanged_root_is_ok`** [L177-181]: `def test_inventory_diff_unchanged_root_is_ok(tmp_path)`
- **test `test_inventory_diff_detects_new_history_identity_and_obs_root`** [L184-195]: `def test_inventory_diff_detects_new_history_identity_and_obs_root(tmp_path)`
- **test `test_inventory_diff_new_top_level_directory_is_new`** [L198-206]: `def test_inventory_diff_new_top_level_directory_is_new(tmp_path)`
- **function `hit`** [L215-216]: `def hit(path, needle='620201')`
- **test `test_classify_hits_with_hws_lists_equals_hws_driver`** [L225-229]: `def test_classify_hits_with_hws_lists_equals_hws_driver(subset)` decorators: @pytest.mark.parametrize('subset', ['declared', 'mixed', 'outside', 'empty'])
- **test `test_classify_hits_defaults_use_contract_fragments`** [L232-241]: `def test_classify_hits_defaults_use_contract_fragments()`
- **function `guard`** [L244-255]: `def guard(monkeypatch, touched, bad)`
- **test `test_seed_search_whole_token_rule_and_excluded_folders`** [L258-284]: `def test_seed_search_whole_token_rule_and_excluded_folders(tmp_path, monkeypatch)`
- **function `git`** [L288-291]: `def git(cwd, *args)`
- **function `sha`** [L294-295]: `def sha(data)`
- **function `synthetic_repo`** [L298-314]: `def synthetic_repo(tmp_path)`
- **test `test_freeze_field_set_and_implementation_hash`** [L317-341]: `def test_freeze_field_set_and_implementation_hash(tmp_path)`
- **test `test_dry_run_refuses_without_rule2_sched`** [L345-359]: `def test_dry_run_refuses_without_rule2_sched(tmp_path, record)` decorators: @pytest.mark.parametrize('record', [None, {'live_history_reservations': ['r1']}])

