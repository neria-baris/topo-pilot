# `tests/hwsu/test_a_u2_p1.py`

- Source: [tests/hwsu/test_a_u2_p1.py](../../../../../tests/hwsu/test_a_u2_p1.py)
- Kind: python
- Lines: 159

## Module docstring

> Author A (job 0223): P1 precision ladder and its blindness (protocol 2.9; API_U2 4.2; DRU5).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 15, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 16, via unique basename)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 17, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 18, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](../../tools/hwsu/u2/__init__.py.md) (line 29, via sys.path edit) (inside a function)

### External (third-party)

- `numpy` (lines 19)
- `pytest` (lines 20)

### Standard library

- `__future__` (lines 6)
- `importlib` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 31: `dynamic: name`

### sys.path additions

- line 13: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `ALL`
- `LAD`
- `MASTERS`
- `NONE`
- `REPO`
- `SEEDS`
- `TWO`

## Classes and functions

- **function `mod`** [L28-31]: `def mod(name)`
- **function `_data`** [L34-38]: `def _data(noise, seed=31)`
- **function `hand`** [L41-61]: `def hand(A, G, ladder=LAD)`
- **function `_p1`** [L64-65]: `def _p1(A, G, ladder=LAD)`
- **function `_norm_passes`** [L68-70]: `def _norm_passes(p)`
- **test `test_all_pass_smallest_N`** [L79-88]: `def test_all_pass_smallest_N()`
- **test `test_two_pass_fallback_precision_limited`** [L91-98]: `def test_two_pass_fallback_precision_limited()`
- **test `test_underpowered`** [L101-110]: `def test_underpowered()`
- **test `test_blindness_constant_shift_of_A`** [L113-119]: `def test_blindness_constant_shift_of_A()` - Adding a constant to every A_j changes mean A_full only: N and passes are identical.
- **test `test_seeds_alt_and_r4n_used`** [L122-150]: `def test_seeds_alt_and_r4n_used(monkeypatch)`
- **test `test_seed_sensitive`** [L153-159]: `def test_seed_sensitive()` - Different seeds change the draws (a borderline fixture would change N): the seeds matter.

