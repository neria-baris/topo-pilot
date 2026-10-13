"""Gradient-free extraction of hook activations and logits at the analysis position."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import numpy as np
import torch

from topo_pilot.contracts import (
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    SequenceLayout,
    StageFailure,
    tokens_hash,
)

if TYPE_CHECKING:
    from topo_pilot.learner import TransformerLM

_COMPONENT = "activations.ActivationExtractor"
_TOL = 1e-5


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def valid_hook_names(n_layers: int) -> tuple[str, ...]:
    """Hook names of a model with ``n_layers`` blocks (learner SPEC)."""
    return ("embed", *(f"resid_post_{k}" for k in range(n_layers)), "ln_final_out")


def resolve_device(device: str) -> torch.device:
    """``"auto"`` is CUDA if available, else CPU; anything else is passed to torch."""
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)


class ActivationExtractor:
    """Extract ``A [M, K, d]`` and ``logits [M, V]`` at position ``end`` (= 32) of each history.

    Position convention: the model input row is ``[BOS, w_1..w_32]`` (33 positions, 0..32).
    Position 32 holds token ``w_32``, sees ``w_1..w_32`` and its logits predict ``w_33``.

    Parameters
    ----------
    hooks : sequence of str
        Hook names, in the order they appear along axis 1 of ``A``.
    batch_size : int
        Rows per forward pass (does not change results beyond float noise).
    device : str
        ``"auto"`` (CUDA if available, else CPU) or a torch device string.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` for a non-positive batch size or an empty hook list.
    """

    def __init__(self, hooks: Sequence[str], batch_size: int = 256, device: str = "auto"):
        if batch_size < 1 or len(hooks) == 0:
            raise _fail(ErrorCode.INVALID_CONFIG, "init", f"batch_size={batch_size}, hooks empty?")
        self.hooks = tuple(hooks)
        self.batch_size = int(batch_size)
        self.device = device

    @staticmethod
    def _select_rows(index: HistoryIndex, panels: Sequence[int] | None) -> np.ndarray:
        if panels is None:
            return np.arange(len(index.history_id))
        return np.flatnonzero(np.isin(index.panel, np.asarray(list(panels))))

    @staticmethod
    def _align(obs: ObservationSet, index: HistoryIndex, rows: np.ndarray) -> np.ndarray:
        """Obs row numbers for the selected index rows, verifying end and token digest."""
        pos_of = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
        analysis = SequenceLayout().analysis_position
        obs_rows = np.empty(len(rows), dtype=np.int64)
        for j, i in enumerate(rows.tolist()):
            sid = int(index.sequence_id[i])
            if int(index.end[i]) != analysis or sid not in pos_of:
                raise _fail(ErrorCode.ALIGNMENT_ERROR, "end_or_sequence_id",
                            f"row {i}: end={int(index.end[i])}, sequence_id {sid} "
                            f"{'found' if sid in pos_of else 'missing'}")
            obs_rows[j] = pos_of[sid]
            digest = tokens_hash(np.asarray(obs.tokens[pos_of[sid], :analysis]))
            if digest != str(index.tokens_hash[i]):
                raise _fail(ErrorCode.ALIGNMENT_ERROR, "tokens_hash",
                            f"row {i}: input digest disagrees with HistoryIndex.tokens_hash")
        return obs_rows

    def extract(self, model: TransformerLM, obs_test: ObservationSet, index: HistoryIndex,
                panels: Sequence[int] | None = None) -> tuple[np.ndarray, np.ndarray, list[str]]:
        """Extract activations and logits for the (filtered) histories, in index order.

        Shapes: returns ``A [M, K, d] float32``, ``logits [M, V] float32``, ``ids`` of length M.

        Raises
        ------
        StageFailure
            ``UNKNOWN_HOOK``; ``ALIGNMENT_ERROR`` (end != 32, unknown sequence id, or a token
            digest differing from ``index.tokens_hash``); ``NUMERICAL_FAILURE`` (hooked logits
            differ from a plain forward pass by more than 1e-5 on the first batch).
        """
        valid = valid_hook_names(int(model.cfg.n_layers))
        bad = [h for h in self.hooks if h not in valid]
        if bad:
            raise _fail(ErrorCode.UNKNOWN_HOOK, "hooks", f"unknown {bad}; valid {list(valid)}")
        rows = self._select_rows(index, panels)
        obs_rows = self._align(obs_test, index, rows)
        inputs = SequenceLayout().model_inputs(obs_test.tokens[obs_rows], obs_test.V)
        dev = resolve_device(self.device)
        model.to(dev).eval()
        pos = SequenceLayout().analysis_position
        a_parts: list[np.ndarray] = []
        l_parts: list[np.ndarray] = []
        with torch.no_grad():
            for start in range(0, len(rows), self.batch_size):
                x = torch.from_numpy(inputs[start : start + self.batch_size]).to(dev)
                out = model(x, return_hooks=self.hooks)
                logits = out.logits[:, pos].float()
                if start == 0:
                    self._verify_plain(model, x, logits)
                a_parts.append(torch.stack([out.hooks[h][:, pos] for h in self.hooks], 1)
                               .float().cpu().numpy())
                l_parts.append(logits.cpu().numpy())
        ids = [str(h) for h in index.history_id[rows].tolist()]
        if not rows.size:
            return (np.zeros((0, len(self.hooks), int(model.cfg.d_model)), np.float32),
                    np.zeros((0, int(obs_test.V)), np.float32), ids)
        return (np.concatenate(a_parts).astype(np.float32, copy=False),
                np.concatenate(l_parts).astype(np.float32, copy=False), ids)

    @staticmethod
    def _verify_plain(model: TransformerLM, x: torch.Tensor, logits: torch.Tensor) -> None:
        plain = model(x).logits[:, SequenceLayout().analysis_position].float()
        if float((plain - logits).abs().max()) > _TOL:
            raise _fail(ErrorCode.NUMERICAL_FAILURE, "plain_forward",
                        "hooked logits differ from a plain forward pass by more than 1e-5")
