"""Direct joint heads for the next k symbols and the multi-horizon loss (D2A-FROZEN-v1 §4.3-4.5).

``MultiHorizonLM`` is the unchanged ``TransformerLM`` trunk plus heads ``joint.k`` (k = 2..H),
``Linear(d_model, V**k, bias=False)`` reading ``ln_final_out`` at the same position; head k
predicts the joint ``(w_{p+1}, ..., w_{p+k})`` (earliest symbol outer) and never sees
``w_{p+1}``. The loss is ``(1/H) sum_k (1/k) CE_k`` with ``CE_1 = lm_loss``.
"""

from __future__ import annotations

import io
import pickle
from dataclasses import dataclass, field

import torch
from torch import nn

from topo_pilot.contracts import ErrorCode, StageFailure

from .config import ModelConfig
from .model import ModelOutput, TransformerLM
from .trainer import lm_loss

_HORIZONS = (2, 3)


@dataclass(frozen=True)
class MultiHorizonOutput(ModelOutput):
    """``ModelOutput`` plus ``joint_logits``: k -> ``[B, n_ctx, vocab_out**k]``."""

    joint_logits: dict[int, torch.Tensor] = field(default_factory=dict)


class MultiHorizonLM(TransformerLM):
    """``TransformerLM`` trunk (same parameter creation, init and causality check) + joint heads.

    Head weights are ``0.02 * N(0, 1)`` from a local generator seeded with ``aux_seed`` (k = 2
    drawn before k = 3), so the global RNG and the trunk are unaffected by the head draw.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for a horizon outside {2, 3}; ``CAUSAL_MASK_FAILED`` if a joint logit
        at a position before a perturbed input moves.
    """

    def __init__(self, cfg: ModelConfig, horizon: int, aux_seed: int):
        super().__init__(cfg)
        if horizon not in _HORIZONS:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.MultiHorizonLM", "horizon",
                               f"horizon must be 2 or 3, got {horizon!r}")
        self.horizon = horizon
        self.joint = nn.ModuleDict({str(k): nn.Linear(cfg.d_model, cfg.vocab_out ** k,
                                                      bias=False)
                                    for k in range(2, horizon + 1)})
        gen = torch.Generator().manual_seed(int(aux_seed))
        with torch.no_grad():
            for k in range(2, horizon + 1):
                weight = self.joint[str(k)].weight
                weight.copy_(0.02 * torch.randn(weight.shape, generator=gen))
        check_causal_joint(self)

    def forward(self, inputs: torch.Tensor, *, return_hooks=()) -> ModelOutput:
        joint = getattr(self, "joint", None)  # None while the parent's check_causal runs
        hooks = tuple(return_hooks)
        need = hooks if joint is None or "ln_final_out" in hooks else hooks + ("ln_final_out",)
        out = super().forward(inputs, return_hooks=need)
        if joint is None:
            return out
        z = out.hooks["ln_final_out"]
        return MultiHorizonOutput(logits=out.logits, hooks={h: out.hooks[h] for h in hooks},
                                  joint_logits={int(k): head(z) for k, head in joint.items()})


@torch.no_grad()
def check_causal_joint(model: MultiHorizonLM, tol: float = 1e-6) -> None:
    """Perturb one input position j (local generator, seed 0); joint logits at positions < j
    must not move by more than ``tol``."""
    cfg = model.cfg
    if cfg.n_ctx < 2:
        return
    gen = torch.Generator().manual_seed(0)
    was_training = model.training
    model.eval()
    x = torch.randint(0, cfg.vocab_in, (4, cfg.n_ctx), generator=gen)
    j = int(torch.randint(1, cfg.n_ctx, (1,), generator=gen))
    x2 = x.clone()
    x2[:, j] = (x2[:, j] + 1) % cfg.vocab_in
    a, b = model(x).joint_logits, model(x2).joint_logits
    diff = max(float((a[k][:, :j] - b[k][:, :j]).abs().max()) for k in a)
    model.train(was_training)
    if diff > tol:
        raise StageFailure(ErrorCode.CAUSAL_MASK_FAILED, "learner.MultiHorizonLM", "causality",
                           f"perturbing position {j} changed earlier joint logits by {diff:.3e}")


def joint_index(y: torch.Tensor, k: int, V: int = 5) -> torch.Tensor:
    """``u_k[:, p] = sum_{j<k} y[:, p+j] V^(k-1-j)`` for ``p = 0..n-k`` -> ``[B, n+1-k]``."""
    n = y.shape[1]
    out = torch.zeros((y.shape[0], n + 1 - k), dtype=torch.int64, device=y.device)
    for j in range(k):
        out = out * V + y[:, j:n + 1 - k + j].to(torch.int64)
    return out


def multi_horizon_loss(out: ModelOutput, y: torch.Tensor, horizon: int) -> torch.Tensor:
    """``(1/H) sum_{k=1..H} (1/k) CE_k`` (§4.4); ``H = 1`` is exactly ``lm_loss``."""
    ce1 = lm_loss(out.logits, y)
    if horizon == 1:
        return ce1
    total = ce1
    V, n = out.logits.shape[-1], y.shape[1]
    for k in range(2, horizon + 1):
        total = total + lm_loss(out.joint_logits[k][:, :n + 1 - k], joint_index(y, k, V)) / k
    return total / horizon


def load_multi_horizon(checkpoint, horizon: int) -> MultiHorizonLM:
    """Rebuild ``MultiHorizonLM`` (CPU, eval) from ``checkpoint.model_config`` and its weights,
    strictly, inside a forked RNG with a fixed disposable auxiliary seed."""
    try:
        with torch.random.fork_rng(devices=[]):
            model = MultiHorizonLM(ModelConfig(**dict(checkpoint.model_config)), horizon, 0)
        state = torch.load(io.BytesIO(checkpoint.state), map_location="cpu", weights_only=True)
        model.load_state_dict(state["model"])
    except StageFailure as exc:
        if exc.code == ErrorCode.INVALID_CONFIG:
            raise
        raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.load_multi_horizon",
                           "checkpoint", str(exc)) from exc
    except (TypeError, KeyError, RuntimeError, ValueError, AttributeError, EOFError,
            pickle.UnpicklingError) as exc:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.load_multi_horizon", "checkpoint",
                           f"{type(exc).__name__}: {exc}") from exc
    return model.eval()


__all__ = ["MultiHorizonLM", "MultiHorizonOutput", "check_causal_joint", "joint_index",
           "load_multi_horizon", "multi_horizon_loss"]
