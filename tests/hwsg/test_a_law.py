"""Author A (job 0224): process override and law bound per sigma (O1/O2/O3; KG5; DRG8).

Real-world builders on a MemoryBackend store (they draw nothing). Expected values from CONTRACT,
hwsb-store/HANDOFF.json (hash-checked) and exact Fraction arithmetic written here.
"""

from __future__ import annotations  # noqa: I001

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hws", "hwsb", "hwsc", "x4_circle_history", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc
    import hwsg_oracle as go
    import hwsb_data
    import hwsb_law
    import hws_exact
    import k4b_cert
    import process_law
    from topo_pilot.contracts import ArtifactStore, MemoryBackend
except Exception as e:
    _ERR = e

ROOT = Path("X:/Downloads/projects/topo-pilot")
C = json.loads((REPO / "tools" / "hwsg" / "CONTRACT.json").read_text(encoding="utf-8"))
TAGS = ("lo", "mid", "hi")
NEIGHBOUR = {"lo": Fraction(1, 24), "mid": Fraction(1, 5), "hi": Fraction(1, 8)}


@pytest.fixture(autouse=True)
def _imports():
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")


def _status(fn, *a, **k):
    try:
        r = fn(*a, **k)
    except Exception as e:
        return getattr(e, "status", repr(e)), None
    return (r.get("status") if isinstance(r, dict) else None), r


_PROCS = {}


def _proc(tag):
    if tag not in _PROCS:
        _PROCS[tag] = go.build_process_g(ArtifactStore(MemoryBackend()), tag)
    return _PROCS[tag]


def test_neighbour_rule_exact():
    for tag in TAGS:
        w = C["worlds"][tag]
        assert (1 - Fraction(w["p"])) / 4 == NEIGHBOUR[tag] == Fraction(w["neighbour"])
    # the unpatched float rule differs for lo
    assert (1 - Fraction(repr(5 / 6))) / 4 != Fraction(1, 24)


@pytest.mark.parametrize("tag", TAGS)
def test_build_process_g_overrides_exact(tag):
    proc = _proc(tag)
    w = C["worlds"][tag]
    assert proc["sigma"] == Fraction(w["sigma"]) and isinstance(proc["sigma"], Fraction)
    assert proc["neighbour"] == NEIGHBOUR[tag] and isinstance(proc["neighbour"], Fraction)


def test_identity_refuses_float_repr_neighbour():
    proc = dict(_proc("lo"))
    proc["neighbour"] = (1 - Fraction(repr(5 / 6))) / 4
    st, r = _status(go.identity, ArtifactStore(MemoryBackend()), proc, "lo")
    # API-AMBIGUITY: identity may return ok False or raise FAIL_TECHNICAL/IDENTITY
    assert (r is not None and r["ok"] is False) or st == "FAIL_TECHNICAL/IDENTITY"


@pytest.mark.parametrize("tag", TAGS)
def test_law_per_sigma(tag):
    r = go.law(_proc(tag), tag)
    z_ref = Fraction(C["worlds"][tag]["stage_a"]["law_bound_Z_exact_upper"])
    assert r["status"] in ("BOUNDED", "PASS")
    assert Fraction(r["kappa"]) < 1
    assert Fraction(r["delta"]) == 0
    assert Fraction(r["Z_bound"]) == z_ref
    assert Fraction(r["F_plan"]) == k4b_cert.F_plan(z_ref) <= Fraction(1, 1000)


def test_law_F_plan_above_max_fails(monkeypatch):
    monkeypatch.setattr(k4b_cert, "F_plan", lambda z: Fraction(1, 1000) + Fraction(1, 10**12))
    assert _status(go.law, _proc("hi"), "hi")[0] == "FAIL_TECHNICAL/LAW_BOUND"


def test_law_Z_off_by_one_numerator_fails(monkeypatch):
    real = hwsb_law.law_bound

    def off(*a, **k):
        r = dict(real(*a, **k))
        z = Fraction(r["Z_bound"])
        r["Z_bound"] = Fraction(z.numerator + 1, z.denominator)
        return r

    monkeypatch.setattr(hwsb_law, "law_bound", off)
    assert _status(go.law, _proc("hi"), "hi")[0] == "FAIL_TECHNICAL/LAW_BOUND"


def test_law_nonbounded_fails(monkeypatch):
    monkeypatch.setattr(hwsb_law, "law_bound", lambda *a, **k: {
        "status": "UNAVAILABLE/NONTERMINATING_LOGIT", "Z_bound": None, "kappa": None,
        "delta": None})
    assert _status(go.law, _proc("mid"), "mid")[0] == "FAIL_TECHNICAL/LAW_BOUND"


def test_w_star_law_equals_handoff():
    hp = ROOT / "hwsb-store" / "HANDOFF.json"
    if not hp.is_file():
        pytest.skip("HANDOFF.json not present")
    assert hashlib.sha256(hp.read_bytes()).hexdigest() == C["w_star"]["handoff_sha256"]
    h = json.loads(hp.read_text(encoding="utf-8"))
    proc = hwsb_data.build_process(ArtifactStore(MemoryBackend()))  # w* configs (defaults)
    r = hwsb_law.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"],
                           sigma=Fraction(7, 4), neighbour=Fraction(1, 5))
    assert r["Z_bound"] == Fraction(h["Z_bound"])
    assert k4b_cert.F_plan(r["Z_bound"]) == Fraction(h["F_plan"])


def test_sigma_5_4_enclosure_delta_zero():
    """DRG8: at sigma 5/4 the rounded enclosure equals process_law.softmax_enclosure (delta 0)."""
    w0_emis = sys.modules["hwsb_config"].W0_EMIS_CFG
    proc = hwsb_data.build_process(ArtifactStore(MemoryBackend()), emission_cfg=w0_emis)
    states = process_law.lattice_states(proc["coords"])
    original = process_law.softmax_enclosure
    with hwsb_law.bound_law(Fraction(5, 4), Fraction(1, 5)):
        a = original(states)
        b = hwsb_law.softmax_enclosure_rounded(states)
        d = hwsb_law.rounding_delta(states)
    assert Fraction(d["delta"]) == 0
    assert a[1] == b[1] and a[2] == b[2]
    assert [list(r) for r in a[0]] == [list(r) for r in b[0]]


# ----------------------------------------------------------------------------- O3 d2a


def _boundary_p():
    """Largest float p with 22528 * Fraction(p) <= 1/100 (independent search)."""
    p = 1 / 2252800
    while 22528 * Fraction(p) > Fraction(1, 100):
        p = math.nextafter(p, 0)
    while 22528 * Fraction(math.nextafter(p, 1)) <= Fraction(1, 100):
        p = math.nextafter(p, 1)
    return p


DUMMY = {"T": None, "E_canon_shared": None, "pi": None}


def test_d2a_boundary_passes(monkeypatch):
    p = _boundary_p()
    monkeypatch.setattr(hws_exact, "p_d2a", lambda *a, **k: p)
    st, r = _status(go.d2a, DUMMY)
    assert r is not None and r["ok"] is True
    assert Fraction(r["value"]) == 22528 * Fraction(p) <= Fraction(1, 100)


def test_d2a_above_fails(monkeypatch):
    p = math.nextafter(_boundary_p(), 1)
    monkeypatch.setattr(hws_exact, "p_d2a", lambda *a, **k: p)
    st, r = _status(go.d2a, DUMMY)
    # API-AMBIGUITY: ok False returned, or INCONCLUSIVE/REGISTRY_RISK raised/returned
    assert st == "INCONCLUSIVE/REGISTRY_RISK" or (r is not None and r["ok"] is False)
