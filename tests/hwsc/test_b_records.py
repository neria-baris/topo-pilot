"""Author B (job 0176): records, the gate runner, lineage, authority records, the study ledger,
pauses, the D6 export (RESULT.json and SEALED_OPENED.json) and the HANDOFF reader.

Written from PROTOCOL_HWSC_v1.md sections 5, 6.4, 8, 9, API.md sections 1.2, 7, 12-14, CONTRACT.json
`handoff`, `records`, `cpu`, `licences`, `disclosure` and TEST_PLAN.md section 3 only (DRC10, DRC12).
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402
import hwsc_bind as cb  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import hwsc_driver as cdr  # noqa: E402
import c1_records  # noqa: E402
import errors  # noqa: E402
import hwsb_config  # noqa: E402
import hwsb_driver  # noqa: E402
import hws_worlds  # noqa: E402
import k4b_driver  # noqa: E402
import k4b_release  # noqa: E402
import k4b_stats  # noqa: E402
import stage_records  # noqa: E402
from topo_pilot.contracts import ErrorCode, StageFailure  # noqa: E402

C = cc.CONTRACT
GF = c1_records.C1GateFailure


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _events(out):
    p = Path(out) / "STAGES.jsonl"
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def _gates(out):
    return stage_records.gates_so_far(Path(out))


# ---------------------------------------------------------------- status_of
def _sf(code):
    return StageFailure(code, "test", "planted", "planted detail")


@pytest.mark.parametrize("exc,status", [
    (GF("INCONCLUSIVE/HEADROOM", "r"), "INCONCLUSIVE/HEADROOM"),
    (GF("FAIL_TECHNICAL/ORACLE", "r"), "FAIL_TECHNICAL/ORACLE"),
    (hwsb_config.HwsbStop("FAIL_TECHNICAL/HOLD", "r"), "FAIL_TECHNICAL/HOLD"),
    (hwsb_config.HwsbStop("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "r"),
     "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"),
    (hws_worlds.HwsStop("FAIL_TECHNICAL/IDENTITY", "r"), "FAIL_TECHNICAL/IDENTITY"),
    (_sf(ErrorCode.NONFINITE_LOSS), "FAIL_TECHNICAL/NONFINITE"),
    (_sf(ErrorCode.SPLIT_OVERLAP), "FAIL_TECHNICAL/LINEAGE"),
    (hwsb_driver.Paused("KC: STAGE"), "PAUSE"),
    (RuntimeError("bare"), "FAIL_TECHNICAL/UNEXPECTED"),
])
def test_status_of(exc, status):
    assert cdr.status_of(exc) == status


def test_status_of_other_exceptions_follow_classify_exception():
    for exc in (errors.Invalid("planted"), KeyError("k"), ValueError("v")):
        want = c1_records.classify_exception(exc)[0]
        want = want if "/" in want else want + "/UNEXPECTED"
        assert cdr.status_of(exc) == want and "/" in cdr.status_of(exc)


# ---------------------------------------------------------------- run_gates_c
def _steps(calls, mid):
    def a():
        calls.append("A")
        return {"status": "PASS", "x": 1}

    def b():
        calls.append("B")
        if isinstance(mid, Exception):
            raise mid
        return {"status": mid}

    def c():
        calls.append("C")
        return {"status": "PASS"}

    return [("A", a), ("B", b), ("C", c)]


@pytest.mark.parametrize("mid,status", [(GF("INCONCLUSIVE/HEADROOM", "r"), "INCONCLUSIVE/HEADROOM"),
                                        ("FAIL_TECHNICAL/ORACLE", "FAIL_TECHNICAL/ORACLE")])
def test_run_gates_stops_at_first_non_pass(tmp_path, mid, status):
    calls = []
    cdr.run_gates_c(tmp_path, _steps(calls, mid))
    assert calls == ["A", "B"]
    got = {g["gate"]: g["status"] for g in _gates(tmp_path)}
    assert got == {"A": "PASS", "B": status, "C": "NOT_RUN"}
    assert [g for g in _gates(tmp_path) if g["gate"] == "A"][0].get("x") == 1


def test_run_gates_dry_continue_calls_later_gates(tmp_path):
    calls = []
    cdr.run_gates_c(tmp_path, _steps(calls, "FAIL_TECHNICAL/ORACLE"), dry_continue=True)
    assert calls == ["A", "B", "C"]
    assert [g["status"] for g in _gates(tmp_path)] == ["PASS", "FAIL_TECHNICAL/ORACLE", "PASS"]


def test_run_gates_pause_is_recorded_and_stops(tmp_path):
    calls = []
    try:
        cdr.run_gates_c(tmp_path, _steps(calls, hwsb_driver.Paused("E1: STAGE")))
    except hwsb_driver.Paused:
        pass
    assert "C" not in calls
    assert {g["gate"]: g["status"] for g in _gates(tmp_path)}["B"] == "PAUSE"


# ---------------------------------------------------------------- lineage_c
def _recorded_store(out):
    k4b_driver.begin_stage(out, "S3")
    f = out / "stages" / "S3" / "x.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("{}", encoding="utf-8")
    k4b_driver.complete_stage(out, "S3", [f])
    for name in ("AUTH_KC_0180.json", "SCHED_0180.json", "RELEASE_A.json", "RESERVATION_W2.json",
                 "KC_ACCEPT.json", "FREEZE.json", "ACCEPT_VALIDATION.json",
                 "DECISION_TRAIN.json", "REGISTRY_OBLIGATION.json"):
        (out / name).write_text("{}", encoding="utf-8")
    (out / "logs").mkdir()
    (out / "logs" / "run.log").write_text("log", encoding="utf-8")
    (out / "tmp").mkdir()
    (out / "tmp" / "scratch.bin").write_bytes(b"x")


def test_lineage_absent_and_recorded(tmp_path):
    assert cdr.lineage_c(tmp_path / "absent")["status"] == "PASS"
    out = tmp_path / "store"
    out.mkdir()
    _recorded_store(out)
    assert cdr.lineage_c(out)["status"] == "PASS"


def test_lineage_unrecorded_file_fails(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    _recorded_store(out)
    (out / "stages" / "S3" / "stray.json").write_text("{}", encoding="utf-8")
    with pytest.raises(GF) as e:
        cdr.lineage_c(out)
    assert e.value.status == "FAIL_TECHNICAL/LINEAGE"


def test_lineage_superseded_manifest(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    _recorded_store(out)
    f = out / "stages" / "S9" / "attempt.json"
    f.parent.mkdir(parents=True)
    f.write_text('{"attempt": 1}', encoding="utf-8")
    dest = k4b_release.archive_attempt(out, "0180-a1", [f], {})
    assert cdr.lineage_c(out)["status"] == "PASS"
    sums = (dest / "SHA256SUMS").read_text(encoding="utf-8")
    (dest / "SHA256SUMS").write_text(("0" if sums[0] != "0" else "1") + sums[1:],
                                     encoding="utf-8")
    with pytest.raises(GF) as e:
        cdr.lineage_c(out)
    assert e.value.status == "FAIL_TECHNICAL/LINEAGE"


# ---------------------------------------------------------------- auth_ok, sched_ok
ADD34 = C["authority"]["owner_addenda"]["34"]["sha256"]


@pytest.mark.parametrize("stage", ["KC", "TRAIN", "E1", "REG2", "E2"])
def test_auth_ok_refusals(stage):
    good = {"job_id": "0180", "stages": [stage], "owner_auth_sha256": ADD34,
            "run_approval_sha256": "a" * 64}
    assert cdr.auth_ok(None, stage)["ok"] is False
    assert cdr.auth_ok(dict(good, stages=["DRY"]), stage)["ok"] is False
    assert cdr.auth_ok(dict(good, owner_auth_sha256="b" * 64), stage)["ok"] is False
    # API-AMBIGUITY: the positive case needs the FREEZE.json run_approval_sha256 (TO_FREEZE).


SCHED = {"record": "SCHED", "utc": "2026-10-29T00:00:00Z", "coordinator_session": "s",
         "live_history_reservations": [], "frozen_registries_awaiting_draw": []}


@pytest.mark.parametrize("stage", ["DRY", "KC", "TRAIN", "E1", "REG2", "E2"])
def test_sched_ok_rules(stage):
    assert cdr.sched_ok(SCHED, stage)["ok"] is True
    assert cdr.sched_ok(None, stage)["ok"] is False
    w2 = dict(SCHED, live_history_reservations=["RES-X"])
    assert cdr.sched_ok(w2, stage)["ok"] is False
    w3 = dict(SCHED, frozen_registries_awaiting_draw=["K-REGX"])
    assert cdr.sched_ok(w3, stage)["ok"] is (stage == "DRY")


# ---------------------------------------------------------------- study ledger
def test_ledger_read_default(tmp_path):
    assert cdr.ledger_read(tmp_path / "none.json") == {"study": "hwsc-v1", "entries": [],
                                                        "cumulative_cpu_s": 0.0}


def test_ledger_append_atomic_cumulative_and_unique(tmp_path):
    p = tmp_path / "HWSC_CPU_LEDGER.json"
    cdr.ledger_append(p, "0180-TRAIN-620301-a1", "0180", "TRAIN", 100.25, "src/a", 620301)
    cdr.ledger_append(p, "0180-TRAIN-620301-a2", "0180", "TRAIN", 50.5, "src/b", 620301)
    led = json.loads(p.read_text(encoding="utf-8"))
    assert led["study"] == "hwsc-v1" and len(led["entries"]) == 2
    assert led["cumulative_cpu_s"] == pytest.approx(150.75, abs=1e-9)
    e = led["entries"][0]
    assert set(C["records"]["ledger_entry"]) <= set(e) and e["master"] == 620301
    assert not list(tmp_path.glob("*.tmp"))
    before = p.read_bytes()
    with pytest.raises(GF) as err:
        cdr.ledger_append(p, "0180-TRAIN-620301-a1", "0181", "TRAIN", 1.0, "src/c")
    assert err.value.status == "FAIL_TECHNICAL/LEDGER" and p.read_bytes() == before


# ---------------------------------------------------------------- pauses
CENTRAL = {"J-C1": 1200, "DRY": 600, "KC": 1500, "TRAIN": 6006.6, "E1": 2000}
CUMUL = {"J-C1": 1200, "DRY": 1800, "KC": 3300, "TRAIN": 9306.6, "E1": 11306.6}


@pytest.mark.parametrize("stage", list(CENTRAL))
def test_pause_check_thresholds_and_strictness(stage):
    r = cdr.pause_check_c(stage, 0.0, 0.0)
    assert r["pause"] is False and r["trigger"] is None
    assert r["stage_threshold"] == pytest.approx(3 * CENTRAL[stage], rel=1e-12)
    assert r["cum_threshold"] == pytest.approx(3 * CUMUL[stage], rel=1e-12)
    st, ct = r["stage_threshold"], r["cum_threshold"]
    assert cdr.pause_check_c(stage, st, 0.0)["pause"] is False  # equality does not pause
    up = cdr.pause_check_c(stage, math.nextafter(st, math.inf), 0.0)
    assert up["pause"] is True and up["trigger"] == "STAGE"
    assert cdr.pause_check_c(stage, 0.0, ct)["pause"] is False
    assert cdr.pause_check_c(stage, 0.0, math.nextafter(ct, math.inf))["trigger"] == "CUMULATIVE"
    both = cdr.pause_check_c(stage, st + 1.0, ct + 1.0)
    assert both["pause"] is True and both["trigger"] == "BOTH"


@pytest.mark.parametrize("k", [1, 2, 4])
def test_pause_check_e2_from_k(k):
    r = cdr.pause_check_c("E2", 0.0, 0.0, k=k)
    central = 300 + 1720.1 * k  # R: CONTRACT cpu.E2_planning.R while R is TO_FREEZE
    assert r["stage_threshold"] == pytest.approx(3 * central, rel=1e-9)
    assert r["cum_threshold"] == pytest.approx(3 * (11306.6 + central), rel=1e-9)
    assert C["cpu"]["E2_planning"][f"k{k}"] == pytest.approx(central, abs=0.5)


def test_pause_or_raise_writes_cpu_only_gate(tmp_path):
    out, led = tmp_path / "store", tmp_path / "ledger.json"
    out.mkdir()
    cdr.ledger_append(led, "0180-KC-a1", "0180", "KC", 1e7, "src")
    with pytest.raises(hwsb_driver.Paused):
        cdr.pause_or_raise_c(out, "KC", time.process_time(), ledger_path=led)
    g = [x for x in _gates(out) if x["gate"] == "PAUSE_KC"]
    assert len(g) == 1 and g[0]["status"] == "PAUSE"
    allowed = {"gate", "status", "utc", "criterion_met", "pause", "trigger", "stage_cpu",
               "stage_threshold", "cum_cpu", "cum_threshold", "stage", "reason"}
    assert set(g[0]) <= allowed, set(g[0]) - allowed
    assert "value" not in g[0] and g[0]["trigger"] in ("STAGE", "BOTH")
    assert any(e.get("event") == "PAUSE" for e in _events(out))


def test_pause_or_raise_exempt_and_disabled(tmp_path):
    out, led = tmp_path / "store", tmp_path / "ledger.json"
    out.mkdir()
    cdr.ledger_append(led, "0180-KC-a1", "0180", "KC", 1e7, "src")
    # API-AMBIGUITY: `cont` passed as the parsed {"stages": [...]} dict.
    cdr.pause_or_raise_c(out, "KC", time.process_time(), ledger_path=led, cont={"stages": ["KC"]})
    cdr.pause_or_raise_c(out, "KC", -1e9, ledger_path=None)
    assert not (out / "GATES.jsonl").exists() or not [
        g for g in _gates(out) if g["gate"].startswith("PAUSE")]


# ---------------------------------------------------------------- D6 export (DRC10)
def _endpoint():
    pm = {j: {"L": 0.004, "U": 0.006, "F_minus": "1/10000", "F_plus": "1/10000",
              "status": "EXCLUDE", "label": None} for j in cc.MASTERS}
    return {"overall": "EXCLUSION", "per_model": pm, "N": 3072, "k": 1}


def _state(result):
    return {"fail": None, "resource": None, "l1": None, "k4b": None, "criterion": None,
            "models": None, "endpoint": result}


def test_export_writes_result_and_sealed_opened_in_one_s8_event(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    rng = np.random.default_rng(5)
    arrays = {"mean_X_minus": {j: rng.normal(size=40) for j in cc.MASTERS},
              "mean_X_plus": {j: rng.normal(size=40) + 1 for j in cc.MASTERS}}
    result, fill = _endpoint(), {"delta4_orc_certified": False}
    with cb.bound_stage_c():
        k4b_stats.write_sealed(out, arrays)
        ann = cg.annotations(result)
        oc = cg.outcome(_state(result))
        p = Path(cdr.export_c(out, result, oc, ann, fill))
        lic = cg.licence(oc, fill)
    d = out / "stages" / "S8"
    assert p == d / "RESULT.json"
    res = json.loads(p.read_text(encoding="utf-8"))
    assert res["outcome"] == oc["outcome"] == "EXCLUSION"
    assert res["annotations"] == json.loads(json.dumps(ann, default=str))
    for j in cc.MASTERS:
        assert f"POSITIVE_BELOW_MARGIN_{j}" in res["annotations"]
    assert "POSITIVE_BELOW_MARGIN" in res["annotations"]
    assert res["licence"] == lic and res["lineage_disclosure"] == C["disclosure"]
    assert res["does_not_establish"] == C["licences"]["does_not_establish"]
    assert res["protocol_sha256"] == C["protocol_sha256"]
    assert res["overall"] == "EXCLUSION" and "outcome_detail" in res
    sealed = json.loads((out / "SEALED_VALIDATION.json").read_text(encoding="utf-8"))
    assert sealed["protocol_sha256"] == C["protocol_sha256"]
    assert json.loads((d / "SEALED_OPENED.json").read_text(encoding="utf-8")) == sealed
    ev = _events(out)
    s8 = [e for e in ev if e.get("event") == "STAGE_COMPLETE" and e.get("stage") == "S8"]
    assert len(s8) == 1 and ev[-1] == s8[0]
    assert s8[0]["files"] == {"stages/S8/RESULT.json": _sha(d / "RESULT.json"),
                              "stages/S8/SEALED_OPENED.json": _sha(d / "SEALED_OPENED.json")}


def test_export_without_sealed_validation_fails(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    result = _endpoint()
    with cb.bound_stage_c():
        with pytest.raises(GF) as e:
            cdr.export_c(out, result, cg.outcome(_state(result)), cg.annotations(result), {})
    assert e.value.status == "FAIL_TECHNICAL/SEALING"


@pytest.mark.parametrize("key", list(k4b_stats.SEALED_KEYS))
def test_sealed_keys_refused_anywhere(key):
    report = {"gates": [], "ladder": {"candidates": {"3072": {"inner": {key: 1.0}}}}}
    with cb.bound_stage_c():
        with pytest.raises(GF) as e:
            k4b_stats.check_unsealed(report)
        assert e.value.status == "FAIL_TECHNICAL/SEALING"
        k4b_stats.check_unsealed({"gates": [], "sdU": {"620301-": 0.1}})


# ---------------------------------------------------------------- HANDOFF reader
def test_load_handoff_real():
    h = cc.load_handoff()
    v = C["handoff"]["values"]
    assert set(h) == set(C["handoff"]["keys"])
    for k in ("Z_bound", "F_plan", "registry_value"):
        assert isinstance(h[k], Fraction) and h[k] == Fraction(v[k])
    for k in ("N_C", "k_C", "model_count"):
        assert type(h[k]) is int and h[k] == v[k]
    assert type(h["p_D2a"]) is float and h["p_D2a"] == v["p_D2a"]
    assert h["stage_c_exclusions"] == tuple(C["handoff"]["stage_c_exclusions"])
    assert len(h["stage_c_exclusions"]) == 24 and h["outcome"] == "HWSB_PASS"
    assert h["training_forecast_s"] == 6006.6282


def _variant(tmp_path, name, mutate):
    data = json.loads(Path(C["handoff"]["path"]).read_bytes())
    mutate(data)
    p = tmp_path / name
    p.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return p, _sha(p)


@pytest.mark.parametrize("name,mutate", [
    ("forbidden.json", lambda d: d["store_inventory"].update({"x/y.npz": {"dev_ce": 1.0}})),
    ("forbidden2.json", lambda d: d.update(registry_obligation={"note": {"captured": 0.5}})),
    ("extra.json", lambda d: d.update(extra_key=1)),
    ("missing.json", lambda d: d.pop("k_C"))])
def test_load_handoff_refuses_structure(tmp_path, name, mutate):
    p, sha = _variant(tmp_path, name, mutate)
    with pytest.raises(GF) as e:
        cc.load_handoff(p, expected_sha256=sha)
    assert e.value.status == "FAIL_TECHNICAL/IDENTITY"


def test_load_handoff_sha_checked(tmp_path):
    raw = Path(C["handoff"]["path"]).read_bytes()
    same = tmp_path / "same.json"
    same.write_bytes(raw)
    assert cc.load_handoff(same)["N_C"] == 3072
    changed = tmp_path / "changed.json"
    changed.write_bytes(raw.replace(b"HWSB_PASS", b"HWSB_PASs", 1))
    with pytest.raises(GF) as e:
        cc.load_handoff(changed)
    assert e.value.status == "FAIL_TECHNICAL/IDENTITY"
