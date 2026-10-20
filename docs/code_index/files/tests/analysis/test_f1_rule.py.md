# `tests/analysis/test_f1_rule.py`

- Source: [tests/analysis/test_f1_rule.py](../../../../../tests/analysis/test_f1_rule.py)
- Kind: python
- Lines: 153

## Module docstring

> Independent tests N01-N06 for the F1 decision rule (RESEARCH_SUMMARY 7.4).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import F1Decision` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 4)
- `pytest` (lines 5)

### Standard library

- `itertools` (lines 2)

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

- `GOOD`

## Classes and functions

- **function `make_table`** [L13-21]: `def make_table(cf, ci, sf, si, panels=None)`
- **test `test_contrasts_known_answer`** [L25-31]: `def test_contrasts_known_answer()`
- **test `test_contrasts_ordered_by_sorted_panel_ids`** [L34-38]: `def test_contrasts_ordered_by_sorted_panel_ids()`
- **test `test_contrasts_missing_key_is_invalid_config`** [L41-46]: `def test_contrasts_missing_key_is_invalid_config()`
- **test `test_noise_envelope_known_answer`** [L50-55]: `def test_noise_envelope_known_answer()`
- **test `test_noise_envelope_matches_bruteforce_and_picks_max_cell`** [L58-65]: `def test_noise_envelope_matches_bruteforce_and_picks_max_cell()`
- **function `rep`** [L69-70]: `def rep(D, u=0.1)`
- **function `reasons_text`** [L76-77]: `def reasons_text(v)`
- **test `test_verdict_supported`** [L81-83]: `def test_verdict_supported()`
- **test `test_verdict_rejected_when_six_of_eight_positive`** [L87-90]: `def test_verdict_rejected_when_six_of_eight_positive()`
- **test `test_verdict_rejected_when_median_below_envelope`** [L93-95]: `def test_verdict_rejected_when_median_below_envelope()`
- **test `test_verdict_inconclusive_on_learning_gate`** [L99-102]: `def test_verdict_inconclusive_on_learning_gate()`
- **test `test_learning_gate_failure_beats_a_rejecting_replicate`** [L105-107]: `def test_learning_gate_failure_beats_a_rejecting_replicate()`
- **test `test_verdict_inconclusive_on_input_status`** [L110-113]: `def test_verdict_inconclusive_on_input_status()`
- **test `test_verdict_all_ok_statuses_do_not_block`** [L116-118]: `def test_verdict_all_ok_statuses_do_not_block()`
- **test `test_verdict_inconclusive_with_fewer_than_three_replicates`** [L121-124]: `def test_verdict_inconclusive_with_fewer_than_three_replicates()`
- **test `test_learning_gate_reason_present_even_with_few_replicates`** [L127-130]: `def test_learning_gate_reason_present_even_with_few_replicates()`
- **test `test_exactly_seven_of_eight_positive_passes`** [L134-136]: `def test_exactly_seven_of_eight_positive_passes()`
- **test `test_zero_contrast_is_not_positive`** [L139-141]: `def test_zero_contrast_is_not_positive()`
- **test `test_median_equal_to_envelope_fails_strictly`** [L144-146]: `def test_median_equal_to_envelope_fails_strictly()`
- **test `test_one_failing_replicate_among_three_is_enough_to_reject`** [L149-153]: `def test_one_failing_replicate_among_three_is_enough_to_reject()`

