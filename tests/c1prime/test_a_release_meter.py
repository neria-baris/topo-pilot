"""Independent tests, author A (job 0026): the C1 release schema checks and the meter-binding
rebindings (TEST_PLAN A-6, last two bullets; protocol sections 17 and 18 field 2; API.md
sections 13 and 14).

Everything lives in pytest tmp_path: a synthetic mailbox (request.json, task.md, the coordinator
runtime and assumption records, the authority files), a synthetic store with FREEZE.json, and a
copy of tools/c1prime/CONTRACT.json whose authority hashes and output_root point at them. API.md
lists the stage-specific release fields but not the common ones; the valid fixture therefore
carries the K4 release.py field set (schema, job_id, task_sha256, released_stages, source_commit,
freeze_sha256, contract_sha256, scoring_released, issued_by, the Claude coordinator fields) plus
the C1 fields, and each negative case breaks exactly one binding. The meter tests never launch a
meter: module globals are inspected and restored.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_meter_bind  # noqa: E402
import c1_release  # noqa: E402
import controls  # noqa: E402
import meter  # noqa: E402
import winjob  # noqa: E402

HEAD = "0123456789abcdef0123456789abcdef01234567"
JOB = "0026"
GIB = 1024**3


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def ref(path):
    return {"path": str(path), "sha256": sha(path)}


def world(tmp_path, stages=("oracle",)):
    mb = tmp_path / "agent-handoff"
    task = put(mb / "jobs" / JOB / "task.md", "# job 0026 synthetic task\n")
    task_sha = sha(task).upper()
    put(mb / "request.json", json.dumps({"command": "RUN_NEXT", "job_id": JOB,
                                         "task_sha256": task_sha}))
    put(mb / "coordinator_runtime.json", json.dumps({"mode": "ACTIVE_CLAUDE_COORDINATOR"}))
    assumption = put(mb / "archive" / "coordinator-assumption" / "ASSUMPTION.json", json.dumps(
        {"schema": "coordinator-assumption-v1", "coordinator_session_id": "sess-c1"}))
    owner = put(mb / "archive" / "owner-decisions-20261015" / "OWNER_DECISIONS.md", "A2 A3\n")
    accept = put(mb / "jobs" / "0023" / "review.md", "ACCEPT\n")
    diag = put(tmp_path / "chart-diag-store-0023" / "DIAG.json", '{"verdict": "GO"}\n')
    out = tmp_path / "c1prime-store"
    freeze = put(out / "FREEZE.json", '{"freeze": "synthetic"}\n')
    reg1 = put(out / "REGISTRY_v1.json", '{"version": 1}\n')
    reg2 = put(out / "REGISTRY_v2.json", '{"version": 2}\n')
    contract = json.loads((REPO / "tools" / "c1prime" / "CONTRACT.json").read_text("utf-8"))
    contract["authority"]["owner_decisions"]["sha256"] = sha(owner)
    contract["authority"]["diag_json_sha256"] = sha(diag)
    contract["resources"]["output_root"] = str(out)
    contract_path = put(tmp_path / "CONTRACT.json", json.dumps(contract, indent=1))
    rel = {
        "schema": "c1prime-release-v1",
        "release": {"oracle": "R1", "fresh": "R3"}.get(stages[0], "R2"),
        "job_id": JOB,
        "task_sha256": task_sha,
        "released_stages": list(stages),
        "source_commit": HEAD,
        "freeze_sha256": sha(freeze),
        "contract_sha256": sha(contract_path),
        "scoring_released": False,
        "issued_by": "claude-coordinator",
        "coordinator_session_id": "sess-c1",
        "coordinator_assumption_ref": ref(assumption),
        "authority": {"owner_decisions": ref(owner), "diag_json": ref(diag),
                      "job_0023_accept": ref(accept)},
        "registry_v1": ref(reg1),
    }
    if "fresh" in stages:
        rel.update(N_test=8192, k=2, registry_v2=ref(reg2))
    w = SimpleNamespace(mb=mb, out=out, contract_path=contract_path, rel=rel,
                        path=mb / "jobs" / JOB / "RELEASE.json")
    return w


def verify(w, head=HEAD):
    if w.path.exists():
        w.path.unlink()
    put(w.path, json.dumps(w.rel, indent=1))
    return c1_release.verify(w.path, mailbox=w.mb, out=w.out, head=head,
                             contract_path=w.contract_path)


def test_release_constants():
    assert c1_release.SCHEMA == "c1prime-release-v1"
    assert set(c1_release.STAGES) == {"oracle", "calibration", "validation", "fresh"}


@pytest.mark.parametrize("stages", [("oracle",), ("calibration", "validation"), ("fresh",)])
def test_valid_releases_verify(tmp_path, stages):
    w = world(tmp_path, stages)
    got = verify(w)
    assert got["released_stages"] == list(stages) and got["job_id"] == JOB


def _drop(key):
    return lambda w: w.rel.pop(key)


BREAKS = {
    "schema": lambda w: w.rel.update(schema="x4-circle-history-release-v1"),
    "issuer": lambda w: w.rel.update(issued_by="codex-coordinator"),
    "unknown stage": lambda w: w.rel.update(released_stages=["oracle", "scoring"]),
    "stages not a list": lambda w: w.rel.update(released_stages="oracle"),
    "contract sha": lambda w: w.rel.update(contract_sha256="0" * 64),
    "freeze sha": lambda w: w.rel.update(freeze_sha256="0" * 64),
    "task digest": lambda w: w.rel.update(task_sha256="A" * 64),
    "job id": lambda w: w.rel.update(job_id="0099"),
    "request command": lambda w: put(w.mb / "request.json", json.dumps(
        {"command": "STOP", "job_id": JOB, "task_sha256": w.rel["task_sha256"]})),
    "task.md changed": lambda w: put(w.mb / "jobs" / JOB / "task.md", "edited\n"),
    "runtime mode": lambda w: put(w.mb / "coordinator_runtime.json", '{"mode": "OTHER"}'),
    "assumption sha": lambda w: w.rel["coordinator_assumption_ref"].update(sha256="0" * 64),
    "no session": _drop("coordinator_session_id"),
    "R1 without authority": _drop("authority"),
    "R1 authority incomplete": lambda w: w.rel["authority"].pop("job_0023_accept"),
    "R1 without registry_v1": _drop("registry_v1"),
    "freeze missing": lambda w: (w.out / "FREEZE.json").unlink(),
}


@pytest.mark.parametrize("name", sorted(BREAKS))
def test_each_broken_binding_is_refused(tmp_path, name):
    w = world(tmp_path)
    BREAKS[name](w)
    with pytest.raises(c1_release.ReleaseError):
        verify(w)


def test_source_head_mismatch_is_refused(tmp_path):
    with pytest.raises(c1_release.ReleaseError):
        verify(world(tmp_path), head="f" * 40)


def test_release_outside_the_dispatched_job_directory_is_refused(tmp_path):
    w = world(tmp_path)
    w.path = w.mb / "jobs" / "9999" / "RELEASE.json"
    with pytest.raises(c1_release.ReleaseError):
        verify(w)


@pytest.mark.parametrize("key", ["N_test", "k", "registry_v2"])
def test_r3_needs_n_test_k_and_registry_v2(tmp_path, key):
    w = world(tmp_path, ("fresh",))
    w.rel = copy.deepcopy(w.rel)
    w.rel.pop(key)
    with pytest.raises(c1_release.ReleaseError):
        verify(w)


# ------------------------------------------------------------------- meter binding (API 14)

BOUND = {meter: ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S",
                 "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION", "limit_reason"),
         controls: ("JOB_ID", "TASK_SHA256"), winjob: ("MEMORY_CAP",)}


@pytest.fixture
def restore_meter(monkeypatch):
    for module, names in BOUND.items():
        for name in names:
            monkeypatch.setattr(module, name, getattr(module, name))


def test_bind_rebinds_every_module_level_name(tmp_path, restore_meter):
    out = tmp_path / "c1prime-store"
    digest = "C" * 64
    c1_meter_bind.bind(JOB, digest, out, "sess-worker-1")
    assert controls.JOB_ID == JOB and controls.TASK_SHA256.upper() == digest
    assert Path(meter.OUT) == out
    for name in ("LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR"):
        assert Path(getattr(meter, name)).parent == out, name
    assert Path(meter.LOCK).name == "RUN.lock"
    assert meter.CAP_S == float("inf") and meter.STOP_NEW_S == float("inf")
    assert meter.OUTPUT_CAP == 16 * GIB
    assert winjob.MEMORY_CAP == 12 * GIB
    assert meter.WORKER_SESSION == "sess-worker-1"


def test_k4_meter_bind_is_not_imported_by_the_c1_binding():
    modules = [v for v in vars(c1_meter_bind).values() if isinstance(v, ModuleType)]
    assert all(m.__name__ != "meter_bind" for m in modules)


def usage_of(free_c, free_x):
    def usage(path):
        drive = str(path).upper()[:1]
        if drive not in ("C", "X"):
            raise AssertionError(path)
        return SimpleNamespace(total=10**13, used=0, free={"C": free_c, "X": free_x}[drive])
    return usage


@pytest.mark.parametrize("free_c, free_x, stop", [
    (2_000_000_000, 30_000_000_000, False), (1_999_999_999, 30_000_000_000, True),
    (2_000_000_000, 29_999_999_999, True), (10**12, 10**12, False)])
def test_disk_safe_stop_thresholds(free_c, free_x, stop):
    reason = c1_meter_bind.disk_reason(usage=usage_of(free_c, free_x))
    assert (reason is not None) is stop
    if stop:
        assert isinstance(reason, str) and reason


def test_disk_safe_stop_fails_closed_on_unreadable_drive():
    def broken(path):
        raise OSError("unreadable")
    assert c1_meter_bind.disk_reason(usage=broken)


SENTINEL = (None, "CONTINUE")


def legacy(*args):
    return SENTINEL


def test_limiter_checks_disk_every_eighth_poll_and_never_caps_cpu(tmp_path):
    lim = c1_meter_bind.make_limiter(disk=lambda: "disk low", legacy=legacy, clock=lambda: 0.0)
    assert lim({}, 1e9, None, 1e9, 3, []) == SENTINEL  # huge CPU and wall: no cap
    assert lim({}, 0.0, None, 0.0, 8, [])[0] == "disk low"
    calm = c1_meter_bind.make_limiter(disk=lambda: None, legacy=legacy, clock=lambda: 0.0)
    assert calm({}, 1e12, None, 0.0, 16, []) == SENTINEL


def test_limiter_kills_an_overdue_native_operation(tmp_path):
    marker = tmp_path / "OPERATION_ACTIVE.json"
    marker.write_text(json.dumps({"state": "active", "seq": 3, "label": "integer_lift",
                                  "started_epoch": 1000.0, "deadline_s": 600}), "utf-8")
    late = c1_meter_bind.make_limiter(op_marker=marker, disk=lambda: None, legacy=legacy,
                                      clock=lambda: 1600.0)  # 600 s elapsed: deadline reached
    reason = late({}, 0.0, None, 0.0, 1, [])[0]
    assert isinstance(reason, str) and reason
    early = c1_meter_bind.make_limiter(op_marker=marker, disk=lambda: None, legacy=legacy,
                                       clock=lambda: 1599.0)
    assert early({}, 0.0, None, 0.0, 1, []) == SENTINEL
