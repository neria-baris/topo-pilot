# `tests/integration/_mini_pipeline.py`

- Source: [tests/integration/_mini_pipeline.py](../../../../../tests/integration/_mini_pipeline.py)
- Kind: python
- Lines: 135

## Module docstring

> Shared mini S1 -> S2 -> S3 pipeline for the I04 / I06 integration tests (CPU, minutes).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, ErrorCode, GateCheck, GateReport, LocalFSBackend, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 13, via package root)
- `from topo_pilot.experiment import load_config, run_stage` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 21, via package root)
- `from topo_pilot.experiment.stages import STAGE_REGISTRY, latest_gate_verdicts` -> [src/topo_pilot/experiment/stages.py](../../src/topo_pilot/experiment/stages.py.md) (line 22, via package root)
- `import topo_pilot.dataset.stage` -> [src/topo_pilot/dataset/stage.py](../../src/topo_pilot/dataset/stage.py.md) (line 73, via package root) (inside a function)
- `from topo_pilot.contracts import ArtifactMeta` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 108, via package root) (inside a function)
- `from topo_pilot.contracts import MetricRecords, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 132, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 7)
- `torch` (lines 8)
- `yaml` (lines 9)

### Standard library

- `hashlib` (lines 130)
- `json` (lines 106)
- `pathlib` (lines 5)
- `shutil` (lines 3)
- `sys` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 11: `str(Path(__file__).parent)` -> `tests/integration`

## Imported by

- [tests/integration/test_leakage_end_to_end.py](test_leakage_end_to_end.py.md) (line 10, import)
- [tests/integration/test_rerun_identity.py](test_rerun_identity.py.md) (line 10, import)

## Top-level constants

- `REPO`
- `THREADS`
- `TIMING_METRICS`
- `_CACHE`

## Classes and functions

- **function `_mini_configs`** [L29-46]: `def _mini_configs(tmp: Path) -> Path`
- **function `_waive_failures`** [L49-57]: `def _waive_failures(store: ArtifactStore, stage: str) -> None`
- **function `build_store`** [L60-90]: `def build_store(tmp: Path, scramble_z: bool = False) -> ArtifactStore` - Run S1, S2, S3 of the mini config into a fresh store under ``tmp``.
- **function `get_store`** [L93-97]: `def get_store(tmp_factory, name: str) -> ArtifactStore` - Session-cached store: ``plain`` or ``scrambled``.
- **function `ids_and_hashes`** [L100-101]: `def ids_and_hashes(store: ArtifactStore, artifact_type) -> dict[str, str]`
- **function `all_artifacts`** [L104-120]: `def all_artifacts(store: ArtifactStore) -> dict[str, dict[str, str]]` - {artifact_type: {artifact_id: payload_sha256}} of every complete artifact.
- **function `_untimed_digest`** [L126-135]: `def _untimed_digest(store: ArtifactStore, artifact_id: str) -> str` - Digest of a MetricRecords without its measured timing rows (wall time, throughput and the

