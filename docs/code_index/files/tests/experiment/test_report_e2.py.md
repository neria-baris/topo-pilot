# `tests/experiment/test_report_e2.py`

- Source: [tests/experiment/test_report_e2.py](../../../../../tests/experiment/test_report_e2.py)
- Kind: python
- Lines: 82

## Module docstring

> E2 report: built from MetricRecords/GateReport only; missing data prints "not run".

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, GateCheck, GateReport, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.experiment.report_e2 import build_e2, f1_table, prediction_table, verdict` -> [src/topo_pilot/experiment/report_e2.py](../../src/topo_pilot/experiment/report_e2.py.md) (line 12, via package root)

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

- **function `store`** [L18-19]: `def store(tmp_path)` decorators: @pytest.fixture
- **function `_r`** [L22-23]: `def _r(space, metric, value, **kw)`
- **function `_analysis_rows`** [L26-42]: `def _analysis_rows(seed=1729)`
- **test `test_f1_table_reports_four_medians_and_positive_count`** [L45-48]: `def test_f1_table_reports_four_medians_and_positive_count()`
- **test `test_verdict_reads_status_and_reasons`** [L51-53]: `def test_verdict_reads_status_and_reasons()`
- **test `test_build_e2_from_records_only`** [L56-69]: `def test_build_e2_from_records_only(store, tmp_path)`
- **test `test_build_e2_without_analysis_says_not_run`** [L72-74]: `def test_build_e2_without_analysis_says_not_run(store, tmp_path)`
- **test `test_n_run_learning_gate_is_not_applicable`** [L77-82]: `def test_n_run_learning_gate_is_not_applicable()`

