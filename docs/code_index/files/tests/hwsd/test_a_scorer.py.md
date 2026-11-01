# `tests/hwsd/test_a_scorer.py`

- Source: [tests/hwsd/test_a_scorer.py](../../../../../tests/hwsd/test_a_scorer.py)
- Kind: python
- Lines: 323

## Module docstring

> Author A (job 0197): the per-checkpoint scorer and its registered statuses (§2.4, §2.6, §7 rows
> 9-10; API.md §6 and §16; DRD6).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 27, via sys.path edit)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](../../tools/hwsd/hwsd_score.py.md) (line 28, via sys.path edit)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 29, via unique basename)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../../tools/k4b/k4b_charts.py.md) (line 30, via unique basename)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](../../tools/k4b/k4b_decoder.py.md) (line 31, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 32, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 33, via unique basename)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 9)
- `collections` (lines 14)
- `fractions` (lines 15)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 16)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `CRIT_FAIL`
- `CRIT_PASS`
- `HERE`
- `REPO`
- `WALL`

## Classes and functions

- **class `FakeChart`** [L42-43]
- **function `tabs`** [L46-55]: `def tabs(n=24, n_land=8, seed=0)`
- **function `install`** [L58-86]: `def install(monkeypatch, log, prod=('PASS', ''), direct=('PASS', ''), c0=('PASS', CRIT_PASS))`
- **function `acts_spy`** [L89-93]: `def acts_spy(log, out_dir, t)`
- **function `run_chart`** [L96-106]: `def run_chart(monkeypatch, tmp_path, j=620301, step=100, skip_direct=False, ledger=None, **kw)`
- **function `kinds`** [L109-110]: `def kinds(log)`
- **test `test_checkpoint_dir_and_one_ledger_per_checkpoint`** [L114-122]: `def test_checkpoint_dir_and_one_ledger_per_checkpoint(tmp_path)`
- **test `test_chart_one_pass_order_and_freeze`** [L126-144]: `def test_chart_one_pass_order_and_freeze(monkeypatch, tmp_path)`
- **test `test_second_construction_of_a_role_is_refused`** [L147-151]: `def test_second_construction_of_a_role_is_refused(monkeypatch, tmp_path)`
- **test `test_c0_cal_failure_no_direct_no_decoder_no_freeze`** [L154-165]: `def test_c0_cal_failure_no_direct_no_decoder_no_freeze(monkeypatch, tmp_path)`
- **test `test_c0_cal_fail_technical_stops`** [L168-171]: `def test_c0_cal_fail_technical_stops(monkeypatch, tmp_path)`
- **test `test_skip_direct`** [L174-178]: `def test_skip_direct(monkeypatch, tmp_path)`
- **test `test_direct_chart_not_pass_labels`** [L188-193]: `def test_direct_chart_not_pass_labels(monkeypatch, tmp_path, st, reason, label)` decorators: @pytest.mark.parametrize('st,reason,label', [('INCONCLUSIVE', 'NO_H1_BAR', 'SCORED_UNVALIDATED/INCONCLUSIVE: NO_H1_BAR'), ('INCONCLUSIVE/CHART_UNAVAILABLE', 'GIANT_BELOW_0.95', 'SCORED_UNVALIDATED/INCONCLUSIVE/CHART_UNAVAILABLE: GIANT_BELOW_0.95'), ('INCONCLUSIVE/RESOURCE', 'memory', 'SCORED_UNVALIDATED/INCONCLUSIVE/RESOURCE: memory'), ('INCONCLUSIVE', WALL, 'SCORED_UNVALIDATED/NATIVE_WALL: ' + WALL)])
- **test `test_direct_fail_technical_stops`** [L196-199]: `def test_direct_fail_technical_stops(monkeypatch, tmp_path)`
- **test `test_c0_val_criteria_label`** [L202-208]: `def test_c0_val_criteria_label(monkeypatch, tmp_path)`
- **test `test_native_wall_at_c0_cal`** [L211-214]: `def test_native_wall_at_c0_cal(monkeypatch, tmp_path)`
- **test `test_archived_wall_label_protocol_reading`** [L217-228]: `def test_archived_wall_label_protocol_reading()`
- **test `test_uncertified_precedes_validation`** [L231-237]: `def test_uncertified_precedes_validation(monkeypatch, tmp_path)`
- **test `test_36_checkpoints_at_most_72_claims`** [L240-249]: `def test_36_checkpoints_at_most_72_claims(monkeypatch, tmp_path)`
- **test `test_map_build_rules`** [L253-265]: `def test_map_build_rules()`
- **function `moments`** [L269-271]: `def moments(n, seed=3)`
- **test `test_arrays_one_planted`** [L274-298]: `def test_arrays_one_planted(monkeypatch)`
- **test `test_controls_one_against_control_arrays`** [L301-323]: `def test_controls_one_against_control_arrays(monkeypatch)`

