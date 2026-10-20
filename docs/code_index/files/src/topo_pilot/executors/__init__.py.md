# `src/topo_pilot/executors/__init__.py`

- Source: [src/topo_pilot/executors/__init__.py](../../../../../../src/topo_pilot/executors/__init__.py)
- Kind: python
- Lines: 12

## Module docstring

> Public API of ``topo_pilot.executors`` (see SPEC.md): run a job locally, through a portable
> bundle, or over ssh.

## Imports

### Internal (repo files)

- `from .base import EXECUTOR_REGISTRY, Executor, JobHandle, JobSpec` -> [src/topo_pilot/executors/base.py](base.py.md) (line 4, via relative)
- `from .bundle import BundleExecutor` -> [src/topo_pilot/executors/bundle.py](bundle.py.md) (line 5, via relative)
- `from .entry import entry` -> [src/topo_pilot/executors/entry.py](entry.py.md) (line 6, via relative)
- `from .local import LocalExecutor` -> [src/topo_pilot/executors/local.py](local.py.md) (line 7, via relative)
- `from .notebook import NotebookExporter` -> [src/topo_pilot/executors/notebook.py](notebook.py.md) (line 8, via relative)
- `from .ssh import SSHExecutor` -> [src/topo_pilot/executors/ssh.py](ssh.py.md) (line 9, via relative)

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

- [tests/executors/exec_helpers.py](../../../tests/executors/exec_helpers.py.md) (line 9, import)
- [tests/executors/test_bundle.py](../../../tests/executors/test_bundle.py.md) (line 14, import)
- [tests/executors/test_exporter.py](../../../tests/executors/test_exporter.py.md) (line 12, import)
- [tests/executors/test_exporter.py](../../../tests/executors/test_exporter.py.md) (line 82, import)
- [tests/executors/test_local.py](../../../tests/executors/test_local.py.md) (line 11, import)
- [tests/executors/test_static.py](../../../tests/executors/test_static.py.md) (line 36, import)

## Top-level constants

- none

## Classes and functions

- none

