# `tests/experiment/test_s7.py`

- Source: [tests/experiment/test_s7.py](../../../../../tests/experiment/test_s7.py)
- Kind: python
- Lines: 272

## Module docstring

> Stage S7 (TEST_PLAN X17-X21), from SPEC.md "Stage S7" only; stub stores, no training.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ActivationSet, ErrorCode, GateReport, MetricRecords, MetricRow, ObservationSet, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 7, via package root)
- `from topo_pilot.contracts.testing import memory_store, tiny_observations` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 16, via package root)
- `from topo_pilot.experiment import STAGE_REGISTRY, load_config, s7_probes` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md), [src/topo_pilot/experiment/s7_probes.py](../../src/topo_pilot/experiment/s7_probes.py.md) (line 17, via package root)
- `from topo_pilot.experiment.s3 import on_test_split` -> [src/topo_pilot/experiment/s3.py](../../src/topo_pilot/experiment/s3.py.md) (line 18, via package root)
- `from topo_pilot.experiment.s7 import S7Runs, gate_gg` -> [src/topo_pilot/experiment/s7.py](../../src/topo_pilot/experiment/s7.py.md) (line 19, via package root)
- `from topo_pilot.experiment.s7_circular import CircularJob` -> [src/topo_pilot/experiment/s7_circular.py](../../src/topo_pilot/experiment/s7_circular.py.md) (line 20, via package root)
- `from topo_pilot.experiment.s7_dev import ProbeData` -> [src/topo_pilot/experiment/s7_dev.py](../../src/topo_pilot/experiment/s7_dev.py.md) (line 21, via package root)
- `from topo_pilot.experiment.s7_probes import ProbesJob` -> [src/topo_pilot/experiment/s7_probes.py](../../src/topo_pilot/experiment/s7_probes.py.md) (line 22, via package root)

### External (third-party)

- `numpy` (lines 4)
- `pytest` (lines 5)

### Standard library

- `pathlib` (lines 2)

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

- `CONS`
- `JOBS`
- `REPO`

## Classes and functions

- **function `cfg`** [L32-33]: `def cfg()` decorators: @pytest.fixture(scope='module')
- **function `_save_rec`** [L36-38]: `def _save_rec(store, config, rows=())`
- **function `_runs`** [L41-42]: `def _runs(cfg)`
- **function `_run_key`** [L45-46]: `def _run_key(r)`
- **function `_fill_store`** [L49-59]: `def _fill_store(cfg, store, skip_run=None, failed_run=None, jobs=JOBS)`
- **test `test_X17_registry_requires_and_gates`** [L63-66]: `def test_X17_registry_requires_and_gates()`
- **test `test_X17_plan_missing_s6_raises_missing_parent`** [L69-78]: `def test_X17_plan_missing_s6_raises_missing_parent(cfg)`
- **test `test_X17_plan_order_with_s6_records`** [L81-90]: `def test_X17_plan_order_with_s6_records(cfg)`
- **test `test_X18_gate_gg_passes_when_all_documented`** [L94-104]: `def test_X18_gate_gg_passes_when_all_documented(cfg)`
- **test `test_X18_gate_gg_fails_for_undocumented_run`** [L107-113]: `def test_X18_gate_gg_fails_for_undocumented_run(cfg)`
- **test `test_X18_gate_gg_failed_run_record_counts_as_documented`** [L116-120]: `def test_X18_gate_gg_failed_run_record_counts_as_documented(cfg)`
- **test `test_X18_gate_gg_fails_for_missing_job_record`** [L123-128]: `def test_X18_gate_gg_fails_for_missing_job_record(cfg)`
- **test `test_X19_failed_run_is_recorded_not_raised`** [L132-152]: `def test_X19_failed_run_is_recorded_not_raised(cfg, monkeypatch)`
- **test `test_X19_non_stagefailure_exception_uses_type_name`** [L155-164]: `def test_X19_non_stagefailure_exception_uses_type_name(cfg, monkeypatch)`
- **function `_row`** [L168-171]: `def _row(metric, value, panel, **kw)`
- **test `test_X20_circular_summary_known_answer`** [L174-189]: `def test_X20_circular_summary_known_answer()`
- **function `_planted`** [L192-199]: `def _planted(rng, W, noise, n_per=16, d=6)`
- **function `_job`** [L202-207]: `def _job()`
- **test `test_X20_probe_recovers_planted_map_and_lambda_uses_val_rows_only`** [L210-238]: `def test_X20_probe_recovers_planted_map_and_lambda_uses_val_rows_only(monkeypatch)`
- **test `test_X20_probe_shuffled_labels_give_low_r2`** [L241-248]: `def test_X20_probe_shuffled_labels_give_low_r2()`
- **function `_obs`** [L252-256]: `def _obs(store, split, seed)`
- **function `_acts`** [L259-264]: `def _acts(store, obs_id)`
- **test `test_X21_on_test_split_distinguishes_dev_and_test`** [L267-272]: `def test_X21_on_test_split_distinguishes_dev_and_test()`

