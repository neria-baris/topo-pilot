# `src/topo_pilot/contracts/_schemas_data.py`

- Source: [src/topo_pilot/contracts/_schemas_data.py](../../../../../../src/topo_pilot/contracts/_schemas_data.py)
- Kind: python
- Lines: 238

## Module docstring

> Data, oracle and baseline artifacts (DATA_SCHEMAS §3–§4).

## Imports

### Internal (repo files)

- `from . import _checks` -> [src/topo_pilot/contracts/_checks.py](_checks.py.md) (line 11, via relative)
- `from .base import Artifact, array_field, optional_array_field` -> [src/topo_pilot/contracts/base.py](base.py.md) (line 12, via relative)
- `from .errors import ErrorCode` -> [src/topo_pilot/contracts/errors.py](errors.py.md) (line 13, via relative)
- `from .ids import make_history_id` -> [src/topo_pilot/contracts/ids.py](ids.py.md) (line 14, via relative)

### External (third-party)

- `numpy` (lines 9)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 5)
- `dataclasses` (lines 6)
- `typing` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/contracts/schemas.py](schemas.py.md) (line 5, import)

## Top-level constants

- `N_OBS`
- `SPLITS`

## Classes and functions

- **function `_token_dtype_ok`** [L20-21]: `def _token_dtype_ok(tokens: np.ndarray, V: int) -> bool`
- **class `ObservationSet(Artifact)`** [L25-62] decorators: @dataclass(frozen=True, eq=False) - Public token data for one split.
- **method `ObservationSet.n_sequences`** [L45-47]: `def n_sequences(self) -> int` decorators: @property - Number of trajectories R.
- **method `ObservationSet.validate`** [L49-62]: `def validate(self) -> None`
- **class `EvalSidecar(Artifact)`** [L66-93] decorators: @dataclass(frozen=True, eq=False) - Privileged latent states for dev/test: ``z: int16[R, 33]``; ``z[:, t]`` emitted
- **method `EvalSidecar.validate`** [L81-93]: `def validate(self) -> None`
- **class `HistoryIndex(Artifact)`** [L97-139] decorators: @dataclass(frozen=True, eq=False) - Analysis histories, one per trajectory, grouped into disjoint panels.
- **method `HistoryIndex.validate`** [L121-139]: `def validate(self) -> None`
- **class `OracleOutputs(Artifact)`** [L143-193] decorators: @dataclass(frozen=True, eq=False) - Exact-filter quantities per history (rows aligned with ``history_id``, float64 unless noted).
- **method `OracleOutputs.validate`** [L167-193]: `def validate(self) -> None`
- **class `ProcessDiagnostics(Artifact)`** [L197-215] decorators: @dataclass(frozen=True, eq=False) - Process-level diagnostics: context gain ``G_C`` (nats), mean entropy of b^(1) (nats),
- **method `ProcessDiagnostics.validate`** [L211-215]: `def validate(self) -> None`
- **class `BaselineOutputs(Artifact)`** [L219-238] decorators: @dataclass(frozen=True, eq=False) - n-gram baseline predictive ``probs: [M, V] float64`` aligned to ``history_id``.
- **method `BaselineOutputs.validate`** [L231-238]: `def validate(self) -> None`

