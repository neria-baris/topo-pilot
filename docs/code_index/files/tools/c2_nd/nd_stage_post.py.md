# `tools/c2_nd/nd_stage_post.py`

- Source: [tools/c2_nd/nd_stage_post.py](../../../../../tools/c2_nd/nd_stage_post.py)
- Kind: python
- Lines: 392

## Module docstring

> C2ND stage body S5 (API.md §10, §14.2; C2ND-DESIGN-v1 §3 rows 27-34, §4, §7, §8): ACCEPT,
> REG2, T-PRE, T-PRE-MODEL, RESP-SPEC, NUM, ENDPOINT, REPORT (licences, unsealing, descriptives,
> POST-DESC). Endpoint arrays exist only for admitted models and only after T-PRE; RESP/SPEC run
> first on each family stream, then the endpoint arrays with the same seed and rows (T-BOOT).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 13, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 16, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 17, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 18, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 19, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 20, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 21, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 22, via same directory)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](nd_decide.py.md) (line 23, via same directory)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](nd_decoy.py.md) (line 24, via same directory)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 25, via same directory)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 26, via same directory)
- `import nd_split` -> [tools/c2_nd/nd_split.py](nd_split.py.md) (line 27, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 28, via same directory)
- `import nd_stage_pre` -> [tools/c2_nd/nd_stage_pre.py](nd_stage_pre.py.md) (line 29, via same directory)
- `from nd_stage_base import EXC, OK, alive, js, orc, problem, put, putj, rec` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 32, via same directory)

### External (third-party)

- `numpy` (lines 30)
- `torch` (lines 31)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 10)
- `pathlib` (lines 11)
- `platform` (lines 8)
- `time` (lines 9)

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

- `FLAGS`
- `PLAN`
- `T0`

## Classes and functions

- **function `y_on`** [L39-42]: `def y_on(ctx, fam, j) -> bool`
- **function `tb`** [L45-46]: `def tb(arrays, guards, fam) -> dict`
- **function `keyed`** [L49-51]: `def keyed(per_model) -> tuple`
- **function `accept`** [L55-58]: `def accept(ctx) -> dict`
- **function `reg2`** [L61-69]: `def reg2(ctx) -> dict` - R'_ND = R_ND rebuilt now plus U_DFIT, U_DFEAS, U_DVAL (§6.4); then k DTEST blocks.
- **function `t_pre`** [L72-111]: `def t_pre(ctx) -> dict` - §3 row 29 in order; FAIL_TECHNICAL ends it at once, unmet criteria give TEST_GATE; X1
- **function `t_pre_model`** [L114-132]: `def t_pre_model(ctx) -> dict` - §3 row 30: Sup(DTEST), L1 and R1 with the frozen decoders (C2 R, RD, M; RT report-only),
- **function `first`** [L136-146]: `def first(ctx, j, fam) -> tuple` - V3x and the SPEC array (Y1; Y1' for D; none for N-M): the first part of the stream.
- **function `stream`** [L149-175]: `def stream(ctx, j, fam) -> tuple` - (arrays, guards, quantities) of the whole family stream of one admitted model.
- **function `resp_spec`** [L178-189]: `def resp_spec(ctx) -> dict`
- **function `num`** [L192-206]: `def num(ctx) -> dict` - Form the admitted models' endpoint arrays; record every bound inside its guard.
- **function `_kc_extra`** [L210-221]: `def _kc_extra(ctx) -> dict` - KC-R contradictions (S4 records) and the DTEST report-only KC / KC-R categories (seed
- **function `endpoint`** [L224-261]: `def endpoint(ctx) -> dict`
- **function `_descriptives`** [L265-293]: `def _descriptives(ctx) -> dict` - lambda_D, eta_comp, iota_M and the LN-scale shares with intervals (seed 630508).
- **function `post_desc`** [L296-313]: `def post_desc(ctx, G, stop)` - C2 §5.7: unlicensed point ratios for the models stopped at T-PRE or RESP-SPEC.
- **function `report`** [L316-386]: `def report(ctx) -> dict` - Always runs. Statuses, licences, rule-6 statements, unsealed VAL values, decoys, leak,

