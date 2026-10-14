"""Builder smoke tests for the scoring-only correction (x5g1-techbench-scoring-v2)."""

import numpy as np
import pytest
import torch

from topo_pilot.contracts import SeedTree
from topo_pilot.experiment import x5g1_scorebench as sb
from topo_pilot.experiment.x5g1t_score import kl_from_log_probs, p32_log_probs, regret_rows
from topo_pilot.learner import ModelConfig, TransformerLM

TINY = {"vocab_in": 37, "vocab_out": 36, "n_layers": 1, "d_model": 8, "n_heads": 2, "d_mlp": 16}


def test_projection_replaces_only_scoring_terms():
    v1 = {"train": 10.0, "init": 1.0, "devCE": 2.0, "scoring": 999.0, "ckpt_io": 3.0,
          "generation": 4.0, "bootstrap": 5.0, "fresh_test": 999.0, "exports": 6.0}
    p = sb.project(v1, s1=1.0, s2=0.5, s0=2.0)
    assert p["scoring"] == 6 * 27 * 1.5 + 60 and p["fresh_test"] == 6 * 1.5 + 60
    assert p["setup"] == 12.0
    assert p["total"] == pytest.approx(10 + 1 + 2 + 3 + 4 + 5 + 6 + p["scoring"]
                                       + p["fresh_test"] + 12)
    assert p["fits"] is (p["total"] <= sb.LIMIT_S)


def test_fixture_is_seedtree_only_and_positive(monkeypatch):
    monkeypatch.setattr(sb, "N_ROWS", 64)
    _, x1, q1 = sb.fixture(TINY)
    _, x2, q2 = sb.fixture(TINY)
    assert x1.shape == (64, 33) and torch.equal(x1, x2) and np.array_equal(q1, q2)
    assert (x1[:, 0] == 36).all() and q1.min() > 0


def test_batched_scoring_equals_single_pass():
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(1).seed("t"))
        model = TransformerLM(ModelConfig(**TINY))
    x = torch.from_numpy(SeedTree(1).generator("x").integers(0, 36, size=(70, 33)))
    x[:, 0] = 36
    q = SeedTree(1).generator("q").dirichlet(np.ones(36), size=70)
    a = regret_rows(model, x, q, batch=16)
    b = regret_rows(model, x, q, batch=70)
    assert a.shape == (70,) and np.allclose(a, b, atol=1e-10) and (a >= -1e-12).all()
    assert model.training  # training flag restored
    assert np.allclose(np.exp(p32_log_probs(model, x, 16)).sum(1), 1.0)


def test_kl_zero_and_support_rules():
    q = np.array([[0.5, 0.5, 0.0]])
    assert kl_from_log_probs(q, np.log(q + np.array([[0, 0, 1e-300]]))) == pytest.approx(0.0)
    with pytest.raises(Exception):
        kl_from_log_probs(q, np.array([[np.log(0.5), -np.inf, 0.0]]))
