"""Stage S3: smoke run (cylinder, O, seed 1729), CPU throughput, compute projection, gate G-E.

``TrainingRun`` is the shared per-run procedure (train → extract activations → learning
metrics) reused by S4/S5; identical run keys give identical artifact ids, so S4 reuses the
S3 run (STAGES §2).
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.activations import ActivationStage
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    GateCheck,
    GateReport,
    HistoryIndex,
    MetricRecords,
    MetricRow,
    ObservationSet,
    OracleOutputs,
    ProcessDiagnostics,
    SeedTree,
    StageFailure,
    WorldSpec,
)
from topo_pilot.learner import LearnerStage, ModelConfig, TrainConfig
from topo_pilot.prediction import LearningGate, PredictiveMetrics

from .config import ResolvedConfig
from .s2 import MODES, child_of
from .stages import Stage, register_stage

log = logging.getLogger(__name__)
CONS = "experiment"


def physical_cores() -> int:
    """Physical core count (logical / 2 when hyper-threaded is assumed), at least 1."""
    logical = os.cpu_count() or 1
    return max(1, logical // 2) if logical >= 4 else logical


def find_run_inputs(store: ArtifactStore, family: str, cond: str, sigma: float | None,
                    master: int) -> dict[str, str]:
    """Locate the S2 artifacts of one (world, condition, replicate)."""
    world = store.find(WorldSpec, family=family)[0]
    flt: dict[str, Any] = {"mode": MODES[cond], "replicate": master}
    flt["sigma"] = sigma if cond in "OP" else None
    emis = child_of(store, EmissionSpec, world, **flt)
    out = {"world": world, "emission": emis}
    for split in ("train", "dev", "test"):
        out[f"obs_{split}"] = child_of(store, ObservationSet, emis, split=split)
    out["history_index"] = child_of(store, HistoryIndex, out["obs_test"])
    out["oracle"] = child_of(store, OracleOutputs, out["history_index"])
    out["diagnostics"] = child_of(store, ProcessDiagnostics, out["history_index"])
    return out


class TrainingRun:
    """Train one model and extract its activations per the stage's extraction policy."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        base = cfg.base
        V = base["emissions"]["V"]
        m, t = base["model"], base["training"]
        self.model_cfg = ModelConfig(vocab_in=V + 1, vocab_out=V, n_ctx=base["sequences"]["n_obs"],
                                     n_layers=m["n_layers"], d_model=m["d_model"],
                                     n_heads=m["n_heads"], d_mlp=m["d_mlp"],
                                     dropout=m["dropout"], tie_embeddings=m["tie_embeddings"])
        self.train_cfg = TrainConfig(steps=t["steps"], batch_size=t["batch_size"], lr=t["lr"],
                                     warmup=t["warmup"], weight_decay=t["weight_decay"],
                                     grad_clip=t["grad_clip"],
                                     checkpoint_steps=tuple(t["checkpoints"]))
        self.hooks = tuple(m["hooks"])

    def train(self, inputs: Mapping[str, str], run_key: tuple, master: int):
        stage = LearnerStage()
        ids = stage.run(inputs["obs_train"], inputs["obs_dev"], self.model_cfg, self.train_cfg,
                        SeedTree(master), run_key, self.store)
        return ids, stage.last_summary

    def extract(self, inputs: Mapping[str, str], ckpt_ids: list[str],
                all_panels_at: tuple[int, ...]) -> dict[int, str]:
        """ActivationSet ids by step: all panels at ``all_panels_at``, panel 1 elsewhere."""
        steps = list(self.train_cfg.checkpoint_steps)
        out = {}
        for step, cid in zip(steps, ckpt_ids):
            panels = None if step in all_panels_at else [1]
            out[step] = ActivationStage().run(cid, inputs["obs_test"], inputs["history_index"],
                                              self.hooks, panels, self.store)
        return out

    def learning(self, inputs: Mapping[str, str], act_id: str) -> dict[str, float]:
        """Regret, G_C and captured at p = 32 over the activation set's histories."""
        acts = self.store.load(ActivationSet, act_id, consumer=CONS)
        oracle = self.store.load(OracleOutputs, inputs["oracle"], consumer=CONS)
        diag = self.store.load(ProcessDiagnostics, inputs["diagnostics"], consumer=CONS)
        row = {h: i for i, h in enumerate(oracle.history_id.tolist())}
        idx = np.array([row[h] for h in acts.history_id.tolist()])
        logits = acts.logits.astype(np.float64)
        p = np.exp(logits - logits.max(axis=1, keepdims=True))
        p /= p.sum(axis=1, keepdims=True)
        regret = PredictiveMetrics.regret(oracle.q[idx], p)
        return {"regret": regret, "G_C": diag.G_C,
                "captured": PredictiveMetrics.captured(regret, diag.G_C)}


