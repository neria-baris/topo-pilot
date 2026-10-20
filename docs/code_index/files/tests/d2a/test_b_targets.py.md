# `tests/d2a/test_b_targets.py`

- Source: [tests/d2a/test_b_targets.py](../../../../../tests/d2a/test_b_targets.py)
- Kind: python
- Lines: 211

## Module docstring

> Independent tests (author B, job 0028): T-BETA, ``d2a_targets.beta`` and ``band_edge_table``.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 17, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 18, via package root)
- `from topo_pilot.oracle import BayesFilter, FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 19, via package root)
- `import d1_seam` -> [tools/d1_seam/d1_seam.py](../../tools/d1_seam/d1_seam.py.md) (line 26, via sys.path edit)
- `import d2a_targets` -> [tools/d2a/d2a_targets.py](../../tools/d2a/d2a_targets.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `str(REPO / _sub)` -> `tools/d1_seam`, `tools/d2a`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `KEYS`
- `REPO`
- `TOL`

## Classes and functions

- **test `test_beta_oracle_is_one_and_pi_blind_is_zero`** [L36-41]: `def test_beta_oracle_is_one_and_pi_blind_is_zero()`
- **test `test_beta_is_slope_through_origin_on_hand_example`** [L44-51]: `def test_beta_is_slope_through_origin_on_hand_example()`
- **test `test_beta_pools_two_dimensional_contrasts`** [L54-59]: `def test_beta_pools_two_dimensional_contrasts()`
- **test `test_beta_scale_and_sign`** [L62-65]: `def test_beta_scale_and_sign()`
- **test `test_beta_undefined_denominator`** [L75-76]: `def test_beta_undefined_denominator(d)` decorators: @pytest.mark.parametrize('d', [np.zeros(4), np.zeros((3, 2)), np.array([0.1, np.nan, 0.2]), np.array([0.1, np.inf]), np.array([1e+200, 1e+200])])
- **test `test_beta_tiny_positive_denominator_is_defined`** [L79-82]: `def test_beta_tiny_positive_denominator_is_defined()`
- **function `_pad`** [L87-88]: `def _pad(history)`
- **function `fm`** [L92-93]: `def fm()` decorators: @pytest.fixture(scope='module')
- **function `tokens`** [L97-103]: `def tokens(fm)` decorators: @pytest.fixture(scope='module') - 64 natural C/M episodes plus the padded canonical pair (w_12..w_33 = sigma0, so p = 33
- **function `ref`** [L107-125]: `def ref(fm, tokens)` decorators: @pytest.fixture(scope='module') - q, q_half [R, 33, 5]: index p = law of w_{p+1} after w_{1:p} (mixture, pi-blind).
- **function `_table`** [L128-135]: `def _table(out)`
- **test `test_reference_has_informed_band_edges`** [L138-140]: `def test_reference_has_informed_band_edges(ref)`
- **test `test_band_edge_table_selects_exactly_sigma0_sigma2_rows`** [L143-151]: `def test_band_edge_table_selects_exactly_sigma0_sigma2_rows(tokens, ref)`
- **test `test_band_edge_d_equals_oracle_contrast`** [L154-156]: `def test_band_edge_d_equals_oracle_contrast(tokens, ref)`
- **test `test_band_edge_r8_uses_the_exact_window8_law`** [L159-164]: `def test_band_edge_r8_uses_the_exact_window8_law(tokens, ref)`
- **test `test_band_edge_oracle_model_gives_rm_equal_d_and_beta_one`** [L167-171]: `def test_band_edge_oracle_model_gives_rm_equal_d_and_beta_one(tokens, ref)`
- **test `test_band_edge_pi_blind_model_gives_beta_zero`** [L174-178]: `def test_band_edge_pi_blind_model_gives_beta_zero(tokens, ref)`
- **test `test_band_edge_rm_reads_model_index_p`** [L181-187]: `def test_band_edge_rm_reads_model_index_p(tokens, ref)` - rm uses q_model[row, p] (index p sees w_1..w_p and predicts w_{p+1}); a model whose law
- **test `test_beta2_oracle_and_pi_blind_on_decision_contrasts`** [L192-211]: `def test_beta2_oracle_and_pi_blind_on_decision_contrasts(fm, tokens)`

