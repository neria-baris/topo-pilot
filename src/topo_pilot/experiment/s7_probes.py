"""S7 probes (D-047; RESEARCH_SUMMARY §7.7): ridge decoding of the 32-symbol belief.

Per O/P run: ``RidgeProbe`` fitted on dev panels ``fit_panels``, λ chosen on dev
``val_panels``, scored once on the 8 test panels (pooled R² and per-panel R²).

| probe | features | target |
|---|---|---|
| ``A{final}->b32`` (main) and ``A0->b32`` | primary hook at that checkpoint | b32 |
| ``A{final}->r_w`` | primary hook | b1 = r_{w32} |
| ``A{final}->b32_shuffled`` | primary hook | b32, fit and val rows permuted (label control) |
| ``onehot_w32->b32`` | one-hot of w32 (best affine last-symbol decoder) | b32 |
| ``F1->b32`` | the exact one-step future q = b32 T E (F1-decoding baseline) | b32 |

Descriptive only: ``pattern`` = 1 iff R²(A_final→b32) exceeds the maximum of the A0,
one-hot and F1 decoders on the same run. No verdict.
"""

from __future__ import annotations

import logging

import numpy as np

from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow, SeedTree, StageFailure
from topo_pilot.prediction import RidgeProbe

from .config import ResolvedConfig
from .s4_analysis import _row
from .s7_dev import DevData, ProbeData

log = logging.getLogger(__name__)
CONS = "experiment"


def _onehot(w: np.ndarray, V: int) -> np.ndarray:
    return np.eye(V, dtype=np.float64)[np.asarray(w, dtype=np.int64)]


class ProbesJob:
    """Writes one MetricRecords (``kind = probes``)."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        p = cfg.stage("S7")["probes"]
        self.lambdas = [float(x) for x in p["lambdas"]]
        self.fit_panels, self.val_panels = list(p["fit_panels"]), list(p["val_panels"])
        self.steps = [int(s) for s in p["checkpoints"]]
        self.final = int(cfg.base["training"]["primary_checkpoint"])
        self.dev = DevData(cfg, store)
        self.parents: set[str] = set()

    def _features(self, world, cond, seed, dev: ProbeData, test: ProbeData, V: int) -> dict:
        feats = {}
        for step in self.steps:
            dev_id = self.dev.dev_acts(world, cond, seed, step)
            test_id = self.dev.aj.acts(world, cond, seed, step)
            self.parents.update((dev_id, test_id))
            feats[f"A{step}"] = (self.dev.features(dev_id, dev.ids),
                                 self.dev.features(test_id, test.ids))
        feats["onehot_w32"] = (_onehot(dev.w32, V), _onehot(test.w32, V))
        feats["F1"] = (dev.q, test.q)
        return feats

    def probe(self, Xd, Yd, Xt, Yt, dev: ProbeData, test: ProbeData,
              shuffle_rng=None) -> tuple[RidgeProbe, dict, list[float]]:
        fit = np.isin(dev.panel, self.fit_panels)
        val = np.isin(dev.panel, self.val_panels)
        Yf, Yv = Yd[fit], Yd[val]
        if shuffle_rng is not None:
            Yf, Yv = Yf[shuffle_rng.permutation(len(Yf))], Yv[shuffle_rng.permutation(len(Yv))]
        probe = RidgeProbe(self.lambdas).fit(Xd[fit], Yf, Xd[val], Yv)
        pooled = probe.score(Xt, Yt)
        per_panel = [probe.score(Xt[test.panel == k], Yt[test.panel == k])["r2"]
                     for k in sorted(set(test.panel.tolist()))]
        return probe, pooled, per_panel

    def run_rows(self, world: str, cond: str, seed: int) -> tuple[list[MetricRow], int]:
        dev, test = self.dev.dev_targets(world, cond, seed), self.dev.test_targets(world, cond,
                                                                                  seed)
        feats = self._features(world, cond, seed, dev, test, test.q.shape[1])
        inputs = self.dev.aj.inputs(world, cond, seed)
        self.parents.update((inputs["oracle"], inputs["obs_dev"], inputs["emission"],
                             self.dev.dev_index(world, cond, seed)))
        fin = f"A{self.final}"
        plan = [(fin, "b32", None), ("A0", "b32", None), (fin, "r_w", None),
                (fin, "b32_shuffled", SeedTree(0).generator("probe_shuffle", world, cond, seed)),
                ("onehot_w32", "b32", None), ("F1", "b32", None)]
        common = {"world": world, "condition": cond, "replicate": seed}
        rows, r2 = [], {}
        for feat, target, rng in plan:
            key = "b1" if target == "r_w" else "b32"
            Xd, Xt = feats[feat]
            probe, pooled, per_panel = self.probe(Xd, getattr(dev, key), Xt, getattr(test, key),
                                                  dev, test, rng)
            name = f"{feat}->{target}"
            r2[name] = pooled["r2"]
            space = f"probe:{name}"
            rows += [_row("r2_test", pooled["r2"], space, **common),
                     _row("mse_test", pooled["mse"], space, **common),
                     _row("lambda", probe.lam, space, **common)]
            rows += [_row("r2_test_panel", v, space, panel=k, **common)
                     for k, v in enumerate(per_panel, start=1)]
        rivals = [r2["A0->b32"], r2["onehot_w32->b32"], r2["F1->b32"]]
        pattern = int(r2[f"{fin}->b32"] > max(rivals))
        rows.append(_row("pattern", float(pattern), "probe:summary", **common,
                         uncertainty_kind="descriptive"))
        return rows, pattern

    def run(self) -> list[str]:
        rows: list[MetricRow] = []
        for cond in self.dev.conditions:
            n, hits = 0, 0
            for world, c, seed in self.dev.runs():
                if c != cond:
                    continue
                try:
                    run_rows, pattern = self.run_rows(world, cond, seed)
                except (KeyError, StageFailure) as exc:  # missing run: documented, not invented
                    log.warning("S7 probes: %s-%s-%s unavailable (%s)", world, cond, seed, exc)
                    rows.append(_row("run_available", None, "probe:summary", status="not_run",
                                     world=world, condition=cond, replicate=seed,
                                     uncertainty_kind=type(exc).__name__))
                    continue
                rows += run_rows
                n, hits = n + 1, hits + pattern
            rows += [_row("n_runs", float(n), "probe:summary", condition=cond),
                     _row("n_pattern", float(hits), "probe:summary", condition=cond,
                          uncertainty_kind="descriptive")]
        mid = self.store.save(MetricRecords(rows=tuple(rows)),
                              config={"stage": "S7", "kind": "probes"},
                              parents=sorted(self.parents), seed_map={}, consumer=CONS)
        log.info("S7 probes: %d rows", len(rows))
        return [mid]
