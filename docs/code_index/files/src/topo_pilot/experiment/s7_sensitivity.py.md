# `src/topo_pilot/experiment/s7_sensitivity.py`

- Source: [src/topo_pilot/experiment/s7_sensitivity.py](../../../../../../src/topo_pilot/experiment/s7_sensitivity.py)
- Kind: python
- Lines: 192

## Module docstring

> S7 one-factor-at-a-time sensitivity (D-047; RESEARCH_SUMMARY §7.7).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import F1Decision, GeometryAlignment, PointSet, Sensitivity, ph_summary` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 25, via package root)
- `from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 26, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 28, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 29, via relative)
- `from .s4_analysis import WORLDS, AnalysisJob, _row` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 30, via relative)
- `from .s7_dev import DevData` -> [src/topo_pilot/experiment/s7_dev.py](s7_dev.py.md) (line 31, via relative)
- `from .x4 import _gt_all, _rho, run_rule_verdict` -> [src/topo_pilot/experiment/x4.py](x4.py.md) (line 32, via relative)

### External (third-party)

- `numpy` (lines 22)
- `scipy` (lines 23)

### Standard library

- `__future__` (lines 18)
- `logging` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 31, import)

## Top-level constants

- `CODE`
- `CONS`

## Classes and functions

- **class `SensitivityJob`** [L39-192] - Writes one MetricRecords (``kind = sensitivity``).
- **method `SensitivityJob.__init__`** [L42-64]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `SensitivityJob.act_D`** [L67-79]: `def act_D(self, variant: str, world, cond, seed, step, p) -> tuple[np.ndarray, list[str]]`
- **method `SensitivityJob.belief_D`** [L81-89]: `def belief_D(self, variant: str, world, cond, seed, p, ids: list[str]) -> dict`
- **method `SensitivityJob.baseline_D`** [L91-102]: `def baseline_D(self, world, cond, seed, p, ids: list[str]) -> dict`
- **method `SensitivityJob.run_panel`** [L105-131]: `def run_panel(self, variant, world, cond, seed, p, S, common) -> tuple[list, dict]`
- **method `SensitivityJob.condition`** [L133-171]: `def condition(self, variant: str, cond: str) -> list[MetricRow]`
- **method `SensitivityJob.gate`** [L173-180]: `def gate(self, cond: str, world: str, seed: int) -> bool | None` - Learning gate of a run from its S4 (O) or S5 (P) run record.
- **method `SensitivityJob.run`** [L182-192]: `def run(self) -> list[str]`

