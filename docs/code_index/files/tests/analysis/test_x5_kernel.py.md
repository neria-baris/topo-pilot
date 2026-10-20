# `tests/analysis/test_x5_kernel.py`

- Source: [tests/analysis/test_x5_kernel.py](../../../../../tests/analysis/test_x5_kernel.py)
- Kind: python
- Lines: 230

## Module docstring

> Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import SpectrumReport, integrated_autocorrelation, is_connected, movement_rate, rate_matched_kernel, spectrum_report` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 16, via package root)
- `from topo_pilot.contracts.testing import tiny_hmm` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 24, via package root)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 9)
- `math` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `HALF`
- `U4`

## Classes and functions

- **function `_two_state`** [L29-30]: `def _two_state(p: float) -> np.ndarray`
- **function `_blocks`** [L33-38]: `def _blocks() -> np.ndarray` - Block-diagonal (reducible) 4-state chain: two lazy 2-state blocks.
- **test `test_movement_rate_hand_value_nonuniform_pi`** [L48-51]: `def test_movement_rate_hand_value_nonuniform_pi()`
- **test `test_movement_rate_lazy_cycle`** [L54-57]: `def test_movement_rate_lazy_cycle()`
- **test `test_is_connected_true_false`** [L63-67]: `def test_is_connected_true_false()`
- **test `test_is_connected_uses_either_direction`** [L70-73]: `def test_is_connected_uses_either_direction()`
- **test `test_spectrum_two_state_hand_values`** [L79-87]: `def test_spectrum_two_state_hand_values()`
- **test `test_spectrum_abs_gap_uses_negative_eigenvalue`** [L90-96]: `def test_spectrum_abs_gap_uses_negative_eigenvalue()`
- **test `test_spectrum_eigenvalues_descending_lazy_cycle`** [L99-106]: `def test_spectrum_eigenvalues_descending_lazy_cycle()`
- **test `test_mixing_bound_uses_ceil`** [L109-116]: `def test_mixing_bound_uses_ceil()`
- **test `test_mixing_bound_eps_and_pi_min`** [L119-124]: `def test_mixing_bound_eps_and_pi_min()`
- **test `test_spectrum_reducible_status`** [L127-130]: `def test_spectrum_reducible_status()`
- **test `test_spectrum_near_unit_gap_status`** [L133-139]: `def test_spectrum_near_unit_gap_status()`
- **test `test_iat_two_state_hand_value`** [L146-150]: `def test_iat_two_state_hand_value(p)` decorators: @pytest.mark.parametrize('p', [0.1, 0.3, 0.45])
- **test `test_iat_two_state_p01_is_nine`** [L153-155]: `def test_iat_two_state_p01_is_nine()`
- **test `test_iat_eigenfunction_of_lazy_cycle`** [L158-165]: `def test_iat_eigenfunction_of_lazy_cycle()`
- **test `test_iat_affine_invariance`** [L168-180]: `def test_iat_affine_invariance()`
- **test `test_iat_constant_function_undefined`** [L183-188]: `def test_iat_constant_function_undefined()`
- **test `test_iat_reducible`** [L191-193]: `def test_iat_reducible()`
- **test `test_rate_matched_valid_equals_formula`** [L199-204]: `def test_rate_matched_valid_equals_formula()`
- **test `test_rate_matched_diag_boundary`** [L207-211]: `def test_rate_matched_diag_boundary()`
- **test `test_rate_matched_nonpositive_alpha_invalid`** [L215-218]: `def test_rate_matched_nonpositive_alpha_invalid(alpha)` decorators: @pytest.mark.parametrize('alpha', [0.0, -0.5])
- **test `test_rate_matched_negative_entry_invalid`** [L221-224]: `def test_rate_matched_negative_entry_invalid()`
- **test `test_rate_matched_diag_below_floor_invalid`** [L227-230]: `def test_rate_matched_diag_below_floor_invalid()`

