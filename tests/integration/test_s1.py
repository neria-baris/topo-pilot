"""I01: S1 on the real core config produces the specs and passes G-A checks 1-2 (and 3)."""

from pathlib import Path

import pytest

from topo_pilot.contracts import (ArtifactStore, EmissionSpec, GateCheck, GateReport,
                                  LocalFSBackend, TransitionSpec, WorldSpec)
from topo_pilot.experiment import load_config, run_stage

pytestmark = [pytest.mark.integration, pytest.mark.experiment]

REPO = Path(__file__).resolve().parents[2]


def test_I01_s1_core_config(tmp_path):
    cfg = load_config(REPO / "configs" / "stages.yaml", repo_root=REPO)
    store = ArtifactStore(LocalFSBackend(tmp_path / "artifacts"))
    s0 = GateReport(stage="S0", gate_id="G-S0", verdict="pass",
                    checks=(GateCheck("stub_for_integration", True),))
    store.save(s0, config={"stage": "S0", "gate": "G-S0"}, parents=[], seed_map={},
               consumer="experiment")

    run_stage("S1", cfg, store)

    worlds = store.find(WorldSpec)
    assert len(worlds) == 2
    assert len(store.find(TransitionSpec)) == 2
    n_sigma = len(cfg.base["emissions"]["sigma_candidates"])
    n_masters = len(cfg.base["seeds"]["masters"])
    assert len(store.find(EmissionSpec)) == 2 * n_masters * (2 * n_sigma + 1)
    (gid,) = store.find(GateReport, stage="S1")
    report = store.load(GateReport, gid, consumer="experiment")
    assert report.gate_id == "G-A"
    assert all(c.passed for c in report.checks), report.checks
    assert report.verdict == "pass"

    # identical rerun gives identical ids (content addressing)
    assert store.find(WorldSpec) == worlds
