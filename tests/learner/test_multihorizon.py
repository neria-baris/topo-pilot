"""Independent tests of learner/multihorizon.py and the Trainer injection (job 0028, author A).

Written from D2A-FROZEN-v1 (sections 4.3-4.6, 11.4) and tools/d2a/API.md section 1 only, before
the module existed. Ids: T-TRUNK, T-HEAD, T-CAUS, T-TARGET, T-LOSS, T-GRAD, T-RNG, T-LOAD,
T-DECAY. Hand references use plain Python / torch, never the module's own loss code.
"""

from __future__ import annotations

import dataclasses
import io
import math
from functools import partial

import numpy as np
import pytest
import torch
from torch import nn

from topo_pilot.contracts import (
    Checkpoint,
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import (
    ModelConfig,
    ModelOutput,
    TrainConfig,
    Trainer,
    TransformerLM,
    load_model,
    serialise_state,
)
from topo_pilot.learner.multihorizon import (
    MultiHorizonLM,
    MultiHorizonOutput,
    check_causal_joint,
    joint_index,
    load_multi_horizon,
    multi_horizon_loss,
)
from topo_pilot.learner.trainer import lm_loss

pytestmark = pytest.mark.learner

TINY = ModelConfig(6, 5, n_layers=1, d_model=16, n_heads=2, d_mlp=32)
DEEP = ModelConfig(6, 5, n_layers=4, d_model=16, n_heads=2, d_mlp=32)  # has resid_post_3
STEP0 = TrainConfig(steps=1, warmup=1, batch_size=4, checkpoint_steps=(0,), device="cpu")
SEEDS_MASTER, RUN_KEY = 1729, ("d2a", 1)
AUX = SeedTree(SEEDS_MASTER).seed("init_joint", "d2a", 1)
JOINT = {2: ("joint.2.weight",), 3: ("joint.2.weight", "joint.3.weight")}


def _x(n=3, seed=2, vocab=6):
    return torch.randint(0, vocab, (n, 33), generator=torch.Generator().manual_seed(seed))


def _mh(horizon, aux=AUX, cfg=TINY, seed=11):
    torch.manual_seed(seed)
    return MultiHorizonLM(cfg, horizon, aux).eval()


def _ds(split, n, seed):
    tokens = np.random.Generator(np.random.PCG64(seed)).integers(0, 5, (n, 33)).astype(np.uint8)
    obs = ObservationSet(split=split, V=5, sequence_id=np.arange(n, dtype=np.int64),
                         tokens=tokens)
    return PublicTokenDataset(obs, SequenceLayout())


@pytest.fixture(scope="module")
def data():
    return _ds("train", 16, 0), _ds("dev", 8, 1)


def _trainer(horizon, train_cfg=STEP0, cfg=TINY):
    seeds = SeedTree(SEEDS_MASTER)
    if horizon == 1:
        return Trainer(cfg, train_cfg, seeds, RUN_KEY)
    return Trainer(cfg, train_cfg, seeds, RUN_KEY,
                   model_factory=partial(MultiHorizonLM, horizon=horizon, aux_seed=AUX),
                   loss_fn=partial(multi_horizon_loss, horizon=horizon))


def _fit(horizon, data, train_cfg=STEP0):
    seen = {}

    def cb(step, model, info):
        seen[step] = ({k: v.detach().clone() for k, v in model.state_dict().items()}, info)

    trainer = _trainer(horizon, train_cfg)
    summary = trainer.fit(data[0], data[1], cb)
    return trainer, summary, seen


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_TRUNK_model_level_trunk_and_logits_bitwise(horizon):
    torch.manual_seed(5)
    ref = TransformerLM(TINY).eval()
    torch.manual_seed(5)
    mh = MultiHorizonLM(TINY, horizon, AUX).eval()
    ref_sd, mh_sd = ref.state_dict(), mh.state_dict()
    assert set(mh_sd) == set(ref_sd) | set(JOINT[horizon])  # names stay unprefixed
    assert all(torch.equal(mh_sd[k], ref_sd[k]) for k in ref_sd)
    with torch.no_grad():
        assert torch.equal(mh(_x()).logits, ref(_x()).logits)


def test_T_TRUNK_trainer_step0_trunks_equal_across_horizons(data):
    states, dev = {}, {}
    for horizon in (1, 2, 3):
        trainer, summary, seen = _fit(horizon, data)
        states[horizon] = seen[0][0]
        dev[horizon] = summary.dev_ce_by_step[0]
        assert isinstance(trainer.model, TransformerLM if horizon == 1 else MultiHorizonLM)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(SEEDS_MASTER).seed("init", *RUN_KEY))
        fresh = TransformerLM(TINY).state_dict()
    for horizon in (1, 2, 3):
        assert set(states[horizon]) == set(fresh) | set(JOINT.get(horizon, ()))
        assert all(torch.equal(states[horizon][k], fresh[k]) for k in fresh), horizon
    assert dev[1] == dev[2] == dev[3]  # next-symbol dev CE from identical trunks
    assert torch.equal(states[2]["joint.2.weight"], states[3]["joint.2.weight"])  # T-HEAD


