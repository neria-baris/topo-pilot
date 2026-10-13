"""S7 one-factor-at-a-time sensitivity (D-047; RESEARCH_SUMMARY §7.7).

Variants, each changing one factor of the primary analysis (raw Euclidean activations,
Hellinger beliefs, M = 512): ``chord`` (activation metric), ``pca32`` (PCA-32 fitted on the
same run's dev activations at the same checkpoint), ``M256`` (first 256 histories of each panel
in HistoryIndex order), ``sqrt_js`` (distribution metric). Per variant and condition (O, P):

- the registered F1 rule (D, u_r recomputed; same learning gates), except ``sqrt_js``, which
  leaves every activation S unchanged and so the F1 rule too (not recomputed);
- Δgeom (all pairs, same-last-symbol pairs) at the final checkpoint, with the fraction of
  positive run-panels;
- the H3′ rule (D-037): ρ_s(d_A, d_B32) at final > at checkpoint 0 and > ρ_s for R2 and R3,
  per panel; verdict via ``run_rule_verdict`` (≥ 7/8 panels in every run of 3 replicates).

Every verdict here is a robustness check of a primary verdict, never a replacement.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy.spatial.distance import cdist

from topo_pilot.analysis import F1Decision, GeometryAlignment, PointSet, Sensitivity, ph_summary
from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow, TransitionSpec

from .config import ResolvedConfig
from .s2 import child_of
from .s4_analysis import WORLDS, AnalysisJob, _row
from .s7_dev import DevData
from .x4 import _gt_all, _rho, run_rule_verdict

log = logging.getLogger(__name__)
CONS = "experiment"
CODE = {"SUPPORTED": 1.0, "REJECTED": 0.0}


class SensitivityJob:
    """Writes one MetricRecords (``kind = sensitivity``)."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        s = cfg.stage("S7")["sensitivity"]
        self.variants = ([f"{m}" for m in s["activation_metric"]]
                         + [f"pca{int(k)}" for k in s["pca_dims"]]
                         + [f"M{int(k)}" for k in s["panel_size"]]
                         + [f"{m}" for m in s["distribution_metric"]])
        self.pca_dims = {f"pca{int(k)}": int(k) for k in s["pca_dims"]}
        self.sizes = {f"M{int(k)}": int(k) for k in s["panel_size"]}
        self.dist_variants = set(s["distribution_metric"])
        base = cfg.base
        self.final = int(base["training"]["primary_checkpoint"])
        self.hook = base["model"]["primary_hook"]
        self.panels = list(range(1, base["data"]["n_panels"] + 1))
        self.seeds = [int(x) for x in base["seeds"]["masters"]]
        rule = base["f1_rule"]
        self.min_panels = int(rule["min_positive_panels"])
        self.f1 = F1Decision(self.min_panels, float(rule["envelope_quantile"]))
        self.dev = DevData(cfg, store)
        self.aj = self.dev.aj
        self.sens = Sensitivity()
        self.k = base["baselines"]["spectral_components"]
        self._jobs: dict[str, AnalysisJob] = {}

    # ---- clouds ---------------------------------------------------------------------------
    def act_D(self, variant: str, world, cond, seed, step, p) -> tuple[np.ndarray, list[str]]:
        cloud = self.aj.sb.activations(self.aj.acts(world, cond, seed, step), self.hook, p)
        X, ids = cloud.X, list(cloud.ids)
        if variant in self.sizes:
            keep = Sensitivity.head(len(ids), self.sizes[variant])
            X, ids = X[keep], [ids[i] for i in keep]
        if variant in self.pca_dims:
            dev_id = self.dev.dev_acts(world, cond, seed, step)
            self.aj.parents.add(dev_id)
            X_fit = self.dev.all_rows(dev_id)
            return self.sens.activation_D(X, "pca", X_fit, self.pca_dims[variant]), ids
        metric = "chord" if variant == "chord" else "euclidean"
        return self.sens.activation_D(X, metric), ids

    def belief_D(self, variant: str, world, cond, seed, p, ids: list[str]) -> dict:
        oracle = self.aj.inputs(world, cond, seed)["oracle"]
        metric = "sqrt_js" if variant in self.dist_variants else "hellinger"
        out = {}
        for which in ("b32", "b1"):
            ps = self.aj.sb.beliefs(oracle, which, p)
            row = {h: i for i, h in enumerate(ps.ids)}
            out[which] = self.sens.distribution_D(ps.X[[row[h] for h in ids]], metric)
        return out

    def baseline_D(self, world, cond, seed, p, ids: list[str]) -> dict:
        inputs = self.aj.inputs(world, cond, seed)
        refs = {"emission_id": inputs["emission"], "obs_test_id": inputs["obs_test"],
                "transition_id": child_of(self.store, TransitionSpec, inputs["world"]),
                "history_index_id": inputs["history_index"], "k": self.k}
        out = {}
        for kind in ("R2", "R3"):
            ps = self.aj.sb.baseline(kind, p, **refs)
            row = {h: i for i, h in enumerate(ps.ids)}
            X = ps.X[[row[h] for h in ids]]
            out[kind] = cdist(X, X)
        return out

    # ---- one run --------------------------------------------------------------------------
    def run_panel(self, variant, world, cond, seed, p, S, common) -> tuple[list, dict]:
        rows, recompute_S = [], variant not in self.dist_variants
        D_A = {}
        for ckpt, step in (("init", 0), ("final", self.final)):
            D_A[ckpt], ids = self.act_D(variant, world, cond, seed, step, p)
            if recompute_S:
                res = ph_summary(PointSet(f"sens:{variant}", None, D_A[ckpt], ids, "euclidean"))
                S[(world, ckpt, p)] = float(res["S_H1"])
                rows.append(_row("S_H1", S[(world, ckpt, p)], f"sens:{variant}",
                                 status=res["status"], checkpoint=step, panel=p, **common))
        B = self.belief_D(variant, world, cond, seed, p, ids)
        last = self.aj._history_tokens(self.aj.inputs(world, cond, seed), offset=-1)
        dg = GeometryAlignment().delta_geom(D_A["final"], B["b32"], B["b1"],
                                            np.array([last[h] for h in ids]))
        iu = np.triu_indices(len(ids), k=1)
        R = self.baseline_D(world, cond, seed, p, ids)
        rho = {name: _rho(M[iu], B["b32"][iu]) for name, M in
               (("final", D_A["final"]), ("init", D_A["init"]), ("R2", R["R2"]),
                ("R3", R["R3"]))}
        h3p = _gt_all(rho["final"], rho["init"], rho["R2"], rho["R3"])
        space = f"sens:{variant}"
        rows += [_row("delta_geom_all", dg["all"], space, panel=p, **common),
                 _row("delta_geom_same_last_symbol", dg["same_last_symbol"], space, panel=p,
                      status="ok" if dg["status_same"] == "ok" else "inconclusive", **common),
                 *[_row(f"rho_b32_{k}", v, space, panel=p, **common) for k, v in rho.items()],
                 _row("h3prime_panel_pass", float(h3p), space, panel=p, **common)]
        return rows, {"dg": dg["all"], "h3p": h3p}

    def condition(self, variant: str, cond: str) -> list[MetricRow]:
        rows, per_rep, gates, statuses = [], [], [], []
        n_pass, run_gates, dgs = {}, {}, []
        space = f"sens:{variant}"
        for seed in self.seeds:
            S: dict = {}
            for world in WORLDS:
                common = {"world": world, "condition": cond, "replicate": seed}
                passes = 0
                for p in self.panels:
                    prow, stat = self.run_panel(variant, world, cond, seed, p, S, common)
                    rows += prow
                    passes += int(stat["h3p"])
                    if stat["dg"] is not None and np.isfinite(stat["dg"]):
                        dgs.append(stat["dg"])
                    statuses += [r.status for r in prow if r.metric_id == "S_H1"]
                n_pass[(world, seed)] = passes
                run_gates[(world, seed)] = self.gate(cond, world, seed)
                rows.append(_row("h3prime_n_pass", float(passes), space, **common))
            gates.append(all(run_gates[(w, seed)] for w in WORLDS))
            if S:
                D, u = self.f1.contrasts(S), self.f1.noise_envelope(S)
                per_rep.append((D, u))
                rows += [_row("D", float(d), space, condition=cond, replicate=seed, panel=p)
                         for p, d in zip(self.panels, D)]
                rows += [_row("u", u, space, condition=cond, replicate=seed),
                         _row("median_D", float(np.median(D)), space, condition=cond,
                              replicate=seed)]
        if variant not in self.dist_variants:
            v = self.f1.verdict(per_rep, gates, statuses)
            rows.append(_row(f"F1rule_verdict_{v.status}", CODE.get(v.status), space,
                             condition=cond, uncertainty_kind="; ".join(v.reasons) or None))
        status, reason = run_rule_verdict(n_pass, run_gates, self.min_panels, len(self.seeds))
        rows += [_row(f"H3prime_verdict_{status}", CODE.get(status), space, condition=cond,
                      uncertainty_kind=reason or None),
                 _row("delta_geom_all_fraction_positive",
                      float(np.mean(np.array(dgs) > 0)) if dgs else None, space,
                      condition=cond)]
        return rows

    def gate(self, cond: str, world: str, seed: int) -> bool | None:
        """Learning gate of a run from its S4 (O) or S5 (P) run record."""
        if cond not in self._jobs:
            self._jobs[cond] = AnalysisJob("S4" if cond == "O" else "S5", self.cfg, self.store)
        job = self._jobs[cond]
        gate = job.learning_gate(world, seed)
        self.aj.parents.update(job.parents)
        return gate

    def run(self) -> list[str]:
        rows: list[MetricRow] = []
        for cond in self.dev.conditions:
            for variant in self.variants:
                log.info("S7 sensitivity: %s under %s", variant, cond)
                rows += self.condition(variant, cond)
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": "S7", "kind": "sensitivity",
                                      "variants": self.variants},
                              parents=sorted(self.aj.parents), seed_map={}, consumer=CONS)
        return [mid]
