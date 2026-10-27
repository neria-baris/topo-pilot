# `tools/x6_stage0/x6_exact.py`

- Source: [tools/x6_stage0/x6_exact.py](../../../../../tools/x6_stage0/x6_exact.py)
- Kind: python
- Lines: 390

## Module docstring

> X6 stage 0: exact Fraction filter (G2), witness families, beta, challenge, 4x8 comparator
> (G3), O1/O2 (X6-FROZEN-v1 sections 4, 6.1, 8.3, 9.2; API.md 5).

## Imports

### Internal (repo files)

- `from x6_dp import CTX, certify, certify_mass, classes, entropy_decimal, kl_decimal, segment_dp` -> [tools/x6_stage0/x6_dp.py](x6_dp.py.md) (line 11, via same directory)
- `from x6_model import ANCHOR, ARMS, ARMS_SEAM, BETA_MAX, G_MIN, LADDER, M_MIN, S3_E, S3_LIST, TOL_LOG, TV_MIN, closed_form, edge_labels, holonomy, lam, model, parikh, parse, perm_name, point_law, seam_letter, statistic, tok` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 13, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 4)
- `collections` (lines 7)
- `decimal` (lines 8)
- `fractions` (lines 9)
- `itertools` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage0/test_x6_stage0.py](../../tests/x6_stage0/test_x6_stage0.py.md) (line 23, import)
- [tests/x6_stage0/test_x6_stage0_dp.py](../../tests/x6_stage0/test_x6_stage0_dp.py.md) (line 26, import)
- [tests/x6_stage1/test_a_designed.py](../../tests/x6_stage1/test_a_designed.py.md) (line 28, import)
- [tests/x6_stage1/test_a_pairs.py](../../tests/x6_stage1/test_a_pairs.py.md) (line 29, import)
- [tests/x6zc/test_x6zc_dryrun.py](../../tests/x6zc/test_x6zc_dryrun.py.md) (line 21, import)
- [tools/x6_stage0/x6_run.py](x6_run.py.md) (line 20, import)
- [tools/x6_stage0/x6_store.py](x6_store.py.md) (line 22, import)
- [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 23, import)
- [tools/x6_stage1/x6s1_registry.py](../x6_stage1/x6s1_registry.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 26, import)
- [tools/x6zc/x6zc_census.py](../x6zc/x6zc_census.py.md) (line 16, import)
- [tools/x6zc/x6zc_core.py](../x6zc/x6zc_core.py.md) (line 40, import)

## Top-level constants

- `FAMILIES`
- `LOOPS`
- `ORDERINGS`
- `P_LOOP`
- `_BAGGED`
- `_EQUAL_ROWS`
- `_PER_Y`
- `_REV`
- `_S7`
- `_SPARSE`
- `_TAILS`
- `_ZERO_SPREAD`

## Classes and functions

- **function `_rows`** [L20-23]: `def _rows(T) -> list`
- **function `_step`** [L24-34]: `def _step(Ts, E, pred: dict, w: int)` - Condition the predictive state law on w: (belief, normaliser, next predictive).
- **function `_q`** [L36-37]: `def _q(pred: dict, E) -> list`
- **function `_dense`** [L38-39]: `def _dense(b: dict, n: int) -> list`
- **function `fraction_filter`** [L40-50]: `def fraction_filter(T, E, pi, tokens) -> dict`
- **function `gate_G2`** [L52-86]: `def gate_G2(arms=ARMS_SEAM, t_max: int = 6) -> dict`
- **function `members`** [L95-96]: `def members(family: str) -> tuple`
- **function `witness_path`** [L97-104]: `def witness_path(family: str, member) -> tuple`
- **function `prefix_tokens`** [L105-106]: `def prefix_tokens(name: str, y0: int = 0) -> tuple`
- **function `witness_tokens`** [L107-109]: `def witness_tokens(family, member, y, prefix='P0', y0=0) -> tuple`
- **function `_cue_tv`** [L110-112]: `def _cue_tv(q1, q2) -> Fraction`
- **function `family_values`** [L113-135]: `def family_values(arm: str, family: str, prefix: str = 'P0', y0: int = 0) -> dict`
- **function `matched`** [L138-157]: `def matched(family: str, y: int = 0) -> dict`
- **function `rs_key`** [L159-163]: `def rs_key(S: str, tokens) -> tuple`
- **function `constant_by_keys`** [L164-166]: `def constant_by_keys(keys) -> bool`
- **function `competitor_holonomy`** [L169-179]: `def competitor_holonomy(kind: str, letters) -> tuple`
- **function `beta`** [L181-194]: `def beta(rows)`
- **function `beta_table`** [L196-215]: `def beta_table() -> dict`
- **function `family_label`** [L217-219]: `def family_label(beta_row: dict) -> str`
- **function `set_gap`** [L222-228]: `def set_gap(laws, prec: int = 80) -> Decimal`
- **function `_w3_laws`** [L229-231]: `def _w3_laws(y: int) -> dict`
- **function `challenge_values`** [L232-245]: `def challenge_values() -> dict`
- **function `block_posterior`** [L247-254]: `def block_posterior(prior: dict, likelihoods) -> dict`
- **function `block_comparator`** [L255-278]: `def block_comparator(y: int = 0) -> dict`
- **function `_cases`** [L290-294]: `def _cases()`
- **function `_ent`** [L295-296]: `def _ent(p) -> Decimal`
- **function `_close`** [L297-298]: `def _close(a: Decimal, b: Decimal) -> bool`
- **function `_window_constant`** [L299-307]: `def _window_constant(fam: str) -> bool` - Bayes k-window predictors (stationary restart) constant on the set for k <= n.
- **function `_matched_ok`** [L309-312]: `def _matched_ok(f: str, m: dict) -> bool`
- **function `gate_G3`** [L313-371]: `def gate_G3() -> dict`
- **function `o1`** [L373-382]: `def o1(g3: dict) -> dict`
- **function `o2_combine`** [L384-385]: `def o2_combine(c1: str, c2: str) -> str`
- **function `o2`** [L386-390]: `def o2(g4: dict) -> dict`

