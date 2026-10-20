# `tests/c1prime/test_c_process_keys.py`

- Source: [tests/c1prime/test_c_process_keys.py](../../../../../tests/c1prime/test_c_process_keys.py)
- Kind: python
- Lines: 46

## Module docstring

> Coordinator regression test (job 0039 review, ruling R11): `c1_driver._process` must return
> `E_named` keyed by int model ids like `canon` and `perm`. The reused job-0014
> `inputs.load_process` keys it by the config's emission keys, which are strings ('1729', ...),
> and H3's named-order check indexes it with int MODELS (the KeyError: 1729 of job 0039).
> Synthetic: `inputs` is replaced by a stub, so no artifact is read.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 21, via sys.path edit)
- `import c1_driver` -> [tools/c1prime/c1_driver.py](../../tools/c1prime/c1_driver.py.md) (line 22, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 7)
- `pathlib` (lines 11)
- `sys` (lines 9)
- `types` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / _sub)` -> `tests/oracle_profile`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **test `test_process_rekeys_e_named_to_int`** [L25-46]: `def test_process_rekeys_e_named_to_int(monkeypatch)`

