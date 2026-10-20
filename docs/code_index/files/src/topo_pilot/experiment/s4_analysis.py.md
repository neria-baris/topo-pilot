# `src/topo_pilot/experiment/s4_analysis.py`

- Source: [src/topo_pilot/experiment/s4_analysis.py](../../../../../../src/topo_pilot/experiment/s4_analysis.py)
- Kind: python
- Lines: 290

## Module docstring

> Analysis job of S4/S5: F1 rule, Δgeom (H2), baselines R1–R3 (D-028), Gaussian floor, H0, G-F.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import F1Decision, GeometryAlignment, PointSet, SpaceBuilder, ph_summary` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 18, via package root)
- `from topo_pilot.contracts import ActivationSet, EmissionSpec, GateCheck, GateReport, HistoryIndex, MetricRecords, MetricRow, ObservationSet, SeedTree, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.prediction import PredictiveMetrics` -> [src/topo_pilot/prediction/__init__.py](../prediction/__init__.py.md) (line 31, via package root)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 33, via relative)
- `from .s3 import TrainingRun, activation_ids, find_run_inputs, selected_sigma` -> [src/topo_pilot/experiment/s3.py](s3.py.md) (line 34, via relative)

### External (third-party)

- `numpy` (lines 15)
- `scipy` (lines 16)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 11)
- `logging` (lines 12)
- `typing` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/circ_audit.py](circ_audit.py.md) (line 45, import)
- [src/topo_pilot/experiment/s4.py](s4.py.md) (line 29, import)
- [src/topo_pilot/experiment/s6.py](s6.py.md) (line 52, import)
- [src/topo_pilot/experiment/s7_circular.py](s7_circular.py.md) (line 31, import)
- [src/topo_pilot/experiment/s7_controls.py](s7_controls.py.md) (line 29, import)
- [src/topo_pilot/experiment/s7_dev.py](s7_dev.py.md) (line 38, import)
- [src/topo_pilot/experiment/s7_probes.py](s7_probes.py.md) (line 28, import)
- [src/topo_pilot/experiment/s7_sensitivity.py](s7_sensitivity.py.md) (line 30, import)
- [src/topo_pilot/experiment/x4.py](x4.py.md) (line 40, import)
- [src/topo_pilot/experiment/x4_inputs.py](x4_inputs.py.md) (line 34, import)
- [src/topo_pilot/experiment/x4f_data.py](x4f_data.py.md) (line 34, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 33, import)
- [tests/experiment/test_runner.py](../../../tests/experiment/test_runner.py.md) (line 23, import)

## Top-level constants

- `BASELINES`
- `CONS`
- `WORLDS`

## Classes and functions

- **function `_row`** [L42-50]: `def _row(metric: str, value: float | None, space: str = 'analysis', **kw: Any) -> MetricRow` - A MetricRow; a non-finite value is stored as None with status ``inconclusive``.
- **function `_S`** [L53-55]: `def _S(ps: PointSet) -> tuple[float, str]`
- **function `_hellinger`** [L58-59]: `def _hellinger(X: np.ndarray) -> np.ndarray`
- **class `AnalysisJob`** [L62-285] - The S4 (condition O) or S5 (condition P) analysis over the stored runs.
- **method `AnalysisJob.__init__`** [L65-77]: `def __init__(self, stage_id: str, cfg, store)`
- **method `AnalysisJob.inputs`** [L80-85]: `def inputs(self, world: str, cond: str, seed: int) -> dict[str, str]`
- **method `AnalysisJob.acts`** [L87-94]: `def acts(self, world: str, cond: str, seed: int, step: int) -> str` - All-panel ActivationSet id of a run; ``KeyError`` if the run is not done.
- **method `AnalysisJob.learning_gate`** [L96-103]: `def learning_gate(self, world: str, seed: int) -> bool | None`
- **method `AnalysisJob.replicate_S`** [L106-135]: `def replicate_S(self, seed: int)` - S of the model (init, final) and of R1–R3 on every panel of both worlds.
- **method `AnalysisJob.baseline_rows`** [L137-153]: `def baseline_rows(self, seed: int, f1: F1Decision, S: dict, base_S: dict, D: np.ndarray) -> list[MetricRow]` - D-028: the F1 contrast with each baseline in place of the final checkpoint, and the
- **method `AnalysisJob.delta_geom`** [L156-176]: `def delta_geom(self, seed: int) -> tuple[list[MetricRow], list[float]]`
- **method `AnalysisJob._history_tokens`** [L178-185]: `def _history_tokens(self, inputs: dict[str, str], offset: int) -> dict[str, int]` - Token at ``end + offset`` per history: ``-1`` is w_32, ``0`` the target w_33.
- **method `AnalysisJob.floor`** [L187-198]: `def floor(self, seed: int) -> list[MetricRow]`
- **method `AnalysisJob.h0_check`** [L200-224]: `def h0_check(self) -> tuple[GateCheck | None, list[MetricRow]]` - D-029: the N model's test NLL at p = 32 is not below H(W) beyond the bootstrap CI.
- **method `AnalysisJob.replicate`** [L227-244]: `def replicate(self, seed: int, f1: F1Decision)` - Rows, ``(D, u)``, learning-gate flag and PH statuses of one complete replicate.
- **method `AnalysisJob.run`** [L246-285]: `def run(self) -> list[str]`
- **function `run_analysis`** [L288-290]: `def run_analysis(stage_id: str, cfg, store) -> list[str]` - Run the full analysis of ``stage_id`` (S4: condition O; S5: condition P).

