"""Author B: lineage, AUTH, H-1 records, ledger, pauses, archive, meter binding (§2.7, §7, §11)."""

from __future__ import annotations  # noqa: I001

import json
import math
import os
import sys
import tempfile
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_records as drec  # noqa: E402
import hwsd_score as ds  # noqa: E402
import hwsd_meter_bind as dm  # noqa: E402
import test_b_util as bu  # noqa: E402

import c1_chart  # noqa: E402
import controls  # noqa: E402
import hwsb_driver  # noqa: E402
import k4b_driver  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import op_guard  # noqa: E402
import pytest  # noqa: E402
import winjob  # noqa: E402

LIN, SEAL, LEDGER = "FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/SEALING", "FAIL_TECHNICAL/LEDGER"
A37 = dc.CONTRACT["authority"]["owner_addenda"]["37"]["sha256"]


def _recorded_store(tmp_path) -> Path:
    out = tmp_path / "hwsd-store"
    out.mkdir()
    k4b_driver.begin_stage(out, "KD")
    f = bu.write_json(out / "stages/KD/KD_RECORD.json", {"status": "PASS"})
    k4b_driver.complete_stage(out, "KD", [f])
    return out


def test_lineage_d(tmp_path, monkeypatch):
    trip = bu.tripwire(monkeypatch, ["hwsc_records.lineage_c"])
    assert drec.lineage_d(tmp_path / "absent")["status"] == "PASS"
    out = _recorded_store(tmp_path)
    for rel in ("AUTH_KD_0300.json", "SCHED_0300.json", "ACCEPT_SAMPLE.json", "KD_ACCEPT.json",
                "FREEZE.json", "DECISION_1.json", "REGISTRY_OBLIGATION.json",
                "REGISTRY_OBLIGATION_0300-a1.json", "logs/x.txt", "tmp/y.bin", "tmp-2/z.json",
                "operations/o.json", "reservations/RES-HWSD-W2-a1.json",
                "reservations/RES-HWSD-W2-a1.END.json"):
        bu.write_json(out / rel, {"r": rel})
    assert drec.lineage_d(out)["status"] == "PASS"
    stray = bu.write_json(out / "stages/KD/STRAY.json", {})
    with pytest.raises(bu.C1GateFailure) as e:
        drec.lineage_d(out)
    assert bu.status_of(e.value) == LIN
    stray.unlink()
    (out / "stages/KD/KD_RECORD.json").write_text("{}", encoding="utf-8")
    with pytest.raises(bu.C1GateFailure):
        drec.lineage_d(out)
    assert trip == []


@pytest.mark.parametrize("name", ["RES-HWSC-W2.json", "RES-HWSD-W2.json", "RES-HWSD-W2-a1.txt",
                                  "notes.json", "RES-HWSU-OF-a1.json"])
def test_lineage_d_foreign_reservation_name(tmp_path, name):
    out = _recorded_store(tmp_path)
    bu.write_json(out / "reservations" / name, {})
    with pytest.raises(bu.C1GateFailure) as e:
        drec.lineage_d(out)
    assert bu.status_of(e.value) == LIN


def test_archive_attempt_and_superseded_sums(tmp_path):
    out = _recorded_store(tmp_path)
    d = out / "stages/SCORE/620301/s0"
    d.mkdir(parents=True)
    led = c1_chart.ConstructionLedger(d / "CHART_CONSTRUCTIONS.json")
    led.claim(620301, "production")
    op_guard.write_marker(out, {"state": "active", "stage": "SCORE", "label": "chart 620301 production"})
    files = [d / "CHART_CONSTRUCTIONS.json", out / op_guard.MARKER]
    sup = drec.archive_attempt_d(out, "0300", 1, files)
    assert Path(sup) == out / "superseded" / "0300-a1" and (Path(sup) / "SHA256SUMS").exists()
    assert not (d / "CHART_CONSTRUCTIONS.json").exists()
    assert drec.lineage_d(out)["status"] == "PASS"
    w = ds.archived_wall(out, 620301, 0)
    assert w is not None and w["role"] == "production" and w["label"] == "chart 620301 production"
    assert ds.archived_wall(out, 620301, 50) is None and ds.archived_wall(out, 620302, 0) is None
    (Path(sup) / "OPERATION_ACTIVE.json").write_text(json.dumps({"state": "idle"}), encoding="utf-8")
    with pytest.raises(bu.C1GateFailure) as e:  # a file changed under superseded/
        drec.lineage_d(out)
    assert bu.status_of(e.value) == LIN
    assert ds.archived_wall(out, 620301, 0) is None  # marker not active


