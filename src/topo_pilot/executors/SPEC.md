# SPEC: `executors` (wave W1)

## Purpose

Run a job somewhere: locally, through a portable bundle on any machine (a notebook GPU, a rented GPU), or over ssh. No dependence on any particular cloud drive or service. See `docs/EXECUTION.md`.

## Public API

```python
@dataclass(frozen=True)
class JobSpec:
    job_id: str; stage_id: str; run_key: tuple | None
    config_hash: str; resolved_config: Mapping[str, Any]
    input_artifact_ids: tuple[str, ...]; expected_output_types: tuple[str, ...]
    resources: Mapping[str, Any]          # {"gpu": bool, "mem_gb": float, "time_h": float}
    env_lock_hash: str

@dataclass(frozen=True)
class JobHandle: job_id: str; executor: str; location: str

class Executor(ABC):
    name: ClassVar[str]
    @abstractmethod
    def submit(self, job: JobSpec, store: ArtifactStore) -> JobHandle: ...
    @abstractmethod
    def status(self, handle: JobHandle) -> Literal["pending", "running", "done", "failed", "awaiting_user"]: ...
    @abstractmethod
    def fetch(self, handle: JobHandle, store: ArtifactStore) -> list[str]: ...   # imported artifact ids

class LocalExecutor(Executor): name = "local"      # subprocess: python -m topo_pilot.executors.entry <job.json>
class BundleExecutor(Executor): name = "bundle"
    # submit -> writes bundle_<job>.tar.gz and returns status "awaiting_user" with instructions;
    # fetch(path to outputs_<job>.tar.gz) -> verify + import
class SSHExecutor(Executor): name = "ssh"          # optional; host/user/path from configs/local.yaml

EXECUTOR_REGISTRY: dict[str, type[Executor]]

def entry(job_json: Path) -> int: ...              # the in-bundle / subprocess entry point
class NotebookExporter:
    def export(self, bundle_path: Path, dest: Path) -> Path: ...   # minimal .ipynb (unpack, install lock, run, pack)
```

## Logic requirements

- **Bundle contents:** the source tree (git SHA recorded), `requirements.lock`, the resolved config, the input artifacts (via `ArtifactStore.export_bundle`), `job.json`, and `run_bundle.py`.
- **Remote run:** `run_bundle.py` verifies the input checksums, runs `entry`, and packs `outputs_<job>.tar.gz` together with a RunManifest that includes the remote hardware.
- **Import:**
  - checksum mismatch raises `CHECKSUM_MISMATCH`;
  - a missing parent raises `MISSING_PARENT`;
  - an output type outside `expected_output_types` is rejected.
- **Secrets:** none in bundles. The exporter refuses to include `configs/local.yaml`, `.env`, and any file matching `*key*` or `*token*`.
- **SSH:** uses the system `ssh` and `scp` through `subprocess`. Credentials come from the user's SSH config, never from the repository.
- **Status `awaiting_user`:** a first-class state. The conductor reports to the owner what to upload and download, then continues with other local work.

## Errors

`EXECUTOR_ERROR` (wrapping the cause), `CHECKSUM_MISMATCH`, `MISSING_PARENT`.

## Dependencies

`contracts` and the standard library (`tarfile`, `subprocess`, `json`). **Must not** import science modules: `entry` dispatches through `experiment.STAGE_REGISTRY` by name, at run time.

## Done when

The TEST_PLAN passes, and the README gives the step-by-step "run on Colab or Kaggle" procedure, with no Drive dependency.
