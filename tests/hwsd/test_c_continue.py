"""Coordinator 080a3e03 (job 0208, owner addendum 42).

--continue reaches the KD, SAMPLE and SUMMARY pause checks (API §26).
"""

from __future__ import annotations  # noqa: I001

import sys
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_driver as hd  # noqa: E402
import hwsd_jobs as hj  # noqa: E402
import hwsd_known as hk  # noqa: E402
import hwsd_records as drec  # noqa: E402
import pytest  # noqa: E402


class _Stop(Exception):
    pass


@pytest.mark.parametrize("cmd", ["kd", "sample", "summary"])
def test_cli_passes_continue(cmd, tmp_path, monkeypatch):
    seen = {}

    def fake(*args, **kw):
        seen["cont"] = kw.get("cont", args[-1] if cmd == "summary" else None)
        return {"status": "PASS"}

    monkeypatch.setattr(hd, "run_kd", fake)
    monkeypatch.setattr(hd, "run_sample", fake)
    monkeypatch.setattr(hj, "run_summary", fake)
    cont = str(tmp_path / "continue.json")
    argv = [cmd, "--out", str(tmp_path / "store"), "--job", "9999", "--continue", cont]
    assert hj.main(argv) == 0
    assert seen["cont"] == cont


def test_cli_without_continue_passes_none(tmp_path, monkeypatch):
    seen = {}
    monkeypatch.setattr(hd, "run_kd",
                        lambda *a, **kw: seen.update(cont=kw.get("cont")) or {"status": "PASS"})
    assert hj.main(["kd", "--out", str(tmp_path / "store"), "--job", "9999"]) == 0
    assert seen["cont"] is None


def test_run_kd_hands_cont_to_the_pause_check(tmp_path, monkeypatch):
    seen = {}

    def pause(out, stage, t0, ledger_path=None, cont=None):
        seen.update(stage=stage, cont=cont)
        raise _Stop

    monkeypatch.setattr(drec, "pause_or_raise_d", pause)
    with pytest.raises(_Stop):
        hk.run_kd(tmp_path / "store", None, None, "9999", 1, str(tmp_path / "c.json"))
    assert seen == {"stage": "KD", "cont": str(tmp_path / "c.json")}


def test_sample_and_summary_wrappers_honour_a_continuation(tmp_path, monkeypatch):
    seen = []
    monkeypatch.setattr(drec, "pause_or_raise_d",
                        lambda out, stage, t0, ledger_path=None, cont=None:
                        seen.append((stage, cont)))
    for stage in ("SAMPLE", "SUMMARY"):
        assert hd.paused(tmp_path, stage, 0.0, lambda: {"ok": 1}, "c.json")() == {"ok": 1}
    assert seen == [("SAMPLE", "c.json"), ("SUMMARY", "c.json")]
