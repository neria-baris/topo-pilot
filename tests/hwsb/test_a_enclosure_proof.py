"""HWSB author A: the B8a enclosure proof steps (protocol §4 B8a with delta as in RC-1; KB4 at
sigma 5/4; DRB12; the proof note obligation of OPEN-3).

Targets (API.md §5): hwsb_law.exact_logits, rounding_delta, softmax_enclosure_rounded, bound_law,
decimal_check. The 144 lattice states are written here; logits q = -d^2/(2 sigma^2) are exact
Fractions; q~ is q rounded to 60 significant digits (ROUND_HALF_EVEN), recomputed here by
integer arithmetic; delta = max |q~ - q|. Proof steps checked on the actual delta: (1) E_dec, lo,
hi from q~ as process_law.softmax_enclosure computes them; (2) softmax(q)/softmax(q~) in
[e^{-2 delta}, e^{2 delta}] at 200 digits; (3) e^{-2 delta} >= 1 - 2 delta and
e^{2 delta} <= 1/(1 - 2 delta) at 120 digits. No store, no payload.
"""

from __future__ import annotations

import decimal
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_oracle_profile", "tools/x4_circle_history", "tools/c1prime_registry",
             "tools/c1prime", "tools/k4b", "tools/hws"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import error_bound  # noqa: E402
import errors  # noqa: E402
import process_law  # noqa: E402

try:
    import hwsb_config as hc  # noqa: E402,F401
    import hwsb_law as hl  # noqa: E402
except ImportError as _exc:  # the implementation is written in parallel
    hc = hl = None
    MISSING = repr(_exc)
else:
    MISSING = None

