"""Author A (job 0223): per-model response statements (protocol 2.9 table; API_U2 4.4 model_status).

Hand-built bounds {stat: {"L", "U", "g"}}; a bound inside its guard (|b| <= g) is neither sign.
Status names are compared after normalising the model suffix (`_j` or `_<master>`), since
API_U2 writes them as RESPONDS_j etc. (ambiguity noted in AUTHORSHIP_A_U2.md)."""

from __future__ import annotations  # noqa: I001

import importlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,F401
import c2_decide  # noqa: E402
import pytest  # noqa: E402

G = 0.01


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def norm(s):
    return re.sub(r"_(j|\d+)(?=$|/)", "_j", s)


def bj(l1, u1, l3, u3, laf=None, uaf=None, g=G):
    laf = l1 if laf is None else laf
    uaf = 1.0 if uaf is None else uaf
    return {
        "ZR010": {"L": l1, "U": u1, "g": g, "mean": (l1 + u1) / 2},
        "ZR030": {"L": l3, "U": u3, "g": g, "mean": (l3 + u3) / 2},
        "AF": {"L": laf, "U": uaf, "g": g, "mean": (laf + uaf) / 2},
    }


def status(b):
    return norm(mod("hwsu_gates").model_status(b)["status"])


def test_responds():
    assert status(bj(0.5, 0.7, 0.2, 0.4)) == "RESPONDS_j"


def test_weak_response():
    assert status(bj(0.05, 0.2, -0.2, -0.05)) == "WEAK_RESPONSE_j"


def test_low_response():
    assert status(bj(-0.3, -0.05, -0.5, -0.25)) == "LOW_RESPONSE_j"


def test_low_response_reachable_with_negative_theta():
    # theta < 0: A < 0 so ZR010, ZR030 and AF all clearly negative
    r = mod("hwsu_gates").model_status(bj(-0.9, -0.6, -1.1, -0.8, laf=-0.7, uaf=-0.4))
    assert norm(r["status"]) == "LOW_RESPONSE_j"
    assert r["rule6"] is False


def test_inconclusive_when_no_row_holds():
    # L(ZR010) > g, but ZR030 straddles zero clearly outside the guard
    assert status(bj(0.05, 0.3, -0.2, 0.2)) == "INC_j"


@pytest.mark.parametrize("edge", [G, -G])
def test_bound_exactly_at_guard_is_neither_sign(edge):
    # L(ZR010) exactly at +g / -g: neither sign; RESPONDS would otherwise hold
    b = bj(edge, 0.7, 0.2, 0.4)
    assert c2_decide.sign(edge, G) == 0
    assert status(b) == "INC_j/NUMERICAL"
    assert status(b) == norm(_expected(b))


def _expected(b):
    m = {"USED": "RESPONDS_j", "PARTIAL": "WEAK_RESPONSE_j", "NOT_USED": "LOW_RESPONSE_j"}
    m.update({"LOW_ALIGNED": "LOW_RESPONSE_j", "INC": "INC_j", "INC/NUMERICAL": "INC_j/NUMERICAL"})
    cat = c2_decide._category({s: dict(b[s]) for s in ("ZR010", "ZR030")}, "ZR010", "ZR030", ())
    return m[cat]


def test_mean_exactly_at_line_never_declared():
    # a bound equal to 0 (mean on the 0.10 line, zero width): inside the guard
    b = bj(0.0, 0.0, -0.2, -0.2)
    assert status(b) == "INC_j/NUMERICAL"


def test_grid_agrees_with_category_mapping():
    vals = (-0.5, -G, -G / 2, 0.0, G / 2, G, 0.5)
    for l1 in vals:
        for u1 in vals:
            for l3 in vals:
                for u3 in vals:
                    if l1 > u1 or l3 > u3:
                        continue
                    b = bj(l1, u1, l3, u3)
                    assert status(b) == _expected(b), (l1, u1, l3, u3)


@pytest.mark.parametrize(
    "laf,u3,want",
    [(0.2, -0.2, True), (G, -0.2, False), (0.2, -G, False), (-0.1, -0.2, False), (0.2, 0.1, False)],
)
def test_rule6(laf, u3, want):
    b = bj(0.05, 0.2, -0.4, u3, laf=laf, uaf=0.6)
    assert mod("hwsu_gates").model_status(b)["rule6"] is want


def test_rule6_with_weak_response():
    r = mod("hwsu_gates").model_status(bj(0.05, 0.2, -0.2, -0.05, laf=0.15, uaf=0.4))
    assert norm(r["status"]) == "WEAK_RESPONSE_j" and r["rule6"] is True


def test_rule6_not_with_responds():
    r = mod("hwsu_gates").model_status(bj(0.5, 0.7, 0.2, 0.4, laf=0.6, uaf=0.9))
    assert r["rule6"] is False


def _coarse(r):
    return set(r["coarse"])


def test_coarse_statements():
    ug = mod("hwsu_gates")
    assert _coarse(ug.model_status(bj(0.05, 0.3, -0.2, 0.2))) == {"theta > 0.10"}
    assert _coarse(ug.model_status(bj(-0.3, 0.3, -0.5, -0.2))) == {"theta < 0.30"}
    both = ug.model_status(bj(0.05, 0.2, -0.2, -0.05))
    assert _coarse(both) == {"theta > 0.10", "theta < 0.30"}
    assert _coarse(ug.model_status(bj(-0.3, 0.3, -0.2, 0.2))) == set()
    assert _coarse(ug.model_status(bj(G, 0.3, -0.2, -G))) == set()


def test_bounds_returned():
    b = bj(0.5, 0.7, 0.2, 0.4)
    r = mod("hwsu_gates").model_status(b)
    assert "bounds" in r
