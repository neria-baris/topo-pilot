"""Runner contracts: gate requirements (X02), idempotent re-runs, prereg refusal (X07)."""
import json
import math
from pathlib import Path

import pytest

from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    ErrorCode,
    GateCheck,
    GateReport,
    LocalFSBackend,
    MetricRecords,
    MetricRow,
    StageFailure,
)
from topo_pilot.experiment import load_config, run_stage
from topo_pilot.experiment.config import ResolvedConfig
from topo_pilot.experiment.prereg import write_prereg
from topo_pilot.experiment.s3 import TrainingRun, activation_ids
from topo_pilot.experiment.s4_analysis import _row
from topo_pilot.experiment.stages import latest_gate_verdicts, save_tool_gate, tool_line

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture
def store(tmp_path):
    return ArtifactStore(LocalFSBackend(tmp_path / "artifacts"), producer_version="test")


@pytest.fixture
def cfg():
    return load_config(REPO / "configs" / "stages.yaml", repo_root=REPO)


def _gate(store, stage, gate_id, verdict, created=None, tag=""):
    passed = verdict != "fail"
    aid = store.save(GateReport(stage=stage, gate_id=gate_id, verdict=verdict,
                                checks=(GateCheck("c", passed),),
                                waiver_reason="test" if verdict == "waived" else None),
                     config={"stage": stage, "gate": gate_id, "tag": tag}, parents=[],
                     seed_map={}, consumer="experiment")
    if created:  # set the creation time explicitly (meta is not part of the payload checksum)
        key = f"GateReport/{aid}/meta.json"
        meta = json.loads(store.backend.get(key))
        meta["created_utc"] = created
        store.backend.put(key, json.dumps(meta).encode("utf-8"))
    return aid


def test_X02_required_stage_needs_every_gate(store, cfg):
    _gate(store, "S2", "G-B", "pass")
    _gate(store, "S2", "G-C", "pass")
    _gate(store, "S2", "G-D", "fail")
    with pytest.raises(StageFailure) as exc:
        run_stage("S3", cfg, store)
    assert exc.value.code == ErrorCode.GATE_FAILED
    assert "G-D" in str(exc.value)


def test_X02_missing_gate_blocks(store, cfg):
    _gate(store, "S2", "G-B", "pass")
    with pytest.raises(StageFailure) as exc:
        run_stage("S3", cfg, store)
    assert "G-C" in str(exc.value) and "G-D" in str(exc.value)


def test_latest_report_per_gate_wins(store):
    _gate(store, "S2", "G-D", "pass", "2026-10-13T10:00:00+00:00", tag="old")
    _gate(store, "S2", "G-D", "fail", "2026-10-13T11:00:00+00:00", tag="new")
    assert latest_gate_verdicts(store, "S2") == {"G-D": ("fail",)}


def test_waiver_in_the_same_second_as_a_failure_counts(store):
    _gate(store, "S1", "G-A", "fail", "2026-10-13T10:00:00+00:00", tag="a")
    _gate(store, "S1", "G-A", "waived", "2026-10-13T10:00:00+00:00", tag="b")
    assert sorted(latest_gate_verdicts(store, "S1")["G-A"]) == ["fail", "waived"]


@pytest.mark.parametrize("raw, line", [
    ("95 passed in 3.73s", "95 passed"),
    ("x\n363 passed, 5 deselected in 113.08s (0:01:53)\n", "363 passed, 5 deselected"),
    ("===== 2 failed, 3 passed in 1.2s =====", "2 failed, 3 passed"),
    ("check_imports: ok (91 files)", "check_imports: ok (91 files)"),
    ("", ""),
])
def test_tool_line_strips_pytest_wall_time(raw, line):
    assert tool_line(raw) == line


def test_tool_gate_rerun_never_collides(store):
    cfg = ResolvedConfig(repo_root=REPO, base={}, stages={})
    a = save_tool_gate(store, cfg, "S0", "G-S0", (GateCheck("t", True, "95 passed"),), [])
    assert save_tool_gate(store, cfg, "S0", "G-S0", (GateCheck("t", True, "95 passed"),), []) == a
    b = save_tool_gate(store, cfg, "S0", "G-S0", (GateCheck("t", True, "96 passed"),), [])
    assert b != a


def test_activation_ids_missing_run_is_empty_not_an_error(store):
    assert activation_ids(store, {"world": "cylinder", "condition": "O", "seed": 2718},
                          (0, 5000)) == {}


def test_nonfinite_analysis_value_is_stored_as_inconclusive(store):
    row = _row("delta_geom_same_last_symbol", math.nan, "geometry", status="ok")
    assert row.value is None and row.status == "inconclusive"
    store.save(MetricRecords(rows=(row, _row("u", 0.25))), config={"k": 1}, parents=[],
               seed_map={}, consumer="experiment")


def _timing_record(store, run_key, ckpt, wall):
    rows = (MetricRow(run_id="r", space="training", metric_id="captured", value=0.98),
            MetricRow(run_id="r", space="training", metric_id="tokens_per_second", value=2.2e4),
            MetricRow(run_id="r", space="training", metric_id="wall_time_s", value=wall),
            MetricRow(run_id="r", space="training", metric_id="dev_ce", value=3.1, checkpoint=0),
            MetricRow(run_id="r", space="training", metric_id="dev_ce", value=2.4,
                      checkpoint=5000))
    store.save(MetricRecords(rows=rows), config={"stage": "S3", "run_key": list(run_key),
                                                 "wall": wall},
               parents=[ckpt], seed_map={}, consumer="experiment")


def _ckpt(store, tag):
    return store.save(Checkpoint(run_id="r", step=5000, observation_id="obs", state=b"w"),
                      config={"tag": tag}, parents=[], seed_map={}, consumer="experiment")


def test_stored_timing_is_read_from_a_record_of_the_same_checkpoints(store, cfg):
    run_key = ("cylinder", "O", 1729)
    mine, other = _ckpt(store, "mine"), _ckpt(store, "other_training_config")
    _timing_record(store, run_key, other, 30.0)  # same run key, different training
    run = TrainingRun(cfg, store)
    assert run.stored_timing(run_key, [mine]) is None
    _timing_record(store, run_key, mine, 960.5)
    assert run.stored_timing(("square", "O", 1729), [mine]) is None
    assert run.stored_timing(run_key, [mine]) == {"wall_time_s": 960.5,
                                                  "tokens_per_second": 2.2e4,
                                                  "dev_ce_by_step": {0: 3.1, 5000: 2.4}}


def test_X07_prereg_refuses_to_overwrite(store, tmp_path):
    (tmp_path / "PREREGISTRATION.md").write_text("approved", encoding="utf-8")
    cfg = ResolvedConfig(repo_root=tmp_path, base={}, stages={})
    with pytest.raises(StageFailure) as exc:
        write_prereg(cfg, store)
    assert exc.value.code == ErrorCode.INVALID_CONFIG
    assert (tmp_path / "PREREGISTRATION.md").read_text(encoding="utf-8") == "approved"