def test_archived_wall_record_and_newest_attempt(tmp_path):
    out = tmp_path / "hwsd-store"
    for k, roles, record in ((1, ["production"], False), (2, ["production", "direct"], False),
                             (3, ["production"], True)):
        a = out / "superseded" / f"0300-a{k}"
        (a / "stages/SCORE/620303/s100").mkdir(parents=True)
        led = c1_chart.ConstructionLedger(a / "stages/SCORE/620303/s100/CHART_CONSTRUCTIONS.json")
        for r in roles:
            led.claim(620303, r)
        bu.write_json(a / "OPERATION_ACTIVE.json", {"state": "active", "label": f"a{k}"})
        if record:
            bu.write_json(a / "stages/SCORE/620303/s100/CHECKPOINT_RECORD.json", {})
    assert ds.archived_wall(out, 620303, 100) is None  # newest (a3) holds a CHECKPOINT_RECORD
    import shutil

    shutil.rmtree(out / "superseded" / "0300-a3")
    assert ds.archived_wall(out, 620303, 100) == {"role": "direct", "label": "a2"}
    assert ds.archived_wall(tmp_path / "none", 620303, 100) is None


def test_auth_ok_d():
    freeze = {"run_approval_sha256": "f" * 64}
    good = {"job_id": "0300", "stages": ["KD", "SAMPLE"], "owner_auth_sha256": A37,
            "run_approval_sha256": "f" * 64, "stage_c_reads": []}
    assert drec.auth_ok_d(good, "KD", freeze)["ok"] is True
    assert drec.auth_ok_d(good, "SCORE", freeze)["ok"] is False
    assert drec.auth_ok_d(dict(good, owner_auth_sha256="0" * 64), "KD", freeze)["ok"] is False
    assert drec.auth_ok_d(dict(good, run_approval_sha256="e" * 64), "KD", freeze)["ok"] is False
    dry = dict(good, stages=["DRY"], run_approval_sha256=None)
    assert drec.auth_ok_d(dry, "DRY", None)["ok"] is True
    assert drec.auth_ok_d(None, "KD", freeze)["ok"] is False


@pytest.mark.parametrize("obj", [{"a": {"b": {"mean": 1}}}, [{"x": [{"L": 0.1}]}],
                                 ({"k": ({"captured": 0.9},)},), {"a": [{"b": {"max_B": "1"}}]},
                                 {"statuses": []}, {"x": {"sigma": "SUPPORT"}}])
def test_no_value_check_refuses(obj):
    with pytest.raises(bu.C1GateFailure) as e:
        drec.no_value_check(obj)
    assert bu.status_of(e.value) == SEAL


def test_no_value_check_passes_clean():
    assert drec.no_value_check({"counts": {"SCORED": 12}, "files_sha256": {"a": "b" * 64},
                                "cpu_s": 3.0, "nested": [{"job": "0300"}]}) is None


def _acc(**over):
    rec = {"job": "0300", "master": 620301, "attempt": 1,
           "counts": {"SCORED": 9, "SCORED_UNVALIDATED": 1, "CHART_UNAVAILABLE": 1, "UNCERTIFIED": 1},
           "fail_technical": None, "files_sha256": {"stages/SCORE/620301/s0/LEARN.json": "a" * 64},
           "cpu_s": 812.5, "protocol_sha256": dc.PROTOCOL_SHA256, "freeze_sha256": "b" * 64,
           "utc": bu.UTC}
    rec.update(over)
    return rec


