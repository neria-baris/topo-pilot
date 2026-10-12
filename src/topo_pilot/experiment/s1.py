"""Stage S1: worlds, transition kernels, emission specs, and the PH calibration gate G-A.

G-A (STAGES §2, thresholds fixed in D-016):
  1. computed β equals expected β for every core world (p = 2 and 3);
  2. Vietoris–Rips on d_M gives a long H1 bar for the cylinder only: S_cyl ≥ 0.20, S_sq < 0.10;
  3. synthetic circle vs disk (M = 512, R^128, noise 0.05): S_circle > max S_disk in ≥ 19/20.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    Diagrams,
    GateCheck,
    GateReport,
    MetricRecords,
    MetricRow,
    SeedTree,
    WorldSpec,
)
from topo_pilot.process import EmissionConfig, ProcessStage, TransitionConfig
from topo_pilot.topology import PersistenceComputer, PHConfig, Summaries, SyntheticShapes
from topo_pilot.world import WorldConfig, WorldStage

from .config import ResolvedConfig
from .stages import Stage, register_stage

log = logging.getLogger(__name__)

S_CYL_MIN, S_SQ_MAX = 0.20, 0.10
CALIB_DRAWS, CALIB_M, CALIB_AMBIENT, CALIB_NOISE, CALIB_MIN_CORRECT = 20, 512, 128, 0.05, 19
CALIB_MASTER = 0  # world-scoped calibration stream (D-012 style), independent of replicates

_MODES = {"O": "overlap", "P": "axis_permuted", "N": "identical"}


def _row(space: str, metric_id: str, value: float | None, world: str | None = None,
         parents: tuple[str, ...] = (), status: str = "ok", units: str = "") -> MetricRow:
    return MetricRow(run_id="S1", space=space, metric_id=metric_id, value=value, status=status,
                     world=world, units=units, parent_ids=parents)


def world_ph(world: WorldSpec, matrix: str, coeff_p: int = 2) -> tuple[Any, float]:
    """Diagrams (H0, H1) of the world's ``dist`` or ``dist_graph`` and the scale s (q95)."""
    D = np.asarray(getattr(world, matrix), dtype=np.float64)
    positive = D[np.triu_indices_from(D, k=1)]
    scale = float(np.percentile(positive[positive > 0], 95))
    diag = PersistenceComputer(PHConfig(maxdim=1, coeff_p=coeff_p)).diagrams(D)
    return diag, scale


def calibration_scores(n_draws: int = CALIB_DRAWS) -> tuple[list[float], list[float]]:
    """S of ``n_draws`` noisy circles and disks (Euclidean VR, H1), seeded per draw."""
    tree = SeedTree(CALIB_MASTER)
    ph = PersistenceComputer(PHConfig(maxdim=1))
    out: dict[str, list[float]] = {"circle": [], "disk": []}
    for shape in out:
        for draw in range(n_draws):
            rng = tree.generator("ga_calibration", shape, draw)
            X = getattr(SyntheticShapes, shape)(CALIB_M, ambient=CALIB_AMBIENT, noise=CALIB_NOISE,
                                                rng=rng)
            D = np.sqrt(np.maximum(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1), 0.0))
            np.fill_diagonal(D, 0.0)
            pos = D[np.triu_indices_from(D, k=1)]
            out[shape].append(Summaries.S(ph.diagrams(D), 1, float(np.percentile(pos, 95))))
    return out["circle"], out["disk"]


