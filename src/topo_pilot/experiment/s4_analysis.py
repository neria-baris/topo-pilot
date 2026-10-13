"""Analysis job of S4/S5: F1 rule, Δgeom (H2), baselines R1–R3 (D-028), Gaussian floor, H0, G-F.

All computations go through the public APIs of ``analysis``, ``topology`` and ``prediction``;
results are stored as one MetricRecords plus GateReport G-F (stage-scoped).
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from scipy.spatial.distance import cdist

from topo_pilot.analysis import F1Decision, GeometryAlignment, PointSet, SpaceBuilder, ph_summary
from topo_pilot.contracts import (
    EmissionSpec,
    GateCheck,
    GateReport,
    HistoryIndex,
    MetricRecords,
    MetricRow,
    ObservationSet,
    SeedTree,
)
from topo_pilot.prediction import PredictiveMetrics

from .s3 import _selected_sigma, find_run_inputs

log = logging.getLogger(__name__)
CONS = "experiment"
FLOOR_DRAWS = 20


def _row(metric: str, value: float | None, space: str = "analysis", **kw: Any) -> MetricRow:
    status = kw.pop("status", "ok" if value is not None else "inconclusive")
    return MetricRow(run_id=kw.pop("run_id", "analysis"), space=space, metric_id=metric,
                     value=None if value is None else float(value), status=status, **kw)


def _acts(store, world: str, cond: str, seed: int, step: int) -> str:
    from .s4 import activation_ids
    job = {"world": world, "condition": cond, "seed": seed}
    ids = activation_ids(store, job, (step,))
    if step not in ids:
        raise KeyError(f"no all-panel activations for {job} step {step}")
    return ids[step]


def _learning_gate(store, stage_id: str, world: str, cond: str, seed: int) -> bool | None:
    for mid in store.find(MetricRecords, stage=stage_id, kind="run"):
        for r in store.load(MetricRecords, mid, consumer=CONS).rows:
            if (r.metric_id == "learning_gate_passed" and r.world == world
                    and r.condition == cond and r.replicate == seed):
                return bool(r.value)
    return None


def _S(ps: PointSet) -> tuple[float, str]:
    res = ph_summary(ps)
    return float(res["S_H1"]), str(res["status"])


def _f1_for_replicate(store, sb, cfg, cond, seed, panels, hook, rows, statuses):
    S, base_S = {}, {}
    final = cfg.base["training"]["primary_checkpoint"]
    for world in ("cylinder", "square"):
        ids = {"init": _acts(store, world, cond, seed, 0),
               "final": _acts(store, world, cond, seed, final)}
        inputs = find_run_inputs(store, world, cond, _selected_sigma(store), seed)
        for p in panels:
            for ckpt, aid in ids.items():
                S[(world, ckpt, p)], st = _S(sb.activations(aid, hook, p))
                statuses.append(st)
                rows.append(_row("S_H1", S[(world, ckpt, p)], f"act:{hook}", world=world,
                                 condition=cond, replicate=seed, panel=p, status=st,
                                 checkpoint=0 if ckpt == "init" else final, parent_ids=(aid,)))
            refs = {"activation_set_id": ids["final"], "emission_id": inputs["emission"],
                    "transition_id": _transition(store, inputs["emission"]),
                    "obs_test_id": inputs["obs_test"],
                    "history_index_id": inputs["history_index"],
                    "k": cfg.base["baselines"]["spectral_components"]}
            for kind in ("R1", "R2", "R3"):
                base_S[(kind, world, p)], st = _S(sb.baseline(kind, p, **refs))
                rows.append(_row("S_H1", base_S[(kind, world, p)], f"base:{kind}", world=world,
                                 condition=cond, replicate=seed, panel=p, status=st))
    return S, base_S


def _transition(store, emission_id: str) -> str:
    from topo_pilot.contracts import TransitionSpec
    world = store.meta(emission_id).parent_ids[0]
    (tid,) = [t for t in store.find(TransitionSpec) if world in store.meta(t).parent_ids]
    return tid


def _delta_geom(store, sb, cfg, cond, seed, panels, hook, rows) -> list[float]:
    final = cfg.base["training"]["primary_checkpoint"]
    out = []
    for world in ("cylinder", "square"):
        inputs = find_run_inputs(store, world, cond, _selected_sigma(store), seed)
        aid = _acts(store, world, cond, seed, final)
        last = _last_symbols(store, inputs)
        for p in panels:
            act = sb.activations(aid, hook, p)
            b32 = sb.beliefs(inputs["oracle"], "b32", p)
            b1 = sb.beliefs(inputs["oracle"], "b1", p)
            D_A = cdist(act.X, act.X)
            D_32 = cdist(np.sqrt(b32.X), np.sqrt(b32.X)) / np.sqrt(2.0)
            D_1 = cdist(np.sqrt(b1.X), np.sqrt(b1.X)) / np.sqrt(2.0)
            res = GeometryAlignment().delta_geom(D_A, D_32, D_1,
                                                 np.array([last[h] for h in act.ids]))
            out.append(res["all"])
            rows += [_row("delta_geom_all", res["all"], "geometry", world=world, condition=cond,
                          replicate=seed, panel=p),
                     _row("delta_geom_same_last_symbol", res["same_last_symbol"], "geometry",
                          world=world, condition=cond, replicate=seed, panel=p,
                          status="ok" if res["status_same"] == "ok" else "inconclusive")]
    return out


def _last_symbols(store, inputs) -> dict[str, int]:
    idx = store.load(HistoryIndex, inputs["history_index"], consumer=CONS)
    obs = store.load(ObservationSet, inputs["obs_test"], consumer=CONS)
    row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    return {h: int(obs.tokens[row[int(s)], e - 1])
            for h, s, e in zip(idx.history_id.tolist(), idx.sequence_id.tolist(),
                               idx.end.tolist())}


def _floor(store, sb, cfg, cond, seed, hook, rows) -> None:
    final = cfg.base["training"]["primary_checkpoint"]
    tree = SeedTree(0)
    for world in ("cylinder", "square"):
        act = sb.activations(_acts(store, world, cond, seed, final), hook, 1)
        for kind in ("iso", "cov"):
            vals = [ph_summary(sb.null(act, kind, tree.generator("floor_s4", world, cond, seed,
                                                                 kind, i)))["S_H1"]
                    for i in range(FLOOR_DRAWS)]
            rows += [_row("S_H1_mean", np.mean(vals), f"null:{kind}:act", world=world,
                          condition=cond, replicate=seed, panel=1),
                     _row("S_H1_q95", np.percentile(vals, 95), f"null:{kind}:act", world=world,
                          condition=cond, replicate=seed, panel=1)]


def _h0_check(store, cfg, rows) -> GateCheck | None:
    """D-029: the N model's test NLL at p = 32 is not below H(W) beyond the bootstrap CI."""
    seed = cfg.base["seeds"]["masters"][0]
    try:
        aid = _acts(store, "any", "N", seed, cfg.base["training"]["primary_checkpoint"])
    except (KeyError, ValueError):
        return None
    from topo_pilot.contracts import ActivationSet
    inputs = find_run_inputs(store, "cylinder", "N", None, seed)
    acts = store.load(ActivationSet, aid, consumer=CONS)
    targets = np.array([_targets(store, inputs)[h] for h in acts.history_id.tolist()])
    logits = acts.logits.astype(np.float64)
    p = np.exp(logits - logits.max(1, keepdims=True))
    p /= p.sum(1, keepdims=True)
    nll = PredictiveMetrics.nll(p, targets)
    H_W = float(store.load(EmissionSpec, inputs["emission"], consumer=CONS).diagnostics["H_W"])
    lo, hi = PredictiveMetrics.bootstrap_ci(nll, np.arange(len(nll)), 1000,
                                            SeedTree(0).generator("h0_bootstrap"))
    half = (hi - lo) / 2.0
    ok = float(nll.mean()) >= H_W - half
    rows += [_row("nll_p32", nll.mean(), "H0", condition="N", replicate=seed),
             _row("H_W", H_W, "H0", condition="N"), _row("ci_half_width", half, "H0")]
    return GateCheck("H0_N_model_nll_not_below_H_W", bool(ok), round(float(nll.mean()), 5),
                     round(H_W - half, 5))


