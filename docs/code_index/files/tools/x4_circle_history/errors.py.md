# `tools/x4_circle_history/errors.py`

- Source: [tools/x4_circle_history/errors.py](../../../../../tools/x4_circle_history/errors.py)
- Kind: python
- Lines: 52

## Module docstring

> Error classes for x4_circle_history (API.md, errors.py).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 37, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 33, import)
- [tests/c1prime/test_a_chart_lcc512.py](../../tests/c1prime/test_a_chart_lcc512.py.md) (line 35, import)
- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 33, import)
- [tests/circle_history/test_adapter.py](../../tests/circle_history/test_adapter.py.md) (line 34, import)
- [tests/circle_history/test_builder_guards.py](../../tests/circle_history/test_builder_guards.py.md) (line 22, import)
- [tests/circle_history/test_builder_v24_runtime.py](../../tests/circle_history/test_builder_v24_runtime.py.md) (line 26, import)
- [tests/circle_history/test_builder_v24_stages.py](../../tests/circle_history/test_builder_v24_stages.py.md) (line 21, import)
- [tests/circle_history/test_chart.py](../../tests/circle_history/test_chart.py.md) (line 27, import)
- [tests/circle_history/test_chart_extension.py](../../tests/circle_history/test_chart_extension.py.md) (line 27, import)
- [tests/circle_history/test_cochain.py](../../tests/circle_history/test_cochain.py.md) (line 25, import)
- [tests/circle_history/test_cochain_chart_v24.py](../../tests/circle_history/test_cochain_chart_v24.py.md) (line 33, import)
- [tests/circle_history/test_cochain_lift.py](../../tests/circle_history/test_cochain_lift.py.md) (line 36, import)
- [tests/circle_history/test_controls.py](../../tests/circle_history/test_controls.py.md) (line 29, import)
- [tests/circle_history/test_error_bound.py](../../tests/circle_history/test_error_bound.py.md) (line 27, import)
- [tests/circle_history/test_process_law.py](../../tests/circle_history/test_process_law.py.md) (line 30, import)
- [tests/circle_history/test_reference_binding.py](../../tests/circle_history/test_reference_binding.py.md) (line 32, import)
- [tests/circle_history/test_reference_cache.py](../../tests/circle_history/test_reference_cache.py.md) (line 30, import)
- [tests/circle_history/test_scores_precision.py](../../tests/circle_history/test_scores_precision.py.md) (line 26, import)
- [tests/circle_history/test_scores_precision_gates.py](../../tests/circle_history/test_scores_precision_gates.py.md) (line 29, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 24, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 23, import)
- [tools/x4_circle_history/adapter.py](adapter.py.md) (line 14, import)
- [tools/x4_circle_history/chart.py](chart.py.md) (line 18, import)
- [tools/x4_circle_history/cochain.py](cochain.py.md) (line 22, import)
- [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 24, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 69, import)
- [tools/x4_circle_history/op_guard.py](op_guard.py.md) (line 17, import)
- [tools/x4_circle_history/precision.py](precision.py.md) (line 9, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 19, import)
- [tools/x4_circle_history/process_law.py](process_law.py.md) (line 23, import)
- [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 17, import)
- [tools/x4_circle_history/release.py](release.py.md) (line 28, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 30, import)
- [tools/x4_circle_history/scores.py](scores.py.md) (line 17, import)
- [tools/x4_circle_history/stage_records.py](stage_records.py.md) (line 18, import)

## Top-level constants

- none

## Classes and functions

- **class `Invalid(RuntimeError)`** [L8-9] - Numerical, integrity or implementation defect: the runner reports FAIL_TECHNICAL.
- **class `CacheMiss(Invalid)`** [L12-13] - cache_only reference lookup missed (spec v2.4): raised, never folded into a status.
- **class `Unresolved(RuntimeError)`** [L16-17] - Valid criterion not met, unsupported, or exhausted: the runner reports INCONCLUSIVE.
- **class `AccessDenied(RuntimeError)`** [L20-21] - Access to a scored panel or scored row attempted without a scoring release.
- **class `JoinError(RuntimeError)`** [L24-25] - Mismatch in cross-model pairing or artifact lineage: stop for review.
- **class `ScoringAuthority`** [L29-40] decorators: @dataclass(frozen=True) - Positively verified owner scoring release (issued only by release.scoring_authority).
- **function `require_scoring`** [L43-52]: `def require_scoring(authority) -> None` - AccessDenied unless ``authority`` is a ScoringAuthority whose scope includes scoring.

