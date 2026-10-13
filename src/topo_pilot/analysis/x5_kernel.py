"""X5 G1 exact process diagnostics (x5g1-feas-v2 §3): rate, spectrum, mixing bound, integrated
autocorrelation of state functions, rate-matched diagnostic kernel. Reversible kernels only."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

_FLOOR = 1e-12


def movement_rate(T: NDArray, pi: NDArray) -> float:
    """``r = sum_z pi_z (1 - T_zz)``."""
    return float(np.sum(np.asarray(pi, float) * (1.0 - np.diag(np.asarray(T, float)))))


def is_connected(T: NDArray) -> bool:
    """Undirected connectivity of ``{i != j : T_ij > 0 or T_ji > 0}``."""
    A = np.asarray(T, float)
    adj = (A > 0) | (A.T > 0)
    np.fill_diagonal(adj, False)
    n = adj.shape[0]
    seen, stack = np.zeros(n, dtype=bool), [0]
    seen[0] = True
    while stack:
        i = stack.pop()
        for j in np.flatnonzero(adj[i] & ~seen):
            seen[j] = True
            stack.append(int(j))
    return bool(seen.all())


def _sym(T: NDArray, pi: NDArray) -> NDArray[np.float64]:
    r = np.sqrt(np.asarray(pi, float))
    S = r[:, None] * np.asarray(T, float) / r[None, :]
    return 0.5 * (S + S.T)


@dataclass(frozen=True, eq=False)
class SpectrumReport:
    """Descending eigenvalues, ``gap = 1 - lam2``, ``abs_gap = 1 - max(|lam2|, |lam_min|)``,
    ``t_rel``, integer ``mixing_bound`` and ``status`` (ok / REDUCIBLE / NEAR_UNIT_GAP)."""

    eigenvalues: NDArray[np.float64]
    gap: float
    abs_gap: float
    t_rel: float | None
    mixing_bound: int | None
    status: str


def spectrum_report(T: NDArray, pi: NDArray, eps: float = 0.25) -> SpectrumReport:
    """Spectrum of a pi-reversible kernel and the bound
    ``t_mix(eps) <= ceil(t_rel log(1 / (eps pi_min)))`` (irreducible, reversible, aperiodic)."""
    lam = np.sort(np.linalg.eigvalsh(_sym(T, pi)))[::-1]
    gap = float(1.0 - lam[1])
    abs_gap = float(1.0 - max(abs(lam[1]), abs(lam[-1])))
    if not is_connected(T):
        return SpectrumReport(lam, gap, abs_gap, None, None, "REDUCIBLE")
    if abs_gap <= _FLOOR:
        return SpectrumReport(lam, gap, abs_gap, None, None, "NEAR_UNIT_GAP")
    t_rel = 1.0 / abs_gap
    bound = math.ceil(t_rel * math.log(1.0 / (eps * float(np.min(pi)))))
    return SpectrumReport(lam, gap, abs_gap, t_rel, int(bound), "ok")


def integrated_autocorrelation(T: NDArray, pi: NDArray, g: NDArray) -> tuple[float | None, str]:
    """Exact integrated autocorrelation time of a state function under a reversible kernel.

    Math
    ----
    ``S = D^{1/2} T D^{-1/2}`` with eigenpairs ``(lam_k, phi_k)`` (descending, k = 1 top);
    ``w_k = (sum_z sqrt(pi_z) (g_z - E_pi g) phi_k(z))^2``;
    ``tau = sum_{k>=2} w_k (1 + lam_k)/(1 - lam_k) / sum_{k>=2} w_k``. ``g`` is a state function
    (e.g. a conditional emission probability), not an observed-token autocorrelation.
    """
    p = np.asarray(pi, float)
    gv = np.asarray(g, float)
    gc = gv - float(p @ gv)
    if float(p @ gc ** 2) <= _FLOOR:
        return None, "UNDEFINED_CONSTANT"
    lam, phi = np.linalg.eigh(_sym(T, pi))
    order = np.argsort(lam)[::-1]
    lam, phi = lam[order], phi[:, order]
    if np.any(lam[1:] >= 1.0 - _FLOOR):
        return None, "REDUCIBLE"
    w = (phi.T @ (np.sqrt(p) * gc)) ** 2
    w, lam = w[1:], lam[1:]
    return float(np.sum(w * (1.0 + lam) / (1.0 - lam)) / np.sum(w)), "ok"


def rate_matched_kernel(T: NDArray, alpha: float) -> tuple[NDArray[np.float64] | None, str]:
    """``I + alpha (T - I)``; ``INVALID_KERNEL`` if alpha <= 0, a negative entry, or a diagonal
    below the 0.2 lazy floor. A process diagnostic only."""
    A = np.asarray(T, float)
    if not alpha > 0:
        return None, "INVALID_KERNEL"
    Ta = np.eye(A.shape[0]) + alpha * (A - np.eye(A.shape[0]))
    if Ta.min() < 0 or np.diag(Ta).min() < 0.2 - _FLOOR:
        return None, "INVALID_KERNEL"
    return Ta, "ok"
