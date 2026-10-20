# `src/topo_pilot/experiment/x5g1_lineage.py`

- Source: [src/topo_pilot/experiment/x5g1_lineage.py](../../../../../../src/topo_pilot/experiment/x5g1_lineage.py)
- Kind: python
- Lines: 65

## Module docstring

> X5 G1 calibration lineage (x5g1-feas-v2 §4): paired generators, named tokens, namespace 8.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 12, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../dataset/__init__.py.md) (line 19, via package root)
- `from .x4b2 import process_code` -> [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 21, via relative)

### External (third-party)

- `numpy` (lines 9, 10)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 32, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 42, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 43, import)
- [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 12, import)
- [tests/experiment/test_x5g1_lineage.py](../../../tests/experiment/test_x5g1_lineage.py.md) (line 26, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 24, import)

## Top-level constants

- `ARMS`
- `NAMESPACE_CODE`
- `N_POOL`
- `STREAM`

## Classes and functions

- **function `paired_generators`** [L29-31]: `def paired_generators() -> tuple[np.random.Generator, np.random.Generator]` - Two separately created generators with the identical frozen seed (common randomness).
- **function `sample_named`** [L34-49]: `def sample_named(T: NDArray, E: NDArray, perm: NDArray, pi: NDArray, rng: np.random.Generator, n: int = N_POOL) -> NDArray` - One sampler call on ``E[:, perm]``; returns ``perm[canon]`` ``[n, 33]``; states dropped.
- **function `sequence_ids`** [L52-57]: `def sequence_ids(arm: str, n: int = N_POOL) -> NDArray[np.int64]` - ``(process_code(..., "x5g1-v1:calibration:" + arm) << 32) | (8 << 28) | index``.
- **function `calibration_obs`** [L60-65]: `def calibration_obs(named: NDArray, seq: NDArray) -> ObservationSet` - Public calibration pool: ``split="dev"`` (schema literal); the role lives in the config.

