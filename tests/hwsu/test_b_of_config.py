"""Author B (job 0198): hwsu_config: constants, the CONTRACT loader (D-2), the blindness guard
(protocol §8.1, J9, D-3) and the HANDOFF mirror (D-4). TEST_PLAN §3 row test_b_of_config; DRO1 loader.
Expected values come from CONTRACT_OF.json and the protocol, never from the code under test."""

from __future__ import annotations

import builtins
import copy
import hashlib
import io
import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _norm(p) -> str:
    return os.path.normcase(os.path.abspath(str(p)))


def _hook(monkeypatch) -> list:
    """Access hook (TEST_PLAN §1): record every path opened through the usual entry points."""
    seen, real_open = [], builtins.open

    def rec(file, *a, **k):
        seen.append(_norm(file)) if isinstance(file, (str, Path)) else None
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", rec)
    monkeypatch.setattr(io, "open", rec)
    for name in ("open", "read_bytes", "read_text"):
        real = getattr(Path, name)

        def wrap(self, *a, _real=real, **k):
            seen.append(_norm(self))
            return _real(self, *a, **k)

        monkeypatch.setattr(Path, name, wrap)
    return seen


def _fails(status, fn, *a, **k):
    with pytest.raises(C1GateFailure) as ei:
        fn(*a, **k)
    assert ei.value.status == status, ei.value.status
    return ei.value


# ------------------------------------------------------------------ constants (API §1.1)
def test_constants_equal_contract():
    w, t, s = C["world"], C["thresholds"], C["sizes"]
    assert uc.KEY == w["key"] == "W12-q1-s1.75-p0.2"
    assert tuple(uc.PROC) == tuple(w["process_code_args"]) == ("cylinder", "overlap", "1.75")
    assert (uc.SCOPE_OF, uc.SCOPE_U, uc.SCOPE_DRY) == (C["scopes"]["of"], C["scopes"]["model"],
                                                       C["scopes"]["dry"])
    assert list(C["namespace"]["U"]["scopes"]) == [uc.SCOPE_OF, uc.SCOPE_U, uc.SCOPE_DRY]
    assert tuple(uc.MASTERS) == tuple(w["masters"]) == (620301, 620302, 620303)
    assert dict(uc.SEEDS_OF) == C["seeds"]["of"]
    assert dict(uc.DRY_SEEDS_OF) == C["seeds"]["dry_of"]
    assert (uc.BLOCK_OF, tuple(uc.BLOCKS_OF)) == (s["block"], tuple(s["blocks"]))
    assert (uc.N_FIT, uc.N_EVAL) == (s["of_fit_singles"], s["of_eval_pairs"])
    assert uc.DRAWS == t["draws"] and tuple(uc.LADDER) == tuple(t["ladder"])
    assert Fraction(uc.POWER).limit_denominator(100) == Fraction(t["power"])
    assert uc.ALPHA_HEADROOM == Fraction(t["alpha_headroom"]) == Fraction(1, 20)
    assert uc.ALPHA_VAL == Fraction(t["alpha_val"]) and uc.ALPHA_FAMILY == Fraction(t["alpha_family"])
    assert uc.HEADROOM == Fraction(t["headroom"]) and uc.SHARE_CEIL == Fraction(t["share_ceiling"])
    assert (uc.RESP_LO, uc.RESP_HI) == tuple(Fraction(x) for x in t["response_lines"])
    assert (uc.SHARE_LO, uc.SHARE_HI) == tuple(Fraction(x) for x in t["share_lines"])
    assert uc.LAMBDA_KO3 == Fraction(t["lambda_ko3"])
    assert uc.ALT_RESP == Fraction(t["alternatives"]["response"])
    assert uc.ALT_SHARE == Fraction(t["alternatives"]["share"])
    assert uc.KO_TOL == t["ko_tol"] and uc.M4_TOL == t["m4_tol"]
    assert uc.DEC_TOL == Fraction(t["decimal_rel_tol"]) and uc.LEMMA_P_SE == t["lemma_p_se"]
    assert (uc.K_HARM, uc.V, uc.N_NUIS, uc.DESIGN_RANK) == (t["harmonics"], w["V"], t["n_nuis"],
                                                            t["design_rank"])
    assert uc.DECIMAL_ROWS == s["decimal_rows"]


