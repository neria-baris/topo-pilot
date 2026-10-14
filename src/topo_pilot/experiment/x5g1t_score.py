"""X5 G1 training-study scoring at p32 (x5g1-train contract §4): batched, float64, stable.

The model sees ``[BOS, w1..w32]``; position 32 predicts ``w33``. Oracle rows must come from the
public history ``w1..w32`` only (see ``x5g1t_oracle``); the target ``w33`` is never read here.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import torch
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

SCORE_BATCH = 512
POSITION = 32


@torch.no_grad()
def p32_log_probs(model: torch.nn.Module, inputs: torch.Tensor, batch: int = SCORE_BATCH,
                  guard: Callable[[str], None] | None = None) -> NDArray[np.float64]:
    """``log softmax(logits[:, 32, :])`` in float64, ``[R, V]``, computed ``batch`` rows at a time.

    ``guard(f"score batch {k}")`` and ``guard(f"score batch {k} done")`` bracket batch ``k`` (the
    study controls: STOP, holds, budget, resources). The model's training flag is restored.
    """
    if inputs.ndim != 2 or inputs.shape[1] != POSITION + 1:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "experiment.X5G1T", "inputs",
                           f"expected [R, 33] inputs, got {tuple(inputs.shape)}")
    was_training = model.training
    model.eval()
    try:
        out = []
        for k, i in enumerate(range(0, inputs.shape[0], batch)):
            if guard:
                guard(f"score batch {k}")
            out.append(torch.log_softmax(model(inputs[i:i + batch]).logits[:, POSITION, :]
                                         .to(torch.float64), dim=-1).numpy())
            if guard:
                guard(f"score batch {k} done")
    finally:
        model.train(was_training)
    return np.concatenate(out, axis=0)


def kl_from_log_probs(q: NDArray, logp: NDArray) -> NDArray[np.float64]:
    """Per-row ``KL(q || p) = sum_v q_v (log q_v - log p_v)`` with ``0 log 0 = 0`` (nats).

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on shape mismatch; ``NUMERICAL_FAILURE`` if q has negative entries
        or rows not summing to 1 within 1e-9, or the result is non-finite.
    """
    q = np.asarray(q, dtype=np.float64)
    logp = np.asarray(logp, dtype=np.float64)
    if q.shape != logp.shape or q.ndim != 2:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "experiment.X5G1T", "kl_shapes",
                           f"q {q.shape} vs logp {logp.shape}")
    if q.min() < 0 or np.max(np.abs(q.sum(axis=1) - 1.0)) > 1e-9:
        raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "experiment.X5G1T", "q_rows",
                           "q must be non-negative rows summing to 1")
    pos = q > 0
    terms = np.where(pos, q * (np.log(np.where(pos, q, 1.0)) - logp), 0.0)
    kl = terms.sum(axis=1)
    if not np.all(np.isfinite(kl)):
        raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "experiment.X5G1T", "kl_finite",
                           "non-finite KL (model assigns zero probability to a q-support symbol)")
    return kl


def regret_rows(model: torch.nn.Module, inputs: torch.Tensor, q: NDArray,
                batch: int = SCORE_BATCH,
                guard: Callable[[str], None] | None = None) -> NDArray[np.float64]:
    """Per-history regret ``KL(q_C(h) || p_model(h))`` at p32, nats, ``[R]`` (guarded batches)."""
    return kl_from_log_probs(q, p32_log_probs(model, inputs, batch, guard))
