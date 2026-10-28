# `tools/x4_oracle_profile/oracle_profile.py`

- Source: [tools/x4_oracle_profile/oracle_profile.py](../../../../../tools/x4_oracle_profile/oracle_profile.py)
- Kind: python
- Lines: 224

## Module docstring

> Pure kernels for the job-0014 circular-history oracle profile (contract: API.md).

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 18, 19)

### Standard library

- `__future__` (lines 14)
- `collections` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_eligibility_support.py](../../tests/c1prime/test_a_eligibility_support.py.md) (line 28, import)
- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 35, import)
- [tests/c1prime/test_b_inference.py](../../tests/c1prime/test_b_inference.py.md) (line 32, import)
- [tests/c1prime/test_b_precision.py](../../tests/c1prime/test_b_precision.py.md) (line 29, import)
- [tests/circle_history/test_builder_e2e.py](../../tests/circle_history/test_builder_e2e.py.md) (line 24, import)
- [tests/circle_history/test_error_bound.py](../../tests/circle_history/test_error_bound.py.md) (line 29, import)
- [tests/circle_history/test_reference_binding.py](../../tests/circle_history/test_reference_binding.py.md) (line 33, import)
- [tests/circle_history/test_scores_precision.py](../../tests/circle_history/test_scores_precision.py.md) (line 28, import)
- [tests/hws/test_b_oracle.py](../../tests/hws/test_b_oracle.py.md) (line 28, import)
- [tests/hws/test_b_worlds.py](../../tests/hws/test_b_worlds.py.md) (line 28, import)
- [tests/k4b/test_a_transport_bound.py](../../tests/k4b/test_a_transport_bound.py.md) (line 38, import)
- [tests/oracle_profile/test_builder_kernels.py](../../tests/oracle_profile/test_builder_kernels.py.md) (line 17, import)
- [tests/oracle_profile/test_oracle_profile.py](../../tests/oracle_profile/test_oracle_profile.py.md) (line 31, import)
- [tests/oracle_profile/test_oracle_profile_kernels.py](../../tests/oracle_profile/test_oracle_profile_kernels.py.md) (line 23, import)
- [tests/oracle_profile/test_oracle_profile_traps.py](../../tests/oracle_profile/test_oracle_profile_traps.py.md) (line 30, import)
- [tests/x2a_stage0/test_x2a_stage0.py](../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 35, import)
- [tools/c1prime/c1_driver.py](../c1prime/c1_driver.py.md) (line 106, import)
- [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 15, import)
- [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 16, import)
- [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 14, import)
- [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 34, import)
- [tools/d2a/d2a_targets.py](../d2a/d2a_targets.py.md) (line 16, import)
- [tools/hws/hws_driver.py](../hws/hws_driver.py.md) (line 330, import)
- [tools/hws/hws_exact.py](../hws/hws_exact.py.md) (line 23, import)
- [tools/hws/hws_known.py](../hws/hws_known.py.md) (line 24, import)
- [tools/hws/hws_oracle.py](../hws/hws_oracle.py.md) (line 13, import)
- [tools/hws/hws_worlds.py](../hws/hws_worlds.py.md) (line 24, import)
- [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 17, import)
- [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 63, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 39, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 171, import)
- [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 21, import)
- [tools/x2a_stage0/x2a_mc.py](../x2a_stage0/x2a_mc.py.md) (line 17, import)
- [tools/x2a_stage0/x2a_model.py](../x2a_stage0/x2a_model.py.md) (line 21, import)
- [tools/x4_circle_history/live_context.py](../x4_circle_history/live_context.py.md) (line 36, import)
- [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 16, import)
- [tools/x4_oracle_profile/audit.py](audit.py.md) (line 32, import)
- [tools/x4_oracle_profile/inputs.py](inputs.py.md) (line 18, import)
- [tools/x4_oracle_profile/run_profile.py](run_profile.py.md) (line 26, import)
- [tools/x4_oracle_profile/runtime.py](runtime.py.md) (line 19, import)
- [tools/x4_oracle_profile/validation.py](validation.py.md) (line 17, import)
- [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 21, import)
- [tools/x6_stage0/x6_run.py](../x6_stage0/x6_run.py.md) (line 22, import)
- [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 300, import)

## Top-level constants

- `PERIOD`

## Classes and functions

- **class `ProfileError(RuntimeError)`** [L24-25] - Every validation failure of this module.
- **function `_finite_array`** [L28-37]: `def _finite_array(name: str, value, ndim: int) -> NDArray[np.float64]`
- **function `circle_features`** [L40-55]: `def circle_features(coords) -> NDArray[np.float64]` - ``[S, 2]`` first-harmonic features of the first coordinate ``x = coords[:, 0]``.
- **function `canonical_emission`** [L58-66]: `def canonical_emission(E_named, symbol_perm) -> NDArray[np.float64]` - ``E_canon = E_named[:, symbol_perm]`` (canonical symbol k is named symbol symbol_perm[k]).
- **function `validate_process`** [L69-91]: `def validate_process(T, E, pi, tol: float = 1e-12) -> dict` - Check shapes, finiteness, nonnegativity, stochastic rows and stationarity of ``pi``.
- **function `_model_arrays`** [L94-103]: `def _model_arrays(T, E, pi) -> tuple` - Structural kernel invariants: finite, nonnegative, consistent shapes (stochasticity and
- **function `_checked_tokens`** [L106-117]: `def _checked_tokens(tokens, n_symbols: int) -> NDArray[np.int64]`
- **function `_checked_k`** [L120-125]: `def _checked_k(K, length: int) -> int`
- **function `suffix_posterior`** [L128-152]: `def suffix_posterior(T, E, pi, tokens, K) -> NDArray[np.float64]` - ``[n, S]`` normalised filtering posteriors ``P(z_L | w_{L-K+1:L})``, stationary restart.
- **function `posterior_means`** [L155-160]: `def posterior_means(T, E, pi, tokens, Ks: Sequence[int], features) -> dict[int, NDArray]` - ``{K: suffix_posterior(...) @ features}``, each ``[n, 2]``.
- **function `residual_rows`** [L163-179]: `def residual_rows(means: Mapping[int, NDArray], full: int = 32) -> dict` - Per-row ``r_K = m_full - m_K``, ``||r_K||`` and ``||r_K||^2`` for every K in ``means``.
- **function `profile_point`** [L182-191]: `def profile_point(norm: Mapping[int, NDArray], sq: Mapping[int, NDArray]) -> dict` - ``{"B": {K: mean norm}, "V": {K: mean sq}}`` as Python floats.
- **function `bootstrap_profile`** [L194-215]: `def bootstrap_profile(norm, sq, Ks: Sequence[int], rng: np.random.Generator, draws: int) -> dict` - Whole-row bootstrap; one ``rng.integers(0, n, size=n)`` per draw shared by all K, B and V.
- **function `percentile_interval`** [L218-224]: `def percentile_interval(samples, probs: Sequence[float]) -> NDArray[np.float64]` - ``np.quantile(samples, probs, axis=0, method="inverted_cdf")``.

