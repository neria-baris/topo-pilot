# `tests/hwsb/test_b_meter_law.py`

- Source: [tests/hwsb/test_b_meter_law.py](../../../../../tests/hwsb/test_b_meter_law.py)
- Kind: python
- Lines: 352

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_meter_law.py`: the meter binding and placement
> (section 6.4 rule 1, RC-5, DRB13b) and the INDEPENDENT test of the B8a enclosure (OPEN-3, DRB12):
> exact rational exp bounds written here contain every exact w* emission entry inside the returned
> enclosure; `law_bound` on w*, w(3/2) and w0; process_law state restored. tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 22, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 23, via sys.path edit)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../../tools/hwsb/hwsb_law.py.md) (line 24, via sys.path edit)
- `import hwsb_meter_bind` -> [tools/hwsb/hwsb_meter_bind.py](../../tools/hwsb/hwsb_meter_bind.py.md) (line 25, via sys.path edit)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 26, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 27, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 28, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../../tools/x4_circle_history/op_guard.py.md) (line 29, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 30, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 31, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 32, via package root)
- `from topo_pilot.process.emission import EmissionConfig` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 6)
- `decimal` (lines 11)
- `fractions` (lines 12)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 13)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `from errors import Invalid` (line 349): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `PROJECT`
- `REPO`
- `SCRATCH`
- `STATES`

## Classes and functions

- **function `code_of`** [L41-45]: `def code_of(fn)`
- **function `preserved`** [L50-66]: `def preserved(monkeypatch)` decorators: @pytest.fixture
- **test `test_bind_sets_memory_cap_temp_root_and_meter_paths`** [L69-83]: `def test_bind_sets_memory_cap_temp_root_and_meter_paths(tmp_path, preserved)`
- **test `test_bind_defaults_temp_root_to_out`** [L86-89]: `def test_bind_defaults_temp_root_to_out(tmp_path, preserved)`
- **test `test_effective_settings`** [L92-98]: `def test_effective_settings(tmp_path, preserved)`
- **test `test_rewrite_argv_appends_inf_caps`** [L101-103]: `def test_rewrite_argv_appends_inf_caps()`
- **test `test_job_paths_test_and_store_kinds`** [L106-115]: `def test_job_paths_test_and_store_kinds()`
- **test `test_placement_ok_for_test_paths_and_planted_inside_root`** [L118-131]: `def test_placement_ok_for_test_paths_and_planted_inside_root()`
- **test `test_this_suites_tmp_path_is_outside_the_project_root`** [L134-135]: `def test_this_suites_tmp_path_is_outside_the_project_root(tmp_path)`
- **function `argv`** [L138-140]: `def argv(*extra, kind='test')`
- **function `paths`** [L144-149]: `def paths(tmp_path, preserved)` decorators: @pytest.fixture
- **test `test_main_binds_and_hands_over_to_the_meter`** [L152-170]: `def test_main_binds_and_hands_over_to_the_meter(paths, preserved)`
- **test `test_main_refuses_foreign_run_lock_and_missing_arguments`** [L173-184]: `def test_main_refuses_foreign_run_lock_and_missing_arguments(paths, preserved)`
- **function `exp_neg_bounds`** [L188-196]: `def exp_neg_bounds(t)` - Rational lo <= exp(-t) <= hi, t >= 0 rational: Taylor sums of exp(t) with a geometric tail.
- **function `reference_entries`** [L199-215]: `def reference_entries(states, sigma)` - {(s, j): (lo, hi)} rational bounds on the exact softmax entry exp(q_j)/sum_k exp(q_k).
- **function `contained`** [L221-228]: `def contained(enclosure, ref)`
- **test `test_reference_code_agrees_with_the_old_enclosure_at_5_4`** [L231-237]: `def test_reference_code_agrees_with_the_old_enclosure_at_5_4()`
- **test `test_rounded_enclosure_contains_every_exact_w_star_entry_at_7_4`** [L240-247]: `def test_rounded_enclosure_contains_every_exact_w_star_entry_at_7_4()`
- **test `test_planted_narrow_enclosure_is_caught_by_the_reference`** [L250-255]: `def test_planted_narrow_enclosure_is_caught_by_the_reference()`
- **function `star`** [L260-261]: `def star()` decorators: @pytest.fixture(scope='module')
- **function `law`** [L264-265]: `def law(proc, sigma, nb=Fraction(1, 5))`
- **test `test_law_bound_w_star_is_bounded_with_kappa_below_one`** [L268-273]: `def test_law_bound_w_star_is_bounded_with_kappa_below_one(star)`
- **test `test_law_bound_default_arguments_are_w_star`** [L276-279]: `def test_law_bound_default_arguments_are_w_star(star)`
- **test `test_law_bound_sigma_3_2_is_bounded`** [L282-289]: `def test_law_bound_sigma_3_2_is_bounded()`
- **test `test_law_bound_w0_equals_contract_with_zero_delta`** [L292-304]: `def test_law_bound_w0_equals_contract_with_zero_delta()`
- **function `snapshot`** [L308-309]: `def snapshot()`
- **test `test_bound_law_sets_and_restores_after_normal_exit`** [L312-320]: `def test_bound_law_sets_and_restores_after_normal_exit()`
- **test `test_bound_law_restores_after_an_exception`** [L323-330]: `def test_bound_law_restores_after_an_exception()`
- **test `test_law_bound_restores_after_normal_return_and_after_a_failure`** [L333-345]: `def test_law_bound_restores_after_normal_return_and_after_a_failure(star, monkeypatch)`
- **test `test_digits_other_than_60_is_refused`** [L348-352]: `def test_digits_other_than_60_is_refused()`

