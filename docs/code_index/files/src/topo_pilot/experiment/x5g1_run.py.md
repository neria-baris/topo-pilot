# `src/topo_pilot/experiment/x5g1_run.py`

- Source: [src/topo_pilot/experiment/x5g1_run.py](../../../../../../src/topo_pilot/experiment/x5g1_run.py)
- Kind: python
- Lines: 225

## Module docstring

> X5 G1 exact-process and calibration gate run (x5g1-feas-v2; handoff job 0006). No training.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import context_status, integrated_autocorrelation, is_connected, movement_rate, percentile_interval, rate_matched_kernel, spectrum_report` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 15, via package root)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, SeedTree, TransitionSpec, WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 24, via package root)
- `from topo_pilot.oracle import FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 32, via package root)
- `from topo_pilot.process import ConductanceConfig, ProcessStage, conductance_kernel` -> [src/topo_pilot/process/__init__.py](../process/__init__.py.md) (line 33, via package root)
- `from .config import producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 35, via relative)
- `from .x4b import ReadThroughBackend, provenance_row` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 36, via relative)
- `from .x4b2 import ROLES` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 37, via relative)
- `from .x4b2 import sequence_ids` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 38, via relative)
- `from .x4b2 import stored_sequence_ids, windows` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 39, via relative)
- `from .x4b_run import listing_hash` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 40, via relative)
- `from .x5g1_controls import RunControls` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 41, via relative)
- `from .x5g1_lineage import ARMS, STREAM, calibration_obs, paired_generators, sample_named` -> [src/topo_pilot/experiment/x5g1_lineage.py](x5g1_lineage.py.md) (line 42, via relative)
- `from .x5g1_lineage import sequence_ids` -> [src/topo_pilot/experiment/x5g1_lineage.py](x5g1_lineage.py.md) (line 43, via relative)
- `from .x5g1_oracle import bootstrap_means, gate_quantities` -> [src/topo_pilot/experiment/x5g1_oracle.py](x5g1_oracle.py.md) (line 44, via relative)
- `from .x5g1_safety import verify_sources_full` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 45, via relative)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 8)
- `logging` (lines 10)
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

- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 33, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 47, import)

## Top-level constants

- `PARENTS_FULL`
- `PROTOCOL`
- `PROTOCOL_DOC`

## Classes and functions

- **class `GateFailed(RuntimeError)`** [L62-63] - A FAILED condition (integrity, state order, a0 equivalence, namespace collision).
- **function `kernel_validity`** [L66-81]: `def kernel_validity(T: np.ndarray, pi: np.ndarray, world: WorldSpec, E: np.ndarray) -> dict` - x5g1-feas-v2 §3.1 checks; ``ok`` iff all hold.
- **function `diagnostics`** [L84-100]: `def diagnostics(T: np.ndarray, pi: np.ndarray, world: WorldSpec, E: np.ndarray) -> dict` - Rate, spectrum, mixing bound and conditional-state integrated autocorrelations.
- **function `_entropy`** [L103-105]: `def _entropy(p: np.ndarray) -> float`
- **function `body`** [L108-211]: `def body(res: dict, ctl: RunControls, repo: Path, main_root: Path, out_root: Path) -> None`
- **function `_paired`** [L214-225]: `def _paired(kl: dict, g) -> list[float]` - Descriptive paired G_C difference (a020 - a0), shared indices, frozen stream.

