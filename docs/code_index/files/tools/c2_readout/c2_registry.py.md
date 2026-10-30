# `tools/c2_readout/c2_registry.py`

- Source: [tools/c2_readout/c2_registry.py](../../../../../tools/c2_readout/c2_registry.py)
- Kind: python
- Lines: 394

## Module docstring

> C2 exposure registry c2-reg-v1: the R and R' sources (the reused C1'/K4b readers a-f, k and
> the X6S1 reader x6), the run-time inventory against the frozen table, builds, loading and the
> split separation (API.md §5, §18, §19.3; C2-FROZEN-v2 §5.3, §7 rows 4, 5, 22). Identity-only
> access; H^Y enters only where it is defined.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 18, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 21, via unique basename)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 22, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 23, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 24, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 25, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 27, via unique basename)
- `from topo_pilot.dataset.checks import check_disjoint` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 29, via package root)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 102, via unique basename) (inside a function)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 135, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 136, via package root) (inside a function)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 329, via unique basename) (inside a function)
- `import x6s1_registry` -> [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 354, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 26)

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `itertools` (lines 15)
- `json` (lines 13)
- `pathlib` (lines 16)
- `time` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_registry.py](../../tests/c2_nd/test_b_registry.py.md) (line 25, import)
- [tests/c2_readout/test_b_lineage.py](../../tests/c2_readout/test_b_lineage.py.md) (line 26, import)
- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 25, import)
- [tests/hwsc/test_b_registry2.py](../../tests/hwsc/test_b_registry2.py.md) (line 28, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 28, import)
- [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 26, import)
- [tools/c2_nd/nd_split.py](../c2_nd/nd_split.py.md) (line 21, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 27, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 24, import)
- [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 13, import)
- [tools/hwsc/hwsc_driver.py](../hwsc/hwsc_driver.py.md) (line 177, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 135, import)
- [tools/hwsc/hwsc_dry2.py](../hwsc/hwsc_dry2.py.md) (line 181, import)
- [tools/hwsc/hwsc_registry.py](../hwsc/hwsc_registry.py.md) (line 12, import)
- [tools/hwsc/hwsc_registry_build.py](../hwsc/hwsc_registry_build.py.md) (line 13, import)

## Top-level constants

- `COUNT_KEYS`
- `EXCLUDE`
- `INVENTORY`
- `OWN`
- `OWN_READERS`
- `SRC_KEYS`
- `VERSIONS`

## Classes and functions

- **class `RegistryLineage(RuntimeError)`** [L42-47] - A registry binding or re-hash mismatch; `.status` is FAIL_TECHNICAL/LINEAGE.
- **method `RegistryLineage.__init__`** [L45-47]: `def __init__(self, detail: str)`
- **function `_root`** [L50-51]: `def _root(root) -> Path`
- **function `_try`** [L54-59]: `def _try(problems, tag, fn)`
- **function `_x6_member`** [L63-74]: `def _x6_member(xr, key, arr, entry)` - Digest chunks of one history-bearing member (token columns 0..31, or hex digests).
- **function `_x6_chunks`** [L77-96]: `def _x6_chunks(xr, store, files, other)`
- **function `x6_source`** [L99-128]: `def x6_source(store=None, run_dir=None) -> dict` - X6-REG2 (re-hashed, manifest bound by CONTRACT.json) as base plus every other history-
- **function `token_sources`** [L132-158]: `def token_sources(root=None) -> dict` - Readers a, b, c, d, e, k through the reused K4b/C1' functions; failures become problems
- **function `_static_readers`** [L162-165]: `def _static_readers() -> dict`
- **function `_tags`** [L168-171]: `def _tags(rec, readers) -> list`
- **function `_violation`** [L174-189]: `def _violation(name, entry, rec, cls, readers) -> str | None`
- **function `inventory`** [L192-211]: `def inventory(root=None, readers=None) -> dict` - k4b_registry.inventory/classify of every top-level directory, checked against the frozen
- **function `_ok_readers`** [L215-223]: `def _ok_readers(src, x6_ok) -> dict`
- **function `_x6_manifest`** [L226-234]: `def _x6_manifest(res, out_dir) -> dict`
- **function `_entry`** [L237-238]: `def _entry(s, kind, n, canon) -> dict`
- **function `build`** [L241-302]: `def build(version, store=None, root=None, extra=None) -> dict` - C2-REG1 (before FIT) or C2-REG2 (R' with the FIT/FEAS/VAL tables in `extra`, keyed by
- **class `Registry`** [L306-357]
- **method `Registry.__init__`** [L307-310]: `def __init__(self, digests, x6, sealed_ranges, predicates, manifest, seq_ids=())`
- **method `Registry.load`** [L313-325]: `def load(cls, store=None, version='C2-REG1') -> Registry` decorators: @classmethod - Re-hashes the digest file and the own x6 runs; the base runs via X6-REG2.
- **method `Registry._x6`** [L328-348]: `def _x6(reg, x6m)` decorators: @staticmethod
- **method `Registry.contains`** [L350-357]: `def contains(self, hex_digests) -> np.ndarray`
- **function `separation`** [L360-386]: `def separation(reg, tables) -> dict` - Every split's role union (H^Y where defined) disjoint from R and from every other split; ids
- **function `first_token_ok`** [L389-394]: `def first_token_ok(table, T, E_canon, pi, split) -> bool` - c1_data.first_token_ok on the first symbols of every 4096-row block.

