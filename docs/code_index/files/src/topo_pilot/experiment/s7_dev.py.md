# `src/topo_pilot/experiment/s7_dev.py`

- Source: [src/topo_pilot/experiment/s7_dev.py](../../../../../../src/topo_pilot/experiment/s7_dev.py)
- Kind: python
- Lines: 169

## Module docstring

> S7 dev data (D-047): dev panels, dev activations, dev and test probe targets.

## Imports

### Internal (repo files)

- `from topo_pilot.activations import ActivationStage` -> [src/topo_pilot/activations/__init__.py](../activations/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import ActivationSet, ArtifactStore, Checkpoint, EmissionSpec, ErrorCode, HistoryIndex, ObservationSet, OracleOutputs, SeedTree, StageFailure, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset import DatasetConfig, PanelBuilder` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 33, via package root)
- `from topo_pilot.oracle import BayesFilter, LastSymbolPosterior` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 34, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 36, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 37, via relative)
- `from .s4_analysis import WORLDS, AnalysisJob` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 38, via relative)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 12)
- `dataclasses` (lines 15)
- `logging` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 13, import)
- [src/topo_pilot/experiment/s7_probes.py](s7_probes.py.md) (line 29, import)
- [src/topo_pilot/experiment/s7_sensitivity.py](s7_sensitivity.py.md) (line 31, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 21, import)

## Top-level constants

- `CONS`
- `END`

## Classes and functions

- **class `ProbeData`** [L46-55] decorators: @dataclass(frozen=True) - Rows of one split: ``ids [M]``, ``panel [M]``, targets ``b32, b1 [M, N]``, ``q [M, V]``
- **class `DevData`** [L58-169] - Dev panels, dev activations and aligned probe targets for the O/P runs.
- **method `DevData.__init__`** [L61-71]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `DevData.runs`** [L73-75]: `def runs(self) -> list[tuple[str, str, int]]`
- **method `DevData.dev_index`** [L78-94]: `def dev_index(self, world: str, cond: str, seed: int) -> str` - The dev HistoryIndex of a run (built and stored on first use).
- **method `DevData.checkpoint`** [L96-102]: `def checkpoint(self, world: str, cond: str, seed: int, step: int) -> str`
- **method `DevData.dev_acts`** [L104-115]: `def dev_acts(self, world: str, cond: str, seed: int, step: int) -> str` - Dev ActivationSet (primary hook, all dev panels) of a run at ``step``.
- **method `DevData.extract_all`** [L117-123]: `def extract_all(self) -> list[str]`
- **method `DevData.features`** [L126-131]: `def features(self, act_id: str, ids: list[str]) -> np.ndarray` - Primary-hook rows ``[M, d]`` of an ActivationSet in the order of ``ids``.
- **method `DevData.all_rows`** [L133-136]: `def all_rows(self, act_id: str) -> np.ndarray` - Every primary-hook row ``[M, d]`` of an ActivationSet (e.g. all dev histories).
- **method `DevData._kernels`** [L138-143]: `def _kernels(self, world: str, cond: str, seed: int)`
- **method `DevData._index_tokens`** [L145-150]: `def _index_tokens(self, index_id: str, obs_id: str)`
- **method `DevData.dev_targets`** [L152-159]: `def dev_targets(self, world: str, cond: str, seed: int) -> ProbeData` - Exact dev targets from the oracle kernels (b32, r_w, F1 = q at p = 32).
- **method `DevData.test_targets`** [L161-169]: `def test_targets(self, world: str, cond: str, seed: int) -> ProbeData` - Stored test oracle targets in HistoryIndex order.

