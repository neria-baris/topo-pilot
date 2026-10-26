# `tests/hws/test_b_worlds.py`

- Source: [tests/hws/test_b_worlds.py](../../../../../tests/hws/test_b_worlds.py)
- Kind: python
- Lines: 394

## Module docstring

> Author B (job 0119), TEST_PLAN §3 `test_b_worlds.py`: grid, keys, X1 worlds, tiers, the
> rectangular centres, the emission builders (canonical OverlapGaussian at W = 12 bitwise, the
> mirrored softmax elsewhere), features, the anchored alias map (CONTRACT `alias.maps`, §4.3
> table), merging, symbol sizes, the known-zero and tiny builders, E3 symmetry, E2 and the
> E1 -> E2 -> E3 order. Protocol §4.1-§4.6, §5.1; DR3, DR4, DR5.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 26, via sys.path edit)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 28, via unique basename)
- `from topo_pilot.contracts import ErrorCode, SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.process import EmissionConfig, GridCenters, OverlapGaussian, TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 31, via package root)
- `from topo_pilot.process._geometry import point_distances` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 38, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 39, via package root)
- `from topo_pilot.world import build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 40, via package root)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)
- `scipy` (lines 29)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 16)
- `json` (lines 13)
- `math` (lines 14)
- `pathlib` (lines 17)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / 'tools' / 'hws')` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `ASYMMETRIC`
- `CELLS`
- `CONTRACT`
- `PROTOCOL_VPRIME`
- `P_LEVELS`
- `REPO`
- `SYMMETRIC`
- `S_LEVELS`

## Classes and functions

- **function `_key`** [L52-53]: `def _key(W, q, s, p) -> str`
- **function `_world`** [L56-57]: `def _world(W, Hh=12)`
- **function `_mirrored`** [L60-64]: `def _mirrored(world, centres, sigma)` - The 4-line softmax of emission._overlap_core, written here independently.
- **function `_g`** [L67-69]: `def _g(W, q) -> list`
- **function `_perm_reflect`** [L72-73]: `def _perm_reflect(W, Hh, c)`
- **test `test_grid_has_225_worlds_in_the_stated_order`** [L78-86]: `def test_grid_has_225_worlds_in_the_stated_order()`
- **test `test_world_keys`** [L89-96]: `def test_world_keys()`
- **test `test_level_constants_match_contract`** [L99-110]: `def test_level_constants_match_contract()`
- **test `test_x1_world_counts_and_order`** [L116-128]: `def test_x1_world_counts_and_order(add_p, add_sigma, count)` decorators: @pytest.mark.parametrize('add_p, add_sigma, count', [(True, False, 30), (False, True, 60), (True, True, 102), (False, False, 0)])
- **test `test_tiers`** [L131-138]: `def test_tiers()`
- **test `test_centres_rectangular_and_gridcenters_bitwise`** [L143-154]: `def test_centres_rectangular_and_gridcenters_bitwise()`
- **test `test_w12_emission_is_the_canonical_overlap_bitwise`** [L158-165]: `def test_w12_emission_is_the_canonical_overlap_bitwise(sigma)` decorators: @pytest.mark.parametrize('sigma', [F(5, 4), F(2), F(11, 8)])
- **test `test_other_circumferences_build`** [L169-187]: `def test_other_circumferences_build(W, N, V)` decorators: @pytest.mark.parametrize('W, N, V', [(8, 96, 24), (16, 192, 48)])
- **test `test_features_equal_circle_features_and_posterior_means`** [L190-204]: `def test_features_equal_circle_features_and_posterior_means()`
- **test `test_repeated_builds_are_identical`** [L207-212]: `def test_repeated_builds_are_identical()`
- **test `test_anchored_labels_match_contract_and_formula`** [L219-234]: `def test_anchored_labels_match_contract_and_formula(W, q)` decorators: @pytest.mark.parametrize('W', [6, 8, 12, 16]) @pytest.mark.parametrize('q', [1, 2, 3])
- **test `test_unanchored_labels`** [L237-242]: `def test_unanchored_labels()`
- **test `test_merge_columns_sums_never_averages`** [L246-257]: `def test_merge_columns_sums_never_averages(W, q)` decorators: @pytest.mark.parametrize('W, q', [(8, 2), (12, 2), (12, 3), (16, 3), (16, 1)])
- **test `test_merge_q1_w12_is_identity_and_tiny_merge`** [L260-266]: `def test_merge_q1_w12_is_identity_and_tiny_merge()`
- **test `test_build_tiny_world`** [L271-291]: `def test_build_tiny_world()`
- **test `test_known_zero_builders`** [L294-299]: `def test_known_zero_builders()`
- **test `test_state_maps`** [L304-311]: `def test_state_maps()`
- **test `test_reflection_symmetric_cells`** [L315-322]: `def test_reflection_symmetric_cells(W, q)` decorators: @pytest.mark.parametrize('W, q', SYMMETRIC)
- **test `test_asymmetric_cells`** [L326-331]: `def test_asymmetric_cells(W, q)` decorators: @pytest.mark.parametrize('W, q', ASYMMETRIC)
- **test `test_unanchored_and_tiny_maps`** [L334-342]: `def test_unanchored_and_tiny_maps()`
- **test `test_e2_threshold_boundaries`** [L347-361]: `def test_e2_threshold_boundaries()`
- **test `test_exact_filters_order_e1_e2_e3`** [L364-376]: `def test_exact_filters_order_e1_e2_e3()`
- **test `test_builder_failures_are_e1`** [L379-394]: `def test_builder_failures_are_e1(monkeypatch)`

