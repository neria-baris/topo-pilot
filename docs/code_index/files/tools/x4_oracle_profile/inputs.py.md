# `tools/x4_oracle_profile/inputs.py`

- Source: [tools/x4_oracle_profile/inputs.py](../../../../../tools/x4_oracle_profile/inputs.py)
- Kind: python
- Lines: 289

## Module docstring

> Read-only inputs for job 0014: hashes, process artifacts, histories and environment.

## Imports

### Internal (repo files)

- `from oracle_profile import ProfileError, canonical_emission, circle_features, validate_process` -> [tools/x4_oracle_profile/oracle_profile.py](oracle_profile.py.md) (line 18, via same directory)
- `from topo_pilot.contracts.base import payload_checksum` -> [src/topo_pilot/contracts/base.py](../../src/topo_pilot/contracts/base.py.md) (line 57, via package root) (inside a function)
- `import topo_pilot` -> [src/topo_pilot/__init__.py](../../src/topo_pilot/__init__.py.md) (line 250, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 17, 223)
- `threadpoolctl` (lines 224)

### Standard library

- `__future__` (lines 9)
- `ctypes` (lines 263, 264)
- `hashlib` (lines 11)
- `json` (lines 12)
- `os` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_a_transport_bound.py](../../tests/k4b/test_a_transport_bound.py.md) (line 37, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 105, import)
- [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 33, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 38, import)
- [tools/x4_circle_history/live_context.py](../x4_circle_history/live_context.py.md) (line 105, import)
- [tools/x4_oracle_profile/audit.py](audit.py.md) (line 31, import)
- [tools/x4_oracle_profile/run_profile.py](run_profile.py.md) (line 25, import)
- [tools/x4_oracle_profile/runtime.py](runtime.py.md) (line 18, import)
- [tools/x4_oracle_profile/validation.py](validation.py.md) (line 16, import)

## Top-level constants

- `CONFIG_PATH`
- `HERE`
- `REPO`

## Classes and functions

- **function `load_config`** [L25-26]: `def load_config() -> dict`
- **function `sha256`** [L29-30]: `def sha256(path) -> str`
- **function `dump_json`** [L33-39]: `def dump_json(path, obj) -> None`
- **function `verify_input_hashes`** [L42-48]: `def verify_input_hashes(cfg: dict) -> dict`
- **function `_manifest`** [L51-52]: `def _manifest(cfg: dict) -> dict`
- **function `load_artifact`** [L55-80]: `def load_artifact(cfg: dict, kind: str, artifact_id: str) -> tuple[dict, dict, dict]` - Verify meta hash, status, payload hash and canonical payload checksum; return arrays.
- **function `_expected_edges`** [L83-90]: `def _expected_edges(coords: np.ndarray, period: int) -> set`
- **function `world_identity`** [L93-122]: `def world_identity(cfg: dict, world: dict, extra: dict, T: np.ndarray) -> dict` - 12x12 cylinder (x periodic) from coords; stored edges and T support match that lattice.
- **function `emission_identity`** [L125-145]: `def emission_identity(cfg: dict, coords: np.ndarray, E_canon: np.ndarray, centers: np.ndarray) -> float` - Rebuild E_canon = softmax_j(-d(z, c_j)^2 / 2 sigma^2) on the x-periodic flat chart.
- **function `load_process`** [L148-193]: `def load_process(cfg: dict) -> dict` - Verified T, pi, canonical E, named emissions/permutations, features and identity record.
- **function `load_split`** [L196-219]: `def load_split(cfg: dict, split: str) -> dict` - Load one split with schema, shape, ID, range and finiteness checks.
- **function `environment`** [L222-259]: `def environment() -> dict`
- **function `peak_working_set`** [L262-289]: `def peak_working_set() -> int`

