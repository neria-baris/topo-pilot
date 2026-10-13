"""Cubical complex: signed boundary matrices over Z, exact ranks and Betti numbers over GF(p)."""

from __future__ import annotations

from typing import Mapping

import numpy as np
import scipy.sparse as sp

from topo_pilot.contracts import ErrorCode, StageFailure

_COMPONENT = "world.CubicalComplex"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def rank_mod_p(matrix: np.ndarray, p: int) -> int:
    """Rank of an integer matrix over GF(p) by Gaussian elimination on dense ``int64``.

    Math
    ----
    Row-reduce ``A mod p`` with pivots inverted via ``pow(a, -1, p)``; the rank is the number
    of pivots.

    Shapes
    ------
    ``matrix: [r, c]`` integers; returns a Python ``int``.
    """
    a = np.array(matrix, dtype=np.int64) % p
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        if rank == rows:
            break
        nz = np.nonzero(a[rank:, col])[0]
        if nz.size == 0:
            continue
        piv = rank + int(nz[0])
        if piv != rank:
            a[[rank, piv]] = a[[piv, rank]]
        a[rank] = (a[rank] * pow(int(a[rank, col]), -1, p)) % p
        below = a[rank + 1:, col].copy()
        if below.any():
            a[rank + 1:] = (a[rank + 1:] - np.outer(below, a[rank])) % p
        rank += 1
    return rank


def _is_prime(p: int) -> bool:
    return p >= 2 and all(p % q for q in range(2, int(p**0.5) + 1))


def _face_table(k: int) -> list[tuple[int, list[int]]]:
    """For a k-cube: ``[(sign, corner indices)]`` of its 2k facets.

    Corner index ``j`` has axis-``i`` coordinate ``(j >> (k-1-i)) & 1``. Facet ``(i, side)``
    has sign ``(-1)^i`` for ``side = 1`` and ``-(-1)^i`` for ``side = 0``.
    """
    table = []
    for i in range(k):
        for side in (1, 0):
            sign = (-1) ** i * (1 if side else -1)
            table.append((sign, [j for j in range(2**k) if (j >> (k - 1 - i)) & 1 == side]))
    return table


def _perm_sign(perm: list[int]) -> int:
    sign, seen = 1, [False] * len(perm)
    for start in range(len(perm)):
        if seen[start]:
            continue
        length, j = 0, start
        while not seen[j]:
            seen[j], j, length = True, perm[j], length + 1
        sign *= -1 if length % 2 == 0 else 1
    return sign


def _relative_orientation(face: tuple[int, ...], stored: tuple[int, ...], m: int) -> int:
    """Sign of the cube symmetry taking the vertex tuple ``face`` to ``stored`` (m-cubes).

    The symmetry is ``corner j -> permute_axes(j) xor r``; its sign is
    ``sgn(axis permutation) * (-1)^popcount(r)``. Raises ``INVALID_GLUE`` if the vertex
    correspondence is not a cube symmetry.
    """
    if m == 0:
        return 1
    bad = _fail(ErrorCode.INVALID_GLUE, "face_orientation", "facet is not a cube symmetry")
    pos = [stored.index(v) for v in face]
    refl = pos[0]
    axis_img = []
    for i in range(m):
        image = pos[1 << (m - 1 - i)] ^ refl
        if image == 0 or image & (image - 1):
            raise bad
        axis_img.append(m - image.bit_length())
    if sorted(axis_img) != list(range(m)):
        raise bad
    for j in range(2**m):
        img = sum(((j >> (m - 1 - i)) & 1) << (m - 1 - axis_img[i]) for i in range(m)) ^ refl
        if img != pos[j]:
            raise bad
    return _perm_sign(axis_img) * (-1) ** bin(refl).count("1")


