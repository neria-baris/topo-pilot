# `src/topo_pilot/experiment/x5g1t_fixture.py`

- Source: [src/topo_pilot/experiment/x5g1t_fixture.py](../../../../../../src/topo_pilot/experiment/x5g1t_fixture.py)
- Kind: python
- Lines: 90

## Module docstring

> SYNTHETIC fixture for the X5 G1 training-study CLI (jobs 0009-0010): a tiny N4/V3 process pair
> and a tiny world in a temporary store, a tiny model and a ``mode = "synthetic-fixture"`` config
> (API v4 §6) that ``validate_config`` keeps apart from production; never real pools, models or
> study data.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from topo_pilot.world import WorldConfig, build_world` -> [src/topo_pilot/world/__init__.py](../world/__init__.py.md) (line 20, via package root)
- `from .x5g1t_config import PRODUCTION` -> [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 22, via relative)
- `from .x5g1t_lineage import MASTERS` -> [src/topo_pilot/experiment/x5g1t_lineage.py](x5g1t_lineage.py.md) (line 23, via relative)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 27, import)
- [tests/experiment/test_x5g1t_config_checks.py](../../../tests/experiment/test_x5g1t_config_checks.py.md) (line 24, import)
- [tests/experiment/test_x5g1t_config_production.py](../../../tests/experiment/test_x5g1t_config_production.py.md) (line 23, import)
- [tests/experiment/test_x5g1t_config_synthetic.py](../../../tests/experiment/test_x5g1t_config_synthetic.py.md) (line 24, import)
- [tests/experiment/test_x5g1t_e2e.py](../../../tests/experiment/test_x5g1t_e2e.py.md) (line 10, import)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 24, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_integration.py](../../../tests/experiment/test_x5g1t_integration.py.md) (line 21, import)

## Top-level constants

- `E0`
- `T0`
- `_REPO`

## Classes and functions

- **function `_entropy`** [L33-35]: `def _entropy(p: np.ndarray) -> float`
- **function `_emission`** [L38-43]: `def _emission(E: np.ndarray, pi: np.ndarray, perm: np.ndarray) -> EmissionSpec`
- **function `build_fixture`** [L46-90]: `def build_fixture(root: Path, sizes: dict | None = None, steps: int = 6, bootstrap_draws: int = 40, cap_s: float = 21600.0) -> Path` - Create ``root/{sources,study,mailbox}`` and return the study config path.

