# `src/topo_pilot/experiment/x5g1_verify.py`

- Source: [src/topo_pilot/experiment/x5g1_verify.py](../../../../../../src/topo_pilot/experiment/x5g1_verify.py)
- Kind: python
- Lines: 261

## Module docstring

> X5 G1 deterministic post-hoc verification (job 0007) of the SAME saved calibration pools.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import integrated_autocorrelation, movement_rate, percentile_interval, rate_matched_kernel, spectrum_report` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 23, via package root)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, ObservationSet, SeedTree, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.oracle import FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 39, via package root)
- `from topo_pilot.process import ConductanceConfig, conductance_kernel` -> [src/topo_pilot/process/__init__.py](../process/__init__.py.md) (line 40, via package root)
- `from .config import producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 42, via relative)
- `from .x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 43, via relative)
- `from .x4b_run import peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 44, via relative)
- `from .x5g1_controls import RunControls` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 45, via relative)
- `from .x5g1_oracle import bootstrap_means, gate_quantities` -> [src/topo_pilot/experiment/x5g1_oracle.py](x5g1_oracle.py.md) (line 46, via relative)
- `from .x5g1_run import PARENTS_FULL, diagnostics, kernel_validity` -> [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 47, via relative)
- `from .x5g1_safety import checked_computation, ensure_new_output_dir, guarded_export` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 48, via relative)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 10)
- `argparse` (lines 12)
- `hashlib` (lines 13)
- `json` (lines 14)
- `logging` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 19)
- `sys` (lines 17)
- `time` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 219: `topo_pilot` -> [src/topo_pilot/__init__.py](../__init__.py.md)

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x5g1_verify.py](../../../tests/experiment/test_x5g1_verify.py.md) (line 6, import)

## Top-level constants

- `OLD_RESULT`
- `OLD_RESULT_SHA`
- `SOURCES`
- `TOL`

## Classes and functions

- **function `_sha`** [L65-66]: `def _sha(path: Path) -> str`
- **function `compute`** [L69-139]: `def compute(store: ArtifactStore, g) -> dict` - Recompute all reported quantities from the saved pools (no sampling).
- **function `_pairs`** [L142-165]: `def _pairs(old: dict, new: dict) -> list[tuple[str, object, object]]` - (name, old, new) for every reported quantity of job 0006 that is recomputed here.
- **function `_maxdiff`** [L168-179]: `def _maxdiff(a, b) -> float`
- **function `compare`** [L182-190]: `def compare(repo: Path, new: dict) -> dict`
- **function `_jsonable`** [L193-202]: `def _jsonable(obj)`
- **function `run_verify`** [L205-242]: `def run_verify(repo: Path, main_root: Path, x5_store: Path, out: Path, mailbox: Path) -> dict`
- **function `main`** [L245-257]: `def main(argv: list[str] | None = None) -> int`

