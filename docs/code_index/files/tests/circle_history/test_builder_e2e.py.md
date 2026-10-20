# `tests/circle_history/test_builder_e2e.py`

- Source: [tests/circle_history/test_builder_e2e.py](../../../../../tests/circle_history/test_builder_e2e.py)
- Kind: python
- Lines: 217

## Module docstring

> BUILDER end-to-end test (not independent): runner stages on a fully synthetic store.

## Imports

### Internal (repo files)

- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../../tools/x4_oracle_profile/oracle_profile.py.md) (line 24, via sys.path edit)
- `import runner` -> [tools/x4_circle_history/runner.py](../../tools/x4_circle_history/runner.py.md) (line 25, via sys.path edit)
- `from adapter import E4Manifest` -> [tools/x4_circle_history/adapter.py](../../tools/x4_circle_history/adapter.py.md) (line 26, via sys.path edit)
- `from stage_records import StageRefused` -> [tools/x4_circle_history/stage_records.py](../../tools/x4_circle_history/stage_records.py.md) (line 27, via sys.path edit)
- `from topo_pilot.contracts import ActivationSet, Checkpoint, HistoryIndex, ObservationSet, make_history_id, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `from topo_pilot.contracts.testing import memory_store` -> [src/topo_pilot/contracts/testing.py](../../src/topo_pilot/contracts/testing.py.md) (line 37, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `copy` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 22: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/circle_history/test_builder_v24_stages.py](test_builder_v24_stages.py.md) (line 22, import)

## Top-level constants

- `MODELS`
- `PERMS`
- `REPO`
- `TOOL`

## Classes and functions

- **function `_process`** [L44-61]: `def _process()`
- **function `_canonical_tokens`** [L64-66]: `def _canonical_tokens()`
- **function `_activations`** [L69-81]: `def _activations(model)`
- **function `_store`** [L84-135]: `def _store()`
- **function `_contract`** [L138-145]: `def _contract(relaxed: bool)`
- **function `_context`** [L148-157]: `def _context(tmp_path, relaxed)`
- **function `_gates`** [L160-161]: `def _gates(tmp_path)`
- **test `test_frozen_thresholds_stop_inconclusive_at_coverage`** [L164-179]: `def test_frozen_thresholds_stop_inconclusive_at_coverage(tmp_path)`
- **test `test_relaxed_thresholds_reach_precision_and_export`** [L182-207]: `def test_relaxed_thresholds_reach_precision_and_export(tmp_path)`
- **test `test_join_mismatch_fails_technical`** [L210-217]: `def test_join_mismatch_fails_technical(tmp_path)` - Spec v2.4 item 1: a technical identity mismatch is FAIL_TECHNICAL (overall FAIL).

