"""Runtime-control classifier for job 0014 (standard library only).

Precedence (first match wins):
1. STOP: owner STOP file, own store STOP file, request.json command STOP, worker_control STOP.
2. INVALID (fail closed): any unreadable/malformed control, request not RUN_NEXT for this job and
   task digest, task.md bytes not matching the digest, unknown worker_control command, or a present
   but malformed usage snapshot (used_percent must be null or a finite number in [0, 100]).
3. HOLD: worker_control WAIT_USAGE_RESET, a relevant usage limit observed at >= 85 % or with a
   current warning, or an unreleased persistent latch (safe-boundary hold; never a kill reason).
4. CONTINUE (runtime readiness only; never scientific authority).

Persistent latch (run mode): the first HOLD writes ``USAGE_LATCH.json`` (evidence, UTC) in the
latch directory. It is released only when ALL hold: a usage snapshot observed after the latch,
observability OBSERVED, every relevant limit non-null and < 85 % without warning; and
worker_control CONTINUE issued after the latch. Clearing a field, a stale CONTINUE or elapsed time
never releases it. A release renames the latch to ``USAGE_LATCH_RELEASED_<utc>.json`` (history).
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

MAILBOX = Path(r"X:\Downloads\projects\topo-pilot\agent-handoff")
JOB_ID = "0014"
TASK_SHA256 = "C8B477C2D393836FBC2F0FD6383E16C1A89685575F2BC72D5E680FCFB8C9483D"
USAGE_THRESHOLD = 85.0
STOP, INVALID, HOLD, CONTINUE = "STOP", "INVALID", "HOLD", "CONTINUE"
LATCH = "USAGE_LATCH.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _utc(text) -> datetime | None:
    """Timezone-aware ISO-8601 instant (accepts 'Z' and 1-9 fractional digits), else None."""
    if not isinstance(text, str):
        return None
    match = re.fullmatch(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d{1,9}))?(Z|[+-]\d\d:\d\d)", text)
    if not match:
        return None
    frac = (match.group(2) or "0")[:6].ljust(6, "0")
    zone = "+00:00" if match.group(3) == "Z" else match.group(3)
    try:
        return datetime.fromisoformat(f"{match.group(1)}.{frac}{zone}")
    except ValueError:
        return None


def _percent_ok(used) -> bool:
    if used is None:
        return True
    if isinstance(used, bool) or not isinstance(used, (int, float)):
        return False
    return math.isfinite(used) and 0.0 <= used <= 100.0


def _usage_state(usage) -> tuple[str, str] | None:
    if not isinstance(usage, dict) or not isinstance(usage.get("limits"), list):
        return INVALID, "usage snapshot malformed"
    for limit in usage["limits"]:
        if not isinstance(limit, dict) or not _percent_ok(limit.get("used_percent")):
            return INVALID, f"usage limit malformed: {limit!r}"
    for limit in usage["limits"]:
        if limit.get("relevant") is False:
            continue
        used = limit.get("used_percent")
        if limit.get("warning"):
            return HOLD, f"usage warning on {limit.get('kind')}: {limit.get('warning')}"
        if used is not None and used >= USAGE_THRESHOLD:
            return HOLD, f"usage {limit.get('kind')} at {used}% >= {USAGE_THRESHOLD}%"
    return None


def _audit_identity(mailbox: Path, control: dict) -> tuple[str, str]:
    """Audit mode: job 0014 must be terminal; coordinator hold still holds; no usage latch."""
    try:
        status = _read_json(mailbox / "jobs" / JOB_ID / "status.json")
    except (OSError, ValueError):
        return INVALID, "job 0014 status unreadable"
    if not isinstance(status, dict) or status.get("status") not in ("DONE", "BLOCKED", "FAILED"):
        return INVALID, "audit requires a terminal job 0014 status"
    if status.get("task_sha256") != TASK_SHA256:
        return INVALID, "job 0014 status digest mismatch"
    if control.get("command") == "WAIT_USAGE_RESET":
        return HOLD, "worker_control WAIT_USAGE_RESET"
    if control.get("command") != "CONTINUE":
        return INVALID, f"unknown worker_control command {control.get('command')!r}"
    return CONTINUE, "audit readiness only"


def _base(mailbox: Path, out, mode: str) -> tuple[tuple[str, str], dict, dict]:
    """Stateless classification; also returns parsed control and usage (or {})."""
    if mode not in ("run", "audit"):
        return (INVALID, f"unknown mode {mode!r}"), {}, {}
    if (mailbox / "STOP").exists():
        return (STOP, "owner STOP file"), {}, {}
    if out is not None and (Path(out) / "STOP").exists():
        return (STOP, "own store STOP file"), {}, {}
    try:
        request = _read_json(mailbox / "request.json")
        control = _read_json(mailbox / "worker_control.json")
    except (OSError, ValueError) as exc:
        return (INVALID, f"control unreadable: {type(exc).__name__}"), {}, {}
    if not isinstance(request, dict) or not isinstance(control, dict):
        return (INVALID, "control is not a JSON object"), {}, {}
    if request.get("command") == "STOP":
        return (STOP, "request.json STOP"), control, {}
    if control.get("command") == "STOP":
        return (STOP, "worker_control STOP"), control, {}
    if mode == "audit":
        return _audit_identity(mailbox, control), control, {}
    if (request.get("command"), request.get("job_id"), request.get("task_sha256")) != (
        "RUN_NEXT",
        JOB_ID,
        TASK_SHA256,
    ):
        return (INVALID, "request is not RUN_NEXT for job 0014 with the task digest"), control, {}
    try:
        digest = hashlib.sha256((mailbox / "jobs" / JOB_ID / "task.md").read_bytes()).hexdigest()
    except OSError:
        return (INVALID, "task.md unreadable"), control, {}
    if digest.upper() != TASK_SHA256:
        return (INVALID, "task.md digest mismatch"), control, {}
    if control.get("command") not in ("CONTINUE", "WAIT_USAGE_RESET"):
        return (INVALID, f"unknown worker_control command {control.get('command')!r}"), control, {}
    usage: dict = {}
    usage_path = mailbox / "claude_usage.json"
    if usage_path.exists():
        try:
            usage = _read_json(usage_path)
        except (OSError, ValueError):
            return (INVALID, "usage snapshot unreadable"), control, {}
        found = _usage_state(usage)
        if found and found[0] == INVALID:
            return found, control, {}
        if control.get("command") != "WAIT_USAGE_RESET" and found:
            return found, control, usage
    if control.get("command") == "WAIT_USAGE_RESET":
        return (HOLD, "worker_control WAIT_USAGE_RESET"), control, usage
    return (CONTINUE, "runtime readiness only"), control, usage


def release_ready(latch: dict, control: dict, usage: dict) -> bool:
    """Fresh OBSERVED clearance after the latch plus a coordinator CONTINUE issued after it."""
    latched = _utc(latch.get("utc"))
    observed, issued = _utc(usage.get("observed_at_utc")), _utc(control.get("issued_at_utc"))
    if latched is None or observed is None or issued is None:
        return False
    if observed <= latched or issued <= latched or control.get("command") != "CONTINUE":
        return False
    if usage.get("observability") != "OBSERVED" or _usage_state(usage) is not None:
        return False
    relevant = [x for x in usage.get("limits", []) if x.get("relevant") is not False]
    return bool(relevant) and all(
        x.get("used_percent") is not None and not x.get("warning") for x in relevant
    )


def _write_new(path: Path, obj) -> None:
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, indent=1, sort_keys=True) + "\n")


def classify(
    mailbox: Path = MAILBOX,
    out: Path | None = None,
    mode: str = "run",
    latch_dir: Path | None = None,
) -> tuple[str, str]:
    """Return ``(state, reason)``; in run mode with ``latch_dir`` apply the persistent latch."""
    mailbox = Path(mailbox)
    (state, why), control, usage = _base(mailbox, out, mode)
    if mode != "run" or latch_dir is None or state in (STOP, INVALID):
        return state, why
    latch_path = Path(latch_dir) / LATCH
    now = datetime.now(timezone.utc).isoformat()
    if not latch_path.exists():
        if state == HOLD:
            try:
                _write_new(
                    latch_path,
                    {
                        "utc": now,
                        "reason": why,
                        "control": control,
                        "usage": usage,
                        "mailbox": str(mailbox),
                    },
                )
            except FileExistsError:
                pass
        return state, why
    try:
        latch = _read_json(latch_path)
    except (OSError, ValueError):
        return INVALID, "usage latch unreadable"
    if state == CONTINUE and release_ready(latch, control, usage):
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        record = dict(latch, released_utc=now, release_control=control, release_usage=usage)
        _write_new(Path(latch_dir) / f"USAGE_LATCH_RELEASED_{stamp}.json", record)
        os.replace(latch_path, Path(latch_dir) / f"USAGE_LATCH_superseded_{stamp}.json")
        return CONTINUE, "latch released on fresh observed clearance and coordinator CONTINUE"
    return HOLD, f"persistent usage latch since {latch.get('utc')} ({latch.get('reason')})"


def classify_all(mailboxes, out: Path | None = None, mode: str = "run") -> tuple[str, str]:
    """Most restrictive state across mailboxes. The real mailbox latches in ``out``; a synthetic
    mailbox latches in its own directory (so synthetic checks never touch the real latch)."""
    order = {STOP: 0, INVALID: 1, HOLD: 2, CONTINUE: 3}
    results = []
    for mailbox in mailboxes:
        real = Path(mailbox) == MAILBOX
        results.append(classify(mailbox, out, mode, (out if real else mailbox)))
    return min(results, key=lambda r: order[r[0]])
