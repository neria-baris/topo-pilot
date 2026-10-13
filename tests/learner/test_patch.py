"""Independent tests written by the X4-F test-writer agent from X4F_GATES_API.md / x4f-exec-v2
before reading the implementation.

Frozen-forward adapter ``forward_with_patch`` (X4F_GATES_API section 1; x4f-exec-v2 section 7).
"""

import ast
import pathlib

import pytest
import torch

import topo_pilot.learner as learner
from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.learner import ModelConfig, PatchedOutput, TransformerLM, forward_with_patch

pytestmark = pytest.mark.learner

SITES = ("resid_post_0", "resid_post_1", "ln_final_out")
CFG = ModelConfig(vocab_in=4, vocab_out=3, n_layers=2, d_model=16, n_heads=2, d_mlp=32)


@pytest.fixture()
def model():
    torch.manual_seed(0)
    m = TransformerLM(CFG).eval()
    with torch.no_grad():  # larger weights make leaks / missed recomputation detectable
        for p in m.parameters():
            if p.ndim == 2:
                torch.nn.init.normal_(p, 0.0, 0.3)
    return m


def _inputs(batch=3, length=33, seed=1):
    gen = torch.Generator().manual_seed(seed)
    return torch.randint(0, CFG.vocab_in, (batch, length), generator=gen)


def _rand_rep(batch=3, seed=7, scale=2.0):
    gen = torch.Generator().manual_seed(seed)
    return scale * torch.randn(batch, CFG.d_model, generator=gen)


def _reference(model, x, site, index, rep):
    """Spec section 1 computation written out with the model's public submodules."""
    with torch.no_grad():
        h = model.tok_emb(x) + model.pos_emb(torch.arange(x.shape[1]))
        if site == "ln_final_out":
            for blk in model.blocks:
                h = blk(h)
            normed = model.ln_final(h).clone()
            normed[:, index, :] = rep
            return model.unembed(normed)
        k = int(site.rsplit("_", 1)[1])
        for j in range(k + 1):
            h = model.blocks[j](h)
        h = h.clone()
        h[:, index, :] = rep
        for j in range(k + 1, len(model.blocks)):
            h = model.blocks[j](h)
        return model.unembed(model.ln_final(h))


# --------------------------------------------------------------------------- identity / shapes

@pytest.mark.parametrize("site", SITES)
@pytest.mark.parametrize("index", [0, 13, 32])
def test_identity_replacement_reproduces_all_logits(model, site, index):
    x = _inputs()
    with torch.no_grad():
        base = model(x, return_hooks=[site])
    rep = base.hooks[site][:, index, :].clone()
    out = forward_with_patch(model, x, site, index, rep)
    assert isinstance(out, PatchedOutput)
    assert out.logits.shape == (3, 33, CFG.vocab_out)
    assert out.logits.dtype == torch.float32
    assert (out.logits - base.logits).abs().max().item() <= 1e-6


def test_identity_on_shorter_sequence(model):
    x = _inputs(batch=2, length=9, seed=4)
    with torch.no_grad():
        base = model(x, return_hooks=["resid_post_0"])
    out = forward_with_patch(model, x, "resid_post_0", 8, base.hooks["resid_post_0"][:, 8].clone())
    assert out.logits.shape == (2, 9, CFG.vocab_out)
    assert (out.logits - base.logits).abs().max().item() <= 1e-6


# ------------------------------------------------------------- causality / known answer

@pytest.mark.parametrize("site", SITES)
@pytest.mark.parametrize("index", [5, 20, 32])
def test_causality_non_identity_patch(model, site, index):
    x = _inputs()
    with torch.no_grad():
        base = model(x).logits
    out = forward_with_patch(model, x, site, index, _rand_rep())
    assert (out.logits[:, :index] - base[:, :index]).abs().max().item() <= 1e-6
    assert (out.logits[:, index] - base[:, index]).abs().max().item() > 1e-4


@pytest.mark.parametrize("site", SITES)
def test_patch_matches_spec_reference_computation(model, site):
    x = _inputs(seed=3)
    rep = _rand_rep(seed=11)
    out = forward_with_patch(model, x, site, 17, rep)
    ref = _reference(model, x, site, 17, rep)
    assert (out.logits - ref).abs().max().item() <= 1e-5


