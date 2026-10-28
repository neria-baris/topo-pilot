"""Author B (job 0161), TEST_PLAN section 3 `test_b_e4path.py`: recipe check (DRB3), the
Trainer composition against `LearnerStage` (DRB2-type, tiny sizes), the checkpoint saver and
SentinelStop, logits/activation equalities (DRB6), thread settings and the torch lock line.
Tiny models and a few steps only; MemoryBackend stores. tools/hwsb/*.py unread."""

from __future__ import annotations

import dataclasses
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hwsb_dry as hdry  # noqa: E402
import hwsb_eval as he  # noqa: E402
import hwsb_train as ht  # noqa: E402
import c1_model  # noqa: E402
from topo_pilot.activations import ActivationExtractor  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore, Checkpoint, HistoryIndex, MemoryBackend, ObservationSet, SeedTree,
    SequenceLayout, make_history_id, payload_checksum, tokens_hash)
from topo_pilot.dataset import PublicTokenDataset  # noqa: E402
from topo_pilot.learner import (  # noqa: E402
    LearnerStage, ModelConfig, Trainer, TrainConfig, TransformerLM, load_model, serialise_state)

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
RECIPE = CONTRACT["recipe"]
TINY_MODEL = ModelConfig(**CONTRACT["dry_run"]["tiny_model"])
E4_MODEL = ModelConfig(**RECIPE["model_config"])
E4_TRAIN = TrainConfig(**{**RECIPE["train_config"],
                          "checkpoint_steps": tuple(RECIPE["train_config"]["checkpoint_steps"])})
MASTER = 629901


# ------------------------------------------------------------------ DRB3
def test_recipe_equals_contract_and_passes():
    assert hc.MODEL_CFG == E4_MODEL and hc.TRAIN_CFG == E4_TRAIN
    assert isinstance(hc.TRAIN_CFG.checkpoint_steps, tuple)
    assert ht.check_recipe(hc.MODEL_CFG, hc.TRAIN_CFG)["status"] == "PASS"


def test_recipe_equals_the_e4_checkpoint_extra_json():
    extra = REPO.parents[0] / "topo-pilot" / "artifacts" / "Checkpoint" / "c3358e3cb9c352fb" \
        / "extra.json"
    if not extra.is_file():
        pytest.skip("E4 checkpoint metadata not present")
    meta = json.loads(extra.read_text(encoding="utf-8"))  # JSON metadata only; no payload read
    assert dataclasses.asdict(hc.MODEL_CFG) == meta["model_config"]
    got = dataclasses.asdict(hc.TRAIN_CFG)
    got["checkpoint_steps"] = list(got["checkpoint_steps"])
    assert got == meta["train_config"]


CHANGES = {
    "vocab_in": 38, "vocab_out": 37, "n_ctx": 34, "n_layers": 3, "d_model": 64, "n_heads": 2,
    "d_mlp": 256, "dropout": 0.1, "tie_embeddings": True,
}
TRAIN_CHANGES = {
    "steps": 4999, "batch_size": 64, "lr": 2e-3, "warmup": 100, "weight_decay": 0.2,
    "grad_clip": 2.0, "checkpoint_steps": (0, 50, 100), "device": "cpu",
}


@pytest.mark.parametrize("field,value", list(CHANGES.items()))
def test_recipe_model_field_change_is_refused(field, value):
    res = ht.check_recipe(dataclasses.replace(E4_MODEL, **{field: value}), E4_TRAIN)
    assert res["status"] == "FAIL_TECHNICAL/KNOWN_CASE"
    assert any(field in str(d["field"]) for d in res["diff"])


@pytest.mark.parametrize("field,value", list(TRAIN_CHANGES.items()))
def test_recipe_train_field_change_is_refused(field, value):
    res = ht.check_recipe(E4_MODEL, dataclasses.replace(E4_TRAIN, **{field: value}))
    assert res["status"] == "FAIL_TECHNICAL/KNOWN_CASE"
    assert any(field in str(d["field"]) for d in res["diff"])


# ------------------------------------------------------------------ tiny DRB2-type world
def tiny_plan():
    train = TrainConfig(steps=10, batch_size=32, lr=1e-3, warmup=2, schedule="cosine",
                        weight_decay=0.1, grad_clip=1.0, checkpoint_steps=(0, 5, 10),
                        device="auto")
    base = hc.dry_plan("dry_tiny", "BE4")
    return dataclasses.replace(base, train_cfg=train, model_cfg=TINY_MODEL,
                               sizes={**base.sizes, "train": 512, "dev": 128})


