"""BUILDER tests (not independent) for spec v2.4 items 7, 11, 12 and 13: native-operation wall
guard (op_guard + meter_bind limiter, one short real metered kill on a temporary store), disk
safe-STOP, ledger allocation sync, dependency manifest and numerical identity. Injected clocks;
nothing waits 180 s. See BUILDER_TESTS.md."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.analysis
REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "x4_circle_history"
for extra in (TOOL, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    sys.path.insert(0, str(extra))

import env_identity  # noqa: E402
import meter_bind  # noqa: E402
import op_guard  # noqa: E402
from errors import Unresolved  # noqa: E402

BASE_PYTHON = Path(sys.base_prefix) / "python.exe"


def _events(out):
    return [json.loads(x) for x in (out / op_guard.LOG).read_text(encoding="utf-8").splitlines()]


def test_timed_records_start_end_and_marker(tmp_path):
    timed = op_guard.timed_factory(tmp_path, 180.0)
    assert timed("ph", lambda: 7) == 7
    assert [e["event"] for e in _events(tmp_path)] == ["start", "end"]
    marker = json.loads((tmp_path / op_guard.MARKER).read_text(encoding="utf-8"))
    assert marker["state"] == "idle" and marker["label"] == "ph"


def test_timed_error_is_logged_and_reraised(tmp_path):
    timed = op_guard.timed_factory(tmp_path, 180.0)
    with pytest.raises(ZeroDivisionError):
        timed("smoothing", lambda: 1 / 0)
    assert [e["event"] for e in _events(tmp_path)] == ["start", "error"]


def test_timed_post_return_check_with_injected_clock(tmp_path):
    ticks = iter([0.0, 180.0])
    timed = op_guard.timed_factory(tmp_path, 180.0, clock=lambda: next(ticks))
    with pytest.raises(Unresolved, match="exceeded"):
        timed("distance", lambda: None)
    assert _events(tmp_path)[-1]["event"] == "exhausted"


def _marker(tmp_path, started, deadline=180.0, state="active"):
    op_guard.write_marker(
        tmp_path,
        {"state": state, "seq": 3, "label": "ph", "started_epoch": started, "deadline_s": deadline},
    )
    return tmp_path / op_guard.MARKER


def test_limiter_kills_overdue_operation_only(tmp_path):
    path = _marker(tmp_path, started=1000.0)
    legacy = lambda *a: (None, "CONTINUE")  # noqa: E731
    for now, expected in ((1179.9, None), (1180.0, "native operation wall")):
        limiter = meter_bind.make_stage_limiter(
            1e9, 0.0, own_cpu=lambda: 0.0, legacy=legacy, op_marker=path,
            op_clock=lambda now=now: now, disk=None,
        )  # fmt: skip
        reason, _ = limiter({}, 0.0, None, 0.0, 1, [])
        assert (reason is None) if expected is None else expected in reason
    _marker(tmp_path, started=0.0, state="idle")
    assert op_guard.overdue(path, 1e12) is None


def test_disk_safe_stop_reason():
    class Usage:
        def __init__(self, free):
            self.free = free

    assert meter_bind.disk_reason(lambda d: Usage(10**12)) is None
    low_c = meter_bind.disk_reason(lambda d: Usage(10**9 if d.startswith("C") else 10**12))
    assert low_c and "C:" in low_c
    limiter = meter_bind.make_stage_limiter(
        1e9,
        0.0,
        own_cpu=lambda: 0.0,
        legacy=lambda *a: (None, "CONTINUE"),
        disk=lambda: "disk safe-STOP: x",
    )
    assert limiter({}, 0.0, None, 0.0, 8, [])[0] == "disk safe-STOP: x"


def test_archive_stale_marker(tmp_path):
    _marker(tmp_path, started=0.0)
    dest = op_guard.archive_stale(tmp_path)
    assert dest.name.startswith("KILLED_3_") and not (tmp_path / op_guard.MARKER).exists()
    assert op_guard.archive_stale(tmp_path) is None


def _ledger(caps, entries):
    return {
        "schema": "x4-oracle-profile-ledger-v1",
        "cumulative_cpu_s": 0.0,
        "cumulative_measured_cpu_s": 0.0,
        "cumulative_tail_allowance_s": 0.0,
        "created_utc": "keep",
        "stage_caps_s": caps,
        "entries": entries,
    }


def test_ledger_allocation_sync_preserves_entries(tmp_path):
    res = meter_bind.CONTRACT["resources"]
    old = res["allocation_history"][0]["stage_caps_s"]
    entries = [{"label": "implementation__a", "charged_cpu_s": 1.5, "x": [1, 2]}]
    path = tmp_path / "cpu_ledger.json"
    path.write_text(json.dumps(_ledger(old, entries)), encoding="utf-8")
    assert meter_bind.sync_ledger_caps(path) is True
    new = json.loads(path.read_text(encoding="utf-8"))
    assert new["entries"] == entries and new["created_utc"] == "keep"
    assert new["stage_caps_s"] == res["stage_caps_s"]
    assert new["allocation_history"][-1]["from"] == old and "owner_override" in new
    assert meter_bind.sync_ledger_caps(path) is False
    path.write_text(json.dumps(_ledger({"oracle": 1}, entries)), encoding="utf-8")
    with pytest.raises(SystemExit, match="neither"):
        meter_bind.sync_ledger_caps(path)


DRIVER = r"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[2]); sys.path.insert(0, sys.argv[3])
import meter_bind
out = Path(sys.argv[1])
meter_bind.CONTRACT["resources"]["output_root"] = str(out)
sys.argv = ["meter_bind", "--stage", "implementation", "--label", "opwall", "--max-wall", "60",
            "--", sys.argv[4], "-I", sys.argv[5], str(out), sys.argv[2]]
sys.exit(meter_bind.main())
"""
CHILD = r"""
import sys, time
sys.path.insert(0, sys.argv[2])
import op_guard
op_guard.timed_factory(sys.argv[1], 1.0)("sleepy", lambda: time.sleep(20))
"""