def _targets(store, inputs) -> dict[str, int]:
    idx = store.load(HistoryIndex, inputs["history_index"], consumer=CONS)
    obs = store.load(ObservationSet, inputs["obs_test"], consumer=CONS)
    row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    return {h: int(obs.tokens[row[int(s)], e])
            for h, s, e in zip(idx.history_id.tolist(), idx.sequence_id.tolist(),
                               idx.end.tolist())}


def run_analysis(stage_id: str, cfg, store) -> list[str]:
    """Run the full analysis of ``stage_id`` (S4: condition O; S5: condition P)."""
    cond = "O" if stage_id == "S4" else "P"
    hook = cfg.base["model"]["primary_hook"]
    panels = list(range(1, cfg.base["data"]["n_panels"] + 1))
    sb = SpaceBuilder(store)
    rule = cfg.base["f1_rule"]
    f1 = F1Decision(rule["min_positive_panels"], rule["envelope_quantile"])
    rows: list[MetricRow] = []
    per_rep, gates, statuses = [], [], []
    for seed in cfg.base["seeds"]["masters"]:
        try:
            S, base_S = _f1_for_replicate(store, sb, cfg, cond, seed, panels, hook, rows, statuses)
        except KeyError as exc:  # a run not done (time cut): reported, never invented
            log.warning("%s analysis: replicate %s missing (%s)", stage_id, seed, exc)
            rows.append(_row("replicate_available", None, status="not_run", replicate=seed))
            continue
        D, u = f1.contrasts(S), f1.noise_envelope(S)
        per_rep.append((D, u))
        gates.append(all(_learning_gate(store, stage_id, w, cond, seed)
                         for w in ("cylinder", "square")))
        rows += [_row("D", float(d), "F1", condition=cond, replicate=seed, panel=p)
                 for p, d in zip(panels, D)]
        rows += [_row("u", u, "F1", condition=cond, replicate=seed),
                 _row("median_D", float(np.median(D)), "F1", condition=cond, replicate=seed)]
        for kind in ("R1", "R2", "R3"):
            S_R = {(w, c, p): (base_S[(kind, w, p)] if c == "final" else S[(w, "init", p)])
                   for w in ("cylinder", "square") for c in ("init", "final") for p in panels}
            D_R = f1.contrasts(S_R)
            rows += [_row("median_D", float(np.median(D_R)), f"F1:base:{kind}", condition=cond,
                          replicate=seed),
                     _row("n_positive", float((D_R > 0).sum()), f"F1:base:{kind}",
                          condition=cond, replicate=seed)]
        dg = _delta_geom(store, sb, cfg, cond, seed, panels, hook, rows)
        rows.append(_row("delta_geom_all_fraction_positive", float(np.mean(np.array(dg) > 0)),
                         "geometry", condition=cond, replicate=seed))
        _floor(store, sb, cfg, cond, seed, hook, rows)
    verdict = f1.verdict(per_rep, gates, statuses)
    code = {"SUPPORTED": 1.0, "REJECTED": 0.0}.get(verdict.status)
    rows.append(_row(f"F1_verdict_{verdict.status}", code, "F1", condition=cond,
                     status="ok" if code is not None else "inconclusive",
                     uncertainty_kind="; ".join(verdict.reasons) or None))
    h0 = _h0_check(store, cfg, rows) if cond == "O" else None
    mid = store.save(MetricRecords(rows=tuple(rows)),
                     config={"stage": stage_id, "kind": "analysis", "condition": cond},
                     parents=[], seed_map={}, consumer=CONS)
    checks = [GateCheck(f"learning_gate_replicate_{i}", bool(g), bool(g), True)
              for i, g in enumerate(gates)] or [GateCheck("any_replicate_trained", False)]
    if cond == "O":
        checks.append(h0 or GateCheck("H0_N_model_available", False, None, "N run"))
    report = GateReport(stage=stage_id, gate_id="G-F",
                        verdict="pass" if all(c.passed for c in checks) else "fail",
                        checks=tuple(checks))
    gid = store.save(report, config={"stage": stage_id, "gate": "G-F",
                                     "config_hash": cfg.config_hash},
                     parents=[mid], seed_map={}, consumer=CONS)
    log.info("%s analysis: F1 %s (%s)", stage_id, verdict.status, "; ".join(verdict.reasons))
    return [mid, gid]
