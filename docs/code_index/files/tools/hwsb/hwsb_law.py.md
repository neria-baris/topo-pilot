# `tools/hwsb/hwsb_law.py`

- Source: [tools/hwsb/hwsb_law.py](../../../../../tools/hwsb/hwsb_law.py)
- Kind: python
- Lines: 169

## Module docstring

> HWSB law enclosure for non-terminating logits (API.md §5; protocol §4 B8a, RC-1, OPEN-3).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 14, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 20, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../x4_circle_history/process_law.py.md) (line 21, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 12)
- `contextlib` (lines 15)
- `decimal` (lines 16, 17)
- `fractions` (lines 18)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `from errors import Invalid` (line 22): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_a_enclosure_proof.py](../../tests/hwsb/test_a_enclosure_proof.py.md) (line 40, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 24, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 20, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 18, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 19, import)

## Top-level constants

- `CHECK_DIGITS`
- `DIGITS`
- `SLACK`

## Classes and functions

- **function `centres`** [L29-31]: `def centres() -> list`
- **function `exact_logits`** [L34-47]: `def exact_logits(states) -> list` - q[s][j] = -d^2/(2 sigma^2) as exact Fractions (process_law.py:112-115).
- **function `rounded_logits`** [L50-52]: `def rounded_logits(q_rows, digits=DIGITS) -> list`
- **function `_delta`** [L55-64]: `def _delta(q_rows, qt_rows, digits) -> dict`
- **function `rounding_delta`** [L67-69]: `def rounding_delta(states, digits=DIGITS) -> dict`
- **function `softmax_enclosure_rounded`** [L72-95]: `def softmax_enclosure_rounded(states, digits=DIGITS)` - (E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (ENCLOSURE_PROOF).
- **function `bound_law`** [L99-109]: `def bound_law(sigma, neighbour)` decorators: @contextlib.contextmanager - Bind LAW sigma/neighbour and the rounded enclosure; restore all three in finally.
- **function `_exact`** [L112-117]: `def _exact(rep)`
- **function `law_bound`** [L120-140]: `def law_bound(T, E, pi, coords, sigma=hc.SIGMA, neighbour=hc.NEIGHBOUR) -> dict` - process_law_bound (unchanged) under the rounded enclosure; exceptions propagate.
- **function `reference_entry`** [L143-150]: `def reference_entry(q_row, j, digits=CHECK_DIGITS) -> Decimal` - Independent softmax entry from the exact logits at `digits` digits.
- **function `decimal_check`** [L153-169]: `def decimal_check(states, enclosure, entries, digits=CHECK_DIGITS) -> dict`

