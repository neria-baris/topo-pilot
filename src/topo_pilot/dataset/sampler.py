"""Vectorised HMM sampler: ``z_1 ~ pi``; emit ``w_t ~ E[z_t]``; then ``z_{t+1} ~ T[z_t]``."""

from __future__ import annotations

import numpy as np

from topo_pilot.contracts import ErrorCode, SequenceLayout, StageFailure

_CHUNK = 4096


def _cumulative_rows(P: np.ndarray) -> np.ndarray:
    """Row-wise CDF with every entry from the last positive probability on set to exactly 1.

    This makes the inverse CDF immune to round-off: a zero-probability column is never drawn.
    """
    cum = np.cumsum(P, axis=1)
    last_pos = P.shape[1] - 1 - np.argmax(P[:, ::-1] > 0, axis=1)
    cols = np.arange(P.shape[1])[None, :]
    cum[cols >= last_pos[:, None]] = 1.0
    return cum


def _draw(cum: np.ndarray, rows: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Inverse CDF: for each ``i`` the smallest ``j`` with ``u[i] < cum[rows[i], j]``."""
    out = np.empty(rows.shape[0], dtype=np.int64)
    for lo in range(0, rows.shape[0], _CHUNK):
        sl = slice(lo, lo + _CHUNK)
        out[sl] = (u[sl, None] >= cum[rows[sl]]).sum(axis=1)
    return np.minimum(out, cum.shape[1] - 1)


class HMMSampler:
    """Samples independent trajectories of ``n_obs = layout.n_obs`` steps.

    Math
    ----
    ``z_1 ~ pi``; for ``t = 1..33``: ``w_t ~ E[z_t]`` (emit), then ``z_{t+1} ~ T[z_t]``.
    Each categorical draw is the inverse CDF of ``u ~ U[0,1)`` on the cumulative row.

    Shapes
    ------
    ``T [N, N]``, ``E [N, V]``, ``pi [N]`` float64; ``sample`` returns ``tokens uint8[n, 33]``
    (``uint16`` if V > 255) and ``states int16[n, 33]``.

    Invariants
    ----------
    ``tokens[:, t]`` is emitted by ``states[:, t]``. Draw order per step is fixed (emission
    uniform, then transition uniform), so the output is a pure function of the rng state.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on inconsistent shapes of ``T``, ``E``, ``pi``.
    """

    def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray, layout: SequenceLayout):
        T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
        n = pi.shape[0]
        if T.shape != (n, n) or E.ndim != 2 or E.shape[0] != n:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "dataset.HMMSampler", "shapes",
                               f"T {T.shape}, E {E.shape}, pi {pi.shape}")
        self.N, self.V = n, E.shape[1]
        self.layout = layout
        self._cum_T = _cumulative_rows(T)
        self._cum_E = _cumulative_rows(E)
        self._cum_pi = _cumulative_rows(pi[None, :])

    def sample(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        """Draw ``n`` trajectories; returns ``(tokens [n, 33], states [n, 33])``."""
        steps = self.layout.n_obs
        tokens = np.zeros((n, steps), dtype=np.uint8 if self.V <= 255 else np.uint16)
        states = np.zeros((n, steps), dtype=np.int16)
        z = _draw(self._cum_pi, np.zeros(n, dtype=np.int64), rng.random(n))
        for t in range(steps):
            states[:, t] = z
            tokens[:, t] = _draw(self._cum_E, z, rng.random(n))
            if t < steps - 1:
                z = _draw(self._cum_T, z, rng.random(n))
        return tokens, states
