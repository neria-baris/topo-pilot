# `tools/k4b/k4b_stats.py`

- Source: [tools/k4b/k4b_stats.py](../../../../../tools/k4b/k4b_stats.py)
- Kind: python
- Lines: 218

## Module docstring

> K4b joint bootstrap, ranks, statuses, the precision ladder and sealing (API.md §8).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 15, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 16, via same directory)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 18, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 19, via unique basename)
- `from k4b_config import ALPHA, DRAWS, LADDER, MARGIN, MODELS, RANKS, SEEDS` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 20, via same directory)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 12)
- `hashlib` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_a_ladder.py](../../tests/hwsb/test_a_ladder.py.md) (line 33, import)
- [tests/k4b/test_a_decision.py](../../tests/k4b/test_a_decision.py.md) (line 33, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 28, import)
- [tests/k4b/test_a_width_b4.py](../../tests/k4b/test_a_width_b4.py.md) (line 29, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 31, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 29, import)
- [tools/hwsb/hwsb_dry2.py](../hwsb/hwsb_dry2.py.md) (line 23, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 22, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 24, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 33, import)

## Top-level constants

- `MIN_SUCCESSES`
- `NUMERICAL`
- `SEALED_FILE`
- `SEALED_KEYS`

## Classes and functions

- **function `joint_bootstrap`** [L30-31]: `def joint_bootstrap(arrays, seed, draws=DRAWS) -> dict`
- **function `_q`** [L34-41]: `def _q(values, p, rank) -> tuple`
- **function `bounds`** [L44-51]: `def bounds(draws_minus, draws_plus) -> dict` - L (rank 84) of the X- draws, U (rank 4,917) of the X+ draws, central 95% of both.
- **function `_fr`** [L54-58]: `def _fr(x) -> Fraction`
- **function `_status`** [L61-66]: `def _status(L, U, Fm, Fp) -> str`
- **function `model_status`** [L69-76]: `def model_status(L, U, F_minus, F_plus) -> dict` - §8.1 in exact rationals, strict inequalities; UNRESOLVED/NUMERICAL when F alone blocks.
- **function `overall`** [L79-89]: `def overall(per_model) -> str`
- **function `sd_upper`** [L92-101]: `def sd_upper(X_minus, X_plus, r4n, seed=SEEDS['val_sd']) -> dict` - SD^U per (model, side): rank-4,917 quantile of the sd draws (precision.sd_b4_draws).
- **function `mde_ok`** [L104-107]: `def mde_ok(sdU, N, F_plan) -> bool`
- **function `centered`** [L110-111]: `def centered(X_dict, keys, N, seed=SEEDS['val_projection']) -> np.ndarray`
- **function `_cols`** [L114-116]: `def _cols(e, keys, j) -> tuple`
- **function `_qa`** [L119-120]: `def _qa(col) -> float`
- **function `_qb`** [L123-124]: `def _qb(col) -> float`
- **function `projection`** [L127-143]: `def projection(e, keys, F_plan) -> dict` - §7.2(2) in float: SUPPORT and EXCLUSION success counts, per model and joint.
- **function `width_diagnostic`** [L146-156]: `def width_diagnostic(D_bar, e, keys, F_plan) -> dict` - §7.6 (report only): [D + e+ + q(e+) + F < 0.01] and [-D + e- + q(e-) - F > -0.01].
- **function `ladder`** [L159-176]: `def ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict` - First N of LADDER with mde_ok and projection ok; else INCONCLUSIVE/UNDERPOWERED.
- **function `_means`** [L179-182]: `def _means(x)`
- **function `write_sealed`** [L185-192]: `def write_sealed(out, arrays) -> str` - The only writer of SEALED_VALIDATION.json (exclusive create, once); returns its sha256.
- **function `check_unsealed`** [L195-204]: `def check_unsealed(report) -> None` - Refuse any SEALED_KEYS key anywhere in a validation report (recursive).
- **function `_ratio`** [L207-212]: `def _ratio(num, den)`
- **function `ratios`** [L215-218]: `def ratios(mean_X_minus, B4, delta4_orc_mean) -> dict` - E X-/B4 (B4 = fresh_b4["point"], R20) and E X-/Delta4_orc; descriptive only (§9.6-9.7).

