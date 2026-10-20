# `tests/analysis/test_sigma_calibrator.py`

- Source: [tests/analysis/test_sigma_calibrator.py](../../../../../tests/analysis/test_sigma_calibrator.py)
- Kind: python
- Lines: 118

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import SigmaCalibrator, SigmaRow` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 5, via package root)

### External (third-party)

- `pytest` (lines 3)

### Standard library

- `math` (lines 1)

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

- `LOG2`
- `PW`
- `V`

## Classes and functions

- **function `rows_for`** [L14-22]: `def rows_for(sigma, cyl=None, sq=None)` - cyl/sq: dict overriding the passing defaults for that world.
- **function `select`** [L25-27]: `def select(*row_groups)`
- **test `test_first_candidate_passes`** [L30-33]: `def test_first_candidate_passes()`
- **test `test_first_fails_in_one_world_second_passes`** [L36-39]: `def test_first_fails_in_one_world_second_passes()`
- **test `test_each_criterion_in_each_world_can_fail`** [L46-49]: `def test_each_criterion_in_each_world_can_fail(world_kw, bad)` decorators: @pytest.mark.parametrize('world_kw', ['cyl', 'sq']) @pytest.mark.parametrize('bad', [{'mean_H_b1': LOG2 - 0.01}, {'G_C': 0.09}, {'min_p_w': PW * 0.9}])
- **test `test_candidate_order_is_first_appearance_not_value`** [L52-54]: `def test_candidate_order_is_first_appearance_not_value()`
- **test `test_boundaries_pass_exactly`** [L57-61]: `def test_boundaries_pass_exactly()`
- **test `test_second_candidate_chosen_even_if_third_better`** [L64-66]: `def test_second_candidate_chosen_even_if_third_better()`
- **test `test_fallback_weak_context_picks_argmax_min_G_C`** [L69-79]: `def test_fallback_weak_context_picks_argmax_min_G_C()`
- **test `test_fallback_uses_min_over_worlds_not_max_or_mean`** [L82-90]: `def test_fallback_uses_min_over_worlds_not_max_or_mean()`
- **test `test_fallback_threshold_exactly_003_accepted`** [L93-97]: `def test_fallback_threshold_exactly_003_accepted()`
- **test `test_stop_h3_when_fallback_below_003`** [L100-108]: `def test_stop_h3_when_fallback_below_003()`
- **test `test_decision_has_reasons_and_table`** [L111-118]: `def test_decision_has_reasons_and_table()`

