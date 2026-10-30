"""Coordinator-written regression test for defect D-0181-2 (API.md §25): the KC stage records the
KC9 rehearsal registry files (hwsc-store/registry/rehearsal/) in its STAGE_COMPLETE, so lineage_c
at E1 gate 0 finds them recorded. Preflight, the binding and run_kc's checks are stubbed; the stub
writes what KC1 and KC9 write (an artifact and the three rehearsal file kinds)."""

from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402,F401
import hwsc_driver as cdr  # noqa: E402
import hwsc_known  # noqa: E402


def _write(p: Path, data: bytes) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def _fake_run_kc(out, auth, sched, job, store=None):
    out = Path(out)
    _write(out / "artifacts" / "WorldSpec" / "w1" / "meta.json", b"{}")
    reh = out / "registry" / "rehearsal"
    _write(reh / "REHEARSAL.json", b"{}")
    _write(reh / "REHEARSAL_digests.npz", b"npz")
    _write(reh / "runs" / "REHEARSAL" / "run_00000.npy", b"npy")
    _write(out / "stages" / "KC" / "G0C.json", b"{}")
    rec = {"status": "PASS"}
    _write(out / "stages" / "KC" / "KC_RECORD.json", json.dumps(rec).encode())
    return rec


def test_kc_stage_records_the_rehearsal_registry(tmp_path, monkeypatch):
    out = tmp_path / "hwsc-store"
    out.mkdir()
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cdr, "preflight", lambda *a, **k: {"refused": False})
    monkeypatch.setattr(cdr, "_audit_gate", lambda out: None)
    monkeypatch.setattr(cdr.hwsc_bind, "bound_stage_c", contextlib.nullcontext)
    monkeypatch.setattr(hwsc_known, "run_kc", _fake_run_kc)
    assert cdr.run_kc(out, {}, {}, "9999")["status"] == "PASS"
    assert cdr.lineage_c(out)["status"] == "PASS"
