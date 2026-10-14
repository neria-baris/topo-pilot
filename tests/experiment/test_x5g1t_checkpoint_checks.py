"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.
"""

from __future__ import annotations

import dataclasses
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, ObservationSet
from topo_pilot.contracts.testing import tiny_observations
from topo_pilot.experiment.x5g1t_train import study_run_key, study_train_config
from topo_pilot.learner import ModelConfig


def _ck():
    return importlib.import_module("topo_pilot.experiment.x5g1t_checks")
MODEL = dataclasses.asdict(ModelConfig(vocab_in=4, vocab_out=3, n_layers=1, d_model=8, n_heads=2,
                                       d_mlp=16))


def _rt(obj):
    return json.loads(json.dumps(obj))


def _flip(h: str) -> str:
    return h[:-1] + ("0" if h[-1] != "0" else "1")


# =============================== §5 checkpoints and full hashes ==================================
STEPS, GRID = 4, (0, 2, 4)
MASTER = 310001


def _obs(split: str, seed: int) -> ObservationSet:
    base = tiny_observations(R=8, seed=seed)
    return ObservationSet(split=split, V=3, sequence_id=np.arange(8, dtype=np.int64) + 100 * seed,
                          tokens=base.tokens)


def _ckstore(root: Path):
    st = ArtifactStore(LocalFSBackend(root))
    kw = dict(parents=[], seed_map={}, consumer="experiment")
    train = st.save(_obs("train", 1), config={"role": "train"}, **kw)
    dev = st.save(_obs("dev", 2), config={"role": "dev"}, **kw)
    other = st.save(_obs("dev", 3), config={"role": "other"}, **kw)
    return st, train, dev, other


def _save_run(st, train_id, dev_id, *, master=MASTER, run_master=None, grid=GRID, steps=STEPS,
              model=MODEL, train_cfg=None, parents=None, obs_id=None) -> dict:
    run_key = study_run_key(run_master if run_master is not None else master)
    tc = train_cfg or dataclasses.asdict(study_train_config(steps, grid))
    rec = []
    for step in grid:
        ck = Checkpoint(run_id="-".join(map(str, run_key)), step=step,
                        observation_id=obs_id or train_id, state=f"weights-{step}".encode(),
                        model_config=model, train_config=tc)
        config = {"run_key": list(run_key), "step": step, "model_config": model,
                  "train_config": tc}
        cid = st.save(ck, config=config, parents=parents or [train_id, dev_id], seed_map={},
                      consumer="experiment")
        rec.append({"step": step, "checkpoint_id": cid,
                    "payload_sha256": st.meta(cid).payload_sha256})
    return {"status": "COMPLETE", "arm": "a0", "master": master, "checkpoints": rec,
            "cause": None}


def _cfg(grid=GRID, steps=STEPS, model=None):
    return SimpleNamespace(grid=grid, steps=steps, model_config=dict(model or MODEL))


@pytest.fixture
def ckrun(tmp_path):
    st, train, dev, other = _ckstore(tmp_path / "store")
    outcome = _save_run(st, train, dev)
    return SimpleNamespace(st=st, train=train, dev=dev, other=other, outcome=outcome,
                           root=tmp_path / "store", tmp=tmp_path)


@pytest.mark.parametrize("grid", [list(GRID), tuple(GRID)])
def test_validate_checkpoints_real_store_passes(ckrun, grid):
    cid0 = ckrun.outcome["checkpoints"][0]["checkpoint_id"]
    assert isinstance(ckrun.st.meta(cid0).config["train_config"]["checkpoint_steps"], list)
    got = _ck().validate_checkpoints(ckrun.st, ckrun.outcome, _cfg(grid=grid), "a0", MASTER,
                                     ckrun.train, ckrun.dev)
    assert set(got) == {c["checkpoint_id"] for c in ckrun.outcome["checkpoints"]}
    for c in ckrun.outcome["checkpoints"]:
        ck, sha = got[c["checkpoint_id"]]
        # "(Checkpoint, sha)": the verify_full expected form (class) or a loaded instance
        assert (ck is Checkpoint or isinstance(ck, Checkpoint)) and sha == c["payload_sha256"]


def test_validate_checkpoints_model_config_compared_with_defaults_filled(ckrun):
    partial = {"vocab_in": 4, "vocab_out": 3, "n_layers": 1, "d_model": 8, "n_heads": 2,
               "d_mlp": 16}
    _ck().validate_checkpoints(ckrun.st, ckrun.outcome, _cfg(model=partial), "a0", MASTER,
                               ckrun.train, ckrun.dev)


def _fails(ckrun, outcome=None, cfg=None, arm="a0", master=MASTER, train=None, dev=None,
           st=None):
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st or ckrun.st, outcome or ckrun.outcome, cfg or _cfg(), arm,
                                master, train or ckrun.train, dev or ckrun.dev)


def test_checkpoints_reordered_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"] = o["checkpoints"][::-1]
    _fails(ckrun, outcome=o)


def test_checkpoints_swapped_ids_same_steps_rejected(ckrun):
    o = _rt(ckrun.outcome)
    a, b = o["checkpoints"][0], o["checkpoints"][1]
    a["checkpoint_id"], b["checkpoint_id"] = b["checkpoint_id"], a["checkpoint_id"]
    a["payload_sha256"], b["payload_sha256"] = b["payload_sha256"], a["payload_sha256"]
    _fails(ckrun, outcome=o)


def test_checkpoints_missing_one_rejected(ckrun):
    o = _rt(ckrun.outcome)
    del o["checkpoints"][1]
    _fails(ckrun, outcome=o)


def test_checkpoints_grid_differs_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(grid=(0, 1, 4)))


def test_checkpoints_wrong_dev_parent_rejected(ckrun):
    _fails(ckrun, dev=ckrun.other)


def test_checkpoints_saved_with_wrong_parents_rejected(tmp_path):
    st, train, dev, other = _ckstore(tmp_path / "s2")
    outcome = _save_run(st, train, dev, parents=[train, other])
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_wrong_model_config_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(model=dict(MODEL, d_model=16)))


def test_checkpoints_wrong_steps_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(steps=STEPS + 2, grid=GRID))


def test_checkpoints_saved_with_wrong_train_config_rejected(tmp_path):
    st, train, dev, _ = _ckstore(tmp_path / "s3")
    tc = dataclasses.asdict(dataclasses.replace(study_train_config(STEPS, GRID), lr=5e-3))
    outcome = _save_run(st, train, dev, train_cfg=tc)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_outcome_arm_mismatch_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["arm"] = "a020"
    _fails(ckrun, outcome=o)
    _fails(ckrun, arm="a020")


def test_checkpoints_outcome_master_mismatch_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["master"] = 310002
    _fails(ckrun, outcome=o)
    _fails(ckrun, master=310002)


def test_checkpoints_of_another_master_rejected(tmp_path):
    """outcome claims master 310001 but the checkpoints carry 310002's run key."""
    st, train, dev, _ = _ckstore(tmp_path / "s4")
    outcome = _save_run(st, train, dev, master=MASTER, run_master=310002)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_wrong_observation_id_rejected(tmp_path):
    st, train, dev, _ = _ckstore(tmp_path / "s5")
    outcome = _save_run(st, train, dev, obs_id=dev)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_recorded_sha_wrong_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"][2]["payload_sha256"] = _flip(o["checkpoints"][2]["payload_sha256"])
    _fails(ckrun, outcome=o)


