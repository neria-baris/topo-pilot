"""L01-L03, L09: architecture contracts."""

import ast
import pathlib

import pytest
import torch

import topo_pilot.learner as learner
from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.learner import HOOK_NAMES, TransformerLM

pytestmark = pytest.mark.learner


@pytest.fixture()
def model(model_cfg):
    torch.manual_seed(0)
    m = TransformerLM(model_cfg).eval()
    for p in m.parameters():  # larger weights make leaks detectable above 1e-6
        torch.nn.init.normal_(p, 0.0, 0.3) if p.ndim == 2 else None
    return m


def _inputs(cfg, batch=3, seed=1):
    gen = torch.Generator().manual_seed(seed)
    return torch.randint(0, cfg.vocab_in, (batch, cfg.n_ctx), generator=gen)


def test_L01_causality_every_position(model, model_cfg):
    x = _inputs(model_cfg)
    base = model(x).logits
    for j in range(1, model_cfg.n_ctx):
        x2 = x.clone()
        x2[:, j] = (x2[:, j] + 1) % model_cfg.vocab_in
        out = model(x2).logits
        assert (out[:, :j] - base[:, :j]).abs().max() <= 1e-6
    assert (out[:, -1] - base[:, -1]).abs().max() > 1e-4  # the perturbation does matter at >= j


def test_L01b_causal_mask_failed_raised_at_construction(monkeypatch, model_cfg):
    import torch.nn.functional as F
    real = F.scaled_dot_product_attention
    monkeypatch.setattr(F, "scaled_dot_product_attention",
                        lambda q, k, v, is_causal=True: real(q, k, v, is_causal=False))
    with pytest.raises(StageFailure) as exc:
        TransformerLM(model_cfg)
    assert exc.value.code is ErrorCode.CAUSAL_MASK_FAILED


def test_L02_shapes_and_hook_names(model, model_cfg):
    x = _inputs(model_cfg, batch=5)
    out = model(x, return_hooks=model.hook_names)
    assert out.logits.shape == (5, 33, model_cfg.vocab_out)
    assert model.hook_names == ("embed", "resid_post_0", "resid_post_1", "ln_final_out")
    assert set(out.hooks) == set(model.hook_names)
    for h in out.hooks.values():
        assert h.shape == (5, 33, model_cfg.d_model)
    assert HOOK_NAMES == ("embed", *(f"resid_post_{k}" for k in range(4)), "ln_final_out")
    assert model(x).hooks == {}
    with pytest.raises(StageFailure) as exc:
        model(x, return_hooks=("resid_post_9",))
    assert exc.value.code is ErrorCode.UNKNOWN_HOOK


def test_L03_resid_to_logits_exact(model, model_cfg):
    x = _inputs(model_cfg)
    out = model(x, return_hooks=("embed", "resid_post_1", "ln_final_out"))
    last = out.hooks["resid_post_1"]
    again = model.unembed(model.ln_final(last))
    assert torch.equal(again, out.logits)
    assert torch.equal(model.ln_final(last), out.hooks["ln_final_out"])
    pos = torch.arange(33)
    assert torch.equal(out.hooks["embed"], model.tok_emb(x) + model.pos_emb(pos))


def test_L09_no_forbidden_imports():
    forbidden = {"world", "process", "oracle", "analysis", "prediction"}
    root = pathlib.Path(learner.__file__).parent
    files = list(root.glob("*.py"))
    assert files
    for path in files:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = [node.module or ""]
            for name in names:
                parts = name.split(".")
                assert not (parts[0] == "topo_pilot" and len(parts) > 1
                            and parts[1] in forbidden), (path.name, name)
