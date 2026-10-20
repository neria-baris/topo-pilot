# `src/topo_pilot/experiment/x5g1t_checks.py`

- Source: [src/topo_pilot/experiment/x5g1t_checks.py](../../../../../../src/topo_pilot/experiment/x5g1t_checks.py)
- Kind: python
- Lines: 104

## Module docstring

> X5 G1 study integrity checks (x5g1-train-v4 §11; API v4 §5, v4.1 §B): full-hash verification
> of used artifacts, semantic pool identity (hashes prove bytes, not which pool) and checkpoint
> identity against the model, arm, master and pools.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, Checkpoint, ObservationSet, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from topo_pilot.learner import ModelConfig` -> [src/topo_pilot/learner/__init__.py](../learner/__init__.py.md) (line 13, via package root)
- `from .x5g1_safety import verify_sources_full` -> [src/topo_pilot/experiment/x5g1_safety.py](x5g1_safety.py.md) (line 15, via relative)
- `from .x5g1t_lineage import sequence_ids, study_pool_config` -> [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 16, via relative)
- `from .x5g1t_train import study_run_key, study_train_config` -> [src/topo_pilot/experiment/x5g1t_train.py](x5g1t_train.py.md) (line 17, via relative)

### External (third-party)

- `numpy` (lines 10)

### Standard library

- `__future__` (lines 5)
- `dataclasses` (lines 7)
- `json` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 28, import)
- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 24, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 40, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 44, import)
- [tests/experiment/test_x5g1t_checkpoint_checks.py](../../../tests/experiment/test_x5g1t_checkpoint_checks.py.md) (line 26, dynamic)
- [tests/experiment/test_x5g1t_export_checks.py](../../../tests/experiment/test_x5g1t_export_checks.py.md) (line 32, dynamic)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 23, import)

## Top-level constants

- none

## Classes and functions

- **class `IntegrityFailed(RuntimeError)`** [L20-21] - A used artifact failed full-hash verification or checkpoint identity checks.
- **function `canonical`** [L24-26]: `def canonical(obj) -> str` - Canonical JSON text: tuples and lists compare equal, key order is irrelevant.
- **function `verify_full`** [L29-32]: `def verify_full(store: ArtifactStore, expected: dict, when: str) -> None`
- **function `validate_pool`** [L35-66]: `def validate_pool(store: ArtifactStore, pool_id: str, sha: str, cfg, split: str, arm: str, master, V: int) -> dict` - ``{pool_id: (ObservationSet, sha)}`` once the pool is proven to be ``split/arm/master``:
- **function `validate_checkpoints`** [L69-104]: `def validate_checkpoints(store: ArtifactStore, outcome: dict, cfg, arm: str, master, train_pool_id: str, dev_pool_id: str) -> dict` - ``{checkpoint_id: (Checkpoint, sha)}`` after checking every identity field.

