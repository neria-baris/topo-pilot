# `tests/d2a/test_a_targets.py`

- Source: [tests/d2a/test_a_targets.py](../../../../../tests/d2a/test_a_targets.py)
- Kind: python
- Lines: 290

## Module docstring

> Independent tests of tools/d2a/d2a_targets.py (job 0028, author A): T-FIX, T-SUPP, T-PRIOR and
> the G0-NUM identities at small sampled batches. Written from D2A-FROZEN-v1 sections 3 and 5.2
> and tools/d2a/API.md section 2.2 only, before the module existed.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 19, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 20, via package root)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 21, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 28, via sys.path edit)
- `import d2a_targets` -> [tools/d2a/d2a_targets.py](../../tools/d2a/d2a_targets.py.md) (line 29, via sys.path edit)
- `import d2a_world` -> [tools/d2a/d2a_world.py](../../tools/d2a/d2a_world.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 16)
- `pytest` (lines 17)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 13)
- `pathlib` (lines 14)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 26: `str(REPO_ROOT.joinpath(*_parts))` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `EXACT`
- `FM`
- `NAMED`
- `PRIORS`
- `REPO_ROOT`
- `T_CC`

## Classes and functions

- **function `_f`** [L42-43]: `def _f(x)`
- **function `_flat`** [L46-47]: `def _flat(J)`
- **function `_tv`** [L50-51]: `def _tv(p, q)`
- **function `_at`** [L54-56]: `def _at(h, proc='CM')`
- **function `_exact_J3`** [L59-73]: `def _exact_J3(b, T, E)` - Independent Fraction J3[25 s1 + 5 s2 + s3] = b T diag(E s1) T diag(E s2) T E s3.
- **function `_sample`** [L76-78]: `def _sample(n, T, name)`
- **function `cm_tokens`** [L82-83]: `def cm_tokens()` decorators: @pytest.fixture(scope='module')
- **test `test_T_FIX_named_histories_match_exact`** [L88-103]: `def test_T_FIX_named_histories_match_exact(name)` decorators: @pytest.mark.parametrize('name', list(NAMED))
- **test `test_T_FIX_three_step_laws_match_independent_fractions`** [L107-119]: `def test_T_FIX_three_step_laws_match_independent_fractions(name)` decorators: @pytest.mark.parametrize('name', list(NAMED))
- **test `test_T_FIX_tv_values_of_g0_fix`** [L122-140]: `def test_T_FIX_tv_values_of_g0_fix()`
- **test `test_g0_fix_gate_passes`** [L143-146]: `def test_g0_fix_gate_passes()`
- **function `_read_strings`** [L150-170]: `def _read_strings(k)` - Indices of k-symbol strings with a read (A/B), reachable with positive probability from
- **test `test_T_SUPP_support_lists_equal_independent_enumeration`** [L173-176]: `def test_T_SUPP_support_lists_equal_independent_enumeration()`
- **test `test_T_SUPP_targets_vanish_off_support`** [L180-187]: `def test_T_SUPP_targets_vanish_off_support(t, cm_tokens)` decorators: @pytest.mark.parametrize('t', [5, 16, 28, 31])
- **test `test_oracle_identities`** [L192-215]: `def test_oracle_identities(t, cm_tokens)` decorators: @pytest.mark.parametrize('t', [3, 16, 28, 32])
- **test `test_cc_oracle_null`** [L218-225]: `def test_cc_oracle_null()`
- **function `_exact_priors`** [L229-234]: `def _exact_priors(model)`
- **test `test_T_PRIOR_window_prior_is_mu_T_power`** [L241-248]: `def test_T_PRIOR_window_prior_is_mu_T_power(proc)` decorators: @pytest.mark.parametrize('proc', ['CM', 'CC'])
- **function `_filter`** [L251-252]: `def _filter(tokens, prior, t, m)`
- **test `test_T_PRIOR_whole_window_equals_full_filter`** [L256-261]: `def test_T_PRIOR_whole_window_equals_full_filter(t, cm_tokens)` decorators: @pytest.mark.parametrize('t', [1, 5, 16, 28, 32])
- **test `test_T_PRIOR_window8_equals_full_oracle_up_to_t8`** [L265-277]: `def test_T_PRIOR_window8_equals_full_oracle_up_to_t8(t, cm_tokens)` decorators: @pytest.mark.parametrize('t', range(1, 9))
- **test `test_T_PRIOR_windows_use_the_true_time_marginal`** [L281-290]: `def test_T_PRIOR_windows_use_the_true_time_marginal(t, cm_tokens)` decorators: @pytest.mark.parametrize('t', [16, 28])

