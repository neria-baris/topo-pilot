# `tests/d2a/test_b_behaviour.py`

- Source: [tests/d2a/test_b_behaviour.py](../../../../../tests/d2a/test_b_behaviour.py)
- Kind: python
- Lines: 148

## Module docstring

> Independent tests (author B, job 0028): behavioural pair scores (``d2a_eval.pair_scores``) and
> the label-shuffle stream (``d2a_eval.shuffle_perm``).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `import d2a_eval` -> [tools/d2a/d2a_eval.py](../../tools/d2a/d2a_eval.py.md) (line 26, via sys.path edit)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 11)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / _sub)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `DATA`
- `E`
- `J_A`
- `J_B`
- `REPO`
- `SCOPE`

## Classes and functions

- **function `law`** [L32-37]: `def law(*head)` - A 25-entry two-step law whose first entries are ``head`` (the rest zero).
- **function `score`** [L44-45]: `def score(q_a, q_b, j_a=J_A, j_b=J_B)`
- **test `test_oracle_predictions_reproduce_and_resolve`** [L48-53]: `def test_oracle_predictions_reproduce_and_resolve()`
- **test `test_contrast_error_exactly_one_half_is_reproduced`** [L56-60]: `def test_contrast_error_exactly_one_half_is_reproduced()`
- **test `test_contrast_error_just_above_one_half_is_not_reproduced`** [L63-68]: `def test_contrast_error_just_above_one_half_is_not_reproduced()`
- **test `test_predicted_pair_tv_band_boundaries`** [L77-80]: `def test_predicted_pair_tv_band_boundaries(q_a, tv, ok)` decorators: @pytest.mark.parametrize('q_a, tv, ok', [(law(0.375, 0.375, 0.25), 0.125, True), (law(0.625, 0.125, 0.25), 0.375, True), (law(0.375 - E, 0.375 + E, 0.25), 0.125 - E, False), (law(0.625 + E, 0.125 - E, 0.25), 0.375 + E, False)])
- **test `test_zero_contrast_prediction_is_not_reproduced`** [L83-86]: `def test_zero_contrast_prediction_is_not_reproduced()`
- **test `test_reversed_contrast_is_not_reproduced`** [L89-92]: `def test_reversed_contrast_is_not_reproduced()`
- **test `test_absolute_resolution_is_separate_and_strict`** [L96-103]: `def test_absolute_resolution_is_separate_and_strict(shift, resolved)` decorators: @pytest.mark.parametrize('shift, resolved', [(0.0625, True), (0.125, False)])
- **test `test_absolute_resolution_needs_both_members`** [L107-112]: `def test_absolute_resolution_needs_both_members(off_a)` decorators: @pytest.mark.parametrize('off_a', [True, False])
- **test `test_template_scale_pair`** [L115-123]: `def test_template_scale_pair()`
- **test `test_shuffle_perm_is_the_registered_stream`** [L131-133]: `def test_shuffle_perm_is_the_registered_stream()`
- **test `test_shuffle_perm_is_deterministic_and_a_permutation`** [L136-141]: `def test_shuffle_perm_is_deterministic_and_a_permutation()`
- **test `test_shuffle_perm_depends_on_scope`** [L144-148]: `def test_shuffle_perm_depends_on_scope()`

