# `src/topo_pilot/experiment/x5g1_techbench.py`

- Source: [src/topo_pilot/experiment/x5g1_techbench.py](../../../../../../src/topo_pilot/experiment/x5g1_techbench.py)
- Kind: python
- Lines: 220

## Module docstring

> X5 G1 technical throughput benchmark (x5g1-techbench-v1; job 0008). NOT a scientific pilot.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.dataset import PublicTokenDataset` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 26, via package root)
- `from topo_pilot.learner import ModelConfig, TrainConfig, Trainer` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 27, via package root)
- `from .x5g1_controls import RunControls` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 29, via relative)
- `from .x5g1_safety import ensure_new_output_dir, guarded_export` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 30, via relative)

### External (third-party)

- `numpy` (lines 22)
- `torch` (lines 23)

### Standard library

- `__future__` (lines 8)
- `argparse` (lines 10)
- `dataclasses` (lines 11)
- `hashlib` (lines 12)
- `io` (lines 13)
- `json` (lines 14)
- `logging` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 20)
- `statistics` (lines 17)
- `sys` (lines 18)
- `time` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/experiment/test_x5g1_techbench_smoke.py](../../../tests/experiment/test_x5g1_techbench_smoke.py.md) (line 7, import)

## Top-level constants

- `ALLOC`
- `REMAINING_SCIENTIFIC_S`
- `STORED_MODEL`
- `TECH_CAP_S`
- `THREADS`

## Classes and functions

- **function `_clock`** [L46-47]: `def _clock() -> tuple[float, float]`
- **function `_delta`** [L50-51]: `def _delta(a: tuple[float, float], b: tuple[float, float]) -> dict`
- **function `_dataset`** [L54-59]: `def _dataset(split: str, n: int) -> PublicTokenDataset`
- **function `_tensors`** [L62-64]: `def _tensors(ds: PublicTokenDataset) -> tuple[torch.Tensor, torch.Tensor]`
- **function `_repeat`** [L67-73]: `def _repeat(fn, n: int = REPEATS) -> list[dict]`
- **function `bench_setting`** [L76-139]: `def bench_setting(threads: int, ctl: RunControls, data: dict) -> dict` - All phases for one intra-op thread setting (see the frozen protocol §3).
- **function `project`** [L142-157]: `def project(r: dict, med) -> dict` - Frozen projection (protocol §4), CPU seconds.
- **function `run`** [L160-203]: `def run(repo: Path, store: Path, out: Path, mailbox: Path) -> dict`
- **function `main`** [L206-216]: `def main(argv: list[str] | None = None) -> int`