@register_stage
class S1Stage(Stage):
    """S1: build both core worlds, their kernels, and O/P/N emissions for every σ candidate and
    replicate; compute world PH and the synthetic calibration; write MetricRecords + G-A."""

    stage_id = "S1"
    requires = ("S0",)
    gates = ("G-A",)

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "S1", "job": "build_and_calibrate"}]

    def _build_specs(self, cfg: ResolvedConfig, store: ArtifactStore) -> dict[str, str]:
        base, stage = cfg.base, cfg.stage("S1")
        dims = tuple(base["worlds"]["dims"])
        world_ids: dict[str, str] = {}
        proc = ProcessStage()
        conditions = stage.get("emissions_for_sigmas", ["O", "P", "N"])
        for family in base["worlds"]["core"]:
            wid = WorldStage().run(WorldConfig(family=family, dims=dims,
                                               metric=base["worlds"]["metric"]), store)
            world_ids[family] = wid
            proc.run_transition(wid, TransitionConfig(p_stay=base["dynamics"]["p_stay"]), store)
            for master in base["seeds"]["masters"]:
                for cond in conditions:
                    sigmas = [None] if cond == "N" else base["emissions"]["sigma_candidates"]
                    for sigma in sigmas:
                        ecfg = EmissionConfig(mode=_MODES[cond], V=base["emissions"]["V"],
                                              sigma=sigma,
                                              center_strategy=base["emissions"]["center_strategy"],
                                              source_mode="overlap" if cond == "P" else None)
                        proc.run_emission(wid, ecfg, SeedTree(master), store)
        return world_ids

    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        world_ids = self._build_specs(cfg, store)
        rows: list[MetricRow] = []
        written: list[str] = []
        betti_ok, s_world = True, {}
        for family, wid in world_ids.items():
            world = store.load(WorldSpec, wid, consumer="experiment")
            betti_ok &= world.betti_computed == world.betti_expected
            cycle_rank = len(world.edges) - world.n_states + 1
            rows += [_row("world", "beta1_gf2", float(world.betti_computed[2][1]), family, (wid,)),
                     _row("world", "graph_cycle_rank", float(cycle_rank), family, (wid,))]
            for matrix in ("dist", "dist_graph"):
                diag, scale = world_ph(world, matrix)
                did = store.save(Diagrams(coeff_p=diag.coeff_p, maxdim=diag.maxdim,
                                          threshold=float(diag.threshold),
                                          library_version=diag.library_version,
                                          rows=diag.rows, status=diag.status.value),
                                 config={"stage": "S1", "world": family, "matrix": matrix},
                                 parents=[wid], seed_map={}, consumer="experiment")
                written.append(did)
                S = Summaries.S(diag, 1, scale)
                if matrix == "dist":
                    s_world[family] = S
                space = "world_flat" if matrix == "dist" else "world_graph"
                rows += [_row(space, "S_H1", S, family, (did,)),
                         _row(space, "scale_s", scale, family, (did,)),
                         _row(space, "n_H1_bars", float((diag.rows[:, 0] == 1).sum()),
                              family, (did,))]
        circle, disk = calibration_scores()
        n_correct = sum(c > max(disk) for c in circle)
        rows += [_row("synthetic", "S_circle_mean", float(np.mean(circle))),
                 _row("synthetic", "S_disk_max", float(max(disk))),
                 _row("synthetic", "n_correct_of_20", float(n_correct))]
        mid = store.save(MetricRecords(rows=tuple(rows)), config={"stage": "S1", "kind": "S1"},
                         parents=list(world_ids.values()), seed_map={}, consumer="experiment")
        written.append(mid)
        checks = (
            GateCheck("betti_correct_both_worlds", bool(betti_ok), betti_ok, True),
            GateCheck("S_cylinder_long_bar", s_world["cylinder"] >= S_CYL_MIN,
                      round(s_world["cylinder"], 6), S_CYL_MIN),
            GateCheck("S_square_no_long_bar", s_world["square"] < S_SQ_MAX,
                      round(s_world["square"], 6), S_SQ_MAX),
            GateCheck("synthetic_circle_vs_disk", n_correct >= CALIB_MIN_CORRECT,
                      int(n_correct), CALIB_MIN_CORRECT),
        )
        verdict = "pass" if all(c.passed for c in checks) else "fail"
        gid = store.save(GateReport(stage="S1", gate_id="G-A", verdict=verdict, checks=checks),
                         config={"stage": "S1", "gate": "G-A", "config_hash": cfg.config_hash},
                         parents=[mid], seed_map={}, consumer="experiment")
        log.info("S1: G-A %s (S_cyl=%.3f, S_sq=%.3f, synthetic %d/20)", verdict,
                 s_world["cylinder"], s_world["square"], n_correct)
        return written + [gid]

