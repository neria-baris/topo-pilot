# `tools/hwsu/hwsu_dry.py`

- Source: [tools/hwsu/hwsu_dry.py](../../../../../tools/hwsu/hwsu_dry.py)
- Kind: python
- Lines: 281

## Module docstring

> HWSU OF dry run DRO1-DRO4 and run_dro (API.md §10; protocol §9). Synthetic worlds and roots only;
> scope hwsu-dry-v1 and the dry seeds. DRO5-DRO9 and the J11 reader fixture live in hwsu_dry_b
> (split by size, API erratum) and are reachable here as hwsu_dry.<name>.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 7, via same directory)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 8, via same directory)
- `import hwsu_freeze` -> [tools/hwsu/hwsu_freeze.py](hwsu_freeze.py.md) (line 9, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 10, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](hwsu_oracle.py.md) (line 11, via same directory)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](hwsu_pairs.py.md) (line 12, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 13, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 20, via unique basename)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../hwsb/hwsb_dry.py.md) (line 21, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 22, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `import hwsu_dry` -> itself (line 252, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 14)
- `fractions` (lines 17)
- `importlib` (lines 243)
- `itertools` (lines 15)
- `json` (lines 16)
- `pathlib` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 245: `hwsu_dry_b` -> [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md)

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 19, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 18, import)
- [tests/hwsu/test_b_of_registry.py](../../tests/hwsu/test_b_of_registry.py.md) (line 34, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 151, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 7, import)

## Top-level constants

- `CASES`
- `SEEDS`

## Classes and functions

- **function `tiny_world`** [L31-40]: `def tiny_world() -> dict`
- **function `nonreversible_chain`** [L43-49]: `def nonreversible_chain() -> dict`
- **function `_w`** [L52-56]: `def _w(path, text) -> Path`
- **function `_h`** [L59-60]: `def _h(path) -> str`
- **function `synthetic_root`** [L63-90]: `def synthetic_root(base) -> dict`
- **function `tiny_pairs`** [L93-96]: `def tiny_pairs(n, block=0)`
- **function `dro1`** [L99-134]: `def dro1(base) -> dict`
- **function `_law`** [L137-150]: `def _law(P, kern)` - Exact law of the prefix given the suffix from a kernel dict (API.md §2.1).
- **function `dro2`** [L153-184]: `def dro2(base) -> dict`
- **function `dro3`** [L187-213]: `def dro3(base) -> dict`
- **function `dro4`** [L216-236]: `def dro4(base) -> dict`
- **function `__getattr__`** [L242-248]: `def __getattr__(name)`
- **function `run_dro`** [L251-281]: `def run_dro(out=uc.DRY_STORE, only=None) -> dict`

