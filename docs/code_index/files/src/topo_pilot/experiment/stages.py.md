# `src/topo_pilot/experiment/stages.py`

- Source: [src/topo_pilot/experiment/stages.py](../../../../../../src/topo_pilot/experiment/stages.py)
- Kind: python
- Lines: 169

## Module docstring

> Stage registry and the W0 stage S0 (environment and contract sanity).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, GateCheck, GateReport, StageFailure, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 17, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 26, via relative)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `abc` (lines 13)
- `collections` (lines 14)
- `hashlib` (lines 9)
- `re` (lines 10)
- `subprocess` (lines 11)
- `sys` (lines 12)
- `typing` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/__init__.py](__init__.py.md) (line 13, import)
- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 29, import)
- [src/topo_pilot/experiment/s1.py](s1.py.md) (line 32, import)
- [src/topo_pilot/experiment/s2.py](s2.py.md) (line 47, import)
- [src/topo_pilot/experiment/s3.py](s3.py.md) (line 43, import)
- [src/topo_pilot/experiment/s4.py](s4.py.md) (line 30, import)
- [src/topo_pilot/experiment/s6.py](s6.py.md) (line 53, import)
- [src/topo_pilot/experiment/s7.py](s7.py.md) (line 38, import)
- [src/topo_pilot/experiment/s8.py](s8.py.md) (line 55, import)
- [src/topo_pilot/experiment/x4.py](x4.py.md) (line 41, import)
- [tests/experiment/test_runner.py](../../../tests/experiment/test_runner.py.md) (line 24, import)
- [tests/integration/_mini_pipeline.py](../../../tests/integration/_mini_pipeline.py.md) (line 22, import)

## Top-level constants

- `STAGE_REGISTRY`
- `_PYTEST_TIMING`

## Classes and functions

- **class `Stage(ABC)`** [L31-49] - A run stage: ``plan`` lists job descriptors; ``execute`` runs one, returns artifact ids.
- **method `Stage.plan`** [L43-44]: `def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]` decorators: @abstractmethod - Job descriptors for this stage, in priority order.
- **method `Stage.execute`** [L47-49]: `def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig, store: ArtifactStore) -> list[str]` decorators: @abstractmethod - Run one job; return the ids of the artifacts it wrote.
- **function `register_stage`** [L55-58]: `def register_stage(cls: type[Stage]) -> type[Stage]` - Class decorator adding a stage to :data:`STAGE_REGISTRY` under its ``stage_id``.
- **function `tool_line`** [L61-65]: `def tool_line(output: str) -> str` - Last output line of a tool run, with pytest's wall time removed (``95 passed in 3.7s``
- **function `run_tool`** [L68-72]: `def run_tool(cmd: list[str], cfg: ResolvedConfig, timeout: int = 600) -> tuple[bool, str]` - Run ``cmd`` in the repository; returns (exit code 0, :func:`tool_line`).
- **function `save_tool_gate`** [L75-89]: `def save_tool_gate(store: ArtifactStore, cfg: ResolvedConfig, stage: str, gate_id: str, checks: Sequence[GateCheck], parents: Sequence[str]) -> str` - Save a GateReport whose checks embed tool output (test counts, file counts).
- **class `S0Stage(Stage)`** [L93-114] decorators: @register_stage - S0: the store is initialised, the environment lock exists, the contracts suite passes,
- **method `S0Stage.plan`** [L100-101]: `def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]`
- **method `S0Stage.execute`** [L103-114]: `def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig, store: ArtifactStore) -> list[str]`
- **function `latest_gate_verdicts`** [L117-132]: `def latest_gate_verdicts(store: ArtifactStore, stage_id: str) -> dict[str, tuple[str, ...]]` - Per gate id of ``stage_id``: the verdicts of its most recent report(s).
- **function `_check_requirements`** [L135-145]: `def _check_requirements(stage: Stage, store: ArtifactStore) -> None` - Raise ``GATE_FAILED`` unless every gate of every required stage passed (or was waived).
- **function `run_stage`** [L148-169]: `def run_stage(stage_id: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[str]` - Run every planned job of ``stage_id`` inline; raises ``INVALID_CONFIG`` for an unknown

