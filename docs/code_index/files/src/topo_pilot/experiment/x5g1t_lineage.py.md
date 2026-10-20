# `src/topo_pilot/experiment/x5g1t_lineage.py`

- Source: [src/topo_pilot/experiment/x5g1t_lineage.py](../../../../../../src/topo_pilot/experiment/x5g1t_lineage.py)
- Kind: python
- Lines: 99

## Module docstring

> X5 G1 training-study lineage (x5g1-train-v3 §3): masters, streams, codes 9/10/11, paired
> pool draws (named = perm[canon], latents dropped) and disjointness counts.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 9, via package root)
- `from .x4b2 import process_code` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 11, via relative)
- `from .x5g1_lineage import sample_named` -> [src/topo_pilot/experiment/x5g1_lineage.py](x5g1_lineage.py.md) (line 12, via relative)

### External (third-party)

- `numpy` (lines 6, 7)

### Standard library

- `__future__` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_checks.py](x5g1t_checks.py.md) (line 16, import)
- [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 29, import)
- [src/topo_pilot/experiment/x5g1t_fixture.py](x5g1t_fixture.py.md) (line 23, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 43, import)
- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 47, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 22, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 24, import)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 26, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 19, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_training.py](../../../tests/experiment/test_x5g1t_training.py.md) (line 20, import)

## Top-level constants

- `ARMS`
- `CODES`
- `MASTERS`
- `NAMESPACE`
- `PROTOCOL`
- `SIZES`
- `TEST_MASTER`

## Classes and functions

- **function `_bad`** [L23-24]: `def _bad(check: str, detail: str) -> StageFailure`
- **function `stream`** [L27-30]: `def stream(split: str) -> tuple[str, ...]`
- **function `_seed_master`** [L33-41]: `def _seed_master(split: str, master) -> int`
- **function `paired_generators`** [L44-47]: `def paired_generators(split: str, master) -> tuple[np.random.Generator, np.random.Generator]` - Two separately created generators with the same frozen seed (common randomness).
- **function `sequence_ids`** [L50-59]: `def sequence_ids(split: str, arm: str, master, n: int) -> NDArray[np.int64]` - ``(process_code(..., f"{NAMESPACE}:{split}:{arm}:{master}") << 32) | (code << 28) | i``.
- **function `draw_pair`** [L62-66]: `def draw_pair(kernels: dict, E: NDArray, perm: NDArray, pi: NDArray, split: str, master, n: int) -> dict[str, NDArray]` - ``{arm: named tokens [n, 33]}``; one sampler call per arm with the paired generators.
- **function `pool_observation`** [L69-73]: `def pool_observation(split: str, named: NDArray, ids: NDArray, V: int) -> ObservationSet`
- **function `pool_config`** [L76-78]: `def pool_config(split: str, arm: str, master) -> dict`
- **function `study_pool_config`** [L81-89]: `def study_pool_config(split: str, arm: str, master, execution_protocol: str) -> dict` - Metadata of a NEW study pool (API v4.1 §A): ``lineage_protocol`` names the frozen
- **function `collisions`** [L92-99]: `def collisions(new: dict[str, NDArray], stored: NDArray) -> dict[str, int]` - Per new id set: how many ids are in ``stored``; ``internal``: duplicates across all new.

