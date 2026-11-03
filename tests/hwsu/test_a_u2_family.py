"""Author A (job 0223): family stream U and Lemma FW-U, response part (protocol 2.9; API_U2 4.4).

family_bounds: keys <j>:ZR010, <j>:ZR030, <j>:AF in master order, one shared index stream,
ranks 67 / 19,934 of 20,000 at alpha = 1/300, guard c2_decide.guard(array, 0.0)."""

from __future__ import annotations  # noqa: I001

import importlib
import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import c1_records  # noqa: E402
import c2_decide  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

MASTERS = [620301, 620302, 620303]
N = 48


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(11)
    G = rng.random(N) + 0.2
    A = {j: t * G + 0.05 * rng.standard_normal(N) for j, t in zip(MASTERS, (0.5, 0.2, 0.0))}
    return A, G


@pytest.fixture(scope="module")
def fb(data):
    A, G = data
    return mod("hwsu_gates").family_bounds(A, G, MASTERS)


def _arrays(A, G, models):
    out = {}
    for j in models:
        out[f"{j}:ZR010"] = A[j] - 0.1 * G
        out[f"{j}:ZR030"] = A[j] - 0.3 * G
        out[f"{j}:AF"] = A[j]
    return out


def test_ranks_at_alpha_1_300():
    a = Fraction(1, 300)
    assert math.ceil(a * 20000) == 67
    assert math.ceil((1 - a) * 20000) == 19934


def test_keys_and_ranks(fb):
    assert list(fb) == [f"{j}:{s}" for j in MASTERS for s in ("ZR010", "ZR030", "AF")]
    for v in fb.values():
        assert v["rank_L"] == 67 and v["rank_U"] == 19934
        assert {"L", "U", "mean", "rank_L", "rank_U", "g"} <= set(v)


def test_equals_one_shared_stream(data, fb):
    A, G = data
    arrays = _arrays(A, G, MASTERS)
    ref = c2_decide.stream_bounds(arrays, 640111, float(Fraction(1, 300)), 20000)
    for k in arrays:
        assert fb[k]["L"] == ref[k]["L"] and fb[k]["U"] == ref[k]["U"]
        assert fb[k]["mean"] == ref[k]["mean"]
        assert fb[k]["g"] == c2_decide.guard(arrays[k], 0.0)


def test_key_order_is_part_of_contract(data, fb):
    """A stream over a permuted key order yields different bounds: order matters."""
    A, G = data
    arrays = _arrays(A, G, MASTERS[::-1])
    perm = c2_decide.stream_bounds(arrays, 640111, float(Fraction(1, 300)), 20000)
    k = f"{MASTERS[0]}:ZR010"
    assert (perm[k]["L"], perm[k]["U"]) != (fb[k]["L"], fb[k]["U"])
    fb2 = mod("hwsu_gates").family_bounds(A, G, MASTERS[::-1])
    assert list(fb2)[0] == f"{MASTERS[-1]}:ZR010"
    assert fb2[k]["L"] == perm[k]["L"]


def test_seed_default_640111(data, fb):
    A, G = data
    other = mod("hwsu_gates").family_bounds(A, G, MASTERS, seed=640112)
    k = f"{MASTERS[0]}:AF"
    assert (other[k]["L"], other[k]["U"]) != (fb[k]["L"], fb[k]["U"])


def test_rank_mismatch_fails_numerical(data, monkeypatch):
    A, G = data
    real = c2_decide.stream_bounds

    def bad(arrays, seed, alpha, draws=20000):
        out = real(arrays, seed, alpha, draws)
        k = next(iter(out))
        out[k] = dict(out[k], rank_L=66)
        return out

    monkeypatch.setattr(c2_decide, "stream_bounds", bad)
    with pytest.raises(c1_records.C1GateFailure) as e:
        mod("hwsu_gates").family_bounds(A, G, MASTERS)
    assert e.value.status == "FAIL_TECHNICAL/NUMERICAL"


def test_bound_ordering(fb):
    for v in fb.values():
        assert v["L"] <= v["mean"] <= v["U"]


# ---- Lemma FW-U, response part --------------------------------------------------------------
# region -> representative theta values (protocol 2.9 lists the regions and events)
REGIONS = {
    "theta <= 0": [Fraction(-1, 2), Fraction(0)],
    "0 < theta <= 0.10": [Fraction(1, 20), Fraction(1, 10)],
    "0.10 < theta < 0.30": [Fraction(1, 5)],
    "theta = 0.30": [Fraction(3, 10)],
    "theta > 0.30": [Fraction(1, 2)],
}


def _events_by_hand(theta):
    """Coverage-failure events whose union contains 'a declared response statement is false'.
    Statements: RESPONDS (L10>0, L30>0), WEAK (L10>0, U30<0), LOW (U10<0, U30<0), RULE6
    (LAF>0, U30<0). A statement is false only if a bound lies on the wrong side of its truth."""
    ev = set()
    t10, t30, taf = theta - Fraction(1, 10), theta - Fraction(3, 10), theta
    stmts = [
        (("L10", "L30"), lambda: theta > Fraction(3, 10)),
        (("L10", "U30"), lambda: Fraction(1, 10) < theta < Fraction(3, 10)),
        (("U10", "U30"), lambda: theta < Fraction(1, 10)),
        (("LAF", "U30"), lambda: 0 < theta < Fraction(3, 10)),
    ]
    truth = {"L10": t10, "U10": t10, "L30": t30, "U30": t30, "LAF": taf}
    for bounds, true in stmts:
        if true():
            continue
        # false statement: some bound's coverage failed (L > 0 with truth <= 0, U < 0 with >= 0)
        fails = [b for b in bounds if (b[0] == "L" and truth[b] <= 0) or (b[0] == "U" and truth[b] >= 0)]
        # a minimal event set: covering failures shared across statements
        ev.add(frozenset(fails))
    # union of all events needed: choose for each false statement one failing bound, minimising
    best = None
    for pick in _choices([sorted(f) for f in ev]):
        s = set(pick)
        if best is None or len(s) < len(best):
            best = s
    return best or set()


def _choices(lists):
    if not lists:
        yield []
        return
    for x in lists[0]:
        for rest in _choices(lists[1:]):
            yield [x] + rest


@pytest.mark.parametrize("region", list(REGIONS))
def test_fw_events_by_hand_at_most_two(region):
    for theta in REGIONS[region]:
        assert len(_events_by_hand(theta)) <= 2


@pytest.mark.parametrize("region", list(REGIONS))
def test_fw_events_implementation_at_most_two(region):
    ug = mod("hwsu_gates")
    for theta in REGIONS[region]:
        n = ug.fw_events(theta)
        assert isinstance(n, int) and 1 <= n <= 2


def test_fw_events_protocol_counts():
    ug = mod("hwsu_gates")
    assert ug.fw_events(Fraction(-1, 2)) == 2
    assert ug.fw_events(Fraction(3, 10)) == 2
    assert ug.fw_events(Fraction(1, 5)) == 2
    assert ug.fw_events(Fraction(1, 2)) == 1


def test_family_error():
    err = 3 * 2 * Fraction(1, 300)
    assert err == Fraction(1, 50) and err <= Fraction(1, 20)
    fe = uc.CONTRACT["outcomes_u2"]["family_error"]
    assert "0.02" in fe and "0.05" in fe and "1/300" in fe
