"""Independent tests (author B) for scores.py: TEST_PLAN items B1-B4 and B8 (spec v2.2).

Written from tools/x4_circle_history/API.md (v2.2), CONTRACT.json and TEST_PLAN.md only; no
production code was read. Expected values are computed here: exact Fractions (stationary pi,
forward filter, zero identity), hashlib digests, and numpy/math references.
Precision tests (B5, B9) live in test_scores_precision_gates.py (split for the 400-line limit).
"""

from __future__ import annotations

import hashlib
import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import errors  # noqa: E402
import independent_reference  # noqa: E402
import oracle_profile  # noqa: E402
import scores  # noqa: E402

pytestmark = pytest.mark.analysis

F = Fraction
S, V = 3, 3
# Tiny asymmetric HMM with dyadic entries (exact as floats) and one impossible emission.
T_EXACT = [[F(1, 2), F(1, 2), F(0)], [F(1, 4), F(1, 4), F(1, 2)], [F(1, 2), F(0), F(1, 2)]]
E_EXACT = [[F(1, 2), F(1, 4), F(1, 4)], [F(1, 8), F(5, 8), F(1, 4)], [F(1, 4), F(0), F(3, 4)]]


def _stationary(trans: list[list[Fraction]]) -> list[Fraction]:
    """Exact stationary law: pi (T - I) = 0 and sum(pi) = 1, Gauss-Jordan in Fractions."""
    n = len(trans)
    rows = [[trans[i][j] - (1 if i == j else 0) for i in range(n)] + [F(0)] for j in range(n - 1)]
    rows.append([F(1)] * n + [F(1)])
    for col in range(n):
        piv = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        pivot = rows[col][col]
        rows[col] = [v / pivot for v in rows[col]]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return [rows[r][n] for r in range(n)]


PI_EXACT = _stationary(T_EXACT)
T = np.array([[float(v) for v in row] for row in T_EXACT])
E = np.array([[float(v) for v in row] for row in E_EXACT])
PI = np.array([float(v) for v in PI_EXACT])
COORDS = np.array([[0.0, 1.0], [3.0, 0.0], [7.0, 2.0]])


