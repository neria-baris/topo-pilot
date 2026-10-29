"""Author B (job 0176): the versioned binding, its audit and the KC7-type stream check.

Written from tools/hwsc/PROTOCOL_HWSC_v1.md section 3.1-3.2, API.md sections 1-2 and 18,
CONTRACT.json `binding`, `seeds`, `masters` and TEST_PLAN.md section 3 only (DRC3, KC7).
"""

from __future__ import annotations

import copy
import importlib
import sys
import types
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402
import hwsc_bind as cb  # noqa: E402
import c1_records  # noqa: E402
from topo_pilot.contracts import SeedTree  # noqa: E402

C = cc.CONTRACT
OLD_MODELS = (1729, 2718, 3141)
NEW_MODELS = (620301, 620302, 620303)
STAGE_C_SEEDS = {
    "val_sd": 620311, "val_b4": 620312, "endpoint": 620313, "fresh_b4": 620314,
    "val_projection": 620315,
}
ROOT = Path("X:/Downloads/projects/topo-pilot")


def _status(exc_info):
    return getattr(exc_info.value, "status", None)


def _live(rows):
    """(module, name, object) for every row, read from the live modules."""
    return [(r["module"], r["name"], getattr(importlib.import_module(r["module"]), r["name"]))
            for r in rows]


def _by_name(rows):
    return {(r["module"], r["name"]): r for r in rows}


# ---------------------------------------------------------------- constants (cc.SEEDS, MASTERS)
def test_config_constants_equal_contract():
    assert cc.SCOPE == "hwsc-v1" and cc.KEY == "W12-q1-s1.75-p0.2"
    assert tuple(cc.PROCESS) == ("cylinder", "overlap", "1.75")
    assert cc.MASTERS == NEW_MODELS == tuple(C["masters"])
    assert cc.DRY_MASTERS == (629911, 629912, 629913) == tuple(C["dry_masters"])
    assert all(type(m) is int for m in cc.MASTERS + cc.DRY_MASTERS)
    assert cc.SEEDS == STAGE_C_SEEDS == C["seeds"]["k4b_seed_names"]
    assert tuple(cc.P1C_SEEDS) == (620311, 620315) == tuple(C["seeds"]["p1c_seeds"])
    assert cc.DRY_SEEDS == {"val_sd": 629921, "val_b4": 629922, "endpoint": 629923,
                            "fresh_b4": 629924, "val_projection": 629925}
    assert list(cc.NEEDLES) == C["seeds"]["g0_needles"] and len(cc.NEEDLES) == 12
    assert cc.SIZES == {"train": 131072, "dev": 4096, "lgate": 4096, "cal": 3072, "val": 3072}
    assert (cc.BLOCK, cc.LGATE_N, cc.PANEL, tuple(cc.LADDER)) == (3072, 4096, 512,
                                                                  (3072, 6144, 12288))
    assert cc.M == Fraction(1, 100) and cc.ALPHA == Fraction(1, 60)
    assert cc.SIGMA == Fraction(7, 4) and cc.NEIGHBOUR == Fraction(1, 5)
    assert (cc.HOLD_S, cc.HOLD_FROM, cc.STEPS) == (6006.6282, 1000, 5000)
    assert cc.HOLD_S == C["cpu"]["per_model_hold_s"]
    assert (cc.RESERVATION_FILE, cc.RESERVATION_ID) == ("RESERVATION_W2.json", "RES-HWSC-W2")
    assert cc.DISCLOSURE == C["disclosure"]
    assert Path(cc.ROOT) == ROOT and Path(cc.STORE) == ROOT / "hwsc-store"
    assert Path(cc.SCRATCH) == Path("X:/Downloads/topo-scratch")
    assert Path(cc.DRY_STORE) == Path("X:/Downloads/topo-scratch/hwsc-dry")


def test_config_margin_matches_k4b():
    import k4b_config

    assert cc.M == k4b_config.MARGIN and cc.RANKS == k4b_config.RANKS
    assert cc.RANKS == {"alpha": 84, "one_minus_alpha": 4917, "b4_lower": 250,
                        "central_lo": 125, "central_hi": 4875}


# ---------------------------------------------------------------- decode and the table
def test_decode_each_encoding(tmp_path):
    assert cb.decode([1, 2, 3]) == (1, 2, 3) and type(cb.decode([1, 2])) is tuple
    assert cb.decode({"__path__": "X:/a/b"}) == Path("X:/a/b")
    assert isinstance(cb.decode({"__path__": "X:/a/b"}), Path)
    assert cb.decode({"__repo__": "tools/x.json"}, repo=tmp_path) == tmp_path / "tools/x.json"
    d = cb.decode({"__dict__": {"a": 1, "b": 2}})
    assert type(d) is dict and d == {"a": 1, "b": 2}
    view = cb.decode({"__contract_view__": "k4b_contract_view"})
    assert view == C["k4b_contract_view"] and view is not C["k4b_contract_view"]
    assert cb.decode(7) == 7 and cb.decode("k4b-sf-v1") == "k4b-sf-v1"
    marker = cb.decode({"__contract__": "ab" * 32})
    assert marker != "ab" * 32  # a marker object, not the bare string


