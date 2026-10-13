"""Analysis job of S4/S5: F1 rule, Δgeom (H2), baselines R1–R3 (D-028), Gaussian floor, H0, G-F.

All computations go through the public APIs of ``analysis``, ``topology`` and ``prediction``;
results are stored as one MetricRecords plus GateReport G-F (stage-scoped). The MetricRecords
has every artifact it was computed from as a parent, so its id changes whenever its inputs do
(for example when a replicate that was missing is finished).
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any

import numpy as np
from scipy.spatial.distance import cdist

from topo_pilot.analysis import F1Decision, GeometryAlignment, PointSet, SpaceBuilder, ph_summary
from topo_pilot.contracts import (
    ActivationSet,
    EmissionSpec,
    GateCheck,
    GateReport,
    HistoryIndex,
    MetricRecords,
    MetricRow,
    ObservationSet,
    SeedTree,
    TransitionSpec,
)
from topo_pilot.prediction import PredictiveMetrics

from .s2 import child_of
from .s3 import TrainingRun, activation_ids, find_run_inputs, selected_sigma

log = logging.getLogger(__name__)
CONS = "experiment"
WORLDS = ("cylinder", "square")
BASELINES = ("R1", "R2", "R3")


def _row(metric: str, value: float | None, space: str = "analysis", **kw: Any) -> MetricRow:
    """A MetricRow; a non-finite value is stored as None with status ``inconclusive``."""
    status = kw.pop("status", "ok")
    if value is not None and not np.isfinite(value):
        value = None
    if value is None and status == "ok":
        status = "inconclusive"
    return MetricRow(run_id=kw.pop("run_id", "analysis"), space=space, metric_id=metric,
                     value=None if value is None else float(value), status=status, **kw)


def _S(ps: PointSet) -> tuple[float, str]:
    res = ph_summary(ps)
    return float(res["S_H1"]), str(res["status"])


def _hellinger(X: np.ndarray) -> np.ndarray:
    return cdist(np.sqrt(X), np.sqrt(X)) / np.sqrt(2.0)


class AnalysisJob:
    """The S4 (condition O) or S5 (condition P) analysis over the stored runs."""

    def __init__(self, stage_id: str, cfg, store):
        base = cfg.base
        self.stage_id, self.cfg, self.store = stage_id, cfg, store
        self.cond = "O" if stage_id == "S4" else "P"
        self.hook = base["model"]["primary_hook"]
        self.final = int(base["training"]["primary_checkpoint"])
        self.panels = list(range(1, base["data"]["n_panels"] + 1))
        self.floor_draws = int(base["topology"]["gaussian_floor_draws"])
        self.sb = SpaceBuilder(store)
        self.sigma = selected_sigma(store)
        self.train_config = dataclasses.asdict(TrainingRun(cfg, store).train_cfg)
        self.parents: set[str] = set()
        self._inputs: dict[tuple, dict[str, str]] = {}

    # ---- lookups --------------------------------------------------------------------------
    def inputs(self, world: str, cond: str, seed: int) -> dict[str, str]:
        key = (world, cond, seed)
        if key not in self._inputs:
            sigma = self.sigma if cond in ("O", "P") else None
            self._inputs[key] = find_run_inputs(self.store, self.cfg, world, cond, sigma, seed)
        return self._inputs[key]

    def acts(self, world: str, cond: str, seed: int, step: int) -> str:
        """All-panel ActivationSet id of a run; ``KeyError`` if the run is not done."""
        job = {"world": world, "condition": cond, "seed": seed}
        ids = activation_ids(self.store, job, (step,), train_config=self.train_config)
        if step not in ids:
            raise KeyError(f"no all-panel activations for {job} step {step}")
        self.parents.add(ids[step])
        return ids[step]

    def learning_gate(self, world: str, seed: int) -> bool | None:
        for mid in self.store.find(MetricRecords, stage=self.stage_id, kind="run"):
            for r in self.store.load(MetricRecords, mid, consumer=CONS).rows:
                if (r.metric_id == "learning_gate_passed" and r.world == world
                        and r.condition == self.cond and r.replicate == seed):
                    self.parents.add(mid)
                    return bool(r.value)
        return None

    # ---- F1 and baselines -----------------------------------------------------------------
    def replicate_S(self, seed: int):
        """S of the model (init, final) and of R1–R3 on every panel of both worlds.

        Returns ``(S, base_S, rows, statuses)``; nothing is recorded unless the whole
        replicate is available (``KeyError`` otherwise).
        """
        S, base_S, rows, statuses = {}, {}, [], []
        for world in WORLDS:
            ids = {"init": self.acts(world, self.cond, seed, 0),
                   "final": self.acts(world, self.cond, seed, self.final)}
            inputs = self.inputs(world, self.cond, seed)
            refs = {"activation_set_id": ids["final"], "emission_id": inputs["emission"],
                    "transition_id": child_of(self.store, TransitionSpec, inputs["world"]),
                    "obs_test_id": inputs["obs_test"],
                    "history_index_id": inputs["history_index"],
                    "k": self.cfg.base["baselines"]["spectral_components"]}
            for p in self.panels:
                for ckpt, aid in ids.items():
                    S[(world, ckpt, p)], st = _S(self.sb.activations(aid, self.hook, p))
                    statuses.append(st)
                    rows.append(_row("S_H1", S[(world, ckpt, p)], f"act:{self.hook}",
                                     world=world, condition=self.cond, replicate=seed, panel=p,
                                     status=st, checkpoint=0 if ckpt == "init" else self.final,
                                     parent_ids=(aid,)))
                for kind in BASELINES:
                    base_S[(kind, world, p)], st = _S(self.sb.baseline(kind, p, **refs))
                    rows.append(_row("S_H1", base_S[(kind, world, p)], f"base:{kind}",
                                     world=world, condition=self.cond, replicate=seed, panel=p,
                                     status=st))
        return S, base_S, rows, statuses

    def baseline_rows(self, seed: int, f1: F1Decision, S: dict, base_S: dict,
                      D: np.ndarray) -> list[MetricRow]:
        """D-028: the F1 contrast with each baseline in place of the final checkpoint, and the
        ratio median D_R / median D_model (descriptive; None when median D_model = 0)."""
        rows, med_model = [], float(np.median(D))
        for kind in BASELINES:
            S_R = {(w, c, p): (base_S[(kind, w, p)] if c == "final" else S[(w, "init", p)])
                   for w in WORLDS for c in ("init", "final") for p in self.panels}
            D_R = f1.contrasts(S_R)
            med = float(np.median(D_R))
            space = f"F1:base:{kind}"
            rows += [_row("median_D", med, space, condition=self.cond, replicate=seed),
                     _row("n_positive", float((D_R > 0).sum()), space, condition=self.cond,
                          replicate=seed),
                     _row("median_D_ratio_to_model", med / med_model if med_model else None,
                          space, condition=self.cond, replicate=seed)]
        return rows

    # ---- H2, floor, H0 --------------------------------------------------------------------
    def delta_geom(self, seed: int) -> tuple[list[MetricRow], list[float]]:
        rows, values = [], []
        for world in WORLDS:
            inputs = self.inputs(world, self.cond, seed)
            aid = self.acts(world, self.cond, seed, self.final)
            last = self._history_tokens(inputs, offset=-1)
            for p in self.panels:
                act = self.sb.activations(aid, self.hook, p)
                b32 = self.sb.beliefs(inputs["oracle"], "b32", p)
                b1 = self.sb.beliefs(inputs["oracle"], "b1", p)
                res = GeometryAlignment().delta_geom(
                    cdist(act.X, act.X), _hellinger(b32.X), _hellinger(b1.X),
                    np.array([last[h] for h in act.ids]))
                if np.isfinite(res["all"]):
                    values.append(float(res["all"]))
                common = {"world": world, "condition": self.cond, "replicate": seed, "panel": p}
                rows += [_row("delta_geom_all", res["all"], "geometry", **common),
                         _row("delta_geom_same_last_symbol", res["same_last_symbol"], "geometry",
                              status="ok" if res["status_same"] == "ok" else "inconclusive",
                              **common)]
        return rows, values

    def _history_tokens(self, inputs: dict[str, str], offset: int) -> dict[str, int]:
        """Token at ``end + offset`` per history: ``-1`` is w_32, ``0`` the target w_33."""
        idx = self.store.load(HistoryIndex, inputs["history_index"], consumer=CONS)
        obs = self.store.load(ObservationSet, inputs["obs_test"], consumer=CONS)
        row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
        return {h: int(obs.tokens[row[int(s)], e + offset])
                for h, s, e in zip(idx.history_id.tolist(), idx.sequence_id.tolist(),
                                   idx.end.tolist())}

    def floor(self, seed: int) -> list[MetricRow]:
        tree, rows = SeedTree(0), []
        for world in WORLDS:
            act = self.sb.activations(self.acts(world, self.cond, seed, self.final), self.hook, 1)
            for kind in ("iso", "cov"):
                vals = [ph_summary(self.sb.null(act, kind, tree.generator(
                            "floor_s4", world, self.cond, seed, kind, i)))["S_H1"]
                        for i in range(self.floor_draws)]
                common = {"world": world, "condition": self.cond, "replicate": seed, "panel": 1}
                rows += [_row("S_H1_mean", np.mean(vals), f"null:{kind}:act", **common),
                         _row("S_H1_q95", np.percentile(vals, 95), f"null:{kind}:act", **common)]
        return rows

    def h0_check(self) -> tuple[GateCheck | None, list[MetricRow]]:
        """D-029: the N model's test NLL at p = 32 is not below H(W) beyond the bootstrap CI."""
        seed = self.cfg.base["seeds"]["masters"][0]
        try:
            aid = self.acts("any", "N", seed, self.final)
        except KeyError:
            return None, []
        inputs = find_run_inputs(self.store, self.cfg, "cylinder", "N", None, seed)
        acts = self.store.load(ActivationSet, aid, consumer=CONS)
        target_of = self._history_tokens(inputs, offset=0)
        targets = np.array([target_of[h] for h in acts.history_id.tolist()])
        logits = acts.logits.astype(np.float64)
        p = np.exp(logits - logits.max(1, keepdims=True))
        p /= p.sum(1, keepdims=True)
        nll = PredictiveMetrics.nll(p, targets)
        H_W = float(self.store.load(EmissionSpec, inputs["emission"],
                                    consumer=CONS).diagnostics["H_W"])
        lo, hi = PredictiveMetrics.bootstrap_ci(nll, np.arange(len(nll)), 1000,
                                                SeedTree(0).generator("h0_bootstrap"))
        half = (hi - lo) / 2.0
        ok = float(nll.mean()) >= H_W - half
        rows = [_row("nll_p32", nll.mean(), "H0", condition="N", replicate=seed),
                _row("H_W", H_W, "H0", condition="N"), _row("ci_half_width", half, "H0")]
        return GateCheck("H0_N_model_nll_not_below_H_W", bool(ok), round(float(nll.mean()), 5),
                         round(H_W - half, 5)), rows

    # ---- driver ---------------------------------------------------------------------------
    def replicate(self, seed: int, f1: F1Decision):
        """Rows, ``(D, u)``, learning-gate flag and PH statuses of one complete replicate."""
        S, base_S, rows, statuses = self.replicate_S(seed)
        D, u = f1.contrasts(S), f1.noise_envelope(S)
        gate = all(self.learning_gate(w, seed) for w in WORLDS)
        rows += [_row("D", float(d), "F1", condition=self.cond, replicate=seed, panel=p)
                 for p, d in zip(self.panels, D)]
        rows += [_row("u", u, "F1", condition=self.cond, replicate=seed),
                 _row("median_D", float(np.median(D)), "F1", condition=self.cond,
                      replicate=seed)]
        rows += self.baseline_rows(seed, f1, S, base_S, D)
        dg_rows, dg = self.delta_geom(seed)
        rows += dg_rows
        rows.append(_row("delta_geom_all_fraction_positive",
                         float(np.mean(np.array(dg) > 0)) if dg else None, "geometry",
                         condition=self.cond, replicate=seed))
        rows += self.floor(seed)
        return rows, (D, u), gate, statuses

    def run(self) -> list[str]:
        rule = self.cfg.base["f1_rule"]
        f1 = F1Decision(rule["min_positive_panels"], rule["envelope_quantile"])
        rows: list[MetricRow] = []
        per_rep, gates, statuses = [], [], []
        for seed in self.cfg.base["seeds"]["masters"]:
            try:
                rep_rows, dU, gate, rep_statuses = self.replicate(seed, f1)
            except KeyError as exc:  # a run not done (time cut): reported, never invented
                log.warning("%s analysis: replicate %s missing (%s)", self.stage_id, seed, exc)
                rows.append(_row("replicate_available", None, status="not_run", replicate=seed))
                continue
            rows += rep_rows
            per_rep.append(dU)
            gates.append(gate)
            statuses += rep_statuses
        verdict = f1.verdict(per_rep, gates, statuses)
        code = {"SUPPORTED": 1.0, "REJECTED": 0.0}.get(verdict.status)
        rows.append(_row(f"F1_verdict_{verdict.status}", code, "F1", condition=self.cond,
                         status="ok" if code is not None else "inconclusive",
                         uncertainty_kind="; ".join(verdict.reasons) or None))
        h0, h0_rows = self.h0_check() if self.cond == "O" else (None, [])
        rows += h0_rows
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": self.stage_id, "kind": "analysis",
                                      "condition": self.cond},
                              parents=sorted(self.parents), seed_map={}, consumer=CONS)
        checks = [GateCheck(f"learning_gate_replicate_{i}", bool(g), bool(g), True)
                  for i, g in enumerate(gates)] or [GateCheck("any_replicate_trained", False)]
        if self.cond == "O":
            checks.append(h0 or GateCheck("H0_N_model_available", False, None, "N run"))
        report = GateReport(stage=self.stage_id, gate_id="G-F",
                            verdict="pass" if all(c.passed for c in checks) else "fail",
                            checks=tuple(checks))
        gid = self.store.save(report, config={"stage": self.stage_id, "gate": "G-F",
                                              "config_hash": self.cfg.config_hash},
                              parents=[mid], seed_map={}, consumer=CONS)
        log.info("%s analysis: F1 %s (%s)", self.stage_id, verdict.status,
                 "; ".join(verdict.reasons))
        return [mid, gid]


def run_analysis(stage_id: str, cfg, store) -> list[str]:
    """Run the full analysis of ``stage_id`` (S4: condition O; S5: condition P)."""
    return AnalysisJob(stage_id, cfg, store).run()
