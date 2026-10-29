# `tools/hwsc/hwsc_bind.py`

- Source: [tools/hwsc/hwsc_bind.py](../../../../../tools/hwsc/hwsc_bind.py)
- Kind: python
- Lines: 246

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

- `import_module` line 63: `dynamic: r['module']`
- `import_module` line 92: `dynamic: r['module']`
- `import_module` line 120: `dynamic: r['module']`

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
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 14, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 21, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 14, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 13, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 15, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 18, import)

## Top-level constants

- `ACTIVE`
- `BINDING`

## Classes and functions

- **class `_ContractMarker`** [L25-30]
- **method `_ContractMarker.__init__`** [L26-27]: `def __init__(self, sha)`
- **method `_ContractMarker.matches`** [L29-30]: `def matches(self, value) -> bool`
- **function `decode`** [L33-48]: `def decode(value, repo=cc.REPO)`
- **function `_rows`** [L51-52]: `def _rows(contract) -> list`
- **function `load_table`** [L55-78]: `def load_table(contract=None, which='stage_c', case=None, case_dir=None) -> list`
- **function `_same`** [L81-86]: `def _same(cur, old) -> bool`
- **function `check_old`** [L89-95]: `def check_old(rows) -> list`
- **function `_encode`** [L98-107]: `def _encode(v)`
- **function `bound_stage_c`** [L111-130]: `def bound_stage_c(table=None)` decorators: @contextmanager
- **function `never_called`** [L133-134]: `def never_called() -> tuple`
- **function `_norm`** [L138-139]: `def _norm(p) -> str`
- **class `_Forbidden`** [L142-172]
- **method `_Forbidden.__init__`** [L143-147]: `def __init__(self, f)`
- **method `_Forbidden.hit`** [L149-172]: `def hit(self, v)`
- **function `_walk`** [L175-194]: `def _walk(v, where, forb, out, depth=0, seen=None)`
- **function `_functions`** [L197-205]: `def _functions(mod)`
- **function `scope_modules`** [L208-218]: `def scope_modules() -> list`
- **function `audit`** [L221-246]: `def audit(modules=None, left_unchanged=None, forbidden=None) -> dict`

