"""X5 G1 training-study runtime controls (x5g1-train-v3 §8–§9).

STOP from the owner file, ``request.json`` or ``worker_control.json`` always wins; malformed
critical controls fail closed. A usage hold pauses the LIVE process (optimizer, scheduler and
batch RNG stay in memory) and resumes only when both the coordinator hold and the worker's own
usage hold are released; time never resumes it. The hold record is audit-only, never a resume
checkpoint. Budget checks at boundaries are periodic, not an instruction-level CPU kill.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

from .x4b_run import peak_memory_bytes
from .x5g1_controls import BudgetExceeded, RunControls, StopRequested
from .x5g1_safety import OutputExists

EST = {"update": 0.383, "dev_ce": 3.92, "score": 3.906, "save": 1.0, "bootstrap": 120.0,
       "exports": 60.0}
MAX_POLL_S = 45.0
AUDIT_KIND = "AUDIT_ONLY_NOT_A_RESUME_CHECKPOINT"


class ControlState(NamedTuple):
    action: str  # "CONTINUE" | "HOLD" | "STOP"
    reasons: tuple[str, ...]


class RunLocked(RuntimeError):
    """A run lock or an outcome already exists; a second start is refused (no retry)."""


class ResourceExceeded(RuntimeError):
    """Peak RAM or new-output storage over its cap, or peak RAM unknown (fail closed)."""


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_controls(mailbox: Path) -> ControlState:
    """Precedence STOP > HOLD > CONTINUE (API §5); ``claude_usage.json`` is never read."""
    mb = Path(mailbox)
    stop: list[str] = []
    hold: list[str] = []
    if (mb / "STOP").exists():
        stop.append("owner_stop_file")
    try:
        cmd = _json(mb / "request.json")["command"]
        if cmd == "STOP":
            stop.append("request_stop")
        elif cmd != "RUN_NEXT":
            stop.append(f"request_unknown_command:{cmd!r}")
    except Exception as exc:  # noqa: BLE001 - missing or malformed critical control
        stop.append(f"request_unreadable:{type(exc).__name__}")
    wc = mb / "worker_control.json"
    if wc.exists():
        try:
            cmd = _json(wc)["command"]
            if cmd == "STOP":
                stop.append("worker_control_stop")
            elif cmd == "WAIT_USAGE_RESET":
                hold.append("coordinator_usage_hold")
            elif cmd != "CONTINUE":
                stop.append(f"worker_control_unknown_command:{cmd!r}")
        except Exception as exc:  # noqa: BLE001
            stop.append(f"worker_control_unreadable:{type(exc).__name__}")
    rs = mb / "runtime_state.json"
    if rs.exists():
        try:
            if _json(rs)["mode"] == "WAIT_USAGE_RESET":
                hold.append("worker_usage_hold")
        except Exception as exc:  # noqa: BLE001
            stop.append(f"runtime_state_unreadable:{type(exc).__name__}")
    if stop:
        return ControlState("STOP", tuple(stop))
    if hold:
        return ControlState("HOLD", tuple(hold))
    return ControlState("CONTINUE", ())


def _atomic_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")
    os.replace(tmp, path)


def _utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def hold_while_needed(mailbox: Path, audit_path: Path, audit: Callable[[], dict],
                      sleep: Callable[[float], None] | None = None,
                      poll_s: float = MAX_POLL_S) -> int:
    """Hold the live process until controls say CONTINUE; STOP raises. Returns held polls.

    ``sleep`` defaults to ``time.sleep`` resolved at call time (injectable for tests).
    """
    sleep = sleep or time.sleep
    if not 0 < poll_s <= MAX_POLL_S:
        raise ValueError(f"poll_s must be in (0, {MAX_POLL_S}], got {poll_s}")
    polls = 0
    while True:
        state = read_controls(mailbox)
        if state.action == "STOP":
            raise StopRequested("controls: " + ", ".join(state.reasons))
        if state.action == "CONTINUE":
            return polls
        _atomic_json(audit_path, {"kind": AUDIT_KIND, "pid": os.getpid(),
                                  "reasons": list(state.reasons), "polls": polls,
                                  "utc": _utc(), **audit()})
        sleep(poll_s)
        polls += 1


class RunLock:
    """Exclusive lock file for one live model run; removed on exit, never suppresses errors."""

    def __init__(self, path: Path, identity: dict) -> None:
        self.path, self.identity = Path(path), identity

    def __enter__(self) -> RunLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RunLocked(f"run lock {self.path} exists (live or unknown run)") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump({"pid": os.getpid(), "identity": self.identity, "utc": _utc()}, fh)
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.path.unlink(missing_ok=True)
        return False


def outcome_path(root: Path, arm: str, master) -> Path:
    return Path(root) / "outcomes" / f"{arm}_{master}.json"


def read_outcome(root: Path, arm: str, master) -> dict | None:
    p = outcome_path(root, arm, master)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def record_outcome(root: Path, arm: str, master, outcome: dict) -> Path:
    p = outcome_path(root, arm, master)
    if p.exists():
        raise OutputExists(f"outcome {p} already recorded")
    _atomic_json(p, outcome)
    return p


def assert_can_start(root: Path, arm: str, master, lock_path: Path) -> None:
    if Path(lock_path).exists():
        raise RunLocked(f"run lock {lock_path} exists")
    if outcome_path(root, arm, master).exists():
        raise RunLocked(f"{arm}/{master} already has a recorded outcome; no retry")


class BudgetPlanner:
    """Proceed iff ``cumulative + factor * next_estimate + reserve <= cap``."""

    def __init__(self, cap_s: float = 21600.0, factor: float = 1.5) -> None:
        self.cap_s, self.factor = cap_s, factor

    def check(self, cumulative_now: float, next_estimate: float, reserve: float,
              what: str) -> None:
        need = cumulative_now + self.factor * next_estimate + reserve
        if need > self.cap_s:
            raise BudgetExceeded(f"{what}: {cumulative_now:.1f} + {self.factor} x "
                                 f"{next_estimate:.1f} + reserve {reserve:.1f} > {self.cap_s}")


def interval_estimate(updates: int, est: dict = EST) -> float:
    return updates * est["update"] + est["dev_ce"] + est["save"]


def evaluation_reserve(unscored_checkpoints: int, unscored_final: int, est: dict = EST,
                       factor: float = 1.5) -> float:
    return factor * (unscored_checkpoints * est["score"] + 60.0 + unscored_final * est["score"]
                     + 60.0 + est["bootstrap"] + est["exports"])


def dir_size(path: Path) -> int:
    p = Path(path)
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.exists() else 0


def check_resources(peak_bytes: int | None, storage_bytes: int, ram_cap: int = 8 * 2**30,
                    storage_cap: int = 2 * 2**30) -> None:
    if peak_bytes is None:
        raise ResourceExceeded("peak memory unavailable (fail closed)")
    if peak_bytes > ram_cap:
        raise ResourceExceeded(f"peak memory {peak_bytes} > {ram_cap}")
    if storage_bytes > storage_cap:
        raise ResourceExceeded(f"new storage {storage_bytes} > {storage_cap}")


class StudyControls:
    """Guard, controls (with live hold), boundary budget and resources at one boundary."""

    def __init__(self, ctl: RunControls, mailbox: Path, planner: BudgetPlanner, out_root: Path,
                 audit_path: Path, sleep: Callable[[float], None] | None = None,
                 poll_s: float = MAX_POLL_S) -> None:
        self.ctl, self.mailbox, self.planner = ctl, Path(mailbox), planner
        self.out_root, self.audit_path = Path(out_root), Path(audit_path)
        self.sleep, self.poll_s = sleep, poll_s
        self.held_polls = 0

    def boundary(self, what: str, next_estimate: float, reserve: float,
                 audit: Callable[[], dict] = dict) -> None:
        self.ctl.guard(what)
        state = read_controls(self.mailbox)
        if state.action == "STOP":
            raise StopRequested(f"{what}: " + ", ".join(state.reasons))
        if state.action == "HOLD":
            def full_audit() -> dict:
                return {"at": what, "cpu_snapshot_s": round(self.ctl.cpu(), 3), **audit()}
            self.held_polls += hold_while_needed(self.mailbox, self.audit_path, full_audit,
                                                 self.sleep, self.poll_s)
        self.planner.check(self.ctl.prior + self.ctl.cpu(), next_estimate, reserve, what)
        check_resources(peak_memory_bytes(), dir_size(self.out_root))
