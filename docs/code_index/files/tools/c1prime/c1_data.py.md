# `tools/c1prime/c1_data.py`

- Source: [tools/c1prime/c1_data.py](../../../../../tools/c1prime/c1_data.py)
- Kind: python
- Lines: 120

## Module docstring

> C1' histories, sequence ids, panels, history tables, exposure registry and separation (API.md
> §12; protocol §2.2-§2.4). Sampling functions exist for the data stages; job 0026 runs none.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 11, via same directory)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 13, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 16, via package root)
- `from topo_pilot.dataset.checks import check_first_token, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 4)
- `hashlib` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_b_registry.py](../../tests/c1prime/test_b_registry.py.md) (line 33, import)
- [tests/c1prime_registry/test_registry_builder.py](../../tests/c1prime_registry/test_registry_builder.py.md) (line 19, import)
- [tests/c2_nd/test_b_registry.py](../../tests/c2_nd/test_b_registry.py.md) (line 23, import)
- [tests/k4b/test_b_registry_rules.py](../../tests/k4b/test_b_registry_rules.py.md) (line 31, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 15, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 12, import)
- [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 21, import)
- [tools/c2_nd/nd_data.py](../c2_nd/nd_data.py.md) (line 16, import)
- [tools/c2_nd/nd_dry.py](../c2_nd/nd_dry.py.md) (line 18, import)
- [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 24, import)
- [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 22, import)
- [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 21, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 11, import)
- [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 16, import)

## Top-level constants

- `BLOCK`
- `PROCESS`

## Classes and functions

- **function `history_generator`** [L23-24]: `def history_generator(split, block)`
- **function `sequence_ids`** [L27-29]: `def sequence_ids(split, block) -> np.ndarray`
- **function `sample_block`** [L32-38]: `def sample_block(T, E_canon, pi, split, block) -> tuple` - One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once.
- **function `panels`** [L41-45]: `def panels(seq_ids, block) -> np.ndarray`
- **function `lowest`** [L48-49]: `def lowest(seq_ids, n) -> np.ndarray`
- **function `history_table`** [L52-59]: `def history_table(canon32, seq_ids, panel) -> dict`
- **function `registry_digests`** [L62-63]: `def registry_digests(canon32) -> set`
- **function `table_union`** [L66-68]: `def table_union(table) -> set`
- **function `_union`** [L71-77]: `def _union(x) -> set`
- **function `separation`** [L80-84]: `def separation(U_cal, U_val, R1) -> dict`
- **function `_file_sha`** [L87-88]: `def _file_sha(path) -> str`
- **function `build_registry`** [L91-112]: `def build_registry(sources) -> dict` - Each source: {name, path, meta, reader?}. reader(path) -> canonical uint8 [n, 32]; the
- **function `first_token_ok`** [L115-120]: `def first_token_ok(first, pE, split) -> bool`

