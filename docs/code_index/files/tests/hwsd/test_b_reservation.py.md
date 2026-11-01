# `tests/hwsd/test_b_reservation.py`

- Source: [tests/hwsd/test_b_reservation.py](../../../../../tests/hwsd/test_b_reservation.py)
- Kind: python
- Lines: 265

## Module docstring

> Author B: reservations, the J8 end record, W2 attestation, stopped sampling (J8, J10 item 3).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 13, via sys.path edit)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](../../tools/hwsd/hwsd_data.py.md) (line 14, via sys.path edit)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](../../tools/hwsd/hwsd_readers.py.md) (line 15, via sys.path edit)
- `import test_b_util` -> [tests/hwsd/test_b_util.py](test_b_util.py.md) (line 16, via same directory)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 18, via unique basename)

### External (third-party)

- `pytest` (lines 19)

### Standard library

- `__future__` (lines 3)
- `hashlib` (lines 213)
- `json` (lines 5)
- `pathlib` (lines 7)
- `sys` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(_p)` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `END_FIELDS`

## Classes and functions

- **function `_active`** [L26-30]: `def _active(path: Path, rid: str) -> Path`
- **function `_end_record`** [L33-40]: `def _end_record(store: Path, res: Path, obligation_rel: str, at: Path | None = None) -> Path`
- **test `test_contract_reservation_and_window`** [L43-48]: `def test_contract_reservation_and_window()`
- **test `test_start_and_verify_reservation`** [L51-57]: `def test_start_and_verify_reservation(tmp_path)`
- **test `test_start_refused_while_another_active_unended`** [L60-66]: `def test_start_refused_while_another_active_unended(tmp_path)`
- **test `test_end_reservation_writes_the_j8_record`** [L69-93]: `def test_end_reservation_writes_the_j8_record(tmp_path)`
- **test `test_end_reservation_refusals_write_nothing`** [L96-117]: `def test_end_reservation_refusals_write_nothing(tmp_path)`
- **test `test_attestation_live_without_end_and_after_changes`** [L120-139]: `def test_attestation_live_without_end_and_after_changes(tmp_path)`
- **test `test_track_u_end_record_is_accepted`** [L142-152]: `def test_track_u_end_record_is_accepted(tmp_path)`
- **test `test_track_u_top_level_reservation`** [L155-166]: `def test_track_u_top_level_reservation(tmp_path)`
- **test `test_end_record_of_wrong_schema_is_live`** [L169-178]: `def test_end_record_of_wrong_schema_is_live(tmp_path)`
- **test `test_non_active_and_schema_failures`** [L181-197]: `def test_non_active_and_schema_failures(tmp_path)`
- **function `_hwsc_w2`** [L200-207]: `def _hwsc_w2(root: Path, res_bytes: bytes, end_bytes: bytes) -> Path`
- **test `test_hwsc_w2_end_fixture_rule_a`** [L210-228]: `def test_hwsc_w2_end_fixture_rule_a(tmp_path, monkeypatch)`
- **test `test_real_hwsc_w2_end_record_copy`** [L231-242]: `def test_real_hwsc_w2_end_record_copy(tmp_path)` - The bound mailbox record and stage C's reservation record (JSON records, copied).
- **test `test_stopped_sample_before_first_row_and_rerun`** [L245-265]: `def test_stopped_sample_before_first_row_and_rerun(tmp_path)` - J10 item 3 / F-1: no history file, obligation + END, a rerun opens a new id.

