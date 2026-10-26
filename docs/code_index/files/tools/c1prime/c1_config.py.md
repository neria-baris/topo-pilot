# `tools/c1prime/c1_config.py`

- Source: [tools/c1prime/c1_config.py](../../../../../tools/c1prime/c1_config.py)
- Kind: python
- Lines: 56

## Module docstring

> C1' configuration: CONTRACT.json loading and constants (API.md §1; protocol §14, §17).

## Imports

### Internal (repo files)

- none

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 17: `str(_p)` -> `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/c1prime/test_a_chart.py](../../tests/c1prime/test_a_chart.py.md) (line 33, import)
- [tests/c1prime/test_a_chart_exceptions.py](../../tests/c1prime/test_a_chart_exceptions.py.md) (line 29, import)
- [tests/c1prime/test_a_chart_lcc512.py](../../tests/c1prime/test_a_chart_lcc512.py.md) (line 32, import)
- [tests/c1prime/test_a_chart_val.py](../../tests/c1prime/test_a_chart_val.py.md) (line 30, import)
- [tests/c1prime/test_a_exceptions.py](../../tests/c1prime/test_a_exceptions.py.md) (line 30, import)
- [tests/c1prime/test_c_process_keys.py](../../tests/c1prime/test_c_process_keys.py.md) (line 21, import)
- [tests/c1prime/test_c_release_worker.py](../../tests/c1prime/test_c_release_worker.py.md) (line 18, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 22, import)
- [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 10, import)
- [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 14, import)
- [tools/c1prime/c1_chart.py](c1_chart.py.md) (line 10, import)
- [tools/c1prime/c1_data.py](c1_data.py.md) (line 10, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 14, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 10, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 11, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 12, import)
- [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 11, import)
- [tools/c1prime/c1_env.py](c1_env.py.md) (line 7, import)
- [tools/c1prime/c1_fit.py](c1_fit.py.md) (line 8, import)
- [tools/c1prime/c1_gates.py](c1_gates.py.md) (line 6, import)
- [tools/c1prime/c1_means.py](c1_means.py.md) (line 10, import)
- [tools/c1prime/c1_model.py](c1_model.py.md) (line 9, import)
- [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 11, import)
- [tools/c1prime/c1_records.py](c1_records.py.md) (line 10, import)
- [tools/c1prime/c1_release.py](c1_release.py.md) (line 12, import)
- [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 20, import)
- [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 35, import)
- [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 27, import)

## Top-level constants

- `BOS`
- `CHART_KERNEL_KEYS`
- `CONTRACT`
- `CONTRACT_PATH`
- `HERE`
- `INDEX`
- `MODELS`
- `REPO`
- `SITE`

## Classes and functions

- **function `_inf_if_null`** [L30-31]: `def _inf_if_null(value)`
- **function `load_contract`** [L34-38]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **function `chart_cfg`** [L44-50]: `def chart_cfg(contract=None) -> dict` - The cfg dict for the frozen chart/cochain kernels (lift cap +inf; operation wall 600).
- **function `status_of`** [L53-56]: `def status_of(full: str) -> tuple` - 'INCONCLUSIVE/SUPPORT' -> ('INCONCLUSIVE', 'SUPPORT'); 'PASS' -> ('PASS', None).

