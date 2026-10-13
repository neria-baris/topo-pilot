"""L04, L05, L07, L08, L10: training loop contracts."""

from dataclasses import replace

import pytest
import torch

from topo_pilot.contracts import ErrorCode, SeedTree, SequenceLayout, StageFailure
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import TrainConfig, Trainer

pytestmark = pytest.mark.learner


def _fit(model_cfg, train_cfg, ds, seed=1729, key=("r", 0)):
    seen = []

    def cb(step, model, info):
        seen.append((step, {k: v.clone() for k, v in model.state_dict().items()}, info))

    trainer = Trainer(model_cfg, train_cfg, SeedTree(seed), key)
    return trainer, trainer.fit(ds, ds, cb), seen


def test_L04_overfit_eight_sequences(model_cfg, tiny_obs):
    # Distinct sequences cannot be memorised below ln(R_distinct)/33 nats: at the first token
    # where two of them differ the prefix is identical but the targets differ. Eight random
    # sequences give a floor of ln(8)/33 = 0.063 > 0.05, so use 8 fixed sequences made of 2
    # distinct ones (floor ln(2)/33 = 0.021).
    tokens = tiny_obs.tokens[[0, 1] * 4].copy()
    tiny_ds = PublicTokenDataset(replace(tiny_obs, tokens=tokens), SequenceLayout())
    cfg = TrainConfig(steps=300, batch_size=32, lr=1e-2, warmup=20, checkpoint_steps=(0, 300),
                      weight_decay=0.0, device="cpu")
    _, summary, _ = _fit(model_cfg, cfg, tiny_ds)
    assert summary.dev_ce_by_step[300] < 0.05
    assert summary.dev_ce_by_step[0] > 0.9


def test_L05_step0_is_initial_weights_and_runs_repeat(model_cfg, train_cfg, tiny_ds):
    from topo_pilot.learner import TransformerLM
    t1, s1, seen1 = _fit(model_cfg, train_cfg, tiny_ds)
    _, s2, seen2 = _fit(model_cfg, train_cfg, tiny_ds)
    _, s3, seen3 = _fit(model_cfg, train_cfg, tiny_ds, seed=2718)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(1729).seed("init", "r", 0))
        fresh = TransformerLM(model_cfg).state_dict()
    step0 = seen1[0][1]
    assert seen1[0][0] == 0
    assert all(torch.equal(step0[k], fresh[k]) for k in fresh)
    assert s1.dev_ce_by_step == s2.dev_ce_by_step
    assert s1.final_train_loss == s2.final_train_loss
    for (_, a, _), (_, b, _) in zip(seen1, seen2, strict=True):
        assert all(torch.equal(a[k], b[k]) for k in a)
    assert s3.dev_ce_by_step != s1.dev_ce_by_step
    assert s1.tokens_per_second > 0 and s1.steps_done == 12 and s1.device == "cpu"
    assert s1.torch_version == torch.__version__ and t1.model is not None


def test_L05b_global_rng_untouched(model_cfg, train_cfg, tiny_ds):
    torch.manual_seed(123)
    expected = torch.rand(3)
    torch.manual_seed(123)
    _fit(model_cfg, train_cfg, tiny_ds)
    assert torch.equal(torch.rand(3), expected)


def test_L07_non_public_dataset_is_leakage(model_cfg, train_cfg, tiny_ds, tiny_obs):
    trainer = Trainer(model_cfg, train_cfg, SeedTree(1), ("r",))
    for bad in (tiny_obs, [(1, 2)], None):
        with pytest.raises(StageFailure) as exc:
            trainer.fit(bad, tiny_ds, lambda *a: None)
        assert exc.value.code is ErrorCode.LEAKAGE
    with pytest.raises(StageFailure) as exc:
        trainer.fit(tiny_ds, tiny_obs, lambda *a: None)
    assert exc.value.code is ErrorCode.LEAKAGE


def test_L08_nan_loss_raises(monkeypatch, model_cfg, train_cfg, tiny_ds):
    calls = {"n": 0}
    real = torch.nn.functional.cross_entropy

    def bad(*args, **kwargs):
        calls["n"] += 1
        out = real(*args, **kwargs)
        return out * float("nan") if calls["n"] > 1 else out  # call 1 = step-0 dev eval

    monkeypatch.setattr(torch.nn.functional, "cross_entropy", bad)
    with pytest.raises(StageFailure) as exc:
        _fit(model_cfg, train_cfg, tiny_ds)
    assert exc.value.code is ErrorCode.NONFINITE_LOSS
    assert exc.value.recoverable is False


def test_L10_schedule_and_optimizer_only_at_final(model_cfg, tiny_ds):
    cfg = TrainConfig(steps=9, batch_size=4, warmup=2, checkpoint_steps=(0, 1, 4, 9), device="cpu")
    _, summary, seen = _fit(model_cfg, cfg, tiny_ds)
    assert [s for s, _, _ in seen] == [0, 1, 4, 9]
    assert sorted(summary.dev_ce_by_step) == [0, 1, 4, 9]
    for step, _, info in seen:
        assert ("optimizer_state" in info) == (step == 9)
        assert ("scheduler_state" in info) == (step == 9)
        assert info["dev_ce"] == summary.dev_ce_by_step[step]
    assert seen[0][2]["train_loss"] is None


def test_L10b_invalid_schedules_rejected(model_cfg, tiny_ds):
    for cfg in (TrainConfig(steps=5, checkpoint_steps=(0, 6), device="cpu"),
                TrainConfig(steps=0, checkpoint_steps=(0,), device="cpu")):
        with pytest.raises(StageFailure) as exc:
            _fit(model_cfg, cfg, tiny_ds)
        assert exc.value.code is ErrorCode.INVALID_CONFIG


def test_lr_schedule_known_values():
    from topo_pilot.learner.trainer import WarmupCosine
    f = WarmupCosine(warmup=4, steps=14)
    assert f(0) == 0.25 and f(3) == 1.0
    assert f(4) == pytest.approx(1.0) and f(9) == pytest.approx(0.5)
    assert f(14) == pytest.approx(0.0, abs=1e-12)


def test_weight_decay_groups(model_cfg, train_cfg):
    from topo_pilot.learner import TransformerLM
    t = Trainer(model_cfg, train_cfg, SeedTree(1), ("r",))
    m = TransformerLM(model_cfg)
    opt = t._optimizer(m)
    decayed = {id(p) for p in opt.param_groups[0]["params"]}
    for name, p in m.named_parameters():
        expect = p.ndim == 2 and not name.startswith(("tok_emb", "pos_emb"))
        assert (id(p) in decayed) == expect, name

