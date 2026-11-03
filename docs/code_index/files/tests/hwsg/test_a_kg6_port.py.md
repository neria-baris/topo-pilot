# `tests/hwsg/test_a_kg6_port.py`

- Source: [tests/hwsg/test_a_kg6_port.py](../../../../../tests/hwsg/test_a_kg6_port.py)
- Kind: python
- Lines: 233

## Module docstring

> Author A (job 0224): KG6 port, the K4b/HWSC known statements under the hi binding (§5 KG6).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 24, via sys.path edit)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](../../tools/hwsg/hwsg_bind.py.md) (line 25, via sys.path edit)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../../tools/hwsc/hwsc_bind.py.md) (line 26, via sys.path edit)
- `import hwsc_outcome` -> [tools/hwsc/hwsc_outcome.py](../../tools/hwsc/hwsc_outcome.py.md) (line 27, via sys.path edit)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../../tools/k4b/k4b_cert.py.md) (line 28, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 29, via sys.path edit)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 30, via sys.path edit)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 13)
- `itertools` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 14)
- `random` (lines 112)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`, `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `E`
- `FEAT`
- `HI`
- `M`
- `PI`
- `REPO`
- `ROWS`
- `T`
- `_ERR`

## Classes and functions

- **function `hi`** [L39-47]: `def hi()` decorators: @pytest.fixture
- **function `_stationary`** [L62-77]: `def _stationary()`
- **function `_forward`** [L83-88]: `def _forward(obs)` - Unnormalised P(obs, z_last) from the stationary start.
- **function `_m`** [L91-96]: `def _m(obs)`
- **test `test_hmm_is_a_law`** [L106-108]: `def test_hmm_is_a_law(hi)`
- **test `test_proposition_1_suffix_only_zero`** [L111-121]: `def test_proposition_1_suffix_only_zero(hi)`
- **function `_norm`** [L124-125]: `def _norm(r)`
- **test `test_theorem_a_support_trap`** [L128-144]: `def test_theorem_a_support_trap(hi)`
- **function `_covers`** [L150-152]: `def _covers(nhat, s, B)`
- **test `test_lemma_n_covers`** [L162-167]: `def test_lemma_n_covers(hi, nhat, M32, M4)` decorators: @pytest.mark.parametrize('nhat,M32,M4', [(0.0, (0, 0), (0, 0)), (1e-300, (Fraction(1, 10 ** 40), 0), (0, 0)), (0.5, (Fraction(3, 10), Fraction(4, 10)), (0, 0)), (10.0, (Fraction(3, 10), Fraction(4, 10)), (0, 0)), (0.1414213562373095, (Fraction(1, 10), 0), (0, Fraction(1, 10)))])
- **test `test_transport_bound_planted`** [L170-178]: `def test_transport_bound_planted(hi, monkeypatch)`
- **test `test_support_equality_not_support`** [L184-188]: `def test_support_equality_not_support(hi)`
- **test `test_exclude_equality_not_exclude`** [L191-199]: `def test_exclude_equality_not_exclude(hi)`
- **test `test_support_exclude_exclusive_and_numerical`** [L202-207]: `def test_support_exclude_exclusive_and_numerical(hi)`
- **function `_pm`** [L210-211]: `def _pm(L_, F, st)`
- **test `test_positive_below_margin`** [L216-221]: `def test_positive_below_margin(hi, st, kind)` decorators: @pytest.mark.parametrize('st,kind', [('EXCLUDE', 'EXCLUDE'), ('UNRESOLVED', 'UNRESOLVED'), ('UNRESOLVED/NUMERICAL', 'UNRESOLVED'), ('SUPPORT', None)])
- **test `test_overall_on_hi_masters`** [L224-233]: `def test_overall_on_hi_masters(hi)`

