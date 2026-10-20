# `src/topo_pilot/experiment/x5g1t_stages.py`

- Source: [src/topo_pilot/experiment/x5g1t_stages.py](../../../../../../src/topo_pilot/experiment/x5g1t_stages.py)
- Kind: python
- Lines: 242

## Module docstring

> X5 G1 training-study stages, part 1 (x5g1-train-v4 §10-§11; API v4 §6): shared stage plumbing,
> ``pools`` and ``train``. ``dev-analysis`` and ``final-test`` are in ``x5g1t_stages_eval``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, ObservationSet, SeedTree, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 33, via package root)
- `from .config import producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 35, via relative)
- `from .x4b import ReadThroughBackend` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 36, via relative)
- `from .x4b_run import peak_memory_bytes` -> [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 37, via relative)
- `from .x5g1_controls import RunControls` -> [src/topo_pilot/experiment/x5g1_controls.py](x5g1_controls.py.md) (line 38, via relative)
- `from .x5g1_safety import ensure_new_output_dir` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 39, via relative)
- `from .x5g1t_checks import IntegrityFailed, canonical, validate_pool, verify_full` -> [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 40, via relative)
- `from .x5g1t_config import StudyConfig, read_chain, read_store, validate_config` -> [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 41, via relative)
- `from .x5g1t_exports import study_export, verify_export_complete` -> [src/topo_pilot/experiment/x5g1t_exports.py](x5g1t_exports.py.md) (line 42, via relative)
- `from .x5g1t_lineage import ARMS, collisions, draw_pair, pool_observation, sequence_ids, stream, study_pool_config` -> [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 43, via relative)
- `from .x5g1t_runtime import EST, BudgetPlanner, StudyControls, evaluation_reserve, read_outcome` -> [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 52, via relative)
- `from .x5g1t_train import study_train_config, train_one` -> [src/topo_pilot/experiment/x5g1t_train.py](x5g1t_train.py.md) (line 59, via relative)

### External (third-party)

- `numpy` (lines 22)
- `torch` (lines 23)

### Standard library

- `__future__` (lines 15)
- `json` (lines 17)
- `pathlib` (lines 20)
- `re` (lines 18)
- `sys` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 29, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 61, import)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 20, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 21, import)

## Top-level constants

- none

## Classes and functions

- **class `StudyFailed(RuntimeError)`** [L62-63] - Collision, prerequisite or authorisation failure (not a scientific verdict).
- **function `stores`** [L66-71]: `def stores(cfg: StudyConfig, repo: Path) -> tuple[ArtifactStore, ArtifactStore]` - (read-only sources, read-through study store writing only to ``study_root/store``).
- **function `_controls`** [L74-76]: `def _controls(cfg: StudyConfig, job: str) -> RunControls`
- **function `_study`** [L79-81]: `def _study(cfg: StudyConfig, ctl: RunControls, name: str) -> StudyControls`
- **function `_sources`** [L84-90]: `def _sources(store: ArtifactStore, cfg: StudyConfig)`
- **function `_meta`** [L93-100]: `def _meta(cfg: StudyConfig, repo: Path, ctl: RunControls, stage: str, report: dict) -> dict`
- **function `tables`** [L103-104]: `def tables(cfg: StudyConfig, *parts: str) -> Path`
- **function `complete_pools`** [L107-122]: `def complete_pools(cfg: StudyConfig) -> dict` - ``pools.json`` of a COMPLETE, manifest-matching pools export whose table has exactly the
- **function `emission_V`** [L125-127]: `def emission_V(store: ArtifactStore, cfg: StudyConfig) -> int`
- **function `validate_pools`** [L130-137]: `def validate_pools(store: ArtifactStore, cfg: StudyConfig, pools: dict, which, V: int) -> dict` - Semantic identity of each ``(split, arm, master)`` pool in the table (API v4.1 §B).
- **function `collision_inputs`** [L140-148]: `def collision_inputs(ro: ArtifactStore) -> tuple[np.ndarray, dict]` - IDs of every read-root ObservationSet, and ``{id: (cls, sha)}`` recorded at load so the
- **function `pool_expected`** [L151-152]: `def pool_expected(pools: dict, keys) -> dict`
- **function `complete_outcome`** [L155-165]: `def complete_outcome(cfg: StudyConfig, arm: str, master) -> dict | None` - The recorded outcome; for a COMPLETE model, only with a COMPLETE matching train export.
- **function `run_pools`** [L168-214]: `def run_pools(cfg: StudyConfig, repo: Path) -> dict` - Train and dev pools for every master and arm (never the fresh test).
- **function `run_train`** [L217-242]: `def run_train(cfg: StudyConfig, repo: Path, arm: str, master) -> dict` - One model; the outcome is recorded by ``train_one`` on every exit.

