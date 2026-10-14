"""Independent contract tests, written from the API contract (X5_G1_TRAINING_API.md §5-§6, §8
"Training composition") and protocol x5g1-train-v3 §2, without reading the implementation.

Covers the study TrainConfig and run key, the checkpoint callback (byte- and id-identical to
``LearnerStage``; ``before`` runs before the write), paired step-0 weights across arms with
parent-distinct checkpoint ids, and ``train_one`` outcomes (COMPLETE, INCOMPLETE + re-raise, no
retry). Tiny model, tiny pools, in-memory stores; ``controls`` is a fake ``.boundary`` object.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from topo_pilot.contracts import Checkpoint, ObservationSet, SeedTree, SequenceLayout
from topo_pilot.contracts.testing import memory_store, tiny_hmm
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.experiment import x5g1t_lineage as lin
from topo_pilot.experiment.x5g1_controls import StopRequested
from topo_pilot.experiment.x5g1t_runtime import RunLocked, outcome_path, read_outcome
from topo_pilot.experiment.x5g1t_train import (
    checkpoint_callback,
    study_run_key,
    study_train_config,
    train_one,
)
from topo_pilot.learner import LearnerStage, ModelConfig, TrainConfig, Trainer

pytestmark = pytest.mark.experiment

T_FLAT, E, PI = tiny_hmm()
T_OTHER = np.full((4, 4), 0.2) + np.eye(4) * 0.2
KERNELS = {"a0": T_FLAT, "a020": T_OTHER}
PERM = np.array([2, 0, 1])
MODEL = ModelConfig(vocab_in=4, vocab_out=3, n_layers=1, d_model=8, n_heads=2, d_mlp=16)
TRAIN = TrainConfig(steps=6, batch_size=4, warmup=1, checkpoint_steps=(0, 3, 6), device="cpu")
MASTER = 310001
STUDY_GRID = tuple(range(0, 1001, 100)) + tuple(range(1250, 5001, 250))


def _add_pools(store, master: int = MASTER) -> dict[str, tuple[str, str]]:
    """Save train (n=32) and dev (n=8) pools per arm; returns {arm: (train_id, dev_id)}."""
    ids: dict[str, list[str]] = {arm: [] for arm in lin.ARMS}
    for split, n in (("train", 32), ("dev", 8)):
        named = lin.draw_pair(KERNELS, E, PERM, PI, split, master, n)
        for arm in lin.ARMS:
            obs = lin.pool_observation(split, named[arm],
                                       lin.sequence_ids(split, arm, master, n), 3)
            ids[arm].append(store.save(obs, config=lin.pool_config(split, arm, master),
                                       parents=[], seed_map={}, consumer="experiment"))
    return {arm: (a, b) for arm, (a, b) in ids.items()}


def _datasets(store, train_id: str, dev_id: str):
    layout = SequenceLayout()
    return tuple(PublicTokenDataset(store.load(ObservationSet, i, consumer="learner"), layout)
                 for i in (train_id, dev_id))


def _ckpts(store) -> list[str]:
    return store.find(Checkpoint)


class FakeControls:
    """``.boundary(what, next_estimate, reserve, audit=...)``; raises STOP at call ``stop_at``."""

    def __init__(self, stop_at: int | None = None) -> None:
        self.stop_at = stop_at
        self.calls: list[tuple] = []

    def boundary(self, what, next_estimate, reserve, audit=None):
        self.calls.append((what, next_estimate, reserve))
        if self.stop_at is not None and len(self.calls) >= self.stop_at:
            raise StopRequested(f"fake stop at {what}")


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "study"
    (r / "outcomes").mkdir(parents=True)
    return r


# ---------------------------------------------------------------- config and run key


def test_study_train_config_defaults():
    cfg = study_train_config()
    assert isinstance(cfg, TrainConfig)
    assert cfg.checkpoint_steps == STUDY_GRID and len(cfg.checkpoint_steps) == 27
    assert cfg.device == "cpu" and cfg.steps == 5000
    stored = TrainConfig()
    for f in ("batch_size", "lr", "warmup", "schedule", "weight_decay", "grad_clip"):
        assert getattr(cfg, f) == getattr(stored, f)
    assert (cfg.batch_size, cfg.lr, cfg.warmup, cfg.weight_decay, cfg.grad_clip) == (
        128, 1e-3, 200, 0.1, 1.0)


def test_study_train_config_custom_grid():
    cfg = study_train_config(steps=6, grid=[0, 3, 6])
    assert cfg == dataclasses.replace(TrainConfig(), steps=6, checkpoint_steps=(0, 3, 6),
                                      device="cpu")
    assert isinstance(cfg.checkpoint_steps, tuple)


@pytest.mark.parametrize("m", [310001, 310002, 310003])
def test_study_run_key(m):
    assert study_run_key(m) == ("x5g1", "cylinder", m)
    assert isinstance(study_run_key(m), tuple)


# ---------------------------------------------------------------- checkpoint callback


def _callback_run(store, train_id, dev_id, before, after):
    seeds, run_key, record = SeedTree(MASTER), study_run_key(MASTER), []
    cb = checkpoint_callback(store, train_id, dev_id, MODEL, TRAIN, seeds, run_key, before,
                             after, record)
    train, dev = _datasets(store, train_id, dev_id)
    Trainer(MODEL, TRAIN, seeds, run_key).fit(train, dev, cb)
    return record


def test_callback_identical_to_learner_stage():
    store, ref_store = memory_store(), memory_store()
    train_id, dev_id = _add_pools(store)["a020"]
    assert _add_pools(ref_store)["a020"] == (train_id, dev_id)
    events = []

    def before(step):
        assert store.find(Checkpoint, step=step) == []  # nothing written yet for this step
        events.append(("before", step))

    def after(step):
        assert len(store.find(Checkpoint, step=step)) == 1
        events.append(("after", step))

    record = _callback_run(store, train_id, dev_id, before, after)
    ref_ids = LearnerStage().run(train_id, dev_id, MODEL, TRAIN, SeedTree(MASTER),
                                 study_run_key(MASTER), ref_store)
    assert events == [(k, s) for s in (0, 3, 6) for k in ("before", "after")]
    assert [r["step"] for r in record] == [0, 3, 6]
    assert [r["checkpoint_id"] for r in record] == ref_ids
    for r in record:
        meta, ref_meta = store.meta(r["checkpoint_id"]), ref_store.meta(r["checkpoint_id"])
        assert r["payload_sha256"] == meta.payload_sha256 == ref_meta.payload_sha256
        assert meta.config == ref_meta.config
        assert meta.config["run_key"] == ["x5g1", "cylinder", MASTER]
        assert meta.config["step"] == r["step"]
        assert set(meta.parent_ids) == {train_id, dev_id} == set(ref_meta.parent_ids)
        assert dict(meta.seed_map) == dict(ref_meta.seed_map) and meta.seed_map
        assert meta.consumer == "experiment"
        got = store.load(Checkpoint, r["checkpoint_id"], consumer="experiment")
        ref = ref_store.load(Checkpoint, r["checkpoint_id"], consumer="experiment")
        assert got.state == ref.state
        assert got.run_id == ref.run_id == f"x5g1-cylinder-{MASTER}"
        assert got.has_optimizer_state == ref.has_optimizer_state == (r["step"] == 6)


def test_stop_in_before_writes_no_artifact_for_that_step():
    store = memory_store()
    train_id, dev_id = _add_pools(store)["a0"]
    afters = []

    def before(step):
        if step == 3:
            raise StopRequested("owner stop")

    record_holder = []
    seeds, run_key = SeedTree(MASTER), study_run_key(MASTER)
    cb = checkpoint_callback(store, train_id, dev_id, MODEL, TRAIN, seeds, run_key, before,
                             afters.append, record_holder)
    train, dev = _datasets(store, train_id, dev_id)
    with pytest.raises(StopRequested):
        Trainer(MODEL, TRAIN, seeds, run_key).fit(train, dev, cb)
    assert [r["step"] for r in record_holder] == [0]
    assert afters == [0]
    assert store.find(Checkpoint, step=3) == [] and store.find(Checkpoint, step=6) == []
    assert _ckpts(store) == [record_holder[0]["checkpoint_id"]]


def test_stop_before_first_write_leaves_store_empty():
    store = memory_store()
    train_id, dev_id = _add_pools(store)["a0"]

    def before(step):
        raise StopRequested("stop at once")

    with pytest.raises(StopRequested):
        _callback_run(store, train_id, dev_id, before, lambda step: None)
    assert _ckpts(store) == []


# ---------------------------------------------------------------- train_one


def _train(store, pools, arm, root, controls, master=MASTER):
    train_id, dev_id = pools[arm]
    return train_one(store, train_id, dev_id, MODEL, TRAIN, master, arm, root, controls)


def test_train_one_complete_matches_learner_stage(root):
    store, ref_store = memory_store(), memory_store()
    pools = _add_pools(store)
    _add_pools(ref_store)
    controls = FakeControls()
    _train(store, pools, "a0", root, controls)
    out = read_outcome(root, "a0", MASTER)
    assert outcome_path(root, "a0", MASTER) == root / "outcomes" / f"a0_{MASTER}.json"
    assert outcome_path(root, "a0", MASTER).exists()
    assert out["status"] == "COMPLETE" and out["cause"] is None
    assert out["arm"] == "a0" and out["master"] == MASTER
    ref_ids = LearnerStage().run(*pools["a0"], MODEL, TRAIN, SeedTree(MASTER),
                                 study_run_key(MASTER), ref_store)
    assert [c["step"] for c in out["checkpoints"]] == [0, 3, 6]
    assert [c["checkpoint_id"] for c in out["checkpoints"]] == ref_ids
    assert sorted(_ckpts(store)) == sorted(ref_ids)
    for c in out["checkpoints"]:
        assert c["payload_sha256"] == store.meta(c["checkpoint_id"]).payload_sha256
        assert c["payload_sha256"] == ref_store.meta(c["checkpoint_id"]).payload_sha256
    assert len(controls.calls) >= 6  # before and after each of the 3 checkpoints
    for _, est, reserve in controls.calls:
        assert np.isfinite(float(est)) and np.isfinite(float(reserve))
    assert not (root / "RUN.lock").exists()


def test_arms_share_step0_weights_and_seeds_but_not_ids(root):
    store = memory_store()
    pools = _add_pools(store)
    for arm in lin.ARMS:
        _train(store, pools, arm, root, FakeControls())
    recs = {arm: read_outcome(root, arm, MASTER)["checkpoints"] for arm in lin.ARMS}
    by_step = {arm: {c["step"]: c["checkpoint_id"] for c in recs[arm]} for arm in lin.ARMS}
    for step in (0, 3, 6):
        assert by_step["a0"][step] != by_step["a020"][step]
    load = {arm: {s: store.load(Checkpoint, i, consumer="experiment")
                  for s, i in by_step[arm].items()} for arm in lin.ARMS}
    assert load["a0"][0].state == load["a020"][0].state  # identical initial weights
    assert load["a0"][3].state != load["a020"][3].state  # different data after training
    metas = {arm: store.meta(by_step[arm][0]) for arm in lin.ARMS}
    # same init and batch-order seeds (SeedTree(m), same run key) in both arms
    assert dict(metas["a0"].seed_map) == dict(metas["a020"].seed_map)
    assert any(k.startswith("batch_order/") for k in metas["a0"].seed_map)
    assert metas["a0"].config == metas["a020"].config  # ids differ only through the parents
    assert set(metas["a0"].parent_ids) == set(pools["a0"])
    assert set(metas["a020"].parent_ids) == set(pools["a020"])


@pytest.mark.parametrize("stop_at", [1, 3])
def test_train_one_incomplete_recorded_and_reraised(root, stop_at):
    store = memory_store()
    pools = _add_pools(store)
    with pytest.raises(StopRequested):
        _train(store, pools, "a020", root, FakeControls(stop_at=stop_at))
    out = read_outcome(root, "a020", MASTER)
    assert out is not None and out["status"] == "INCOMPLETE"
    assert out["arm"] == "a020" and out["master"] == MASTER
    assert isinstance(out["cause"], str) and out["cause"].startswith("StopRequested:")
    recorded = [c["checkpoint_id"] for c in out["checkpoints"]]
    assert sorted(recorded) == sorted(_ckpts(store))  # every written checkpoint is recorded
    assert len(recorded) < 3
    if stop_at == 1:
        assert recorded == []
    assert not (root / "RUN.lock").exists()


def test_second_start_refused_after_complete(root):
    store = memory_store()
    pools = _add_pools(store)
    _train(store, pools, "a0", root, FakeControls())
    before = (read_outcome(root, "a0", MASTER), sorted(_ckpts(store)))
    controls = FakeControls()
    with pytest.raises(RunLocked):
        _train(store, pools, "a0", root, controls)
    assert (read_outcome(root, "a0", MASTER), sorted(_ckpts(store))) == before


def test_second_start_refused_after_incomplete(root):
    store = memory_store()
    pools = _add_pools(store)
    with pytest.raises(StopRequested):
        _train(store, pools, "a0", root, FakeControls(stop_at=3))
    first = read_outcome(root, "a0", MASTER)
    n_ckpt = len(_ckpts(store))
    with pytest.raises(RunLocked):
        _train(store, pools, "a0", root, FakeControls())  # no retry, even when allowed
    assert read_outcome(root, "a0", MASTER) == first and len(_ckpts(store)) == n_ckpt


def test_existing_lock_refuses_start(root):
    store = memory_store()
    pools = _add_pools(store)
    lock = root / "RUN.lock"
    lock.write_text('{"pid": 0, "identity": {}, "utc": "x"}', encoding="utf-8")
    with pytest.raises(RunLocked):
        _train(store, pools, "a0", root, FakeControls())
    assert _ckpts(store) == []
    assert lock.exists()  # a refused start never removes another run's lock
