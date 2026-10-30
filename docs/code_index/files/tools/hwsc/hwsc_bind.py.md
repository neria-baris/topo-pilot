# `tools/hwsc/hwsc_bind.py`

- Source: [tools/hwsc/hwsc_bind.py](../../../../../tools/hwsc/hwsc_bind.py)
- Kind: python
- Lines: 272

## Module docstring

> HWSC versioned binding: the binding table, bound_stage_c() and the binding audit (API.md §2;
> protocol §3.1-§3.2, RC-1). No existing file is edited: K4b/HWSB module attributes are rebound
> for the duration of a `with` block and restored in `finally`.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 19, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `contextlib` (lines 16)
- `copy` (lines 8)
- `dataclasses` (lines 9)
- `hashlib` (lines 10)
- `importlib` (lines 11)
- `inspect` (lines 12)
- `json` (lines 13)
- `pathlib` (lines 17)
- `sys` (lines 14)
- `types` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 64: `dynamic: r['module']`
- `import_module` line 93: `dynamic: r['module']`
- `import_module` line 121: `dynamic: r['module']`

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_a_decision.py](../../tests/hwsc/test_a_decision.py.md) (line 25, import)
- [tests/hwsc/test_a_k4b_known_bound.py](../../tests/hwsc/test_a_k4b_known_bound.py.md) (line 31, import)
- [tests/hwsc/test_a_ladder.py](../../tests/hwsc/test_a_ladder.py.md) (line 24, import)
- [tests/hwsc/test_a_outcomes.py](../../tests/hwsc/test_a_outcomes.py.md) (line 23, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 25, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 27, import)
- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 25, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 23, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 25, import)
- [tests/hwsc/test_r_0184_kc7_inside_binding.py](../../tests/hwsc/test_r_0184_kc7_inside_binding.py.md) (line 18, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 14, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 21, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 14, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 13, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 15, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 18, import)

## Top-level constants

- `ACTIVE`
- `BINDING`
- `_STACK`

## Classes and functions

- **class `_ContractMarker`** [L26-31]
- **method `_ContractMarker.__init__`** [L27-28]: `def __init__(self, sha)`
- **method `_ContractMarker.matches`** [L30-31]: `def matches(self, value) -> bool`
- **function `decode`** [L34-49]: `def decode(value, repo=cc.REPO)`
- **function `_rows`** [L52-53]: `def _rows(contract) -> list`
- **function `load_table`** [L56-79]: `def load_table(contract=None, which='stage_c', case=None, case_dir=None) -> list`
- **function `_same`** [L82-87]: `def _same(cur, old) -> bool`
- **function `check_old`** [L90-96]: `def check_old(rows) -> list`
- **function `_encode`** [L99-108]: `def _encode(v)`
- **function `bound_stage_c`** [L112-134]: `def bound_stage_c(table=None)` decorators: @contextmanager
- **function `suspended`** [L138-156]: `def suspended()` decorators: @contextmanager - Unbound for the block inside an active bound_stage_c, re-bound after (D-0184-1: KC7
- **function `never_called`** [L159-160]: `def never_called() -> tuple`
- **function `_norm`** [L164-165]: `def _norm(p) -> str`
- **class `_Forbidden`** [L168-198]
- **method `_Forbidden.__init__`** [L169-173]: `def __init__(self, f)`
- **method `_Forbidden.hit`** [L175-198]: `def hit(self, v)`
- **function `_walk`** [L201-220]: `def _walk(v, where, forb, out, depth=0, seen=None)`
- **function `_functions`** [L223-231]: `def _functions(mod)`
- **function `scope_modules`** [L234-244]: `def scope_modules() -> list`
- **function `audit`** [L247-272]: `def audit(modules=None, left_unchanged=None, forbidden=None) -> dict`

