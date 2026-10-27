# `tools/c2_readout/c2_decide.py`

- Source: [tools/c2_readout/c2_decide.py](../../../../../tools/c2_readout/c2_decide.py)
- Kind: python
- Lines: 397

## Module docstring

> C2 decisions: the family bound streams, the NUM guard, the Lemma FW per-model rules (R, S*, M),
> the coarse statements and their prerequisites, the 2-of-3 rule, endpoint statuses, qualifiers
> and the Q-CODE licence fill (API.md §11; C2-FROZEN-v1 §3, §6.2-§6.5, §9.2, §10).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 13, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 16, via unique basename)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 9)
- `re` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_family.py](../../tests/c2_nd/test_a_family.py.md) (line 25, import)
- [tests/c2_nd/test_a_known.py](../../tests/c2_nd/test_a_known.py.md) (line 25, import)
- [tests/c2_nd/test_b_layer2.py](../../tests/c2_nd/test_b_layer2.py.md) (line 25, import)
- [tests/c2_readout/test_a_inference.py](../../tests/c2_readout/test_a_inference.py.md) (line 34, import)
- [tests/c2_readout/test_a_partition.py](../../tests/c2_readout/test_a_partition.py.md) (line 35, import)
- [tests/c2_readout/test_a_scope.py](../../tests/c2_readout/test_a_scope.py.md) (line 38, import)
- [tests/c2_readout/test_b_screens.py](../../tests/c2_readout/test_b_screens.py.md) (line 23, import)
- [tools/c2_nd/nd_attrib.py](../c2_nd/nd_attrib.py.md) (line 21, import)
- [tools/c2_nd/nd_decide.py](../c2_nd/nd_decide.py.md) (line 14, import)
- [tools/c2_nd/nd_split.py](../c2_nd/nd_split.py.md) (line 18, import)
- [tools/c2_nd/nd_stage_post.py](../c2_nd/nd_stage_post.py.md) (line 19, import)
- [tools/c2_nd/nd_stage_val.py](../c2_nd/nd_stage_val.py.md) (line 15, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 23, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 16, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 16, import)

## Top-level constants

- `A_STATS`
- `CAT`
- `CLAIM`
- `M_CAT`
- `NON_EXCLUDING`
- `OUT`
- `QCODE`
- `REASON_ORDER`
- `RES_KEYS`
- `S_SUB`
- `T`
- `_GEN`
- `_M_LOW`
- `_PREFIX`
- `_R_LOW`
- `_TEXT`

## Classes and functions

- **function `stream_bounds`** [L38-46]: `def stream_bounds(arrays, seed, alpha, draws=20000) -> dict` - One shared index stream; per key the tree mean and the ranked bounds at alpha, 1 - alpha.
- **function `guard`** [L49-50]: `def guard(s, beta=0.0) -> float`
- **function `_rows`** [L53-55]: `def _rows(x, E=None)`
- **function `beta_A`** [L58-62]: `def beta_A(d, M, dy, delta_P, coef, E=None) -> float` - |coef| max_i 1/2 ||M' d_i|| delta_P ||dy_i|| (A_S-type terms).
- **function `beta_E`** [L65-72]: `def beta_E(M, dy, P_S, delta_P, coef, E=None) -> float` - |coef| max_i (2 ||C M P_S dy_i|| + ||CM|| delta_P ||dy_i||) ||CM|| delta_P ||dy_i||.
- **function `sign`** [L75-76]: `def sign(b, g) -> int`
- **function `stream_guards`** [L79-92]: `def stream_guards(arrays, geo) -> dict` - Guards of one R/S* stream; geo: M, x/y = (d, dy, E), proj = {prefix: (P_S, delta_P)}.
- **function `model_bounds`** [L95-99]: `def model_bounds(res, guards, model) -> dict` - The stream_bounds entries of one model keyed by statistic, each with its guard.
- **function `_sg`** [L103-104]: `def _sg(b, stat, side) -> int`
- **function `_category`** [L107-115]: `def _category(b, z1, z5, energy) -> str`
- **function `_unresolved`** [L118-119]: `def _unresolved(b) -> list`
- **function `_result`** [L125-127]: `def _result(b, status, resp, spec, coarse, formed) -> dict`
- **function `_gate`** [L130-134]: `def _gate(b, spec_stat, y_active) -> tuple`
- **function `r_model`** [L137-145]: `def r_model(b, y_active) -> dict` - R and S* rules 1-5; NEGATIVE and the coarse statements only after RESP and SPEC.
- **function `m_model`** [L148-161]: `def m_model(b, y2_active) -> dict` - M rules 1-7: RESP, Y2, ROUTED first, the UPSTREAM categories, INC (E-7).
- **function `variant_category`** [L164-171]: `def variant_category(b, variant, primary) -> str` - The R category rule on the variant arrays, with the primary RESP/SPEC prerequisites.
- **function `_generic`** [L175-179]: `def _generic(family, status) -> str | None`
- **function `overall`** [L182-202]: `def overall(family, statuses, cnhs) -> str` - §6.5: study failure; >= 2 CNHS; fewer than 2 valid models -> INCONCLUSIVE/<the reason of
- **function `_applies`** [L205-209]: `def _applies(rec, model, family) -> bool`
- **function `endpoint_status`** [L212-229]: `def endpoint_status(model, family, gate_history) -> str` - SCORED; NOT_RUN/<gate> for the first applicable stop (exclusion before ACCEPT, T-PRE,
- **function `qualifiers`** [L236-258]: `def qualifiers(family, per_model, variants, y_active, p1) -> list` - The §3.1 qualifiers in the API.md §2 order, models ascending within each kind.
- **function `_fmt`** [L363-368]: `def _fmt(x) -> str`
- **function `_key`** [L371-378]: `def _key(family, outcome) -> str`
- **function `licence`** [L381-397]: `def licence(family, outcome, values) -> str` - The §3 sentence, [name] filled (absent: "[ ]"), then the §3.2 caveats (M) and Q-CODE.

