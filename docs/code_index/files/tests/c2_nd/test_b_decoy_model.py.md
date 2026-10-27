# `tests/c2_nd/test_b_decoy_model.py`

- Source: [tests/c2_nd/test_b_decoy_model.py](../../../../../tests/c2_nd/test_b_decoy_model.py)
- Kind: python
- Lines: 345

## Module docstring

> Author B, T-DECOY-EXACT (protocol §2.6, §2.7, §3 rows 11 and 20, §5.1; API.md §6).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 21, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 24, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../tools/c2_readout/c2_model.py.md) (line 25, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 26, via sys.path edit)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](../../tools/c2_nd/nd_decoy.py.md) (line 27, via sys.path edit)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](../../tools/c2_nd/nd_driver.py.md) (line 28, via sys.path edit)
- `from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 29)
- `pytest` (lines 30)
- `torch` (lines 31)

### Standard library

- `__future__` (lines 8)
- `copy` (lines 10)
- `fractions` (lines 14)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 15)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `COORD`
- `HEAD`
- `N`
- `REPO`

## Classes and functions

- **function `tiny_model`** [L41-49]: `def tiny_model(seed)`
- **function `tokens`** [L52-55]: `def tokens(seed, n=N)`
- **function `projector`** [L58-66]: `def projector(seed, r=31)` - Oblique GLS projectors: L (11 x r) with rows 0..4 for Gamma, 5..10 for B; P_S = B L_B.
- **function `hooks`** [L69-72]: `def hooks(model, X)`
- **function `at_gate`** [L75-78]: `def at_gate(gate)`
- **function `rel_rows`** [L81-85]: `def rel_rows(a, b, tol)` - Per row max|a - b| <= tol * max(1, max|b|).
- **function `base`** [L89-100]: `def base()` decorators: @pytest.fixture(scope='module')
- **function `expected_head`** [L103-106]: `def expected_head(kind, WU, Q0, P_S, g=G_D)`
- **function `head`** [L109-111]: `def head(b, kind, P=None, g=G_D)`
- **function `coord_decoys`** [L114-119]: `def coord_decoys(b)`
- **test `test_shapes_and_pi_s`** [L122-128]: `def test_shapes_and_pi_s(base)`
- **test `test_head_edit_formula`** [L135-140]: `def test_head_edit_formula(base, kind)` decorators: @pytest.mark.parametrize('kind', HEAD)
- **test `test_null_heads_annihilate_code`** [L144-148]: `def test_null_heads_annihilate_code(base, kind)` decorators: @pytest.mark.parametrize('kind', ('DNULL', 'DNULL1'))
- **test `test_donly_and_ddose_identities`** [L151-162]: `def test_donly_and_ddose_identities(base)`
- **test `test_head_decoy_is_the_base_with_a_new_head`** [L166-182]: `def test_head_decoy_is_the_base_with_a_new_head(base, kind)` decorators: @pytest.mark.parametrize('kind', HEAD)
- **test `test_patch_and_basis_unchanged_on_head_decoy`** [L186-199]: `def test_patch_and_basis_unchanged_on_head_decoy(base, kind)` decorators: @pytest.mark.parametrize('kind', HEAD)
- **test `test_coordinate_wrapper`** [L202-228]: `def test_coordinate_wrapper(base)`
- **test `test_coordinate_decoys_predict_like_their_partners`** [L231-239]: `def test_coordinate_decoys_predict_like_their_partners(base)`
- **function `m0d_inputs`** [L242-250]: `def m0d_inputs(b, P=None, g=G_D)`
- **test `test_m0d_passes_on_correct_decoys`** [L257-262]: `def test_m0d_passes_on_correct_decoys(base)`
- **test `test_m0d_fails_on_misbuilt_head_decoys`** [L266-271]: `def test_m0d_fails_on_misbuilt_head_decoys(base, bad)` decorators: @pytest.mark.parametrize('bad', ('g5', 'transposed', 'other_model'))
- **test `test_m0d_refused_outside_its_gates`** [L274-277]: `def test_m0d_refused_outside_its_gates(base)`
- **function `dx_arrays`** [L284-287]: `def dx_arrays(b, P_build)`
- **test `test_dx_passes_on_correct_decoys`** [L290-293]: `def test_dx_passes_on_correct_decoys(base)`
- **test `test_dx_fails_on_misbuilt_decoys`** [L297-302]: `def test_dx_fails_on_misbuilt_decoys(base, bad)` decorators: @pytest.mark.parametrize('bad', ('transposed', 'other_model'))
- **function `ref_sha64`** [L305-313]: `def ref_sha64(module, record)`
- **function `record_of`** [L316-320]: `def record_of(kind, j=1729)`
- **class `_Buf(torch.nn.Module)`** [L323-326]
- **method `_Buf.__init__`** [L324-326]: `def __init__(self, t)`
- **test `test_decoy_sha64`** [L329-345]: `def test_decoy_sha64(base)`

