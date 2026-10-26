"""Author A (job 0119): S3 evaluation, selection, every outcome branch and the licences.

TEST_PLAN §2 `test_a_outcomes.py`; protocol §7.1, §7.2, §5.6 items 3-4 (RC-1, RC-7, R-HWS-1),
DR9. States are planted fixtures ("fixture": true); each record's class and failed list come
from an independent §5.4 classifier written here. The `s3` entries are planted in the shape of
`s3_evaluate` output (API §5.3), which is tested on its own below.
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
LIC = CONTRACT["licences"]
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


def bnd(mean, se=0.001):
    return {"n": 4096, "mean": mean, "sd": se * 64.0, "se": se, "L1": mean - Z1 * se,
            "U1": mean + Z1 * se, "Lw": mean - ZW * se, "Uw": mean + ZW * se}


def my_class(elig, b):
    if elig != "ELIGIBLE":
        return elig, []
    failed = [c for c, q in CRIT if not b[q]["Uw"] >= FLOORS[q]]
    if failed:
        return "EXCLUDED/" + failed[0], failed
    if all(b[q]["L1"] >= FLOORS[q] for _, q in CRIT):
        return "CANDIDATE/CONFIDENT", []
    return ("CANDIDATE/POSSIBLE" if b["D4"]["mean"] >= 0.03 else "CANDIDATE/MARGINAL"), []


def rec(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig="ELIGIBLE", stage="S1"):
    s, p = F(s), F(p)
    b = {"D4": bnd(d4), "GC": bnd(gc), "G4": bnd(g4), "G4A": bnd(g4a)}
    cls, failed = my_class(elig, b)
    dist = (F(CONTRACT["levels"]["index"]["p"][str(p)])
            + F(CONTRACT["levels"]["index"]["sigma"][str(s)]) + (q - 1) + (W != 12))
    tier = 0 if (W, q) == (12, 1) else 1 if (W, q) == (12, 2) else 2
    return {"fixture": True, "key": f"W{W}-q{q}-s{float(s)!r}-p{float(p)!r}", "W": W, "q": q,
            "sigma": str(s), "p": str(p), "tier": tier,
            "changed": int(p != F(1, 5)) + int(s != F(5, 4)) + int(q != 1) + int(W != 12),
            "distance": str(dist), "stage": stage, "n": 4096, "eligibility": elig,
            "bounds": b, "class": cls, "failed": failed, "annotations": []}


def s3e(kind="ordinary", qual=False, below=False, at=False):
    return {"fixture": True, "kind": kind, "ok": True, "qualifies": qual, "below_3x": below,
            "at_3x": at, "criteria_L3": {"C1": qual or at, "C2": True, "C3": True, "C4": True}}


def state(recs, ordinary=(), fallback=(), s3=None, complete=True, fail=None):
    return {"fixture": True, "fail": fail, "complete": complete, "records": Records(recs),
            "finalists": {"ordinary": list(ordinary), "fallback_only": list(fallback)},
            "s3": dict(s3 or {}), "floors": dict(FLOORS)}


FIN = [rec(12, 1, F(5, 4), F(7, 8), stage="S3"), rec(12, 2, F(5, 4), F(1, 5), stage="S3"),
       rec(12, 1, F(3, 2), F(7, 8), stage="S3"), rec(16, 1, F(5, 4), F(7, 8), stage="S3"),
       rec(8, 1, F(5, 4), F(7, 8), stage="S3")]
KEYS = [r["key"] for r in FIN]
SEL_CASES = [  # qualifiers by finalist index -> (outcome, selected index, fallback indices)
    ("T0", (0, 2, 3, 4), "HWS_SELECTED/T0", 0, (2, 3)),
    ("T1", (1, 2, 4), "HWS_SELECTED/T1", 1, (2, 4)),
    ("T2", (3, 4), "HWS_SELECTED/T2", 3, (4,)),
]


def _sel_state(quals, **kw):
    s3 = {k: s3e(qual=i in quals, below=i in quals, at=i in quals) for i, k in enumerate(KEYS)}
    return state(FIN, ordinary=KEYS, s3=s3, **kw)


@pytest.mark.parametrize("name, quals, out, sel, fb", SEL_CASES, ids=[c[0] for c in SEL_CASES])
def test_selected_first_ordinary_qualifier_in_finalist_order(name, quals, out, sel, fb):
    st = _sel_state(quals)
    got = hsel.outcome(st)
    assert got["outcome"] == out
    assert got["selected"] == KEYS[sel]  # no re-ranking on S3 data
    assert list(got["fallback_list"]) == [KEYS[i] for i in fb]
    direct = hsel.selection(st["finalists"], st["s3"])
    assert direct["selected"] == KEYS[sel]
    assert list(direct["fallback_list"]) == [KEYS[i] for i in fb]
    addendum = LIC["HWS_SELECTED_T1_T2_addendum"]
    assert (addendum in got["licence"]) == (name != "T0")
    assert "does not license" in got["licence"]


def test_fail_technical_first_then_inconclusive():
    got = hsel.outcome(_sel_state((0,), fail="NULL"))
    assert got["outcome"].startswith("FAIL_TECHNICAL") and "NULL" in got["outcome"]
    assert got["outcome"] != "FAIL_TECHNICAL/OUTCOME"
    got = hsel.outcome(_sel_state((0,), complete=False))
    assert got["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    assert LIC["INCONCLUSIVE/RESOURCE_OR_AUTHORITY"] in got["licence"]


def test_fallback_only_worlds_give_below_3x_never_selected():
    g1, g2 = rec(12, 1, F(5, 4), F(3, 4), stage="S3"), rec(16, 1, F(2), F(1, 2), stage="S3")
    s3 = {g1["key"]: s3e("fallback_only", below=True, at=True),
          g2["key"]: s3e("fallback_only", below=True)}
    got = hsel.outcome(state([g1, g2], fallback=[g1["key"], g2["key"]], s3=s3))
    assert got["outcome"] == "HWS_BELOW_3X"
    assert got["selected"] is None and list(got["fallback_list"]) == []
    assert set(got["below_3x_worlds"]) == {g1["key"], g2["key"]}
    assert list(got["at_3x_fallback_only"]) == [g1["key"]]
    sel = hsel.selection({"ordinary": [], "fallback_only": [g1["key"], g2["key"]]}, s3)
    assert sel["selected"] is None and list(sel["fallback_list"]) == []


def _below_state(extra=()):
    o1 = rec(12, 1, F(5, 4), F(7, 8), d4=0.0256, stage="S3")  # S3 Uw(D4) 0.0295: EXCLUDED/C1
    o2 = rec(12, 1, F(3, 2), F(7, 8), d4=0.005, stage="S3")
    others = [rec(16, 1, F(5, 4), F(1, 5), d4=0.004), rec(8, 1, F(2), F(1, 2), gc=0.05),
              rec(16, 2, F(3), F(1, 2), d4=0.2, elig="INELIGIBLE/E5")]
    recs = [o1, o2] + others + list(extra)
    s3 = {o1["key"]: s3e(below=True), o2["key"]: s3e()}
    return state(recs, ordinary=[o1["key"], o2["key"]], s3=s3), o1


def test_below_3x_absence_shown():
    st, o1 = _below_state()
    assert st["records"][0]["class"] == "EXCLUDED/C1"
    assert hsel.absence_shown(st["records"])
    got = hsel.outcome(st)
    assert got["outcome"] == "HWS_BELOW_3X" and got["selected"] is None
    assert list(got["below_3x_worlds"]) == [o1["key"]] and got["absence_3x_shown"]
    assert "3x absence among all evaluated worlds: shown" in got["licence"]


def test_below_3x_absence_not_shown():
    marg = rec(16, 3, F(5, 4), F(1, 2), d4=0.027)
    assert marg["class"] == "CANDIDATE/MARGINAL"
    st, _ = _below_state([marg])
    assert not hsel.absence_shown(st["records"])
    got = hsel.outcome(st)
    assert got["outcome"] == "HWS_BELOW_3X" and not got["absence_3x_shown"]
    assert "3x absence among all evaluated worlds: not shown" in got["licence"]


def test_absence_shown_ignores_ineligible_worlds():
    recs = [rec(12, 1, F(5, 4), F(1, 5), d4=0.01),
            rec(12, 1, F(2), F(1, 2), elig="INELIGIBLE/E5")]  # bounds would pass under Uw
    assert hsel.absence_shown(Records(recs))
    assert not hsel.absence_shown(Records(recs + [rec(16, 1, F(3), F(1, 2))]))


def _nwc_state(extra):
    o1 = rec(12, 1, F(5, 4), F(7, 8), d4=0.005, stage="S3")
    base = [o1, rec(16, 1, F(5, 4), F(1, 5), d4=0.004)]
    return state(base + extra, ordinary=[o1["key"]], s3={o1["key"]: s3e()})


def test_no_world_confirmed_needs_an_unresolved_world():
    m1 = rec(16, 1, F(5, 2), F(1, 2), d4=0.027)  # MARGINAL: passes E1-E6, Uw passes C1-C4
    got = hsel.outcome(_nwc_state([m1]))
    assert got["outcome"] == "HWS_NO_WORLD_CONFIRMED"
    assert list(got["unresolved"]) == [m1["key"]]
    assert m1["key"] in got["licence"] and "not" in got["licence"]


def test_ineligible_world_with_passing_bounds_is_not_unresolved():
    stale = rec(16, 1, F(5, 2), F(1, 2), elig="INELIGIBLE/E5")  # RC-7
    got = hsel.outcome(_nwc_state([stale]))
    assert got["outcome"] == "HWS_NO_SUITABLE_WORLD/HEADROOM"
    assert list(got["unresolved"]) == []


HEAD = [rec(16, 1, F(5, 4), F(1, 5), d4=0.01), rec(16, 1, F(3, 2), F(1, 5), d4=0.02, gc=0.05),
        rec(8, 1, F(2), F(1, 2), d4=0.004, elig="INELIGIBLE/E5")]


def test_no_suitable_world_headroom():
    assert [r["class"] for r in HEAD[:2]] == ["EXCLUDED/C1", "EXCLUDED/C1"]
    got = hsel.outcome(state(HEAD))
    assert got["outcome"] == "HWS_NO_SUITABLE_WORLD/HEADROOM"
    assert got["selected"] is None and list(got["unresolved"]) == []
    assert got["max_D4"]["key"] == HEAD[1]["key"] and got["max_D4"]["value"] == 0.02
    assert "HEADROOM" in got["licence"] and HEAD[1]["key"] in got["licence"]
    assert "It does not license" in got["licence"]


def test_no_suitable_world_filter():
    c2 = rec(16, 2, F(5, 4), F(1, 2), d4=0.05, gc=0.05)  # eligible, excluded by C2 only
    assert c2["class"] == "EXCLUDED/C2"
    assert hsel.outcome(state(HEAD + [c2]))["outcome"] == "HWS_NO_SUITABLE_WORLD/FILTER"
    inel = [rec(16, 1, F(5, 4), F(1, 5), d4=0.01, elig="INELIGIBLE/E5"),
            rec(16, 2, F(3), F(1, 5), d4=0.001, elig="INELIGIBLE/E5")]
    got = hsel.outcome(state(inel))  # HEADROOM with no eligible world becomes FILTER
    assert got["outcome"] == "HWS_NO_SUITABLE_WORLD/FILTER"


def test_paused_search_never_gets_the_no_world_licence():
    got = hsel.outcome(state(HEAD, complete=False))
    assert got["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    st, _ = _below_state()
    st["complete"] = False
    assert hsel.outcome(st)["outcome"] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


def test_outcome_fallthrough_is_fail_technical_outcome():
    # API-AMBIGUITY: API.md names the fallthrough (choice 35) but no state that reaches it;
    # a world neither INELIGIBLE, EXCLUDED nor unresolved (class NOT_RUN) is used here,
    # and both a returned outcome and a raised HwsStop are accepted.
    odd = dict(rec(16, 1, F(5, 4), F(1, 5), d4=0.01), eligibility="NOT_RUN", **{"class": "NOT_RUN"})
    try:
        got = hsel.outcome(state([odd]))["outcome"]
    except hw.HwsStop as err:
        got = err.status
    assert got == "FAIL_TECHNICAL/OUTCOME"


def _s3rec(d4=0.03, gc=0.10, g4=0.0078, g4a=0.004, elig="ELIGIBLE"):
    # API-AMBIGUITY: the rec_s3 shape is not fixed; eligibility "ELIGIBLE" (E1-E5 passed on
    # the S3 rows) with E6 passed, and an L3 per criterion.
    b = {q: dict(bnd(v), L3=v) for q, v in (("D4", d4), ("GC", gc), ("G4", g4), ("G4A", g4a))}
    return {"fixture": True, "eligibility": elig, "e6_ok": True, "e6": {"ok": True},
            "bounds": b, "L3": {q: b[q]["L3"] for q in b}}


S3_CASES = [  # (kind, record kwargs, qualifies, below_3x, at_3x)
    ("ordinary", {}, True, True, True),  # every L3 exactly at its floor
    ("ordinary", {"d4": 0.02}, False, True, False),
    ("ordinary", {"d4": float(np.nextafter(0.02, 0.0))}, False, False, False),
    ("ordinary", {"gc": float(np.nextafter(0.1, 0.0))}, False, False, False),
    ("ordinary", {"g4a": float(np.nextafter(0.004, 0.0))}, False, False, False),
    ("fallback_only", {"d4": 0.031}, False, True, True),
    ("fallback_only", {"d4": 0.025}, False, True, False),
    ("ordinary", {"elig": "INELIGIBLE/E5"}, False, False, False),
]


@pytest.mark.parametrize("kind, kw, qual, below, at", S3_CASES)
def test_s3_evaluate(kind, kw, qual, below, at):
    got = hsel.s3_evaluate(_s3rec(**kw), FLOORS, kind)
    assert (bool(got["qualifies"]), bool(got["below_3x"]), bool(got["at_3x"])) == (qual, below,
                                                                                     at)
    if not kw.get("elig"):
        assert set(got["criteria_L3"]) == {"C1", "C2", "C3", "C4"}


SEL_FILL = {"W": 12, "q": 1, "sigma": 1.5, "p": 0.875, "L3_D4": 0.0312, "L3_GC": 0.21,
            "L3_G4": 0.0110, "g4_star": 0.0091, "L3_G4A": 0.0060, "g4A_star": 0.0042}


@pytest.mark.parametrize("tier", [0, 1, 2])
def test_licence_selected(tier):
    text = hsel.licence(f"HWS_SELECTED/T{tier}", SEL_FILL)
    base = LIC["HWS_SELECTED"].format(**SEL_FILL)
    assert text.startswith(base)
    assert "In world w* = (12, 1, 1.5, 0.875)" in text and "0.0312 >= 0.03" in text
    assert "(1) that any model learns it" in text and "(6) anything outside the grid" in text
    if tier == 0:
        assert text == base
    else:
        assert LIC["HWS_SELECTED_T1_T2_addendum"] in text


def test_licence_other_outcomes():
    fill = {"worlds": "W16-q1-s2.0-p0.875", "fallback_at_3x": "none", "absence": "not shown"}
    assert hsel.licence("HWS_BELOW_3X", fill) == LIC["HWS_BELOW_3X"].format(**fill)
    fill = {"unresolved": "W16-q1-s1.25-p0.5"}
    text = hsel.licence("HWS_NO_WORLD_CONFIRMED", fill)
    assert text == LIC["HWS_NO_WORLD_CONFIRMED"].format(**fill)
    fill = {"z_w": 3.94, "sub_reason": "HEADROOM", "max_D4": 0.021,
            "max_D4_key": "W16-q1-s1.25-p0.2"}
    text = hsel.licence("HWS_NO_SUITABLE_WORLD/HEADROOM", fill)
    assert text == LIC["HWS_NO_SUITABLE_WORLD"].format(**fill)
    assert "It does not license" in text and "Sub-reason HEADROOM" in text
    for head in ("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", "FAIL_TECHNICAL/NULL"):
        assert "No scientific statement is licensed." in hsel.licence(head, {})
