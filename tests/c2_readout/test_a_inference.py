"""Independent tests, author A (job 0101): T-FAMILY (Lemma FW, FW-M), T-RULES (RC-8, RC-13,
NEW-6) and T-BOOT (shared index stream, Fraction ranks) (C2-FROZEN-v1 3, 5.7, 6.2-6.5, 13.3).
The C2-M descriptive stream of T-BOOT is in test_a_partition.py, T-LADDER in test_a_gls.py.

Targets (API.md 10, 11): cdc.sign, cdc.r_model, cdc.m_model, cdc.overall,
cdc.endpoint_status, cdc.qualifiers, cdc.licence, cdc.stream_bounds, ca.post_desc. Expected
values come from the protocol's rules re-implemented here, exact Fraction arithmetic and the
reused c1_means kernels.

API-ASSUMPTIONS (formats API.md leaves open): r_model/m_model take {statistic: {"L", "U", "g",
...}} (report.json per_model.bounds layout) and return the API.md 11.2 keys with booleans;
endpoint_status takes the GATES.jsonl records (API.md 15.1) as a list of dicts; qualifiers
takes r_model outputs, {model: {variant: category}} and the cs.p1 result.
"""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402
import c1_means  # noqa: E402
import c2_attrib as ca  # noqa: E402
import c2_decide as cdc  # noqa: E402

G = 1e-9
SIG = {1: 1.0, 0: 0.0, -1: -1.0}
PAIRS = [(1, 1), (0, 1), (-1, 1), (0, 0), (-1, 0), (-1, -1)]  # (sign L, sign U), L <= U
C1, C5 = Fr(1, 10), Fr(1, 2)
VALUES = {"k": 2, "list": [1729, 2718], "other": "INC", "psi_hat": 0.6, "lower": 0.55,
          "upper": 0.7, "tau_hat": 0.05, "psi_M_hat": 0.6, "gate": "R1", "values": "-",
          "statuses": "-", "models": [1729, 2718], "registration": 0.6, "R2_code_0": 0.8,
          "rho_inc": 0.95, "intervals": "-", "theta_rot": 0.5, "interval": (0.4, 0.6),
          "s_rot": 0.9, "m": 1}


def _bd(L, U):
    return {"mean": (L + U) / 2, "L": float(L), "U": float(U), "rank_L": 84, "rank_U": 19917,
            "g": G}


def _sg(x):
    return 1 if x > G else (-1 if x < -G else 0)


def _coarse(out):
    co = out.get("coarse") or {}
    return {"gt010": bool(co.get("gt010", False)), "lt050": bool(co.get("lt050", False))}


def _occ(b, ev, mu):
    side, s = ev
    return Fr(b[s]["L"]) > mu[s] if side == "L" else Fr(b[s]["U"]) < mu[s]


def _cat_events(psi, mu, z1, z5, energy):
    if psi < C1:
        bad = [s for s in energy if mu[s] >= 0]
        return [("L", z1)] + ([("U", bad[0])] if bad else [])
    if psi == C1:
        return [("L", z1), ("U", z1)]
    if psi < C5:
        return [("L", z5), ("U", z1)]
    return [("L", z5), ("U", z5)] if psi == C5 else [("U", z5)]


# ---- T-FAMILY (R) ----------------------------------------------------------------------------
def _expect_r(b, y_active):
    if _sg(b["V3x"]["L"]) != 1:
        return "EXCLUDED/MODEL_HEADROOM"
    if y_active and _sg(b["Y1"]["U"]) != -1:
        return "EXCLUDED/NUISANCE_IN_S"
    l1, u1, l5, u5 = (_sg(b[s][k]) for s in ("Z010", "Z050") for k in ("L", "U"))
    if l5 == 1 and l1 == 1:
        return "USED"
    if l1 == 1 and u5 == -1:
        return "PARTIAL"
    if u1 == -1 and u5 == -1:
        ok = _sg(b["Vabs"]["U"]) == -1 and _sg(b["Vrand"]["U"]) == -1
        return "NOT_USED" if ok else "LOW_ALIGNED"
    return "INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC"


