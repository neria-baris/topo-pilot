# `src/topo_pilot/experiment/report_e4.py`

- Source: [src/topo_pilot/experiment/report_e4.py](../../../../../../src/topo_pilot/experiment/report_e4.py)
- Kind: python
- Lines: 162

## Module docstring

> Report for exit level E4 (S7 + S8), from MetricRecords and GateReports only.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 15, via package root)
- `from .report import _fmt` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 17, via relative)
- `from .report_e2 import _one, _pick, analysis_rows, replicates, verdict` -> [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 18, via relative)
- `from .report_e3 import H3_READING, H4_READING, h4_status, s6_rows, x4_compare` -> [src/topo_pilot/experiment/report_e3.py](report_e3.py.md) (line 19, via relative)
- `from .report_e4_s7 import circular_figure, circular_table, control_runs, control_table, controls_ph_table, gate_lines, probe_figure, probe_table, rerun_table, s7_rows, sensitivity_table` -> [src/topo_pilot/experiment/report_e4_s7.py](report_e4_s7.py.md) (line 20, via relative)
- `from .report_x4 import _verdict, x4_rows` -> [src/topo_pilot/experiment/report_x4.py](report_x4.py.md) (line 33, via relative)

### External (third-party)

- none

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

- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 27, import)
- [tests/experiment/test_s8_e4.py](../../../tests/experiment/test_s8_e4.py.md) (line 14, import)

## Top-level constants

- `CIRC_NOTE`
- `ORDER_NOTE`
- `PROBE_NOTE`
- `S8_NOTE`
- `SENS_NOTE`
- `U_NOTE`

## Classes and functions

- **function `_h2_summary`** [L66-71]: `def _h2_summary(rows: Sequence[MetricRow]) -> str`
- **function `_f1_values`** [L74-77]: `def _f1_values(rows: Sequence[MetricRow]) -> str` - ``median D/u_r`` per replicate.
- **function `_dg_fraction`** [L80-82]: `def _dg_fraction(rows: Sequence[MetricRow]) -> str`
- **function `primary_section`** [L85-102]: `def primary_section(rows_o, rows_p, dyn_o, x4, s4_h0, ctrl) -> list[str]`
- **function `build_e4`** [L105-146]: `def build_e4(store: ArtifactStore, out_dir: Path, final: int = 5000) -> Path` - Write ``summary.md`` and the two figures; returns the summary path.
- **function `_integrity_lines`** [L149-162]: `def _integrity_lines(integ: Sequence[MetricRow], reports: Sequence[MetricRow]) -> list[str]`

