# `tests/circle_history/test_chart_extension.py`

- Source: [tests/circle_history/test_chart_extension.py](../../../../../tests/circle_history/test_chart_extension.py)
- Kind: python
- Lines: 391

## Module docstring

> Independent synthetic tests, author A (spec v2.3): chart.extend, agreement, bins,
> resultant and chart_gates (TEST_PLAN A11, A12, A15).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 26, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 10)
- `dataclasses` (lines 12)
- `json` (lines 13)
- `math` (lines 14)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `ARRAY_FIELDS`
- `CHART_KEYS`
- `EVEN`
- `GAUGE0`
- `PHI24`
- `PKG`
- `Q_BELOW`
- `Q_CENTRE`
- `REPO_ROOT`
- `RING_X`
- `TWO_PI`

## Classes and functions

- **function `make_cfg`** [L42-47]: `def make_cfg(**overrides)`
- **function `make_ids`** [L50-51]: `def make_ids(n)`
- **function `circle_points`** [L54-57]: `def circle_points(theta)`
- **function `square_ring`** [L60-65]: `def square_ring(side=6)` - Boundary of [0,6]^2, counter-clockwise from (0,0): k0..5 bottom, k6..11 right
- **function `ring_chart`** [L76-77]: `def ring_chart()` decorators: @pytest.fixture(scope='module')
- **function `custom`** [L80-81]: `def custom(base, **changes)`
- **function `circ_gap`** [L84-85]: `def circ_gap(a, b)`
- **function `ref_row`** [L88-100]: `def ref_row(landmarks, phi_g, sigma, q, nearest=None)` - Written formula: stable 8-NN, log-shifted Gaussian weights, exact-duplicate rule.
- **test `test_extend_formula_and_stable_ties`** [L104-127]: `def test_extend_formula_and_stable_ties(ring_chart)`
- **test `test_extend_eighth_distance_boundary`** [L130-137]: `def test_extend_eighth_distance_boundary(ring_chart)`
- **function `split_phases`** [L140-146]: `def split_phases(at_zero)` - Phases for the 8 nearest of Q_BELOW (k3,k2,k4,k1,k5,k0,k6,k7): `at_zero` of them 0.
- **test `test_extend_resultant_boundary`** [L149-165]: `def test_extend_resultant_boundary(ring_chart)`
- **test `test_extend_exact_duplicates_average_all`** [L168-191]: `def test_extend_exact_duplicates_average_all(ring_chart)`
- **test `test_extend_never_mutates`** [L194-205]: `def test_extend_never_mutates(ring_chart)`
- **function `explicit_agreement`** [L208-210]: `def explicit_agreement(a, b)`
- **test `test_extend_held_out_circle_agrees_with_direct`** [L213-226]: `def test_extend_held_out_circle_agrees_with_direct()`
- **test `test_far_query_keeps_exact_normalised_weights`** [L230-246]: `def test_far_query_keeps_exact_normalised_weights(ring_chart)`
- **test `test_far_query_with_fitted_scale_unsupported`** [L249-253]: `def test_far_query_with_fitted_scale_unsupported(ring_chart)`
- **test `test_extend_nonfinite_z_invalid`** [L257-266]: `def test_extend_nonfinite_z_invalid(ring_chart, field)` decorators: @pytest.mark.parametrize('field', ['phi', 'sigma'])
- **test `test_agreement_known_answers`** [L270-280]: `def test_agreement_known_answers()`
- **function `centres`** [L283-284]: `def centres(bins=12)`
- **test `test_phase_bin_counts_known_answers`** [L287-295]: `def test_phase_bin_counts_known_answers()`
- **test `test_overall_resultant_known_answers`** [L298-302]: `def test_overall_resultant_known_answers()`
- **function `make_ext`** [L305-310]: `def make_ext(phase, supported=None)`
- **function `overall`** [L313-315]: `def overall(result)`
- **function `gates`** [L318-327]: `def gates(phase, direct=None, supported=None)`
- **test `test_chart_gates_all_pass_with_exactly_eight_per_bin`** [L333-340]: `def test_chart_gates_all_pass_with_exactly_eight_per_bin()`
- **test `test_chart_gates_seven_in_a_bin_is_inconclusive`** [L343-347]: `def test_chart_gates_seven_in_a_bin_is_inconclusive()`
- **test `test_chart_gates_fidelity_boundary`** [L350-361]: `def test_chart_gates_fidelity_boundary()`
- **test `test_chart_gates_resultant_boundary`** [L364-369]: `def test_chart_gates_resultant_boundary()`
- **test `test_chart_gates_support_and_overall_order`** [L372-382]: `def test_chart_gates_support_and_overall_order()`
- **test `test_chart_gates_defects_invalid`** [L385-391]: `def test_chart_gates_defects_invalid()`

