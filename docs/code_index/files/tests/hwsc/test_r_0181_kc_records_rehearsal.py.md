# `tests/hwsc/test_r_0181_kc_records_rehearsal.py`

- Source: [tests/hwsc/test_r_0181_kc_records_rehearsal.py](../../../../../tests/hwsc/test_r_0181_kc_records_rehearsal.py)
- Kind: python
- Lines: 48

## Module docstring

> Coordinator-written regression test for defect D-0181-2 (API.md §25): the KC stage records the
> KC9 rehearsal registry files (hwsc-store/registry/rehearsal/) in its STAGE_COMPLETE, so lineage_c
> at E1 gate 0 finds them recorded. Preflight, the binding and run_kc's checks are stubbed; the stub
> writes what KC1 and KC9 write (an artifact and the three rehearsal file kinds).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 16, via sys.path edit)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](../../tools/hwsc/hwsc_driver.py.md) (line 17, via sys.path edit)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 18, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `contextlib` (lines 8)
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

- line 14: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `_write`** [L21-23]: `def _write(p: Path, data: bytes) -> None`
- **function `_fake_run_kc`** [L26-36]: `def _fake_run_kc(out, auth, sched, job, store=None)`
- **test `test_kc_stage_records_the_rehearsal_registry`** [L39-48]: `def test_kc_stage_records_the_rehearsal_registry(tmp_path, monkeypatch)`

