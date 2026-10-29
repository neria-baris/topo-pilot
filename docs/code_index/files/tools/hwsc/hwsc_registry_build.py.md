# `tools/hwsc/hwsc_registry_build.py`

- Source: [tools/hwsc/hwsc_registry_build.py](../../../../../tools/hwsc/hwsc_registry_build.py)
- Kind: python
- Lines: 171

## Module docstring

> HWSC registry build and obligation record (API.md §4 `build`, `obligation`; split from
> hwsc_registry by size, API erratum). A mirror of nd_registry.build with the stage-C sources;
> every source is looked up at call time so that the dry run and tests can replace it.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 12, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 13, via unique basename)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 14, via same directory)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 15, via unique basename)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 16, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 18, via unique basename)

### External (third-party)

- `numpy` (lines 17)
- `psutil` (lines 26)

### Standard library

- `__future__` (lines 5)
- `hashlib` (lines 8)
- `pathlib` (lines 10)
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

- [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 381, import)

## Top-level constants

- `ND_TAGS`

## Classes and functions

- **function `_peak_memory`** [L24-31]: `def _peak_memory()`
- **function `_default_sources`** [L34-52]: `def _default_sources(root, scratch, run_dir, handoff, store, own_expected) -> dict`
- **function `_summary`** [L55-57]: `def _summary(r) -> dict`
- **function `build`** [L60-153]: `def build(version, out_dir, root=None, scratch=None, handoff=None, own_expected=None, extra=None, sources=None) -> dict`
- **function `obligation`** [L156-171]: `def obligation(store, extra_paths=()) -> dict`

