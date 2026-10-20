# `tools/k4b/k4b_registry_k.py`

- Source: [tools/k4b/k4b_registry_k.py](../../../../../tools/k4b/k4b_registry_k.py)
- Kind: python
- Lines: 122

## Module docstring

> K4b registry, reader k for K4b's own store (API.md §16, ruling R28, defect D5).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 9)
- `fnmatch` (lines 11)
- `hashlib` (lines 12)
- `pathlib` (lines 14)
- `zipfile` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/k4b/k4b_registry.py](k4b_registry.py.md) (line 22, import)
- [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 23, import)

## Top-level constants

- `DERIVED`
- `GROUPS`
- `HISTORY_KEYS`
- `IDENTITY_KEYS`
- `INCOMPLETE`

## Classes and functions

- **function `_sha`** [L25-26]: `def _sha(path) -> str`
- **function `_npz_header`** [L29-40]: `def _npz_header(path) -> dict` - {key: (dtype, shape)} from the .npy headers only (no array data, no pickle).
- **function `_history_arrays`** [L43-47]: `def _history_arrays(header) -> dict` - {key: shape} of the history arrays of one npz header (§3.4 history detection).
- **function `_derived`** [L50-53]: `def _derived(parts) -> bool`
- **function `_staged`** [L56-58]: `def _staged(parts) -> bool`
- **function `_stage_source`** [L61-78]: `def _stage_source(f, rel, hist) -> dict` - One own stage table, read in full here (a partial read raises, §16 item 3): every history
- **function `source_k`** [L81-110]: `def source_k(store_root) -> dict` - Classifies every file under k4b-store (§16 item 2 a-d); other non-empty -> INCOMPLETE.
- **function `summary`** [L113-122]: `def summary(res) -> dict` - Manifest `k4b_store` (§16 item 4): counts and sha256s per group; None -> not read.

