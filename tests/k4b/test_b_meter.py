"""Author B, K4b TEST_PLAN B19 and B20: the actual meter bindings (controls, meter, winjob values
after bind; --max-cpu inf --max-wall inf; op_guard deadline per operation, not per stage; child
TEMP/TMP/TMPDIR on X:; worker session and RUN.lock identity from the release) and the limiter
order: STOP/INVALID keep reason and state; HOLD alone never kills, a resource reason may kill
under HOLD with the HOLD state returned; legacy (latch processing) runs exactly once per poll;
ordinary overdue and disk failures, including unreadable free space.

Every rebinding is undone by monkeypatch; fake legacy, fake disk and fake clocks throughout."""

from __future__ import annotations

import argparse
import collections
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import pytest  # noqa: E402

import controls  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import op_guard  # noqa: E402
import winjob  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

INF = float("inf")
TEMP = Path("X:/Downloads/projects/topo-pilot/k4b-store/tmp-0047")
METER_NAMES = ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S", "STOP_NEW_S",
               "OUTPUT_CAP", "WORKER_SESSION", "limit_reason", "main")
Usage = collections.namedtuple("Usage", "total used free")


@pytest.fixture
def preserved(monkeypatch):
    """Record every module global bind() may rebind, so monkeypatch restores it afterwards."""
    for name in METER_NAMES:
        monkeypatch.setattr(meter, name, getattr(meter, name))
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(controls, name, getattr(controls, name))
    monkeypatch.setattr(winjob, "MEMORY_CAP", winjob.MEMORY_CAP)
    return monkeypatch


# --------------------------------------------------------------------- bindings (B19)

def test_bind_sets_every_registered_value(tmp_path, preserved):
    k4b_meter_bind.bind("0047", "ab12" * 16, tmp_path, "sess-k4b")
    assert controls.JOB_ID == "0047"
    assert controls.TASK_SHA256 == ("ab12" * 16).upper()
    assert Path(meter.OUT) == tmp_path
    assert Path(meter.LEDGER) == tmp_path / "cpu_ledger.json"
    assert Path(meter.EMERGENCY) == tmp_path / "cpu_ledger.emergency.jsonl"
    assert Path(meter.LOCK) == tmp_path / "RUN.lock"
    assert Path(meter.ACTIVE) == tmp_path / "METER_ACTIVE.lock"
    assert Path(meter.LOG_DIR) == tmp_path / "logs"
    assert meter.CAP_S == INF and meter.STOP_NEW_S == INF
    assert meter.OUTPUT_CAP == 4 * 1024**3
    assert winjob.MEMORY_CAP == 12 * 1024**3
    assert meter.WORKER_SESSION == "sess-k4b"


def test_run_lock_identity_follows_the_release_session(tmp_path, preserved):
    k4b_meter_bind.bind("0047", "CD" * 32, tmp_path, "sess-k4b")
    args = argparse.Namespace(lock_owner=None, mode="run")
    (tmp_path / "RUN.lock").write_text('{"session": "sess-k4b"}', encoding="utf-8")
    assert meter.lock_refusal(args) is None
    (tmp_path / "RUN.lock").write_text('{"session": "someone-else"}', encoding="utf-8")
    assert meter.lock_refusal(args) is not None


@pytest.mark.parametrize("argv", [
    ["meter.py", "--label", "S3", "--max-cpu", "600", "--max-wall", "3600"],
    ["meter.py", "--max-wall", "10", "--label", "S3"],
    ["meter.py", "--label", "S3"],
])
def test_rewrite_argv_forces_infinite_cpu_and_wall(argv):
    got = k4b_meter_bind.rewrite_argv(list(argv))
    assert got[0] == "meter.py"
    for flag in ("--max-cpu", "--max-wall"):
        assert got.count(flag) == 1
        assert got[got.index(flag) + 1] == "inf"
    assert "600" not in got and "3600" not in got and "10" not in got
    assert got[got.index("--label") + 1] == "S3"


def test_child_env_temp_on_x_and_single_thread():
    base = {"PATH": "p", "TEMP": r"C:\Users\x\AppData\Local\Temp", "OMP_NUM_THREADS": "8"}
    frozen = dict(base)
    env = k4b_meter_bind.child_env("0047", base)
    for var in ("TEMP", "TMP", "TMPDIR"):
        assert Path(env[var]) == TEMP
        assert env[var][:2].upper() == "X:"
    for var in meter.THREAD_VARS:
        assert env[var] == "1"
    assert env["PATH"] == "p"
    assert base == frozen


