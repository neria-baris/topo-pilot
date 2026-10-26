# `tools/c2_readout/c2_config.py`

- Source: [tools/c2_readout/c2_config.py](../../../../../tools/c2_readout/c2_config.py)
- Kind: python
- Lines: 192

## Module docstring

> C2 configuration: bindings, paths, CONTRACT.json loading, constants, exact Fraction levels
> and ranks, seeds, and the sys.path convention (API.md §1, §3, §19.3; C2-FROZEN-v2 §5.2, §6.2,
> §9.1, §21).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](../c1prime/c1_config.py.md) (line 35, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 36, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 15)
- `json` (lines 12)
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

- line 33: `[str(p) for p in _PATHS if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime`, `tools/c1prime_registry`, `tools/c2_readout`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`, `tools/x6_stage1`

## Imported by

- [tests/c2_nd/test_b_lineage.py](../../tests/c2_nd/test_b_lineage.py.md) (line 20, import)
- [tests/c2_readout/test_a_gls.py](../../tests/c2_readout/test_a_gls.py.md) (line 29, import)
- [tests/c2_readout/test_a_inference.py](../../tests/c2_readout/test_a_inference.py.md) (line 31, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 31, import)
- [tests/c2_readout/test_a_partition.py](../../tests/c2_readout/test_a_partition.py.md) (line 30, import)
- [tests/c2_readout/test_a_readout.py](../../tests/c2_readout/test_a_readout.py.md) (line 27, import)
- [tests/c2_readout/test_a_scope.py](../../tests/c2_readout/test_a_scope.py.md) (line 35, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../tests/c2_readout/test_b_fwl_l1.py.md) (line 21, import)
- [tests/c2_readout/test_b_lineage.py](../../tests/c2_readout/test_b_lineage.py.md) (line 23, import)
- [tests/c2_readout/test_b_patch.py](../../tests/c2_readout/test_b_patch.py.md) (line 24, import)
- [tests/c2_readout/test_b_policy.py](../../tests/c2_readout/test_b_policy.py.md) (line 23, import)
- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 22, import)
- [tests/c2_readout/test_b_screens.py](../../tests/c2_readout/test_b_screens.py.md) (line 20, import)
- [tools/c2_nd/nd_config.py](../c2_nd/nd_config.py.md) (line 24, import)
- [tools/c2_nd/nd_data.py](../c2_nd/nd_data.py.md) (line 17, import)
- [tools/c2_nd/nd_decoy.py](../c2_nd/nd_decoy.py.md) (line 22, import)
- [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 16, import)
- [tools/c2_readout/c2_code.py](c2_code.py.md) (line 14, import)
- [tools/c2_readout/c2_data.py](c2_data.py.md) (line 19, import)
- [tools/c2_readout/c2_decide.py](c2_decide.py.md) (line 13, import)
- [tools/c2_readout/c2_driver.py](c2_driver.py.md) (line 19, import)
- [tools/c2_readout/c2_model.py](c2_model.py.md) (line 14, import)
- [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 16, import)
- [tools/c2_readout/c2_registry.py](c2_registry.py.md) (line 18, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 13, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 10, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 13, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 10, import)
- [tools/c2_readout/c2_stats.py](c2_stats.py.md) (line 20, import)

## Top-level constants

- `ADDENDUM1_SHA256`
- `ADDENDUM2_SHA256`
- `ALPHA`
- `ARTIFACT_ROOT`
- `AUTH_PATH`
- `AUTH_SHA256`
- `BASE_COMMIT`
- `BLOCK`
- `C0V_SUPPORT`
- `C1P_STORE`
- `CONTRACT`
- `CONTRACT_PATH`
- `DESC_ALPHA`
- `E_RAND`
- `FAMILIES`
- `FILE_FAMILY`
- `F_DRIFT`
- `H4`
- `H5_ALPHA`
- `HERE`
- `HOOK_KEYS`
- `K4_FREEZE`
- `MAILBOX`
- `MODELS`
- `MODULES`
- `N_LADDER`
- `OWNER23_SHA256`
- `PAIRS`
- `POWER`
- `PROBLEMS`
- `PROCESS`
- `PROJECT_ROOT`
- `PROTOCOL_FILE`
- `PROTOCOL_ID`
- `PROTOCOL_SHA256`
- `RANKS`
- `RANK_R`
- `REG_VERSION`
- `REPO`
- `RIDGE_GRID`
- `ROLES`
- `ROT_DOSES`
- `R_COMMIT`
- `SCOPE`
- `SCRATCH_ROOT`
- `SITES`
- `SPLIT_BLOCKS`
- `STORE`
- `TEST_K`
- `T_DEC_POST`
- `T_SYM`
- `UNIT_ROUNDOFF`
- `V1_SHA256`
- `VAL_ALPHA`
- `VARIANTS`
- `WORKTREE`
- `X6S1_STORE`
- `Y_MID`
- `_BS`
- `_LV`
- `_PATHS`
- `_RK`
- `_T`
- `_TL`

## Classes and functions

- **function `load_contract`** [L61-68]: `def load_contract(path=CONTRACT_PATH) -> dict` - CONTRACT.json (utf-8); ValueError unless it names the frozen protocol sha256.
- **function `frac`** [L78-80]: `def frac(s) -> Fraction` - The exact rational a CONTRACT string names ("1/240", "1e-9", "0.75").
- **function `chart_cfg`** [L83-85]: `def chart_cfg() -> dict` - The C1' CONTRACT chart block (f8df2e43...a379), unchanged.
- **function `status_of`** [L88-89]: `def status_of(full) -> tuple`
- **function `seed`** [L92-93]: `def seed(name) -> int`
- **function `ranks`** [L130-132]: `def ranks(draws, alpha) -> tuple` - (rank of the lower bound, rank of the upper bound) of `draws` at level `alpha`.

