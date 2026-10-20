# `src/topo_pilot/experiment/x4b.py`

- Source: [src/topo_pilot/experiment/x4b.py](../../../../../../src/topo_pilot/experiment/x4b.py)
- Kind: python
- Lines: 259

## Module docstring

> X4 Phase B adapter (M1/M2): frozen inputs, float64 future maps and reachable pools.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import joint_marginals` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 15, via package root)
- `from topo_pilot.contracts import ArtifactBackend, ArtifactStore, ErrorCode, HistoryIndex, ObservationSet, StageFailure, TransitionSpec, tokens_hash` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 16, via package root)
- `from topo_pilot.oracle import BayesFilter, FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 26, via package root)
- `from .config import ResolvedConfig` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 28, via relative)
- `from .s2 import child_of` -> [src/topo_pilot/experiment/s2.py](s2.py.md) (line 29, via relative)
- `from .s3 import find_run_inputs, selected_sigma` -> [src/topo_pilot/experiment/s3.py](s3.py.md) (line 30, via relative)

### External (third-party)

- `numpy` (lines 12, 13)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py](../../../docs/proposals/X4F_GATES_OUTPUTS/family_diagnostic_script.py.md) (line 8, import)
- [src/topo_pilot/experiment/circ_audit.py](circ_audit.py.md) (line 46, import)
- [src/topo_pilot/experiment/x4b2.py](x4b2.py.md) (line 29, import)
- [src/topo_pilot/experiment/x4b2_run.py](x4b2_run.py.md) (line 36, import)
- [src/topo_pilot/experiment/x4b_audit.py](x4b_audit.py.md) (line 23, import)
- [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 36, import)
- [src/topo_pilot/experiment/x4f_data.py](x4f_data.py.md) (line 35, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 34, import)
- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 29, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 36, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 43, import)
- [src/topo_pilot/experiment/x5g1t_config.py](x5g1t_config.py.md) (line 26, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 36, import)
- [tests/experiment/test_x4b.py](../../../tests/experiment/test_x4b.py.md) (line 7, import)
- [tests/experiment/test_x5g1t_identity.py](../../../tests/experiment/test_x5g1t_identity.py.md) (line 21, import)
- [tests/experiment/test_x5g1t_identity_eval.py](../../../tests/experiment/test_x5g1t_identity_eval.py.md) (line 22, import)

## Top-level constants

- `CONS`
- `END`
- `EXPECTED`
- `MAP_LIMITS`
- `PROTOCOL_VERSION`
- `S7_RECORDS`
- `SEEDS`
- `SHARED`
- `SIGMA`

## Classes and functions

- **function `_missing`** [L56-57]: `def _missing(check: str, detail: str) -> StageFailure`
- **class `ReadThroughBackend(ArtifactBackend)`** [L60-76] - Reads from ``writable`` then ``read_only``; writes only to ``writable``.
- **method `ReadThroughBackend.__init__`** [L63-64]: `def __init__(self, read_only: ArtifactBackend, writable: ArtifactBackend) -> None`
- **method `ReadThroughBackend.put`** [L66-67]: `def put(self, key: str, data: bytes) -> None`
- **method `ReadThroughBackend.get`** [L69-70]: `def get(self, key: str) -> bytes`
- **method `ReadThroughBackend.exists`** [L72-73]: `def exists(self, key: str) -> bool`
- **method `ReadThroughBackend.list`** [L75-76]: `def list(self, prefix: str) -> list[str]`
- **function `ancestors`** [L79-91]: `def ancestors(store: ArtifactStore, artifact_id: str) -> set[str]` - Every transitive parent id of ``artifact_id``.
- **function `resolve_inputs`** [L94-118]: `def resolve_inputs(cfg: ResolvedConfig, store: ArtifactStore) -> dict[int, dict[str, str]]` - Resolve the cylinder-O inputs of each seed and check them against the frozen table.
- **function `provenance_row`** [L121-126]: `def provenance_row(store: ArtifactStore, artifact_id: str, role: str) -> dict` - Identity of one input artifact (type, producer commit, checksum, parents).
- **class `FutureMaps`** [L130-136] decorators: @dataclass(frozen=True, eq=False) - ``G1 [N, V]``, joint ``G2 [N, V*V]`` (lexicographic) and the checks of protocol §3.
- **function `future_maps`** [L144-173]: `def future_maps(T: NDArray, E: NDArray) -> FutureMaps` - Float64 one-step and joint two-step maps by two FutureOperator routes, cross-checked.
- **function `map_failures`** [L176-181]: `def map_failures(maps: FutureMaps) -> list[str]` - Names of protocol §3 checks that fail (empty when all pass).
- **function `canonical_tokens`** [L184-186]: `def canonical_tokens(tokens: NDArray, symbol_perm: NDArray) -> NDArray[np.int64]` - Canonical indices ``j`` with ``token = symbol_perm[j]`` (D-019).
- **function `index_tokens`** [L189-199]: `def index_tokens(store: ArtifactStore, index_id: str, obs_id: str) -> tuple[HistoryIndex, NDArray]` - HistoryIndex and its ``[M, 32]`` run-vocabulary tokens (checked against tokens_hash).
- **class `Pool`** [L203-215] decorators: @dataclass(frozen=True, eq=False) - One reachable pool in the canonical vocabulary (rows in the first run's index order).
- **function `build_pool`** [L218-243]: `def build_pool(name: str, split: str, runs: list[tuple[int, HistoryIndex, NDArray, NDArray]], T: NDArray, E_canon: NDArray, pi: NDArray, maps: FutureMaps) -> Pool` - Canonical pool from one or more runs sharing trajectories (``(seed, index, tokens,
- **function `pool_checks`** [L246-252]: `def pool_checks(pool: Pool, V: int) -> dict[str, float]` - Row sums, minimum entries and Σ_j Q2 = Q1 for a pool (protocol §5).
- **function `pool_failures`** [L255-259]: `def pool_failures(checks: dict[str, float]) -> list[str]` - Names of failed pool checks.

