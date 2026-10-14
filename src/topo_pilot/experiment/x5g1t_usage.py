"""Worker self-hold latch from actual usage evidence (x5g1-train-v4 §8; API v4 §1).

An observed relevant limit at or above the threshold, or any relevant warning, SETS a persistent
latch. The latch CLEARS only on new OBSERVED evidence (strictly later than the latch) showing
every previously blocking limit present, relevant, numeric, below the threshold and without a
warning, with nothing else blocking. Elapsed time, reset times and the runtime mode are never
consulted; ``UNAVAILABLE`` alone is never a hold. Nothing here invents quotas or reset times.
"""

from __future__ import annotations

import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

THRESHOLD_PERCENT = 85
LATCH_NAME = "usage_hold_latch.json"
LATCH_SCHEMA = "usage-hold-latch-v1"
USAGE_NAME = "claude_usage.json"
_TS = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d{1,7})?(Z|[+-]\d{2}:\d{2})$")


class UsageMalformed(ValueError):
    """Malformed usage evidence or latch; callers treat it as STOP (fail closed)."""


class UsageDecision(NamedTuple):
    action: str  # "CONTINUE" | "HOLD"
    reasons: tuple[str, ...]
    set_latch: dict | None
    clear_latch: bool


def parse_utc(text) -> datetime:
    """ISO 8601 with ``Z`` or ``+hh:mm`` and 0-7 fractional digits -> aware UTC datetime."""
    if not isinstance(text, str):
        raise UsageMalformed(f"timestamp must be a string, got {type(text).__name__}")
    m = _TS.match(text.strip())
    if not m:
        raise UsageMalformed(f"unparseable or naive timestamp {text!r}")
    frac = (m.group(2) or ".0")[1:7].ljust(6, "0")
    tz = "+00:00" if m.group(3) == "Z" else m.group(3)
    try:
        dt = datetime.fromisoformat(f"{m.group(1)}.{frac}{tz}")
    except ValueError as exc:
        raise UsageMalformed(f"invalid timestamp {text!r}") from exc
    return dt.astimezone(timezone.utc)


def _limits(usage) -> list[dict]:
    if not isinstance(usage, dict) or usage.get("observability") not in ("OBSERVED",
                                                                         "UNAVAILABLE"):
        raise UsageMalformed("usage must be an object with observability OBSERVED/UNAVAILABLE")
    limits = usage.get("limits")
    if not isinstance(limits, list):
        raise UsageMalformed("usage limits must be a list")
    for lim in limits:
        if not isinstance(lim, dict) or not isinstance(lim.get("kind"), str) \
                or not isinstance(lim.get("relevant"), bool):
            raise UsageMalformed(f"limit {lim!r} needs a str kind and a bool relevant")
        u = lim.get("used_percent")
        if u is not None and (isinstance(u, bool) or not isinstance(u, (int, float))
                              or not math.isfinite(u) or not 0 <= u <= 100):
            raise UsageMalformed(f"used_percent {u!r} must be null or a number in [0, 100]")
        if lim.get("warning") is not None and not isinstance(lim["warning"], str):
            raise UsageMalformed("warning must be null or a string")
    return limits


def blocking_limits(usage, threshold: float = THRESHOLD_PERCENT) -> list[dict]:
    """Relevant limits with a warning (any observability) or, when OBSERVED, used >= threshold."""
    limits = _limits(usage)
    observed = usage["observability"] == "OBSERVED"
    return [lim for lim in limits if lim["relevant"] and (
        lim.get("warning") is not None
        or (observed and lim.get("used_percent") is not None
            and lim["used_percent"] >= threshold))]


def make_latch(blocking: list[dict], source, now: datetime) -> dict:
    return {"schema": LATCH_SCHEMA, "set_at_utc": now.astimezone(timezone.utc).isoformat(),
            "source": source, "blocking": [{"kind": b["kind"],
                                            "used_percent": b.get("used_percent"),
                                            "warning": b.get("warning")} for b in blocking]}


