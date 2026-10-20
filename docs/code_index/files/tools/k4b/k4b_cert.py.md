# `tools/k4b/k4b_cert.py`

- Source: [tools/k4b/k4b_cert.py](../../../../../tools/k4b/k4b_cert.py)
- Kind: python
- Lines: 190

## Module docstring

> K4b references, moment check, row bounds, Lemma N, B_num, F and guards (API.md §7).

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../c1prime/c1_bounds.py.md) (line 13, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 14, via unique basename)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 15, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 16, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 18, via unique basename)
- `from k4b_config import CAP, FLOOR, KS, P2_MAX_ABS` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 19, via same directory)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../x4_circle_history/process_law.py.md) (line 159, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 17)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 11)
- `math` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_a_decision.py](../../tests/k4b/test_a_decision.py.md) (line 31, import)
- [tests/k4b/test_a_lemma_n.py](../../tests/k4b/test_a_lemma_n.py.md) (line 28, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 26, import)
- [tests/k4b/test_a_transport_bound.py](../../tests/k4b/test_a_transport_bound.py.md) (line 27, import)
- [tests/k4b/test_a_width_b4.py](../../tests/k4b/test_a_width_b4.py.md) (line 28, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 16, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 16, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 29, import)

## Top-level constants

- `CONTROL_K`
- `D_LEMMA_N`
- `MOMENT_TOL`
- `NUMERICAL`
- `S_ENVELOPE`

## Classes and functions

- **function `_fr`** [L28-30]: `def _fr(x) -> Fraction`
- **function `envelopes`** [L33-35]: `def envelopes(Ks=KS) -> dict`
- **function `references`** [L38-39]: `def references(T, E, pi, coords, canon32, cache=None) -> list`
- **function `moment_check`** [L42-52]: `def moment_check(m_hat, refs) -> dict` - |Fraction(float(m_hat)) - Fraction(M~)| <= MOMENT_TOL for every row, K and coordinate.
- **function `isqrt_bracket`** [L55-60]: `def isqrt_bracket(s, D=D_LEMMA_N) -> int` - k with k/D <= sqrt(s) < (k+1)/D, for a non-negative Fraction s = a/b.
- **function `norm_bound`** [L63-70]: `def norm_bound(n_hat, M32, M4, eps4, eps32, D=D_LEMMA_N) -> Fraction` - Lemma N: B_N = max(|n - k/D|, |n - (k+1)/D|) + (3/2)(eps_K + eps32).
- **function `phase_bound`** [L73-74]: `def phase_bound(x_hat, phi, MK, M32, epsK, eps32) -> Fraction`
- **function `endpoint_bounds`** [L77-95]: `def endpoint_bounds(arrays, supported, phi, refs, eps, K=4) -> dict` - Supported rows: phase bound; unsupported rows (X-/+ = -/+ n_hat): Lemma N; B4: Lemma N.
- **function `control_bounds`** [L98-102]: `def control_bounds(x, phi, refs, eps, K=4) -> dict`
- **function `cap_ok`** [L105-106]: `def cap_ok(max_b) -> bool`
- **function `p2_ok`** [L109-111]: `def p2_ok(X) -> bool`
- **function `certify`** [L114-130]: `def certify(primary: dict, controls: dict) -> dict` - primary/controls: {name: {"X": array, "max_B": Fraction}}. Primary defects raise
- **function `b_num`** [L133-134]: `def b_num(max_b, max_abs, n) -> Fraction`
- **function `margin`** [L137-138]: `def margin(B_num, Z_bound) -> Fraction`
- **function `F_plan`** [L141-144]: `def F_plan(Z_bound) -> Fraction` - §7.1: max(B_constant(1e-4, 4, 12288), FLOOR) + Z_bound.
- **function `b4_guard`** [L147-155]: `def b4_guard(r4n, B_norm_max, Z_bound, seed, n) -> dict`
- **function `transport_bound`** [L158-168]: `def transport_bound(T, E, pi, coords) -> dict`
- **function `control_bounds_all`** [L171-190]: `def control_bounds_all(controls, refs, eps) -> dict` - Row certificates of every control entry (reported, never gating; R22 per side).

