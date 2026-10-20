# `tests/c1prime/test_a_chart_exceptions.py`

- Source: [tests/c1prime/test_a_chart_exceptions.py](../../../../../tests/c1prime/test_a_chart_exceptions.py)
- Kind: python
- Lines: 237

## Module docstring

> Independent tests, author A (job 0026): the chart-specific exception mapping at the C1 gate
> boundary (TEST_PLAN A-2; protocol section 14 'Failure classification' and section 16
> conventions; API.md section 2 adapt_chart_exception / smoothing_diagnostics / run_c1_gate).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 29, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 30, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 31, via sys.path edit)
- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 32, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 33, via sys.path edit)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 11)
- `math` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)
- `traceback` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 27: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `BETA3`
- `PATH3`
- `REPO`

## Classes and functions

- **function `caught`** [L40-45]: `def caught(fn)`
- **function `full`** [L48-53]: `def full(status, reason)`
- **function `gate_outcome`** [L56-60]: `def gate_outcome(tmp_path, fn, chart_boundary=True)`
- **function `not_a_cocycle`** [L63-68]: `def not_a_cocycle()` - Triangle (0,1,2) with a = (1, 0, 0) on edges (01, 02, 12): D1 a = 1, not 0 mod 47.
- **function `fake_lsqr`** [L71-74]: `def fake_lsqr(values)`
- **function `smoothing`** [L77-80]: `def smoothing(monkeypatch, values, edges=PATH3, beta=BETA3)`
- **test `test_filtration_boundary_cocycle_error_is_chart_unavailable`** [L83-95]: `def test_filtration_boundary_cocycle_error_is_chart_unavailable(tmp_path)`
- **test `test_cocycle_error_outside_the_chart_boundary_stays_technical`** [L98-100]: `def test_cocycle_error_outside_the_chart_boundary_stays_technical(tmp_path)`
- **test `test_same_message_not_raised_by_integer_lift_is_technical`** [L103-109]: `def test_same_message_not_raised_by_integer_lift_is_technical(tmp_path)`
- **test `test_finite_smoothing_residual_above_tolerance_is_chart_unavailable`** [L112-125]: `def test_finite_smoothing_residual_above_tolerance_is_chart_unavailable(tmp_path, monkeypatch)`
- **test `test_non_finite_f_is_technical`** [L128-135]: `def test_non_finite_f_is_technical(tmp_path, monkeypatch)`
- **test `test_finite_f_with_infinite_residual_is_technical`** [L138-145]: `def test_finite_f_with_infinite_residual_is_technical(tmp_path, monkeypatch)`
- **test `test_finite_f_with_nan_residual_is_technical`** [L148-164]: `def test_finite_f_with_nan_residual_is_technical(tmp_path, monkeypatch)` - A NaN normaliser makes the residual NaN while f stays finite.
- **test `test_unavailable_smoothing_diagnostics_are_technical`** [L167-173]: `def test_unavailable_smoothing_diagnostics_are_technical(monkeypatch)`
- **test `test_smoothing_style_invalid_without_a_smooth_phase_frame_is_technical`** [L176-182]: `def test_smoothing_style_invalid_without_a_smooth_phase_frame_is_technical(tmp_path)`
- **test `test_integer_certificate_defect_is_technical`** [L185-197]: `def test_integer_certificate_defect_is_technical(tmp_path)`
- **test `test_conflicting_duplicate_landmarks_in_extension_are_technical`** [L200-213]: `def test_conflicting_duplicate_landmarks_in_extension_are_technical(tmp_path)`
- **test `test_lineage_join_error_is_technical`** [L216-222]: `def test_lineage_join_error_is_technical(tmp_path)`
- **test `test_unresolved_chart_kernel_is_chart_unavailable`** [L225-237]: `def test_unresolved_chart_kernel_is_chart_unavailable(tmp_path)` - Unresolved from a frozen chart kernel (protocol section 14: INCONCLUSIVE/

