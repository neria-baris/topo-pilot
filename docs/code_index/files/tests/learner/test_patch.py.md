# `tests/learner/test_patch.py`

- Source: [tests/learner/test_patch.py](../../../../../tests/learner/test_patch.py)
- Kind: python
- Lines: 309

## Module docstring

> Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
> before reading the implementation.

## Imports

### Internal (repo files)

- `import topo_pilot.learner` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 13, via package root)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 14, via package root)
- `from topo_pilot.learner import ModelConfig, PatchedOutput, TransformerLM, forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 15, via package root)

### External (third-party)

- `pytest` (lines 10)
- `torch` (lines 11)

### Standard library

- `ast` (lines 7)
- `pathlib` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `CFG`
- `SITES`

## Classes and functions

- **function `model`** [L24-31]: `def model()` decorators: @pytest.fixture()
- **function `_inputs`** [L34-36]: `def _inputs(batch=3, length=33, seed=1)`
- **function `_rand_rep`** [L39-41]: `def _rand_rep(batch=3, seed=7, scale=2.0)`
- **function `_reference`** [L44-61]: `def _reference(model, x, site, index, rep)` - Spec section 1 computation written out with the model's public submodules.
- **test `test_identity_replacement_reproduces_all_logits`** [L68-77]: `def test_identity_replacement_reproduces_all_logits(model, site, index)` decorators: @pytest.mark.parametrize('site', SITES) @pytest.mark.parametrize('index', [0, 13, 32])
- **test `test_identity_on_shorter_sequence`** [L80-86]: `def test_identity_on_shorter_sequence(model)`
- **test `test_causality_non_identity_patch`** [L93-99]: `def test_causality_non_identity_patch(model, site, index)` decorators: @pytest.mark.parametrize('site', SITES) @pytest.mark.parametrize('index', [5, 20, 32])
- **test `test_patch_matches_spec_reference_computation`** [L103-108]: `def test_patch_matches_spec_reference_computation(model, site)` decorators: @pytest.mark.parametrize('site', SITES)
- **test `test_resid_post_0_patch_propagates_to_later_positions`** [L111-117]: `def test_resid_post_0_patch_propagates_to_later_positions(model)` - The forward continues through blocks[1]: later positions attend to the patched vector.
- **test `test_ln_final_out_patch_touches_only_index`** [L120-126]: `def test_ln_final_out_patch_touches_only_index(model)`
- **test `test_ln_final_out_has_no_second_layernorm`** [L129-143]: `def test_ln_final_out_has_no_second_layernorm(model)`
- **test `test_hook_at_site_shows_replacement`** [L149-159]: `def test_hook_at_site_shows_replacement(model, site)` decorators: @pytest.mark.parametrize('site', SITES)
- **test `test_hooks_downstream_are_after_the_patch`** [L162-178]: `def test_hooks_downstream_are_after_the_patch(model)`
- **test `test_no_hooks_by_default`** [L181-183]: `def test_no_hooks_by_default(model)`
- **test `test_parameters_and_buffers_bitwise_unchanged`** [L189-199]: `def test_parameters_and_buffers_bitwise_unchanged(model, site)` decorators: @pytest.mark.parametrize('site', SITES)
- **test `test_inputs_and_replacement_not_mutated`** [L202-208]: `def test_inputs_and_replacement_not_mutated(model)`
- **function `_code`** [L213-216]: `def _code(fn)`
- **test `test_training_mode_is_invalid_config`** [L219-224]: `def test_training_mode_is_invalid_config(model)`
- **test `test_unknown_site`** [L229-231]: `def test_unknown_site(model, site)` decorators: @pytest.mark.parametrize('site', ['embed', 'resid_post_9', 'resid_post_2', 'foo', 'resid_post_', 'ln_final'])
- **test `test_unknown_return_hook`** [L235-237]: `def test_unknown_return_hook(model, hooks)` decorators: @pytest.mark.parametrize('hooks', [('foo',), ('resid_post_9',), ('resid_post_1', 'bar')])
- **test `test_index_out_of_range`** [L241-243]: `def test_index_out_of_range(model, index)` decorators: @pytest.mark.parametrize('index', [-1, 33, 100])
- **test `test_index_out_of_range_for_short_sequence`** [L246-249]: `def test_index_out_of_range_for_short_sequence(model)`
- **test `test_replacement_wrong_shape`** [L253-256]: `def test_replacement_wrong_shape(model, shape)` decorators: @pytest.mark.parametrize('shape', [(3, 17), (3, 15), (2, 16), (4, 16), (16,), (3, 1, 16)])
- **test `test_non_finite_replacement`** [L261-265]: `def test_non_finite_replacement(model, bad, site)` decorators: @pytest.mark.parametrize('bad', [float('nan'), float('inf'), float('-inf')]) @pytest.mark.parametrize('site', SITES)
- **test `test_bad_inputs_alignment_error`** [L276-279]: `def test_bad_inputs_alignment_error(model, make)` decorators: @pytest.mark.parametrize('make', [lambda : torch.randint(0, 4, (33,)), lambda : torch.randint(0, 4, (3, 33, 1)), lambda : torch.randint(0, 4, (3, 33)).float(), lambda : torch.full((3, 33), 4, dtype=torch.long), lambda : torch.full((3, 33), -1, dtype=torch.long), lambda : torch.randint(0, 4, (3, 34))])
- **test `test_single_out_of_vocab_token`** [L282-286]: `def test_single_out_of_vocab_token(model)`
- **test `test_patch_module_imports_no_forbidden_modules`** [L291-309]: `def test_patch_module_imports_no_forbidden_modules()`

