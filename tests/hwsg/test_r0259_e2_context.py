"""R-0259-1: run_e2 sets ctx["test_acts"] as stage C does, and every ctx key read after H2-FRESH
is present (API.md section 25)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import mod  # noqa: E402


def test_run_e2_context_reaches_t_pre_endpoint_ratio_and_export(tmp_path, monkeypatch):
    jobs, gc = mod("hwsg_jobs"), mod("gc")
    store = tmp_path / "hwsg-store"
    (store / "registry").mkdir(parents=True)
    (store / "registry" / "K-REG2.json").write_text("{}", encoding="utf-8")
    wd = gc.world_dir(store, "lo")
    wd.mkdir(parents=True)
    seen = {}

    def t_pre_spy(out, ctx):
        for k in ("proc", "test", "Z", "test_acts"):
            assert k in ctx, k
        seen["acts"] = ctx["test_acts"](0, "step5000")
        ctx["test_arrays"], ctx["controls"] = {}, {}
        return {}

    def endpoint_spy(ctx):
        for k in ("test_arrays", "controls", "test", "Z"):
            assert k in ctx, k
        ctx["result"] = {"per_model": {}}
        return {}

    def ratio_spy(ctx, result, b4, seed, out=None):
        assert "test_arrays" in ctx and result is ctx["result"]
        seen["ratio"] = True
        return {"status": "DEFINED", "files": []}

    def export_spy(world_dir, result, oc, ann, fill, ratio_files):
        seen["export"] = Path(world_dir)
        return Path(world_dir) / "RESULT.json"

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
        lambda *a, **k: {
            "proc": {"perm": {0: "P0"}},
            "Z": 0,
            "models": {(0, "step5000"): "M"},
            "reservation_path": wd / "R.json",
        },
    )
    monkeypatch.setattr(jobs.hwsg_registry, "recheck", lambda r: None)
    monkeypatch.setattr(jobs.hwsc_data, "sample_test_c", lambda *a, **k: {"canon32": np.zeros(2)})
    monkeypatch.setattr(jobs.k4b_fresh, "require_release_b", lambda *a, **k: {"N": 1, "k": 1})
    monkeypatch.setattr(jobs.hwsc_data, "h2_fresh_c", lambda out, ctx: {})
    monkeypatch.setattr(
        importlib.import_module("k4b_data"), "model_inputs", lambda c, perm: ("in", perm)
    )
    monkeypatch.setattr(importlib.import_module("c1_model"), "activations", lambda m, x: (m, x))
    monkeypatch.setattr(jobs.k4b_fresh, "t_pre", t_pre_spy)
    monkeypatch.setattr(jobs.k4b_fresh, "endpoint_gate", endpoint_spy)
    monkeypatch.setattr(jobs.hwsg_ratio, "ratio_gate", ratio_spy)
    monkeypatch.setattr(jobs.hwsc_outcome, "annotations", lambda r: [])
    monkeypatch.setattr(jobs.stage_records, "gates_so_far", lambda w: [])
    monkeypatch.setattr(jobs.hwsc_outcome, "state_from_gates", lambda g, result=None: {})
    monkeypatch.setattr(jobs.rec, "outcome_g", lambda s: {"outcome": "X", "annotations": []})
    monkeypatch.setattr(jobs.stage_records, "record_gate", lambda *a, **k: None)
    monkeypatch.setattr(jobs.hwsc_jobs, "_fill", lambda r: {})
    monkeypatch.setattr(jobs.rec, "export_g", export_spy)
    out = jobs.run_e2(store, "lo", {}, {})
    assert out["status"] == "PASS", out
    assert seen["acts"] == ("M", ("in", "P0"))
    assert seen["ratio"] and seen["export"] == wd