def test_checkpoints_not_a_checkpoint_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"][0]["checkpoint_id"] = ckrun.train
    o["checkpoints"][0]["payload_sha256"] = ckrun.st.meta(ckrun.train).payload_sha256
    _fails(ckrun, outcome=o)


def test_checkpoints_same_metadata_mutated_payload_rejected(ckrun):
    cid = ckrun.outcome["checkpoints"][1]["checkpoint_id"]
    meta_before = (ckrun.root / "Checkpoint" / cid / "meta.json").read_bytes()
    (ckrun.root / "Checkpoint" / cid / "state.pt").write_bytes(b"tampered-weights")
    assert (ckrun.root / "Checkpoint" / cid / "meta.json").read_bytes() == meta_before
    _fails(ckrun)


# ---- verify_full ------------------------------------------------------------------------------
def test_verify_full_passes_on_lawful_artifacts(ckrun):
    exp = {ckrun.train: (ObservationSet, ckrun.st.meta(ckrun.train).payload_sha256)}
    for c in ckrun.outcome["checkpoints"]:
        exp[c["checkpoint_id"]] = (Checkpoint, c["payload_sha256"])
    assert _ck().verify_full(ckrun.st, exp, "before") is None


def test_verify_full_missing_id_rejected(ckrun):
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {"0123456789abcdef": (ObservationSet, "0" * 64)}, "before")


def test_verify_full_wrong_sha_rejected(ckrun):
    ck = _ck()
    sha = ckrun.st.meta(ckrun.train).payload_sha256
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {ckrun.train: (ObservationSet, _flip(sha))}, "before")


def test_verify_full_wrong_class_rejected(ckrun):
    ck = _ck()
    sha = ckrun.st.meta(ckrun.train).payload_sha256
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {ckrun.train: (Checkpoint, sha)}, "before")


def test_verify_full_mutated_payload_rejected(ckrun):
    c = ckrun.outcome["checkpoints"][0]
    (ckrun.root / "Checkpoint" / c["checkpoint_id"] / "state.pt").write_bytes(b"x")
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {c["checkpoint_id"]: (Checkpoint, c["payload_sha256"])},
                       "after")
