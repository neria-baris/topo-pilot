# `tools/d2a/d2a_decide.py`

- Source: [tools/d2a/d2a_decide.py](../../../../../tools/d2a/d2a_decide.py)
- Kind: python
- Lines: 396

## Module docstring

> D-2a flags, ordered decision rules and the stage-1 / stage-3 drivers; the bootstrap primitives
> live in d2a_world and are re-exported (D2A-FROZEN-v1 §6, §10; tools/d2a/API.md §2.5, §4, §5).

## Imports

### Internal (repo files)

- `import d2a_train` -> [tools/d2a/d2a_train.py](d2a_train.py.md) (line 19, via same directory)
- `import d2a_world` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 20, via same directory)
- `from d2a_world import boot_counts, interval, quantiles, r2_from_sums` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 21, via same directory)
- `import d2a_eval` -> [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 171, via same directory) (inside a function)
- `import d2a_targets` -> [tools/d2a/d2a_targets.py](d2a_targets.py.md) (line 172, via same directory) (inside a function)
- `import d2a_eval` -> [tools/d2a/d2a_eval.py](d2a_eval.py.md) (line 342, via same directory) (inside a function)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 344, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 16)
- `torch` (lines 173, 343)

### Standard library

- `__future__` (lines 4)
- `os` (lines 6)
- `pathlib` (lines 14)
- `re` (lines 13)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(Path(__file__).resolve().parent)` -> `tools/d2a`

## Imported by

- [tests/d2a/test_b_rules_decide.py](../../tests/d2a/test_b_rules_decide.py.md) (line 23, import)
- [tests/d2a/test_b_rules_flags.py](../../tests/d2a/test_b_rules_flags.py.md) (line 25, import)
- [tests/d2a/test_b_rules_qualifiers.py](../../tests/d2a/test_b_rules_qualifiers.py.md) (line 23, import)

## Top-level constants

- none

## Classes and functions

- **function `licences`** [L26-29]: `def licences(protocol=W.PROTOCOL) -> dict` - §1.4 quoted licensed sentences, verbatim from the hash-bound frozen protocol (gate 1).
- **function `_ok`** [L32-33]: `def _ok(v) -> bool`
- **function `_n`** [L36-37]: `def _n(xs) -> int`
- **function `learned`** [L40-49]: `def learned(beta1, beta1_lo, kappa1, diff_lo, *, model_status='PRESENT') -> str` - MISSING/INVALID model → FAIL; a present model with any undefined value → UNRESOLVED (Q6).
- **function `stage1_decision`** [L52-56]: `def stage1_decision(v1, v2) -> str`
- **function `arm_value`** [L59-62]: `def arm_value(values) -> str`
- **function `carries`** [L65-66]: `def carries(d, d_lo) -> bool`
- **function `low_increment`** [L69-70]: `def low_increment(d) -> bool`
- **function `beta2_pass`** [L73-74]: `def beta2_pass(b, lo) -> bool`
- **function `precision_ok`** [L77-79]: `def precision_ok(hw_r_pi_16, hw_r_pi_28, hw_c8_16, hw_c8_28) -> bool`
- **function `_seeds_ok`** [L82-83]: `def _seeds_ok(per_seed) -> bool`
- **function `c_hor`** [L86-90]: `def c_hor(mean, p2_5, per_seed) -> str`
- **function `c_len`** [L93-100]: `def c_len(mean, p1_25, p98_75, per_seed, precision_all) -> str`
- **function `pipeline_null_ok`** [L103-104]: `def pipeline_null_ok(upper: dict) -> bool`
- **function `decide`** [L107-152]: `def decide(flags: dict) -> dict` - §10.5 ordered rules (first match) and the outcome-4–10 qualifiers.
- **function `_lo`** [L155-156]: `def _lo(ci)`
- **function `learned_stats`** [L159-166]: `def learned_stats(be: dict, n: int, B: int, scope) -> dict` - β₁, its interval, β₁⁽⁸⁾, κ₁ and the paired lower bound of β₁ − β₁⁽⁸⁾ (§6).
- **function `stage1_main`** [L169-211]: `def stage1_main(store_root=W.STORE) -> str` - CLI ``stage1``: learnability gate on val for H3-s1, H3-s2 (§6) plus descriptive R_π.
- **function `model_flags`** [L214-258]: `def model_flags(mid, P, data, B=2000) -> dict` - Primary per-model statistics with paired draws: R_X, ctrl_X, R_X − ctrl_X (§10.1-10.3).
- **function `confirmatory`** [L261-284]: `def confirmatory(P, data, B=20000) -> dict` - C-HOR and C-LEN: the four seed pairs averaged per draw, episode-cluster (§10.3-10.4).
- **function `assemble`** [L287-330]: `def assemble(F, oracle, R, stage1, conf) -> dict` - The decide() flag table from per-model statistics and validity records (API §2.5).
- **function `_save`** [L333-337]: `def _save(out: Path, name: str, rec, preds=None) -> None`
- **function `stage3_main`** [L340-392]: `def stage3_main(store_root=W.STORE) -> str` - CLI ``stage3`` (API §4): primary passes, decision, then budgeted secondary work.

