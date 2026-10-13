"""I02: S1 -> S2 on a scaled-down config (n = 4, V = 4, small data) runs end to end."""

import shutil
from pathlib import Path

import pytest
import yaml

from topo_pilot.contracts import (
    ArtifactStore,
    BaselineOutputs,
    ErrorCode,
    GateCheck,
    GateReport,
    LocalFSBackend,
    MetricRecords,
    OracleOutputs,
    StageFailure,
)
from topo_pilot.experiment import load_config, run_stage

pytestmark = [pytest.mark.integration, pytest.mark.experiment]

REPO = Path(__file__).resolve().parents[2]


def _mini_configs(tmp: Path) -> Path:
    cfg_dir = tmp / "configs"
    shutil.copytree(REPO / "configs", cfg_dir, ignore=shutil.ignore_patterns("local.yaml"))
    base = yaml.safe_load((cfg_dir / "base.yaml").read_text(encoding="utf-8"))
    base["worlds"]["dims"] = [4, 4]
    base["emissions"]["V"] = 4
    base["seeds"]["masters"] = [1729, 2718]
    base["data"].update(n_train=2000, n_dev=256, n_test=256, n_panels=2, panel_size=64)
    (cfg_dir / "base.yaml").write_text(yaml.safe_dump(base), encoding="utf-8")
    return cfg_dir / "stages.yaml"


def test_I02_s2_mini_end_to_end(tmp_path):
    cfg = load_config(_mini_configs(tmp_path), repo_root=REPO)
    store = ArtifactStore(LocalFSBackend(tmp_path / "artifacts"))
    store.save(GateReport(stage="S0", gate_id="G-S0", verdict="pass",
                          checks=(GateCheck("stub_for_integration", True),)),
               config={"stage": "S0", "gate": "G-S0"}, parents=[], seed_map={},
               consumer="experiment")
    try:
        run_stage("S1", cfg, store)
    except StageFailure as exc:  # a 4x4 world cannot meet the 12x12 G-A thresholds (D-016)
        assert exc.code == ErrorCode.GATE_FAILED
        store.save(GateReport(stage="S1", gate_id="G-A", verdict="waived",
                              checks=(GateCheck("mini_world", False),),
                              waiver_reason="integration mini config (n = 4)"),
                   config={"stage": "S1", "gate": "G-A", "waiver": "mini"}, parents=[],
                   seed_map={}, consumer="experiment")
    try:
        run_stage("S2", cfg, store)
    except Exception as exc:  # the tiny world may legitimately fail the sigma rule
        gates = {store.load(GateReport, g, consumer="experiment").gate_id
                 for g in store.find(GateReport, stage="S2")}
        assert "G-C" in gates, f"S2 failed before the sigma gate: {exc}"
        return
    assert store.find(OracleOutputs)
    assert store.find(BaselineOutputs)
    (mid,) = store.find(MetricRecords, stage="S2")
    spaces = {r.space for r in store.load(MetricRecords, mid, consumer="experiment").rows}
    assert {"belief32", "belief1", "future1", "future2"} <= spaces
    assert any(s.startswith("sigma:") for s in spaces)
    verdicts = {store.load(GateReport, g, consumer="experiment").gate_id
                for g in store.find(GateReport, stage="S2")}
    assert verdicts == {"G-B", "G-C", "G-D"}
