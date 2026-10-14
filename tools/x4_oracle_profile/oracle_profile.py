"""Pure kernels for the job-0014 circular-history oracle profile (contract: API.md).

Math (API.md section 1). Row conventions ``T[i, j] = P(z_next = j | z = i)``,
``E[i, w] = P(w | z = i)``, stationary ``pi``. For a history row ``w_1..w_L`` and suffix length
``K`` the suffix posterior is ``post_K = P(z_L | w_{L-K+1:L})`` with the window's first state drawn
from ``pi`` (restart at the suffix boundary): emit first, transition only between emissions, no
transition after the last emission. Circular mean ``m_K = post_K @ c`` with
``c[s] = (cos(2 pi x_s / 12), sin(2 pi x_s / 12))``. Residual ``r_K = m_32 - m_K``;
``B_K = mean ||r_K||``, ``V_K = mean ||r_K||^2``.

No I/O; randomness only through an injected ``np.random.Generator``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from numpy.typing import NDArray

PERIOD = 12


class ProfileError(RuntimeError):
    """Every validation failure of this module."""


def _finite_array(name: str, value, ndim: int) -> NDArray[np.float64]:
    try:
        arr = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ProfileError(f"{name}: not convertible to float64 ({exc})") from exc
    if arr.ndim != ndim or arr.size == 0:
        raise ProfileError(f"{name}: expected a non-empty {ndim}-d array, got shape {arr.shape}")
    if not np.isfinite(arr).all():
        raise ProfileError(f"{name}: non-finite entries")
    return arr


def circle_features(coords) -> NDArray[np.float64]:
    """``[S, 2]`` first-harmonic features of the first coordinate ``x = coords[:, 0]``.

    Raises ProfileError unless every ``x`` is finite, integer-valued and in ``0..11``.
    """
    try:
        arr = np.asarray(coords, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ProfileError(f"coords: not convertible ({exc})") from exc
    if arr.ndim != 2 or arr.shape[0] == 0 or arr.shape[1] < 1 or not np.isfinite(arr).all():
        raise ProfileError(f"coords: expected finite [S, >=1], got shape {arr.shape}")
    x = arr[:, 0]
    if np.any(x != np.round(x)) or x.min() < 0 or x.max() > PERIOD - 1:
        raise ProfileError("coords[:, 0] must be integers in 0..11")
    angle = 2.0 * np.pi * x / PERIOD
    return np.column_stack((np.cos(angle), np.sin(angle)))


def canonical_emission(E_named, symbol_perm) -> NDArray[np.float64]:
    """``E_canon = E_named[:, symbol_perm]`` (canonical symbol k is named symbol symbol_perm[k])."""
    E = _finite_array("E_named", E_named, 2)
    perm = np.asarray(symbol_perm)
    if perm.dtype.kind not in "iu" or perm.ndim != 1 or perm.shape[0] != E.shape[1]:
        raise ProfileError("symbol_perm must be a 1-d integer array of length V")
    if not np.array_equal(np.sort(perm), np.arange(E.shape[1])):
        raise ProfileError("symbol_perm is not a permutation of 0..V-1")
    return E[:, perm]


def validate_process(T, E, pi, tol: float = 1e-12) -> dict:
    """Check shapes, finiteness, nonnegativity, stochastic rows and stationarity of ``pi``.

    Returns the observed maxima; raises ProfileError when any exceeds ``tol``.
    """
    T = _finite_array("T", T, 2)
    E = _finite_array("E", E, 2)
    pi = _finite_array("pi", pi, 1)
    n_states = pi.shape[0]
    if T.shape != (n_states, n_states) or E.shape[0] != n_states:
        raise ProfileError(f"inconsistent shapes T{T.shape} E{E.shape} pi{pi.shape}")
    if T.min() < 0 or E.min() < 0 or pi.min() < 0:
        raise ProfileError("negative probability")
    found = {
        "T_row_sum_max_abs_err": float(np.max(np.abs(T.sum(axis=1) - 1.0))),
        "E_row_sum_max_abs_err": float(np.max(np.abs(E.sum(axis=1) - 1.0))),
        "pi_sum_abs_err": float(abs(pi.sum() - 1.0)),
        "stationarity_max_abs_err": float(np.max(np.abs(pi @ T - pi))),
    }
    bad = {key: value for key, value in found.items() if not value <= tol}
    if bad:
        raise ProfileError(f"process check failed (tol {tol}): {bad}")
    return found


def _model_arrays(T, E, pi) -> tuple:
    """Structural kernel invariants: finite, nonnegative, consistent shapes (stochasticity and
    stationarity are checked by ``validate_process`` at the runner boundary)."""
    T, E, pi = _finite_array("T", T, 2), _finite_array("E", E, 2), _finite_array("pi", pi, 1)
    n_states = pi.shape[0]
    if T.shape != (n_states, n_states) or E.shape[0] != n_states:
        raise ProfileError(f"inconsistent shapes T{T.shape} E{E.shape} pi{pi.shape}")
    if T.min() < 0 or E.min() < 0 or pi.min() < 0:
        raise ProfileError("negative probability")
    return T, E, pi


def _checked_tokens(tokens, n_symbols: int) -> NDArray[np.int64]:
    try:
        tok = np.asarray(tokens)
    except (TypeError, ValueError) as exc:
        raise ProfileError(f"tokens: not convertible ({exc})") from exc
    if tok.ndim != 2 or tok.shape[0] == 0 or tok.shape[1] == 0:
        raise ProfileError(f"tokens: expected non-empty [n, L], got shape {tok.shape}")
    if tok.dtype.kind not in "iu":
        raise ProfileError(f"tokens: integer dtype required, got {tok.dtype}")
    if tok.min() < 0 or tok.max() >= n_symbols:
        raise ProfileError("tokens: symbol outside 0..V-1")
    return tok.astype(np.int64)


def _checked_k(K, length: int) -> int:
    if isinstance(K, (bool, np.bool_)) or not isinstance(K, (int, np.integer)):
        raise ProfileError(f"K must be an integer, got {K!r}")
    if not 1 <= int(K) <= length:
        raise ProfileError(f"K={K} outside 1..{length}")
    return int(K)


def suffix_posterior(T, E, pi, tokens, K) -> NDArray[np.float64]:
    """``[n, S]`` normalised filtering posteriors ``P(z_L | w_{L-K+1:L})``, stationary restart.

    Recurrence (per row, normalising after every emission for stability):
    ``b <- pi * E[:, w_{L-K+1}]``; then for each later symbol ``b <- (b @ T) * E[:, w]``.
    Raises ProfileError for invalid tokens/K or a zero-probability suffix.
    """
    T, E, pi = _model_arrays(T, E, pi)
    tok = _checked_tokens(tokens, E.shape[1])
    k = _checked_k(K, tok.shape[1])
    suffix = tok[:, tok.shape[1] - k :]
    belief = np.broadcast_to(pi, (tok.shape[0], pi.shape[0])).copy()
    for step in range(k):
        if step:
            belief = belief @ T
        belief = belief * E[:, suffix[:, step]].T
        mass = belief.sum(axis=1, keepdims=True)
        if not np.all(np.isfinite(mass)):
            raise ProfileError("non-finite filtering mass")
        if not np.all(mass > 0):
            raise ProfileError("impossible history: zero-probability suffix")
        belief = belief / mass
    if not np.isfinite(belief).all() or np.max(np.abs(belief.sum(axis=1) - 1.0)) > 1e-12:
        raise ProfileError("posterior not finite/normalised")
    return belief


def posterior_means(T, E, pi, tokens, Ks: Sequence[int], features) -> dict[int, NDArray]:
    """``{K: suffix_posterior(...) @ features}``, each ``[n, 2]``."""
    feats = _finite_array("features", features, 2)
    if feats.shape[1] != 2 or feats.shape[0] != np.shape(pi)[0] or len(Ks) == 0:
        raise ProfileError(f"features must be [S, 2] and Ks non-empty; got {feats.shape}, {Ks}")
    return {int(K): suffix_posterior(T, E, pi, tokens, K) @ feats for K in Ks}


def residual_rows(means: Mapping[int, NDArray], full: int = 32) -> dict:
    """Per-row ``r_K = m_full - m_K``, ``||r_K||`` and ``||r_K||^2`` for every K in ``means``."""
    if full not in means:
        raise ProfileError(f"full K={full} missing")
    reference = _finite_array(f"means[{full}]", means[full], 2)
    if reference.shape[1] != 2:
        raise ProfileError(f"means[{full}] must be [n, 2], got {reference.shape}")
    out: dict = {"r": {}, "norm": {}, "sq": {}}
    for K, value in means.items():
        arr = _finite_array(f"means[{K}]", value, 2)
        if arr.shape != reference.shape:
            raise ProfileError(f"means[{K}] shape {arr.shape} != {reference.shape}")
        r = reference - arr
        out["r"][K] = r
        out["norm"][K] = np.sqrt(np.sum(r * r, axis=1))
        out["sq"][K] = np.sum(r * r, axis=1)
    return out


def profile_point(norm: Mapping[int, NDArray], sq: Mapping[int, NDArray]) -> dict:
    """``{"B": {K: mean norm}, "V": {K: mean sq}}`` as Python floats."""
    if not norm or set(norm) != set(sq):
        raise ProfileError("norm/sq must be non-empty with identical K keys")
    b = {K: _finite_array(f"norm[{K}]", v, 1) for K, v in norm.items()}
    v = {K: _finite_array(f"sq[{K}]", x, 1) for K, x in sq.items()}
    return {
        "B": {K: float(np.mean(x)) for K, x in b.items()},
        "V": {K: float(np.mean(x)) for K, x in v.items()},
    }


def bootstrap_profile(norm, sq, Ks: Sequence[int], rng: np.random.Generator, draws: int) -> dict:
    """Whole-row bootstrap; one ``rng.integers(0, n, size=n)`` per draw shared by all K, B and V."""
    if isinstance(draws, bool) or not isinstance(draws, (int, np.integer)) or draws < 1:
        raise ProfileError("draws must be an integer >= 1")
    if len(Ks) == 0:
        raise ProfileError("Ks must be non-empty")
    try:
        norms = [_finite_array(f"norm[{K}]", norm[K], 1) for K in Ks]
        sqs = [_finite_array(f"sq[{K}]", sq[K], 1) for K in Ks]
    except KeyError as exc:
        raise ProfileError(f"missing K {exc}") from exc
    n = norms[0].shape[0]
    if n < 2 or any(a.shape != (n,) for a in norms + sqs):
        raise ProfileError("bootstrap needs equal-length 1-d rows, n >= 2")
    B = np.empty((draws, len(Ks)))
    V = np.empty((draws, len(Ks)))
    for d in range(draws):
        idx = rng.integers(0, n, size=n)
        for k in range(len(Ks)):
            B[d, k] = np.mean(norms[k][idx])
            V[d, k] = np.mean(sqs[k][idx])
    return {"B": B, "V": V}


def percentile_interval(samples, probs: Sequence[float]) -> NDArray[np.float64]:
    """``np.quantile(samples, probs, axis=0, method="inverted_cdf")``."""
    arr = _finite_array("samples", samples, np.ndim(samples) or 1)
    p = np.asarray(probs, dtype=np.float64)
    if p.size == 0 or not np.isfinite(p).all() or p.min() < 0 or p.max() > 1:
        raise ProfileError("probs must be non-empty values in [0, 1]")
    return np.quantile(arr, probs, axis=0, method="inverted_cdf")
