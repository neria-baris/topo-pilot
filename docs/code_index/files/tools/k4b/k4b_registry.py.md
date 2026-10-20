# `tools/k4b/k4b_registry.py`

- Source: [tools/k4b/k4b_registry.py](../../../../../tools/k4b/k4b_registry.py)
- Kind: python
- Lines: 389

## Module docstring

> K4b exposure registry (API.md §3; protocol §3.4, RC6, RC7). Identity-only access.

## Imports

### Internal (repo files)

- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 16, via unique basename)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 17, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 18, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 20, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 21, via unique basename)
- `from k4b_registry_k import HISTORY_KEYS, IDENTITY_KEYS, INCOMPLETE, _history_arrays, _npz_header, _sha, source_k, summary` -> [tools/k4b/k4b_registry_k.py](k4b_registry_k.py.md) (line 22, via same directory)
- `from topo_pilot.contracts import ArtifactStore, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 190, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 191, via package root) (inside a function)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 242, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 243, via package root) (inside a function)
- `from topo_pilot.contracts import ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 265, via package root) (inside a function)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 300, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 301, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `time` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_b_registry.py](../../tests/k4b/test_b_registry.py.md) (line 31, import)
- [tests/k4b/test_b_registry_fixes.py](../../tests/k4b/test_b_registry_fixes.py.md) (line 30, import)
- [tests/k4b/test_b_registry_rules.py](../../tests/k4b/test_b_registry_rules.py.md) (line 34, import)
- [tests/k4b/test_b_store_reader.py](../../tests/k4b/test_b_store_reader.py.md) (line 38, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 354, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 387, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 19, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 21, import)
- [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 22, import)

## Top-level constants

- `ART`
- `KS`
- `LINEAGE`
- `OWN_READERS`
- `ROOT`
- `VERSIONS`

## Classes and functions

- **function `inventory`** [L43-66]: `def inventory(root=ROOT, exclude=()) -> dict` - Every top-level directory of root (main too, R23 rule 3), recursively: history files with
- **function `_under`** [L69-74]: `def _under(path, base) -> bool`
- **function `_in_segment`** [L77-82]: `def _in_segment(dirs) -> bool` - R23 rule 2(a): a pytest-of-* directory, or bt*/pt-* directly under tmp-*/coord-scratch.
- **function `_fixture`** [L85-89]: `def _fixture(name, top, path, shapes) -> bool` - R23 rules 2-4: path rule (main: tests/, .venv or a segment) and <= 1,024 history rows.
- **function `classify`** [L92-131]: `def classify(inv, scanned_readers) -> dict` - SCANNED (a reader covers it), NOT_SCANNED (nothing found, or only synthetic test fixtures),
- **function `validate_handoff_json`** [L134-141]: `def validate_handoff_json(root) -> dict`
- **function `source_a`** [L144-147]: `def source_a(root_art, store=None) -> tuple`
- **function `source_b`** [L150-151]: `def source_b(root=ROOT) -> list`
- **function `source_c`** [L154-158]: `def source_c(root=ROOT / 'agent-handoff') -> list`
- **function `source_d`** [L161-179]: `def source_d(store=ROOT / 'c1prime-store') -> list`
- **function `_npz_raw32`** [L182-184]: `def _npz_raw32(path) -> np.ndarray`
- **function `_d2a_reader`** [L187-202]: `def _d2a_reader(store, pool, entry)` - A permitted pool's raw tokens[:, :32] (uint8, no canonicalisation).
- **function `source_e`** [L205-236]: `def source_e(store=ROOT / 'd2a-store', pools_meta=None) -> dict`
- **function `source_f`** [L239-260]: `def source_f(root, inv, classes) -> list` - ObservationSet stores under other directories, canonicalised by their EmissionSpec perm
- **function `_raw_reader`** [L263-268]: `def _raw_reader(store, oid)`
- **function `revalidate_coverage`** [L271-287]: `def revalidate_coverage(root_art, root=ROOT, extra_ids=None, store=None, seqs_a=None) -> dict` - crs.coverage on populated source-(a) ids (R26 D3), then x4b and extra ids by value.
- **function `_try`** [L290-295]: `def _try(problems, tag, fn)`
- **function `build`** [L298-373]: `def build(version, out_dir, root=ROOT, extra=None) -> dict` - Builds K-REG1/K-REG2 from scratch; manifest and digest npz written by exclusive create.
- **function `load`** [L376-389]: `def load(out_dir, version) -> tuple`

