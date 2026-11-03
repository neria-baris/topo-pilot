# `tools/hwsg/hwsg_handoff.py`

- Source: [tools/hwsg/hwsg_handoff.py](../../../../../tools/hwsg/hwsg_handoff.py)
- Kind: python
- Lines: 115

## Module docstring

> HWSG WORLD_HANDOFF: build, write, load, view for stage-C functions (API.md §3; protocol §2.6).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 11, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 12, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 13, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `fractions` (lines 8)
- `hashlib` (lines 6)
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

- [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 42, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 8, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 8, import)
- [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 88, import)
- [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 241, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 133, import)

## Top-level constants

- `FILE`
- `IDENT`

## Classes and functions

- **function `build`** [L19-26]: `def build(w, o_result) -> dict`
- **function `write`** [L29-32]: `def write(world_dir, handoff) -> str`
- **function `_recorded_sha`** [L35-47]: `def _recorded_sha(store, d)`
- **function `load`** [L50-83]: `def load(w, store=None, expected_sha256=None) -> dict`
- **function `_forbidden`** [L86-96]: `def _forbidden(obj, names) -> list`
- **function `as_hwsc`** [L99-104]: `def as_hwsc(h) -> dict`
- **function `loader`** [L107-115]: `def loader(key)` - Function with the hwsc_config.load_handoff signature returning the stage-C view.

