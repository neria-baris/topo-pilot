"""Author A (job 0176): decision maths and the POSITIVE_BELOW_MARGIN annotation.

Protocol HWSC §5 decision, §6.1 annotation (RC-6); DRC5. API.md §6
(`positive_below_margin`, `annotations`), §12.1-§12.2; K4b API §8
(`model_status`, `overall`). Written from the specification only.
"""

from __future__ import annotations

import copy
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_bind as cb  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import k4b_stats  # noqa: E402

M = Fraction(1, 100)
J1, J2, J3 = 620301, 620302, 620303
MODELS = (J1, J2, J3)
F_SMALL = Fraction(1, 10**9) + Fraction(1, 10**12)


@pytest.fixture
def bound():
    with cb.bound_stage_c() as info:
        yield info


def ref_status(L, U, Fm, Fp):
    """Independent K4B §8.1 rule in exact rationals (L <= U assumed)."""
    lo, up = Fraction(float(L)), Fraction(float(U))

    def st(fm, fp):
        if lo - fm > M:
            return "SUPPORT"
        if up + fp < M and lo - fm > -M:
            return "EXCLUDE"
        return "UNRESOLVED"

    s, s0 = st(Fraction(Fm), Fraction(Fp)), st(0, 0)
    if s == "UNRESOLVED" and s0 != "UNRESOLVED":
        s = "UNRESOLVED/NUMERICAL"
    labels = ["NEGATIVE_ALIGNMENT"] if up + Fraction(Fp) < -M else []
    return s, labels


def ms(L, U, Fm, Fp):
    return k4b_stats.model_status(L, U, Fm, Fp)


def lower_at(target, L):
    """F_minus such that Fraction(L) - F_minus == target exactly (F_minus > 0)."""
    F = Fraction(float(L)) - target
    assert F > 0
    return F


def upper_at(target, U):
    """F_plus such that Fraction(U) + F_plus == target exactly (F_plus > 0)."""
    F = target - Fraction(float(U))
    assert F > 0
    return F


# ---------------------------------------------------------------- model_status


def test_bound_constants(bound):
    assert k4b_stats.MODELS == cc.MASTERS == MODELS
    assert cc.M == M == Fraction(1, 100)


def test_support_and_exclude_basic(bound):
    assert ms(0.02, 0.03, F_SMALL, F_SMALL)["status"] == "SUPPORT"
    assert ms(0.0, 0.005, F_SMALL, F_SMALL)["status"] == "EXCLUDE"
    assert ms(0.0, 0.02, F_SMALL, F_SMALL)["status"] == "UNRESOLVED"


def test_support_boundary_is_unresolved(bound):
    L = 0.01 + 1e-9
    Fm = lower_at(M, L)
    assert Fraction(L) - Fm == M
    r = ms(L, 0.05, Fm, F_SMALL)
    assert r["status"] not in ("SUPPORT", "EXCLUDE")
    # with F = 0 the same L would be SUPPORT, so F alone blocks
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    # one ulp higher in L clears the margin
    L2 = math.nextafter(L, math.inf)
    assert ms(L2, 0.05, Fm, F_SMALL)["status"] == "SUPPORT"


def test_exclude_upper_boundary_is_unresolved(bound):
    U = 0.01 - 1e-9
    Fp = upper_at(M, U)
    assert Fraction(U) + Fp == M
    r = ms(0.0, U, F_SMALL, Fp)
    assert r["status"] not in ("SUPPORT", "EXCLUDE")
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    U2 = math.nextafter(U, -math.inf)
    assert ms(0.0, U2, F_SMALL, Fp)["status"] == "EXCLUDE"


def test_exclude_lower_side_boundary(bound):
    L = -0.01 + 1e-9
    Fm = lower_at(-M, L)
    assert Fraction(L) - Fm == -M
    r = ms(L, 0.0, Fm, F_SMALL)
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    L2 = math.nextafter(L, math.inf)
    assert ms(L2, 0.0, Fm, F_SMALL)["status"] == "EXCLUDE"