def _r_patterns():
    for v3, y1, z1, z5, va, vr in itertools.product((1, 0), (-1, 0), PAIRS, PAIRS, (-1, 1),
                                                    (-1, 1)):
        yield {"V3x": _bd(SIG[v3], 2.0), "Y1": _bd(-2.0, SIG[y1]),
               "Z010": _bd(SIG[z1[0]], SIG[z1[1]]), "Z050": _bd(SIG[z5[0]], SIG[z5[1]]),
               "Vabs": _bd(-2.0, SIG[va]), "Vrand": _bd(-2.0, SIG[vr]), "NEG": _bd(-2.0, -1.0)}


def test_lemma_fw_r_exhaustive_grid():
    psis = [Fr(-1), Fr(1, 20), C1, Fr(3, 10), C5, Fr(7, 10)]
    runs = []
    for y_active in (True, False):
        for b in _r_patterns():
            out = cdc.r_model(b, y_active)
            assert out["status"] == _expect_r(b, y_active)
            resp = _sg(b["V3x"]["L"]) == 1
            assert bool(out["resp"]) == resp
            if resp and y_active:
                assert bool(out["spec"]) == (_sg(b["Y1"]["U"]) == -1)
            pre = resp and (not y_active or _sg(b["Y1"]["U"]) == -1)
            co = _coarse(out)
            assert co["gt010"] == (pre and _sg(b["Z010"]["L"]) == 1)
            assert co["lt050"] == (pre and _sg(b["Z050"]["U"]) == -1)
            cats = [_sg(b["Z050"]["L"]) == 1 and _sg(b["Z010"]["L"]) == 1,
                    _sg(b["Z010"]["L"]) == 1 and _sg(b["Z050"]["U"]) == -1,
                    _sg(b["Z010"]["U"]) == -1 and _sg(b["Z050"]["U"]) == -1]
            assert sum(cats) <= 1  # mutually exclusive (L <= U on the same draws)
            pos = cdc.r_model(dict(b, NEG=_bd(-1.0, 1.0)), y_active)  # NEGATIVE: outside
            assert pos["status"] == out["status"] and not bool(pos["negative"])
            if not resp:
                assert not bool(out["negative"])  # only after rule 1
            elif not out["status"].startswith("EXCLUDED"):
                assert bool(out["negative"])
            runs.append((b, out, y_active))
    for psi, v3, y1, va, vr in itertools.product(psis, (1, -1), (-1, 1), (-1, 1), (-1, 1)):
        mu = {"V3x": Fr(v3, 2), "Y1": Fr(y1, 2), "Z010": psi - C1, "Z050": psi - C5,
              "Vabs": Fr(va, 2), "Vrand": Fr(vr, 2)}
        truth = {"USED": psi > C5, "PARTIAL": C1 < psi < C5, "LOW_ALIGNED": psi < C1,
                 "NOT_USED": psi < C1 and va < 0 and vr < 0}
        for b, out, y_active in runs:
            listed = [("L", "V3x")] + ([("U", "Y1")] if y_active else []) + _cat_events(
                psi, mu, "Z010", "Z050", ("Vabs", "Vrand"))
            assert len(listed) <= (4 if y_active else 3)
            false = []
            if out["resp"] and not mu["V3x"] > 0:
                false.append("RESP")
            if y_active and out["resp"] and out["spec"] and not mu["Y1"] < 0:
                false.append("SPEC")
            if out["status"] in truth and not truth[out["status"]]:
                false.append(out["status"])
            co = _coarse(out)
            if co["gt010"] and not psi > C1:
                false.append("gt010")
            if co["lt050"] and not psi < C5:
                false.append("lt050")
            if false:
                assert any(_occ(b, ev, mu) for ev in listed), (false, psi, mu, y_active)


