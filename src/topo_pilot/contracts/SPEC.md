# SPEC: `contracts` (wave W0, critical, independent tests)

## Purpose

The shared vocabulary of the project:
- artifact schemas;
- the artifact store and access policy;
- ids and seeds;
- the sequence layout;
- errors;
- tiny test fixtures.

It contains **no science**. Every other module depends on it, and it depends on nothing in the project.

## Public API

```python
SCHEMA_VERSION: str = "1.0.0"

class ErrorCode(str, Enum):
    INVALID_CONFIG; SCHEMA_VERSION_MISMATCH; ARTIFACT_MISSING; CHECKSUM_MISMATCH; LEAKAGE
    INVALID_GLUE; BETTI_MISMATCH; NON_METRIC; NONSTOCHASTIC; STATIONARITY_FAILURE
    INVALID_SIGMA; STATE_ORDER_MISMATCH; SPLIT_OVERLAP; ALIGNMENT_ERROR; IMPOSSIBLE_HISTORY
    NUMERICAL_FAILURE; NONFINITE_LOSS; CAUSAL_MASK_FAILED; UNKNOWN_HOOK; JOIN_CARDINALITY
    PH_RESOURCE_LIMIT; SAMPLE_ID_MISMATCH; GATE_FAILED; MISSING_PARENT; CONFIG_DRIFT; EXECUTOR_ERROR

class Status(str, Enum):  # non-exception outcomes stored in results
    OK; COLLAPSED; CENSORED; NONSEPARABLE; INCONCLUSIVE; NOT_RUN; APPROXIMATE

@dataclass(frozen=True)
class StageFailure(Exception):
    code: ErrorCode; component: str; check: str; detail: str
    artifact_id: str | None = None; recoverable: bool = False

@dataclass(frozen=True)
class ArtifactMeta: ...          # fields exactly as DATA_SCHEMAS §1

class Artifact(ABC):             # base of every typed artifact
    ARTIFACT_TYPE: ClassVar[str]
    def validate(self) -> None: ...                       # raises StageFailure
    @abstractmethod
    def to_payload(self) -> tuple[dict[str, np.ndarray], dict[str, Any]]: ...
    @classmethod
    @abstractmethod
    def from_payload(cls, arrays: dict[str, np.ndarray], extra: dict[str, Any]) -> Self: ...

# typed artifacts (schemas.py), one frozen dataclass each, fields per DATA_SCHEMAS:
WorldSpec, TransitionSpec, EmissionSpec, ObservationSet, EvalSidecar, HistoryIndex,
OracleOutputs, ProcessDiagnostics, BaselineOutputs, Checkpoint, ActivationSet,
DistanceArtifact, Diagrams, MetricRecords, GateReport, RunManifest

def make_artifact_id(artifact_type: str, config: Mapping, parent_ids: Sequence[str],
                     schema_version: str = SCHEMA_VERSION) -> str: ...
def canonical_json(obj: Any) -> str: ...      # sorted keys, floats via repr, no whitespace

class ArtifactBackend(ABC):                     # bytes-level storage
    def put(self, key: str, data: bytes) -> None; def get(self, key: str) -> bytes
    def exists(self, key: str) -> bool; def list(self, prefix: str) -> list[str]
class LocalFSBackend(ArtifactBackend): def __init__(self, root: Path): ...
class MirrorBackend(ArtifactBackend): def __init__(self, primary: ArtifactBackend, mirror_root: Path): ...

class AccessPolicy:
    def __init__(self, rules: Mapping[str, frozenset[str]]): ...   # artifact_type -> allowed consumers
    def check(self, artifact_type: str, consumer: str) -> None: ... # raises LEAKAGE
DEFAULT_ACCESS_POLICY: AccessPolicy               # table in DATA_SCHEMAS §7

class ArtifactStore:
    def __init__(self, backend: ArtifactBackend, policy: AccessPolicy = DEFAULT_ACCESS_POLICY): ...
    def save(self, artifact: Artifact, *, config: Mapping, parents: Sequence[str],
             seed_map: Mapping[str, int], consumer: str) -> str: ...   # validate → id → write; idempotent
    def load(self, cls: type[A], artifact_id: str, *, consumer: str) -> A: ...
    def meta(self, artifact_id: str) -> ArtifactMeta: ...
    def find(self, cls: type[Artifact], **config_filter) -> list[str]: ...
    def export_bundle(self, ids: Sequence[str], dest: Path) -> Path: ...   # tar.gz, content-addressed
    def import_bundle(self, src: Path) -> list[str]: ...                   # verifies checksums + parents

class SeedTree:
    def __init__(self, master: int): ...
    def seed(self, name: str, *scope: str | int) -> int: ...        # stable digest, platform-independent
    def generator(self, name: str, *scope: str | int) -> np.random.Generator: ...

@dataclass(frozen=True)
class SequenceLayout:
    n_obs: int = 33; context: int = 32; analysis_position: int = 32
    def bos_id(self, V: int) -> int: ...                 # == V
    def model_inputs(self, tokens: np.ndarray) -> np.ndarray: ...   # [R,33] -> [R,33] = [BOS, w1..w32]
    def targets(self, tokens: np.ndarray) -> np.ndarray: ...        # [R,33] -> [R,33] = [w1..w33]
    def history(self, tokens_row: np.ndarray, p: int) -> np.ndarray: ...  # w_1..w_p
```

`contracts.testing` contains fixtures only. It is importable from tests and never from `src` code.

```python
def tiny_world_spec(family: Literal["square","cylinder"]="cylinder", n: int = 3) -> WorldSpec
def tiny_hmm() -> tuple[np.ndarray, np.ndarray, np.ndarray]   # T[4,4], E[4,3], pi[4], hand-chosen, documented
def tiny_observations(R: int = 8, seed: int = 0) -> ObservationSet
def memory_store() -> ArtifactStore                            # in-memory backend
```

## Invariants and rules

- **Ids:** `make_artifact_id` is deterministic and independent of dict ordering, the platform, and the Python hash seed. `created_utc` is excluded from the id.
- **Saving:**
  - `save` calls `validate()` first;
  - writing an existing id verifies `payload_sha256`; a mismatch raises `CHECKSUM_MISMATCH`;
  - a partial write leaves `status = incomplete`, and `load` refuses incomplete artifacts.
- **Loading:**
  - `load` calls `policy.check` first;
  - an unknown major schema version raises `SCHEMA_VERSION_MISMATCH`.
- **Serialisation:** arrays go to a single `.npz` (no pickle). Torch state is stored as an opaque `state.pt` blob.
- **Seeds:** `SeedTree.seed` uses `sha256(master, name, *scope)`, giving the same result on every OS.
- **Layout:** `SequenceLayout` is the **only** place that encodes alignment. Its docstring reproduces the table in DATA_SCHEMAS §3.

## Dependencies

numpy and the standard library only. Torch is **not** imported here: `Checkpoint` stores the state as bytes.

## Done when

- every item of `tests/contracts/TEST_PLAN.md` passes;
- the README documents the id derivation and the access policy;
- the conductor freezes the API (DECISIONS line).
