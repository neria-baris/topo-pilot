"""Coordinator-written regression test for defect D-0181-1 (API.md §24): g0c checks the store's
lineage before it writes stages/<stage>/G0C.json, which is recorded only when the stage completes.
Authority files, the stage-B handoff and the seed search are synthetic (monkeypatched); the store
is a tmp_path store holding only its FREEZE.json."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402
import hwsc_known  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

SCHED = {"record": "SCHED_9999", "live_history_reservations": [],
         "frozen_registries_awaiting_draw": []}


def _file(p: Path, text: str) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _setup(tmp_path, monkeypatch):
    root, out = tmp_path / "root", tmp_path / "root" / "hwsc-store"
    auth = {"owner_addenda": {}, "kc0_addenda": ["34"]}
    auth["owner_addenda"]["34"] = {"path": "a/ADD34.md", "sha256": _file(root / "a/ADD34.md", "34")}
    ra = _file(root / "a/ADD36.md", "36")
    auth["run_approval"] = {"path": "a/ADD36.md", "sha256": ra}
    hw = _file(root / "b/FREEZE.json", "{}")
    auth["hwsb_freeze_json"] = {"path": str(root / "b/FREEZE.json"), "sha256": hw}
    for name in ("selection_json", "hws_final_report"):
        auth[name] = {"path": str(root / f"c/{name}"), "sha256": _file(root / f"c/{name}", name)}
    monkeypatch.setitem(cc.CONTRACT, "authority", auth)
    monkeypatch.setattr(cc, "load_handoff", lambda: {"freeze_sha256": hw})
    monkeypatch.setattr(hwsc_known, "seed_search_c", lambda r, n: [])
    monkeypatch.setattr(hwsc_known, "classify_hits_c", lambda h: {"status": "PASS", "hits": []})
    out.mkdir(parents=True)
    (out / "FREEZE.json").write_text(json.dumps({"run_approval_sha256": ra}), encoding="utf-8")
    return root, out, {"run_approval_sha256": ra}


def test_g0c_passes_on_a_store_holding_only_its_freeze(tmp_path, monkeypatch):
    root, out, auth = _setup(tmp_path, monkeypatch)
    checks = hwsc_known.g0c(out, "KC", auth, SCHED, root=root)
    assert checks["lineage"]["status"] == "PASS"
    assert (out / "stages" / "KC" / "G0C.json").is_file()


def test_g0c_still_fails_closed_on_an_unrecorded_file(tmp_path, monkeypatch):
    root, out, auth = _setup(tmp_path, monkeypatch)
    _file(out / "stages" / "KC" / "stray.json", "{}")
    with pytest.raises(C1GateFailure) as exc:
        hwsc_known.g0c(out, "KC", auth, SCHED, root=root)
    assert "LINEAGE" in str(exc.value.args[0])
    assert not (out / "stages" / "KC" / "G0C.json").exists()
