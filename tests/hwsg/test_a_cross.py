"""Author A (job 0224): CROSS decision table and RC-1 boundaries (§2.7, §7.3; DRG7/10/14).

Planted world summaries in the `load_world` shape of API §8. Expected readings from the CONTRACT
`cross` table; spread pairing recomputed here with an independent PCG64(620640) generator.
"""

from __future__ import annotations  # noqa: I001

import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hwsb", "hwsc", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc  # noqa: F401
    import hwsg_cross as gx
except Exception as e:
    _ERR = e

MASTERS = {"lo": (620611, 620612, 620613), "mid": (620621, 620622, 620623),
           "hi": (620631, 620632, 620633)}


@pytest.fixture(autouse=True)
def _imports():
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")


def _rho_draws(centre, rng, width=0.01):
    return centre + width * rng.standard_normal(5000)


def W(tag, outcome, statuses=None, endpoint=None, p1=None, rho=None, ratio_status="DEFINED",
      L=0.05, F=1e-6, seed=0):
    """A planted load_world summary. rho: {j: (rhoL, rhoU)} or a centre for draws."""
    js = MASTERS[tag]
    endpoint = outcome in ("SUPPORT", "EXCLUSION", "MIXED", "INCONCLUSIVE",
                           "INCONCLUSIVE/NUMERICAL") if endpoint is None else endpoint
    p1 = endpoint if p1 is None else p1
    st = statuses or {"SUPPORT": "SUPPORT", "EXCLUSION": "EXCLUDE"}.get(outcome, "UNRESOLVED")
    per_status = {j: (st[i] if isinstance(st, (list, tuple)) else st) for i, j in enumerate(js)}
    per_model = {j: {"L": L, "U": L + 0.01, "F_minus": F, "F_plus": F,
                     "status": per_status[j]} for j in js}
    ratio, draws = None, None
    if endpoint:
        rng = np.random.default_rng(seed)
        rho = rho if rho is not None else 0.8
        pm, draws = {}, {}
        for i, j in enumerate(js):
            if isinstance(rho, dict):
                lo_, hi_ = rho[j]
                c = (lo_ + hi_) / 2
                d = _rho_draws(c, rng, 1e-9)
                pm[j] = {"rho": c, "rhoL": lo_, "rhoU": hi_,
                         "central_minus": (float(np.sort(d)[124]), float(np.sort(d)[4874]))}
            else:
                c = rho[i] if isinstance(rho, (list, tuple)) else rho
                d = _rho_draws(c, rng)
                s = np.sort(d)
                pm[j] = {"rho": c, "rhoL": float(s[83]), "rhoU": float(s[4916]),
                         "central_minus": (float(s[124]), float(s[4874]))}
            draws[j] = d
        for j in pm:  # API-AMBIGUITY: central intervals in the k4b_stats.bounds shape too
            pm[j]["status"] = ratio_status
            s_ = np.sort(draws[j])
            c95 = ((float(s_[124]), 125), (float(s_[4874]), 4875))
            pm[j]["central95_minus"] = pm[j]["central95_plus"] = c95
        ratio = {"status": ratio_status, "per_model": pm if ratio_status == "DEFINED" else {}}
        # API-AMBIGUITY: per-model ratio fields are read as floats (rhoL/rhoU), the world ratio
        # status as ratio["status"] in {"DEFINED", "RATIO_UNRESOLVED"}.
    return {"tag": tag, "outcome": outcome, "endpoint": endpoint, "p1_passed": p1,
            "per_model_status": per_status, "per_model": per_model, "ratio": ratio,
            "rho_draws": draws if ratio_status == "DEFINED" else None}


def _reading(r, *names):
    return r.get("reading") if isinstance(r, dict) else r


def _dump(x):
    return json.dumps(x, default=str)


# ----------------------------------------------------------------------------- general


def test_all_support_general():
    r = gx.general([W(t, "SUPPORT") for t in ("lo", "mid", "hi")])
    assert _reading(r) == "GENERAL"


def test_two_support_not_general():
    r = gx.general([W(t, "SUPPORT") for t in ("lo", "mid")])
    assert _reading(r) == "GENERAL_UNAVAILABLE"


def test_not_learned_world_unavailable_never_exclusion():  # DRG7
    ws = [W("lo", "INCONCLUSIVE/NOT_LEARNED", endpoint=False, p1=False),
          W("mid", "SUPPORT"), W("hi", "SUPPORT")]
    r = gx.general(ws)
    assert _reading(r) == "GENERAL_UNAVAILABLE"
    assert "EXCLUSION" not in _dump(r.get("reasons", ""))


