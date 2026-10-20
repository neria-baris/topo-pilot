# `tests/k4b/test_b_h1_meta.py`

- Source: [tests/k4b/test_b_h1_meta.py](../../../../../tests/k4b/test_b_h1_meta.py)
- Kind: python
- Lines: 359

## Module docstring

> Author B, round 2: API §14.1 and coordinator ruling R19 (API §15). The H1 checkpoint-meta
> identity check: `expected_meta` from CONTRACT (payload_sha256 from
> checkpoints[j].meta_payload_sha256, never None), `check_checkpoint_meta` with exact,
> type-strict comparisons (`==` plus `type(...) is` for ints; a list run_key is never equal to a
> tuple), and `checkpoint_meta`, which reads <root>/Checkpoint/<id>/meta.json and nothing else.

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 29, via sys.path edit)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../../tools/k4b/k4b_driver.py.md) (line 30, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 10)
- `builtins` (lines 12)
- `copy` (lines 13)
- `io` (lines 14)
- `json` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 18)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `CASES`
- `CK`
- `FORBIDDEN`
- `IDENTITY`
- `IDS`
- `LABELS`
- `MISSING`
- `MODELS`
- `ORDER`
- `PAYLOAD`
- `REPO`
- `RUN_KEY`
- `SEEDS`
- `STEP`
- `TYPE_CASES`
- `VALUE_CASES`

## Classes and functions

- **function `seed_key`** [L58-59]: `def seed_key(j) -> str`
- **function `good_meta`** [L62-70]: `def good_meta(j, label) -> dict` - A meta.json as ArtifactStore writes it (extra keys included), built from the literals.
- **function `check`** [L73-74]: `def check(meta, j=1729, label='step5000') -> dict`
- **function `only_mismatch`** [L77-83]: `def only_mismatch(res, token) -> dict`
- **function `set_at`** [L86-91]: `def set_at(meta, path, value) -> dict`
- **function `del_at`** [L94-99]: `def del_at(meta, path) -> dict`
- **test `test_expected_meta_from_contract`** [L105-116]: `def test_expected_meta_from_contract(j, label)` decorators: @pytest.mark.parametrize('j,label', CASES)
- **test `test_expected_payload_sha_is_bound_never_none`** [L120-125]: `def test_expected_payload_sha_is_bound_never_none(j, label)` decorators: @pytest.mark.parametrize('j,label', CASES)
- **test `test_expected_meta_unknown_model_or_label_raises`** [L129-131]: `def test_expected_meta_unknown_model_or_label_raises(j, label)` decorators: @pytest.mark.parametrize('j,label', [(1234, 'step5000'), (1729, 'step100'), (1729, 'emission')])
- **test `test_contract_meta_passes_and_check_is_pure`** [L137-154]: `def test_contract_meta_passes_and_check_is_pure(j, label, monkeypatch)` decorators: @pytest.mark.parametrize('j,label', CASES)
- **test `test_single_field_value_mismatch_is_identity`** [L179-184]: `def test_single_field_value_mismatch_is_identity(token, path, value, label)` decorators: @pytest.mark.parametrize('label', LABELS) @pytest.mark.parametrize('token,path,value', VALUE_CASES)
- **test `test_wrong_type_follows_pinned_strictness`** [L204-207]: `def test_wrong_type_follows_pinned_strictness(token, path, value, labels)` decorators: @pytest.mark.parametrize('token,path,value,labels', TYPE_CASES)
- **test `test_missing_key_is_a_mismatch_not_an_exception`** [L223-225]: `def test_missing_key_is_a_mismatch_not_an_exception(token, path)` decorators: @pytest.mark.parametrize('token,path', MISSING)
- **test `test_missing_config_fails_run_key_and_step`** [L228-233]: `def test_missing_config_fails_run_key_and_step()`
- **test `test_other_models_meta_fails_on_every_model_bound_field`** [L236-245]: `def test_other_models_meta_fails_on_every_model_bound_field()` - 2718's complete meta checked against 1729's expectation: id, run_key, seed, payload.
- **test `test_several_mismatches_are_all_reported_in_checked_order`** [L248-258]: `def test_several_mismatches_are_all_reported_in_checked_order()`
- **test `test_trained_meta_against_step0_expectation_fails`** [L261-265]: `def test_trained_meta_against_step0_expectation_fails()`
- **function `ck_dir`** [L270-273]: `def ck_dir(root: Path, aid: str) -> Path`
- **function `with_payload_files`** [L276-279]: `def with_payload_files(d: Path) -> None`
- **function `guard_payload`** [L282-298]: `def guard_payload(monkeypatch, seen: list) -> None`
- **test `test_checkpoint_meta_reads_meta_json_only`** [L302-315]: `def test_checkpoint_meta_reads_meta_json_only(tmp_path, monkeypatch, j, label)` decorators: @pytest.mark.parametrize('j,label', CASES)
- **test `test_checkpoint_meta_unreadable_or_malformed_is_identity`** [L320-339]: `def test_checkpoint_meta_unreadable_or_malformed_is_identity(tmp_path, monkeypatch, case)` decorators: @pytest.mark.parametrize('case', ['missing_dir', 'missing_file', 'empty', 'truncated', 'not_json', 'bad_utf8', 'is_directory'])
- **test `test_checkpoint_meta_reads_the_named_id_only`** [L342-349]: `def test_checkpoint_meta_reads_the_named_id_only(tmp_path)`
- **test `test_json_str_step_on_disk_fails_identity`** [L352-359]: `def test_json_str_step_on_disk_fails_identity(tmp_path)`