def test_unresolved_numerical_when_f_alone_blocks(bound):
    Fm = Fp = Fraction(1, 10**9)
    r = ms(0.01 + 5e-10, 0.02, Fm, Fp)
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    assert r["status_without_F"] == "SUPPORT"
    r = ms(0.0, 0.01 - 5e-10, Fm, Fp)
    assert r["status"] == "UNRESOLVED/NUMERICAL"
    assert r["status_without_F"] == "EXCLUDE"
    r = ms(0.0, 0.02, Fm, Fp)
    assert r["status"] == "UNRESOLVED"
    assert r["status_without_F"] == "UNRESOLVED"


def test_negative_alignment_label(bound):
    r = ms(-0.04, -0.02, F_SMALL, F_SMALL)
    assert "NEGATIVE_ALIGNMENT" in r["labels"]
    assert r["status"] == "UNRESOLVED"
    U = -0.01 - 1e-9
    Fp = upper_at(-M, U)
    assert Fraction(U) + Fp == -M
    r = ms(-0.04, U, F_SMALL, Fp)
    assert "NEGATIVE_ALIGNMENT" not in r["labels"]  # strict: equality is not a label
    r = ms(-0.04, math.nextafter(U, -math.inf), F_SMALL, Fp)
    assert "NEGATIVE_ALIGNMENT" in r["labels"]


def test_random_grid_matches_reference_and_exclusive(bound):
    rnd = random.Random(20261029)
    pts = [-0.03, -0.0100000001, -0.01, -0.0099999999, 0.0, 0.0099999999,
           0.01, 0.0100000001, 0.03]
    for _ in range(400):
        a = rnd.choice(pts) + rnd.uniform(-2e-9, 2e-9) * rnd.choice((0, 1))
        b = rnd.choice(pts) + rnd.uniform(-2e-9, 2e-9) * rnd.choice((0, 1))
        L, U = min(a, b), max(a, b)
        Fm = Fraction(rnd.randint(0, 3), 10**9)
        Fp = Fraction(rnd.randint(0, 3), 10**9)
        r = ms(L, U, Fm, Fp)
        s, labels = ref_status(L, U, Fm, Fp)
        assert r["status"] == s, (L, U, Fm, Fp)
        assert ("NEGATIVE_ALIGNMENT" in r["labels"]) == bool(labels)
        assert r["status"] != "SUPPORT" or Fraction(U) + Fp >= M  # never both


# --------------------------------------------------------------------- overall


@pytest.mark.parametrize("statuses, expected", [
    (("SUPPORT",) * 3, "SUPPORT"),
    (("EXCLUDE",) * 3, "EXCLUSION"),
    (("SUPPORT", "EXCLUDE", "UNRESOLVED"), "MIXED"),
    (("SUPPORT", "SUPPORT", "UNRESOLVED"), "MIXED"),
    (("EXCLUDE", "EXCLUDE", "UNRESOLVED/NUMERICAL"), "MIXED"),
    (("SUPPORT", "SUPPORT", "EXCLUDE"), "MIXED"),
    (("UNRESOLVED",) * 3, "INCONCLUSIVE"),
    (("UNRESOLVED", "UNRESOLVED/NUMERICAL", "UNRESOLVED"), "INCONCLUSIVE/NUMERICAL"),
    (("UNRESOLVED/NUMERICAL",) * 3, "INCONCLUSIVE/NUMERICAL"),
])
def test_overall_stage_c_keys(bound, statuses, expected):
    assert k4b_stats.overall(dict(zip(MODELS, statuses))) == expected


# ------------------------------------------------------- positive_below_margin


def entry(L, U, Fm, Fp, as_str=True):
    r = ms(L, U, Fm, Fp)
    return {"L": L, "U": U, "F_minus": str(Fm) if as_str else Fm,
            "F_plus": str(Fp) if as_str else Fp, "status": r["status"],
            "labels": list(r["labels"]), "status_without_F": r["status_without_F"]}


def zero_point(F):
    """Largest float x with Fraction(x) <= F."""
    x = float(F)
    if Fraction(x) > F:
        x = math.nextafter(x, -math.inf)
    return x


def pbm_kind(res, j):
    pm = res["per_model"]
    return pm[j] if j in pm else pm[str(j)]


def pbm_pos(res, j):
    p = res["positive"]
    return p[j] if j in p else p[str(j)]


