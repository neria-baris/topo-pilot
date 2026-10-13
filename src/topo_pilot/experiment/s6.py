"""Stage S6: training dynamics and H4 (D-034), checkpoint-order null, layer sweep.

Per condition (O always; P once S5 has an analysis) two jobs, each writing one MetricRecords
(``kind`` = ``dynamics`` or ``layers``):

- **dynamics:** on panel 1 at the 12 checkpoints, S of the primary hook and the regret
  KL(q_C || p_model); ``t_h`` (first regret < G_C), ``t_s`` (first S_t − S_0 > u_r, with u_r the
  replicate's F1 envelope from the S4/S5 analysis), the run's H4 classification, the
  checkpoint-order null (descriptive), and the H4 verdict over the cylinder runs.
- **layers:** the F1 contrast D (8 panels, checkpoints 0 and final) for every hook and for
  their concatenation (descriptive, RESEARCH_SUMMARY §7.7).

Missing runs are recorded as ``not_run``, never invented. S6 has no gate.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.analysis import Dynamics, F1Decision, LayerSweep, ph_summary
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    MetricRecords,
    MetricRow,
    OracleOutputs,
    ProcessDiagnostics,
    SeedTree,
)
from topo_pilot.prediction import PredictiveMetrics

from .config import ResolvedConfig
from .report_e2 import analysis_rows
from .s3 import activation_ids
from .s4_analysis import WORLDS, AnalysisJob, _row
from .stages import Stage, register_stage

log = logging.getLogger(__name__)
CONS = "experiment"
STAGE_OF = {"O": "S4", "P": "S5"}
H4_CODE = {"consistent": 1.0, "violated": 0.0}


def h4_class(t_h: int | None, t_s: int | None) -> str:
    """D-034 classification of one run: ``consistent``, ``violated``, ``no_rise`` or
    ``no_history_use`` (regret never drops below G_C)."""
    if t_s is None:
        return "no_rise"
    if t_h is None:
        return "no_history_use"
    return "consistent" if t_s >= t_h else "violated"


def h4_verdict(classes: list[str], gates: list[bool], n_required: int) -> tuple[str, str]:
    """D-034 verdict over the cylinder runs: ``(SUPPORTED|REJECTED|INCONCLUSIVE, reason)``."""
    if "violated" in classes and all(gates):
        return "REJECTED", "S rose before history use in a cylinder run"
    if len(classes) < n_required:
        return "INCONCLUSIVE", f"cylinder runs: {len(classes)} < {n_required}"
    if not all(gates):
        return "INCONCLUSIVE", "a learning gate failed"
    if all(c == "consistent" for c in classes):
        return "SUPPORTED", ""
    return "INCONCLUSIVE", "runs: " + ", ".join(classes)


def first_step(steps: list[int], flags: list[bool]) -> int | None:
    return next((s for s, f in zip(steps, flags) if f), None)


class S6Job:
    """Dynamics and layer sweep of one condition, on top of the S4/S5 analysis lookups."""

    def __init__(self, cond: str, cfg: ResolvedConfig, store: ArtifactStore):
        self.cond, self.cfg, self.store = cond, cfg, store
        self.aj = AnalysisJob(STAGE_OF[cond], cfg, store)
        self.steps = [int(s) for s in self.aj.train_config["checkpoint_steps"]]
        self.n_perm = int(cfg.stage("S6")["checkpoint_order_null_permutations"])
        self.u = {r.replicate: r.value for r in analysis_rows(store, STAGE_OF[cond])
                  if r.space == "F1" and r.metric_id == "u"}

    @property
    def parents(self) -> set[str]:
        return self.aj.parents

    def act_at(self, world: str, seed: int, step: int) -> str:
        """ActivationSet id at ``step`` (all panels where extracted, else panel 1 only)."""
        job = {"world": world, "condition": self.cond, "seed": seed}
        for panels in ("all", [1]):
            ids = activation_ids(self.store, job, (step,), panels=panels,
                                 train_config=self.aj.train_config)
            if step in ids:
                self.parents.add(ids[step])
                return ids[step]
        raise KeyError(f"no activations for {job} step {step}")

    # ---- dynamics -------------------------------------------------------------------------
    def curve(self, world: str, seed: int) -> tuple[list[float], list[float], float]:
        """S and regret on panel 1 at every checkpoint, and G_C."""
        inputs = self.aj.inputs(world, self.cond, seed)
        oracle = self.store.load(OracleOutputs, inputs["oracle"], consumer=CONS)
        G_C = float(self.store.load(ProcessDiagnostics, inputs["diagnostics"],
                                    consumer=CONS).G_C)
        q_row = {str(h): i for i, h in enumerate(oracle.history_id.tolist())}
        S, regret = [], []
        for step in self.steps:
            aid = self.act_at(world, seed, step)
            ps = self.aj.sb.activations(aid, self.aj.hook, 1)
            S.append(float(ph_summary(ps)["S_H1"]))
            acts = self.store.load(ActivationSet, aid, consumer=CONS)
            a_row = {str(h): i for i, h in enumerate(acts.history_id.tolist())}
            logits = acts.logits.astype(np.float64)[[a_row[h] for h in ps.ids]]
            p = np.exp(logits - logits.max(axis=1, keepdims=True))
            p /= p.sum(axis=1, keepdims=True)
            regret.append(PredictiveMetrics.regret(oracle.q[[q_row[h] for h in ps.ids]], p))
        return S, regret, G_C

    def dynamics(self) -> list[MetricRow]:
        rows: list[MetricRow] = []
        classes, gates = [], []
        for seed in self.cfg.base["seeds"]["masters"]:
            for world in WORLDS:
                common = {"world": world, "condition": self.cond, "replicate": seed}
                try:
                    S, regret, G_C = self.curve(world, seed)
                except KeyError as exc:
                    log.warning("S6 dynamics: %s %s missing (%s)", world, seed, exc)
                    rows.append(_row("run_available", None, "dyn", status="not_run", **common))
                    continue
                rows += [_row("S_H1", s, "dyn:S", checkpoint=t, panel=1, **common)
                         for t, s in zip(self.steps, S)]
                rows += [_row("regret", r, "dyn:regret", checkpoint=t, panel=1, **common)
                         for t, r in zip(self.steps, regret)]
                u = self.u.get(seed)
                t_h = first_step(self.steps, [r < G_C for r in regret])
                t_s = None if u is None else first_step(self.steps, [s - S[0] > u for s in S])
                cls = h4_class(t_h, t_s) if u is not None else "no_envelope"
                null = Dynamics().checkpoint_order_null(
                    S, self.n_perm, SeedTree(0).generator("s6_order_null", world, self.cond,
                                                          seed))
                rows += [_row("G_C", G_C, "dyn", **common), _row("u_r", u, "dyn", **common),
                         _row("t_history", t_h, "dyn", **common),
                         _row("t_rise", t_s, "dyn", **common),
                         _row("h4_consistent", H4_CODE.get(cls), "dyn", uncertainty_kind=cls,
                              **common),
                         _row("order_null_first_third_share", null["statistic"], "dyn",
                              **common),
                         _row("order_null_p", null["p_value"], "dyn", **common)]
                if world == "cylinder":
                    classes.append(cls)
                    gates.append(bool(self.aj.learning_gate(world, seed)))
        status, reason = h4_verdict(classes, gates, len(self.cfg.base["seeds"]["masters"]))
        code = {"SUPPORTED": 1.0, "REJECTED": 0.0}.get(status)
        rows.append(_row(f"H4_verdict_{status}", code, "H4", condition=self.cond,
                         status="ok" if code is not None else "inconclusive",
                         uncertainty_kind=reason or None))
        log.info("S6 dynamics %s: H4 %s %s", self.cond, status, reason)
        return rows

    # ---- layer sweep ----------------------------------------------------------------------
    def layers(self) -> list[MetricRow]:
        rule = self.cfg.base["f1_rule"]
        f1 = F1Decision(rule["min_positive_panels"], rule["envelope_quantile"])
        rows: list[MetricRow] = []
        for seed in self.cfg.base["seeds"]["masters"]:
            S: dict[str, dict[tuple, float]] = {}
            try:
                ids = {(w, ck): self.aj.acts(w, self.cond, seed, step) for w in WORLDS
                       for ck, step in (("init", 0), ("final", self.aj.final))}
            except KeyError as exc:
                log.warning("S6 layers: replicate %s missing (%s)", seed, exc)
                rows.append(_row("replicate_available", None, "layers", status="not_run",
                                 condition=self.cond, replicate=seed))
                continue
            for (world, ck), aid in ids.items():
                for p in self.aj.panels:
                    for res in LayerSweep().run(aid, p, self.store):
                        S.setdefault(res["hook"], {})[(world, ck, p)] = float(res["S_H1"])
                        rows.append(_row("S_H1", res["S_H1"], f"layer:{res['hook']}",
                                         world=world, condition=self.cond, replicate=seed,
                                         panel=p, status=str(res["status"]),
                                         checkpoint=0 if ck == "init" else self.aj.final))
            for hook, cells in S.items():
                D = f1.contrasts(cells)
                common = {"condition": self.cond, "replicate": seed}
                rows += [_row("median_D", float(np.median(D)), f"layer:{hook}", **common),
                         _row("n_positive", float((D > 0).sum()), f"layer:{hook}", **common),
                         _row("u", f1.noise_envelope(cells), f"layer:{hook}", **common)]
        return rows


@register_stage
class S6Stage(Stage):
    """S6: dynamics + H4 (D-034), checkpoint-order null, layer sweep; O, and P after S5."""

    stage_id = "S6"
    requires = ("S4",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        conds = ["O"] + (["P"] if analysis_rows(store, "S5") else [])
        kinds = ["dynamics"] + (["layers"] if cfg.stage("S6").get("layer_sweep") else [])
        return [{"stage": "S6", "job": k, "condition": c} for c in conds for k in kinds]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        s6 = S6Job(job["condition"], cfg, store)
        rows = s6.dynamics() if job["job"] == "dynamics" else s6.layers()
        return [store.save(MetricRecords(rows=tuple(rows)),
                           config={"stage": "S6", "kind": job["job"],
                                   "condition": job["condition"]},
                           parents=sorted(s6.parents), seed_map={}, consumer=CONS)]
