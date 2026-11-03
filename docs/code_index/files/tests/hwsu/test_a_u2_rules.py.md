# `tests/hwsu/test_a_u2_rules.py`

- Source: [tests/hwsu/test_a_u2_rules.py](../../../../../tests/hwsu/test_a_u2_rules.py)
- Kind: python
- Lines: 142

## Module docstring

> Author A (job 0223): per-model response statements (protocol 2.9 table; API_U2 4.4 model_status).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 17, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 18, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 25, via sys.path edit) (inside a function)

### External (third-party)

- `pytest` (lines 19)

### Standard library

- `__future__` (lines 7)
- `importlib` (lines 9)
- `pathlib` (lines 12)
- `re` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 27: `dynamic: name`

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `G`
- `REPO`

## Classes and functions

- **function `mod`** [L24-27]: `def mod(name)`
- **function `norm`** [L30-31]: `def norm(s)`
- **function `bj`** [L34-41]: `def bj(l1, u1, l3, u3, laf=None, uaf=None, g=G)`
- **function `status`** [L44-45]: `def status(b)`
- **test `test_responds`** [L48-49]: `def test_responds()`
- **test `test_weak_response`** [L52-53]: `def test_weak_response()`
- **test `test_low_response`** [L56-57]: `def test_low_response()`
- **test `test_low_response_reachable_with_negative_theta`** [L60-64]: `def test_low_response_reachable_with_negative_theta()`
- **test `test_inconclusive_when_no_row_holds`** [L67-69]: `def test_inconclusive_when_no_row_holds()`
- **test `test_bound_exactly_at_guard_is_neither_sign`** [L73-78]: `def test_bound_exactly_at_guard_is_neither_sign(edge)` decorators: @pytest.mark.parametrize('edge', [G, -G])
- **function `_expected`** [L81-85]: `def _expected(b)`
- **test `test_mean_exactly_at_line_never_declared`** [L88-91]: `def test_mean_exactly_at_line_never_declared()`
- **test `test_grid_agrees_with_category_mapping`** [L94-103]: `def test_grid_agrees_with_category_mapping()`
- **test `test_rule6`** [L110-112]: `def test_rule6(laf, u3, want)` decorators: @pytest.mark.parametrize('laf,u3,want', [(0.2, -0.2, True), (G, -0.2, False), (0.2, -G, False), (-0.1, -0.2, False), (0.2, 0.1, False)])
- **test `test_rule6_with_weak_response`** [L115-117]: `def test_rule6_with_weak_response()`
- **test `test_rule6_not_with_responds`** [L120-122]: `def test_rule6_not_with_responds()`
- **function `_coarse`** [L125-126]: `def _coarse(r)`
- **test `test_coarse_statements`** [L129-136]: `def test_coarse_statements()`
- **test `test_bounds_returned`** [L139-142]: `def test_bounds_returned()`

