# `tests/hwsc/test_b_guard_meter.py`

- Source: [tests/hwsc/test_b_guard_meter.py](../../../../../tests/hwsc/test_b_guard_meter.py)
- Kind: python
- Lines: 346

## Module docstring

> Author B (job 0176): the blindness guard (exactly the R-0176-G1 five-path list), the G0c seed
> search and its mirror equality (R-0176-G2), hit classification, and the meter binding (DRC11,
> DRC13, DRC14, KC0 pieces).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 26, via sys.path edit)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 27, via sys.path edit)
- `import hwsc_meter_bind` -> [tools/hwsc/hwsc_meter_bind.py](../../tools/hwsc/hwsc_meter_bind.py.md) (line 28, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 29, via unique basename)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../../tools/x4_oracle_profile/controls.py.md) (line 30, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../../tools/hwsb/hwsb_known.py.md) (line 31, via unique basename)
- `import hws_driver` -> [tools/hws/hws_driver.py](../../tools/hws/hws_driver.py.md) (line 32, via unique basename)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../../tools/k4b/k4b_meter_bind.py.md) (line 33, via unique basename)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../../tools/x4_oracle_profile/meter.py.md) (line 34, via unique basename)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../../tools/x4_oracle_profile/winjob.py.md) (line 35, via unique basename)

### External (third-party)

- `pytest` (lines 19)

### Standard library

- `__future__` (lines 11)
- `json` (lines 13)
- `math` (lines 14)
- `os` (lines 15)
- `pathlib` (lines 17)
- `sys` (lines 16)
- `tempfile` (lines 298)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `BLINDED`
- `C`
- `CAPS`
- `PROJECT`
- `READABLE`
- `REPO`
- `_HWSC`
- `_REC`

## Classes and functions

- **function `_audit`** [L43-45]: `def _audit(event, args)`
- **function `rec`** [L52-56]: `def rec()` decorators: @pytest.fixture
- **function `_opened`** [L59-61]: `def _opened(records, path)`
- **function `_write`** [L64-67]: `def _write(path, text='{}')`
- **test `test_blindness_list_is_exactly_the_five_rules`** [L85-88]: `def test_blindness_list_is_exactly_the_five_rules()`
- **test `test_blinded_true`** [L92-96]: `def test_blinded_true(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', BLINDED)
- **test `test_blinded_false`** [L100-101]: `def test_blinded_false(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', READABLE)
- **test `test_blinded_default_root_is_pure`** [L104-107]: `def test_blinded_default_root_is_pure()`
- **test `test_public_summary`** [L116-117]: `def test_public_summary(tmp_path, rel, want)` decorators: @pytest.mark.parametrize('rel,want', [('00_READ_ME_FIRST_Research_Summary/a.pdf', True), ('x/00_read_me_first.md', True), ('docs/research_summary/main.tex', True), ('docs/research_summary', True), ('Docs/Research_Summary/fig.png', True), ('docs/research_summary_old/x', False), ('mydocs/research_summary/x', False), ('docs/code_index/FILES.md', False), ('x/read_me_first.md', False)])
- **test `test_guard_refuses_before_any_open`** [L126-133]: `def test_guard_refuses_before_any_open(tmp_path, rec, rel)` decorators: @pytest.mark.parametrize('rel', ['hwsb-store/REPORT.json', 'hwsb-store/GATES.jsonl', 'hwsb-store/stages/EVAL/x.json', 'hwsb-store/CHART_CONSTRUCTIONS_trained.json', 'agent-handoff/jobs/0175/review.md', '00_READ_ME_FIRST_x/a.json', 'docs/research_summary/b.json'])
- **test `test_guard_reads_dispatch_metadata`** [L139-145]: `def test_guard_reads_dispatch_metadata(tmp_path, rel)` decorators: @pytest.mark.parametrize('rel', ['agent-handoff/jobs/0175/task.json', 'agent-handoff/jobs/0175/request.before.json', 'hwsb-store/HANDOFF.json'])
- **test `test_needle_in`** [L154-156]: `def test_needle_in(needle, line, want)` decorators: @pytest.mark.parametrize('needle,line,want', [('620301', 'seed 620301,', True), ('620301', '620301', True), ('620301', '"620301"', True), ('620301', 'a620301b', False), ('620301', '6203011', False), ('620301', 'x620301f9', False), ('620301', '_620301', False), ('620301', '1620301', False), ('hwsc-v1', 'xhwsc-v1y', True), ('hwsc-v1', 'hwsc-v2', False)])
- **function `_seed_root`** [L159-177]: `def _seed_root(root, blinded=True)`
- **function `_rel`** [L180-181]: `def _rel(root, hits)`
- **test `test_seed_search_c_prunes_and_never_opens_blinded`** [L184-197]: `def test_seed_search_c_prunes_and_never_opens_blinded(tmp_path, rec)`
- **test `test_seed_search_c_equals_hws_mirror_without_blinded_paths`** [L200-205]: `def test_seed_search_c_equals_hws_mirror_without_blinded_paths(tmp_path)`
- **test `test_classify_hits_c`** [L208-227]: `def test_classify_hits_c(tmp_path)`
- **function `meter_state`** [L232-240]: `def meter_state(monkeypatch)` decorators: @pytest.fixture
- **test `test_bind_per_stage`** [L248-266]: `def test_bind_per_stage(tmp_path, meter_state, stage)` decorators: @pytest.mark.parametrize('stage', list(CAPS))
- **test `test_bind_default_temp_root_and_unknown_stage`** [L269-274]: `def test_bind_default_temp_root_and_unknown_stage(tmp_path, meter_state)`
- **test `test_job_paths_and_placement`** [L277-291]: `def test_job_paths_and_placement()`
- **test `test_this_suite_runs_outside_the_project`** [L294-301]: `def test_this_suite_runs_outside_the_project(tmp_path)`
- **function `_argv`** [L304-309]: `def _argv(**drop)`
- **function `_main_code`** [L312-316]: `def _main_code()`
- **test `test_main_missing_argument_is_2`** [L320-324]: `def test_main_missing_argument_is_2(monkeypatch, meter_state, drop)` decorators: @pytest.mark.parametrize('drop', ['stage', 'job', 'kind', 'session', 'task_sha256'])
- **test `test_main_unknown_stage_is_2`** [L327-332]: `def test_main_unknown_stage_is_2(monkeypatch, meter_state)`
- **test `test_main_refuses_a_foreign_run_lock`** [L335-346]: `def test_main_refuses_a_foreign_run_lock(tmp_path, monkeypatch, meter_state)`

