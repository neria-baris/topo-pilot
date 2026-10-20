# `tests/chart_diag/test_chart_diag.py`

- Source: [tests/chart_diag/test_chart_diag.py](../../../../../tests/chart_diag/test_chart_diag.py)
- Kind: python
- Lines: 85

## Module docstring

> Builder tests of tools/chart_diag (job 0023): synthetic geometry only, no E4 artifact access.

## Imports

### Internal (repo files)

- `import chart_diag` -> [tools/chart_diag/chart_diag.py](../../tools/chart_diag/chart_diag.py.md) (line 15, via sys.path edit)

### External (third-party)

- `numpy` (lines 8)
- `pytest` (lines 9)

### Standard library

- `__future__` (lines 3)
- `pathlib` (lines 6)
- `sys` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `str(REPO_ROOT / 'tools' / 'chart_diag')` -> `tools/chart_diag`

## Imported by

- none

## Top-level constants

- `REPO_ROOT`

## Classes and functions

- **function `_ids`** [L18-19]: `def _ids(n)`
- **function `_circle`** [L22-26]: `def _circle(n, rng, radius=1.0, noise=0.01, dim=4)`
- **test `test_components_follow_edge_list_rule`** [L29-35]: `def test_components_follow_edge_list_rule()`
- **test `test_x_interval_and_verdict_rule`** [L38-43]: `def test_x_interval_and_verdict_rule()`
- **test `test_connected_circle_has_full_giant`** [L46-53]: `def test_connected_circle_has_full_giant()`
- **test `test_far_outlier_is_reported_outside_giant`** [L56-69]: `def test_far_outlier_is_reported_outside_giant()`
- **test `test_k4_landmark_checks_are_applied`** [L72-78]: `def test_k4_landmark_checks_are_applied()`
- **test `test_reused_k4_files_match_freeze`** [L81-85]: `def test_reused_k4_files_match_freeze()`

