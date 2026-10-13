"""Stage S3: smoke run (cylinder, O, seed 1729), CPU throughput, compute projection, gate G-E.

``TrainingRun`` is the shared per-run procedure (train → extract activations → learning
metrics) reused by S4/S5. A run whose checkpoints and timing are already stored is not trained
again, and stored ActivationSets are not extracted again, so S4 reuses the S3 run (STAGES §2)
and re-running a stage after a failure repeats no finished work.
"""

from __future__ import annotations

import dataclasses
import logging
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from topo_pilot.activations import ActivationStage
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
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
)
from topo_pilot.learner import LearnerStage, ModelConfig, TrainConfig
from topo_pilot.prediction import LearningGate, PredictiveMetrics

from .config import ResolvedConfig
from .s2 import MODES, child_of, world_id
from .stages import Stage, register_stage

log = logging.getLogger(__name__)
CONS = "experiment"
TIMING_METRICS = ("wall_time_s", "tokens_per_second")


def physical_cores() -> int:
    """Physical core count (logical / 2 when hyper-threaded is assumed), at least 1."""
    logical = os.cpu_count() or 1
    return max(1, logical // 2) if logical >= 4 else logical


def torch_threads(policy: Mapping[str, Any]) -> int:
    """Thread count from ``device_policy.torch_threads``: ``physical_cores`` or an integer."""
    value = policy.get("torch_threads", "physical_cores")
    return physical_cores() if value == "physical_cores" else max(1, int(value))


def all_panels_at(cfg: ResolvedConfig) -> tuple[int, ...]:
    """Checkpoint steps extracted on all panels (panel 1 only elsewhere); STAGES §2."""
    return tuple(int(s) for s in cfg.stage("S4")["extract"]["all_panels_at"])


def find_run_inputs(store: ArtifactStore, cfg: ResolvedConfig, family: str, cond: str,
                    sigma: float | None, master: int) -> dict[str, str]:
    """Locate the S2 artifacts of one (world, condition, replicate)."""
    world = world_id(store, cfg, family)
    flt: dict[str, Any] = {"mode": MODES[cond], "replicate": master}
    flt["sigma"] = sigma if cond in ("O", "P") else None
    emis = child_of(store, EmissionSpec, world, **flt)
    out = {"world": world, "emission": emis}
    for split in ("train", "dev", "test"):
        out[f"obs_{split}"] = child_of(store, ObservationSet, emis, split=split)
    out["history_index"] = child_of(store, HistoryIndex, out["obs_test"])
    out["oracle"] = child_of(store, OracleOutputs, out["history_index"])
    out["diagnostics"] = child_of(store, ProcessDiagnostics, out["history_index"])
    return out


def run_key_of(job: Mapping[str, Any]) -> tuple:
    return (job["world"], job["condition"], int(job["seed"]))


def on_test_split(store: ArtifactStore, activation_set_id: str) -> bool:
    """True if the ActivationSet was extracted from test histories (S7 also extracts dev
    histories for probes and PCA, D-047; those never enter the test-panel analyses)."""
    return any(store.meta(p).artifact_type == "ObservationSet"
               and store.meta(p).config.get("split") == "test"
               for p in store.meta(activation_set_id).parent_ids)


def activation_ids(store: ArtifactStore, job: Mapping[str, Any], steps: tuple[int, ...],
                   panels: str = "all",
                   train_config: Mapping[str, Any] | None = None) -> dict[int, str]:
    """ActivationSet ids of one run at ``steps`` with the given panel coverage.

    Steps without a checkpoint or without such an ActivationSet are absent from the result (a
    run not done yet). ``train_config`` (optional) restricts the checkpoints to one training
    configuration; more than one matching checkpoint raises ``INVALID_CONFIG``.
    """
    flt: dict[str, Any] = {"run_key": list(run_key_of(job))}
    if train_config is not None:
        flt["train_config"] = dict(train_config)
    out = {}
    for step in steps:
        cids = store.find(Checkpoint, step=step, **flt)
        if len(cids) > 1:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.activation_ids",
                               "checkpoint", f"{len(cids)} checkpoints for {flt['run_key']} "
                               f"step {step}; pass train_config to choose one")
        found = store.find(ActivationSet, checkpoint_id=cids[0], panels=panels) if cids else []
        found = [a for a in found if on_test_split(store, a)]
        if found:
            out[step] = found[0]
    return out


