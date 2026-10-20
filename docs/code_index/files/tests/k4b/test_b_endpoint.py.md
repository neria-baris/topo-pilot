# `tests/k4b/test_b_endpoint.py`

- Source: [tests/k4b/test_b_endpoint.py](../../../../../tests/k4b/test_b_endpoint.py)
- Kind: python
- Lines: 398

## Module docstring

> Author B, round 2: API §14.2–14.3 and rulings R20–R22 (API §15). Control arrays, the single
> 610103 bootstrap dict, control summaries, decoder agreement, ratios (B4 = fresh_b4["point"]), the
> init qualifier (strict exact L − F > 1/100), two-sided controls per side with no status (R22 key
> names point_/central95_minus/plus, which supersede the §14.2 "pair" wording), support entries and
> `endpoint` (exact §11 keys, no writes). Synthetic 24-row inputs; expected values from independent
> formulas or from order statistics of the captured draws; structure only where internals are open.

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../../tools/c1prime/c1_bounds.py.md) (line 26, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 27, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 28, via sys.path edit)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../../tools/k4b/k4b_fresh.py.md) (line 29, via sys.path edit)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 30, via sys.path edit)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../../tools/k4b/k4b_stats.py.md) (line 31, via sys.path edit)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 32, via sys.path edit)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 23)
- `pytest` (lines 24)

### Standard library

- `__future__` (lines 8)
- `builtins` (lines 10)
- `fractions` (lines 14)
- `io` (lines 11)
- `math` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `B_SIDE`
- `ENTRY`
- `MODELS`
- `NAMES`
- `PER_MODEL_KEYS`
- `REPO`
- `RESULT_KEYS`
- `TWO_PI`

## Classes and functions

- **function `vphase`** [L49-51]: `def vphase(m)`
- **function `dot`** [L54-55]: `def dot(phi, m32, mK)`
- **function `val`** [L58-59]: `def val(x) -> float`
- **function `kth`** [L62-63]: `def kth(draws, k) -> float`
- **function `at`** [L66-67]: `def at(d, key)`
- **function `check_side`** [L70-73]: `def check_side(g, pk, ck, d, X) -> None`
- **function `extension`** [L76-80]: `def extension(rng)`
- **function `decoder`** [L83-90]: `def decoder(seed) -> dict`
- **function `inputs`** [L93-101]: `def inputs(reason='degenerate bandwidth') -> dict`
- **function `psi_of`** [L104-109]: `def psi_of(dec, canon32)`
- **function `agreement`** [L112-114]: `def agreement(I, j) -> float`
- **function `one`** [L117-118]: `def one(phi, m32, mK) -> dict`
- **function `two`** [L121-124]: `def two(phi, sup, m32, mK) -> dict`
- **function `my_controls`** [L127-141]: `def my_controls(I) -> dict`
- **function `endpoint_arrays_for`** [L144-149]: `def endpoint_arrays_for(I) -> dict`
- **function `expected_keys`** [L152-158]: `def expected_keys(controls) -> list`
- **function `bounds_for`** [L161-167]: `def bounds_for(controls, uncertified=()) -> dict`
- **function `check_summary`** [L170-191]: `def check_summary(s, draws, controls, bounds_all) -> None`
- **test `test_control_arrays_names_entries_shapes_and_values`** [L194-216]: `def test_control_arrays_names_entries_shapes_and_values()`
- **test `test_bootstrap_inputs_fixed_order_one_dict`** [L219-239]: `def test_bootstrap_inputs_fixed_order_one_dict()`
- **test `test_decoder_agreement_and_unavailable_form`** [L243-249]: `def test_decoder_agreement_and_unavailable_form(reason)` decorators: @pytest.mark.parametrize('reason', ['degenerate bandwidth', 'equivalence'])
- **test `test_ratios_values_and_undefined_denominators`** [L254-261]: `def test_ratios_values_and_undefined_denominators(bad)` decorators: @pytest.mark.parametrize('bad', [None, 0.0, -0.0, -0.001, float('nan'), float('inf'), float('-inf')])
- **test `test_init_qualifier_strict_exact`** [L274-281]: `def test_init_qualifier_strict_exact(L, F, want)` decorators: @pytest.mark.parametrize('L,F,want', [(Fraction(3, 100), Fraction(2, 100), False), (Fraction(3, 100) + Fraction(1, 10 ** 40), Fraction(2, 100), True), (Fraction(3, 100) - Fraction(1, 10 ** 40), Fraction(2, 100), False), (Fraction(-1, 2), Fraction(1, 10 ** 9), False), (Fraction(1, 2), Fraction(1, 10 ** 9), True)] + [(F + 0.01, F, None) for F in (1e-09, 0.0025, 0.07, 0.1, 0.123456789, 0.2, 0.3, 0.6)])
- **function `run`** [L285-321]: `def run(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **test `test_endpoint_keys_single_stream_and_no_writes`** [L324-336]: `def test_endpoint_keys_single_stream_and_no_writes(run)`
- **function `expected_status`** [L339-344]: `def expected_status(L, U, Fm, Fp)`
- **test `test_endpoint_per_model_bounds_margins_status_support_and_overall`** [L347-381]: `def test_endpoint_per_model_bounds_margins_status_support_and_overall(run)`
- **test `test_endpoint_summaries_ratios_init_qualifier_and_agreement`** [L384-398]: `def test_endpoint_summaries_ratios_init_qualifier_and_agreement(run)`