def test_trainer_uses_loss_fn_for_joint_heads(data):
    cfg = TrainConfig(steps=2, warmup=1, batch_size=4, checkpoint_steps=(0, 2), device="cpu")
    _, summary, seen = _fit(3, data, cfg)
    for name in JOINT[3]:  # heads get gradient only through loss_fn
        assert not torch.equal(seen[0][0][name], seen[2][0][name]), name
    assert math.isfinite(summary.final_train_loss)


def test_T_HEAD_init_shared_between_horizons_and_matches_spec():
    m2, m3 = _mh(2, seed=1), _mh(3, seed=2)
    assert torch.equal(m2.joint["2"].weight, m3.joint["2"].weight)
    g = torch.Generator().manual_seed(AUX)
    w2 = 0.02 * torch.randn((25, TINY.d_model), generator=g)
    w3 = 0.02 * torch.randn((125, TINY.d_model), generator=g)
    assert torch.equal(m3.joint["2"].weight, w2) and torch.equal(m3.joint["3"].weight, w3)
    assert set(m2.joint.keys()) == {"2"} and set(m3.joint.keys()) == {"2", "3"}
    assert all(m3.joint[k].bias is None for k in ("2", "3"))
    assert m2.horizon == 2 and m3.horizon == 3
    assert not torch.equal(_mh(2, aux=AUX + 1).joint["2"].weight, w2)


@pytest.mark.parametrize("horizon", [2, 3])
def test_heads_read_ln_final_out_and_forward_returns_requested_hooks(horizon):
    m, x = _mh(horizon), _x()
    with torch.no_grad():
        plain = m(x)
        out = m(x, return_hooks=("ln_final_out",))
        one = m(x, return_hooks=("resid_post_0",))
    assert isinstance(plain, MultiHorizonOutput) and plain.hooks == {}
    assert set(out.hooks) == {"ln_final_out"} and set(one.hooks) == {"resid_post_0"}
    assert set(plain.joint_logits) == set(range(2, horizon + 1))
    z = out.hooks["ln_final_out"]
    for k in range(2, horizon + 1):
        assert plain.joint_logits[k].shape == (3, 33, 5**k)
        ref = torch.nn.functional.linear(z, m.joint[str(k)].weight)
        assert float((plain.joint_logits[k] - ref).abs().max()) <= 1e-6
    assert torch.equal(plain.logits, out.logits)
    with pytest.raises(StageFailure) as exc:
        m(x, return_hooks=("resid_post_7",))
    assert exc.value.code is ErrorCode.UNKNOWN_HOOK