def test_pbm_zero_is_not_positive_next_float_is(bound):
    F = Fraction(1.0000000011248e-9)  # dyadic: the zero point is a float
    x0 = float(F)
    assert Fraction(x0) - F == 0
    x1 = math.nextafter(x0, math.inf)
    pm = {J1: entry(x0, 0.005, F, F_SMALL), J2: entry(x1, 0.005, F, F_SMALL),
          J3: entry(x1, 0.005, F, F_SMALL, as_str=False)}
    assert all(pm[j]["status"] == "EXCLUDE" for j in MODELS)
    r = cg.positive_below_margin(pm)
    assert not pbm_pos(r, J1)
    assert pbm_kind(r, J1) is None
    assert pbm_pos(r, J2) and pbm_kind(r, J2) == "EXCLUDE"
    assert pbm_pos(r, J3) and pbm_kind(r, J3) == "EXCLUDE"
    assert sorted(int(j) for j in r["models"]) == [J2, J3]
    assert not r["all_positive"]


def test_pbm_non_dyadic_F_zero_point(bound):
    F = Fraction(1, 10**9) + Fraction(11248, 10**16)  # not a float
    x0 = zero_point(F)
    assert Fraction(x0) - F < 0
    x1 = math.nextafter(x0, math.inf)
    assert Fraction(x1) - F > 0
    pm = {J1: entry(x0, 0.005, F, F_SMALL), J2: entry(x1, 0.005, F, F_SMALL),
          J3: entry(x1, 0.02, F, F_SMALL)}
    r = cg.positive_below_margin(pm)
    assert pbm_kind(r, J1) is None and not pbm_pos(r, J1)
    assert pbm_kind(r, J2) == "EXCLUDE"
    assert pm[J3]["status"] == "UNRESOLVED"
    assert pbm_kind(r, J3) == "UNRESOLVED"


def test_pbm_kinds_and_support_never(bound):
    Fn = Fraction(1, 10**9)
    pm = {J1: entry(0.05, 0.06, F_SMALL, F_SMALL),          # SUPPORT, positive
          J2: entry(0.01 + 5e-10, 0.02, Fn, Fn),            # UNRESOLVED/NUMERICAL
          J3: entry(0.002, 0.005, F_SMALL, F_SMALL)}        # EXCLUDE, positive
    assert [pm[j]["status"] for j in MODELS] == [
        "SUPPORT", "UNRESOLVED/NUMERICAL", "EXCLUDE"]
    r = cg.positive_below_margin(pm)
    assert pbm_pos(r, J1) and pbm_kind(r, J1) is None
    assert pbm_kind(r, J2) == "UNRESOLVED"
    assert pbm_kind(r, J3) == "EXCLUDE"
    assert r["all_positive"]
    pm[J3] = entry(-0.002, 0.005, F_SMALL, F_SMALL)        # EXCLUDE, negative
    r = cg.positive_below_margin(pm)
    assert pbm_kind(r, J3) is None and not r["all_positive"]


def test_pbm_str_keys_accepted(bound):
    pm = {str(j): entry(0.002, 0.005, F_SMALL, F_SMALL) for j in MODELS}
    r = cg.positive_below_margin(pm)
    assert r["all_positive"]
    assert len(r["models"]) == 3


# ----------------------------------------------------------------- annotations


def result(pm, fresh_low=False):
    statuses = {j: pm[j]["status"] for j in MODELS}
    fb = {"status": "HEADROOM" if fresh_low else "PASS"}
    if fresh_low:
        # API-AMBIGUITY: how FRESH_B4_LOW is "set" in the ENDPOINT result is not
        # pinned; every plausible marker is present together.
        fb.update({"FRESH_B4_LOW": True, "flag": "FRESH_B4_LOW",
                   "flags": ["FRESH_B4_LOW"], "label": "FRESH_B4_LOW"})
    return {"per_model": pm, "overall": k4b_stats.overall(statuses),
            "fresh_B4": fb, "init_qualifier": {j: False for j in MODELS},
            "Z_bound": "1/1000000000000", "N": 3072, "k": 1}


def check_outcome_unchanged(res):
    before = copy.deepcopy(res)
    ann = cg.annotations(res)
    assert res == before
    st = {"fail": None, "resource": None, "l1": None, "k4b": None,
          "criterion": None, "models": None, "endpoint": res}
    oc = cg.outcome(st)
    assert oc["outcome"] == res["overall"]
    assert res == before
    return ann


