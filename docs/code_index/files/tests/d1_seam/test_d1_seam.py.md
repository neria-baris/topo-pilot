# `tests/d1_seam/test_d1_seam.py`

- Source: [tests/d1_seam/test_d1_seam.py](../../../../../tests/d1_seam/test_d1_seam.py)
- Kind: python
- Lines: 399

## Module docstring

> Independent tests of tools/d1_seam (job 0019), from D1-FROZEN-v1, its addendum and API.md only.
> The module is imported, never read; the exact ``ref_*`` reference uses none of its kernels.

## Imports

### Internal (repo files)

- `from topo_pilot.process import _geometry` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 17, via package root)
- `from topo_pilot.process.transition import TransitionBuilder, TransitionConfig` -> [src/topo_pilot/process/transition.py](../../src/topo_pilot/process/transition.py.md) (line 18, via package root)
- `from topo_pilot.world import WORLD_REGISTRY` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 19, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 29, via sys.path edit)
- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 4)
- `decimal` (lines 9)
- `fractions` (lines 10)
- `functools` (lines 11)
- `importlib` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 12)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `spec_from_file_location` line 223: `dynamic: d1_seam.__file__`

### sys.path additions

- line 26: `str(REPO_ROOT.joinpath(*_parts))` -> `tests/oracle_profile`, `tools/d1_seam`

## Imported by

- none

## Top-level constants

- `AX`
- `D_T`
- `E_LIT`
- `GATES`
- `HI_MASS`
- `HI_T`
- `H_A`
- `H_B`
- `H_MAX`
- `KEYS`
- `NU`
- `N_T`
- `REPO_ROOT`
- `_DSTR`
- `_REGISTRY_BEFORE_IMPORT`

## Classes and functions

- **function `_vec`** [L46-47]: `def _vec(spec: str) -> list[Q]`
- **function `_rows`** [L48-49]: `def _rows(*specs: str) -> list[list[Q]]`
- **function `idx`** [L50-51]: `def idx(x: int, y: int) -> int`
- **function `unit`** [L52-53]: `def unit(i: int, n: int = 12) -> list[Q]`
- **function `_vm`** [L54-55]: `def _vm(v, M) -> list[Q]`
- **function `_mix`** [L56-57]: `def _mix(pc, pm, pi)`
- **function `_norm`** [L58-59]: `def _norm(x)`
- **function `rho`** [L60-61]: `def rho(b) -> list[Q]`
- **function `tv`** [L62-65]: `def tv(p, q) -> Q`
- **function `ref_edges`** [L70-73]: `def ref_edges(world: str) -> set[tuple[int, int]]`
- **function `ref_T`** [L74-80]: `def ref_T(world: str) -> list[list[Q]]`
- **function `ref_model`** [L82-94]: `def ref_model(variant: str = 'frozen') -> dict` decorators: @lru_cache(maxsize=None)
- **function `ref_mixture`** [L95-98]: `def ref_mixture(variant: str = 'frozen')`
- **function `ref_forward`** [L99-104]: `def ref_forward(wm, h) -> list[Q]`
- **function `ref_futures`** [L105-109]: `def ref_futures(wm, b)`
- **function `ref_parity`** [L110-115]: `def ref_parity(h) -> tuple[int, int]`
- **function `ref_history`** [L117-133]: `def ref_history(h: tuple, variant: str = 'frozen') -> dict` decorators: @lru_cache(maxsize=None)
- **function `ref_enumerate`** [L135-142]: `def ref_enumerate(K: int) -> dict` decorators: @lru_cache(maxsize=None)
- **function `ref_marginals`** [L143-150]: `def ref_marginals(variant: str, K: int = 8) -> dict`
- **function `check_module`** [L154-159]: `def check_module(h: tuple, variant: str = 'frozen') -> dict`
- **test `test_constants`** [L161-165]: `def test_constants()`
- **test `test_exact_model_matches_reference`** [L167-172]: `def test_exact_model_matches_reference(variant)` decorators: @pytest.mark.parametrize('variant', ['frozen', 'N1', 'N2', 'N3', 'L1', 'L2'])
- **test `test_float_model_is_the_production_kernels`** [L173-185]: `def test_float_model_is_the_production_kernels()`
- **function `_square_boundary`** [L186-191]: `def _square_boundary(cell) -> dict`
- **function `_rank_mod`** [L192-202]: `def _rank_mod(rows, p: int) -> int`
- **test `test_worlds_edges_boundary_and_orientability`** [L203-219]: `def test_worlds_edges_boundary_and_orientability()`
- **test `test_registry_untouched_by_import_and_build`** [L220-229]: `def test_registry_untouched_by_import_and_build(monkeypatch)`
- **test `test_geometry_helpers_are_never_called`** [L230-241]: `def test_geometry_helpers_are_never_called(monkeypatch)`
- **test `test_module_file_at_most_400_lines`** [L242-246]: `def test_module_file_at_most_400_lines()`
- **test `test_h_star_closed_forms_and_chain_identity`** [L248-263]: `def test_h_star_closed_forms_and_chain_identity()`
- **test `test_posterior_isolation_pair`** [L264-281]: `def test_posterior_isolation_pair()`
- **test `test_band_edge_and_h_max_probe`** [L282-295]: `def test_band_edge_and_h_max_probe()`
- **test `test_reachable_counts_by_recursion`** [L296-301]: `def test_reachable_counts_by_recursion()`
- **test `test_exhaustive_enumeration_to_depth_5`** [L302-326]: `def test_exhaustive_enumeration_to_depth_5()`
- **test `test_start_law_artefact_and_decision_phase_mass`** [L327-337]: `def test_start_law_artefact_and_decision_phase_mass()`
- **test `test_gates_pass`** [L339-341]: `def test_gates_pass(name)` decorators: @pytest.mark.parametrize('name', ['G0', 'G0S', 'G0O', 'G1', 'G3', 'G6'])
- **test `test_gate_G2_values`** [L342-349]: `def test_gate_G2_values()`
- **test `test_decimal_trap`** [L352-366]: `def test_decimal_trap()`
- **test `test_controls_N1_N2_null`** [L367-372]: `def test_controls_N1_N2_null()`
- **test `test_control_N3_symmetric_start`** [L373-378]: `def test_control_N3_symmetric_start()`
- **test `test_control_L1_label_leak`** [L379-383]: `def test_control_L1_label_leak()`
- **test `test_control_L2_narrow_interior`** [L384-391]: `def test_control_L2_narrow_interior()`
- **test `test_run_without_passing_preflight_is_invalid`** [L393-399]: `def test_run_without_passing_preflight_is_invalid(tmp_path, preflight)` decorators: @pytest.mark.parametrize('preflight', [{}, {'x': False}])

