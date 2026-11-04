"""R-0257-1: run_e2 hands the STORE (not the world folder) to the reused stage-C functions that
read the store-level registry/K-REG2.json (API.md section 24)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import mod  # noqa: E402


def test_run_e2_passes_store_to_release_b_and_h2_fresh(tmp_path, monkeypatch):
    jobs, gc = mod("hwsg_jobs"), mod("gc")
    store = tmp_path / "hwsg-store"
    (store / "registry").mkdir(parents=True)
    (store / "registry" / "K-REG2.json").write_text("{}", encoding="utf-8")
    wd = gc.world_dir(store, "lo")
    wd.mkdir(parents=True)
    seen = {}

    def release_spy(out, rp, session):
        seen["release_b"] = Path(out)
        assert (Path(out) / "registry" / "K-REG2.json").is_file()
        return {"N": 1, "k": 1}

    def h2_spy(out, ctx):
        seen["h2_fresh"] = Path(out)
        assert (Path(out) / "registry" / "K-REG2.json").is_file()
        return {"ok": True}

    def stop(*a, **k):
        raise jobs.C1GateFailure("FAIL_TECHNICAL/STOP", "test stop after H2-FRESH")

    monkeypatch.setattr(jobs.rec, "preflight", lambda *a, **k: {})
    monkeypatch.setattr(
        jobs.rec, "release_barrier", lambda s: {"ok": True, "release_b_missing": []}
    )
    monkeypatch.setattr(jobs, "_audit_gate", lambda *a, **k: None)
    monkeypatch.setattr(jobs.hwsg_handoff, "load", lambda *a, **k: {})
    monkeypatch.setattr(jobs.hwsg_handoff, "as_hwsc", lambda h: h)
    monkeypatch.setattr(
        jobs.hwsc_jobs,
        "e2_context",
        lambda *a, **k: {"proc": {}, "Z": 0, "reservation_path": wd / "R.json"},
    )
    monkeypatch.setattr(jobs.hwsg_registry, "recheck", lambda r: None)
    monkeypatch.setattr(jobs.hwsc_data, "sample_test_c", lambda *a, **k: {"canon32": np.zeros(1)})
    monkeypatch.setattr(jobs.k4b_fresh, "require_release_b", release_spy)
    monkeypatch.setattr(jobs.hwsc_data, "h2_fresh_c", h2_spy)
    monkeypatch.setattr(jobs.k4b_fresh, "t_pre", stop)
    out = jobs.run_e2(store, "lo", {}, {}, dry_continue=False)
    assert seen == {"release_b": store, "h2_fresh": store}
    assert out["status"] != "PASS"
