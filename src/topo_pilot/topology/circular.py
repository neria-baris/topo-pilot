"""Circular coordinates (de Silva, Morozov, Vejdemo-Johansson) from the top H1 cocycle."""

from __future__ import annotations

import numpy as np
import ripser as _ripser
from numpy.typing import NDArray
from scipy.sparse import coo_matrix

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "topology.CircularCoordinates"
_LIFETIME_FRACTION = 0.5  # scale r = birth + fraction * (death - birth)


class CircularCoordinates:
    """Angles on S^1 from the cocycle of the most persistent H1 class.

    Math
    ----
    1. Rips persistence over ``F_p`` with cocycles; take the finite H1 bar ``(b, d)`` of maximal
       persistence and its cocycle ``a: edges -> {0..p-1}``.
    2. Scale ``r = (b + d) / 2`` (inside the lifetime). Graph ``G_r``: edges with ``D <= r``.
    3. Lift to integers: ``alpha_e = a_e`` if ``a_e <= p/2`` else ``a_e - p`` (0 on edges outside
       the cocycle support), seen as a real 1-cochain on ``G_r``.
    4. Solve ``f = argmin_f sum_{(i,j) in G_r} (f_j - f_i - alpha_ij)^2`` (graph Laplacian
       least squares; minimal-norm solution). ``alpha - delta f`` is the harmonic representative.
    5. ``theta_i = 2 pi (f_i mod 1)``.

    Shapes
    ------
    ``D: [M, M]`` -> angles ``[M]`` in ``[0, 2 pi)``. Angles are defined up to rotation and
    reflection (global sign of the cocycle). Disconnected components of ``G_r`` get independent
    offsets.

    Raises
    ------
    StageFailure
        ``INVALID_CONFIG`` (``coeff_p`` not an odd prime), ``NON_METRIC`` (bad D),
        ``NUMERICAL_FAILURE`` (check ``no_h1_class``) when D has no finite H1 bar.
    """

    def __init__(self, coeff_p: int = 47):
        if coeff_p < 3 or any(coeff_p % k == 0 for k in range(2, int(coeff_p**0.5) + 1)):
            raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "coeff_p",
                               "coeff_p must be an odd prime (a field with a lift to Z)")
        self.coeff_p = coeff_p

    def _top_cocycle(self, D: NDArray[np.float64]):
        out = _ripser.ripser(D, maxdim=1, thresh=float(D.max()), coeff=self.coeff_p,
                             distance_matrix=True, do_cocycles=True)
        dgm = out["dgms"][1]
        if len(dgm) == 0:
            raise StageFailure(ErrorCode.NUMERICAL_FAILURE, _COMPONENT, "no_h1_class",
                               "no finite H1 bar to build coordinates from")
        k = int(np.argmax(dgm[:, 1] - dgm[:, 0]))
        return float(dgm[k, 0]), float(dgm[k, 1]), np.asarray(out["cocycles"][1][k])

    def fit_transform(self, D: NDArray[np.float64]) -> NDArray[np.float64]:
        """Return circular coordinates ``[M]`` in ``[0, 2 pi)`` for the distance matrix ``D``."""
        D = np.asarray(D, dtype=np.float64)
        if D.ndim != 2 or D.shape[0] != D.shape[1] or not np.allclose(D, D.T):
            raise StageFailure(ErrorCode.NON_METRIC, _COMPONENT, "distance_matrix",
                               "D must be square and symmetric")
        birth, death, coc = self._top_cocycle(D)
        r = birth + _LIFETIME_FRACTION * (death - birth)
        M = D.shape[0]
        iu, ju = np.triu_indices(M, k=1)
        in_graph = D[iu, ju] <= r
        iu, ju = iu[in_graph], ju[in_graph]
        alpha = np.zeros(len(iu))
        vals = coc[:, 2].astype(np.int64)
        vals = np.where(vals > self.coeff_p // 2, vals - self.coeff_p, vals)
        flip = np.where(coc[:, 0] <= coc[:, 1], 1.0, -1.0)  # orient every entry as i < j
        lo = np.minimum(coc[:, 0], coc[:, 1]).astype(np.int64)
        hi = np.maximum(coc[:, 0], coc[:, 1]).astype(np.int64)
        edge_index = {(int(a), int(b)): n for n, (a, b) in enumerate(zip(iu, ju))}
        for a, b, val, sg in zip(lo, hi, vals, flip):
            n = edge_index.get((int(a), int(b)))
            if n is not None:
                alpha[n] = sg * val
        E = len(iu)
        rows = np.repeat(np.arange(E), 2)
        B = coo_matrix((np.tile([-1.0, 1.0], E), (rows, np.column_stack([iu, ju]).ravel())),
                       shape=(E, M)).tocsr()
        f = np.linalg.lstsq((B.T @ B).toarray(), B.T @ alpha, rcond=None)[0]
        return np.mod(f, 1.0) * 2.0 * np.pi
