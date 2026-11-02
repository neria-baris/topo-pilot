# `tools/hwsd/hwsd_records.py`

- Source: [tools/hwsd/hwsd_records.py](../../../../../tools/hwsd/hwsd_records.py)
- Kind: python
- Lines: 296

## Module docstring

> HWSD records: lineage, AUTH/SCHED, FREEZE, S0, preflight, budget and pauses, ledger, H-1
> checks and archive (API.md §10, §19). Reused hwsc_records names are re-exported (called through
> the module at call time).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 15, via unique basename)
- `import hws_records` -> [tools/hws/hws_records.py](../hws/hws_records.py.md) (line 16, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 17, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 20, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 21, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `fnmatch` (lines 8)
- `fractions` (lines 12)
- `json` (lines 9)
- `pathlib` (lines 13)
- `re` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 17, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 18, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 20, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 38, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 28, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 19, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 25, import)
- [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 16, import)

## Top-level constants

- `FREE_FOLDERS_D`
- `RECORD_FILES_D`
- `RECORD_PATTERNS_D`
- `RES_NAME`

## Classes and functions

- **function `run_gates_c`** [L36-37]: `def run_gates_c(*a, **k)`
- **function `superseded_ok`** [L40-41]: `def superseded_ok(out)`
- **function `sched_ok`** [L44-45]: `def sched_ok(sched, stage)`
- **function `record_gate_files`** [L48-49]: `def record_gate_files(out, stage, names)`
- **function `ledger_append`** [L52-53]: `def ledger_append(*a, **k)`
- **function `lineage_d`** [L57-86]: `def lineage_d(out) -> dict`
- **function `auth_ok_d`** [L90-102]: `def auth_ok_d(auth, stage, freeze=None) -> dict`
- **function `_git`** [L105-106]: `def _git(repo, *args) -> bytes`
- **function `_sha`** [L109-110]: `def _sha(data: bytes) -> str`
- **function `implementation_files_d`** [L113-116]: `def implementation_files_d(repo, h_exec) -> dict`
- **function `freeze_d`** [L119-142]: `def freeze_d(out, repo, h_exec, dry_report, pf_record, kd4_params, run_approval) -> dict`
- **function `verify_freeze_d`** [L145-164]: `def verify_freeze_d(out, repo=dc.REPO) -> dict`
- **function `s0_d`** [L167-183]: `def s0_d(repo, r_ref, h_exec) -> dict`
- **function `preflight_d`** [L186-200]: `def preflight_d(out, stage, auth, sched, repo=dc.REPO) -> dict`
- **function `central_d`** [L204-207]: `def central_d(stage) -> float`
- **function `cumulative_d`** [L210-213]: `def cumulative_d(stage) -> float`
- **function `pause_check_d`** [L216-224]: `def pause_check_d(stage, stage_cpu, cum_cpu, job_cpu=None) -> dict`
- **function `pause_or_raise_d`** [L227-239]: `def pause_or_raise_d(out, stage, t0, ledger_path=None, cont=None) -> None`
- **function `ledger_init`** [L242-249]: `def ledger_init(path) -> dict`
- **function `ledger_append_d`** [L252-256]: `def ledger_append_d(path, label, job, stage, cpu_s, source, master=None) -> dict`
- **function `no_value_check`** [L260-269]: `def no_value_check(obj) -> None`
- **function `acceptance_check`** [L272-292]: `def acceptance_check(rec) -> None`
- **function `archive_attempt_d`** [L295-296]: `def archive_attempt_d(out, job, attempt, files, suffixes=None) -> Path`

