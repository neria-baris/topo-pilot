# `tests/hwsu/test_b_of_registry.py`

- Source: [tests/hwsu/test_b_of_registry.py](../../../../../tests/hwsu/test_b_of_registry.py)
- Kind: python
- Lines: 333

## Module docstring

> Author B (job 0198): the J11 obligation reader on fixtures written in the other track's form,
> the fail-closed rules of J10/J11, the root inventory (§8.4 hygiene) and the registry rows of
> CONTRACT_OF. Joint rulings J4, J10 (addendum 3), J11 (addendum 4); API J11 erratum; DRO9.
> Readers: `hwsu_resv.read_obligation` (J11 erratum) and `hwsu_dry.obligation_reader_fixture`.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 23, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 24, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 25, via unique basename)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../../tools/hwsu/hwsu_dry.py.md) (line 34, via sys.path edit) (inside a function)
- `import hwsu_resv` -> [tools/hwsu/hwsu_resv.py](../../tools/hwsu/hwsu_resv.py.md) (line 35, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 6)
- `builtins` (lines 8)
- `copy` (lines 9)
- `hashlib` (lines 10)
- `io` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 15)
- `re` (lines 311)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `D_RULES`
- `INC`
- `REPO`

## Classes and functions

- **function `_readers`** [L33-36]: `def _readers()`
- **function `_norm`** [L39-40]: `def _norm(p) -> str`
- **function `_hook`** [L43-62]: `def _hook(monkeypatch) -> list`
- **function `_sha`** [L65-66]: `def _sha(p) -> str`
- **function `_npz`** [L69-73]: `def _npz(path, **arrays) -> Path`
- **function `_hist`** [L76-81]: `def _hist(path)`
- **function `_entry`** [L84-90]: `def _entry(store, rel, cls, basis=None)`
- **function `_d_store`** [L93-111]: `def _d_store(root)` - A store as track D would write it (J11 form, track "D", its own name rules).
- **function `_obl`** [L114-123]: `def _obl(store, files, name='REGISTRY_OBLIGATION.json', utc='2026-11-01T12:00:00Z', **over)`
- **function `_status`** [L126-132]: `def _status(store)`
- **test `test_reader_track_d_form_passes`** [L136-142]: `def test_reader_track_d_form_passes(tmp_path, monkeypatch)`
- **function `_mutations`** [L145-163]: `def _mutations()`
- **test `test_reader_one_mutated_key_is_incomplete`** [L167-173]: `def test_reader_one_mutated_key_is_incomplete(tmp_path, mut)` decorators: @pytest.mark.parametrize('mut', _mutations(), ids=lambda f: f.__name__)
- **test `test_reader_unlisted_array_is_incomplete`** [L176-180]: `def test_reader_unlisted_array_is_incomplete(tmp_path)`
- **test `test_reader_sha_mismatch_is_incomplete`** [L183-188]: `def test_reader_sha_mismatch_is_incomplete(tmp_path)`
- **test `test_reader_checkpoint_sha_null_not_rehashed`** [L191-195]: `def test_reader_checkpoint_sha_null_not_rehashed(tmp_path)`
- **test `test_reader_unmatched_name_rule_basis_is_incomplete`** [L198-202]: `def test_reader_unmatched_name_rule_basis_is_incomplete(tmp_path)`
- **test `test_reader_newest_governs`** [L205-213]: `def test_reader_newest_governs(tmp_path)`
- **test `test_reader_known_case_records_only`** [L216-221]: `def test_reader_known_case_records_only(tmp_path)`
- **test `test_reader_arrays_without_obligation_until_coordinator_writes_one`** [L224-231]: `def test_reader_arrays_without_obligation_until_coordinator_writes_one(tmp_path)` - J10 item 4: an aborted dry store stays incomplete until an obligation lists every array.
- **test `test_reader_accepts_own_writer_output`** [L234-243]: `def test_reader_accepts_own_writer_output(tmp_path)` - Round trip: the HWSU writer's record (track U) is accepted by the J11 reader.
- **function `_touch`** [L247-250]: `def _touch(p)`
- **test `test_root_inventory_counts_and_pruning`** [L253-284]: `def test_root_inventory_counts_and_pruning(tmp_path, monkeypatch)`
- **test `test_root_inventory_detects_new_array`** [L287-293]: `def test_root_inventory_detects_new_array(tmp_path)`
- **test `test_contract_obligation_block_is_j11`** [L297-316]: `def test_contract_obligation_block_is_j11()`
- **test `test_contract_reservation_baseline_and_root_baseline`** [L319-333]: `def test_contract_reservation_baseline_and_root_baseline()`

