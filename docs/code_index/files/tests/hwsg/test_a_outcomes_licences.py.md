# `tests/hwsg/test_a_outcomes_licences.py`

- Source: [tests/hwsg/test_a_outcomes_licences.py](../../../../../tests/hwsg/test_a_outcomes_licences.py)
- Kind: python
- Lines: 138

## Module docstring

> Author A (job 0224): outcome precedence and licences (§7.2, §7.4, §7.5; API §12-§13).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 22, via sys.path edit)
- `import hwsg_cross` -> [tools/hwsg/hwsg_cross.py](../../tools/hwsg/hwsg_cross.py.md) (line 23, via sys.path edit)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](../../tools/hwsg/hwsg_records.py.md) (line 24, via sys.path edit)

### External (third-party)

- `pytest` (lines 14)

### Standard library

- `__future__` (lines 7)
- `json` (lines 9)
- `pathlib` (lines 12)
- `re` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`

## Imported by

- none

## Top-level constants

- `C`
- `EP_SUPPORT`
- `HI`
- `KEY_HI`
- `L1`
- `LIC`
- `REPO`
- `ROWS`
- `_ERR`

## Classes and functions

- **function `_imports`** [L34-36]: `def _imports()` decorators: @pytest.fixture(autouse=True)
- **function `_state`** [L39-43]: `def _state(**kw)`
- **test `test_precedence`** [L72-75]: `def test_precedence(state, expected)` decorators: @pytest.mark.parametrize('state,expected', ROWS)
- **test `test_not_learned_label_k_of_3`** [L78-80]: `def test_not_learned_label_k_of_3()`
- **test `test_endpoint_outcomes_pass_through`** [L83-86]: `def test_endpoint_outcomes_pass_through()`
- **test `test_world_support_and_exclusion_licence`** [L94-98]: `def test_world_support_and_exclusion_licence()`
- **test `test_not_general_carries_error_statement`** [L101-105]: `def test_not_general_carries_error_statement()`
- **test `test_capture_at_least_half_names_unavailable`** [L108-110]: `def test_capture_at_least_half_names_unavailable()`
- **test `test_general_unavailable_missing_key_na`** [L113-115]: `def test_general_unavailable_missing_key_na()`
- **test `test_similarity_sentence_words`** [L119-126]: `def test_similarity_sentence_words(word)` decorators: @pytest.mark.parametrize('word', ['compatible', 'not compatible'])
- **test `test_disclosure_and_does_not_establish`** [L129-138]: `def test_disclosure_and_does_not_establish()`

