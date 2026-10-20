# `tests/x6_stage1/test_a_rules.py`

- Source: [tests/x6_stage1/test_a_rules.py](../../../../../tests/x6_stage1/test_a_rules.py)
- Kind: python
- Lines: 309

## Module docstring

> Author A: T-RULES (X6S1-FROZEN-v1 §2.4-§2.7, §3, §7.2, §7.6, §7.9, §10.1, §14.3; API.md §3.4,
> §9). Every §7.9 branch and its precedence, the missing-model convention, UNRESOLVED routing,
> SHARP/TARGET statuses, designed counts and the exact-rational thresholds (3/4)G0- and
> (3/4)Delta_W2^lo, with float inputs placed one ulp either side of the exact rational edges.

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 19, via sys.path edit)
- `import x6s1_decide` -> [tools/x6_stage1/x6s1_decide.py](../../tools/x6_stage1/x6s1_decide.py.md) (line 20, via sys.path edit)

### External (third-party)

- `pytest` (lines 14)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `decimal` (lines 10)
- `fractions` (lines 11)
- `math` (lines 8)
- `pathlib` (lines 12)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`

## Imported by

- none

## Top-level constants

- `BAND`
- `DW2_LO`
- `G0_S`
- `G8_S`
- `NOT_DET`
- `REGISTERED`
- `REPO`
- `RULE_CASES`
- `SEEDS`
- `VALIDITY`

## Classes and functions

- **function `float_le`** [L32-37]: `def float_le(x: Fraction) -> float` - Largest float f with Fraction(f) <= x.
- **test `test_stage0_thresholds_are_exact_rationals`** [L41-48]: `def test_stage0_thresholds_are_exact_rationals()`
- **test `test_sharp_target_statuses_at_exact_edges`** [L52-68]: `def test_sharp_target_statuses_at_exact_edges()`
- **test `test_cord_rule`** [L72-81]: `def test_cord_rule()`
- **function `ds`** [L85-90]: `def ds(**kw)`
- **function `plc`** [L93-94]: `def plc(**kw)`
- **function `ordd`** [L97-99]: `def ordd(na=None, init=None, ab=None, zc=None)`
- **test `test_ord_d_pass_fail_and_regret_bar_exact`** [L102-118]: `def test_ord_d_pass_fail_and_regret_bar_exact()`
- **test `test_ord_d_unresolved_routing`** [L134-140]: `def test_ord_d_unresolved_routing(na, init, ab, zc, limited)` decorators: @pytest.mark.parametrize('na,init,ab,zc,limited', [(ds(cue_mass_median=0.05), None, None, None, False), (ds(nonfinite=True), None, None, None, False), (ds(beta_W2=float('nan')), None, None, None, False), (ds(beta_W2_y=[0.6, float('nan'), 0.7]), None, None, None, False), (ds(rho_C=0.26), None, None, None, False), (ds(beta_W2=0.0, cue_mass_median=0.05), None, None, None, False), (None, plc(beta_W2=0.11), None, None, True), (None, None, plc(beta_W2=-0.2), None, True), (None, None, plc(rho_W2=0.26), None, True), (None, None, None, plc(rho_W2=0.3), True), (None, None, None, plc(beta_W2=float('nan')), True)])
- **test `test_ord_d_missing_model_fails_the_seed`** [L143-147]: `def test_ord_d_missing_model_fails_the_seed()`
- **test `test_readout_and_placebo_checks`** [L150-158]: `def test_readout_and_placebo_checks()`
- **test `test_seed_flags_and_designed_counts`** [L161-174]: `def test_seed_flags_and_designed_counts()`
- **function `ev`** [L178-193]: `def ev(**paths)`
- **test `test_decide_ordered_rules`** [L265-267]: `def test_decide_ordered_rules(over, outcome, rule)` decorators: @pytest.mark.parametrize('over,outcome,rule', RULE_CASES)
- **test `test_decide_not_run_after_first_validity_failure`** [L270-275]: `def test_decide_not_run_after_first_validity_failure()`
- **test `test_qualifiers_registered_names_order_and_designed_unresolved`** [L285-294]: `def test_qualifiers_registered_names_order_and_designed_unresolved()`
- **test `test_licence_sentences_and_designed_counts`** [L297-309]: `def test_licence_sentences_and_designed_counts()`

