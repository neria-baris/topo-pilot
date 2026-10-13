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

## Stage S6 extras and report E3 (D-044)

- S6 job `x4curves` (when `S6.x4_curves` lists views; V1 and V5 only): per run, on panel 1 at the 12 checkpoints, S under V1 = `ln_gauge_free(resid_post_3)` and V5 = `predictive_pointset(logits)`, plus `t_rise` = first checkpoint with S_t − S_0 > u_r(view), u_r(view) from the newest X4 record (`x4:<Vk>` / `u`, same condition and replicate). Rows: space `dyn:x4:<Vk>`, metrics `S_H1` (checkpoint, panel 1), `u_r`, `t_rise` (None with `uncertainty_kind` `no_rise` / `no_envelope`). Descriptive; never a verdict. Run X4 before S6.
- `topo-pilot report --level E3` (`report_e3.build_e3`) writes `reports/E3/summary.md`, `condition_P.md` (S5 in the E2 layout + X4 section for P), `fig_dynamics.png`, `fig_x4_curves.png`. Fixed readings: H3 REJECTED is printed with the one-sided note (PREREGISTRATION §3); H4 is decided on the O cylinder runs only, P is descriptive (D-034); X4-b under P is descriptive; H3′ is a decision under P and a comparison under O (D-037).

## Stage X4 (wave WX4; `PREREGISTRATION_X4.md`, operational details D-039)

Re-analysis only: never trains, never extracts, writes no GateReport. Module `topo_pilot/experiment/x4.py` (+ `x4_inputs.py` for store resolution, `report_x4.py` for the report section). `X4Stage` is registered in `STAGE_REGISTRY` with `stage_id = "X4"`, `requires = ("S4",)`, one job.

```python
@dataclass(frozen=True)
class X4Panel:                      # one panel of one run at one checkpoint
    ids: tuple[str, ...]            # history ids, HistoryIndex order
    Z: np.ndarray                   # [M, d] resid_post_3   (V0)
    ln_out: np.ndarray              # [M, d] ln_final_out   (V2)
    logits: np.ndarray              # [M, V]                (V5)

@dataclass(frozen=True)
class X4Run:
    world: str                      # "cylinder" | "square" | "any" (N)
    condition: str                  # "O" | "P" | "N"
    seed: int
    panels: Mapping[tuple[int, int], X4Panel]     # (step, panel), step in {0, final}
    weights: Mapping[int, tuple[np.ndarray, np.ndarray, np.ndarray]]  # step -> (gamma [d], beta [d], W_U [V, d])
    oracle: Mapping[int, Mapping[str, np.ndarray]] | None
        # panel -> {"b32" [M,N], "b1" [M,N], "q" [M,V], "last_symbol" [M], "R2" [M,k], "R3" [M,k]},
        # rows in the panel's id order; None for N (b ≡ π)
    learning_gate: bool | None
    stored_S_V0: Mapping[tuple[int, int], tuple[float, str]]  # (step, panel) -> (S, status) from the source analysis; may be empty
    parents: tuple[str, ...]        # every artifact id this run's data came from

Resolver = Callable[[str], tuple[list[X4Run], list[tuple[str, str, int]]]]
    # source stage id -> (runs found, missing run keys (world, condition, seed))

class X4Job:
    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore, resolver: Resolver | None = None): ...
        # default resolver: x4_inputs.StoreResolver(cfg, store) (consumer "experiment"; Checkpoint
        # weights via learner.load_model: ln_final.weight/bias, unembed.weight)
    def rows(self, runs: Sequence[X4Run], missing: Sequence[tuple[str, str, int]]) -> list[MetricRow]: ...
    def run(self) -> str: ...       # one MetricRecords; returns its id

def x4c_category(v3_status: str, v4_status: str) -> str: ...
    # "V3_only" | "V4_only" | "both" | "neither"; a view counts iff its status == "SUPPORTED"
def run_rule_verdict(n_pass: Mapping[tuple[str, int], int], gates: Mapping[tuple[str, int], bool | None],
                     min_panels: int, n_replicates: int) -> tuple[str, str]: ...
    # keys (world, seed) over cylinder/square runs. INCONCLUSIVE (reason named) if any gate is not True,
    # or fewer than n_replicates seeds have both worlds; else SUPPORTED iff every n_pass >= min_panels,
    # else REJECTED.
```