def test_acceptance_check():
    assert set(_acc()) == set(dc.CONTRACT["records"]["SCORE_ACCEPTANCE"]["keys"])
    assert drec.acceptance_check(_acc()) is None
    assert drec.acceptance_check(_acc(fail_technical="FAIL_TECHNICAL/NUMERICAL")) is None
    bad = [_acc(extra=1), {k: v for k, v in _acc().items() if k != "utc"},
           _acc(statuses=["SCORED"] * 12),
           _acc(counts={"SCORED": 12, "SCORED_UNVALIDATED": 1, "CHART_UNAVAILABLE": 0, "UNCERTIFIED": 0}),
           _acc(counts={"SCORED": 12, "SCORED_UNVALIDATED": 0, "CHART_UNAVAILABLE": 0}),
           _acc(counts={"SCORED": 12, "SCORED_UNVALIDATED": 0, "CHART_UNAVAILABLE": 0,
                        "UNCERTIFIED": 0, "EXTRA": 0}),
           _acc(counts={"SCORED": 12.0, "SCORED_UNVALIDATED": 0, "CHART_UNAVAILABLE": 0, "UNCERTIFIED": 0}),
           _acc(fail_technical="INCONCLUSIVE/HEADROOM"),
           _acc(files_sha256={"a": "XYZ"}), _acc(files_sha256={"a": {"mean": 1}}),
           _acc(job={"L": 0.1})]
    for rec in bad:
        with pytest.raises(bu.C1GateFailure) as e:
            drec.acceptance_check(rec)
        assert bu.status_of(e.value) == SEAL, rec


def test_score_acceptance_record(tmp_path):
    out = tmp_path / "hwsd-store"
    j = 620301
    for step in (0, 50):
        bu.write_json(out / f"stages/SCORE/{j}/s{step}/LEARN.json", {"captured": 0.5})
        bu.write_json(out / f"stages/SCORE/{j}/s{step}/CHECKPOINT_RECORD.json", {"L": 0.1})
    bu.write_json(out / f"stages/SCORE/{j}/SCORE_IDENT.json", {"ok": True})
    st = ["SCORED"] * 6 + ["SCORED_UNVALIDATED"] * 3 + ["CHART_UNAVAILABLE"] * 2 + ["UNCERTIFIED"]
    records = [{"status": s, "label": s, "L": 0.01, "U": 0.02, "valid": True} for s in st]
    rec = ds.acceptance(out, j, "0301", 1, records, 812.5, "c" * 64)
    path = out / f"stages/SCORE/{j}/ACCEPTANCE.json"
    assert json.loads(path.read_text(encoding="utf-8")) == json.loads(json.dumps(rec))
    assert set(rec) == set(dc.CONTRACT["records"]["SCORE_ACCEPTANCE"]["keys"])
    assert rec["counts"] == {"SCORED": 6, "SCORED_UNVALIDATED": 3, "CHART_UNAVAILABLE": 2,
                             "UNCERTIFIED": 1}
    assert rec["master"] == j and rec["job"] == "0301" and rec["attempt"] == 1
    assert rec["fail_technical"] is None and rec["freeze_sha256"] == "c" * 64
    assert rec["protocol_sha256"] == dc.PROTOCOL_SHA256
    files = {p.relative_to(out).as_posix(): bu.sha(p) for p in (out / f"stages/SCORE/{j}").rglob("*")
             if p.is_file() and p.name != "ACCEPTANCE.json"}
    got = {k.replace("\\", "/"): v for k, v in rec["files_sha256"].items()}
    assert {k.split(f"stages/SCORE/{j}/")[-1]: v for k, v in got.items()} == \
        {k.split(f"stages/SCORE/{j}/")[-1]: v for k, v in files.items()}
    drec.acceptance_check(rec)
    with pytest.raises(FileExistsError):
        ds.acceptance(out, j, "0301", 1, records, 812.5, "c" * 64)


