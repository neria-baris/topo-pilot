"""Tests A01-A06 for the activations module (see TEST_PLAN.md)."""

from __future__ import annotations

import ast
import dataclasses
import sys
import types
from pathlib import Path

import numpy as np
import pytest
import torch

import topo_pilot.activations as act_pkg
from topo_pilot.activations import ActivationExtractor, ActivationStage
from topo_pilot.contracts import (
    ActivationSet,
    Checkpoint,
    ErrorCode,
    EvalSidecar,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.contracts.testing import memory_store

PANEL_SIZE = 4
V = 3

pytestmark = pytest.mark.activations

HOOKS = ("embed", "resid_post_1", "ln_final_out", "resid_post_0")


def test_A01_row_order_equals_index_order_for_any_batch_size(tiny_model, tiny_obs, tiny_index):
    results = [ActivationExtractor(HOOKS, batch_size=b, device="cpu")
               .extract(tiny_model, tiny_obs, tiny_index) for b in (1, 7, 256)]
    A0, L0, ids0 = results[0]
    assert ids0 == tiny_index.history_id.tolist()
    assert A0.dtype == np.float32 and L0.dtype == np.float32
    assert A0.shape == (len(ids0), len(HOOKS), 16) and L0.shape == (len(ids0), V)
    for A, L, ids in results[1:]:
        assert ids == ids0
        np.testing.assert_allclose(A, A0, atol=1e-6)
        np.testing.assert_allclose(L, L0, atol=1e-6)
    # the index is reversed relative to the observations: row i must be trajectory index[i]
    x = torch.from_numpy(SequenceLayout().model_inputs(tiny_obs.tokens[[-1]], tiny_obs.V))
    with torch.no_grad():
        ref = tiny_model(x, return_hooks=("embed",)).hooks["embed"][0, 32].numpy()
    np.testing.assert_allclose(A0[0, 0], ref, atol=1e-6)


def test_A02_logits_equal_plain_forward_at_position_32(tiny_model, tiny_obs, tiny_index):
    _, L, _ = ActivationExtractor(["ln_final_out"], batch_size=5, device="cpu").extract(
        tiny_model, tiny_obs, tiny_index)
    rows = [int(np.flatnonzero(tiny_obs.sequence_id == s)[0]) for s in tiny_index.sequence_id]
    x = torch.from_numpy(SequenceLayout().model_inputs(tiny_obs.tokens[rows], tiny_obs.V))
    with torch.no_grad():
        plain = tiny_model(x).logits[:, 32].numpy()
    assert np.abs(L - plain).max() <= 1e-5


def _extract_one(model, obs, build_index):
    return ActivationExtractor(HOOKS, device="cpu").extract(model, obs, build_index(obs))[0]


def test_A03_w33_invisible_w32_visible(tiny_model, tiny_obs, index_builder):
    base = _extract_one(tiny_model, tiny_obs, index_builder)
    tok33 = tiny_obs.tokens.copy()
    tok33[:, 32] = (tok33[:, 32] + 1) % V
    tok32 = tiny_obs.tokens.copy()
    tok32[:, 31] = (tok32[:, 31] + 1) % V
    np.testing.assert_array_equal(
        _extract_one(tiny_model, dataclasses.replace(tiny_obs, tokens=tok33), index_builder), base)
    changed = _extract_one(tiny_model, dataclasses.replace(tiny_obs, tokens=tok32), index_builder)
    assert np.abs(changed - base).max() > 1e-6


def test_A04_unknown_hook_and_corrupted_hash(tiny_model, tiny_obs, tiny_index):
    with pytest.raises(StageFailure) as exc:
        ActivationExtractor(["resid_post_9"], device="cpu").extract(
            tiny_model, tiny_obs, tiny_index)
    assert exc.value.code == ErrorCode.UNKNOWN_HOOK
    bad_hash = tiny_index.tokens_hash.copy()
    bad_hash[3] = "0" * 16
    bad = dataclasses.replace(tiny_index, tokens_hash=bad_hash)
    with pytest.raises(StageFailure) as exc:
        ActivationExtractor(["embed"], device="cpu").extract(tiny_model, tiny_obs, bad)
    assert exc.value.code == ErrorCode.ALIGNMENT_ERROR
    bad_end = dataclasses.replace(tiny_index, end=np.full(len(bad_hash), 31, dtype=np.int64))
    with pytest.raises(StageFailure) as exc:
        ActivationExtractor(["embed"], device="cpu").extract(tiny_model, tiny_obs, bad_end)
    assert exc.value.code == ErrorCode.ALIGNMENT_ERROR


def test_A04_numerical_failure_when_hooked_path_disagrees(tiny_obs, tiny_index, standin_cls):
    class Drifting(standin_cls):
        def forward(self, inputs, return_hooks=()):
            out = super().forward(inputs, return_hooks)
            if return_hooks:
                out.logits = out.logits + 1e-3
            return out

    with pytest.raises(StageFailure) as exc:
        ActivationExtractor(["embed"], device="cpu").extract(Drifting(), tiny_obs, tiny_index)
    assert exc.value.code == ErrorCode.NUMERICAL_FAILURE


def test_A05_panel_filter_returns_exactly_the_panel_ids(tiny_model, tiny_obs, tiny_index):
    A, L, ids = ActivationExtractor(["embed"], device="cpu").extract(
        tiny_model, tiny_obs, tiny_index, panels=[1])
    expected = tiny_index.history_id[tiny_index.panel == 1].tolist()
    assert len(ids) == PANEL_SIZE and ids == expected
    assert A.shape[0] == L.shape[0] == PANEL_SIZE
    _, _, ids23 = ActivationExtractor(["embed"], device="cpu").extract(
        tiny_model, tiny_obs, tiny_index, panels=[3, 2])
    assert ids23 == tiny_index.history_id[np.isin(tiny_index.panel, [2, 3])].tolist()


def _is_forbidden(name: str) -> bool:
    banned = {"world", "process", "oracle", "analysis", "prediction", "dataset"}
    parts = name.split(".")
    return parts[0] == "topo_pilot" and len(parts) > 1 and parts[1] in banned


def test_A06_static_imports_are_allowed_only():
    allowed_top = {"topo_pilot", "numpy", "torch", "__future__", "typing", "logging"}
    for path in Path(act_pkg.__file__).parent.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and not node.level:
                mods = [node.module or ""]
            for m in mods:
                assert not _is_forbidden(m), (path.name, m)
                assert m.split(".")[0] in allowed_top, (path.name, m)
                if m.startswith("topo_pilot."):
                    assert m.split(".")[1] in {"contracts", "learner"}, (path.name, m)


def test_A06_sidecar_access_raises_leakage_and_stage_roundtrip(
        tiny_model, tiny_obs, tiny_index, monkeypatch):
    store = memory_store()
    side = EvalSidecar(split="test", N=4, sequence_id=tiny_obs.sequence_id,
                       z=np.zeros(tiny_obs.tokens.shape, dtype=np.int16))
    sid = store.save(side, config={"k": 1}, parents=[], seed_map={}, consumer="dataset")
    with pytest.raises(StageFailure) as exc:
        store.load(EvalSidecar, sid, consumer="activations")
    assert exc.value.code == ErrorCode.LEAKAGE

    ckpt = Checkpoint(run_id="r", step=0, observation_id="o", state=b"x")
    cid = store.save(ckpt, config={"c": 1}, parents=[], seed_map={}, consumer="learner")
    oid = store.save(tiny_obs, config={"o": 1}, parents=[], seed_map={}, consumer="dataset")
    iid = store.save(tiny_index, config={"i": 1}, parents=[], seed_map={}, consumer="dataset")
    try:
        import topo_pilot.learner as learner_mod
    except ImportError:  # pragma: no cover - stand-in mode
        learner_mod = types.ModuleType("topo_pilot.learner")
        monkeypatch.setitem(sys.modules, "topo_pilot.learner", learner_mod)
    monkeypatch.setattr(learner_mod, "load_model", lambda c: tiny_model, raising=False)
    out = ActivationStage(device="cpu").run(cid, oid, iid, ["embed", "ln_final_out"], [2], store)
    got = store.load(ActivationSet, out, consumer="analysis")
    assert got.source == "model" and got.checkpoint_id == cid
    assert got.hooks == ("embed", "ln_final_out")
    assert got.history_id.tolist() == tiny_index.history_id[tiny_index.panel == 2].tolist()
    assert got.A.shape == (PANEL_SIZE, 2, 16) and got.logits.shape == (PANEL_SIZE, V)