**Settings** (`configs/stages.yaml: X4`): `sources` (subset of `[S4, S5]`; S4 → condition O, S5 → P), `views` (subset of `V0..V5`), `ln_eps`, `positive_control_min_rho`, `reuse_stored_V0`. F1 parameters come from `base.yaml: f1_rule`; `final` = `training.primary_checkpoint`.

**Views** per (run, step, panel), weights of the same step: V0 = Z; V1 = `ln_gauge_free(Z, ln_eps)`; V2 = ln_out; (V3, V4) = `split_readout(V1, readout_projector(gamma, W_U))`; V5 = `predictive_pointset(logits)`. S via `analysis.ph_summary`. V0's S is taken from `stored_S_V0` when present and `reuse_stored_V0` is true, else computed.

**Rows** (`MetricRow`; `condition`, `replicate` = seed, `world`, `panel`, `checkpoint` set where they apply; non-finite → `None` + `inconclusive`):

| space | metric_id | grain |
|---|---|---|
| `x4:<Vk>` | `S_H1` (status = PH status) | run × step × panel |
| `x4:<Vk>` | `D` | condition × replicate × panel |
| `x4:<Vk>` | `median_D`, `n_positive`, `u` | condition × replicate |
| `x4:<Vk>` | `F1rule_verdict_<STATUS>` (value 1/0/None, reasons in `uncertainty_kind`) | condition |
| `x4:<Vk>` | `delta_geom_all`, `delta_geom_same_last_symbol` (step = final) | run × panel |
| `x4:check` | `ln_reconstruction_max_abs` (‖gamma⊙V1+beta − ln_out‖∞), `logits_from_U_max_abs`, `logits_from_visible_max_abs` (vs stored logits) | run × step |
| `x4:b` | `rho_V5_future1` (step = final) | run × panel |
| `x4:b` | `rho_V5_future1_median` | run |
| `x4:b` | `positive_control_passed` (1/0), `X4b_verdict_<STATUS>` | condition |
| `x4:a` | `X4a_verdicts_equal` (1/0), `X4a_caveat` (1 iff V0 SUPPORTED and V1 not) | condition |
| `x4:c` | `median_D_V3`, `median_D_V4`, `ratio_V3_V4` (None if median_D_V4 = 0) | condition × replicate |
| `x4:c` | `X4c_<category>` (value 1) | condition |
| `x4:d:<A>` (A = V0, V1) | `rho_same_model`, `rho_same_R2`, `rho_same_R3`, `panel_pass` (1/0) | run × panel |
| `x4:d:<A>` | `n_pass` | run |
| `x4:d:<A>` | `X4d_verdict_<STATUS>` | condition |
| `x4:h3p:<A>` | `rho_all_final`, `rho_all_init`, `rho_all_R2`, `rho_all_R3`, `panel_pass` | run × panel |
| `x4:h3p:<A>` | `n_pass` | run |
| `x4:h3p:<A>` | `H3prime_verdict_<STATUS>` | condition |
| `x4` | `run_available` (status `not_run`, value None) | each missing run |

Items that need a view not in `views`, or the oracle (N runs), are skipped for that run; verdicts then follow `run_rule_verdict` / `F1Decision` (missing data → INCONCLUSIVE, never invented).

**Store contract:** `run()` saves exactly one `MetricRecords` with config `{"stage": "X4", "kind": "analysis", "sources": [...], "settings": {...}}` and parents = the sorted union of every run's `parents`; it writes nothing else. Identical inputs give the identical id (D-032).

## Errors

`GATE_FAILED`, `MISSING_PARENT`, `CONFIG_DRIFT`, `EXECUTOR_ERROR` (wrapped from executors).

## Dependencies

`contracts`, `executors`, and the public `*Stage` classes of all modules. These are called, never subclassed.

## Done when

The TEST_PLAN passes, and the mini end-to-end integration test (`tests/integration`) passes.
