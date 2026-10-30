"""Author A (job 0176): the documented-law identity and the pilot exclusions.

Protocol HWSC §3.1 row 5, §4 KC4, §5 gate 1 (H1-C law step); DRC8.
API.md §1.2 (`load_handoff`), §6 (`law_identity`, `exclusion_check`);
hwsb API `law_bound`, `bound_law`, `w0_process`. Real-world builders on a
`MemoryBackend` store only (they draw nothing).
"""

from __future__ import annotations

import copy
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[:1] != [_HWSC]:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402,I001
import hwsc_data as cd  # noqa: E402
import hwsc_gates as cg  # noqa: E402
import c1_records  # noqa: E402
import hwsb_known  # noqa: E402
import hwsb_law  # noqa: E402
import k4b_cert  # noqa: E402
import process_law  # noqa: E402
from topo_pilot.contracts import ArtifactStore, MemoryBackend  # noqa: E402

HV = cc.CONTRACT["handoff"]["values"]
KC4 = cc.CONTRACT["known_cases"]["KC4"]
EXCL = tuple(cc.CONTRACT["handoff"]["stage_c_exclusions"])


def law_state():
    return (process_law.LAW.get("sigma"), process_law.LAW.get("neighbour"),
            process_law.softmax_enclosure)


def assert_restored(before):
    after = law_state()
    assert after[0] == before[0] and after[1] == before[1]
    assert after[2] is before[2]


@pytest.fixture(scope="module")
def proc_star():
    return cd.build_process_c(ArtifactStore(MemoryBackend()))


@pytest.fixture(scope="module")
def handoff():
    return cc.load_handoff()


@pytest.fixture(scope="module")
def identity(proc_star, handoff):
    before = law_state()
    r = cg.law_identity(proc_star, handoff)
    assert_restored(before)
    return r


def test_handoff_values(handoff):
    assert handoff["Z_bound"] == Fraction(HV["Z_bound"]) == Fraction(KC4["w_star_Z_bound"])
    assert handoff["F_plan"] == Fraction(HV["F_plan"]) == Fraction(KC4["F_plan"])
    assert tuple(handoff["stage_c_exclusions"]) == EXCL and len(EXCL) == 24


def test_process_is_w_star(proc_star):
    assert proc_star["sigma"] == Fraction(7, 4)
    assert proc_star["neighbour"] == Fraction(1, 5)
    assert set(proc_star["perm"]) == set(cc.MASTERS)


def test_law_identity_pass(identity, handoff):
    assert identity["status"] == "PASS"
    assert identity["Z_bound"] == handoff["Z_bound"]
    assert isinstance(identity["Z_bound"], Fraction)
    assert Fraction(identity["sigma"]) == Fraction(7, 4)
    assert Fraction(identity["neighbour"]) == Fraction(1, 5)
    assert Fraction(identity["kappa"]) < 1


def test_f_plan_identity(identity, handoff):
    assert k4b_cert.F_plan(handoff["Z_bound"]) == handoff["F_plan"]
    assert k4b_cert.F_plan(identity["Z_bound"]) == Fraction(HV["F_plan"])


def test_law_identity_refuses_last_digit(proc_star, handoff):
    num, den = HV["Z_bound"].split("/")
    last = str((int(num[-1]) + 1) % 10)
    bad = copy.deepcopy(dict(handoff))
    bad["Z_bound"] = Fraction(int(num[:-1] + last), int(den))
    assert bad["Z_bound"] != handoff["Z_bound"]
    before = law_state()
    with pytest.raises(c1_records.C1GateFailure) as ei:
        cg.law_identity(proc_star, bad)
    assert ei.value.status == "FAIL_TECHNICAL/LAW_BOUND"
    assert_restored(before)


def test_law_identity_maps_exception_and_status(proc_star, handoff, monkeypatch):
    def boom(*a, **kw):
        raise ArithmeticError("planted")

    monkeypatch.setattr(hwsb_law, "law_bound", boom)
    with pytest.raises(c1_records.C1GateFailure) as ei:
        cg.law_identity(proc_star, handoff)
    assert ei.value.status == "FAIL_TECHNICAL/LAW_BOUND"

    def unbounded(*a, **kw):
        return {"status": "UNBOUNDED", "Z_bound": None, "kappa": None, "delta": None,
                "sigma": Fraction(7, 4), "neighbour": Fraction(1, 5), "reason": "planted"}

    monkeypatch.setattr(hwsb_law, "law_bound", unbounded)
    with pytest.raises(c1_records.C1GateFailure) as ei:
        cg.law_identity(proc_star, handoff)
    assert ei.value.status == "FAIL_TECHNICAL/LAW_BOUND"


def test_law_identity_called_with_registered_law(proc_star, handoff, monkeypatch):
    seen = {}
    real = hwsb_law.law_bound

    def spy(T, E, pi, coords, *a, **kw):
        seen["args"] = (a, kw)
        seen["E_is_shared"] = E is proc_star["E_canon_shared"]
        return real(T, E, pi, coords, *a, **kw)

    monkeypatch.setattr(hwsb_law, "law_bound", spy)
    r = cg.law_identity(proc_star, handoff)
    assert r["status"] == "PASS"
    a, kw = seen["args"]
    vals = list(a) + [kw.get("sigma"), kw.get("neighbour")]
    assert Fraction(7, 4) in vals and Fraction(1, 5) in vals
    assert seen["E_is_shared"]


def test_w0_law_equals_old_enclosure():
    before = law_state()
    p0 = hwsb_known.w0_process(ArtifactStore(MemoryBackend()))
    law = hwsb_law.law_bound(p0["T"], p0["E_canon_shared"], p0["pi"], p0["coords"],
                             Fraction(5, 4), Fraction(1, 5))
    assert law["status"] == "BOUNDED"
    assert law["Z_bound"] == Fraction(KC4["w0_Z_bound"])
    assert law["delta"] == 0
    assert_restored(before)


def test_exclusion_check():
    fresh = [f"{i:016x}" for i in range(0xabc000, 0xabc006)]
    assert not set(fresh) & set(EXCL)
    handoff = {"stage_c_exclusions": EXCL}
    r = cg.exclusion_check(fresh, handoff)
    assert r["ok"] and list(r["excluded"]) == []
    r = cg.exclusion_check(fresh[:5] + [EXCL[7]], handoff)
    assert not r["ok"] and list(r["excluded"]) == [EXCL[7]]
    r = cg.exclusion_check([EXCL[3], EXCL[1]] + fresh[:4], handoff)
    assert list(r["excluded"]) == sorted([EXCL[3], EXCL[1]])


def test_exclusion_check_fixture_list():
    fixture = {"stage_c_exclusions": ("aaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbb")}
    assert not cg.exclusion_check(["bbbbbbbbbbbbbbbb", "cccccccccccccccc"], fixture)["ok"]
    assert cg.exclusion_check(["cccccccccccccccc"], fixture)["ok"]