def _rows(n: int, width: int = 32) -> np.ndarray:
    """Deterministic canonical histories (every token sequence is possible under the HMM)."""
    return np.array([[(r + t * (r + 1) + (t * t) // 3) % V for t in range(width)]
                     for r in range(n)], dtype=np.int64)


def test_fixture_hmm_is_exactly_stationary_and_asymmetric() -> None:
    assert PI_EXACT == [F(3, 7), F(2, 7), F(2, 7)]
    assert [sum(PI_EXACT[i] * T_EXACT[i][j] for i in range(S)) for j in range(S)] == PI_EXACT
    assert all(sum(row) == 1 for row in T_EXACT + E_EXACT)
    assert T_EXACT != [list(col) for col in zip(*T_EXACT)]


# ---- B1: canonical_from_named, history_digests -------------------------------------------
def test_canonical_from_named_inverse_permutation() -> None:
    perm = np.array([2, 0, 3, 1])           # argsort(perm) = [1, 3, 0, 2] (hand-derived)
    named = np.array([[0, 1, 2, 3], [3, 3, 0, 1]])
    canonical = scores.canonical_from_named(named, perm)
    assert canonical.dtype == np.int64
    assert canonical.tolist() == [[1, 3, 0, 2], [2, 2, 1, 3]]
    assert np.array_equal(perm[canonical], named)


def test_canonical_from_named_round_trips_contract_formula() -> None:
    rng = np.random.Generator(np.random.PCG64(20160))
    perm = rng.permutation(7)
    canonical = rng.integers(0, 7, size=(5, 32))
    named = perm[canonical]                 # CONTRACT: named = symbol_perm[canonical]
    assert np.array_equal(scores.canonical_from_named(named, perm), canonical)


@pytest.mark.parametrize("perm", [[0, 0, 1, 2], [0, 1, 2, 4], [-1, 0, 1, 2], [1, 2, 3, 4]])
def test_canonical_from_named_rejects_non_permutations(perm: list[int]) -> None:
    # [0, 1, 2, 4] passes the round trip for named [0, 1]: only the permutation check catches it.
    with pytest.raises(errors.Invalid):
        scores.canonical_from_named(np.array([[0, 1]]), np.array(perm))


def test_canonical_from_named_round_trip_check_catches_negative_named() -> None:
    # inverse[-1] wraps to a valid index, so only perm[canonical] == named can detect it.
    with pytest.raises(errors.Invalid):
        scores.canonical_from_named(np.array([[0, -1]]), np.array([2, 0, 3, 1]))


def test_history_digests_known_values_and_shape() -> None:
    rows = np.array([list(range(32)), [5] * 32, [(7 * t) % 3 for t in range(32)]], np.int64)
    expected = [hashlib.sha256(bytes(int(v) for v in row)).hexdigest() for row in rows]
    assert list(scores.history_digests(rows)) == expected
    assert list(scores.history_digests(rows.astype(np.uint8))) == expected
    assert len(set(expected)) == 3
    # Interpretation: a wrong shape is an integrity defect -> errors.Invalid.
    for bad in (np.zeros((2, 33), np.int64), np.zeros((2, 31), np.int64), np.zeros(32, np.int64)):
        with pytest.raises(errors.Invalid):
            scores.history_digests(bad)


# ---- B2: oracle_moments --------------------------------------------------------------------
def test_oracle_moments_equals_posterior_means_and_decimal_reference() -> None:
    feats = oracle_profile.circle_features(COORDS)
    hist = _rows(4)
    got = scores.oracle_moments(T, E, PI, hist, feats)
    want = oracle_profile.posterior_means(T, E, PI, hist, (1, 4, 32), feats)
    assert sorted(got) == [1, 4, 32]
    for k in (1, 4, 32):
        assert got[k].shape == (4, 2)
        np.testing.assert_allclose(got[k], want[k], rtol=0, atol=1e-15)
        for r in range(hist.shape[0]):     # restart-at-pi suffix posterior of the LAST k tokens
            post = independent_reference.decimal_suffix_posterior(T, E, PI, hist[r, 32 - k:])
            ref = [sum(float(p) * feats[s, j] for s, p in enumerate(post)) for j in (0, 1)]
            np.testing.assert_allclose(got[k][r], ref, rtol=0, atol=1e-12)


@pytest.mark.parametrize("width", [33, 31])
def test_oracle_moments_rejects_any_width_but_32(width: int) -> None:
    feats = oracle_profile.circle_features(COORDS)
    with pytest.raises(errors.Invalid):
        scores.oracle_moments(T, E, PI, _rows(2, width), feats)


# ---- B3: suffix-only zero identity (exhaustive, exact) -------------------------------------
L_ENUM = 5
COORDS_RATIONAL = np.array([[0.0, 0.0], [3.0, 0.0], [6.0, 0.0]])
FEAT_EXACT = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0))]   # (cos, sin)(2 pi x / 12), x = 0, 3, 6
CONTROLS = ("m1_unit", "m4_unit", "sha256_last4")


def _forward(word: tuple[int, ...]) -> list[Fraction]:
    """Exact unnormalised forward vector of a window started at pi (emit first)."""
    alpha = [PI_EXACT[i] * E_EXACT[i][word[0]] for i in range(S)]
    for sym in word[1:]:
        alpha = [sum(alpha[i] * T_EXACT[i][j] for i in range(S)) * E_EXACT[j][sym]
                 for j in range(S)]
    return alpha


def _posterior(word: tuple[int, ...]) -> tuple[list[Fraction], Fraction]:
    alpha = _forward(word)
    total = sum(alpha, F(0))
    return [a / total for a in alpha], total


def _moment(post: list[Fraction]) -> tuple[Fraction, Fraction]:
    return tuple(sum((p * c[j] for p, c in zip(post, FEAT_EXACT)), F(0)) for j in (0, 1))


@pytest.fixture(scope="module")
def exact_enum():
    words = list(itertools.product(range(V), repeat=L_ENUM))
    table = {w: _posterior(w) for w in words}
    return words, {w: table[w][1] for w in words}, {w: table[w][0] for w in words}


@pytest.fixture(scope="module")
def float_enum():
    words = list(itertools.product(range(V), repeat=L_ENUM))
    tokens = np.array(words, dtype=np.int64)
    feats = oracle_profile.circle_features(COORDS_RATIONAL)
    means = oracle_profile.posterior_means(T, E, PI, tokens, (1, 4, L_ENUM), feats)
    padded = np.zeros((len(words), 32), dtype=np.int64)
    padded[:, 32 - L_ENUM:] = tokens          # columns 28:32 are exactly the last 4 tokens
    return words, means, scores.control_vectors(means[1], means[4], padded)


