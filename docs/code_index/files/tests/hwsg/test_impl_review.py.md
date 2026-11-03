# `tests/hwsg/test_impl_review.py`

- Source: [tests/hwsg/test_impl_review.py](../../../../../tests/hwsg/test_impl_review.py)
- Kind: python
- Lines: 119

## Module docstring

> Implementer regression tests for R-0224-3 items 1-6 (one per item).

## Imports

### Internal (repo files)

- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](../../tools/hwsg/hwsg_bind.py.md) (line 10, via sys.path edit)
- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 11, via sys.path edit)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](../../tools/hwsg/hwsg_handoff.py.md) (line 12, via sys.path edit)
- `import hwsg_known` -> [tools/hwsg/hwsg_known.py](../../tools/hwsg/hwsg_known.py.md) (line 13, via sys.path edit)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](../../tools/hwsg/hwsg_oracle.py.md) (line 14, via sys.path edit)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](../../tools/hwsg/hwsg_records.py.md) (line 15, via sys.path edit)
- `import hwsg_registry` -> [tools/hwsg/hwsg_registry.py](../../tools/hwsg/hwsg_registry.py.md) (line 16, via sys.path edit)
- `import hwsg_train` -> [tools/hwsg/hwsg_train.py](../../tools/hwsg/hwsg_train.py.md) (line 17, via sys.path edit)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](../../tools/hwsc/hwsc_registry.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 19, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 20, via unique basename)
- `from hwsc_records import superseded_ok` -> [tools/hwsc/hwsc_records.py](../../tools/hwsc/hwsc_records.py.md) (line 97, via unique basename) (inside a function)

### External (third-party)

- none

### Standard library

- `json` (lines 2)
- `os` (lines 90)
- `pathlib` (lines 4)
- `sys` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 8: `str(HERE)` -> `tools/hwsg`

## Imported by

- none

## Top-level constants

- `HERE`

## Classes and functions

- **test `test_1_inventory_g_passes_readers`** [L23-35]: `def test_1_inventory_g_passes_readers(monkeypatch, tmp_path)`
- **test `test_2_run_train_creates_reservation`** [L38-54]: `def test_2_run_train_creates_reservation(monkeypatch, tmp_path)`
- **test `test_3_sources_passes_contract_scratch_table`** [L57-64]: `def test_3_sources_passes_contract_scratch_table(monkeypatch, tmp_path)`
- **test `test_4_rerun_archives_and_kg4_takes_newest`** [L67-93]: `def test_4_rerun_archives_and_kg4_takes_newest(monkeypatch, tmp_path)`
- **test `test_5_superseded_name_accepted`** [L96-103]: `def test_5_superseded_name_accepted(tmp_path)`
- **test `test_6_identity_checker_uses_passed_store`** [L106-119]: `def test_6_identity_checker_uses_passed_store(monkeypatch, tmp_path)`