@register_stage
class S3Stage(Stage):
    """S3: the smoke run, throughput, the S4/S5 projection, and gate G-E."""

    stage_id = "S3"
    requires = ("S2",)
    gates = ("G-E",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [dict(r) for r in cfg.stage("S3")["runs"]]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        import torch

        policy = cfg.stage("S3")["device_policy"]
        torch.set_num_threads(physical_cores())
        sigma = _selected_sigma(store)
        inputs = find_run_inputs(store, job["world"], job["condition"], sigma, job["seed"])
        run = TrainingRun(cfg, store)
        run_key = (job["world"], job["condition"], job["seed"])
        ckpts, summary = run.train(inputs, run_key, job["seed"])
        final = run.train_cfg.steps
        acts = run.extract(inputs, ckpts, tuple(cfg.stage("S4")["extract"]["all_panels_at"]))
        learn = run.learning(inputs, acts[final])
        gate_check, status = LearningGate(cfg.base["learning_gate"]["captured_min"]) \
            .evaluate_with_status(learn["captured"])
        hours_per_run = summary.wall_time_s / 3600.0
        n_s4 = len(cfg.stage("S4")["runs_ordered"]) - 1
        projected = {"S4": n_s4 * hours_per_run, "S5": len(cfg.stage("S5")["runs_ordered"])
                     * hours_per_run}
        limit = float(policy["local_cpu_max_projected_hours"])
        rows = [MetricRow(run_id="-".join(map(str, run_key)), space="training", metric_id=k,
                          value=float(v), world=job["world"], condition=job["condition"],
                          replicate=job["seed"], checkpoint=final, parent_ids=(acts[final],))
                for k, v in (*learn.items(), ("tokens_per_second", summary.tokens_per_second),
                             ("wall_time_s", summary.wall_time_s),
                             ("projected_hours_S4", projected["S4"]),
                             ("projected_hours_S5", projected["S5"]))]
        rows += [MetricRow(run_id="-".join(map(str, run_key)), space="training",
                           metric_id="dev_ce", value=float(ce), checkpoint=int(step),
                           world=job["world"], condition=job["condition"], replicate=job["seed"])
                 for step, ce in sorted(summary.dev_ce_by_step.items())]
        mid = store.save(MetricRecords(rows=tuple(rows)),
                         config={"stage": "S3", "run_key": list(run_key)},
                         parents=[acts[final], inputs["oracle"]], seed_map={}, consumer=CONS)
        checks = (gate_check,
                  GateCheck("projected_S4_hours_local_cpu", projected["S4"] <= limit,
                            round(projected["S4"], 3), limit))
        verdict = "pass" if all(c.passed for c in checks) else "fail"
        gid = store.save(GateReport(stage="S3", gate_id="G-E", verdict=verdict, checks=checks),
                         config={"stage": "S3", "gate": "G-E", "config_hash": cfg.config_hash},
                         parents=[mid], seed_map={}, consumer=CONS)
        log.info("S3: captured=%.3f (%s), %.0f tok/s, run %.1f min, S4 projected %.2f h",
                 learn["captured"], status.value, summary.tokens_per_second,
                 summary.wall_time_s / 60, projected["S4"])
        return [*ckpts, *acts.values(), mid, gid]


def _selected_sigma(store: ArtifactStore) -> float:
    for mid in store.find(MetricRecords, stage="S2"):
        for r in store.load(MetricRecords, mid, consumer=CONS).rows:
            if r.space == "sigma" and r.metric_id == "selected":
                return float(r.value)
    raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.S3", "sigma",
                       "S2 sigma decision not found in MetricRecords")
