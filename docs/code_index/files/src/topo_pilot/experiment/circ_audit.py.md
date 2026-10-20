# `src/topo_pilot/experiment/circ_audit.py`

- Source: [src/topo_pilot/experiment/circ_audit.py](../../../../../../src/topo_pilot/experiment/circ_audit.py)
- Kind: python
- Lines: 290

## Module docstring

> E4 circular-baseline audit (protocol circ-audit-v1): descriptive, existing artifacts only.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import CircularCorrespondence, SpaceBuilder, belief_angle, circular_agreement, lattice_angle, symbol_only_bound` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 22, via package root)
- `from topo_pilot.contracts import ArtifactStore, ErrorCode, EvalSidecar, LocalFSBackend, MetricRecords, MetricRow, SeedTree, StageFailure, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 30, via package root)
- `from .config import load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 43, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 44, via relative)
- `from .s4_analysis import AnalysisJob` -> [src/topo_pilot/experiment/s4_analysis.py](s4_analysis.py.md) (line 45, via relative)
- `from .x4b import ReadThroughBackend, index_tokens, provenance_row` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 46, via relative)
- `from .x4b_run import Budget, BudgetExceeded, _sha256, listing_hash, peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 47, via relative)

### External (third-party)

- `numpy` (lines 19)
- `scipy` (lines 20)

### Standard library

- `__future__` (lines 10)
- `argparse` (lines 12)
- `csv` (lines 13)
- `json` (lines 14)
- `logging` (lines 15)
- `pathlib` (lines 17)
- `time` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/experiment/test_circ_audit.py](../../../tests/experiment/test_circ_audit.py.md) (line 4, import)

## Top-level constants

- `BASELINES`
- `CONS`
- `HOOK`
- `PANELS`
- `PROTOCOL`
- `PROTOCOL_DOC`
- `S7_CIRCULAR`
- `S7_KEYS`
- `SEEDS`
- `SPACE`

## Classes and functions

- **function `_s7_rows`** [L63-68]: `def _s7_rows(store: ArtifactStore) -> dict`
- **function `_latent`** [L71-78]: `def _latent(store: ArtifactStore, sidecar_id: str, seqs: np.ndarray, ends: np.ndarray)`
- **function `_baseline_row`** [L81-91]: `def _baseline_row(cc: CircularCorrespondence, X: np.ndarray, theta, theta_y, rng) -> dict`
- **function `_repro`** [L94-103]: `def _repro(cc, store, act, side, world, oracle, seed, step, p, stored) -> tuple[dict, bool]`
- **function `audit_run`** [L106-153]: `def audit_run(store: ArtifactStore, aj: AnalysisJob, seed: int, s7: dict) -> tuple[list, list]` - All panel rows of one run, plus reproduction failures.
- **function `compare_panel`** [L156-168]: `def compare_panel(panel: dict, reps: dict) -> dict` - Frozen C1/C2 of circ-audit-v1 for one panel.
- **function `summarize`** [L171-193]: `def summarize(rows: list[dict]) -> dict` - Per-run counts and the frozen reading (all 3 / 0 / mixed).
- **function `run_audit`** [L196-211]: `def run_audit(repo: Path, main_root: Path, out_root: Path, tables: Path) -> dict`
- **function `_export`** [L214-268]: `def _export(repo, main_root, out_root, tables, store, aj, rows, summary, budget, before, after)`
- **function `main`** [L271-286]: `def main(argv: list[str] | None = None) -> int`

