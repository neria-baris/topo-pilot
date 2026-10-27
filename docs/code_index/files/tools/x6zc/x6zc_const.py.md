# `tools/x6zc/x6zc_const.py`

- Source: [tools/x6zc/x6zc_const.py](../../../../../tools/x6zc/x6zc_const.py)
- Kind: python
- Lines: 66

## Module docstring

> X6ZC constants: CONTRACT loading, names and bindings, streams (X6ZC-DESIGN-v1; API.md
> §3, §20 C-52). Re-exported by x6zc_core. Import reads CONTRACT.json and the protocol only.

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 18, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 22, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `hashlib` (lines 7)
- `json` (lines 8)
- `pathlib` (lines 11)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(_p)` -> `tools/x6_stage1`, `tools/x6zc`

## Imported by

- [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 21, import)
- [tools/x6zc/x6zc_decide.py](x6zc_decide.py.md) (line 12, import)

## Top-level constants

- `ANSWERS`
- `CELLS`
- `CONTRACT`
- `HERE`
- `REPO`
- `T`
- `VARIANTS`
- `W1_CROSS_STEPS`
- `_MISS`

## Classes and functions

- **function `load_contract`** [L28-32]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `frac`** [L33-33]: `def frac(s) -> Fraction`
- **function `stream`** [L61-62]: `def stream(name) -> np.random.Generator`
- **function `dry_stream`** [L63-64]: `def dry_stream(*names) -> np.random.Generator`
- **function `_fl`** [L65-65]: `def _fl(x) -> float`
- **function `_ints`** [L66-66]: `def _ints(row) -> tuple`