@pytest.mark.parametrize("horizon", [0, 1, 4])
def test_horizon_outside_2_3_is_invalid_config(horizon):
    with pytest.raises(StageFailure) as exc:
        MultiHorizonLM(TINY, horizon, AUX)
    assert exc.value.code is ErrorCode.INVALID_CONFIG


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_CAUS_next_symbol_and_joint_logits(horizon):
    m, x = _mh(horizon), _x(4)
    for j in (1, 7, 16, 32):
        x2 = x.clone()
        x2[:, j] = (x2[:, j] + 1) % 6
        with torch.no_grad():
            a, b = m(x), m(x2)
        assert float((a.logits[:, :j] - b.logits[:, :j]).abs().max()) <= 1e-6
        for k in a.joint_logits:
            assert float((a.joint_logits[k][:, :j] - b.joint_logits[k][:, :j]).abs().max()) <= 1e-6
        assert float((a.logits[:, j:] - b.logits[:, j:]).abs().max()) > 0  # the probe bites


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_TARGET_tokens_after_p_change_nothing_at_p(horizon):
    m, x = _mh(horizon, cfg=DEEP), _x(4, seed=3)
    gen = torch.Generator().manual_seed(9)
    for p in (0, 16, 28, 31):
        x2 = x.clone()
        x2[:, p + 1:] = (x2[:, p + 1:] + torch.randint(1, 6, x2[:, p + 1:].shape,
                                                       generator=gen)) % 6
        with torch.no_grad():
            a = m(x, return_hooks=("resid_post_3",))
            b = m(x2, return_hooks=("resid_post_3",))
        h = (a.hooks["resid_post_3"][:, p] - b.hooks["resid_post_3"][:, p]).abs().max()
        assert float(h) <= 1e-6 and float((a.logits[:, p] - b.logits[:, p]).abs().max()) <= 1e-6
        for k in a.joint_logits:
            assert float((a.joint_logits[k][:, p] - b.joint_logits[k][:, p]).abs().max()) <= 1e-6


class _Leak(nn.Module):  # output at p copies a feature from position n_ctx - 1 - p
    def forward(self, z):
        return z.flip(1)[..., :1].expand(-1, -1, 25)


def _rng_untouched(fn):
    torch.manual_seed(123)
    expected = torch.rand(3)
    torch.manual_seed(123)
    result = fn()
    assert torch.equal(torch.rand(3), expected)
    return result


def test_check_causal_joint_passes_clean_model_and_catches_a_leak():
    m = _mh(2)
    _rng_untouched(lambda: check_causal_joint(m))  # local generator only
    m.joint["2"] = _Leak()
    with pytest.raises(StageFailure) as exc:
        check_causal_joint(m)
    assert exc.value.code is ErrorCode.CAUSAL_MASK_FAILED


def _y():
    rows = [[(3 * p + 1) % 5 for p in range(33)], [(p * p + 2) % 5 for p in range(33)]]
    rows[0][:4] = [1, 2, 3, 4]
    return torch.tensor(rows, dtype=torch.int64)


def _hand_ce(logits, targets):
    rows = logits.reshape(-1, logits.shape[-1]).tolist()
    tg = targets.reshape(-1).tolist()
    vals = [math.log(sum(math.exp(v) for v in r)) - r[t] for r, t in zip(rows, tg, strict=True)]
    return sum(vals) / len(vals)


def test_T_LOSS_joint_index_hand_values():
    y = _y()
    u2, u3 = joint_index(y, 2), joint_index(y, 3)
    assert u2.shape == (2, 32) and u3.shape == (2, 31) and u2.dtype == u3.dtype == torch.int64
    assert u2[0, :3].tolist() == [1 * 5 + 2, 2 * 5 + 3, 3 * 5 + 4]
    assert u3[0, 0].item() == 1 * 25 + 2 * 5 + 3 and u3[0, 1].item() == 2 * 25 + 3 * 5 + 4
    yl = y.tolist()
    for b in range(2):
        assert u2[b].tolist() == [yl[b][p] * 5 + yl[b][p + 1] for p in range(32)]
        assert u3[b].tolist() == [yl[b][p] * 25 + yl[b][p + 1] * 5 + yl[b][p + 2]
                                  for p in range(31)]
    small = torch.tensor([[2, 1, 0] * 11], dtype=torch.int64)
    assert joint_index(small, 2, V=3)[0, :3].tolist() == [7, 3, 2]


