# `tools/c2_nd/nd_data.py`

- Source: [tools/c2_nd/nd_data.py](../../../../../tools/c2_nd/nd_data.py)
- Kind: python
- Lines: 163

## Module docstring

> C2ND data: the c2nd-v1 samplers and sequence ids, the needle scan, the cross-lineage hygiene
> check and store admission (API.md §4, §20.3 ND-C35; C2ND-DESIGN-v1 §6.1, §6.6, §3 row 1 (vii)).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 13, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 16, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 17, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 18, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 22, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 23, via package root)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 9)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_lineage.py](../../tests/c2_nd/test_b_lineage.py.md) (line 21, import)

## Top-level constants

- `C2_NEEDLE`
- `LINEAGE`
- `ND_PAYLOAD`
- `NEEDLE`
- `PARALLEL_NEEDLES`
- `PAYLOAD_DIRS`
- `SPLITS`

## Classes and functions

- **function `_scope`** [L35-39]: `def _scope(scope) -> str`
- **function `history_generator`** [L42-45]: `def history_generator(split, block, scope=None) -> np.random.Generator`
- **function `sequence_ids`** [L48-52]: `def sequence_ids(split, block, scope=None) -> np.ndarray`
- **function `sample_block`** [L55-62]: `def sample_block(T, E_canon, pi, split, block, scope=None) -> tuple` - One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once.
- **function `sample_split`** [L65-73]: `def sample_split(T, E_canon, pi, split, blocks, scope=None) -> tuple` - Blocks 0..blocks-1 in block order: canonical uint8 [n, 32], sequence ids, panels.
- **function `_under`** [L82-83]: `def _under(path, base) -> bool`
- **function `namespace_scan`** [L86-110]: `def namespace_scan(root=None, pinned=None, lineage=None) -> dict` - G0 (vi): every file of C2's scanned set whose bytes contain "c2nd-v1" must be pinned C2ND
- **function `_scanned_files`** [L113-123]: `def _scanned_files(base, root, skip=())` - The files under `base` in C2's scanned set, judged on the path relative to `root` (or to
- **function `hygiene_check`** [L126-139]: `def hygiene_check(root=None) -> dict` - §6.6: no C2ND file of C2's scanned set (tools/c2_nd/ except the protocol copy; the C2ND
- **function `store_admission`** [L147-159]: `def store_admission(store, lineage, first_sampling) -> dict` - c2_data.store_admission, and at first sampling also no file under decoys/ or registry/.
- **function `own_records`** [L162-163]: `def own_records(store, stage, lineage) -> dict`

