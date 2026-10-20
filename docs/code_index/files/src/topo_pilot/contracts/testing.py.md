# `src/topo_pilot/contracts/testing.py`

- Source: [src/topo_pilot/contracts/testing.py](../../../../../../src/topo_pilot/contracts/testing.py)
- Kind: python
- Lines: 102

## Module docstring

> Tiny, deterministic test fixtures. Importable from tests only, never from ``src`` code.

## Imports

### Internal (repo files)

- `from .backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](backends.py.md) (line 12, via relative)
- `from .errors import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 13, via relative)
- `from .ids import SeedTree` -> [src/topo_pilot/contracts/ids.py](ids.py.md) (line 14, via relative)
- `from .schemas import ObservationSet, WorldSpec` -> [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 15, via relative)
- `from .store import ArtifactStore` -> [src/topo_pilot/contracts/store.py](store.py.md) (line 16, via relative)

### External (third-party)

- `numpy` (lines 10)

### Standard library

- `__future__` (lines 6)
- `typing` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/activations/conftest.py](../../../tests/activations/conftest.py.md) (line 13, import)
- [tests/activations/test_activations.py](../../../tests/activations/test_activations.py.md) (line 25, import)
- [tests/analysis/test_sensitivity_circular.py](../../../tests/analysis/test_sensitivity_circular.py.md) (line 27, import)
- [tests/analysis/test_x5_kernel.py](../../../tests/analysis/test_x5_kernel.py.md) (line 24, import)
- [tests/circle_history/test_adapter.py](../../../tests/circle_history/test_adapter.py.md) (line 26, import)
- [tests/circle_history/test_builder_e2e.py](../../../tests/circle_history/test_builder_e2e.py.md) (line 37, import)
- [tests/contracts/conftest.py](../../../tests/contracts/conftest.py.md) (line 7, import)
- [tests/contracts/test_bundle_determinism.py](../../../tests/contracts/test_bundle_determinism.py.md) (line 3, import)
- [tests/contracts/test_fixtures.py](../../../tests/contracts/test_fixtures.py.md) (line 6, import)
- [tests/contracts/test_store.py](../../../tests/contracts/test_store.py.md) (line 10, import)
- [tests/dataset/conftest.py](../../../tests/dataset/conftest.py.md) (line 6, import)
- [tests/dataset/test_panels.py](../../../tests/dataset/test_panels.py.md) (line 13, import)
- [tests/dataset/test_public.py](../../../tests/dataset/test_public.py.md) (line 14, import)
- [tests/dataset/test_sampler.py](../../../tests/dataset/test_sampler.py.md) (line 6, import)
- [tests/experiment/test_s7.py](../../../tests/experiment/test_s7.py.md) (line 16, import)
- [tests/experiment/test_s8_e4.py](../../../tests/experiment/test_s8_e4.py.md) (line 12, import)
- [tests/experiment/test_x5g1_controls.py](../../../tests/experiment/test_x5g1_controls.py.md) (line 18, import)
- [tests/experiment/test_x5g1_lineage.py](../../../tests/experiment/test_x5g1_lineage.py.md) (line 24, import)
- [tests/experiment/test_x5g1t_checkpoint_checks.py](../../../tests/experiment/test_x5g1t_checkpoint_checks.py.md) (line 20, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 21, import)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 18, import)
- [tests/k4b/test_b_registry_rules.py](../../../tests/k4b/test_b_registry_rules.py.md) (line 237, import)
- [tests/learner/conftest.py](../../../tests/learner/conftest.py.md) (line 8, import)
- [tests/learner/test_checkpoint.py](../../../tests/learner/test_checkpoint.py.md) (line 16, import)
- [tests/oracle/test_oracle.py](../../../tests/oracle/test_oracle.py.md) (line 8, import)
- [tests/prediction/test_stage.py](../../../tests/prediction/test_stage.py.md) (line 13, import)
- [tests/process/conftest.py](../../../tests/process/conftest.py.md) (line 8, import)
- [tests/process/test_conductance.py](../../../tests/process/test_conductance.py.md) (line 26, import)
- [tests/process/test_controls.py](../../../tests/process/test_controls.py.md) (line 18, import)
- [tests/world/test_world.py](../../../tests/world/test_world.py.md) (line 10, import)

## Top-level constants

- `_BETTI`

## Classes and functions

- **function `tiny_world_spec`** [L22-60]: `def tiny_world_spec(family: Literal['square', 'cylinder'] = 'cylinder', n: int = 3) -> WorldSpec` - An ``n x n`` square or cylinder (axis 0 periodic) built by direct enumeration.
- **function `tiny_hmm`** [L63-79]: `def tiny_hmm() -> tuple[np.ndarray, np.ndarray, np.ndarray]` - A hand-chosen 4-state, 3-symbol HMM: ``(T [4,4], E [4,3], pi [4])``.
- **function `tiny_observations`** [L82-97]: `def tiny_observations(R: int = 8, seed: int = 0) -> ObservationSet` - ``R`` test-split trajectories of 33 symbols sampled from :func:`tiny_hmm`.
- **function `memory_store`** [L100-102]: `def memory_store() -> ArtifactStore` - A fresh :class:`ArtifactStore` over an in-memory backend with the default access policy.

