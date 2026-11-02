# `tools/hwsd/hwsd_dry.py`

- Source: [tools/hwsd/hwsd_dry.py](../../../../../tools/hwsd/hwsd_dry.py)
- Kind: python
- Lines: 398

## Module docstring

> hwsd synthetic dry run: helpers, DRD1, DRD4/KD4 (seq_cases, plant_acts), run_dry (API.md §12).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 10, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 21, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 22, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 23, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../hwsb/hwsb_dry.py.md) (line 24, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 25, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 26, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 27, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 28, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 29, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 30, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 31, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 33, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 34, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 36, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 37, via same directory)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 38, via same directory)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 39, via same directory)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](hwsd_statements.py.md) (line 40, via same directory)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 41, via same directory)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 43, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 44, via package root)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 252, via unique basename) (inside a function)
- `import hwsd_dry2` -> [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 363, via same directory) (inside a function)
- `import hwsd_dry3` -> [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 364, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 32)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 18)
- `hashlib` (lines 11)
- `importlib` (lines 57)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 19)
- `shutil` (lines 14)
- `time` (lines 15)
- `traceback` (lines 16)
- `uuid` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 59: `dynamic: _LAZY[name]`

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_kd4.py](../../tests/hwsd/test_a_kd4.py.md) (line 30, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 100, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 33, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 41, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 266, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 233, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 50, import)

## Top-level constants

- `KD4_DEFAULT`
- `REGISTERED`
- `_EXPECT`
- `_LAZY`
- `_PROC`

## Classes and functions

- **function `__getattr__`** [L55-60]: `def __getattr__(name)`
- **function `_registered`** [L63-64]: `def _registered(s) -> bool`
- **function `_res`** [L67-69]: `def _res(ok, reading='EXACT', **details) -> dict`
- **function `case_dir`** [L72-75]: `def case_dir(out, case) -> Path`
- **function `fixture_root`** [L78-79]: `def fixture_root(job, case) -> Path`
- **function `fresh_fixture`** [L82-86]: `def fresh_fixture(job, case) -> Path` - A new empty folder under fixture_root (decision 6: never inside the hwsd-dry store).
- **function `_job`** [L89-90]: `def _job(ctx) -> str`
- **function `proc_star`** [L93-97]: `def proc_star() -> dict`
- **function `in_memory_rows`** [L100-103]: `def in_memory_rows(case, n, splits=dc.SPLITS, process=dc.PROCESS) -> dict`
- **function `_u`** [L106-108]: `def _u(ids) -> np.ndarray`
- **function `_g`** [L111-114]: `def _g(theta, a) -> np.ndarray`
- **function `plant_acts`** [L117-132]: `def plant_acts(case_id, table, m, params) -> np.ndarray` - Planted float64 activations [n, 128]: coordinates 0 and 1 carry the signal.
- **function `bounds_row`** [L135-150]: `def bounds_row(rec, arrays, step, Z=None) -> dict` - The statement row of one checkpoint: bootstraps on the dry seeds (inside a dry binding).
- **function `_case_ok`** [L166-176]: `def _case_ok(cid, row, delta4) -> bool`
- **function `seq_cases`** [L179-230]: `def seq_cases(out, params=None, cases=None, sequences=None, rows=3072) -> dict`
- **function `drd4`** [L233-237]: `def drd4(out, ctx) -> dict`
- **function `_train_tiny`** [L241-247]: `def _train_tiny(store, proc, plan, scope) -> dict`
- **function `drd1`** [L250-355]: `def drd1(out, ctx) -> dict` - The tiny-world pipeline: train, SAMPLE tables, H2-D, ORACLE-D, B4-TEST, LGATE, SCORE, SUMMARY.
- **function `run_dry`** [L359-398]: `def run_dry(out=dc.DRY_STORE, sched=None, only=None, job=None) -> dict`

