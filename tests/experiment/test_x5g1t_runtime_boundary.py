"""Independent tests written from the API contract only (X5_G1_TRAINING_API.md §5 and §8
"Runtime"; protocol x5g1-train-v3 §8-§9), before reading ``x5g1t_runtime``.

Part 2: run lock and outcome records, budget arithmetic (including the prior ledger of
17.016 CPU s), resource caps, and ``StudyControls.boundary`` composed with a real
``RunControls`` on a temporary ledger. Part 1 (controls and hold) is
``test_x5g1t_runtime.py``.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from topo_pilot.experiment import x4b_run
from topo_pilot.experiment import x5g1t_runtime as rt
from topo_pilot.experiment.x5g1_controls import (
    BudgetExceeded,
    LedgerCorrupt,
    RunControls,
    StopRequested,
)
from topo_pilot.experiment.x5g1_safety import OutputExists

pytestmark = pytest.mark.experiment

PRIOR = 17.016
GIB = 2**30
EST = {"update": 0.383, "dev_ce": 3.92, "score": 3.906, "save": 1.0, "bootstrap": 120.0,
       "exports": 60.0}


# ---------------------------------------------------------------- run lock and outcomes


def test_runlock_is_exclusive_and_removed(tmp_path: Path) -> None:
    lock = tmp_path / "RUN.lock"
    ident = {"arm": "a0", "master": 310001}
    with rt.RunLock(lock, ident):
        rec = json.loads(lock.read_text(encoding="utf-8"))
        assert rec["pid"] == os.getpid() and rec["identity"] == ident and "utc" in rec
        before = lock.read_bytes()
        with pytest.raises(rt.RunLocked):
            with rt.RunLock(lock, {"arm": "a020", "master": 310001}):
                pytest.fail("second lock acquired")
        assert lock.read_bytes() == before  # the refused attempt did not touch the lock
    assert not lock.exists()
    with rt.RunLock(lock, ident):  # reusable once released
        assert lock.exists()
    assert not lock.exists()


def test_runlock_refuses_stale_lock_of_unknown_state(tmp_path: Path) -> None:
    lock = tmp_path / "RUN.lock"
    lock.write_text("not even json", encoding="utf-8")
    with pytest.raises(rt.RunLocked):
        with rt.RunLock(lock, {}):
            pass
    assert lock.read_text(encoding="utf-8") == "not even json"


def test_runlock_removed_on_error_and_never_suppresses(tmp_path: Path) -> None:
    lock = tmp_path / "RUN.lock"
    with pytest.raises(KeyError, match="boom"):
        with rt.RunLock(lock, {"arm": "a0"}):
            raise KeyError("boom")
    assert not lock.exists()
    with pytest.raises(StopRequested):
        with rt.RunLock(lock, {"arm": "a0"}):
            raise StopRequested("x")
    assert not lock.exists()
    assert issubclass(rt.RunLocked, RuntimeError)


def test_outcome_path_and_roundtrip(tmp_path: Path) -> None:
    root = tmp_path / "study"
    assert rt.outcome_path(root, "a020", 310002) == root / "outcomes" / "a020_310002.json"
    assert rt.read_outcome(root, "a020", 310002) is None  # outcomes dir absent
    out = {"status": "INCOMPLETE", "arm": "a020", "master": 310002, "checkpoints": [],
           "cause": "StopRequested: x"}
    rt.record_outcome(root, "a020", 310002, out)
    assert rt.read_outcome(root, "a020", 310002) == out
    assert rt.read_outcome(root, "a0", 310002) is None


def test_record_outcome_refuses_overwrite(tmp_path: Path) -> None:
    root = tmp_path / "study"
    rt.record_outcome(root, "a0", 310001, {"status": "COMPLETE"})
    path = rt.outcome_path(root, "a0", 310001)
    original = path.read_bytes()
    with pytest.raises(OutputExists):
        rt.record_outcome(root, "a0", 310001, {"status": "INCOMPLETE"})
    assert path.read_bytes() == original
    assert sorted(p.name for p in path.parent.iterdir()) == ["a0_310001.json"]


def test_assert_can_start(tmp_path: Path) -> None:
    root, lock = tmp_path / "study", tmp_path / "study" / "RUN.lock"
    assert rt.assert_can_start(root, "a0", 310001, lock) is None
    root.mkdir()
    lock.write_text("{}", encoding="utf-8")
    with pytest.raises(rt.RunLocked):
        rt.assert_can_start(root, "a0", 310001, lock)
    lock.unlink()
    rt.record_outcome(root, "a0", 310001, {"status": "INCOMPLETE"})
    with pytest.raises(rt.RunLocked):  # no retry after any recorded outcome
        rt.assert_can_start(root, "a0", 310001, lock)
    assert rt.assert_can_start(root, "a020", 310001, lock) is None
    assert rt.assert_can_start(root, "a0", 310002, lock) is None


# ---------------------------------------------------------------- budget


def test_est_constants_and_defaults() -> None:
    assert rt.EST == EST
    planner = rt.BudgetPlanner()
    assert planner.cap_s == 21600.0 and planner.factor == 1.5


def test_check_boundary_equal_passes_above_raises() -> None:
    planner = rt.BudgetPlanner()
    planner.check(21000.0, 200.0, 300.0, "eq")  # 21000 + 1.5*200 + 300 == 21600
    with pytest.raises(BudgetExceeded):
        planner.check(21000.0, 200.0, 300.5, "above")
    with pytest.raises(BudgetExceeded):
        planner.check(21000.0, 200.5, 300.0, "above_estimate")
    with pytest.raises(BudgetExceeded):
        planner.check(21600.25, 0.0, 0.0, "already_over")
    planner.check(0.0, 0.0, 0.0, "zero")


def test_factor_is_applied_to_estimate_only() -> None:
    rt.BudgetPlanner(cap_s=100.0).check(0.0, 66.0, 1.0, "x")  # 99 + 1
    with pytest.raises(BudgetExceeded):
        rt.BudgetPlanner(cap_s=100.0).check(0.0, 70.0, 0.0, "x")  # 105 > 100
    rt.BudgetPlanner(cap_s=100.0, factor=1.0).check(0.0, 70.0, 30.0, "x")
    rt.BudgetPlanner(cap_s=100.0, factor=2.0).check(0.0, 50.0, 0.0, "x")
    with pytest.raises(BudgetExceeded):
        rt.BudgetPlanner(cap_s=100.0, factor=2.0).check(0.0, 50.5, 0.0, "x")
    with pytest.raises(BudgetExceeded):  # the reserve is not multiplied but does count
        rt.BudgetPlanner(cap_s=100.0).check(0.0, 0.0, 100.5, "x")


def test_interval_estimate() -> None:
    assert rt.interval_estimate(250) == pytest.approx(250 * 0.383 + 3.92 + 1.0)
    assert rt.interval_estimate(250) == pytest.approx(100.67)
    assert rt.interval_estimate(100) == pytest.approx(43.22)
    assert rt.interval_estimate(0) == pytest.approx(4.92)
    est = dict(EST, update=1.0, dev_ce=2.0, save=3.0)
    assert rt.interval_estimate(10, est=est) == pytest.approx(15.0)


def test_evaluation_reserve() -> None:
    assert rt.evaluation_reserve(0, 0) == pytest.approx(1.5 * 300.0)
    assert rt.evaluation_reserve(10, 2) == pytest.approx(1.5 * (39.06 + 60 + 7.812 + 60 + 180))
    # nothing scored yet: 6 models x 27 grid checkpoints and 6 finals -> ~1.43 ks (§9)
    nothing = rt.evaluation_reserve(162, 6)
    assert nothing == pytest.approx(1434.312)
    assert 1425.0 < nothing < 1440.0
    assert rt.evaluation_reserve(10, 2, factor=1.0) == pytest.approx(346.872)
    est = dict(EST, score=1.0, bootstrap=0.0, exports=0.0)
    assert rt.evaluation_reserve(3, 1, est=est, factor=2.0) == pytest.approx(2 * 124.0)


def test_realistic_boundary_with_prior_ledger() -> None:
    planner = rt.BudgetPlanner()
    nxt, reserve = rt.interval_estimate(250), rt.evaluation_reserve(162, 6)
    room = 21600.0 - PRIOR - 1.5 * nxt - reserve  # largest admissible run CPU so far
    assert room == pytest.approx(21600.0 - 17.016 - 151.005 - 1434.312)
    planner.check(PRIOR + 13400.25, nxt, reserve, "projected run")  # §9 projection fits
    planner.check(PRIOR + room - 0.01, nxt, reserve, "just inside")
    with pytest.raises(BudgetExceeded):
        planner.check(PRIOR + room + 0.01, nxt, reserve, "just outside")


# ---------------------------------------------------------------- resources


def test_check_resources_caps() -> None:
    assert issubclass(rt.ResourceExceeded, RuntimeError)
    rt.check_resources(8 * GIB, 2 * GIB)  # at caps: ok
    rt.check_resources(0, 0)
    with pytest.raises(rt.ResourceExceeded):
        rt.check_resources(None, 0)  # unknown peak fails closed
    with pytest.raises(rt.ResourceExceeded):
        rt.check_resources(8 * GIB + 1, 0)
    with pytest.raises(rt.ResourceExceeded):
        rt.check_resources(0, 2 * GIB + 1)
    rt.check_resources(10, 20, ram_cap=10, storage_cap=20)
    with pytest.raises(rt.ResourceExceeded):
        rt.check_resources(11, 0, ram_cap=10, storage_cap=20)
    with pytest.raises(rt.ResourceExceeded):
        rt.check_resources(None, 0, ram_cap=10**18, storage_cap=10**18)


def test_dir_size(tmp_path: Path) -> None:
    assert rt.dir_size(tmp_path / "missing") == 0
    root = tmp_path / "out"
    root.mkdir()
    assert rt.dir_size(root) == 0
    (root / "a.bin").write_bytes(b"x" * 100)
    (root / "sub" / "deeper").mkdir(parents=True)
    (root / "sub" / "b.bin").write_bytes(b"y" * 23)
    (root / "sub" / "deeper" / "c.bin").write_bytes(b"z" * 1000)
    (root / "sub" / "empty").mkdir()
    assert rt.dir_size(root) == 1123


# ---------------------------------------------------------------- StudyControls.boundary


@pytest.fixture
def env(tmp_path: Path, monkeypatch):
    """Prior ledger (17.016 s), an allowing mailbox and deterministic, small resource use."""
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"entries": [{"job": "prior", "cpu_s": PRIOR,
                                               "status": "ok"}],
                                  "cumulative_cpu_s": PRIOR}), encoding="utf-8")
    box = tmp_path / "mailbox"
    box.mkdir()
    (box / "request.json").write_text(json.dumps({"command": "RUN_NEXT"}), encoding="utf-8")
    out = tmp_path / "study" / "runs"
    out.mkdir(parents=True)
    peak = {"value": 512 * 2**20}
    monkeypatch.setattr(rt, "peak_memory_bytes", lambda: peak["value"], raising=False)
    monkeypatch.setattr(x4b_run, "peak_memory_bytes", lambda: peak["value"])
    return {"ledger": ledger, "box": box, "out": out, "audit": tmp_path / "hold.json",
            "peak": peak}


def _ctl(env) -> RunControls:
    return RunControls(env["ledger"], cap_s=1e6, stop_path=env["box"] / "STOP", job="x5t",
                       cumulative_cap_s=1e9)


def _study(env, ctl, planner=None) -> rt.StudyControls:
    return rt.StudyControls(ctl, env["box"], planner or rt.BudgetPlanner(), env["out"],
                            env["audit"])


def _last(env) -> dict:
    data = json.loads(env["ledger"].read_text(encoding="utf-8"))
    assert len(data["entries"]) == 2 and data["entries"][0]["job"] == "prior"
    assert data["cumulative_cpu_s"] >= PRIOR
    return data["entries"][-1]


def test_boundary_continue_records_guard_step(env) -> None:
    with _ctl(env) as ctl:
        assert ctl.prior == pytest.approx(PRIOR)
        _study(env, ctl).boundary("ckpt_250", 100.67, 1434.312)
        assert ctl.steps[-1]["step"] == "ckpt_250"  # step 1: ctl.guard(what)
    assert _last(env)["status"] == "ok"
    assert not env["audit"].exists()


def test_boundary_planner_sees_prior_plus_cpu(env) -> None:
    seen = []

    class Recording(rt.BudgetPlanner):
        def check(self, cumulative_now, next_estimate, reserve, what):
            seen.append((cumulative_now, next_estimate, reserve, what))
            return super().check(cumulative_now, next_estimate, reserve, what)

    with _ctl(env) as ctl:
        _study(env, ctl, Recording()).boundary("ckpt", 7.0, 9.0)
        upper = PRIOR + ctl.cpu()
    (cum, nxt, res, what), = seen
    assert PRIOR <= cum <= upper + 1e-9 and (nxt, res, what) == (7.0, 9.0, "ckpt")


def test_boundary_stop_file(env) -> None:
    (env["box"] / "STOP").write_text("", encoding="utf-8")
    with pytest.raises(StopRequested):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 1.0, 0.0)
    assert _last(env)["status"] == "stopped"


def test_boundary_request_stop(env) -> None:
    (env["box"] / "request.json").write_text(json.dumps({"command": "STOP"}), encoding="utf-8")
    with pytest.raises(StopRequested):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 1.0, 0.0)
    assert _last(env)["status"] == "stopped"


def _inject_sleep(monkeypatch, on_sleep) -> list:
    """Contract ambiguity: StudyControls takes no ``sleep``; patch the module-level
    ``hold_while_needed`` so its sleep is the fake (and ``time.sleep`` as a safety net)."""
    calls: list = []
    orig = rt.hold_while_needed

    def fake_sleep(seconds: float) -> None:
        calls.append(seconds)
        if len(calls) > 50:
            raise AssertionError("hold did not end")
        on_sleep(len(calls))

    def wrapper(*args, **kwargs):
        if len(args) >= 4:
            args = args[:3] + (fake_sleep,) + args[4:]
        else:
            kwargs["sleep"] = fake_sleep
        return orig(*args, **kwargs)

    monkeypatch.setattr(rt, "hold_while_needed", wrapper)
    monkeypatch.setattr(time, "sleep", fake_sleep)
    return calls


def test_boundary_hold_then_release_proceeds(env, monkeypatch) -> None:
    wc = env["box"] / "worker_control.json"
    wc.write_text(json.dumps({"command": "WAIT_USAGE_RESET"}), encoding="utf-8")

    def release(n: int) -> None:
        if n == 2:
            wc.write_text(json.dumps({"command": "CONTINUE"}), encoding="utf-8")

    calls = _inject_sleep(monkeypatch, release)
    with _ctl(env) as ctl:
        _study(env, ctl).boundary("ckpt_500", 1.0, 0.0, audit=lambda: {"run": "a0_310001"})
    assert len(calls) == 2 and all(0 < s <= 45 for s in calls)
    rec = json.loads(env["audit"].read_text(encoding="utf-8"))
    assert rec["kind"] == "AUDIT_ONLY_NOT_A_RESUME_CHECKPOINT" and rec["run"] == "a0_310001"
    assert _last(env)["status"] == "ok"


def test_boundary_stop_while_held(env, monkeypatch) -> None:
    rs = env["box"] / "runtime_state.json"
    rs.write_text(json.dumps({"mode": "WAIT_USAGE_RESET"}), encoding="utf-8")
    _inject_sleep(monkeypatch, lambda n: (env["box"] / "STOP").write_text("", "utf-8"))
    with pytest.raises(StopRequested):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 1.0, 0.0)
    assert _last(env)["status"] == "stopped"


def test_boundary_budget_exceeded(env) -> None:
    with pytest.raises(BudgetExceeded):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 14400.0, 0.0)  # 17.016 + 21600 > 21600
    entry = _last(env)
    assert entry["status"] == "budget"


def test_boundary_budget_includes_prior(env) -> None:
    with pytest.raises(BudgetExceeded):  # fits without the prior 17.016 s, not with it
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 0.0, 21590.0)
    assert _last(env)["status"] == "budget"


def test_boundary_resources_fail_closed(env) -> None:
    env["peak"]["value"] = None
    with pytest.raises(rt.ResourceExceeded):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 1.0, 0.0)
    assert _last(env)["status"] == "error:ResourceExceeded"


def test_corrupt_ledger_raises_and_keeps_bytes(env) -> None:
    corrupt = b'{"entries": [], "cumulative_cpu_s": 17.0'
    env["ledger"].write_bytes(corrupt)
    with pytest.raises(LedgerCorrupt):
        with _ctl(env) as ctl:
            _study(env, ctl).boundary("ckpt", 1.0, 0.0)
    assert env["ledger"].read_bytes() == corrupt
