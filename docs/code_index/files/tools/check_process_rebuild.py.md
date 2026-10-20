# `tools/check_process_rebuild.py`

- Source: [tools/check_process_rebuild.py](../../../../tools/check_process_rebuild.py)
- Kind: python
- Lines: 63

## Module docstring

> Rebuild every stored TransitionSpec and EmissionSpec and compare id + payload checksum.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, MemoryBackend, SeedTree, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.process import EmissionConfig, ProcessStage, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../src/topo_pilot/process/__init__.py.md) (line 26, via package root)

### External (third-party)

- none

### Standard library

- `__future__` (lines 11)
- `argparse` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

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

- `PROCESS_KEYS`

## Classes and functions

- **function `main`** [L31-59]: `def main() -> int`

