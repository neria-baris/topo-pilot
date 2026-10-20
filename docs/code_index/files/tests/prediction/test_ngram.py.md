# `tests/prediction/test_ngram.py`

- Source: [tests/prediction/test_ngram.py](../../../../../tests/prediction/test_ngram.py)
- Kind: python
- Lines: 87

## Module docstring

> R03, R04, R05 (unit part): n-gram baselines.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 6, via package root)
- `from topo_pilot.prediction import NGramBaseline` -> [src/topo_pilot/prediction/__init__.py](../../src/topo_pilot/prediction/__init__.py.md) (line 7, via package root)

### External (third-party)

- `numpy` (lines 3)
- `pytest` (lines 4)

### Standard library

- none

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

- none

## Classes and functions

- **function `make_obs`** [L12-15]: `def make_obs(tokens, split='train', V=3)`
- **test `test_R03_unigram_exact_frequencies`** [L18-23]: `def test_R03_unigram_exact_frequencies()`
- **test `test_R03_additive_smoothing_hand_value`** [L26-29]: `def test_R03_additive_smoothing_hand_value()`
- **test `test_R03_kneser_ney_order1_equals_mle`** [L32-36]: `def test_R03_kneser_ney_order1_equals_mle()`
- **test `test_R04_bigram_on_cycle_predicts_successor`** [L39-44]: `def test_R04_bigram_on_cycle_predicts_successor()`
- **test `test_bigram_contexts_do_not_cross_sequences`** [L47-50]: `def test_bigram_contexts_do_not_cross_sequences()`
- **test `test_bigram_unseen_context_alpha_zero_backs_off_to_unigram`** [L53-56]: `def test_bigram_unseen_context_alpha_zero_backs_off_to_unigram()`
- **test `test_kneser_ney_hand_value_and_rows_normalised`** [L59-66]: `def test_kneser_ney_hand_value_and_rows_normalised()`
- **test `test_R05_select_smoothing_uses_dev_and_picks_argmin`** [L69-76]: `def test_R05_select_smoothing_uses_dev_and_picks_argmin()`
- **test `test_error_paths`** [L79-87]: `def test_error_paths()`

