# `src/topo_pilot/contracts/errors.py`

- Source: [src/topo_pilot/contracts/errors.py](../../../../../../src/topo_pilot/contracts/errors.py)
- Kind: python
- Lines: 105

## Module docstring

> Error codes, result statuses, and the single project exception ``StageFailure``.

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)
- `enum` (lines 6)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/__init__.py](__init__.py.md) (line 8, import)
- [src/topo_pilot/contracts/_bundle.py](_bundle.py.md) (line 17, import)
- [src/topo_pilot/contracts/_checks.py](_checks.py.md) (line 9, import)
- [src/topo_pilot/contracts/_schemas_data.py](_schemas_data.py.md) (line 13, import)
- [src/topo_pilot/contracts/_schemas_results.py](_schemas_results.py.md) (line 14, import)
- [src/topo_pilot/contracts/_schemas_world.py](_schemas_world.py.md) (line 13, import)
- [src/topo_pilot/contracts/backends.py](backends.py.md) (line 10, import)
- [src/topo_pilot/contracts/base.py](base.py.md) (line 17, import)
- [src/topo_pilot/contracts/ids.py](ids.py.md) (line 15, import)
- [src/topo_pilot/contracts/layout.py](layout.py.md) (line 9, import)
- [src/topo_pilot/contracts/store.py](store.py.md) (line 17, import)
- [src/topo_pilot/contracts/testing.py](testing.py.md) (line 13, import)
- [tools/x6_stage1/x6s1_registry.py](../../../tools/x6_stage1/x6s1_registry.py.md) (line 29, import)

## Top-level constants

- none

## Classes and functions

- **class `ErrorCode(str, Enum)`** [L10-38] - Codes carried by :class:`StageFailure`. The value equals the name.
- **class `Status(str, Enum)`** [L41-50] - Non-exception outcomes stored in results ("cannot decide" is a status, not an error).
- **class `StageFailure(Exception)`** [L54-95] decorators: @dataclass(frozen=True, eq=False) - The only exception type raised for invariant violations anywhere in the project.
- **method `StageFailure.__post_init__`** [L86-87]: `def __post_init__(self) -> None`
- **method `StageFailure.__str__`** [L89-92]: `def __str__(self) -> str`
- **method `StageFailure.__reduce__`** [L94-95]: `def __reduce__(self) -> tuple[Any, tuple[Any, ...]]`
- **function `_stage_failure_setattr`** [L98-102]: `def _stage_failure_setattr(self: StageFailure, name: str, value: Any) -> None`

