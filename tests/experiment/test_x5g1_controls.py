"""Independent tests written by the X5 G1 test-writer agent from X5_G1_GATES_API.md / x5g1-feas-v2
before reading the implementation.

Execution controls (protocol x5g1-feas-v2 §7, API §3 ``x5g1_controls``): the ledger is written
on every exit path and never reset, STOP and budget guards, and parent checksum verification.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, ErrorCode, MemoryBackend, StageFailure
from topo_pilot.contracts.testing import tiny_world_spec
from topo_pilot.experiment.x5g1_controls import (
    BudgetExceeded,
    RunControls,
    StopRequested,
    verify_parents,
)

pytestmark = pytest.mark.experiment

ENTRY_KEYS = {"job", "cpu_s", "status", "steps"}


def _burn(seconds: float = 0.05) -> None:
    """Spend at least ``seconds`` of process CPU time."""
    t0 = time.process_time()
    x = np.ones(1000)
    while time.process_time() - t0 < seconds:
        x = np.sqrt(x * 1.0000001)


def _rc(tmp: Path, *, cap_s=3600.0, cum_cap=3600.0, job="unit") -> RunControls:
    return RunControls(tmp / "ledger.json", cap_s, tmp / "STOP", job, cum_cap)


def _ledger(tmp: Path) -> dict:
    return json.loads((tmp / "ledger.json").read_text(encoding="utf-8"))


def test_ledger_written_on_normal_exit(tmp_path):
    rc = _rc(tmp_path, job="x5g1-test")
    with rc:
        rc.guard("integrity")
        _burn(0.02)
        rc.guard("kernels")
    led = _ledger(tmp_path)
    assert len(led["entries"]) == 1
    entry = led["entries"][0]
    assert ENTRY_KEYS <= set(entry)
    assert entry["status"] == "ok" and entry["job"] == "x5g1-test"
    assert entry["cpu_s"] >= 0.0
    assert "integrity" in json.dumps(entry["steps"]) and "kernels" in json.dumps(entry["steps"])
    assert led["cumulative_cpu_s"] == pytest.approx(entry["cpu_s"], abs=1e-9)


def test_ledger_written_on_exception_and_exception_propagates(tmp_path):
    rc = _rc(tmp_path)
    with pytest.raises(ValueError, match="boom"):
        with rc:
            rc.guard("export")
            raise ValueError("boom")
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "error:ValueError"


def test_ledger_written_on_stage_failure(tmp_path):
    rc = _rc(tmp_path)
    with pytest.raises(StageFailure):
        with rc:
            raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "test", "x", "y")
    assert _ledger(tmp_path)["entries"][-1]["status"] == "error:StageFailure"


def test_stop_requested_mid_run(tmp_path):
    rc = _rc(tmp_path)
    with pytest.raises(StopRequested):
        with rc:
            rc.guard("before")
            (tmp_path / "STOP").write_text("stop", encoding="utf-8")
            rc.guard("after")
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "stopped"
    assert issubclass(StopRequested, RuntimeError)


def test_budget_exceeded_per_run(tmp_path):
    rc = _rc(tmp_path, cap_s=1e-6)
    with pytest.raises(BudgetExceeded):
        with rc:
            _burn(0.05)
            rc.guard("oracle_batch")
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "budget"
    assert entry["cpu_s"] > 0.0
    assert issubclass(BudgetExceeded, RuntimeError)


def test_cumulative_accumulates_and_is_never_reset(tmp_path):
    for job in ("first", "second"):
        rc = _rc(tmp_path, job=job)
        with rc:
            _burn(0.03)
            rc.guard(job)
    led = _ledger(tmp_path)
    assert [e["job"] for e in led["entries"]] == ["first", "second"]
    total = sum(e["cpu_s"] for e in led["entries"])
    assert led["cumulative_cpu_s"] == pytest.approx(total, rel=1e-9, abs=1e-9)
    assert led["cumulative_cpu_s"] >= led["entries"][0]["cpu_s"] > 0.0


def test_prior_cumulative_is_kept(tmp_path):
    prior = {"entries": [{"job": "old", "cpu_s": 7.5, "status": "ok", "steps": []}],
             "cumulative_cpu_s": 7.5}
    (tmp_path / "ledger.json").write_text(json.dumps(prior), encoding="utf-8")
    rc = _rc(tmp_path)
    with rc:
        rc.guard("one")
    led = _ledger(tmp_path)
    assert len(led["entries"]) == 2 and led["entries"][0]["job"] == "old"
    assert led["cumulative_cpu_s"] == pytest.approx(7.5 + led["entries"][1]["cpu_s"], abs=1e-9)


def test_cumulative_cap_exceeded(tmp_path):
    prior = {"entries": [], "cumulative_cpu_s": 10.0}
    (tmp_path / "ledger.json").write_text(json.dumps(prior), encoding="utf-8")
    rc = _rc(tmp_path, cap_s=3600.0, cum_cap=5.0)
    with pytest.raises(BudgetExceeded):
        with rc:
            rc.guard("integrity")
    led = _ledger(tmp_path)
    assert led["entries"][-1]["status"] == "budget"
    assert led["cumulative_cpu_s"] >= 10.0


def test_missing_ledger_starts_at_zero(tmp_path):
    assert not (tmp_path / "ledger.json").exists()
    rc = _rc(tmp_path, cum_cap=1.0)                 # 0 prior + tiny run stays under the cap
    with rc:
        rc.guard("one")
    led = _ledger(tmp_path)
    assert led["cumulative_cpu_s"] == pytest.approx(led["entries"][0]["cpu_s"], abs=1e-9)


# ---------------------------------------------------------------- verify_parents


@pytest.fixture()
def store_and_id():
    store = ArtifactStore(MemoryBackend())
    wid = store.save(tiny_world_spec("cylinder", n=3), config={"family": "cylinder", "n": 3},
                     parents=[], seed_map={}, consumer="world")
    return store, wid


def test_verify_parents_matching_prefix(store_and_id):
    store, wid = store_and_id
    sha = store.meta(wid).payload_sha256
    assert verify_parents(store, {wid: sha[:12]}) == []
    assert verify_parents(store, {wid: sha}) == []
    assert verify_parents(store, {}) == []


def test_verify_parents_wrong_prefix(store_and_id):
    store, wid = store_and_id
    sha = store.meta(wid).payload_sha256
    bad = ("0" if sha[0] != "0" else "1") + sha[1:12]
    out = verify_parents(store, {wid: bad})
    assert len(out) == 1 and isinstance(out[0], str)


def test_verify_parents_missing_id_never_raises(store_and_id):
    store, wid = store_and_id
    sha = store.meta(wid).payload_sha256
    out = verify_parents(store, {"0123456789abcdef": "ab", wid: sha[:8]})
    assert len(out) == 1 and all(isinstance(s, str) for s in out)
    out = verify_parents(store, {"0123456789abcdef": "ab", wid: "zz"})
    assert len(out) == 2


def test_verify_parents_backend_error_never_raises():
    class _Broken:
        def meta(self, artifact_id):
            raise OSError("disk gone")

    out = verify_parents(_Broken(), {"0123456789abcdef": "ab"})
    assert len(out) == 1 and isinstance(out[0], str)
