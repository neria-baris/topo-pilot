"""Author B: binding and rebinding (protocol 2.3, G3, KG1, DRG3). Black-box on API.md section 2."""
from __future__ import annotations

import importlib
import sys
import textwrap
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, TAGS, expect_fail, mod  # noqa: E402

ROW_NAMES = CONTRACT["binding"]["rows_per_world"]
ADAPTERS = ("hwsc_config.load_handoff", "hwsc_data.build_process_c", "hwsc_data.process_identity")
NON_PLAIN = ("TRANS_CFG", "EMIS_CFG", "REAL_PLAN", "HWSC_PLAN", "load_handoff",
             "build_process_c", "process_identity")


def _res(dotted):
    m, n = dotted.split(".")
    return importlib.import_module(m), n


def _snapshot():
    mod("gb")
    return {d: getattr(*_res(d)) for d in ROW_NAMES}


@pytest.mark.parametrize("tag", TAGS)
def test_rows_listing(tag):
    gb = mod("gb")
    rows = gb.rows(tag)
    assert [f"{r['module']}.{r['name']}" for r in rows] == ROW_NAMES


@pytest.mark.parametrize("tag", TAGS)
def test_values_inside_and_restored_after(tag):
    gb, gc = mod("gb"), mod("gc")
    W = gc.world(tag)
    before = _snapshot()
    with gb.world(tag) as info:
        assert gb.ACTIVE == tag
        assert importlib.import_module("hwsc_bind").ACTIVE is True
        assert info["tag"] == tag and info["key"] == W.key
        hb, hc = importlib.import_module("hwsb_config"), importlib.import_module("hwsc_config")
        k4d = importlib.import_module("k4b_data")
        k4r = importlib.import_module("k4b_driver")
        assert hb.KEY == W.key and hc.KEY == W.key
        assert hb.SCOPE == "hwsg-v1" and hc.SCOPE == "hwsg-v1"
        assert hc.SIGMA == Fraction(W.sigma) and hb.SIGMA == Fraction(W.sigma)
        assert hc.NEIGHBOUR == (1 - Fraction(W.p)) / 4 and hb.NEIGHBOUR == hc.NEIGHBOUR
        assert hb.TRANS_CFG.p_stay == W.p_float
        assert tuple(hc.MASTERS) == tuple(W.masters) and tuple(hb.MASTERS) == tuple(W.masters)
        assert tuple(hc.P1C_SEEDS) == (W.seeds["val_sd"], W.seeds["val_projection"])
        assert k4d.SCOPE == "hwsg-v1/" + W.key
        assert tuple(k4d.PROCESS) == tuple(W.process)
        assert k4r.SEEDS["endpoint"] == W.seeds["endpoint"]
        assert hc.RESERVATION_ID == W.reservation_id
        assert W.key in str(hc.STORE).replace("\\", "/")
        assert W.key in str(hc.HANDOFF_PATH).replace("\\", "/")
        for d in ADAPTERS:  # the copied-default hazard: the adapters are swapped in
            assert getattr(*_res(d)) is not before[d], d
        for r in gb.rows(tag):  # every plain row holds its new value
            if r["name"] in NON_PLAIN:
                continue
            cur = getattr(importlib.import_module(r["module"]), r["name"])
            assert cur == r["new"] or cur is r["new"], r
    assert gb.ACTIVE is None
    assert importlib.import_module("hwsc_bind").ACTIVE is False
    for d, old in before.items():
        assert getattr(*_res(d)) is old, d


@pytest.mark.parametrize("tag", TAGS)
def test_restored_after_exception_including_adapters(tag):
    gb = mod("gb")
    before = _snapshot()
    with pytest.raises(RuntimeError):
        with gb.world(tag):
            raise RuntimeError("boom")
    assert gb.ACTIVE is None
    for d, old in before.items():
        assert getattr(*_res(d)) is old, d
    for d in ADAPTERS:
        assert getattr(*_res(d)) is before[d]


def test_nested_world_refused_and_state_intact():
    gb, gc = mod("gb"), mod("gc")
    before = _snapshot()
    with gb.world("lo"):
        expect_fail("FAIL_TECHNICAL/BINDING", gb.world("hi").__enter__)
        assert gb.ACTIVE == "lo"
        assert importlib.import_module("hwsb_config").KEY == gc.world("lo").key
    for d, old in before.items():
        assert getattr(*_res(d)) is old, d


