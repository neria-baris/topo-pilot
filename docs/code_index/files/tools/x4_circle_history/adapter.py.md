# `tools/x4_circle_history/adapter.py`

- Source: [tools/x4_circle_history/adapter.py](../../../../../tools/x4_circle_history/adapter.py)
- Kind: python
- Lines: 184

## Module docstring

> Restricted, read-only E4 adapter (API.md adapter.py).

## Imports

### Internal (repo files)

- `from errors import AccessDenied, JoinError, require_scoring` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 14, via same directory)
- `from scores import history_digests` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 15, via same directory)
- `from topo_pilot.contracts import ActivationSet, HistoryIndex, ObservationSet, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root) (inside a function)
- `from scores import canonical_from_named` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 125, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 13)

### Standard library

- `__future__` (lines 9)
- `dataclasses` (lines 11)
- `hashlib` (lines 154)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/circle_history/test_adapter.py](../../tests/circle_history/test_adapter.py.md) (line 33, import)
- [tests/circle_history/test_builder_e2e.py](../../tests/circle_history/test_builder_e2e.py.md) (line 26, import)
- [tests/circle_history/test_controls.py](../../tests/circle_history/test_controls.py.md) (line 28, import)
- [tools/chart_diag/chart_diag.py](../chart_diag/chart_diag.py.md) (line 127, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 107, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 51, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 65, import)

## Top-level constants

- `ALLOWED_PANELS`

## Classes and functions

- **class `E4Manifest`** [L21-26] decorators: @dataclass(frozen=True)
- **function `_contracts`** [L29-32]: `def _contracts()`
- **class `RestrictedE4Adapter`** [L35-150] - Panels 1-2 only by default; lineage verified before any array is returned.
- **method `RestrictedE4Adapter.__init__`** [L38-41]: `def __init__(self, store, manifest: E4Manifest, *, scoring_release=None) -> None`
- **method `RestrictedE4Adapter._ids`** [L43-47]: `def _ids(self, model)`
- **method `RestrictedE4Adapter._load`** [L49-55]: `def _load(self, model)`
- **method `RestrictedE4Adapter._verify`** [L57-89]: `def _verify(self, model, obs, hist, acts, tokens_hash) -> dict`
- **method `RestrictedE4Adapter.lineage`** [L91-93]: `def lineage(self, model) -> dict`
- **method `RestrictedE4Adapter.panels`** [L95-117]: `def panels(self, model, panels=(1, 2)) -> dict`
- **method `RestrictedE4Adapter.join_keys`** [L119-135]: `def join_keys(self, model, symbol_perm) -> dict` - Identity-only join material for ALL panels: sequence_id, panel and canonical digest.
- **method `RestrictedE4Adapter.identity_report`** [L137-150]: `def identity_report(self) -> dict` - All lineage/join checks for every model and panel; counts/booleans/digests only.
- **function `_digest_of`** [L153-156]: `def _digest_of(values) -> str`
- **function `cross_model_join`** [L159-184]: `def cross_model_join(per_model: dict) -> dict` - Pair rows across models by sequence_id with identical canonical digests; no fallback.