def world(plan):
    store = ArtifactStore(MemoryBackend())
    proc = hdry.build_tiny_process(store)
    return store, hd.make_train_dev(store, proc, MASTER, plan)


@pytest.fixture(scope="module")
def stores():
    plan = tiny_plan()
    a, ids_a = world(plan)
    b, ids_b = world(plan)
    return plan, a, ids_a, b, ids_b


def test_identical_observation_sets_in_both_stores(stores):
    _, _, ids_a, _, ids_b = stores
    assert ids_a["train"] == ids_b["train"] and ids_a["dev"] == ids_b["dev"]


@pytest.fixture(scope="module")
def trained(stores):
    plan, a, ids_a, b, ids_b = stores
    mine = ht.train(a, {"train": ids_a["train"], "dev": ids_a["dev"]}, MASTER, plan)
    rk = hc.run_key(plan, MASTER)
    ref = LearnerStage().run(ids_b["train"], ids_b["dev"], plan.model_cfg, plan.train_cfg,
                             SeedTree(MASTER), rk, b)
    return mine, ref


def test_train_equals_learner_stage_bitwise(stores, trained):
    plan, a, _, b, _ = stores
    mine, ref = trained
    steps = list(plan.train_cfg.checkpoint_steps)
    assert [mine["checkpoint_ids"][s] for s in steps] == ref
    for s, cid in zip(steps, ref):
        assert mine["checksums"][s] == b.meta(cid).payload_sha256 == a.meta(cid).payload_sha256
    assert list(mine["run_key"]) == list(hc.run_key(plan, MASTER))
    assert mine["summary"]["steps_done"] == 10 and mine["holds"] == []


def test_sentinel_stop_keeps_in_memory_checkpoints(stores, trained):
    plan, a, ids_a, _, _ = stores
    mine, _ = trained
    train = a.load(ObservationSet, ids_a["train"], consumer="learner")
    dev = a.load(ObservationSet, ids_a["dev"], consumer="learner")
    seeds, rk = SeedTree(MASTER), hc.run_key(plan, MASTER)
    saver = ht.CheckpointSaver(None, ids_a["train"], ids_a["dev"], plan.model_cfg,
                               plan.train_cfg, seeds, rk, stop_after=5)
    layout = SequenceLayout()
    with pytest.raises(ht.SentinelStop) as e:
        Trainer(plan.model_cfg, plan.train_cfg, seeds, rk).fit(
            PublicTokenDataset(train, layout), PublicTokenDataset(dev, layout), saver)
    assert e.value.step == 5 and isinstance(e.value, Exception)
    assert sorted(saver.checkpoints) == [0, 5] and saver.ids == []
    for s in (0, 5):
        assert saver.checksums[s] == mine["checksums"][s]
        assert payload_checksum(*saver.checkpoints[s].to_payload()) == mine["checksums"][s]
        assert saver.dev_ce[s] == mine["dev_ce"][s]
    assert saver.train_loss[0] is None and saver.train_loss[5] is not None


def test_build_checkpoint_is_the_learner_stage_save_body():
    cfg = dataclasses.replace(TINY_MODEL)
    torch.manual_seed(0)
    model = TransformerLM(cfg)
    tc = tiny_plan().train_cfg
    got = ht.build_checkpoint(5, model, {"dev_ce": 1.0}, "run-x", "obs-1", cfg, tc)
    want = Checkpoint(run_id="run-x", step=5, observation_id="obs-1",
                      state=serialise_state(model, {}), model_config=dataclasses.asdict(cfg),
                      train_config=dataclasses.asdict(tc), has_optimizer_state=False)
    assert payload_checksum(*got.to_payload()) == payload_checksum(*want.to_payload())
    assert got.has_optimizer_state is False
    final = ht.build_checkpoint(10, model, {"optimizer_state": {}, "scheduler_state": {}},
                                "run-x", "obs-1", cfg, tc)
    assert final.has_optimizer_state is True


# ------------------------------------------------------------------ DRB6
def history(obs, dataset_id="drb6"):
    n = obs.tokens.shape[0]
    th = np.array([tokens_hash(np.asarray(obs.tokens[i, :32])) for i in range(n)], dtype="<U16")
    sid = obs.sequence_id
    hid = np.array([make_history_id(dataset_id, int(s), 32, h) for s, h in zip(sid, th)],
                   dtype="<U16")
    return HistoryIndex(dataset_id=dataset_id, history_id=hid, sequence_id=sid,
                        end=np.full(n, 32, dtype=np.int64), panel=np.ones(n, dtype=np.int64),
                        tokens_hash=th, panel_size=n, n_panels=1)


