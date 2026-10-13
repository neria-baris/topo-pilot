"""Stage S2: data, exact oracle, n-gram baselines, σ calibration, discriminability (no model).

Gates (STAGES §2): G-B oracle correct + N/U controls behave; G-C σ selected by the rule;
G-D no latent field in public data + leakage checks. World-difference rule: D-023.
"""

from __future__ import annotations

import dataclasses
import logging
import sys
from collections.abc import Mapping
from typing import Any

import numpy as np

from topo_pilot.analysis import (
    DiscriminabilityTable,
    PointSet,
    SigmaCalibrator,
    SigmaRow,
    SpaceBuilder,
    ph_summary,
)
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    EvalSidecar,
    GateCheck,
    MetricRecords,
    MetricRow,
    ObservationSet,
    OracleOutputs,
    ProcessDiagnostics,
    SeedTree,
    StageFailure,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.dataset import DatasetConfig, DatasetStage
from topo_pilot.oracle import OracleStage
from topo_pilot.prediction import PredictionStage
from topo_pilot.process import EmissionConfig, ProcessStage

from .config import ResolvedConfig
from .stages import Stage, register_stage, run_tool, save_tool_gate

log = logging.getLogger(__name__)
CONS = "experiment"
MODES = {"O": "overlap", "P": "axis_permuted", "N": "identical", "U": "unique"}
PUBLIC_FIELDS = {"split", "V", "sequence_id", "tokens", "layout_version"}


def world_id(store: ArtifactStore, cfg: ResolvedConfig, family: str) -> str:
    """The unique WorldSpec of ``family`` with the configured dims and metric."""
    worlds = cfg.base["worlds"]
    ids = store.find(WorldSpec, family=family, dims=list(worlds["dims"]), metric=worlds["metric"])
    if len(ids) != 1:
        raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.world_id", "world",
                           f"WorldSpec {family} {worlds['dims']} {worlds['metric']}: "
                           f"{len(ids)} found")
    return ids[0]


def child_of(store: ArtifactStore, cls: type, parent: str, **flt: Any) -> str:
    """The unique ``cls`` artifact with ``parent`` among its parents and matching config."""
    ids = [a for a in store.find(cls, **flt) if parent in store.meta(a).parent_ids]
    if len(ids) != 1:
        raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.S2", "child_of",
                           f"{cls.__name__} under {parent} with {flt}: {len(ids)} found")
    return ids[0]


def _row(space: str, metric: str, value: float | None, world: str | None = None,
         condition: str | None = None, panel: int | None = None, replicate: int | None = None,
         status: str = "ok", parents: tuple[str, ...] = ()) -> MetricRow:
    return MetricRow(run_id="S2", space=space, metric_id=metric, value=value, status=status,
                     world=world, condition=condition, panel=panel, replicate=replicate,
                     parent_ids=parents)


