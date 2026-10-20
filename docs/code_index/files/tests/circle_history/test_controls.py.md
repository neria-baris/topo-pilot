# `tests/circle_history/test_controls.py`

- Source: [tests/circle_history/test_controls.py](../../../../../tests/circle_history/test_controls.py)
- Kind: python
- Lines: 164

## Module docstring

> Independent tests (author B) for the validation controls and the error taxonomy: TEST_PLAN
> items B15 and B16 (spec v2.4).

## Imports

### Internal (repo files)

- `import adapter` -> [tools/x4_circle_history/adapter.py](../../tools/x4_circle_history/adapter.py.md) (line 28, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 29, via sys.path edit)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 30, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 20)
- `pytest` (lines 21)

### Standard library

- `__future__` (lines 13)
- `hashlib` (lines 15)
- `math` (lines 16)
- `pathlib` (lines 18)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO_ROOT / _sub)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `BASE`
- `MODELS`
- `NAMES`
- `REPO_ROOT`

## Classes and functions

- **function `_hand_phase`** [L40-42]: `def _hand_phase(last4) -> float`
- **test `test_control_scores_equal_unit_dot_residual`** [L45-65]: `def test_control_scores_equal_unit_dot_residual() -> None`
- **function `_controls`** [L73-77]: `def _controls() -> dict`
- **function `_manual_draws`** [L80-88]: `def _manual_draws(C: dict) -> dict`
- **test `test_control_summary_reproduces_shared_index_stream`** [L91-121]: `def test_control_summary_reproduces_shared_index_stream() -> None`
- **function `_bad_summaries`** [L124-136]: `def _bad_summaries() -> dict`
- **test `test_control_summary_fail_closed`** [L140-143]: `def test_control_summary_fail_closed(case: str) -> None` decorators: @pytest.mark.parametrize('case', sorted(_bad_summaries()))
- **test `test_error_classes_unchanged`** [L147-152]: `def test_error_classes_unchanged() -> None`
- **test `test_join_failure_is_join_error_never_unresolved`** [L155-164]: `def test_join_failure_is_join_error_never_unresolved() -> None`

