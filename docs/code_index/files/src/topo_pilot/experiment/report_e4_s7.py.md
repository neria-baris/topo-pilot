# `src/topo_pilot/experiment/report_e4_s7.py`

- Source: [src/topo_pilot/experiment/report_e4_s7.py](../../../../../../src/topo_pilot/experiment/report_e4_s7.py)
- Kind: python
- Lines: 294

## Module docstring

> S7 and S8 tables and figures of the E4 report, from MetricRecords and GateReports only.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)
- `from .report import GRID, INK, INK_MUTED, _fmt` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 13, via relative)
- `from .report_e2 import SURFACE, WORLDS, _latest, _median, _one, _pick` -> [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 14, via relative)

### External (third-party)

- `matplotlib` (lines 242, 252, 255, 273, 276)

### Standard library

- `__future__` (lines 6)
- `collections` (lines 8)
- `pathlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 20, import)
- [tests/experiment/test_s8_e4.py](../../../tests/experiment/test_s8_e4.py.md) (line 15, import)

## Top-level constants

- `CIRC`
- `PROBES`
- `WORLD_COLOR`

## Classes and functions

- **function `s7_rows`** [L26-32]: `def s7_rows(store: ArtifactStore, kind: str) -> list[MetricRow]` - Rows of the newest S7 (or S8) record of ``kind``.
- **function `control_runs`** [L35-47]: `def control_runs(store: ArtifactStore) -> dict[tuple, dict[str, float | None]]` - Newest S7 run record per run key: final metrics, H0 rows and failure notes.
- **function `control_table`** [L50-79]: `def control_table(runs: dict[tuple, dict], s4_h0: Sequence[MetricRow]) -> list[str]`
- **function `_h0_floor`** [L82-85]: `def _h0_floor(v: dict) -> float | None`
- **function `controls_ph_table`** [L88-105]: `def controls_ph_table(rows: Sequence[MetricRow], final: int) -> list[str]`
- **function `r_space`** [L108-110]: `def r_space(rows: Sequence[MetricRow]) -> str`
- **function `probe_table`** [L113-135]: `def probe_table(rows: Sequence[MetricRow]) -> list[str]`
- **function `circular_table`** [L138-158]: `def circular_table(rows: Sequence[MetricRow], final: int) -> list[str]`
- **function `sensitivity_table`** [L161-186]: `def sensitivity_table(rows: Sequence[MetricRow], primary: dict) -> list[str]`
- **function `gate_lines`** [L189-197]: `def gate_lines(store: ArtifactStore, stage: str, gate_id: str) -> list[str]`
- **function `rerun_table`** [L200-221]: `def rerun_table(rows: Sequence[MetricRow]) -> list[str]`
- **function `_dot_panel`** [L224-238]: `def _dot_panel(ax, groups: list[tuple[str, dict[str, list[float]]]], xlabel: str) -> None`
- **function `_save`** [L241-248]: `def _save(fig, path: Path) -> Path`
- **function `probe_figure`** [L251-269]: `def probe_figure(rows: Sequence[MetricRow], path: Path) -> Path`
- **function `circular_figure`** [L272-294]: `def circular_figure(rows: Sequence[MetricRow], final: int, path: Path) -> Path`

