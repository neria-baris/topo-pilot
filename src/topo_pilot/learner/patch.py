"""Frozen forward pass with one replaced vector (X4-F, x4f-exec-v2 §7; no science imports).

The learner receives public token tensors and a precomputed numeric replacement only; it never
sees targets, beliefs, oracle outputs or sidecars.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

import torch

from topo_pilot.contracts import ErrorCode, StageFailure

from .model import TransformerLM

_COMPONENT = "learner.forward_with_patch"


@dataclass(frozen=True)
class PatchedOutput:
    """``logits [R, L, vocab_out]`` at every position and the requested ``hooks`` (each
    ``[R, L, d_model]``), all computed after the patch."""

    logits: torch.Tensor
    hooks: dict[str, torch.Tensor] = field(default_factory=dict)


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def _check(model: TransformerLM, inputs: torch.Tensor, site: str, index: int,
           replacement: torch.Tensor, return_hooks: Sequence[str]) -> int | None:
    """Validate arguments; return the block index k for ``resid_post_k`` (None for final LN)."""
    if model.training:
        raise _fail(ErrorCode.INVALID_CONFIG, "eval_mode", "model must be in eval mode")
    if inputs.ndim != 2 or inputs.dtype not in (torch.int64, torch.int32, torch.int16,
                                                torch.uint8):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "inputs", "inputs must be a 2-D integer tensor")
    R, L = inputs.shape
    if L > model.cfg.n_ctx or (inputs.numel() and (int(inputs.min()) < 0
                                                    or int(inputs.max()) >= model.cfg.vocab_in)):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "inputs", "length or token outside vocabulary")
    unknown = [h for h in return_hooks if h not in model.hook_names]
    if unknown:
        raise _fail(ErrorCode.UNKNOWN_HOOK, "return_hooks", f"unknown hooks {unknown}")
    k = None
    if site != "ln_final_out":
        prefix = "resid_post_"
        tail = site[len(prefix):] if site.startswith(prefix) else ""
        if not tail.isdigit() or not 0 <= int(tail) < model.cfg.n_layers:
            raise _fail(ErrorCode.UNKNOWN_HOOK, "site", f"site {site!r} not patchable")
        k = int(tail)
    if not 0 <= index < L:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "index", f"index {index} outside 0..{L - 1}")
    if tuple(replacement.shape) != (R, model.cfg.d_model):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "replacement",
                    f"replacement {tuple(replacement.shape)} != {(R, model.cfg.d_model)}")
    if not bool(torch.isfinite(replacement).all()):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "replacement", "non-finite replacement")
    return k


def forward_with_patch(model: TransformerLM, inputs: torch.Tensor, site: str, index: int,
                       replacement: torch.Tensor, *,
                       return_hooks: Sequence[str] = ()) -> PatchedOutput:
    """Run the frozen model with the vector at ``(site, index)`` replaced.

    Math
    ----
    ``resid_post_k``: embed -> blocks[0..k] -> ``x[:, index] = replacement`` -> blocks[k+1..]
    -> ln_final -> unembed. ``ln_final_out``: full forward to ``ln_final``; then
    ``normed[:, index] = replacement`` -> unembed (no second LayerNorm).

    Shapes
    ------
    ``inputs: [R, L]`` integer (``L <= n_ctx``); ``replacement: [R, d_model]``;
    output ``logits: [R, L, vocab_out]``.

    Invariants
    ----------
    No gradient, no parameter or buffer write, no mode change. With the unpatched value as the
    replacement the logits equal ``model(inputs).logits``; positions ``< index`` never change.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (model in training mode), ``ALIGNMENT_ERROR`` (inputs, index or
        replacement shape), ``UNKNOWN_HOOK`` (site or hook name), ``NUMERICAL_FAILURE``
        (non-finite replacement).
    """
    k = _check(model, inputs, site, index, replacement, return_hooks)
    wanted = set(return_hooks)
    hooks: dict[str, torch.Tensor] = {}
    with torch.no_grad():
        tokens = inputs.to(torch.int64)
        pos = torch.arange(tokens.shape[1], device=tokens.device)
        x = model.tok_emb(tokens) + model.pos_emb(pos)
        if "embed" in wanted:
            hooks["embed"] = x
        repl = replacement.to(dtype=x.dtype, device=x.device)
        for j, block in enumerate(model.blocks):
            x = block(x)
            if j == k:
                x = x.clone()
                x[:, index, :] = repl
            if f"resid_post_{j}" in wanted:
                hooks[f"resid_post_{j}"] = x
        normed = model.ln_final(x)
        if k is None:
            normed = normed.clone()
            normed[:, index, :] = repl
        if "ln_final_out" in wanted:
            hooks["ln_final_out"] = normed
        logits = model.unembed(normed)
    return PatchedOutput(logits=logits, hooks=hooks)