def test_rc1_support_plus_mixed_without_exclude():
    mixed = W("hi", "MIXED", statuses=("SUPPORT", "UNRESOLVED", "SUPPORT"))
    r = gx.general([W("lo", "SUPPORT"), W("mid", "SUPPORT"), mixed])
    assert _reading(r) == "GENERAL_UNAVAILABLE"


def test_rc1_mixed_with_unresolved_numerical_not_exclude():
    mixed = W("mid", "MIXED", statuses=("SUPPORT", "UNRESOLVED/NUMERICAL", "SUPPORT"))
    r = gx.general([W("lo", "SUPPORT"), mixed, W("hi", "SUPPORT")])
    assert _reading(r) == "GENERAL_UNAVAILABLE"


def test_rc1_p1_passed_mixed_with_exclude_not_general():
    mixed = W("mid", "MIXED", statuses=("SUPPORT", "EXCLUDE", "UNRESOLVED"))
    r = gx.general([W("lo", "SUPPORT"), mixed, W("hi", "SUPPORT")])
    assert _reading(r) == "NOT_GENERAL"
    d = _dump(r)
    assert "mid" in d or "W12-q1-s2.0-p0.2" in d
    assert "620622" in d


def test_exclude_without_p1_pass_not_general_refused():
    """NOT_GENERAL needs p1_passed and endpoint; an EXCLUDE status otherwise does not count."""
    odd = W("mid", "MIXED", statuses=("SUPPORT", "EXCLUDE", "SUPPORT"), p1=False)
    r = gx.general([W("lo", "SUPPORT"), odd, W("hi", "SUPPORT")])
    assert _reading(r) == "GENERAL_UNAVAILABLE"


def test_exclusion_world_not_general():
    r = gx.general([W("lo", "SUPPORT"), W("mid", "SUPPORT"), W("hi", "EXCLUSION")])
    assert _reading(r) == "NOT_GENERAL"
    assert "620631" in _dump(r)


@pytest.mark.parametrize("bad", ["FAIL_TECHNICAL/TRAINING", "FAIL_TECHNICAL/LAW_BOUND",
                                 "INCONCLUSIVE/ORACLE_FEASIBILITY", "INCONCLUSIVE/UNDERPOWERED"])
def test_failed_or_dropped_world_unavailable(bad):
    r = gx.general([W("lo", bad, endpoint=False, p1=False), W("mid", "SUPPORT"),
                    W("hi", "SUPPORT")])
    assert _reading(r) == "GENERAL_UNAVAILABLE"
    assert r.get("reasons")


# ----------------------------------------------------------------------------- capture


def test_capture_one_endpoint_unavailable():
    ws = [W("lo", "SUPPORT"), W("mid", "FAIL_TECHNICAL/TRAINING", endpoint=False, p1=False),
          W("hi", "INCONCLUSIVE/NOT_LEARNED", endpoint=False, p1=False)]
    assert _reading(gx.capture(ws)) == "CAPTURE_UNAVAILABLE"


def _rh(tag, pairs):
    return dict(zip(MASTERS[tag], pairs))


def test_capture_at_least_half_with_equality():
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(0.5, 0.7), (0.6, 0.8), (0.55, 0.9)])),
          W("mid", "SUPPORT", rho=_rh("mid", [(0.51, 0.7)] * 3)),
          W("hi", "INCONCLUSIVE/NOT_LEARNED", endpoint=False, p1=False)]
    r = gx.capture(ws)
    assert _reading(r) == "CAPTURE_AT_LEAST_HALF"
    assert set(r["worlds_covered"]) >= {"lo", "mid"} or "lo" in _dump(r["worlds_covered"])
    assert "hi" in _dump(r["unavailable"]) or "W12-q1-s2.5-p0.5" in _dump(r["unavailable"])


def test_capture_just_below_half_lower_not_at_least():
    lo_ = np.nextafter(0.5, 0.0)
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(lo_, 0.7), (0.6, 0.8), (0.55, 0.9)])),
          W("mid", "SUPPORT", rho=_rh("mid", [(0.6, 0.7)] * 3))]
    assert _reading(gx.capture(ws)) == "CAPTURE_UNRESOLVED"


def test_capture_below_half():
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(0.6, 0.7), (0.2, 0.49), (0.55, 0.9)])),
          W("mid", "SUPPORT", rho=_rh("mid", [(0.6, 0.7)] * 3))]
    assert _reading(gx.capture(ws)) == "CAPTURE_BELOW_HALF"


def test_capture_upper_exactly_half_not_below():
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(0.4, 0.5), (0.6, 0.8), (0.55, 0.9)])),
          W("mid", "SUPPORT", rho=_rh("mid", [(0.6, 0.7)] * 3))]
    assert _reading(gx.capture(ws)) == "CAPTURE_UNRESOLVED"