def test_annotations_exclusion_all_positive(bound):
    pm = {j: entry(0.002, 0.005, F_SMALL, F_SMALL) for j in MODELS}
    res = result(pm)
    assert res["overall"] == "EXCLUSION"
    ann = check_outcome_unchanged(res)
    for j in MODELS:
        assert f"POSITIVE_BELOW_MARGIN_{j}" in ann
    assert "POSITIVE_BELOW_MARGIN" in ann
    assert "FRESH_B4_LOW" not in ann


def test_annotations_support_never(bound):
    pm = {j: entry(0.05, 0.06, F_SMALL, F_SMALL) for j in MODELS}
    res = result(pm)
    assert res["overall"] == "SUPPORT"
    ann = check_outcome_unchanged(res)
    assert not [a for a in ann if a.startswith("POSITIVE_BELOW_MARGIN")]


def test_annotations_mixed_all_positive(bound):
    pm = {J1: entry(0.05, 0.06, F_SMALL, F_SMALL),
          J2: entry(0.002, 0.005, F_SMALL, F_SMALL),
          J3: entry(0.002, 0.02, F_SMALL, F_SMALL)}
    res = result(pm)
    assert res["overall"] == "MIXED"
    ann = check_outcome_unchanged(res)
    assert f"POSITIVE_BELOW_MARGIN_{J1}" not in ann
    assert f"POSITIVE_BELOW_MARGIN_{J2}" in ann
    assert f"POSITIVE_BELOW_MARGIN_{J3}" in ann
    assert "POSITIVE_BELOW_MARGIN" in ann


def test_annotations_not_all_positive(bound):
    F = Fraction(1.0000000011248e-9)
    x0 = float(F)
    pm = {J1: entry(x0, 0.005, F, F_SMALL),                  # exactly 0: not positive
          J2: entry(0.002, 0.005, F_SMALL, F_SMALL),
          J3: entry(0.002, 0.02, F_SMALL, F_SMALL)}
    res = result(pm)
    ann = check_outcome_unchanged(res)
    assert f"POSITIVE_BELOW_MARGIN_{J1}" not in ann
    assert f"POSITIVE_BELOW_MARGIN_{J2}" in ann
    assert "POSITIVE_BELOW_MARGIN" not in ann


def test_annotations_negative_numerical_fresh(bound):
    Fn = Fraction(1, 10**9)
    pm = {J1: entry(-0.04, -0.02, F_SMALL, F_SMALL),        # NEGATIVE_ALIGNMENT
          J2: entry(0.0, 0.01 - 5e-10, Fn, Fn),             # UNRESOLVED/NUMERICAL
          J3: entry(-0.002, 0.02, F_SMALL, F_SMALL)}
    assert "NEGATIVE_ALIGNMENT" in pm[J1]["labels"]
    assert pm[J2]["status"] == "UNRESOLVED/NUMERICAL"
    res = result(pm, fresh_low=True)
    assert res["overall"] == "INCONCLUSIVE/NUMERICAL"
    ann = check_outcome_unchanged(res)
    assert f"NEGATIVE_ALIGNMENT_{J1}" in ann
    assert f"NEGATIVE_ALIGNMENT_{J2}" not in ann
    # API-AMBIGUITY: the per-model UNRESOLVED/NUMERICAL annotation may or may not
    # carry the model key; either spelling is accepted.
    assert [a for a in ann if a.startswith("UNRESOLVED/NUMERICAL")]
    assert "FRESH_B4_LOW" in ann
    assert not [a for a in ann if a.startswith("POSITIVE_BELOW_MARGIN")]


def test_annotations_no_flags_when_clean(bound):
    pm = {j: entry(-0.002, 0.005, F_SMALL, F_SMALL) for j in MODELS}
    res = result(pm)
    assert res["overall"] == "EXCLUSION"
    ann = check_outcome_unchanged(res)
    assert not [a for a in ann if a.startswith(("NEGATIVE_ALIGNMENT",
                                                "UNRESOLVED/NUMERICAL",
                                                "POSITIVE_BELOW_MARGIN",
                                                "FRESH_B4_LOW"))]
