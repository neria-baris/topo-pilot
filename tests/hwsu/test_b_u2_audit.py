"""Author B (job 0223, phase 2): the phase-2 audit u2/hwsu_bind_u2.py (protocol 11.2; API_U2 2.6;
DRU7; R-0223-3, R-0223-5, R-0223-6). Planted modules live under tmp_path only; planted contract
variants are deep copies of the loaded CONTRACT."""

from __future__ import annotations

import copy
import importlib
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001

BIND = "FAIL_TECHNICAL/BINDING"
HEAD = "from __future__ import annotations  # noqa: I001\n\nimport hwsu_config as uc\n"
CONDITIONAL_FUNCS = {"hwsc_gates.expected_meta_c", "hwsc_registry_build._default_sources",
                     "hwsb_train.train", "hwsc_data.make_train_dev_c", "hwsc_registry_build.build"}


def _b2():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_bind_u2")


def _plant(tmp_path, body, name="hwsu_planted.py") -> Path:
    p = tmp_path / "u2plant" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(HEAD + textwrap.dedent(body), encoding="utf-8")
    return p


def _calls(tmp_path, body, name="hwsu_planted.py"):
    return _b2().audit_u2(files=[_plant(tmp_path, body, name)])


# ------------------------------------------------------------------ calls (never_called, unlisted)
@pytest.mark.parametrize("mod,fn", [
    ("c2_model", "load_models"), ("c2_oracle", "load_process"), ("c2_stats", "p1"),
    ("c2_model", "m0"), ("k4b_stats", "write_sealed"), ("nd_decoy", "head_edit"),
    ("k4b_stats", "check_unsealed"), ("k4b_driver", "load_checkpoint")])
def test_never_called_names_fail(tmp_path, mod, fn):
    r = _calls(tmp_path, f"""
        import {mod}

        def f(x):
            return {mod}.{fn}(x)
        """)
    assert r["status"] == BIND and r["calls"]["status"] == BIND
    assert r["calls"]["never_called"] or r["calls"]["unlisted"]


def test_unlisted_name_fails(tmp_path):
    r = _calls(tmp_path, """
        import c2_model

        def f(x):
            return c2_model.some_unlisted_helper(x)
        """)
    assert r["calls"]["status"] == BIND and r["calls"]["unlisted"]


def test_from_import_outside_the_lists_fails(tmp_path):
    r = _calls(tmp_path, """
        from c2_model import load_models

        def f():
            return load_models
        """)
    assert r["calls"]["status"] == BIND


def test_allowlisted_names_pass(tmp_path):
    r = _calls(tmp_path, """
        import c2_model
        import c1_model
        import c1_oracle

        def f(m, x, perm):
            b = c2_model.readout_basis(m)
            return b, c1_model.model_inputs(x), c1_oracle.named_from_canonical(x, perm), uc.CONTRACT
        """)
    assert r["calls"]["status"] == "PASS" and not r["calls"]["unlisted"]
    assert not r["calls"]["never_called"]


def test_c2_seed_default_reference_fails(tmp_path):
    r = _calls(tmp_path, """
        import c2_config

        def f(seed=c2_config.SEEDS):
            return seed
        """)
    assert r["calls"]["status"] == BIND


# ------------------------------------------------------------------ conditional reads (R-0223-3/6)
@pytest.mark.parametrize("body", [
    "import hwsb_train\n\ndef f(s, m):\n    return hwsb_train.train(s, m)\n",
    "import hwsc_data\n\ndef f(s, p, m):\n    return hwsc_data.make_train_dev_c(s, p, m)\n"])
def test_train_and_make_train_dev_c_admitted_only_in_hwsu_dry2(tmp_path, body):
    ok = _b2().audit_u2(files=[_plant(tmp_path / "a", body, "hwsu_dry2.py")])
    assert ok["calls"]["status"] == "PASS", ok["calls"]
    bad = _b2().audit_u2(files=[_plant(tmp_path / "b", body, "hwsu_gates.py")])
    assert bad["status"] == BIND


def test_conditional_reads_name_exactly_the_sanctioned_functions():
    c = uc.CONTRACT["binding"]
    names = {e["function"] for e in c.get("conditional_reads_u2", [])}
    assert names <= CONDITIONAL_FUNCS and names
    # R-0223-6: the reads admitted for build are exactly the three hwsc_config names
    reads = {e["read"] for e in c["conditional_reads_u2"] if e["function"] == "hwsc_registry_build.build"}  # noqa: E501
    assert reads in (set(), {"hwsc_config.PROTOCOL_SHA256", "hwsc_config.ROOT", "hwsc_config.SCRATCH"})  # noqa: E501
    assert set(c["conditional_functions_u2"]) == CONDITIONAL_FUNCS