def test_child_env_default_copies_os_environ():
    before = dict(os.environ)
    env = k4b_meter_bind.child_env("0047")
    assert dict(os.environ) == before
    assert Path(env["TMP"]) == TEMP


def test_main_without_valid_release_never_runs_the_meter(tmp_path, preserved):
    ran = []
    preserved.setattr(meter, "main", lambda *a, **k: ran.append(1) or 0)
    out_before = meter.OUT
    bad = tmp_path / "release.json"
    bad.write_text('{"kind": "A",', encoding="utf-8")
    for argv in (["k4b_meter_bind.py", "--label", "S3", "--", "python", "-c", "pass"],
                 ["k4b_meter_bind.py", "--release", str(bad), "--label", "S3", "--", "python"]):
        preserved.setattr(sys, "argv", list(argv))
        try:
            code = k4b_meter_bind.main()
        except (SystemExit, C1GateFailure) as exc:
            code = getattr(exc, "code", 1) or 1
        assert code != 0
        assert ran == []
        assert meter.OUT == out_before


def test_op_guard_deadline_is_per_operation(tmp_path):
    now = {"t": 1000.0}
    clock = lambda: now["t"]  # noqa: E731
    timed = op_guard.timed_factory(tmp_path, 600, clock=clock, wall_clock=clock)
    lim = k4b_meter_bind.make_limiter(tmp_path / op_guard.MARKER, disk=lambda: None,
                                      legacy=lambda *a: (None, controls.CONTINUE), clock=clock)
    seen = []

    def op(advance):
        def fn():
            now["t"] += advance
            seen.append(lim({}, 0.0, None, 0.0, 1, []))
            return advance
        return fn

    for label in ("distance", "ph", "edges"):
        timed(label, op(599.0))  # the stage takes 1797 s, every operation < 600 s
    assert seen == [(None, controls.CONTINUE)] * 3
    with pytest.raises(Exception):
        timed("integer_lift", op(600.0))
    assert seen[-1][0] is not None and "integer_lift" in seen[-1][0]
    assert seen[-1][1] == controls.CONTINUE


# --------------------------------------------------------------- limiter order (B20)

class Legacy:
    def __init__(self, result):
        self.result, self.calls = result, 0

    def __call__(self, ledger, child, args, active_wall, polls, mailboxes):
        self.calls += 1
        return self.result


class Disk:
    def __init__(self, reason):
        self.reason, self.calls = reason, 0

    def __call__(self):
        self.calls += 1
        return self.reason


DISK_REASON = "disk safe-STOP: X:\\ free 1 < 30000000000 bytes"


def overdue_marker(tmp_path):
    op_guard.write_marker(tmp_path, {"state": "active", "seq": 4, "label": "ph",
                                     "started_epoch": 1000.0, "deadline_s": 600.0, "pid": 1})
    return tmp_path / op_guard.MARKER


def poll(lim, polls=8):
    return lim({"cumulative_cpu_s": 0.0}, 0.0, None, 0.0, polls, [])


@pytest.mark.parametrize("control", [("STOP: owner STOP file", controls.STOP),
                                     ("INVALID: control unreadable", controls.INVALID)])
def test_stop_and_invalid_keep_precedence_over_overdue_and_disk(tmp_path, control):
    legacy, disk = Legacy(control), Disk(DISK_REASON)
    lim = k4b_meter_bind.make_limiter(overdue_marker(tmp_path), disk=disk, legacy=legacy,
                                      clock=lambda: 5000.0)
    assert poll(lim) == control
    assert legacy.calls == 1 and disk.calls == 0
    assert k4b_meter_bind.classify_stop(*control) == control[1]


def test_hold_without_resource_failure_never_kills(tmp_path):
    legacy, disk = Legacy((None, controls.HOLD)), Disk(None)
    lim = k4b_meter_bind.make_limiter(overdue_marker(tmp_path), disk=disk, legacy=legacy,
                                      clock=lambda: 1200.0)
    for p in range(1, 17):
        assert poll(lim, p) == (None, controls.HOLD)
    assert legacy.calls == 16  # latch processing on every poll
    assert disk.calls == 2  # polls 8 and 16 only


def test_hold_with_overdue_operation_kills_and_keeps_hold(tmp_path):
    legacy = Legacy((None, controls.HOLD))
    lim = k4b_meter_bind.make_limiter(overdue_marker(tmp_path), disk=Disk(None), legacy=legacy,
                                      clock=lambda: 1600.0)
    reason, state = poll(lim, 3)
    assert reason and "native operation wall" in reason
    assert state == controls.HOLD and legacy.calls == 1
    assert k4b_meter_bind.classify_stop(reason, state) == "INCONCLUSIVE/RESOURCE"


