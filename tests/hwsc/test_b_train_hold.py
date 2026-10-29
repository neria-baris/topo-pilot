"""Author B (job 0176): the TRAIN job (with spies: no real sampling or training), the per-model
training hold and a tiny held-and-continued training (DRC12).

Written from PROTOCOL_HWSC_v1.md sections 2.3, 5 (T1-T3), 8.3, API.md sections 7.3, 11.1, 13, 14
and 18 (R-0176-G12), CONTRACT.json `cpu`, `records`, `recipe` and TEST_PLAN.md section 3 only.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402, I001
import hwsc_bind as cb  # noqa: E402
import hwsc_data as cd  # noqa: E402
import hwsc_driver as cdr  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import hwsc_known as ck  # noqa: E402
import hwsc_registry as cr  # noqa: E402
import hwsb_config  # noqa: E402
import hwsb_dry  # noqa: E402
import hwsb_known  # noqa: E402
import hwsb_train  # noqa: E402
import k4b_fresh  # noqa: E402
import k4b_release  # noqa: E402
import stage_records  # noqa: E402
from topo_pilot.contracts import ArtifactStore, ErrorCode, MemoryBackend, StageFailure  # noqa: E402

C = cc.CONTRACT
KEY = "W12-q1-s1.75-p0.2"
STEPS = tuple(C["recipe"]["train_config"]["checkpoint_steps"])
DRY = (629911, 629912, 629913)
SCHED = {"record": "SCHED", "utc": "2026-10-29T00:00:00Z", "coordinator_session": "s",
         "live_history_reservations": [], "frozen_registries_awaiting_draw": []}
AUTH = {"job_id": "0180", "stages": ["TRAIN"], "owner_auth_sha256": "a" * 64,
        "run_approval_sha256": "b" * 64}


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _outcome(fn):
    """(raised status or None, returned value or None)."""
    try:
        return None, fn()
    except Exception as exc:  # noqa: BLE001
        return cdr.status_of(exc), None


def _statuses(out, raised, ret):
    found = {raised} if raised else set()
    if isinstance(ret, dict) and "status" in ret:
        found.add(ret["status"])
    if (Path(out) / "GATES.jsonl").exists():
        found |= {g["status"] for g in stage_records.gates_so_far(Path(out))}
    for rec in Path(out).glob("stages/TRAIN/*/TRAIN_RECORD.json"):
        found.add(json.loads(rec.read_text(encoding="utf-8"))["status"])
    return found


def _patch_all(monkeypatch, name, value, also=()):
    """Set `name` on every loaded stage-C module that defines it (a split by size may keep the
    function in a helper module and re-export it, API.md section 0), and on `also`."""
    for mod in [m for k, m in list(sys.modules.items()) if k.startswith("hwsc_")] + list(also):
        if hasattr(mod, name):
            monkeypatch.setattr(mod, name, value)


# ---------------------------------------------------------------- run_train with spies
@pytest.fixture
def train_env(tmp_path, monkeypatch):
    out = tmp_path / "hwsc-store"
    (out / "stages" / "KC").mkdir(parents=True)
    ids = cd.build_process_c(ArtifactStore(MemoryBackend()))["ids"]
    kc = out / "stages" / "KC" / "KC_RECORD.json"
    kc.write_text(json.dumps({"status": "PASS", "process_ids": hwsb_known.jsonable(ids)}),
                  encoding="utf-8")
    acc = out / "KC_ACCEPT.json"
    acc.write_text(json.dumps({"accept": True, "kc_record_sha256": _sha(kc),
                               "six_thread_ruling": False}), encoding="utf-8")
    seen = {"train": [], "mtd": []}
    _patch_all(monkeypatch, "preflight", lambda *a, **k: {"refused": False, "status": "PASS"})
    _patch_all(monkeypatch, "pause_or_raise_c", lambda *a, **k: None)
    monkeypatch.setattr(hwsb_train, "set_threads",
                        lambda n: {"requested": n, "torch_threads": n, "torch_version": "x",
                                   "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})

    def fake_mtd(store, proc, master, plan, scope=cc.SCOPE):
        seen["mtd"].append({"plan": plan, "master": master, "scope": scope})
        return {"train": "a" * 16, "dev": "b" * 16, "streams": {}, "n": {"train": 131072,
                "dev": 4096}, "replicates": {"train": f"hwsc-v1/train/{master}",
                                             "dev": f"hwsc-v1/dev/{master}"}}

    behaviour = {"raise": None}

    def fake_train(store, obs_ids, master, plan=None, hold=None, seeds=None):
        seen["train"].append({"plan": plan, "master": master, "hold": hold, "obs": obs_ids,
                              "run_key": tuple(hwsb_config.run_key(plan, master)),
                              "active": cb.ACTIVE})
        if behaviour["raise"] is not None:
            raise behaviour["raise"]
        return {"run_key": list(hwsb_config.run_key(plan, master)),
                "checkpoint_ids": {s: f"{s:016x}" for s in STEPS},
                "checksums": {s: "0" * 64 for s in STEPS}, "dev_ce": {s: 1.0 for s in STEPS},
                "train_loss": {s: 1.0 for s in STEPS},
                "summary": {"steps_done": 5000, "final_train_loss": 1.0, "wall_time_s": 1.0,
                            "tokens_per_second": 1.0, "device": "cpu", "torch_version": "x"},
                "holds": []}

    _patch_all(monkeypatch, "make_train_dev_c", fake_mtd)
    monkeypatch.setattr(hwsb_train, "train", fake_train)

    def run(master=620301, accept=acc):
        # API-AMBIGUITY: kc_accept is the parsed KC_ACCEPT.json dict (a path is not accepted).
        data = json.loads(Path(accept).read_text(encoding="utf-8"))
        return _outcome(lambda: cdr.run_train(out, AUTH, SCHED, master, data))

    return out, seen, behaviour, run, acc


def test_run_train_passes_stage_c_plan_and_hold(train_env):
    out, seen, _, run, _ = train_env
    raised, _ = run()
    assert raised is None
    assert len(seen["train"]) == 1 and len(seen["mtd"]) == 1
    call = seen["train"][0]
    assert call["plan"] is cc.HWSC_PLAN and seen["mtd"][0]["plan"] is cc.HWSC_PLAN
    assert type(call["master"]) is int and call["master"] == 620301
    assert call["run_key"] == ("hwsc-v1", KEY, 620301) == cc.run_key(cc.HWSC_PLAN, 620301)
    assert call["active"] is True and call["obs"] == {"train": "a" * 16, "dev": "b" * 16}
    hold = call["hold"]
    assert isinstance(hold, hwsb_train.HoldRule)
    assert (hold.cap_s, hold.steps, hold.from_step) == (6006.6282, 5000, 1000)
    assert Path(hold.out_dir) == out / "stages" / "TRAIN" / "620301"
    rec = json.loads((out / "stages/TRAIN/620301/TRAIN_RECORD.json").read_text(encoding="utf-8"))
    assert set(C["records"]["TRAIN_RECORD"]) <= set(rec)
    assert rec["status"] == "COMPLETE" and rec["master"] == 620301
    assert list(rec["run_key"]) == ["hwsc-v1", KEY, 620301]
    assert cb.ACTIVE is False


def test_run_train_existing_record_is_rerun(train_env):
    out, seen, _, run, _ = train_env
    assert run()[0] is None
    raised, ret = run()
    assert "FAIL_TECHNICAL/RERUN" in _statuses(out, raised, ret)
    assert len(seen["train"]) == 1


def test_run_train_wrong_kc_accept_is_refused(train_env, tmp_path):
    out, seen, _, run, acc = train_env
    bad = tmp_path / "KC_ACCEPT_bad.json"
    data = json.loads(acc.read_text(encoding="utf-8"))
    bad.write_text(json.dumps(dict(data, kc_record_sha256="0" * 64)), encoding="utf-8")
    raised, ret = run(accept=bad)
    assert seen["train"] == [] and not list(out.glob("stages/TRAIN/*/TRAIN_RECORD.json"))
    gates = [g for g in stage_records.gates_so_far(out) if g["gate"] == "KC_ACCEPT"] if (
        out / "GATES.jsonl").exists() else []
    assert gates and gates[-1]["status"] != "PASS" or raised is not None


def test_run_train_owner_stop_at_hold_writes_record(train_env):
    out, seen, behaviour, run, _ = train_env
    behaviour["raise"] = hwsb_config.HwsbStop("INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
                                              "owner STOP at hold step 1000")
    raised, ret = run()
    rec = json.loads((out / "stages/TRAIN/620301/TRAIN_RECORD.json").read_text(encoding="utf-8"))
    assert rec["status"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    assert raised in (None, "INCONCLUSIVE/RESOURCE_OR_AUTHORITY")


def test_run_train_nonfinite_loss(train_env):
    out, _, behaviour, run, _ = train_env
    behaviour["raise"] = StageFailure(ErrorCode.NONFINITE_LOSS, "trainer", "loss", "nan")
    raised, ret = run()
    assert "FAIL_TECHNICAL/NONFINITE" in _statuses(out, raised, ret)


# ---------------------------------------------------------------- the training hold
def _rule(tmp_path, decision="CONTINUE"):
    d = tmp_path / "620301"
    d.mkdir()
    box = {"cpu": 0.0}

    def sleep(_):
        for h in d.glob("HOLD_*.json"):
            dec = d / f"DECISION_{h.stem.split('_')[1]}.json"
            if not dec.exists():
                dec.write_text(json.dumps({"decision": decision, "by": "test", "utc": "x"}),
                               encoding="utf-8")

    rule = hwsb_train.HoldRule(d, cap_s=cc.HOLD_S, steps=cc.STEPS, from_step=cc.HOLD_FROM,
                               cpu_fn=lambda: box["cpu"], poll_s=0.0, sleep=sleep)
    return rule, box, d


def test_hold_constants():
    assert cc.HOLD_S == 6006.6282 == C["cpu"]["per_model_hold_s"]
    assert C["cpu"]["per_model_central_s"] * 3 == pytest.approx(cc.HOLD_S, abs=1e-9)
    assert C["handoff"]["values"]["training_forecast_s"] == cc.HOLD_S
    assert (cc.HOLD_FROM, cc.STEPS) == (1000, 5000)


def test_no_hold_before_step_1000(tmp_path):
    rule, box, d = _rule(tmp_path)
    box["cpu"] = 3000.0  # projected 21,428 at step 700, but projection starts at 1,000
    assert rule(700) is None and not list(d.glob("HOLD_*"))


def test_projection_above_cap_holds_and_continue_exempts(tmp_path):
    rule, box, d = _rule(tmp_path)
    box["cpu"] = 1201.33  # projection 6,006.65 > 6,006.6282
    ev = rule(1000)
    assert ev is not None and rule.exempt is True
    hold = json.loads((d / "HOLD_1000.json").read_text(encoding="utf-8"))
    assert set(hold) == {"step", "cpu_s", "projected_s", "trigger", "utc"}
    assert hold["step"] == 1000 and hold["trigger"] == "PROJECTED"
    assert hold["projected_s"] == pytest.approx(6006.65, abs=1e-6)
    box["cpu"] = 1e6
    assert rule(2000) is None and not (d / "HOLD_2000.json").exists()


def test_cap_equality_does_not_hold(tmp_path):
    rule, box, d = _rule(tmp_path)
    box["cpu"] = 6006.6282  # projection = spent = cap exactly at step 5,000 (strict >)
    assert rule(5000) is None
    box["cpu"] = math.nextafter(6006.6282, math.inf)
    assert rule(5000) is not None and (d / "HOLD_5000.json").exists()


def test_stop_at_hold_is_inconclusive(tmp_path):
    rule, box, _ = _rule(tmp_path, decision="STOP")
    box["cpu"] = 2000.0
    with pytest.raises(hwsb_config.HwsbStop) as e:
        rule(1000)
    assert e.value.status == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


# ---------------------------------------------------------------- held and continued: bitwise
def _tiny_run(tmp_path, name, hold_dir=None):
    store = ArtifactStore(MemoryBackend())
    proc = hwsb_dry.build_tiny_process(store, masters=DRY)
    base = cc.dry_plan("dry_tiny", "H")
    tc = dataclasses.replace(base.train_cfg, steps=20, warmup=2, checkpoint_steps=(0, 10, 20))
    plan = dataclasses.replace(base, train_cfg=tc, sizes={"train": 2048, "dev": 256})
    obs = cd.make_train_dev_c(store, proc, DRY[0], plan, scope="hwsc-v1")
    hold = None
    if hold_dir is not None:
        hold_dir.mkdir()
        cpu = iter([0.0, 100.0])

        def sleep(_):
            (hold_dir / "DECISION_10.json").write_text(
                json.dumps({"decision": "CONTINUE", "by": "test", "utc": "x"}), encoding="utf-8")

        hold = hwsb_train.HoldRule(hold_dir, cap_s=50.0, steps=20, from_step=10,
                                   cpu_fn=lambda: next(cpu, 1e9), poll_s=0.0, sleep=sleep)
    return hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, DRY[0],
                            plan=plan, hold=hold)


def test_held_and_continued_tiny_run_is_bitwise_equal(tmp_path):
    with cb.bound_stage_c(cb.load_table(which="dry", case="H", case_dir=tmp_path / "case")):
        free = _tiny_run(tmp_path, "free")
        held = _tiny_run(tmp_path, "held", hold_dir=tmp_path / "hold")
    assert (tmp_path / "hold" / "HOLD_10.json").exists()
    assert len(held["holds"]) == 1
    assert set(free["checksums"]) == {0, 10, 20}
    assert held["checksums"] == free["checksums"]
    assert held["checkpoint_ids"] == free["checkpoint_ids"]
    assert list(held["run_key"]) == ["hwsc-v1", "DRY", "H", DRY[0]]


# ---------------------------------------------------------------- R-0176-P10: audit failure stops
# API.md section 2 names the hit keys module/where/kind/hit; "top" is added as a superset.
_HIT = {"module": "planted", "where": "X", "top": "X", "kind": "global", "hit": 1729}
FAILED_AUDIT = {"status": "FAIL_TECHNICAL/BINDING", "n_hits": 1, "modules": ["planted"],
                "hits": [_HIT], "unlisted": [_HIT]}
DOWNSTREAM = {
    "E2": [(k4b_fresh, "load_recorded"), (k4b_fresh, "load_frozen"), (k4b_fresh, "t_pre"),
           (k4b_fresh, "endpoint_gate"), (cd, "sample_test_c"), (cd, "h2_fresh_c"), (cg, "h1c"),
           (cd, "build_process_c")],
    "REG2": [(cr, "build"), (k4b_fresh, "load_recorded")],
    "KC": [(ck, "run_kc"), (ck, "g0c"), (ck, "kc1")],
    "TRAIN": [(cd, "make_train_dev_c"), (hwsb_train, "train")]}


def _plant_failing_audit(monkeypatch, stage):
    _patch_all(monkeypatch, "audit", lambda *a, **k: json.loads(json.dumps(FAILED_AUDIT)))
    _patch_all(monkeypatch, "preflight", lambda *a, **k: {"refused": False, "status": "PASS"})
    _patch_all(monkeypatch, "verify_freeze_c", lambda *a, **k: {"status": "PASS"})
    _patch_all(monkeypatch, "auth_ok", lambda *a, **k: {"ok": True, "reason": None})
    _patch_all(monkeypatch, "sched_ok", lambda *a, **k: {"ok": True, "reason": None})
    # Release and reservation checks pass, so only the audit can stop the job (whatever their
    # position relative to BINDING_AUDIT).
    rel_b = {"kind": "B", "job_id": "0180", "N": 3072, "k": 1, "reservation": cc.RESERVATION_ID,
             "kreg2_sha256": "0" * 64, "protocol_sha256": C["protocol_sha256"]}
    _patch_all(monkeypatch, "require_release_b", lambda *a, **k: dict(rel_b), also=(k4b_fresh,))
    _patch_all(monkeypatch, "verify_reservation", lambda *a, **k: {"status": "PASS"},
               also=(k4b_release,))
    started = []
    for mod, name in DOWNSTREAM[stage]:
        def spy(*a, _n=name, **k):
            started.append(_n)
            raise RuntimeError(f"{_n} started after a failed binding audit")

        if name.startswith("run_"):  # also a driver entry-point name: patch its own module only
            monkeypatch.setattr(mod, name, spy)
        else:
            _patch_all(monkeypatch, name, spy, also=(mod,))
    return started


def _assert_stopped_at_audit(out, raised, ret, started):
    assert started == [], started
    gates = stage_records.gates_so_far(out) if (out / "GATES.jsonl").exists() else []
    names = [g["gate"] for g in gates]
    assert "BINDING_AUDIT" in names, names
    i = names.index("BINDING_AUDIT")
    assert gates[i]["status"] != "PASS"
    assert all(g["status"] == "NOT_RUN" for g in gates[i + 1:]), gates[i + 1:]
    assert "FAIL_TECHNICAL/BINDING" in _statuses(out, raised, ret)
    assert cb.ACTIVE is False


@pytest.mark.parametrize("stage", ["E2", "REG2", "KC"])
def test_failed_binding_audit_stops_the_job(tmp_path, monkeypatch, stage):
    out = tmp_path / "hwsc-store"
    out.mkdir()
    started = _plant_failing_audit(monkeypatch, stage)
    auth = dict(AUTH, stages=[stage])
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")  # verify_freeze_c is stubbed
    rep = out / "stages" / "S5" / "VALIDATION_REPORT.json"  # a valid ACCEPT, whatever the order
    rep.parent.mkdir(parents=True)
    rep.write_text("{}", encoding="utf-8")
    accept = {"verdict": "ACCEPT", "validation_report_sha256": _sha(rep), "by": "t", "utc": "x"}
    call = {"E2": lambda: cdr.run_e2(out, auth, SCHED, tmp_path / "RELEASE_B.json", "sess"),
            "REG2": lambda: cdr.run_reg2(out, auth, SCHED, accept),  # parsed, as kc_accept
            "KC": lambda: cdr.run_kc(out, auth, SCHED, "0180")}[stage]
    raised, ret = _outcome(call)
    _assert_stopped_at_audit(out, raised, ret, started)


def test_failed_binding_audit_stops_train(train_env, monkeypatch):
    out, seen, _, run, _ = train_env
    started = _plant_failing_audit(monkeypatch, "TRAIN")
    raised, ret = run()
    _assert_stopped_at_audit(out, raised, ret, started)
    assert seen["train"] == []