def _fake_out():
    g = torch.Generator().manual_seed(4)
    logits = torch.randn((2, 33, 5), generator=g, dtype=torch.float64)
    joint = {k: torch.randn((2, 33, 5**k), generator=g, dtype=torch.float64) for k in (2, 3)}
    return logits, joint


def test_T_LOSS_multi_horizon_loss_hand_values_and_exclusion():
    y, (logits, joint) = _y(), _fake_out()
    yl = y.tolist()
    u2 = torch.tensor([[r[p] * 5 + r[p + 1] for p in range(32)] for r in yl])
    u3 = torch.tensor([[r[p] * 25 + r[p + 1] * 5 + r[p + 2] for p in range(31)] for r in yl])
    ce1 = _hand_ce(logits, y)
    ce2 = _hand_ce(joint[2][:, :32], u2)  # positions p = 0..31 (p > 33 - 2 excluded)
    ce3 = _hand_ce(joint[3][:, :31], u3)  # positions p = 0..30
    out2 = MultiHorizonOutput(logits=logits, hooks={}, joint_logits={2: joint[2]})
    out3 = MultiHorizonOutput(logits=logits, hooks={}, joint_logits=dict(joint))
    l2 = float(multi_horizon_loss(out2, y, 2))
    l3 = float(multi_horizon_loss(out3, y, 3))
    assert abs(l2 - (ce1 + ce2 / 2) / 2) <= 1e-12
    assert abs(l3 - (ce1 + ce2 / 2 + ce3 / 3) / 3) <= 1e-12
    bumped = {k: v.clone() for k, v in joint.items()}
    bumped[2][:, 32] += 50.0 * torch.arange(25, dtype=torch.float64)
    bumped[3][:, 31:] -= 70.0 * torch.arange(125, dtype=torch.float64)
    out3b = MultiHorizonOutput(logits=logits, hooks={}, joint_logits=bumped)
    assert float(multi_horizon_loss(out3b, y, 3)) == l3  # excluded positions do not enter


def test_T_LOSS_horizon_one_is_lm_loss_exactly():
    y, (logits, joint) = _y(), _fake_out()
    expected = lm_loss(logits, y)
    assert torch.equal(multi_horizon_loss(ModelOutput(logits=logits, hooks={}), y, 1), expected)
    out = MultiHorizonOutput(logits=logits, hooks={}, joint_logits=dict(joint))
    assert torch.equal(multi_horizon_loss(out, y, 1), expected)
    assert abs(float(expected) - _hand_ce(logits, y)) <= 1e-12


def test_T_GRAD_ce2_alone_reaches_trunk_through_position_p():
    m, p = _mh(2).train(), 10
    x = _x(4, seed=6)
    y = torch.randint(0, 5, (4, 33), generator=torch.Generator().manual_seed(7))
    z = m(x).joint_logits[2][:, p]
    torch.nn.functional.cross_entropy(z, joint_index(y, 2)[:, p]).backward()  # CE2 at p alone
    for name in ("tok_emb.weight", "blocks.0.attn.qkv.weight", "blocks.0.fc_in.weight",
                 "ln_final.weight", "joint.2.weight"):
        assert float(dict(m.named_parameters())[name].grad.abs().max()) > 0, name
    pos = m.pos_emb.weight.grad
    assert float(pos[p].abs().max()) > 0 and float(pos[p + 1:].abs().max()) <= 1e-6
    unembed = m.unembed.weight.grad
    assert unembed is None or float(unembed.abs().max()) == 0.0


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_RNG_global_rng_untouched_by_fit_with_factory(horizon, data):
    cfg = TrainConfig(steps=2, warmup=1, batch_size=4, checkpoint_steps=(0, 2), device="cpu")
    _rng_untouched(lambda: _fit(horizon, data, cfg))


def _ckpt(model, cfg=TINY, state=None):
    blob = serialise_state(model, {}) if state is None else state
    return Checkpoint(run_id="d2a-test", step=0, observation_id="obs", state=blob,
                      model_config=dataclasses.asdict(cfg), train_config={})


