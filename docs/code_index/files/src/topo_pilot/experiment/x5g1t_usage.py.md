# `src/topo_pilot/experiment/x5g1t_usage.py`

- Source: [src/topo_pilot/experiment/x5g1t_usage.py](../../../../../../src/topo_pilot/experiment/x5g1t_usage.py)
- Kind: python
- Lines: 177

## Module docstring

> Worker self-hold latch from actual usage evidence (x5g1-train-v4 §8; API v4 §1).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `datetime` (lines 16)
- `json` (lines 12)
- `math` (lines 13)
- `os` (lines 14)
- `pathlib` (lines 17)
- `re` (lines 15)
- `typing` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_main.py](x5g1t_main.py.md) (line 31, import)
- [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 25, import)
- [tests/experiment/test_x5g1t_usage.py](../../../tests/experiment/test_x5g1t_usage.py.md) (line 17, import)
- [tests/experiment/test_x5g1t_usage_files.py](../../../tests/experiment/test_x5g1t_usage_files.py.md) (line 18, import)

## Top-level constants

- `LATCH_NAME`
- `LATCH_SCHEMA`
- `THRESHOLD_PERCENT`
- `USAGE_NAME`
- `_TS`

## Classes and functions

- **class `UsageMalformed(ValueError)`** [L27-28] - Malformed usage evidence or latch; callers treat it as STOP (fail closed).
- **class `UsageDecision(NamedTuple)`** [L31-35]
- **function `parse_utc`** [L38-51]: `def parse_utc(text) -> datetime` - ISO 8601 with ``Z`` or ``+hh:mm`` and 0-7 fractional digits -> aware UTC datetime.
- **function `_limits`** [L54-71]: `def _limits(usage) -> list[dict]`
- **function `blocking_limits`** [L74-81]: `def blocking_limits(usage, threshold: float = THRESHOLD_PERCENT) -> list[dict]` - Relevant limits with a warning (any observability) or, when OBSERVED, used >= threshold.
- **function `make_latch`** [L84-88]: `def make_latch(blocking: list[dict], source, now: datetime) -> dict`
- **function `_check_latch`** [L91-98]: `def _check_latch(latch) -> datetime`
- **function `latch_clears`** [L101-121]: `def latch_clears(latch, usage, threshold: float = THRESHOLD_PERCENT) -> tuple[bool, str]` - True only on new OBSERVED evidence clearing every latched limit (see module doc).
- **function `usage_decision`** [L124-143]: `def usage_decision(usage, latch, now: datetime, threshold: float = THRESHOLD_PERCENT) -> UsageDecision`
- **function `_read`** [L146-155]: `def _read(path: Path)`
- **function `_write`** [L158-161]: `def _write(path: Path, obj) -> None`
- **function `apply_usage`** [L164-177]: `def apply_usage(mailbox: Path, now: datetime | None = None) -> tuple[str, tuple[str, ...]]` - Read evidence and latch, apply the decision (set or archive the latch atomically).

