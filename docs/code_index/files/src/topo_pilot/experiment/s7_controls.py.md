# `src/topo_pilot/experiment/s7_controls.py`

- Source: [src/topo_pilot/experiment/s7_controls.py](../../../../../../src/topo_pilot/experiment/s7_controls.py)
- Kind: python
- Lines: 122

## Module docstring

> S7 controls (D-047): H0 rows of the extra N runs, and the descriptive ``controls`` job.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ActivationSet, ArtifactStore, EmissionSpec, MetricRecords, MetricRow, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.prediction import PredictiveMetrics` -> [src/topo_pilot/prediction/__init__.py](../prediction/__init__.py.md) (line 25, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 27, via relative)
- `from .s3 import TrainingRun, activation_ids` -> [src/topo_pilot/experiment/s3.py](s3.py.md) (line 28, via relative)
- `from .s4_analysis import _S, AnalysisJob, _row` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 29, via relative)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 9)
- `collections` (lines 13)
- `dataclasses` (lines 11)
- `logging` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7.py](s7.py.md) (line 140, import)
- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 19, import)

## Top-level constants

- `CONS`

## Classes and functions

- **function `_softmax`** [L35-38]: `def _softmax(logits: np.ndarray) -> np.ndarray`
- **function `h0_rows`** [L41-58]: `def h0_rows(cfg: ResolvedConfig, store: ArtifactStore, inputs: Mapping[str, str], act_id: str, seed: int) -> list[MetricRow]` - D-029 for one N run: test NLL at p = 32 must not be below H(W) by more than the 95%
- **class `ControlsJob`** [L61-122] - Descriptive PH of the U and N control models (no rule; RESEARCH_PLAN §3.3 note on U).
- **method `ControlsJob.__init__`** [L64-71]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `ControlsJob.runs`** [L73-75]: `def runs(self) -> list[dict]`
- **method `ControlsJob.acts`** [L77-81]: `def acts(self, job: Mapping, step: int) -> str | None` - All-panel ActivationSet of a control run at ``step`` (None if not trained).
- **method `ControlsJob.run_rows`** [L83-102]: `def run_rows(self, job: Mapping) -> tuple[list[MetricRow], dict[tuple[str, int], float]]`
- **method `ControlsJob.run`** [L104-122]: `def run(self) -> list[str]`

