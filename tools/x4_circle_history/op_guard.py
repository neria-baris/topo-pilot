"""Native-operation wall guard, child side (API.md spec v2.4 item 7; builder-tested).

timed_factory returns the `timed(label, fn)` hook that fit_chart/extend call around each heavy
operation. It records every attempt in OPERATIONS.jsonl and keeps OPERATION_ACTIVE.json
current. The PRIMARY enforcement is the existing meter supervisor loop: meter_bind's stage
limiter reads the marker at every poll and has the unchanged meter kill the Job Object once
the deadline passes. The post-return check here is secondary only. No thread, no watcher.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from errors import Unresolved

MARKER = "OPERATION_ACTIVE.json"
LOG = "OPERATIONS.jsonl"


def _utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_marker(out: Path, record: dict) -> None:
    tmp = Path(out) / (MARKER + ".tmp")
    tmp.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    os.replace(tmp, Path(out) / MARKER)


def _log(out: Path, record: dict) -> None:
    with (Path(out) / LOG).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(record, utc=_utc()), sort_keys=True) + "\n")


def timed_factory(out: Path, wall_s: float, clock=time.monotonic, wall_clock=time.time):
    out, wall_s, state = Path(out), float(wall_s), {"seq": 0}

    def timed(label: str, fn):
        state["seq"] += 1
        seq = state["seq"]
        _log(out, {"event": "start", "seq": seq, "label": label, "deadline_s": wall_s})
        write_marker(
            out,
            {
                "state": "active",
                "seq": seq,
                "label": label,
                "started_epoch": wall_clock(),
                "deadline_s": wall_s,
                "pid": os.getpid(),
            },
        )
        t0 = clock()
        try:
            result = fn()
        except BaseException as exc:
            write_marker(out, {"state": "idle", "seq": seq, "label": label})
            _log(out, {"event": "error", "seq": seq, "label": label, "type": type(exc).__name__})
            raise
        elapsed = clock() - t0
        write_marker(out, {"state": "idle", "seq": seq, "label": label})
        _log(out, {"event": "end", "seq": seq, "label": label, "elapsed_s": elapsed})
        if elapsed >= wall_s:
            _log(out, {"event": "exhausted", "seq": seq, "label": label, "elapsed_s": elapsed})
            raise Unresolved(f"native operation {label} exceeded its {wall_s} s wall")
        return result

    return timed


def overdue(marker_path: Path, now_epoch: float):
    """Kill reason if the marker shows an active operation past its deadline, else None.

    Used by the supervisor limiter; an absent, idle or (transiently) unreadable marker is None.
    """
    try:
        record = json.loads(Path(marker_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if record.get("state") != "active":
        return None
    if now_epoch - float(record["started_epoch"]) >= float(record["deadline_s"]):
        return (
            f"native operation wall {record['deadline_s']}s exceeded: "
            f"{record.get('label')} (seq {record.get('seq')})"
        )
    return None


def archive_stale(out: Path):
    """Move a stale ACTIVE marker (killed attempt) to operations/KILLED_<seq>.json; return path."""
    path = Path(out) / MARKER
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if record.get("state") != "active":
        return None
    dest_dir = Path(out) / "operations"
    dest_dir.mkdir(exist_ok=True)
    dest = (
        dest_dir
        / f"KILLED_{record.get('seq')}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    )
    with dest.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(record, archived_utc=_utc()), sort_keys=True) + "\n")
    path.unlink()
    return dest
