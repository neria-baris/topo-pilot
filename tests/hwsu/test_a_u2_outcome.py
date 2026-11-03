"""Author A (job 0223): aggregation, outcomes and licences (protocol 2.9 overall rules, 7;
API_U2 4.5, 4.9). Expected values come from a hand reimplementation of the protocol rules."""

from __future__ import annotations  # noqa: I001

import importlib
import itertools
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import c1_records  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

MASTERS = (620301, 620302, 620303)
CATS = ("RESPONDS_j", "WEAK_RESPONSE_j", "LOW_RESPONSE_j")
STATUSES = CATS + ("INC_j", "EXCLUDED_j/M0")
OUT = uc.CONTRACT["outcomes_u2"]
SHARE = "INCONCLUSIVE/ORACLE_FEASIBILITY"


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def base(s):
    return re.sub(r"_(j|\d+)(?=$|/)", "_j", s)


def expected(per_model):
    sts = [base(s) for s in per_model.values()]
    live = [s for s in sts if not s.startswith(("EXCLUDED", "NOT_RUN"))]
    if len(live) < 2:
        return "INCONCLUSIVE/M0"
    for c, name in zip(CATS, ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE")):
        if sum(s == c for s in live) >= 2:
            return name
    if sum(s in CATS for s in live) >= 2:
        return "MIXED"
    return "INCONCLUSIVE/PRECISION"


COMBOS = list(itertools.product(STATUSES, repeat=3))


@pytest.mark.parametrize("combo", COMBOS, ids=["-".join(base(x)[:4] for x in c) for c in COMBOS])
def test_every_combination(combo):
    per_model = dict(zip(MASTERS, combo))
    r = mod("hwsu_gates").response_outcome(per_model)
    assert r["outcome"] == expected(per_model)


def test_order_responds_beats_weak():
    pm = dict(zip(MASTERS, ("RESPONDS_j", "RESPONDS_j", "WEAK_RESPONSE_j")))
    assert mod("hwsu_gates").response_outcome(pm)["outcome"] == "RESPONDS"


def test_mixed_and_precision():
    ug = mod("hwsu_gates")
    pm = dict(zip(MASTERS, ("RESPONDS_j", "WEAK_RESPONSE_j", "LOW_RESPONSE_j")))
    assert ug.response_outcome(pm)["outcome"] == "MIXED"
    pm = dict(zip(MASTERS, ("RESPONDS_j", "INC_j", "INC_j")))
    assert ug.response_outcome(pm)["outcome"] == "INCONCLUSIVE/PRECISION"
    pm = dict(zip(MASTERS, ("RESPONDS_j", "INC_j/NUMERICAL", "LOW_RESPONSE_j")))
    assert ug.response_outcome(pm)["outcome"] == "MIXED"


def test_fewer_than_two_live_names_the_gate():
    ug = mod("hwsu_gates")
    pm = dict(zip(MASTERS, ("RESPONDS_j", "EXCLUDED_j/X1", "EXCLUDED_j/X1")))
    assert ug.response_outcome(pm)["outcome"] == "INCONCLUSIVE/X1"


def test_dissent_names_differing_models():
    ug = mod("hwsu_gates")
    pm = dict(zip(MASTERS, ("RESPONDS_j", "RESPONDS_j", "LOW_RESPONSE_j")))
    r = ug.response_outcome(pm)
    dis = r["dissent"]
    assert len(dis) == 1 and str(MASTERS[2]) in str(dis[0]) and "DISSENT" in str(dis[0])
    pm = dict(zip(MASTERS, ("WEAK_RESPONSE_j",) * 3))
    assert ug.response_outcome(pm)["dissent"] in ([], (), None)


def _ms(status, rule6):
    return {"status": status, "rule6": rule6}


@pytest.mark.parametrize("flags,want", [((1, 1, 1), "all three"), ((1, 1, 0), "in 2 models"),
                                         ((1, 0, 0), None), ((0, 0, 0), None)])
def test_rule6_aggregation(flags, want):
    """per_model given as model_status results (status + rule6) for the rule-6 count."""
    pm = {j: _ms("WEAK_RESPONSE_j", bool(f)) for j, f in zip(MASTERS, flags)}
    r = mod("hwsu_gates").response_outcome(pm)
    text = " ".join(map(str, r["rule6"] if isinstance(r["rule6"], (list, tuple)) else [r["rule6"]]))
    if want is None:
        assert "RESP_POSITIVE_BELOW_MARGIN" not in text
    else:
        assert "RESP_POSITIVE_BELOW_MARGIN" in text and want in text


# ---- the fixed share outcome ----------------------------------------------------------------
def test_share_outcome_is_fixed():
    ug = mod("hwsu_gates")
    ob = {"status": "PASS", "outcome": "OF_PASS_RESPONSE_ONLY", "share_outcome": SHARE,
          "freeze_of_sha256": "f" * 64, "of_accept_sha256": "a" * 64}
    r = ug.share_outcome(ob)
    assert r["outcome"] == SHARE == OUT["share_fixed"]
    assert r["source"] == "OF_ACCEPT.json"
    assert r["of_accept_sha256"] == "a" * 64


def test_share_outcome_ignores_any_data():
    """No data path can change it: whatever responses are, the share stays fixed."""
    ug = mod("hwsu_gates")
    ob = {"status": "PASS", "outcome": "OF_PASS_RESPONSE_ONLY", "share_outcome": SHARE,
          "freeze_of_sha256": "f" * 64, "of_accept_sha256": "b" * 64}
    for combo in (("RESPONDS_j",) * 3, ("LOW_RESPONSE_j",) * 3):
        ug.response_outcome(dict(zip(MASTERS, combo)))
        assert ug.share_outcome(ob)["outcome"] == SHARE


def test_share_entry_points_fail_closed():
    ug = mod("hwsu_gates")
    assert ug.share_dropped({})["status"] == "NOT_RUN/SHARE_DROPPED"
    for fn in (ug.share_family, ug.share_arrays_u, ug.haar_frames_u, mod("hwsu_known").ku_cases):
        with pytest.raises(c1_records.C1GateFailure) as e:
            fn()
        assert e.value.status == "FAIL_TECHNICAL/BINDING"


# ---- study outcome precedence ---------------------------------------------------------------
def _rec(gate, status):
    return {"gate": gate, "status": status}


RESP = {"outcome": "RESPONDS"}
SH = {"outcome": SHARE}


def test_study_outcome_precedence():
    ug = mod("hwsu_gates")
    recs = [_rec("H5-U", "INCONCLUSIVE/HEADROOM"), _rec("AUTH", "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"),
            _rec("X1", "FAIL_TECHNICAL/X1")]
    assert ug.study_outcome(recs, RESP, SH) == "FAIL_TECHNICAL/X1"
    assert ug.study_outcome(recs[:2], RESP, SH) == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    assert ug.study_outcome(recs[:1], RESP, SH) == "INCONCLUSIVE/HEADROOM"
    ok = [_rec("BASIS", "PASS"), _rec("SUP", "NOT_RUN/SHARE_DROPPED")]
    assert ug.study_outcome(ok, RESP, SH) == "RESPONDS"
    assert ug.study_outcome(ok, {"outcome": "LOW_RESPONSE"}, SH) == "LOW_RESPONSE"


def test_contract_precedence_and_share_fixed():
    assert OUT["precedence"][0].startswith("FAIL_TECHNICAL")
    assert OUT["precedence"][1] == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    assert OUT["share_fixed"] == SHARE
    assert OUT["response"] == ["RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE", "MIXED",
                               "INCONCLUSIVE/PRECISION"]


# ---- licences --------------------------------------------------------------------------------
def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _strings(v)


def _pipeline(thetas):
    ug = mod("hwsu_gates")
    rng = np.random.default_rng(21)
    n = 400
    G = rng.random(n) + 0.5
    A = {j: t * G + 0.01 * rng.standard_normal(n) for j, t in zip(MASTERS, thetas)}
    fb = ug.family_bounds(A, G, list(MASTERS))
    pm = {j: ug.model_status({s: fb[f"{j}:{s}"] for s in ("ZR010", "ZR030", "AF")}) for j in MASTERS}
    resp = ug.response_outcome({j: pm[j]["status"] for j in MASTERS})
    desc = ug.descriptives(A, G, {j: A[j] for j in MASTERS}, list(MASTERS))
    return ug.licences(resp, pm, fb, desc), resp


@pytest.mark.parametrize("thetas,outcome", [((0.8, 0.8, 0.8), "RESPONDS"),
                                            ((0.0, 0.0, 0.0), "LOW_RESPONSE")])
def test_licences_carry_scope_clause_and_disclosure(thetas, outcome):
    lic, resp = _pipeline(thetas)
    assert resp["outcome"] == outcome
    texts = list(_strings(lic))
    assert any(OUT["scope_clause"] in t for t in texts)
    assert any(OUT["disclosure"] in t for t in texts)
    assert any(OUT["licences"]["SHARE_INCONCLUSIVE_ORACLE_FEASIBILITY"] in t for t in texts)
    for k in ("USED", "PARTIAL", "NOT_USED", "LOW_ALIGNED_SHARE", "SHARE_POSITIVE_BELOW_MARGIN"):
        assert not any(re.search(rf"\b{k}\b", t) for t in texts), k
    if outcome == "LOW_RESPONSE":
        assert any(OUT["licences"]["LOW_RESPONSE_not_licensed"] in t for t in texts)