def test_equality_and_guard_are_never_declared():
    assert cdc.sign(G, G) == 0 and cdc.sign(-G, G) == 0 and cdc.sign(0.0, G) == 0
    assert cdc.sign(G * (1 + 1e-12), G) == 1 and cdc.sign(-G * (1 + 1e-12), G) == -1
    b = {"V3x": _bd(1.0, 2.0), "Y1": _bd(-2.0, -1.0), "Z010": _bd(1.0, 2.0),
         "Z050": _bd(G, 1.0), "Vabs": _bd(-2.0, -1.0), "Vrand": _bd(-2.0, -1.0),
         "NEG": _bd(-2.0, 1.0)}
    assert cdc.r_model(b, True)["status"] == "INC/NUMERICAL"  # L(Z050) = g: not > g
    assert cdc.r_model(dict(b, V3x=_bd(G, 2.0)), True)["status"] == "EXCLUDED/MODEL_HEADROOM"


# ---- T-FAMILY (M, Lemma FW-M) ----------------------------------------------------------------
def _expect_m(b, y2):
    if _sg(b["V3x"]["L"]) != 1:
        return {"EXCLUDED/MODEL_HEADROOM"}
    if y2 and _sg(b["Y2"]["U"]) != -1:
        return {"EXCLUDED/NUISANCE_IN_S"}
    lt, ut = _sg(b["Ztau"]["L"]), _sg(b["Ztau"]["U"])
    if ut == -1:
        return {"ROUTED"}
    if lt != 1:  # API-AMBIGUITY: rule 6 does not say whether a Ztau guard hit is INC/NUMERICAL
        return {"INC", "INC/NUMERICAL"} if 0 in (lt, ut) else {"INC"}
    l1, u1, l5, u5 = (_sg(b[s][k]) for s in ("ZM010", "ZM050") for k in ("L", "U"))
    if l5 == 1 and l1 == 1:
        return {"UPSTREAM_USED"}
    if l1 == 1 and u5 == -1:
        return {"UPSTREAM_PARTIAL"}
    if u1 == -1 and u5 == -1:
        return {"UPSTREAM_NOT_USED" if _sg(b["VM"]["U"]) == -1 else "UPSTREAM_LOW_ALIGNED"}
    return {"INC/NUMERICAL"} if 0 in (l1, u1, l5, u5) else {"INC"}


def test_lemma_fw_m_exhaustive_grid():
    runs = []
    for y2 in (True, False):
        for v3, yy, zt, z1, z5, vm in itertools.product((1, 0), (-1, 0), PAIRS, PAIRS, PAIRS,
                                                        (-1, 1)):
            b = {"V3x": _bd(SIG[v3], 2.0), "Y2": _bd(-2.0, SIG[yy]),
                 "Ztau": _bd(SIG[zt[0]], SIG[zt[1]]), "ZM010": _bd(SIG[z1[0]], SIG[z1[1]]),
                 "ZM050": _bd(SIG[z5[0]], SIG[z5[1]]), "VM": _bd(-2.0, SIG[vm]),
                 "NEG": _bd(-2.0, -1.0)}
            out = cdc.m_model(b, y2)
            assert out["status"] in _expect_m(b, y2)
            runs.append((b, out, y2))
    for tau, psi, vm, v3, yy in itertools.product((Fr(1, 20), C1, Fr(3, 10)),
                                                  (Fr(1, 20), C1, Fr(3, 10), C5, Fr(7, 10)),
                                                  (-1, 1), (1, -1), (-1, 1)):
        mu = {"V3x": Fr(v3, 2), "Y2": Fr(yy, 2), "Ztau": tau - C1, "ZM010": psi - C1,
              "ZM050": psi - C5, "VM": Fr(vm, 2)}
        up = tau > C1
        truth = {"ROUTED": tau < C1, "UPSTREAM_USED": up and psi > C5,
                 "UPSTREAM_PARTIAL": up and C1 < psi < C5, "UPSTREAM_LOW_ALIGNED": up and psi < C1,
                 "UPSTREAM_NOT_USED": up and psi < C1 and vm < 0}
        for b, out, y2 in runs:
            listed = [("L", "V3x")] + ([("U", "Y2")] if y2 else [])
            if tau < C1:
                listed.append(("L", "Ztau"))
            elif tau == C1:
                listed += [("L", "Ztau"), ("U", "Ztau")]
            else:
                listed += [("U", "Ztau")] + _cat_events(psi, mu, "ZM010", "ZM050", ("VM",))
            assert len(listed) <= 6
            false = []
            if out["resp"] and not mu["V3x"] > 0:
                false.append("RESP")
            if y2 and out["resp"] and out["spec"] and not mu["Y2"] < 0:
                false.append("SPEC")
            if out["status"] in truth and not truth[out["status"]]:
                false.append(out["status"])
            if false:
                assert any(_occ(b, ev, mu) for ev in listed), (false, tau, psi, mu, y2)


