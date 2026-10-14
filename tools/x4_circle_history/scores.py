"""Oracle targets, K4 scores and suffix-only controls (API.md scores.py).

Reuses the job-0014 pure oracle kernels UNCHANGED (tools/x4_oracle_profile/oracle_profile.py).
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "x4_oracle_profile"))

import oracle_profile  # noqa: E402
from errors import Invalid  # noqa: E402

TWO_PI = 2.0 * np.pi


def canonical_from_named(named, symbol_perm) -> np.ndarray:
    """canonical = argsort(perm)[named]; verifies perm[canonical] == named."""
    perm = np.asarray(symbol_perm)
    named = np.asarray(named)
    if (
        perm.ndim != 1
        or perm.dtype.kind not in "iu"
        or not np.array_equal(np.sort(perm), np.arange(perm.size))
    ):
        raise Invalid("symbol_perm is not an integer permutation of 0..V-1")
    if named.dtype.kind not in "iu" or (
        named.size and (named.min() < 0 or named.max() >= perm.size)
    ):
        raise Invalid("named tokens must be integers in 0..V-1")
    canonical = np.argsort(perm)[named.astype(np.int64)]
    if not np.array_equal(perm[canonical], named):
        raise Invalid("named/canonical round trip failed")
    return canonical.astype(np.int64)


def _require32(canonical32) -> np.ndarray:
    tok = np.asarray(canonical32)
    if tok.ndim != 2 or tok.shape[1] != 32:
        raise Invalid(f"canonical histories must be [n, 32] (w1..w32 only), got {tok.shape}")
    return tok


def history_digests(canonical32) -> list[str]:
    tok = _require32(canonical32)
    if tok.dtype.kind not in "iu" or (tok.size and (tok.min() < 0 or tok.max() > 255)):
        raise Invalid("tokens must be integers in 0..255")
    return [hashlib.sha256(row.astype(np.uint8).tobytes()).hexdigest() for row in tok]


def oracle_moments(T, E_canon, pi, canonical32, features) -> dict:
    """{1, 4, 32: [n, 2]} first-harmonic suffix means via the unchanged job-0014 kernel."""
    tok = _require32(canonical32)
    try:
        return oracle_profile.posterior_means(T, E_canon, pi, tok, (1, 4, 32), features)
    except oracle_profile.ProfileError as exc:
        raise Invalid(f"oracle kernel rejected input: {exc}") from exc


def unit_vectors(phi) -> np.ndarray:
    phi = np.asarray(phi, dtype=np.float64)
    if phi.ndim != 1 or not np.isfinite(phi).all():
        raise Invalid("phases must be finite 1-d")
    return np.column_stack((np.cos(phi), np.sin(phi)))


def _pair(a, b) -> tuple[np.ndarray, np.ndarray]:
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if (
        a.shape != b.shape
        or a.ndim != 2
        or a.shape[1] != 2
        or not (np.isfinite(a).all() and np.isfinite(b).all())
    ):
        raise Invalid("expected two finite [n, 2] arrays of equal shape")
    return a, b


def scores(u, m32, m4) -> np.ndarray:
    m32, m4 = _pair(m32, m4)
    u, _ = _pair(u, m32)
    return np.sum(u * (m32 - m4), axis=1)


def r4_norms(m32, m4) -> np.ndarray:
    m32, m4 = _pair(m32, m4)
    return np.sqrt(np.sum((m32 - m4) ** 2, axis=1))


def sha256_phase(last4_row) -> float:
    row = np.asarray(last4_row)
    if row.shape != (4,) or row.dtype.kind not in "iu" or row.min() < 0 or row.max() > 255:
        raise Invalid("last4 must be four integer tokens in 0..255")
    digest = hashlib.sha256(bytes(row.astype(np.uint8))).digest()[:8]
    return TWO_PI * int.from_bytes(digest, "big") / 2**64


def _finite_pairs(m) -> np.ndarray:
    m = np.asarray(m, dtype=np.float64)
    if m.ndim != 2 or m.shape[1] != 2 or not np.isfinite(m).all():
        raise Invalid("control means must be finite [n, 2]")
    return m


def _magnitude(m) -> np.ndarray:
    """Stable ||m||: scale by the largest absolute component first (no underflow to 0)."""
    scale = np.max(np.abs(m), axis=1)
    out = np.zeros(m.shape[0])
    nz = scale > 0
    scaled = m[nz] / scale[nz, None]
    out[nz] = scale[nz] * np.sqrt(np.sum(scaled * scaled, axis=1))
    return out


def _unit(m) -> np.ndarray:
    """m/||m|| by scale-first normalisation; EXACT (0, 0) -> (1, 0); no epsilon."""
    m = _finite_pairs(m)
    out = np.empty_like(m)
    scale = np.max(np.abs(m), axis=1)
    zero = scale == 0.0
    out[zero] = (1.0, 0.0)
    scaled = m[~zero] / scale[~zero, None]
    out[~zero] = scaled / np.sqrt(np.sum(scaled * scaled, axis=1))[:, None]
    return out


def control_vectors(m1, m4, canonical32) -> dict:
    tok = _require32(canonical32)
    phases = np.array([sha256_phase(row[28:32]) for row in tok])
    return {"m1_unit": _unit(m1), "m4_unit": _unit(m4), "sha256_last4": unit_vectors(phases)}


def angular_instability(m, bound) -> np.ndarray:
    """Diagnostic flag 0 < ||m|| <= bound (bound scalar or per row); never alters vectors."""
    m = _finite_pairs(m)
    bound = np.asarray(bound, dtype=np.float64)
    if not np.isfinite(bound).all() or np.any(bound < 0):
        raise Invalid("instability bound must be finite and nonnegative")
    norm = _magnitude(m)
    return (norm > 0.0) & (norm <= bound)


CONTROL_NAMES = ("m1_unit", "m4_unit", "sha256_last4")


def control_scores(m1, m4, m32, canonical32) -> dict:
    """{name: u_c . (m32 - m4)} for the three fixed suffix-only controls (spec v2.4 item 10)."""
    vectors = control_vectors(m1, m4, canonical32)
    return {name: scores(vectors[name], m32, m4) for name in CONTROL_NAMES}
