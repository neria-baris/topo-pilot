# `src/topo_pilot/experiment/x5g1_main.py`

- Source: [src/topo_pilot/experiment/x5g1_main.py](../../../../../../src/topo_pilot/experiment/x5g1_main.py)
- Kind: python
- Lines: 161

## Module docstring

> X5 G1 gate driver: controls, verdict precedence and immutable exports (x5g1-feas-v2 §7–§8).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import x5_overall_verdict` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 20, via package root)
- `from .config import producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 28, via relative)
- `from .x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 29, via relative)
- `from .x4b_run import _sha256, peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 30, via relative)
- `from .x5g1_controls import BudgetExceeded, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 31, via relative)
- `from .x5g1_lineage import ARMS` -> [src/topo_pilot/experiment/x5g1_lineage.py](x5g1_lineage.py.md) (line 32, via relative)
- `from .x5g1_run import CAP_S, CUMULATIVE_CAP_S, PROTOCOL, PROTOCOL_DOC, GateFailed, body` -> [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 33, via relative)
- `from .x5g1_safety import ensure_new_output_dir, guarded_export` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 34, via relative)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 9)
- `json` (lines 10)
- `logging` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 80: `topo_pilot` -> [src/topo_pilot/__init__.py](../__init__.py.md)

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x5g1_export_integration.py](../../../tests/experiment/test_x5g1_export_integration.py.md) (line 27, import)
- [tests/experiment/test_x5g1_smoke.py](../../../tests/experiment/test_x5g1_smoke.py.md) (line 8, import)

## Top-level constants

- none

## Classes and functions

- **function `_jsonable`** [L39-48]: `def _jsonable(obj)`
- **function `run_gate`** [L51-73]: `def run_gate(repo: Path, main_root: Path, out_root: Path, tables: Path, mailbox: Path) -> dict` - Run once; the ledger entry is written by ``RunControls`` whatever happens.
- **function `_export`** [L76-139]: `def _export(repo: Path, main_root: Path, out_root: Path, tables: Path, res: dict, ctl: RunControls) -> None`
- **function `main`** [L142-157]: `def main(argv: list[str] | None = None) -> int`

