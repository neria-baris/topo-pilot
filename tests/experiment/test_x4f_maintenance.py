"""Author-written maintenance regressions on synthetic arrays and temporary stores only."""
import hashlib
import json
import time
from types import SimpleNamespace

import numpy as np
import pytest

from topo_pilot.experiment import x4f_damage, x4f_gates, x4f_probe, x4f_run
from topo_pilot.experiment.x5g1_controls import BudgetExceeded, StopRequested

pytestmark = pytest.mark.experiment


@pytest.mark.parametrize("exc,status", [
    (StopRequested("synthetic STOP"), "stopped"),
    (BudgetExceeded("synthetic budget"), "budget"),
    (ValueError("synthetic export failure"), "error:ValueError"),
    (KeyboardInterrupt(), "error:KeyboardInterrupt"),
])
def test_runner_persists_prior_cpu_and_failure(tmp_path, monkeypatch, exc, status):
    out = tmp_path / "out"
    out.mkdir()
    ledger = out / "cpu_ledger.json"
    prior = {"entries": [{"job": "previous", "cpu_s": 7}], "cumulative_cpu_s": 7}
    ledger.write_text(json.dumps(prior))

    def fail(*args):
        raise exc

    monkeypatch.setattr(x4f_run, "_run_gates", fail)
    with pytest.raises(type(exc)):
        x4f_run.run_gates(tmp_path, tmp_path / "main", out,
                         tmp_path / "tables", tmp_path / "mailbox")
    recorded = json.loads(ledger.read_text())
    assert recorded["entries"][0] == prior["entries"][0]
    assert recorded["entries"][-1]["status"] == status
    assert recorded["cumulative_cpu_s"] >= 7


def test_stop_precedes_any_source_load(tmp_path, monkeypatch):
    (tmp_path / "STOP").touch()
    monkeypatch.setattr(x4f_run, "_run_gates", lambda *args: pytest.fail("source was read"))
    with pytest.raises(StopRequested):
        x4f_run.run_gates(tmp_path, tmp_path / "main", tmp_path / "out",
                         tmp_path / "tables", tmp_path)


def test_completed_exports_are_not_overwritten(tmp_path):
    tables = tmp_path / "tables"
    tables.mkdir()
    historical = tables / "verdict.json"
    historical.write_text("historical")
    with pytest.raises(FileExistsError):
        x4f_run.run_gates(tmp_path, tmp_path / "main", tmp_path / "out", tables, tmp_path)
    assert historical.read_text() == "historical"
    assert not (tmp_path / "out" / "cpu_ledger.json").exists()


def test_ridge_stop_inside_solver_grid():
    rng = np.random.default_rng(6)
    X, Y = rng.normal(size=(24, 4)), rng.normal(size=(24, 2))
    seen = []

    def guard(step):
        seen.append(step)
        if step == "ridge solve 0.01":
            raise StopRequested(step)

    with pytest.raises(StopRequested):
        x4f_probe.nested_ridge(X, Y, np.repeat([1, 2, 3], 8), X, Y, checkpoint=guard)
    assert "ridge solve 0.001 complete" in seen
    assert "ridge validation complete" not in seen


def test_shuffle_stop_inside_refits(monkeypatch):
    X = np.arange(24).reshape(12, 2)
    d = SimpleNamespace(cal=np.arange(12) < 8, val=np.arange(12) >= 8,
                        panel=np.repeat([1, 2, 3], 4), seed=1729)
    fits = []
    monkeypatch.setattr(x4f_gates, "nested_ridge",
                        lambda *a, **kw: fits.append(1) or SimpleNamespace(r2=0))

    def guard(step):
        if step.endswith(" 2"):
            raise StopRequested(step)

    with pytest.raises(StopRequested):
        x4f_gates.shuffled(d, X, X, "synthetic", guard)
    assert len(fits) == 2


def test_unmatched_family_keeps_partial_and_control_maps(monkeypatch):
    from topo_pilot.analysis import fit_oblique_eraser, whiten

    rng = np.random.default_rng(2)
    h, target = rng.normal(size=(32, 4)), rng.normal(size=(32, 2))
    cal = np.arange(32) < 24
    d = SimpleNamespace(acts={"resid_post_1": h}, cal=cal, seed=1729)
    wh = whiten(h[cal])
    primary = fit_oblique_eraser(h[cal], target[cal], wh)
    monkeypatch.setattr(x4f_damage, "random_family", lambda *args, **kw: SimpleNamespace(
        status="FAMILY_UNMATCHED", n_draws=10, n_degenerate_draws=0,
        accepted_draws=[3], maps=[primary.M], mean_displacements=[1.]))
    result, clouds = x4f_damage.g4(d, None, wh, primary,
                                  {name: target for name in x4f_gates.CONTROLS})
    assert result["status"] == "INCONCLUSIVE:FAMILY_UNMATCHED"
    assert not clouds
    assert set(result["_maps"]) == {"primary", "random_3", *x4f_gates.CONTROLS}


def test_export_round_trips_all_maps_without_pickle_and_records_hash(tmp_path, monkeypatch):
    monkeypatch.setattr(x4f_run, "SEEDS", (1729,))
    monkeypatch.setattr(x4f_run, "producer_version", lambda _: "maintenance-test")
    monkeypatch.setattr(x4f_run, "provenance_row", lambda *args: {"artifact_id": "input"})
    source = tmp_path / x4f_run.PROTOCOL_DOC
    source.parent.mkdir(parents=True)
    source.write_text("synthetic maintenance contract")
    data = SimpleNamespace(history_id=("one", "two"), panel=np.array([1, 2]),
                           targets={"m32": np.zeros((2, 2))})
    maps = {name: (np.arange(3.), np.eye(3), 1, "ok")
            for name in ("primary", "random_3", *x4f_gates.CONTROLS)}
    rw = SimpleNamespace(save=lambda *args, **kwargs: "synthetic_metric_id")
    summary = {"overall": "INCONCLUSIVE", "status": {1729: {"G4": "INCONCLUSIVE"}}}
    budget = SimpleNamespace(t0=time.process_time(), w0=time.time(), cap=100, steps=[])
    out, tables = tmp_path / "out", tmp_path / "tables"
    x4f_run._export(tmp_path, None, rw, out, tables, {1729: {}}, {1729: "act"},
                    {1729: data}, {}, {1729: {"maps": maps}}, summary, budget,
                    ("before", 0), ("before", 0), {"entries": [], "cumulative_cpu_s": 0})
    export = out / "exports" / "x4f_gates_1729.npz"
    with np.load(export, allow_pickle=False) as arrays:
        for name, (mu, M, rank, status) in maps.items():
            np.testing.assert_array_equal(arrays[f"map_{name}_mu"], mu)
            np.testing.assert_array_equal(arrays[f"map_{name}_M"], M)
            assert arrays[f"map_{name}_rank"].item() == rank
            assert arrays[f"map_{name}_status"].item() == status
    metadata = json.loads((tables / "run.json").read_text())
    digest = hashlib.sha256(export.read_bytes()).hexdigest()
    assert metadata["exports_sha256"][export.name] == digest
