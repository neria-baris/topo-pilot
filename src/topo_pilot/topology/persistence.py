"""Vietoris-Rips persistent homology via ripser, with censoring, dedup-safe input and timeout."""

from __future__ import annotations

import multiprocessing as mp
from dataclasses import dataclass
from typing import Literal

import numpy as np
import ripser as _ripser
from numpy.typing import NDArray
from scipy.sparse.csgraph import minimum_spanning_tree

from topo_pilot.contracts import ErrorCode, StageFailure, Status

_COMPONENT = "topology.PersistenceComputer"
_DIRECT_MAX_POINTS = 600  # up to this (maxdim <= 1, timeout >= 1 s) ripser runs in-process


def _is_prime(n: int) -> bool:
    return n >= 2 and all(n % k for k in range(2, int(n**0.5) + 1))


@dataclass(frozen=True)
class PHConfig:
    """Persistent-homology configuration.

    ``threshold="auto"`` means ``max(D)`` (every H1 bar closes). ``landmarks`` is only legal with
    ``maxdim >= 2`` (extensions). ``pca_dims`` is carried for the caller; it is not used here.
    """

    maxdim: int = 1
    coeff_p: int = 2
    threshold: Literal["auto"] | float = "auto"
    pca_dims: int | None = None
    landmarks: int | None = None
    timeout_s: float = 600

    def __post_init__(self) -> None:
        bad = (
            self.maxdim < 0
            or not _is_prime(self.coeff_p)
            or self.timeout_s <= 0
            or (self.threshold != "auto" and not float(self.threshold) > 0)
            or (self.landmarks is not None and (self.landmarks < 2 or self.maxdim < 2))
        )
        if bad:
            raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "PHConfig", f"invalid {self}")


@dataclass(frozen=True, eq=False)
class DiagramResult:
    """Persistence diagrams (pure result; persisted later as ``Diagrams``).

    Shapes
    ------
    ``rows: [n, 4] float64`` columns (dim, birth, death, censored), sorted by (dim, birth, death).

    Invariants
    ----------
    ``censored == 1`` iff dim >= 1 and death is inf. H0 essential bars keep death = inf with
    censored = 0. ``status``: OK, CENSORED (a censored bar or a timeout), COLLAPSED (single
    point or all-zero D), APPROXIMATE (landmarks).
    """

    rows: NDArray[np.float64]
    coeff_p: int
    maxdim: int
    threshold: float
    library_version: str
    status: Status


def _validate_matrix(D: NDArray[np.float64]) -> NDArray[np.float64]:
    D = np.asarray(D, dtype=np.float64)
    ok = D.ndim == 2 and D.shape[0] == D.shape[1] and D.shape[0] >= 1 and np.all(np.isfinite(D))
    if ok:
        tol = 1e-9 * max(1.0, float(np.abs(D).max()))
        ok = bool(
            np.abs(D - D.T).max() <= tol and D.min() >= -tol and np.abs(np.diag(D)).max() <= tol
        )
    if not ok:
        raise StageFailure(ErrorCode.NON_METRIC, _COMPONENT, "distance_matrix",
                           "D must be finite, square, symmetric, non-negative, zero diagonal")
    return D


def _rows_from_dgms(dgms: list[NDArray[np.float64]]) -> NDArray[np.float64]:
    blocks = []
    for dim, dgm in enumerate(dgms):
        if len(dgm) == 0:
            continue
        cens = (np.isinf(dgm[:, 1]) & (dim >= 1)).astype(np.float64)
        blocks.append(np.column_stack([np.full(len(dgm), dim, dtype=np.float64), dgm, cens]))
    if not blocks:
        return np.zeros((0, 4), dtype=np.float64)
    rows = np.vstack(blocks)
    return rows[np.lexsort((rows[:, 2], rows[:, 1], rows[:, 0]))]


def _ripser_job(conn, D, maxdim, coeff, thresh) -> None:  # runs in a spawned worker
    try:
        out = _ripser.ripser(D, maxdim=maxdim, thresh=thresh, coeff=coeff, distance_matrix=True)
        conn.send(("ok", out["dgms"]))
    except BaseException as exc:  # noqa: BLE001 - reported to the parent, never swallowed
        conn.send(("err", repr(exc)))
    finally:
        conn.close()


def _run_ripser_worker(D, maxdim, coeff, thresh, timeout_s):
    """Run ripser in a spawned process; ``None`` on timeout (worker is terminated)."""
    ctx = mp.get_context("spawn")
    parent, child = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_ripser_job, args=(child, D, maxdim, coeff, thresh), daemon=True)
    proc.start()
    child.close()
    try:
        if not parent.poll(timeout_s):
            return None
        kind, payload = parent.recv()
    except EOFError:
        kind, payload = "err", "worker died"
    finally:
        proc.terminate()
        proc.join(5)
        parent.close()
    if kind != "ok":
        raise StageFailure(ErrorCode.PH_RESOURCE_LIMIT, _COMPONENT, "worker", str(payload),
                           recoverable=True)
    return payload


