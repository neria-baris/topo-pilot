# `tools/hwsd/hwsd_jobs.py`

- Source: [tools/hwsd/hwsd_jobs.py](../../../../../tools/hwsd/hwsd_jobs.py)
- Kind: python
- Lines: 288

## Module docstring

> HWSD jobs SCORE and SUMMARY and the CLI (API.md §11, §15.3, §15.4; split from hwsd_driver by
> size, API erratum; the driver re-exports run_score, run_summary and main). hwsd_driver is
> imported lazily inside the functions (the hwsc_jobs pattern).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import hwsb_driver` -> [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 14, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 15, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 16, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 17, via same directory)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 18, via same directory)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 19, via same directory)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 20, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 21, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 22, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 23, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 24, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 26, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 27, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 28, via unique basename)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.contracts.backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 31, via package root)
- `from hwsd_known import ident_d` -> [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 60, via same directory) (inside a function)
- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 97, via same directory) (inside a function)
- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 160, via same directory) (inside a function)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 161, via same directory) (inside a function)
- `import hwsd_driver` -> [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 226, via same directory) (inside a function)
- `import hwsd_dry` -> [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 264, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 25)

### Standard library

- `__future__` (lines 5)
- `argparse` (lines 8)
- `fractions` (lines 11)
- `json` (lines 9)
- `pathlib` (lines 12)
- `time` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 16, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 358, import)

## Top-level constants

- `OPTS`
- `REFUSE`

## Classes and functions

- **function `_npz`** [L36-38]: `def _npz(path) -> dict`
- **function `_accept_sample_ok`** [L41-46]: `def _accept_sample_ok(out, acc) -> bool`
- **function `_archive_interrupted`** [L49-55]: `def _archive_interrupted(out, job, attempt, j) -> None`
- **function `_score_ident`** [L58-75]: `def _score_ident(out, accept, j) -> dict`
- **function `_score_ctx`** [L78-93]: `def _score_ctx(out, j) -> dict`
- **function `run_score`** [L96-139]: `def run_score(out, auth, sched, job, attempt, master, accept_sample, cont=None) -> dict`
- **function `_shared`** [L142-145]: `def _shared(out) -> dict`
- **function `_accept_scores_ok`** [L148-156]: `def _accept_scores_ok(out, accepts) -> bool`
- **function `run_summary`** [L159-203]: `def run_summary(out, auth, sched, job, attempt, accepts, cont=None) -> dict`
- **function `_load`** [L207-208]: `def _load(p)`
- **function `_exit`** [L211-217]: `def _exit(res) -> int`
- **function `main`** [L225-288]: `def main(argv=None) -> int`

