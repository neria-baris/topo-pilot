"""Independent tests (author B) for process_law.py: TEST_PLAN items B13 and B14 (spec v2.4).

Written from API.md (spec v2.4 item 4), ERROR_BOUND.md v2.2 section 9, CONTRACT.json and
TEST_PLAN.md, plus the frozen src/topo_pilot/dataset/sampler.py (read, not imported); no
production code was read. Expected laws come from an independent breakpoint sweep over the RAW
thresholds on the 2^-53 grid, the documented lattice law is rebuilt here in Fractions, and
softmax entries are recomputed at 80 digits.

Interpretations (reported): row_tv values and threshold_law entries are read with Fraction(...);
process_law_bound scalar results are read through _value, which accepts a number, an exact
string, or a dict with a "float" entry, because API.md says only "exact strings and floats".
"""

from __future__ import annotations

import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import errors  # noqa: E402
import process_law  # noqa: E402

pytestmark = pytest.mark.analysis

F = Fraction
SCALE = 2**53
STATES = [(s // 12, s % 12) for s in range(144)]
COORDS144 = np.array(STATES, dtype=np.float64)
CLAIM = ("bound on |E_Q[g·(M32-M4)]| under the IDEALIZED sampling law; not an exact zero for "
         "the fixed saved data")


def _cumulative_rows(P: np.ndarray) -> np.ndarray:
    """Replica of the frozen dataset/sampler.py `_cumulative_rows` (read, not imported)."""
    cum = np.cumsum(P, axis=1)
    last_pos = P.shape[1] - 1 - np.argmax(P[:, ::-1] > 0, axis=1)
    cols = np.arange(P.shape[1])[None, :]
    cum[cols >= last_pos[:, None]] = 1.0
    return cum


def _sweep_q(c_row) -> list[Fraction]:
    """Direct comparison-count law of j = min(#{i: c_i <= k 2^-53}, V-1), k = 0..2^53-1, from the
    RAW thresholds: c_i <= k 2^-53 iff k >= ceil(c_i 2^53); N is constant between breakpoints."""
    v = len(c_row)
    g = [math.ceil(F(float(c)) * SCALE) for c in c_row]
    points = sorted({0, SCALE} | {x for x in g if 0 < x < SCALE})
    counts = [0] * (v + 1)
    for a, b in zip(points, points[1:]):
        counts[sum(1 for x in g if x <= a)] += b - a
    q = [F(n, SCALE) for n in counts[:v]]
    q[v - 1] += F(counts[v], SCALE)
    return q


def _clamp(c_row) -> list[Fraction]:
    return [min(max(F(float(c)), F(0)), F(1)) for c in c_row]


def _monotone(c_row) -> bool:
    cl = _clamp(c_row)
    return all(a <= b for a, b in zip(cl, cl[1:])) and cl[-1] == 1


# ---- B13: sampler thresholds and the exact grid law ----
P_ROWS = np.array([[0.1, 0.2, 0.3, 0.4], [0.5, 0.5 + 2.0**-52, 0.0, 1e-17]])


def test_sampler_cdf_matches_frozen_cumulative_rows() -> None:
    got = process_law.sampler_cdf(P_ROWS)
    assert np.array_equal(got, _cumulative_rows(P_ROWS))
    # the raw cumsum exceeds 1 BEFORE the last positive entry in row 1
    assert got[1].tolist() == [0.5, 1.0 + 2.0**-52, 1.0 + 2.0**-52, 1.0]


@pytest.mark.parametrize("c_row, monotone", [
    (_cumulative_rows(P_ROWS)[0], True),           # monotone, ends at 1
    (_cumulative_rows(P_ROWS)[1], True),           # raw thresholds > 1 before the last positive
    (np.array([0.6, 0.3, 1.0]), False),            # hand-made non-monotone (not sampler output)
    (np.array([-0.25, 0.5, 1.0]), True),           # negative threshold clamps to 0
    (np.array([0.3, 0.7, 0.9]), False),            # never reaches 1: P(N = V) folds into V-1
])
def test_threshold_law_equals_direct_counting(c_row, monotone: bool) -> None:
    out = process_law.threshold_law(c_row)
    q = [F(x) for x in out["q"]]
    assert q == _sweep_q(c_row)
    assert sum(q) == 1
    assert [F(x) for x in out["clamped"]] == _clamp(c_row)
    assert bool(out["monotone"]) is monotone is _monotone(c_row)


def test_threshold_law_hand_values() -> None:
    q = [F(x) for x in process_law.threshold_law(_cumulative_rows(P_ROWS)[1])["q"]]
    assert q == [F(1, 2), F(1, 2), 0, 0]
    q = [F(x) for x in process_law.threshold_law(np.array([-0.25, 0.5, 1.0]))["q"]]
    assert q == [0, F(1, 2), F(1, 2)]


def _row_tv(p_hat, dev, c_row) -> tuple[Fraction, Fraction | None]:
    q = _sweep_q(c_row)
    grid = sum((abs(qj - F(float(pj))) + dj for qj, pj, dj in zip(q, p_hat, dev)), F(0)) / 2
    if not _monotone(c_row):
        return grid, None
    e, acc = [], F(0)
    for cj, pj in zip(_clamp(c_row), p_hat):
        acc += F(float(pj))
        e.append(cj - acc)
    doc = sum((abs(e[j]) + (abs(e[j - 1]) if j else 0) + F(1, SCALE) + dev[j]
               for j in range(len(e))), F(0)) / 2
    return grid, doc


def test_row_tv_grid_and_documented() -> None:
    dev = [F(1, 10**20)] * 4
    p_hat = P_ROWS[0]
    out = process_law.row_tv(p_hat, dev, _cumulative_rows(P_ROWS)[0])
    grid, doc = _row_tv(p_hat, dev, _cumulative_rows(P_ROWS)[0])
    assert F(out["grid"]) == grid
    assert out["documented"] is not None and F(out["documented"]) == doc >= grid
    dev3 = [F(0)] * 3
    out = process_law.row_tv(np.array([0.3, 0.3, 0.4]), dev3, np.array([0.6, 0.3, 1.0]))
    assert out["documented"] is None
    assert F(out["grid"]) == _row_tv(np.array([0.3, 0.3, 0.4]), dev3, [0.6, 0.3, 1.0])[0]


# ---- B14: lattice, documented transition, softmax enclosure ----
def _neighbours(x: int, y: int) -> set[tuple[int, int]]:
    out = {((x + 1) % 12, y), ((x - 1) % 12, y)}
    out |= {(x, y + d) for d in (-1, 1) if 0 <= y + d <= 11}
    return out


def _t_star() -> list[list[Fraction]]:
    index = {st: s for s, st in enumerate(STATES)}
    rows = []
    for x, y in STATES:
        row = [F(0)] * 144
        nb = _neighbours(x, y)
        for st in nb:
            row[index[st]] = F(1, 5)
        row[index[(x, y)]] = 1 - F(len(nb), 5)
        rows.append(row)
    return rows


def _d2(x: int, y: int, j: int) -> Fraction:
    a, b = divmod(j, 6)
    dx = abs(F(x) - (F(1, 2) + 2 * a)) % 12
    dy = F(y) - (F(1, 2) + 2 * b)
    return min(dx, 12 - dx) ** 2 + dy ** 2


def test_lattice_states_and_rejections() -> None:
    assert [tuple(map(int, st)) for st in process_law.lattice_states(COORDS144)] == STATES
    permuted = COORDS144[[1, 0] + list(range(2, 144))]
    shifted = COORDS144.copy()
    shifted[5, 0] += 0.5
    for bad in (permuted, shifted, COORDS144[:143]):
        with pytest.raises(process_law.Mismatch):
            process_law.lattice_states(bad)


def test_documented_transition_degrees_wrap_and_identities() -> None:
    T_star = process_law.documented_transition(STATES)
    assert [[F(v) for v in row] for row in T_star] == _t_star()
    for s, (x, y) in enumerate(STATES):
        degree = sum(1 for t in range(144) if t != s and T_star[s][t] != 0)
        assert degree == (3 if y in (0, 11) else 4)
    assert T_star[STATES.index((0, 5))][STATES.index((11, 5))] == F(1, 5)     # x wraps
    assert T_star[STATES.index((3, 0))][STATES.index((3, 11))] == 0           # y does not
    assert process_law.ideal_identities(_t_star(), 144) is None
    perturbed = _t_star()
    perturbed[0][1] += F(1, 100)                 # row sums kept, symmetry broken
    perturbed[0][0] -= F(1, 100)
    with pytest.raises(process_law.Mismatch):
        process_law.ideal_identities(perturbed, 144)


def test_softmax_enclosure_contains_80_digit_values() -> None:
    assert _d2(0, 0, 0) == F(1, 2) and -8 * _d2(0, 0, 0) / 25 == F(-4, 25)   # API example
    assert _d2(11, 0, 0) == F(5, 2)                                          # x-periodic
    e_dec, lo, hi = process_law.softmax_enclosure(STATES)
    u = F(1, 2 * 10**59)
    assert F(lo) == (1 - 2 * u) * (1 - u) / ((1 + 2 * u) * (1 + u) ** 36)
    assert F(hi) == (1 + 2 * u) * (1 + u) / ((1 - 2 * u) * (1 - u) ** 36)
    assert F(lo) < 1 < F(hi) and F(hi) - F(lo) < F(1, 10**55)
    for x, y in ((0, 0), (11, 0), (5, 7), (11, 11)):
        s = STATES.index((x, y))
        with localcontext() as ctx:
            ctx.prec = 80
            n = [(Decimal(-8) * Decimal((_d2(x, y, j)).numerator)
                  / Decimal(25 * _d2(x, y, j).denominator)).exp() for j in range(36)]
            total = sum(n, Decimal(0))
            ref = [F(v / total) for v in n]
        for j in range(36):
            got = F(e_dec[s][j])
            assert got / F(hi) <= ref[j] <= got / F(lo), (x, y, j)


# ---- B14: process_law_bound on the documented law rounded to float64 ----
def _value(out: dict, key: str) -> float:
    v = out[key]
    if isinstance(v, dict):
        v = v["float"]
    return float(F(v)) if isinstance(v, str) else float(v)


def _float_law() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    T_hat = np.array([[float(v) for v in row] for row in _t_star()])
    logits = np.array([[-8 * float(_d2(x, y, j)) / 25 for j in range(36)] for x, y in STATES])
    w = np.exp(logits - logits.max(axis=1, keepdims=True))
    return T_hat, w / w.sum(axis=1, keepdims=True), np.full(144, 1 / 144)


@pytest.fixture(scope="module")
def float_law():
    return _float_law()


def test_law_constants() -> None:
    assert process_law.LAW == {"dims": (12, 12), "x_period": 12, "neighbour": F(1, 5),
                               "grid": 6, "sigma": F(5, 4), "L": 32,
                               "draws": {"pi": 1, "emission": 32, "transition": 31}}


def test_process_law_bound_on_the_rounded_documented_law(float_law) -> None:
    T_hat, E_hat, pi_hat = float_law
    out = process_law.process_law_bound(T_hat, E_hat, pi_hat, COORDS144)
    assert out["status"] == "BOUNDED"
    kappa = max(_value(out, k) for k in ("kappa_T", "kappa_pi", "kappa_E"))
    assert 0 < kappa < 1e-12
    z = _value(out, "Z_bound")
    assert math.isfinite(z) and 0 < z < 1e-9
    assert out["TV_documented"] is not None       # sampler thresholds are monotone after clamping
    assert out["claim"] == CLAIM


def _unavailable_cases(float_law) -> dict:
    T_hat, E_hat, pi_hat = float_law
    support = T_hat.copy()
    support[0, 50] = 1e-3                          # (0,0)-(4,2) is not a lattice edge
    zero_e = E_hat.copy()
    zero_e[0, 35] = 0.0
    big_pi = pi_hat.copy()
    big_pi[0] = 3 / 144                            # kappa_pi = 2 >= 1
    swapped = COORDS144[[1, 0] + list(range(2, 144))]
    return {"zero_support": (support, E_hat, pi_hat, COORDS144),
            "zero_E": (T_hat, zero_e, pi_hat, COORDS144),
            "kappa_ge_1": (T_hat, E_hat, big_pi, COORDS144),
            "permuted_coords": (T_hat, E_hat, pi_hat, swapped),
            "S_143": (T_hat[:143, :143], E_hat[:143], pi_hat[:143], COORDS144[:143])}


@pytest.mark.parametrize("case", ["zero_support", "zero_E", "kappa_ge_1", "permuted_coords",
                                  "S_143"])
def test_process_law_bound_unavailable_with_reason(float_law, case: str) -> None:
    out = process_law.process_law_bound(*_unavailable_cases(float_law)[case])
    assert out["status"] == "UNAVAILABLE", case
    assert isinstance(out["reason"], str) and out["reason"].strip()


def test_process_law_bound_invalid_only_for_nonfinite_or_misshaped(float_law) -> None:
    T_hat, E_hat, pi_hat = float_law
    nan_t = T_hat.copy()
    nan_t[3, 3] = np.nan
    with pytest.raises(errors.Invalid):
        process_law.process_law_bound(nan_t, E_hat, pi_hat, COORDS144)
    with pytest.raises(errors.Invalid):
        process_law.process_law_bound(T_hat[0], E_hat, pi_hat, COORDS144)
