# `tests/k4b/test_b_flow.py`

- Source: [tests/k4b/test_b_flow.py](../../../../../tests/k4b/test_b_flow.py)
- Kind: python
- Lines: 279

## Module docstring

> Author B, K4b TEST_PLAN B9, B10, B11, B14, B21: the sealed file and the refusal of any
> report that would let X-bar(+/-) = C +/- D be reconstructed; gate order and first-non-PASS
> stop; no fresh access without a verified release B; the G0 seed classification (RC5).

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 22, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 23, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 24, via sys.path edit)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 25, via sys.path edit)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../../tools/k4b/k4b_fresh.py.md) (line 26, via sys.path edit)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../../tools/k4b/k4b_release.py.md) (line 27, via sys.path edit)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 28, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 29, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 30, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)
- `from topo_pilot.dataset.checks import check_disjoint` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 187, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 7)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `AUTHORITY`
- `REPO`
- `SEALED_KEYS`

## Classes and functions

- **test `test_sealed_keys_are_the_registered_tuple`** [L41-42]: `def test_sealed_keys_are_the_registered_tuple()`
- **function `clean_report`** [L45-50]: `def clean_report()`
- **test `test_check_unsealed_accepts_a_clean_report`** [L53-54]: `def test_check_unsealed_accepts_a_clean_report()`
- **test `test_check_unsealed_refuses_any_sealed_key_anywhere`** [L59-70]: `def test_check_unsealed_refuses_any_sealed_key_anywhere(key, where)` decorators: @pytest.mark.parametrize('key', SEALED_KEYS) @pytest.mark.parametrize('where', ['top', 'nested', 'in_list'])
- **test `test_report_with_width_and_supported_contribution_refused`** [L73-78]: `def test_report_with_width_and_supported_contribution_refused()` - C = mean(A u r4) beside D = width/2 would unseal X-bar(+/-) = C +/- D (RC3).
- **function `support_inputs`** [L81-91]: `def support_inputs()`
- **test `test_support_report_sealed_form_has_no_reconstructing_keys`** [L94-104]: `def test_support_report_sealed_form_has_no_reconstructing_keys()`
- **test `test_support_report_unsealed_form_is_refused_in_a_validation_report`** [L107-116]: `def test_support_report_unsealed_form_is_refused_in_a_validation_report()`
- **test `test_write_sealed_never_overwrites`** [L119-125]: `def test_write_sealed_never_overwrites(tmp_path)`
- **test `test_gate_order_release_a`** [L130-132]: `def test_gate_order_release_a()`
- **function `gate_lines`** [L135-137]: `def gate_lines(out)`
- **function `full`** [L140-141]: `def full(rec)`
- **function `make_steps`** [L144-152]: `def make_steps(failure_at, exc, calls)`
- **test `test_run_gates_all_pass_in_order`** [L155-163]: `def test_run_gates_all_pass_in_order(tmp_path)`
- **test `test_first_non_pass_stops_and_later_gates_not_run`** [L172-183]: `def test_first_non_pass_stops_and_later_gates_not_run(tmp_path, exc, expected)` decorators: @pytest.mark.parametrize('exc,expected', [(C1GateFailure('INCONCLUSIVE/HEADROOM', 'lower 0.009'), 'INCONCLUSIVE/HEADROOM'), (C1GateFailure('FAIL_TECHNICAL/ORACLE', 'moment gap'), 'FAIL_TECHNICAL/ORACLE'), (ValueError('boom'), 'FAIL_TECHNICAL'), (errors.Unresolved('zero gauge alignment'), 'INCONCLUSIVE')])
- **test `test_split_overlap_maps_to_lineage`** [L186-196]: `def test_split_overlap_maps_to_lineage(tmp_path)`
- **function `release`** [L201-210]: `def release(path, **over)`
- **test `test_verify_release_refuses_mismatches`** [L221-225]: `def test_verify_release_refuses_mismatches(tmp_path, over, kind, task, session)` decorators: @pytest.mark.parametrize('over,kind,task,session', [({'kind': 'A'}, 'B', 'AB' * 32, 'sess-1'), ({}, 'B', 'AB' * 32, 'sess-2'), ({}, 'B', 'CD' * 32, 'sess-1'), ({'protocol_sha256': 'f' * 64}, 'B', 'AB' * 32, 'sess-1'), ({'N': None, 'k': None}, 'B', 'AB' * 32, 'sess-1'), ({'worker_session': ''}, 'B', 'AB' * 32, '')])
- **test `test_authorized_worker`** [L228-232]: `def test_authorized_worker()`
- **test `test_no_fresh_access_without_release_b`** [L236-249]: `def test_no_fresh_access_without_release_b(tmp_path, case)` decorators: @pytest.mark.parametrize('case', ['missing', 'malformed', 'kind_A', 'session'])
- **function `hit`** [L254-255]: `def hit(kind, i=0)`
- **test `test_own_declarations_are_not_prior_use`** [L258-263]: `def test_own_declarations_are_not_prior_use()`
- **test `test_no_hits_pass`** [L266-267]: `def test_no_hits_pass()`
- **test `test_prior_or_unclassified_hit_fails_closed`** [L271-279]: `def test_prior_or_unclassified_hit_fails_closed(bad)` decorators: @pytest.mark.parametrize('bad', ['prior_issuance', 'unclassified', 'maybe'])

