"""BUILDER tests (not independent): spec v2.3 guards: supervisor-inclusive stage limiter,
finalization reserve, strict release/scoring authority, and source integrity before payload I/O.
Synthetic counters and files only. See BUILDER_TESTS.md."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.analysis
REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "x4_circle_history"
for extra in (TOOL, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    sys.path.insert(0, str(extra))

import errors  # noqa: E402
import live_context  # noqa: E402
import meter_bind  # noqa: E402
import release  # noqa: E402

NOT_PASS = (None, "CONTINUE")


def test_stage_limiter_includes_supervisor_and_tail():
    def legacy(*_):
        return NOT_PASS

    limiter = meter_bind.make_stage_limiter(10.0, 8.0, own_cpu=lambda: 1.0, legacy=legacy)
    tail = meter_bind.meter.TAIL_ALLOWANCE_S
    reason, _ = limiter({}, 10.0 - 8.0 - 1.0 - tail, None, 0.0, 1, [])
    assert reason and "stage ceiling" in reason
    assert limiter({}, 0.5, None, 0.0, 1, []) == NOT_PASS


def test_stage_limiter_grows_with_supervisor_cpu():
    supervisor = {"cpu": 0.0}
    limiter = meter_bind.make_stage_limiter(
        5.0, 0.0, own_cpu=lambda: supervisor["cpu"], legacy=lambda *_: NOT_PASS
    )
    assert limiter({}, 1.0, None, 0.0, 1, []) == NOT_PASS
    supervisor["cpu"] = 4.0
    assert "stage ceiling" in limiter({}, 1.0, None, 0.0, 1, [])[0]


def test_stage_limiter_delegates_to_unchanged_global_limiter():
    calls = []

    def legacy(*args):
        calls.append(args)
        return ("global", "CONTINUE")

    limiter = meter_bind.make_stage_limiter(100.0, 0.0, own_cpu=lambda: 0.0, legacy=legacy)
    assert limiter({}, 1.0, None, 0.0, 1, [])[0] == "global" and len(calls) == 1


@pytest.fixture()
def restore_meter(monkeypatch):
    for name in (
        "OUT",
        "LEDGER",
        "EMERGENCY",
        "LOCK",
        "ACTIVE",
        "LOG_DIR",
        "CAP_S",
        "STOP_NEW_S",
        "OUTPUT_CAP",
        "limit_reason",
    ):
        monkeypatch.setattr(meter_bind.meter, name, getattr(meter_bind.meter, name))
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(meter_bind.controls, name, getattr(meter_bind.controls, name))


def test_finalization_reserve_binding(tmp_path, restore_meter):
    meter_bind.bind("0016", "AB", tmp_path, finalization=False)
    assert meter_bind.meter.STOP_NEW_S == 3480.0
    meter_bind.bind("0016", "AB", tmp_path, finalization=True)
    assert meter_bind.meter.STOP_NEW_S == 3600.0


def test_finalization_only_for_export(tmp_path, restore_meter):
    with pytest.raises(SystemExit):
        meter_bind.rewrite_argv(["--stage", "charts", "--finalization", "--label", "x", "--", "c"])


@pytest.mark.parametrize("value", [None, False, True, {}, "token", object(), 1])
def test_require_scoring_denies_non_authority(value):
    with pytest.raises(errors.AccessDenied):
        errors.require_scoring(value)


@pytest.mark.parametrize("scope,sha", [(("feasibility",), "0" * 64), (("scoring",), "0" * 10)])
def test_require_scoring_denies_wrong_scope_or_sha(scope, sha):
    auth = errors.ScoringAuthority("x", sha, scope, "0099")
    with pytest.raises(errors.AccessDenied):
        errors.require_scoring(auth)


def test_require_scoring_accepts_verified_shape():
    errors.require_scoring(errors.ScoringAuthority("x", "0" * 64, ("scoring",), "0099"))


def test_head_without_subprocess_matches_git():
    expected = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert release._head() == expected


def _release(tmp_path, scoring=False, ref=None):
    rel = {"scoring_released": scoring, "job_id": "0099"}
    if ref is not None:
        rel["owner_scoring_release_ref"] = ref
    return rel


def test_scoring_authority_requires_strict_true_and_owner_record(tmp_path):
    record = tmp_path / "owner.md"
    record.write_text("owner approves scoring", encoding="utf-8")
    good = {
        "path": str(record),
        "sha256": hashlib.sha256(record.read_bytes()).hexdigest(),
        "scope": ["scoring"],
    }
    auth = release.scoring_authority(_release(tmp_path, True, good))
    errors.require_scoring(auth)
    for rel in (
        _release(tmp_path, False, good),
        _release(tmp_path, "True", good),
        _release(tmp_path, True, None),
        _release(tmp_path, True, dict(good, sha256="0" * 64)),
        _release(tmp_path, True, dict(good, scope=["feasibility"])),
        _release(tmp_path, True, dict(good, path=str(tmp_path / "missing"))),
    ):
        with pytest.raises(release.ReleaseError):
            release.scoring_authority(rel)


def test_scoring_authority_constructed_only_in_release_and_errors():
    sites = [
        p.name for p in TOOL.glob("*.py") if "ScoringAuthority(" in p.read_text(encoding="utf-8")
    ]
    assert sorted(sites) == ["release.py"]


def test_dirty_source_refused_before_io(tmp_path):
    real = {
        "files": {"tools/x4_circle_history/errors.py": "0" * 64},
        "environment": {"dist_info": []},
    }
    with pytest.raises(RuntimeError, match="frozen file changed"):
        live_context._pin_modules(real)


def test_frozen_file_set_change_refused():
    import freeze_bind

    files = freeze_bind.frozen_files()
    files.pop(next(iter(files)))
    with pytest.raises(RuntimeError, match="file set"):
        live_context._pin_modules({"files": files, "environment": {"dist_info": []}})


def test_release_strict_boolean_in_verify(tmp_path):
    box = tmp_path / "box"
    (box / "jobs" / "0099").mkdir(parents=True)
    (box / "jobs" / "0099" / "task.md").write_bytes(b"t")
    digest = hashlib.sha256(b"t").hexdigest().upper()
    (box / "request.json").write_text(
        json.dumps({"command": "RUN_NEXT", "job_id": "0099", "task_sha256": digest}),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    out.mkdir()
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")
    rel = {
        "schema": release.SCHEMA,
        "job_id": "0099",
        "task_sha256": digest,
        "released_stages": ["identity"],
        "source_commit": release._head(),
        "freeze_sha256": hashlib.sha256(b"{}").hexdigest(),
        "contract_sha256": hashlib.sha256((TOOL / "CONTRACT.json").read_bytes()).hexdigest(),
        "scoring_released": 0,
        "issued_by": "codex-coordinator",
    }
    path = box / "jobs" / "0099" / "RELEASE.json"
    path.write_text(json.dumps(rel), encoding="utf-8")
    with pytest.raises(release.ReleaseError, match="strict boolean"):
        release.verify(path, mailbox=box, out=out)
