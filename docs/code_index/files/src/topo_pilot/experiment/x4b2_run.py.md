# `src/topo_pilot/experiment/x4b2_run.py`

- Source: [src/topo_pilot/experiment/x4b2_run.py](../../../../../../src/topo_pilot/experiment/x4b2_run.py)
- Kind: python
- Lines: 302

## Module docstring

> X4 Phase B2 run (protocol x4b2-v1): four fresh pools, one at a time, under the x4b-v1 screen.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import hellinger, overall_verdict, practical_verdict, screen_pool, strict_verdict, tangent_audit` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 19, via package root)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 27, via package root)
- `from .config import load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 35, via relative)
- `from .x4b import SHARED, ReadThroughBackend, canonical_tokens, future_maps, index_tokens, map_failures, pool_checks, pool_failures, provenance_row, resolve_inputs` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 36, via relative)
- `from .x4b2 import PROTOCOL_VERSION, ROLES, TEST_ROLE, ambient_match, beliefs_p32, build_b2_pool, sample_pool, sequence_ids, stored_sequence_ids, windows` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 48, via relative)
- `from .x4b_audit import pool_audit, screen` -> [src/topo_pilot/experiment/x4b_audit.py](x4b_audit.py.md) (line 60, via relative)
- `from .x4b_run import Budget, BudgetExceeded, _ambient_json, _load_process, _sha256, listing_hash, peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 61, via relative)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 8)
- `argparse` (lines 10)
- `csv` (lines 11)
- `json` (lines 12)
- `logging` (lines 13)
- `pathlib` (lines 15)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `CODE_NOTES`
- `PROTOCOL_DOC`

## Classes and functions

- **function `_float32_check`** [L77-87]: `def _float32_check(res: dict, pool) -> dict` - Q2 distances from float32-cast Q2 for the same pairs; flips and status.
- **function `_permutation_check`** [L90-104]: `def _permutation_check(res: dict, pool, proc: dict, seed: int = 1729) -> dict` - Reference pool recomputed in replicate ``seed``'s vocabulary; must screen identically.
- **function `_old_windows`** [L107-122]: `def _old_windows(main: ArtifactStore, inputs: dict, proc: dict) -> dict` - Canonical 32-symbol windows of the old cylinder-O test, dev and train splits.
- **function `_one_pool`** [L125-150]: `def _one_pool(role: str, proc: dict, maps, budget: Budget, out: Path) -> tuple[dict, list]`
- **function `run_b2`** [L153-197]: `def run_b2(repo: Path, main_root: Path, out_root: Path, tables: Path, b_tables: Path) -> dict` - Run x4b2-v1 once; write tables and exports; return the verdict summary.
- **function `_separation`** [L200-219]: `def _separation(pools: dict, old_ids: np.ndarray, old_win: dict) -> dict`
- **function `_export`** [L222-275]: `def _export(repo, main_root, out_root, tables, b_tables, main, inputs, proc, maps, ambient, link, pools, sep, summary, budget, before, after) -> None`
- **function `main`** [L278-298]: `def main(argv: list[str] | None = None) -> int`

