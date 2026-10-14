"""Shared job-0014 runtime helpers: safe-boundary control guard and immutable NPZ export."""

from __future__ import annotations

import io
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tests" / "oracle_profile"))

import controls  # noqa: E402
import inputs  # noqa: E402
import oracle_profile as op  # noqa: E402

CFG = inputs.load_config()
OUT = Path(CFG["output_root"])
SPLITS = tuple(CFG["splits"])


class Stopped(RuntimeError):
    pass


def guard(where: str) -> None:
    """Safe-boundary runtime control check (HOLD waits here; STOP/INVALID raise)."""
    state, why = controls.classify_all([controls.MAILBOX], OUT)
    held = False
    while state == controls.HOLD:
        if not held:
            with (OUT / "HOLD_EVENTS.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "event": "HOLD",
                            "where": where,
                            "reason": why,
                            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        }
                    )
                    + "\n"
                )
            held = True
        time.sleep(30)
        state, why = controls.classify_all([controls.MAILBOX], OUT)
    if held:
        with (OUT / "HOLD_EVENTS.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"event": "RESUME", "where": where, "state": state}) + "\n")
    if state != controls.CONTINUE:
        raise Stopped(f"{state} at {where}: {why}")


def headroom(extra: int) -> None:
    used = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    if used + extra > CFG["output_cap_bytes"]:
        raise op.ProfileError("output cap would be exceeded")


def save_npz(path: Path, **arrays) -> str:
    buffer = io.BytesIO()
    np.savez_compressed(buffer, **arrays)
    data = buffer.getvalue()
    headroom(len(data))
    with path.open("xb") as handle:
        handle.write(data)
    return inputs.sha256(path)
