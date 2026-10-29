"""Coordinator-written regression tests for defects D-0187-1 and D-0187-2 (API.md §27).

D-0187-1: run_e1 verifies release A inside the stage-C binding, so a release carrying the stage-C
protocol sha256 passes (unbound, k4b_release.verify_release compared it with K4b's own protocol).
D-0187-2: the E1 and E2 gate files (G0C.json, H1C.json, L1.json; H1C_E2.json) are recorded in a
STAGE_COMPLETE, so lineage_c passes after the stage. Preflight, the gates and the E2 context are
stubbed; the store is a tmp_path store."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402
import hwsc_driver as cdr  # noqa: E402
import hwsc_jobs  # noqa: E402
import stage_records  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

SESSION, TASK = "sess-0187", "AB" * 32


def _store(tmp_path, monkeypatch):
    out = tmp_path / "hwsc-store"
    out.mkdir()
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cdr, "preflight", lambda *a, **k: {"refused": False})
    monkeypatch.setattr(cdr, "_audit_gate", lambda out: None)
    monkeypatch.setattr(cc, "load_handoff", lambda: {})
    return out


def _release(out, protocol):
    rel = {"kind": "A", "job_id": "0190", "task_sha256": TASK, "worker_session": SESSION,
           "protocol_sha256": protocol, "freeze_sha256": stage_records.sha256(out / "FREEZE.json"),
           "reservation": cc.RESERVATION_ID}
    p = out / "RELEASE_A.json"
    p.write_text(json.dumps(rel), encoding="utf-8")
    return p


def _gate_writing(out, name):
    def run():
        p = Path(out) / "stages" / "E1" / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{}", encoding="utf-8")
        return {}
    return (name, run)


def test_run_e1_accepts_a_stage_c_release_and_records_its_gate_files(tmp_path, monkeypatch):
    out = _store(tmp_path, monkeypatch)
    rel = _release(out, cc.PROTOCOL_SHA256)
    monkeypatch.setattr(cdr, "e1_steps", lambda out, ctx, *a: [
        _gate_writing(out, n) for n in ("G0C", "H1C", "L1")])
    res = cdr.run_e1(out, {}, {}, rel, SESSION, TASK)
    assert res["status"] == "PASS", res
    assert cdr.lineage_c(out)["status"] == "PASS"


def test_run_e1_still_refuses_a_k4b_protocol_release(tmp_path, monkeypatch):
    out = _store(tmp_path, monkeypatch)
    import k4b_config

    rel = _release(out, k4b_config.CONTRACT["protocol_sha256"])  # unbound: K4b's own protocol
    monkeypatch.setattr(cdr, "e1_steps", lambda *a: [])
    try:
        cdr.run_e1(out, {}, {}, rel, SESSION, TASK)
    except C1GateFailure as exc:
        assert "protocol_sha256" in str(exc)
    else:
        raise AssertionError("a release with K4b's protocol sha256 was accepted")


def test_run_e2_records_h1c_e2(tmp_path, monkeypatch):
    out = _store(tmp_path, monkeypatch)
    monkeypatch.setattr(hwsc_jobs, "preflight", lambda *a, **k: {"refused": False})
    monkeypatch.setattr(cdr, "_audit_gate", lambda out: None)
    monkeypatch.setattr(hwsc_jobs.k4b_fresh, "require_release_b",
                        lambda out, path, session: {"N": 3072, "k": 1})

    def ctx(out, rel, handoff, dry=False):
        p = Path(out) / "stages" / "E2" / "H1C_E2.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{}", encoding="utf-8")
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "stub stops after H1C_E2.json")

    monkeypatch.setattr(hwsc_jobs, "e2_context", ctx)
    hwsc_jobs.run_e2(out, {}, {}, out / "RELEASE_B.json", SESSION)
    done = [e for e in stage_records.stages_so_far(out) if e.get("stage") == "E2_GATES"]
    assert done and "stages/E2/H1C_E2.json" in done[0]["files"]
