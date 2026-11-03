# `tools/hwsu/u2/hwsu_gates.py`

- Source: [tools/hwsu/u2/hwsu_gates.py](../../../../../../tools/hwsu/u2/hwsu_gates.py)
- Kind: python
- Lines: 372

## Module docstring

> HWSU E1 gates, share-family stubs and the validation report (API_U2.md section 4.1, 4.7, 4.9).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 10, via unique basename)
- `import hwsu_decide` -> [tools/hwsu/u2/hwsu_decide.py](hwsu_decide.py.md) (line 11, via same directory)
- `import hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 12, via same directory)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 13, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../hwsu_of.py.md) (line 14, via unique basename)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../hwsu_oracle.py.md) (line 15, via unique basename)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../hwsu_pairs.py.md) (line 16, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 17, via unique basename)
- `import hwsu_registry` -> [tools/hwsu/u2/hwsu_registry.py](hwsu_registry.py.md) (line 18, via same directory)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 19, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../c1prime/c1_means.py.md) (line 25, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../../c2_readout/c2_config.py.md) (line 26, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../c2_readout/c2_decide.py.md) (line 27, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../../hwsc/hwsc_data.py.md) (line 28, via unique basename)
- `import hwsc_records` -> [tools/hwsc/hwsc_records.py](../../hwsc/hwsc_records.py.md) (line 29, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../k4b/k4b_data.py.md) (line 30, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 32, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 33, via unique basename)

### External (third-party)

- `numpy` (lines 31)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 22)
- `importlib` (lines 20)
- `json` (lines 21)
- `pathlib` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 51: `hwsu_e2` -> [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md)

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_b_u2_records.py](../../../tests/hwsu/test_b_u2_records.py.md) (line 31, dynamic)
- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md) (line 10, import)

## Top-level constants

- `FAIL`
- `SPLIT`

## Classes and functions

- **function `of_hist`** [L42-45]: `def of_hist(dry=False) -> list`
- **function `__getattr__`** [L49-52]: `def __getattr__(name)`
- **function `_missing`** [L55-56]: `def _missing(name)`
- **function `share_dropped`** [L59-61]: `def share_dropped(ctx=None) -> dict`
- **function `share_family`** [L64-65]: `def share_family(*args, **kwargs)`
- **function `qsum_tol`** [L71-72]: `def qsum_tol() -> Fraction`
- **function `_handoff`** [L75-76]: `def _handoff(ctx) -> dict`
- **function `ensure_proc`** [L79-82]: `def ensure_proc(ctx) -> dict`
- **function `register_new`** [L85-96]: `def register_new(out, stage, rel_dir) -> list` - STAGE_COMPLETE for every file of rel_dir not yet recorded (registry files, J10 lineage).
- **function `g0u_e1`** [L100-110]: `def g0u_e1(out, ctx) -> dict`
- **function `h1_u`** [L113-133]: `def h1_u(out, ctx) -> dict`
- **function `reg1`** [L136-156]: `def reg1(out, ctx) -> dict`
- **function `_table_files`** [L160-167]: `def _table_files(out, dry, order) -> list`
- **function `sample_e1`** [L170-192]: `def sample_e1(out, ctx) -> dict`
- **function `h2_check`** [L195-208]: `def h2_check(ctx, tables, kreg, rows) -> dict` - Separation from the registry, sealed-D-2a predicate, registry risk (H2-U, H2-FRESH-U).
- **function `h2_u`** [L211-217]: `def h2_u(ctx) -> dict`
- **function `h3_split`** [L220-247]: `def h3_split(ctx, a1, a2, label) -> dict` - OF-1 (i)-(v) on one pair split plus the sum of q (H3-U, T-PRE).
- **function `h3_u`** [L250-263]: `def h3_u(ctx) -> dict`
- **function `h5_bounds`** [L266-270]: `def h5_bounds(G, seed, alpha) -> dict`
- **function `h5_u`** [L273-286]: `def h5_u(ctx) -> dict`
- **function `basis_step`** [L290-294]: `def basis_step(ctx) -> dict`
- **function `m0_step`** [L297-300]: `def m0_step(ctx) -> dict`
- **function `x1_step`** [L303-304]: `def x1_step(ctx) -> dict`
- **function `kc_u`** [L307-318]: `def kc_u(ctx) -> dict`
- **function `model_A`** [L321-330]: `def model_A(ctx, a1, a2, d_canon) -> tuple` - A_full per model from the readout coordinates (closed form; no logit).
- **function `p1_step`** [L333-354]: `def p1_step(out, ctx) -> dict`
- **function `validation_report`** [L357-371]: `def validation_report(out, ctx, records) -> Path`

