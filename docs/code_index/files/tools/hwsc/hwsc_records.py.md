# `tools/hwsc/hwsc_records.py`

- Source: [tools/hwsc/hwsc_records.py](../../../../../tools/hwsc/hwsc_records.py)
- Kind: python
- Lines: 344

## Module docstring

> HWSC records: exception map, gate runner, lineage, authority, FREEZE, S0, budget, ledger and the
> D6 export (API.md §7.1, §7.2, §7.3 export_c; split from hwsc_driver by size, API erratum; the
> driver re-exports every name).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 19, via unique basename)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 20, via unique basename)
- `import hws_records` -> [tools/hws/hws_records.py](../hws/hws_records.py.md) (line 21, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 22, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 23, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 24, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 25, via unique basename)
- `from c1_records import C1GateFailure, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 26, via unique basename)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../hws/hws_worlds.py.md) (line 40, via unique basename) (inside a function)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 42, via package root) (inside a function)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 327, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 170)
- `torch` (lines 171)

### Standard library

- `__future__` (lines 5)
- `fnmatch` (lines 8)
- `fractions` (lines 16)
- `hashlib` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 17)
- `platform` (lines 12)
- `subprocess` (lines 13)
- `sys` (lines 14)
- `time` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 24, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 25, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 17, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 16, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 23, import)

## Top-level constants

- `C`
- `EXTRA_RECORDS`
- `RECORD_PATTERNS`

## Classes and functions

- **function `utc`** [L35-36]: `def utc() -> str`
- **function `status_of`** [L39-54]: `def status_of(exc) -> str`
- **function `run_gates_c`** [L57-77]: `def run_gates_c(out, steps, dry_continue=False) -> list`
- **function `superseded_ok`** [L80-96]: `def superseded_ok(out) -> list` - Mirror of k4b_release._superseded_ok (R-0176-P2): every file of superseded/<job>/ must be
- **function `lineage_c`** [L99-126]: `def lineage_c(out) -> dict`
- **function `record_gate_files`** [L129-134]: `def record_gate_files(out, stage, names) -> None` - D-0187-2: the E1/E2 gate files enter a STAGE_COMPLETE, so a later lineage_c finds them.
- **function `auth_ok`** [L137-149]: `def auth_ok(auth, stage, freeze=None) -> dict`
- **function `sched_ok`** [L152-158]: `def sched_ok(sched, stage) -> dict`
- **function `_git`** [L161-162]: `def _git(repo, *args) -> bytes`
- **function `_sha`** [L165-166]: `def _sha(data: bytes) -> str`
- **function `environment`** [L169-174]: `def environment() -> dict`
- **function `implementation_files`** [L177-180]: `def implementation_files(repo, h_exec) -> dict`
- **function `freeze_c`** [L183-205]: `def freeze_c(out, repo, h_exec, dry_report, pf_record, run_approval) -> dict`
- **function `verify_freeze_c`** [L208-227]: `def verify_freeze_c(out, repo=cc.REPO) -> dict`
- **function `s0`** [L230-246]: `def s0(repo, r_ref, h_exec) -> dict`
- **function `preflight`** [L249-263]: `def preflight(out, stage, auth, sched, repo=cc.REPO) -> dict`
- **function `central`** [L267-271]: `def central(stage, k=None, R=None) -> float`
- **function `_cumulative`** [L274-277]: `def _cumulative(stage, k=None) -> float`
- **function `pause_check_c`** [L280-286]: `def pause_check_c(stage, stage_cpu, cum_cpu, k=None) -> dict`
- **function `ledger_read`** [L289-293]: `def ledger_read(path) -> dict`
- **function `ledger_append`** [L296-306]: `def ledger_append(path, label, job, stage, cpu_s, source, master=None) -> dict`
- **function `pause_or_raise_c`** [L309-322]: `def pause_or_raise_c(out, stage, t0, ledger_path=None, cont=None, k=None) -> None`
- **function `export_c`** [L326-344]: `def export_c(out, result, oc, ann, fill) -> Path`

