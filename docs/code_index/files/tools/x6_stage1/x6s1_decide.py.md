# `tools/x6_stage1/x6s1_decide.py`

- Source: [tools/x6_stage1/x6s1_decide.py](../../../../../tools/x6_stage1/x6s1_decide.py)
- Kind: python
- Lines: 289

## Module docstring

> X6S1 decide: learnability, C-ORD, SHARP/TARGET, readout and placebo checks, ordD, per-seed
> flags, the ordered decision rules, qualifiers, licence sentences and the report (X6S1-FROZEN-v1
> §2.5-§2.7, §3, §4.7, §7.6, §7.9, §11.4; API.md §9). Inputs are plain dicts; a missing or INVALID
> model is None and fails every per-seed condition. Import performs no I/O.

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 20, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `decimal` (lines 11)
- `fractions` (lines 12)
- `math` (lines 9)
- `pathlib` (lines 13)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 19: `[str(p) for p in _EXTRA if str(p) not in sys.path]` -> `tests/oracle_profile`, `tools/c1prime_registry`, `tools/d2a`, `tools/k4b`, `tools/x4_oracle_profile`, `tools/x6_stage0`, `tools/x6_stage1`

## Imported by

- [tests/x6_stage1/test_a_numerics.py](../../tests/x6_stage1/test_a_numerics.py.md) (line 26, import)
- [tests/x6_stage1/test_a_rules.py](../../tests/x6_stage1/test_a_rules.py.md) (line 20, import)
- [tools/x6_stage1/x6s1_stage_post.py](x6s1_stage_post.py.md) (line 22, import)

## Top-level constants

- `REPO`
- `SEEDS`
- `_DES`
- `_EXTRA`
- `_NAT`
- `_NONE`
- `_REG`
- `_RULE1`
- `_TEXT`
- `_UNRES`

## Classes and functions

- **function `_fin`** [L26-30]: `def _fin(x) -> bool`
- **function `_fr`** [L33-35]: `def _fr(x) -> Fraction`
- **function `_dec_fr`** [L38-43]: `def _dec_fr(U)`
- **function `learned_val`** [L47-52]: `def learned_val(ub, g8_lo, nonfinite=False) -> str`
- **function `learn_decision`** [L55-58]: `def learn_decision(status_s1, status_s2) -> str`
- **function `learned_test`** [L61-65]: `def learned_test(U, g8_lo) -> str`
- **function `ctrl`** [L69-73]: `def ctrl(b_init, b_ab, b_zc)`
- **function `cord`** [L76-81]: `def cord(mean, lb, adjusted, tail_status, resolved) -> str`
- **function `sharp_target`** [L84-89]: `def sharp_target(U, g0_lo) -> dict`
- **function `cue_ok`** [L92-93]: `def cue_ok(median) -> bool`
- **function `placebo_natural`** [L96-98]: `def placebo_natural(betas) -> dict`
- **function `_defined`** [L102-104]: `def _defined(d, keys) -> bool`
- **function `ord_d`** [L107-128]: `def ord_d(na, init, ab, zc, dw2_lo) -> dict`
- **function `seed_flags`** [L132-139]: `def seed_flags(adj, lb_adj, U025, xbar, hw95, g0_lo) -> dict`
- **function `designed_counts`** [L142-145]: `def designed_counts(statuses) -> dict`
- **function `decide`** [L156-186]: `def decide(ev) -> dict`
- **function `_models`** [L190-191]: `def _models(d, pred) -> list`
- **function `qualifiers`** [L194-229]: `def qualifiers(ev) -> list`
- **function `licence`** [L279-281]: `def licence(outcome, values) -> str`
- **function `report`** [L284-289]: `def report(ev, values) -> dict`

