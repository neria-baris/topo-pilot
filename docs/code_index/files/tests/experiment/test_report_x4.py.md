# `tests/experiment/test_report_x4.py`

- Source: [tests/experiment/test_report_x4.py](../../../../../tests/experiment/test_report_x4.py)
- Kind: python
- Lines: 48

## Module docstring

> X4 report section (TEST_PLAN X13): verbatim prereg lines, "not run" when missing.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.experiment.report_x4 import x4_section` -> [src/topo_pilot/experiment/report_x4.py](../../src/topo_pilot/experiment/report_x4.py.md) (line 5, via package root)

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

- `PREREG`

## Classes and functions

- **function `store`** [L23-24]: `def store(tmp_path)` decorators: @pytest.fixture
- **function `_save`** [L27-29]: `def _save(store, rows)`
- **test `test_X13_missing_record_says_not_run`** [L32-36]: `def test_X13_missing_record_says_not_run(store, tmp_path)`
- **test `test_X13_quotes_prereg_interpretation_and_addendum`** [L41-48]: `def test_X13_quotes_prereg_interpretation_and_addendum(store, tmp_path, cat, expected)` decorators: @pytest.mark.parametrize('cat, expected', [('V4_only', 'V4 supported, V3 not → null sentence;'), ('neither', 'both / neither → reported as such.')])

