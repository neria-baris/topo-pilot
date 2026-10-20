# `src/topo_pilot/experiment/s7_circular.py`

- Source: [src/topo_pilot/experiment/s7_circular.py](../../../../../../src/topo_pilot/experiment/s7_circular.py)
- Kind: python
- Lines: 113

## Module docstring

> S7 circular coordinates (D-047; RESEARCH_SUMMARY §7.7): do the circular coordinates of the
> activation cloud track the latent x angle?

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import CircularCorrespondence` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import ArtifactStore, EvalSidecar, MetricRecords, MetricRow, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 20, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 29, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 30, via relative)
- `from .s4_analysis import WORLDS, AnalysisJob, _row` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 31, via relative)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 13)
- `logging` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/s7_jobs.py](s7_jobs.py.md) (line 27, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 20, import)

## Top-level constants

- `CONS`
- `SPACE`

## Classes and functions

- **class `CircularJob`** [L38-113] - Writes one MetricRecords (``kind = circular``).
- **method `CircularJob.__init__`** [L41-50]: `def __init__(self, cfg: ResolvedConfig, store: ArtifactStore)`
- **method `CircularJob.runs`** [L52-60]: `def runs(self) -> list[tuple[str, str, int]]`
- **method `CircularJob.run_rows`** [L62-77]: `def run_rows(self, world: str, cond: str, seed: int) -> list[MetricRow]`
- **method `CircularJob.summary`** [L80-96]: `def summary(rows: list[MetricRow], common: dict) -> list[MetricRow]` decorators: @staticmethod
- **method `CircularJob.run`** [L98-113]: `def run(self) -> list[str]`

