# `tests/experiment/test_report_e3.py`

- Source: [tests/experiment/test_report_e3.py](../../../../../tests/experiment/test_report_e3.py)
- Kind: python
- Lines: 115

## Module docstring

> E3 report (X14–X16): records only, fixed status readings, P wording, S6 plan.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.experiment.report_e3 import H3_READING, build_e3, h4_table` -> [src/topo_pilot/experiment/report_e3.py](../../src/topo_pilot/experiment/report_e3.py.md) (line 5, via package root)
- `from topo_pilot.experiment.report_x4 import P_X4B_NOTE, x4_section` -> [src/topo_pilot/experiment/report_x4.py](../../src/topo_pilot/experiment/report_x4.py.md) (line 6, via package root)
- `from topo_pilot.experiment.s6 import S6Stage` -> [src/topo_pilot/experiment/s6.py](../../src/topo_pilot/experiment/s6.py.md) (line 7, via package root)

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

- `DECISIONS`
- `PREREG`

## Classes and functions

- **function `repo`** [L21-26]: `def repo(tmp_path)` decorators: @pytest.fixture
- **function `store`** [L30-31]: `def store(tmp_path)` decorators: @pytest.fixture
- **function `_r`** [L34-35]: `def _r(space, metric, value, **kw)`
- **function `_save`** [L38-40]: `def _save(store, rows, **config)`
- **function `_dyn_rows`** [L43-57]: `def _dyn_rows(cond='O', seed=1729)`
- **test `test_X14_empty_store_says_not_run`** [L60-68]: `def test_X14_empty_store_says_not_run(store, repo, tmp_path)`
- **test `test_X14_rejected_h3_is_read_one_sided`** [L71-76]: `def test_X14_rejected_h3_is_read_one_sided(store, repo, tmp_path)`
- **test `test_X15_dynamics_table_and_figures`** [L79-87]: `def test_X15_dynamics_table_and_figures(store, repo, tmp_path)`
- **test `test_X16_x4_section_p_wording`** [L90-97]: `def test_X16_x4_section_p_wording(store, tmp_path)`
- **class `_Cfg`** [L100-105]
- **method `_Cfg.__init__`** [L101-102]: `def __init__(self, s6)`
- **method `_Cfg.stage`** [L104-105]: `def stage(self, stage_id)`
- **test `test_X16_s6_plan_includes_x4curves_and_p_after_s5`** [L108-115]: `def test_X16_s6_plan_includes_x4curves_and_p_after_s5(store)`

