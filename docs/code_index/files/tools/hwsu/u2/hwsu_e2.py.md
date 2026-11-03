# `tools/hwsu/u2/hwsu_e2.py`

- Source: [tools/hwsu/u2/hwsu_e2.py](../../../../../../tools/hwsu/u2/hwsu_e2.py)
- Kind: python
- Lines: 239

## Module docstring

> HWSU E2 gates: RELEASE-B, S7, H2-FRESH-U, T-PRE, NUM, ENDPOINT, SEALED_OPENED and the report
> (API_U2.md sections 4.3-4.8). Split from hwsu_gates by size (API erratum); every name stays
> reachable as hwsu_gates.<name>. Response family only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 8, via unique basename)
- `import hwsu_decide` -> [tools/hwsu/u2/hwsu_decide.py](hwsu_decide.py.md) (line 9, via same directory)
- `import hwsu_gates` -> [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 10, via same directory)
- `import hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 11, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../hwsu_oracle.py.md) (line 12, via unique basename)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 13, via same directory)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../hwsu_pairs.py.md) (line 14, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 15, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 16, via same directory)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 17, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../c1prime/c1_means.py.md) (line 22, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../c1prime/c1_oracle.py.md) (line 23, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../c2_readout/c2_decide.py.md) (line 24, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../../c2_readout/c2_model.py.md) (line 25, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../../hwsc/hwsc_records.py.md) (line 26, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 29, via unique basename)

### External (third-party)

- `numpy` (lines 27)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 19)
- `json` (lines 18)
- `pathlib` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 51, dynamic)

## Top-level constants

- none

## Classes and functions

- **function `_sha`** [L34-35]: `def _sha(out, rel) -> str`
- **function `release_b_check`** [L38-55]: `def release_b_check(out, ctx) -> dict`
- **function `sample_e2`** [L58-81]: `def sample_e2(out, ctx) -> dict`
- **function `h2_fresh`** [L84-88]: `def h2_fresh(ctx) -> dict`
- **function `_tpre_models`** [L91-120]: `def _tpre_models(ctx, pol) -> dict` - M0 (arm 1) and X1 (natural arms) on the 1,024 lowest-id test pairs; ephemeral logits.
- **function `t_pre`** [L123-149]: `def t_pre(out, ctx) -> dict`
- **function `num_gate`** [L152-180]: `def num_gate(out, ctx) -> dict`
- **function `sealed_opened`** [L183-187]: `def sealed_opened(out, ctx) -> Path`
- **function `endpoint`** [L190-216]: `def endpoint(out, ctx) -> dict`
- **function `report_u`** [L219-239]: `def report_u(out, ctx, records) -> Path`

