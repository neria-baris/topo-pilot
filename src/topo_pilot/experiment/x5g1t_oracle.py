"""X5 G1 training-study oracle rows (x5g1-train-v3 §4): the exact predictive for w33 from the
public history w1..w32 only; column 33 (the target) is never read."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from topo_pilot.oracle import BayesFilter

END = 32


def oracle_q32(T: NDArray, E: NDArray, pi: NDArray, tokens: NDArray,
               guard: Callable[[str], None] | None = None, batch: int = 4096) -> NDArray:
    """``BayesFilter(T, E, pi).run(tokens[:, :32]).q[:, 32]`` in batches; ``[R, V]`` float64.

    Tokens are named (``perm[canon]``), so ``E`` is the stored, named emission matrix.
    """
    hist = np.asarray(tokens)[:, :END].astype(np.int64)
    filt = BayesFilter(*(np.asarray(a, dtype=np.float64) for a in (T, E, pi)))
    out = []
    for i in range(0, hist.shape[0], batch):
        if guard:
            guard(f"oracle {i}")
        out.append(filt.run(hist[i:i + batch]).q[:, END])
        if guard:
            guard(f"oracle {i} done")
    return np.concatenate(out, axis=0)
