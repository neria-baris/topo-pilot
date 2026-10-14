"""Independent tests written by the X5 G1 test-writer agent from X5_G1_REPAIR_API.md §4 before
reading the implementation.

Covers the real gate-driver export path ``x5g1_main._export`` (§4.1: the single guarded
MetricRecords save, STOP before and during export, normal run, ``global_failed``) and the
``RunControls`` ledger validation (§4.2). Synthetic artifacts only, under ``tmp_path``.
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path

import numpy as np
import pytest

import topo_pilot.contracts as contracts
from topo_pilot.contracts import (
    ArtifactStore,
    LocalFSBackend,
    MetricRecords,
    ObservationSet,
    TransitionSpec,
)
from topo_pilot.experiment.x5g1_controls import LedgerCorrupt, RunControls, StopRequested
from topo_pilot.experiment.x5g1_main import _export

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]
TABLE_FILES = ("verdict.json", "result.json", "run.json")


# ---------------------------------------------------------------- helpers


def _spec() -> TransitionSpec:
    return TransitionSpec(T=np.array([[0.5, 0.5], [0.5, 0.5]]), pi=np.array([0.5, 0.5]))


def _obs(offset: int) -> ObservationSet:
    tokens = (np.arange(2 * 33).reshape(2, 33) + offset) % 36
    return ObservationSet(split="dev", V=36, sequence_id=np.array([offset, offset + 1],
                          dtype=np.int64), tokens=tokens.astype(np.uint8))


def _build_main(main_root: Path) -> dict:
    """Lawful parents in a LocalFS main store; returns the ids used by ``res``."""
    store = ArtifactStore(LocalFSBackend(main_root))
    prov = [store.save(_spec(), config={"k": k}, parents=[], seed_map={}, consumer="process")
            for k in ("world_stand_in", "T_a0")]
    t_a020 = store.save(_spec(), config={"k": "T_a020"}, parents=[], seed_map={},
                        consumer="process")
    obs = {arm: store.save(_obs(off), config={"arm": arm}, parents=[], seed_map={},
                           consumer="dataset")
           for arm, off in (("a0", 0), ("a020", 100))}
    assert len({*prov, t_a020, *obs.values()}) == 5
    return {"prov": prov, "t_a020": t_a020, "obs": obs}


def _res(ids: dict, global_failed=None) -> dict:
    arms = {}
    for i, arm in enumerate(("a0", "a020")):
        arms[arm] = {"obs_id": ids["obs"][arm], "GC": 0.05 + 0.01 * i,
                     "GC_stationary": 0.20 + 0.01 * i, "two_token_regret": 0.01 + 0.001 * i,
                     "context": "PASS"}
    failed = list(global_failed or [])
    return {"provenance": [{"artifact_id": a} for a in ids["prov"]],
            "T_a020_id": ids["t_a020"], "arms": arms,
            "verdict": "FAILED" if failed else "FEASIBLE",
            "reason": failed[0] if failed else "all arms PASS",
            "global_failed": failed, "global_inconclusive": []}


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """Main store, output dirs, controls paths, and a counting spy on ArtifactStore.save."""
    main_root = tmp_path / "main"
    ids = _build_main(main_root)
    out_root = tmp_path / "out"
    out_root.mkdir()
    tables = tmp_path / "tables"
    tables.mkdir()
    mailbox = tmp_path / "mailbox"
    mailbox.mkdir()
    state = {"calls": 0, "on_save": None, "saved_types": []}
    real_save = contracts.ArtifactStore.save

    def spy(self, artifact, *args, **kwargs):
        state["calls"] += 1
        state["saved_types"].append(type(artifact).__name__)
        aid = real_save(self, artifact, *args, **kwargs)
        if state["on_save"] is not None:
            state["on_save"]()
        return aid

    monkeypatch.setattr(contracts.ArtifactStore, "save", spy)
    return {"main": main_root, "out": out_root, "tables": tables, "ids": ids,
            "stop": mailbox / "STOP", "ledger": out_root / "cpu_ledger.json", "spy": state}


def _ctl(env) -> RunControls:
    return RunControls(env["ledger"], 60.0, env["stop"], "test", 60.0)


def _last_entry(env) -> dict:
    return json.loads(env["ledger"].read_text(encoding="utf-8"))["entries"][-1]


def _status(env) -> dict:
    return json.loads((env["tables"] / "EXPORT_STATUS.json").read_text(encoding="utf-8"))


def _metric_dir(env) -> Path:
    return env["out"] / "store" / "MetricRecords"


def _metric_ids(env) -> list[str]:
    d = _metric_dir(env)
    return sorted(p.name for p in d.iterdir() if p.is_dir()) if d.is_dir() else []


def _expected_parents(ids: dict) -> set[str]:
    return {*ids["prov"], ids["t_a020"], *ids["obs"].values()}


# ---------------------------------------------------------------- §4.1 export integration


def test_stop_before_export_saves_nothing(env):
    env["stop"].write_text("stop", encoding="utf-8")
    ctl = _ctl(env)
    with pytest.raises(StopRequested):
        with ctl:
            _export(REPO, env["main"], env["out"], env["tables"], _res(env["ids"]), ctl)
    assert env["spy"]["calls"] == 0                          # no ArtifactStore.save at all
    assert not _metric_dir(env).exists()                     # no MetricRecords directory
    status = _status(env)
    assert status["status"] == "STOPPED_DURING_EXPORT"
    assert status["completed_steps"] == []
    for name in TABLE_FILES:
        assert not (env["tables"] / name).exists()
    entry = _last_entry(env)
    assert entry["status"] == "stopped"
    assert entry["cause"] is not None and entry["cause"].startswith("StopRequested")


def test_normal_export_single_save_and_manifest(env):
    ctl = _ctl(env)
    with ctl:
        _export(REPO, env["main"], env["out"], env["tables"], _res(env["ids"]), ctl)
    assert env["spy"]["calls"] == 1
    assert env["spy"]["saved_types"] == ["MetricRecords"]
    for name in TABLE_FILES:
        assert (env["tables"] / name).is_file()
    run = json.loads((env["tables"] / "run.json").read_text(encoding="utf-8"))
    assert "metric_records_id" in run
    mid = run["metric_records_id"]
    assert isinstance(mid, str) and _metric_ids(env) == [mid]
    out_store = ArtifactStore(LocalFSBackend(env["out"] / "store"))
    meta = out_store.meta(mid)
    assert meta.artifact_type == "MetricRecords" and meta.status == "complete"
    assert set(meta.parent_ids) == _expected_parents(env["ids"])
    records = out_store.load(MetricRecords, mid, consumer="experiment")
    assert isinstance(records, MetricRecords)
    manifest_path = env["tables"] / "MANIFEST.json"
    assert manifest_path.is_file()
    manifest_text = manifest_path.read_text(encoding="utf-8")
    json.loads(manifest_text)                                # valid JSON
    for name in TABLE_FILES:
        assert name in manifest_text
    entry = _last_entry(env)
    assert entry["status"] == "ok" and entry["cause"] is None


def test_stop_created_during_save_skips_remaining_steps(env):
    env["spy"]["on_save"] = lambda: env["stop"].write_text("stop", encoding="utf-8")
    ctl = _ctl(env)
    with pytest.raises(StopRequested):
        with ctl:
            _export(REPO, env["main"], env["out"], env["tables"], _res(env["ids"]), ctl)
    assert env["spy"]["calls"] == 1
    mids = _metric_ids(env)                                  # that save completed
    assert len(mids) == 1
    out_store = ArtifactStore(LocalFSBackend(env["out"] / "store"))
    assert out_store.meta(mids[0]).status == "complete"
    status = _status(env)
    assert status["status"] == "STOPPED_DURING_EXPORT"
    assert status["completed_steps"] == ["metric_records"]
    assert not (env["tables"] / "verdict.json").exists()
    assert not (env["tables"] / "MANIFEST.json").exists()
    entry = _last_entry(env)
    assert entry["status"] == "stopped" and entry["cause"] is not None


def test_global_failed_writes_tables_without_save(env):
    res = _res(env["ids"], global_failed=["integrity: synthetic failure"])
    ctl = _ctl(env)
    with ctl:
        _export(REPO, env["main"], env["out"], env["tables"], res, ctl)
    assert env["spy"]["calls"] == 0
    assert _metric_ids(env) == []
    for name in (*TABLE_FILES, "MANIFEST.json"):
        assert (env["tables"] / name).is_file()
    verdict_text = (env["tables"] / "verdict.json").read_text(encoding="utf-8")
    assert "FAILED" in verdict_text


def test_missing_parent_id_gives_no_save(env):
    # §4.1: the save runs only if the IDs exist in the main store. Whether _export then raises
    # is not specified, so only the absence of any save is asserted.
    res = _res(env["ids"])
    res["T_a020_id"] = "0123456789abcdef"
    ctl = _ctl(env)
    with contextlib.suppress(Exception):
        with ctl:
            _export(REPO, env["main"], env["out"], env["tables"], res, ctl)
    assert env["spy"]["calls"] == 0
    assert _metric_ids(env) == []


# ---------------------------------------------------------------- §4.2 ledger validation

_OK_ENTRY = '{"job": "old", "cpu_s": 1.0, "status": "ok", "steps": []}'

INVALID_LEDGERS = {
    "cum_nan": '{"entries": [], "cumulative_cpu_s": NaN}',
    "cum_inf": '{"entries": [], "cumulative_cpu_s": Infinity}',
    "cum_neg_inf": '{"entries": [], "cumulative_cpu_s": -Infinity}',
    "cum_negative": '{"entries": [], "cumulative_cpu_s": -1.0}',
    "cum_bool": '{"entries": [], "cumulative_cpu_s": true}',
    "cum_string": '{"entries": [], "cumulative_cpu_s": "12"}',
    "entries_string": '{"entries": "not a list", "cumulative_cpu_s": 1.0}',
    "entries_dict": '{"entries": {"job": "old"}, "cumulative_cpu_s": 1.0}',
    "entry_not_object": '{"entries": [' + _OK_ENTRY + ', 7], "cumulative_cpu_s": 1.0}',
    "entry_string": '{"entries": ["old"], "cumulative_cpu_s": 1.0}',
}


@pytest.mark.parametrize("text", list(INVALID_LEDGERS.values()), ids=list(INVALID_LEDGERS))
def test_invalid_ledger_raises_at_construction_and_keeps_bytes(tmp_path, text):
    path = tmp_path / "ledger.json"
    raw = text.encode("utf-8")
    path.write_bytes(raw)
    with pytest.raises(LedgerCorrupt):
        RunControls(path, 60.0, tmp_path / "STOP", "test", 60.0)
    assert path.read_bytes() == raw
    assert list(tmp_path.glob("*.tmp")) == []
    assert issubclass(LedgerCorrupt, RuntimeError)


def test_valid_ledger_survives_run_that_raises(tmp_path):
    path = tmp_path / "ledger.json"
    prior = {"entries": [{"job": "p1", "cpu_s": 2.0, "status": "ok", "steps": ["a"]},
                         {"job": "p2", "cpu_s": 3.0, "status": "stopped", "steps": [],
                          "cause": "StopRequested: earlier"}],
             "cumulative_cpu_s": 5.0}
    path.write_text(json.dumps(prior), encoding="utf-8")
    ctl = RunControls(path, 60.0, tmp_path / "STOP", "test", 60.0)
    with pytest.raises(RuntimeError, match="synthetic"):
        with ctl:
            ctl.guard("work")
            raise RuntimeError("synthetic")
    led = json.loads(path.read_text(encoding="utf-8"))
    assert len(led["entries"]) == 3
    assert led["entries"][:2] == prior["entries"]
    last = led["entries"][2]
    assert last["job"] == "test" and last["status"] == "error:RuntimeError"
    assert last["cause"] is not None and "synthetic" in last["cause"]
    assert led["cumulative_cpu_s"] >= prior["cumulative_cpu_s"]
    assert list(tmp_path.glob("*.tmp")) == []