def _expect_score(enum, k: int, g) -> Fraction:
    """Exact E[g(suffix_k) . (m_L - m_k)] over every history of length L_ENUM."""
    words, prob, post = enum
    m_k = {s: _moment(_posterior(s)[0]) for s in itertools.product(range(V), repeat=k)}
    total = F(0)
    for w in words:
        s = w[L_ENUM - k:]
        m_full, (gx, gy) = _moment(post[w]), g(s)
        total += prob[w] * (gx * (m_full[0] - m_k[s][0]) + gy * (m_full[1] - m_k[s][1]))
    return total


@pytest.mark.parametrize("k", [2, 4])
def test_zero_identity_exact_per_suffix(exact_enum, k: int) -> None:
    """sum_prefix P(prefix + s) (P_L - P_k(s)) == 0 for every suffix s: by linearity this is the
    identity for EVERY suffix function g and every feature map."""
    words, prob, post = exact_enum
    assert sum(prob.values(), F(0)) == 1
    for suffix in itertools.product(range(V), repeat=k):
        post_k = _posterior(suffix)[0]
        acc = [F(0)] * S
        for prefix in itertools.product(range(V), repeat=L_ENUM - k):
            w = prefix + suffix
            acc = [a + prob[w] * (pf - pk) for a, pf, pk in zip(acc, post[w], post_k)]
        assert acc == [0, 0, 0]
    gap = sum((prob[w] * sum((pf - pk) ** 2 for pf, pk in zip(post[w],
                                                              _posterior(w[L_ENUM - k:])[0]))
               for w in words), F(0))
    assert gap > 0                            # m_L really differs from m_k: not a vacuous zero


@pytest.mark.parametrize("k", [2, 4])
def test_zero_identity_exact_for_rational_suffix_functions(exact_enum, k: int) -> None:
    def g(s):
        return F(1 + (3 * sum(s)) % 5, 7), F(-(2 + s[-1]), 3)

    def h(s):
        return (F(1), F(0)) if s[0] == s[-1] else (F(0), F(-5, 2))

    assert _expect_score(exact_enum, k, g) == 0
    assert _expect_score(exact_enum, k, h) == 0


@pytest.mark.parametrize("name", CONTROLS)
def test_zero_identity_exact_for_the_three_controls(exact_enum, float_enum, name: str) -> None:
    words, _, ctrl = float_enum
    table: dict[tuple[int, ...], tuple[Fraction, Fraction]] = {}
    for i, w in enumerate(words):   # exact suffix function by construction: first row per suffix
        table.setdefault(w[L_ENUM - 4:], (F(float(ctrl[name][i, 0])), F(float(ctrl[name][i, 1]))))
    assert len(table) == V ** 4
    assert _expect_score(exact_enum, 4, table.__getitem__) == 0


@pytest.mark.parametrize("name", CONTROLS)
def test_zero_identity_float_controls_within_1e12(exact_enum, float_enum, name: str) -> None:
    words, means, ctrl = float_enum
    prob = exact_enum[1]
    x = scores.scores(ctrl[name], means[L_ENUM], means[4])
    weights = np.array([float(prob[w]) for w in words])
    assert x.shape == (len(words),)
    assert np.max(np.abs(x)) > 1e-6
    assert abs(float(np.dot(weights, x))) <= 1e-12


# ---- B4: unit vectors, scores, controls, sha256 phase, angular instability -----------------
def test_unit_vectors_scores_and_r4_norms_known_answers() -> None:
    phi = np.array([0.0, np.pi / 2, 1.0, 5.5])
    u = scores.unit_vectors(phi)
    np.testing.assert_array_equal(u, np.column_stack((np.cos(phi), np.sin(phi))))
    assert u[0].tolist() == [1.0, 0.0]
    m32 = np.array([[3.5, 4.25], [1.0, -1.0]])
    m4 = np.array([[0.5, 0.25], [1.0, -1.0]])
    np.testing.assert_array_equal(scores.r4_norms(m32, m4), [5.0, 0.0])
    np.testing.assert_array_equal(scores.scores(np.array([[0.5, 0.25], [1.0, 0.0]]), m32, m4),
                                  [2.5, 0.0])


def _hand_phase(last4: np.ndarray) -> float:
    digest = hashlib.sha256(bytes(int(v) for v in last4)).digest()
    return 2 * math.pi * int.from_bytes(digest[:8], "big") / 2**64


def test_sha256_phase_hand_derived_from_hashlib() -> None:
    for row in ([0, 1, 2, 3], [2, 2, 2, 2], [1, 0, 1, 0]):
        got = scores.sha256_phase(np.array(row, dtype=np.int64))
        assert 0.0 <= got < 2 * math.pi
        assert abs(got - _hand_phase(np.array(row))) <= 4e-15