def test_resid_post_0_patch_propagates_to_later_positions(model):
    """The forward continues through blocks[1]: later positions attend to the patched vector."""
    x = _inputs()
    with torch.no_grad():
        base = model(x).logits
    out = forward_with_patch(model, x, "resid_post_0", 10, _rand_rep(scale=5.0))
    assert (out.logits[:, 11:] - base[:, 11:]).abs().max().item() > 1e-4


def test_ln_final_out_patch_touches_only_index(model):
    x = _inputs()
    with torch.no_grad():
        base = model(x).logits
    out = forward_with_patch(model, x, "ln_final_out", 10, _rand_rep())
    others = [j for j in range(33) if j != 10]
    assert (out.logits[:, others] - base[:, others]).abs().max().item() <= 1e-6


def test_ln_final_out_has_no_second_layernorm(model):
    with torch.no_grad():
        gen = torch.Generator().manual_seed(5)
        model.ln_final.weight.copy_(0.5 + torch.rand(CFG.d_model, generator=gen) * 2.0)
        model.ln_final.bias.copy_(torch.randn(CFG.d_model, generator=gen))
    assert model.ln_final.weight.std().item() > 0.1 and model.ln_final.bias.abs().max() > 0.1
    x = _inputs()
    rep = _rand_rep(seed=9, scale=3.0)
    for index in (0, 32):
        out = forward_with_patch(model, x, "ln_final_out", index, rep)
        expected = rep @ model.unembed.weight.detach().T
        assert (out.logits[:, index] - expected).abs().max().item() <= 1e-5
        # a second LayerNorm (with the non-trivial gamma / beta) would give something else
        again = model.unembed(model.ln_final(rep)).detach()
        assert (again - expected).abs().max().item() > 1e-2


# --------------------------------------------------------------------------- hooks

@pytest.mark.parametrize("site", SITES)
def test_hook_at_site_shows_replacement(model, site):
    x = _inputs()
    rep = _rand_rep()
    out = forward_with_patch(model, x, site, 12, rep, return_hooks=[site])
    assert set(out.hooks) == {site}
    h = out.hooks[site]
    assert h.shape == (3, 33, CFG.d_model)
    assert (h[:, 12] - rep).abs().max().item() == 0.0
    with torch.no_grad():
        base = model(x, return_hooks=[site]).hooks[site]
    assert (h[:, :12] - base[:, :12]).abs().max().item() <= 1e-6


def test_hooks_downstream_are_after_the_patch(model):
    x = _inputs()
    rep = _rand_rep()
    names = ("embed", "resid_post_0", "resid_post_1", "ln_final_out")
    out = forward_with_patch(model, x, "resid_post_0", 12, rep, return_hooks=names)
    assert set(out.hooks) == set(names)
    with torch.no_grad():
        base = model(x, return_hooks=names).hooks
    assert (out.hooks["embed"] - base["embed"]).abs().max().item() <= 1e-6
    assert (out.hooks["resid_post_0"][:, 12] - rep).abs().max().item() == 0.0
    # resid_post_1 is recomputed from the patched stream
    assert (out.hooks["resid_post_1"][:, 12] - base["resid_post_1"][:, 12]).abs().max() > 1e-4
    with torch.no_grad():
        relog = model.unembed(out.hooks["ln_final_out"])
        renorm = model.ln_final(out.hooks["resid_post_1"])
    assert (relog - out.logits).abs().max().item() <= 1e-5
    assert (renorm - out.hooks["ln_final_out"]).abs().max().item() <= 1e-5


def test_no_hooks_by_default(model):
    out = forward_with_patch(model, _inputs(), "resid_post_1", 3, _rand_rep())
    assert out.hooks == {}


# --------------------------------------------------------------------------- no side effects

@pytest.mark.parametrize("site", SITES)
def test_parameters_and_buffers_bitwise_unchanged(model, site):
    before = {k: v.detach().clone() for k, v in model.state_dict().items()}
    x = _inputs()
    out = forward_with_patch(model, x, site, 4, _rand_rep(), return_hooks=[site])
    after = model.state_dict()
    assert set(after) == set(before)
    for k, v in before.items():
        assert torch.equal(v, after[k]), k
    assert model.training is False
    assert not out.logits.requires_grad
    assert all(p.grad is None for p in model.parameters())


