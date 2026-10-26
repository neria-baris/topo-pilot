# `tests/c2_nd/test_b_layer2.py`

- Source: [tests/c2_nd/test_b_layer2.py](../../../../../tests/c2_nd/test_b_layer2.py)
- Kind: python
- Lines: 260

## Module docstring

> Author B, KM1-KM4 (protocol §2.4, §5.1) and T-RESP with ORACLE-FEAS (i) (§2.5, §3 rows 9,
> 21, 23, §5.1; API.md §7.2, §7.4, §8.2).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 21, via sys.path edit)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 24, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 25, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](../../tools/c2_nd/nd_attrib.py.md) (line 26, via sys.path edit)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 27, via sys.path edit)
- `from topo_pilot.learner import ModelConfig, TransformerLM, forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 28)
- `pytest` (lines 29)
- `torch` (lines 30)

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

- line 19: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `DD`
- `NEGATIVE_CLAIMS`
- `NM`
- `NM_KEYS`
- `NR`
- `REPO`

## Classes and functions

- **function `spaces`** [L38-43]: `def spaces(seed)` - P2: orthogonal projector onto a 6-d S inside 1-perp; PC: onto 1-perp minus S.
- **function `km_model`** [L46-64]: `def km_model(seed, W, mlp=False)`
- **function `reflect`** [L67-70]: `def reflect(h, P, rng)`
- **function `donors`** [L73-81]: `def donors(seed, P2, PC, norm_only=False)`
- **function `zpatch`** [L84-87]: `def zpatch(model, X, rep)`
- **function `run_km`** [L90-99]: `def run_km(model, P2, h, Dp, Dm)`
- **function `shares`** [L102-105]: `def shares(cm_)`
- **function `bounds`** [L108-110]: `def bounds(arrays, seed=630505, alpha=Fraction(1, 360), draws=2000)`
- **function `nm_status`** [L113-117]: `def nm_status(cm_, A_full)`
- **test `test_km1_code_only_head_is_necessary_m`** [L120-133]: `def test_km1_code_only_head_is_necessary_m()`
- **test `test_km2_complement_only_head_is_not_necessary_m`** [L136-142]: `def test_km2_complement_only_head_is_not_necessary_m()`
- **test `test_km3_layernorm_scale_loophole`** [L145-161]: `def test_km3_layernorm_scale_loophole()` - The head reads only S and the code is the same in both donors; the complement changes
- **test `test_km4_mlp_gate_interaction`** [L164-179]: `def test_km4_mlp_gate_interaction()`
- **function `bd`** [L183-185]: `def bd(sgn, g=1e-09)`
- **test `test_no_full_response_is_model_headroom`** [L196-209]: `def test_no_full_response_is_model_headroom(y_active)` decorators: @pytest.mark.parametrize('y_active', (False, True))
- **test `test_unamplified_decoy_fails_and_gain_six_passes`** [L212-237]: `def test_unamplified_decoy_fails_and_gain_six_passes()`
- **function `oracle_fixture`** [L240-248]: `def oracle_fixture(n=32)`
- **test `test_oracle_feas_identity`** [L251-260]: `def test_oracle_feas_identity()`

