"""Independent tests of x4_oracle_profile: suffix boundary, orientation traps, symbol permutation
and error paths (job 0014; API.md section 4 items 2, 3, 4 and 6).

The deliberately WRONG filters below are defined in this test file and are never production code.
Each trap is shown to differ from exact path enumeration by more than 1e-6 on a hand-constructed
case and on the exhaustive case set, while production matches enumeration within 1e-12 on every
case. Written from ``tools/x4_oracle_profile/API.md`` only: production is imported, never read.
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
# Same HMM as test_oracle_profile.py, where pi = (72, 70, 33) / 175 is derived by exact
# elimination and checked; strings containing two consecutive 2s are impossible.
T_Q = [[Q(1, 2), Q(1, 3), Q(1, 6)], [Q(1, 5), Q(1, 2), Q(3, 10)], [Q(2, 3), Q(1, 3), Q(0)]]
E_Q = [[Q(2, 3), Q(1, 3), Q(0)], [Q(1, 4), Q(3, 4), Q(0)], [Q(1, 5), Q(0), Q(4, 5)]]
PI_Q = [Q(72, 175), Q(70, 175), Q(33, 175)]
S, V, L_MAX = 3, 3, 4
T_F = np.array([[float(x) for x in row] for row in T_Q], dtype=np.float64)
E_F = np.array([[float(x) for x in row] for row in E_Q], dtype=np.float64)
PI_F = np.array([float(x) for x in PI_Q], dtype=np.float64)
SYMBOL_PERM = np.array([2, 0, 1], dtype=np.int64)  # a 3-cycle, so it differs from its inverse
INVERSE_PERM = np.argsort(SYMBOL_PERM)  # [1, 2, 0]
E_CANON_EXPECTED = E_F[:, SYMBOL_PERM]
TOL_PROD, TRAP_GAP = 1e-12, 1e-6


def strings(length: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(V), repeat=length))


@lru_cache(maxsize=None)
def exact(suffix: tuple[int, ...]) -> tuple[Fraction, ...] | None:
    """Exact posterior of the float model by path enumeration; None when impossible."""
    try:
        return tuple(ref.enumerate_posterior(T_F, E_F, PI_F, list(suffix)))
    except ValueError:
        return None


def gap(values, fracs) -> float:
    return float(max(abs(Q(float(a)) - Q(f)) for a, f in zip(values, fracs)))


def named(row: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(int(SYMBOL_PERM[c]) for c in row)


@lru_cache(maxsize=None)
def prod_one(row: tuple[int, ...], K: int, canonical: bool = False) -> np.ndarray:
    """Production posterior of one row (canonical tokens with the canonical emission if asked)."""
    E = op.canonical_emission(E_F, SYMBOL_PERM) if canonical else E_F
    return op.suffix_posterior(T_F, E, PI_F, np.array([row], dtype=np.int64), K)[0]


def wrong_filter(T, E, init, symbols, *, transpose=False, extra_step=False):
    """Plain float forward filter with switchable MISTAKES (test-only, never production).

    transpose: propagates with T.T (alpha_{t+1}(j) = E(j, w) sum_i alpha_t(i) T[j, i]).
    extra_step: applies one more transition after the last emission (returns post @ T).
    Returns None when the (wrong) model gives the symbols zero probability.
    """
    A = T.T if transpose else T
    b = init * E[:, symbols[0]]
    for w in symbols[1:]:
        b = (b @ A) * E[:, w]
    total = b.sum()
    if total <= 0:
        return None
    b = b / total
    return b @ T if extra_step else b


def last(row, K):
    return row[len(row) - K:]


# name: (trap(row, K), constructed (row, K), uses canonical tokens)
# Constructed cases (exact answers from test_oracle_profile.py):
#   transposed_T   (2, 0) K=2: correct (16/19, 3/19, 0); with T.T: prop. to (1/9, 3/40, 0).
#   extra_trans    (2,)   K=1: correct (0, 0, 1); one more step gives T[2] = (2/3, 1/3, 0).
#   prefix         (0, 2) K=1: correct (0, 0, 1); prefix (0,) gives (480, 175, 66) / 721.
#   carry_over     (2, 0) K=1: correct (480, 175, 66)/721; whole-row filter gives (16/19, 3/19, 0).
#   uniform_start  (0,)   K=1: correct (480, 175, 66)/721; uniform start gives (40, 15, 12) / 67.
#   E_named        canonical (0,) = named (2,): correct (0, 0, 1); E_named[:, 0] gives
#                  (480, 175, 66) / 721.
#   inverse_perm   canonical (0,): E_named[:, inv][:, 0] = E_named[:, 1] -> (24, 52.5, 0) / 76.5.
TRAPS = {
    "transposed_T": (
        lambda r, K: wrong_filter(T_F, E_F, PI_F, last(r, K), transpose=True), ((2, 0), 2), False
    ),
    "extra_transition_after_last_emission": (
        lambda r, K: wrong_filter(T_F, E_F, PI_F, last(r, K), extra_step=True), ((2,), 1), False
    ),
    "prefix_instead_of_suffix": (
        lambda r, K: wrong_filter(T_F, E_F, PI_F, r[:K]), ((0, 2), 1), False
    ),
    "carry_over_filtered_belief": (
        lambda r, K: wrong_filter(T_F, E_F, PI_F, r), ((2, 0), 1), False
    ),
    "uniform_restart_instead_of_pi": (
        lambda r, K: wrong_filter(T_F, E_F, np.full(S, 1.0 / S), last(r, K)), ((0,), 1), False
    ),
    "canonical_tokens_with_E_named": (
        lambda r, K: wrong_filter(T_F, E_F, PI_F, last(r, K)), ((0,), 1), True
    ),
    "inverse_permutation": (
        lambda r, K: wrong_filter(T_F, E_F[:, INVERSE_PERM], PI_F, last(r, K)), ((0,), 1), True
    ),
}


def correct(row, K, canonical):
    return exact(named(last(row, K)) if canonical else last(row, K))


@pytest.mark.parametrize("name", sorted(TRAPS))
def test_trap_differs_from_enumeration_while_production_matches(name):
    """Item 3 (a)-(d), plus the two restart traps of item 2."""
    trap, (row0, K0), canonical = TRAPS[name]
    wrong0 = trap(row0, K0)
    assert wrong0 is not None
    assert gap(wrong0, correct(row0, K0, canonical)) > TRAP_GAP
    assert gap(prod_one(row0, K0, canonical), correct(row0, K0, canonical)) <= TOL_PROD
    worst, n_cases = 0.0, 0
    for length in range(1, L_MAX + 1):
        for row in strings(length):
            for K in range(1, length + 1):
                expected = correct(row, K, canonical)
                if expected is None:
                    continue
                assert gap(prod_one(row, K, canonical), expected) <= TOL_PROD, (row, K)
                wrong = trap(row, K)
                if wrong is not None:
                    worst = max(worst, gap(wrong, expected))
                n_cases += 1
    assert n_cases > 300 and worst > TRAP_GAP


def test_tokens_before_suffix_have_no_effect():
    """Item 2: every prefix (even ones making the full row impossible) leaves post_K unchanged."""
    n_impossible_full_rows = 0
    for K in (1, 2, 3):
        for suffix in strings(K):
            if exact(suffix) is None:
                continue
            rows = [p + suffix for p in strings(L_MAX - K)]
            got = op.suffix_posterior(T_F, E_F, PI_F, np.array(rows, dtype=np.int64), K)
            alone = op.suffix_posterior(T_F, E_F, PI_F, np.array([suffix], dtype=np.int64), K)
            assert np.max(np.abs(got - got[0])) <= 1e-14
            assert np.max(np.abs(got - alone)) <= 1e-14
            assert gap(alone[0], exact(suffix)) <= TOL_PROD
            n_impossible_full_rows += sum(exact(r) is None for r in rows)
    assert n_impossible_full_rows > 0


def test_restart_uses_stationary_pi():
    """Item 2: post_1 of (..., 0) is pi * E[:, 0] normalised, whatever came before."""
    expected = (Q(480, 721), Q(175, 721), Q(66, 721))
    for row in [(0,), (2, 0), (1, 2, 0), (2, 1, 2, 0)]:
        assert gap(prod_one(row, 1), expected) <= TOL_PROD


def test_canonical_emission_is_the_column_permutation():
    """Item 4."""
    E_before, perm_before = E_F.copy(), SYMBOL_PERM.copy()
    E_c = op.canonical_emission(E_F, SYMBOL_PERM)
    assert E_c.dtype == np.float64 and np.array_equal(E_c, E_CANON_EXPECTED)
    assert np.array_equal(E_F, E_before) and np.array_equal(SYMBOL_PERM, perm_before)
    assert np.array_equal(op.canonical_emission(E_F, np.arange(V)), E_F)
    assert np.array_equal(op.canonical_emission(E_F, SYMBOL_PERM.astype(np.int32)), E_c)


def test_canonical_filtering_equals_named_filtering():
    """Item 4: canonical tokens with E_canon == named tokens symbol_perm[canonical] with E_named."""
    E_c = op.canonical_emission(E_F, SYMBOL_PERM)
    n_compared = 0
    for length in range(1, L_MAX + 1):
        canon = np.array(strings(length), dtype=np.int64)
        named_tokens = SYMBOL_PERM[canon]
        for K in range(1, length + 1):
            suffixes = [tuple(int(x) for x in r[length - K:]) for r in named_tokens]
            keep = [i for i, s in enumerate(suffixes) if exact(s) is not None]
            a = op.suffix_posterior(T_F, E_c, PI_F, canon[keep], K)
            b = op.suffix_posterior(T_F, E_F, PI_F, named_tokens[keep], K)
            assert np.max(np.abs(a - b)) <= TOL_PROD
            n_compared += len(keep)
    assert n_compared > 300
    with pytest.raises(op.ProfileError):  # canonical (0, 0) is named (2, 2): impossible
        op.suffix_posterior(T_F, E_c, PI_F, np.array([[0, 0]], dtype=np.int64), 2)


@pytest.mark.parametrize(
    "perm",
    [[0, 0, 1], [0, 1, 3], [0, 1], [3, 0, 1, 2], [-1, 0, 1], [0.0, 1.5, 2.0], [[0, 1, 2]]],
    ids=["repeat", "out_of_range", "too_short", "too_long", "negative", "non_integer", "two_d"],
)
def test_canonical_emission_rejects_non_permutations(perm):
    """Item 4."""
    with pytest.raises(op.ProfileError):
        op.canonical_emission(E_F, np.array(perm))


VALID = np.array([[0, 1, 2]], dtype=np.int64)
BAD_CALLS = {
    "impossible_suffix": (np.array([[0, 2, 2]]), 2),
    "impossible_row_in_batch": (np.array([[0, 1, 0], [1, 2, 2]]), 2),
    "token_too_large_in_suffix": (np.array([[0, 1, 3]]), 1),
    "token_too_large_before_suffix": (np.array([[3, 1, 0]]), 1),
    "uint8_token_too_large": (np.array([[0, 1, 255]], dtype=np.uint8), 1),
    "negative_token_in_suffix": (np.array([[0, -1, 1]]), 2),
    "negative_token_before_suffix": (np.array([[-1, 0, 1]]), 1),
    "float_dtype": (VALID.astype(np.float64), 1),
    "K_zero": (VALID, 0),
    "K_negative": (VALID, -1),
    "K_L_plus_1": (VALID, 4),
    "bool_K": (VALID, True),
    "one_dimensional_tokens": (np.array([0, 1, 2]), 1),
    "three_dimensional_tokens": (VALID[None], 1),
    "empty_rows": (np.zeros((0, 3), dtype=np.int64), 1),
    "empty_columns": (np.zeros((1, 0), dtype=np.int64), 1),
}


@pytest.mark.parametrize("name", sorted(BAD_CALLS))
def test_suffix_posterior_error_paths(name):
    """Item 6."""
    tokens, K = BAD_CALLS[name]
    with pytest.raises(op.ProfileError):
        op.suffix_posterior(T_F, E_F, PI_F, tokens, K)


def test_integer_dtypes_and_numpy_integer_K_are_accepted():
    rows = np.array([r for r in strings(3) if exact(r) is not None], dtype=np.int64)
    base = op.suffix_posterior(T_F, E_F, PI_F, rows, 2)
    for dtype in (np.int8, np.int16, np.int32, np.uint8, np.uint16, np.uint32, np.uint64):
        got = op.suffix_posterior(T_F, E_F, PI_F, rows.astype(dtype), 2)
        assert np.max(np.abs(got - base)) <= 1e-15, dtype
    for K in (np.int64(2), np.int32(2), np.uint8(2)):
        assert np.max(np.abs(op.suffix_posterior(T_F, E_F, PI_F, rows, K) - base)) <= 1e-15
    assert op.suffix_posterior(T_F, E_F, PI_F, rows, 3).shape == (len(rows), S)


def test_inputs_are_not_mutated():
    tokens = np.array([r for r in strings(3) if exact(r) is not None], dtype=np.int64)
    arrays = (T_F, E_F, PI_F, tokens)
    copies = [a.copy() for a in arrays]
    op.suffix_posterior(T_F, E_F, PI_F, tokens, 2)
    op.posterior_means(T_F, E_F, PI_F, tokens, [1, 3], np.ones((S, 2)))
    for a, c in zip(arrays, copies):
        assert np.array_equal(a, c) and a.dtype == c.dtype