class CubicalComplex:
    """Cells of dim 0..3 as ordered vertex tuples (a k-cube has 2**k vertices, in local
    lexicographic order).

    Math
    ----
    ``d(c) = sum_i (-1)^i (face_{i,1} - face_{i,0})`` for a k-cube whose axis ``i`` is bit
    ``k-1-i`` of the local corner index; facets are re-oriented to the stored vertex order of
    the matching (k-1)-cell, so ``d_{k-1} d_k = 0``.
    ``beta_k = n_k - rank_p d_k - rank_p d_{k+1}``.

    Shapes
    ------
    ``cells[k]: int [n_k, 2**k]``; ``boundary_matrix(k): csr int64 [n_{k-1}, n_k]``.

    Invariants
    ----------
    Cell dims are ``0..K`` contiguous; widths ``2**k``; vertex ids in ``[0, n_vertices)``.

    Raises
    ------
    StageFailure
        ``INVALID_GLUE`` for a bad width/id, a cell repeating a vertex, a missing facet or a
        facet that is not a cube symmetry of its stored cell.
    """

    def __init__(self, n_vertices: int, cells: Mapping[int, np.ndarray]):
        self.n_vertices = int(n_vertices)
        arrs = {int(k): np.asarray(v, dtype=np.int64) for k, v in cells.items()}
        arrs.setdefault(0, np.arange(self.n_vertices, dtype=np.int64)[:, None])
        if sorted(arrs) != list(range(len(arrs))):
            raise _fail(ErrorCode.INVALID_GLUE, "cell_dims", f"cell dims {sorted(arrs)} not 0..K")
        for k, arr in arrs.items():
            if arr.ndim != 2 or arr.shape[1] != 2**k:
                raise _fail(ErrorCode.INVALID_GLUE, f"cells_{k}_width", f"{k}-cells need 2**k ids")
            if arr.size and (arr.min() < 0 or arr.max() >= self.n_vertices):
                raise _fail(ErrorCode.INVALID_GLUE, f"cells_{k}_ids", "vertex id out of range")
            srt = np.sort(arr, axis=1)
            if k > 0 and np.any(srt[:, 1:] == srt[:, :-1]):
                raise _fail(ErrorCode.INVALID_GLUE, f"cells_{k}_repeat", "a cell repeats a vertex")
        self.cells = arrs
        self._boundary: dict[int, sp.csr_matrix] = {}

    @property
    def top_dim(self) -> int:
        """Highest cell dimension K."""
        return len(self.cells) - 1

    def boundary_matrix(self, k: int) -> sp.csr_matrix:
        """Signed integer boundary ``d_k`` of shape ``[n_{k-1}, n_k]`` (cached)."""
        if k not in self._boundary:
            self._boundary[k] = self._build_boundary(k)
        return self._boundary[k]

    def _build_boundary(self, k: int) -> sp.csr_matrix:
        n_hi = len(self.cells[k]) if k in self.cells else 0
        if k < 1 or k > self.top_dim:
            n_lo = len(self.cells[k - 1]) if (k - 1) in self.cells else 0
            return sp.csr_matrix((n_lo, n_hi), dtype=np.int64)
        lower = self.cells[k - 1]
        index = {tuple(sorted(row)): j for j, row in enumerate(lower.tolist())}
        table = _face_table(k)
        rows, cols, vals = [], [], []
        for c, cell in enumerate(self.cells[k].tolist()):
            for sign, corners in table:
                face = tuple(cell[j] for j in corners)
                r = index.get(tuple(sorted(face)))
                if r is None:
                    raise _fail(ErrorCode.INVALID_GLUE, "missing_face", f"a {k}-cell has no facet")
                s = _relative_orientation(face, tuple(lower[r].tolist()), k - 1)
                rows.append(r)
                cols.append(c)
                vals.append(sign * s)
        mat = sp.coo_matrix((vals, (rows, cols)), shape=(len(lower), n_hi), dtype=np.int64)
        return mat.tocsr()

    def betti(self, p: int = 2) -> tuple[int, ...]:
        """Betti numbers ``(beta_0..beta_K)`` over GF(p), p prime.

        Raises ``INVALID_CONFIG`` if ``p`` is not prime.
        """
        if not _is_prime(int(p)):
            raise _fail(ErrorCode.INVALID_CONFIG, "prime", f"p={p} is not prime")
        top = self.top_dim
        ranks = [0] + [rank_mod_p(self.boundary_matrix(k).toarray(), p) for k in range(1, top + 1)]
        ranks.append(0)
        return tuple(len(self.cells[k]) - ranks[k] - ranks[k + 1] for k in range(top + 1))

    def euler_characteristic(self) -> int:
        """``sum_k (-1)^k n_k``."""
        return int(sum((-1) ** k * len(c) for k, c in self.cells.items()))

    def one_skeleton(self) -> np.ndarray:
        """``int32[E, 2]`` edges, canonical ``(lo, hi)``, unique, lexicographically sorted."""
        if 1 not in self.cells:
            return np.zeros((0, 2), dtype=np.int32)
        return np.unique(np.sort(self.cells[1], axis=1), axis=0).astype(np.int32)


def check_boundary_closed(cx: CubicalComplex) -> None:
    """Require ``d_{k-1} d_k = 0`` over Z for all k.

    Raises ``BETTI_MISMATCH`` with check ``boundary_not_closed``.
    """
    for k in range(2, cx.top_dim + 1):
        if (cx.boundary_matrix(k - 1) @ cx.boundary_matrix(k)).count_nonzero():
            raise StageFailure(ErrorCode.BETTI_MISMATCH, _COMPONENT, "boundary_not_closed",
                               f"d_{k - 1} d_{k} != 0")