# ---- T-RULES ---------------------------------------------------------------------------------
U, PA, NU, LA = "USED", "PARTIAL", "NOT_USED", "LOW_ALIGNED"
OVERALL = [
    ("R", (U, U, U), [], "USED"), ("R", (U, U, PA), [], "USED"),
    ("R", (U, PA, NU), [], "MIXED"), ("R", (U, "INC", "INC/NUMERICAL"), [],
                                      "INCONCLUSIVE/PRECISION"),
    ("R", (NU, NU, LA), [], "NOT_USED"), ("R", (NU, LA, "INC"), [], "LOW_ALIGNED_SHARE"),
    ("R", (LA, LA, U), [], "LOW_ALIGNED_SHARE"), ("R", (PA, PA, "INC/NUMERICAL"), [], "PARTIAL"),
    ("R", (U, NU, "INC"), [], "MIXED"), ("R", (U, U, "EXCLUDED/LINK"), [], "USED"),
    ("R", (U, U, "EXCLUDED/MODEL_HEADROOM"), [], "USED"),
    ("R", (U, "EXCLUDED/LINK", "EXCLUDED/LINK"), [], "INCONCLUSIVE/LINK"),
    ("R", ("CNHS", "CNHS", U), [1729, 2718], "CIRCLE_NOT_HISTORY_SENSITIVE"),
    ("R", (U, "CNHS", PA), [2718], "MIXED"),
    ("M", ("ROUTED", "ROUTED", "UPSTREAM_USED"), [], "ROUTED_AROUND"),
    ("M", ("ROUTED",) * 3, [], "ROUTED_AROUND"),
    ("M", ("ROUTED", "UPSTREAM_USED", "UPSTREAM_USED"), [], "UPSTREAM_USED"),
    ("M", ("UPSTREAM_NOT_USED", "UPSTREAM_LOW_ALIGNED", "INC"), [], "UPSTREAM_LOW_ALIGNED"),
    ("M", ("UPSTREAM_PARTIAL", "UPSTREAM_PARTIAL", "ROUTED"), [], "UPSTREAM_PARTIAL"),
    ("M", ("ROUTED", "UPSTREAM_USED", "INC"), [], "MIXED"),
    ("M", ("CNHS", "CNHS", "ROUTED"), [1729, 2718], "CNHS-2"),
    ("M", ("INC", "INC", "ROUTED"), [], "INCONCLUSIVE/PRECISION"),
    ("S*", (U, U, "INC"), [], "X_PHASE_USED"), ("S*", (NU, NU, PA), [], "X_PHASE_NOT_USED"),
    ("S*", (NU, LA, "INC"), [], "X_PHASE_LOW_ALIGNED"), ("S*", (PA,) * 3, [], "X_PHASE_PARTIAL"),
    ("S*", ("CNHS",) * 3, [1729, 2718, 3141], "X_PHASE_NOT_HISTORY_SENSITIVE"),
    ("S*", (U, PA, "INC"), [], "MIXED"),
]


@pytest.mark.parametrize("fam, sts, cnhs, expect", OVERALL)
def test_overall_two_of_three_rules(fam, sts, cnhs, expect):
    assert cdc.overall(fam, dict(zip((1729, 2718, 3141), sts)), cnhs) == expect


ORDER = ("IMPL", "AUTH-ADMIT", "G0", "PF", "H1", "REG", "H2", "H3", "H4", "H5", "M0", "C0c",
         "F1", "C0v", "L1", "R1", "N2", "SURVIVAL", "X1", "V3x", "V3y", "Y1", "Y1*", "Y2", "P1",
         "ACCEPT", "REG2", "T-PRE", "T-PRE-MODEL", "RESP-SPEC", "NUM", "ENDPOINT", "REPORT")