def test_capture_unresolved_ratio_world():
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(0.6, 0.7)] * 3)),
          W("mid", "SUPPORT", ratio_status="RATIO_UNRESOLVED")]
    assert _reading(gx.capture(ws)) == "CAPTURE_UNRESOLVED"


def test_capture_precedence_below_half_wins():  # OPEN-7
    ws = [W("lo", "SUPPORT", rho=_rh("lo", [(0.1, 0.3)] * 3)),
          W("mid", "SUPPORT", ratio_status="RATIO_UNRESOLVED"),
          W("hi", "SUPPORT", rho=_rh("hi", [(0.6, 0.9)] * 3))]
    assert _reading(gx.capture(ws)) == "CAPTURE_BELOW_HALF"


# ----------------------------------------------------------------------------- annotations


def test_all_exclusion_needs_two_endpoint_worlds():
    one = [W("lo", "EXCLUSION"), W("mid", "FAIL_TECHNICAL/TRAINING", endpoint=False, p1=False)]
    two = [W("lo", "EXCLUSION"), W("mid", "EXCLUSION"),
           W("hi", "INCONCLUSIVE/NOT_LEARNED", endpoint=False, p1=False)]
    assert "ALL_EXCLUSION" not in _dump(gx.annotations(one))
    assert "ALL_EXCLUSION" in _dump(gx.annotations(two))
    assert "ALL_EXCLUSION" not in _dump(gx.annotations([W("lo", "EXCLUSION"),
                                                       W("mid", "MIXED",
                                                         statuses=("EXCLUDE", "SUPPORT",
                                                                   "EXCLUDE"))]))


def test_positive_everywhere_exact():
    F = 1e-6
    pos = [W(t, "EXCLUSION", L=np.nextafter(F, 1.0), F=F) for t in ("lo", "mid")]
    zero = [W("lo", "EXCLUSION", L=F, F=F), W("mid", "EXCLUSION", L=0.004, F=F)]
    assert "POSITIVE_EVERYWHERE" in _dump(gx.annotations(pos))
    assert "POSITIVE_EVERYWHERE" not in _dump(gx.annotations(zero))
    assert "POSITIVE_EVERYWHERE" not in _dump(gx.annotations(
        [W("lo", "FAIL_TECHNICAL/TRAINING", endpoint=False, p1=False)]))


# ----------------------------------------------------------------------------- similarity


def test_similarity_compatible_and_not():
    same = [W(t, "SUPPORT", rho=0.8, seed=i) for i, t in enumerate(("lo", "mid", "hi"))]
    apart = [W("lo", "SUPPORT", rho=0.3, seed=1), W("mid", "SUPPORT", rho=0.8, seed=2),
             W("hi", "SUPPORT", rho=0.8, seed=3)]
    a, b = gx.similarity(same), gx.similarity(apart)
    assert _compat(a) is True and _compat(b) is False


def _compat(r):
    # API-AMBIGUITY: the label may be a boolean field or the COMMON_FRACTION_COMPATIBLE string
    if isinstance(r.get("compatible"), bool):
        return r["compatible"]
    return "COMMON_FRACTION_COMPATIBLE" in _dump(r).replace("NOT_COMPATIBLE", "")


def test_similarity_spread_pairing():  # OPEN-8
    ws = [W("lo", "SUPPORT", rho=0.6, seed=4), W("mid", "SUPPORT", rho=0.8, seed=5),
          W("hi", "SUPPORT", rho=0.7, seed=6)]
    g = np.random.Generator(np.random.PCG64(620640))
    vs = []
    for w in ws:  # worlds_order lo, mid, hi
        bar = np.mean(np.stack([w["rho_draws"][j] for j in MASTERS[w["tag"]]]), axis=0)
        vs.append(bar[g.permutation(5000)])
    S = np.max(np.stack(vs), axis=0) - np.min(np.stack(vs), axis=0)
    bound = float(np.sort(S)[4916])
    r = gx.similarity(ws, seed=620640)
    nums = _floats(r)
    assert any(abs(x - bound) <= 1e-12 * max(1.0, abs(bound)) for x in nums)
    spread = max(0.6, 0.8, 0.7) - min(0.6, 0.8, 0.7)
    assert any(abs(x - spread) <= 1e-12 for x in nums)


def _floats(x):
    if isinstance(x, dict):
        return [f for v in x.values() for f in _floats(v)]
    if isinstance(x, (list, tuple)):
        return [f for v in x for f in _floats(v)]
    if isinstance(x, (float, np.floating)):
        return [float(x)]
    return []
