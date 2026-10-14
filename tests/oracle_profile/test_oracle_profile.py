"""Independent tests of x4_oracle_profile suffix posteriors (job 0014, API.md section 4).

This file: the asymmetric test HMM with an exactly derived stationary pi, items 1 (exhaustive
agreement with path enumeration), 5 (normalisation) and 12 (decimal reference self-checks), plus
hand-computed known answers and ``posterior_means``. Items 2, 3, 4 and 6 are in
``test_oracle_profile_traps.py``; items 7 to 11 in ``test_oracle_profile_kernels.py``.

Written from ``tools/x4_oracle_profile/API.md`` only: the production module is imported, never read.
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.oracle

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "x4_oracle_profile"), ("tests", "oracle_profile")):
    _path = str(REPO_ROOT.joinpath(*_parts))
    if _path not in sys.path:
        sys.path.insert(0, _path)

import independent_reference as ref  # noqa: E402
import oracle_profile as op  # noqa: E402

Q = Fraction
# Non-symmetric, irreducible, aperiodic (T[0, 0] > 0) and NOT doubly stochastic
# (column sums 41/30, 7/6, 7/15), so pi is non-uniform and T != T.T.
T_Q = [[Q(1, 2), Q(1, 3), Q(1, 6)], [Q(1, 5), Q(1, 2), Q(3, 10)], [Q(2, 3), Q(1, 3), Q(0)]]
# Symbol 2 is emitted only by state 2 and T[2, 2] = 0, so a string is impossible exactly when it
# contains two consecutive 2s; symbol 1 is impossible from state 2, symbol 2 from states 0 and 1.
E_Q = [[Q(2, 3), Q(1, 3), Q(0)], [Q(1, 4), Q(3, 4), Q(0)], [Q(1, 5), Q(0), Q(4, 5)]]
S, V, L_MAX = 3, 3, 4
COORDS = np.array([[0, 5], [4, 1], [7, 2]], dtype=np.int64)  # x_s = 0, 4, 7
TOL_PROD = 1e-12


def exact_stationary(T: list[list[Fraction]]) -> list[Fraction]:
    """Solve pi T = pi, sum(pi) = 1 exactly by Gauss-Jordan elimination over Fractions.

    Equation j < n-1: sum_i pi_i (T[i][j] - [i == j]) = 0; last equation: sum_i pi_i = 1.
    """
    n = len(T)
    A = [[T[i][j] - (1 if i == j else 0) for i in range(n)] for j in range(n - 1)]
    A.append([Q(1)] * n)
    b = [Q(0)] * (n - 1) + [Q(1)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv], b[col], b[piv] = A[piv], A[col], b[piv], b[col]
        for r in range(n):
            if r != col and A[r][col] != 0:
                factor = A[r][col] / A[col][col]
                A[r] = [x - factor * y for x, y in zip(A[r], A[col])]
                b[r] -= factor * b[col]
    return [b[i] / A[i][i] for i in range(n)]


PI_Q = exact_stationary(T_Q)
T_F = np.array([[float(x) for x in row] for row in T_Q], dtype=np.float64)
E_F = np.array([[float(x) for x in row] for row in E_Q], dtype=np.float64)
PI_F = np.array([float(x) for x in PI_Q], dtype=np.float64)


def strings(length: int) -> list[tuple[int, ...]]:
    """All V**length observation strings."""
    return list(itertools.product(range(V), repeat=length))


def has_double_two(s: tuple[int, ...]) -> bool:
    return any(a == 2 and b == 2 for a, b in zip(s, s[1:]))


@lru_cache(maxsize=None)
def exact(suffix: tuple[int, ...]) -> tuple[Fraction, ...] | None:
    """Exact posterior of the float model (inputs converted exactly); None when impossible."""
    try:
        return tuple(ref.enumerate_posterior(T_F, E_F, PI_F, list(suffix)))
    except ValueError:
        return None


def gap(values, fracs) -> float:
    """max_s |values[s] - fracs[s]| computed exactly, returned as float."""
    return float(max(abs(Q(float(a)) - Q(f)) for a, f in zip(values, fracs)))


def production(rows, K):
    return op.suffix_posterior(T_F, E_F, PI_F, np.array(rows, dtype=np.int64), K)


def indep_features(coords) -> np.ndarray:
    x = np.asarray(coords, dtype=np.float64)[:, 0]
    return np.column_stack([np.cos(2 * np.pi * x / 12), np.sin(2 * np.pi * x / 12)])


def test_hmm_is_asymmetric_with_exact_nonuniform_stationary_pi():
    assert PI_Q == [Q(72, 175), Q(70, 175), Q(33, 175)]
    for j in range(S):
        assert sum(PI_Q[i] * T_Q[i][j] for i in range(S)) == PI_Q[j]
    assert all(sum(row) == 1 for row in T_Q) and all(sum(row) == 1 for row in E_Q)
    assert any(T_Q[i][j] != T_Q[j][i] for i in range(S) for j in range(S))
    assert any(sum(T_Q[i][j] for i in range(S)) != 1 for j in range(S))
    assert len(set(PI_Q)) == S
    assert any(x == 0 for row in E_Q for x in row)
    op.validate_process(T_F, E_F, PI_F)


def test_impossible_strings_are_exactly_those_with_two_consecutive_twos():
    n_impossible = 0
    for length in range(1, L_MAX + 1):
        for s in strings(length):
            assert (exact(s) is None) == has_double_two(s)
            n_impossible += exact(s) is None
    assert n_impossible > 0


def test_production_matches_exhaustive_enumeration():
    """Item 1: every string of length L <= 4 and every K in 1..L; impossible suffixes raise."""
    n_checked = n_impossible = 0
    for length in range(1, L_MAX + 1):
        rows = strings(length)
        for K in range(1, length + 1):
            ok = [r for r in rows if exact(r[length - K:]) is not None]
            bad = [r for r in rows if exact(r[length - K:]) is None]
            got = production(ok, K)
            assert got.shape == (len(ok), S) and got.dtype == np.float64
            for r, row in zip(ok, got):
                assert gap(row, exact(r[length - K:])) <= TOL_PROD, (r, K)
            for r in bad:
                with pytest.raises(op.ProfileError):
                    production([r], K)
            n_checked += len(ok)
            n_impossible += len(bad)
    assert n_checked > 300 and n_impossible > 0


def test_rows_are_normalised_and_nonnegative():
    """Item 5."""
    for length in range(1, L_MAX + 1):
        for K in range(1, length + 1):
            ok = [r for r in strings(length) if exact(r[length - K:]) is not None]
            got = production(ok, K)
            assert np.all(got >= 0.0)
            assert np.max(np.abs(got.sum(axis=1) - 1.0)) <= 1e-12


def test_hand_computed_known_answers():
    """Exact rational model (T_Q, E_Q, PI_Q): posteriors derived by hand.

    w = (0,):   pi * E[:, 0] = (48, 17.5, 6.6) / 175           -> (480, 175, 66) / 721.
    w = (2, 0): only state 2 emits 2; T[2] * E[:, 0] = (4/9, 1/12, 0) -> (16/19, 3/19, 0).
    w = (1, 2): only state 2 emits 2                             -> (0, 0, 1).
    """
    cases = {
        (0,): (Q(480, 721), Q(175, 721), Q(66, 721)),
        (2, 0): (Q(16, 19), Q(3, 19), Q(0)),
        (1, 2): (Q(0), Q(0), Q(1)),
    }
    for suffix, expected in cases.items():
        assert tuple(ref.enumerate_posterior(T_Q, E_Q, PI_Q, list(suffix))) == expected
        assert gap(production([suffix], len(suffix))[0], expected) <= TOL_PROD
        # The decimal reference reads Decimal(float(x)): the float model, ~1e-16 from the rationals.
        assert gap(ref.decimal_suffix_posterior(T_Q, E_Q, PI_Q, list(suffix)), expected) <= 1e-14
    row = (1, 1) + (2, 0)  # the same suffix inside a longer history
    assert gap(production([row], 2)[0], cases[(2, 0)]) <= TOL_PROD


def test_decimal_reference_matches_enumeration():
    """Items 1 and 12: decimal forward summation vs exact path enumeration on every suffix."""
    worst = Q(0)
    for length in range(1, L_MAX + 1):
        for s in strings(length):
            expected = exact(s)
            if expected is None:
                with pytest.raises(ValueError):
                    ref.decimal_suffix_posterior(T_F, E_F, PI_F, list(s))
                continue
            dec = ref.decimal_suffix_posterior(T_F, E_F, PI_F, list(s))
            assert len(dec) == S
            worst = max(worst, max(abs(Q(d) - e) for d, e in zip(dec, expected)))
    assert worst <= Q(1, 10**15)
    # A 28-digit (default) context would leave errors near 1e-28; 60 digits give far less.
    assert worst <= Q(1, 10**50)


def test_decimal_precision_context_is_honoured():
    """Item 12: >= 60 significant digits are carried; a lower request is refused."""
    suffix = [0, 1, 0, 1]
    post60 = ref.decimal_suffix_posterior(T_F, E_F, PI_F, suffix)
    post100 = ref.decimal_suffix_posterior(T_F, E_F, PI_F, suffix, digits=100)
    len60 = max(len(d.as_tuple().digits) for d in post60)
    len100 = max(len(d.as_tuple().digits) for d in post100)
    assert 28 < len60 <= 60
    assert 60 < len100 <= 100
    assert max(abs(Q(a) - Q(b)) for a, b in zip(post60, post100)) <= Q(1, 10**55)
    with pytest.raises(ValueError):
        ref.decimal_suffix_posterior(T_F, E_F, PI_F, suffix, digits=28)
    with pytest.raises(ValueError):
        ref.enumerate_posterior(T_F, E_F, PI_F, [2, 2])


def test_decimal_circular_mean_matches_exact_mean():
    """Item 12: decimal circular mean vs the exact Fraction mean of the enumerated posterior."""
    feats = indep_features(COORDS)
    for length in range(1, 4):
        for s in strings(length):
            expected = exact(s)
            if expected is None:
                continue
            dec_mean = ref.decimal_circular_mean(
                ref.decimal_suffix_posterior(T_F, E_F, PI_F, list(s)), feats
            )
            for k in (0, 1):
                exact_mean = sum(expected[i] * Q(float(feats[i, k])) for i in range(S))
                assert abs(Q(dec_mean[k]) - exact_mean) <= Q(1, 10**50)


def test_posterior_means_matches_suffix_posterior_and_reference():
    """posterior_means = suffix_posterior @ features for every K; vs the decimal reference."""
    rows = [r for r in strings(L_MAX) if exact(r) is not None]  # every suffix then possible
    tokens = np.array(rows, dtype=np.int64)
    feats = op.circle_features(COORDS)
    assert feats.shape == (S, 2)
    assert np.max(np.abs(feats - indep_features(COORDS))) <= 1e-15
    Ks = [1, 2, 3, 4]
    means = op.posterior_means(T_F, E_F, PI_F, tokens, Ks, feats)
    assert sorted(means) == Ks
    for K in Ks:
        assert means[K].shape == (len(rows), 2)
        direct = op.suffix_posterior(T_F, E_F, PI_F, tokens, K) @ feats
        assert np.max(np.abs(means[K] - direct)) <= 1e-14
        for r, got in zip(rows, means[K]):
            post = ref.decimal_suffix_posterior(T_F, E_F, PI_F, list(r[L_MAX - K:]))
            dec_mean = ref.decimal_circular_mean(post, feats)
            assert max(abs(Q(float(got[k])) - Q(dec_mean[k])) for k in (0, 1)) <= TOL_PROD
