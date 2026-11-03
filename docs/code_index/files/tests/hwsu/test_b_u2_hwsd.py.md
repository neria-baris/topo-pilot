# `tests/hwsu/test_b_u2_hwsd.py`

- Source: [tests/hwsu/test_b_u2_hwsd.py](../../../../../tests/hwsu/test_b_u2_hwsd.py)
- Kind: python
- Lines: 342

## Module docstring

> Author B (job 0223, phase 2): U5 (source_hwsd), J10 obligations of another store and R-0213-1
> (API_U2 2.4, 3; TEST_PLAN_U2 row test_b_u2_hwsd). Track-D-form fixtures only, under tmp_path; no
> real hwsd-store file is opened. Obligations use the phase-1 obligation shape
> (hws-registry-obligation-v1), with their own name_rule.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 21, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 22, via unique basename)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 6)
- `builtins` (lines 8)
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

- `import_module` line 29: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 30: `hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](../../tools/hwsu/u2/hwsu_registry.py.md)
- `import_module` line 34: `u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md)
- `import_module` line 35: `hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](../../tools/hwsu/u2/hwsu_known.py.md)

### sys.path additions

- line 19: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `AUTH`
- `INC`
- `REPO`
- `RULES`

## Classes and functions

- **function `_reg`** [L28-30]: `def _reg()`
- **function `_known`** [L33-35]: `def _known()`
- **function `_sha`** [L38-39]: `def _sha(b: bytes) -> str`
- **function `_put`** [L42-45]: `def _put(p: Path, data: bytes) -> str`
- **function `_nonhist`** [L52-58]: `def _nonhist(store: Path, rel='stages/KC/ORACLE_kc.npz') -> dict`
- **function `_hist`** [L61-69]: `def _hist(store: Path, rel='stages/KC/HIST_kc_b0.npz', seed=1) -> dict`
- **function `_obl`** [L72-79]: `def _obl(store: Path, files: list, name='REGISTRY_OBLIGATION.json', utc='2026-11-02T12:00:00Z', rules=None)` - A J11-form obligation (API.md J11 erratum): all top-level keys, files sorted by relpath.
- **function `opens`** [L83-108]: `def opens(monkeypatch)` decorators: @pytest.fixture
- **function `_roots`** [L111-115]: `def _roots(tmp_path)`
- **test `test_hwsd_store_absent_passes`** [L119-122]: `def test_hwsd_store_absent_passes(tmp_path)`
- **test `test_hwsd_store_without_obligation_is_incomplete`** [L125-129]: `def test_hwsd_store_without_obligation_is_incomplete(tmp_path)`
- **test `test_hwsd_known_case_only_store_passes`** [L132-136]: `def test_hwsd_known_case_only_store_passes(tmp_path)`
- **test `test_hwsd_listed_history_file_is_read_by_its_reader`** [L139-145]: `def test_hwsd_listed_history_file_is_read_by_its_reader(tmp_path)`
- **test `test_hwsd_unlisted_chart_array_is_incomplete`** [L148-153]: `def test_hwsd_unlisted_chart_array_is_incomplete(tmp_path)`
- **test `test_hwsd_newest_obligation_governs`** [L156-163]: `def test_hwsd_newest_obligation_governs(tmp_path)`
- **test `test_hwsd_newer_complete_obligation_rescues_older_incomplete`** [L166-172]: `def test_hwsd_newer_complete_obligation_rescues_older_incomplete(tmp_path)`
- **test `test_hwsd_dry_directory_without_obligation_is_incomplete`** [L175-178]: `def test_hwsd_dry_directory_without_obligation_is_incomplete(tmp_path)`
- **test `test_read_obligation_u2_uses_each_obligations_own_name_rules`** [L181-197]: `def test_read_obligation_u2_uses_each_obligations_own_name_rules(tmp_path)`
- **test `test_only_obligation_reservation_and_end_files_are_opened`** [L200-210]: `def test_only_obligation_reservation_and_end_files_are_opened(tmp_path, opens)`
- **function `_end`** [L214-218]: `def _end(store: Path, rel: str, rid='RES-HWSD-1')`
- **test `test_store_relative_obligation_file_resolves_in_store`** [L221-227]: `def test_store_relative_obligation_file_resolves_in_store(tmp_path)`
- **test `test_root_relative_path_inside_the_store_is_accepted`** [L230-236]: `def test_root_relative_path_inside_the_store_is_accepted(tmp_path)`
- **test `test_store_candidate_wins_over_root_candidate`** [L239-245]: `def test_store_candidate_wins_over_root_candidate(tmp_path)`
- **test `test_candidates_existing_only_outside_the_store_are_not_used`** [L248-259]: `def test_candidates_existing_only_outside_the_store_are_not_used(tmp_path)`
- **function `_reservation`** [L263-267]: `def _reservation(store: Path, rid='RES-HWSD-1', state='ACTIVE')`
- **function `_end_record`** [L270-277]: `def _end_record(store: Path, rid, res_f, res_sha, obl_f, obl_sha, root)`
- **function `_ended_store`** [L280-285]: `def _ended_store(root: Path, obl_rel='REGISTRY_OBLIGATION.json')`
- **test `test_w2_store_relative_end_record_counts_as_ended`** [L288-292]: `def test_w2_store_relative_end_record_counts_as_ended(tmp_path)`
- **test `test_w2_root_relative_end_record_inside_store_counts_as_ended`** [L295-298]: `def test_w2_root_relative_end_record_inside_store_counts_as_ended(tmp_path)`
- **test `test_w2_reservation_without_end_record_is_live`** [L301-306]: `def test_w2_reservation_without_end_record_is_live(tmp_path)`
- **test `test_w2_changed_reservation_file_is_live`** [L309-315]: `def test_w2_changed_reservation_file_is_live(tmp_path)`
- **test `test_w2_obligation_only_outside_the_store_is_live`** [L318-325]: `def test_w2_obligation_only_outside_the_store_is_live(tmp_path)`
- **test `test_w2_changed_obligation_bytes_is_live`** [L328-333]: `def test_w2_changed_obligation_bytes_is_live(tmp_path)`
- **test `test_w2_own_reservation_is_excluded`** [L336-342]: `def test_w2_own_reservation_is_excluded(tmp_path)`