FAILS = {"L1": "EXCLUDED/LINK", "T-PRE": "INCONCLUSIVE/TEST_GATE",
         "T-PRE-MODEL": "EXCLUDED/TEST_GATE", "RESP-SPEC": "EXCLUDED/MODEL_HEADROOM",
         "V3x": "EXCLUDED/MODEL_HEADROOM", "SURVIVAL": "INCONCLUSIVE/LINK"}


def _history(fail=None, model=None, family=None, scope="model"):
    """GATES.jsonl-style records (API.md 15.1): every gate PASS except `fail`; after a study
    stop the later gates are NOT_RUN."""
    out, stopped = [], False
    for gate in ORDER:
        full = "NOT_RUN" if stopped else ("PASS" if gate != fail else FAILS[gate])
        out.append({"gate": gate, "status": full.split("/")[0], "full_status": full,
                    "criterion_met": full == "PASS", "model": model if gate == fail else None,
                    "family": family if gate == fail else None, "problem": None,
                    "scope": scope if gate == fail else "study", "reason": None, "values": {}})
        stopped = stopped or (gate == fail and scope == "study")
    return out


CASES = [
    (None, None, None, "model", (1729, "R"), "SCORED"),
    ("L1", 1729, "R", "model", (1729, "R"), "NOT_RUN/L1"),
    ("L1", 1729, "R", "model", (1729, "M"), "SCORED"),
    ("L1", 1729, "R", "model", (2718, "R"), "SCORED"),
    ("T-PRE", None, None, "study", (2718, "S*"), "NOT_RUN/T-PRE"),
    ("T-PRE-MODEL", 2718, None, "model", (2718, "M"), "NOT_RUN/T-PRE"),
    ("RESP-SPEC", 3141, "R", "model", (3141, "R"), "NOT_RUN/RESP-SPEC"),
    ("V3x", 1729, None, "model", (1729, "S*"), "NOT_RUN/V3x"),
    ("SURVIVAL", None, "M", "family", (3141, "M"), "NOT_RUN/SURVIVAL"),
]


@pytest.mark.parametrize("fail, model, family, scope, who, expect", CASES)
def test_endpoint_status_new6(fail, model, family, scope, who, expect):
    hist = _history(fail, model, family, scope)
    got = cdc.endpoint_status(who[0], who[1], hist)
    assert got == expect and not got.startswith("SEALED_UNSCORED")
    post = hist + [{"gate": "REPORT", "status": "PASS", "full_status": "PASS",
                    "criterion_met": True, "model": None, "family": None, "problem": None,
                    "scope": "study", "reason": None, "values": {"post_desc": {"psi": 0.1}}}]
    assert cdc.endpoint_status(who[0], who[1], post) == expect  # POST-DESC changes nothing


def test_post_desc_values_are_labelled_unlicensed_point_ratios():
    # API-AMBIGUITY: API.md 10 does not fix the input layout of post_desc; the test passes
    # {name: {"num", "den", "E", "gate"}} and accepts any output entry holding the ratio and
    # the label.
    rng = np.random.default_rng(1)
    E = rng.random(50) < 0.8
    num, den = rng.normal(0.2, 1, 50), rng.normal(1.0, 0.2, 50)
    out = ca.post_desc({"psi": {"num": num, "den": den, "E": E, "gate": "T-PRE"}})
    entry = out["psi"]
    vals = list(entry.values()) if isinstance(entry, dict) else list(entry)
    label = "unlicensed (gate T-PRE); computed after the outcome"
    assert label in vals
    ratio = num[E].mean() / den[E].mean()
    assert any(isinstance(v, float) and abs(v - ratio) <= 1e-12 for v in vals)


