# `tests/hws/test_a_budget.py`

- Source: [tests/hws/test_a_budget.py](../../../../../tests/hws/test_a_budget.py)
- Kind: python
- Lines: 113

## Module docstring

> Author A (job 0119): frozen CPU rates, stage forecasts and the two 3x pause triggers.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 18, via sys.path edit)
- `import hws_select` -> [tools/hws/hws_select.py](../../tools/hws/hws_select.py.md) (line 19, via sys.path edit)

### External (third-party)

- `pytest` (lines 11)

### Standard library

- `fractions` (lines 8)
- `pathlib` (lines 9)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `HWS_DIR` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `CELLS`
- `F`
- `HWS_DIR`
- `P`
- `REPO`
- `S`
- `SCREEN`

## Classes and functions

- **function `_s1_max`** [L28-29]: `def _s1_max()`
- **function `_x1_max`** [L32-34]: `def _x1_max()`
- **test `test_screening_rates`** [L38-40]: `def test_screening_rates(stage)` decorators: @pytest.mark.parametrize('stage', ['S1', 'X1', 'S2'])
- **test `test_s3_rates_and_s0_refused`** [L43-49]: `def test_s3_rates_and_s0_refused()`
- **test `test_fixed_forecasts`** [L52-54]: `def test_fixed_forecasts()`
- **test `test_maximal_s1_and_x1_forecasts`** [L57-62]: `def test_maximal_s1_and_x1_forecasts()`
- **test `test_s2_and_s3_forecasts_are_sums_over_the_actual_worklist`** [L65-75]: `def test_s2_and_s3_forecasts_are_sums_over_the_actual_worklist()`
- **test `test_pause_check_strict_triggers`** [L78-86]: `def test_pause_check_strict_triggers()`
- **function `_cumulative_table`** [L89-96]: `def _cumulative_table()`
- **test `test_cumulative_thresholds_of_the_protocol_table`** [L99-105]: `def test_cumulative_thresholds_of_the_protocol_table()`
- **test `test_per_stage_thresholds_of_the_protocol_table`** [L108-113]: `def test_per_stage_thresholds_of_the_protocol_table()`

