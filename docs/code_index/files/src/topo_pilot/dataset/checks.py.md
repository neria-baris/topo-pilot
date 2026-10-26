# `src/topo_pilot/dataset/checks.py`

- Source: [src/topo_pilot/dataset/checks.py](../../../../../../src/topo_pilot/dataset/checks.py)
- Kind: python
- Lines: 76

## Module docstring

> Pure checks and the sequence-id rule.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7)
- `scipy` (lines 8)

### Standard library

- `__future__` (lines 3)
- `hashlib` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/dataset/stage.py](stage.py.md) (line 23, import)
- [tests/c1prime/test_b_registry.py](../../../tests/c1prime/test_b_registry.py.md) (line 24, import)
- [tests/c2_readout/test_b_policy.py](../../../tests/c2_readout/test_b_policy.py.md) (line 32, import)
- [tests/dataset/test_stage.py](../../../tests/dataset/test_stage.py.md) (line 6, import)
- [tests/k4b/test_b_data.py](../../../tests/k4b/test_b_data.py.md) (line 29, import)
- [tests/k4b/test_b_flow.py](../../../tests/k4b/test_b_flow.py.md) (line 187, import)
- [tests/x6_stage1/test_b_ingest_bundle.py](../../../tests/x6_stage1/test_b_ingest_bundle.py.md) (line 33, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 31, import)
- [tests/x6_stage1/test_b_train_chain.py](../../../tests/x6_stage1/test_b_train_chain.py.md) (line 31, import)
- [tools/c1prime/c1_data.py](../../../tools/c1prime/c1_data.py.md) (line 17, import)
- [tools/c1prime/c1_driver.py](../../../tools/c1prime/c1_driver.py.md) (line 149, import)
- [tools/c2_readout/c2_data.py](../../../tools/c2_readout/c2_data.py.md) (line 29, import)
- [tools/c2_readout/c2_registry.py](../../../tools/c2_readout/c2_registry.py.md) (line 29, import)
- [tools/k4b/k4b_data.py](../../../tools/k4b/k4b_data.py.md) (line 20, import)
- [tools/x6_stage1/x6s1_cloud.py](../../../tools/x6_stage1/x6s1_cloud.py.md) (line 28, import)
- [tools/x6_stage1/x6s1_data.py](../../../tools/x6_stage1/x6s1_data.py.md) (line 25, import)
- [tools/x6_stage1/x6s1_registry.py](../../../tools/x6_stage1/x6s1_registry.py.md) (line 30, import)
- [tools/x6_stage1/x6s1_run.py](../../../tools/x6_stage1/x6s1_run.py.md) (line 445, import)

## Top-level constants

- `MIN_FOR_CHI2`
- `P_THRESHOLD`
- `SPLIT_CODES`

## Classes and functions

- **function `process_code`** [L17-20]: `def process_code(family: str, mode: str, sigma: str, replicate: int | str) -> int` - First 31 bits of ``sha256(canonical_json([family, mode, sigma, replicate]))``.
- **function `make_sequence_ids`** [L23-32]: `def make_sequence_ids(code: int, split: str, n: int) -> np.ndarray` - ``int64 = (process_code << 32) | (split_code << 28) | index`` for ``index = 0..n-1``.
- **function `check_ranges`** [L35-41]: `def check_ranges(tokens: np.ndarray, states: np.ndarray, V: int, N: int) -> None` - Raise ``ALIGNMENT_ERROR`` if any token is >= V or any state is outside ``0..N-1``.
- **function `check_disjoint`** [L44-51]: `def check_disjoint(**splits: np.ndarray) -> None` - Raise ``SPLIT_OVERLAP`` if any ``sequence_id`` occurs in more than one split.
- **function `check_first_token`** [L54-76]: `def check_first_token(first: np.ndarray, p_w: np.ndarray, split: str) -> float | None` - Chi-square test of first-token counts against ``n * (pi E)``; returns the p-value.

