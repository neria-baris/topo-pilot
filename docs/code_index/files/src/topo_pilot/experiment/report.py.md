# `src/topo_pilot/experiment/report.py`

- Source: [src/topo_pilot/experiment/report.py](../../../../../../src/topo_pilot/experiment/report.py)
- Kind: python
- Lines: 108

## Module docstring

> Report generation from MetricRecords and GateReports only (W0/W1 scope: level E0).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 13, via package root)

### External (third-party)

- `matplotlib` (lines 52, 55)

### Standard library

- `__future__` (lines 8)
- `collections` (lines 10)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 24, import)
- [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 19, import)
- [src/topo_pilot/experiment/report_e3.py](report_e3.py.md) (line 24, import)
- [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 17, import)
- [src/topo_pilot/experiment/report_e4_s7.py](report_e4_s7.py.md) (line 13, import)
- [src/topo_pilot/experiment/report_x4.py](report_x4.py.md) (line 15, import)

## Top-level constants

- `SERIES`

## Classes and functions

- **function `_rows`** [L20-24]: `def _rows(store: ArtifactStore, stage: str) -> list[MetricRow]`
- **function `_value`** [L27-30]: `def _value(rows: Sequence[MetricRow], space: str, metric: str, world: str | None) -> float | None`
- **function `_fmt`** [L33-34]: `def _fmt(v: float | None, digits: int = 3) -> str`
- **function `e0_table`** [L37-46]: `def e0_table(rows: Sequence[MetricRow]) -> list[str]` - Markdown lines: graph cycles vs surface holes, and S per world and metric.
- **function `e0_figure`** [L49-88]: `def e0_figure(rows: Sequence[MetricRow], path: Path) -> Path` - Dot plot of S (longest H1 bar / q95 scale) per world, one series per metric, with the
- **function `build_e0`** [L91-108]: `def build_e0(store: ArtifactStore, out_dir: Path) -> Path` - Write ``summary.md`` and ``fig_world_ph.png`` for exit level E0; returns the summary path.

