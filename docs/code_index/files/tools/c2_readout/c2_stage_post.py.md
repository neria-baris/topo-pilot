# `tools/c2_readout/c2_stage_post.py`

- Source: [tools/c2_readout/c2_stage_post.py](../../../../../tools/c2_readout/c2_stage_post.py)
- Kind: python
- Lines: 368

## Module docstring

> C2 stage body S5 (R-0104-1; API.md §19.2, §19.3; C2-FROZEN-v2 §3, §5.7, §6.2-§6.5, §7 rows
> 21-28, §8 S4/S5/S8): ACCEPT, REG2, T-PRE, T-PRE-MODEL, RESP-SPEC, NUM, ENDPOINT, REPORT (with the
> §2.12 descriptives and POST-DESC). Endpoint arrays exist only for admitted models and only after
> T-PRE (NEW-6); the sealed VAL values are opened only in REPORT, after every outcome.

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 10, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 13, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 14, via same directory)
- `import c2_data` -> [tools/c2_readout/c2_data.py](c2_data.py.md) (line 15, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](c2_decide.py.md) (line 16, via same directory)
- `import c2_driver` -> [tools/c2_readout/c2_driver.py](c2_driver.py.md) (line 17, via same directory)
- `import c2_model` -> [tools/c2_readout/c2_model.py](c2_model.py.md) (line 18, via same directory)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 19, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](c2_registry.py.md) (line 20, via same directory)
- `import c2_stage_base` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 21, via same directory)
- `import c2_stage_pre` -> [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 22, via same directory)
- `import c2_stage_val` -> [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 23, via same directory)
- `from c2_stage_base import EXC, FAM, OK, X3, alive, bundle, fitb, js, orc, prob, rec` -> [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 25, via same directory)
- `from c2_stage_val import sg` -> [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 26, via same directory)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 8)

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

- `PLAN`
- `SEED`
- `SPEC`
- `TEST_GATE`

## Classes and functions

- **function `_on`** [L33-35]: `def _on(ctx, fam, j) -> bool`
- **function `_E`** [L38-39]: `def _E(ctx, p, split='test') -> np.ndarray`
- **function `tb`** [L42-43]: `def tb(arrays, guards, fam, draws=cc.TEST_DRAWS) -> dict`
- **function `accept`** [L47-50]: `def accept(ctx) -> dict`
- **function `reg2`** [L53-60]: `def reg2(ctx) -> dict` - R' = R u U_FIT u U_FEAS u U_VAL rebuilt (C-10); then k TEST blocks sampled once, with the
- **function `t_pre`** [L63-97]: `def t_pre(ctx) -> dict` - §7 row 23 in order; FAIL_TECHNICAL ends it at once, unmet criteria give TEST_GATE.
- **function `t_pre_model`** [L100-118]: `def t_pre_model(ctx) -> dict` - §7 row 24: Sup(TEST), L1 and R1 with the frozen FIT decoders, N2 (M); TEST tallies.
- **function `first`** [L122-135]: `def first(ctx, j, fam) -> tuple` - V3x and the SPEC array (first part of the family stream; no endpoint array).
- **function `keyed`** [L138-140]: `def keyed(per_model) -> tuple`
- **function `_split`** [L143-144]: `def _split(b, j) -> dict`
- **function `resp_spec`** [L147-163]: `def resp_spec(ctx) -> dict`
- **function `stream`** [L166-186]: `def stream(ctx, j, fam) -> tuple` - The whole family stream of one admitted model (§11.1), its guards (§9.2; M: C-44) and the
- **function `num`** [L189-208]: `def num(ctx) -> dict` - Form the admitted models' endpoint arrays (policy: test_endpoint) and record every
- **function `endpoint`** [L212-245]: `def endpoint(ctx) -> dict`
- **function `quantities`** [L249-260]: `def quantities(ctx, j, fam) -> dict` - x-pair quantities of one model for POST-DESC (formed only now, after every outcome).
- **function `post_desc`** [L263-273]: `def post_desc(ctx, G, stop)`
- **function `lic_values`** [L276-306]: `def lic_values(ctx, fam, outcome, pm, G, act) -> dict` - The §3 bracket values (B3): the claim models and their count from the generic category,
- **function `report`** [L309-362]: `def report(ctx) -> dict` - Always runs (S4: values kept). Statuses, licences, unsealed VAL values, coverage,

