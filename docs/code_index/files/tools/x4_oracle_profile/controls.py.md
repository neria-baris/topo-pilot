# `tools/x4_oracle_profile/controls.py`

- Source: [tools/x4_oracle_profile/controls.py](../../../../../tools/x4_oracle_profile/controls.py)
- Kind: python
- Lines: 222

## Module docstring

> Runtime-control classifier for job 0014 (standard library only).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 19)
- `datetime` (lines 27)
- `hashlib` (lines 21)
- `json` (lines 22)
- `math` (lines 23)
- `os` (lines 24)
- `pathlib` (lines 28)
- `re` (lines 25)
- `time` (lines 26)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_release_meter.py](../../tests/c1prime/test_a_release_meter.py.md) (line 36, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 34, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 26, import)
- [tests/hwsc/test_b_guard_meter.py](../../tests/hwsc/test_b_guard_meter.py.md) (line 30, import)
- [tests/k4b/test_b_meter.py](../../tests/k4b/test_b_meter.py.md) (line 26, import)
- [tests/oracle_profile/test_builder_controls.py](../../tests/oracle_profile/test_builder_controls.py.md) (line 17, import)
- [tests/x6_stage1/test_b_nb_s0_ops.py](../../tests/x6_stage1/test_b_nb_s0_ops.py.md) (line 303, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 40, import)
- [tools/c1prime/c1_meter_bind.py](../c1prime/c1_meter_bind.py.md) (line 27, import)
- [tools/c2_nd/store_template/nd_meter_bind.py](../c2_nd/store_template/nd_meter_bind.py.md) (line 65, import)
- [tools/d2a/d2a_train.py](../d2a/d2a_train.py.md) (line 114, import)
- [tools/hws/hws_dry.py](../hws/hws_dry.py.md) (line 169, import)
- [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 18, import)
- [tools/x4_circle_history/live_context.py](../x4_circle_history/live_context.py.md) (line 80, import)
- [tools/x4_circle_history/meter_bind.py](../x4_circle_history/meter_bind.py.md) (line 47, import)
- [tools/x4_oracle_profile/meter.py](meter.py.md) (line 28, import)
- [tools/x4_oracle_profile/runtime.py](runtime.py.md) (line 17, import)

## Top-level constants

- `JOB_ID`
- `LATCH`
- `MAILBOX`
- `TASK_SHA256`
- `USAGE_THRESHOLD`

## Classes and functions

- **function `_read_json`** [L38-39]: `def _read_json(path: Path)`
- **function `_utc`** [L42-54]: `def _utc(text) -> datetime | None` - Timezone-aware ISO-8601 instant (accepts 'Z' and 1-9 fractional digits), else None.
- **function `_percent_ok`** [L57-62]: `def _percent_ok(used) -> bool`
- **function `_usage_state`** [L65-79]: `def _usage_state(usage) -> tuple[str, str] | None`
- **function `_audit_identity`** [L82-96]: `def _audit_identity(mailbox: Path, control: dict) -> tuple[str, str]` - Audit mode: job 0014 must be terminal; coordinator hold still holds; no usage latch.
- **function `_base`** [L99-148]: `def _base(mailbox: Path, out, mode: str) -> tuple[tuple[str, str], dict, dict]` - Stateless classification; also returns parsed control and usage (or {}).
- **function `release_ready`** [L151-164]: `def release_ready(latch: dict, control: dict, usage: dict) -> bool` - Fresh OBSERVED clearance after the latch plus a coordinator CONTINUE issued after it.
- **function `_write_new`** [L167-169]: `def _write_new(path: Path, obj) -> None`
- **function `classify`** [L172-211]: `def classify(mailbox: Path = MAILBOX, out: Path | None = None, mode: str = 'run', latch_dir: Path | None = None) -> tuple[str, str]` - Return ``(state, reason)``; in run mode with ``latch_dir`` apply the persistent latch.
- **function `classify_all`** [L214-222]: `def classify_all(mailboxes, out: Path | None = None, mode: str = 'run') -> tuple[str, str]` - Most restrictive state across mailboxes. The real mailbox latches in ``out``; a synthetic