def test_load_table_has_the_21_contract_rows():
    rows = cb.load_table()
    raw = C["binding"]["table"]
    assert len(rows) == 21 == len(raw)
    for r, w in zip(rows, raw):
        assert (r["module"], r["name"]) == (w["module"], w["name"])
        assert r["old"] == cb.decode(w["old"]) or w["name"] == "CONTRACT"
        assert r["new"] == cb.decode(w["new"])
    t = _by_name(rows)
    assert t[("k4b_config", "MODELS")]["old"] == OLD_MODELS
    assert t[("k4b_config", "MODELS")]["new"] == NEW_MODELS
    assert t[("hwsb_config", "SCOPE")]["old"] == "hwsb-v1"
    assert t[("hwsb_config", "MASTERS")]["old"] == (620201, 620202)
    assert t[("hwsb_config", "DRY_MASTERS")]["new"] == (629911, 629912, 629913)
    assert t[("k4b_driver", "SEEDS")]["new"] == STAGE_C_SEEDS
    assert t[("k4b_config", "CONTRACT")]["new"] == C["k4b_contract_view"]
    assert t[("k4b_config", "CONTRACT_PATH")]["new"] == REPO / "tools/hwsc/CONTRACT.json"
    assert cb.never_called() == tuple(C["binding"]["never_called"])


def test_check_old_is_empty_on_live_modules():
    assert cb.check_old(cb.load_table()) == []


@pytest.fixture
def synth(monkeypatch):
    mod = types.ModuleType("b_bind_synth")
    mod.X = (1, 2)
    mod.P = Path("X:/Downloads/b/store")
    mod.S = "X:/Downloads/b/store"
    mod.C = {"protocol_sha256": "ab" * 32, "other": 1}
    monkeypatch.setitem(sys.modules, "b_bind_synth", mod)
    return mod


def test_check_old_rules_on_a_synthetic_module(synth):
    row = {"module": "b_bind_synth", "name": "X", "old": (1, 2), "new": (3, 4)}
    assert cb.check_old([row]) == []
    synth.X = [1, 2]  # equal values, different type
    assert len(cb.check_old([row])) == 1
    path_row = {"module": "b_bind_synth", "name": "P", "old": Path("X:/Downloads/b/store"),
                "new": Path("X:/x")}
    assert cb.check_old([path_row]) == []
    str_row = dict(path_row, name="S")  # a str is not a Path
    assert len(cb.check_old([str_row])) == 1
    good = {"module": "b_bind_synth", "name": "C", "old": cb.decode({"__contract__": "ab" * 32}),
            "new": {}}
    bad = dict(good, old=cb.decode({"__contract__": "cd" * 32}))
    assert cb.check_old([good]) == [] and len(cb.check_old([bad])) == 1


def test_bound_stage_c_on_a_synthetic_table(synth):
    before = synth.X
    table = [{"module": "b_bind_synth", "name": "X", "old": (1, 2), "new": (3, 4)}]
    with cb.bound_stage_c(table) as info:
        assert synth.X == (3, 4) and cb.ACTIVE is True
        assert info["rows"] == 1 and len(info["table_sha256"]) == 64
    assert synth.X is before and cb.ACTIVE is False


# ---------------------------------------------------------------- the real binding
def test_bound_stage_c_sets_every_name_and_restores_identity():
    rows = cb.load_table()
    before = _live(rows)
    assert cb.ACTIVE is False
    with cb.bound_stage_c():
        import hwsb_config
        import k4b_config
        import k4b_data
        import k4b_driver
        import k4b_stats

        for mod, name, _ in before:
            assert getattr(sys.modules[mod], name) == _by_name(rows)[(mod, name)]["new"]
        assert k4b_config.MODELS == NEW_MODELS and k4b_stats.MODELS == NEW_MODELS
        assert k4b_data.SCOPE == "hwsc-v1" and k4b_data.PROCESS[2] == "1.75"
        assert k4b_driver.SEEDS["endpoint"] == 620313
        assert Path(k4b_driver.ARTIFACTS) == ROOT / "hwsc-store" / "artifacts"
        assert Path(k4b_config.STORE) == ROOT / "hwsc-store"
        assert k4b_config.CONTRACT["protocol_sha256"] == C["protocol_sha256"]
        assert hwsb_config.SCOPE == "hwsc-v1"
        assert hwsb_config.MASTERS == NEW_MODELS
        assert hwsb_config.DRY_MASTERS == (629911, 629912, 629913)
        assert cb.ACTIVE is True
        aud = cb.audit()
        assert aud["status"] == "PASS" and aud["unlisted"] == []
        listed = {(r["module"], r["name"]) for r in C["binding"]["left_unchanged"]}
        assert ("k4b_stats", "sd_upper.__defaults__") in listed
        # API-AMBIGUITY: the hit's top name is read from "where" (prefix) or a "top" key.
        tops = {(h["module"], str(h.get("top", h["where"]))) for h in aud["hits"]}
        for fn in ("sd_upper.__defaults__", "centered.__defaults__"):
            assert any(m == "k4b_stats" and w.startswith(fn) for m, w in tops), fn
    assert cb.ACTIVE is False
    for mod, name, obj in before:
        assert getattr(sys.modules[mod], name) is obj, (mod, name)


