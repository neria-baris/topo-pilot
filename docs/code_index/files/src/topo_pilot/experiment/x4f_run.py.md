# `src/topo_pilot/experiment/x4f_run.py`

- Source: [src/topo_pilot/experiment/x4f_run.py](../../../../../../src/topo_pilot/experiment/x4f_run.py)
- Kind: python
- Lines: 238

## Module docstring

> Prospective X4-F maintenance runner; the historical x4f-exec-v2 cohort stays closed.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import fit_oblique_eraser, gate_verdict, whiten` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 22, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.learner import load_model` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 30, via package root)
- `from .config import load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 32, via relative)
- `from .s4_analysis import AnalysisJob` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 33, via relative)
- `from .x4b import ReadThroughBackend, provenance_row` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 34, via relative)
- `from .x4b_run import Budget, _sha256, listing_hash, peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 35, via relative)
- `from .x4f_damage import g3, g4, g5` -> [src/topo_pilot/experiment/x4f_damage.py](x4f_damage.py.md) (line 36, via relative)
- `from .x4f_data import SEEDS, extract, load_model_data, resolve` -> [src/topo_pilot/experiment/x4f_data.py](x4f_data.py.md) (line 37, via relative)
- `from .x4f_gates import ValForward, control_targets, g1, g2` -> [src/topo_pilot/experiment/x4f_gates.py](x4f_gates.py.md) (line 38, via relative)
- `from .x5g1_controls import BudgetExceeded, RunControls, StopRequested` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 39, via relative)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 9)
- `argparse` (lines 11)
- `csv` (lines 12)
- `json` (lines 13)
- `logging` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 18)
- `sys` (lines 16)
- `time` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 173: `topo_pilot` -> [src/topo_pilot/__init__.py](../__init__.py.md)

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x4f_maintenance.py](../../../tests/experiment/test_x4f_maintenance.py.md) (line 10, import)

## Top-level constants

- `PROTOCOL`
- `PROTOCOL_DOC`

## Classes and functions

- **function `_gate`** [L47-48]: `def _gate(status: str) -> str`
- **function `run_gates`** [L51-63]: `def run_gates(repo: Path, main_root: Path, out_root: Path, tables: Path, mailbox: Path) -> dict` - Prospective maintenance runner; never overwrite an earlier cohort's exports.
- **function `_run_gates`** [L66-131]: `def _run_gates(repo, main_root, out_root, tables, ctl)`
- **function `_jsonable`** [L134-143]: `def _jsonable(obj)`
- **function `_export`** [L146-201]: `def _export(repo, main, rw, out_root, tables, ids, act_ids, data, rec, state, summary, budget, before, after, ledger, checkpoint=lambda _: None) -> None`
- **function `_profiles_csv`** [L204-216]: `def _profiles_csv(path: Path, rec: dict) -> None`
- **function `main`** [L219-234]: `def main(argv: list[str] | None = None) -> int`

