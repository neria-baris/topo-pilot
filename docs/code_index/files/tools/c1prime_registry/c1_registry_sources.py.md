# `tools/c1prime_registry/c1_registry_sources.py`

- Source: [tools/c1prime_registry/c1_registry_sources.py](../../../../../tools/c1prime_registry/c1_registry_sources.py)
- Kind: python
- Lines: 312

## Module docstring

> C1' exposure registry v1: per-source readers for the frozen c1_data.build_registry (job 0027;
> protocol §2.4 sources a-c, §16 row 2). Kept outside tools/c1prime so the job-0026 frozen
> file set is unchanged. Identity-only: token arrays and identity columns (sequence
> id, history id) are read; no scored diagnostic, activation or endpoint is decoded.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../c1prime/c1_config.py.md) (line 20, via sys.path edit)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 21, via sys.path edit)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 53, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 54, via package root) (inside a function)
- `from topo_pilot.contracts import EmissionSpec, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 61, via package root) (inside a function)
- `from topo_pilot.contracts import HistoryIndex` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 194, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 15)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(Path(__file__).resolve().parents[1] / 'c1prime')` -> `tools/c1prime`

## Imported by

- [tests/c1prime_registry/test_registry_builder.py](../../tests/c1prime_registry/test_registry_builder.py.md) (line 20, import)
- [tests/k4b/test_b_data.py](../../tests/k4b/test_b_data.py.md) (line 26, import)
- [tests/k4b/test_b_registry.py](../../tests/k4b/test_b_registry.py.md) (line 29, import)
- [tests/k4b/test_b_registry_fixes.py](../../tests/k4b/test_b_registry_fixes.py.md) (line 28, import)
- [tests/k4b/test_b_registry_rules.py](../../tests/k4b/test_b_registry_rules.py.md) (line 32, import)
- [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 20, import)
- [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 22, import)
- [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 17, import)
- [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 21, import)

## Top-level constants

- `ART`
- `EMPTY`
- `NOT_SCANNED`
- `ROOT`
- `SCANNED_STORES`

## Classes and functions

- **function `sha`** [L28-29]: `def sha(path) -> str`
- **function `_u8`** [L32-41]: `def _u8(tokens) -> np.ndarray` - First 32 columns as uint8 after checking integer dtype and the 0..255 range (no silent
- **function `canonical32`** [L44-49]: `def canonical32(named, perm) -> np.ndarray` - canonical = argsort(perm)[named] (K4 CONTRACT symbols), first 32 tokens.
- **function `_store`** [L52-56]: `def _store()`
- **function `observation_set_sources`** [L59-82]: `def observation_set_sources(store=None, root=ART) -> tuple` - Source (a): every ObservationSet, canonicalised with its own EmissionSpec perm.
- **function `_npz_tokens`** [L85-89]: `def _npz_tokens(key)`
- **function `_empty`** [L92-95]: `def _empty(reason)`
- **function `store_sources`** [L98-146]: `def store_sources(root=ROOT) -> list` - Source (b): the stores named in §2.4(b), each recorded explicitly (empty ones included).
- **function `reference_cache_reader`** [L149-156]: `def reference_cache_reader(path) -> np.ndarray`
- **function `_token_lists`** [L159-168]: `def _token_lists(obj, found)`
- **function `handoff_sources`** [L171-189]: `def handoff_sources(root=ROOT / 'agent-handoff') -> list` - Source (c): every JSON under agent-handoff (excluding .git and CLI logs) scanned for
- **function `history_index_ids`** [L192-202]: `def history_index_ids(store=None, root=ART) -> dict` - history_id -> sequence_id over every HistoryIndex (identity columns only).
- **function `coverage`** [L205-234]: `def coverage(seqs_a: dict, hist_ids: dict, root=ROOT) -> dict` - Id-only stores reference only histories of source (a) (or of a scanned store).
- **function `store_file_hashes`** [L255-264]: `def store_file_hashes(dirs=SCANNED_STORES, root=ROOT) -> dict` - Content hash of every file of each scanned store (binding, not a filename listing).
- **function `history_index_hashes`** [L267-269]: `def history_index_hashes(root=ART) -> dict`
- **function `build`** [L272-304]: `def build(out_dir) -> dict`

