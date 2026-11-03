# `tests/hwsu/test_b_of_bind.py`

- Source: [tests/hwsu/test_b_of_bind.py](../../../../../tests/hwsu/test_b_of_bind.py)
- Kind: python
- Lines: 298

## Module docstring

> Author B (job 0198): the call-allowlist and call-time-read audit run by OF-B (protocol §11.2,
> RC-10; API §7; D-25), including default arguments, dataclass fields and the explicit-argument
> rule for the accepted conditional reads (coordinator phase-1 rulings, "Conditional reads").
> Planted modules live under tmp_path only. TEST_PLAN §3 row test_b_of_bind_meter (audit part).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 19, via sys.path edit)
- `import hwsu_bind` -> [tools/hwsu/hwsu_bind.py](../../tools/hwsu/hwsu_bind.py.md) (line 20, via sys.path edit)

### External (third-party)

- `b0198_plant_mod` (lines 228)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)
- `textwrap` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `__import__` line 265: `dynamic: mod`

### sys.path additions

- line 17: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `BIND`
- `C`
- `CFG`
- `EXPLICIT_FAIL`
- `EXPLICIT_PASS`
- `HEAD`
- `MOD`
- `PHASE1_PY`
- `REPO`

## Classes and functions

- **function `_plant`** [L27-31]: `def _plant(tmp_path, body, name='hwsu_planted.py') -> Path`
- **function `_calls`** [L34-35]: `def _calls(tmp_path, body)`
- **test `test_references_resolve_aliases`** [L39-53]: `def test_references_resolve_aliases(tmp_path)`
- **test `test_allowlisted_and_external_pass`** [L57-74]: `def test_allowlisted_and_external_pass(tmp_path)`
- **test `test_unlisted_reference_fails`** [L79-83]: `def test_unlisted_reference_fails(tmp_path, ref)` decorators: @pytest.mark.parametrize('ref', ['c2_code.fwl', 'k4b_data.sealed_d2a_predicate', 'hwsc_data.load_world', 'c2_stage_s1.run', 'hwsb_config.MASTERS', 'k4b_config.chart_cfg'])
- **test `test_never_called_fails`** [L91-95]: `def test_never_called_fails(tmp_path, ref)` decorators: @pytest.mark.parametrize('ref', ['c2_model.load_models', 'c2_oracle.load_process', 'c2_oracle.h3', 'c2_oracle.decimal_rows', 'c2_stats.p1', 'c2_stats._summaries', 'k4b_driver.anything', 'k4b_driver.begin_stage', 'c2_model.m0', 'hwsc_data.registry_risk', 'c2_code.haar_frames', 'c2_attrib.desc_intervals', 'hwsc_config.load_handoff'])
- **test `test_never_called_wins_over_allowlist`** [L98-104]: `def test_never_called_wins_over_allowlist(tmp_path, monkeypatch)`
- **test `test_unlisted_from_import_fails`** [L109-111]: `def test_unlisted_from_import_fails(tmp_path, line)` decorators: @pytest.mark.parametrize('line', ['from c2_code import problem', 'from hwsc_data import process_identity', 'from hwsu_config import CONTRACT', 'from c1_records import run_c1_gate'])
- **test `test_listed_from_import_passes`** [L117-118]: `def test_listed_from_import_passes(tmp_path, line)` decorators: @pytest.mark.parametrize('line', ['from topo_pilot.contracts import SeedTree, ArtifactStore', 'from oracle_profile import ProfileError', 'from pathlib import Path', 'from json import dumps'])
- **test `test_contract_binding_lists`** [L121-131]: `def test_contract_binding_lists()`
- **function `_explicit_file`** [L150-159]: `def _explicit_file(tmp_path, call)`
- **test `test_argument_less_conditional_call_fails`** [L163-166]: `def test_argument_less_conditional_call_fails(tmp_path, call)` decorators: @pytest.mark.parametrize('call', EXPLICIT_FAIL)
- **test `test_explicit_conditional_call_passes`** [L170-171]: `def test_explicit_conditional_call_passes(tmp_path, call)` decorators: @pytest.mark.parametrize('call', EXPLICIT_PASS)
- **function `planted_reads`** [L220-231]: `def planted_reads(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `_reads`** [L234-239]: `def _reads(mod, qualname) -> set`
- **test `test_function_reads_direct`** [L249-250]: `def test_function_reads_direct(planted_reads, fn, want)` decorators: @pytest.mark.parametrize('fn,want', [('reads_const', {'b0198_plant_mod.SCALE'}), ('reads_world', {'b0198_plant_mod.CONTRACT["world"]'}), ('reads_models', {'b0198_plant_mod.CONTRACT["models"]'}), ('reads_default', {'b0198_plant_cfg.TOL'}), ('reads_alias', {'b0198_plant_cfg.SEED'})])
- **test `test_function_reads_descend_dataclass_and_callee`** [L255-258]: `def test_function_reads_descend_dataclass_and_callee(planted_reads, fn, want)` decorators: @pytest.mark.parametrize('fn,want', [('makes_box', {'b0198_plant_mod.LIMIT'}), ('calls_local', {'b0198_plant_mod.SCALE'})])
- **test `test_function_reads_real_functions_equal_contract`** [L261-267]: `def test_function_reads_real_functions_equal_contract()`
- **test `test_audit_reads_real_contract_pass`** [L271-273]: `def test_audit_reads_real_contract_pass()`
- **test `test_audit_reads_missing_listed_key_fails`** [L276-280]: `def test_audit_reads_missing_listed_key_fails()`
- **test `test_audit_reads_forbidden_without_conditional_entry`** [L283-288]: `def test_audit_reads_forbidden_without_conditional_entry()`
- **test `test_audit_real_phase1_files_pass`** [L295-298]: `def test_audit_real_phase1_files_pass()` decorators: @pytest.mark.skipif(not all((p.is_file() for p in PHASE1_PY)), reason='phase-1 code not complete yet')