STATES = [(s // 12, s % 12) for s in range(144)]
CENTRES = [(Fraction(1, 2) + 2 * a, Fraction(1, 2) + 2 * b) for a in range(6) for b in range(6)]
U60 = Fraction(1, 2 * 10**59)
S54, S74, NB = Fraction(5, 4), Fraction(7, 4), Fraction(1, 5)


def need():
    if MISSING:
        pytest.fail("tools/hwsb modules not importable: " + MISSING)


def logits_ref(sigma):
    out = []
    for x, y in STATES:
        row = []
        for cx, cy in CENTRES:
            dx = abs(Fraction(x) - cx) % 12
            d2 = min(dx, 12 - dx) ** 2 + (Fraction(y) - cy) ** 2
            row.append(-d2 / (2 * sigma**2))
        out.append(row)
    return out


def round60(q: Fraction) -> Fraction:
    """q rounded to 60 significant decimal digits, ties to even (exact integer arithmetic)."""
    if q == 0:
        return q
    a = abs(q)
    e = math.floor(math.log10(a.numerator) - math.log10(a.denominator)) - 59
    while a / Fraction(10) ** e >= 10**60:
        e += 1
    while a / Fraction(10) ** e < 10**59:
        e -= 1
    s = a / Fraction(10) ** e
    n = s.numerator // s.denominator
    r = s - n
    if r > Fraction(1, 2) or (r == Fraction(1, 2) and n % 2 == 1):
        n += 1
    return (1 if q > 0 else -1) * n * Fraction(10) ** e


def lo_hi0():
    u, n_add = U60, 36
    lo = (1 - 2 * u) * (1 - u) / ((1 + 2 * u) * (1 + u) ** n_add)
    hi = (1 + 2 * u) * (1 + u) / ((1 - 2 * u) * (1 - u) ** n_add)
    return lo, hi


def dec(fr: Fraction, prec: int) -> Decimal:
    with decimal.localcontext(decimal.Context(prec=prec, rounding=decimal.ROUND_HALF_EVEN)):
        return Decimal(fr.numerator) / Decimal(fr.denominator)


def softmax_dec(row, prec):
    with decimal.localcontext(decimal.Context(prec=prec, rounding=decimal.ROUND_HALF_EVEN)):
        num = [v.exp() for v in row]
        den = sum(num, Decimal(0))
        return [v / den for v in num]


@pytest.fixture(scope="module")
def ref74():
    q = logits_ref(S74)
    qt = [[round60(v) for v in row] for row in q]
    delta = max(abs(a - b) for ra, rb in zip(qt, q) for a, b in zip(ra, rb))
    q_max = max(abs(v) for row in q for v in row)
    n_inexact = sum(a != b for ra, rb in zip(qt, q) for a, b in zip(ra, rb))
    return {"q": q, "qt": qt, "delta": delta, "Q_max": q_max, "n_inexact": n_inexact}


@pytest.fixture(scope="module")
def enc74():
    if MISSING:
        return None
    with hl.bound_law(S74, NB):
        return hl.softmax_enclosure_rounded(STATES)


# ------------------------------------------------------------- pure reference checks

def test_reference_states_are_the_documented_lattice():
    coords = np.array([[s // 12, s % 12] for s in range(144)], dtype=np.float64)
    assert process_law.lattice_states(coords) == STATES
    assert error_bound.u_digits(60) == U60


def test_reference_round60_agrees_with_decimal_division(ref74):
    ctx = error_bound.trapping_context(60)
    for row_q, row_t in list(zip(ref74["q"], ref74["qt"]))[::17]:
        for q, t in zip(row_q, row_t):
            with decimal.localcontext(ctx):
                assert Fraction(Decimal(q.numerator) / Decimal(q.denominator)) == t


def test_reference_sigma_5_4_logits_terminate():
    q = logits_ref(S54)
    assert all(round60(v) == v for row in q for v in row)


def test_reference_step3_inequalities_for_u_qmax(ref74):
    # step (3) holds for every 0 < x < 1; checked here at the bound 2 u Q_max
    x = dec(2 * U60 * ref74["Q_max"], 120)
    with decimal.localcontext(decimal.Context(prec=120)):
        assert (-x).exp() >= 1 - x and x.exp() <= 1 / (1 - x)


# ------------------------------------------------------------- exact logits

def test_exact_logits_equal_independent_fractions():
    need()
    with hl.bound_law(S74, NB):
        assert hl.exact_logits(STATES) == logits_ref(S74)
    with hl.bound_law(Fraction(3, 2), NB):
        assert hl.exact_logits(STATES[:12]) == logits_ref(Fraction(3, 2))[:12]
    with hl.bound_law(S54, NB):
        got = hl.exact_logits(STATES)
    assert got == logits_ref(S54)
    assert all(isinstance(v, Fraction) for row in got for v in row)


def test_centres_in_softmax_enclosure_order():
    need()
    assert list(hl.centres()) == CENTRES


# ------------------------------------------------------------- sigma = 5/4: delta = 0 (KB4)

def test_sigma_5_4_delta_zero_and_identical_to_old_enclosure():
    need()
    old = process_law.softmax_enclosure
    with hl.bound_law(S54, NB):
        r = hl.rounding_delta(STATES)
        new = hl.softmax_enclosure_rounded(STATES)
        ref = old(STATES)
    assert r["delta"] == 0 and r["n_inexact"] == 0
    E_new, lo_new, hi_new = new
    E_old, lo_old, hi_old = ref
    assert lo_new == lo_old and hi_new == hi_old
    assert isinstance(lo_new, Fraction) and isinstance(hi_new, Fraction)
    assert len(E_new) == len(E_old) == 144
    for row_n, row_o in zip(E_new, E_old):
        assert len(row_n) == 36
        assert all(a == b and str(a) == str(b) for a, b in zip(row_n, row_o))


# ------------------------------------------------------------- sigma = 7/4: delta > 0 (RC-1)

def test_sigma_7_4_rounding_delta(ref74):
    need()
    with hl.bound_law(S74, NB):
        r = hl.rounding_delta(STATES)
    assert r["delta"] == ref74["delta"] > 0
    assert r["Q_max"] == ref74["Q_max"]
    assert r["u"] == U60
    assert r["bound"] == U60 * ref74["Q_max"]
    assert r["delta"] <= r["bound"]
    assert 2 * r["delta"] < 1
    assert r["n_inexact"] == ref74["n_inexact"] > 0
    assert ref74["Q_max"] == Fraction(8, 49) * Fraction(281, 2)  # d^2 max = 5.5^2 + 10.5^2


def test_sigma_7_4_rounded_logits_are_q_tilde(ref74):
    need()
    with hl.bound_law(S74, NB):
        qt = hl.rounded_logits(hl.exact_logits(STATES))
    for row_d, row_t in zip(qt, ref74["qt"]):
        assert [Fraction(v) for v in row_d] == row_t


def test_sigma_7_4_widened_lo_hi(ref74, enc74):
    need()
    _, lo, hi = enc74
    lo0, hi0 = lo_hi0()
    d = ref74["delta"]
    assert lo == lo0 * (1 - 2 * d)
    assert hi == hi0 / (1 - 2 * d)
    assert lo < lo0 < 1 < hi0 < hi


def test_sigma_7_4_e_dec_computed_from_q_tilde(ref74, enc74):
    """Step (1): the existing analysis applies to the exact inputs q~ (process_law.py:117-124)."""
    need()
    E_dec = enc74[0]
    ctx = error_bound.trapping_context(60)
    for s in range(0, 144, 7):
        with decimal.localcontext(ctx):
            row = [Decimal(t.numerator) / Decimal(t.denominator) for t in ref74["qt"][s]]
            num = [v.exp() for v in row]
            den = sum(num, Decimal(0))
            expected = [v / den for v in num]
        assert E_dec[s] == expected, s


def test_step2_ratio_bound_at_200_digits(ref74):
    rows = sorted({0, 13, 77, 143} | {max(range(144), key=lambda s: max(
        abs(v) for v in ref74["q"][s]))})
    d = ref74["delta"]
    with decimal.localcontext(decimal.Context(prec=200)):
        lo_b, hi_b = (-2 * dec(d, 200)).exp(), (2 * dec(d, 200)).exp()
    for s in rows:
        exact = softmax_dec([dec(v, 200) for v in ref74["q"][s]], 200)
        tilde = softmax_dec([dec(v, 200) for v in ref74["qt"][s]], 200)
        with decimal.localcontext(decimal.Context(prec=200)):
            for a, b in zip(exact, tilde):
                ratio = a / b
                assert lo_b <= ratio <= hi_b, s


def test_step3_on_actual_delta(ref74):
    x = dec(2 * ref74["delta"], 120)
    with decimal.localcontext(decimal.Context(prec=120)):
        left = (-x).exp() - (1 - x)
        right = 1 / (1 - x) - x.exp()
        assert left > 0 and right > 0
        # both margins are about x^2/2, far above the 120-digit rounding (about 1e-120)
        assert x * x / 2 > Decimal(10) ** -118
        assert left > x * x / 4 and right > x * x / 4


def test_enclosure_contains_exact_entries_on_sampled_rows(ref74, enc74):
    """Steps (1)-(3) combined: E*_j in [E_dec (1 - 2 delta)/hi0, E_dec/(lo0 (1 - 2 delta))]."""
    need()
    E_dec, lo, hi = enc74
    for s in (0, 5, 66, 143):
        exact = softmax_dec([dec(v, 200) for v in ref74["q"][s]], 200)
        for j in range(36):
            e = Fraction(exact[j])
            assert Fraction(E_dec[s][j]) / hi - Fraction(1, 10**190) <= e
            assert e <= Fraction(E_dec[s][j]) / lo + Fraction(1, 10**190)


# ------------------------------------------------------------- refusals and checks

def test_digits_other_than_60_raise_invalid():
    need()
    with hl.bound_law(S74, NB):
        for digits in (50, 61, 200):
            with pytest.raises(errors.Invalid):
                hl.softmax_enclosure_rounded(STATES, digits=digits)


def entries_with_extremes(ref74, k=58, seed=616601):
    flat = [(s, j) for s in range(144) for j in range(36)]
    mags = {(s, j): abs(ref74["q"][s][j]) for s, j in flat}
    extremes = [max(flat, key=mags.get), min(flat, key=mags.get)]
    rng = np.random.default_rng(seed)
    picks = [flat[i] for i in rng.choice(len(flat), size=k, replace=False)]
    return extremes + [p for p in picks if p not in extremes]


def test_decimal_check_passes_on_true_enclosure(ref74, enc74):
    need()
    entries = entries_with_extremes(ref74)
    assert len(entries) >= 50
    with hl.bound_law(S74, NB):
        res = hl.decimal_check(STATES, enc74, entries)
    assert res["n"] == len(entries)
    assert res["n_fail"] == 0 and res["pass"]


def test_decimal_check_catches_planted_narrow_enclosure(ref74, enc74):
    need()
    entries = entries_with_extremes(ref74, k=20)
    narrow = (enc74[0], Fraction(1), Fraction(1))
    with hl.bound_law(S74, NB):
        res = hl.decimal_check(STATES, narrow, entries)
    assert not res["pass"]
    assert res["n_fail"] == res["n"] == len(entries)


def test_bound_law_restores_process_law_state():
    need()
    before = (process_law.LAW["sigma"], process_law.LAW["neighbour"],
              process_law.softmax_enclosure)
    with hl.bound_law(S74, NB):
        assert process_law.LAW["sigma"] == S74 and process_law.LAW["neighbour"] == NB
        assert process_law.softmax_enclosure is hl.softmax_enclosure_rounded
    assert (process_law.LAW["sigma"], process_law.LAW["neighbour"],
            process_law.softmax_enclosure) == before
    with pytest.raises(ZeroDivisionError):
        with hl.bound_law(Fraction(3, 2), NB):
            raise ZeroDivisionError("planted")
    assert (process_law.LAW["sigma"], process_law.LAW["neighbour"],
            process_law.softmax_enclosure) == before


def test_proof_note_exists_and_names_delta_and_rounding():
    """OPEN-3: the reviewed proof note is in tools/hwsb (content reviewed elsewhere)."""
    need()
    path = REPO / "tools" / "hwsb" / "ENCLOSURE_PROOF.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8").lower()
    assert ("δ" in text or "delta" in text) and "round" in text
