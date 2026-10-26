# `tools/c2_nd/nd_config.py`

- Source: [tools/c2_nd/nd_config.py](../../../../../tools/c2_nd/nd_config.py)
- Kind: python
- Lines: 182

## Module docstring

> C2ND configuration: bindings, paths, CONTRACT.json loading, constants, exact Fraction levels
> and ranks, seeds, and the sys.path convention (API.md §1, §3, §20; C2ND-DESIGN-v1 §2.1, §4.1,
> §6.1, §11.3).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 24, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 27, via unique basename)

### External (third-party)

- none

### Standard library

- `__future__` (lines 11)
- `fractions` (lines 15)
- `json` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(_p)` -> `tools/c2_nd`, `tools/c2_readout`

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 19, import)
- [tests/c2_nd/test_a_family.py](../../tests/c2_nd/test_a_family.py.md) (line 22, import)
- [tests/c2_nd/test_a_identity.py](../../tests/c2_nd/test_a_identity.py.md) (line 21, import)
- [tests/c2_nd/test_a_inference.py](../../tests/c2_nd/test_a_inference.py.md) (line 21, import)
- [tests/c2_nd/test_a_known.py](../../tests/c2_nd/test_a_known.py.md) (line 20, import)
- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 21, import)
- [tests/c2_nd/test_b_layer2.py](../../tests/c2_nd/test_b_layer2.py.md) (line 21, import)
- [tests/c2_nd/test_b_lineage.py](../../tests/c2_nd/test_b_lineage.py.md) (line 17, import)
- [tests/c2_nd/test_b_policy.py](../../tests/c2_nd/test_b_policy.py.md) (line 15, import)
- [tests/c2_nd/test_b_registry.py](../../tests/c2_nd/test_b_registry.py.md) (line 20, import)
- [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 15, import)
- [tools/c2_nd/nd_data.py](nd_data.py.md) (line 13, import)
- [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 11, import)
- [tools/c2_nd/nd_decoy.py](nd_decoy.py.md) (line 18, import)
- [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 18, import)
- [tools/c2_nd/nd_dry.py](nd_dry.py.md) (line 15, import)
- [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 21, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 10, import)
- [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 16, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 13, import)
- [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 13, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 9, import)

## Top-level constants

- `ALPHA`
- `AUTH_PATH`
- `AUTH_SHA256`
- `BASE_COMMIT`
- `BLOCK`
- `C2_H2`
- `C2_STORE`
- `CONTRACT`
- `CONTRACT_PATH`
- `COORD_DECOYS`
- `DECOYS`
- `DECOY_VERSION`
- `DESC_ALPHA`
- `DESIGN_ID`
- `DRY_SCOPE`
- `FAMILIES`
- `FILE_FAMILY`
- `G_D`
- `H3_ROWS`
- `H4`
- `H5_ALPHA`
- `HEAD_EDITS`
- `HERE`
- `HWS_STORE`
- `INDEX`
- `KCR_CASES`
- `KC_CASES`
- `LOWID_ROWS`
- `M0_ROWS`
- `MAILBOX`
- `MAILBOX_FILE`
- `MODELS`
- `MODULES`
- `NEG_LOW`
- `NULL_SV_REL`
- `N_LADDER`
- `P1_GATED`
- `PAIRS`
- `POWER`
- `PROCESS`
- `PROJECT_ROOT`
- `PROTOCOL_FILE`
- `PROTOCOL_ID`
- `PROTOCOL_SHA256`
- `RANKS`
- `REFITS`
- `REG_NAMES`
- `REG_VERSION`
- `REPO`
- `RHO`
- `ROLES`
- `SCOPE`
- `SCRATCH_ROOT`
- `SITES`
- `SPLITS`
- `SPLIT_BLOCKS`
- `STORE`
- `TEST_K`
- `T_COND_MAX`
- `U_RANK`
- `U_SV_RATIO`
- `VAL_ALPHA`
- `VARIANTS`
- `WORKTREE`
- `X6ZC_STORE`
- `_DC`
- `_PROTO`
- `_RK`
- `_T`
- `_TL`
- `_WANT`

## Classes and functions

- **function `load_contract`** [L49-56]: `def load_contract(path=CONTRACT_PATH) -> dict` - CONTRACT.json (utf-8); ValueError unless it names the C2ND protocol sha256.
- **function `frac`** [L64-66]: `def frac(s) -> Fraction` - The exact rational a CONTRACT string names ("1/300", "1e-9", "6").
- **function `status_of`** [L69-70]: `def status_of(full) -> tuple`
- **function `seed`** [L73-74]: `def seed(name) -> int`
- **function `rank`** [L77-79]: `def rank(draws, p) -> int` - The rank ceil(draws * p) of c1_means.rank_for.
- **function `ranks`** [L135-137]: `def ranks(draws, alpha) -> tuple` - (rank of the lower bound, rank of the upper bound) of `draws` at level `alpha`.

