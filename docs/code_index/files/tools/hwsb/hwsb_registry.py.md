# `tools/hwsb/hwsb_registry.py`

- Source: [tools/hwsb/hwsb_registry.py](../../../../../tools/hwsb/hwsb_registry.py)
- Kind: python
- Lines: 180

## Module docstring

> HWSB H2-B separation and the fail-closed registry reader (API.md §2.4, §2.5; protocol §2.3,
> §6.3, B9a). Split out of hwsb_data by size; hwsb_data re-exports every name, so `hd.<name>`
> keeps working.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 11, via same directory)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 15, via same directory)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 17, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 18, via unique basename)
- `from hwsb_data import BLOCKS, LINEAGE, READER, REGISTRY, canonical32, load_block` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 19, via same directory)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, ObservationSet, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.dataset.checks import check_disjoint` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 9)
- `collections` (lines 12)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 349, import)

## Top-level constants

- none

## Classes and functions

- **function `train_dev_canonical`** [L34-36]: `def train_dev_canonical(store, ids, perm) -> tuple`
- **function `hws_store_digests`** [L39-46]: `def hws_store_digests(root=hc.HWS_STORE, key=hc.KEY) -> dict`
- **function `duplicates`** [L49-58]: `def duplicates(digests) -> dict`
- **function `separation`** [L61-87]: `def separation(blocks, train_dev, hws=None) -> dict`
- **function `_rel`** [L90-91]: `def _rel(store, f) -> str`
- **function `history_inventory`** [L94-104]: `def history_inventory(store) -> dict` - {relpath: sha256} of every file under artifacts/ObservationSet/, hist/, superseded/.
- **function `_art_roots`** [L107-112]: `def _art_roots(store) -> list`
- **function `_os_digests`** [L115-123]: `def _os_digests(root, aid) -> list`
- **function `registry_digests`** [L126-180]: `def registry_digests(store, expected=None) -> dict` - Fail-closed digest reader of every stage-B history (B9a ii).

