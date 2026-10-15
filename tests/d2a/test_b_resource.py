"""Independent tests (author B, job 0028): T-RESOURCE for ``d2a_train`` (dispatch identity, meter
binding, supervisor, budgets, disk floors, STOP/HOLD propagation) plus RUNS, WAVES and Limits.

Written from D2A-FROZEN-v1 (§4.1, §4.7, §10.7 S6/S8, §11.3, §11.5, ruling D6) and tools/d2a/API.md
(§2.3) only; no tools/d2a source was read. Everything runs on tmp_path mailboxes, fake module
namespaces and fake process handles; no real mailbox, store, meter or child process is touched.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import re
import sys
import types
from collections import namedtuple
from collections.abc import Mapping
from pathlib import Path

import pytest

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.learner import ModelConfig, TrainConfig

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/d2a", "tools/d1_seam", "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import d2a_train  # noqa: E402
from d2a_train import D2AStop  # noqa: E402

GIB, HOUR = 2**30, 3600.0
JOB, SESSION = "0028", "c0ffee00-0000-4000-8000-000000000028"
TASK_MD = b"# job 0028 (synthetic task for tests)\r\nline two\n"
DIGEST = hashlib.sha256(TASK_MD).hexdigest().upper()


# ---------------------------------------------------------------------- RUNS, WAVES, Limits

def test_runs_are_the_fourteen_registered_models():
    expected = {f"d2a-s{s}-H{h}": (s, h, "CM") for s in range(1, 5) for h in (1, 2, 3)}
    expected.update({f"d2a-s{s}-N": (s, 3, "CC") for s in (1, 2)})
    assert {k: tuple(v) for k, v in d2a_train.RUNS.items()} == expected


def test_waves_follow_the_fixed_order():
    expected = {"W1": ("d2a-s1-H3", "d2a-s2-H3"),
                "W2": ("d2a-s1-H1", "d2a-s1-H2", "d2a-s2-H1"),
                "W3": ("d2a-s2-H2", "d2a-s3-H1", "d2a-s3-H2"),
                "W4": ("d2a-s3-H3", "d2a-s4-H1", "d2a-s4-H2"),
                "W5": ("d2a-s4-H3", "d2a-s1-N", "d2a-s2-N")}
    waves = {k: tuple(v) for k, v in d2a_train.WAVES.items()}
    assert waves == expected and list(d2a_train.WAVES) == list(expected)
    members = [r for w in waves.values() for r in w]
    assert sorted(members) == sorted(d2a_train.RUNS) and len(members) == 14
    assert max(len(w) for w in waves.values()) <= 3  # at most 3 trainings in parallel


def test_training_and_model_configs():
    assert d2a_train.TRAIN_CFG == TrainConfig(
        steps=10000, checkpoint_steps=(0, 1000, 2500, 5000, 7500, 10000), device="cpu")
    assert d2a_train.MODEL_CFG == ModelConfig(vocab_in=6, vocab_out=5)


def test_limits_defaults_are_the_s6_values():
    lim = d2a_train.Limits()
    assert lim.model_cpu_s == 3.5 * HOUR
    assert lim.process_mem == 3 * GIB
    assert dict(lim.stage_cpu_s) == {"preflight": 1 * HOUR, "stage0": 1 * HOUR,
                                     "stage1": 7 * HOUR, "stage2": 42 * HOUR, "stage3": 6 * HOUR}
    assert lim.total_cpu_s == 57 * HOUR
    assert lim.job_mem == 12 * GIB
    assert lim.poll_s == 2.0


# ------------------------------------------------------------------- verify_identity, D6

def _mailbox(tmp_path, *, command="RUN_NEXT", req_job=JOB, req_digest=DIGEST,
             json_digest=DIGEST, task_md=TASK_MD, lock_session=SESSION):
    box = tmp_path / "mailbox"
    for job in (JOB, "0029"):  # a second, equally valid job dir: only the request names one
        jdir = box / "jobs" / job
        jdir.mkdir(parents=True)
        (jdir / "task.json").write_text(json.dumps(
            {"protocol": "handoff-v1", "job_id": job, "task_sha256": json_digest}), "utf-8")
        (jdir / "task.md").write_bytes(task_md)
    (box / "request.json").write_text(json.dumps(
        {"protocol": "handoff-v1", "command": command, "job_id": req_job,
         "task_path": str(box / "jobs" / req_job / "task.md"), "task_sha256": req_digest}),
        "utf-8")
    lock = tmp_path / "store" / "RUN.lock"
    lock.parent.mkdir()
    lock.write_text(json.dumps({"session": lock_session, "purpose": "test"}), "utf-8")
    return box, lock


def test_verify_identity_accepts_the_correct_identity(tmp_path):
    box, lock = _mailbox(tmp_path)
    d2a_train.verify_identity(box, JOB, DIGEST, SESSION, lock)


@pytest.mark.parametrize("call, build", [
    ({"job_id": "0029"}, {}),                                  # wrong job id requested
    ({"task_sha256": "0" * 64}, {}),                           # wrong task digest given
    ({"session": "someone-else"}, {}),                         # wrong executing session
    ({}, {"command": "STOP"}),                                 # request is not RUN_NEXT
    ({}, {"req_job": "0029"}),                                 # request names another job
    ({}, {"req_digest": "F" * 64}),                            # request digest differs
    ({}, {"json_digest": "E" * 64}),                           # task.json digest differs
    ({}, {"task_md": TASK_MD + b"tampered"}),                  # task.md bytes differ
    ({}, {"lock_session": "another-session"}),                 # RUN.lock owned by another
])
def test_verify_identity_rejects_each_wrong_identity(tmp_path, call, build):
    box, lock = _mailbox(tmp_path, **build)
    args = {"job_id": JOB, "task_sha256": DIGEST, "session": SESSION}
    args.update(call)
    with pytest.raises(StageFailure) as info:
        d2a_train.verify_identity(box, args["job_id"], args["task_sha256"], args["session"], lock)
    assert info.value.code == ErrorCode.INVALID_CONFIG


def test_verify_identity_fails_closed_without_a_lock(tmp_path):
    box, lock = _mailbox(tmp_path)
    lock.unlink()
    with pytest.raises(Exception):
        d2a_train.verify_identity(box, JOB, DIGEST, SESSION, lock)


# ------------------------------------------------------------------------- bind_meter, §11.3

def _fakes(tmp_path):
    old = tmp_path / "old-store"
    meter = types.SimpleNamespace(
        OUT=old, LEDGER=old / "cpu_ledger.json", LOCK=old / "RUN.lock",
        EMERGENCY=old / "cpu_ledger.emergency.jsonl", ACTIVE=old / "METER_ACTIVE.lock",
        LOG_DIR=old / "logs", WORKER_SESSION="old-session", CAP_S=3600.0, STOP_NEW_S=3480.0,
        OUTPUT_CAP=128 * 2**20, TAIL_ALLOWANCE_S=0.1, THREAD_VARS=("OMP_NUM_THREADS",))
    controls = types.SimpleNamespace(JOB_ID="0014", TASK_SHA256="C8B4" * 16,
                                     MAILBOX=Path("unchanged-mailbox"), USAGE_THRESHOLD=85.0)
    winjob = types.SimpleNamespace(MEMORY_CAP=8 * GIB, CREATE_SUSPENDED=4)
    return meter, controls, winjob


def test_bind_meter_sets_exactly_the_section_11_3_names(tmp_path):
    meter, controls, winjob = _fakes(tmp_path)
    before = [dict(vars(m)) for m in (meter, controls, winjob)]
    out = tmp_path / "d2a-store"
    d2a_train.bind_meter(meter, controls, winjob, out, JOB, DIGEST, SESSION)
    assert Path(meter.OUT) == out
    assert Path(meter.LEDGER) == out / "cpu_ledger.json"
    assert Path(meter.LOCK) == out / "RUN.lock"
    assert Path(meter.LOG_DIR) == out / "logs"
    for name in ("EMERGENCY", "ACTIVE"):
        assert Path(getattr(meter, name)).parent == out
    paths = {Path(getattr(meter, n)) for n in ("LEDGER", "LOCK", "EMERGENCY", "ACTIVE", "LOG_DIR")}
    assert len(paths) == 5
    assert math.isinf(meter.CAP_S) and meter.CAP_S > 0
    assert math.isinf(meter.STOP_NEW_S) and meter.STOP_NEW_S > 0
    assert meter.OUTPUT_CAP == 4 * GIB
    assert winjob.MEMORY_CAP == 12 * GIB  # the aggregate Job Object memory limit
    assert (controls.JOB_ID, controls.TASK_SHA256, meter.WORKER_SESSION) == (JOB, DIGEST, SESSION)
    expected = [{"OUT", "LEDGER", "LOCK", "EMERGENCY", "ACTIVE", "LOG_DIR", "CAP_S",
                 "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION"}, {"JOB_ID", "TASK_SHA256"},
                {"MEMORY_CAP"}]
    for module, old, names in zip((meter, controls, winjob), before, expected):
        now = vars(module)
        assert set(now) == set(old)  # no new module names
        assert {k for k in now if now[k] != old[k]} == names


# ------------------------------------------------------------------------- Supervisor, S6

class Procs:
    def __init__(self, cpu, mem):
        self.cpu, self.mem, self.killed = dict(cpu), dict(mem), []

    def supervisor(self, limits=None):
        return d2a_train.Supervisor(limits or d2a_train.Limits(), self.cpu.__getitem__,
                                    self.mem.__getitem__, self.killed.append,
                                    clock=lambda: 1000.0)


def _status(reason):
    if isinstance(reason, Mapping):
        found = [v for v in reason.values() if isinstance(v, str) and v.startswith("INCOMPLETE:")]
        assert found, reason
        return found[0]
    return str(reason)


def _poll(reason):
    if isinstance(reason, Mapping):
        return reason.get("polling_interval_s")
    match = re.search(r"polling_interval_s\D*?([0-9.]+)", str(reason))
    return float(match.group(1)) if match else None


CHILDREN = {"d2a-s1-H1": "h1", "d2a-s1-H2": "h2", "d2a-s2-H1": "h3"}


def test_supervisor_quiet_when_every_limit_is_met_exactly():
    lim = d2a_train.Limits()
    procs = Procs({"h1": lim.model_cpu_s, "h2": 10.0, "h3": 10.0},
                  {"h1": 1 * GIB, "h2": lim.process_mem, "h3": 0})
    assert dict(procs.supervisor().check(CHILDREN, 0.0, 0.0, "stage2")) == {}
    assert procs.killed == []


def test_supervisor_model_cpu_kills_only_that_child():
    lim = d2a_train.Limits()
    procs = Procs({"h1": 10.0, "h2": lim.model_cpu_s + 1.0, "h3": 10.0},
                  {"h1": GIB, "h2": GIB, "h3": GIB})
    got = procs.supervisor().check(CHILDREN, 0.0, 0.0, "stage2")
    assert list(got) == ["d2a-s1-H2"] and _status(got["d2a-s1-H2"]) == "INCOMPLETE:MODEL_CPU"
    assert procs.killed == ["h2"]


def test_supervisor_process_memory_kills_only_that_child():
    procs = Procs({"h1": 10.0, "h2": 10.0, "h3": 10.0},
                  {"h1": GIB, "h2": GIB, "h3": 3 * GIB + 1})
    got = procs.supervisor().check(CHILDREN, 0.0, 0.0, "stage2")
    assert list(got) == ["d2a-s2-H1"]
    assert _status(got["d2a-s2-H1"]) == "INCOMPLETE:PROCESS_MEMORY"
    assert procs.killed == ["h3"]


@pytest.mark.parametrize("cpu2, over", [(50.0, True), (40.0, False)])
def test_supervisor_stage_budget_kills_all(cpu2, over):
    lim = d2a_train.Limits()
    children = {"d2a-s1-H3": "a", "d2a-s2-H3": "b"}
    procs = Procs({"a": 60.0, "b": cpu2}, {"a": GIB, "b": GIB})
    spent_stage = lim.stage_cpu_s["stage1"] - 100.0  # remaining 100 s; children use 110 or 100
    got = procs.supervisor().check(children, spent_stage, spent_stage, "stage1")
    if over:
        assert set(got) == set(children) and sorted(procs.killed) == ["a", "b"]
        assert {_status(r) for r in got.values()} == {"INCOMPLETE:STAGE_CPU"}
    else:
        assert dict(got) == {} and procs.killed == []


@pytest.mark.parametrize("cpu3, over", [(5.0, True), (4.0, False)])
def test_supervisor_total_budget_kills_all(cpu3, over):
    lim = d2a_train.Limits()
    procs = Procs({"h1": 3.0, "h2": 3.0, "h3": cpu3}, {"h1": GIB, "h2": GIB, "h3": GIB})
    spent_total = lim.total_cpu_s - 10.0  # the stage itself is far below its ceiling
    got = procs.supervisor().check(CHILDREN, 0.0, spent_total, "stage2")
    if over:
        assert set(got) == set(CHILDREN) and sorted(procs.killed) == ["h1", "h2", "h3"]
        assert {_status(r) for r in got.values()} == {"INCOMPLETE:TOTAL_CPU"}
    else:
        assert dict(got) == {} and procs.killed == []


def test_supervisor_reasons_record_the_polling_interval():
    lim = dataclasses.replace(d2a_train.Limits(), poll_s=3.25)
    procs = Procs({"h1": lim.model_cpu_s * 2, "h2": 1.0, "h3": 1.0},
                  {"h1": GIB, "h2": 4 * GIB, "h3": GIB})
    got = procs.supervisor(lim).check(CHILDREN, 0.0, 0.0, "stage2")
    assert set(got) == {"d2a-s1-H1", "d2a-s1-H2"}
    assert all(_poll(r) == 3.25 for r in got.values())


# ---------------------------------------------------------------- admit and ledger spending

@pytest.mark.parametrize("spent_stage, spent_total, need, ok", [
    (25000.0, 25000.0, 200.0, True),            # remaining stage budget == need: admitted
    (25000.0, 25000.0, 200.5, False),           # remaining stage budget < need
    (0.0, 57 * HOUR - 100.0, 150.0, False),     # total budget binds although the stage is fresh
    (0.0, 57 * HOUR - 150.0, 150.0, True),
])
def test_admit(spent_stage, spent_total, need, ok):
    lim = d2a_train.Limits()
    assert bool(d2a_train.admit("stage1", spent_stage, spent_total, lim, need)) is ok


def test_stage_and_total_spent_on_a_synthetic_ledger():
    ledger = {"schema": "x4-oracle-profile-ledger-v1", "cumulative_cpu_s": 123.5, "entries": [
        {"label": "stage1__W1", "charged_cpu_s": 10.0},
        {"label": "stage1__W1-rerun", "charged_cpu_s": 5.5},
        {"label": "stage10__x", "charged_cpu_s": 1000.0},   # not "stage1__"
        {"label": "stage2__W2", "charged_cpu_s": 7.0},
        {"label": "preflight__tests", "charged_cpu_s": 3.0},
        {"label": "xstage1__y", "charged_cpu_s": 99.0},
    ]}
    assert d2a_train.stage_spent(ledger, "stage1") == pytest.approx(15.5)
    assert d2a_train.stage_spent(ledger, "stage2") == pytest.approx(7.0)
    assert d2a_train.stage_spent(ledger, "stage3") == 0
    assert d2a_train.total_spent(ledger) == 123.5


# --------------------------------------------------------------------- disk floors, S8

Usage = namedtuple("Usage", "total used free")


def _usage(free_c, free_x, broken=""):
    seen = []

    def usage(path):
        drive = str(path).lstrip("\\/")[:1].upper()
        seen.append(drive)
        if drive in broken:
            raise OSError("unreadable")
        free = {"C": free_c, "X": free_x}.get(drive, 10**15)
        return Usage(10**15, 10**15 - free, free)

    return usage, seen


@pytest.mark.parametrize("free_c, free_x, broken, stop", [
    (2_000_000_000, 30_000_000_000, "", False),
    (1_999_999_999, 30_000_000_000, "", True),
    (2_000_000_000, 29_999_999_999, "", True),
    (10**12, 10**13, "C", True),
    (10**12, 10**13, "X", True),
])
def test_disk_reason(free_c, free_x, broken, stop):
    usage, seen = _usage(free_c, free_x, broken)
    reason = d2a_train.disk_reason(usage=usage)
    if stop:
        assert isinstance(reason, str) and reason.startswith("disk safe-STOP")
    else:
        assert reason is None and {"C", "X"} <= set(seen)


# ------------------------------------------------------------------- boundary, STOP/HOLD

def _classify(states):
    it = iter(states)
    calls = []

    def classify():
        calls.append(1)
        return next(it)

    return classify, calls


def test_boundary_continue_returns_at_once():
    classify, calls = _classify([("CONTINUE", "ok")])
    sleeps = []
    d2a_train.boundary(classify, sleeps.append, poll_s=7)
    assert calls == [1] and sleeps == []


def test_boundary_hold_waits_then_continues():
    classify, calls = _classify([("HOLD", "usage"), ("HOLD", "usage"), ("CONTINUE", "ok")])
    sleeps = []
    d2a_train.boundary(classify, sleeps.append, poll_s=7)
    assert len(calls) == 3 and sleeps == [7, 7]


@pytest.mark.parametrize("state", ["STOP", "INVALID"])
@pytest.mark.parametrize("holds", [0, 2])
def test_boundary_stop_and_invalid_raise(state, holds):
    why = f"{state.lower()} reason 42"
    classify, calls = _classify([("HOLD", "usage")] * holds + [(state, why)])
    sleeps = []
    with pytest.raises(D2AStop) as info:
        d2a_train.boundary(classify, sleeps.append, poll_s=7)
    assert why in str(info.value)
    assert len(calls) == holds + 1 and sleeps == [7] * holds
