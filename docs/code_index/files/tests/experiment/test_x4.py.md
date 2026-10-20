# `tests/experiment/test_x4.py`

- Source: [tests/experiment/test_x4.py](../../../../../tests/experiment/test_x4.py)
- Kind: python
- Lines: 399

## Module docstring

> Stage X4 (TEST_PLAN X08-X12), from SPEC.md "Stage X4" only; tiny runs, fake resolver.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 8, via package root)
- `from topo_pilot.experiment import STAGE_REGISTRY, load_config` -> [src/topo_pilot/experiment/__init__.py](../../src/topo_pilot/experiment/__init__.py.md) (line 9, via package root)
- `from topo_pilot.experiment.x4 import X4Job, X4Panel, X4Run, run_rule_verdict, x4c_category` -> [src/topo_pilot/experiment/x4.py](../../src/topo_pilot/experiment/x4.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 5)
- `pytest` (lines 6)

### Standard library

- `collections` (lines 2)
- `pathlib` (lines 3)

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

- `CATEGORIES`
- `FINAL`
- `N_PANELS`
- `REPO`
- `SEEDS`
- `STATUSES`
- `VIEWS`

## Classes and functions

- **function `store`** [L26-27]: `def store(tmp_path)` decorators: @pytest.fixture
- **function `cfg`** [L31-32]: `def cfg()` decorators: @pytest.fixture
- **function `_softmax_rows`** [L38-40]: `def _softmax_rows(rng, n_rows, n_cols)`
- **function `_weights`** [L43-47]: `def _weights(rng)`
- **function `_panel`** [L50-57]: `def _panel(rng, tag, gamma, beta, W_U)`
- **function `_oracle`** [L60-71]: `def _oracle(rng)`
- **function `make_run`** [L74-87]: `def make_run(world, condition, seed, parents, with_oracle=True)`
- **function `save_parents`** [L90-95]: `def save_parents(store, n=5)`
- **function `make_runs`** [L98-109]: `def make_runs(parents, skip=())` - 3 replicates x 2 worlds (condition O) + one N run. ``parents`` has >= 5 ids.
- **function `fake_resolver`** [L112-120]: `def fake_resolver(runs, missing)` - Source-aware like StoreResolver: S4 holds the O and N runs, S5 the P runs.
- **function `all_files`** [L123-124]: `def all_files(store)`
- **function `load_rows`** [L127-128]: `def load_rows(store, aid)`
- **function `verdicts`** [L131-134]: `def verdicts(rows, space, prefix, condition='O')` - Suffixes (statuses) of the verdict rows `prefix + <STATUS>` of one space and condition.
- **test `test_X08_x4c_category`** [L149-150]: `def test_X08_x4c_category(v3, v4, expected)` decorators: @pytest.mark.parametrize('v3, v4, expected', [('SUPPORTED', 'SUPPORTED', 'both'), ('SUPPORTED', 'REJECTED', 'V3_only'), ('REJECTED', 'SUPPORTED', 'V4_only'), ('REJECTED', 'REJECTED', 'neither'), ('INCONCLUSIVE', 'SUPPORTED', 'V4_only'), ('SUPPORTED', 'INCONCLUSIVE', 'V3_only'), ('INCONCLUSIVE', 'INCONCLUSIVE', 'neither')])
- **function `_keys`** [L153-154]: `def _keys(seeds=SEEDS, worlds=('cylinder', 'square'))`
- **function `_args`** [L157-159]: `def _args(n_pass_value=8, seeds=SEEDS, gate=True)`
- **test `test_X08_run_rule_all_runs_pass_is_supported`** [L162-166]: `def test_X08_run_rule_all_runs_pass_is_supported()`
- **test `test_X08_run_rule_exactly_min_passes_is_supported`** [L169-171]: `def test_X08_run_rule_exactly_min_passes_is_supported()`
- **test `test_X08_run_rule_one_run_below_min_is_rejected`** [L174-177]: `def test_X08_run_rule_one_run_below_min_is_rejected()`
- **test `test_X08_run_rule_failed_gate_is_inconclusive_with_reason`** [L181-186]: `def test_X08_run_rule_failed_gate_is_inconclusive_with_reason(bad)` decorators: @pytest.mark.parametrize('bad', [False, None])
- **test `test_X08_run_rule_failed_gate_beats_failed_count`** [L189-193]: `def test_X08_run_rule_failed_gate_beats_failed_count()`
- **test `test_X08_run_rule_two_of_three_replicates_is_inconclusive`** [L196-200]: `def test_X08_run_rule_two_of_three_replicates_is_inconclusive()`
- **test `test_X08_run_rule_replicate_with_one_world_is_inconclusive`** [L203-207]: `def test_X08_run_rule_replicate_with_one_world_is_inconclusive()`
- **test `test_X09_x4job_writes_expected_rows`** [L213-276]: `def test_X09_x4job_writes_expected_rows(store, cfg)`
- **test `test_X09_grains_of_the_rows`** [L279-330]: `def test_X09_grains_of_the_rows(store, cfg)`
- **test `test_X09_n_run_only_contributes_sh1_and_check`** [L333-344]: `def test_X09_n_run_only_contributes_sh1_and_check(store, cfg)`
- **test `test_X10_rerun_returns_same_id`** [L350-359]: `def test_X10_rerun_returns_same_id(store, cfg)`
- **test `test_X11_missing_run_is_not_run_and_verdicts_inconclusive`** [L365-388]: `def test_X11_missing_run_is_not_run_and_verdicts_inconclusive(store, cfg)`
- **test `test_X12_x4_registered_with_requires_s4_and_no_gates`** [L394-399]: `def test_X12_x4_registered_with_requires_s4_and_no_gates()`

