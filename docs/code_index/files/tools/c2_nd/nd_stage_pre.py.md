# `tools/c2_nd/nd_stage_pre.py`

- Source: [tools/c2_nd/nd_stage_pre.py](../../../../../tools/c2_nd/nd_stage_pre.py)
- Kind: python
- Lines: 303

## Module docstring

> C2ND stage bodies S1-S3 (API.md §9.3, §10; C2ND-DESIGN-v1 §3 rows 0-18, §6) in §3 order,
> the decoy builder and the split-level helpers reused by S4, S5 and T-PRE (sampling, oracle,
> L1, R1, N2, support, H5). DFEAS reads no logit; DFIT logits only on the M0/M0-D rows (L2).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 13, via same directory)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 16, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../c2_readout/c2_code.py.md) (line 17, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 18, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 19, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 20, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 21, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 22, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 23, via same directory)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](nd_decoy.py.md) (line 24, via same directory)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 25, via same directory)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 26, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 27, via same directory)
- `from nd_split import build_decoys, h3_run, h5_bounds, l1_check, m0_rows, move_T, n2_check, r1_check, sample, support, w32` -> [tools/c2_nd/nd_split.py](nd_split.py.md) (line 29, via same directory)
- `from nd_stage_base import EXC, bundle, c2fit, npz, orc, proc, put, putj, rec` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 42, via same directory)

### External (third-party)

- `numpy` (lines 28)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `os` (lines 7)
- `pathlib` (lines 11)
- `subprocess` (lines 8)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_dry_hs.py](../../tests/c2_nd/test_b_dry_hs.py.md) (line 33, import)
- [tests/c2_nd/test_impl_dry_hs.py](../../tests/c2_nd/test_impl_dry_hs.py.md) (line 37, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 29, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 22, import)

## Top-level constants

- `ENTRY`
- `PLAN`
- `S1`
- `S2`
- `S3`
- `SUITES`

## Classes and functions

- **function `auth_admit`** [L48-52]: `def auth_admit(ctx) -> dict`
- **function `g0_step`** [L55-57]: `def g0_step(ctx) -> dict`
- **function `impl`** [L60-65]: `def impl(ctx) -> dict`
- **function `pf`** [L72-87]: `def pf(ctx) -> dict` - API.md §9.3; the basetemp has a test_ component (§20.4 row-9 trap).
- **function `h1`** [L90-92]: `def h1(ctx) -> dict`
- **function `reg_files`** [L95-98]: `def reg_files(ctx, version) -> None`
- **function `reg`** [L101-106]: `def reg(ctx) -> dict`
- **function `h2`** [L109-110]: `def h2(ctx) -> dict`
- **function `h3`** [L113-115]: `def h3(ctx) -> dict`
- **function `h4`** [L118-123]: `def h4(ctx) -> dict` - f_x >= 9/10, f_y >= 17/20 on DFIT, DFEAS, DVAL (frozen s_max); the coverage tally.
- **function `h5`** [L126-128]: `def h5(ctx) -> dict`
- **function `oracle_feas`** [L131-145]: `def oracle_feas(ctx) -> dict` - (i) the oracle's own log-predictive gives G per DVAL row under each model's symbol
- **function `m0`** [L149-160]: `def m0(ctx) -> dict`
- **function `m0d`** [L163-186]: `def m0d(ctx) -> dict` - nd_decoy.m0d on the M0 rows; decoys/DECOY_<j>.json and decoys/HEAD_<j>.npz.
- **function `c0c`** [L189-204]: `def c0c(ctx) -> dict` - Chart sha256 (a dry-run store: the c2/ stand-in table) and Sup(DFIT) >= 0.99; DFIT
- **function `refit`** [L207-220]: `def refit(ctx, j, p, Y, aux, arr, dec) -> tuple` - One refit problem on DFIT natural rows: C2 F1 exactly, decoders, m-tilde (§3 row 13).
- **function `f1`** [L223-259]: `def f1(ctx) -> dict` - The refits R@D (y) and R@T (y @ T.T) per model (§2.8); fits/REFIT_<j>, DEC_<j>; the
- **function `sup`** [L263-268]: `def sup(ctx) -> dict`
- **function `_with_rt`** [L271-276]: `def _with_rt(ctx, check) -> dict` - The family records plus the report-only R@T records of D (problem RT; never exclude).
- **function `l1`** [L279-280]: `def l1(ctx) -> dict`
- **function `r1`** [L283-284]: `def r1(ctx) -> dict`
- **function `n2`** [L287-288]: `def n2(ctx) -> dict`
- **function `survival`** [L291-293]: `def survival(ctx) -> dict`

