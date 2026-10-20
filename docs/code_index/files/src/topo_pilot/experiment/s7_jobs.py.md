# `src/topo_pilot/experiment/s7_jobs.py`

- Source: [src/topo_pilot/experiment/s7_jobs.py](../../../../../../src/topo_pilot/experiment/s7_jobs.py)
- Kind: python
- Lines: 34

## Module docstring

> Dispatch of the S7 analysis jobs (D-047); each writes one MetricRecords.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRecords` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 5, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 7, via relative)
- `from .s7_dev import DevData` -> [src/topo_pilot/experiment/s7_dev.py](s7_dev.py.md) (line 13, via relative) (inside a function)
- `from .s7_controls import ControlsJob` -> [src/topo_pilot/experiment/s7_controls.py](s7_controls.py.md) (line 19, via relative) (inside a function)
- `from .s7_probes import ProbesJob` -> [src/topo_pilot/experiment/s7_probes.py](s7_probes.py.md) (line 23, via relative) (inside a function)
- `from .s7_circular import CircularJob` -> [src/topo_pilot/experiment/s7_circular.py](s7_circular.py.md) (line 27, via relative) (inside a function)
- `from .s7_sensitivity import SensitivityJob` -> [src/topo_pilot/experiment/s7_sensitivity.py](s7_sensitivity.py.md) (line 31, via relative) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7.py](s7.py.md) (line 202, import)

## Top-level constants

- none

## Classes and functions

- **function `run`** [L10-34]: `def run(kind: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[str]` - Run S7 job ``kind``: dev_extract, controls, probes, circular or sensitivity.

