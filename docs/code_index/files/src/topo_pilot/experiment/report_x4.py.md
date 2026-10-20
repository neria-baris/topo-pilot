# `src/topo_pilot/experiment/report_x4.py`

- Source: [src/topo_pilot/experiment/report_x4.py](../../../../../../src/topo_pilot/experiment/report_x4.py)
- Kind: python
- Lines: 154

## Module docstring

> X4 section of the E2 report (secondary; PREREGISTRATION_X4.md), from the X4 MetricRecords.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 13, via package root)
- `from .report import _fmt` -> [src/topo_pilot/experiment/report.py](report.py.md) (line 15, via relative)
- `from .report_e2 import WORLDS, _latest, _median, _one, _pick` -> [src/topo_pilot/experiment/report_e2.py](report_e2.py.md) (line 16, via relative)

### External (third-party)

- none

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

- [src/topo_pilot/experiment/cli.py](cli.py.md) (line 28, import)
- [src/topo_pilot/experiment/report_e3.py](report_e3.py.md) (line 37, import)
- [src/topo_pilot/experiment/report_e4.py](report_e4.py.md) (line 33, import)
- [src/topo_pilot/experiment/s6.py](s6.py.md) (line 50, import)
- [tests/experiment/test_report_e3.py](../../../tests/experiment/test_report_e3.py.md) (line 6, import)
- [tests/experiment/test_report_x4.py](../../../tests/experiment/test_report_x4.py.md) (line 5, import)

## Top-level constants

- `P_X4B_NOTE`
- `VIEWS`
- `VIEW_NAMES`
- `X4C_LINE`

## Classes and functions

- **function `x4_rows`** [L29-31]: `def x4_rows(store: ArtifactStore) -> list[MetricRow]`
- **function `_verdict`** [L34-38]: `def _verdict(rows: Sequence[MetricRow], space: str, prefix: str, cond: str) -> tuple[str, str]`
- **function `_prereg_line`** [L41-42]: `def _prereg_line(lines: Sequence[str], prefix: str) -> str`
- **function `_addendum`** [L45-47]: `def _addendum(lines: Sequence[str]) -> list[str]`
- **function `view_table`** [L50-65]: `def view_table(rows: Sequence[MetricRow], cond: str, final: int) -> list[str]`
- **function `geometry_lines`** [L68-78]: `def geometry_lines(rows: Sequence[MetricRow], cond: str) -> list[str]`
- **function `run_table`** [L81-84]: `def run_table(rows: Sequence[MetricRow], space: str, metric: str, cond: str, digits=0) -> str`
- **function `x4_section`** [L87-154]: `def x4_section(store: ArtifactStore, prereg: Path, cond: str = 'O', final: int = 5000) -> list[str]` - Markdown lines of the X4 section (secondary; F1 stays the headline).

