# `tools/hwsg/hwsg_dry2.py`

- Source: [tools/hwsg/hwsg_dry2.py](../../../../../tools/hwsg/hwsg_dry2.py)
- Kind: python
- Lines: 243

## Module docstring

> HWSG dry run, part 2: DRG1, DRG2, DRG9, DRG12-DRG14 and the DRY report (API.md §16; §10.1).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import hwsg_cross` -> [tools/hwsg/hwsg_cross.py](hwsg_cross.py.md) (line 6, via same directory)
- `import hwsg_dry` -> [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 7, via same directory)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 8, via same directory)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 9, via same directory)
- `import hwsg_registry` -> [tools/hwsg/hwsg_registry.py](hwsg_registry.py.md) (line 10, via same directory)
- `import hwsg_train` -> [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 11, via same directory)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 18, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 22, via unique basename)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 3)
- `hashlib` (lines 12)
- `json` (lines 13)
- `os` (lines 14)
- `pathlib` (lines 16)
- `tempfile` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `INC`

## Classes and functions

- **function `_res`** [L27-28]: `def _res(checks, **extra) -> dict`
- **function `_hist`** [L31-37]: `def _hist(path, n=4, seed=0) -> dict`
- **function `_entry`** [L40-43]: `def _entry(store, rel, cls='K4b history table', reader='k4b_history_table') -> dict`
- **function `_obl`** [L46-49]: `def _obl(store, entries, name='REGISTRY_OBLIGATION.json', utc='2026-11-02T00:00:00Z') -> None`
- **function `drg9`** [L52-105]: `def drg9() -> dict`
- **function `drg12`** [L108-151]: `def drg12() -> dict`
- **function `drg13`** [L154-165]: `def drg13() -> dict`
- **function `drg14`** [L168-191]: `def drg14() -> dict`
- **function `drg2`** [L194-199]: `def drg2() -> dict`
- **function `drg1`** [L202-217]: `def drg1() -> dict` - Record-side pipeline on synthetic inputs; geometry-dependent K4b gates are planted.
- **function `run_dry`** [L220-243]: `def run_dry(out, auth=None, sched=None, job='dry', repo=None) -> dict`

