# `tools/k4b/k4b_scores.py`

- Source: [tools/k4b/k4b_scores.py](../../../../../tools/k4b/k4b_scores.py)
- Kind: python
- Lines: 159

## Module docstring

> K4b oracle moments, X-/X+ assembly, control and descriptive phases (API.md §4).

## Imports

### Internal (repo files)

- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 9, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 10, via same directory)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 12, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 13, via unique basename)
- `from k4b_config import KS` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 14, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 21, via unique basename) (inside a function)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 127, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 11)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_b_oracle.py](../../tests/hws/test_b_oracle.py.md) (line 27, import)
- [tests/k4b/test_a_theorem_a.py](../../tests/k4b/test_a_theorem_a.py.md) (line 238, import)
- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 30, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 28, import)
- [tools/hws/hws_known.py](../hws/hws_known.py.md) (line 22, import)
- [tools/hws/hws_oracle.py](../hws/hws_oracle.py.md) (line 11, import)
- [tools/hws/hws_stats.py](../hws/hws_stats.py.md) (line 15, import)
- [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 10, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 21, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 23, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 32, import)

## Top-level constants

- `NUMERICAL`
- `TWO_PI`

## Classes and functions

- **function `oracle_moments`** [L20-24]: `def oracle_moments(T, E_canon, pi, canon32, features) -> dict`
- **function `wrap_phase`** [L27-32]: `def wrap_phase(phi) -> np.ndarray`
- **function `vector_phase`** [L35-38]: `def vector_phase(m) -> np.ndarray`
- **function `m4_phase`** [L41-42]: `def m4_phase(m4) -> np.ndarray`
- **function `oracle_phase`** [L45-46]: `def oracle_phase(m32) -> np.ndarray`
- **function `sha_phase`** [L49-51]: `def sha_phase(canon32) -> np.ndarray`
- **function `phase_scores`** [L54-55]: `def phase_scores(phi, m32, mK) -> np.ndarray`
- **function `_bounded`** [L58-66]: `def _bounded(phi, supported, m32, mK) -> dict`
- **function `endpoint_arrays`** [L69-71]: `def endpoint_arrays(phi, supported, m32, m4) -> dict` - §1.4: X- = X+ = u(phi).r4 on supported rows; -/+ ||r4|| on unsupported rows.
- **function `secondary_arrays`** [L74-75]: `def secondary_arrays(phi, supported, m, K) -> dict`
- **function `naive_scores`** [L78-79]: `def naive_scores(phi, m32, m4) -> np.ndarray`
- **function `support_reasons`** [L82-89]: `def support_reasons(ext, R) -> dict`
- **function `_summary`** [L92-96]: `def _summary(x) -> dict`
- **function `_mean`** [L99-101]: `def _mean(x) -> float | None`
- **function `support_report`** [L104-118]: `def support_report(ext, R, r4n, phi, m32, m4, sealed) -> dict` - §10 support report; the sealed form omits the supported contribution (§7.5).
- **function `_one`** [L121-122]: `def _one(phi, m32, m4) -> dict`
- **function `control_arrays`** [L125-150]: `def control_arrays(m, canon32, ext, init_ext, decoders) -> dict` - API.md §14.2: the eight control families (two-sided: init, delta1, delta2).
- **function `_radius`** [L153-154]: `def _radius(R, j) -> float`
- **function `support_entries`** [L157-159]: `def support_entries(ext, R, arrays, m) -> dict`

