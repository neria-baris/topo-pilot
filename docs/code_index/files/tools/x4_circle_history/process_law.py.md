# `tools/x4_circle_history/process_law.py`

- Source: [tools/x4_circle_history/process_law.py](../../../../../tools/x4_circle_history/process_law.py)
- Kind: python
- Lines: 274

## Module docstring

> Process-law bound Z_bound (ERROR_BOUND.md v2.2 sections 6 and 9; API.md spec v2.4 item 4).

## Imports

### Internal (repo files)

- `from errors import Invalid` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 23, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 92, via same directory) (inside a function)
- `from error_bound import u_digits` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 99, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 13)
- `decimal` (lines 15, 18)
- `fractions` (lines 19)
- `importlib` (lines 16)
- `math` (lines 17)
- `pathlib` (lines 20)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `spec_from_file_location` line 131: `dynamic: SAMPLER_FILE` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md)

### sys.path additions

- none

## Imported by

- [tests/circle_history/test_process_law.py](../../tests/circle_history/test_process_law.py.md) (line 31, import)
- [tests/hws/test_b_exact.py](../../tests/hws/test_b_exact.py.md) (line 29, import)
- [tests/hwsb/test_a_enclosure_proof.py](../../tests/hwsb/test_a_enclosure_proof.py.md) (line 36, import)
- [tests/hwsb/test_b_meter_law.py](../../tests/hwsb/test_b_meter_law.py.md) (line 30, import)
- [tests/k4b/test_a_transport_bound.py](../../tests/k4b/test_a_transport_bound.py.md) (line 28, import)
- [tools/hws/hws_exact.py](../hws/hws_exact.py.md) (line 24, import)
- [tools/hwsb/hwsb_dry2.py](../hwsb/hwsb_dry2.py.md) (line 26, import)
- [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 21, import)
- [tools/hwsb/hwsb_law.py](../hwsb/hwsb_law.py.md) (line 21, import)
- [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 159, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 115, import)

## Top-level constants

- `GRID`
- `LAW`
- `REPORT_GRID`
- `SAMPLER_FILE`
- `_SAMPLER`

## Classes and functions

- **class `Mismatch(Exception)`** [L40-41] - A documented-law condition fails: the bound is UNAVAILABLE (not a defect).
- **function `lattice_states`** [L44-54]: `def lattice_states(coords) -> list[tuple[int, int]]`
- **function `_neighbours`** [L57-60]: `def _neighbours(states, s, t) -> bool`
- **function `documented_transition`** [L63-73]: `def documented_transition(states) -> list[list[Fraction]]`
- **function `ideal_identities`** [L76-88]: `def ideal_identities(T_star, S) -> None`
- **function `_ctx`** [L91-94]: `def _ctx() -> decimal.Context`
- **function `softmax_enclosure`** [L97-125]: `def softmax_enclosure(states, digits=60)` - (E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (positive).
- **function `_sampler`** [L128-135]: `def _sampler()`
- **function `sampler_cdf`** [L138-140]: `def sampler_cdf(P) -> np.ndarray` - The ACTUAL sampler thresholds (_cumulative_rows of the frozen dataset/sampler.py).
- **function `_G`** [L143-144]: `def _G(x: Fraction) -> int`
- **function `threshold_law`** [L147-155]: `def threshold_law(c_row) -> dict` - Exact law of j = min(#{i: c'_i <= u}, V-1) for u on the 2^-53 grid, c' clamped to [0, 1].
- **function `row_tv`** [L158-171]: `def row_tv(p_hat_row, dev_row, c_row) -> dict`
- **function `_up`** [L174-175]: `def _up(x: Fraction) -> Fraction`
- **function `_report`** [L178-179]: `def _report(x)`
- **function `_arrays`** [L182-189]: `def _arrays(T, E, pi, coords)`
- **function `_kappas`** [L192-219]: `def _kappas(T, E, pi, T_star, E_dec, lo, hi)`
- **function `process_law_bound`** [L222-274]: `def process_law_bound(T, E, pi, coords) -> dict`