def test_logits32_equals_activation_extractor_bitwise():
    torch.manual_seed(1)
    model = TransformerLM(TINY_MODEL).eval()
    rng = np.random.default_rng(2)
    obs = ObservationSet(split="test", V=3, sequence_id=np.arange(300, dtype=np.int64) + 77,
                         tokens=rng.integers(0, 3, size=(300, 33)).astype(np.uint8))
    _, ref, _ = ActivationExtractor(("resid_post_0",), 256).extract(model, obs, history(obs))
    inputs = torch.from_numpy(SequenceLayout().model_inputs(obs.tokens, obs.V))
    got = he.logits32(model, inputs)
    assert got.dtype == np.float32 and got.shape == (300, 3)
    assert got.tobytes() == ref.tobytes()


def small_checkpoint(n_layers, seed=3, vocab=(37, 36)):
    cfg = ModelConfig(vocab_in=vocab[0], vocab_out=vocab[1], n_layers=n_layers, d_model=16,
                      n_heads=2, d_mlp=32)
    torch.manual_seed(seed)
    model = TransformerLM(cfg)
    ckpt = Checkpoint(run_id="r", step=0, observation_id="o", state=serialise_state(model, {}),
                      model_config=dataclasses.asdict(cfg),
                      train_config=dataclasses.asdict(E4_TRAIN), has_optimizer_state=False)
    return cfg, ckpt


def test_activations_at_site_equal_c1_model_bitwise():
    threads = torch.get_num_threads()
    try:
        _, ckpt = small_checkpoint(4)
        model64, sha = he.load64(ckpt)
        canon = np.random.default_rng(4).integers(0, 36, size=(20, 32)).astype(np.uint8)
        inputs = c1_model.model_inputs(canon)
        got = he.activations(model64, inputs, hc.SITE, hc.INDEX)
        ref = c1_model.activations(model64, inputs, 1024)
        assert got.dtype == np.float64 and got.shape == (20, 16) and got.tobytes() == ref.tobytes()
        assert he.activations(model64, inputs).tobytes() == ref.tobytes()
        assert isinstance(sha, str) and len(sha) == 64
        other = he.activations(model64, inputs, site="resid_post_0", index=32)
        with torch.no_grad():
            h = model64(inputs, return_hooks=("resid_post_0",)).hooks["resid_post_0"]
        assert other.tobytes() == h[:, 32, :].to(torch.float64).numpy().tobytes()
    finally:
        torch.set_num_threads(threads)


def test_model_predictive_is_canonical_softmax():
    _, ckpt = small_checkpoint(1, seed=5)
    rng = np.random.default_rng(6)
    perm = rng.permutation(36)
    canon = rng.integers(0, 36, size=(12, 32)).astype(np.uint8)
    got = he.model_predictive(ckpt, canon, perm)
    model = load_model(ckpt)
    x = torch.from_numpy(np.hstack([np.full((12, 1), 36), perm[canon.astype(np.int64)]]))
    with torch.no_grad():
        lg = model(x).logits[:, 32].float().numpy().astype(np.float64)
    p = np.exp(lg - lg.max(axis=1, keepdims=True))
    p /= p.sum(axis=1, keepdims=True)
    assert got.shape == (12, 36) and np.allclose(got, p[:, perm], rtol=1e-12, atol=1e-15)
    assert np.allclose(got.sum(axis=1), 1.0, atol=1e-6)


# ------------------------------------------------------------------ threads, torch lock
def test_set_threads_records_values(monkeypatch):
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        monkeypatch.setenv(var, "unset")
    before = torch.get_num_threads()
    try:
        info = ht.set_threads(1)
        assert info["requested"] == 1 and info["torch_threads"] == 1 == torch.get_num_threads()
        assert info["OMP_NUM_THREADS"] == "1" and info["MKL_NUM_THREADS"] == "1"
        assert os.environ["OMP_NUM_THREADS"] == os.environ["MKL_NUM_THREADS"] == "1"
        assert info["torch_version"] == torch.__version__
    finally:
        torch.set_num_threads(before)


def test_torch_versions_reads_the_lock_line(tmp_path):
    (tmp_path / "requirements.lock").write_text(
        "numpy==2.0.0\n  torch==9.9.9+cpu  \ntorchvision==1\n", encoding="utf-8")
    got = ht.torch_versions(tmp_path)
    assert got["lock"] == "torch==9.9.9+cpu" and got["in_use"] == torch.__version__
    assert ht.torch_versions()["lock"] == CONTRACT["known_cases"]["KB2"]["torch_lock"]["value"]
