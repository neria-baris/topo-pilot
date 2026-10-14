"""Independent tests written by the X5 G1 test-writer agent from X5_G1_REPAIR_API.md before
reading the implementation.

Full-hash source checks, export guards, the atomic ledger and immutable outputs (API §1-§3).
"""

from __future__ import annotations

import io
import json
import time
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, MemoryBackend, TransitionSpec
from topo_pilot.experiment.x5g1_controls import (
    BudgetExceeded,
    LedgerCorrupt,
    RunControls,
    StopRequested,
)
from topo_pilot.experiment.x5g1_safety import (
    OutputExists,
    SourceTampered,
    checked_computation,
    ensure_new_output_dir,
    guarded_export,
    verify_sources_full,
)

pytestmark = pytest.mark.experiment


# ---------------------------------------------------------------- helpers


def _burn(seconds: float = 0.05) -> None:
    t0 = time.process_time()
    x = np.ones(1000)
    while time.process_time() - t0 < seconds:
        x = np.sqrt(x * 1.0000001)


def _spec() -> TransitionSpec:
    return TransitionSpec(T=np.array([[0.5, 0.5], [0.5, 0.5]]), pi=np.array([0.5, 0.5]))


class _FlakyBackend(MemoryBackend):
    broken = False

    def get(self, key: str) -> bytes:
        if self.broken:
            raise OSError("disk gone")
        return super().get(key)


@pytest.fixture()
def saved():
    """A store with two lawfully saved TransitionSpecs and their full expected hashes."""
    backend = _FlakyBackend()
    store = ArtifactStore(backend)
    expected = {}
    for k in (1, 2):
        aid = store.save(_spec(), config={"k": k}, parents=[], seed_map={}, consumer="process")
        expected[aid] = (TransitionSpec, store.meta(aid).payload_sha256)
    return store, backend, expected


def _key(backend: MemoryBackend, aid: str, name: str) -> str:
    keys = [k for k in backend.list(f"TransitionSpec/{aid}/") if k.endswith(name)]
    assert len(keys) == 1
    return keys[0]


def _mutate_payload(backend: MemoryBackend, aid: str) -> None:
    # rewrite payload.npz in place with different (still valid) numbers; meta untouched
    key = _key(backend, aid, "payload.npz")
    with np.load(io.BytesIO(backend.get(key)), allow_pickle=False) as npz:
        arrays = {k: npz[k] for k in npz.files}
    arrays["T"] = np.array([[0.4, 0.6], [0.6, 0.4]])
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    backend.put(key, buf.getvalue())


def _mutate_meta_hash(backend: MemoryBackend, aid: str) -> None:
    key = _key(backend, aid, "meta.json")
    meta = json.loads(backend.get(key))
    sha = meta["payload_sha256"]
    meta["payload_sha256"] = ("0" if sha[0] != "0" else "1") + sha[1:]
    backend.put(key, json.dumps(meta, sort_keys=True, indent=1).encode("utf-8"))


def _rc(tmp: Path, *, cap_s=3600.0, cum_cap=3600.0, job="unit") -> RunControls:
    return RunControls(tmp / "ledger.json", cap_s, tmp / "STOP", job, cum_cap)


