# `tools/hwsd/hwsd_known.py`

- Source: [tools/hwsd/hwsd_known.py](../../../../../tools/hwsd/hwsd_known.py)
- Kind: python
- Lines: 289

## Module docstring

> HWSD G0d and the known cases KD0-KD6 (API.md §9; protocol §6, §9). hwsd_driver and hwsd_dry are
> imported lazily inside run_kd (API §0 dependency order).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 6, via same directory)
- `import hwsb_kb` -> [tools/hwsb/hwsb_kb.py](../hwsb/hwsb_kb.py.md) (line 17, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 18, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 19, via unique basename)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 20, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 21, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 22, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 23, via same directory)
- `import hwsd_readers` -> [tools/hwsd/hwsd_readers.py](hwsd_readers.py.md) (line 24, via same directory)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 25, via same directory)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 26, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)
- `from hwsd_known2 import c0_val_line, kd2, repro_c` -> [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 37, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 192, via unique basename) (inside a function)
- `import hwsd_dry` -> [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 231, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 14)
- `hashlib` (lines 7)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 15)
- `re` (lines 10)
- `subprocess` (lines 11)
- `sys` (lines 12)
- `time` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_learning.py](../../tests/hwsd/test_a_learning.py.md) (line 25, import)
- [tests/hwsd/test_b_guard_search.py](../../tests/hwsd/test_b_guard_search.py.md) (line 14, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 19, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 19, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 38, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 60, import)

## Top-level constants

- `SKIP_DIRS`
- `TEXT_SUFFIXES`

## Classes and functions

- **function `_skip_dir`** [L41-45]: `def _skip_dir(parent, name, root, scratch) -> bool`
- **function `seed_search_d`** [L48-63]: `def seed_search_d(root, needles, scratch=dc.SCRATCH) -> list`
- **function `_ints`** [L66-67]: `def _ints(track) -> list`
- **function `needles_d`** [L70-72]: `def needles_d(namespace) -> dict`
- **function `_reserved`** [L75-77]: `def _reserved(track) -> set`
- **function `overlap_check`** [L80-82]: `def overlap_check(namespace) -> dict`
- **function `_hash`** [L85-87]: `def _hash(path, exempt=False) -> str`
- **function `_sha_check`** [L90-96]: `def _sha_check(root, rel, want, absent=AUTH_REFUSE, differ='FAIL_TECHNICAL/AUTHORITY', exempt=False) -> None`
- **function `g0d`** [L99-146]: `def g0d(out, stage, auth=None, sched=None, root=dc.ROOT) -> dict`
- **function `ident_d`** [L150-187]: `def ident_d(masters=dc.MASTERS, steps=dc.STEPS, hwsc=dc.HWSC_STORE, handoff=None) -> dict`
- **function `kd5`** [L191-207]: `def kd5() -> dict`
- **function `kd6`** [L210-227]: `def kd6(job) -> dict`
- **function `run_kd`** [L230-284]: `def run_kd(out, auth, sched, job, attempt=1, cont=None) -> dict`
- **function `_audit`** [L287-289]: `def _audit() -> dict`