def test_inputs_and_replacement_not_mutated(model):
    x = _inputs()
    x0 = x.clone()
    rep = _rand_rep()
    rep0 = rep.clone()
    forward_with_patch(model, x, "resid_post_1", 4, rep)
    assert torch.equal(x, x0) and torch.equal(rep, rep0)


# --------------------------------------------------------------------------- errors

def _code(fn):
    with pytest.raises(StageFailure) as exc:
        fn()
    return exc.value.code


def test_training_mode_is_invalid_config(model):
    model.train()
    x = _inputs()
    assert _code(lambda: forward_with_patch(model, x, "resid_post_1", 3, _rand_rep())) \
        is ErrorCode.INVALID_CONFIG
    assert model.training is True  # the adapter never toggles the mode


@pytest.mark.parametrize("site", ["embed", "resid_post_9", "resid_post_2", "foo", "resid_post_",
                                  "ln_final"])
def test_unknown_site(model, site):
    assert _code(lambda: forward_with_patch(model, _inputs(), site, 3, _rand_rep())) \
        is ErrorCode.UNKNOWN_HOOK


@pytest.mark.parametrize("hooks", [("foo",), ("resid_post_9",), ("resid_post_1", "bar")])
def test_unknown_return_hook(model, hooks):
    assert _code(lambda: forward_with_patch(model, _inputs(), "resid_post_1", 3, _rand_rep(),
                                            return_hooks=hooks)) is ErrorCode.UNKNOWN_HOOK


@pytest.mark.parametrize("index", [-1, 33, 100])
def test_index_out_of_range(model, index):
    assert _code(lambda: forward_with_patch(model, _inputs(), "resid_post_1", index, _rand_rep())) \
        is ErrorCode.ALIGNMENT_ERROR


def test_index_out_of_range_for_short_sequence(model):
    x = _inputs(length=10)
    assert _code(lambda: forward_with_patch(model, x, "ln_final_out", 10, _rand_rep())) \
        is ErrorCode.ALIGNMENT_ERROR


@pytest.mark.parametrize("shape", [(3, 17), (3, 15), (2, 16), (4, 16), (16,), (3, 1, 16)])
def test_replacement_wrong_shape(model, shape):
    rep = torch.zeros(shape)
    assert _code(lambda: forward_with_patch(model, _inputs(), "resid_post_0", 3, rep)) \
        is ErrorCode.ALIGNMENT_ERROR


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("site", SITES)
def test_non_finite_replacement(model, bad, site):
    rep = _rand_rep()
    rep[1, 5] = bad
    assert _code(lambda: forward_with_patch(model, _inputs(), site, 3, rep)) \
        is ErrorCode.NUMERICAL_FAILURE


@pytest.mark.parametrize("make", [
    lambda: torch.randint(0, 4, (33,)),                     # 1-D
    lambda: torch.randint(0, 4, (3, 33, 1)),                # 3-D
    lambda: torch.randint(0, 4, (3, 33)).float(),           # not integer
    lambda: torch.full((3, 33), 4, dtype=torch.long),       # token == vocab_in
    lambda: torch.full((3, 33), -1, dtype=torch.long),      # negative token
    lambda: torch.randint(0, 4, (3, 34)),                   # L > n_ctx
])
def test_bad_inputs_alignment_error(model, make):
    x = make()
    assert _code(lambda: forward_with_patch(model, x, "resid_post_1", 3, _rand_rep())) \
        is ErrorCode.ALIGNMENT_ERROR


def test_single_out_of_vocab_token(model):
    x = _inputs()
    x[2, 30] = CFG.vocab_in
    assert _code(lambda: forward_with_patch(model, x, "resid_post_1", 3, _rand_rep())) \
        is ErrorCode.ALIGNMENT_ERROR


# --------------------------------------------------------------------------- imports

def test_patch_module_imports_no_forbidden_modules():
    forbidden = {"world", "process", "oracle", "analysis", "prediction"}
    path = pathlib.Path(learner.__file__).parent / "patch.py"
    assert path.is_file()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                mods = [node.module or ""]
            elif node.level >= 2:  # relative import leaving the learner package
                base = (node.module or "").split(".")[0]
                mods = [f"topo_pilot.{base}"] if base else \
                    [f"topo_pilot.{a.name}" for a in node.names]
        for name in mods:
            parts = name.split(".")
            assert not (parts[0] == "topo_pilot" and len(parts) > 1 and parts[1] in forbidden), name
