# `tools/hwsg/hwsg_records.py`

- Source: [tools/hwsg/hwsg_records.py](../../../../../tools/hwsg/hwsg_records.py)
- Kind: python
- Lines: 349

## Module docstring

> HWSG records: preflight, S0, FREEZE, lineage, ledger, outcome, terminal RESULT, export,
> release barrier (API.md §9; protocol §7.1 S0/PF/WIN, §10.3). Stage-C record code is reused.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import hwsc_outcome` -> [tools/hwsc/hwsc_outcome.py](../hwsc/hwsc_outcome.py.md) (line 15, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 16, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 17, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 18, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 20, via unique basename)
- `from hwsc_records import environment, record_gate_files, run_gates_c, status_of, superseded_ok, utc` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 21, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `fnmatch` (lines 7)
- `fractions` (lines 12)
- `hashlib` (lines 8)
- `json` (lines 9)
- `os` (lines 10)
- `pathlib` (lines 13)
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

- [tests/hwsg/test_a_outcomes_licences.py](../../tests/hwsg/test_a_outcomes_licences.py.md) (line 24, import)
- [tools/hwsg/hwsg_cross.py](hwsg_cross.py.md) (line 173, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 9, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 11, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 58, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 295, import)
- [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 242, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 108, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 134, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 196, import)

## Top-level constants

- `C`
- `FREE_DIRS`
- `RECORD_NAMES`
- `RECORD_PATTERNS`
- `_G_INC`

## Classes and functions

- **function `_sha`** [L36-37]: `def _sha(data: bytes) -> str`
- **function `lineage_g`** [L41-72]: `def lineage_g(out) -> dict`
- **function `auth_ok`** [L76-88]: `def auth_ok(auth, stage, freeze=None) -> dict`
- **function `window_ok`** [L91-108]: `def window_ok(sched, root=None, stage=None, own=None) -> dict`
- **function `verify_freeze_g`** [L111-128]: `def verify_freeze_g(out, repo=None) -> dict`
- **function `preflight`** [L131-148]: `def preflight(out, stage, auth, sched, repo=None) -> dict`
- **function `_git`** [L152-153]: `def _git(repo, *args) -> bytes`
- **function `s0`** [L156-181]: `def s0(repo, r_ref, h_exec) -> dict`
- **function `freeze_g`** [L184-207]: `def freeze_g(out, repo, h_exec, dry_report, pf_record) -> dict`
- **function `ledger_read`** [L211-215]: `def ledger_read(path) -> dict`
- **function `ledger_append`** [L218-229]: `def ledger_append(path, label, job, stage, cpu_s, source, world=None, master=None) -> dict`
- **function `central`** [L232-235]: `def central(stage, k=None) -> float`
- **function `meter_caps`** [L238-247]: `def meter_caps(stage, k=None) -> dict`
- **function `output_cap`** [L250-252]: `def output_cap(kind) -> int`
- **function `marker_replace`** [L255-266]: `def marker_replace(path, obj, retries=5, sleep_s=0.2) -> None`
- **function `outcome_g`** [L270-275]: `def outcome_g(state) -> dict`
- **function `licence_g`** [L278-288]: `def licence_g(oc, fill, world) -> str`
- **function `terminal_result`** [L291-304]: `def terminal_result(world_dir, w, status, stage, gate, details, p1_passed) -> Path`
- **function `export_g`** [L307-324]: `def export_g(world_dir, result, oc, ann, fill, ratio_files) -> Path`
- **function `_accepted`** [L327-331]: `def _accepted(path, keys, want) -> bool`
- **function `release_barrier`** [L334-349]: `def release_barrier(store) -> dict`

