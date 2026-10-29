# `tools/hwsc/hwsc_outcome.py`

- Source: [tools/hwsc/hwsc_outcome.py](../../../../../tools/hwsc/hwsc_outcome.py)
- Kind: python
- Lines: 151

## Module docstring

> HWSC outcome precedence, POSITIVE_BELOW_MARGIN annotation and licences (API.md §6, §12;
> protocol §6.1-§6.4). Split from hwsc_gates by size (API erratum); re-exported by hwsc_gates.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 222, import)

## Top-level constants

- `ENDPOINT`
- `K4B_REASONS`
- `LIC`
- `RESOURCE`

## Classes and functions

- **function `_fr`** [L16-23]: `def _fr(x) -> Fraction`
- **function `positive_below_margin`** [L26-36]: `def positive_below_margin(per_model) -> dict`
- **function `annotations`** [L39-56]: `def annotations(result) -> list`
- **function `_ft`** [L59-60]: `def _ft(status) -> str`
- **function `outcome`** [L63-93]: `def outcome(state) -> dict`
- **function `state_from_gates`** [L96-113]: `def state_from_gates(records, l1_record=None, result=None) -> dict`
- **class `_Fill(dict)`** [L116-118]
- **method `_Fill.__missing__`** [L117-118]: `def __missing__(self, key)`
- **function `_head`** [L121-129]: `def _head(o) -> str`
- **function `licence`** [L132-151]: `def licence(oc, fill) -> str`

