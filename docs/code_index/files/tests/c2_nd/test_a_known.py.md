# `tests/c2_nd/test_a_known.py`

- Source: [tests/c2_nd/test_a_known.py](../../../../../tests/c2_nd/test_a_known.py)
- Kind: python
- Lines: 310

## Module docstring

> Author A (job 0121): T-NEC-KNOWN (with erratum E-C2ND-1), T-RULE6, T-PROJ-ND and T-COPY.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 20, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 23, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 24, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 25, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 26, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `DD`
- `EXTRA`
- `GRD`
- `NM`
- `NO_P1`
- `NR`
- `PAT`
- `REPO`

## Classes and functions

- **function `_centre`** [L34-35]: `def _centre(v)`
- **function `_bounds`** [L38-41]: `def _bounds(arrays, j=1729, seed=630506, draws=2000)` - One shared stream (VAL level 1/60, 2,000 draws) and C2 guards with beta = 0.
- **function `_known`** [L44-66]: `def _known(psi, seed, n=2048, cancel=False)` - A readout with a known code share: outputs 0-3 read only col(B) (scale a), outputs 4-7
- **function `_run_known`** [L69-75]: `def _run_known(f, y_active=False)`
- **test `test_nec_known_categories`** [L84-91]: `def test_nec_known_categories(psi, r_cat, nr_cat)` decorators: @pytest.mark.parametrize('psi, r_cat, nr_cat', [(1.0, 'USED', 'NECESSARY'), (0.0, 'NOT_USED', 'NOT_NECESSARY'), (0.3, 'PARTIAL', 'NOT_NECESSARY'), (0.7, 'USED', 'CODE_DOMINANT')])
- **test `test_nec_known_half_share_is_neither_partial_nor_code_dominant`** [L94-100]: `def test_nec_known_half_share_is_neither_partial_nor_code_dominant()`
- **test `test_nec_known_cancellation_is_low_aligned_not_necessary`** [L103-111]: `def test_nec_known_cancellation_is_low_aligned_not_necessary()`
- **test `test_nec_known_negative_complement`** [L114-123]: `def test_nec_known_negative_complement()`
- **function `_bd`** [L131-136]: `def _bd(**cfg)`
- **function `_nr`** [L145-146]: `def _nr(y_active=True, **kw)`
- **test `test_rule6a_complement_positive_below_margin`** [L150-161]: `def test_rule6a_complement_positive_below_margin()`
- **test `test_rule6b_decoy_positive_below_margin`** [L164-174]: `def test_rule6b_decoy_positive_below_margin()`
- **test `test_nested_entry_only_inside_not_necessary`** [L177-185]: `def test_nested_entry_only_inside_not_necessary()`
- **test `test_rule6c_layer2_and_routed`** [L188-196]: `def test_rule6c_layer2_and_routed()`
- **test `test_statement_count_needs_two_models`** [L199-206]: `def test_statement_count_needs_two_models()`
- **function `_quals`** [L210-212]: `def _quals(primary, cats)`
- **test `test_proj_variant_categories_and_qualifiers`** [L215-238]: `def test_proj_variant_categories_and_qualifiers()`
- **test `test_proj_excluded_absent_and_necessary_primary`** [L241-258]: `def test_proj_excluded_absent_and_necessary_primary()`
- **function `_copy_case`** [L262-295]: `def _copy_case(kind, seed=701, n_fit=4096, n_eval=1024)`
- **test `test_copy_is_absorbed_and_used`** [L299-310]: `def test_copy_is_absorbed_and_used(kind)` decorators: @pytest.mark.parametrize('kind', ['copy_in_K', 'move_and_visible_copy', 'null_copy'])