def _h0_from_mst(D: NDArray[np.float64]) -> list[NDArray[np.float64]]:
    """H0 diagram from the minimum spanning tree (cheap partial result after a timeout)."""
    w = np.sort(minimum_spanning_tree(np.where(D > 0, D, 1e-300)).data) if len(D) > 1 else []
    finite = np.column_stack([np.zeros(len(w)), np.asarray(w)]) if len(w) else np.zeros((0, 2))
    return [np.vstack([finite, [[0.0, np.inf]]])]


class PersistenceComputer:
    """Vietoris-Rips persistent homology of a distance matrix.

    Math
    ----
    Filtration ``VR_r(D)`` = clique complex of the graph with edges ``D[i,j] <= r``, homology
    over ``F_p`` (``coeff_p``), dimensions ``0..maxdim``, threshold ``thresh``.

    Shapes
    ------
    ``D: [M, M]`` -> ``DiagramResult.rows: [n, 4]``.

    Raises
    ------
    StageFailure
        ``NON_METRIC`` (bad D), ``INVALID_CONFIG``, ``PH_RESOURCE_LIMIT`` (worker failure or
        MemoryError). A timeout is not an error: status ``CENSORED`` with the H0 diagram only.
    """

    def __init__(self, cfg: PHConfig):
        self.cfg = cfg

    def _dgms(self, D: NDArray[np.float64], thresh: float):
        cfg = self.cfg
        cheap = len(D) <= _DIRECT_MAX_POINTS and cfg.maxdim <= 1 and cfg.timeout_s >= 1.0
        try:
            if cheap:
                out = _ripser.ripser(D, maxdim=cfg.maxdim, thresh=thresh, coeff=cfg.coeff_p,
                                     distance_matrix=True)
                return out["dgms"]
            return _run_ripser_worker(D, cfg.maxdim, cfg.coeff_p, thresh, cfg.timeout_s)
        except MemoryError as exc:
            raise StageFailure(ErrorCode.PH_RESOURCE_LIMIT, _COMPONENT, "memory", repr(exc),
                               recoverable=True) from exc

    def diagrams(self, D: NDArray[np.float64]) -> DiagramResult:
        """Compute the diagrams of ``D`` (see class docstring); never crashes on a timeout."""
        cfg = self.cfg
        D = _validate_matrix(D)
        version = f"ripser {_ripser.__version__}"
        dmax = float(D.max())
        thresh = dmax if cfg.threshold == "auto" else float(cfg.threshold)
        if dmax == 0.0 or len(D) == 1:
            rows = _rows_from_dgms([np.array([[0.0, np.inf]])])
            return DiagramResult(rows, cfg.coeff_p, cfg.maxdim, thresh, version, Status.COLLAPSED)
        status = Status.OK
        if cfg.landmarks is not None:
            D = D[np.ix_(*(2 * [self._maxmin(D, cfg.landmarks, 0)]))]
            status = Status.APPROXIMATE
        dgms = self._dgms(D, thresh)
        if dgms is None:
            return DiagramResult(_rows_from_dgms(_h0_from_mst(D)), cfg.coeff_p, cfg.maxdim,
                                 thresh, version, Status.CENSORED)
        rows = _rows_from_dgms(dgms)
        if rows[:, 3].any():
            status = Status.CENSORED
        return DiagramResult(rows, cfg.coeff_p, cfg.maxdim, thresh, version, status)

    @staticmethod
    def _maxmin(D: NDArray[np.float64], m: int, start: int) -> NDArray[np.int64]:
        idx = [start]
        mind = D[start].copy()
        for _ in range(m - 1):
            nxt = int(np.argmax(mind))
            idx.append(nxt)
            mind = np.minimum(mind, D[nxt])
        return np.asarray(idx, dtype=np.int64)

    def maxmin_landmarks(self, D: NDArray[np.float64], m: int,
                         rng: np.random.Generator) -> NDArray[np.int64]:
        """Greedy farthest-point (maxmin) landmarks: random first point, then argmax of min-dist.

        Returns ``[m]`` int64 indices. Raises ``INVALID_CONFIG`` unless ``1 <= m <= M``.
        """
        D = _validate_matrix(D)
        if not 1 <= m <= len(D):
            raise StageFailure(ErrorCode.INVALID_CONFIG, _COMPONENT, "landmarks",
                               f"m={m} not in [1, {len(D)}]")
        return self._maxmin(D, m, int(rng.integers(len(D))))
