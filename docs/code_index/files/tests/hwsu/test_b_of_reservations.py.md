# `tests/hwsu/test_b_of_reservations.py`

- Source: [tests/hwsu/test_b_of_reservations.py](../../../../../tests/hwsu/test_b_of_reservations.py)
- Kind: python
- Lines: 323

## Module docstring

> Author B (job 0198): reservation files, the J8 end record and the W2 attestation
> (protocol §8.2 item 3; joint rulings J2, J8, J10 item 3; S-3). TEST_PLAN §3 row
> test_b_of_reservations; DRO7, DRO9. Synthetic roots under tmp_path only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 18, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 19, via unique basename)

### External (third-party)

- `pytest` (lines 12)

### Standard library

- `__future__` (lines 5)
- `hashlib` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `END_FIELDS`
- `REPO`
- `UTC`

## Classes and functions

- **function `_sha`** [L27-28]: `def _sha(p) -> str`
- **function `_json`** [L31-35]: `def _json(p, obj) -> Path`
- **function `_active`** [L38-42]: `def _active(store, rid, name=None, **extra) -> Path`
- **function `_end_fixture`** [L45-51]: `def _end_fixture(store, rid, res_file, obl_file, root, schema='hws-reservation-end-v1')` - An end record written by hand in the J8 form (as track D's hwsd_data.end_reservation).
- **function `_fails`** [L54-57]: `def _fails(status, fn, *a, **k)`
- **test `test_reservation_file_mapping`** [L66-67]: `def test_reservation_file_mapping(rid, name)` decorators: @pytest.mark.parametrize('rid,name', [('RES-HWSU-OF', 'RESERVATION_OF.json'), ('RES-HWSU-OF-a2', 'RESERVATION_OF-a2.json'), ('RES-HWSU-OF-a11', 'RESERVATION_OF-a11.json'), ('RES-HWSU-U', 'RESERVATION_U.json'), ('RES-HWSU-U-a3', 'RESERVATION_U-a3.json')])
- **test `test_reservation_file_refuses_other_ids`** [L72-74]: `def test_reservation_file_refuses_other_ids(rid)` decorators: @pytest.mark.parametrize('rid', ['RES-HWSD-W2', 'RES-HWSC-W2', 'RES-HWSU-OF-a1', 'RES-HWSU-OF-a0', 'RES-HWSU-OF-ax', 'RES-HWSU-E1', 'RES-HWSU-OF-a2x', ''])
- **test `test_contract_reservation_names`** [L77-82]: `def test_contract_reservation_names()`
- **test `test_write_reservation_k4b_form_exclusive`** [L86-101]: `def test_write_reservation_k4b_form_exclusive(tmp_path)`
- **function `_store_with_obligation`** [L105-111]: `def _store_with_obligation(tmp_path, rid='RES-HWSU-OF')`
- **test `test_end_reservation_writes_exact_record`** [L114-126]: `def test_end_reservation_writes_exact_record(tmp_path)`
- **test `test_end_reservation_written_by_argument`** [L129-132]: `def test_end_reservation_written_by_argument(tmp_path)`
- **test `test_end_reservation_refuses_absent_reservation`** [L135-138]: `def test_end_reservation_refuses_absent_reservation(tmp_path)`
- **test `test_end_reservation_refuses_not_active`** [L142-152]: `def test_end_reservation_refuses_not_active(tmp_path, state)` decorators: @pytest.mark.parametrize('state', ['ENDED', 'active', None])
- **test `test_end_reservation_refuses_absent_obligation`** [L155-159]: `def test_end_reservation_refuses_absent_obligation(tmp_path)`
- **test `test_end_reservation_refuses_second_call`** [L162-168]: `def test_end_reservation_refuses_second_call(tmp_path)`
- **function `_attest`** [L172-173]: `def _attest(root, **k)`
- **test `test_attestation_live_without_end`** [L176-180]: `def test_attestation_live_without_end(tmp_path)`
- **test `test_attestation_ended_by_own_end_record`** [L183-187]: `def test_attestation_ended_by_own_end_record(tmp_path)`
- **test `test_attestation_reservation_changed_after_end_is_live`** [L190-195]: `def test_attestation_reservation_changed_after_end_is_live(tmp_path)`
- **test `test_attestation_obligation_changed_after_end_is_live`** [L198-203]: `def test_attestation_obligation_changed_after_end_is_live(tmp_path)`
- **test `test_attestation_obligation_deleted_after_end_is_live`** [L206-210]: `def test_attestation_obligation_deleted_after_end_is_live(tmp_path)`
- **test `test_attestation_wrong_schema_end_record_is_live`** [L213-219]: `def test_attestation_wrong_schema_end_record_is_live(tmp_path)`
- **test `test_attestation_accepts_track_d_form_end_record`** [L222-232]: `def test_attestation_accepts_track_d_form_end_record(tmp_path)` - J8 item 5: the other track's end record, written by hand in the shared schema.
- **function `_w2_fixture`** [L235-242]: `def _w2_fixture(root, mailbox)`
- **test `test_attestation_rule_a_hwsc_w2`** [L245-249]: `def test_attestation_rule_a_hwsc_w2(tmp_path)`
- **test `test_attestation_rule_a_mismatches_are_live`** [L252-259]: `def test_attestation_rule_a_mismatches_are_live(tmp_path)`
- **test `test_attestation_rule_a_only_for_res_hwsc_w2`** [L262-270]: `def test_attestation_rule_a_only_for_res_hwsc_w2(tmp_path)`
- **test `test_attestation_stateless_files_not_active`** [L273-278]: `def test_attestation_stateless_files_not_active(tmp_path)`
- **test `test_attestation_own_is_excluded`** [L281-286]: `def test_attestation_own_is_excluded(tmp_path)`
- **test `test_attestation_reservations_dir_files_inspected`** [L289-294]: `def test_attestation_reservations_dir_files_inspected(tmp_path)`
- **test `test_attestation_unreadable_file_is_live`** [L297-303]: `def test_attestation_unreadable_file_is_live(tmp_path)`
- **test `test_attestation_end_records_not_reservations`** [L306-312]: `def test_attestation_end_records_not_reservations(tmp_path)` - END records are excluded from the inspected set; a stale END alone changes nothing.
- **test `test_stopped_attempt_then_rerun_reservation`** [L315-323]: `def test_stopped_attempt_then_rerun_reservation(tmp_path)` - J10 item 3 / D-17: a no-history obligation ends RES-HWSU-OF; the rerun's own id is excluded.

