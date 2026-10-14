"""BUILDER tests (not independent): runtime-control classifier on synthetic mailboxes only.

Written by the job-0014 builder after the coordinator pre-freeze reviews; see BUILDER_TESTS.md.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.oracle
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "x4_oracle_profile"))
import controls  # noqa: E402

TASK = b"synthetic task body\n"
DIGEST = hashlib.sha256(TASK).hexdigest().upper()


@pytest.fixture()
def box(tmp_path, monkeypatch):
    monkeypatch.setattr(controls, "TASK_SHA256", DIGEST)
    (tmp_path / "jobs" / "0014").mkdir(parents=True)
    (tmp_path / "jobs" / "0014" / "task.md").write_bytes(TASK)
    write(
        tmp_path, "request.json", {"command": "RUN_NEXT", "job_id": "0014", "task_sha256": DIGEST}
    )
    write(tmp_path, "worker_control.json", {"command": "CONTINUE"})
    write(tmp_path, "claude_usage.json", usage(None, None))
    return tmp_path


def write(root: Path, name: str, obj) -> None:
    (root / name).write_text(json.dumps(obj), encoding="utf-8")


def usage(percent, warning, relevant=True) -> dict:
    return {
        "limits": [
            {"kind": "session", "used_percent": percent, "warning": warning, "relevant": relevant}
        ]
    }


def state(root, out=None, mode="run"):
    return controls.classify(root, out, mode)[0]


def test_continue(box):
    assert state(box) == controls.CONTINUE


@pytest.mark.parametrize("where", ["owner", "own"])
def test_stop_files(box, tmp_path_factory, where):
    out = tmp_path_factory.mktemp("out")
    (box if where == "owner" else out).joinpath("STOP").write_text("x")
    assert state(box, out) == controls.STOP


def test_request_and_control_stop(box):
    write(box, "request.json", {"command": "STOP"})
    assert state(box) == controls.STOP
    write(box, "request.json", {"command": "RUN_NEXT", "job_id": "0014", "task_sha256": DIGEST})
    write(box, "worker_control.json", {"command": "STOP"})
    assert state(box) == controls.STOP


def test_stop_beats_invalid_and_hold(box):
    write(box, "worker_control.json", {"command": "STOP"})
    write(box, "claude_usage.json", usage(99, "warn"))
    assert state(box) == controls.STOP
    (box / "STOP").write_text("x")
    (box / "request.json").write_text("{broken")
    assert state(box) == controls.STOP


@pytest.mark.parametrize(
    "request_obj",
    [
        {"command": "RUN_NEXT", "job_id": "0015", "task_sha256": DIGEST},
        {"command": "RUN_NEXT", "job_id": "0014", "task_sha256": "0" * 64},
        {"command": "PAUSE", "job_id": "0014", "task_sha256": DIGEST},
        [1, 2],
    ],
)
def test_invalid_request(box, request_obj):
    write(box, "request.json", request_obj)
    assert state(box) == controls.INVALID


def test_invalid_unreadable_and_task_bytes(box):
    (box / "worker_control.json").write_text("{broken")
    assert state(box) == controls.INVALID
    write(box, "worker_control.json", {"command": "CONTINUE"})
    (box / "jobs" / "0014" / "task.md").write_bytes(b"changed")
    assert state(box) == controls.INVALID
    (box / "jobs" / "0014" / "task.md").unlink()
    assert state(box) == controls.INVALID


def test_invalid_unknown_control_and_usage(box):
    write(box, "worker_control.json", {"command": "GO"})
    assert state(box) == controls.INVALID
    write(box, "worker_control.json", {"command": "CONTINUE"})
    for bad in (None, [], {"limits": "x"}, {"limits": [3]}, usage("85", None)):
        write(box, "claude_usage.json", bad)
        assert state(box) == controls.INVALID
    (box / "claude_usage.json").write_text("{broken")
    assert state(box) == controls.INVALID


def test_holds(box):
    write(box, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert state(box) == controls.HOLD
    write(box, "worker_control.json", {"command": "CONTINUE"})
    for percent, warning, expected in (
        (85, None, controls.HOLD),
        (85.0, None, controls.HOLD),
        (84.9, None, controls.CONTINUE),
        (None, "approaching", controls.HOLD),
        (None, None, controls.CONTINUE),
    ):
        write(box, "claude_usage.json", usage(percent, warning))
        assert state(box) == expected
    write(box, "claude_usage.json", usage(99, "x", relevant=False))
    assert state(box) == controls.CONTINUE
    (box / "claude_usage.json").unlink()
    assert state(box) == controls.CONTINUE


def test_audit_mode(box):
    assert state(box, mode="audit") == controls.INVALID
    write(box / "jobs" / "0014", "status.json", {"status": "RUNNING", "task_sha256": DIGEST})
    assert state(box, mode="audit") == controls.INVALID
    write(box / "jobs" / "0014", "status.json", {"status": "DONE", "task_sha256": DIGEST})
    write(box, "request.json", {"command": "RUN_NEXT", "job_id": "0015", "task_sha256": "x"})
    assert state(box, mode="audit") == controls.CONTINUE
    write(box, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert state(box, mode="audit") == controls.HOLD
    write(box, "request.json", {"command": "STOP"})
    assert state(box, mode="audit") == controls.STOP
    write(box / "jobs" / "0014", "status.json", {"status": "DONE", "task_sha256": "0"})
    write(box, "request.json", {"command": "RUN_NEXT"})
    write(box, "worker_control.json", {"command": "CONTINUE"})
    assert state(box, mode="audit") == controls.INVALID
    assert state(box, mode="bogus") == controls.INVALID


def test_classify_all_most_restrictive(box, tmp_path_factory):
    other = tmp_path_factory.mktemp("other")
    for name in ("request.json", "worker_control.json", "claude_usage.json"):
        (other / name).write_bytes((box / name).read_bytes())
    (other / "jobs" / "0014").mkdir(parents=True)
    (other / "jobs" / "0014" / "task.md").write_bytes(TASK)
    write(other, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert controls.classify_all([box, other])[0] == controls.HOLD
    (other / "STOP").write_text("x")
    assert controls.classify_all([box, other])[0] == controls.STOP


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1.0, 100.5, True, "50"])
def test_malformed_percent_fails_closed(box, value):
    write(box, "claude_usage.json", usage(value, None))
    assert state(box) == controls.INVALID


def test_utc_parsing_accepts_coordinator_timestamps():
    assert controls._utc("2026-10-14T09:50:07.7178489Z") is not None
    assert controls._utc("2026-10-14T15:12:06.184685+00:00") is not None
    for bad in ("2026-10-14T09:50:07", "yesterday", None, 5):
        assert controls._utc(bad) is None


def latched(box, latch_dir):
    return controls.classify(box, None, "run", latch_dir)


def test_persistent_latch_requires_fresh_clearance_and_release(box, tmp_path_factory):
    latch_dir = tmp_path_factory.mktemp("latch")
    write(box, "claude_usage.json", usage(None, "approaching limit"))
    assert latched(box, latch_dir)[0] == controls.HOLD
    assert (latch_dir / controls.LATCH).exists()
    # Warning cleared but no fresh observed evidence and no coordinator release: still HOLD.
    write(box, "claude_usage.json", usage(None, None))
    assert latched(box, latch_dir)[0] == controls.HOLD
    # Stale CONTINUE (issued before the latch) with fresh observed clearance: still HOLD.
    fresh = dict(
        usage(40.0, None), observability="OBSERVED", observed_at_utc="2099-01-01T00:00:00Z"
    )
    write(box, "claude_usage.json", fresh)
    write(
        box, "worker_control.json", {"command": "CONTINUE", "issued_at_utc": "2000-01-01T00:00:00Z"}
    )
    assert latched(box, latch_dir)[0] == controls.HOLD
    # Fresh coordinator CONTINUE but unavailable (null) percentages: still HOLD.
    write(
        box, "worker_control.json", {"command": "CONTINUE", "issued_at_utc": "2099-01-01T00:00:01Z"}
    )
    write(
        box,
        "claude_usage.json",
        dict(
            fresh,
            limits=[{"kind": "session", "used_percent": None, "warning": None, "relevant": True}],
        ),
    )
    assert latched(box, latch_dir)[0] == controls.HOLD
    write(box, "claude_usage.json", dict(fresh, observability="UNAVAILABLE"))
    assert latched(box, latch_dir)[0] == controls.HOLD
    # Fresh observed clearance AND fresh coordinator CONTINUE: released, history kept.
    write(box, "claude_usage.json", fresh)
    assert latched(box, latch_dir)[0] == controls.CONTINUE
    assert not (latch_dir / controls.LATCH).exists()
    assert len(list(latch_dir.glob("USAGE_LATCH_RELEASED_*.json"))) == 1
    assert len(list(latch_dir.glob("USAGE_LATCH_superseded_*.json"))) == 1


def test_latch_from_coordinator_hold_and_stop_precedence(box, tmp_path_factory):
    latch_dir = tmp_path_factory.mktemp("latch")
    write(box, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert latched(box, latch_dir)[0] == controls.HOLD
    write(box, "worker_control.json", {"command": "CONTINUE"})
    assert latched(box, latch_dir)[0] == controls.HOLD
    write(box, "worker_control.json", {"command": "STOP"})
    assert latched(box, latch_dir)[0] == controls.STOP
    (latch_dir / controls.LATCH).write_text("{broken")
    write(box, "worker_control.json", {"command": "CONTINUE"})
    assert latched(box, latch_dir)[0] == controls.INVALID


def test_classify_all_latches_synthetic_in_its_own_dir(box, tmp_path_factory):
    out = tmp_path_factory.mktemp("out")
    write(box, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert controls.classify_all([box], out)[0] == controls.HOLD
    assert (box / controls.LATCH).exists() and not (out / controls.LATCH).exists()
