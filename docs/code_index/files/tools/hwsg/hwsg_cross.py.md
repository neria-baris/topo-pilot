# `tools/hwsg/hwsg_cross.py`

- Source: [tools/hwsg/hwsg_cross.py](../../../../../tools/hwsg/hwsg_cross.py)
- Kind: python
- Lines: 200

## Module docstring

> HWSG cross-world readings: generality, annotations, capture, similarity, licences (API.md §8;
> protocol §2.7, §7.1 X, §7.4). Inputs are the sha256-bound RESULT.json files of the worlds.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 11, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 13, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 14, via unique basename)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 173, via same directory) (inside a function)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 174, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 8)
- `json` (lines 7)
- `pathlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsg/test_a_cross.py](../../tests/hwsg/test_a_cross.py.md) (line 23, import)
- [tests/hwsg/test_a_outcomes_licences.py](../../tests/hwsg/test_a_outcomes_licences.py.md) (line 23, import)
- [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 8, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 6, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 240, import)

## Top-level constants

- `CROSS`
- `LIC`

## Classes and functions

- **function `_bound_sha`** [L21-26]: `def _bound_sha(wd, rel)`
- **function `load_world`** [L29-59]: `def load_world(store, w) -> dict`
- **function `general`** [L62-72]: `def general(worlds) -> dict`
- **function `_ep`** [L75-76]: `def _ep(worlds) -> list`
- **function `annotations`** [L79-86]: `def annotations(worlds) -> list`
- **function `_models`** [L89-90]: `def _models(w) -> dict`
- **function `capture`** [L93-109]: `def capture(worlds) -> dict`
- **function `similarity`** [L112-141]: `def similarity(worlds, seed=None) -> dict`
- **function `licence`** [L144-164]: `def licence(reading, fill=None) -> str`
- **class `_Fill(dict)`** [L167-169]
- **method `_Fill.__missing__`** [L168-169]: `def __missing__(self, key)`
- **function `run_cross`** [L172-200]: `def run_cross(out, auth, sched, job) -> dict`

