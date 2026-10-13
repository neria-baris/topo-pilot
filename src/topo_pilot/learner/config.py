"""Frozen configuration dataclasses of the learner (SPEC public API)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ModelConfig:
    """Decoder-only transformer hyper-parameters.

    Shapes: input vocabulary ``vocab_in = V + 1`` (BOS = V), output vocabulary ``vocab_out = V``,
    ``n_ctx = 33`` positions, ``d_model`` divisible by ``n_heads``.

    Invariants: ``dropout`` is 0 in all experiments; ``tie_embeddings`` must be False (the input
    and output vocabularies differ, so the unembedding is always separate).
    """

    vocab_in: int
    vocab_out: int
    n_ctx: int = 33
    n_layers: int = 4
    d_model: int = 128
    n_heads: int = 4
    d_mlp: int = 512
    activation: Literal["gelu"] = "gelu"
    dropout: float = 0.0
    tie_embeddings: bool = False


@dataclass(frozen=True)
class TrainConfig:
    """Optimisation hyper-parameters (RESEARCH_SUMMARY section 6).

    Math: lr(s) = lr * (s + 1) / warmup for s < warmup, then
    lr * 0.5 * (1 + cos(pi * (s - warmup) / (steps - warmup))), where s counts finished updates;
    the multiplier reaches 0 at ``s = steps``.
    """

    steps: int = 5000
    batch_size: int = 128
    lr: float = 1e-3
    warmup: int = 200
    schedule: Literal["cosine"] = "cosine"
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    checkpoint_steps: tuple[int, ...] = (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000,
                                         4000, 5000)
    device: str = "auto"
