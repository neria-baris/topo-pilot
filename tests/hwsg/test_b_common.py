"""Shared helpers of author B (no tests here). Imports are lazy so collection never fails."""
from __future__ import annotations

import importlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _p in (REPO / "tools" / "hwsg",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

ALIASES = {"gc": "hwsg_config", "gb": "hwsg_bind", "gh": "hwsg_handoff", "go": "hwsg_oracle",
           "gt": "hwsg_train", "gr": "hwsg_registry", "gq": "hwsg_ratio", "gx": "hwsg_cross",
           "grec": "hwsg_records"}
TAGS = ("lo", "mid", "hi")
CONTRACT = json.loads((REPO / "tools" / "hwsg" / "CONTRACT.json").read_text(encoding="utf-8"))
GIB = 1024 ** 3


def mod(alias_or_name):
    name = ALIASES.get(alias_or_name, alias_or_name)
    try:
        if name != "hwsg_config" and "hwsg_config" not in sys.modules:
            importlib.import_module("hwsg_config")  # sets sys.path for reused tools first
        return importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001  the code may not exist yet
        pytest.fail(f"cannot import {name}: {type(exc).__name__}: {exc}")


def status_of(exc) -> str:
    s = getattr(exc, "status", None)
    return str(s if s is not None else (exc.args[0] if exc.args else exc))


def expect_fail(status_prefix, fn, *a, **k):
    gc = mod("gc")  # noqa: F841  ensure sys.path
    c1 = importlib.import_module("c1_records")
    with pytest.raises(c1.C1GateFailure) as ei:
        fn(*a, **k)
    got = status_of(ei.value)
    assert got.startswith(status_prefix) or status_prefix in str(ei.value), got
    return ei.value


def ok_of(r) -> bool:
    # API-AMBIGUITY: dict results carry "ok" or a "status" == "PASS"
    return bool(r["ok"]) if "ok" in r else r.get("status") == "PASS"


def sha_bytes(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def is_incomplete(out: dict) -> bool:
    return bool(out.get("other")) or "INCOMPLETE" in str(out.get("status"))


F = Fraction
