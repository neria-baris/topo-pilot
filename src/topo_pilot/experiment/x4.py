"""Stage X4: representation geometry vs readout geometry (PREREGISTRATION_X4.md, D-039).

Re-analysis of stored runs only (no training, no extraction, no gate). Per run, checkpoint
(0, final) and panel, six views of the same histories are built:

- V0 resid_post_3 (raw), V1 = ``ln_gauge_free(V0)``, V2 ln_final_out;
- V3 / V4 = readout-visible / readout-null part of V1 (``readout_projector`` of the same
  checkpoint's final-LN gamma and W_U);
- V5 = softmax(logits) under Hellinger.

Then: S per view, the F1 rule per view, Δgeom per view, the X4-b positive control, X4-a, X4-c,
X4-d (same-w32 H2 baseline) and H3′. One MetricRecords is written (stage ``X4``); its parents
are every input artifact, so identical inputs give the identical id (D-032). Only counts are
logged, never values.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import spearmanr

from topo_pilot.analysis import (
    F1Decision,
    GeometryAlignment,
    PointSet,
    ln_gauge_free,
    ph_summary,
    predictive_pointset,
    readout_projector,
    split_readout,
)
from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow

from .config import ResolvedConfig
from .s4_analysis import _hellinger, _row
from .stages import Stage, register_stage
from .x4_inputs import StoreResolver, X4Panel, X4Run

__all__ = ["X4Job", "X4Panel", "X4Run", "X4Stage", "run_rule_verdict", "x4c_category"]

log = logging.getLogger(__name__)
CONS = "experiment"
VIEWS = ("V0", "V1", "V2", "V3", "V4", "V5")
WORLDS = ("cylinder", "square")
MIN_SAME_PAIRS = 200  # analysis SPEC: fewer same-w32 pairs is inconclusive
CODE = {"SUPPORTED": 1.0, "REJECTED": 0.0}
Resolver = Callable[[str], tuple[list[X4Run], list[tuple[str, str, int]]]]


def x4c_category(v3_status: str, v4_status: str) -> str:
    """X4-c category: a view counts iff its F1-rule status is ``SUPPORTED``."""
    v3, v4 = v3_status == "SUPPORTED", v4_status == "SUPPORTED"
    return {(True, False): "V3_only", (False, True): "V4_only",
            (True, True): "both"}.get((v3, v4), "neither")


def run_rule_verdict(n_pass: Mapping[tuple[str, int], int],
                     gates: Mapping[tuple[str, int], bool | None],
                     min_panels: int, n_replicates: int) -> tuple[str, str]:
    """D-039 rule over runs ``(world, seed)``: INCONCLUSIVE if a learning gate is not True or
    fewer than ``n_replicates`` seeds have both worlds; else SUPPORTED iff every run has
    ``n_pass >= min_panels``, else REJECTED. Returns ``(status, reason)``."""
    reasons = [f"learning gate not passed: {w}-{s}" for (w, s), g in sorted(gates.items())
               if g is not True]
    complete = {s for (_, s) in n_pass if all((w, s) in n_pass for w in WORLDS)}
    if len(complete) < n_replicates:
        reasons.append(f"complete replicates: {len(complete)} < {n_replicates}")
    if reasons:
        return "INCONCLUSIVE", "; ".join(reasons)
    low = [f"{w}-{s}: {n}" for (w, s), n in sorted(n_pass.items()) if n < min_panels]
    return ("REJECTED", "runs below the panel minimum: " + ", ".join(low)) if low else (
        "SUPPORTED", "")


def _rho(a: np.ndarray, b: np.ndarray) -> float | None:
    """Spearman correlation; None when undefined (fewer than 3 pairs or a constant input)."""
    if a.size < 3 or np.ptp(a) == 0.0 or np.ptp(b) == 0.0:
        return None
    value = float(spearmanr(a, b)[0])
    return value if np.isfinite(value) else None


def _dist(X: np.ndarray, view: str) -> np.ndarray:
    return _hellinger(X) if view == "V5" else cdist(X, X)


def _gt_all(x: float | None, *others: float | None) -> bool:
    return x is not None and all(o is not None and x > o for o in others)


class X4Job:
    """Builds the views, computes every X4 quantity and saves one MetricRecords."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore,
                 resolver: Resolver | None = None):
        self.cfg, self.store = cfg, store
        self.resolver = resolver or StoreResolver(cfg, store)
        self.settings = {k: v for k, v in dict(cfg.stage("X4")).items() if k != "requires"}
        self.sources = list(self.settings.get("sources", ["S4"]))
        self.views = [v for v in VIEWS if v in self.settings.get("views", VIEWS)]
        self.eps = float(self.settings.get("ln_eps", 1e-5))
        self.min_rho = float(self.settings.get("positive_control_min_rho", 0.9))
        self.reuse = bool(self.settings.get("reuse_stored_V0", True))
        self.final = int(cfg.base["training"]["primary_checkpoint"])
        self.seeds = [int(s) for s in cfg.base["seeds"]["masters"]]
        rule = cfg.base["f1_rule"]
        self.min_panels = int(rule["min_positive_panels"])
        self.f1 = F1Decision(self.min_panels, float(rule["envelope_quantile"]), len(self.seeds))

    def run(self) -> str:
        runs, missing = [], []
        for source in self.sources:
            found, miss = self.resolver(source)
            runs += found
            missing += miss
        rows = self.rows(runs, missing)
        parents = sorted({p for r in runs for p in r.parents})
        log.info("X4: %d runs, %d missing, %d rows", len(runs), len(missing), len(rows))
        return self.store.save(MetricRecords(rows=tuple(rows)),
                               config={"stage": "X4", "kind": "analysis",
                                       "sources": self.sources, "settings": self.settings},
                               parents=parents, seed_map={}, consumer=CONS)

    def rows(self, runs: Sequence[X4Run], missing: Sequence[tuple[str, str, int]]
             ) -> list[MetricRow]:
        out = [_row("run_available", None, "x4", run_id="X4", status="not_run", world=w,
                    condition=c, replicate=s) for w, c, s in missing]
        stats = {}
        for run in runs:
            run_rows, stats[(run.world, run.condition, run.seed)] = self._run(run)
            out += run_rows
        conds = list(dict.fromkeys(c for _, c, _ in [*stats, *missing] if c != "N"))
        gates = {(r.world, r.condition, r.seed): r.learning_gate for r in runs}
        for cond in conds:
            out += self._condition(cond, {(w, s): v for (w, c, s), v in stats.items()
                                          if c == cond and w in WORLDS},
                                   {(w, s): g for (w, c, s), g in gates.items() if c == cond})
        return out

    # ---- one run ------------------------------------------------------------------------------
    def _points(self, pan: X4Panel, weights, P: np.ndarray) -> tuple[dict, list[float]]:
        gamma, beta, W_U = weights
        U = ln_gauge_free(pan.Z, self.eps)
        vis, null = split_readout(U, P)
        pts = {"V0": pan.Z, "V1": U, "V2": pan.ln_out, "V3": vis, "V4": null,
               "V5": predictive_pointset(pan.logits, pan.ids).X}
        checks = [float(np.abs(gamma * U + beta - pan.ln_out).max()),
                  float(np.abs((gamma * U + beta) @ W_U.T - pan.logits).max()),
                  float(np.abs((gamma * vis + beta) @ W_U.T - pan.logits).max())]
        return pts, checks

    def _S(self, run: X4Run, view: str, step: int, p: int, X: np.ndarray, ids) -> tuple:
        if view == "V0" and self.reuse and (step, p) in run.stored_S_V0:
            return run.stored_S_V0[(step, p)]
        res = ph_summary(PointSet(f"x4:{view}", X, None, list(ids),
                                  "hellinger" if view == "V5" else "euclidean"))
        return float(res["S_H1"]), str(res["status"])

    def _run(self, run: X4Run) -> tuple[list[MetricRow], dict]:
        common = {"run_id": "X4", "world": run.world, "condition": run.condition,
                  "replicate": run.seed}
        rows: list[MetricRow] = []
        st: dict[str, dict] = {"S": {}, "b": {}, "d": {}, "h3": {}}
        oracle_D: dict[int, dict[str, np.ndarray]] = {}
        h3_init: dict[tuple[str, int], float | None] = {}
        for step in (0, self.final):
            P = readout_projector(run.weights[step][0], run.weights[step][2])
            worst = [0.0, 0.0, 0.0]
            for p in sorted(q for (s, q) in run.panels if s == step):
                pan = run.panels[(step, p)]
                pts, checks = self._points(pan, run.weights[step], P)
                worst = [max(a, b) for a, b in zip(worst, checks)]
                for v in self.views:
                    S, status = self._S(run, v, step, p, pts[v], pan.ids)
                    st["S"][(v, step, p)] = (S, status)
                    rows.append(_row("S_H1", S, f"x4:{v}", status=status, panel=p,
                                     checkpoint=step, **common))
                if run.oracle is None:
                    continue
                if p not in oracle_D:
                    oracle_D[p] = self._oracle_D(run.oracle[p])
                iu = np.triu_indices(len(pan.ids), k=1)
                D = {v: _dist(pts[v], v) for v in self.views
                     if step == self.final or v in ("V0", "V1")}
                if step == 0:
                    h3_init.update({(a, p): _rho(D[a][iu], oracle_D[p]["b32"][iu])
                                    for a in ("V0", "V1") if a in D})
                else:
                    rows += self._panel_final(run, p, D, oracle_D[p], h3_init, st, common)
            rows += [_row(m, val, "x4:check", checkpoint=step, **common) for m, val in
                     zip(("ln_reconstruction_max_abs", "logits_from_U_max_abs",
                          "logits_from_visible_max_abs"), worst)]
        rows += self._run_summaries(st, common)
        return rows, st

    def _oracle_D(self, o: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
        D = {k: _hellinger(o[k]) for k in ("b32", "b1", "q")}
        D.update({k: cdist(o[k], o[k]) for k in ("R2", "R3")})
        D["last_symbol"] = np.asarray(o["last_symbol"])
        return D

    def _panel_final(self, run: X4Run, p: int, D: dict, od: dict, h3_init: dict, st: dict,
                     common: dict) -> list[MetricRow]:
        rows, iu = [], np.triu_indices(od["b32"].shape[0], k=1)
        ls = od["last_symbol"]
        at_final = {**common, "checkpoint": self.final}
        for v, DA in D.items():
            res = GeometryAlignment().delta_geom(DA, od["b32"], od["b1"], ls)
            rows += [_row("delta_geom_all", res["all"], f"x4:{v}", panel=p, **at_final),
                     _row("delta_geom_same_last_symbol", res["same_last_symbol"], f"x4:{v}",
                          panel=p, status="ok" if res["status_same"] == "ok" else
                          "inconclusive", **at_final)]
        if "V5" in D:
            st["b"][p] = _rho(D["V5"][iu], od["q"][iu])
            rows.append(_row("rho_V5_future1", st["b"][p], "x4:b", panel=p, **at_final))
        same = (ls[:, None] == ls[None, :])[iu]
        ok = int(same.sum()) >= MIN_SAME_PAIRS
        d32, d32s = od["b32"][iu], od["b32"][iu][same]
        r_same = {k: _rho(od[k][iu][same], d32s) if ok else None for k in ("R2", "R3")}
        r_all = {k: _rho(od[k][iu], d32) for k in ("R2", "R3")}
        for a in ("V0", "V1"):
            if a not in D:
                continue
            m_same = _rho(D[a][iu][same], d32s) if ok else None
            passed = _gt_all(m_same, r_same["R2"], r_same["R3"])
            st["d"][(a, p)] = passed
            rows += [_row(m, val, f"x4:d:{a}", panel=p, **at_final) for m, val in
                     (("rho_same_model", m_same), ("rho_same_R2", r_same["R2"]),
                      ("rho_same_R3", r_same["R3"]), ("panel_pass", float(passed)))]
            final, init = _rho(D[a][iu], d32), h3_init.get((a, p))
            passed = _gt_all(final, init, r_all["R2"], r_all["R3"])
            st["h3"][(a, p)] = passed
            rows += [_row(m, val, f"x4:h3p:{a}", panel=p, **common) for m, val in
                     (("rho_all_final", final), ("rho_all_init", init),
                      ("rho_all_R2", r_all["R2"]), ("rho_all_R3", r_all["R3"]),
                      ("panel_pass", float(passed)))]
        return rows

    def _run_summaries(self, st: dict, common: dict) -> list[MetricRow]:
        rows = []
        if st["b"]:
            vals = [v for v in st["b"].values() if v is not None]
            st["b_median"] = float(np.median(vals)) if len(vals) == len(st["b"]) else None
            rows.append(_row("rho_V5_future1_median", st["b_median"], "x4:b", **common))
        for key, space in (("d", "x4:d"), ("h3", "x4:h3p")):
            for a in ("V0", "V1"):
                flags = [f for (b, _), f in st[key].items() if b == a]
                if flags:
                    st[f"n_{key}_{a}"] = int(sum(flags))
                    rows.append(_row("n_pass", float(sum(flags)), f"{space}:{a}", **common))
        return rows

    # ---- one condition ------------------------------------------------------------------------
    def _verdict_row(self, metric: str, status: str, space: str, cond: str,
                     reason: str = "") -> MetricRow:
        code = CODE.get(status)
        return _row(f"{metric}_{status}", code, space, run_id="X4", condition=cond,
                    status="ok" if code is not None else "inconclusive",
                    uncertainty_kind=reason or None)

    def _f1_view(self, view: str, cond: str, stats: dict, gates: dict
                 ) -> tuple[list[MetricRow], str, dict[int, float]]:
        rows, per_rep, rep_gates, statuses, medians = [], [], [], [], {}
        common = {"run_id": "X4", "condition": cond}
        for seed in self.seeds:
            if not all((w, seed) in stats for w in WORLDS):
                continue
            cells = {}
            for w in WORLDS:
                for (v, step, p), (S, status) in stats[(w, seed)]["S"].items():
                    if v == view:
                        cells[(w, "init" if step == 0 else "final", p)] = S
                        statuses.append(status)
            if not cells:
                continue
            D, u = self.f1.contrasts(cells), self.f1.noise_envelope(cells)
            panels = sorted({p for (_, _, p) in cells})
            rows += [_row("D", float(d), f"x4:{view}", replicate=seed, panel=p, **common)
                     for p, d in zip(panels, D)]
            medians[seed] = float(np.median(D))
            rows += [_row("median_D", medians[seed], f"x4:{view}", replicate=seed, **common),
                     _row("n_positive", float((D > 0).sum()), f"x4:{view}", replicate=seed,
                          **common),
                     _row("u", u, f"x4:{view}", replicate=seed, **common)]
            per_rep.append((D, u))
            rep_gates.append(all(gates.get((w, seed)) is True for w in WORLDS))
        verdict = self.f1.verdict(per_rep, rep_gates, statuses)
        rows.append(self._verdict_row("F1rule_verdict", verdict.status, f"x4:{view}", cond,
                                      "; ".join(verdict.reasons)))
        return rows, verdict.status, medians

    def _condition(self, cond: str, stats: dict, gates: dict) -> list[MetricRow]:
        rows: list[MetricRow] = []
        status, medians = {}, {}
        for v in self.views:
            v_rows, status[v], medians[v] = self._f1_view(v, cond, stats, gates)
            rows += v_rows
        common = {"run_id": "X4", "condition": cond}
        if "V5" in self.views:
            meds = [s.get("b_median") for s in stats.values()]
            passed = bool(meds) and all(m is not None and m >= self.min_rho for m in meds)
            rows.append(_row("positive_control_passed", float(passed), "x4:b", **common))
            rows.append(self._verdict_row("X4b_verdict", status["V5"] if passed else
                                          "INCONCLUSIVE", "x4:b", cond,
                                          "" if passed else "positive control failed"))
        if "V0" in status and "V1" in status:
            rows += [_row("X4a_verdicts_equal", float(status["V0"] == status["V1"]), "x4:a",
                          **common),
                     _row("X4a_caveat", float(status["V0"] == "SUPPORTED"
                                              and status["V1"] != "SUPPORTED"), "x4:a", **common)]
        if "V3" in status and "V4" in status:
            for seed in sorted(set(medians["V3"]) & set(medians["V4"])):
                m3, m4 = medians["V3"][seed], medians["V4"][seed]
                rows += [_row("median_D_V3", m3, "x4:c", replicate=seed, **common),
                         _row("median_D_V4", m4, "x4:c", replicate=seed, **common),
                         _row("ratio_V3_V4", m3 / m4 if m4 != 0 else None, "x4:c",
                              replicate=seed, **common)]
            rows.append(_row(f"X4c_{x4c_category(status['V3'], status['V4'])}", 1.0, "x4:c",
                             **common))
        for key, space, metric in (("d", "x4:d", "X4d_verdict"),
                                   ("h3", "x4:h3p", "H3prime_verdict")):
            for a in ("V0", "V1"):
                if a not in self.views:
                    continue
                n_pass = {k: s[f"n_{key}_{a}"] for k, s in stats.items()
                          if f"n_{key}_{a}" in s}
                verdict, reason = run_rule_verdict(n_pass, gates, self.min_panels,
                                                   len(self.seeds))
                rows.append(self._verdict_row(metric, verdict, f"{space}:{a}", cond, reason))
        return rows


@register_stage
class X4Stage(Stage):
    """X4: secondary readout-geometry analyses on the stored runs of ``X4.sources``."""

    stage_id = "X4"
    requires = ("S4",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "X4", "job": "analysis"}]

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        return [X4Job(cfg, store).run()]
