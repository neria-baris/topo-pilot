"""X5 G1 oracle quantities at p32 (x5g1-feas-v2 §5); history w1..w32 only, w33 never read."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from topo_pilot.analysis import kl_rows
from topo_pilot.contracts import StageFailure
from topo_pilot.oracle import BayesFilter, LastSymbolPosterior

BATCH = 4096
END = 32


def _entropy(q: NDArray) -> NDArray[np.float64]:
    safe = np.where(q > 0, q, 1.0)
    return -(q * np.log(safe)).sum(axis=-1)


def _valid_rows(q: NDArray) -> bool:
    return bool(np.all(np.isfinite(q)) and q.min() >= 0
                and np.max(np.abs(q.sum(axis=-1) - 1.0)) <= 1e-10)


def gate_quantities(T: NDArray, E: NDArray, pi: NDArray, tokens33: NDArray,
                    guard: Callable[[str], None] | None = None) -> dict:
    """Per-row KL of the full-history predictive against last-symbol, stationary-marginal and
    two-symbol predictives (nats), mean positional Bayes entropy, and a validity flag.

    Math
    ----
    ``q_C = b32 T E``; ``q_last = r_{w32} T E``; ``q_2 = b2 T E`` with ``b2`` from (w31, w32)
    under ``pi``; ``q_stat = pi E``. Oracle numerical failures set ``valid = False``.
    """
    hist = np.asarray(tokens33, dtype=np.int64)[:, :END]
    T_, E_, pi_ = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    TE = T_ @ E_
    filt, last = BayesFilter(T_, E_, pi_), LastSymbolPosterior(T_, E_, pi_)
    q_stat = pi_ @ E_
    out = {k: [] for k in ("kl_last", "kl_stationary", "kl_two")}
    pos = np.zeros(END + 1)
    valid = True
    for i in range(0, hist.shape[0], BATCH):
        if guard:
            guard(f"oracle batch {i}")
        h = hist[i:i + BATCH]
        try:
            res = filt.run(h)
            qC = res.q[:, END]
            q_last = last.q_last(h[:, -1])
            q_two = filt.run(h[:, END - 2:]).b[:, 1] @ TE
        except StageFailure:
            valid = False
            break
        valid &= all(_valid_rows(q) for q in (res.q, q_last, q_two))
        for key, ref in (("kl_last", q_last), ("kl_stationary", np.broadcast_to(q_stat, qC.shape)),
                         ("kl_two", q_two)):
            vals, status = kl_rows(qC, ref)
            if vals is None:
                valid = False
                vals = np.full(qC.shape[0], np.nan)
            out[key].append(vals)
        pos += _entropy(res.q).sum(axis=0)
        if guard:
            guard(f"oracle batch {i} done")
    res_out = {k: (np.concatenate(v) if v else np.zeros(0)) for k, v in out.items()}
    res_out["position_entropy"] = pos / hist.shape[0]
    res_out["valid"] = bool(valid and all(np.all(np.isfinite(v)) for v in res_out.values()
                                          if isinstance(v, np.ndarray)))
    return res_out


def bootstrap_means(values: NDArray, rng: np.random.Generator, n_draws: int = 2000,
                    batch: int = 500, guard: Callable[[str], None] | None = None) -> NDArray:
    """Means of ``values[rng.integers(0, n, n)]`` for ``n_draws`` draws, in batches with the
    guard called before and after each batch."""
    v = np.asarray(values, dtype=np.float64)
    n = v.size
    out = np.empty(n_draws)
    for start in range(0, n_draws, batch):
        if guard:
            guard(f"bootstrap {start}")
        for j in range(start, min(start + batch, n_draws)):
            out[j] = v[rng.integers(0, n, n)].mean()
        if guard:
            guard(f"bootstrap {start} done")
    return out
