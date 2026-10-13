"""Stage S7: U and extra N controls, dev panels, probes, circular coordinates, sensitivity, G-G.

Jobs (D-047), in order: the four control runs of ``S7.runs_ordered`` (U-cyl, U-sq, N-2718,
N-3141), then ``dev_extract``, ``controls``, ``probes``, ``circular``, ``sensitivity`` and
``gate``. Every analysis job writes one MetricRecords (config ``stage = S7``, ``kind`` = the job
name). A run that fails is recorded as a ``not_run`` row with the error, never dropped (G-G:
all runs documented, failures included). Stored runs and records are reused (D-032), so the
stage can be re-run after an interruption.

S7 needs the S6 records (dynamics); S6 writes no gate, so S7 requires the G-F gates of S4 and S5
and checks the S6 records itself.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    GateCheck,
    GateReport,
    MetricRecords,
    MetricRow,
    OracleOutputs,
    StageFailure,
)
from topo_pilot.prediction import LearningGate, PredictiveMetrics

from .config import ResolvedConfig
from .s3 import TrainingRun, all_panels_at, find_run_inputs, run_key_of, torch_threads
from .s4 import run_world
from .stages import Stage, register_stage

log = logging.getLogger(__name__)
CONS = "experiment"
ANALYSIS_JOBS = ("dev_extract", "controls", "probes", "circular", "sensitivity")


def run_inputs(cfg: ResolvedConfig, store: ArtifactStore, job: Mapping[str, Any]) -> dict:
    """S2 artifacts of an S7 run (U and N have no σ; N uses the cylinder world, D-029)."""
    from .s3 import selected_sigma

    cond = job["condition"]
    sigma = selected_sigma(store) if cond in ("O", "P") else None
    return find_run_inputs(store, cfg, run_world(job), cond, sigma, int(job["seed"]))


def _finite(v: float | None) -> float | None:
    return float(v) if v is not None and np.isfinite(v) else None


def u_context_gain(store: ArtifactStore, inputs: Mapping[str, str], act_id: str) -> float:
    """``G_U = mean KL(q_C || pi E)`` over the run's final-checkpoint histories (D-047): the
    gain of the exact predictor over the unigram marginal. Under U, ``G_C = 0`` by
    construction (the last symbol reveals the state), so this replaces it for the
    descriptive U sanity check."""
    from topo_pilot.contracts import ActivationSet, TransitionSpec

    from .s2 import child_of

    acts = store.load(ActivationSet, act_id, consumer=CONS)
    oracle = store.load(OracleOutputs, inputs["oracle"], consumer=CONS)
    emis = store.load(EmissionSpec, inputs["emission"], consumer=CONS)
    trans = store.load(TransitionSpec, child_of(store, TransitionSpec, inputs["world"]),
                       consumer=CONS)
    row = {h: i for i, h in enumerate(oracle.history_id.tolist())}
    q = oracle.q[[row[h] for h in acts.history_id.tolist()]]
    p_w = np.asarray(trans.pi, dtype=np.float64) @ np.asarray(emis.E, dtype=np.float64)
    return float(np.mean(PredictiveMetrics.kl(q, np.repeat(p_w[None, :], len(q), axis=0))))


class S7Runs:
    """Training jobs of S7: train (or reuse) one control run and write its run record."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        self.u_min = float(cfg.stage("S7").get("u_sanity_captured_min", 0.8))

    def execute(self, job: Mapping[str, Any]) -> list[str]:
        try:
            return self._train(job)
        except Exception as exc:  # documented failure (G-G), never silent
            log.error("S7: run %s failed: %s", run_key_of(job), exc)
            detail = (f"{exc.code.value}: {exc.check}" if isinstance(exc, StageFailure)
                      else type(exc).__name__)
            row = MetricRow(run_id="-".join(map(str, run_key_of(job))), space="training",
                            metric_id="run_available", value=None, status="not_run",
                            world=job["world"], condition=job["condition"],
                            replicate=int(job["seed"]), uncertainty_kind=detail[:200])
            return [self.store.save(MetricRecords(rows=(row,)),
                                    config={"stage": "S7", "kind": "run", "outcome": "failed",
                                            "run_key": list(run_key_of(job))},
                                    parents=[], seed_map={}, consumer=CONS)]

    def _train(self, job: Mapping[str, Any]) -> list[str]:
        import torch

        torch.set_num_threads(torch_threads(self.cfg.stage("S3")["device_policy"]))
        inputs = run_inputs(self.cfg, self.store, job)
        V = int(self.store.meta(inputs["obs_train"]).config["V"])
        run = TrainingRun(self.cfg, self.store, V=V)
        res = run.run(inputs, run_key_of(job), int(job["seed"]), all_panels_at(self.cfg))
        final = run.train_cfg.steps
        acts = res.activations
        learn = run.learning(inputs, acts[final])
        check, status = LearningGate(self.cfg.base["learning_gate"]["captured_min"]) \
            .evaluate_with_status(learn["captured"])
        run_id = "-".join(map(str, run_key_of(job)))
        common = {"run_id": run_id, "space": "training", "world": job["world"],
                  "condition": job["condition"], "replicate": int(job["seed"])}
        values = [*learn.items(), ("tokens_per_second", res.tokens_per_second),
                  ("wall_time_s", res.wall_time_s), ("V", float(V))]
        if job["condition"] == "U":
            g_u = u_context_gain(self.store, inputs, acts[final])
            cap_u = 1.0 - learn["regret"] / g_u if g_u > 1e-6 else None
            values += [("G_U", g_u), ("captured_U", cap_u)]
        rows = [MetricRow(metric_id=k, value=_finite(v), checkpoint=final,
                          status="ok" if _finite(v) is not None else "inconclusive",
                          parent_ids=(acts[final],), **common) for k, v in values]
        rows.append(MetricRow(metric_id="learning_gate_passed",
                              value=float(check.passed) if status.value == "ok" else None,
                              status=status.value, checkpoint=final,
                              uncertainty_kind=None if status.value == "ok"
                              else "G_C = 0 by construction", **common))
        if job["condition"] == "U":
            cap_u = dict(values)["captured_U"]
            rows.append(MetricRow(
                metric_id="u_sanity_passed", value=None if cap_u is None
                else float(cap_u >= self.u_min), status="ok" if cap_u is not None
                else "inconclusive", checkpoint=final, uncertainty_kind="descriptive", **common))
        rows += [MetricRow(metric_id="dev_ce", value=float(ce), checkpoint=int(s), **common)
                 for s, ce in sorted(res.dev_ce_by_step.items())]
        if job["condition"] == "N":
            from .s7_controls import h0_rows

            rows += h0_rows(self.cfg, self.store, inputs, acts[final], int(job["seed"]))
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": "S7", "kind": "run",
                                      "run_key": list(run_key_of(job))},
                              parents=[acts[final], inputs["oracle"]], seed_map={},
                              consumer=CONS)
        log.info("S7: run %s done (%.1f min, regret %.4f)", run_id, res.wall_time_s / 60,
                 learn["regret"])
        return [*res.checkpoints, *acts.values(), mid]


