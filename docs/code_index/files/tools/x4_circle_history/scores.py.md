# `tools/x4_circle_history/scores.py`

- Source: [tools/x4_circle_history/scores.py](../../../../../tools/x4_circle_history/scores.py)
- Kind: python
- Lines: 154

## Module docstring

> Oracle targets, K4 scores and suffix-only controls (API.md scores.py).

## Imports

### Internal (repo files)

- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 16, via sys.path edit)
- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 17, via same directory)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 14: `str(Path(__file__).resolve().parents[1] / 'x4_oracle_profile')` -> `tools/x4_oracle_profile`

## Imported by

- [tests/c1prime/test_b_registry.py](../../tests/c1prime/test_b_registry.py.md) (line 34, import)
- [tests/c1prime_registry/test_registry_builder.py](../../tests/c1prime_registry/test_registry_builder.py.md) (line 22, import)
- [tests/circle_history/test_controls.py](../../tests/circle_history/test_controls.py.md) (line 31, import)
- [tests/circle_history/test_error_bound.py](../../tests/circle_history/test_error_bound.py.md) (line 30, import)
- [tests/circle_history/test_reference_binding.py](../../tests/circle_history/test_reference_binding.py.md) (line 34, import)
- [tests/circle_history/test_scores_precision.py](../../tests/circle_history/test_scores_precision.py.md) (line 29, import)
- [tests/k4b/test_a_theorem_a.py](../../tests/k4b/test_a_theorem_a.py.md) (line 239, import)
- [tests/k4b/test_b_data.py](../../tests/k4b/test_b_data.py.md) (line 24, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 32, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 30, import)
- [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 13, import)
- [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 25, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 14, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 25, import)
- [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 12, import)
- [tools/x4_circle_history/adapter.py](adapter.py.md) (line 15, import)
- [tools/x4_circle_history/adapter.py](adapter.py.md) (line 125, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 28, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 73, import)
- [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 93, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 52, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 88, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 187, import)

## Top-level constants

- `CONTROL_NAMES`
- `TWO_PI`

## Classes and functions

- **function `canonical_from_named`** [L22-39]: `def canonical_from_named(named, symbol_perm) -> np.ndarray` - canonical = argsort(perm)[named]; verifies perm[canonical] == named.
- **function `_require32`** [L42-46]: `def _require32(canonical32) -> np.ndarray`
- **function `history_digests`** [L49-53]: `def history_digests(canonical32) -> list[str]`
- **function `oracle_moments`** [L56-62]: `def oracle_moments(T, E_canon, pi, canonical32, features) -> dict` - {1, 4, 32: [n, 2]} first-harmonic suffix means via the unchanged job-0014 kernel.
- **function `unit_vectors`** [L65-69]: `def unit_vectors(phi) -> np.ndarray`
- **function `_pair`** [L72-81]: `def _pair(a, b) -> tuple[np.ndarray, np.ndarray]`
- **function `scores`** [L84-87]: `def scores(u, m32, m4) -> np.ndarray`
- **function `r4_norms`** [L90-92]: `def r4_norms(m32, m4) -> np.ndarray`
- **function `sha256_phase`** [L95-100]: `def sha256_phase(last4_row) -> float`
- **function `_finite_pairs`** [L103-107]: `def _finite_pairs(m) -> np.ndarray`
- **function `_magnitude`** [L110-117]: `def _magnitude(m) -> np.ndarray` - Stable ||m||: scale by the largest absolute component first (no underflow to 0).
- **function `_unit`** [L120-129]: `def _unit(m) -> np.ndarray` - m/||m|| by scale-first normalisation; EXACT (0, 0) -> (1, 0); no epsilon.
- **function `control_vectors`** [L132-135]: `def control_vectors(m1, m4, canonical32) -> dict`
- **function `angular_instability`** [L138-145]: `def angular_instability(m, bound) -> np.ndarray` - Diagnostic flag 0 < ||m|| <= bound (bound scalar or per row); never alters vectors.
- **function `control_scores`** [L151-154]: `def control_scores(m1, m4, m32, canonical32) -> dict` - {name: u_c . (m32 - m4)} for the three fixed suffix-only controls (spec v2.4 item 10).

