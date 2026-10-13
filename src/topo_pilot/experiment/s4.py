"""Stage S4 (and S5): per-run training jobs in the pre-registered order, then the analysis job.

Jobs come from ``runs_ordered`` (seed-major, world-paired; STAGES §2) followed by one
``{"job": "analysis"}`` job. Re-running is idempotent: a stored run (checkpoints + timing) is
reused instead of trained again (so the S3 smoke run is reused), and every stored value is a
function of stored artifacts, so identical ids always carry identical content.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow
from topo_pilot.prediction import LearningGate

from .config import ResolvedConfig
from .s3 import (
    TrainingRun,
    all_panels_at,
    find_run_inputs,
    run_key_of,
    selected_sigma,
    torch_threads,
)
from .s4_analysis import run_analysis
from .stages import Stage, register_stage

log = logging.getLogger(__name__)
CONS = "experiment"


def run_world(job: Mapping[str, Any]) -> str:
    """The N control is world-independent; its data come from the cylinder world (D-029)."""
    return "cylinder" if job["world"] == "any" else job["world"]


class TrainingStageBase(Stage):
    """Shared plan/execute for S4 and S5."""

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [dict(r) for r in cfg.stage(self.stage_id)["runs_ordered"]] + [{"job": "analysis"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        if job.get("job") == "analysis":
            return run_analysis(self.stage_id, cfg, store)
        import torch

        torch.set_num_threads(torch_threads(cfg.stage("S3")["device_policy"]))
        sigma = selected_sigma(store)
        inputs = find_run_inputs(store, cfg, run_world(job), job["condition"], sigma,
                                 int(job["seed"]))
        run = TrainingRun(cfg, store)
        res = run.run(inputs, run_key_of(job), int(job["seed"]), all_panels_at(cfg))
        final = run.train_cfg.steps
        acts = res.activations
        learn = run.learning(inputs, acts[final])
        check, status = LearningGate(cfg.base["learning_gate"]["captured_min"]) \
            .evaluate_with_status(learn["captured"])
        run_id = "-".join(map(str, run_key_of(job)))
        common = {"run_id": run_id, "space": "training", "world": job["world"],
                  "condition": job["condition"], "replicate": int(job["seed"])}
        rows = [MetricRow(metric_id=k, value=_finite(v), checkpoint=final,
                          status="ok" if _finite(v) is not None else "inconclusive",
                          parent_ids=(acts[final],), **common)
                for k, v in (*learn.items(), ("tokens_per_second", res.tokens_per_second),
                             ("wall_time_s", res.wall_time_s))]
        rows.append(MetricRow(metric_id="learning_gate_passed", value=float(check.passed),
                              checkpoint=final, **common))
        rows += [MetricRow(metric_id="dev_ce", value=float(ce), checkpoint=int(s), **common)
                 for s, ce in sorted(res.dev_ce_by_step.items())]
        mid = store.save(MetricRecords(rows=tuple(rows)),
                         config={"stage": self.stage_id, "kind": "run", "run_key":
                                 list(run_key_of(job))},
                         parents=[acts[final], inputs["oracle"]], seed_map={}, consumer=CONS)
        log.info("%s: run %s captured=%.3f (%s) gate=%s (%.1f min)", self.stage_id, run_id,
                 learn["captured"], status.value, check.passed, res.wall_time_s / 60)
        return [*res.checkpoints, *acts.values(), mid]


def _finite(v: float) -> float | None:
    return float(v) if np.isfinite(v) else None


@register_stage
class S4Stage(TrainingStageBase):
    """S4: 6 O runs + 1 N run, then F1, H2, R0–R3, Gaussian floor, H0 checks, gate G-F."""

    stage_id = "S4"
    requires = ("S3",)
    gates = ("G-F",)


@register_stage
class S5Stage(TrainingStageBase):
    """S5: the 6 P runs and the same analysis (H3)."""

    stage_id = "S5"
    requires = ("S4",)
    gates = ("G-F",)
