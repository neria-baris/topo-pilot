# `tests/hwsg/test_a_ratio.py`

- Source: [tests/hwsg/test_a_ratio.py](../../../../../tests/hwsg/test_a_ratio.py)
- Kind: python
- Lines: 205

## Module docstring

> Author A (job 0224): capture ratio and its joint bootstrap (§2.7; N1, N7; KG7; DRG10).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 23, via sys.path edit)
- `import hwsg_ratio` -> [tools/hwsg/hwsg_ratio.py](../../tools/hwsg/hwsg_ratio.py.md) (line 24, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 25, via sys.path edit)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../../tools/k4b/k4b_fresh.py.md) (line 26, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 11)
- `pathlib` (lines 12)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`

## Imported by

- none

## Top-level constants

- `CS`
- `J`
- `N`
- `REPO`
- `SEED`
- `_CACHE`
- `_ERR`

## Classes and functions

- **function `_imports`** [L38-42]: `def _imports(monkeypatch)` decorators: @pytest.fixture(autouse=True)
- **function `_v`** [L45-46]: `def _v(x)`
- **function `_status`** [L49-54]: `def _status(fn, *a, **k)`
- **function `_fixture`** [L57-64]: `def _fixture(shift=0.0)`
- **function `_draws`** [L70-74]: `def _draws()`
- **test `test_d_key`** [L77-78]: `def test_d_key()`
- **test `test_draws_equal_joint_bootstrap_bitwise`** [L81-87]: `def test_draws_equal_joint_bootstrap_bitwise()`
- **test `test_planted_ratio_point_and_bounds`** [L90-100]: `def test_planted_ratio_point_and_bounds()`
- **test `test_ratio_draws_definition`** [L103-107]: `def test_ratio_draws_definition()`
- **test `test_seed_sensitivity`** [L110-115]: `def test_seed_sensitivity()`
- **test `test_ratio_unclipped`** [L118-126]: `def test_ratio_unclipped()`
- **function `_gate`** [L132-141]: `def _gate(tmp_path, monkeypatch, dr, b4=True, result=None)`
- **function `_lu`** [L144-146]: `def _lu(dr, j)`
- **function `_planted`** [L149-158]: `def _planted(dshift=0.0, zero_at=None)`
- **function `_ratio_status`** [L161-162]: `def _ratio_status(st, r)`
- **test `test_gate_defined`** [L165-168]: `def test_gate_defined(tmp_path, monkeypatch)`
- **test `test_gate_identity_mismatch_numerical`** [L171-179]: `def test_gate_identity_mismatch_numerical(tmp_path, monkeypatch)`
- **test `test_gate_D_rank84_nonpositive`** [L182-185]: `def test_gate_D_rank84_nonpositive(tmp_path, monkeypatch)`
- **test `test_gate_single_nonpositive_draw`** [L188-192]: `def test_gate_single_nonpositive_draw(tmp_path, monkeypatch)`
- **test `test_gate_b4_not_passed`** [L195-197]: `def test_gate_b4_not_passed(tmp_path, monkeypatch)`
- **test `test_gate_identity_real_draws`** [L200-205]: `def test_gate_identity_real_draws(tmp_path, monkeypatch)` - L, U re-derived from the real joint bootstrap equal a planted RESULT bitwise.

