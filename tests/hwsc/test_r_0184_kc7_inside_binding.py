"""Coordinator-written regression test for defect D-0184-1 (API.md §26): run_kc runs every KC
item inside the stage-C binding, and KC7 compares unbound and bound calls. Inside the binding KC7
raised "code drift"; under hwsc_bind.suspended() it passes, and the outer binding is re-applied
afterwards and removed at its exit."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402,F401
import hwsc_bind  # noqa: E402
import hwsc_known  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402


def _values(rows):
    return [getattr(importlib.import_module(r["module"]), r["name"]) for r in rows]


def test_kc7_inside_the_binding_needs_suspension():
    with hwsc_bind.bound_stage_c():
        with pytest.raises(C1GateFailure, match="code drift"):
            hwsc_known.kc7()


def test_kc7_passes_under_suspended_and_the_binding_is_reapplied():
    rows = hwsc_bind.load_table()
    unbound = _values(rows)
    with hwsc_bind.bound_stage_c():
        bound = _values(rows)
        with hwsc_bind.suspended():
            assert hwsc_bind.ACTIVE is False
            assert all(a is b for a, b in zip(_values(rows), unbound))
            assert hwsc_known.kc7()["status"] == "PASS"
        assert hwsc_bind.ACTIVE is True
        assert all(a is b for a, b in zip(_values(rows), bound))
    assert hwsc_bind.ACTIVE is False
    assert all(a is b for a, b in zip(_values(rows), unbound))


def test_suspended_outside_a_binding_is_a_no_op():
    with hwsc_bind.suspended():
        assert hwsc_bind.ACTIVE is False
