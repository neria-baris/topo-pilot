# `tests/integration/test_rerun_identity.py`

- Source: [tests/integration/test_rerun_identity.py](../../../../../tests/integration/test_rerun_identity.py)
- Kind: python
- Lines: 24

## Module docstring

> I06: a from-scratch rerun of S1-S3 into a second store reproduces every artifact id and
> payload checksum (CPU, fixed thread count, bitwise determinism).

## Imports

### Internal (repo files)

- `import _mini_pipeline` -> [tests/integration/_mini_pipeline.py](_mini_pipeline.py.md) (line 10, via same directory)

### External (third-party)

- `pytest` (lines 7)

### Standard library

- `pathlib` (lines 5)
- `sys` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 9: `str(Path(__file__).parent)` -> `tests/integration`

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **test `test_I06_rerun_identity`** [L15-24]: `def test_I06_rerun_identity(tmp_path_factory)`