def test_control_vectors_zero_maps_to_unit_x_and_others_unit_norm() -> None:
    m1 = np.array([[0.0, 0.0], [3.0, -4.0], [1e-3, 2e-3]])
    m4 = np.array([[0.25, -0.5], [0.0, 0.0], [-7.0, 0.0]])
    last4 = np.array([[0, 1, 2, 3], [2, 2, 2, 2], [1, 0, 1, 0]])
    hist = np.zeros((3, 32), np.int64)
    hist[:, 28:] = last4
    other = hist.copy()
    other[:, :28] = 2                          # different prefix, same last 4 tokens
    out = scores.control_vectors(m1, m4, hist)
    assert out["m1_unit"][0].tolist() == [1.0, 0.0]
    assert out["m4_unit"][1].tolist() == [1.0, 0.0]
    assert out["m4_unit"][2].tolist() == [-1.0, 0.0]
    for name, m in (("m1_unit", m1), ("m4_unit", m4)):
        for r in range(3):
            if m[r, 0] == 0.0 and m[r, 1] == 0.0:
                continue
            np.testing.assert_allclose(out[name][r], m[r] / math.hypot(*m[r]), rtol=0, atol=1e-15)
            assert abs(math.hypot(*out[name][r]) - 1.0) <= 1e-15
    for r in range(3):
        phase = _hand_phase(last4[r])
        np.testing.assert_allclose(out["sha256_last4"][r], [math.cos(phase), math.sin(phase)],
                                   rtol=0, atol=1e-14)
    np.testing.assert_array_equal(scores.control_vectors(m1, m4, other)["sha256_last4"],
                                  out["sha256_last4"])


def test_angular_instability_boundaries() -> None:
    m = np.array([[0.0, 0.0], [3.0, 4.0], [0.0, -5.0], [-3.0, 4.0], [1e-3, 0.0]])
    # magnitudes 0, 5, 5, 5, 1e-3: all exact under the scale-first norm (4 * 1.25 = 5).
    assert np.asarray(scores.angular_instability(m, 5.0)).tolist() == [False] + [True] * 4
    below = math.nextafter(5.0, 0.0)
    assert np.asarray(scores.angular_instability(m, below)).tolist() == [False] * 4 + [True]
    assert np.asarray(scores.angular_instability(m, 1e-4)).tolist() == [False] * 5


# ---- B8 (spec v2.2): scale-first normalisation on tiny and subnormal vectors -----------------
def test_control_vectors_tiny_and_subnormal_vectors() -> None:
    tiny = 5e-324                              # smallest positive subnormal binary64
    m1 = np.array([[tiny, 0.0], [-tiny, tiny], [1e-300, -3e-300], [0.0, 0.0], [0.0, -tiny]])
    m4 = m1[::-1].copy()
    out = scores.control_vectors(m1, m4, np.zeros((5, 32), np.int64))
    h = math.sqrt(0.5)
    want = np.array([[1.0, 0.0], [-h, h], [1 / math.sqrt(10), -3 / math.sqrt(10)],
                     [1.0, 0.0], [0.0, -1.0]])
    for name, rows in (("m1_unit", want), ("m4_unit", want[::-1])):
        got = np.asarray(out[name])
        assert np.all(np.isfinite(got))
        np.testing.assert_allclose(got, rows, rtol=0, atol=1e-15)
    assert np.asarray(out["m1_unit"])[0].tolist() == [1.0, 0.0]
    assert np.asarray(out["m1_unit"])[3].tolist() == [1.0, 0.0]


def test_angular_instability_uses_stable_magnitude_for_subnormals() -> None:
    tiny = 5e-324
    m = np.array([[tiny, 0.0], [-tiny, tiny], [1e-200, 1e-200], [0.0, 0.0]])
    # a naive sqrt(x^2 + y^2) underflows to 0 here and would report False
    assert np.asarray(scores.angular_instability(m, 1e-150)).tolist() == [True] * 3 + [False]


@pytest.mark.parametrize("bad_m", [[[np.nan, 0.0]], [[0.0, np.inf]], [[-np.inf, 1.0]]])
def test_angular_instability_rejects_nonfinite_input(bad_m) -> None:
    with pytest.raises(errors.Invalid):
        scores.angular_instability(np.array(bad_m), 1.0)


@pytest.mark.parametrize("bound", [-1.0, -1e-300, np.nan, np.inf])
def test_angular_instability_rejects_bad_bound(bound: float) -> None:
    with pytest.raises(errors.Invalid):
        scores.angular_instability(np.array([[1.0, 0.0]]), bound)
