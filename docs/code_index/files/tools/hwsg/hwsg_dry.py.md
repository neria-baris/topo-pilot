# `tools/hwsg/hwsg_dry.py`

- Source: [tools/hwsg/hwsg_dry.py](../../../../../tools/hwsg/hwsg_dry.py)
- Kind: python
- Lines: 213

## Module docstring

> HWSG dry run, part 1: synthetic cases DRG3-DRG8, DRG10, DRG11 (API.md §16; protocol §10.1).
> Synthetic inputs only: no real master, stream, store write or array file under the project root.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 7, via same directory)
- `import hwsg_cross` -> [tools/hwsg/hwsg_cross.py](hwsg_cross.py.md) (line 8, via same directory)
- `import hwsg_known` -> [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 9, via same directory)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 10, via same directory)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 16, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 17, via unique basename)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 18, via unique basename)
- `import hwsc_outcome` -> [tools/hwsc/hwsc_outcome.py](../hwsc/hwsc_outcome.py.md) (line 19, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 20, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)
- `from topo_pilot.process import TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 25, via package root)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 151, via package root) (inside a function)
- `from topo_pilot.contracts.backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 152, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 4)
- `dataclasses` (lines 11)
- `fractions` (lines 13)
- `pathlib` (lines 14)
- `tempfile` (lines 133)
- `types` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 7, import)

## Top-level constants

- none

## Classes and functions

- **function `_res`** [L28-29]: `def _res(checks, **extra) -> dict`
- **function `_raises`** [L32-37]: `def _raises(fn, status=None) -> bool`
- **function `drg3`** [L40-71]: `def drg3() -> dict`
- **function `drg4`** [L74-78]: `def drg4() -> dict`
- **function `_model`** [L81-84]: `def _model(L, U, Fm, Fp)`
- **function `_overall`** [L87-90]: `def _overall(rows) -> dict`
- **function `drg5`** [L93-111]: `def drg5() -> dict`
- **function `drg6`** [L114-120]: `def drg6() -> dict`
- **function `_w`** [L123-126]: `def _w(tag, outcome, endpoint=True, p1=True, status=None, ratio=None, draws=None)`
- **function `drg7`** [L129-139]: `def drg7() -> dict`
- **function `drg8`** [L142-164]: `def drg8() -> dict`
- **function `_ratio_world`** [L167-176]: `def _ratio_world(tag, rho_l, rho_u, rho=0.8, n=5000, seed=1)`
- **function `drg10`** [L179-198]: `def drg10() -> dict`
- **function `drg11`** [L201-210]: `def drg11() -> dict`