@dataclass(frozen=True)
class RunResult:
    """Outputs of one training run: checkpoint ids (step order), ActivationSet ids by step, and
    the timing of the training that produced the checkpoints (fixed once recorded)."""

    checkpoints: tuple[str, ...]
    activations: dict[int, str]
    wall_time_s: float
    tokens_per_second: float
    dev_ce_by_step: dict[int, float]


class TrainingRun:
    """Train one model (or reuse a stored run) and extract its activations."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore, V: int | None = None):
        """``V`` overrides the vocabulary of ``base.yaml`` (the U control has V = N = 144)."""
        self.cfg, self.store = cfg, store
        base = cfg.base
        V = int(V) if V is not None else base["emissions"]["V"]
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

    def run(self, inputs: Mapping[str, str], run_key: tuple, master: int,
            all_panels: Sequence[int]) -> RunResult:
        """Checkpoints (stored, or trained now), then activations at every checkpoint."""
        ckpts = self.stored_checkpoints(inputs, run_key)
        timing = self.stored_timing(run_key, ckpts) if ckpts is not None else None
        if ckpts is None or timing is None:
            ckpts, timing = self._train(inputs, run_key, master)
        else:
            log.info("run %s: reusing %d stored checkpoints", run_key, len(ckpts))
        acts = self.extract(inputs, ckpts, tuple(all_panels))
        return RunResult(tuple(ckpts), acts, **timing)

    def _train(self, inputs: Mapping[str, str], run_key: tuple,
               master: int) -> tuple[list[str], dict[str, Any]]:
        stage = LearnerStage()
        ids = stage.run(inputs["obs_train"], inputs["obs_dev"], self.model_cfg, self.train_cfg,
                        SeedTree(master), run_key, self.store)
        summary = stage.last_summary
        timing = {"wall_time_s": float(summary.wall_time_s),
                  "tokens_per_second": float(summary.tokens_per_second),
                  "dev_ce_by_step": {int(k): float(v) for k, v in summary.dev_ce_by_step.items()}}
        run_id = "-".join(map(str, run_key))
        rows = [MetricRow(run_id=run_id, space="training", metric_id=k, value=timing[k])
                for k in TIMING_METRICS]
        rows += [MetricRow(run_id=run_id, space="training", metric_id="dev_ce", value=ce,
                           checkpoint=step)
                 for step, ce in sorted(timing["dev_ce_by_step"].items())]
        self.store.save(MetricRecords(rows=tuple(rows)),
                        config={"kind": "run_timing", "run_key": list(run_key)},
                        parents=ids, seed_map={}, consumer=CONS)
        return ids, timing

    def stored_checkpoints(self, inputs: Mapping[str, str], run_key: tuple) -> list[str] | None:
        """Ids of a complete stored run (exactly one checkpoint per step), else None."""
        ids = []
        for step in self.train_cfg.checkpoint_steps:
            found = [c for c in self.store.find(
                         Checkpoint, run_key=list(run_key), step=step,
                         model_config=dataclasses.asdict(self.model_cfg),
                         train_config=dataclasses.asdict(self.train_cfg))
                     if inputs["obs_train"] in self.store.meta(c).parent_ids]
            if len(found) != 1:
                return None
            ids.append(found[0])
        return ids

    def _linked(self, mid: str, ckpts: set[str]) -> bool:
        """True if MetricRecords ``mid`` was derived from one of ``ckpts`` (directly, or via an
        ActivationSet of one of them)."""
        for pid in self.store.meta(mid).parent_ids:
            meta = self.store.meta(pid)
            if pid in ckpts or (meta.artifact_type == "ActivationSet"
                                and meta.config.get("checkpoint_id") in ckpts):
                return True
        return False

    def stored_timing(self, run_key: tuple, ckpt_ids: Sequence[str]) -> dict[str, Any] | None:
        """Timing of the training that produced ``ckpt_ids``, from any MetricRecords of
        ``run_key`` derived from those checkpoints (the ``run_timing`` record, or a stage record
        such as S3's); None if there is none. A record of the same run key but another training
        configuration never matches."""
        ckpts = set(ckpt_ids)
        for mid in self.store.find(MetricRecords, run_key=list(run_key)):
            if not self._linked(mid, ckpts):
                continue
            rows = self.store.load(MetricRecords, mid, consumer=CONS).rows
            vals = {r.metric_id: r.value for r in rows
                    if r.space == "training" and r.metric_id in TIMING_METRICS}
            dev = {int(r.checkpoint): float(r.value) for r in rows
                   if r.metric_id == "dev_ce" and r.checkpoint is not None and r.value is not None}
            if all(vals.get(k) is not None for k in TIMING_METRICS) and dev:
                return {**{k: float(vals[k]) for k in TIMING_METRICS}, "dev_ce_by_step": dev}
        return None

    def extract(self, inputs: Mapping[str, str], ckpt_ids: Sequence[str],
                all_panels: tuple[int, ...]) -> dict[int, str]:
        """ActivationSet ids by step: all panels at ``all_panels``, panel 1 elsewhere; stored
        sets are reused."""
        out = {}
        for step, cid in zip(self.train_cfg.checkpoint_steps, ckpt_ids):
            panels = None if step in all_panels else [1]
            found = self.store.find(ActivationSet, checkpoint_id=cid, hooks=list(self.hooks),
                                    panels="all" if panels is None else panels)
            out[step] = found[0] if found else ActivationStage().run(
                cid, inputs["obs_test"], inputs["history_index"], self.hooks, panels, self.store)
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
        torch.set_num_threads(torch_threads(policy))
        sigma = selected_sigma(store)
        inputs = find_run_inputs(store, cfg, job["world"], job["condition"], sigma, job["seed"])
        run = TrainingRun(cfg, store)
        run_key = (job["world"], job["condition"], job["seed"])
        res = run.run(inputs, run_key, job["seed"], all_panels_at(cfg))
        final = run.train_cfg.steps
        acts = res.activations
        learn = run.learning(inputs, acts[final])
        gate_check, status = LearningGate(cfg.base["learning_gate"]["captured_min"]) \
            .evaluate_with_status(learn["captured"])
        hours_per_run = res.wall_time_s / 3600.0
        n_s4 = len(cfg.stage("S4")["runs_ordered"]) - 1
        projected = {"S4": n_s4 * hours_per_run, "S5": len(cfg.stage("S5")["runs_ordered"])
                     * hours_per_run}
        limit = float(policy["local_cpu_max_projected_hours"])
        rows = [MetricRow(run_id="-".join(map(str, run_key)), space="training", metric_id=k,
                          value=float(v), world=job["world"], condition=job["condition"],
                          replicate=job["seed"], checkpoint=final, parent_ids=(acts[final],))
                for k, v in (*learn.items(), ("tokens_per_second", res.tokens_per_second),
                             ("wall_time_s", res.wall_time_s),
                             ("projected_hours_S4", projected["S4"]),
                             ("projected_hours_S5", projected["S5"]))]
        rows += [MetricRow(run_id="-".join(map(str, run_key)), space="training",
                           metric_id="dev_ce", value=float(ce), checkpoint=int(step),
                           world=job["world"], condition=job["condition"], replicate=job["seed"])
                 for step, ce in sorted(res.dev_ce_by_step.items())]
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
                 learn["captured"], status.value, res.tokens_per_second,
                 res.wall_time_s / 60, projected["S4"])
        return [*res.checkpoints, *acts.values(), mid, gid]


def selected_sigma(store: ArtifactStore) -> float:
    """The σ selected in S2 (MetricRecords row ``space=sigma, metric_id=selected``)."""
    for mid in store.find(MetricRecords, stage="S2"):
        for r in store.load(MetricRecords, mid, consumer=CONS).rows:
            if r.space == "sigma" and r.metric_id == "selected":
                return float(r.value)
    raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.S3", "sigma",
                       "S2 sigma decision not found in MetricRecords")
