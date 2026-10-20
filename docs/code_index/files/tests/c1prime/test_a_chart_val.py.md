# `tests/c1prime/test_a_chart_val.py`

- Source: [tests/c1prime/test_a_chart_val.py](../../../../../tests/c1prime/test_a_chart_val.py)
- Kind: python
- Lines: 221

## Module docstring

> Independent tests, author A (job 0026): C0-val criteria and the construction ledger
> (TEST_PLAN A-1 items 7 and 8; protocol section 14 'Validation chart gates' and 'Construction
> limit').

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 29, via sys.path edit)
- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 30, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 31, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 32, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 25: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`
- line 27: `str(REPO / 'src')` -> `src`

## Imported by

- none

## Top-level constants

- `ANGLES`
- `BALANCED_507`
- `GAUGE`
- `L`
- `NAMES`
- `PROD`
- `REPO`
- `RING`

## Classes and functions

- **function `synthetic_chart`** [L41-47]: `def synthetic_chart(landmarks, phi, info=None)`
- **function `queries`** [L53-58]: `def queries(bin_counts, n_far)`
- **function `direct_for`** [L61-63]: `def direct_for(ext_phase, cstar, phi=None)`
- **function `criteria`** [L66-76]: `def criteria(result)`
- **function `no_chart_gates`** [L80-86]: `def no_chart_gates(monkeypatch)` decorators: @pytest.fixture(autouse=True) - chart.chart_gates must never be called (its support criterion is every-row).
- **function `evaluate`** [L89-115]: `def evaluate(bin_counts, n_far, cstar=None, direct_phi=None)`
- **test `test_support_507_of_512_passes`** [L121-123]: `def test_support_507_of_512_passes()`
- **test `test_support_506_of_512_fails`** [L126-131]: `def test_support_506_of_512_fails()`
- **test `test_bins_and_resultant_use_all_512_queries_including_unsupported`** [L134-140]: `def test_bins_and_resultant_use_all_512_queries_including_unsupported()` - Bins and resultant count every production-extension query, supported or not.
- **test `test_resultant_fails_while_bins_pass`** [L143-146]: `def test_resultant_fails_while_bins_pass()`
- **test `test_bins_fail_while_resultant_passes`** [L149-152]: `def test_bins_fail_while_resultant_passes()`
- **test `test_fidelity_uses_the_complete_direct_component_unmasked_by_support`** [L155-165]: `def test_fidelity_uses_the_complete_direct_component_unmasked_by_support()`
- **test `test_fidelity_below_080_fails`** [L168-175]: `def test_fidelity_below_080_fails()`
- **test `test_extend_phase_is_the_frozen_extend`** [L178-184]: `def test_extend_phase_is_the_frozen_extend()`
- **function `ledger_path`** [L187-188]: `def ledger_path(tmp_path)`
- **test `test_six_constructions_then_refusal`** [L191-199]: `def test_six_constructions_then_refusal(tmp_path)`
- **test `test_no_second_claim_of_the_same_model_and_role`** [L202-209]: `def test_no_second_claim_of_the_same_model_and_role(tmp_path)`
- **test `test_claims_survive_a_new_ledger_object`** [L212-221]: `def test_claims_survive_a_new_ledger_object(tmp_path)`