def _check_latch(latch) -> datetime:
    if not isinstance(latch, dict) or latch.get("schema") != LATCH_SCHEMA:
        raise UsageMalformed("latch has the wrong schema")
    blocking = latch.get("blocking")
    if not isinstance(blocking, list) or not blocking or not all(
            isinstance(b, dict) and isinstance(b.get("kind"), str) for b in blocking):
        raise UsageMalformed("latch blocking must be a non-empty list of {kind: str}")
    return parse_utc(latch.get("set_at_utc"))


def latch_clears(latch, usage, threshold: float = THRESHOLD_PERCENT) -> tuple[bool, str]:
    """True only on new OBSERVED evidence clearing every latched limit (see module doc)."""
    set_at = _check_latch(latch)
    if usage is None:
        return False, "no usage evidence"
    limits = _limits(usage)
    if usage["observability"] != "OBSERVED":
        return False, "usage not OBSERVED"
    if not isinstance(usage.get("source"), str) or usage["source"] == "unavailable":
        return False, "usage source unavailable"
    if parse_utc(usage.get("observed_at_utc")) <= set_at:
        return False, "evidence not newer than the latch"
    for b in latch["blocking"]:
        ok = [lim for lim in limits if lim["kind"] == b["kind"] and lim["relevant"]
              and lim.get("used_percent") is not None and lim["used_percent"] < threshold
              and lim.get("warning") is None]
        if not ok:
            return False, f"latched limit {b['kind']!r} not shown cleared"
    if blocking_limits(usage, threshold):
        return False, "another relevant limit blocks"
    return True, "fresh OBSERVED evidence clears every latched limit"


def usage_decision(usage, latch, now: datetime,
                   threshold: float = THRESHOLD_PERCENT) -> UsageDecision:
    if latch is not None:
        cleared, why = latch_clears(latch, usage, threshold)
        if cleared:
            return UsageDecision("CONTINUE", (), None, True)
        new = [b for b in (blocking_limits(usage, threshold) if usage is not None else [])
               if b["kind"] not in {x["kind"] for x in latch["blocking"]}]
        extended = None
        if new:  # a further limit now blocks: extend the latch so its clearance is required too
            extended = make_latch(list(latch["blocking"]) + new, usage.get("source"), now)
        return UsageDecision("HOLD", (f"usage_latch: {why}",), extended, False)
    if usage is None:
        return UsageDecision("CONTINUE", (), None, False)
    block = blocking_limits(usage, threshold)
    if block:
        kinds = ", ".join(b["kind"] for b in block)
        return UsageDecision("HOLD", (f"usage_blocking: {kinds}",),
                             make_latch(block, usage.get("source"), now), False)
    return UsageDecision("CONTINUE", (), None, False)


def _read(path: Path):
    if not path.exists():
        return None  # only a MISSING file is absence; a present file must hold an object
    try:
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as exc:
        raise UsageMalformed(f"{path.name}: {type(exc).__name__}: {exc}") from exc
    if not isinstance(obj, dict):
        raise UsageMalformed(f"{path.name}: present file holds {type(obj).__name__}, not an object")
    return obj


def _write(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def apply_usage(mailbox: Path, now: datetime | None = None) -> tuple[str, tuple[str, ...]]:
    """Read evidence and latch, apply the decision (set or archive the latch atomically)."""
    mb = Path(mailbox)
    now = now or datetime.now(timezone.utc)
    usage, latch = _read(mb / USAGE_NAME), _read(mb / LATCH_NAME)
    d = usage_decision(usage, latch, now)
    if d.set_latch is not None:
        _write(mb / LATCH_NAME, d.set_latch)
    if d.clear_latch:
        stamp = now.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        _write(mb / f"usage_hold_latch.cleared-{stamp}.json",
               {"latch": latch, "cleared_by": usage, "cleared_at_utc": now.isoformat()})
        (mb / LATCH_NAME).unlink()
    return d.action, d.reasons
