# `tools/c1prime/materialise_protocol.py`

- Source: [tools/c1prime/materialise_protocol.py](../../../../../tools/c1prime/materialise_protocol.py)
- Kind: python
- Lines: 112

## Module docstring

> Materialise C1'-v1 = C1-FROZEN-v1 + the 33 anchored edits of C1PRIME-DELTA-FROZEN-v1 (job 0026).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `hashlib` (lines 12)
- `pathlib` (lines 15)
- `re` (lines 13)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `BASE_SHA`
- `DELTA_SHA`
- `OPS`

## Classes and functions

- **function `sha`** [L29-30]: `def sha(b: bytes) -> str`
- **function `parse`** [L33-40]: `def parse(delta: str) -> dict`
- **function `_line_span`** [L43-47]: `def _line_span(text: str, anchor: str) -> tuple[int, int]`
- **function `apply`** [L50-82]: `def apply(text: str, n: int, fences: list) -> str`
- **function `main`** [L85-108]: `def main(resp_dir: Path, out: Path) -> dict`

