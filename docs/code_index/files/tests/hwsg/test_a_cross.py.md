# `tests/hwsg/test_a_cross.py`

- Source: [tests/hwsg/test_a_cross.py](../../../../../tests/hwsg/test_a_cross.py)
- Kind: python
- Lines: 278

## Module docstring

> Author A (job 0224): CROSS decision table and RC-1 boundaries (§2.7, §7.3; DRG7/10/14).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](../../tools/hwsg/hwsg_config.py.md) (line 22, via sys.path edit)
- `import hwsg_cross` -> [tools/hwsg/hwsg_cross.py](../../tools/hwsg/hwsg_cross.py.md) (line 23, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 7)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / _d)` -> `tools/c1prime`, `tools/hwsb`, `tools/hwsc`, `tools/hwsg`, `tools/k4b`

## Imported by

- none

## Top-level constants

- `MASTERS`
- `REPO`
- `_ERR`

## Classes and functions

- **function `_imports`** [L32-34]: `def _imports()` decorators: @pytest.fixture(autouse=True)
- **function `_rho_draws`** [L37-38]: `def _rho_draws(centre, rng, width=0.01)`
- **function `W`** [L41-81]: `def W(tag, outcome, statuses=None, endpoint=None, p1=None, rho=None, ratio_status='DEFINED', L=0.05, F=1e-06, seed=0)` - A planted load_world summary. rho: {j: (rhoL, rhoU)} or a centre for draws.
- **function `_reading`** [L84-85]: `def _reading(r, *names)`
- **function `_dump`** [L88-89]: `def _dump(x)`
- **test `test_all_support_general`** [L95-97]: `def test_all_support_general()`
- **test `test_two_support_not_general`** [L100-102]: `def test_two_support_not_general()`
- **test `test_not_learned_world_unavailable_never_exclusion`** [L105-110]: `def test_not_learned_world_unavailable_never_exclusion()`
- **test `test_rc1_support_plus_mixed_without_exclude`** [L113-116]: `def test_rc1_support_plus_mixed_without_exclude()`
- **test `test_rc1_mixed_with_unresolved_numerical_not_exclude`** [L119-122]: `def test_rc1_mixed_with_unresolved_numerical_not_exclude()`
- **test `test_rc1_p1_passed_mixed_with_exclude_not_general`** [L125-131]: `def test_rc1_p1_passed_mixed_with_exclude_not_general()`
- **test `test_exclude_without_p1_pass_not_general_refused`** [L134-138]: `def test_exclude_without_p1_pass_not_general_refused()` - NOT_GENERAL needs p1_passed and endpoint; an EXCLUDE status otherwise does not count.
- **test `test_exclusion_world_not_general`** [L141-144]: `def test_exclusion_world_not_general()`
- **test `test_failed_or_dropped_world_unavailable`** [L149-153]: `def test_failed_or_dropped_world_unavailable(bad)` decorators: @pytest.mark.parametrize('bad', ['FAIL_TECHNICAL/TRAINING', 'FAIL_TECHNICAL/LAW_BOUND', 'INCONCLUSIVE/ORACLE_FEASIBILITY', 'INCONCLUSIVE/UNDERPOWERED'])
- **test `test_capture_one_endpoint_unavailable`** [L159-162]: `def test_capture_one_endpoint_unavailable()`
- **function `_rh`** [L165-166]: `def _rh(tag, pairs)`
- **test `test_capture_at_least_half_with_equality`** [L169-176]: `def test_capture_at_least_half_with_equality()`
- **test `test_capture_just_below_half_lower_not_at_least`** [L179-183]: `def test_capture_just_below_half_lower_not_at_least()`
- **test `test_capture_below_half`** [L186-189]: `def test_capture_below_half()`
- **test `test_capture_upper_exactly_half_not_below`** [L192-195]: `def test_capture_upper_exactly_half_not_below()`
- **test `test_capture_unresolved_ratio_world`** [L198-201]: `def test_capture_unresolved_ratio_world()`
- **test `test_capture_precedence_below_half_wins`** [L204-208]: `def test_capture_precedence_below_half_wins()`
- **test `test_all_exclusion_needs_two_endpoint_worlds`** [L214-223]: `def test_all_exclusion_needs_two_endpoint_worlds()`
- **test `test_positive_everywhere_exact`** [L226-233]: `def test_positive_everywhere_exact()`
- **test `test_similarity_compatible_and_not`** [L239-244]: `def test_similarity_compatible_and_not()`
- **function `_compat`** [L247-251]: `def _compat(r)`
- **test `test_similarity_spread_pairing`** [L254-268]: `def test_similarity_spread_pairing()`
- **function `_floats`** [L271-278]: `def _floats(x)`

