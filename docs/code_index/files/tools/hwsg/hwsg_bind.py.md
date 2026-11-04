# `tools/hwsg/hwsg_bind.py`

- Source: [tools/hwsg/hwsg_bind.py](../../../../../tools/hwsg/hwsg_bind.py)
- Kind: python
- Lines: 243

## Module docstring

> HWSG world rebinding and audit (API.md §2; protocol §2.3). No existing file is edited: the
> HWSB/HWSC/K4b module attributes are rebound inside `world(w)` and restored in `finally`.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 14, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../hwsc/hwsc_bind.py.md) (line 15, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 16, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 17, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 18, via unique basename)
- `from topo_pilot.dataset import checks` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 20, via package root)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 42, via same directory) (inside a function)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 43, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `contextlib` (lines 10)
- `dataclasses` (lines 7)
- `fractions` (lines 11)
- `importlib` (lines 8)
- `pathlib` (lines 12)
- `sys` (lines 9)
- `types` (lines 199)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 38: `dynamic: m`
- `import_module` line 135: `dynamic: r['module']`
- `import_module` line 142: `dynamic: m`
- `import_module` line 146: `dynamic: r['module']`

### sys.path additions

- none

## Imported by

- [tests/hwsg/test_a_kg6_port.py](../../tests/hwsg/test_a_kg6_port.py.md) (line 25, import)
- [tests/hwsg/test_impl_review.py](../../tests/hwsg/test_impl_review.py.md) (line 10, import)
- [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 7, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 7, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 6, import)
- [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 6, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 6, import)

## Top-level constants

- `ACTIVE`
- `BAD`
- `_ADAPTERS`
- `_IMPORT_VALUES`
- `_ORIG_PC`
- `_REQUIRED`
- `_ROWS`

## Classes and functions

- **function `process_code_g`** [L27-33]: `def process_code_g(*args)` - process_code accepts (family, mode, sigma, replicate); PROC_w + replicate has six fields
- **function `_values`** [L41-77]: `def _values(d, store_dir, dry_case=None) -> dict`
- **function `rows`** [L80-86]: `def rows(w, dry_case=None) -> list`
- **function `stage_c_table`** [L89-122]: `def stage_c_table(w, dry_case=None) -> list`
- **function `world`** [L126-155]: `def world(w, dry_case=None)` decorators: @contextmanager
- **class `_Forbidden`** [L159-185]
- **method `_Forbidden.__init__`** [L160-165]: `def __init__(self, f, own_floats=(), own_fractions=())`
- **method `_Forbidden.hit`** [L167-185]: `def hit(self, v)`
- **function `scope_modules`** [L188-195]: `def scope_modules() -> list`
- **function `audit`** [L198-228]: `def audit(w, modules=None, left_unchanged=None) -> dict`
- **function `check_explicit`** [L236-240]: `def check_explicit(fn_name, kwargs) -> None`