def s7_records(store: ArtifactStore, kind: str) -> list[str]:
    """Ids of the S7 MetricRecords of one ``kind``."""
    return store.find(MetricRecords, stage="S7", kind=kind)


def gate_gg(cfg: ResolvedConfig, store: ArtifactStore) -> str:
    """G-G (D-047): every planned S7 run has a run record (trained, or not_run with its error)
    and every analysis job wrote its record. Results (H0, U sanity) are reported, not gated."""
    checks, parents = [], []
    for job in cfg.stage("S7")["runs_ordered"]:
        key = list(run_key_of(job))
        found = store.find(MetricRecords, stage="S7", kind="run", run_key=key)
        parents += found
        checks.append(GateCheck(f"run_documented_{'-'.join(map(str, key))}", bool(found),
                                len(found), ">= 1 record"))
    for kind in ANALYSIS_JOBS:
        found = s7_records(store, kind)
        parents += found
        checks.append(GateCheck(f"analysis_documented_{kind}", bool(found), len(found),
                                ">= 1 record"))
    verdict = "pass" if all(c.passed for c in checks) else "fail"
    return store.save(GateReport(stage="S7", gate_id="G-G", verdict=verdict, checks=tuple(checks)),
                      config={"stage": "S7", "gate": "G-G", "config_hash": cfg.config_hash},
                      parents=sorted(set(parents)), seed_map={}, consumer=CONS)


@register_stage
class S7Stage(Stage):
    """S7: control runs, probes, circular coordinates, sensitivity; gate G-G."""

    stage_id = "S7"
    requires = ("S4", "S5")
    gates = ("G-G",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        for cond in ("O", "P"):
            if not store.find(MetricRecords, stage="S6", kind="dynamics", condition=cond):
                raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.S7", "S6",
                                   f"no S6 dynamics record for condition {cond}")
        return ([dict(r) for r in cfg.stage("S7")["runs_ordered"]]
                + [{"job": j} for j in (*ANALYSIS_JOBS, "gate")])

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        kind = job.get("job")
        if kind is None:
            return S7Runs(cfg, store).execute(job)
        if kind == "gate":
            return [gate_gg(cfg, store)]
        from . import s7_jobs

        return s7_jobs.run(kind, cfg, store)