def test_hold_with_disk_failure_kills_and_keeps_hold():
    legacy = Legacy((None, controls.HOLD))
    lim = k4b_meter_bind.make_limiter(None, disk=Disk(DISK_REASON), legacy=legacy,
                                      clock=lambda: 0.0)
    assert poll(lim, 8) == (DISK_REASON, controls.HOLD)
    assert legacy.calls == 1
    assert k4b_meter_bind.classify_stop(DISK_REASON, controls.HOLD) == "INCONCLUSIVE/RESOURCE"


def test_ordinary_overdue_beats_disk_and_returns_control_state(tmp_path):
    disk = Disk(DISK_REASON)
    lim = k4b_meter_bind.make_limiter(overdue_marker(tmp_path), disk=disk,
                                      legacy=Legacy((None, controls.CONTINUE)),
                                      clock=lambda: 1600.0)
    reason, state = poll(lim, 8)
    assert "native operation wall" in reason and state == controls.CONTINUE
    assert disk.calls == 0


def test_not_yet_overdue_and_disk_only_every_eighth_poll(tmp_path):
    disk = Disk(DISK_REASON)
    lim = k4b_meter_bind.make_limiter(overdue_marker(tmp_path), disk=disk,
                                      legacy=Legacy((None, controls.CONTINUE)),
                                      clock=lambda: 1599.0)
    assert poll(lim, 3) == (None, controls.CONTINUE)
    assert disk.calls == 0
    assert poll(lim, 16) == (DISK_REASON, controls.CONTINUE)


def test_default_legacy_is_the_original_meter_limit_reason(tmp_path, preserved):
    preserved.setattr(meter, "OUT", tmp_path)
    preserved.setattr(meter, "STOP_NEW_S", INF)
    state = {"value": (controls.STOP, "owner STOP file")}
    preserved.setattr(controls, "classify_all", lambda mailboxes, out, mode: state["value"])
    disk = Disk(DISK_REASON)
    lim = k4b_meter_bind.make_limiter(None, disk=disk, clock=lambda: 0.0)
    args = argparse.Namespace(mode="run", max_cpu=INF, max_wall=INF)
    led = {"cumulative_cpu_s": 0.0}
    assert lim(led, 0.0, args, 0.0, 8, []) == ("STOP: owner STOP file", controls.STOP)
    assert disk.calls == 0
    state["value"] = (controls.HOLD, "usage at 90%")
    assert lim(led, 0.0, args, 0.0, 8, []) == (DISK_REASON, controls.HOLD)


# ------------------------------------------------------------------ disk_reason (B20)

def usage_of(free):
    def usage(drive):
        return Usage(10**13, 10**13 - free[drive], free[drive])
    return usage


def test_disk_minima_registered():
    assert k4b_meter_bind.DISK_MIN_FREE == {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}


def test_disk_reason_none_at_or_above_minimum():
    free = {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}
    assert k4b_meter_bind.disk_reason(usage_of(free)) is None


@pytest.mark.parametrize("drive,low", [("C:\\", 1_999_999_999), ("X:\\", 29_999_999_999)])
def test_disk_reason_below_minimum(drive, low):
    free = {"C:\\": 5 * 10**10, "X:\\": 5 * 10**11, drive: low}
    minimum = k4b_meter_bind.DISK_MIN_FREE[drive]
    got = k4b_meter_bind.disk_reason(usage_of(free))
    assert got == f"disk safe-STOP: {drive} free {low} < {minimum} bytes"
    assert k4b_meter_bind.classify_stop(got, controls.CONTINUE) == "INCONCLUSIVE/RESOURCE"


def test_disk_reason_unreadable_free_space():
    def usage(drive):
        if drive == "X:\\":
            raise OSError("device not ready")
        return Usage(10**13, 0, 10**12)

    got = k4b_meter_bind.disk_reason(usage)
    assert got.startswith("disk safe-STOP: X:\\ free space unreadable (")
    assert "OSError" in got
    assert k4b_meter_bind.classify_stop(got, controls.HOLD) == "INCONCLUSIVE/RESOURCE"


def test_output_cap_reason_is_a_resource_stop():
    reason = f"output cap {4 * 1024**3} bytes"
    assert k4b_meter_bind.classify_stop(reason, controls.CONTINUE) == "INCONCLUSIVE/RESOURCE"