def test_exception_inside_restores_everything():
    before = _live(cb.load_table())
    with pytest.raises(KeyError):
        with cb.bound_stage_c():
            raise KeyError("planted")
    for mod, name, obj in before:
        assert getattr(sys.modules[mod], name) is obj
    assert cb.ACTIVE is False


def test_entering_twice_fails_with_binding():
    before = _live(cb.load_table())
    with cb.bound_stage_c():
        with pytest.raises(c1_records.C1GateFailure) as e:
            with cb.bound_stage_c():
                pass
        assert _status(e) == "FAIL_TECHNICAL/BINDING"
        import k4b_config

        assert k4b_config.MODELS == NEW_MODELS  # the outer binding is untouched
    for mod, name, obj in before:
        assert getattr(sys.modules[mod], name) is obj


def test_planted_drift_refuses_and_sets_nothing(monkeypatch):
    import k4b_config
    import k4b_data

    monkeypatch.setattr(k4b_data, "SCOPE", "x")
    models = k4b_config.MODELS
    with pytest.raises(c1_records.C1GateFailure) as e:
        with cb.bound_stage_c():
            pytest.fail("entered a drifted binding")
    assert _status(e) == "FAIL_TECHNICAL/BINDING"
    assert k4b_config.MODELS is models and k4b_data.SCOPE == "x" and cb.ACTIVE is False


def test_audit_outside_the_binding_fails():
    aud = cb.audit()
    assert aud["status"] == "FAIL_TECHNICAL/BINDING"
    assert any(h["module"] == "k4b_config" and str(h.get("top", h["where"])).startswith("MODELS")
               for h in aud["unlisted"])


# ---------------------------------------------------------------- planted audit defects
PLANTS = [
    ("X = (1729, 2718, 3141)\n", "X"),
    ("D = {1729: 'a', 2718: 'b', 3141: 'c'}\n", "D"),
    ("def f(a=610101):\n    return a\n", "f.__defaults__"),
    ("def g(*, b=620202):\n    return b\n", "g.__kwdefaults__"),
    ("class K:\n    def m(self, a=(1, 610103)):\n        return a\n", "K.m.__defaults__"),
    ("class S:\n    @staticmethod\n    def s(a=620214):\n        return a\n", "S.s.__defaults__"),
    ("import dataclasses\n@dataclasses.dataclass(frozen=True)\nclass DC:\n    f: tuple\n"
     "INST = DC((620201, 620202))\n", "INST"),
    ("from pathlib import Path\nP = Path('X:/Downloads/projects/topo-pilot/k4b-store')\n", "P"),
    ("S = 'X:/Downloads/projects/topo-pilot/k4b-store/'\n", "S"),
    ("W = 'X:/Downloads/topo-scratch/hwsb-dry'\n", "W"),
    ("TAG = ['ok', {'deep': ['hwsb-v1']}]\n", "TAG"),
    ("SD = {'val_sd': 610101, 'val_b4': 1}\n", "SD"),
    ("PR = ('cylinder', 'overlap', '1.25')\n", "PR"),
]


def _module(monkeypatch, name, src):
    mod = types.ModuleType(name)
    monkeypatch.setitem(sys.modules, name, mod)
    exec(compile(src, f"<{name}>", "exec"), mod.__dict__)
    return mod


@pytest.mark.parametrize("src,top", PLANTS, ids=[p[1] for p in PLANTS])
def test_planted_defect_is_a_hit(monkeypatch, src, top):
    name = "b_audit_" + top.replace(".", "_")
    mod = _module(monkeypatch, name, src)
    aud = cb.audit(modules=[mod])
    assert aud["status"] == "FAIL_TECHNICAL/BINDING"
    assert aud["unlisted"] and all(h["module"] == name for h in aud["unlisted"])
    assert aud["n_hits"] >= 1 and name in aud["modules"]
    # Covering exactly (module, top name) on left_unchanged makes the audit pass.
    cover = [{"module": name, "name": top, "reason": "planted"}]
    ok = cb.audit(modules=[mod], left_unchanged=cover)
    assert ok["status"] == "PASS" and ok["unlisted"] == [], ok


