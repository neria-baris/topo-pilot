# `tools/k4b/k4b_config.py`

- Source: [tools/k4b/k4b_config.py](../../../../../tools/k4b/k4b_config.py)
- Kind: python
- Lines: 168

## Module docstring

> K4b configuration: CONTRACT.json loading, constants, chart-cfg equality with C1' (API.md §1).

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](../c1prime/c1_bounds.py.md) (line 26, via sys.path edit)
- `import c1_config` -> [tools/c1prime/c1_config.py](../c1prime/c1_config.py.md) (line 27, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 28, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 10)
- `pathlib` (lines 11)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 24: `_p` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/hwsb/test_a_ladder.py](../../tests/hwsb/test_a_ladder.py.md) (line 32, import)
- [tests/hwsc/test_a_k4b_known_bound.py](../../tests/hwsc/test_a_k4b_known_bound.py.md) (line 34, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 80, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 169, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 216, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 224, import)
- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 309, import)
- [tests/k4b/test_a_decision.py](../../tests/k4b/test_a_decision.py.md) (line 32, import)
- [tests/k4b/test_a_lemma_n.py](../../tests/k4b/test_a_lemma_n.py.md) (line 29, import)
- [tests/k4b/test_a_ranks_ladder.py](../../tests/k4b/test_a_ranks_ladder.py.md) (line 27, import)
- [tests/k4b/test_b_charts.py](../../tests/k4b/test_b_charts.py.md) (line 26, import)
- [tests/k4b/test_b_data.py](../../tests/k4b/test_b_data.py.md) (line 22, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 24, import)
- [tests/k4b/test_b_h1_meta.py](../../tests/k4b/test_b_h1_meta.py.md) (line 29, import)
- [tests/k4b/test_b_registry.py](../../tests/k4b/test_b_registry.py.md) (line 30, import)
- [tests/k4b/test_b_registry_fixes.py](../../tests/k4b/test_b_registry_fixes.py.md) (line 29, import)
- [tests/k4b/test_b_registry_rules.py](../../tests/k4b/test_b_registry_rules.py.md) (line 33, import)
- [tools/hwsb/hwsb_gates.py](../hwsb/hwsb_gates.py.md) (line 15, import)
- [tools/hwsb/hwsb_stages.py](../hwsb/hwsb_stages.py.md) (line 23, import)
- [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 28, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 183, import)
- [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 19, import)
- [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 23, import)
- [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 22, import)
- [tools/k4b/k4b_cert.py](k4b_cert.py.md) (line 16, import)
- [tools/k4b/k4b_cert.py](k4b_cert.py.md) (line 19, import)
- [tools/k4b/k4b_charts.py](k4b_charts.py.md) (line 15, import)
- [tools/k4b/k4b_data.py](k4b_data.py.md) (line 12, import)
- [tools/k4b/k4b_data.py](k4b_data.py.md) (line 16, import)
- [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 9, import)
- [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 12, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 15, import)
- [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 28, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 15, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 30, import)
- [tools/k4b/k4b_meter_bind.py](k4b_meter_bind.py.md) (line 17, import)
- [tools/k4b/k4b_registry.py](k4b_registry.py.md) (line 18, import)
- [tools/k4b/k4b_release.py](k4b_release.py.md) (line 18, import)
- [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 10, import)
- [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 14, import)
- [tools/k4b/k4b_stats.py](k4b_stats.py.md) (line 16, import)
- [tools/k4b/k4b_stats.py](k4b_stats.py.md) (line 20, import)

## Top-level constants

- `ALPHA`
- `CAP`
- `CONTRACT`
- `CONTRACT_PATH`
- `DRAWS`
- `FLOOR`
- `HERE`
- `KS`
- `LADDER`
- `MARGIN`
- `MODELS`
- `P2_MAX_ABS`
- `PROCESS`
- `PROTOCOL_PATH`
- `RANKS`
- `REPO`
- `ROOT`
- `SCOPE`
- `SEEDS`
- `STORE`
- `_RANK_P`

## Classes and functions

- **function `load_contract`** [L76-78]: `def load_contract(path=CONTRACT_PATH) -> dict` - CONTRACT.json; chart.lift_cpu_cap_s and resources.cpu_cap_s null -> +inf.
- **function `chart_cfg`** [L84-86]: `def chart_cfg(contract=None) -> dict` - The kernel cfg (12 CHART_KERNEL_KEYS, lift cap +inf, operation wall 600 s).
- **function `check_chart_equality`** [L89-97]: `def check_chart_equality(k4b=None, c1=None) -> dict` - C2 (§4.2): the K4b chart cfg, giant and val_support equal C1''s, key for key.
- **function `status_of`** [L100-101]: `def status_of(full: str) -> tuple`
- **function `require_int_keys`** [L104-114]: `def require_int_keys(d, what) -> dict` - Return d iff its keys are exactly the int seeds of MODELS (R11 lesson).
- **function `expected_meta`** [L117-131]: `def expected_meta(model, step_label) -> dict`
- **function `_same`** [L134-137]: `def _same(a, b) -> bool`
- **function `check_checkpoint_meta`** [L140-168]: `def check_checkpoint_meta(meta, expected) -> dict` - Pure (API.md §14.1, R19); a missing key is a mismatch, never an exception.

