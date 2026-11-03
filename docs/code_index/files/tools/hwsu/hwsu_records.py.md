# `tools/hwsu/hwsu_records.py`

- Source: [tools/hwsu/hwsu_records.py](../../../../../tools/hwsu/hwsu_records.py)
- Kind: python
- Lines: 215

## Module docstring

> HWSU records: gate runner, stages, lineage, ledger, pauses, registry risk (API.md §5.1-§5.2).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 9, via same directory)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 22, via unique basename)
- `from oracle_profile import ProfileError` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 23, via unique basename)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `fnmatch` (lines 10)
- `fractions` (lines 15)
- `hashlib` (lines 11)
- `importlib` (lines 210)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 16)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 214: `dynamic: mod`

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_of_driver.py](../../tests/hwsu/test_b_of_driver.py.md) (line 22, import)
- [tests/hwsu/test_b_of_freeze.py](../../tests/hwsu/test_b_of_freeze.py.md) (line 22, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 24, import)
- [tests/hwsu/test_b_of_records.py](../../tests/hwsu/test_b_of_records.py.md) (line 22, import)
- [tests/hwsu/test_b_of_registry.py](../../tests/hwsu/test_b_of_registry.py.md) (line 24, import)
- [tests/hwsu/test_b_of_reservations.py](../../tests/hwsu/test_b_of_reservations.py.md) (line 18, import)
- [tests/hwsu/test_b_of_seed.py](../../tests/hwsu/test_b_of_seed.py.md) (line 27, import)
- [tests/hwsu/test_b_of_streams.py](../../tests/hwsu/test_b_of_streams.py.md) (line 166, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 7, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 13, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 11, import)
- [tools/hwsu/hwsu_freeze.py](hwsu_freeze.py.md) (line 13, import)
- [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 13, import)
- [tools/hwsu/hwsu_resv.py](hwsu_resv.py.md) (line 14, import)
- [tools/hwsu/hwsu_seed.py](hwsu_seed.py.md) (line 7, import)

## Top-level constants

- `_SPLIT`

## Classes and functions

- **class `Paused(Exception)`** [L26-27] - Raised by pause_or_raise_u.
- **function `utc`** [L30-31]: `def utc() -> str`
- **function `_sha`** [L34-35]: `def _sha(data: bytes) -> str`
- **function `_canon_sha`** [L38-39]: `def _canon_sha(obj) -> str`
- **function `_append`** [L42-44]: `def _append(path, entry) -> None`
- **function `status_of`** [L47-58]: `def status_of(exc) -> str`
- **function `run_gates_u`** [L61-81]: `def run_gates_u(out, steps, continuing=('PASS', 'SHARE_DROPPED'), dry_continue=False) -> list`
- **function `begin_stage`** [L84-89]: `def begin_stage(out, stage) -> None`
- **function `complete_stage`** [L92-100]: `def complete_stage(out, stage, files) -> dict`
- **function `lineage_u`** [L103-128]: `def lineage_u(out) -> dict`
- **function `central`** [L132-136]: `def central(stage, contract=None) -> float`
- **function `cumulative_central`** [L139-144]: `def cumulative_central(stage, contract=None) -> float`
- **function `pause_check_u`** [L147-153]: `def pause_check_u(stage, stage_cpu, cum_cpu, contract=None) -> dict`
- **function `ledger_read`** [L156-159]: `def ledger_read(path) -> dict`
- **function `ledger_append`** [L162-172]: `def ledger_append(path, label, job, stage, cpu_s, source) -> dict`
- **function `running_cpu`** [L175-179]: `def running_cpu(stage, ledger_path, t0) -> tuple`
- **function `pause_or_raise_u`** [L182-193]: `def pause_or_raise_u(out, stage, t0, ledger_path=None, cont=None) -> None`
- **function `registry_risk_u`** [L196-198]: `def registry_risk_u(p_d2a, rows) -> dict`
- **function `__getattr__`** [L209-215]: `def __getattr__(name)`