def test_ledger(tmp_path):
    p = tmp_path / "HWSD_CPU_LEDGER.json"
    led = drec.ledger_init(p)
    assert led == {"study": "hwsd-v1", "entries": [], "cumulative_cpu_s": 0.0}
    assert json.loads(p.read_text(encoding="utf-8")) == led
    assert drec.ledger_init(p)["study"] == "hwsd-v1"
    drec.ledger_append_d(p, "0300-KD-a1", "0300", "KD", 400.0, "meter")
    r = drec.ledger_append_d(p, "0301-SCORE-620301-a1", "0301", "SCORE", 800.5, "meter", master=620301)
    assert math.isclose(r["cumulative_cpu_s"], 1200.5)
    on = json.loads(p.read_text(encoding="utf-8"))
    assert [e["label"] for e in on["entries"]] == ["0300-KD-a1", "0301-SCORE-620301-a1"]
    assert set(on["entries"][1]) == set(dc.CONTRACT["records"]["ledger_entry"])
    with pytest.raises(bu.C1GateFailure) as e:
        drec.ledger_append_d(p, "0300-KD-a1", "0300", "KD", 1.0, "meter")
    assert bu.status_of(e.value) == LEDGER
    with pytest.raises(ValueError):
        drec.ledger_append_d(p, "x-a1", "0300", "E2", 1.0, "meter")
    other = bu.write_json(tmp_path / "other.json", {"study": "hwsc-v1", "entries": [],
                                                    "cumulative_cpu_s": 0.0})
    with pytest.raises(bu.C1GateFailure) as e:
        drec.ledger_init(other)
    assert bu.status_of(e.value) == LEDGER


def test_centrals():
    for st, c, cum in (("J-D1", 700, 700), ("DRY", 250, 950), ("KD", 450, 5200),
                       ("SAMPLE", 1350, 7000), ("SCORE", 2400, 9400), ("SUMMARY", 350, 9750)):
        assert drec.central_d(st) == c and drec.cumulative_d(st) == cum
    for fn in (drec.central_d, drec.cumulative_d):
        with pytest.raises(ValueError):
            fn("E2")


def test_pause_check_d(monkeypatch):
    bu.tripwire(monkeypatch, ["hwsc_records.pause_check_c", "hwsb_driver.pause_check"])
    r = drec.pause_check_d("SCORE", 7200.0, 28200.0, 2400.0)
    assert r["pause"] is False and r["trigger"] is None
    assert (r["stage_threshold"], r["cum_threshold"], r["model_threshold"]) == (7200, 28200, 2400)
    assert drec.pause_check_d("SCORE", 7200.001, 0.0, 0.0)["trigger"] == "STAGE"
    assert drec.pause_check_d("SCORE", 0.0, 28200.01, 0.0)["trigger"] == "CUMULATIVE"
    assert drec.pause_check_d("SCORE", 0.0, 0.0, 2400.01)["trigger"] == "MODEL"
    assert drec.pause_check_d("SCORE", 9e9, 9e9, 9e9)["trigger"] == "STAGE+CUMULATIVE+MODEL"
    k = drec.pause_check_d("KD", 1350.0, 15600.0, 9e9)
    assert k["pause"] is False and k["stage_threshold"] == 1350 and k["cum_threshold"] == 15600
    assert drec.pause_check_d("KD", 1350.5, 0.0)["pause"] is True


