# `src/topo_pilot/experiment/x4_inputs.py`

- Source: [src/topo_pilot/experiment/x4_inputs.py](../../../../../../src/topo_pilot/experiment/x4_inputs.py)
- Kind: python
- Lines: 203

## Module docstring

> Stage X4 inputs: plain arrays per run, resolved from the store (consumer "experiment").

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import SpaceBuilder, require_same_ids` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import ActivationSet, ArtifactStore, Checkpoint, ErrorCode, HistoryIndex, MetricRecords, StageFailure, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.learner import load_model` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 30, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 32, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 33, via relative)
- `from .s4_analysis import AnalysisJob` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 34, via relative)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 11)
- `collections` (lines 14)
- `dataclasses` (lines 15)
- `logging` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x4.py](x4.py.md) (line 42, import)

## Top-level constants

- `CONDITION_OF`
- `CONS`

## Classes and functions

- **class `X4Panel`** [L43-50] decorators: @dataclass(frozen=True, eq=False) - One panel of one run at one checkpoint: ``Z [M, d]`` (resid_post_3), ``ln_out [M, d]``
- **class `X4Run`** [L54-71] decorators: @dataclass(frozen=True, eq=False) - Everything X4 needs from one training run (see experiment/SPEC.md, Stage X4).
- **function `_fail`** [L74-75]: `def _fail(check: str, detail: str, aid: str | None = None) -> StageFailure`
- **class `StoreResolver`** [L78-203] - ``resolver(source_stage) -> (runs, missing run keys)`` over the stored runs of a stage.
- **method `StoreResolver.__init__`** [L81-84]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `StoreResolver.__call__`** [L86-100]: `def __call__(self, source: str) -> tuple[list[X4Run], list[tuple[str, str, int]]]`
- **method `StoreResolver._run`** [L103-127]: `def _run(self, aj: AnalysisJob, key: tuple[str, str, int], source: str, stored: dict, analysis_id: str | None) -> X4Run`
- **method `StoreResolver._weights`** [L129-138]: `def _weights(self, act: ActivationSet, step: int, aid: str) -> tuple[Weights, str]`
- **method `StoreResolver._panels`** [L140-156]: `def _panels(self, act: ActivationSet, aid: str) -> dict[int, X4Panel]`
- **method `StoreResolver._oracle`** [L158-180]: `def _oracle(self, aj: AnalysisJob, inputs: dict, final_aid: str, panels: dict) -> dict[int, dict[str, np.ndarray]]`
- **method `StoreResolver._learning_gate`** [L183-188]: `def _learning_gate(self, source: str, key: tuple) -> tuple[bool | None, str | None]`
- **method `StoreResolver._stored_S`** [L190-203]: `def _stored_S(self, source: str) -> tuple[dict, str | None]` - S of the primary hook per (world, cond, seed, step, panel) from the newest source

