"""Integer cochains on the Vietoris-Rips 1- and 2-skeleton (API.md, cochain.py).

Conventions: edges (i, j) with i < j in lexicographic order; a 1-cochain is an int64 value on the
oriented edge i->j; triangles (i, j, k) with i < j < k; (D1 a)(i,j,k) = a(j,k) - a(i,k) + a(i,j);
vertex coboundary (delta f)(i,j) = f(j) - f(i).

Provenance: minimal extraction of the candidate functions triangle_system, check_lift, lift,
primitive and the smoothing step of the stopped history-feasibility core
(topo-pilot-x4-history-feas tools/x4_history_feas/core.py, frozen; statically inspected only after
the independent test authors received the written specification). Changes: split into the
API.md functions, explicit closure/congruence checks, injected guard/clock, no file I/O.
"""

from __future__ import annotations

import math
import time
import warnings
from collections import deque

import numpy as np
from errors import Invalid, Unresolved
from scipy.optimize import Bounds, LinearConstraint, OptimizeWarning, milp
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import lsqr


def edge_list(D, radius: float) -> np.ndarray:
    """All i < j with D[i, j] <= radius, lexicographic order; int64 [E, 2]."""
    D = np.asarray(D, dtype=np.float64)
    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise Invalid("distance matrix must be square")
    i, j = np.triu_indices(D.shape[0], 1)
    keep = D[i, j] <= radius
    return np.column_stack((i[keep], j[keep])).astype(np.int64)


def triangle_system(edges, n: int) -> tuple[csr_matrix, np.ndarray]:
    """D1 (int64 sparse [T, E]) and triangles (int64 [T, 3]) of the clique 2-skeleton."""
    edges = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    index = {(int(a), int(b)): k for k, (a, b) in enumerate(edges)}
    neigh: list[set[int]] = [set() for _ in range(n)]
    for a, b in edges:
        neigh[int(a)].add(int(b))
        neigh[int(b)].add(int(a))
    triangles, rows, cols, vals = [], [], [], []
    for i in range(n):
        for j in sorted(k for k in neigh[i] if k > i):
            for k in sorted(x for x in neigh[i] & neigh[j] if x > j):
                row = len(triangles)
                triangles.append((i, j, k))
                rows.extend((row, row, row))
                cols.extend((index[(j, k)], index[(i, k)], index[(i, j)]))
                vals.extend((1, -1, 1))
    D1 = coo_matrix(
        (np.asarray(vals, np.int64), (rows, cols)),
        shape=(len(triangles), len(edges)),
        dtype=np.int64,
    ).tocsr()
    return D1, np.asarray(triangles, dtype=np.int64).reshape(-1, 3)


def _edge_values(values, edges) -> dict:
    return {(int(a), int(b)): int(v) for (a, b), v in zip(np.asarray(edges), np.asarray(values))}


def check_closure(alpha, edges, triangles) -> None:
    """Invalid unless alpha(j,k) - alpha(i,k) + alpha(i,j) == 0 for every triangle."""
    d = _edge_values(alpha, edges)
    for i, j, k in np.asarray(triangles, dtype=np.int64).reshape(-1, 3):
        if d[(int(j), int(k))] - d[(int(i), int(k))] + d[(int(i), int(j))] != 0:
            raise Invalid(f"integer closure fails on triangle {(int(i), int(j), int(k))}")


def check_congruence(alpha, a, p: int) -> None:
    """Invalid unless alpha == a (mod p) on every edge."""
    for v, w in zip(np.asarray(alpha), np.asarray(a)):
        if (int(v) - int(w)) % p:
            raise Invalid("lift is not congruent to the cochain mod p")


HIGHS_PINNED = {"threads": 1, "parallel": False}


def _milp_correction(D1, b, bound, cfg, remaining_s):
    """One bounded zero-objective feasibility MILP; HiGHS pinned to one thread (fail closed)."""
    n_var = D1.shape[1]
    options = {
        "node_limit": cfg["lift_node_limit"],
        "mip_rel_gap": 0.0,
        "disp": False,
        "presolve": True,
        "time_limit": float(remaining_s),
        **HIGHS_PINNED,
    }
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = milp(
            np.zeros(n_var),
            integrality=np.ones(n_var),
            bounds=Bounds(-bound * np.ones(n_var), bound * np.ones(n_var)),
            constraints=LinearConstraint(D1, b, b),
            options=options,
        )
    rejected = [str(w.message) for w in caught if issubclass(w.category, OptimizeWarning)]
    if rejected:
        raise Invalid(f"HiGHS rejected a pinned option: {rejected}")
    record = {"bound": int(bound), "status": int(result.status)}
    if result.x is None:
        return None, record
    candidate = np.rint(result.x).astype(np.int64)
    if (
        np.max(np.abs(result.x - candidate)) > cfg["lift_rounding_tol"]
        or np.any(np.abs(candidate) > bound)
        or not np.array_equal(D1 @ candidate, b)
    ):
        return None, record
    return candidate, record


