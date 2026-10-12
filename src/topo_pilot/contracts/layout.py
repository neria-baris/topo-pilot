"""The single source of sequence alignment (DATA_SCHEMAS §3)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .errors import ErrorCode, StageFailure


@dataclass(frozen=True)
class SequenceLayout:
    """Alignment between observed symbols, model positions, targets, and oracle quantities.

    A trajectory has ``n_obs = 33`` observed symbols ``w_1..w_33`` (stored as ``tokens[:, 0..32]``).
    The model sees ``context + 1 = 33`` positions ``p = 0..32``.

    ==========  ===========  =========  ========  ====================  ==========================
    position p  input token  history    target    oracle quantity       latent label
    ==========  ===========  =========  ========  ====================  ==========================
    0           BOS (= V)    (empty)    w_1       q_0 = pi E            z_1
    p >= 1      w_p          w_1..w_p   w_{p+1}   b_p, q_p = b_p T E    z_p (current), z_{p+1}
    32          w_32         w_1..w_32  w_33      b_32, b^(1)=r_{w_32}  z_32
    ==========  ===========  =========  ========  ====================  ==========================

    Shapes: ``tokens`` is ``[R, 33]`` integer; ``model_inputs`` and ``targets`` are ``[R, 33]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` for a wrong shape, a non-integer dtype, or a position out of range.
    """

    n_obs: int = 33
    context: int = 32
    analysis_position: int = 32

    def bos_id(self, V: int) -> int:
        """Id of the BOS token: ``V`` (the input vocabulary is ``V + 1``)."""
        return int(V)

    def _check(self, tokens: np.ndarray) -> np.ndarray:
        arr = np.asarray(tokens)
        if arr.ndim != 2 or arr.shape[1] != self.n_obs or not np.issubdtype(arr.dtype, np.integer):
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "contracts.SequenceLayout", "shape",
                               f"expected integer [R, {self.n_obs}], got {arr.dtype} {arr.shape}")
        return arr

    def model_inputs(self, tokens: np.ndarray, V: int) -> np.ndarray:
        """``[BOS, w_1..w_32]`` per row: ``[R, 33] -> [R, 33]``, dtype int64.

        ``V`` is required to know the BOS id (SPEC deviation D-008: the SPEC omitted it).
        """
        arr = self._check(tokens)
        bos = np.full((arr.shape[0], 1), self.bos_id(V), dtype=np.int64)
        return np.concatenate([bos, arr[:, : self.context].astype(np.int64)], axis=1)

    def targets(self, tokens: np.ndarray) -> np.ndarray:
        """``[w_1..w_33]`` per row: ``[R, 33] -> [R, 33]``, dtype int64 (a copy)."""
        return self._check(tokens).astype(np.int64, copy=True)

    def history(self, tokens_row: np.ndarray, p: int) -> np.ndarray:
        """The history seen at position ``p``: ``w_1..w_p`` (empty for ``p = 0``), int64."""
        row = np.asarray(tokens_row)
        if row.ndim != 1 or row.shape[0] != self.n_obs:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "contracts.SequenceLayout", "row_shape",
                               f"expected a row of {self.n_obs} tokens, got {row.shape}")
        if not 0 <= int(p) <= self.context:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "contracts.SequenceLayout", "position",
                               f"position {p} outside 0..{self.context}")
        return row[: int(p)].astype(np.int64, copy=True)