def test_pause_or_raise_d(tmp_path, monkeypatch):
    out = tmp_path / "hwsd-store"
    out.mkdir()
    called = []
    monkeypatch.setattr(hwsb_driver, "running_cpu", lambda *a, **k: called.append(1) or (9e9, 9e9))
    assert drec.pause_or_raise_d(out, "KD", 0.0, ledger_path=None) is None
    assert called == [] and not (out / "GATES.jsonl").exists()
    cont = bu.write_json(tmp_path / "cont.json", {"stages": ["KD"]})
    assert drec.pause_or_raise_d(out, "KD", 0.0, ledger_path=tmp_path / "L.json", cont=cont) is None
    with pytest.raises(hwsb_driver.Paused):
        drec.pause_or_raise_d(out, "KD", 0.0, ledger_path=tmp_path / "L.json")
    gates = [json.loads(x) for x in (out / "GATES.jsonl").read_text(encoding="utf-8").splitlines()]
    g = [x for x in gates if x["gate"] == "PAUSE_KD"]
    assert len(g) == 1 and g[0]["status"] == "PAUSE"
    drec.no_value_check(g[0])
    assert {"stage_cpu", "cum_cpu", "stage_threshold", "cum_threshold"} <= set(g[0])
    events = [json.loads(x) for x in (out / "STAGES.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(e.get("event") == "PAUSE" for e in events)
    monkeypatch.setattr(hwsb_driver, "running_cpu", lambda *a, **k: (1.0, 1.0))
    assert drec.pause_or_raise_d(out, "KD", 0.0, ledger_path=tmp_path / "L.json") is None


def test_run_close_writes_its_obligation(tmp_path):
    import hwsd_driver as ddr
    import hwsd_readers as drd

    out = _recorded_store(tmp_path)
    (out / "GATES.jsonl").write_text(json.dumps({"gate": "H1D", "status": "FAIL_TECHNICAL/IDENTITY",
                                                 "utc": bu.UTC}) + "\n", encoding="utf-8")
    ddr.run_close(out, "FAIL_TECHNICAL/IDENTITY", "planted", "0300", 2)
    close = json.loads((out / "stages/CLOSE/CLOSE.json").read_text(encoding="utf-8"))
    assert "outcome" in close and close.get("reason") == "planted"
    drec.no_value_check(close)
    assert (out / "REGISTRY_OBLIGATION_0300-a2.json").exists()
    assert drd.obligation_check(out)["status"] == "PASS"
    assert drec.lineage_d(out)["status"] == "PASS"


# ------------------------------------------------------------------------- meter

METER_ATTRS = ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S", "STOP_NEW_S",
               "OUTPUT_CAP", "WORKER_SESSION", "limit_reason")


@pytest.fixture
def meter_state(monkeypatch):
    for mod, names in ((meter, METER_ATTRS), (winjob, ("MEMORY_CAP",)),
                       (controls, ("JOB_ID", "TASK_SHA256")), (k4b_meter_bind, ("TEMP_ROOT",))):
        for n in names:
            if hasattr(mod, n):
                monkeypatch.setattr(mod, n, getattr(mod, n))
    for k in ("TEMP", "TMP", "TMPDIR"):
        monkeypatch.setenv(k, os.environ.get(k, tempfile.gettempdir()))


@pytest.mark.parametrize("stage,gib", [("J-D1", 8), ("DRY", 12), ("KD", 12), ("SAMPLE", 12),
                                       ("SCORE", 8), ("SUMMARY", 8)])
def test_bind_per_stage(tmp_path, meter_state, stage, gib):
    assert dm.memory_cap(stage) == gib * bu.GIB
    winjob.MEMORY_CAP = 1
    dm.bind("0197", "ab" * 32, tmp_path, "session-b", stage)
    assert winjob.MEMORY_CAP == gib * bu.GIB
    assert meter.OUTPUT_CAP == 8 * bu.GIB == dc.CONTRACT["resources"]["output_cap_bytes"]
    assert meter.CAP_S == math.inf and meter.STOP_NEW_S == math.inf
    assert Path(k4b_meter_bind.TEMP_ROOT) == tmp_path and Path(meter.OUT) == tmp_path
    eff = dm.effective_settings()
    assert set(eff) >= {"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"}
    assert eff["memory_cap"] == gib * bu.GIB and eff["output_cap"] == 8 * bu.GIB


def test_bind_unknown_stage_and_temp_root(tmp_path, meter_state):
    with pytest.raises(ValueError):
        dm.memory_cap("E2")
    dm.bind("0197", "ab" * 32, tmp_path, "s", "DRY", temp_root=tmp_path / "tr")
    assert Path(k4b_meter_bind.TEMP_ROOT) == tmp_path / "tr"
    env = dm.child_env_d("0197")
    assert env["TEMP"] == env["TMP"] == env["TMPDIR"]
    assert bu.under(env["TEMP"], tmp_path / "tr") and Path(env["TEMP"]).is_dir()
    assert all(env[v] == "1" for v in meter.THREAD_VARS)
    argv = k4b_meter_bind.rewrite_argv(["--max-cpu", "600", "x.py", "--max-wall", "9"])
    assert argv[-4:] == ["--max-cpu", "inf", "--max-wall", "inf"] and argv.count("--max-cpu") == 1


def test_job_paths_and_placement():
    t = dm.job_paths("0197", "test")
    assert Path(t["out"]) == dc.SCRATCH / "test_hwsd-0197" and Path(t["temp_root"]) == Path(t["out"])
    assert Path(t["basetemp"]) == dc.SCRATCH / "test_hwsd-0197" / "pytest"
    s = dm.job_paths("0300", "store")
    assert Path(s["out"]) == dc.STORE and Path(s["temp_root"]) == dc.STORE / "tmp" and s["basetemp"] is None
    with pytest.raises(ValueError):
        dm.job_paths("0197", "dry")
    r = dm.placement_ok(t)  # the hwsc_meter_bind.placement_ok shape {"ok", "checks"}
    assert r["ok"] is True
    for k in ("out_outside_root", "temp_outside_root", "basetemp_outside_root", "test_prefixed"):
        assert r["checks"][k] is True, k
    bad = dm.placement_ok(dict(t, out=dc.ROOT / "test_hwsd-0197", basetemp=dc.ROOT / "x" / "pytest"))
    assert bad["ok"] is False
    assert bad["checks"]["out_outside_root"] is False and bad["checks"]["basetemp_outside_root"] is False
    wrong = dm.placement_ok(dict(t, out=dc.SCRATCH / "hwsd-0197", temp_root=dc.SCRATCH / "hwsd-0197"))
    assert wrong["ok"] is False and wrong["checks"]["test_prefixed"] is False
    so = dm.placement_ok(s)
    assert so["ok"] is True
    assert so["checks"]["out_is_store"] is True and so["checks"]["temp_under_store_tmp"] is True
    assert dm.placement_ok(dict(s, temp_root=dc.STORE / "elsewhere"))["ok"] is False


def test_this_suite_runs_outside_the_project(tmp_path):
    assert not bu.under(tmp_path, dc.ROOT)
    assert bu.under(tmp_path, dc.SCRATCH)
    assert not bu.under(tempfile.gettempdir(), dc.ROOT)


@pytest.mark.parametrize("argv", [["--job", "0197", "--task-sha256", "ab" * 32, "--session", "s",
                                   "--kind", "test"],
                                  ["--job", "0197", "--task-sha256", "ab" * 32, "--session", "s",
                                   "--kind", "test", "--stage", "BOGUS"],
                                  ["--job", "0197", "--task-sha256", "ab" * 32, "--session", "s",
                                   "--kind", "elsewhere", "--stage", "DRY"]])
def test_meter_main_refuses_bad_arguments(monkeypatch, meter_state, argv):
    monkeypatch.setattr(sys, "argv", ["hwsd_meter_bind"] + argv + ["--", "python", "-c", "pass"])
    assert dm.main() == 2
