# `src/topo_pilot/experiment/x4f_data.py`

- Source: [src/topo_pilot/experiment/x4f_data.py](../../../../../../src/topo_pilot/experiment/x4f_data.py)
- Kind: python
- Lines: 144

## Module docstring

> X4-F gate data (x4f-exec-v2 §2–§3): frozen inputs, dev activations and oracle targets.

## Imports

### Internal (repo files)

- `from topo_pilot.activations import ActivationStage` -> [src/topo_pilot/activations/__init__.py](../activations/__init__.py.md) (line 15, via package root)
- `from topo_pilot.analysis import circle_expectation` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 16, via package root)
- `from topo_pilot.contracts import ActivationSet, ArtifactStore, Checkpoint, EmissionSpec, ErrorCode, HistoryIndex, ObservationSet, SequenceLayout, StageFailure, TransitionSpec, WorldSpec, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.oracle import BayesFilter, LastSymbolPosterior` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 31, via package root)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 33, via relative)
- `from .s4_analysis import AnalysisJob` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 34, via relative)
- `from .x4b import EXPECTED, S7_RECORDS, SHARED, ancestors` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 35, via relative)

### External (third-party)

- `numpy` (lines 12, 13)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py](../../../docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py.md) (line 9, import)
- [src/topo_pilot/experiment/x4f_damage.py](x4f_damage.py.md) (line 18, import)
- [src/topo_pilot/experiment/x4f_gates.py](x4f_gates.py.md) (line 28, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 37, import)
- [tests/experiment/test_x4f_gates_smoke.py](../../../tests/experiment/test_x4f_gates_smoke.py.md) (line 10, import)

## Top-level constants

- `CAL_PANELS`
- `CONS`
- `HOOKS`
- `INDEX`
- `PERIOD`
- `SEEDS`
- `STEP`
- `VAL_PANELS`

## Classes and functions

- **function `_missing`** [L47-48]: `def _missing(check: str, detail: str) -> StageFailure`
- **function `resolve`** [L51-75]: `def resolve(aj: AnalysisJob, store: ArtifactStore, seed: int) -> dict[str, str]` - Frozen ids of one model: checkpoint (step 5000), dev index/obs, emission, T, world.
- **function `extract`** [L78-81]: `def extract(rw_store: ArtifactStore, ids: dict[str, str]) -> str` - Dev ActivationSet (HOOKS, panels 1-8) of one step-5000 checkpoint in ``rw_store``.
- **class `ModelData`** [L85-95] decorators: @dataclass(frozen=True, eq=False) - Per-model dev rows in HistoryIndex order; ``cal``/``val`` are boolean row masks.
- **function `_incidence`** [L98-104]: `def _incidence(world: WorldSpec) -> NDArray[np.float64]`
- **function `load_model_data`** [L107-144]: `def load_model_data(store: ArtifactStore, ids: dict[str, str], act_id: str, seed: int) -> ModelData` - Tokens, activations at input index 32 and oracle targets of one model's dev pool.

