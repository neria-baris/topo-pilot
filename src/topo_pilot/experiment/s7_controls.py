"""S7 controls (D-047): H0 rows of the extra N runs, and the descriptive ``controls`` job.

``controls`` writes one MetricRecords (``kind = controls``) with, for each U and N run of S7
(and, for comparison, the S4 N run): S of the primary hook on all 8 panels at checkpoints 0 and
final, the per-run median, and for the U pair the cylinder–square contrast D on the 8 panels
(one replicate, so no F1 rule: descriptive only). Missing runs are ``not_run`` rows.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Mapping

import numpy as np

from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    EmissionSpec,
    MetricRecords,
    MetricRow,
    SeedTree,
)
from topo_pilot.prediction import PredictiveMetrics

from .config import ResolvedConfig
from .s3 import TrainingRun, activation_ids
from .s4_analysis import _S, AnalysisJob, _row

log = logging.getLogger(__name__)
CONS = "experiment"


def _softmax(logits: np.ndarray) -> np.ndarray:
    z = logits.astype(np.float64)
    p = np.exp(z - z.max(axis=1, keepdims=True))
    return p / p.sum(axis=1, keepdims=True)


def h0_rows(cfg: ResolvedConfig, store: ArtifactStore, inputs: Mapping[str, str], act_id: str,
            seed: int) -> list[MetricRow]:
    """D-029 for one N run: test NLL at p = 32 must not be below H(W) by more than the 95%
    bootstrap half-width (resampling trajectories; stream ``h0_bootstrap`` scoped by seed)."""
    aj = AnalysisJob("S4", cfg, store)
    acts = store.load(ActivationSet, act_id, consumer=CONS)
    target_of = aj._history_tokens(inputs, offset=0)
    targets = np.array([target_of[h] for h in acts.history_id.tolist()])
    nll = PredictiveMetrics.nll(_softmax(acts.logits), targets)
    H_W = float(store.load(EmissionSpec, inputs["emission"], consumer=CONS).diagnostics["H_W"])
    lo, hi = PredictiveMetrics.bootstrap_ci(nll, np.arange(len(nll)), 1000,
                                            SeedTree(0).generator("h0_bootstrap", seed))
    half = (hi - lo) / 2.0
    common = {"run_id": f"any-N-{seed}", "condition": "N", "replicate": seed}
    return [_row("nll_p32", float(nll.mean()), "H0", **common),
            _row("H_W", H_W, "H0", **common),
            _row("ci_half_width", half, "H0", **common),
            _row("h0_passed", float(nll.mean() >= H_W - half), "H0", **common)]


class ControlsJob:
    """Descriptive PH of the U and N control models (no rule; RESEARCH_PLAN §3.3 note on U)."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        base = cfg.base
        self.hook = base["model"]["primary_hook"]
        self.final = int(base["training"]["primary_checkpoint"])
        self.panels = list(range(1, base["data"]["n_panels"] + 1))
        self.parents: set[str] = set()
        self.aj = AnalysisJob("S4", cfg, store)

    def runs(self) -> list[dict]:
        s4_n = [dict(r) for r in self.cfg.stage("S4")["runs_ordered"] if r["condition"] == "N"]
        return s4_n + [dict(r) for r in self.cfg.stage("S7")["runs_ordered"]]

    def acts(self, job: Mapping, step: int) -> str | None:
        """All-panel ActivationSet of a control run at ``step`` (None if not trained)."""
        train = TrainingRun(self.cfg, self.store).train_cfg  # training settings do not depend on V
        ids = activation_ids(self.store, job, (step,), train_config=dataclasses.asdict(train))
        return ids.get(step)

    def run_rows(self, job: Mapping) -> tuple[list[MetricRow], dict[tuple[str, int], float]]:
        rows, S = [], {}
        common = {"world": job["world"], "condition": job["condition"],
                  "replicate": int(job["seed"])}
        for ckpt, step in (("init", 0), ("final", self.final)):
            aid = self.acts(job, step)
            if aid is None:
                rows.append(_row("run_available", None, "controls", status="not_run",
                                 checkpoint=step, **common))
                continue
            self.parents.add(aid)
            vals = []
            for p in self.panels:
                S[(ckpt, p)], st = _S(self.aj.sb.activations(aid, self.hook, p))
                vals.append(S[(ckpt, p)])
                rows.append(_row("S_H1", S[(ckpt, p)], f"controls:act:{self.hook}", status=st,
                                 checkpoint=step, panel=p, parent_ids=(aid,), **common))
            rows.append(_row("S_H1_median", float(np.median(vals)), f"controls:act:{self.hook}",
                             checkpoint=step, **common))
        return rows, S

    def run(self) -> list[str]:
        rows: list[MetricRow] = []
        per_run = {}
        for job in self.runs():
            run_rows, S = self.run_rows(job)
            rows += run_rows
            per_run[(job["world"], job["condition"])] = S
        cyl, sq = per_run.get(("cylinder", "U"), {}), per_run.get(("square", "U"), {})
        for p in self.panels:
            keys = [("final", p), ("init", p)]
            if all(k in cyl and k in sq for k in keys):
                D = (cyl[("final", p)] - cyl[("init", p)]) - (sq[("final", p)] - sq[("init", p)])
                rows.append(_row("D", D, "controls:U", condition="U", panel=p,
                                 uncertainty_kind="descriptive (one replicate)"))
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": "S7", "kind": "controls"},
                              parents=sorted(self.parents), seed_map={}, consumer=CONS)
        log.info("S7 controls: %d rows", len(rows))
        return [mid]
