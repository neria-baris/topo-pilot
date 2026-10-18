"""Maintenance regression: real Windows launcher grandchildren, no research data or training.

These are implementation-author tests, not independent protocol acceptance tests.
"""
import dataclasses
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = [pytest.mark.learner, pytest.mark.skipif(os.name != "nt", reason="Win32 jobs")]
REPO = Path(__file__).resolve().parents[2]
for directory in ("tools/d2a", "tools/x4_oracle_profile"):
    sys.path.insert(0, str(REPO / directory))

from d2a_train import Limits, Supervisor  # noqa: E402
from process_tree import TrainingProcess  # noqa: E402


def launch_grandchild(tmp_path):
    ready = tmp_path / "ready.json"
    code = ("import time,json; from pathlib import Path; "
            "data=bytearray(32*1024**2); start=time.process_time(); "
            "exec('while time.process_time()-start < .2: pass'); "
            f"Path({str(ready)!r}).write_text(json.dumps(time.process_time()-start)); "
            "time.sleep(30)")
    launcher = ("import subprocess,sys; "
                f"subprocess.Popen([sys.executable,'-c',{code!r}])")
    child = TrainingProcess([sys.executable, "-c", launcher],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 15
        while not ready.exists():
            if time.monotonic() > deadline:
                raise AssertionError("synthetic grandchild never became ready")
            time.sleep(.02)
        child.process.wait(timeout=5)
        return child, json.loads(ready.read_text())
    except BaseException:
        child.terminate()
        child.close()
        raise


def test_exited_launcher_does_not_hide_live_grandchild_or_its_usage(tmp_path):
    child, measured = launch_grandchild(tmp_path)
    try:
        assert child.process.returncode == 0
        assert child.poll() is None
        assert child.cpu_s() >= measured * .8
        assert child.memory_bytes() >= 32 * 1024**2
        before = child.cpu_s()
        child.terminate()
        assert child.poll() == 0  # root exited normally; the whole tree is now drained
        assert child.cpu_s() >= before  # exited grandchildren remain charged
    finally:
        child.terminate()
        child.close()


@pytest.mark.parametrize("limit,reason", [
    ({"model_cpu_s": .05}, "INCOMPLETE:MODEL_CPU"),
    ({"process_mem": 1024**2}, "INCOMPLETE:PROCESS_MEMORY"),
])
def test_supervisor_enforces_limits_on_grandchild(tmp_path, limit, reason):
    child, _ = launch_grandchild(tmp_path)
    try:
        supervisor = Supervisor(dataclasses.replace(Limits(), **limit),
                                lambda p: p.cpu_s(), lambda p: p.memory_bytes(),
                                lambda p: p.terminate())
        result = supervisor.check({"synthetic": child}, 0, 0, "stage1")
        assert result["synthetic"]["reason"] == reason
        assert child.poll() is not None
    finally:
        child.terminate()
        child.close()


def test_wave_exception_closes_all_started_trees(tmp_path, monkeypatch):
    import d2a_train as train

    events = []

    class FakeTree:
        def terminate(self):
            events.append("terminate")

        def close(self):
            events.append("close")

    (tmp_path / "cpu_ledger.json").write_text('{"entries":[],"cumulative_cpu_s":0}')
    monkeypatch.setattr(train, "_launch", lambda *args: FakeTree())
    monkeypatch.setattr(train.time, "sleep", lambda _: None)

    def fail():
        raise OSError("synthetic monitoring failure")

    monkeypatch.setattr(train, "disk_reason", fail)
    with pytest.raises(OSError, match="monitoring failure"):
        train.wave_main("W1", tmp_path)
    assert events == ["terminate", "close", "terminate", "close"]
    assert not (tmp_path / "waves" / "W1.lock").exists()


@pytest.mark.parametrize("record", ["waves/W1.json", "runs/d2a-s1-H3.json",
                                    "runs/d2a-s2-H3.attempt.json"])
def test_wave_refuses_duplicate_training_before_launch(tmp_path, monkeypatch, record):
    import d2a_train as train

    path = tmp_path / record
    path.parent.mkdir(parents=True)
    path.write_text("historical")
    monkeypatch.setattr(train, "_launch", lambda *args: pytest.fail("duplicate was launched"))
    with pytest.raises(FileExistsError, match="duplicate training"):
        train.wave_main("W1", tmp_path)
    assert path.read_text() == "historical"


def test_concurrent_wave_is_refused_before_launch(tmp_path, monkeypatch):
    import d2a_train as train
    from process_tree import wave_lease

    monkeypatch.setattr(train, "_launch", lambda *args: pytest.fail("overlap was launched"))
    with wave_lease(tmp_path, "W1"):
        with pytest.raises(FileExistsError):
            train.wave_main("W1", tmp_path)
        assert (tmp_path / "waves" / "W1.lock").exists()
    assert not (tmp_path / "waves" / "W1.lock").exists()


@pytest.mark.parametrize("wave", ["../escape", "..\\escape", "X:escape"])
def test_wave_lease_rejects_path_components_before_creating_files(tmp_path, wave):
    from process_tree import wave_lease

    with pytest.raises(ValueError, match="alphanumeric"):
        with wave_lease(tmp_path, wave):
            pytest.fail("invalid lease admitted")
    assert not list(tmp_path.iterdir())
