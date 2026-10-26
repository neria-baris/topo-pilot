# `tests/c2_readout/test_a_inference.py`

- Source: [tests/c2_readout/test_a_inference.py](../../../../../tests/c2_readout/test_a_inference.py)
- Kind: python
- Lines: 376

## Module docstring

> Independent tests, author A (job 0101): T-FAMILY (Lemma FW, FW-M), T-RULES (RC-8, RC-13,
> NEW-6) and T-BOOT (shared index stream, Fraction ranks) (C2-FROZEN-v1 3, 5.7, 6.2-6.5, 13.3).
> The C2-M descriptive stream of T-BOOT is in test_a_partition.py, T-LADDER in test_a_gls.py.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 31, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 32, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 33, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 34, via sys.path edit)

### External (third-party)

- `numpy` (lines 24)
- `pytest` (lines 25)

### Standard library

- `__future__` (lines 16)
- `fractions` (lines 21)
- `itertools` (lines 18)
- `math` (lines 19)
- `pathlib` (lines 22)
- `sys` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 29: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `CASES`
- `FAILS`
- `G`
- `ORDER`
- `OVERALL`
- `PAIRS`
- `REPO`
- `SIG`
- `VALUES`

## Classes and functions

- **function `_bd`** [L47-49]: `def _bd(L, U)`
- **function `_sg`** [L52-53]: `def _sg(x)`
- **function `_coarse`** [L56-58]: `def _coarse(out)`
- **function `_occ`** [L61-63]: `def _occ(b, ev, mu)`
- **function `_cat_events`** [L66-74]: `def _cat_events(psi, mu, z1, z5, energy)`
- **function `_expect_r`** [L78-91]: `def _expect_r(b, y_active)`
- **function `_r_patterns`** [L94-99]: `def _r_patterns()`
- **test `test_lemma_fw_r_exhaustive_grid`** [L102-150]: `def test_lemma_fw_r_exhaustive_grid()`
- **test `test_equality_and_guard_are_never_declared`** [L153-160]: `def test_equality_and_guard_are_never_declared()`
- **function `_expect_m`** [L164-181]: `def _expect_m(b, y2)`
- **test `test_lemma_fw_m_exhaustive_grid`** [L184-222]: `def test_lemma_fw_m_exhaustive_grid()`
- **test `test_overall_two_of_three_rules`** [L254-255]: `def test_overall_two_of_three_rules(fam, sts, cnhs, expect)` decorators: @pytest.mark.parametrize('fam, sts, cnhs, expect', OVERALL)
- **function `_history`** [L268-279]: `def _history(fail=None, model=None, family=None, scope='model')` - GATES.jsonl-style records (API.md 15.1): every gate PASS except `fail`; after a study
- **test `test_endpoint_status_new6`** [L296-303]: `def test_endpoint_status_new6(fail, model, family, scope, who, expect)` decorators: @pytest.mark.parametrize('fail, model, family, scope, who, expect', CASES)
- **test `test_post_desc_values_are_labelled_unlicensed_point_ratios`** [L306-319]: `def test_post_desc_values_are_labelled_unlicensed_point_ratios()`
- **test `test_qualifiers_order_dissent_and_licence_texts`** [L322-344]: `def test_qualifiers_order_dissent_and_licence_texts()`
- **test `test_shared_index_stream_resp_spec_first_then_endpoint`** [L348-362]: `def test_shared_index_stream_resp_spec_first_then_endpoint()`
- **test `test_fraction_ranks`** [L368-376]: `def test_fraction_ranks(draws, alpha, ranks)` decorators: @pytest.mark.parametrize('draws, alpha, ranks', [(20000, Fr(1, 240), (84, 19917)), (20000, Fr(1, 360), (56, 19945)), (5000, Fr(1, 60), (84, 4917))])

