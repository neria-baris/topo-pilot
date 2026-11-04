"""Author A (job 0224): outcome precedence and licences (§7.2, §7.4, §7.5; API §12-§13).

Planted states only. Expected texts come from CONTRACT `licences`, `cross.error_statements`,
`disclosure`; the precedence order from CONTRACT `outcomes.precedence`.
"""

from __future__ import annotations  # noqa: I001

import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hwsb", "hwsc", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc
    import hwsg_cross as gx
    import hwsg_records as grec
except Exception as e:
    _ERR = e

C = json.loads((REPO / "tools" / "hwsg" / "CONTRACT.json").read_text(encoding="utf-8"))
LIC = C["licences"]
HI = (620631, 620632, 620633)


@pytest.fixture(autouse=True)
def _imports():
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")


def _state(**kw):
    s = {"fail": None, "resource": None, "l1": None, "k4b": None, "endpoint": None,
         "criterion": None, "models": None}
    s.update(kw)
    return s


EP_SUPPORT = {"overall": "SUPPORT",
              "per_model": {j: {"L": 0.05, "U": 0.07, "F_minus": 1e-6, "F_plus": 1e-6,
                                "status": "SUPPORT", "labels": []} for j in HI}}
L1 = {"k": 2, "models": [HI[0], HI[2]]}

ROWS = [  # (state, expected outcome), each row one precedence level below the previous
    (_state(fail="FAIL_TECHNICAL/LAW_BOUND", resource="INCONCLUSIVE/RESOURCE_OR_AUTHORITY",
            k4b="INCONCLUSIVE/REGISTRY_RISK", l1=L1, endpoint=EP_SUPPORT),
     "FAIL_TECHNICAL/LAW_BOUND"),
    (_state(resource="INCONCLUSIVE/RESOURCE_OR_AUTHORITY", k4b="INCONCLUSIVE/REGISTRY_RISK",
            l1=L1, endpoint=EP_SUPPORT), "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"),
    (_state(k4b="INCONCLUSIVE/REGISTRY_RISK", l1=L1, endpoint=EP_SUPPORT),
     "INCONCLUSIVE/REGISTRY_RISK"),
    (_state(k4b="INCONCLUSIVE/ORACLE_FEASIBILITY", l1=L1, endpoint=EP_SUPPORT),
     "INCONCLUSIVE/ORACLE_FEASIBILITY"),
    (_state(k4b="INCONCLUSIVE/REGISTRY_INCOMPLETE", l1=L1, endpoint=EP_SUPPORT),
     "INCONCLUSIVE/REGISTRY_INCOMPLETE"),
    (_state(l1=L1, k4b="INCONCLUSIVE/UNDERPOWERED", endpoint=EP_SUPPORT),
     "INCONCLUSIVE/NOT_LEARNED"),
    (_state(k4b="INCONCLUSIVE/UNDERPOWERED", endpoint=EP_SUPPORT), "INCONCLUSIVE/UNDERPOWERED"),
    (_state(k4b="INCONCLUSIVE/HEADROOM", endpoint=EP_SUPPORT), "INCONCLUSIVE/HEADROOM"),
    (_state(endpoint=EP_SUPPORT), "SUPPORT"),
]


@pytest.mark.parametrize("state,expected", ROWS)
def test_precedence(state, expected):
    # API-AMBIGUITY: rank-3 statuses are planted in the `k4b` slot (API §12 "mapping ... to rank 3")
    oc = grec.outcome_g(state)
    assert oc["outcome"] == expected


def test_not_learned_label_k_of_3():
    oc = grec.outcome_g(_state(l1=L1))
    assert oc["outcome"] == "INCONCLUSIVE/NOT_LEARNED" and "2/3" in oc["label"]


def test_endpoint_outcomes_pass_through():
    for ov in ("EXCLUSION", "MIXED", "INCONCLUSIVE", "INCONCLUSIVE/NUMERICAL"):
        ep = dict(EP_SUPPORT, overall=ov)
        assert grec.outcome_g(_state(endpoint=ep))["outcome"] == ov


# ----------------------------------------------------------------------------- licences

KEY_HI = C["worlds"]["hi"]["key"]


def test_world_support_and_exclusion_licence():
    for head in ("SUPPORT", "EXCLUSION"):
        t = gx.licence(head, {"world": KEY_HI, "N": 6144})
        assert KEY_HI in t and ("6144" in t or "{N}" not in LIC[head])
        assert t == LIC[head].format_map({"world": KEY_HI, "N": 6144})


def test_not_general_carries_error_statement():
    t = gx.licence("NOT_GENERAL", {"worlds": "mid", "models": "620622"})
    assert "mid" in t and "620622" in t
    es = C["cross"]["error_statements"]["NOT_GENERAL"]
    assert es.lower().rstrip(".") in t.lower() or "0.30" in t


def test_capture_at_least_half_names_unavailable():
    t = gx.licence("CAPTURE_AT_LEAST_HALF", {"n": 6, "worlds": "lo, mid", "unavailable": "hi"})
    assert "hi" in t and "lo, mid" in t and "6" in t


def test_general_unavailable_missing_key_na():
    t = gx.licence("GENERAL_UNAVAILABLE", {})
    assert "n/a" in t and "{" not in t


@pytest.mark.parametrize("word", ["compatible", "not compatible"])
def test_similarity_sentence_words(word):
    t = gx.licence("SIMILARITY", {"compatible": word})
    # API-AMBIGUITY: the fill may be the word or a boolean; either sentence is accepted
    if f"are {word} with" not in t:
        t = gx.licence("SIMILARITY", {"compatible": word == "compatible"})
    assert f"are {word} with" in t
    for bad in ("equal", "equivalent", "same fraction", "significant"):
        assert bad not in t.lower()


def test_disclosure_and_does_not_establish():
    assert gc.DISCLOSURE == C["disclosure"]
    items = LIC["does_not_establish"]
    nums = set()
    for it in items:
        m = re.match(r"(\d+) ", it)
        if m:
            nums.add(int(m.group(1)))
    assert nums == set(range(15, 27))
    assert any("items 1-10" in it and "11-14" in it for it in items)
