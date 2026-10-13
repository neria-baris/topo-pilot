"""Dispatch of the S7 analysis jobs (D-047); each writes one MetricRecords."""

from __future__ import annotations

from topo_pilot.contracts import ArtifactStore, MetricRecords

from .config import ResolvedConfig


def run(kind: str, cfg: ResolvedConfig, store: ArtifactStore) -> list[str]:
    """Run S7 job ``kind``: dev_extract, controls, probes, circular or sensitivity."""
    if kind == "dev_extract":
        from .s7_dev import DevData

        ids = DevData(cfg, store).extract_all()
        return [store.save(MetricRecords(rows=()), config={"stage": "S7", "kind": "dev_extract"},
                           parents=sorted(ids), seed_map={}, consumer="experiment"), *ids]
    if kind == "controls":
        from .s7_controls import ControlsJob

        return ControlsJob(cfg, store).run()
    if kind == "probes":
        from .s7_probes import ProbesJob

        return ProbesJob(cfg, store).run()
    if kind == "circular":
        from .s7_circular import CircularJob

        return CircularJob(cfg, store).run()
    if kind == "sensitivity":
        from .s7_sensitivity import SensitivityJob

        return SensitivityJob(cfg, store).run()
    raise ValueError(f"unknown S7 job {kind!r}")
