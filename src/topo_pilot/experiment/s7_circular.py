"""S7 circular coordinates (D-047; RESEARCH_SUMMARY §7.7): do the circular coordinates of the
activation cloud track the latent x angle?

Per run of ``circular_coordinates.conditions`` (O, P: 3 replicates × 2 worlds; U: seed 1729 × 2
worlds), at ``checkpoints`` (0 and final), on the 8 test panels: ``analysis.CircularCorrespondence``
on the primary hook (raw Euclidean, top H₁ cocycle, coefficient field F_47), against
θ = 2π x(z₃₂)/12 with the y angle as control, a 1000-permutation null over histories, and the
oracle's agreement (circular mean of b32) as a reference. All values are ``privileged_eval``
and descriptive. Per run and checkpoint the job adds the median agreement over panels and the
number of panels whose agreement exceeds the null q95.
"""

from __future__ import annotations

import logging

import numpy as np

from topo_pilot.analysis import CircularCorrespondence
from topo_pilot.contracts import (
    ArtifactStore,
    EvalSidecar,
    MetricRecords,
    MetricRow,
    SeedTree,
    StageFailure,
)

from .config import ResolvedConfig
from .s2 import child_of
from .s4_analysis import WORLDS, AnalysisJob, _row

log = logging.getLogger(__name__)
CONS = "experiment"
SPACE = "privileged_eval:circular"


class CircularJob:
    """Writes one MetricRecords (``kind = circular``)."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        c = cfg.stage("S7")["circular_coordinates"]
        self.cc = CircularCorrespondence(int(c["coeff_p"]), int(c["n_perm"]))
        self.steps = [int(s) for s in c["checkpoints"]]
        self.conditions = list(c["conditions"])
        self.hook = cfg.base["model"]["primary_hook"]
        self.panels = list(range(1, cfg.base["data"]["n_panels"] + 1))
        self.aj = AnalysisJob("S4", cfg, store)
        self.parents: set[str] = set()

    def runs(self) -> list[tuple[str, str, int]]:
        out = []
        for cond in self.conditions:
            seeds = self.cfg.base["seeds"]["masters"]
            if cond == "U":
                seeds = sorted({int(r["seed"]) for r in self.cfg.stage("S7")["runs_ordered"]
                                if r["condition"] == "U"})
            out += [(w, cond, int(s)) for s in seeds for w in WORLDS]
        return out

    def run_rows(self, world: str, cond: str, seed: int) -> list[MetricRow]:
        inputs = self.aj.inputs(world, cond, seed)
        sidecar = child_of(self.store, EvalSidecar, inputs["emission"], split="test")
        self.parents.update((sidecar, inputs["oracle"], inputs["world"]))
        rows = []
        for step in self.steps:
            act = self.aj.acts(world, cond, seed, step)
            common = {"world": world, "condition": cond, "replicate": seed, "checkpoint": step}
            step_rows = []
            for p in self.panels:
                rng = SeedTree(0).generator("circ_null", world, cond, seed, step, p)
                step_rows += self.cc.run(self.store, act, sidecar, inputs["world"],
                                         inputs["oracle"], self.hook, p, rng, **common)
            rows += step_rows
            rows += self.summary(step_rows, common)
        return rows

    @staticmethod
    def summary(rows: list[MetricRow], common: dict) -> list[MetricRow]:
        by_panel: dict[int, dict[str, float | None]] = {}
        for r in rows:
            by_panel.setdefault(r.panel, {})[r.metric_id] = r.value
        agree = [v.get("agreement_x") for v in by_panel.values()]
        ok = [a for a in agree if a is not None]
        above = sum(1 for v in by_panel.values() if v.get("agreement_x") is not None
                    and v["agreement_x"] > v["agreement_x_null_q95"])
        ctrl = [v["agreement_control"] for v in by_panel.values()
                if v.get("agreement_control") is not None]
        oracle = [v["agreement_oracle_x"] for v in by_panel.values()]
        return [_row("agreement_x_median", float(np.median(ok)) if ok else None, SPACE, **common),
                _row("n_panels_above_null_q95", float(above), SPACE, **common),
                _row("n_panels_with_h1_class", float(len(ok)), SPACE, **common),
                _row("agreement_control_median", float(np.median(ctrl)) if ctrl else None,
                     SPACE, **common),
                _row("agreement_oracle_x_median", float(np.median(oracle)), SPACE, **common)]

    def run(self) -> list[str]:
        rows: list[MetricRow] = []
        for world, cond, seed in self.runs():
            try:
                rows += self.run_rows(world, cond, seed)
            except (KeyError, StageFailure) as exc:  # missing run: documented, not invented
                log.warning("S7 circular: %s-%s-%s unavailable (%s)", world, cond, seed, exc)
                rows.append(_row("run_available", None, SPACE, status="not_run", world=world,
                                 condition=cond, replicate=seed,
                                 uncertainty_kind=type(exc).__name__))
        self.parents.update(self.aj.parents)
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": "S7", "kind": "circular"},
                              parents=sorted(self.parents), seed_map={}, consumer=CONS)
        log.info("S7 circular: %d rows", len(rows))
        return [mid]