def test_clean_module_and_bool_and_foreign_functions(monkeypatch):
    other = _module(monkeypatch, "b_audit_other", "def far(a=610101):\n    return a\n")
    assert cb.audit(modules=[other])["status"] == "FAIL_TECHNICAL/BINDING"
    mod = _module(monkeypatch, "b_audit_clean",
                  "FLAG = True\nN = 0\nT = (True, False)\nS = 'hwsc-v1'\nM = (620301,)\n")
    mod.FAR = other.far  # a function defined elsewhere: its defaults belong to its own module
    aud = cb.audit(modules=[mod])
    assert aud["status"] == "PASS" and aud["hits"] == [] and aud["unlisted"] == []


def test_wrong_top_name_does_not_cover(monkeypatch):
    mod = _module(monkeypatch, "b_audit_wrong", "def f(a=610101):\n    return a\n")
    cover = [{"module": "b_audit_wrong", "name": "f", "reason": "global, not defaults"}]
    assert cb.audit(modules=[mod], left_unchanged=cover)["status"] == "FAIL_TECHNICAL/BINDING"


# ---------------------------------------------------------------- identity and dry tables
def test_identity_table_is_a_no_op():
    rows = cb.load_table(which="identity")
    assert len(rows) == 21
    for r in rows:
        assert r["new"] == r["old"]
    before = _live(rows)
    with cb.bound_stage_c(rows):
        for mod, name, obj in before:
            assert getattr(sys.modules[mod], name) == obj
        import k4b_config

        assert k4b_config.MODELS == OLD_MODELS
    for mod, name, obj in before:
        assert getattr(sys.modules[mod], name) is obj


def test_dry_table_binds_the_dry_values(tmp_path):
    case_dir = tmp_path / "case"
    rows = cb.load_table(which="dry", case="DRC1", case_dir=case_dir)
    t = _by_name(rows)
    assert len(rows) == 21
    for mod in ("k4b_config", "k4b_data", "k4b_stats", "k4b_driver", "k4b_fresh"):
        assert t[(mod, "MODELS")]["new"] == (629911, 629912, 629913)
    for mod in ("k4b_config", "k4b_data", "k4b_decoder"):
        assert t[(mod, "SCOPE")]["new"] == "hwsc-v1/DRY/DRC1"
    for mod in ("k4b_config", "k4b_data"):
        assert tuple(t[(mod, "PROCESS")]["new"]) == ("cylinder", "overlap", "1.0")
    for mod in ("k4b_config", "k4b_driver", "k4b_fresh"):
        assert t[(mod, "SEEDS")]["new"] == cc.DRY_SEEDS
    assert Path(t[("k4b_config", "STORE")]["new"]) == case_dir
    assert Path(t[("k4b_driver", "ARTIFACTS")]["new"]) == case_dir / "artifacts"
    assert t[("hwsb_config", "SCOPE")]["new"] == "hwsc-v1"
    assert t[("hwsb_config", "MASTERS")]["new"] == NEW_MODELS
    assert t[("hwsb_config", "DRY_MASTERS")]["new"] == (629911, 629912, 629913)
    before = _live(rows)
    with cb.bound_stage_c(rows):
        import k4b_data

        assert k4b_data.MODELS == (629911, 629912, 629913)
        assert k4b_data.SCOPE == "hwsc-v1/DRY/DRC1"
    for mod, name, obj in before:
        assert getattr(sys.modules[mod], name) is obj


@pytest.mark.parametrize("kw", [{}, {"case": "DRC1"}, {"case_dir": "x"}])
def test_dry_table_requires_case_and_dir(kw):
    with pytest.raises(ValueError):
        cb.load_table(which="dry", **kw)


def test_table_is_not_mutated_by_binding():
    rows = cb.load_table()
    snap = copy.deepcopy(rows)
    with cb.bound_stage_c(rows):
        pass
    assert rows == snap


# ---------------------------------------------------------------- KC7-type stream check
def test_kc7_cal_stream_inside_the_binding():
    import k4b_data

    ref = SeedTree(0).generator("data", "hwsc-v1", "cal", 0, "cylinder", "overlap", "1.75")
    want = ref.integers(0, 2**63, size=64)
    with cb.bound_stage_c():
        got = k4b_data.history_generator("cal", 0).integers(0, 2**63, size=64)
    assert np.array_equal(got, want)
    outside = k4b_data.history_generator("cal", 0).integers(0, 2**63, size=64)
    assert not np.array_equal(outside, want)  # unbound: the K4b scope and process
