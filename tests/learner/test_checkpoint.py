"""L06 and stage-level checkpoint contracts."""

import dataclasses
import io

import pytest
import torch

from topo_pilot.contracts import (
    Checkpoint,
    ErrorCode,
    ObservationSet,
    SeedTree,
    StageFailure,
)
from topo_pilot.contracts.testing import memory_store, tiny_observations
from topo_pilot.learner import LearnerStage, TransformerLM, load_model

pytestmark = pytest.mark.learner


@pytest.fixture()
def store_ids(tiny_obs):
    store = memory_store()
    dev = dataclasses.replace(tiny_observations(R=4, seed=5), split="dev")
    ids = []
    for obs, name in ((tiny_obs, "train"), (dev, "dev")):
        ids.append(store.save(obs, config={"split": name}, parents=[], seed_map={},
                              consumer="dataset"))
    return store, ids


def _run(store_ids, model_cfg, train_cfg):
    store, (tr, dv) = store_ids
    stage = LearnerStage()
    ids = stage.run(tr, dv, model_cfg, train_cfg, SeedTree(1729), ("rep", 1729), store)
    return stage, ids, store, (tr, dv)


def test_L06_save_load_reproduces_logits(store_ids, model_cfg, train_cfg):
    stage, ids, store, (tr, dv) = _run(store_ids, model_cfg, train_cfg)
    assert len(ids) == 3 and stage.last_summary.checkpoint_ids == tuple(ids)
    ck = store.load(Checkpoint, ids[-1], consumer="learner")
    assert ck.run_id == "rep-1729" and ck.step == 12 and ck.observation_id == tr
    assert ck.model_config["d_model"] == 16 and ck.train_config["checkpoint_steps"] == [0, 5, 12]
    assert store.meta(ids[-1]).parent_ids == tuple(sorted((tr, dv)))
    model = load_model(ck)
    assert not model.training
    x = torch.randint(0, 4, (3, 33), generator=torch.Generator().manual_seed(2))
    raw = torch.load(io.BytesIO(ck.state), weights_only=True)
    ref = TransformerLM(model_cfg)
    ref.load_state_dict(raw["model"])
    assert (model(x).logits - ref.eval()(x).logits).abs().max() <= 1e-6
    assert set(raw) == {"model", "optimizer", "scheduler"}


def test_L06b_optimizer_flags_and_byte_determinism(store_ids, model_cfg, train_cfg):
    _, ids, store, _ = _run(store_ids, model_cfg, train_cfg)
    cks = [store.load(Checkpoint, i, consumer="learner") for i in ids]
    assert [c.has_optimizer_state for c in cks] == [False, False, True]
    assert [c.step for c in cks] == [0, 5, 12]
    assert set(torch.load(io.BytesIO(cks[0].state), weights_only=True)) == {"model"}
    # same run again into the same store: identical ids, no CHECKSUM_MISMATCH (bytes identical)
    _, ids2, _, _ = _run((store, store_ids[1]), model_cfg, train_cfg)
    assert ids2 == ids
    # serialising equal state twice yields identical bytes, even across a re-load / later time
    from topo_pilot.learner.stage import serialise_state
    model = load_model(cks[0])
    assert serialise_state(model, {}) == serialise_state(load_model(cks[0]), {})
    assert serialise_state(model, {}) == cks[0].state


def test_L06c_load_model_rejects_bad_checkpoint(store_ids, model_cfg, train_cfg):
    _, ids, store, _ = _run(store_ids, model_cfg, train_cfg)
    ck = store.load(Checkpoint, ids[0], consumer="learner")
    bad = dataclasses.replace(ck, model_config={**ck.model_config, "d_model": 32})
    with pytest.raises(StageFailure) as exc:
        load_model(bad)
    assert exc.value.code is ErrorCode.INVALID_CONFIG


def test_stage_reads_observations_only_with_learner_policy(store_ids):
    store, (tr, _) = store_ids
    assert isinstance(store.load(ObservationSet, tr, consumer="learner"), ObservationSet)
