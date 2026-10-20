# `tools/x4_circle_history/stage_records.py`

- Source: [tools/x4_circle_history/stage_records.py](../../../../../tools/x4_circle_history/stage_records.py)
- Kind: python
- Lines: 157

## Module docstring

> Gate and stage records for runner.py (API.md spec v2.4 items 1 and 8; builder-tested).

## Imports

### Internal (repo files)

- `from errors import Invalid, JoinError, Unresolved` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 18, via same directory)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 15)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 38, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 34, import)
- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 36, import)
- [tests/c1prime/test_a_gates.py](../../tests/c1prime/test_a_gates.py.md) (line 25, import)
- [tests/circle_history/test_builder_e2e.py](../../tests/circle_history/test_builder_e2e.py.md) (line 27, import)
- [tests/circle_history/test_builder_v24_stages.py](../../tests/circle_history/test_builder_v24_stages.py.md) (line 20, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 21, import)
- [tools/c1prime/c1_driver_cal.py](../c1prime/c1_driver_cal.py.md) (line 19, import)
- [tools/c1prime/c1_driver_fresh.py](../c1prime/c1_driver_fresh.py.md) (line 20, import)
- [tools/c1prime/c1_driver_late.py](../c1prime/c1_driver_late.py.md) (line 21, import)
- [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 12, import)
- [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 17, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 26, import)
- [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 27, import)
- [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 20, import)
- [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 18, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 29, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 31, import)

## Top-level constants

- `PREREQUISITE`

## Classes and functions

- **class `StageRefused(RuntimeError)`** [L23-24] - Out-of-order, repeated or integrity-failed stage invocation (no gate record).
- **function `_utc`** [L27-28]: `def _utc() -> str`
- **function `sha256`** [L31-32]: `def sha256(path: Path) -> str`
- **function `write_new`** [L35-37]: `def write_new(path: Path, obj) -> None`
- **function `save_npz`** [L40-42]: `def save_npz(path: Path, **arrays) -> None`
- **function `_lines`** [L45-48]: `def _lines(path: Path) -> list`
- **function `gates_so_far`** [L51-52]: `def gates_so_far(out: Path) -> list`
- **function `stages_so_far`** [L55-56]: `def stages_so_far(out: Path) -> list`
- **function `_append`** [L59-61]: `def _append(path: Path, entry: dict) -> None`
- **function `record_gate`** [L64-67]: `def record_gate(out: Path, gate: str, status: str, **details) -> str`
- **function `run_gate`** [L70-79]: `def run_gate(out: Path, gate: str, fn)` - Invalid/JoinError -> FAIL_TECHNICAL; Unresolved -> INCONCLUSIVE (spec v2.4 item 1).
- **function `refuse`** [L82-93]: `def refuse(out: Path, stage: str, reason: str, integrity: bool = False)`
- **function `_check_prerequisite`** [L96-119]: `def _check_prerequisite(out: Path, stage: str, models, stages: list, gates: list) -> None`
- **function `begin`** [L122-136]: `def begin(out: Path, stage: str, models) -> None` - Refuse a repeated, out-of-order or integrity-failed invocation; else record STARTED.
- **function `complete`** [L139-150]: `def complete(out: Path, stage: str, files, outcome: str = 'done') -> None`
- **function `attempts_without_completion`** [L153-157]: `def attempts_without_completion(out: Path) -> list`

