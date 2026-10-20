# `tests/x2a_stage0/test_x2a_stage0.py`

- Source: [tests/x2a_stage0/test_x2a_stage0.py](../../../../../tests/x2a_stage0/test_x2a_stage0.py)
- Kind: python
- Lines: 386

## Module docstring

> Independent tests of tools/x2a_stage0 (job 0025), part 1: construction, exact laws, JS, nulls.

## Imports

### Internal (repo files)

- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 19, via package root)
- `from topo_pilot.process import _geometry` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 20, via package root)
- `from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 21, via package root)
- `from topo_pilot.process.transition import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/transition.py](../../src/topo_pilot/process/transition.py.md) (line 22, via package root)
- `from topo_pilot.world import WORLD_REGISTRY, CubicalComplex, Identification` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 23, via package root)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 35, via sys.path edit)
- `import x2a_mc` -> [tools/x2a_stage0/x2a_mc.py](../../tools/x2a_stage0/x2a_mc.py.md) (line 36, via sys.path edit)
- `import x2a_model` -> [tools/x2a_stage0/x2a_model.py](../../tools/x2a_stage0/x2a_model.py.md) (line 37, via sys.path edit)
- `import x2a_ph` -> [tools/x2a_stage0/x2a_ph.py](../../tools/x2a_stage0/x2a_ph.py.md) (line 38, via sys.path edit)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 7)
- `decimal` (lines 12)
- `fractions` (lines 13)
- `importlib` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 14)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `spec_from_file_location` line 351: `dynamic: MODULE_DIR / f'{name}.py'`

### sys.path additions

- line 32: `str(REPO_ROOT.joinpath(*_parts))` -> `tests/oracle_profile`, `tools/x2a_stage0`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CENTRES`
- `GRID`
- `LN2`
- `MODULE_DIR`
- `REPO_ROOT`
- `VARIANTS`
- `_REGISTRY_AFTER_IMPORT`
- `_REGISTRY_BEFORE_IMPORT`

## Classes and functions

- **function `ref_d12`** [L50-52]: `def ref_d12(u, v) -> np.ndarray`
- **function `ref_e`** [L53-55]: `def ref_e() -> np.ndarray`
- **function `ref_field_2d`** [L56-70]: `def ref_field_2d(mode: str = 'min') -> np.ndarray` - G1 reference: squared distance over the 9 deck images (m, n in {-1, 0, 1}), then a 2-D
- **function `ref_neighbours`** [L71-73]: `def ref_neighbours(i: int) -> set[int]`
- **function `ref_G`** [L74-75]: `def ref_G(e: np.ndarray, d: int) -> float`
- **function `ref_pair`** [L76-77]: `def ref_pair(T: np.ndarray, E: np.ndarray) -> np.ndarray`
- **function `ref_law2`** [L78-82]: `def ref_law2(T: np.ndarray, E: np.ndarray) -> np.ndarray`
- **function `ref_law3`** [L83-88]: `def ref_law3(T: np.ndarray, E: np.ndarray) -> np.ndarray`
- **function `ref_js`** [L89-95]: `def ref_js(pa, pb) -> float`
- **function `ref_acc`** [L96-97]: `def ref_acc(pa, pb) -> float`
- **function `ref_phi`** [L98-102]: `def ref_phi(r: float) -> float`
- **function `spec`** [L106-107]: `def spec()` decorators: @pytest.fixture(scope='module')
- **function `models`** [L109-110]: `def models(spec)` decorators: @pytest.fixture(scope='module')
- **test `test_constants_and_index_helpers`** [L113-127]: `def test_constants_and_index_helpers()`
- **test `test_E_A_matches_minimum_image_softmax`** [L130-141]: `def test_E_A_matches_minimum_image_softmax()`
- **test `test_summed_images_differ_from_minimum_image`** [L142-146]: `def test_summed_images_differ_from_minimum_image()`
- **test `test_world_counts_betti_and_builder`** [L149-166]: `def test_world_counts_betti_and_builder(spec)`
- **test `test_kernel_matches_fraction_formula`** [L167-177]: `def test_kernel_matches_fraction_formula(spec)`
- **test `test_mixture_blocks_and_stationarity`** [L178-189]: `def test_mixture_blocks_and_stationarity(models)`
- **test `test_emission_variants_against_reference`** [L192-236]: `def test_emission_variants_against_reference(spec, models)`
- **test `test_T1_T2_and_lemma_U_closed_forms`** [L239-262]: `def test_T1_T2_and_lemma_U_closed_forms(models)`
- **test `test_exact_enumeration_k2_k3`** [L265-289]: `def test_exact_enumeration_k2_k3(models)`
- **test `test_js_on_toy_laws_and_series_branch`** [L292-319]: `def test_js_on_toy_laws_and_series_branch()`
- **test `test_null_and_swap_identities_on_short_histories`** [L322-343]: `def test_null_and_swap_identities_on_short_histories(models)`
- **test `test_registry_untouched_by_import_and_build`** [L346-360]: `def test_registry_untouched_by_import_and_build(monkeypatch)`
- **test `test_geometry_helpers_are_never_called`** [L363-378]: `def test_geometry_helpers_are_never_called(monkeypatch)`
- **test `test_module_files_at_most_400_lines`** [L382-386]: `def test_module_files_at_most_400_lines(name)` decorators: @pytest.mark.parametrize('name', ['x2a_model', 'x2a_mc', 'x2a_ph'])

