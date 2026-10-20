# `tools/x4_circle_history/error_bound.py`

- Source: [tools/x4_circle_history/error_bound.py](../../../../../tools/x4_circle_history/error_bound.py)
- Kind: python
- Lines: 398

## Module docstring

> Per-row numerical certificate (ERROR_BOUND.md v2.2; API.md error_bound.py, spec v2.4).

## Imports

### Internal (repo files)

- `import independent_reference` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 23, via sys.path edit)
- `from errors import CacheMiss, Invalid, require_scoring` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 24, via same directory)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 9)
- `decimal` (lines 11, 15)
- `fractions` (lines 16)
- `hashlib` (lines 12)
- `math` (lines 13)
- `pathlib` (lines 17)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(Path(__file__).resolve().parents[2] / 'tests' / 'oracle_profile')` -> `tests/oracle_profile`

## Imported by

- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 32, import)
- [tests/c1prime/test_a_oracle.py](../../tests/c1prime/test_a_oracle.py.md) (line 31, import)
- [tests/c1prime/test_b_cert_bounds.py](../../tests/c1prime/test_b_cert_bounds.py.md) (line 36, import)
- [tests/c1prime/test_b_cert_oracle.py](../../tests/c1prime/test_b_cert_oracle.py.md) (line 36, import)
- [tests/circle_history/test_error_bound.py](../../tests/circle_history/test_error_bound.py.md) (line 26, import)
- [tests/circle_history/test_reference_binding.py](../../tests/circle_history/test_reference_binding.py.md) (line 31, import)
- [tests/circle_history/test_reference_cache.py](../../tests/circle_history/test_reference_cache.py.md) (line 29, import)
- [tests/k4b/test_a_lemma_n.py](../../tests/k4b/test_a_lemma_n.py.md) (line 27, import)
- [tools/c1prime/c1_cert.py](../c1prime/c1_cert.py.md) (line 16, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 18, import)
- [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 12, import)
- [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 15, import)
- [tools/x4_circle_history/cost_probe.py](cost_probe.py.md) (line 23, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 58, import)
- [tools/x4_circle_history/process_law.py](process_law.py.md) (line 92, import)
- [tools/x4_circle_history/process_law.py](process_law.py.md) (line 99, import)
- [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 32, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 86, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 186, import)

## Top-level constants

- `EPS_V`
- `MOMENT_TOL`
- `MOMENT_TOL_EXACT`
- `TAIL_LIMIT`
- `TAYLOR_N`
- `TERM_SUM_BOUND`
- `X_MAX`
- `_TRAPS`
- `_WATCHED_FLAGS`

## Classes and functions

- **function `u_digits`** [L43-44]: `def u_digits(n) -> Fraction`
- **function `gamma_digits`** [L47-51]: `def gamma_digits(k, n) -> Fraction`
- **function `trapping_context`** [L54-65]: `def trapping_context(prec) -> decimal.Context`
- **function `_factorial_fraction`** [L68-69]: `def _factorial_fraction(x: Fraction, n: int) -> Fraction`
- **function `_series_bound`** [L72-84]: `def _series_bound(first: int, n: int) -> Fraction` - Exact upper bound of the COMPLETE positive series sum_k X^(2k+first)/(2k+first)!.
- **function `_verify_taylor_constants`** [L87-109]: `def _verify_taylor_constants() -> tuple[Fraction, Fraction]` - Exact verification (ERROR_BOUND.md v2.2 section 8).
- **function `_eps_v`** [L115-120]: `def _eps_v() -> Fraction`
- **function `decimal_cos_sin`** [L126-143]: `def decimal_cos_sin(x: float, digits=FEATURE_DIGITS) -> tuple[Decimal, Decimal, Fraction]` - (cos, sin, eps_v) of Decimal(x) exactly by fixed N-term Taylor sums (ERROR_BOUND §4).
- **function `exact_features`** [L146-173]: `def exact_features(coords) -> list[tuple[Decimal, Decimal]]` - Exact (cos, sin)(pi*x/6) at 80 digits for integer x in 0..11: 0, +-1, +-1/2, +-sqrt(3)/2.
- **function `feature_envelope`** [L176-177]: `def feature_envelope() -> Fraction`
- **function `posterior_envelope`** [L180-190]: `def posterior_envelope(L, S) -> Fraction` - beta of ERROR_BOUND §3(a): N = 1 + (L-1)(2S+2) positive-path operations at 60 digits.
- **function `moment_envelope`** [L193-196]: `def moment_envelope(beta, S) -> Fraction`
- **function `_reference_posterior`** [L199-212]: `def _reference_posterior(T, E, pi, suffix) -> list[Decimal]` - The nested reference context (its own localcontext) INHERITS these traps, so any
- **function `process_digest`** [L215-222]: `def process_digest(T, E, pi, coords) -> str` - sha256 binding of the exact process and feature inputs (dtype, shape, C-order bytes).
- **function `_checked_histories`** [L225-233]: `def _checked_histories(canonical32, n_symbols: int) -> np.ndarray`
- **function `reference_moments`** [L236-264]: `def reference_moments(T, E, pi, coords, canonical32, Ks=(4, 32), cache=None, cache_only=False) -> list[dict]` - Per row {K: (Mx, My)} Decimal moments with exact features.
- **function `row_bound`** [L267-277]: `def row_bound(x_hat, phi, M4, M32, eps_M4, eps_M32) -> dict` - Exact-rational R, Delta, E_ref and B for one row (ERROR_BOUND §2-3).
- **function `_deny_scoring`** [L280-284]: `def _deny_scoring(split, scoring_release)`
- **function `_moment_gap`** [L290-292]: `def _moment_gap(m_hat_row, ref) -> Fraction` - Exact rational gap |m_hat - M_ref| (compared exactly; floats only for reporting).
- **function `reference_check_rows`** [L295-323]: `def reference_check_rows(T, E, pi, coords, canonical32, m_hat: dict, Ks, split, scoring_release=None, cache=None, cache_only=False) -> dict` - Early gate: every row and K in Ks, |m_hat - M_ref| <= 1e-10 (no phase needed).
- **function `certify_rows`** [L326-398]: `def certify_rows(T, E, pi, coords, canonical32, phi, x_hat, m4_hat, m32_hat, split, scoring_release=None, cap=0.0001, cache=None, cache_only=False) -> dict` - Per-row score certificate; CERTIFIED / INCONCLUSIVE / FAIL_TECHNICAL (ERROR_BOUND §7).

