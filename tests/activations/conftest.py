"""Module-local fixtures: tiny model (real TransformerLM if importable, else a stand-in)."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest
import torch
from torch import nn

from topo_pilot.contracts import HistoryIndex, make_history_id, tokens_hash
from topo_pilot.contracts.testing import tiny_observations

V = 3
N_LAYERS = 2
D_MODEL = 16
PANEL_SIZE = 4
N_PANELS = 3
DATASET_ID = "ds_tiny"


class StandInLM(nn.Module):
    """Stand-in for ``learner.TransformerLM`` implementing only its public interface.

    Causal by construction: each block adds ``tanh(Linear(cumulative mean of the stream))``.
    """

    def __init__(self, n_layers: int = N_LAYERS, d_model: int = D_MODEL, vocab: int = V):
        super().__init__()
        self.cfg = SimpleNamespace(n_layers=n_layers, d_model=d_model, vocab_in=vocab + 1,
                                   vocab_out=vocab)
        self.tok = nn.Embedding(vocab + 1, d_model)
        self.pos = nn.Embedding(33, d_model)
        self.blocks = nn.ModuleList(nn.Linear(d_model, d_model) for _ in range(n_layers))
        self.ln = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab, bias=False)

    def forward(self, inputs, return_hooks=()):
        x = self.tok(inputs) + self.pos(torch.arange(inputs.shape[1]))
        hooks = {"embed": x}
        counts = torch.arange(1, inputs.shape[1] + 1).view(1, -1, 1)
        for k, block in enumerate(self.blocks):
            x = x + torch.tanh(block(torch.cumsum(x, dim=1) / counts))
            hooks[f"resid_post_{k}"] = x
        hooks["ln_final_out"] = self.ln(x)
        out = SimpleNamespace(logits=self.unembed(hooks["ln_final_out"]),
                              hooks={n: hooks[n] for n in return_hooks})
        return out


def _real_learner():
    try:
        from topo_pilot.learner import ModelConfig, TransformerLM
    except ImportError:
        return None
    return ModelConfig, TransformerLM


@pytest.fixture(scope="session")
def tiny_model() -> nn.Module:
    torch.manual_seed(0)
    real = _real_learner()
    if real is None:
        return StandInLM().eval()
    model_config, transformer_lm = real
    cfg = model_config(vocab_in=V + 1, vocab_out=V, n_layers=N_LAYERS, d_model=D_MODEL,
                       n_heads=2, d_mlp=32)
    return transformer_lm(cfg).eval()


def build_index(obs, order=None) -> HistoryIndex:
    """HistoryIndex over ``obs`` rows in ``order`` (default reversed); panels interleaved."""
    rows = list(range(len(obs.sequence_id)))[::-1] if order is None else list(order)
    sid = obs.sequence_id[rows].astype(np.int64)
    hashes = [tokens_hash(obs.tokens[r, :32]) for r in rows]
    ids = [make_history_id(DATASET_ID, int(s), 32, h) for s, h in zip(sid, hashes)]
    return HistoryIndex(
        dataset_id=DATASET_ID, history_id=np.array(ids, dtype="<U16"), sequence_id=sid,
        end=np.full(len(rows), 32, dtype=np.int64),
        panel=(np.arange(len(rows)) % N_PANELS + 1).astype(np.int64),
        tokens_hash=np.array(hashes, dtype="<U16"), panel_size=PANEL_SIZE, n_panels=N_PANELS)


@pytest.fixture(scope="session")
def tiny_obs():
    return tiny_observations(R=PANEL_SIZE * N_PANELS, seed=1)


@pytest.fixture(scope="session")
def tiny_index(tiny_obs) -> HistoryIndex:
    return build_index(tiny_obs)


@pytest.fixture(scope="session")
def index_builder():
    return build_index


@pytest.fixture(scope="session")
def standin_cls():
    return StandInLM
