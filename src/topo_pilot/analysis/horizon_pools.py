"""Horizon feasibility (part e, X4 Phase B): reachable near-Q1 / distinct-Q2 screening.

Pure functions over per-history arrays of one pool. Nearest-neighbour pairs are dependent and
are never treated as experimental units; every count here is descriptive or a frozen screen.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

from .horizon import hellinger, safe_sqrt

_COMPONENT = "analysis.horizon_pools"
N_ANCHORS = 512
N_NEIGHBOURS = 5
Q1_MAX = 0.01
Q2_MIN = 0.05
MIN_ELIGIBLE = 128
MIN_FRACTION = 0.05
ANCHOR_SALT = "x4b-v1|anchor|"


def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail)


def select_anchors(canonical_ids: Sequence[str], n: int = N_ANCHORS,
                   salt: str = ANCHOR_SALT) -> NDArray[np.int64]:
    """Rows of the ``n`` ids with the smallest ``sha256(salt + id)`` (hex order), in that order.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if ids repeat or fewer than ``n`` exist.
    """
    ids = [str(x) for x in canonical_ids]
    if len(set(ids)) != len(ids) or len(ids) < n:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "anchor_ids", f"{len(ids)} ids, need {n} unique")
    keys = [hashlib.sha256((salt + h).encode("utf-8")).hexdigest() for h in ids]
    return np.array(sorted(range(len(ids)), key=lambda i: keys[i])[:n], dtype=np.int64)


@dataclass(frozen=True, eq=False)
class Partners:
    """Nearest-Q1 partners of each anchor: ``idx [A, k]`` (-1 = none), ``d1 [A, k]`` (NaN = none),
    ``group_size [A]`` candidates after exclusions, ``n_duplicate [A]`` identical-history rows
    excluded (besides the anchor's own row)."""

    idx: NDArray[np.int64]
    d1: NDArray[np.float64]
    group_size: NDArray[np.int64]
    n_duplicate: NDArray[np.int64]


def nearest_partners(Q1: NDArray, history_keys: Sequence[str], anchors: NDArray,
                     last_symbol: NDArray | None, canonical_ids: Sequence[str],
                     k: int = N_NEIGHBOURS) -> Partners:
    """``k`` nearest Hellinger-Q1 neighbours of each anchor inside one pool.

    Math
    ----
    Candidates of anchor ``a``: rows ``h != a`` whose history key (the canonical 32-symbol
    window) differs from ``a``'s and, if ``last_symbol`` is given, with the same last symbol.
    Sorted by ``(H(Q1_a, Q1_h), canonical_id_h)``; the first ``k`` are kept.

    Shapes
    ------
    ``Q1: [M, V]``; ``history_keys, canonical_ids: [M]``; ``anchors: [A]``; ``last_symbol: [M]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` on length mismatch.
    """
    q = np.asarray(Q1, dtype=np.float64)
    m = q.shape[0]
    if len(history_keys) != m or len(canonical_ids) != m or (
            last_symbol is not None and len(last_symbol) != m):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "pool_lengths", "per-history arrays differ")
    root = safe_sqrt(q)
    keys = np.asarray([str(x) for x in history_keys])
    order_id = np.argsort(np.asarray([str(x) for x in canonical_ids]), kind="stable")
    tie_rank = np.empty(m, dtype=np.int64)
    tie_rank[order_id] = np.arange(m)
    sym = None if last_symbol is None else np.asarray(last_symbol)
    A = len(anchors)
    idx, d1 = np.full((A, k), -1, dtype=np.int64), np.full((A, k), np.nan)
    sizes, dups = np.zeros(A, dtype=np.int64), np.zeros(A, dtype=np.int64)
    for row, a in enumerate(np.asarray(anchors, dtype=np.int64)):
        same = keys == keys[a]
        cand = ~same if sym is None else (~same & (sym == sym[a]))
        dups[row] = int(same.sum()) - 1
        c = np.flatnonzero(cand)
        sizes[row] = c.size
        if not c.size:
            continue
        dist = np.linalg.norm(root[c] - root[a], axis=1) / np.sqrt(2.0)
        pick = np.lexsort((tie_rank[c], dist))[:k]
        idx[row, :pick.size], d1[row, :pick.size] = c[pick], dist[pick]
    return Partners(idx, d1, sizes, dups)


@dataclass(frozen=True, eq=False)
class PoolScreen:
    """Frozen screen of one pool: per-anchor flags, partner Q2 distances and the pool status."""

    d2: NDArray[np.float64]
    admissible: NDArray[np.bool_]
    eligible: NDArray[np.bool_]
    witness: NDArray[np.bool_]
    n_eligible: int
    n_witness: int
    fraction: float | None
    status: str