def test_paths_equal_contract():
    r = C["resources"]
    assert Path(uc.ROOT) == Path(r["project_root"]) and Path(uc.STORE) == Path(r["store"])
    assert Path(uc.SCRATCH) == Path(r["scratch_root"])
    assert Path(uc.DRY_STORE) == Path(r["scratch_root"]) / "hwsu-dry-of"
    assert Path(uc.MAILBOX) == Path(r["mailbox"])
    assert Path(uc.STUDY_LEDGER) == Path(C["records"]["study_ledger"]["path"])
    assert Path(uc.HWSC_STORE) == Path(C["stage_c"]["store"])
    assert Path(uc.HANDOFF_PATH) == Path(r["project_root"]) / C["handoff"]["path"]
    here = REPO / "tools" / "hwsu"
    assert Path(uc.CONTRACT_OF_PATH).resolve() == (here / "CONTRACT_OF.json").resolve()
    assert Path(uc.CONTRACT_PATH).resolve() == (here / "CONTRACT.json").resolve()
    assert Path(uc.PROTOCOL_PATH).resolve() == (here / "PROTOCOL_HWSU_v1.md").resolve()


def test_import_contract_is_phase1_file():
    raw = (REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_bytes()
    p2 = REPO / "tools" / "hwsu" / "CONTRACT.json"
    if not p2.exists():  # phase 1: OF runs with CONTRACT.json absent
        assert uc.CONTRACT == json.loads(raw)
        assert uc.CONTRACT_SHA256 == {"of": _sha(raw), "phase2": None}
    else:  # phase 2 adds keys only (D-2); every phase-1 value is unchanged
        assert uc.CONTRACT_SHA256 == {"of": _sha(raw), "phase2": _sha(p2.read_bytes())}
        assert all(uc.CONTRACT[k] == v for k, v in json.loads(raw).items()
                   if not isinstance(v, dict))
    assert _sha((REPO / "tools" / "hwsu" / "PROTOCOL_HWSU_v1.md").read_bytes()) == C["protocol_sha256"]


# ------------------------------------------------------------------ loader (API §1.2, D-2)
OF = {"a": 1, "b": {"c": 2, "l": [1, 2]}, "s": "x"}


def _files(tmp_path, p2=None, of=OF, raw_p2=None):
    of_path = tmp_path / "CONTRACT_OF.json"
    of_path.write_bytes(json.dumps(of).encode("utf-8"))
    p2_path = tmp_path / "CONTRACT.json"
    if raw_p2 is not None:
        p2_path.write_bytes(raw_p2)
    elif p2 is not None:
        p2_path.write_bytes(json.dumps(p2).encode("utf-8"))
    return of_path, p2_path, _sha(of_path.read_bytes())


def test_loader_absent_phase2_returns_deep_copy(tmp_path):
    of_path, p2_path, _ = _files(tmp_path)
    got = uc.load_contract(of_path, p2_path)
    assert got == OF
    got["b"]["l"].append(9)
    assert uc.load_contract(of_path, p2_path) == OF
    assert uc.load_contract(of_path, None) == OF


def test_loader_union_adds_top_level_and_nested_keys(tmp_path):
    of_path, p2_path, sha = _files(tmp_path)
    p2 = {"contract_of_sha256": sha, "d": {"e": 3}, "b": {"n": [7]}}
    p2_path.write_bytes(json.dumps(p2).encode("utf-8"))
    got = uc.load_contract(of_path, p2_path)
    assert got == {"a": 1, "b": {"c": 2, "l": [1, 2], "n": [7]}, "s": "x", "d": {"e": 3},
                   "contract_of_sha256": sha}


def test_loader_real_contract_with_nested_resource_key(tmp_path):
    raw = (REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_bytes()
    p2_path = tmp_path / "CONTRACT.json"
    p2 = {"contract_of_sha256": _sha(raw), "contract_phase2": {"job": "x"},
          "resources": {"memory_cap_bytes": {"E1": 12 * 1024**3}}, "name_rule": {"phase2": {
              "prefixes": ["ACTS_"]}}}
    p2_path.write_bytes(json.dumps(p2).encode("utf-8"))
    got = uc.load_contract(uc.CONTRACT_OF_PATH, p2_path)
    assert got["resources"]["memory_cap_bytes"] == dict(C["resources"]["memory_cap_bytes"],
                                                        E1=12 * 1024**3)
    assert got["name_rule"]["phase1"] == C["name_rule"]["phase1"]
    assert got["contract_phase2"] == {"job": "x"} and got["phase1_files"] == C["phase1_files"]


@pytest.mark.parametrize("p2", [{"d": 1}, {"contract_of_sha256": "0" * 64, "d": 1},
                                {"contract_of_sha256": None, "d": 1}])
def test_loader_refuses_unbound_phase2(tmp_path, p2):
    of_path, p2_path, _ = _files(tmp_path, p2=p2)
    _fails("FAIL_TECHNICAL/BINDING", uc.load_contract, of_path, p2_path)


@pytest.mark.parametrize("extra", [{"a": 2}, {"a": 1}, {"b": {"c": 2}}, {"b": {"l": [3]}},
                                   {"b": {"l": [1, 2]}}, {"b": 5}, {"s": {"t": 1}}])
def test_loader_refuses_any_override_even_equal(tmp_path, extra):
    of_path, p2_path, sha = _files(tmp_path)
    p2_path.write_bytes(json.dumps(dict(extra, contract_of_sha256=sha)).encode("utf-8"))
    _fails("FAIL_TECHNICAL/BINDING", uc.load_contract, of_path, p2_path)


def test_loader_override_reason_names_dotted_key(tmp_path):
    of_path, p2_path, sha = _files(tmp_path, p2=None)
    p2_path.write_bytes(json.dumps({"contract_of_sha256": sha, "b": {"c": 9}}).encode("utf-8"))
    exc = _fails("FAIL_TECHNICAL/BINDING", uc.load_contract, of_path, p2_path)
    assert "b.c" in str(exc.reason)


def test_loader_refuses_unreadable_of(tmp_path):
    _fails("FAIL_TECHNICAL/BINDING", uc.load_contract, tmp_path / "absent.json", None)
    bad = tmp_path / "bad.json"
    bad.write_bytes(b"{not json")
    _fails("FAIL_TECHNICAL/BINDING", uc.load_contract, bad, None)


def test_merge_is_pure_and_lists_are_leaves():
    a, b = copy.deepcopy(OF), {"b": {"m": [3]}, "z": [1]}
    a0, b0 = copy.deepcopy(a), copy.deepcopy(b)
    got = uc.merge(a, b)
    assert got == {"a": 1, "b": {"c": 2, "l": [1, 2], "m": [3]}, "s": "x", "z": [1]}
    assert (a, b) == (a0, b0)
    got["b"]["m"].append(4)
    assert b == b0
    with pytest.raises(C1GateFailure) as ei:
        uc.merge({"x": {"y": [1]}}, {"x": {"y": [2]}})
    assert ei.value.status == "FAIL_TECHNICAL/BINDING"


# ------------------------------------------------------------------ blindness (API §1.3)
BLIND = ["hwsb-store/REPORT.json", "hwsb-store/stages/EVAL/x.json", "hwsc-store/stages/S8",
         "hwsc-store/stages/S8/RESULT.json", "hwsc-store/stages/S5/VALIDATION_REPORT.json",
         "hwsc-store/stages/s5/x/y.json", "hwsc-store/stages/E1/L1.json",
         "hwsc-store/SEALED_VALIDATION.json", "hwsc-store/SEALED_OPENED.json",
         "agent-handoff/planning/coord-hws-dyn-x.md",
         "agent-handoff/planning/requests/coord-hws-dyn-20261101.md",
         "agent-handoff/planning/HWSD-x.md", "agent-handoff/records/HWSD_x.json",
         "agent-handoff/jobs/hwsd-0001/task.md",
         "hwsd-store/x.json", "hwsd-store/stages/y.json", "hwsd-store/stages/REGISTRY_OBLIGATION.json",
         "hwsd-store/reservations/sub/x.json", "hwsd-store/artifacts/Checkpoint/a/meta.json"]
OPEN = ["hwsd-store", "hwsd-store/REGISTRY_OBLIGATION.json",
        "hwsd-store/REGISTRY_OBLIGATION_X-a1.json", "hwsd-store/RESERVATION_X.json",
        "hwsd-store/reservations", "hwsd-store/reservations/x.END.json",
        "hwsd-store/reservations/RES-HWSD-X.json",
        "hwsc-store/stages/E1/other.json", "hwsc-store/RESERVATION_W2.json",
        "hwsc-store/artifacts/EmissionSpec/a/meta.json",
        "agent-handoff/records/HWS_UD_NAMESPACE.json", "agent-handoff/records/HWSC_W2_END.json",
        "agent-handoff/planning/responses/coord-hws-ud-20261101.joint-rulings.md",
        "agent-handoff/planning/responses/HWSU-DESIGN-v1.md", "hwsu-store/FREEZE_OF.json",
        "topo-pilot/tools/hwsu/CONTRACT_OF.json"]


@pytest.mark.parametrize("rel", BLIND)
def test_blinded_true(tmp_path, rel, monkeypatch):
    seen = _hook(monkeypatch)
    root = tmp_path / "root"
    assert uc.blinded(root / rel, root) is True
    assert uc.blinded(str(root / rel).upper(), str(root)) is True  # case-insensitive
    assert seen == []  # pure: no file access


@pytest.mark.parametrize("rel", OPEN)
def test_blinded_false(tmp_path, rel):
    root = tmp_path / "root"
    assert uc.blinded(root / rel, root) is False


def test_blinded_is_relative_to_root(tmp_path):
    root, other = tmp_path / "root", tmp_path / "other"
    assert uc.blinded(other / "hwsd-store" / "x.json", root) is False
    assert uc.blinded(other / "hwsc-store" / "stages" / "S8" / "x", root) is False


def test_guard_raises_before_any_open(tmp_path, monkeypatch):
    root = tmp_path / "root"
    target = root / "hwsc-store" / "stages" / "S8" / "RESULT.json"
    target.parent.mkdir(parents=True)
    target.write_text('{"outcome": "fixture"}', encoding="utf-8")
    dyn = root / "agent-handoff" / "planning" / "coord-hws-dyn-x.md"
    dyn.parent.mkdir(parents=True)
    dyn.write_text("fixture", encoding="utf-8")
    seen = _hook(monkeypatch)
    for fn in (uc.read_json, uc.read_bytes, uc.sha256_file, uc.guard):
        for p in (target, dyn):
            _fails("FAIL_TECHNICAL/BLINDNESS", fn, p, root)
    _fails("FAIL_TECHNICAL/BLINDNESS", uc.guard, root / "docs" / "research_summary" / "x.tex", root)
    _fails("FAIL_TECHNICAL/BLINDNESS", uc.guard, root / "00_READ_ME_FIRST_x" / "a.pdf", root)
    assert _norm(target) not in seen and _norm(dyn) not in seen


def test_read_helpers_on_open_paths(tmp_path):
    root = tmp_path / "root"
    p = root / "hwsd-store" / "REGISTRY_OBLIGATION.json"
    p.parent.mkdir(parents=True)
    p.write_bytes(b'\xef\xbb\xbf{"a": [1, 2]}')
    assert uc.read_json(p, root) == {"a": [1, 2]}  # a UTF-8 BOM is accepted
    assert uc.read_bytes(p, root) == p.read_bytes()
    assert uc.sha256_file(p, root) == _sha(p.read_bytes())
    assert Path(uc.guard(p, root)) == p
    assert uc.public_summary(root / "docs" / "research_summary" / "a.tex") is True
    assert uc.public_summary(root / "docs" / "other" / "a.tex") is False


# ------------------------------------------------------------------ HANDOFF mirror (D-4)
def _handoff(tmp_path, **over):
    d = {"p_D2a": 1.25e-15, "stage_c_exclusions": ["a1", 7], "freeze_sha256": "f", "models": [1]}
    d.update(over)
    p = tmp_path / "HANDOFF.json"
    p.write_bytes(json.dumps(d).encode("utf-8"))
    return p, _sha(p.read_bytes())


def test_load_handoff_u_two_keys_only(tmp_path):
    p, sha = _handoff(tmp_path)
    got = uc.load_handoff_u(p, expected_sha256=sha)
    assert got == {"p_D2a": 1.25e-15, "stage_c_exclusions": ("a1", "7")}
    assert isinstance(got["stage_c_exclusions"], tuple) and isinstance(got["p_D2a"], float)


def test_load_handoff_u_refusals(tmp_path):
    p, sha = _handoff(tmp_path)
    _fails("FAIL_TECHNICAL/IDENTITY", uc.load_handoff_u, p, expected_sha256="0" * 64)
    _fails("FAIL_TECHNICAL/IDENTITY", uc.load_handoff_u, p)  # default: CONTRACT handoff.sha256
    d = {"p_D2a": 1.0e-15}
    q = tmp_path / "H2.json"
    q.write_bytes(json.dumps(d).encode("utf-8"))
    _fails("FAIL_TECHNICAL/IDENTITY", uc.load_handoff_u, q, expected_sha256=_sha(q.read_bytes()))


@pytest.mark.skipif(not Path(C["resources"]["project_root"], C["handoff"]["path"]).is_file(),
                    reason="real HANDOFF.json absent")
def test_load_handoff_u_real_record():
    got = uc.load_handoff_u()
    assert got["p_D2a"] == C["handoff"]["p_D2a_copy_for_tests"]
    assert len(got["stage_c_exclusions"]) == 24 and set(got) == {"p_D2a", "stage_c_exclusions"}
