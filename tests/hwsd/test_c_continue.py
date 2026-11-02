"""Coordinator 080a3e03 (jobs 0208, 0210; owner addendum 42).

--continue reaches the KD, SAMPLE and SUMMARY pause checks (API §26); KD1 records PASS when
ident_d returns (API §27).
"""

from __future__ import annotations  # noqa: I001

import json
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


class _Stop(BaseException):  # not swallowed by run_kd's per-item except
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


def test_kd1_passes_when_ident_d_returns(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(drec, "pause_or_raise_d", lambda *a, **kw: None)
    monkeypatch.setattr(hk, "g0d", lambda *a, **kw: {"checks": {}})
    monkeypatch.setattr(hk, "ident_d", lambda: {"n": 36, "per_master": {}})

    def stop(*a, **kw):
        calls.append("KD2")
        raise _Stop

    monkeypatch.setattr(hk, "kd2", stop)
    (tmp_path / "store").mkdir()
    with pytest.raises(_Stop):
        hk.run_kd(tmp_path / "store", None, None, "9999", 1)
    gates = [json.loads(x) for x in (tmp_path / "store" / "GATES.jsonl").read_text(
        encoding="utf-8").splitlines()]
    assert [(g["gate"], g["status"]) for g in gates] == [("KD0", "PASS"), ("KD1", "PASS")]
    assert calls == ["KD2"]


def test_kd_end_to_end_with_stub_items_leaves_no_arrays_in_store(tmp_path, monkeypatch):
    """R-0209-2: KD4 runs unbound with output outside the store; KD closes with an obligation."""
    import hwsc_bind
    import hwsd_bind
    import hwsd_dry
    import numpy as np

    store, seen = tmp_path / "store", {}
    store.mkdir()
    monkeypatch.setattr(drec, "pause_or_raise_d", lambda *a, **kw: None)
    monkeypatch.setattr(hk, "g0d", lambda *a, **kw: {"checks": {}})
    monkeypatch.setattr(hk, "ident_d", lambda: {"n": 36, "per_master": {}})
    monkeypatch.setattr(hk, "kd2", lambda: {"status": "PASS"})

    def repro(out):
        d = Path(out) / "stages" / "KD" / "REPRO" / "1" / "s0"
        d.mkdir(parents=True)
        (d / "CHART_CONSTRUCTIONS.json").write_text("{}\n", encoding="utf-8")
        return {"status": "PASS"}

    def seq(out):
        seen.update(active=hwsc_bind.ACTIVE, out=Path(out))
        Path(out).mkdir(parents=True)
        np.savez(Path(out) / "x.npz", a=np.zeros(2))
        return {"status": "PASS"}

    monkeypatch.setattr(hk, "repro_c", repro)
    monkeypatch.setattr(hwsd_dry, "seq_cases", seq)
    monkeypatch.setattr(hk, "kd5", lambda: {"status": "PASS"})
    monkeypatch.setattr(hk, "kd6", lambda job: {"status": "PASS"})
    monkeypatch.setattr(hk, "_audit", lambda: {"status": "PASS", "n_hits": 0})
    with hwsd_bind.bound_hwsd():
        rec = hk.run_kd(store, None, None, "9999", 1)
    assert rec["status"] == "PASS"
    assert seen["active"] is False
    assert store.resolve() not in seen["out"].resolve().parents
    assert not list(store.rglob("*.npz"))
    assert (store / "REGISTRY_OBLIGATION_9999-a1.json").is_file()
    assert drec.lineage_d(store)["status"] == "PASS"


@pytest.mark.parametrize("rel,ended", [("hwsu-store/REGISTRY_OBLIGATION_OF.json", True),
                                       ("REGISTRY_OBLIGATION_OF.json", True),
                                       ("other/REGISTRY_OBLIGATION_OF.json", False)])
def test_reservation_end_accepts_a_root_relative_obligation(rel, ended, tmp_path):
    """R-0213-1: track U names the obligation relative to the root (J8 leaves it open)."""
    import hashlib

    import hwsd_data

    root = tmp_path / "root"
    store = root / "hwsu-store"
    (store / "reservations").mkdir(parents=True)
    (root / "other").mkdir()
    res = store / "RESERVATION_OF.json"
    res.write_text(json.dumps({"id": "RES-HWSU-OF", "state": "ACTIVE"}), encoding="utf-8")
    for d in (store, root / "other"):
        (d / "REGISTRY_OBLIGATION_OF.json").write_text("{}", encoding="utf-8")
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    (store / "reservations" / "RES-HWSU-OF.END.json").write_text(json.dumps({
        "schema": "hws-reservation-end-v1", "reservation_id": "RES-HWSU-OF",
        "reservation_sha256": sha(res), "obligation_file": rel,
        "obligation_sha256": sha(store / "REGISTRY_OBLIGATION_OF.json")}), encoding="utf-8")
    assert hwsd_data.reservation_ended(res, root)["ended"] is ended
