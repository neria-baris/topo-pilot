# `src/topo_pilot/experiment/report_e2.py`

- Source: [src/topo_pilot/experiment/report_e2.py](../../../../../../src/topo_pilot/experiment/report_e2.py)
- Kind: python
- Lines: 252

## Module docstring

> Report for exit level E2 (S4) and the condition-P section of E3 (S5), from MetricRecords and
> GateReports only.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 17, via package root)
- `from .report import GRID, INK, INK_MUTED, _fmt` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 19, via relative)

### External (third-party)

- `matplotlib` (lines 172, 175)
- `numpy` (lines 15)

### Standard library

- `__future__` (lines 10)
- `collections` (lines 12)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [reports/he_summary/extract_data.py](../../../reports/he_summary/extract_data.py.md) (line 17, import)
- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 25, import)
- [src/topo_pilot/experiment/report_e3.py](report_e3.py.md) (line 25, import)
- [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 18, import)
- [src/topo_pilot/experiment/report_e4_s7.py](report_e4_s7.py.md) (line 14, import)
- [src/topo_pilot/experiment/report_x4.py](report_x4.py.md) (line 16, import)
- [src/topo_pilot/experiment/s6.py](s6.py.md) (line 49, import)
- [tests/experiment/test_report_e2.py](../../../tests/experiment/test_report_e2.py.md) (line 12, import)

## Top-level constants

- `BASELINES`
- `WORLDS`

## Classes and functions

- **function `_latest`** [L26-29]: `def _latest(store: ArtifactStore, cls, **filters) -> list[str]` - Ids matching ``filters``, newest first (``created_utc``).
- **function `run_rows`** [L32-45]: `def run_rows(store: ArtifactStore, stage: str) -> dict[tuple, dict[str, float | None]]` - Per run key ``(world, condition, seed)``: the final-checkpoint training metrics of the
- **function `analysis_rows`** [L48-50]: `def analysis_rows(store: ArtifactStore, stage: str) -> list[MetricRow]`
- **function `_pick`** [L53-55]: `def _pick(rows: Sequence[MetricRow], space: str, metric: str, **kw) -> list[MetricRow]`
- **function `_one`** [L58-60]: `def _one(rows: Sequence[MetricRow], space: str, metric: str, **kw) -> float | None`
- **function `_median`** [L63-65]: `def _median(values: Sequence[float | None]) -> float | None`
- **function `_act_space`** [L68-71]: `def _act_space(rows: Sequence[MetricRow]) -> str` - The activation space name (``act:<primary hook>``) used by the analysis job.
- **function `replicates`** [L74-75]: `def replicates(rows: Sequence[MetricRow]) -> list[int]`
- **function `prediction_table`** [L78-94]: `def prediction_table(runs: dict[tuple, dict], cond: str) -> list[str]`
- **function `f1_table`** [L97-112]: `def f1_table(rows: Sequence[MetricRow], final: int) -> list[str]`
- **function `verdict`** [L115-120]: `def verdict(rows: Sequence[MetricRow]) -> tuple[str, str]` - ``(status, reasons)`` of the F1 verdict row; ``("not run", "")`` if absent.
- **function `baseline_table`** [L123-136]: `def baseline_table(rows: Sequence[MetricRow]) -> list[str]`
- **function `geometry_table`** [L139-150]: `def geometry_table(rows: Sequence[MetricRow]) -> list[str]`
- **function `floor_table`** [L153-165]: `def floor_table(rows: Sequence[MetricRow], final: int) -> list[str]`
- **function `f1_figure`** [L168-211]: `def f1_figure(rows: Sequence[MetricRow], path: Path, title: str) -> Path` - Dot plot of D_{r,i} (8 panels) per replicate, with the median (diamond) and the noise
- **function `build_e2`** [L214-251]: `def build_e2(store: ArtifactStore, out_dir: Path, stage: str = 'S4', final: int = 5000, extra: Sequence[str] = (), name: str = 'summary.md', figure: str = 'fig_f1_contrasts.png') -> Path` - Write ``name`` and ``figure`` for ``stage`` (S4: O, E2; S5: P, part of E3); ``extra``

