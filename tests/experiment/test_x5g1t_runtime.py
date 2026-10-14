"""Independent tests written from the API contract only (X5_G1_TRAINING_API.md §5 and §8
"Runtime"; protocol x5g1-train-v3 §8), before reading ``x5g1t_runtime``.

Part 1: the control precedence table (``read_controls``) and the live usage hold
(``hold_while_needed``). Run lock, budget, resources and ``StudyControls`` are covered in
``test_x5g1t_runtime_boundary.py``. Every mailbox is a ``tmp_path``; no real sleeping.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from topo_pilot.experiment import x5g1t_runtime as rt
from topo_pilot.experiment.x5g1_controls import StopRequested

pytestmark = pytest.mark.experiment

KIND = "AUDIT_ONLY_NOT_A_RESUME_CHECKPOINT"


def _put(mailbox: Path, name: str, content) -> None:
    text = content if isinstance(content, str) else json.dumps(content)
    (mailbox / name).write_text(text, encoding="utf-8")


@pytest.fixture
def mb(tmp_path: Path) -> Path:
    """A mailbox that allows running: only a valid request.json."""
    box = tmp_path / "mailbox"
    box.mkdir()
    _put(box, "request.json", {"command": "RUN_NEXT"})
    return box


def _action(mailbox: Path) -> str:
    state = rt.read_controls(mailbox)
    if state.action in ("STOP", "HOLD"):
        assert len(state.reasons) > 0, f"{state.action} needs a reason"
    return state.action


# ---------------------------------------------------------------- read_controls


def test_controlstate_is_namedtuple(mb: Path) -> None:
    state = rt.read_controls(mb)
    assert isinstance(state, rt.ControlState) and isinstance(state, tuple)
    action, reasons = state
    assert action == state.action == "CONTINUE"
    assert reasons == state.reasons


def test_stop_file_is_stop_with_owner_reason(mb: Path) -> None:
    (mb / "STOP").write_text("", encoding="utf-8")
    state = rt.read_controls(mb)
    assert state.action == "STOP"
    assert any("owner_stop_file" in str(r) for r in state.reasons)


def test_stop_file_beats_worker_hold(mb: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    (mb / "STOP").write_text("stop", encoding="utf-8")
    assert _action(mb) == "STOP"


def test_request_stop_command(mb: Path) -> None:
    _put(mb, "request.json", {"command": "STOP"})
    assert _action(mb) == "STOP"


@pytest.mark.parametrize("content", [None, "{not json", "", "[1, 2]", '"RUN_NEXT"',
                                     {"command": "PAUSE"}, {"command": "run_next"},
                                     {"command": None}, {}])
def test_request_missing_or_bad_fails_closed(mb: Path, content) -> None:
    if content is None:
        (mb / "request.json").unlink()
    else:
        _put(mb, "request.json", content)
    assert _action(mb) == "STOP"


@pytest.mark.parametrize("command, expected", [("STOP", "STOP"),
                                               ("WAIT_USAGE_RESET", "HOLD"),
                                               ("CONTINUE", "CONTINUE")])
def test_worker_control_commands(mb: Path, command: str, expected: str) -> None:
    _put(mb, "worker_control.json", {"command": command})
    assert _action(mb) == expected


@pytest.mark.parametrize("content", ["{oops", "", "[]", '"STOP"', {"command": "PAUSE"},
                                     {"command": "wait_usage_reset"}])
def test_worker_control_malformed_or_unknown_is_stop(mb: Path, content) -> None:
    _put(mb, "worker_control.json", content)
    assert _action(mb) == "STOP"


def test_worker_control_missing_is_allowed(mb: Path) -> None:
    assert not (mb / "worker_control.json").exists()
    assert _action(mb) == "CONTINUE"


def test_runtime_state_wait_is_hold(mb: Path) -> None:
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    assert _action(mb) == "HOLD"


@pytest.mark.parametrize("mode", ["RUNNING", "IDLE", "CONTINUE", "STOP", "anything"])
def test_runtime_state_other_modes_are_noop(mb: Path, mode: str) -> None:
    _put(mb, "runtime_state.json", {"mode": mode})
    assert _action(mb) == "CONTINUE"


@pytest.mark.parametrize("content", ["{bad", "", "[1]", "42"])
def test_runtime_state_malformed_is_stop(mb: Path, content: str) -> None:
    _put(mb, "runtime_state.json", content)
    assert _action(mb) == "STOP"


@pytest.mark.parametrize("content", [{"observability": "UNAVAILABLE"},
                                     {"observability": "UNAVAILABLE", "mode": "STOP"},
                                     "{garbage"])
def test_claude_usage_is_never_read(mb: Path, content) -> None:
    _put(mb, "claude_usage.json", content)
    assert _action(mb) == "CONTINUE"


@pytest.mark.parametrize("stop_src", ["file", "request", "worker", "worker_bad", "state_bad"])
@pytest.mark.parametrize("hold_src", ["worker", "state"])
def test_stop_beats_hold_from_any_source(mb: Path, stop_src: str, hold_src: str) -> None:
    if hold_src == "worker":
        _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    else:
        _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    if stop_src == "file":
        (mb / "STOP").write_text("", encoding="utf-8")
    elif stop_src == "request":
        _put(mb, "request.json", {"command": "STOP"})
    elif stop_src == "worker":
        _put(mb, "worker_control.json", {"command": "STOP"})
    elif stop_src == "worker_bad":
        _put(mb, "worker_control.json", "{broken")
    else:
        _put(mb, "runtime_state.json", "{broken")
    assert _action(mb) == "STOP"


def test_both_holds_give_hold_with_reasons(mb: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    _put(mb, "claude_usage.json", {"observability": "UNAVAILABLE"})
    assert _action(mb) == "HOLD"


# ---------------------------------------------------------------- hold_while_needed


class Script:
    """A fake ``sleep`` that applies one mailbox mutation per call and records audits."""

    def __init__(self, mailbox: Path, audit_path: Path, steps, clock=None) -> None:
        self.mailbox, self.audit_path, self.steps = mailbox, audit_path, list(steps)
        self.calls: list[float] = []
        self.audits: list[dict] = []
        self.clock = clock

    def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)
        self.audits.append(json.loads(self.audit_path.read_text(encoding="utf-8")))
        if self.clock is not None:
            self.clock[0] += 10 * 3600.0  # ten hours pass per poll: time must not matter
        if len(self.calls) > 200:
            raise AssertionError("hold loop did not terminate")
        step = self.steps[len(self.calls) - 1] if len(self.calls) <= len(self.steps) else None
        if step is not None:
            step(self.mailbox)


def _wc(command: str):
    return lambda box: _put(box, "worker_control.json", {"command": command})


def _rs(mode: str):
    return lambda box: _put(box, "runtime_state.json", {"mode": mode})


def _noop(box: Path) -> None:
    return None


def _audit() -> dict:
    return {"run": "a0_310001", "checkpoints": [{"step": 250, "checkpoint_id": "abc"}],
            "cpu_s": 12.5}


def _hold(mb: Path, audit_path: Path, script: Script, poll_s: float = 45.0) -> int:
    return rt.hold_while_needed(mb, audit_path, _audit, sleep=script, poll_s=poll_s)


def test_no_hold_returns_zero_without_sleep_or_audit(mb: Path, tmp_path: Path) -> None:
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [])
    assert _hold(mb, audit, script) == 0
    assert script.calls == [] and not audit.exists()


def test_stop_before_hold_raises(mb: Path, tmp_path: Path) -> None:
    (mb / "STOP").write_text("", encoding="utf-8")
    audit = tmp_path / "hold.json"
    with pytest.raises(StopRequested):
        _hold(mb, audit, Script(mb, audit, []))


def test_resume_only_after_both_holds_released(mb: Path, tmp_path: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    # poll1 both held; release coordinator -> poll2 worker usage hold still active;
    # idle poll -> poll3 still held; clear usage hold -> poll4 continues.
    script = Script(mb, audit, [_wc("CONTINUE"), _noop, _rs("RUNNING")])
    assert _hold(mb, audit, script, poll_s=30.0) == 3
    assert script.calls == [30.0, 30.0, 30.0]
    polls = [a["polls"] for a in script.audits]
    assert all(isinstance(p, int) for p in polls) and polls == sorted(set(polls))


def test_release_in_other_order(mb: Path, tmp_path: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [_rs("IDLE"), _wc("CONTINUE")])
    assert _hold(mb, audit, script) == 2
    assert script.calls == [45.0, 45.0]


def test_removing_worker_control_releases_coordinator_hold(mb: Path, tmp_path: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [lambda box: (box / "worker_control.json").unlink()])
    assert _hold(mb, audit, script) == 1


def test_time_never_resumes(mb: Path, tmp_path: Path, monkeypatch) -> None:
    clock = [time.time()]
    monkeypatch.setattr(time, "time", lambda: clock[0])
    monkeypatch.setattr(time, "monotonic", lambda: clock[0])
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [_noop] * 7 + [_rs("RUNNING")], clock=clock)
    assert _hold(mb, audit, script) == 8
    assert len(script.calls) == 8


def test_unreleased_hold_never_returns(mb: Path, tmp_path: Path) -> None:
    class Done(Exception):
        pass

    def stuck(_seconds: float) -> None:
        stuck.n += 1
        if stuck.n >= 25:
            raise Done

    stuck.n = 0
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    with pytest.raises(Done):
        rt.hold_while_needed(mb, tmp_path / "hold.json", _audit, sleep=stuck, poll_s=1.0)
    assert stuck.n == 25


@pytest.mark.parametrize("stopper", [
    lambda box: (box / "STOP").write_text("", encoding="utf-8"),
    lambda box: _put(box, "request.json", {"command": "STOP"}),
    lambda box: _put(box, "worker_control.json", {"command": "STOP"}),
    lambda box: _put(box, "runtime_state.json", "{corrupt"),
    lambda box: (box / "request.json").unlink(),
])
def test_stop_while_held_raises(mb: Path, tmp_path: Path, stopper) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [_noop, stopper])
    with pytest.raises(StopRequested):
        _hold(mb, audit, script)
    assert len(script.calls) == 2


def test_audit_record_is_audit_only(mb: Path, tmp_path: Path) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    audit = tmp_path / "audit" / "hold.json"
    audit.parent.mkdir()
    script = Script(mb, audit, [_noop, _wc("CONTINUE")])
    assert _hold(mb, audit, script) == 2
    rec = json.loads(audit.read_text(encoding="utf-8"))
    assert rec["kind"] == KIND
    assert rec["pid"] == os.getpid()
    assert isinstance(rec["reasons"], list) and rec["reasons"]
    assert isinstance(rec["polls"], int)
    assert "utc" in rec
    for key, value in _audit().items():
        assert rec[key] == value
    for snap in script.audits:
        assert snap["kind"] == KIND and snap["pid"] == os.getpid()
    raw = audit.read_text(encoding="utf-8").lower()
    assert "resume checkpoint" not in raw and "resume-checkpoint" not in raw
    assert raw.count("resume_checkpoint") == 1  # only inside the NOT_A_... kind
    assert sorted(p.name for p in audit.parent.iterdir()) == ["hold.json"]  # atomic, no temp


@pytest.mark.parametrize("poll_s", [45.0001, 46.0, 3600.0, 0.0, -1.0])
def test_poll_bounds_rejected_while_held(mb: Path, tmp_path: Path, poll_s: float) -> None:
    _put(mb, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [_wc("CONTINUE")])
    with pytest.raises(ValueError):
        _hold(mb, audit, script, poll_s=poll_s)
    assert script.calls == []


@pytest.mark.parametrize("poll_s", [46.0, 0.0])
def test_poll_bounds_rejected_even_without_hold(mb: Path, tmp_path: Path, poll_s) -> None:
    audit = tmp_path / "hold.json"
    with pytest.raises(ValueError):
        _hold(mb, audit, Script(mb, audit, []), poll_s=poll_s)


@pytest.mark.parametrize("poll_s", [45.0, 0.01])
def test_poll_bounds_inclusive_upper(mb: Path, tmp_path: Path, poll_s: float) -> None:
    _put(mb, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    audit = tmp_path / "hold.json"
    script = Script(mb, audit, [_rs("RUNNING")])
    assert _hold(mb, audit, script, poll_s=poll_s) == 1
    assert script.calls == [poll_s]
