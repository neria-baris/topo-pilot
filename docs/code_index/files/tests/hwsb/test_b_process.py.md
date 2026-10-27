# `tests/hwsb/test_b_process.py`

- Source: [tests/hwsb/test_b_process.py](../../../../../tests/hwsb/test_b_process.py)
- Kind: python
- Lines: 194

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_process.py`: `build_process` on a
> MemoryBackend store (KB1 identities, KB4 identity part), `arrays_sha256`, `spec_checksums`,
> IDENTITY failures, and `hwsb_dry.build_tiny_process`. tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 21, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 22, via sys.path edit)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 23, via sys.path edit)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, MemoryBackend, SeedTree, payload_checksum` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.process.emission import EmissionConfig` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 27, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `fractions` (lines 11)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `KB1`
- `KB2`
- `REPO`
- `W0_CFG`

## Classes and functions

- **function `f64_sha`** [L35-36]: `def f64_sha(x)`
- **function `star`** [L40-42]: `def star()` decorators: @pytest.fixture(scope='module')
- **function `w0`** [L46-48]: `def w0()` decorators: @pytest.fixture(scope='module')
- **test `test_star_ids_match_contract`** [L52-56]: `def test_star_ids_match_contract(star)`
- **test `test_star_shapes_and_constants`** [L59-67]: `def test_star_shapes_and_constants(star)`
- **test `test_star_spec_checksums_match_contract`** [L70-77]: `def test_star_spec_checksums_match_contract(star)`
- **test `test_star_arrays_sha256_equal_selection`** [L80-87]: `def test_star_arrays_sha256_equal_selection(star)`
- **test `test_star_e_canon_is_shared_and_named_inverts`** [L90-101]: `def test_star_e_canon_is_shared_and_named_inverts(star)`
- **test `test_star_canonical_symbol_is_axial_cell_centre`** [L104-113]: `def test_star_canonical_symbol_is_axial_cell_centre(star)`
- **test `test_w0_emission_identity_matches_contract`** [L117-126]: `def test_w0_emission_identity_matches_contract(w0)`
- **class `PlantedStore(ArtifactStore)`** [L130-142] - Returns a modified EmissionSpec for one planted artifact id (planted defect fixture).
- **method `PlantedStore.__init__`** [L133-135]: `def __init__(self, target, mutate)`
- **method `PlantedStore.load`** [L137-142]: `def load(self, cls, artifact_id, *, consumer)`
- **function `set_attr`** [L145-146]: `def set_attr(obj, name, value)`
- **test `test_non_permutation_perm_is_identity_failure`** [L149-154]: `def test_non_permutation_perm_is_identity_failure(star)`
- **test `test_differing_e_canon_is_identity_failure`** [L157-168]: `def test_differing_e_canon_is_identity_failure(star)`
- **test `test_build_tiny_process_shapes_and_naming`** [L172-189]: `def test_build_tiny_process_shapes_and_naming()`
- **test `test_build_tiny_process_masters_argument`** [L192-194]: `def test_build_tiny_process_masters_argument()`