def pair_d2(Q2: NDArray, anchors: NDArray, partners: Partners) -> NDArray[np.float64]:
    """``H(Q2_a, Q2_partner)`` for every anchor/partner slot (NaN where there is no partner)."""
    q2 = np.asarray(Q2, dtype=np.float64)
    out = np.full(partners.idx.shape, np.nan)
    have = partners.idx >= 0
    rows, cols = np.nonzero(have)
    a = np.asarray(anchors, dtype=np.int64)[rows]
    out[rows, cols] = hellinger(q2[a], q2[partners.idx[rows, cols]])
    return out


def screen_pool(d1: NDArray, d2: NDArray, q1_max: float = Q1_MAX, q2_min: float = Q2_MIN,
                min_eligible: int = MIN_ELIGIBLE, min_fraction: float = MIN_FRACTION) -> PoolScreen:
    """Apply the frozen screen: admissible ``d1 <= q1_max``; eligible = any admissible partner;
    witness = an admissible partner with ``d2 >= q2_min``. Status UNDERCOVERED if fewer than
    ``min_eligible`` eligible anchors, else WITNESS iff witnesses / eligible >= ``min_fraction``,
    else NO_MATERIAL_GAP."""
    d1a, d2a = np.asarray(d1, dtype=np.float64), np.asarray(d2, dtype=np.float64)
    admissible = np.nan_to_num(d1a, nan=np.inf) <= q1_max
    eligible = admissible.any(axis=1)
    witness = (admissible & (np.nan_to_num(d2a, nan=-np.inf) >= q2_min)).any(axis=1)
    n_el, n_wi = int(eligible.sum()), int(witness.sum())
    frac = n_wi / n_el if n_el else None
    if n_el < min_eligible:
        status = "UNDERCOVERED"
    else:
        status = "WITNESS" if frac is not None and frac >= min_fraction else "NO_MATERIAL_GAP"
    return PoolScreen(d2a, admissible, eligible, witness, n_el, n_wi, frac, status)


def practical_verdict(statuses: Mapping[str, str], test_pool: str = "test") -> tuple[str, str]:
    """``(GAP | NO_GAP | INCONCLUSIVE, reason)`` from pool statuses (test + dev pools).

    GAP iff test is WITNESS and >= 2 dev pools are WITNESS; NO_GAP iff test and >= 2 dev pools
    are NO_MATERIAL_GAP and no pool is WITNESS; otherwise INCONCLUSIVE.
    """
    if test_pool not in statuses:
        return "INCONCLUSIVE", "test pool missing"
    dev = [s for p, s in statuses.items() if p != test_pool]
    test = statuses[test_pool]
    if test == "WITNESS" and sum(s == "WITNESS" for s in dev) >= 2:
        return "GAP", "witness fraction met in test and in >= 2 dev pools"
    if (test == "NO_MATERIAL_GAP" and sum(s == "NO_MATERIAL_GAP" for s in dev) >= 2
            and "WITNESS" not in statuses.values()):
        return "NO_GAP", "covered pools show no material gap"
    if "UNDERCOVERED" in statuses.values() and "WITNESS" not in statuses.values():
        return "INCONCLUSIVE", "insufficient near-neighbour coverage"
    return "INCONCLUSIVE", "pools inconsistent or under-covered"


def strict_verdict(ambient: str) -> str:
    """SUFFICIENT_AMBIENT iff the ambient map factorizes; otherwise UNRESOLVED (numerical
    equality never proves an exact reachable witness)."""
    return "SUFFICIENT_AMBIENT" if ambient == "FACTORIZES" else "UNRESOLVED"


def overall_verdict(ambient: str, factor_conditioned: bool, practical: str,
                    checks_ok: bool) -> tuple[str, str]:
    """``(GO | NO-GO | INCONCLUSIVE, reason)`` per protocol x4b-v1 section 7."""
    if not checks_ok:
        return "INCONCLUSIVE", "a validity, precision, permutation or budget check failed"
    if ambient == "FACTORIZES":
        if factor_conditioned:
            return "NO-GO", "Q2 factorizes through Q1 on the simplex, practically conditioned"
        return "INCONCLUSIVE", "Q2 factorizes through Q1 but the inverse is ill-conditioned"
    if practical == "NO_GAP":
        return "NO-GO", "no material reachable gap in adequately covered pools (sample-scoped)"
    if ambient == "ALLOWS_STABLE" and practical == "GAP":
        return "GO", "practical near-Q1/distinct-Q2 accessibility (not strict insufficiency)"
    if ambient == "TOLERANCE_DEPENDENT":
        return "INCONCLUSIVE", "ambient rank conclusion depends on the tolerance"
    return "INCONCLUSIVE", f"practical screen {practical.lower()}"
