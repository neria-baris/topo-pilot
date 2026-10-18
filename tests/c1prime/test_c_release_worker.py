"""Coordinator regression test (job 0035, ruling R10): `c1_release.authorized_worker` takes the
executing worker session from a verified release (protocol §18: "the authorized executing
worker session"), requires the job's task.md to name it, and falls back to the CONTRACT default
when the release has no `worker_session`. Pure function; no meter, no store, no git."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_oracle_profile", "tools/x4_circle_history", "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_config  # noqa: E402
import c1_release  # noqa: E402

SESSION = "11111111-2222-4333-8444-555555555555"


def _job(tmp_path, task_text):
    job = tmp_path / "jobs" / "0099"
    job.mkdir(parents=True)
    (job / "task.md").write_text(task_text, encoding="utf-8")
    return job / "release_R1.json"


def test_release_session_named_in_task(tmp_path):
    rel_path = _job(tmp_path, f"Who may claim: worker **{SESSION}** only.\n")
    assert c1_release.authorized_worker({"worker_session": SESSION}, rel_path) == SESSION


def test_release_session_not_in_task_is_refused(tmp_path):
    rel_path = _job(tmp_path, "Who may claim: someone else.\n")
    with pytest.raises(c1_release.ReleaseError):
        c1_release.authorized_worker({"worker_session": SESSION}, rel_path)


@pytest.mark.parametrize("bad", ["", 7, None.__class__])
def test_malformed_release_session_is_refused(tmp_path, bad):
    rel_path = _job(tmp_path, f"{SESSION}\n")
    with pytest.raises(c1_release.ReleaseError):
        c1_release.authorized_worker({"worker_session": bad}, rel_path)


def test_no_release_session_falls_back_to_contract(tmp_path):
    rel_path = _job(tmp_path, "anything\n")
    expected = str(c1_config.CONTRACT["resources"]["worker_session"])
    assert c1_release.authorized_worker({}, rel_path) == expected
