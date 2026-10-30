# `tests/hwsc/test_a_outcomes.py`

- Source: [tests/hwsc/test_a_outcomes.py](../../../../../tests/hwsc/test_a_outcomes.py)
- Kind: python
- Lines: 332

## Module docstring

> Author A (job 0176): outcome precedence, gate-record mapping and licences.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 22, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 23, via sys.path edit)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../../tools/hwsc/hwsc_gates.py.md) (line 24, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 25, via unique basename)

### External (third-party)

- `pytest` (lines 15)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `pathlib` (lines 13)
- `re` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `_HWSC` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `ALL`
- `C`
- `FILL`
- `FS`
- `LIC`
- `MODELS`
- `NO_STATEMENT`
- `PASSES`
- `REPO`
- `_HWSC`

## Classes and functions

- **function `state`** [L35-39]: `def state(**kw)`
- **function `endpoint`** [L42-53]: `def endpoint(spec)` - spec {j: (L, U)} -> an ENDPOINT-like result (statuses by k4b_stats).
- **test `test_fail_beats_everything`** [L64-69]: `def test_fail_beats_everything()`
- **test `test_resource_beats_not_learned_and_k4b`** [L72-74]: `def test_resource_beats_not_learned_and_k4b()`
- **test `test_not_learned_beats_k4b`** [L78-85]: `def test_not_learned_beats_k4b(k)` decorators: @pytest.mark.parametrize('k', [1, 2, 3])
- **test `test_k4b_reasons_pass_through`** [L89-98]: `def test_k4b_reasons_pass_through(reason)` decorators: @pytest.mark.parametrize('reason', C['outcomes']['k4b_reasons'])
- **test `test_k4b_beats_endpoint`** [L101-104]: `def test_k4b_beats_endpoint()`
- **test `test_authority_resource_map_to_row2`** [L108-109]: `def test_authority_resource_map_to_row2(st)` decorators: @pytest.mark.parametrize('st', ['INCONCLUSIVE/AUTHORITY', 'INCONCLUSIVE/RESOURCE'])
- **test `test_unknown_inconclusive_reason_is_fail_technical`** [L112-114]: `def test_unknown_inconclusive_reason_is_fail_technical()`
- **test `test_endpoint_passes_through_with_annotations`** [L123-129]: `def test_endpoint_passes_through_with_annotations(spec, expected)` decorators: @pytest.mark.parametrize('spec, expected', [({j: (0.05, 0.06) for j in MODELS}, 'SUPPORT'), ({j: (0.002, 0.005) for j in MODELS}, 'EXCLUSION'), ({J1: (0.05, 0.06), J2: (0.002, 0.005), J3: (0.0, 0.02)}, 'MIXED'), ({j: (0.0, 0.02) for j in MODELS}, 'INCONCLUSIVE')])
- **test `test_endpoint_inconclusive_numerical`** [L132-135]: `def test_endpoint_inconclusive_numerical()`
- **test `test_empty_state_returns_fail_technical_outcome`** [L138-140]: `def test_empty_state_returns_fail_technical_outcome()`
- **test `test_literally_empty_dict_state`** [L143-146]: `def test_literally_empty_dict_state()`
- **function `rec`** [L152-153]: `def rec(gate, status, **details)`
- **test `test_state_from_gates_fail_first`** [L159-163]: `def test_state_from_gates_fail_first()`
- **test `test_state_from_gates_resource`** [L168-171]: `def test_state_from_gates_resource(status)` decorators: @pytest.mark.parametrize('status', ['INCONCLUSIVE/RESOURCE_OR_AUTHORITY', 'INCONCLUSIVE/AUTHORITY', 'INCONCLUSIVE/RESOURCE'])
- **test `test_state_from_gates_not_learned`** [L174-186]: `def test_state_from_gates_not_learned()`
- **test `test_state_from_gates_k4b_and_endpoint`** [L189-196]: `def test_state_from_gates_k4b_and_endpoint()`
- **class `_NA(dict)`** [L202-204]
- **method `_NA.__missing__`** [L203-204]: `def __missing__(self, key)`
- **function `oc_of`** [L212-214]: `def oc_of(outcome, k=None, models=None, criterion=None, annotations=(), pbm=None)`
- **function `expected`** [L217-223]: `def expected(head, fill, oc)`
- **test `test_support_licence_exact`** [L226-231]: `def test_support_licence_exact()`
- **test `test_missing_fields_are_na`** [L234-237]: `def test_missing_fields_are_na()`
- **function `excl`** [L240-241]: `def excl(fill)`
- **test `test_exclusion_oracle_sentence_rules`** [L244-255]: `def test_exclusion_oracle_sentence_rules()`
- **test `test_no_statement_heads`** [L260-261]: `def test_no_statement_heads(outcome)` decorators: @pytest.mark.parametrize('outcome', ['FAIL_TECHNICAL/LINEAGE', 'FAIL_TECHNICAL/OUTCOME', 'INCONCLUSIVE/RESOURCE_OR_AUTHORITY'])
- **test `test_not_learned_and_chart_unavailable_texts`** [L264-271]: `def test_not_learned_and_chart_unavailable_texts()`
- **test `test_limitation_heads`** [L277-279]: `def test_limitation_heads(outcome)` decorators: @pytest.mark.parametrize('outcome', ['MIXED', 'INCONCLUSIVE', 'INCONCLUSIVE/NUMERICAL', 'INCONCLUSIVE/HEADROOM', 'INCONCLUSIVE/UNDERPOWERED', 'INCONCLUSIVE/REGISTRY_INCOMPLETE'])
- **test `test_every_contract_head_fills`** [L282-293]: `def test_every_contract_head_fills()`
- **test `test_positive_below_margin_licence_sentences`** [L296-307]: `def test_positive_below_margin_licence_sentences()`
- **test `test_pbm_licence_only_exclude_kind`** [L310-317]: `def test_pbm_licence_only_exclude_kind()`
- **test `test_disclosure_equals_protocol_6_4`** [L323-332]: `def test_disclosure_equals_protocol_6_4()`

