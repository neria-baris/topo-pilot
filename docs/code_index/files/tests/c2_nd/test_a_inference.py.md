# `tests/c2_nd/test_a_inference.py`

- Source: [tests/c2_nd/test_a_inference.py](../../../../../tests/c2_nd/test_a_inference.py)
- Kind: python
- Lines: 361

## Module docstring

> Author A (job 0121): T-RULES-ND, T-BOOT-ND and T-LADDER-ND.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 21, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 24, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 25, via unique basename)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 26, via sys.path edit)
- `import nd_stage_val` -> [tools/c2_nd/nd_stage_val.py](../../tools/c2_nd/nd_stage_val.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `math` (lines 10)
- `pathlib` (lines 13)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `DD`
- `DISCLOSE`
- `KM3`
- `MODELS`
- `NM`
- `NR`
- `PAT`
- `QD1`
- `QD3`
- `QN`
- `QN2`
- `REPO`

## Classes and functions

- **function `_bd`** [L33-35]: `def _bd(**cfg)`
- **function `_o`** [L44-45]: `def _o(family, a, b, c, cnhs=(), kc=False)`
- **test `test_rules_nr_overall`** [L49-61]: `def test_rules_nr_overall()`
- **test `test_rules_d_overall`** [L64-75]: `def test_rules_d_overall()`
- **test `test_rules_nm_overall`** [L78-86]: `def test_rules_nm_overall()`
- **function `_rec`** [L89-91]: `def _rec(gate, full, model=None, family=None, problem=None, decoy=None, values=None)`
- **test `test_rules_endpoint_status`** [L94-105]: `def test_rules_endpoint_status()`
- **test `test_rules_qualifier_order`** [L108-131]: `def test_rules_qualifier_order()`
- **test `test_licences_carry_the_sentences_and_qcode`** [L151-178]: `def test_licences_carry_the_sentences_and_qcode()`
- **test `test_statement_licences`** [L181-190]: `def test_statement_licences()`
- **test `test_package_statement_caveat_and_unions`** [L193-219]: `def test_package_statement_caveat_and_unions()`
- **test `test_boot_shared_index_streams`** [L223-241]: `def test_boot_shared_index_streams()`
- **test `test_boot_fraction_ranks_and_contract`** [L244-255]: `def test_boot_fraction_ranks_and_contract()`
- **test `test_boot_indicator_form_sign`** [L258-266]: `def test_boot_indicator_form_sign()`
- **test `test_boot_ratio_intervals_undefined_and_no_draw_discarded`** [L269-289]: `def test_boot_ratio_intervals_undefined_and_no_draw_discarded()`
- **class `_FakePrecision`** [L293-320] - Records the kernel calls; precision_summary passes model j at N iff (name, N, j) in ok.
- **method `_FakePrecision.__init__`** [L296-297]: `def __init__(self, arrays, ok)`
- **method `_FakePrecision._name`** [L299-301]: `def _name(self, X)`
- **method `_FakePrecision.sd_b4_draws`** [L303-306]: `def sd_b4_draws(self, X, r4n, models, seed, draws, size)`
- **method `_FakePrecision.centered_draws`** [L308-310]: `def centered_draws(self, X, models, seed, draws, size)`
- **method `_FakePrecision.precision_summary`** [L312-320]: `def precision_summary(self, sd, e, models, cfg)`
- **function `_ladder`** [L323-345]: `def _ladder(monkeypatch, family, names, ok_fn)`
- **test `test_ladder_nr_all_pass_at_first_rung`** [L348-351]: `def test_ladder_nr_all_pass_at_first_rung(monkeypatch)`
- **test `test_ladder_two_of_three_and_underpowered`** [L354-361]: `def test_ladder_two_of_three_and_underpowered(monkeypatch)`

