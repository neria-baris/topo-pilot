# `tests/c1prime/test_b_frames.py`

- Source: [tests/c1prime/test_b_frames.py](../../../../../tests/c1prime/test_b_frames.py)
- Kind: python
- Lines: 173

## Module docstring

> Independent tests (author B, job 0026), TEST_PLAN B-3 part 2: Haar frames and the M1 identities.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../../tools/c1prime/c1_fit.py.md) (line 28, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `D`
- `REPO`
- `TWO_PI`

## Classes and functions

- **function `_status`** [L36-37]: `def _status(res) -> str`
- **function `_qr_pos`** [L40-42]: `def _qr_pos(M) -> np.ndarray`
- **function `_f`** [L45-46]: `def _f(phi) -> np.ndarray`
- **function `_frame`** [L49-51]: `def _frame(model_seed, r) -> np.ndarray`
- **function `_family`** [L54-65]: `def _family(seed, rows=24)`
- **function `fam`** [L69-70]: `def fam()` decorators: @pytest.fixture(scope='module')
- **function `_m1`** [L73-77]: `def _m1(f, Dp=None, Dm=None, cp=None, cm=None, frames=None)`
- **test `test_qr_pos_matches_numpy_with_a_positive_diagonal`** [L83-91]: `def test_qr_pos_matches_numpy_with_a_positive_diagonal()`
- **test `test_haar_frames_are_the_seeded_streams`** [L94-103]: `def test_haar_frames_are_the_seeded_streams()`
- **test `test_primary_coordinates_basis_and_isometry`** [L106-111]: `def test_primary_coordinates_basis_and_isometry(fam)`
- **test `test_control_displacement_isometry_and_the_same_frame_on_both_arms`** [L114-126]: `def test_control_displacement_isometry_and_the_same_frame_on_both_arms(fam)`
- **test `test_m1_passes_on_a_consistent_family`** [L132-133]: `def test_m1_passes_on_a_consistent_family(fam)`
- **test `test_m1_fails_on_a_frame_that_is_not_orthonormal`** [L136-139]: `def test_m1_fails_on_a_frame_that_is_not_orthonormal(fam)`
- **test `test_m1_fails_when_the_coordinates_lose_norm`** [L142-143]: `def test_m1_fails_when_the_coordinates_lose_norm(fam)`
- **test `test_m1_fails_when_the_displacement_leaves_span_WB`** [L146-149]: `def test_m1_fails_when_the_displacement_leaves_span_WB(fam)`
- **test `test_m1_zero_primary_norm_requires_exact_zeros`** [L152-158]: `def test_m1_zero_primary_norm_requires_exact_zeros(fam)`
- **test `test_m1_all_zero_displacements_use_the_zero_spectrum_rule`** [L161-163]: `def test_m1_all_zero_displacements_use_the_zero_spectrum_rule(fam)`
- **test `test_m1_frame_from_an_exactly_rank_deficient_draw_fails`** [L166-173]: `def test_m1_frame_from_an_exactly_rank_deficient_draw_fails(fam)`

