"""Independent tests (author B) for the v2.4 error_bound corrections: TEST_PLAN item B11, plus the
ERROR_BOUND.md v2.2 section 8 Taylor bounds and certify_rows "moment_check_max_by_K".

Written from API.md (spec v2.4), ERROR_BOUND.md v2.2, CONTRACT.json and TEST_PLAN.md only; no
production code was read. process_digest is recomputed here with hashlib from the written
formula; exact gaps are built from exact Decimals; Taylor bounds are exact Fractions.

Interpretation (stated, not verified against code): a `cache` argument is the dict documented
as load_cache's return value, {(process_digest, K, int64 row bytes): (Decimal, Decimal)}, filled
in place by a non-cache_only call.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import error_bound  # noqa: E402
import errors  # noqa: E402
import oracle_profile  # noqa: E402
import scores  # noqa: E402

pytestmark = pytest.mark.analysis

F = Fraction
T = np.array([[0.5, 0.5, 0.0], [0.25, 0.25, 0.5], [0.5, 0.0, 0.5]])    # pi = (3/7, 2/7, 2/7)
E = np.array([[0.5, 0.25, 0.25], [0.125, 0.625, 0.25], [0.25, 0.0, 0.75]])
PI = np.array([3 / 7, 2 / 7, 2 / 7])
COORDS = np.array([[0.0, 2.0], [3.0, 0.0], [7.0, 1.0]])
FEATS = oracle_profile.circle_features(COORDS)
# four DISTINCT valid histories (base-3 prefix), V = 3
HIST = np.array([[r // 3, r % 3] + [(r + t * t) % 3 for t in range(2, 32)] for r in range(4)],
                dtype=np.int64)
PHI = np.array([0.3, 2.5, 5.9, 6.2])
KS = (1, 4, 32)
E2 = E.copy()
E2[1] = [0.25, 0.5, 0.25]                    # process P2: one E row changed, still stochastic
E_BAD = np.array([[0.0, 0.5, 0.5]] * 3)      # every history containing token 0 is impossible


def _digest(T_, E_, pi_, coords_) -> str:
    """process_digest recomputed from the written formula (API.md v2.4 item 2)."""
    h = hashlib.sha256()
    for name, x in (("T", T_), ("E", E_), ("pi", pi_), ("coords", coords_)):
        a = np.ascontiguousarray(np.asarray(x, dtype=np.float64))
        h.update(f"{name}:{a.dtype.str}:{list(a.shape)}\n".encode())
        h.update(a.tobytes())
    return h.hexdigest()


def _row_bytes(row) -> bytes:
    return np.asarray(row, dtype=np.int64).tobytes()


def _check(E_, m_hat, hist=HIST, ks=KS, split="calibration", **kw) -> dict:
    return error_bound.reference_check_rows(T, E_, PI, COORDS, hist, m_hat, ks, split, **kw)


# ---- process_digest ----
def test_process_digest_matches_written_formula_and_binds_every_input() -> None:
    digest = error_bound.process_digest(T, E, PI, COORDS)
    assert isinstance(digest, str) and digest.lower() == _digest(T, E, PI, COORDS)
    # inputs are converted to float64 first: integer coords give the SAME digest
    assert error_bound.process_digest(T, E, PI, COORDS.astype(np.int64)) == digest
    seen = {digest}
    for name in ("T", "E", "pi", "coords"):
        arrays = {"T": T, "E": E, "pi": PI, "coords": COORDS}
        bumped = arrays[name].copy()
        bumped.flat[1] = np.nextafter(bumped.flat[1], np.inf)       # one ulp
        arrays[name] = bumped
        changed = error_bound.process_digest(arrays["T"], arrays["E"], arrays["pi"],
                                             arrays["coords"])
        assert changed.lower() == _digest(arrays["T"], arrays["E"], arrays["pi"],
                                          arrays["coords"])
        assert changed not in seen, name
        seen.add(changed)
    reshaped = error_bound.process_digest(T, E, PI, COORDS[:, :1])  # shape change
    assert reshaped not in seen


# ---- cache binding ----
def test_cache_filled_under_one_process_never_hits_under_another() -> None:
    m1 = scores.oracle_moments(T, E, PI, HIST, FEATS)
    m2 = scores.oracle_moments(T, E2, PI, HIST, FEATS)
    assert max(float(np.max(np.abs(m1[k] - m2[k]))) for k in KS) > 1e-3    # P1 != P2
    cache: dict = {}
    assert _check(E, m1, cache=cache)["status"] == "PASS"
    assert cache
    reused = _check(E2, m2, cache=cache)
    fresh = _check(E2, m2, cache={})
    assert reused["status"] == fresh["status"] == "PASS"
    assert reused["moment_check_max"] == fresh["moment_check_max"]
    assert _check(E2, m1, cache=cache)["status"] == "FAIL_TECHNICAL"     # no P1 hit under P2
    d1, d2 = _digest(T, E, PI, COORDS), _digest(T, E2, PI, COORDS)
    assert {str(key[0]).lower() for key in cache} == {d1, d2}
    rows = {_row_bytes(r) for r in HIST}
    for d in (d1, d2):     # distinct valid histories never share a key
        got = {(int(k[1]), bytes(k[2])) for k in cache if str(k[0]).lower() == d}
        assert got == set(itertools.product(KS, rows))


def test_cache_only_hits_a_filled_cache() -> None:
    m1 = scores.oracle_moments(T, E, PI, HIST, FEATS)
    cache: dict = {}
    first = _check(E, m1, cache=cache)
    again = _check(E, m1, cache=cache, cache_only=True)
    assert first["status"] == again["status"] == "PASS"
    assert first["moment_check_max"] == again["moment_check_max"]


def test_cache_only_miss_raises_before_any_reference() -> None:
    """With E_BAD the reference itself would fail (impossible suffix); the miss error shows that
    no reference computation was attempted."""
    assert (HIST == 0).any()
    m = scores.oracle_moments(T, E, PI, HIST, FEATS)            # finite, correctly shaped
    with pytest.raises(errors.Invalid, match="reference cache miss"):
        _check(E_BAD, m, cache={}, cache_only=True)
    x_hat = scores.scores(scores.unit_vectors(PHI), m[32], m[4])
    with pytest.raises(errors.Invalid, match="reference cache miss"):
        error_bound.certify_rows(T, E_BAD, PI, COORDS, HIST, PHI, x_hat, m[4], m[32],
                                 "calibration", cache={}, cache_only=True)


# ---- history validation before any conversion ----
E6 = np.array([[2, 1, 1, 2, 1, 1], [1, 2, 1, 1, 2, 1], [1, 1, 2, 1, 1, 2]]) / 8.0   # V = 6
HIST6 = np.array([[(r + 5 * t + t * t) % 6 for t in range(32)] for r in range(3)], np.int64)
HIST6[:, 10] = 4                     # 4 is valid for V = 6; 260 as uint8 would wrap to 4


def _malformed() -> dict[str, np.ndarray]:
    wrapped = HIST6.copy()
    wrapped[0, 10] = 260
    at_v, negative = HIST6.copy(), HIST6.copy()
    at_v[1, 3] = 6
    negative[2, 0] = -1
    return {"wrapped_260_int64": wrapped, "wrapped_260_uint16": wrapped.astype(np.uint16),
            "value_eq_V": at_v, "negative": negative, "float": HIST6.astype(np.float64),
            "bool": HIST6 > 2, "one_d": HIST6[0], "width_33": np.hstack([HIST6, HIST6[:, :1]])}


def test_valid_histories_pass_for_signed_and_unsigned_dtypes() -> None:
    m6 = scores.oracle_moments(T, E6, PI, HIST6, FEATS)
    signed = _check(E6, m6, hist=HIST6, split="validation")
    unsigned = _check(E6, m6, hist=HIST6.astype(np.uint8), split="validation")
    assert signed["status"] == unsigned["status"] == "PASS"
    assert signed["moment_check_max"] == unsigned["moment_check_max"]


@pytest.mark.parametrize("name", sorted(_malformed()))
def test_malformed_histories_invalid_before_any_reference_work(name: str) -> None:
    m6 = scores.oracle_moments(T, E6, PI, HIST6, FEATS)
    hist = _malformed()[name]
    for kw in ({}, {"cache": {}, "cache_only": True}):
        with pytest.raises(errors.Invalid) as exc:
            _check(E6, m6, hist=hist, split="validation", **kw)
        # validation precedes the cache lookup, hence any reference work
        assert "reference cache miss" not in str(exc.value), (name, kw)


# ---- exact moment gaps ----
def _gap_cache(mx_ref: Decimal) -> dict:
    key = (error_bound.process_digest(T, E, PI, COORDS), 4, _row_bytes(HIST[0]))
    return {key: (mx_ref, Decimal("0.25"))}


def test_exact_gap_boundary_at_one_over_ten_to_the_ten() -> None:
    m_hat = {4: np.array([[0.5, 0.25]])}                 # exact binary values
    at = Decimal("0.4999999999")                          # exact gap 1/10^10
    above = at - Decimal("1E-30")                         # exact gap 1/10^10 + 10^-30
    assert F(0.5) - F(at) == F(1, 10**10)
    assert F(0.5) - F(above) > F(1, 10**10)
    assert float(F(0.5) - F(above)) == 1e-10 == float(F(0.5) - F(at))    # floats cannot tell
    for ref, want in ((at, "PASS"), (above, "FAIL_TECHNICAL")):
        out = _check(E, m_hat, hist=HIST[:1], ks=(4,), cache=_gap_cache(ref), cache_only=True)
        assert out["status"] == want, ref


# ---- certify_rows by-K report ----
def test_certify_rows_reports_moment_check_by_k() -> None:
    m = scores.oracle_moments(T, E, PI, HIST, FEATS)
    x_hat = scores.scores(scores.unit_vectors(PHI), m[32], m[4])
    out = error_bound.certify_rows(T, E, PI, COORDS, HIST, PHI, x_hat, m[4], m[32], "calibration")
    assert out["status"] == "CERTIFIED"
    by_k = out["moment_check_max_by_K"]
    assert sorted(by_k) == [4, 32]
    assert out["moment_check_max"] == max(by_k.values()) <= 1e-12


# ---- ERROR_BOUND v2.2 section 8: separate exact even/odd series bounds ----
def test_taylor_series_bounds_each_parity_separately() -> None:
    x_max, n, a_bound = F(6284, 1000), 48, 270
    assert error_bound.TAYLOR_N == n
    for first in (0, 1):
        terms = [x_max ** (2 * k + first) / math.factorial(2 * k + first) for k in range(n + 32)]
        r = x_max ** 2 / ((2 * n + 3 + first) * (2 * n + 4 + first))
        assert r < 1
        assert sum(terms[:n + 1], F(0)) + terms[n + 1] / (1 - r) <= a_bound
        for k in range(n + 1, n + 31):        # every later ratio t_{k+1}/t_k is <= r
            assert terms[k + 1] / terms[k] <= r
        assert terms[n + 1] < F(1, 10**75)    # Leibniz remainder (first neglected term)
