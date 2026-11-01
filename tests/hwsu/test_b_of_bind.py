"""Author B (job 0198): the call-allowlist and call-time-read audit run by OF-B (protocol §11.2,
RC-10; API §7; D-25), including default arguments, dataclass fields and the explicit-argument
rule for the accepted conditional reads (coordinator phase-1 rulings, "Conditional reads").
Planted modules live under tmp_path only. TEST_PLAN §3 row test_b_of_bind_meter (audit part)."""

from __future__ import annotations

import copy
import json
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_bind as ub  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
BIND = "FAIL_TECHNICAL/BINDING"
HEAD = "from __future__ import annotations  # noqa: I001\n\nimport hwsu_config as uc\n"


def _plant(tmp_path, body, name="hwsu_planted.py") -> Path:
    p = tmp_path / "tools" / "hwsu_plant" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(HEAD + textwrap.dedent(body), encoding="utf-8")
    return p


def _calls(tmp_path, body):
    return ub.audit_calls(files=[_plant(tmp_path, body)])


# ------------------------------------------------------------------ references (API §7)
def test_references_resolve_aliases(tmp_path):
    p = _plant(tmp_path, """
        import c2_code as cc2
        from fractions import Fraction

        def f(x):
            return cc2.problem(x), uc.CONTRACT
        """)
    refs = ub.references(p)
    plain = [(r["module"], r["name"]) for r in refs if not r.get("from")]
    assert ("c2_code", "problem") in plain and ("hwsu_config", "CONTRACT") in plain
    line = [r["line"] for r in refs if (r["module"], r["name"]) == ("c2_code", "problem")]
    assert line == [p.read_text(encoding="utf-8").splitlines().index(
        "    return cc2.problem(x), uc.CONTRACT") + 1]
    assert any(r.get("from") and (r["module"], r["name"]) == ("fractions", "Fraction") for r in refs)


# ------------------------------------------------------------------ audit_calls (API §7)
def test_allowlisted_and_external_pass(tmp_path):
    r = _calls(tmp_path, """
        import c2_code
        import k4b_data as kd
        import numpy as np
        import stage_records
        from c1_records import C1GateFailure
        from topo_pilot.contracts import SeedTree
        from topo_pilot.dataset.checks import make_sequence_ids

        def f(x):
            np.linalg.norm(x)
            kd.predicate_check(x, ("sealed_d2a",))
            stage_records.write_new("p", {})
            return c2_code.problem, SeedTree, make_sequence_ids, C1GateFailure, uc.SEEDS_OF
        """)
    assert r["status"] == "PASS" and r["unlisted"] == [] and r["never_called"] == []
    assert r["n_refs"] >= 6


@pytest.mark.parametrize("ref", ["c2_code.fwl", "k4b_data.sealed_d2a_predicate", "hwsc_data.load_world",
                                 "c2_stage_s1.run", "hwsb_config.MASTERS", "k4b_config.chart_cfg"])
def test_unlisted_reference_fails(tmp_path, ref):
    mod, name = ref.split(".")
    r = _calls(tmp_path, f"import {mod}\n\n\ndef f():\n    return {mod}.{name}\n")
    assert r["status"] == BIND
    assert name in json.dumps(r["unlisted"]) + json.dumps(r["never_called"])


@pytest.mark.parametrize("ref", ["c2_model.load_models", "c2_oracle.load_process", "c2_oracle.h3",
                                 "c2_oracle.decimal_rows", "c2_stats.p1", "c2_stats._summaries",
                                 "k4b_driver.anything", "k4b_driver.begin_stage", "c2_model.m0",
                                 "hwsc_data.registry_risk", "c2_code.haar_frames",
                                 "c2_attrib.desc_intervals", "hwsc_config.load_handoff"])
def test_never_called_fails(tmp_path, ref):
    mod, name = ref.split(".")
    r = _calls(tmp_path, f"import {mod} as m\n\n\ndef f():\n    return m.{name}()\n")
    assert r["status"] == BIND
    assert name in json.dumps(r["never_called"])


