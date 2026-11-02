# `tools/hwsd/hwsd_driver.py`

- Source: [tools/hwsd/hwsd_driver.py](../../../../../tools/hwsd/hwsd_driver.py)
- Kind: python
- Lines: 361

## Module docstring

> HWSD driver: common job helpers and the jobs KD, SAMPLE, CLOSE, inventory (API.md §11, §15.1,
> §15.2). SCORE, SUMMARY and the CLI live in hwsd_jobs (split by size, API erratum) and are
> re-exported here under their API names. Every job runs its gates inside one bound_hwsd().

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import hwsb_records` -> [tools/hwsb/hwsb_records.py](../hwsb/hwsb_records.py.md) (line 13, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 14, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 15, via unique basename)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 16, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 17, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 18, via same directory)
- `import hwsd_known` -> [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 19, via same directory)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 20, via same directory)
- `import hwsd_registry` -> [tools/hwsd/hwsd_registry.py](hwsd_registry.py.md) (line 21, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 22, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 23, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 28, via package root)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../c1prime/c1_cert.py.md) (line 143, via unique basename) (inside a function)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 327, via same directory) (inside a function)
- `from hwsd_jobs import main, run_score, run_summary` -> [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 358, via same directory)

### External (third-party)

- `torch` (lines 144)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `json` (lines 8)
- `pathlib` (lines 11)
- `time` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 274, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 17, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 141, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 206, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 272, import)

## Top-level constants

- `REFUSE`

## Classes and functions

- **function `_files_under`** [L33-35]: `def _files_under(d) -> set`
- **function `audit_gate`** [L38-43]: `def audit_gate(out) -> None`
- **function `run_gates_d`** [L46-68]: `def run_gates_d(out, steps, soft=()) -> list` - hwsc_records.run_gates_c, except that a gate named in `soft` records its status and does
- **function `paused`** [L71-76]: `def paused(out, stage, t0, fn, cont=None)`
- **function `end_obligation`** [L79-84]: `def end_obligation(out, job, attempt, reservation_id=None) -> Path`
- **function `refuse_exit`** [L87-92]: `def refuse_exit(out, ret, job, attempt)` - J10 item 2: a refused job that wrote anything into the store still writes its obligation.
- **function `first_bad`** [L95-97]: `def first_bad(recs, soft=())`
- **function `run_kd`** [L101-108]: `def run_kd(out, auth, sched, job, attempt=1, cont=None) -> dict`
- **function `_kd_accept_ok`** [L112-116]: `def _kd_accept_ok(out, kd_accept) -> bool`
- **function `_h1d`** [L119-157]: `def _h1d(out, ctx) -> dict`
- **function `_regd`** [L160-170]: `def _regd(out, ctx, root, scratch) -> dict`
- **function `_close_res`** [L173-182]: `def _close_res(out, ctx, job, attempt) -> None` - J8: the obligation right after the four tables, then the reservation end (new code).
- **function `_s3d`** [L185-203]: `def _s3d(out, ctx, job, attempt) -> dict`
- **function `_h2d`** [L206-217]: `def _h2d(out, ctx) -> dict`
- **function `_oracle`** [L220-231]: `def _oracle(out, ctx) -> dict`
- **function `_b4`** [L234-244]: `def _b4(out, ctx) -> dict`
- **function `_lgate`** [L247-251]: `def _lgate(out, ctx) -> dict`
- **function `run_sample`** [L254-303]: `def run_sample(out, auth, sched, job, attempt, kd_accept, root=dc.ROOT, scratch=dc.SCRATCH, cont=None) -> dict`
- **function `state_from_gates`** [L307-323]: `def state_from_gates(out) -> dict` - The outcome_d state keys (decision 10) read from GATES.jsonl and the SCORE folders.
- **function `run_close`** [L326-343]: `def run_close(out, status, reason, job, attempt) -> dict`
- **function `inventory`** [L346-355]: `def inventory(root, save=None, compare=None) -> dict`

