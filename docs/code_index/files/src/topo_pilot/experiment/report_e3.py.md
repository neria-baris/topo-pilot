# `src/topo_pilot/experiment/report_e3.py`

- Source: [src/topo_pilot/experiment/report_e3.py](../../../../../../src/topo_pilot/experiment/report_e3.py)
- Kind: python
- Lines: 339

## Module docstring

> Report for exit level E3 (S5 + S6, with X4 under O and P), from MetricRecords only.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 22, via package root)
- `from .report import GRID, INK, INK_MUTED, _fmt` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 24, via relative)
- `from .report_e2 import SURFACE, WORLDS, _latest, _median, _one, _pick, analysis_rows, build_e2, replicates, verdict` -> [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 25, via relative)
- `from .report_x4 import _prereg_line, _verdict, run_table, x4_rows, x4_section` -> [src/topo_pilot/experiment/report_x4.py](report_x4.py.md) (line 37, via relative)

### External (third-party)

- `matplotlib` (lines 194, 197)

### Standard library

- `__future__` (lines 17)
- `collections` (lines 19)
- `pathlib` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [reports/he_summary/extract_data.py](../../../reports/he_summary/extract_data.py.md) (line 18, import)
- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 26, import)
- [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 19, import)
- [tests/experiment/test_report_e3.py](../../../tests/experiment/test_report_e3.py.md) (line 5, import)

## Top-level constants

- `H3_READING`
- `H4_READING`
- `HOOKS`
- `WORLD_COLOR`

## Classes and functions

- **function `s6_rows`** [L61-64]: `def s6_rows(store: ArtifactStore, kind: str, cond: str) -> list[MetricRow]` - Rows of the newest S6 record of ``kind`` (dynamics / layers / x4curves) for ``cond``.
- **function `h4_status`** [L67-71]: `def h4_status(rows: Sequence[MetricRow]) -> tuple[str, str]`
- **function `_runs`** [L74-75]: `def _runs(rows: Sequence[MetricRow], space: str, metric: str) -> list[tuple[int, str]]`
- **function `h4_table`** [L78-95]: `def h4_table(dyn: Sequence[MetricRow], curves: Sequence[MetricRow]) -> list[str]` - Per run: G_C, u_r, t_history, t_rise (V0; and V1/V5, descriptive), D-034 class and the
- **function `_step`** [L98-99]: `def _step(t: float | None) -> str`
- **function `layer_table`** [L102-118]: `def layer_table(by_cond: dict[str, Sequence[MetricRow]]) -> list[str]` - Layer sweep (descriptive): per hook and condition, median D, panels D > 0 and u_r per
- **function `x4_compare`** [L121-144]: `def x4_compare(rows: Sequence[MetricRow]) -> list[str]` - Secondary X4 outcomes under O and P side by side.
- **function `compare_table`** [L147-165]: `def compare_table(rows_o: Sequence[MetricRow], rows_p: Sequence[MetricRow]) -> list[str]` - F1 contrast and baselines per replicate, O (E2) vs P (E3).
- **function `geometry_compare`** [L168-179]: `def geometry_compare(rows_o: Sequence[MetricRow], rows_p: Sequence[MetricRow]) -> list[str]`
- **function `_series`** [L183-188]: `def _series(rows: Sequence[MetricRow], space: str, metric: str) -> dict[tuple, list[tuple]]`
- **function `_grid_figure`** [L191-238]: `def _grid_figure(cells: list[list[dict]], path: Path, title: str) -> Path` - Small multiples: each cell holds ``series`` {(world, seed): [(step, value)]}, ``ylabel``,
- **function `dynamics_figure`** [L241-251]: `def dynamics_figure(dyn: dict[str, Sequence[MetricRow]], path: Path) -> Path`
- **function `curves_figure`** [L254-258]: `def curves_figure(curves: dict[str, Sequence[MetricRow]], path: Path) -> Path`
- **function `_quote`** [L262-264]: `def _quote(path: Path, prefix: str) -> str`
- **function `_decision`** [L267-269]: `def _decision(path: Path, did: str) -> str`
- **function `build_e3`** [L272-339]: `def build_e3(store: ArtifactStore, out_dir: Path, repo_root: Path, final: int = 5000) -> Path` - Write ``summary.md``, ``condition_P.md`` and the two figures; returns the summary path.

