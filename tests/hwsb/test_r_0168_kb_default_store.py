"""Regression D-0168-1 (coordinator 08ad4eaf, job 0168).

run_kb with no store must build its own LocalFSBackend store. The real KB job calls
run_kb(out, auth, sched) without a store; the tests and the dry run always passed one,
so the default path raised AttributeError (hd.LocalFSBackend) before KB0.
KB0 is stubbed here to stop at once.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_driver as hdr  # noqa: E402
import hwsb_known as hk  # noqa: E402


def test_run_kb_default_store_reaches_kb0(tmp_path, monkeypatch):
    def stop(out, auth, sched):
        raise hc.HwsbStop("FAIL_TECHNICAL/SEED_SCOPE", "stub KB0")

    monkeypatch.setattr(hk, "kb0", stop)
    monkeypatch.setattr(hdr, "pause_or_raise", lambda *a, **k: None)
    rec = hk.run_kb(tmp_path, None, None)
    assert rec["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    assert rec["kb"]["KB1"] == {"status": "NOT_RUN"}
    on_disk = json.loads(
        (tmp_path / "stages" / "KB" / "KB_RECORD.json").read_text(encoding="utf-8")
    )
    assert on_disk["status"] == rec["status"]
    # D-0170-1: the API §13 record fields are present
    assert on_disk["deviation_flags"] == []
    assert set(on_disk["threads"]) == {"KB2", "KB3"}
    assert on_disk["freeze_sha256"] is None
