# `tests/hwsu/test_b_of_obligation.py`

- Source: [tests/hwsu/test_b_of_obligation.py](../../../../../tests/hwsu/test_b_of_obligation.py)
- Kind: python
- Lines: 360

## Module docstring

> Author B (job 0198): the array name rule, the J10/J11 obligation writer and the OF-H hygiene
> gate (protocol §8.2 4(b), §4.2 OF-H, RC-5; joint rulings J10, J11 = addendum 4; API §5.6 and
> the J11 erratum). TEST_PLAN §3 row test_b_of_obligation; DRO7, DRO9. Synthetic stores only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 23, via sys.path edit)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../../tools/hwsu/hwsu_records.py.md) (line 24, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 25, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 26, via unique basename)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 318, via sys.path edit) (inside a function)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 325, via sys.path edit) (inside a function)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 326, via sys.path edit) (inside a function)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 340, via sys.path edit) (inside a function)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 349, via sys.path edit) (inside a function)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 357, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 5)
- `builtins` (lines 7)
- `copy` (lines 8)
- `fractions` (lines 267)
- `hashlib` (lines 9)
- `io` (lines 10)
- `json` (lines 11)
- `os` (lines 12)
- `pathlib` (lines 15)
- `re` (lines 13)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `C`
- `HIST`
- `LINEAGE`
- `OB`
- `REPO`

## Classes and functions

- **function `_norm`** [L33-34]: `def _norm(p) -> str`
- **function `_hook`** [L37-56]: `def _hook(monkeypatch) -> list`
- **function `_sha`** [L59-60]: `def _sha(p) -> str`
- **function `_hist_arrays`** [L63-67]: `def _hist_arrays(n=4, sym=10)`
- **function `_npz`** [L70-74]: `def _npz(path, **arrays) -> Path`
- **test `test_obligation_names`** [L78-84]: `def test_obligation_names()`
- **test `test_name_class`** [L115-116]: `def test_name_class(rel, dry, want)` decorators: @pytest.mark.parametrize('rel,dry,want', [('stages/OF/HIST_OF_fit_b0.npz', False, HIST), ('stages/OF/HIST_OF_eval_a2_b1.npz', False, HIST), ('stages/OF/ORACLE_OF_eval.npz', False, 'NON_HISTORY'), ('stages/OF/MOMENTS_x.npz', False, 'NON_HISTORY'), ('stages/OF/FIT_OF_O.npz', False, 'NON_HISTORY'), ('stages/OF/BOOT_OF.npz', False, 'NON_HISTORY'), ('stages/OF/PREC_OF.npz', False, 'NON_HISTORY'), ('stages/X/PAIR_1.npy', False, 'NON_HISTORY'), ('stages/X/OTHER_1.npz', False, None), ('stages/OF/ACTS_x.npz', False, None), ('ORACLE_x.npz', False, None), ('registry/x.npz', False, 'NON_HISTORY_REGISTRY'), ('artifacts/Checkpoint/abc/payload.npz', False, 'NON_HISTORY_ARTIFACT'), ('artifacts/Checkpoint/abc/state.pt', False, 'NON_HISTORY_ARTIFACT'), ('artifacts/EmissionSpec/abc/payload.npz', False, 'NON_HISTORY_ARTIFACT'), ('artifacts/WorldSpec/abc/payload.npz', False, 'NON_HISTORY_ARTIFACT'), ('artifacts/ObservationSet/abc/payload.npz', False, None), ('artifacts/Checkpoint/abc/other.npz', False, None), ('stages/OF/DRYHIST_OF_fit_b0.npz', False, None), ('stages/OF/DRYHIST_OF_fit_b0.npz', True, HIST), ('stages/OF/HIST_OF_fit_b0.npz', True, None), ('stages/OF/ORACLE_OF_eval.npz', True, 'NON_HISTORY')])
- **test `test_name_class_non_array_refused`** [L119-122]: `def test_name_class_non_array_refused()`
- **test `test_name_class_reads_contract_prefixes`** [L125-129]: `def test_name_class_reads_contract_prefixes()`
- **test `test_save_array_accepts_named_and_history`** [L132-143]: `def test_save_array_accepts_named_and_history(tmp_path)`
- **test `test_save_array_refuses_outside_rule`** [L150-158]: `def test_save_array_refuses_outside_rule(tmp_path, rel, dry)` decorators: @pytest.mark.parametrize('rel,dry', [('stages/X/OTHER_1.npz', False), ('registry/x.npz', False), ('artifacts/Checkpoint/a/payload.npz', False), ('stages/OF/HIST_OF_fit_b0.npz', True), ('stages/OF/DRYHIST_OF_fit_b0.npz', False)]) - DRO9 (7): a write outside the frozen name rule is refused before anything is written.
- **function `_fixture_store`** [L162-177]: `def _fixture_store(root)`
- **function `_expected_entry`** [L180-189]: `def _expected_entry(rel, path)`
- **test `test_write_obligation_exact_j11_form`** [L192-214]: `def test_write_obligation_exact_j11_form(tmp_path, monkeypatch)`
- **test `test_write_obligation_rules_match_their_files`** [L217-224]: `def test_write_obligation_rules_match_their_files(tmp_path)`
- **test `test_write_obligation_refuses_unclassifiable`** [L227-233]: `def test_write_obligation_refuses_unclassifiable(tmp_path)`
- **test `test_write_obligation_no_history_and_exclusive`** [L236-247]: `def test_write_obligation_no_history_and_exclusive(tmp_path)`
- **test `test_write_obligation_dry_store`** [L250-262]: `def test_write_obligation_dry_store(tmp_path)`
- **test `test_registry_risk_exact_rationals`** [L266-276]: `def test_registry_risk_exact_rationals()`
- **function `_p_d2a`** [L280-285]: `def _p_d2a(T, E, pi)`
- **function `_ctx`** [L288-301]: `def _ctx(E_low=0.01, planted=False)`
- **function `_status`** [L304-309]: `def _status(fn, *a)`
- **function `_handoff`** [L312-314]: `def _handoff(monkeypatch, p)`
- **test `test_of_h_pass`** [L317-321]: `def test_of_h_pass(monkeypatch)`
- **test `test_of_h_sealed_row_first_and_no_oracle`** [L324-335]: `def test_of_h_sealed_row_first_and_no_oracle(monkeypatch)`
- **test `test_of_h_sealed_row_in_any_split`** [L339-345]: `def test_of_h_sealed_row_in_any_split(monkeypatch, where)` decorators: @pytest.mark.parametrize('where', ['fit', 'a1'])
- **test `test_of_h_p_d2a_mismatch`** [L348-353]: `def test_of_h_p_d2a_mismatch(monkeypatch)`
- **test `test_of_h_registry_risk_over_cap`** [L356-360]: `def test_of_h_registry_risk_over_cap(monkeypatch)`