def test_refused_inside_active_bound_stage_c():
    gb = mod("gb")
    hb = importlib.import_module("hwsc_bind")
    with hb.bound_stage_c():
        expect_fail("FAIL_TECHNICAL/BINDING", gb.world("mid").__enter__)
        assert gb.ACTIVE is None


def test_drifted_row_refused_and_nothing_set(monkeypatch):
    gb = mod("gb")
    hc = importlib.import_module("hwsc_config")
    key_before = importlib.import_module("hwsb_config").KEY
    monkeypatch.setattr(hc, "SIGMA", Fraction(99, 7))  # not the import-time object
    expect_fail("FAIL_TECHNICAL/BINDING", gb.world("lo").__enter__)
    assert importlib.import_module("hwsb_config").KEY == key_before
    assert gb.ACTIVE is None


def test_constants_differ_between_worlds():
    gb = mod("gb")
    per = {}
    for tag in TAGS:
        with gb.world(tag):
            hc = importlib.import_module("hwsc_config")
            per[tag] = {n: getattr(hc, n) for n in ("KEY", "SIGMA", "NEIGHBOUR", "MASTERS",
                                                    "SEEDS", "P1C_SEEDS", "RESERVATION_ID",
                                                    "PROCESS")}
            per[tag]["HANDOFF"] = str(hc.HANDOFF_PATH)
            per[tag]["STORE"] = str(hc.STORE)
            per[tag]["p_stay"] = importlib.import_module("hwsb_config").TRANS_CFG.p_stay
    for name in per["lo"]:
        assert len({repr(per[t][name]) for t in TAGS}) == 3, name


def test_kg1_wstar_import_time_values_are_stage_c():
    gb = mod("gb")
    rows = {f"{r['module']}.{r['name']}": r["old"] for r in gb.rows("lo")}
    assert rows["hwsc_config.SIGMA"] == Fraction(7, 4)
    assert rows["hwsc_config.NEIGHBOUR"] == Fraction(1, 5)
    assert rows["hwsb_config.TRANS_CFG"].p_stay == 0.2
    assert tuple(rows["hwsc_config.MASTERS"]) == tuple(importlib.import_module("hwsc_config").MASTERS)


def _planted_module(tmp_path, name, body):
    (tmp_path / f"{name}.py").write_text(textwrap.dedent(body), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(tmp_path))


def test_audit_catches_planted_w_star_constants(tmp_path):
    gb = mod("gb")
    m = _planted_module(tmp_path, "b_planted_hit", """
        from dataclasses import dataclass
        SIGMA_COPY = 1.75
        def f(p_stay=0.2):
            return p_stay
        @dataclass
        class Cfg:
            master: int = 620301
            other: int = 620302
            third: int = 620303
    """)
    with gb.world("hi"):
        # API-AMBIGUITY: the modules argument is taken as module objects
        r = gb.audit("hi", modules=[m], left_unchanged=[])
    assert r["n_hits"] >= 3 and r["status"] != "PASS"
    assert r["unlisted"]


def test_audit_mid_own_value_is_not_a_hit(tmp_path):  # OPEN-5
    gb = mod("gb")
    m = _planted_module(tmp_path, "b_planted_mid", """
        P_STAY = 0.2
        def g(p_stay=0.2):
            return p_stay
    """)
    with gb.world("mid"):
        r = gb.audit("mid", modules=[m], left_unchanged=[])
    assert r["status"] == "PASS", r


def test_check_explicit_stale_default_trap():
    gb = mod("gb")
    # API-AMBIGUITY: fn_name is the dotted name string
    expect_fail("FAIL_TECHNICAL/BINDING", gb.check_explicit, "hwsb_gates.ladder_pilot", {})
    expect_fail("FAIL_TECHNICAL/BINDING", gb.check_explicit, "hwsb_gates.ladder_pilot",
                {"models": (1, 2, 3)})
    assert gb.check_explicit("hwsb_gates.ladder_pilot",
                             {"models": (1, 2, 3), "seeds": (4, 5), "ladder": (3072,)}) is None