def test_never_called_wins_over_allowlist(tmp_path, monkeypatch):
    c = copy.deepcopy(uc.CONTRACT)
    c["binding"]["allowlist"].setdefault("c2_code", {})["haar_frames"] = {
        "kind": "function", "call_time_reads": {}, "calls_tools_functions": []}
    p = _plant(tmp_path, "import c2_code\n\n\ndef f():\n    return c2_code.haar_frames\n")
    r = ub.audit_calls(files=[p], contract=c)
    assert r["status"] == BIND and "haar_frames" in json.dumps(r["never_called"])


@pytest.mark.parametrize("line", ["from c2_code import problem", "from hwsc_data import process_identity",
                                  "from hwsu_config import CONTRACT", "from c1_records import run_c1_gate"])
def test_unlisted_from_import_fails(tmp_path, line):
    r = _calls(tmp_path, line + "\n")
    assert r["status"] == BIND


@pytest.mark.parametrize("line", ["from topo_pilot.contracts import SeedTree, ArtifactStore",
                                  "from oracle_profile import ProfileError",
                                  "from pathlib import Path", "from json import dumps"])
def test_listed_from_import_passes(tmp_path, line):
    assert _calls(tmp_path, line + "\n")["status"] == "PASS"


def test_contract_binding_lists():
    b = C["binding"]
    assert "hwsc_config.load_handoff" in b["never_called"] and "k4b_driver.*" in b["never_called"]
    for f, r in (("hwsb_known.classify_hits", 'hwsb_config.CONTRACT["seeds"]'),
                 ("hwsb_data.build_process", "hwsb_config.MASTERS"),
                 ("hwsb_dry.build_tiny_process", "hwsb_config.DRY_MASTERS")):
        assert {"function": f, "read": r} == {k: v for k, v in
                                              next(x for x in b["conditional_reads"] if x["function"] == f).items()
                                              if k in ("function", "read")}
        mod, name = f.split(".")
        assert r in b["allowlist"][mod][name]["call_time_reads"]


# ------------------------------------------------------------------ explicit-argument rule
EXPLICIT_FAIL = ["hwsb_known.classify_hits(hits)",
                 "hwsb_known.classify_hits(hits, frags)",
                 "hwsb_known.classify_hits(hits, fragments=frags)",
                 "hwsb_known.classify_hits(hits, job_scratch=js, label='x')",
                 "hwsb_data.build_process(store)",
                 "hwsb_data.build_process(store, emission_cfg=None)",
                 "hwsb_dry.build_tiny_process(store)"]
EXPLICIT_PASS = ["hwsb_known.classify_hits(hits, frags, js, label='x')",
                 "hwsb_known.classify_hits(hits, fragments=frags, job_scratch=js, label='x')",
                 "hwsb_known.classify_hits(hits, frags, job_scratch=js)",
                 "hwsb_data.build_process(store, masters=(620301,))",
                 "hwsb_data.build_process(store, (620301, 620302))",
                 "hwsb_dry.build_tiny_process(store, masters=(649906,))"]


def _explicit_file(tmp_path, call):
    return _plant(tmp_path, f"""
        import hwsb_data
        import hwsb_dry
        import hwsb_known


        def f(hits, frags, js, store):
            return {call}
        """)


@pytest.mark.parametrize("call", EXPLICIT_FAIL)
def test_argument_less_conditional_call_fails(tmp_path, call):
    # SPEC-QUESTION: API §7 does not name the sub-check that enforces the ruling's explicit-
    # argument rule; the test reads only the overall audit status (OF-B runs ub.audit).
    assert ub.audit(files=[_explicit_file(tmp_path, call)])["status"] == BIND


@pytest.mark.parametrize("call", EXPLICIT_PASS)
def test_explicit_conditional_call_passes(tmp_path, call):
    assert ub.audit(files=[_explicit_file(tmp_path, call)])["status"] == "PASS"


# ------------------------------------------------------------------ function_reads (API §7; D-25)
CFG = "TOL = 0.5\nSEED = 1\n\n\ndef helper(x):\n    return x\n"
MOD = """
import b0198_plant_cfg as pc
from dataclasses import dataclass

LIMIT = 5
SCALE = 2.0
CONTRACT = {"world": {"k": 1}, "models": {"m": 2}}


@dataclass
class Box:
    n: int = LIMIT


def reads_const(x):
    return x * SCALE


def reads_world():
    return CONTRACT["world"]


def reads_models():
    return CONTRACT["models"]


def reads_default(x, k=pc.TOL):
    return x + k


def reads_alias():
    return pc.SEED + pc.helper(1)


def makes_box():
    return Box()


def calls_local(x):
    return reads_const(x)
"""


