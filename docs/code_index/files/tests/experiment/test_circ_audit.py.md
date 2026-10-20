# `tests/experiment/test_circ_audit.py`

- Source: [tests/experiment/test_circ_audit.py](../../../../../tests/experiment/test_circ_audit.py)
- Kind: python
- Lines: 58

## Module docstring

> circ-audit-v1: frozen per-panel comparison (C1, C2) and the three-run reading.

## Imports

### Internal (repo files)

- `from topo_pilot.experiment.circ_audit import BASELINES, compare_panel, summarize` -> [src/topo_pilot/experiment/circ_audit.py](../../src/topo_pilot/experiment/circ_audit.py.md) (line 4, via package root)

### External (third-party)

- `pytest` (lines 2)

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

- **function `_reps`** [L9-16]: `def _reps(model, r1='no_h1_class', r2=0.5, r3=0.4)`
- **function `_panel`** [L19-20]: `def _panel(bound=0.8, b1=0.7)`
- **test `test_compare_panel_excludes_failed_baselines_and_counts_them`** [L23-27]: `def test_compare_panel_excludes_failed_baselines_and_counts_them()`
- **test `test_compare_panel_fails_below_bound_or_baseline`** [L30-35]: `def test_compare_panel_fails_below_bound_or_baseline()`
- **function `_rows`** [L38-45]: `def _rows(seed, n_pass)`
- **test `test_summarize_three_run_reading`** [L53-58]: `def test_summarize_three_run_reading(passes, reading)` decorators: @pytest.mark.parametrize('passes,reading', [((8, 7, 8), 'BEYOND_SYMBOL_AND_MIXING'), ((6, 0, 2), 'SYMBOL_MIXING_SUFFICES_FOR_NOW'), ((8, 6, 8), 'NOT_ESTABLISHED_MIXED')])

