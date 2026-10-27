"""Author A (job 0119): floors, criteria, eligibility, classes, ranking, annotations, finalists,
the X1 trigger and the S2 worklist (TEST_PLAN §2 `test_a_classify.py`; protocol §5.1-§5.6, §6.2,
§7.3; RC-1, RC-6, R-HWS-1). Records are planted fixtures; their class and failed list come from
an independent classifier written here (§5.4), never from the module under test.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
HWS_DIR = str(REPO / "tools" / "hws")
if HWS_DIR not in sys.path:
    sys.path.insert(0, HWS_DIR)

import hws_worlds as hw  # noqa: E402
import hws_select as hsel  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
LEV = CONTRACT["levels"]
P_IDX = {Fraction(k): Fraction(v) for k, v in LEV["index"]["p"].items()}
S_IDX = {Fraction(k): Fraction(v) for k, v in LEV["index"]["sigma"].items()}
P_LEV = [Fraction(x) for x in LEV["p"]]
S_LEV = [Fraction(x) for x in LEV["sigma"]]
P_MID = {(Fraction(a), Fraction(b)): Fraction(m) for a, b, m in LEV["s2_p_edges"]}
S_MID = {(Fraction(a), Fraction(b)): Fraction(m) for a, b, m in LEV["s2_sigma_edges"]}
Z1 = NormalDist().inv_cdf(float(1 - Fraction(1, 100)))
ZW = NormalDist().inv_cdf(float(1 - Fraction(1, 24640)))
FLOORS = {"D4": 0.03, "GC": 0.10, "G4": 0.0078, "G4A": 0.004}
CRIT = (("C1", "D4"), ("C2", "GC"), ("C3", "G4"), ("C4", "G4A"))
F = Fraction


class Records(list):
    """API-AMBIGUITY: `records` may be read as a list of records or as {key: record}; this
    container answers both readings (iteration yields the records)."""

    def __init__(self, recs):
        super().__init__(recs)
        self.by_key = {r["key"]: r for r in recs}

    def keys(self):
        return self.by_key.keys()

    def values(self):
        return self.by_key.values()

    def items(self):
        return self.by_key.items()

    def get(self, k, default=None):
        return self.by_key.get(k, default)

    def __getitem__(self, i):
        if isinstance(i, str):
            return self.by_key[i]
        return i if isinstance(i, dict) else list.__getitem__(self, i)

    def __contains__(self, k):
        return k in self.by_key if isinstance(k, str) else list.__contains__(self, k)


def key_of(W, q, s, p):
    return f"W{W}-q{q}-s{float(s)!r}-p{float(p)!r}"


def tier_of(W, q):
    return 0 if (W, q) == (12, 1) else 1 if (W, q) == (12, 2) else 2


def changed_of(W, q, s, p):
    return int(p != F(1, 5)) + int(s != F(5, 4)) + int(q != 1) + int(W != 12)


def dist_of(W, q, s, p):
    return P_IDX[F(p)] + S_IDX[F(s)] + (q - 1) + (0 if W == 12 else 1)


def bnd(mean, se=0.001):
    return {"n": 4096, "mean": mean, "sd": se * 64.0, "se": se, "L1": mean - Z1 * se,
            "U1": mean + Z1 * se, "Lw": mean - ZW * se, "Uw": mean + ZW * se}


def my_class(elig, b, fl=FLOORS):
    """Protocol §5.4, written independently."""
    if elig != "ELIGIBLE":
        return elig, []
    failed = [c for c, q in CRIT if not b[q]["Uw"] >= fl[q]]
    if failed:
        return "EXCLUDED/" + failed[0], failed
    if all(b[q]["L1"] >= fl[q] for _, q in CRIT):
        return "CANDIDATE/CONFIDENT", []
    return ("CANDIDATE/POSSIBLE" if b["D4"]["mean"] >= 0.03 else "CANDIDATE/MARGINAL"), []


def rec(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig="ELIGIBLE", over=None, se=0.001):
    s, p = F(s), F(p)
    b = {"D4": bnd(d4, se), "GC": bnd(gc, se), "G4": bnd(g4, se), "G4A": bnd(g4a, se)}
    for name, values in (over or {}).items():
        b[name].update(values)
    cls, failed = my_class(elig, b)
    return {"fixture": True, "key": key_of(W, q, s, p), "W": W, "q": q, "sigma": str(s),
            "p": str(p), "tier": tier_of(W, q), "changed": changed_of(W, q, s, p),
            "distance": str(dist_of(W, q, s, p)), "stage": "S1", "n": 4096,
            "eligibility": elig, "bounds": b, "class": cls, "failed": failed, "annotations": []}


def my_rank(r):
    b = r["bounds"]
    return (0 if r["class"] == "CANDIDATE/CONFIDENT" else 1, r["tier"], r["changed"],
            F(r["distance"]), -b["G4"]["L1"], r["key"])


def test_floors_both_ways():
    low = hsel.floors(0.005, 0.002)
    assert low == {"D4": 0.03, "GC": 0.10, "G4": 0.0078, "G4A": 0.002}
    high = hsel.floors(0.0123, 0.0045)
    assert high["G4"] == 0.0123 and high["G4A"] == 0.0045
    assert hsel.floors(0.0078, 0.001)["G4"] == float(F(39, 5000))


@pytest.mark.parametrize("which", ["L1", "Uw", "L3", "Lw"])
def test_criteria_equality_passes(which):
    bounds = {q: {which: FLOORS[q]} for _, q in CRIT}
    assert all(bool(v) for v in hsel.criteria(bounds, FLOORS, which).values())
    for c, q in CRIT:
        low = {k: dict(v) for k, v in bounds.items()}
        low[q][which] = float(np.nextafter(FLOORS[q], 0.0))
        got = hsel.criteria(low, FLOORS, which)
        assert [k for k, _ in CRIT if not got[k]] == [c]


def test_eligibility_order_and_e6():
    assert hsel.eligibility("INELIGIBLE/E3", False, True) == "INELIGIBLE/E3"
    assert hsel.eligibility("PASS", False, True) == "INELIGIBLE/E5"
    assert hsel.eligibility("PASS", True, True) == "ELIGIBLE"
    for status in ("PASS", "INELIGIBLE/E2"):
        with pytest.raises(hw.HwsStop) as err:  # E6 is never a scientific exclusion
            hsel.eligibility(status, True, False)
        assert err.value.status == "FAIL_TECHNICAL/E6"


CASES = [
    ("E1", dict(elig="INELIGIBLE/E1"), "INELIGIBLE/E1", None),
    ("E4", dict(elig="INELIGIBLE/E4"), "INELIGIBLE/E4", None),
    ("E5", dict(elig="INELIGIBLE/E5", d4=0.2), "INELIGIBLE/E5", None),
    ("C1", dict(d4=0.01), "EXCLUDED/C1", ["C1"]),
    ("C2C4", dict(gc=0.05, g4a=-0.001), "EXCLUDED/C2", ["C2", "C4"]),
    ("all", dict(d4=0.0, gc=0.0, g4=0.0, g4a=-0.01), "EXCLUDED/C1", ["C1", "C2", "C3", "C4"]),
    ("conf", dict(), "CANDIDATE/CONFIDENT", []),
    ("poss_eq", dict(d4=0.03), "CANDIDATE/POSSIBLE", None),
    ("poss_g4", dict(g4=0.009), "CANDIDATE/POSSIBLE", None),
    ("marg", dict(d4=float(np.nextafter(0.03, 0.0))), "CANDIDATE/MARGINAL", None),
]


@pytest.mark.parametrize("name, kw, cls, failed", CASES, ids=[c[0] for c in CASES])
def test_classify_every_class(name, kw, cls, failed):
    r = rec(12, 1, F(5, 4), F(1, 5), **kw)
    assert r["class"] == cls  # the independent classifier agrees with the planted answer
    got = hsel.classify({"eligibility": r["eligibility"], "bounds": r["bounds"]}, FLOORS)
    assert got["class"] == cls
    if failed is not None:
        assert list(got["failed"]) == failed


def test_classify_random_looks_match_the_protocol():
    rng = np.random.default_rng(119201)
    for _ in range(300):
        r = rec(12, 1, F(5, 4), F(1, 5), d4=rng.uniform(0.0, 0.06), gc=rng.uniform(0.05, 0.2),
                g4=rng.uniform(0.0, 0.02), g4a=rng.uniform(0.0, 0.01),
                se=rng.uniform(0.0005, 0.003))
        got = hsel.classify({"eligibility": "ELIGIBLE", "bounds": r["bounds"]}, FLOORS)
        assert got["class"] == r["class"]
        if r["class"].startswith("EXCLUDED"):
            assert list(got["failed"]) == r["failed"]


@pytest.mark.parametrize("q", ["D4", "GC", "G4", "G4A"])
def test_classify_nan_bound_is_technical(q):
    # API-AMBIGUITY: API.md does not name the function that rejects a NaN bound; TEST_PLAN
    # and DR9 require FAIL_TECHNICAL, so classify must raise HwsStop FAIL_TECHNICAL/*.
    r = rec(12, 1, F(5, 4), F(1, 5), over={q: {"Uw": float("nan"), "L1": float("nan")}})
    with pytest.raises(hw.HwsStop) as err:
        hsel.classify({"eligibility": "ELIGIBLE", "bounds": r["bounds"]}, FLOORS)
    assert err.value.status.startswith("FAIL_TECHNICAL")


def test_world_helpers():
    w = hw.World(16, 3, F(3), F(15, 16))
    assert hw.tier(hw.W0) == 0 and hw.tier(hw.World(12, 2, F(5, 4), F(1, 5))) == 1
    assert hw.tier(hw.World(8, 1, F(5, 4), F(1, 5))) == 2 and hw.tier(w) == 2
    with pytest.raises(ValueError):
        hw.tier(hw.World(12, 3, F(5, 4), F(1, 5)))
    assert hw.changed_factors(hw.W0) == 0 and hw.changed_factors(w) == 4
    assert hw.changed_factors(hw.World(12, 1, F(3, 2), F(1, 5))) == 1  # sigma counts
    assert hw.distance(hw.W0) == 0 and hw.distance(w) == F(11)
    for s, p, d in ((F(5, 4), F(3, 8), F(1, 2)), (F(11, 8), F(1, 5), F(1, 2)),
                    (F(7, 2), F(31, 32), F(10)), (F(4), F(23, 24), F(21, 2))):
        assert hw.distance(hw.World(12, 1, s, p)) == d
    assert hw.W0.key == "W12-q1-s1.25-p0.2" and w.key == "W16-q3-s3.0-p0.9375"


RANK_PAIRS = [  # (first, second): first ranks strictly before second
    ("class", rec(16, 1, F(5, 4), F(1, 5)), rec(12, 1, F(5, 4), F(1, 2), d4=0.035, se=0.003)),
    ("tier", rec(12, 1, F(3), F(15, 16)), rec(12, 2, F(5, 4), F(1, 5))),
    ("changed_sigma", rec(12, 1, F(5, 4), F(15, 16)), rec(12, 1, F(3, 2), F(1, 2))),
    ("half_step", rec(12, 1, F(7, 4), F(1, 5)), rec(12, 1, F(5, 4), F(3, 4), g4=0.09)),
    ("half_step_p", rec(12, 1, F(5, 4), F(3, 8)), rec(12, 1, F(5, 4), F(1, 2))),
    ("g4", rec(12, 1, F(3, 2), F(1, 5), g4=0.06), rec(12, 1, F(5, 4), F(1, 2))),
    ("key", rec(12, 1, F(5, 4), F(1, 2)), rec(12, 1, F(3, 2), F(1, 5))),
    ("key_str", rec(16, 1, F(5, 4), F(1, 5)), rec(8, 1, F(5, 4), F(1, 5))),
]


@pytest.mark.parametrize("name, first, second", RANK_PAIRS, ids=[p[0] for p in RANK_PAIRS])
def test_rank_key_every_tie_break_level(name, first, second):
    assert my_rank(first) < my_rank(second)
    assert hsel.rank_key(first) < hsel.rank_key(second)
    assert sorted([second, first], key=hsel.rank_key)[0] is first


def test_rank_key_tuple():
    r = rec(12, 1, F(7, 4), F(1, 5), g4=0.02)
    assert tuple(hsel.rank_key(r)) == (0, 0, 1, F(3, 2), -r["bounds"]["G4"]["L1"], r["key"])


def test_annotations_boundaries():
    def ann(lw, uw):
        return set(hsel.annotations({"mean": (lw + uw) / 2, "Lw": lw, "Uw": uw}))

    c, s = "ORACLE_POSITIVE_BELOW_C_MARGIN", "ORACLE_POSITIVE_BELOW_SWEEP_REQUIREMENT"
    assert ann(0.001, 0.009) == {c, s}
    assert ann(0.005, 0.005) == {c, s}  # Lw = Uw
    assert ann(0.0, 0.009) == set()  # Lw must be > 0
    assert ann(0.002, 0.01) == {s}  # Uw = 0.01 is not below the C margin
    assert ann(0.002, float(np.nextafter(0.03, 0.0))) == {s}
    assert ann(0.002, 0.03) == set()


def _tier0_tier1_records():
    out = []
    for si, s in enumerate(S_LEV):
        for pi, p in enumerate(P_LEV):
            d4 = 0.05 if (si + pi) % 2 == 0 else 0.028  # CONFIDENT / MARGINAL
            out.append(rec(12, 1, s, p, d4=d4, g4=0.02 + 0.001 * pi))
            out.append(rec(12, 2, s, p, d4=0.035, se=0.003, g4=0.03 - 0.001 * si))  # POSSIBLE
    return out


def test_finalists_first_16_ordinary_never_marginal():
    recs = _tier0_tier1_records()
    assert {r["class"] for r in recs} == {"CANDIDATE/CONFIDENT", "CANDIDATE/MARGINAL",
                                          "CANDIDATE/POSSIBLE"}
    cand = [r for r in recs if r["class"] in ("CANDIDATE/CONFIDENT", "CANDIDATE/POSSIBLE")]
    expect = [r["key"] for r in sorted(cand, key=my_rank)[:16]]
    got = hsel.finalists(Records(recs))
    assert list(got["ordinary"]) == expect and list(got["fallback_only"]) == []


def test_marginal_never_fills_an_ordinary_slot():
    recs = [rec(12, 1, F(5, 4), F(1, 5)), rec(12, 1, F(3, 2), F(1, 2))]
    recs += [rec(12, 1, F(2), p, d4=0.028) for p in P_LEV[:3]]
    got = hsel.finalists(Records(recs))
    assert list(got["ordinary"]) == [r["key"] for r in sorted(recs[:2], key=my_rank)]
    assert list(got["fallback_only"]) == []


def test_fallback_only_2x_set_membership():
    recs = [
        rec(16, 1, F(5, 4), F(1, 5), d4=0.012, over={"D4": {"Uw": 0.02}}),  # equality: in
        rec(16, 1, F(3, 2), F(1, 5), d4=0.012, over={"D4": {"Uw": float(np.nextafter(0.02, 0))}}),
        rec(16, 1, F(2), F(1, 5), d4=0.021, g4=-0.001),  # EXCLUDED/C1 and C3: out
        rec(16, 1, F(5, 2), F(1, 5), d4=0.021, elig="INELIGIBLE/E5"),  # not eligible: out
        rec(16, 1, F(3), F(1, 5), d4=0.027),  # MARGINAL: only the 2x set may hold it
        rec(16, 2, F(5, 4), F(1, 5), d4=0.021),  # EXCLUDED/C1, Uw(D4) 0.0249: in
    ]
    assert recs[0]["class"] == recs[1]["class"] == recs[5]["class"] == "EXCLUDED/C1"
    assert recs[4]["class"] == "CANDIDATE/MARGINAL"
    got = hsel.finalists(Records(recs))
    assert list(got["ordinary"]) == []
    assert list(got["fallback_only"]) == [recs[4]["key"], recs[5]["key"], recs[0]["key"]]


def test_fallback_only_2x_set_cap_and_ties():
    worlds = [(s, p) for s in S_LEV for p in P_LEV][:18]
    means = [0.02 + 0.0002 * k for k in range(18)]
    means[2] = means[1]  # an exact tie across the 16th place
    recs = [rec(16, 1, s, p, d4=m) for (s, p), m in zip(worlds, means)]
    assert all(r["class"] == "EXCLUDED/C1" for r in recs)
    order = sorted(recs, key=lambda r: (-r["bounds"]["D4"]["mean"], r["key"]))
    got = hsel.finalists(Records(recs))
    assert list(got["fallback_only"]) == [r["key"] for r in order[:16]]


X1_CASES = [  # (top world, add_p, add_sigma)
    ((12, 1, F(5, 4), F(15, 16)), True, False),
    ((16, 2, F(3), F(1, 2)), False, True),
    ((8, 1, F(3), F(15, 16)), True, True),
    ((12, 1, F(2), F(1, 2)), False, False),
]


@pytest.mark.parametrize("top, add_p, add_s", X1_CASES)
def test_x1_trigger_condition(top, add_p, add_s):
    base = [rec(12, 1, F(5, 4), F(1, 5), d4=0.005), rec(16, 1, F(2), F(1, 2), d4=0.006)]
    recs = base + [rec(*top, d4=0.012)]
    assert all(r["class"].startswith("EXCLUDED") for r in recs)  # eligible, no candidate
    got = hsel.x1_trigger(Records(recs))
    assert bool(got["fire"]) == (add_p or add_s)
    if add_p or add_s:
        assert got["world"] == key_of(*top)
        assert bool(got["add_p"]) == add_p and bool(got["add_sigma"]) == add_s
    cand = recs + [rec(16, 3, F(5, 4), F(1, 5), d4=0.028)]  # one MARGINAL candidate
    assert not hsel.x1_trigger(Records(cand))["fire"]


def test_x1_trigger_ties_ineligible_and_empty():
    tie = [rec(12, 1, F(5, 4), F(15, 16), d4=0.012), rec(12, 1, F(3, 2), F(1, 5), d4=0.012)]
    got = hsel.x1_trigger(Records(tie))
    assert got["fire"] and got["world"] == "W12-q1-s1.25-p0.9375"  # ascending key wins
    tie2 = [rec(12, 1, F(5, 4), F(1, 2), d4=0.012), rec(12, 1, F(3), F(1, 5), d4=0.012)]
    assert not hsel.x1_trigger(Records(tie2))["fire"]
    inel = [rec(12, 1, F(5, 4), F(15, 16), d4=0.02, elig="INELIGIBLE/E5"),
            rec(12, 1, F(2), F(1, 2), d4=0.012)]
    assert not hsel.x1_trigger(Records(inel))["fire"]
    none = [rec(12, 1, F(5, 4), F(15, 16), d4=0.02, elig="INELIGIBLE/E5")]
    got = hsel.x1_trigger(Records(none))
    assert not got["fire"] and got["world"] is None


def _keys(worlds):
    return [w.key for w in worlds]


def test_s2_worklist_edges_lowest_tier():
    S, P = F(5, 4), F(1, 5)
    recs = [rec(12, 1, S, P, d4=0.005), rec(12, 1, S, F(1, 2), d4=0.028),
            rec(12, 1, F(3, 2), P, d4=0.005), rec(12, 1, F(3, 2), F(1, 2), d4=0.031),
            rec(12, 1, S, F(3, 4), d4=0.005), rec(12, 1, F(2), F(1, 2), elig="INELIGIBLE/E5"),
            rec(12, 1, F(5, 2), P), rec(12, 2, S, P, d4=0.005), rec(12, 2, S, F(1, 2))]
    assert [r["class"] for r in recs[:4]] == ["EXCLUDED/C1", "CANDIDATE/MARGINAL",
                                              "EXCLUDED/C1", "CANDIDATE/POSSIBLE"]
    expect = [key_of(12, 1, S, F(3, 8)), key_of(12, 1, S, F(2, 3)), key_of(12, 1, F(3, 2), F(3, 8))]
    assert _keys(hsel.s2_worklist(Records(recs))) == expect
    excl = [r for r in recs if not r["class"].startswith("CANDIDATE")]
    assert list(hsel.s2_worklist(Records(excl))) == []  # no candidate: S2 does not fire


def test_s2_worklist_uses_x1_levels_that_ran():
    recs = [rec(12, 1, F(5, 4), F(15, 16)), rec(12, 1, F(5, 4), F(31, 32), d4=0.005),
            rec(12, 1, F(3), F(1, 5)), rec(12, 1, F(7, 2), F(1, 5), d4=0.005)]
    mids = [(12, 1, F(5, 4), F(23, 24)), (12, 1, F(13, 4), F(1, 5))]
    expect = sorted(mids, key=lambda w: (changed_of(*w), dist_of(*w), key_of(*w)))
    assert _keys(hsel.s2_worklist(Records(recs))) == [key_of(*w) for w in expect]


def test_s2_worklist_cap_40_by_changed_distance_key():
    recs, mids = [], set()
    for W, q in ((8, 1), (16, 1), (16, 2), (16, 3)):
        for si, s in enumerate(S_LEV):
            for pi, p in enumerate(P_LEV):
                recs.append(rec(W, q, s, p, d4=0.05 if (si + pi) % 2 == 0 else 0.005))
                if pi + 1 < len(P_LEV):
                    mids.add((W, q, s, P_MID[(p, P_LEV[pi + 1])]))
                if si + 1 < len(S_LEV):
                    mids.add((W, q, S_MID[(s, S_LEV[si + 1])], p))
    assert len(mids) == 160
    order = [key_of(*w) for w in sorted(mids, key=lambda w: (changed_of(*w), dist_of(*w),
                                                                key_of(*w)))]
    assert _keys(hsel.s2_worklist(Records(recs))) == order[:40]
    assert _keys(hsel.s2_worklist(Records(recs), cap=5)) == order[:5]


def test_x1_worlds_counts_and_order():
    cells = [tuple(c) for c in CONTRACT["grid"]["eligible_cells_expected"]]
    grid_keys = {w.key for w in hw.grid()}
    for add_p, add_s, n in ((True, False, 30), (False, True, 60), (True, True, 102)):
        ws = hw.x1_worlds(add_p, add_s, cells)
        assert len(ws) == n and not ({w.key for w in ws} & grid_keys)
        assert list(ws) == sorted(ws, key=lambda w: (w.W, w.q, w.sigma, w.p))
    assert len(hw.x1_worlds(True, True, [(12, 1)])) == 6 * 7 - 25
