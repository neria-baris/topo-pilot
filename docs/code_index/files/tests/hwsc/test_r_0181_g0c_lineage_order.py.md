# `tests/hwsc/test_r_0181_g0c_lineage_order.py`

- Source: [tests/hwsc/test_r_0181_g0c_lineage_order.py](../../../../../tests/hwsc/test_r_0181_g0c_lineage_order.py)
- Kind: python
- Lines: 64

## Module docstring

> Coordinator-written regression test for defect D-0181-1 (API.md §24): g0c checks the store's
> lineage before it writes stages/<stage>/G0C.json, which is recorded only when the stage completes.
> Authority files, the stage-B handoff and the seed search are synthetic (monkeypatched); the store
> is a tmp_path store holding only its FREEZE.json.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 18, via sys.path edit)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 19, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 20, via unique basename)

### External (third-party)

- `pytest` (lines 13)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`
- `SCHED`

## Classes and functions

- **function `_file`** [L26-29]: `def _file(p: Path, text: str) -> str`
- **function `_setup`** [L32-48]: `def _setup(tmp_path, monkeypatch)`
- **test `test_g0c_passes_on_a_store_holding_only_its_freeze`** [L51-55]: `def test_g0c_passes_on_a_store_holding_only_its_freeze(tmp_path, monkeypatch)`
- **test `test_g0c_still_fails_closed_on_an_unrecorded_file`** [L58-64]: `def test_g0c_still_fails_closed_on_an_unrecorded_file(tmp_path, monkeypatch)`

