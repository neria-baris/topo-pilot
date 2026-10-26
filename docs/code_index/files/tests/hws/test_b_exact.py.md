# `tests/hws/test_b_exact.py`

- Source: [tests/hws/test_b_exact.py](../../../../../tests/hws/test_b_exact.py)
- Kind: python
- Lines: 283

## Module docstring

> Author B (job 0119), TEST_PLAN §3 `test_b_exact.py`: p_D2a against brute force (tiny world,
> tiny rational HMM by Fractions), the E4 boundary, symbol law, A_eff, mean last-symbol entropy,
> the K <= 3 suffix enumeration, the Decimal and BayesFilter spot checks (pass on the correct world,
> fail when one side sees a perturbed E), the tier-0 law report (RC-3, DR13) and `exact_world`.
> Protocol §2.4, §2.6, §5.1 E4, §8; DR6, DR13; KC9, KC10.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 25, via sys.path edit)
- `import hws_exact` -> [tools/hws/hws_exact.py](../../tools/hws/hws_exact.py.md) (line 26, via sys.path edit)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../../tools/x4_circle_history/error_bound.py.md) (line 28, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../../tools/x4_circle_history/process_law.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 31, via package root)
- `from topo_pilot.process import TransitionBuilder` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 9)
- `decimal` (lines 11)
- `fractions` (lines 15)
- `itertools` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 23: `str(REPO / 'tools' / 'hws')` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `EXACT_KEYS`
- `E_Q`
- `PI_Q`
- `REPO`
- `TAU`
- `T_Q`

## Classes and functions

- **function `_f`** [L41-43]: `def _f(m)`
- **function `_forward`** [L46-50]: `def _forward(T, E, pi, hist)`
- **function `_forward_q`** [L53-57]: `def _forward_q(hist)`
- **function `_perturbed`** [L60-63]: `def _perturbed(E)`
- **function `tiny`** [L67-68]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **function `w0`** [L72-73]: `def w0()` decorators: @pytest.fixture(scope='module')
- **test `test_p_d2a_equals_brute_force_on_the_tiny_world`** [L79-83]: `def test_p_d2a_equals_brute_force_on_the_tiny_world(tiny, alphabet)` decorators: @pytest.mark.parametrize('alphabet', [(0,), (0, 1), (1, 2)])
- **test `test_p_d2a_full_alphabet_and_symbols_beyond_v`** [L86-92]: `def test_p_d2a_full_alphabet_and_symbols_beyond_v(tiny)`
- **test `test_p_d2a_equals_exact_fractions_on_a_rational_hmm`** [L96-99]: `def test_p_d2a_equals_exact_fractions_on_a_rational_hmm(alphabet, Lh)` decorators: @pytest.mark.parametrize('alphabet, Lh', [((0, 1), 6), ((2,), 5), ((0,), 7)])
- **test `test_e4_boundary`** [L102-114]: `def test_e4_boundary()`
- **function `_direct_entropy`** [L119-125]: `def _direct_entropy(T, E, pi)`
- **test `test_symbol_law_aeff_and_last_entropy_direct`** [L128-137]: `def test_symbol_law_aeff_and_last_entropy_direct(tiny)`
- **test `test_aeff_on_known_zero_worlds`** [L140-144]: `def test_aeff_on_known_zero_worlds()`
- **test `test_suffix_enumeration_against_brute_force`** [L147-165]: `def test_suffix_enumeration_against_brute_force(tiny)`
- **test `test_decimal_spot_check_passes_and_detects_a_perturbed_e`** [L170-179]: `def test_decimal_spot_check_passes_and_detects_a_perturbed_e(w0, monkeypatch)`
- **test `test_decimal_spot_check_is_w12_only`** [L182-184]: `def test_decimal_spot_check_is_w12_only(tiny)`
- **test `test_bayes_cross_check_passes_and_detects_a_perturbed_e`** [L187-198]: `def test_bayes_cross_check_passes_and_detects_a_perturbed_e(tiny, monkeypatch)`
- **test `test_law_bound_report_nonterminating_logit`** [L204-215]: `def test_law_bound_report_nonterminating_logit(sigma)` decorators: @pytest.mark.parametrize('sigma', [F(3, 2), F(11, 8)])
- **test `test_law_bound_report_with_injected_enclosures`** [L218-244]: `def test_law_bound_report_with_injected_enclosures()`
- **test `test_exact_world_on_a_symmetric_cell`** [L253-265]: `def test_exact_world_on_a_symmetric_cell()`
- **test `test_exact_world_identity_fields_at_w0`** [L268-273]: `def test_exact_world_identity_fields_at_w0(w0)`
- **test `test_exact_world_e1_carries_only_e1`** [L276-283]: `def test_exact_world_e1_carries_only_e1(monkeypatch)`

