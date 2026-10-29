"""Author A (job 0176): the P1 ladder, the N rule and the registry-risk check.

Protocol HWSC §2.4 C6, §3.2 item 1, §3.4 "Registry-risk check", §5 P1 (RC-1);
DRC6; K4B §7.1-§7.2. API.md §3.4, §6 (`p1c_ladder`, `choose_N`); hwsb API
`ladder_pilot`; x4 `precision` API. Planted synthetic arrays only.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_bind as cb  # noqa: E402
import hwsc_data as cd  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import c1_records  # noqa: E402
import hwsb_gates  # noqa: E402
import hws_exact  # noqa: E402
import k4b_cert  # noqa: E402
import precision  # noqa: E402

MODELS = (620301, 620302, 620303)
LADDER = (3072, 6144, 12288)
M = Fraction(1, 100)
ALPHA = Fraction(1, 60)
HV = cc.CONTRACT["handoff"]["values"]
F_PLAN = k4b_cert.F_plan(Fraction(HV["Z_bound"]))
N_ROWS = 3072


def planted(sd, seed, n=N_ROWS):
    """Three strongly correlated models (shared base), small width on 10% of rows."""
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n)
    base = (base - base.mean()) / base.std(ddof=1) * sd
    Xm, Xp, r4n = {}, {}, {}
    for j in MODELS:
        xm = base + rng.standard_normal(n) * sd * 0.05
        xp = xm + 0.02 * (rng.random(n) < 0.1)
        Xm[j], Xp[j], r4n[j] = xm, xp, np.abs(xp) + 0.1
    D = {j: float(np.mean(Xp[j] - Xm[j]) / 2) for j in MODELS}
    return Xm, Xp, r4n, D


def deq(a, b):
    if isinstance(a, dict) or isinstance(b, dict):
        return (isinstance(a, dict) and isinstance(b, dict) and a.keys() == b.keys()
                and all(deq(a[k], b[k]) for k in a))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.array_equal(np.asarray(a), np.asarray(b))
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return (type(a) is type(b) and len(a) == len(b)
                and all(deq(x, y) for x, y in zip(a, b)))
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return a == b


def get(d, j):
    return d[j] if j in d else d[str(j)]


def reference(Xm, Xp, r4n, F, seeds=(620311, 620315)):
    """Independent re-implementation of K4B §7.1-§7.2 for the stage-C keys."""
    n = len(next(iter(Xm.values())))
    sdU = {}
    for s, X in (("-", Xm), ("+", Xp)):
        sd, _ = precision.sd_b4_draws({j: X[j] for j in MODELS}, {j: r4n[j] for j in MODELS},
                                      list(MODELS), seeds[0], 5000, n)
        for i, j in enumerate(MODELS):
            sdU[(j, s)] = float(np.sort(sd[:, i])[4917 - 1])
    keys = [(j, s) for j in MODELS for s in ("-", "+")]
    Xd = {(j, "-"): Xm[j] for j in MODELS}
    Xd.update({(j, "+"): Xp[j] for j in MODELS})
    Ff = float(F)
    cands = {}
    for N in LADDER:
        cfg = {"delta": float(M + F), "alpha": float(ALPHA), "power": 0.80, "projected_N": N}
        mde_ok = all(precision.mde(sdU[k], cfg) <= 0.02 for k in keys)
        e = precision.centered_draws(Xd, keys, seeds[1], 5000, N)
        sup, exc = {}, {}
        sup_all = np.ones(5000, bool)
        exc_all = np.ones(5000, bool)
        for j in MODELS:
            em, ep = e[:, keys.index((j, "-"))], e[:, keys.index((j, "+"))]
            qa, qb = np.sort(em)[84 - 1], np.sort(ep)[4917 - 1]
            s_ok = 0.02 + em + qa - Ff > 0.01
            x_ok = (ep + qb + Ff < 0.01) & (em + qa - Ff > -0.01)
            sup[j], exc[j] = int(s_ok.sum()), int(x_ok.sum())
            sup_all &= s_ok
            exc_all &= x_ok
        ok = (min(sup.values()) >= 4000 and min(exc.values()) >= 4000
              and int(sup_all.sum()) >= 4000 and int(exc_all.sum()) >= 4000)
        cands[N] = {"mde_ok": mde_ok, "support": sup, "support_joint": int(sup_all.sum()),
                    "exclusion": exc, "exclusion_joint": int(exc_all.sum()), "ok": ok}
    chosen = next((N for N in LADDER if cands[N]["mde_ok"] and cands[N]["ok"]), None)
    return sdU, cands, chosen


CASES = {"n3072": (0.10, 11, 3072), "n6144": (0.20, 12, 6144), "none": (0.50, 13, None)}
_CACHE = {}


def run_case(name):
    if name not in _CACHE:
        sd, seed, _ = CASES[name]
        Xm, Xp, r4n, D = planted(sd, seed)
        got = cg.p1c_ladder(Xm, Xp, r4n, F_PLAN, D)
        ref = hwsb_gates.ladder_pilot(Xm, Xp, r4n, F_PLAN, models=MODELS,
                                      seeds=(620311, 620315), D_bar=D, ladder=LADDER)
        _CACHE[name] = (Xm, Xp, r4n, D, got, ref)
    return _CACHE[name]


@pytest.mark.parametrize("name", list(CASES))
def test_p1c_equals_ladder_pilot_and_reference(name):
    Xm, Xp, r4n, D, got, ref = run_case(name)
    assert deq(got, ref)
    sdU, cands, chosen = reference(Xm, Xp, r4n, F_PLAN)
    assert got["N"] == chosen == CASES[name][2]
    assert got["status"] == ("PASS" if chosen else "INCONCLUSIVE/UNDERPOWERED")
    assert got["k"] == (chosen // 3072 if chosen else None)
    assert set(got["sdU"]) == set(sdU)
    for k, v in sdU.items():
        assert got["sdU"][k] == v
    assert got["candidates"], "no candidate reported"
    for N, c in got["candidates"].items():
        r = cands[int(N)]
        assert bool(c["mde_ok"]) == r["mde_ok"], N
        proj = c["projection"]
        for j in MODELS:
            assert get(proj["support"]["per_model"], j) == r["support"][j]
            assert get(proj["exclusion"]["per_model"], j) == r["exclusion"][j]
        assert proj["support"]["joint"] == r["support_joint"]
        assert proj["exclusion"]["joint"] == r["exclusion_joint"]
        assert bool(proj["ok"]) == r["ok"]
    if name == "n6144":
        assert not got["candidates"][3072]["mde_ok"]


def test_seed_sensitive_fixture():
    Xm, Xp, r4n, D, got, _ = run_case("n3072")
    k4b_seeds = hwsb_gates.ladder_pilot(Xm, Xp, r4n, F_PLAN, models=MODELS,
                                        seeds=(610101, 610105), D_bar=D, ladder=LADDER)
    assert any(k4b_seeds["sdU"][k] != got["sdU"][k] for k in got["sdU"])
    assert not deq(k4b_seeds["candidates"], got["candidates"])


def test_p1c_inside_binding_equal():
    Xm, Xp, r4n, D, got, _ = run_case("n3072")
    with cb.bound_stage_c():
        inside = cg.p1c_ladder(Xm, Xp, r4n, F_PLAN, D)
    assert deq(inside, got)


def test_projection_invariant_to_mean_shift():
    Xm, Xp, r4n, D, got, _ = run_case("n6144")
    sh = cg.p1c_ladder({j: Xm[j] + 0.25 for j in MODELS}, {j: Xp[j] + 0.25 for j in MODELS},
                       r4n, F_PLAN, D)
    assert sh["N"] == got["N"]
    assert set(sh["candidates"]) == set(got["candidates"])
    for N in got["candidates"]:
        a, b = got["candidates"][N]["projection"], sh["candidates"][N]["projection"]
        for scen in ("support", "exclusion"):
            assert deq(a[scen]["per_model"], b[scen]["per_model"])
            assert a[scen]["joint"] == b[scen]["joint"]


# -------------------------------------------------------------------- choose_N


@pytest.mark.parametrize("N_C", [3072, 6144])
@pytest.mark.parametrize("N_P1", [3072, 6144, 12288])
def test_choose_N_max(N_C, N_P1):
    r = cg.choose_N(N_C, {"N": N_P1, "status": "PASS"})
    assert r["status"] == "PASS"
    assert r["N"] == max(N_C, N_P1)
    assert r["k"] == max(N_C, N_P1) // 3072
    assert r["N_P1"] == N_P1 and r["N_C"] == N_C


@pytest.mark.parametrize("N_C", [3072, 6144, 12288])
def test_choose_N_underpowered(N_C):
    r = cg.choose_N(N_C, {"N": None, "status": "INCONCLUSIVE/UNDERPOWERED"})
    assert r["status"] == "INCONCLUSIVE/UNDERPOWERED"
    assert r["N"] is None and r["k"] is None


@pytest.mark.parametrize("N_C, N_P1", [(5000, 3072), (24576, 3072), (9216, 6144)])
def test_choose_N_off_ladder(N_C, N_P1):
    with pytest.raises(c1_records.C1GateFailure) as ei:
        cg.choose_N(N_C, {"N": N_P1, "status": "PASS"})
    assert ei.value.status == "FAIL_TECHNICAL/NUMERICAL"


# --------------------------------------------------------------- registry risk


def rows(N):
    return 4096 + 3072 + 3072 + N


@pytest.mark.parametrize("N", LADDER)
def test_registry_risk_value_exact(N):
    p = HV["p_D2a"]
    r = cd.registry_risk(p, N)
    exact = rows(N) * Fraction(float(p))
    assert Fraction(r["value"]) == exact
    assert bool(r["ok"])
    assert int(r["N"]) == N
    assert int(r["rows"]) == rows(N)


def test_registry_risk_desk_value():
    r = cd.registry_risk(HV["p_D2a"], 3072)
    v = float(Fraction(r["value"]))
    assert abs(v - 7.2e-11) / 7.2e-11 < 0.01


@pytest.mark.parametrize("N", LADDER)
def test_registry_risk_boundary(N):
    # API-AMBIGUITY: Fraction(float(p)) is dyadic, so rows * Fraction(float(p))
    # can never equal 1/100 exactly; the boundary is tested at float resolution:
    # the largest float p with rows*p <= 1/100 passes, the next float fails.
    cap = Fraction(1, 100)
    p = float(cap / rows(N))
    while rows(N) * Fraction(p) > cap:
        p = math.nextafter(p, -math.inf)
    while rows(N) * Fraction(math.nextafter(p, math.inf)) <= cap:
        p = math.nextafter(p, math.inf)
    assert rows(N) * Fraction(p) <= cap < rows(N) * Fraction(math.nextafter(p, math.inf))
    assert cd.registry_risk(p, N)["ok"]
    assert not cd.registry_risk(math.nextafter(p, math.inf), N)["ok"]
    assert not cd.registry_risk(2 * p, N)["ok"]


# --------------------------------------------------------------- p_D2a check


def proc_stub():
    return {"T": np.eye(2), "E_canon_shared": np.eye(2), "pi": np.full(2, 0.5)}


def test_p_d2a_check_tolerance(monkeypatch):
    ref = 1.0
    k = 1
    while (ref + k * 2.0**-52 - ref) / ref <= 1e-12:
        k += 1
    p_fail, p_pass = ref + k * 2.0**-52, ref + (k - 1) * 2.0**-52
    assert abs(p_pass - ref) / abs(ref) <= 1e-12 < abs(p_fail - ref) / abs(ref)
    for value, ok in ((p_pass, True), (p_fail, False), (ref, True),
                      (ref - (k - 1) * 2.0**-53, True)):
        monkeypatch.setattr(hws_exact, "p_d2a", lambda T, E, pi, *a, _v=value, **kw: _v)
        r = cd.p_d2a_check(proc_stub(), ref)
        assert bool(r["ok"]) is ok, value
        assert r["p_D2a"] == value and r["p_D2a_ref"] == ref
        assert r["rel_diff"] == abs(value - ref) / abs(ref)


def test_p_d2a_check_handoff_value(monkeypatch):
    p = HV["p_D2a"]
    monkeypatch.setattr(hws_exact, "p_d2a", lambda T, E, pi, *a, **kw: p)
    r = cd.p_d2a_check(proc_stub(), p)
    assert r["ok"] and r["rel_diff"] == 0.0
    monkeypatch.setattr(hws_exact, "p_d2a", lambda T, E, pi, *a, **kw: p * (1 + 1e-9))
    assert not cd.p_d2a_check(proc_stub(), p)["ok"]
