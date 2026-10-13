"""Decoder-only pre-LN transformer with named residual-stream hooks."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

import torch
import torch.nn.functional as F
from torch import nn

from topo_pilot.contracts import ErrorCode, StageFailure

from .config import ModelConfig

HOOK_NAMES: tuple[str, ...] = ("embed", "resid_post_0", "resid_post_1", "resid_post_2",
                               "resid_post_3", "ln_final_out")


def hook_names(n_layers: int) -> tuple[str, ...]:
    """Hook names for a model with ``n_layers`` blocks (equals ``HOOK_NAMES`` for 4)."""
    return ("embed", *(f"resid_post_{k}" for k in range(n_layers)), "ln_final_out")


@dataclass(frozen=True)
class ModelOutput:
    """Forward result: ``logits [B, n_ctx, vocab_out]`` and requested ``hooks`` (each
    ``[B, n_ctx, d_model]``)."""

    logits: torch.Tensor
    hooks: dict[str, torch.Tensor] = field(default_factory=dict)


class CausalSelfAttention(nn.Module):
    """Multi-head causal self-attention: softmax(Q K^T / sqrt(d_head) + causal mask) V."""

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.n_heads = cfg.n_heads
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model)
        self.proj = nn.Linear(cfg.d_model, cfg.d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, width = x.shape
        q, k, v = self.qkv(x).split(width, dim=2)
        q, k, v = (t.view(batch, length, self.n_heads, -1).transpose(1, 2) for t in (q, k, v))
        out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.proj(out.transpose(1, 2).reshape(batch, length, width))


class Block(nn.Module):
    """Pre-LN block: ``x = x + Attn(LN(x)); x = x + MLP(LN(x))``."""

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.d_model)
        self.attn = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.fc_in = nn.Linear(cfg.d_model, cfg.d_mlp)
        self.fc_out = nn.Linear(cfg.d_mlp, cfg.d_model)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.drop(self.attn(self.ln1(x)))
        return x + self.drop(self.fc_out(F.gelu(self.fc_in(self.ln2(x)))))


class TransformerLM(nn.Module):
    """Decoder-only, pre-LN, learned positional embeddings, final LN, untied unembedding.

    Math: ``h0 = E[x] + P``; ``h_{k+1} = Block_k(h_k)``; ``logits = LN_f(h_L) W_U`` (no bias).

    Shapes: ``inputs [B, n_ctx]`` int64 in ``[0, vocab_in)``; logits ``[B, n_ctx, vocab_out]``.
    Weight decay convention (see Trainer): matrices decay, biases / LayerNorm / embeddings do not.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (bad dims, tied embeddings, non-gelu), ``UNKNOWN_HOOK`` in ``forward``,
        ``CAUSAL_MASK_FAILED`` at construction if a position leaks into earlier logits.
    """

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        _validate(cfg)
        self.cfg = cfg
        self.hook_names = hook_names(cfg.n_layers)
        self.tok_emb = nn.Embedding(cfg.vocab_in, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.n_ctx, cfg.d_model)
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.n_layers))
        self.ln_final = nn.LayerNorm(cfg.d_model)
        self.unembed = nn.Linear(cfg.d_model, cfg.vocab_out, bias=False)
        self._init_weights()
        check_causal(self)

    def _init_weights(self) -> None:
        """N(0, 0.02) for embeddings and matrices; residual output projections scaled by
        1/sqrt(2 L); biases zero (LayerNorm keeps its 1/0 default)."""
        small = 0.02 / math.sqrt(2 * self.cfg.n_layers)
        for name, p in self.named_parameters():
            if p.ndim == 2:
                std = small if name.endswith(("proj.weight", "fc_out.weight")) else 0.02
                nn.init.normal_(p, 0.0, std)
            elif name.endswith(".bias") and "ln" not in name:
                nn.init.zeros_(p)

    def forward(self, inputs: torch.Tensor, *, return_hooks: Sequence[str] = ()) -> ModelOutput:
        unknown = [h for h in return_hooks if h not in self.hook_names]
        if unknown:
            raise StageFailure(ErrorCode.UNKNOWN_HOOK, "learner.TransformerLM", "return_hooks",
                               f"unknown hooks {unknown}; valid: {self.hook_names}")
        wanted = set(return_hooks)
        hooks: dict[str, torch.Tensor] = {}
        pos = torch.arange(inputs.shape[1], device=inputs.device)
        x = self.tok_emb(inputs) + self.pos_emb(pos)
        if "embed" in wanted:
            hooks["embed"] = x
        for k, block in enumerate(self.blocks):
            x = block(x)
            if f"resid_post_{k}" in wanted:
                hooks[f"resid_post_{k}"] = x
        normed = self.ln_final(x)
        if "ln_final_out" in wanted:
            hooks["ln_final_out"] = normed
        return ModelOutput(logits=self.unembed(normed), hooks=hooks)


def _validate(cfg: ModelConfig) -> None:
    problems = []
    if cfg.activation != "gelu":
        problems.append(f"activation={cfg.activation!r}")
    if cfg.tie_embeddings:
        problems.append("tie_embeddings=True unsupported (vocab_in != vocab_out)")
    if cfg.d_model % cfg.n_heads:
        problems.append("d_model not divisible by n_heads")
    if min(cfg.vocab_in, cfg.vocab_out, cfg.n_ctx, cfg.n_layers, cfg.d_model, cfg.d_mlp) < 1:
        problems.append("non-positive dimension")
    if problems:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "learner.TransformerLM", "model_config",
                           "; ".join(problems))


@torch.no_grad()
def check_causal(model: TransformerLM, tol: float = 1e-6) -> None:
    """Perturb one input position j of a random batch; logits at positions < j must not move.

    Uses a local ``torch.Generator`` (fixed seed), never the global RNG.

    Raises
    ------
    StageFailure
        ``CAUSAL_MASK_FAILED`` when the maximal change at positions < j exceeds ``tol``.
    """
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
    diff = float((model(x).logits[:, :j] - model(x2).logits[:, :j]).abs().max())
    model.train(was_training)
    if diff > tol:
        raise StageFailure(ErrorCode.CAUSAL_MASK_FAILED, "learner.TransformerLM", "causality",
                           f"perturbing position {j} changed earlier logits by {diff:.3e}")
