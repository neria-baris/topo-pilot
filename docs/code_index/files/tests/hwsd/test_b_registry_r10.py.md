# `tests/hwsd/test_b_registry_r10.py`

- Source: [tests/hwsd/test_b_registry_r10.py](../../../../../tests/hwsd/test_b_registry_r10.py)
- Kind: python
- Lines: 354

## Module docstring

> Author B: obligations (J3, J4, J10, J11) and the R10 reader (API.md §3.4, §4; DRD8).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 14, via sys.path edit)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 15, via sys.path edit)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](../../tools/hwsd/hwsd_readers.py.md) (line 16, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 17, via same directory)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 3)
- `copy` (lines 5)
- `json` (lines 6)
- `pathlib` (lines 8)
- `shutil` (lines 332)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 12: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `FILE_MUTATIONS`
- `OBL`
- `PER_FILE`
- `TOP`
- `TOP_MUTATIONS`

## Classes and functions

- **test `test_contract_obligation_is_exactly_j11`** [L29-39]: `def test_contract_obligation_is_exactly_j11()`
- **function `_d_store`** [L45-58]: `def _d_store(tmp_path) -> Path`
- **function `_expected_class`** [L61-70]: `def _expected_class(rel: str)`
- **test `test_write_obligation_j11_form_and_round_trip`** [L73-106]: `def test_write_obligation_j11_form_and_round_trip(tmp_path)`
- **test `test_write_obligation_unclassifiable_is_lineage_and_writes_nothing`** [L111-117]: `def test_write_obligation_unclassifiable_is_lineage_and_writes_nothing(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['stages/S4/UNKNOWN.npz', 'stages/SCORE/620301/s0/X.npy', 'tmp/w.pt', 'artifacts/Bogus/abc1/payload.npz'])
- **test `test_classify_file_rules`** [L120-132]: `def test_classify_file_rules(tmp_path)`
- **test `test_write_obligation_name_rule`** [L137-141]: `def test_write_obligation_name_rule(tmp_path, name)` decorators: @pytest.mark.parametrize('name', ['REGISTRY_OBLIGATION_0301-a1.json', 'REGISTRY_OBLIGATION_0300-a2.json', 'REGISTRY_OBLIGATION_X.json', 'OBLIGATION.json'])
- **test `test_write_obligation_exclusive`** [L144-151]: `def test_write_obligation_exclusive(tmp_path)`
- **test `test_kd_only_store_with_its_obligation_passes`** [L154-162]: `def test_kd_only_store_with_its_obligation_passes(tmp_path)`
- **function `ustore`** [L169-173]: `def ustore(tmp_path)` decorators: @pytest.fixture
- **test `test_reader_accepts_track_u_form`** [L176-184]: `def test_reader_accepts_track_u_form(ustore, monkeypatch)`
- **function `_file`** [L198-199]: `def _file(o, suffix)`
- **test `test_one_mutated_key_or_value_is_incomplete`** [L228-236]: `def test_one_mutated_key_or_value_is_incomplete(ustore, which)` decorators: @pytest.mark.parametrize('which', sorted(TOP_MUTATIONS) + sorted(FILE_MUTATIONS))
- **test `test_os_payload_sha_mismatch_is_incomplete`** [L239-245]: `def test_os_payload_sha_mismatch_is_incomplete(ustore)`
- **test `test_unlisted_array_added_after_obligation_is_incomplete`** [L248-251]: `def test_unlisted_array_added_after_obligation_is_incomplete(ustore)`
- **test `test_newest_obligation_governs`** [L254-265]: `def test_newest_obligation_governs(ustore)`
- **test `test_written_utc_tie_takes_last_name`** [L268-275]: `def test_written_utc_tie_takes_last_name(ustore)`
- **test `test_store_without_obligation_is_incomplete`** [L278-284]: `def test_store_without_obligation_is_incomplete(tmp_path)`
- **test `test_kd_only_store_in_track_u_form_passes`** [L287-291]: `def test_kd_only_store_in_track_u_form_passes(tmp_path)`
- **function `_hwsu_dry`** [L297-306]: `def _hwsu_dry(folder: Path, with_obligation: bool) -> None`
- **test `test_source_hwsu_store_with_of_obligation_only`** [L309-315]: `def test_source_hwsu_store_with_of_obligation_only(tmp_path, ustore)`
- **test `test_source_hwsu_absent_everything`** [L318-322]: `def test_source_hwsu_absent_everything(tmp_path)`
- **test `test_source_hwsu_dry_store_needs_its_own_obligation`** [L325-337]: `def test_source_hwsu_dry_store_needs_its_own_obligation(tmp_path)`
- **test `test_source_hwsu_unreadable_array_in_job_folder`** [L340-344]: `def test_source_hwsu_unreadable_array_in_job_folder(tmp_path)`
- **test `test_source_hwsu_skips_test_roots`** [L347-354]: `def test_source_hwsu_skips_test_roots(tmp_path, monkeypatch)`

