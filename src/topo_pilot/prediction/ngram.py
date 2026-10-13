"""n-gram baselines (part a): additive and interpolated Kneser-Ney smoothing."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, ObservationSet, StageFailure

_COMPONENT = "prediction.NGramBaseline"
_DEFAULT_ALPHA = {"additive": 1.0, "kneser_ney": 0.75}


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


class NGramBaseline:
    """Order-1 (unigram) or order-2 (bigram) next-token model fitted on train tokens only.

    Math
    ----
    Additive: ``p(w|c) = (n(c,w) + a) / (n(c) + a V)``.
    Kneser-Ney (order 2, interpolated, absolute discount ``d = a``)::

        p(w|c) = max(n(c,w) - d, 0)/n(c) + d N1+(c,.)/n(c) * p_cont(w)
        p_cont(w) = N1+(.,w) / N1+(.,.)

    Order 1 with ``kneser_ney`` equals additive with ``a = 0`` (MLE). With ``a = 0`` an unseen
    context (``n(c) = 0``) backs off to the unigram MLE; for KN an unseen context uses
    ``p_cont``. Order 2 conditions on the last token only (order - 1 tokens).

    Shapes
    ------
    ``fit``: all 33 positions of ``train.tokens [R, 33]``; contexts never cross sequences and
    no BOS context exists. ``predict(histories [M, p]) -> [M, V]`` float64, rows sum to 1.

    Invariants
    ----------
    Only the train set is used by ``fit``; ``select_smoothing`` touches dev only to score.
    The default alpha is 1.0 (additive) or 0.75 (kneser_ney).

    Raises
    ------
    INVALID_CONFIG : bad order, smoothing name, negative alpha, empty grid.
    ALIGNMENT_ERROR : ``predict`` called before ``fit`` or with bad history shape.
    """

    def __init__(self, order: int, smoothing: Literal["additive", "kneser_ney"],
                 alpha: float | None = None) -> None:
        if order not in (1, 2):
            raise _fail(ErrorCode.INVALID_CONFIG, "order", f"order={order}")
        if smoothing not in _DEFAULT_ALPHA:
            raise _fail(ErrorCode.INVALID_CONFIG, "smoothing", f"smoothing={smoothing!r}")
        self.order = order
        self.smoothing = smoothing
        self.alpha = self._check_alpha(_DEFAULT_ALPHA[smoothing] if alpha is None else alpha)
        self._unigram: NDArray[np.float64] | None = None
        self._bigram: NDArray[np.float64] | None = None
        self.V = 0

    @staticmethod
    def _check_alpha(alpha: float) -> float:
        if not np.isfinite(alpha) or alpha < 0:
            raise _fail(ErrorCode.INVALID_CONFIG, "alpha", f"alpha={alpha}")
        return float(alpha)

    def fit(self, train: ObservationSet) -> NGramBaseline:
        """Count unigrams (all positions) and within-sequence bigrams on ``train``."""
        tokens = train.tokens.astype(np.int64)
        self.V = int(train.V)
        self._unigram = np.bincount(tokens.ravel(), minlength=self.V).astype(np.float64)
        pair = tokens[:, :-1] * self.V + tokens[:, 1:]
        self._bigram = np.bincount(pair.ravel(), minlength=self.V**2).astype(
            np.float64).reshape(self.V, self.V)
        return self

    def _require_fit(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        if self._unigram is None or self._bigram is None:
            raise _fail(ErrorCode.ALIGNMENT_ERROR, "fitted", "fit() has not been called")
        return self._unigram, self._bigram

    def _unigram_probs(self, uni: NDArray[np.float64], alpha: float) -> NDArray[np.float64]:
        return (uni + alpha) / (uni.sum() + alpha * self.V)

    def _context_table(self, alpha: float) -> NDArray[np.float64]:
        """Return ``[V, V]`` table ``P[c, w]`` for order 2 (one row per possible context)."""
        uni, big = self._require_fit()
        row = big.sum(axis=1, keepdims=True)
        seen = row[:, 0] > 0
        safe_row = np.where(row > 0, row, 1.0)
        if self.smoothing == "additive":
            table = (big + alpha) / np.where(row + alpha * self.V > 0, row + alpha * self.V, 1.0)
            table[~seen] = self._unigram_probs(uni, alpha)
            return table
        types_in = (big > 0).sum(axis=0).astype(np.float64)
        p_cont = types_in / types_in.sum()
        n_follow = (big > 0).sum(axis=1, keepdims=True).astype(np.float64)
        table = np.maximum(big - alpha, 0.0) / safe_row + alpha * n_follow / safe_row * p_cont
        table[~seen] = p_cont
        return table

    def predict(self, histories: np.ndarray) -> np.ndarray:
        """Map histories ``[M, p]`` of token ids to next-token distributions ``[M, V]``."""
        uni, _ = self._require_fit()
        hist = np.asarray(histories)
        if hist.ndim != 2 or (self.order == 2 and hist.shape[1] < 1):
            raise _fail(ErrorCode.ALIGNMENT_ERROR, "histories", f"shape {hist.shape}")
        if self.order == 1:
            alpha = 0.0 if self.smoothing == "kneser_ney" else self.alpha
            return np.tile(self._unigram_probs(uni, alpha), (hist.shape[0], 1))
        return self._context_table(self.alpha)[hist[:, -1].astype(np.int64)]

    def select_smoothing(self, dev: ObservationSet, grid: Sequence[float]) -> float:
        """Pick alpha minimising dev CE of ``w_33`` given ``w_1..w_32`` (D-021).

        Ties go to the earliest grid value. Nothing is refitted.
        """
        if len(grid) == 0:
            raise _fail(ErrorCode.INVALID_CONFIG, "grid", "empty smoothing grid")
        tokens = dev.tokens.astype(np.int64)
        histories, targets = tokens[:, :32], tokens[:, 32]
        scores = []
        for alpha in grid:
            self.alpha = self._check_alpha(alpha)
            probs = self.predict(histories)[np.arange(len(targets)), targets]
            with np.errstate(divide="ignore"):
                scores.append(float(-np.mean(np.log(probs))))
        self.alpha = float(grid[int(np.argmin(scores))])
        return self.alpha
