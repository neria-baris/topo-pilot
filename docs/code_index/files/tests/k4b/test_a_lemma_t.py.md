# `tests/k4b/test_a_lemma_t.py`

- Source: [tests/k4b/test_a_lemma_t.py](../../../../../tests/k4b/test_a_lemma_t.py)
- Kind: python
- Lines: 171

## Module docstring

> K4b author A, TEST_PLAN A4 (protocol §1.3, CERTIFICATE §2): Lemma T on an exact toy.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `pytest` (lines 17)

### Standard library

- `__future__` (lines 9)
- `fractions` (lines 12)
- `functools` (lines 13)
- `itertools` (lines 14)
- `pathlib` (lines 15)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `C`
- `E_OP`
- `E_STAR`
- `KAPPA`
- `PI_OP`
- `PI_STAR`
- `REPO`
- `RHO`
- `T_OP`
- `T_STAR`
- `UNITS`

## Classes and functions

- **function `forward`** [L42-47]: `def forward(law, obs)`
- **function `normalise`** [L50-52]: `def normalise(a)`
- **function `mean_of`** [L55-56]: `def mean_of(post)`
- **function `history_law`** [L60-68]: `def history_law(law)` decorators: @lru_cache(maxsize=None) - {w: (P(w), full posterior, suffix posterior restarted at pi, r = m_L - m_K)}.
- **function `path_prob`** [L71-76]: `def path_prob(law, z, w)`
- **function `l1`** [L79-80]: `def l1(a, b)`
- **function `tv_histories`** [L83-85]: `def tv_histories()`
- **function `z_bound`** [L88-89]: `def z_bound()`
- **test `test_kappa_is_known_exactly`** [L92-101]: `def test_kappa_is_known_exactly()`
- **test `test_path_law_l1_within_rho`** [L104-112]: `def test_path_law_l1_within_rho()`
- **test `test_posteriors_within_rho`** [L115-119]: `def test_posteriors_within_rho()`
- **test `test_residual_difference_within_two_rho`** [L122-128]: `def test_residual_difference_within_two_rho()`
- **function `_fields`** [L131-138]: `def _fields()` - Scores f(h, r): 1-Lipschitz in r (Euclidean) and |f(h, r)| <= |r|.
- **test `test_lemma_t_transport_bound`** [L142-147]: `def test_lemma_t_transport_bound(idx)` decorators: @pytest.mark.parametrize('idx', range(len(_fields())))
- **test `test_lemma_t_is_not_vacuous`** [L150-161]: `def test_lemma_t_is_not_vacuous()`
- **test `test_zero_perturbation_gives_zero_bound_and_zero_gap`** [L164-171]: `def test_zero_perturbation_gives_zero_bound_and_zero_gap()`