def _ledger(tmp: Path) -> dict:
    return json.loads((tmp / "ledger.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- verify_sources_full


def test_verify_full_hash_of_lawful_artifacts_passes(saved):
    store, _, expected = saved
    assert all(len(sha) == 64 for _, sha in expected.values())
    assert verify_sources_full(store, expected) == []
    assert verify_sources_full(store, expected, consumer="experiment") == []
    assert verify_sources_full(store, {}) == []


def test_verify_wrong_full_hash_fails(saved):
    store, _, expected = saved
    aid = next(iter(expected))
    bad = dict(expected)
    sha = expected[aid][1]
    bad[aid] = (TransitionSpec, sha[:-1] + ("0" if sha[-1] != "0" else "1"))
    out = verify_sources_full(store, bad)
    assert len(out) == 1 and isinstance(out[0], str)


def test_verify_prefix_only_hash_rejected(saved):
    store, _, expected = saved
    prefixed = {aid: (cls, sha[:16]) for aid, (cls, sha) in expected.items()}
    out = verify_sources_full(store, prefixed)
    assert len(out) == 2 and all(isinstance(s, str) for s in out)


def test_verify_payload_mutated_with_meta_intact_fails(saved):
    store, backend, expected = saved
    aid = next(iter(expected))
    _mutate_payload(backend, aid)
    assert store.meta(aid).payload_sha256 == expected[aid][1]      # meta step alone passes
    out = verify_sources_full(store, expected)
    assert len(out) == 1 and isinstance(out[0], str)


def test_verify_meta_hash_mutated_fails(saved):
    store, backend, expected = saved
    aid = next(iter(expected))
    _mutate_meta_hash(backend, aid)
    out = verify_sources_full(store, expected)
    assert len(out) == 1 and isinstance(out[0], str)


def test_verify_disallowed_consumer_is_failure_not_raise(saved):
    store, _, expected = saved
    out = verify_sources_full(store, expected, consumer="world")   # policy forbids
    assert len(out) == 2 and all(isinstance(s, str) for s in out)


def test_verify_missing_artifact_is_failure_not_raise(saved):
    store, _, expected = saved
    sha = next(iter(expected.values()))[1]
    with_missing = dict(expected)
    with_missing["0123456789abcdef"] = (TransitionSpec, sha)
    out = verify_sources_full(store, with_missing)
    assert len(out) == 1 and isinstance(out[0], str)


def test_verify_broken_backend_is_failure_not_raise(saved):
    store, backend, expected = saved
    backend.broken = True
    out = verify_sources_full(store, expected)
    assert len(out) == 2 and all(isinstance(s, str) for s in out)


# ---------------------------------------------------------------- checked_computation


def test_checked_computation_returns_result_when_clean(saved):
    store, _, expected = saved
    calls = []

    def fn():
        calls.append(1)
        return {"value": 42}

    assert checked_computation(store, expected, fn) == {"value": 42}
    assert calls == [1]


def test_checked_computation_before_failure_skips_fn(saved):
    store, _, expected = saved
    aid = next(iter(expected))
    bad = dict(expected)
    bad[aid] = (TransitionSpec, expected[aid][1][:16])               # prefix only
    called = {"flag": False}

    def fn():
        called["flag"] = True
        return 1

    with pytest.raises(SourceTampered) as excinfo:
        checked_computation(store, bad, fn)
    assert str(excinfo.value).startswith("before")
    assert called["flag"] is False


@pytest.mark.parametrize("mutate", [_mutate_payload, _mutate_meta_hash],
                         ids=["payload", "meta_hash"])
def test_checked_computation_tamper_inside_fn_raises_after(saved, mutate):
    store, backend, expected = saved
    aid = next(iter(expected))
    called = {"flag": False}
    returned = []

    def fn():
        called["flag"] = True
        mutate(backend, aid)
        return "result"

    with pytest.raises(SourceTampered) as excinfo:
        returned.append(checked_computation(store, expected, fn))
    assert called["flag"] is True
    assert str(excinfo.value).startswith("after")
    assert returned == []


# ---------------------------------------------------------------- ensure_new_output_dir


def test_output_dir_new_path_is_created(tmp_path):
    target = tmp_path / "a" / "b" / "out_v2"
    assert not target.exists()
    result = ensure_new_output_dir(target)
    assert Path(result) == target
    assert target.is_dir() and list(target.iterdir()) == []
    assert Path(ensure_new_output_dir(target)) == target            # existing empty: accepted
    assert target.is_dir() and list(target.iterdir()) == []


@pytest.mark.parametrize("kind", ["file", "subdir"])
def test_output_dir_non_empty_raises_and_is_untouched(tmp_path, kind):
    target = tmp_path / "used"
    target.mkdir()
    if kind == "file":
        (target / "result.json").write_bytes(b'{"x": 1}')
        (target / "fig.png").write_bytes(b"\x89PNG fake")
    else:
        (target / "sub").mkdir()
    before = sorted((p.relative_to(target).as_posix(), p.is_dir(),
                     p.read_bytes() if p.is_file() else None) for p in target.rglob("*"))
    with pytest.raises(OutputExists) as excinfo:
        ensure_new_output_dir(target)
    assert isinstance(excinfo.value, FileExistsError)
    assert issubclass(SourceTampered, RuntimeError) and issubclass(LedgerCorrupt, RuntimeError)
    after = sorted((p.relative_to(target).as_posix(), p.is_dir(),
                    p.read_bytes() if p.is_file() else None) for p in target.rglob("*"))
    assert after == before


# ---------------------------------------------------------------- guarded_export


def _steps(log: list, names=("s1", "s2"), hooks=None):
    hooks = hooks or {}

    def make(name):
        def fn():
            log.append(name)
            if name in hooks:
                hooks[name]()
        return fn

    return [(n, make(n)) for n in names]


def test_export_without_stop_runs_all_in_order(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    ctl = _rc(tmp_path)
    with ctl:
        guarded_export(ctl, _steps(log, ("s1", "s2", "s3")), status)
    assert log == ["s1", "s2", "s3"]
    assert not status.exists()
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "ok" and entry["cause"] is None
    steps_text = json.dumps(entry["steps"])
    assert "export s1" in steps_text and "export s3" in steps_text


def test_export_stop_file_created_in_step1(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    stop = lambda: (tmp_path / "STOP").write_text("stop", encoding="utf-8")  # noqa: E731
    ctl = _rc(tmp_path)
    with pytest.raises(StopRequested):
        with ctl:
            guarded_export(ctl, _steps(log, hooks={"s1": stop}), status)
    assert log == ["s1"]                                               # step 2 never ran
    doc = json.loads(status.read_text(encoding="utf-8"))
    assert doc["status"] == "STOPPED_DURING_EXPORT"
    assert doc["completed_steps"] in ([], ["s1"])
    assert "s2" not in doc["completed_steps"]
    assert doc["cause"].startswith("StopRequested")
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "stopped"
    assert entry["cause"] is not None and entry["cause"].startswith("StopRequested")


def test_export_stop_in_middle_step_keeps_completed(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    stop = lambda: (tmp_path / "STOP").write_text("stop", encoding="utf-8")  # noqa: E731
    ctl = _rc(tmp_path)
    with pytest.raises(StopRequested):
        with ctl:
            guarded_export(ctl, _steps(log, ("s1", "s2", "s3"), {"s2": stop}), status)
    assert log == ["s1", "s2"]
    doc = json.loads(status.read_text(encoding="utf-8"))
    assert doc["status"] == "STOPPED_DURING_EXPORT"
    assert doc["completed_steps"][:1] == ["s1"]
    assert set(doc["completed_steps"]) <= {"s1", "s2"}


def test_export_stop_present_before_start_runs_nothing(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    (tmp_path / "STOP").write_text("stop", encoding="utf-8")
    ctl = _rc(tmp_path)
    with pytest.raises(StopRequested):
        with ctl:
            guarded_export(ctl, _steps(log), status)
    assert log == []
    doc = json.loads(status.read_text(encoding="utf-8"))
    assert doc["status"] == "STOPPED_DURING_EXPORT" and doc["completed_steps"] == []


def test_export_budget_exceeded(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    ctl = _rc(tmp_path, cap_s=1e-6)
    with pytest.raises(BudgetExceeded):
        with ctl:
            guarded_export(ctl, _steps(log, hooks={"s1": lambda: _burn(0.05)}), status)
    assert "s2" not in log
    doc = json.loads(status.read_text(encoding="utf-8"))
    assert doc["status"] == "BUDGET_DURING_EXPORT"
    assert "s2" not in doc["completed_steps"]
    assert doc["cause"].startswith("BudgetExceeded")
    entry = _ledger(tmp_path)["entries"][-1]
    assert entry["status"] == "budget" and entry["cause"] is not None


def test_export_other_exception_propagates_without_status(tmp_path):
    log: list = []
    status = tmp_path / "export_status.json"
    err = ValueError("plot failed")

    def boom():
        raise err

    ctl = _rc(tmp_path)
    with pytest.raises(ValueError) as excinfo:
        with ctl:
            guarded_export(ctl, _steps(log, hooks={"s1": boom}), status)
    assert excinfo.value is err
    assert log == ["s1"]
    assert not status.exists()
    assert _ledger(tmp_path)["entries"][-1]["status"] == "error:ValueError"


# ---------------------------------------------------------------- RunControls ledger


def test_ledger_preserves_history_on_error_and_is_atomic(tmp_path):
    prior = {"entries": [{"job": "old1", "cpu_s": 4.0, "status": "ok", "steps": []},
                         {"job": "old2", "cpu_s": 6.0, "status": "budget", "steps": ["x"]}],
             "cumulative_cpu_s": 10.0}
    (tmp_path / "ledger.json").write_text(json.dumps(prior), encoding="utf-8")
    ctl = _rc(tmp_path, cum_cap=1e6, job="new")
    with pytest.raises(ValueError, match="kaboom"):
        with ctl:
            ctl.guard("work")
            _burn(0.02)
            raise ValueError("kaboom")
    led = _ledger(tmp_path)
    assert len(led["entries"]) == 3
    assert led["entries"][:2] == prior["entries"]
    last = led["entries"][2]
    assert last["job"] == "new" and last["status"] == "error:ValueError"
    assert last["cause"].startswith("ValueError") and "kaboom" in last["cause"]
    assert led["cumulative_cpu_s"] >= 10.0
    assert led["cumulative_cpu_s"] == pytest.approx(10.0 + last["cpu_s"], abs=1e-9)
    assert list(tmp_path.glob("*.tmp")) == []


def test_corrupt_ledger_raises_and_keeps_bytes(tmp_path):
    path = tmp_path / "ledger.json"
    raw = b'{"entries": [{"job": "old", "cpu_s": 3.0 ,,, not json'
    path.write_bytes(raw)
    with pytest.raises(LedgerCorrupt):
        _rc(tmp_path)
    assert path.read_bytes() == raw
    assert list(tmp_path.glob("*.tmp")) == []
