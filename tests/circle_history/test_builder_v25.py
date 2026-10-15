"""BUILDER tests (not independent) for spec v2.5 (job 0017): release issuer binding for the
designated Claude coordinator, measure-only CPU policy under the owner override, and the
[0, 2pi) phase interval (F4). Synthetic temporary mailboxes and stores only."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.analysis
REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "x4_circle_history"
for extra in (TOOL, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    sys.path.insert(0, str(extra))

import chart as ch  # noqa: E402
import meter_bind  # noqa: E402
import release  # noqa: E402

SESSION = "c351b245-9ff3-4f5c-b324-60ee25725fd7"


def _mailbox(tmp_path, mode="ACTIVE_CLAUDE_COORDINATOR", issuer="claude-coordinator"):
    box = tmp_path / "box"
    (box / "jobs" / "0099").mkdir(parents=True)
    task = b"synthetic release task\n"
    (box / "jobs" / "0099" / "task.md").write_bytes(task)
    digest = hashlib.sha256(task).hexdigest().upper()
    request = {"command": "RUN_NEXT", "job_id": "0099", "task_sha256": digest}
    (box / "request.json").write_text(json.dumps(request), encoding="utf-8")
    (box / "coordinator_runtime.json").write_text(json.dumps({"mode": mode}), encoding="utf-8")
    (box / "archive" / "incoming").mkdir(parents=True)
    assumption = box / "archive" / "incoming" / "ASSUMPTION.json"
    assumption.write_text(
        json.dumps({"schema": "coordinator-assumption-v1", "coordinator_session_id": SESSION}),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    out.mkdir()
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")
    rel = {
        "schema": release.SCHEMA,
        "job_id": "0099",
        "task_sha256": digest,
        "released_stages": ["identity", "oracle", "charts", "precision", "export"],
        "source_commit": release._head(),
        "freeze_sha256": hashlib.sha256(b"{}").hexdigest(),
        "contract_sha256": hashlib.sha256((TOOL / "CONTRACT.json").read_bytes()).hexdigest(),
        "scoring_released": False,
        "issued_by": issuer,
    }
    if issuer == "claude-coordinator":
        rel["coordinator_session_id"] = SESSION
        rel["coordinator_assumption_ref"] = {
            "path": str(assumption),
            "sha256": hashlib.sha256(assumption.read_bytes()).hexdigest().upper(),
        }
    return box, out, rel


def _verify(box, out, rel):
    path = box / "jobs" / "0099" / "RELEASE.json"
    path.write_text(json.dumps(rel), encoding="utf-8")
    return release.verify(path, mailbox=box, out=out)


def test_claude_release_verifies(tmp_path):
    box, out, rel = _mailbox(tmp_path)
    assert _verify(box, out, rel)["issued_by"] == "claude-coordinator"


def _mutations(box, rel, tmp_path):
    ref = rel["coordinator_assumption_ref"]
    other = tmp_path / "outside.json"
    other.write_bytes(Path(ref["path"]).read_bytes())
    wrong_schema = box / "archive" / "incoming" / "WRONG.json"
    wrong_schema.write_text(
        json.dumps({"schema": "other", "coordinator_session_id": SESSION}), encoding="utf-8"
    )
    return {
        "wrong session": {"coordinator_session_id": "00000000-0000-0000-0000-000000000000"},
        "wrong sha": {"coordinator_assumption_ref": dict(ref, sha256="0" * 64)},
        "wrong schema": {
            "coordinator_assumption_ref": {
                "path": str(wrong_schema),
                "sha256": hashlib.sha256(wrong_schema.read_bytes()).hexdigest(),
            }
        },
        "outside archive": {"coordinator_assumption_ref": dict(ref, path=str(other))},
        "missing session": {"coordinator_session_id": None},
        "missing ref": {"coordinator_assumption_ref": None},
        "unknown issuer": {"issued_by": "someone-else"},
    }


@pytest.mark.parametrize(
    "case",
    [
        "wrong session",
        "wrong sha",
        "wrong schema",
        "outside archive",
        "missing session",
        "missing ref",
        "unknown issuer",
    ],
)
def test_claude_release_refuses_bad_binding(tmp_path, case):
    box, out, rel = _mailbox(tmp_path)
    for key, value in _mutations(box, rel, tmp_path)[case].items():
        if value is None:
            rel.pop(key)
        else:
            rel[key] = value
    with pytest.raises(release.ReleaseError):
        _verify(box, out, rel)


def test_claude_release_refused_when_runtime_not_claude_active(tmp_path):
    box, out, rel = _mailbox(tmp_path, mode="RELINQUISHED")
    with pytest.raises(release.ReleaseError, match="active Claude coordinator"):
        _verify(box, out, rel)


def test_codex_release_verifies_only_while_not_relinquished(tmp_path):
    box, out, rel = _mailbox(
        tmp_path, mode="ISOLATED_IMPLEMENTATION_RUNNING", issuer="codex-coordinator"
    )
    assert _verify(box, out, rel)["issued_by"] == "codex-coordinator"
    (box / "coordinator_runtime.json").write_text(
        json.dumps({"mode": "ACTIVE_CLAUDE_COORDINATOR"}), encoding="utf-8"
    )
    with pytest.raises(release.ReleaseError, match="relinquished"):
        _verify(box, out, rel)


def test_codex_release_with_claude_fields_refused(tmp_path):
    box, out, rel = _mailbox(
        tmp_path, mode="ISOLATED_IMPLEMENTATION_RUNNING", issuer="codex-coordinator"
    )
    rel["coordinator_session_id"] = SESSION
    with pytest.raises(release.ReleaseError, match="must not carry"):
        _verify(box, out, rel)


def test_missing_runtime_file_fails_closed(tmp_path):
    box, out, rel = _mailbox(tmp_path)
    (box / "coordinator_runtime.json").unlink()
    with pytest.raises(release.ReleaseError, match="unreadable"):
        _verify(box, out, rel)


@pytest.fixture()
def measured(tmp_path, monkeypatch):
    """The real v2.5 CONTRACT (measure-only policy) bound to a temporary store."""
    contract = copy.deepcopy(meter_bind.CONTRACT)
    assert contract["resources"]["cpu_policy"] == "MEASURE_ONLY_OWNER_OVERRIDE"
    contract["resources"]["output_root"] = str(tmp_path)
    monkeypatch.setattr(meter_bind, "CONTRACT", contract)
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(meter_bind.controls, name, getattr(meter_bind.controls, name))
    for name in ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S", "STOP_NEW_S"):
        monkeypatch.setattr(meter_bind.meter, name, getattr(meter_bind.meter, name))
    monkeypatch.setattr(meter_bind.meter, "limit_reason", meter_bind.meter.limit_reason)
    return tmp_path


def _ledger(out, entries, policy=None):
    ledger = {
        "schema": "x4-oracle-profile-ledger-v1",
        "entries": entries,
        "stage_caps_s": meter_bind.CONTRACT["resources"]["stage_caps_s"],
        "created_utc": "keep",
    }
    if policy:
        ledger["cpu_policy"] = policy
    (out / "cpu_ledger.json").write_text(json.dumps(ledger), encoding="utf-8")


def test_measure_only_never_stops_on_cpu(measured):
    _ledger(measured, [{"label": "implementation__a", "charged_cpu_s": 1e6}])
    args = meter_bind.rewrite_argv(
        ["--stage", "implementation", "--label", "t", "--max-cpu", "5", "--", "cmd"]
    )
    assert args[args.index("--label") + 1] == "implementation__t"
    assert args[args.index("--max-cpu") + 1] == "inf" and args.count("--max-cpu") == 1
    assert args[-1] == "cmd"
    assert meter_bind.meter.CAP_S == float("inf") and meter_bind.meter.STOP_NEW_S == float("inf")


def test_measure_only_unreleased_stage_still_refused(measured):
    _ledger(measured, [])
    args = meter_bind.rewrite_argv(["--stage", "charts", "--label", "t", "--", "cmd"])
    assert args[args.index("--label") + 1].endswith("__REFUSED_stage_ceiling_or_unreleased")
    assert args[-1] == "raise SystemExit(4)"


def test_measure_only_limiter_has_no_cpu_reason_but_keeps_other_guards(tmp_path):
    legacy = lambda *a: (None, "CONTINUE")  # noqa: E731
    limiter = meter_bind.make_stage_limiter(
        float("inf"), 1e9, own_cpu=lambda: 1e9, legacy=legacy, disk=None
    )
    assert limiter({}, 1e12, None, 0.0, 1, [])[0] is None
    disk = meter_bind.make_stage_limiter(
        float("inf"), 0.0, own_cpu=lambda: 0.0, legacy=legacy, disk=lambda: "disk safe-STOP: x"
    )
    assert disk({}, 0.0, None, 0.0, 8, [])[0] == "disk safe-STOP: x"


def test_ledger_policy_sync_preserves_entries(measured):
    entries = [{"label": "implementation__a", "charged_cpu_s": 2.5, "nested": {"k": [1]}}]
    _ledger(measured, entries)
    path = measured / "cpu_ledger.json"
    assert meter_bind.sync_ledger_caps(path) is True
    new = json.loads(path.read_text(encoding="utf-8"))
    assert new["entries"] == entries and new["created_utc"] == "keep"
    assert new["cpu_policy"] == "MEASURE_ONLY_OWNER_OVERRIDE"
    assert new["allocation_history"][-1]["policy"] == "MEASURE_ONLY_OWNER_OVERRIDE"
    assert meter_bind.sync_ledger_caps(path) is False


def test_wrap_maps_two_pi_to_zero():
    two_pi = 2.0 * np.pi
    raw = np.array([-1e-17, -0.0, 0.5, two_pi, 3 * two_pi - 1e-17])
    assert np.any(raw % two_pi >= two_pi)  # precondition: the plain modulo reaches 2pi
    out = ch._wrap(raw)
    assert np.all((out >= 0.0) & (out < two_pi))
    assert out[0] == 0.0 and out[2] == 0.5


def test_apply_gauge_never_returns_two_pi():
    gauge = ch.Gauge(sign=1, shift=1e-17, alignment=1.0)
    phi = ch.apply_gauge(np.array([0.0, 1.0]), gauge)
    assert phi[0] == 0.0 and np.all(phi < 2.0 * np.pi)


def _equidistant_chart(phases):
    d = len(phases) // 2 + 1
    eye = np.eye(d)
    landmarks = np.vstack([eye, -eye])[: len(phases)]
    zeros = np.zeros(1)
    return ch.Chart(
        landmark_ids=np.array([f"h{k:02d}" for k in range(len(phases))]),
        landmarks=landmarks,
        phi=np.asarray(phases, dtype=np.float64),
        sigma=1.0,
        support_radius=10.0,
        d8=np.ones(len(phases)),
        edges=zeros,
        cocycle=zeros,
        integer_lift=zeros,
        lift_correction=zeros,
        primitive=zeros,
        tree_potential=zeros,
        period_gcd=1,
    )


def test_extend_never_returns_two_pi():
    """A query equidistant from 8 landmarks whose mean angle is a tiny negative number."""
    cfg = {"extension_k": 8, "support_min_resultant": 0.2}
    gauge = ch.Gauge(sign=1, shift=0.0, alignment=1.0)
    for delta in (1e-16, 2e-16, 5e-17, 3e-16, 4e-17, 1.5e-16):
        phases = [0.1] * 4 + [-0.1 - delta] * 4 + [1.0, 2.0]
        chart = _equidistant_chart(phases)
        q = np.zeros((1, chart.landmarks.shape[1]))
        phi_g = ch.apply_gauge(chart.phi, gauge)[:8]
        raw = np.angle(np.exp(1j * phi_g).sum() / 8.0) % (2.0 * np.pi)  # extend's z
        if raw >= 2.0 * np.pi:
            break
    else:
        pytest.fail("no synthetic case reached 2pi under the plain modulo")
    ext = ch.extend(chart, gauge, q, cfg)
    assert ext.phase[0] == 0.0