@pytest.fixture
def planted_reads(tmp_path, monkeypatch):
    d = tmp_path / "tools" / "b0198_plant"
    d.mkdir(parents=True)
    (d / "b0198_plant_cfg.py").write_text(CFG, encoding="utf-8")
    (d / "b0198_plant_mod.py").write_text(MOD, encoding="utf-8")
    monkeypatch.syspath_prepend(str(d))
    for m in ("b0198_plant_cfg", "b0198_plant_mod"):
        sys.modules.pop(m, None)
    import b0198_plant_mod
    yield b0198_plant_mod
    for m in ("b0198_plant_cfg", "b0198_plant_mod"):
        sys.modules.pop(m, None)


def _reads(mod, qualname) -> set:
    try:  # API-AMBIGUITY: `module` read as the module name; the module object is also accepted
        r = ub.function_reads(mod.__name__, qualname)
    except (TypeError, AttributeError):
        r = ub.function_reads(mod, qualname)
    return set(r)


@pytest.mark.parametrize("fn,want", [
    ("reads_const", {"b0198_plant_mod.SCALE"}),
    ("reads_world", {'b0198_plant_mod.CONTRACT["world"]'}),
    ("reads_models", {'b0198_plant_mod.CONTRACT["models"]'}),
    ("reads_default", {"b0198_plant_cfg.TOL"}),  # default-argument expressions are included
    ("reads_alias", {"b0198_plant_cfg.SEED"}),  # the callable helper is not a read
])
def test_function_reads_direct(planted_reads, fn, want):
    assert _reads(planted_reads, fn) == want


@pytest.mark.parametrize("fn,want", [("makes_box", {"b0198_plant_mod.LIMIT"}),
                                     ("calls_local", {"b0198_plant_mod.SCALE"})])
def test_function_reads_descend_dataclass_and_callee(planted_reads, fn, want):
    # SPEC-QUESTION: D-25 descends into functions and classes "defined under tools/"; the planted
    # module lies under <tmp>/tools/..., read here as "a tools/ path", not only <REPO>/tools.
    assert _reads(planted_reads, fn) == want


def test_function_reads_real_functions_equal_contract():
    al = C["binding"]["allowlist"]
    for mod, name in (("hwsb_known", "classify_hits"), ("hwsb_data", "build_process"),
                      ("hwsb_dry", "build_tiny_process"), ("hwsc_data", "process_identity")):
        __import__(mod)
        got = _reads(sys.modules[mod], name)
        assert got == set(al[mod][name]["call_time_reads"]), (mod, name)


# ------------------------------------------------------------------ audit_reads / audit
def test_audit_reads_real_contract_pass():
    r = ub.audit_reads()
    assert r["status"] == "PASS" and r["unlisted"] == [] and r["forbidden"] == []


def test_audit_reads_missing_listed_key_fails():
    c = copy.deepcopy(uc.CONTRACT)
    c["binding"]["allowlist"]["hwsb_data"]["build_process"]["call_time_reads"].pop("oracle_profile.PERIOD")
    r = ub.audit_reads(contract=c)
    assert r["status"] == BIND and "PERIOD" in json.dumps(r["unlisted"])


def test_audit_reads_forbidden_without_conditional_entry():
    c = copy.deepcopy(uc.CONTRACT)
    c["binding"]["conditional_reads"] = [x for x in c["binding"]["conditional_reads"]
                                         if x["function"] != "hwsb_known.classify_hits"]
    r = ub.audit_reads(contract=c)
    assert r["status"] == BIND and "seeds" in json.dumps(r["forbidden"])


PHASE1_PY = [REPO / p for p in C["phase1_files"] if p.endswith(".py")]


@pytest.mark.skipif(not all(p.is_file() for p in PHASE1_PY), reason="phase-1 code not complete yet")
def test_audit_real_phase1_files_pass():
    r = ub.audit()
    assert r["status"] == "PASS", r
    assert r["calls"]["status"] == "PASS" and r["reads"]["status"] == "PASS"
