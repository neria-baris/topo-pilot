# `tests/hwsu/test_a_u2_outcome.py`

- Source: [tests/hwsu/test_a_u2_outcome.py](../../../../../tests/hwsu/test_a_u2_outcome.py)
- Kind: python
- Lines: 204

## Module docstring

> Author A (job 0223): aggregation, outcomes and licences (protocol 2.9 overall rules, 7;
> API_U2 4.5, 4.9). Expected values come from a hand reimplementation of the protocol rules.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 15, via sys.path edit)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 16, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 28, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 4)
- `importlib` (lines 6)
- `itertools` (lines 7)
- `pathlib` (lines 10)
- `re` (lines 8)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 30: `dynamic: name`

### sys.path additions

- line 13: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `CATS`
- `COMBOS`
- `MASTERS`
- `OUT`
- `REPO`
- `RESP`
- `SH`
- `SHARE`
- `STATUSES`

## Classes and functions

- **function `mod`** [L27-30]: `def mod(name)`
- **function `base`** [L33-34]: `def base(s)`
- **function `expected`** [L37-47]: `def expected(per_model)`
- **test `test_every_combination`** [L54-57]: `def test_every_combination(combo)` decorators: @pytest.mark.parametrize('combo', COMBOS, ids=['-'.join((base(x)[:4] for x in c)) for c in COMBOS])
- **test `test_order_responds_beats_weak`** [L60-62]: `def test_order_responds_beats_weak()`
- **test `test_mixed_and_precision`** [L65-72]: `def test_mixed_and_precision()`
- **test `test_fewer_than_two_live_names_the_gate`** [L75-78]: `def test_fewer_than_two_live_names_the_gate()`
- **test `test_dissent_names_differing_models`** [L81-88]: `def test_dissent_names_differing_models()`
- **function `_ms`** [L91-92]: `def _ms(status, rule6)`
- **test `test_rule6_aggregation`** [L97-105]: `def test_rule6_aggregation(flags, want)` decorators: @pytest.mark.parametrize('flags,want', [((1, 1, 1), 'all three'), ((1, 1, 0), 'in 2 models'), ((1, 0, 0), None), ((0, 0, 0), None)]) - per_model given as model_status results (status + rule6) for the rule-6 count.
- **test `test_share_outcome_is_fixed`** [L109-116]: `def test_share_outcome_is_fixed()`
- **test `test_share_outcome_ignores_any_data`** [L119-126]: `def test_share_outcome_ignores_any_data()` - No data path can change it: whatever responses are, the share stays fixed.
- **test `test_share_entry_points_fail_closed`** [L129-135]: `def test_share_entry_points_fail_closed()`
- **function `_rec`** [L139-140]: `def _rec(gate, status)`
- **test `test_study_outcome_precedence`** [L147-156]: `def test_study_outcome_precedence()`
- **test `test_contract_precedence_and_share_fixed`** [L159-164]: `def test_contract_precedence_and_share_fixed()`
- **function `_strings`** [L168-176]: `def _strings(x)`
- **function `_pipeline`** [L179-189]: `def _pipeline(thetas)`
- **test `test_licences_carry_scope_clause_and_disclosure`** [L194-204]: `def test_licences_carry_scope_clause_and_disclosure(thetas, outcome)` decorators: @pytest.mark.parametrize('thetas,outcome', [((0.8, 0.8, 0.8), 'RESPONDS'), ((0.0, 0.0, 0.0), 'LOW_RESPONSE')])

