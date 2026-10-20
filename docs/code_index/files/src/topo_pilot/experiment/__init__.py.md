# `src/topo_pilot/experiment/__init__.py`

- Source: [src/topo_pilot/experiment/__init__.py](../../../../../../src/topo_pilot/experiment/__init__.py)
- Kind: python
- Lines: 16

## Module docstring

> Public API of ``topo_pilot.experiment`` (W0 skeleton: CLI, config layering, stage registry).

## Imports

### Internal (repo files)

- `from . import s1` -> [src/topo_pilot/experiment/s1.py](s1.py.md) (line 3, via relative)
- `from . import s2` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 4, via relative)
- `from . import s3` -> [src/topo_pilot/experiment/s3.py](s3.py.md) (line 5, via relative)
- `from . import s4` -> [src/topo_pilot/experiment/s4.py](s4.py.md) (line 6, via relative)
- `from . import s6` -> [src/topo_pilot/experiment/s6.py](s6.py.md) (line 7, via relative)
- `from . import s7` -> [src/topo_pilot/experiment/s7.py](s7.py.md) (line 8, via relative)
- `from . import s8` -> [src/topo_pilot/experiment/s8.py](s8.py.md) (line 9, via relative)
- `from . import x4` -> [src/topo_pilot/experiment/x4.py](x4.py.md) (line 10, via relative)
- `from .cli import main, status_lines` -> [src/topo_pilot/experiment/cli.py](cli.py.md) (line 11, via relative)
- `from .config import ResolvedConfig, load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 12, via relative)
- `from .stages import STAGE_REGISTRY, Stage, register_stage, run_stage` -> [src/topo_pilot/experiment/stages.py](stages.py.md) (line 13, via relative)

### External (third-party)

- none

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/executors/entry.py](../executors/entry.py.md) (line 57, dynamic)
- [tests/executors/stub_stage.py](../../../tests/executors/stub_stage.py.md) (line 19, import)
- [tests/experiment/test_runner.py](../../../tests/experiment/test_runner.py.md) (line 19, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 17, import)
- [tests/experiment/test_s8_e4.py](../../../tests/experiment/test_s8_e4.py.md) (line 13, import)
- [tests/experiment/test_x4.py](../../../tests/experiment/test_x4.py.md) (line 9, import)
- [tests/integration/_mini_pipeline.py](../../../tests/integration/_mini_pipeline.py.md) (line 21, import)
- [tests/integration/test_s1.py](../../../tests/integration/test_s1.py.md) (line 16, import)
- [tests/integration/test_s2_mini.py](../../../tests/integration/test_s2_mini.py.md) (line 20, import)

## Top-level constants

- none

## Classes and functions

- none