def _blob(state_dict):
    buf = io.BytesIO()
    torch.save({"model": state_dict}, buf)
    return buf.getvalue()


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_LOAD_round_trip(horizon):
    src = _mh(horizon, aux=AUX + 7, seed=99)
    ck = _ckpt(src)
    loaded = _rng_untouched(lambda: load_multi_horizon(ck, horizon))
    assert isinstance(loaded, MultiHorizonLM) and not loaded.training
    assert all(p.device.type == "cpu" for p in loaded.parameters())
    x = _x(seed=8)
    with torch.no_grad():
        a, b = src(x), loaded(x)
    assert float((a.logits - b.logits).abs().max()) <= 1e-6
    assert set(b.joint_logits) == set(range(2, horizon + 1))
    for k in a.joint_logits:
        assert float((a.joint_logits[k] - b.joint_logits[k]).abs().max()) <= 1e-6


def _bad_checkpoints():
    m2, m3 = _mh(2), _mh(3)
    sd2 = {k: v.clone() for k, v in m2.state_dict().items()}
    missing = {k: v for k, v in sd2.items() if k != "joint.2.weight"}
    extra = dict(sd2, **{"joint.4.weight": torch.zeros(625, TINY.d_model)})
    shape = dict(sd2, **{"joint.2.weight": torch.zeros(24, TINY.d_model)})
    no_model = io.BytesIO()
    torch.save({"weights": sd2}, no_model)
    wide = dataclasses.replace(TINY, d_model=32)
    return {
        "h2_as_h3": (_ckpt(m2), 3), "h3_as_h2": (_ckpt(m3), 2),
        "missing_head": (_ckpt(m2, state=_blob(missing)), 2),
        "unexpected_head": (_ckpt(m2, state=_blob(extra)), 2),
        "bad_shape": (_ckpt(m2, state=_blob(shape)), 2),
        "config_shape": (_ckpt(m2, cfg=wide), 2),
        "garbage_state": (_ckpt(m2, state=b"not a torch archive"), 2),
        "no_model_key": (_ckpt(m2, state=no_model.getvalue()), 2),
        "horizon_1": (_ckpt(m2), 1), "horizon_4": (_ckpt(m3), 4),
        "h1_checkpoint": (_ckpt(TransformerLM(TINY)), 2),  # no joint head in an H1 checkpoint
    }


def test_T_LOAD_rejections_are_invalid_config():
    for name, (ck, horizon) in _bad_checkpoints().items():
        with pytest.raises(StageFailure) as exc:
            load_multi_horizon(ck, horizon)
        assert exc.value.code is ErrorCode.INVALID_CONFIG, name


def test_T_LOAD_horizon1_checkpoint_uses_load_model():
    torch.manual_seed(3)
    ref = TransformerLM(TINY).eval()
    model = load_model(_ckpt(ref))
    assert type(model) is TransformerLM and not model.training
    with torch.no_grad():
        assert float((model(_x(seed=10)).logits - ref(_x(seed=10)).logits).abs().max()) <= 1e-6


@pytest.mark.parametrize("horizon", [2, 3])
def test_T_DECAY_groups_equal_transformer_plus_joint_matrices(horizon):
    trainer = Trainer(TINY, STEP0, SeedTree(1), ("r",))

    def groups(model):
        names = {id(p): n for n, p in model.named_parameters()}
        opt = trainer._optimizer(model)
        return [({names[id(p)] for p in g["params"]}, g["weight_decay"]) for g in opt.param_groups]

    torch.manual_seed(0)
    ref = groups(TransformerLM(TINY))
    torch.manual_seed(0)
    got = groups(MultiHorizonLM(TINY, horizon, AUX))
    assert len(got) == len(ref) == 2
    assert got[0][0] == ref[0][0] | set(JOINT[horizon]) and got[0][1] == ref[0][1] == 0.1
    assert got[1] == ref[1] and ref[1][1] == 0.0
