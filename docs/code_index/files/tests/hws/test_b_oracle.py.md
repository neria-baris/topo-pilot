# `tests/hws/test_b_oracle.py`

- Source: [tests/hws/test_b_oracle.py](../../../../../tests/hws/test_b_oracle.py)
- Kind: python
- Lines: 304

## Module docstring

> Author B (job 0119), TEST_PLAN §3 `test_b_oracle.py`: stream scopes (§6.6), one
> `HMMSampler.sample` call per world-look returning contiguous uint8 tokens without w_last or
> states (§4.7, RC-5), `row_arrays` keys/shapes/dtypes and formulas, the DR8 formula bridge at
> W = 12, the DR11 alignment traps against an independent reference filter written here, the DR3
> forced unanchored world (m_K = 0), `prefix_permuted`, `p4_rows` and the marginal conventions.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](../../tools/hws/hws_worlds.py.md) (line 24, via sys.path edit)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../../tools/hws/hws_oracle.py.md) (line 25, via sys.path edit)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../../tools/k4b/k4b_scores.py.md) (line 27, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 28, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 31, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 14)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / 'tools' / 'hws')` -> `tools/hws`

## Imported by

- none

## Top-level constants

- `REPO`
- `STAGES`
- `TINY`

## Classes and functions

- **function `tiny`** [L38-39]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **function `w0`** [L43-44]: `def w0()` decorators: @pytest.fixture(scope='module')
- **function `_tok`** [L47-48]: `def _tok(n, L, V, a=7, b=1)`
- **function `_kl`** [L51-52]: `def _kl(p, q)`
- **function `_H`** [L55-56]: `def _H(p)`
- **function `_spy`** [L59-70]: `def _spy(monkeypatch)`
- **test `test_history_streams_match_the_seedtree_scopes`** [L75-89]: `def test_history_streams_match_the_seedtree_scopes()`
- **test `test_stream_refusals`** [L92-97]: `def test_stream_refusals()`
- **test `test_sample_calls_the_sampler_once_and_drops_the_last_symbol`** [L102-111]: `def test_sample_calls_the_sampler_once_and_drops_the_last_symbol(tiny, monkeypatch)`
- **test `test_world_look_streams_and_bit_identical_regeneration`** [L114-129]: `def test_world_look_streams_and_bit_identical_regeneration(tiny, monkeypatch)`
- **test `test_row_arrays_keys_shapes_dtypes_and_formulas`** [L134-176]: `def test_row_arrays_keys_shapes_dtypes_and_formulas(tiny)`
- **test `test_dr8_formula_bridge_at_w12`** [L179-205]: `def test_dr8_formula_bridge_at_w12(w0)`
- **function `_ref_belief`** [L210-226]: `def _ref_belief(T, E, pi, tok, K, transpose=False, symmap=None, prefix=False, inherit=False, trailing=False)` - Independent suffix filter: restart from pi, emit first, transition between emissions.
- **test `test_dr11_alignment_traps_are_detected`** [L229-249]: `def test_dr11_alignment_traps_are_detected(tiny)`
- **test `test_dr3_forced_unanchored_world_has_zero_moments`** [L254-260]: `def test_dr3_forced_unanchored_world_has_zero_moments()`
- **test `test_identical_emission_has_no_beyond_k_information`** [L263-270]: `def test_identical_emission_has_no_beyond_k_information()`
- **test `test_prefix_permuted_and_p4_rows`** [L273-290]: `def test_prefix_permuted_and_p4_rows(tiny)`
- **test `test_marginal_index_conventions`** [L293-304]: `def test_marginal_index_conventions()`