def test_qualifiers_order_dissent_and_licence_texts():
    def pm(status, neg=False):
        return {"status": status, "resp": True, "spec": True, "negative": neg,
                "coarse": {"gt010": True, "lt050": False}, "unresolved": [],
                "endpoint_formed": True}
    per = {1729: pm(U), 2718: pm(U, neg=True), 3141: pm(PA)}
    variants = {1729: {"R_E": PA, "R_K1": U, "R_K2": U}, 2718: {"R_E": U, "R_K1": U, "R_K2": U},
                3141: {"R_E": PA, "R_K1": U, "R_K2": PA}}
    p1 = {"N_F": 4096, "pass": {4096: [1729, 2718]}, "status": "PASS",
          "precision_limited": [3141], "summaries": {}}
    q = cdc.qualifiers("R", per, variants, False, p1)
    assert q == ["SPECIFICITY_NOT_ESTABLISHED", "NEGATIVE_ALIGNED_CONTRIBUTION(2718)",
                 "PROJECTOR_DEPENDENT(1729)", "HARMONIC_DEPENDENT(3141, 1)",
                 "PRECISION_LIMITED(3141)", "DISSENT(3141: PARTIAL)"]
    assert "SPECIFICITY_NOT_ESTABLISHED" not in cdc.qualifiers("R", per, variants, True, p1)
    tail = "this is an assay-registration finding, not evidence that the representation " \
           "carries no history"
    for fam, outcome, extra in (("R", "CIRCLE_NOT_HISTORY_SENSITIVE", "first-harmonic phase"),
                                ("M", "CNHS-2", "layer-2 first-harmonic phase"),
                                ("S*", "X_PHASE_NOT_HISTORY_SENSITIVE", "oracle-phase")):
        text = cdc.licence(fam, outcome, VALUES)
        assert tail in text and extra in text and "They do not exclude predictive use" in text
    assert "defined by the layer-2 fit and projector" in cdc.licence("M", "CNHS-2", VALUES)


# ---- T-BOOT ----------------------------------------------------------------------------------
def test_shared_index_stream_resp_spec_first_then_endpoint():
    rng = np.random.default_rng(2)
    n, draws, seed = 300, 3000, cc.seed("test_R")
    x, y, z = rng.normal(0.4, 1, n), rng.normal(-0.2, 1, n), rng.normal(0.1, 1, n)
    first = cdc.stream_bounds({"V3x|1729": x, "Y1|1729": y}, seed, cc.ALPHA["R"], draws=draws)
    second = cdc.stream_bounds({"Z010|1729": x, "Z050|1729": z}, seed, cc.ALPHA["R"],
                               draws=draws)
    for k in ("L", "U", "rank_L", "rank_U", "mean"):
        assert first["V3x|1729"][k] == second["Z010|1729"][k]  # identical index streams
    means = c1_means.bootstrap_means({"a": x, "b": z}, seed, draws)
    L, rL = c1_means.quantile_with_rank(means["b"], Fr(1, 240))
    Uq, rU = c1_means.quantile_with_rank(means["b"], 1 - Fr(1, 240))
    assert (second["Z050|1729"]["L"], second["Z050|1729"]["U"]) == (L, Uq)
    assert (rL, rU) == (math.ceil(Fr(draws, 240)), math.ceil(Fr(draws * 239, 240)))
    assert second["Z050|1729"]["mean"] == c1_means.tree_mean(z)


@pytest.mark.parametrize("draws, alpha, ranks", [(20000, Fr(1, 240), (84, 19917)),
                                                 (20000, Fr(1, 360), (56, 19945)),
                                                 (5000, Fr(1, 60), (84, 4917))])
def test_fraction_ranks(draws, alpha, ranks):
    assert (math.ceil(draws * alpha), math.ceil(draws * (1 - alpha))) == ranks
    x = np.random.default_rng(3).normal(size=24)
    res = cdc.stream_bounds({"V3x|1729": x}, cc.seed("test_R"), alpha, draws=draws)
    assert (res["V3x|1729"]["rank_L"], res["V3x|1729"]["rank_U"]) == ranks
    assert math.ceil(5000 * Fr(1, 20)) == 250 == c1_means.rank_for(Fr(1, 20), 5000)
    assert (math.ceil(5000 * Fr(1, 40)), math.ceil(5000 * Fr(39, 40))) == (125, 4875)
    assert Fr(cc.ALPHA["R"]) == Fr(1, 240) and Fr(cc.ALPHA["M"]) == Fr(1, 360)
    assert Fr(cc.VAL_ALPHA) == Fr(1, 60) and Fr(cc.DESC_ALPHA) == Fr(1, 40)