def _local_passes(z, edges, n, cfg, over_cap):
    edges = np.asarray(edges, dtype=np.int64)
    for _ in range(cfg["local_passes"]):
        for v in range(min(cfg["local_vertices"], n)):
            if over_cap():
                raise Unresolved("lift CPU cap reached during local improvement")
            d0 = (edges[:, 1] == v).astype(np.int64) - (edges[:, 0] == v).astype(np.int64)
            current = int(np.abs(z).sum())
            options = []
            for s in (-1, 1):
                trial = z + s * d0
                norm = int(np.abs(trial).sum())
                if norm < current:
                    options.append((norm, tuple(int(x) for x in trial), trial))
            if options:
                z = min(options, key=lambda item: (item[0], item[1]))[2]
    return z


def integer_lift(a, D1, edges, triangles, n, cfg, guard=None, clock=time.process_time):
    """Exact integer lift alpha = a - p z of a mod-p cocycle a (API.md integer_lift).

    The CPU timer starts at ENTRY (spec v2.4 item 5); every successful return is preceded,
    after its final exact checks, by the cap check, including the already-closed branch.
    """
    start = clock()
    cap = float(cfg["lift_cpu_cap_s"])

    def elapsed():
        return clock() - start

    def over_cap():
        return elapsed() >= cap

    p = int(cfg["field"])
    a = np.asarray(a, dtype=np.int64)
    defect = D1 @ a
    if np.any(defect % p):
        raise Invalid("not a cocycle mod p")
    if not np.any(defect):
        check_closure(a, edges, triangles)
        check_congruence(a, a, p)
        if over_cap():
            raise Unresolved("integer lift CPU cap exceeded before the certificate was accepted")
        return a.copy(), {
            "kind": "centered_exact",
            "solver_calls": 0,
            "calls": [],
            "l1_correction": 0,
        }
    b = defect // p
    z, calls = None, []
    for bound in cfg["lift_bounds"]:
        if guard is not None:
            guard()
        if over_cap():
            raise Unresolved("integer lift CPU cap reached before a solver call")
        remaining = min(cap - elapsed(), float(cfg.get("native_operation_wall_s", 180)))
        candidate, record = _milp_correction(D1, b, bound, cfg, remaining)
        calls.append(record)
        if over_cap():
            raise Unresolved("integer lift CPU cap exceeded during a native solver call")
        if candidate is not None:
            z = candidate
            break
    if z is None:
        raise Unresolved("no exact integer lift within the bounded search")
    z = _local_passes(z, edges, n, cfg, over_cap)
    if not np.array_equal(D1 @ z, b):
        raise Invalid("local improvement broke D1 z = b")
    alpha = a - p * z
    check_closure(alpha, edges, triangles)
    check_congruence(alpha, a, p)
    if over_cap():
        raise Unresolved("integer lift CPU cap exceeded before the certificate was accepted")
    return alpha, {
        "kind": "corrected_exact",
        "solver_calls": len(calls),
        "calls": calls,
        "l1_correction": int(np.abs(z).sum()),
        "correction": z,
    }


def primitive_class(alpha, edges, triangles, n, p):
    """Primitive integer class beta with alpha = g*beta + delta q (API.md primitive_class)."""
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for (i, j), v in zip(np.asarray(edges, dtype=np.int64), np.asarray(alpha, dtype=np.int64)):
        adjacency[int(i)].append((int(j), int(v)))
        adjacency[int(j)].append((int(i), -int(v)))
    q: list[int | None] = [None] * n
    q[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, v in sorted(adjacency[i]):
            if q[j] is None:
                q[j] = q[i] + v
                queue.append(j)
    if any(value is None for value in q):
        raise Unresolved("graph at the selected scale is disconnected")
    q_arr = np.asarray(q, dtype=np.int64)
    edges = np.asarray(edges, dtype=np.int64)
    dq = q_arr[edges[:, 1]] - q_arr[edges[:, 0]]
    periods = np.asarray(alpha, dtype=np.int64) - dq
    g = 0
    for value in periods:
        g = math.gcd(g, abs(int(value)))
    if g == 0 or g % p == 0:
        raise Unresolved("zero or p-divisible cycle period")
    beta = periods // g
    if not np.array_equal(g * beta + dq, np.asarray(alpha, dtype=np.int64)):
        raise Invalid("primitive compatibility g*beta + delta q != alpha")
    check_closure(beta, edges, triangles)
    return beta, q_arr, int(g)


def smooth_phase(beta, edges, n):
    """Least squares f (f[0] = 0) of ||beta + B f||; phi = 2 pi f mod 2 pi (API.md)."""
    edges = np.asarray(edges, dtype=np.int64)
    beta = np.asarray(beta, dtype=np.float64)
    rows = np.repeat(np.arange(len(edges)), 2)
    B = coo_matrix(
        (np.tile([-1.0, 1.0], len(edges)), (rows, edges.ravel())), shape=(len(edges), n)
    ).tocsr()
    f = np.r_[0.0, lsqr(B[:, 1:], -beta, atol=1e-12, btol=1e-12, iter_lim=10 * max(n, 1))[0]]
    residual = float(np.max(np.abs(B.T @ (beta + B @ f)))) / (1.0 + float(np.linalg.norm(beta)))
    if not np.isfinite(f).all() or not residual <= 1e-8:
        raise Invalid(f"smoothing residual {residual}")
    return (2.0 * np.pi * f) % (2.0 * np.pi), residual
