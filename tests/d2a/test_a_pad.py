"""Independent T-PAD test (job 0028, author A), from D2A-FROZEN-v1 sections 2.2 and 11.4 and
tools/d2a/API.md only: padding a constructed history after t changes no activation, next-symbol
logit or joint logit at model positions <= t. Tiny MultiHorizonLM (4 layers, so every hook
including resid_post_3 exists), CPU, eval mode.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import torch

from topo_pilot.contracts import SequenceLayout
from topo_pilot.learner import ModelConfig
from topo_pilot.learner.multihorizon import MultiHorizonLM

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "d2a"), ("tools", "d1_seam"), ("tools", "x4_oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

import d1_seam  # noqa: E402
import d2a_world as W  # noqa: E402

pytestmark = pytest.mark.learner

CFG = ModelConfig(6, 5, n_layers=4, d_model=16, n_heads=2, d_mlp=32)
S0, S2, S3, A, B = 0, 1, 2, 3, 4


def _histories():
    t16 = tuple(W.template_enumeration(16)[5][1])
    t28 = tuple(W.template_enumeration(28)[4000][0])
    return {"h_star": d1_seam.H_STAR, "h_edge": d1_seam.H_EDGE, "h_a": d1_seam.H_A,
            "h_max": d1_seam.H_MAX, "tpl16": t16, "tpl28": t28, "len32": (A, S2, S3) * 10 + (A, B)}


@pytest.fixture(scope="module")
def model():
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(17)
        m = MultiHorizonLM(CFG, 3, 12345)
    return m.eval()


@pytest.mark.parametrize("name", list(_histories()))
def test_T_PAD_padding_after_t_changes_nothing_up_to_t(name, model):
    h = _histories()[name]
    t = len(h)
    padded = np.asarray(W.pad(h))
    assert padded.shape == (33,) and padded.dtype == np.uint8 and not padded[t:].any()
    rng = np.random.Generator(np.random.PCG64(t))
    rows = [padded]
    for fill in (B, S3):
        rows.append(np.concatenate([np.asarray(h, dtype=np.uint8),
                                    np.full(33 - t, fill, dtype=np.uint8)]))
    rows.append(np.concatenate([np.asarray(h, dtype=np.uint8),
                                rng.integers(0, 5, 33 - t).astype(np.uint8)]))
    x = torch.from_numpy(SequenceLayout().model_inputs(np.stack(rows), 5))
    assert torch.equal(x[0, 1:t + 1], torch.tensor(h, dtype=torch.int64))
    with torch.no_grad():
        out = model(x, return_hooks=model.hook_names)
    assert set(out.hooks) == set(model.hook_names) and "resid_post_3" in out.hooks
    tensors = {"logits": out.logits, **out.hooks,
               **{f"joint{k}": v for k, v in out.joint_logits.items()}}
    for key, val in tensors.items():
        ref = val[0, :t + 1]
        for r in range(1, len(rows)):
            assert float((val[r, :t + 1] - ref).abs().max()) <= 1e-6, (name, key, r)
    if t < 32:  # the probe bites: position t + 1 sees a different padded symbol
        assert float((out.logits[1, t + 1] - out.logits[0, t + 1]).abs().max()) > 0