def test_real_meter_kills_overdue_marked_operation(tmp_path):
    out = tmp_path / "store"
    out.mkdir()
    caps = meter_bind.CONTRACT["resources"]["stage_caps_s"]
    (out / "cpu_ledger.json").write_text(json.dumps(_ledger(caps, [])), encoding="utf-8")
    lock = {"session": meter_bind.meter.WORKER_SESSION}
    (out / "RUN.lock").write_text(json.dumps(lock), encoding="utf-8")
    (tmp_path / "driver.py").write_text(DRIVER, encoding="utf-8")
    (tmp_path / "child.py").write_text(CHILD, encoding="utf-8")
    oracle_tools = str(REPO / "tools" / "x4_oracle_profile")
    start = time.monotonic()
    cmd = [str(BASE_PYTHON), "-I", str(tmp_path / "driver.py"), str(out), str(TOOL), oracle_tools]
    cmd += [sys.executable, str(tmp_path / "child.py")]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert time.monotonic() - start < 15, done.stderr
    entry = json.loads((out / "cpu_ledger.json").read_text(encoding="utf-8"))["entries"][-1]
    assert entry["status"] == "KILLED", (entry, done.stdout, done.stderr)
    assert "native operation wall 1.0s exceeded: sleepy" in entry["killed_reason"]
    assert op_guard.archive_stale(out).name.startswith("KILLED_1_")  # what rewrite_argv calls


def test_frozen_files_bind_project_dependencies():
    import freeze_bind

    files = freeze_bind.frozen_files()
    contracts = {p for p in files if p.startswith("src/topo_pilot/contracts/")}
    assert "src/topo_pilot/contracts/__init__.py" in contracts and len(contracts) >= 10
    assert {"src/topo_pilot/__init__.py", "src/topo_pilot/dataset/sampler.py"} <= set(files)
    assert not any("__pycache__" in p for p in files)


def test_unfrozen_project_module_detected():
    fake = type(sys)("fake_mod")
    fake.__file__ = str(REPO / "src" / "topo_pilot" / "analysis" / "f1.py")
    ok = type(sys)("ok_mod")
    ok.__file__ = str(REPO / "src" / "topo_pilot" / "__init__.py")
    bad = env_identity.unfrozen_project_modules(
        {"src/topo_pilot/__init__.py"}, {"fake_mod": fake, "ok_mod": ok}
    )
    assert bad == ["fake_mod: src/topo_pilot/analysis/f1.py"]


def test_numerical_identity_record_is_deterministic():
    import numpy

    first = env_identity.record({"numpy": numpy})
    assert first == env_identity.record({"numpy": numpy})
    assert set(first["distributions"]) == {"numpy", "numpy.libs"}
    assert first["python"]["stdlib_lib_tree"] and first["limitation"]
    assert set(first["informational_verified"]) == {
        "platform", "processor", "numpy_cpu_features", "threadpools",
    }  # fmt: skip
