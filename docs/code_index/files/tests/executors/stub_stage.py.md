# `tests/executors/stub_stage.py`

- Source: [tests/executors/stub_stage.py](../../../../../tests/executors/stub_stage.py)
- Kind: python
- Lines: 46

## Module docstring

> Stub stage for the executors tests, imported in subprocesses via ``import_modules``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, GateCheck, GateReport, MetricRecords, MetricRow, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 10, via package root)
- `from topo_pilot.experiment import ResolvedConfig, Stage, register_stage` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 19, via package root)

### External (third-party)

- none

### Standard library

- `collections` (lines 7)
- `typing` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/executors/test_bundle.py](test_bundle.py.md) (line 53, import)

## Top-level constants

- none

## Classes and functions

- **class `StubStage(Stage)`** [L23-46] decorators: @register_stage - Writes one tiny artifact so executors can be tested without science code.
- **method `StubStage.plan`** [L28-29]: `def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]`
- **method `StubStage.execute`** [L31-46]: `def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig, store: ArtifactStore) -> list[str]`

