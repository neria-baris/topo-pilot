# SPEC: `experiment` (CLI skeleton in W0; full in W4)

## Purpose

Orchestration with no science in it:
- the CLI;
- the stage runner;
- the gate registry;
- run planning (priority order);
- manifests;
- preregistration and report generation.

## Public API

```python
# CLI (entry point "topo-pilot")
topo-pilot status                                   # artifacts, gates, runs, exit level
topo-pilot stage <S0..S8|X1..X3> --config configs/stages.yaml [--executor local|bundle|ssh] [--only <run_key>]
topo-pilot gate <gate_id>                           # re-evaluate a gate from stored artifacts
topo-pilot report [--level E0..E4]                  # README + figures from MetricRecords only
topo-pilot prereg                                   # writes PREREGISTRATION.md from S2 outputs + base.yaml
topo-pilot export-bundle --stage <id> [--only <run_key>]; topo-pilot import-bundle <path>
topo-pilot export-notebook --stage <id>

class Stage(ABC):
    stage_id: ClassVar[str]; requires: ClassVar[tuple[str, ...]]; gates: ClassVar[tuple[str, ...]]
    @abstractmethod
    def plan(self, cfg: StageConfig, store) -> list[JobSpec]: ...       # one job per run where applicable
    @abstractmethod
    def execute(self, job: JobSpec, store) -> list[str]: ...           # calls module *Stage classes
STAGE_REGISTRY: dict[str, type[Stage]]

class Gate(ABC):
    gate_id: ClassVar[str]
    @abstractmethod
    def evaluate(self, store) -> GateReport: ...
GATE_REGISTRY: dict[str, type[Gate]]       # G-A ... G-G per docs/STAGES.md

class RunPlanner:
    def ordered_runs(self, stage_id: str, cfg) -> list[RunKey]: ...    # seed-major, world-paired (STAGES §2)

class ReportBuilder:
    def build(self, level: str, store) -> Path: ...                   # reads MetricRecords/GateReport/RunManifest ONLY
```

## Logic requirements

- **Configs:** read `configs/base.yaml` (closed decisions), then `configs/stages.yaml` (per-stage overrides), then the untracked `configs/local.yaml` (executor hosts and paths). The resolved config hash is stored in the RunManifest. A change to a closed key after S2 raises `CONFIG_DRIFT`, unless it is waived through H3, in which case the waiver is recorded.
- **Stage order:** a stage refuses to run if a required stage or gate is missing or failed (`GATE_FAILED`). `--waive` requires `--reason` and is recorded.
- **Execution:** each job is executed through an `Executor` (`executors` module). The runner never imports torch itself.
- **Report:**
  - the README is generated in English with exactly one finding sentence for the reached level, chosen from templates keyed by the F1 verdict (supported / rejected / inconclusive + reason);
  - the four S values, $u_r$, Δgeom, baselines, and the Gaussian floor always appear;
  - unrun stages are listed as "not run".
- **Figures:** produced by matplotlib from MetricRecords only. `make reproduce-figures` calls `topo-pilot report`.
- **`status`:** prints at most 40 lines. It is the command a new conductor runs first.

## Errors

`GATE_FAILED`, `MISSING_PARENT`, `CONFIG_DRIFT`, `EXECUTOR_ERROR` (wrapped from executors).

## Dependencies

`contracts`, `executors`, and the public `*Stage` classes of all modules. These are called, never subclassed.

## Done when

The TEST_PLAN passes, and the mini end-to-end integration test (`tests/integration`) passes.
