# `tests/hwsc/test_r_0184_kc7_inside_binding.py`

- Source: [tests/hwsc/test_r_0184_kc7_inside_binding.py](../../../../../tests/hwsc/test_r_0184_kc7_inside_binding.py)
- Kind: python
- Lines: 50

## Module docstring

> Coordinator-written regression test for defect D-0184-1 (API.md §26): run_kc runs every KC
> item inside the stage-C binding, and KC7 compares unbound and bound calls. Inside the binding KC7
> raised "code drift"; under hwsc_bind.suspended() it passes, and the outer binding is re-applied
> afterwards and removed at its exit.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../../tools/hwsc/hwsc_config.py.md) (line 17, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 18, via sys.path edit)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../../tools/hwsc/hwsc_known.py.md) (line 19, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 20, via unique basename)

### External (third-party)

- `pytest` (lines 12)

### Standard library

- `__future__` (lines 6)
- `importlib` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 24: `dynamic: r['module']`

### sys.path additions

- line 15: `str(REPO / 'tools' / 'hwsc')` -> `tools/hwsc`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `_values`** [L23-24]: `def _values(rows)`
- **test `test_kc7_inside_the_binding_needs_suspension`** [L27-30]: `def test_kc7_inside_the_binding_needs_suspension()`
- **test `test_kc7_passes_under_suspended_and_the_binding_is_reapplied`** [L33-45]: `def test_kc7_passes_under_suspended_and_the_binding_is_reapplied()`
- **test `test_suspended_outside_a_binding_is_a_no_op`** [L48-50]: `def test_suspended_outside_a_binding_is_a_no_op()`

