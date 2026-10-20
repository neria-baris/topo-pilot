# `src/topo_pilot/oracle/stage.py`

- Source: [src/topo_pilot/oracle/stage.py](../../../../../../src/topo_pilot/oracle/stage.py)
- Kind: python
- Lines: 131

## Module docstring

> `OracleStage`: the only place in `oracle` that touches the artifact store.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, ErrorCode, HistoryIndex, ObservationSet, OracleOutputs, ProcessDiagnostics, TransitionSpec, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)
- `from ._common import fail` -> [src/topo_pilot/oracle/_common.py](_common.py.md) (line 22, via relative)
- `from ._filter import BayesFilter, LastSymbolPosterior` -> [src/topo_pilot/oracle/_filter.py](_filter.py.md) (line 23, via relative)
- `from ._futures import FutureOperator, context_gain` -> [src/topo_pilot/oracle/_futures.py](_futures.py.md) (line 24, via relative)

### External (third-party)

- `numpy` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `logging` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/oracle/__init__.py](__init__.py.md) (line 5, import)

## Top-level constants

- `ANALYSIS_END`
- `CONSUMER`
- `K_MAX`
- `OBS_LEN`
- `_LOG`

## Classes and functions

- **function `_entropy`** [L33-36]: `def _entropy(b: NDArray[np.float64]) -> NDArray[np.float64]` - Shannon entropy in nats per row, with ``0 log 0 = 0``.
- **function `_world_family`** [L39-53]: `def _world_family(store: ArtifactStore, artifact_id: str) -> str` - ``config["family"]`` of the nearest WorldSpec ancestor of ``artifact_id`` ("" if none).
- **class `OracleStage`** [L56-131] - Compute exact-oracle panels and process diagnostics from public artifacts only.
- **method `OracleStage.run`** [L77-115]: `def run(self, transition_id: str, emission_id: str, obs_test_id: str, history_index_id: str, store: ArtifactStore) -> dict[str, str]` - Write one ``OracleOutputs`` and one ``ProcessDiagnostics``; return their ids.
- **method `OracleStage._history_rows`** [L118-131]: `def _history_rows(obs: ObservationSet, hist: HistoryIndex) -> NDArray[np.int64]` decorators: @staticmethod - Row index in ``obs`` for each history; checks end == 32 and tokens_hash.

