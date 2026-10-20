# `src/topo_pilot/dataset/stage.py`

- Source: [src/topo_pilot/dataset/stage.py](../../../../../../src/topo_pilot/dataset/stage.py)
- Kind: python
- Lines: 148

## Module docstring

> I/O layer of the module: the only place that touches the artifact store.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, ErrorCode, EvalSidecar, HistoryIndex, ObservationSet, SeedTree, SequenceLayout, StageFailure, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from .checks import check_disjoint, check_first_token, check_ranges, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](checks.py.md) (line 23, via relative)
- `from .config import DatasetConfig` -> [src/topo_pilot/dataset/config.py](config.py.md) (line 30, via relative)
- `from .panels import PanelBuilder` -> [src/topo_pilot/dataset/panels.py](panels.py.md) (line 31, via relative)
- `from .public import assert_public` -> [src/topo_pilot/dataset/public.py](public.py.md) (line 32, via relative)
- `from .sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](sampler.py.md) (line 33, via relative)

### External (third-party)

- `numpy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `logging` (lines 5)
- `typing` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/dataset/__init__.py](__init__.py.md) (line 7, import)
- [tests/integration/_mini_pipeline.py](../../../tests/integration/_mini_pipeline.py.md) (line 73, import)

## Top-level constants

- `CONSUMER`

## Classes and functions

- **function `_sigma_str`** [L39-40]: `def _sigma_str(sigma: Any) -> str`
- **class `DatasetStage`** [L43-148] - Samples, splits, checks, and saves the public and privileged data of one process.
- **method `DatasetStage.run`** [L67-80]: `def run(self, transition_id: str, emission_id: str, cfg: DatasetConfig, seeds: SeedTree, store: ArtifactStore) -> dict[str, str]`
- **method `DatasetStage._sample_all`** [L82-101]: `def _sample_all(self, trans: TransitionSpec, emis: EmissionSpec, cfg: DatasetConfig, seeds: SeedTree, scope: tuple[str, str, str]) -> dict[str, Any]`
- **method `DatasetStage._save_all`** [L103-138]: `def _save_all(self, data: dict[str, Any], scope: tuple[str, str, str], parents: tuple[str, str], cfg: DatasetConfig, seeds: SeedTree, store: ArtifactStore) -> dict[str, str]`
- **method `DatasetStage._save_panels`** [L140-148]: `def _save_panels(self, test: ObservationSet, test_id: str, base: dict[str, Any], cfg: DatasetConfig, store: ArtifactStore) -> str`

