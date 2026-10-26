# `tools/c2_readout/c2_stage_pre.py`

- Source: [tools/c2_readout/c2_stage_pre.py](../../../../../tools/c2_readout/c2_stage_pre.py)
- Kind: python
- Lines: 307

## Module docstring

> C2 stage bodies S1-S3 (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §5, §6.6, §7 rows 0-16, §8):
> PLAN["S1"], PLAN["S2"], PLAN["S3"] in §7 order. A step fn(ctx) returns {"status", "values"} or
> per-line "records"; c2_driver records them through run_gate inside the policy. FEAS reads no
> logit; FIT logits only on the M0 rows (§5.7).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 13, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 16, via unique basename)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../c1prime/c1_fit.py.md) (line 17, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 18, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 19, via same directory)
- `import c2_code` -> [tools/c2_readout/c2_code.py](c2_code.py.md) (line 20, via same directory)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 21, via same directory)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 22, via same directory)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 23, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](c2_registry.py.md) (line 24, via same directory)
- `import c2_stage_base` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 25, via same directory)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](c2_stats.py.md) (line 26, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 28, via unique basename)
- `from c2_stage_base import EXC, FAM, J1, X3, alive, frac, js, orc, proc, put, putj, rec, table` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 29, via same directory)

### External (third-party)

- `numpy` (lines 27)

### Standard library

- `__future__` (lines 6)
- `os` (lines 8)
- `pathlib` (lines 11)
- `subprocess` (lines 9)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 22, import)

## Top-level constants

- `PLAN`
- `S1`
- `S3`
- `SUITES`

## Classes and functions

- **function `impl`** [L35-38]: `def impl(ctx) -> dict`
- **function `pf`** [L45-62]: `def pf(ctx) -> dict` - §12.3 unchanged (moved from c2_driver, API.md §19.2); the E-0102-2 file-size scope.
- **function `h1`** [L65-67]: `def h1(ctx) -> dict`
- **function `reg`** [L70-74]: `def reg(ctx) -> dict`
- **function `h2`** [L77-78]: `def h2(ctx) -> dict`
- **function `oracle_splits`** [L81-94]: `def oracle_splits(ctx, splits, smax=None) -> tuple` - The four-role oracle of each split from the H2 / H2' cache (H^Y on Y_def rows only),
- **function `h3`** [L97-107]: `def h3(ctx) -> dict`
- **function `h4`** [L110-118]: `def h4(ctx) -> dict` - f_x >= 9/10 and f_y >= 17/20 on FIT, FEAS, VAL (OFF_GRID_Y rows ineligible); tally.
- **function `h5`** [L121-127]: `def h5(ctx) -> dict`
- **function `m0`** [L131-141]: `def m0(ctx) -> dict`
- **function `c0c`** [L144-159]: `def c0c(ctx) -> dict`
- **function `f1_model`** [L162-204]: `def f1_model(ctx, j, recs) -> None` - The six problems of one model, decoders, m-tilde, N2 fit, J and the affine readouts.
- **function `f1`** [L207-211]: `def f1(ctx) -> dict`
- **function `c0v`** [L215-237]: `def c0v(ctx) -> dict`
- **function `_fit_target`** [L240-242]: `def _fit_target(ctx, j, fam) -> np.ndarray`
- **function `_rff_rest`** [L245-259]: `def _rff_rest(ctx, j) -> dict` - The descriptive RFF decoder of f1 from P_rest y (C-27): FIT fit, FEAS score.
- **function `l1`** [L262-276]: `def l1(ctx) -> dict` - L1 per (model, family) on FEAS; L1_DESC.json: the complete-decoder scores and the RFF
- **function `r1`** [L279-285]: `def r1(ctx) -> dict`
- **function `n2`** [L288-289]: `def n2(ctx) -> dict`
- **function `survival`** [L292-300]: `def survival(ctx) -> dict` - Each family needs >= 2 ok models; the FEAS per-model, per-family coverage tally.