def test_merged_contract_unions_tables_without_mutating_input():
    b2 = _b2()
    c = copy.deepcopy(uc.CONTRACT)
    before = copy.deepcopy(c)
    m = b2.merged_contract(c)
    assert c == before
    assert "hwsc_gates" in m["binding"]["allowlist"]
    assert "expected_meta_c" in m["binding"]["allowlist"]["hwsc_gates"]
    assert "exclusion_check" in m["binding"]["allowlist"]["hwsc_gates"]  # phase-2 merged per module
    assert "readout_basis" in m["binding"]["allowlist"]["c2_model"]
    for n in uc.CONTRACT["binding"]["never_called_u2"]:
        assert n in m["binding"]["never_called"]


def test_real_phase2_files_pass_the_audit():
    r = _b2().audit_u2()
    assert r["status"] == "PASS", {k: r[k] for k in ("calls", "reads") if k in r}
    assert any("hwsc_registry_build" in str(x) for x in r["by_path"])


# ------------------------------------------------------------------ reads
def _mutate(fn):
    c = copy.deepcopy(uc.CONTRACT)
    fn(c["binding"])
    return c


def test_unlisted_read_of_a_function_fails():
    """A reused function reading a name that is not in its call_time_reads fails the read audit
    (emulated by removing a recorded read: the AST set no longer equals the table)."""
    def f(b):
        del b["allowlist"]["c2_model"]["x1_attainable"]["call_time_reads"]["c2_config.X1_ATTAIN"]
    r = _b2().audit_u2(files=[], contract=_mutate(f))
    assert r["status"] == BIND


def test_extra_read_in_table_fails():
    def f(b):
        b["allowlist"]["c2_model"]["closed_logits"]["call_time_reads"]["c2_config.INDEX"] = "32"
    assert _b2().audit_u2(files=[], contract=_mutate(f))["status"] == BIND


def test_forbidden_read_fails_closed_without_conditional_entry():
    def f(b):
        b["conditional_reads_u2"] = []
        b.setdefault("conditional_reads", [])
    r = _b2().audit_u2(files=[], contract=_mutate(f))
    assert r["status"] == BIND


def test_fifth_forbidden_read_fails_closed():
    """A forbidden name recorded as a read of a function that is not a sanctioned one."""
    def f(b):
        fr = b["forbidden_reads"][0]
        b["allowlist"]["c2_model"]["closed_logits"]["call_time_reads"][f"hwsc_config.{fr}"] = "x"
    assert _b2().audit_u2(files=[], contract=_mutate(f))["status"] == BIND


def test_ast_refs_mismatch_fails():
    def f(b):
        e = b["allowlist_conditional_u2"]["hwsc_registry_build"]["build"]
        e["ast_refs"] = list(e["ast_refs"]) + ["c2_registry.nonexistent"]
    assert _b2().audit_u2(files=[], contract=_mutate(f))["status"] == BIND


def test_missing_module_without_ast_by_path_is_not_swallowed():
    try:
        import psutil  # noqa: F401
        pytest.skip("psutil importable: the by-path fallback is not needed here")
    except ImportError:
        pass

    def f(b):
        b["allowlist_conditional_u2"]["hwsc_registry_build"]["build"].pop("ast_by_path", None)
    r = _b2().audit_u2(files=[], contract=_mutate(f))
    assert r["status"] == BIND


# ------------------------------------------------------------------ file lists
def test_u2_files_lists_package_including_init_and_audit():
    fs = [Path(p) for p in _b2().u2_files()]
    names = [p.name for p in fs]
    assert "__init__.py" in names and "hwsu_bind_u2.py" in names
    assert names == sorted(names) or fs == sorted(fs)
    assert all(p.parent.name == "u2" for p in fs)


def test_phase1_audit_globs_never_see_u2():
    ub = importlib.import_module("hwsu_bind")
    for attr in ("_default_files", "default_files"):
        if hasattr(ub, attr):
            assert not [p for p in getattr(ub, attr)() if "u2" in Path(p).parts]
    assert not [f for f in uc.CONTRACT["phase1_files"] if "/u2/" in f]
    r = ub.audit()
    assert r["status"] == "PASS"


# ------------------------------------------------------------------ reads_by_path (no import)
def test_reads_by_path_does_not_import_and_equals_recorded_refs(tmp_path):
    script = tmp_path / "probe.py"
    script.write_text(textwrap.dedent("""
        import json, sys
        import hwsu_config as uc
        import u2
        import hwsu_bind_u2 as b2
        r = b2.reads_by_path("hwsc_registry_build", "build")
        e = uc.CONTRACT["binding"]["allowlist_conditional_u2"]["hwsc_registry_build"]["build"]
        print(json.dumps({"refs": sorted(r), "want": sorted(e["ast_refs"]),
                          "psutil": "psutil" in sys.modules,
                          "imported": "hwsc_registry_build" in sys.modules,
                          "all_true": all(v is True for v in r.values())}))
        """), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "src") + os.pathsep + str(REPO / "tools" / "hwsu")
    out = subprocess.run([sys.executable, "-s", str(script)], capture_output=True, text=True,
                         env=env, cwd=str(tmp_path))
    assert out.returncode == 0, out.stderr[-800:]
    import json
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["refs"] == d["want"] and d["all_true"]
    assert not d["psutil"] and not d["imported"]
