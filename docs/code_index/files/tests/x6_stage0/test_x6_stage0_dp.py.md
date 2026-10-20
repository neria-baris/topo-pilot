# `tests/x6_stage0/test_x6_stage0_dp.py`

- Source: [tests/x6_stage0/test_x6_stage0_dp.py](../../../../../tests/x6_stage0/test_x6_stage0_dp.py)
- Kind: python
- Lines: 400

## Module docstring

> X6 stage 0 independent tests (X6-FROZEN-v1 section 10.4: tests 6-8, 10-12, 15-17), written
> from the protocol and API.md only; references: brute force, Fractions, ints, Decimal, hashlib,
> json and the independent helpers of test_x6_stage0.py. Stores live under pytest's tmp_path.

## Imports

### Internal (repo files)

- `from test_x6_stage0 import ANC, NB, A, C, C2, E0, comp, dec, dkl, emis, filt, labels, lam, letter, lift, mu, nbrs, w_tokens` -> [tests/x6_stage0/test_x6_stage0.py](test_x6_stage0.py.md) (line 21, via same directory)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](../../tools/x6_stage0/x6_dp.py.md) (line 25, via paired directory)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../../tools/x6_stage0/x6_exact.py.md) (line 26, via paired directory)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 27, via paired directory)
- `import x6_run` -> [tools/x6_stage0/x6_run.py](../../tools/x6_stage0/x6_run.py.md) (line 28, via paired directory)
- `from independent_reference import decimal_suffix_posterior` -> [tests/oracle_profile/independent_reference.py](../oracle_profile/independent_reference.py.md) (line 29, via unique basename)

### External (third-party)

- `pytest` (lines 18)

### Standard library

- `__future__` (lines 5)
- `collections` (lines 13)
- `decimal` (lines 14)
- `fractions` (lines 15)
- `hashlib` (lines 7)
- `inspect` (lines 8)
- `json` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 16)
- `shutil` (lines 11)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(Path(__file__).resolve().parent)` -> `tests/x6_stage0`

## Imported by

- none

## Top-level constants

- `DP_ITEMS`
- `IDX`
- `INV`
- `LADDER`

## Classes and functions

- **function `stat`** [L38-40]: `def stat(s, k)`
- **function `brute_layers`** [L42-53]: `def brute_layers(arm, n_max)`
- **function `brute_tally`** [L55-63]: `def brute_tally(start, m_max)`
- **function `layer_at`** [L65-68]: `def layer_at(arm, n)`
- **test `test_06_zc_witness_and_ab_fixed_point`** [L71-90]: `def test_06_zc_witness_and_ab_fixed_point()`
- **test `test_07_gauge_nocue_tokperm_eta1`** [L93-126]: `def test_07_gauge_nocue_tokperm_eta1()`
- **test `test_08_dp_against_brute_force`** [L129-166]: `def test_08_dp_against_brute_force()`
- **test `test_10_decimal_inputs_pass_through`** [L169-183]: `def test_10_decimal_inputs_pass_through()`
- **test `test_g5_reference_inputs_and_tolerances`** [L186-192]: `def test_g5_reference_inputs_and_tolerances()`
- **test `test_11_enclosures_certification_memo`** [L195-236]: `def test_11_enclosures_certification_memo()`
- **function `_st`** [L239-240]: `def _st(**over)`
- **test `test_12_outcome_logic`** [L243-279]: `def test_12_outcome_logic()`
- **test `test_15_indicator_se_and_rs_keys`** [L282-299]: `def test_15_indicator_se_and_rs_keys()`
- **function `put`** [L302-305]: `def put(path, data=b'x')`
- **function `sha`** [L307-308]: `def sha(path)`
- **test `test_16_rerun_and_lineage_rule`** [L311-363]: `def test_16_rerun_and_lineage_rule(tmp_path)`
- **test `test_17_eta1_markers_manifests`** [L366-400]: `def test_17_eta1_markers_manifests(tmp_path)`

