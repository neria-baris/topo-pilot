# `tests/d2a/test_a_templates.py`

- Source: [tests/d2a/test_a_templates.py](../../../../../tests/d2a/test_a_templates.py)
- Kind: python
- Lines: 155

## Module docstring

> Independent tests of the equal-gap templates in tools/d2a (job 0028, author A): T-TPL.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 18, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 25, via sys.path edit)
- `import d2a_targets` -> [tools/d2a/d2a_targets.py](../../tools/d2a/d2a_targets.py.md) (line 26, via sys.path edit)
- `import d2a_world` -> [tools/d2a/d2a_world.py](../../tools/d2a/d2a_world.py.md) (line 27, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 12)
- `hashlib` (lines 10)
- `itertools` (lines 13)
- `pathlib` (lines 14)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO_ROOT.joinpath(*_parts))` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `DATA`
- `HAND`
- `Q1_DECISION`
- `REPO_ROOT`
- `Y_LAW`

## Classes and functions

- **function `_member`** [L37-45]: `def _member(r1, x5, r9, exc, j)`
- **function `_my_enumeration`** [L48-52]: `def _my_enumeration(t)`
- **function `_pairs`** [L66-67]: `def _pairs(t)`
- **test `test_T_TPL_counts`** [L70-73]: `def test_T_TPL_counts()`
- **test `test_T_TPL_enumeration_order_follows_api`** [L77-81]: `def test_T_TPL_enumeration_order_follows_api(t)` decorators: @pytest.mark.parametrize('t', [16, 28])
- **test `test_T_TPL_structure_of_every_pair`** [L85-92]: `def test_T_TPL_structure_of_every_pair(t)` decorators: @pytest.mark.parametrize('t', [16, 28])
- **test `test_T_TPL_exact_identities_at_hand_template`** [L96-106]: `def test_T_TPL_exact_identities_at_hand_template(t)` decorators: @pytest.mark.parametrize('t', [16, 28])
- **test `test_T_TPL_canonical_pair_windows_differ_and_are_not_required_equal`** [L109-117]: `def test_T_TPL_canonical_pair_windows_differ_and_are_not_required_equal()`
- **test `test_T_TPL_registered_templates`** [L120-127]: `def test_T_TPL_registered_templates()`
- **test `test_template_hashes`** [L131-137]: `def test_template_hashes(t)` decorators: @pytest.mark.parametrize('t', [16, 28])
- **test `test_registered_templates_exact_g0_tpl_sample`** [L140-149]: `def test_registered_templates_exact_g0_tpl_sample()` - Every 32nd registered t = 28 pair and every 8th t = 16 pair, exactly (G0-TPL values).
- **test `test_g0_tpl_gate_passes`** [L152-155]: `def test_g0_tpl_gate_passes()`

