# `tools/c2_nd/nd_stage_val.py`

- Source: [tools/c2_nd/nd_stage_val.py](../../../../../tools/c2_nd/nd_stage_val.py)
- Kind: python
- Lines: 362

## Module docstring

> C2ND stage body S4, DVAL (API.md §10; C2ND-DESIGN-v1 §3 rows 19-26, §4.5, §6.7 L5): X1, DX,
> V3x, V3y, Y1, V3x', Y1', V3x'-g1, KC, KC-R, P1 (p1_nd, the sealed VAL bundle, the R-0116-2
> equivalence check in the dry run), and the helpers S5 reuses (quantities of the base model and
> the decoys, X1, DX, the C2-M arms, the bound wrapper). KC, KC-R, V3x', V3x'-g1 and Y1' release
> PASS/FAIL only; method statistics use the refit projectors only (S12).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 9, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 12, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 13, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 14, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 15, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 16, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 17, via same directory)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 18, via same directory)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 19, via same directory)
- `import nd_split` -> [tools/c2_nd/nd_split.py](nd_split.py.md) (line 20, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 21, via same directory)
- `import nd_stage_pre` -> [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 22, via same directory)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 24, via unique basename)
- `from nd_stage_base import EXC, alive, bundle, orc, problem, putj, rec` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 25, via same directory)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_inference.py](../../tests/c2_nd/test_a_inference.py.md) (line 27, import)

## Top-level constants

- `C1`
- `DREF`
- `MDE`
- `PLAN`
- `S4`

## Classes and functions

- **function `x1`** [L33-34]: `def x1(ctx) -> dict`
- **function `dx`** [L37-42]: `def dx(ctx) -> dict`
- **function `v3`** [L45-57]: `def v3(ctx, pair, seed, fams, fail) -> dict` - V3x (N-R, N-M: MODEL_HEADROOM) or V3y (Y1 activity only; excludes no model), base.
- **function `v3x`** [L60-61]: `def v3x(ctx) -> dict`
- **function `v3y`** [L64-65]: `def v3y(ctx) -> dict`
- **function `y_on`** [L68-69]: `def y_on(ctx, j, key='V3y') -> bool`
- **function `_y1`** [L72-76]: `def _y1(Q) -> tuple` - Y1-type array and guard on the y pair under Q's projector (frozen C2 or RD).
- **function `y1`** [L79-89]: `def y1(ctx) -> dict`
- **function `_d_alive`** [L92-93]: `def _d_alive(ctx) -> list`
- **function `v3x_d`** [L96-116]: `def v3x_d(ctx) -> dict` - V3x' and V3y' (one call, seed 630514; ND-C4) for DNULL under RD; PASS/FAIL release.
- **function `y1_d`** [L119-138]: `def y1_d(ctx) -> dict`
- **function `v3x_g1`** [L141-154]: `def v3x_g1(ctx) -> dict` - V3x'-g1 (report-only): the unamplified decoy DNULL1 under RD; never excludes.
- **function `case_guards`** [L157-169]: `def case_guards(arrays, Q) -> dict` - KC / KC-R case guards: C2 stream_guards on the R keys; beta_A (coef 1) on the
- **function `kc_arrays`** [L172-181]: `def kc_arrays(ctx, split, j, cases) -> tuple` - (arrays, guards) keyed "<case>:<stat>|<j>" of the given cases of model j.
- **function `kc_eval`** [L184-201]: `def kc_eval(ctx, split, seed, cases, alpha=nc.VAL_ALPHA, draws=nc.VAL_DRAWS) -> dict` - {j: {case: PASS | CONTRADICTED | UNRESOLVED | NOT_COMPUTED}} (one bootstrap call).
- **function `kc`** [L204-210]: `def kc(ctx) -> dict`
- **function `kc_r`** [L213-219]: `def kc_r(ctx) -> dict`
- **function `summaries`** [L223-236]: `def summaries(arrays, r4n, models, seeds, alpha, alternative) -> dict` - The c2_stats._summaries loop with explicit integer seeds (kernels called directly).
- **function `p1_nd`** [L239-261]: `def p1_nd(family, arrays, afull_or_G, models, alpha) -> dict` - §4.5: N_F = the smallest N at which every model passes every gated array, else the
- **function `_same`** [L264-271]: `def _same(a, b) -> bool` - Bitwise equality of nested summaries (arrays by dtype, shape and bytes).
- **function `p1_equivalence`** [L274-279]: `def p1_equivalence(arrays, afull, models, alpha) -> dict` - R-0116-2: the direct kernel path with C2's seeds reproduces c2_stats._summaries.
- **function `_fam_arrays`** [L282-294]: `def _fam_arrays(ctx, fam, j) -> tuple` - (stream arrays, P1 base array, sealed quantities) of one family and model on DVAL.
- **function `_bnd`** [L301-302]: `def _bnd(b) -> dict`
- **function `p1`** [L305-356]: `def p1(ctx) -> dict`

