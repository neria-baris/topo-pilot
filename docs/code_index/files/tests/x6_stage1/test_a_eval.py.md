# `tests/x6_stage1/test_a_eval.py`

- Source: [tests/x6_stage1/test_a_eval.py](../../../../../tests/x6_stage1/test_a_eval.py)
- Kind: python
- Lines: 288

## Module docstring

> Author A: T-EVAL and T-QUANT (X6S1-FROZEN-v1 §2.2, §10.2 T13/T17/T20/T25, §14.3; API.md §2, §7).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../../tools/x6_stage1/x6s1_data.py.md) (line 24, via sys.path edit)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../../tools/x6_stage1/x6s1_cloud.py.md) (line 25, via sys.path edit)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 26, via sys.path edit)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 27, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 31, via sys.path edit)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 17)
- `pytest` (lines 18)
- `torch` (lines 19)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 8)
- `decimal` (lines 12)
- `fractions` (lines 13)
- `functools` (lines 14)
- `hashlib` (lines 9)
- `math` (lines 10)
- `pathlib` (lines 15)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(REPO / 'tools' / 'x6_stage1')` -> `tools/x6_stage1`
- line 30: `str(REPO / 'tools' / 'x6_stage0')` -> `tools/x6_stage0`

## Imported by

- none

## Top-level constants

- `ANCHOR`
- `FLOOR`
- `REPO`

## Classes and functions

- **function `walks`** [L39-46]: `def walks(n_rows: int, seed: int) -> np.ndarray`
- **function `synth_state`** [L50-54]: `def synth_state()` decorators: @lru_cache(maxsize=None)
- **function `predictor`** [L58-59]: `def predictor()` decorators: @lru_cache(maxsize=None)
- **function `ref_probs`** [L62-71]: `def ref_probs(tokens, t)` - Independent float64 forward: input [BOS, w_1..w_32], softmax of logits[i, t_i].
- **test `test_pad_and_model_inputs`** [L75-84]: `def test_pad_and_model_inputs()`
- **test `test_readout_position_index`** [L87-101]: `def test_readout_position_index()`
- **test `test_padding_independence`** [L104-108]: `def test_padding_independence()`
- **test `test_float64_determinism_vector_t_and_normalisation`** [L111-119]: `def test_float64_determinism_vector_t_and_normalisation()`
- **test `test_model_predictor_from_verified_file`** [L122-133]: `def test_model_predictor_from_verified_file(tmp_path)`
- **test `test_oracle_predictor_and_qstar_codes`** [L136-147]: `def test_oracle_predictor_and_qstar_codes()`
- **test `test_kl_rows_zeros_and_infinity`** [L150-159]: `def test_kl_rows_zeros_and_infinity()`
- **test `test_cue_mass_and_cue_normalise`** [L162-174]: `def test_cue_mass_and_cue_normalise()`
- **function `my_quantise`** [L178-190]: `def my_quantise(s)`
- **function `random_laws`** [L193-200]: `def random_laws(n, seed)`
- **test `test_quantise_conservation_and_independent_reference`** [L203-211]: `def test_quantise_conservation_and_independent_reference()`
- **test `test_quantise_ties_and_zero_rule_hand_cases`** [L214-232]: `def test_quantise_ties_and_zero_rule_hand_cases()`
- **test `test_quant_invalid`** [L236-251]: `def test_quant_invalid(bad)` decorators: @pytest.mark.parametrize('bad', ['sum_high', 'sum_low', 'negative', 'nan', 'inf'])
- **test `test_readout_exact_positivity_and_float`** [L254-266]: `def test_readout_exact_positivity_and_float()`
- **function `_dec`** [L269-270]: `def _dec(fr)`
- **test `test_readout_floor_on_exact_laws_t17`** [L273-288]: `def test_readout_floor_on_exact_laws_t17()`

