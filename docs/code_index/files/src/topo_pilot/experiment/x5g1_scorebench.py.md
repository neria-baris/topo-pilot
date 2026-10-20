# `src/topo_pilot/experiment/x5g1_scorebench.py`

- Source: [src/topo_pilot/experiment/x5g1_scorebench.py](../../../../../../src/topo_pilot/experiment/x5g1_scorebench.py)
- Kind: python
- Lines: 195

## Module docstring

> X5 G1 scoring-only timing correction (x5g1-techbench-scoring-v2; job 0009). NOT scientific.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 33, via package root)
- `from topo_pilot.learner import ModelConfig, TransformerLM, load_model, serialise_state` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 34, via package root)
- `from .x4b_run import peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 36, via relative)
- `from .x5g1_controls import RunControls` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 37, via relative)
- `from .x5g1_safety import ensure_new_output_dir, guarded_export` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 38, via relative)
- `from .x5g1t_score import SCORE_BATCH, regret_rows` -> [src/topo_pilot/experiment/x5g1t_score.py](x5g1t_score.py.md) (line 39, via relative)

### External (third-party)

- `numpy` (lines 22)
- `torch` (lines 23)

### Standard library

- `__future__` (lines 9)
- `argparse` (lines 11)
- `hashlib` (lines 12)
- `json` (lines 13)
- `logging` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 20)
- `statistics` (lines 16)
- `subprocess` (lines 17)
- `sys` (lines 18)
- `time` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 160: `topo_pilot` -> [src/topo_pilot/__init__.py](../__init__.py.md)

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x5g1_scorebench_smoke.py](../../../tests/experiment/test_x5g1_scorebench_smoke.py.md) (line 8, import)

## Top-level constants

- `FIXED_MODEL`
- `LIMIT_S`
- `PROTOCOL`
- `PROTOCOL_DOC`
- `STORED_CKPT`
- `STORED_TRAIN`
- `TECH_CAP_S`
- `V1_PROJECTION`

## Classes and functions

- **function `_clock`** [L58-59]: `def _clock() -> tuple[float, float]`
- **function `_delta`** [L62-63]: `def _delta(a: tuple[float, float], b: tuple[float, float]) -> dict`
- **function `stored_model_config`** [L66-72]: `def stored_model_config(main_root: Path) -> tuple[dict, str]` - Read-only metadata assertion of the stored E3 checkpoint; returns (model_config, sha).
- **function `fixture`** [L75-88]: `def fixture(model_cfg: dict) -> tuple[TransformerLM, torch.Tensor, np.ndarray]`
- **function `project`** [L91-101]: `def project(v1: dict, s1: float, s2: float, s0: float) -> dict` - Frozen corrected projection (protocol §4); v1 terms other than scoring kept.
- **function `_sha`** [L104-105]: `def _sha(path: Path) -> str`
- **function `run`** [L108-177]: `def run(repo: Path, main_root: Path, store: Path, out: Path, mailbox: Path) -> dict`
- **function `main`** [L180-191]: `def main(argv: list[str] | None = None) -> int`

