# `tools/hwsu/u2/hwsu_driver.py`

- Source: [tools/hwsu/u2/hwsu_driver.py](../../../../../../tools/hwsu/u2/hwsu_driver.py)
- Kind: python
- Lines: 345

## Module docstring

> HWSU jobs KC, E1, REG2, E2, the metered entry point and the CLI (API_U2.md section 5).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 8, via unique basename)
- `import hwsu_decide` -> [tools/hwsu/u2/hwsu_decide.py](hwsu_decide.py.md) (line 9, via same directory)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](../hwsu_driver_of.py.md) (line 10, via unique basename)
- `import hwsu_gates` -> [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 11, via same directory)
- `import hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 12, via same directory)
- `import hwsu_meter_bind` -> [tools/hwsu/hwsu_meter_bind.py](../hwsu_meter_bind.py.md) (line 13, via unique basename)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 14, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../hwsu_of.py.md) (line 15, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 16, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 17, via same directory)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 18, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../k4b/k4b_meter_bind.py.md) (line 26, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../k4b/k4b_release.py.md) (line 27, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../x4_oracle_profile/meter.py.md) (line 28, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../x4_circle_history/op_guard.py.md) (line 29, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 30, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../x4_oracle_profile/winjob.py.md) (line 31, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 32, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `importlib` (lines 19)
- `json` (lines 20)
- `os` (lines 21)
- `pathlib` (lines 24)
- `sys` (lines 22)
- `time` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 331: `hwsu_bind_u2` -> [tools/hwsu/u2/hwsu_bind_u2.py](hwsu_bind_u2.py.md)
- `import_module` line 335: `hwsu_dry2` -> [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md)

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_records.py](../../../tests/hwsu/test_b_u2_records.py.md) (line 36, dynamic)
- [tools/hwsu/u2/hwsu_dry2c.py](hwsu_dry2c.py.md) (line 16, import)

## Top-level constants

- `EXIT`
- `STAGES`
- `STAGE_OUTPUTS`
- `SUPERSEDED_RULE`

## Classes and functions

- **function `build_ctx_u`** [L39-50]: `def build_ctx_u(out, job, attempt, stage, reservation_id=None, root=uc.ROOT, mailbox=uc.MAILBOX, hwsc_store=uc.HWSC_STORE, scope=uc.SCOPE_U, seeds=None, dry=False) -> dict`
- **function `reg2`** [L53-67]: `def reg2(out, ctx) -> dict`
- **function `steps`** [L70-97]: `def steps(stage, ctx) -> list`
- **function `memory_cap_u2`** [L100-104]: `def memory_cap_u2(stage) -> int`
- **function `job_paths_u2`** [L107-114]: `def job_paths_u2(job, kind) -> dict`
- **function `_exit_code`** [L117-120]: `def _exit_code(outcome, registered) -> int`
- **function `_unrecorded`** [L123-134]: `def _unrecorded(out, rels) -> list`
- **function `_outcome`** [L137-142]: `def _outcome(stage, records, ctx) -> str`
- **function `archive_previous`** [L153-166]: `def archive_previous(out, stage, job) -> Path | None` - Pre-attempt archive (R-0223-10 item 2): earlier outputs of the same stage move to
- **function `write_obligation_u2`** [L173-207]: `def write_obligation_u2(store, name, job, written_by, dry=False, attempt=None, reservation_id=None) -> Path` - Phase-1 obligation writer (hwsu_records.write_obligation) extended to the arrays of
- **function `bind_stage`** [L210-213]: `def bind_stage(stage) -> str` - The stage name phase-1 bind accepts: the stage itself when its table knows it, else OF
- **function `run_job`** [L216-272]: `def run_job(stage, out, job, attempt=1, reservation_id=None, repo=uc.REPO, ledger_path=None, ctx=None, dry_continue=False) -> dict`
- **function `meter_main`** [L275-307]: `def meter_main(argv=None) -> int`
- **function `main`** [L310-341]: `def main(argv=None) -> int`