@register_stage
class S2Stage(Stage):
    """S2 as one job: calibrate σ, then build all replicate datasets, oracles and baselines."""

    stage_id = "S2"
    requires = ("S1",)
    gates = ("G-B", "G-C", "G-D")

    def plan(self, cfg: ResolvedConfig, store: ArtifactStore) -> list[Mapping[str, Any]]:
        return [{"stage": "S2", "job": "data_oracle_calibration"}]

    # ---- building blocks ------------------------------------------------------------------
    def _ctx(self, cfg: ResolvedConfig, store: ArtifactStore) -> dict[str, Any]:
        base = cfg.base
        worlds = {f: world_id(store, cfg, f) for f in base["worlds"]["core"]}
        trans = {f: child_of(store, TransitionSpec, w) for f, w in worlds.items()}
        data = base["data"]
        dcfg = DatasetConfig(n_train=data["n_train"], n_dev=data["n_dev"], n_test=data["n_test"],
                             n_panels=data["n_panels"], panel_size=data["panel_size"],
                             analysis_position=base["sequences"]["analysis_position"])
        return {"worlds": worlds, "trans": trans, "dcfg": dcfg, "V": base["emissions"]["V"]}

    def _emission(self, ctx: dict, store: ArtifactStore, family: str, cond: str,
                  sigma: float | None, master: int) -> str:
        V = ctx["N"] if cond == "U" else ctx["V"]
        ecfg = EmissionConfig(mode=MODES[cond], V=V, sigma=sigma if cond in ("O", "P") else None,
                              source_mode="overlap" if cond == "P" else None)
        return ProcessStage().run_emission(ctx["worlds"][family], ecfg, SeedTree(master), store)

    def _pipeline(self, ctx: dict, store: ArtifactStore, family: str, eid: str, master: int,
                  baselines: bool) -> dict[str, str]:
        tid = ctx["trans"][family]
        ds = DatasetStage().run(tid, eid, ctx["dcfg"], SeedTree(master), store)
        orc = OracleStage().run(tid, eid, ds["obs_test"], ds["history_index"], store)
        out = {**ds, **orc, "emission": eid, "world": ctx["worlds"][family]}
        if baselines:
            ids = PredictionStage().run_baselines(ds["obs_train"], ds["obs_dev"], ds["obs_test"],
                                                  ds["history_index"], store)
            out.update({f"baseline_{i + 1}": b for i, b in enumerate(ids)})
        return out

    # ---- calibration ----------------------------------------------------------------------
    def _calibrate(self, cfg: ResolvedConfig, ctx: dict, store: ArtifactStore):
        base, rows, records = cfg.base, [], []
        master = base["seeds"]["masters"][0]
        for sigma in base["emissions"]["sigma_candidates"]:
            for family in base["worlds"]["core"]:
                eid = self._emission(ctx, store, family, "O", sigma, master)
                ref = self._pipeline(ctx, store, family, eid, master, baselines=False)
                diag = store.load(ProcessDiagnostics, ref["diagnostics"], consumer=CONS)
                p_w = store.load(EmissionSpec, eid, consumer=CONS).diagnostics["p_w"]
                rows.append(SigmaRow(sigma=float(sigma), world=family, mean_H_b1=diag.mean_H_b1,
                                     G_C=diag.G_C, min_p_w=float(min(p_w)), V=ctx["V"]))
                records += [_row(f"sigma:{sigma!r}", k, float(v), family, "O",
                                 parents=(ref["diagnostics"],))
                            for k, v in (("mean_H_b1", diag.mean_H_b1), ("G_C", diag.G_C),
                                         ("min_p_w", min(p_w)))]
        rule = base["emissions"]["sigma_rule"]
        decision = SigmaCalibrator(rule["min_mean_entropy_b1"], rule["min_context_gain_nats"],
                                   rule["min_symbol_prob_factor"],
                                   rule["fallback_min_context_gain_nats"]).select(rows)
        return decision, records

    # ---- floor and world-difference summary -----------------------------------------------
    def _floor(self, store: ArtifactStore, ref: dict, family: str, cond: str,
               n_draws: int) -> list[MetricRow]:
        b32 = SpaceBuilder(store).beliefs(ref["oracle"], "b32", 1)
        hell = PointSet(space="belief32_hellinger_embedding", X=np.sqrt(b32.X) / np.sqrt(2.0),
                        D=None, ids=b32.ids, metric="euclidean")
        tree, rows = SeedTree(0), []
        for kind in ("iso", "cov"):
            vals = [ph_summary(SpaceBuilder(store).null(
                hell, kind, tree.generator("gaussian_floor", family, cond, kind, i)))["S_H1"]
                for i in range(n_draws)]
            rows += [_row(f"null:{kind}:belief32", "S_H1_mean", float(np.mean(vals)), family, cond,
                          1, parents=(ref["oracle"],)),
                     _row(f"null:{kind}:belief32", "S_H1_q95", float(np.percentile(vals, 95)),
                          family, cond, 1, parents=(ref["oracle"],))]
        return rows

    @staticmethod
    def world_difference(table: MetricRecords, n_panels: int) -> list[MetricRow]:
        """Per space × condition: number of panels with S_cyl > S_sq (D-023)."""
        S = {(r.space, r.world, r.condition, r.panel): r.value for r in table.rows
             if r.metric_id == "S_H1" and r.panel is not None}
        out = []
        for space, cond in sorted({(k[0], k[2]) for k in S}):
            pos = sum((S.get((space, "cylinder", cond, i)) or 0.0)
                      > (S.get((space, "square", cond, i)) or 0.0) for i in range(1, n_panels + 1))
            out.append(_row(space, "n_panels_cyl_gt_sq", float(pos), None, cond))
        return out

    # ---- execute --------------------------------------------------------------------------
    def execute(self, job: Mapping[str, Any], cfg: ResolvedConfig,
                store: ArtifactStore) -> list[str]:
        ctx = self._ctx(cfg, store)
        ctx["N"] = store.load(WorldSpec, next(iter(ctx["worlds"].values())), consumer=CONS).n_states
        decision, records = self._calibrate(cfg, ctx, store)
        log.info("S2: sigma decision %s (%s)", decision.sigma, decision.status)
        if decision.sigma is None:
            gid = save_tool_gate(store, cfg, "S2", "G-C",
                                 (GateCheck("sigma_selected", False, None, "rule"),), [])
            raise StageFailure(ErrorCode.GATE_FAILED, "experiment.S2", "G-C",
                               "no sigma meets the rule or the fallback: checkpoint H3", gid)
        refs = self._build_all(cfg, ctx, store, decision.sigma)
        written = list(refs["_ids"])
        disc = DiscriminabilityTable(store).compute(
            {(f, c): refs[(f, c, refs["_m0"])] for f in ctx["worlds"] for c in ("O", "P")},
            list(range(1, ctx["dcfg"].n_panels + 1)))
        draws = int(cfg.base["topology"]["gaussian_floor_draws"])
        floor = [r for f in ctx["worlds"] for c in ("O", "P")
                 for r in self._floor(store, refs[(f, c, refs["_m0"])], f, c, draws)]
        diff = self.world_difference(disc, ctx["dcfg"].n_panels)
        rows = tuple(records) + disc.rows + tuple(floor) + tuple(diff) + (
            _row("sigma", "selected", float(decision.sigma), status="ok"),)
        mid = store.save(MetricRecords(rows=rows), config={"stage": "S2", "kind": "S2"},
                         parents=[refs[(f, c, refs["_m0"])]["oracle"] for f in ctx["worlds"]
                                  for c in ("O", "P")], seed_map={}, consumer=CONS)
        written.append(mid)
        written += self._gates(cfg, ctx, store, refs, decision, mid)
        return written

    def _build_all(self, cfg, ctx, store, sigma) -> dict:
        refs: dict = {"_ids": []}
        masters = cfg.base["seeds"]["masters"]
        refs["_m0"] = masters[0]
        for master in masters:
            for family in ctx["worlds"]:
                for cond in ("O", "P", "N"):
                    eid = self._emission(ctx, store, family, cond, sigma, master)
                    refs[(family, cond, master)] = self._pipeline(ctx, store, family, eid, master,
                                                                  baselines=True)
                    refs["_ids"].append(refs[(family, cond, master)]["oracle"])
        for family in ctx["worlds"]:
            eid = self._emission(ctx, store, family, "U", None, masters[0])
            refs[(family, "U", masters[0])] = self._pipeline(ctx, store, family, eid, masters[0],
                                                             baselines=False)
        return refs

    def _gates(self, cfg, ctx, store, refs, decision, mid) -> list[str]:
        m0 = refs["_m0"]
        n_err = u_err = 0.0
        for family in ctx["worlds"]:
            o_n = store.load(OracleOutputs, refs[(family, "N", m0)]["oracle"], consumer=CONS)
            pi = store.load(TransitionSpec, ctx["trans"][family], consumer=CONS).pi
            n_err = max(n_err, float(np.abs(o_n.b32 - pi).max()),
                        float(np.abs(o_n.q - 1.0 / o_n.q.shape[1]).max()))
            o_u = store.load(OracleOutputs, refs[(family, "U", m0)]["oracle"], consumer=CONS)
            u_err = max(u_err, float(np.abs(o_u.b32.max(axis=1) - 1.0).max()))
        oracle_ok, oracle_line = _pytest(cfg, "tests/oracle")
        g_b = (GateCheck("oracle_suite_brute_force", oracle_ok, oracle_line, "all pass"),
               GateCheck("N_control_belief_is_pi_and_q_uniform", n_err < 1e-10, n_err, 1e-10),
               GateCheck("U_control_belief_is_delta", u_err < 1e-10, u_err, 1e-10))
        g_c = (GateCheck("sigma_selected_by_rule", decision.status in ("ok", "weak_context"),
                         decision.sigma, decision.status),)
        fields = {f.name for f in dataclasses.fields(ObservationSet)}
        try:
            sid = refs[(next(iter(ctx["worlds"])), "O", m0)]["sidecar_test"]
            store.load(EvalSidecar, sid, consumer="learner")
            leak_blocked = False
        except StageFailure as exc:
            leak_blocked = exc.code == ErrorCode.LEAKAGE
        imports_ok, imports_line = run_tool([sys.executable, "tools/check_imports.py"], cfg, 900)
        ds_ok, ds_line = _pytest(cfg, "tests/dataset")
        g_d = (GateCheck("no_latent_field_in_ObservationSet", fields == PUBLIC_FIELDS,
                         sorted(fields), sorted(PUBLIC_FIELDS)),
               GateCheck("learner_cannot_load_sidecar", leak_blocked, leak_blocked, True),
               GateCheck("check_imports_clean", imports_ok, imports_line, "clean"),
               GateCheck("dataset_leakage_tests", ds_ok, ds_line, "all pass"))
        return [save_tool_gate(store, cfg, "S2", gid, checks, [mid])
                for gid, checks in (("G-B", g_b), ("G-C", g_c), ("G-D", g_d))]


def _pytest(cfg: ResolvedConfig, folder: str) -> tuple[bool, str]:
    return run_tool([sys.executable, "-m", "pytest", folder, "-q", "-p", "no:cacheprovider"],
                    cfg, 900)
