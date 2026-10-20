# `src/topo_pilot/analysis/spaces.py`

- Source: [src/topo_pilot/analysis/spaces.py](../../../../../../src/topo_pilot/analysis/spaces.py)
- Kind: python
- Lines: 221

## Module docstring

> SpaceBuilder: reference comparison spaces on the same histories (consumer "analysis").

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ActivationSet, ArtifactStore, EmissionSpec, ErrorCode, HistoryIndex, ObservationSet, OracleOutputs, StageFailure, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)
- `from topo_pilot.topology import NullClouds` -> [src/topo_pilot/topology/__init__.py](../topology/__init__.py.md) (line 21, via package root)
- `from .baselines import r2_points, r3_points, spectral_embedding` -> [src/topo_pilot/analysis/baselines.py](baselines.py.md) (line 23, via relative)
- `from .pointset import PointSet` -> [src/topo_pilot/analysis/pointset.py](pointset.py.md) (line 24, via relative)

### External (third-party)

- `numpy` (lines 7)

### Standard library

- `__future__` (lines 3)
- `typing` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 33, import)
- [src/topo_pilot/analysis/circular.py](circular.py.md) (line 23, import)
- [src/topo_pilot/analysis/discriminability.py](discriminability.py.md) (line 10, import)
- [src/topo_pilot/analysis/dynamics.py](dynamics.py.md) (line 12, import)

## Top-level constants

- `_COMPONENT`
- `_CONSUMER`
- `_F2_TOL`

## Classes and functions

- **function `_fail`** [L31-32]: `def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure`
- **class `SpaceBuilder`** [L35-221] - Builds :class:`PointSet` objects from stored artifacts.
- **method `SpaceBuilder.__init__`** [L57-59]: `def __init__(self, store: ArtifactStore)`
- **method `SpaceBuilder.world`** [L61-65]: `def world(self, world_id: str) -> PointSet` - The N states with the world distance as D, metric ``flat``.
- **method `SpaceBuilder.emission`** [L67-71]: `def emission(self, emission_id: str) -> PointSet` - The N rows of E as distributions, metric Hellinger.
- **method `SpaceBuilder._oracle`** [L73-88]: `def _oracle(self, oracle_id: str) -> tuple[OracleOutputs, HistoryIndex]`
- **method `SpaceBuilder._panel_rows`** [L90-96]: `def _panel_rows(self, oracle_id: str, panel: int)`
- **method `SpaceBuilder.beliefs`** [L98-104]: `def beliefs(self, oracle_id: str, which: Literal['b32', 'b1'], panel: int) -> PointSet` - Belief rows b^(32) or b^(1) of one panel, metric Hellinger.
- **method `SpaceBuilder.futures`** [L106-122]: `def futures(self, oracle_id: str, horizon: Literal[1, 2], panel: int) -> PointSet` - Next-symbol predictive F1 (= q) or flattened two-step F2 of one panel.
- **method `SpaceBuilder.null`** [L124-134]: `def null(self, like: PointSet, kind: Literal['iso', 'cov'], rng) -> PointSet` - Gaussian null cloud with the same M and feature dimension as ``like`` (Euclidean).
- **method `SpaceBuilder._index_of`** [L136-143]: `def _index_of(self, artifact_id: str) -> HistoryIndex`
- **method `SpaceBuilder.hooks`** [L145-147]: `def hooks(self, activation_set_id: str) -> tuple[str, ...]` - The hook names of an ActivationSet, in storage order.
- **method `SpaceBuilder.activations`** [L149-173]: `def activations(self, activation_set_id: str, hook: str, panel: int, space: str | None = None) -> PointSet` - Activations of one hook for one panel, metric Euclidean, space ``act:<hook>``.
- **method `SpaceBuilder.baseline`** [L175-199]: `def baseline(self, kind: Literal['R0', 'R1', 'R2', 'R3'], panel: int, **refs) -> PointSet` - Representation baseline R0..R3 on the panel histories (RESEARCH_SUMMARY 7.6).
- **method `SpaceBuilder._need`** [L202-205]: `def _need(refs: dict, key: str) -> str` decorators: @staticmethod
- **method `SpaceBuilder._panel_tokens`** [L207-221]: `def _panel_tokens(self, index_id: str, obs_id: str, panel: int)`

