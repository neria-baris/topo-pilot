"""Author B (job 0198): the gate runner, status mapping, stage events, lineage, the study ledger
and pauses (protocol §4.1, §6 convention, §10.2-§10.3; API §5.1-§5.2). TEST_PLAN §3 row
test_b_of_records (the freeze and OF-B parts are in test_b_of_freeze.py). tmp_path only."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
import oracle_profile  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402
from topo_pilot.contracts import ErrorCode, StageFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))


def _lines(p) -> list:
    p = Path(p)
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x] if p.exists() else []


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ status_of (API §5.1)
def test_status_of_mapping():
    assert ur.status_of(C1GateFailure("INCONCLUSIVE/AUTHORITY", "x")) == "INCONCLUSIVE/AUTHORITY"
    assert ur.status_of(C1GateFailure("FAIL_TECHNICAL/ORACLE")) == "FAIL_TECHNICAL/ORACLE"
    assert ur.status_of(ur.Paused("cpu")) == "PAUSE"
    assert ur.status_of(oracle_profile.ProfileError("p")) == "FAIL_TECHNICAL/IDENTITY"
    sf = StageFailure(ErrorCode.INVALID_CONFIG, "dataset.checks", "n_too_large", "1")
    assert ur.status_of(sf) == "FAIL_TECHNICAL/SAMPLER"
    assert ur.status_of(ValueError("v")) == "FAIL_TECHNICAL/UNEXPECTED"
    assert ur.status_of(KeyError("k")) == "FAIL_TECHNICAL/UNEXPECTED"
    assert ur.status_of(C1GateFailure("FAIL_TECHNICAL")) == "FAIL_TECHNICAL/UNEXPECTED"


# ------------------------------------------------------------------ run_gates_u (API §5.1)
def _steps(calls, spec):
    def mk(gate, act):
        def fn():
            calls.append(gate)
            if isinstance(act, BaseException):
                raise act
            return act
        return gate, fn
    return [mk(g, a) for g, a in spec]


def test_run_gates_stops_after_failure(tmp_path):
    calls = []
    steps = _steps(calls, [("A", {"x": 1}), ("B", C1GateFailure("FAIL_TECHNICAL/ORACLE", "bad")),
                           ("C", {"y": 2}), ("D", None)])
    recs = ur.run_gates_u(tmp_path, steps)
    assert calls == ["A", "B"]
    assert [(r["gate"], r["status"]) for r in recs] == [
        ("A", "PASS"), ("B", "FAIL_TECHNICAL/ORACLE"), ("C", "NOT_RUN"), ("D", "NOT_RUN")]
    assert recs[0]["x"] == 1 and recs[1]["reason"] == "bad"
    g = _lines(tmp_path / "GATES.jsonl")
    assert [(x["gate"], x["status"]) for x in g] == [(r["gate"], r["status"]) for r in recs]
    assert g[0]["x"] == 1 and g[1]["reason"] == "bad"


def test_run_gates_share_dropped_continues(tmp_path):
    calls = []
    steps = _steps(calls, [("OF-3", {"status": "SHARE_DROPPED", "share_outcome": "I"}),
                           ("OF-4", {"status": "SHARE_DROPPED"}), ("OF-5", {})])
    recs = ur.run_gates_u(tmp_path, steps)
    assert calls == ["OF-3", "OF-4", "OF-5"]
    assert [r["status"] for r in recs] == ["SHARE_DROPPED", "SHARE_DROPPED", "PASS"]
    assert "status" not in {k for k in recs[0] if k not in ("gate", "status")}


def test_run_gates_inconclusive_stops(tmp_path):
    calls = []
    steps = _steps(calls, [("A", {"status": "INCONCLUSIVE/ORACLE_FEASIBILITY"}), ("B", {})])
    recs = ur.run_gates_u(tmp_path, steps)
    assert calls == ["A"] and recs[1]["status"] == "NOT_RUN"


def test_run_gates_dry_continue_calls_every_fn(tmp_path):
    calls = []
    steps = _steps(calls, [("A", C1GateFailure("FAIL_TECHNICAL/SAMPLER")), ("B", {}),
                           ("C", ValueError("v"))])
    recs = ur.run_gates_u(tmp_path, steps, dry_continue=True)
    assert calls == ["A", "B", "C"]
    assert [r["status"] for r in recs] == ["FAIL_TECHNICAL/SAMPLER", "PASS",
                                           "FAIL_TECHNICAL/UNEXPECTED"]


def test_run_gates_pause_recorded_then_reraised(tmp_path):
    calls = []
    steps = _steps(calls, [("A", {}), ("B", ur.Paused("cpu")), ("C", {})])
    with pytest.raises(ur.Paused):
        ur.run_gates_u(tmp_path, steps)
    assert calls == ["A", "B"]
    g = _lines(tmp_path / "GATES.jsonl")
    assert [(x["gate"], x["status"]) for x in g] == [("A", "PASS"), ("B", "PAUSE")]


def test_run_gates_details_json_safe_and_reason_capped(tmp_path):
    calls = []
    steps = _steps(calls, [("A", {"p": Path("x/y"), "f": Fraction(1, 3), "a": np.float64(1.5),
                                  "t": (1, 2)}),
                           ("B", C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "r" * 5000))])
    recs = ur.run_gates_u(tmp_path, steps)
    json.dumps(recs)  # JSON-safe
    assert recs[0]["f"] == "1/3" and recs[0]["a"] == 1.5 and recs[0]["t"] == [1, 2]
    assert recs[0]["p"] == str(Path("x/y"))
    assert len(recs[1]["reason"]) == 2000
    assert _lines(tmp_path / "GATES.jsonl")[0]["f"] == "1/3"


def test_contract_gate_order_and_continuing():
    g = C["gates_of"]
    assert g["order"] == ["OF-B", "OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2",
                          "OF-3", "OF-4", "OF-5"]
    assert g["continuing_statuses"] == ["PASS", "SHARE_DROPPED"]
    assert g["exit_codes"] == {"0": "OF_PASS or OF_PASS_RESPONSE_ONLY",
                               "2": "refused (nothing sampled)", "3": "FAIL_TECHNICAL",
                               "4": "PAUSE", "5": "INCONCLUSIVE"}


# ------------------------------------------------------------------ stage events (API §5.1)
def test_begin_and_complete_stage(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    ur.begin_stage(out, "OF_S")
    marker = json.loads((out / "OPERATION_ACTIVE.json").read_text(encoding="utf-8"))
    assert marker == {"state": "idle", "stage": "OF_S", "label": "stage OF_S", "seq": 0}
    f1 = Path(ur.save_array(out, "stages/OF/ORACLE_a.npz", x=np.arange(3)))
    f2 = out / "stages" / "OF" / "G0_OF.json"
    f2.write_text("{}", encoding="utf-8")
    ev = ur.complete_stage(out, "OF_S", [f1, f2])
    lines = _lines(out / "STAGES.jsonl")
    assert [(x["stage"], x["event"]) for x in lines] == [("OF_S", "BEGIN"), ("OF_S", "STAGE_COMPLETE")]
    assert set(lines[0]) == {"stage", "event", "utc"}
    want = {"stages/OF/ORACLE_a.npz": _sha(f1), "stages/OF/G0_OF.json": _sha(f2)}
    assert lines[1]["files"] == want and ev["files"] == want
    raw = (out / "STAGES.jsonl").read_text(encoding="utf-8").splitlines()[1]
    assert raw == json.dumps(json.loads(raw), sort_keys=True)  # sort_keys


# ------------------------------------------------------------------ lineage_u (API §5.1)
def _store(tmp_path):
    out = tmp_path / "hwsu-store"
    out.mkdir()
    ur.begin_stage(out, "OF")
    f = Path(ur.save_array(out, "stages/OF/ORACLE_OF_eval.npz", G=np.arange(4.0)))
    ur.complete_stage(out, "OF", [f])
    return out, f


def test_lineage_absent_and_recorded(tmp_path):
    assert ur.lineage_u(tmp_path / "absent")["status"] == "PASS"
    out, f = _store(tmp_path)
    r = ur.lineage_u(out)
    assert r["status"] == "PASS" and r["n_recorded"] == 1


EXEMPT = ["FREEZE_OF.json", "FREEZE.json", "RESERVATION_OF.json", "RESERVATION_OF-a2.json",
          "REGISTRY_OBLIGATION_OF.json", "REGISTRY_OBLIGATION_OF-a1.json", "AUTH_OF_0300.json",
          "SCHED_x.json", "ACCEPT_x.json", "OF_ACCEPT.json", "DECISION_x.json", "RELEASE_x.json",
          "GATES.jsonl", "STAGES.jsonl", "cpu_ledger.json", "cpu_ledger.emergency.jsonl",
          "RUN.lock", "METER_ACTIVE.lock", "OPERATION_ACTIVE.json", "OPERATIONS.jsonl",
          "reservations/RES-HWSU-OF.END.json", "logs/run.log", "operations/KILLED_1.json",
          "tmp/x.bin", "tmp-0300/y.txt"]


def test_lineage_exemptions(tmp_path):
    out, f = _store(tmp_path)
    for rel in EXEMPT:
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_bytes(b"x")
    assert ur.lineage_u(out)["status"] == "PASS"


@pytest.mark.parametrize("rel", ["stages/OF/ORACLE_x.npz", "stages/OF/OF_REPORT.json", "NOTES.json",
                                 "reservations/sub/x.json", "stages/OF/HIST_OF_fit_b0.npz"])
def test_lineage_unrecorded_file(tmp_path, rel):
    out, f = _store(tmp_path)
    p = out / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"unrecorded")
    with pytest.raises(C1GateFailure) as ei:
        ur.lineage_u(out)
    assert ei.value.status == "FAIL_TECHNICAL/LINEAGE"


def test_lineage_changed_recorded_file(tmp_path):
    out, f = _store(tmp_path)
    f.write_bytes(f.read_bytes() + b"\0")
    with pytest.raises(C1GateFailure) as ei:
        ur.lineage_u(out)
    assert ei.value.status == "FAIL_TECHNICAL/LINEAGE"


def test_lineage_superseded(tmp_path):
    out, f = _store(tmp_path)
    job = out / "superseded" / "0299"
    job.mkdir(parents=True)
    (job / "a.json").write_bytes(b"old")
    (job / "SHA256SUMS").write_text(f"{_sha(job / 'a.json')}  a.json\n", encoding="utf-8")
    assert ur.lineage_u(out)["status"] == "PASS"
    (job / "b.json").write_bytes(b"unlisted")
    with pytest.raises(C1GateFailure) as ei:
        ur.lineage_u(out)
    assert ei.value.status == "FAIL_TECHNICAL/LINEAGE"


# ------------------------------------------------------------------ ledger (API §5.2; §10.3)
def test_central_and_cumulative():
    assert [ur.central(s) for s in ("J-OF", "DRO", "OF")] == [900, 200, 700]
    assert [ur.cumulative_central(s) for s in ("J-OF", "DRO", "OF")] == [900, 1100, 1800]
    for fn in (ur.central, ur.cumulative_central):
        with pytest.raises(ValueError):
            fn("E1")
    c = json.loads(json.dumps(uc.CONTRACT))
    c["cpu"]["central_s"]["DRO"] = 300
    assert ur.central("DRO", contract=c) == 300 and ur.cumulative_central("OF", contract=c) == 1900


def test_ledger_read_absent(tmp_path):
    assert ur.ledger_read(tmp_path / "L.json") == {"study": "hwsu-v1", "entries": [],
                                                   "cumulative_cpu_s": 0.0}


def test_ledger_append_unique_atomic(tmp_path, monkeypatch):
    path = tmp_path / "HWSU_CPU_LEDGER.json"
    replaced = []
    real = os.replace
    monkeypatch.setattr(os, "replace", lambda a, b: (replaced.append((str(a), str(b))), real(a, b))[1])
    ur.ledger_append(path, "J-OF-0198-a1", "0198", "J-OF", 400.5, "meter")
    d = ur.ledger_append(path, "DRO-0199-a1", "0199", "DRO", 99.5, "meter")
    assert d["cumulative_cpu_s"] == 500.0
    disk = json.loads(path.read_text(encoding="utf-8"))
    assert disk["cumulative_cpu_s"] == 500.0 and len(disk["entries"]) == 2
    e = disk["entries"][0]
    assert set(e) == {"label", "job", "stage", "cpu_s", "source", "utc"}
    assert (e["label"], e["job"], e["stage"], e["cpu_s"], e["source"]) == (
        "J-OF-0198-a1", "0198", "J-OF", 400.5, "meter")
    assert len(replaced) == 2 and all(a.endswith(".json.tmp") and Path(b) == path
                                      for a, b in replaced)
    before = path.read_bytes()
    with pytest.raises(C1GateFailure) as ei:
        ur.ledger_append(path, "J-OF-0198-a1", "0198", "J-OF", 1.0, "meter")
    assert ei.value.status == "FAIL_TECHNICAL/LEDGER" and path.read_bytes() == before
    assert not path.with_suffix(".json.tmp").exists()


@pytest.mark.parametrize("stage,s_th,c_th", [("J-OF", 2700, 2700), ("DRO", 600, 3300),
                                             ("OF", 2100, 5400)])
def test_pause_check_thresholds_strict(stage, s_th, c_th):
    r = ur.pause_check_u(stage, s_th, c_th)
    assert r["pause"] is False and r["trigger"] is None
    assert (r["stage_threshold"], r["cum_threshold"]) == (s_th, c_th)
    assert ur.pause_check_u(stage, s_th + 0.001, 0)["trigger"] == "STAGE"
    assert ur.pause_check_u(stage, 0, c_th + 0.001)["trigger"] == "CUMULATIVE"
    r = ur.pause_check_u(stage, s_th + 1, c_th + 1)
    assert r["pause"] is True and r["trigger"] == "BOTH"


def test_running_cpu(tmp_path):
    path = tmp_path / "L.json"
    ur.ledger_append(path, "OF-1-a1", "1", "OF", 100.0, "m")
    ur.ledger_append(path, "DRO-1-a1", "1", "DRO", 50.0, "m")
    s, c = ur.running_cpu("OF", path, time.process_time())
    assert 100.0 <= s < 101.0 and 150.0 <= c < 151.0


def test_pause_or_raise_disabled_without_ledger(tmp_path):
    assert ur.pause_or_raise_u(tmp_path, "OF", time.process_time(), ledger_path=None) is None
    assert not (tmp_path / "GATES.jsonl").exists() and not (tmp_path / "STAGES.jsonl").exists()


def test_pause_or_raise_records_cpu_fields_only(tmp_path):
    path = tmp_path / "L.json"
    ur.ledger_append(path, "OF-1-a1", "1", "OF", 3000.0, "m")
    out = tmp_path / "store"
    out.mkdir()
    assert ur.pause_or_raise_u(out, "DRO", time.process_time(), ledger_path=path) is None
    with pytest.raises(ur.Paused):
        ur.pause_or_raise_u(out, "OF", time.process_time(), ledger_path=path)
    ev = _lines(out / "STAGES.jsonl")
    assert [(x["stage"], x["event"]) for x in ev] == [("OF", "PAUSE")]
    g = _lines(out / "GATES.jsonl")
    assert len(g) == 1 and g[0]["gate"] == "PAUSE_OF" and g[0]["status"] == "PAUSE"
    allowed = {"gate", "status", "criterion_met", "utc", "pause", "trigger", "stage_cpu",
               "stage_threshold", "cum_cpu", "cum_threshold"}
    assert set(g[0]) <= allowed and {"stage_cpu", "cum_cpu"} <= set(g[0])
