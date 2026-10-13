"""Scaled forward filter and the last-symbol posterior (pure kernels)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode

from ._common import as_model, check_rows_sum_to_one, check_tokens, fail, normalise_rows


@dataclass(frozen=True, eq=False)
class FilterResult:
    """Output of :meth:`BayesFilter.run`.

    Shapes: ``b [R, P, N]`` with ``b[:, t-1] = b_t``; ``q [R, P+1, V]`` with ``q[:, 0] = pi E`` and
    ``q[:, t] = b_t T E``; ``log_evidence [R]`` (nats, sum of log normalisers);
    ``ce [R, P]`` with ``ce[:, t-1] = -log q_{t-1}(w_t)``. All float64.
    """

    b: NDArray[np.float64]
    q: NDArray[np.float64]
    log_evidence: NDArray[np.float64]
    ce: NDArray[np.float64]


class BayesFilter:
    """Exact scaled forward filter (row vectors, float64, reset to ``pi`` per row).

    Math
    ----
    ``a_1 = pi``; ``b_t = a_t * E[:, w_t] / (a_t E[:, w_t])``; ``a_{t+1} = b_t T``;
    ``q_t = b_t T E``; ``q_0 = pi E``; ``log p(w_{1:P}) = sum_t log(a_t E[:, w_t])``.

    Shapes
    ------
    ``T: [N, N]``, ``E: [N, V]``, ``pi: [N]``; ``tokens: [R, P]`` integer, ``P <= 33``.

    Invariants
    ----------
    Beliefs and predictives sum to 1 within 1e-10. No epsilon is ever added.

    Raises
    ------
    StageFailure
        ``IMPOSSIBLE_HISTORY`` (zero normaliser), ``NUMERICAL_FAILURE`` (sums off 1),
        ``ALIGNMENT_ERROR`` (P > 33, symbol >= V, bad shapes).
    """

    def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray) -> None:
        self.T, self.E, self.pi = as_model(T, E, pi)
        self.TE = self.T @ self.E

    def run(self, tokens: np.ndarray) -> FilterResult:
        """Filter every row of ``tokens [R, P]`` (see class docstring for the recursion)."""
        tok = check_tokens(tokens, self.E.shape[1])
        n_rows, length = tok.shape
        b = np.empty((n_rows, length, self.T.shape[0]))
        q = np.empty((n_rows, length + 1, self.E.shape[1]))
        ce = np.empty((n_rows, length))
        log_ev = np.zeros(n_rows)
        q[:, 0] = self.pi @ self.E
        prior = np.broadcast_to(self.pi, (n_rows, self.pi.size))
        for t in range(length):
            w = tok[:, t]
            post, norm = normalise_rows(prior * self.E[:, w].T, f"evidence_t{t + 1}")
            b[:, t] = post
            q[:, t + 1] = post @ self.TE
            ce[:, t] = -np.log(q[np.arange(n_rows), t, w])
            log_ev += np.log(norm)
            prior = post @ self.T
        check_rows_sum_to_one(b, "belief_sums")
        check_rows_sum_to_one(q, "predictive_sums")
        return FilterResult(b=b, q=q, log_evidence=log_ev, ce=ce)

    def belief_at(self, tokens: np.ndarray, p: int) -> NDArray[np.float64]:
        """``b_p [R, N]`` (posterior after ``w_p``), ``1 <= p <= P``.

        Raises
        ------
        StageFailure
            ``ALIGNMENT_ERROR`` if ``p`` is outside ``1..P``.
        """
        tok = np.asarray(tokens)
        if tok.ndim != 2 or not 1 <= p <= tok.shape[1]:
            raise fail(ErrorCode.ALIGNMENT_ERROR, "belief_position", f"p={p} outside 1..P")
        return self.run(tok[:, :p]).b[:, p - 1]


class LastSymbolPosterior:
    """Posterior from the last symbol alone, ``r_w``, and its predictive ``q_last = r_w T E``.

    Math
    ----
    ``r_w = pi * E[:, w] / (pi E[:, w])``.

    Shapes
    ------
    ``w: [R]`` integer; ``r: [R, N]``; ``q_last: [R, V]``.

    Raises
    ------
    StageFailure
        ``IMPOSSIBLE_HISTORY`` if ``pi E[:, w] = 0``; ``ALIGNMENT_ERROR`` for bad symbols.
    """

    def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray) -> None:
        self.T, self.E, self.pi = as_model(T, E, pi)
        self.TE = self.T @ self.E

    def r(self, w: np.ndarray) -> NDArray[np.float64]:
        """``r_w`` for each symbol in ``w``."""
        sym = check_tokens(np.asarray(w).reshape(-1, 1), self.E.shape[1])[:, 0]
        return normalise_rows(self.pi * self.E[:, sym].T, "last_symbol_evidence")[0]

    def q_last(self, w: np.ndarray) -> NDArray[np.float64]:
        """``r_w T E`` for each symbol in ``w``."""
        out = self.r(w) @ self.TE
        check_rows_sum_to_one(out, "q_last_sums")
        return out
