# `tests/hwsd/test_a_evaluate.py`

- Source: [tests/hwsd/test_a_evaluate.py](../../../../../tests/hwsd/test_a_evaluate.py)
- Kind: python
- Lines: 188

## Module docstring

> Author A (job 0197): evaluate, diagnostics, reading texts and the outcome precedence.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](../../tools/hwsd/hwsd_config.py.md) (line 20, via sys.path edit)
- `import hwsd_statements` -> [tools/hwsd/hwsd_statements.py](../../tools/hwsd/hwsd_statements.py.md) (line 21, via sys.path edit)
- `import hwsd_summary` -> [tools/hwsd/hwsd_summary.py](../../tools/hwsd/hwsd_summary.py.md) (line 22, via sys.path edit)
- `import test_a_hwsd_ref` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 23, via same directory)
- `from test_a_hwsd_ref import EXC, NOC, SC, SU, SUP, UC, UNR, UNV, row, seq` -> [tests/hwsd/test_a_hwsd_ref.py](test_a_hwsd_ref.py.md) (line 24, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 11)
- `pathlib` (lines 12)
- `re` (lines 9)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `_p` -> `tests/hwsd`, `tools/hwsd`

## Imported by

- none

## Top-level constants

- `AFTER`
- `HERE`
- `J`
- `NE`
- `REPO`

## Classes and functions

- **function `table`** [L30-31]: `def table(*rows_per_model)`
- **function `category`** [L34-35]: `def category(v)`
- **function `strings`** [L38-46]: `def strings(obj)`
- **test `test_evaluate_structure_and_values`** [L52-71]: `def test_evaluate_structure_and_values()`
- **test `test_evaluate_headroom_and_resource`** [L74-89]: `def test_evaluate_headroom_and_resource()`
- **test `test_evaluate_any_sequence_length`** [L92-96]: `def test_evaluate_any_sequence_length()`
- **test `test_diagnostics_mc_positive`** [L99-108]: `def test_diagnostics_mc_positive()`
- **test `test_diagnostics_chart_at_init_rc4`** [L111-120]: `def test_diagnostics_chart_at_init_rc4()`
- **test `test_diagnostics_est_loss_only_unvalidated_k1`** [L123-127]: `def test_diagnostics_est_loss_only_unvalidated_k1()`
- **test `test_fill_templates_texts`** [L130-138]: `def test_fill_templates_texts()`
- **test `test_fill_templates_d4_second_sentence_and_d3_chart_at_init`** [L141-149]: `def test_fill_templates_d4_second_sentence_and_d3_chart_at_init()`
- **test `test_fill_templates_missing_field_reads_n_a`** [L152-158]: `def test_fill_templates_missing_field_reads_n_a(monkeypatch)`
- **test `test_outcome_precedence`** [L161-174]: `def test_outcome_precedence()`
- **test `test_order_categories_reachable_in_evaluate`** [L177-188]: `def test_order_categories_reachable_in_evaluate()`

