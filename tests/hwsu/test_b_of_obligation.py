"""Author B (job 0198): the array name rule, the J10/J11 obligation writer and the OF-H hygiene
gate (protocol §8.2 4(b), §4.2 OF-H, RC-5; joint rulings J10, J11 = addendum 4; API §5.6 and
the J11 erratum). TEST_PLAN §3 row test_b_of_obligation; DRO7, DRO9. Synthetic stores only."""

from __future__ import annotations

import builtins
import copy
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
import k4b_data  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
OB = C["obligation"]
LINEAGE = "FAIL_TECHNICAL/LINEAGE"


def _norm(p) -> str:
    return os.path.normcase(os.path.abspath(str(p)))


def _hook(monkeypatch) -> list:
    seen, real_open, real_load = [], builtins.open, np.load

    def rec(file, *a, **k):
        if isinstance(file, (str, Path)):
            seen.append(_norm(file))
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", rec)
    monkeypatch.setattr(io, "open", rec)
    for name in ("open", "read_bytes", "read_text"):
        real = getattr(Path, name)

        def wrap(self, *a, _real=real, **k):
            seen.append(_norm(self))
            return _real(self, *a, **k)

        monkeypatch.setattr(Path, name, wrap)
    monkeypatch.setattr(np, "load", lambda f, *a, **k: (seen.append(_norm(f)), real_load(f, *a, **k))[1])
    return seen


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _hist_arrays(n=4, sym=10):
    canon = np.full((n, 32), sym, dtype=np.uint8)
    canon[:, 0] = np.arange(n) + 5
    t = k4b_data.history_table(canon, np.arange(n, dtype=np.int64) + 100, "of-fit", 0)
    return {k: t[k] for k in ("canon32", "seq_ids", "digest", "landmark", "ref_row", "decoder_panel")}


def _npz(path, **arrays) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **(arrays or {"x": np.arange(3.0)}))
    return path


# ------------------------------------------------------------------ obligation names (J10 item 2)
def test_obligation_names():
    assert ur.obligation_name("OF") == "REGISTRY_OBLIGATION_OF.json" == OB["names"]["OF"]
    assert ur.obligation_name("OF", 1) == "REGISTRY_OBLIGATION_OF-a1.json"
    assert ur.obligation_name("OF", 3) == "REGISTRY_OBLIGATION_OF-a3.json"
    assert ur.obligation_name("E1", 2) == "REGISTRY_OBLIGATION_E1-a2.json"
    assert ur.obligation_name("OF", final=True) == "REGISTRY_OBLIGATION.json"
    assert ur.obligation_name("E2", 1, final=True) == OB["names"]["study_end"]


# ------------------------------------------------------------------ name rule (protocol §8.2 4(b))
HIST = "K4b history table"


@pytest.mark.parametrize("rel,dry,want", [
    ("stages/OF/HIST_OF_fit_b0.npz", False, HIST),
    ("stages/OF/HIST_OF_eval_a2_b1.npz", False, HIST),
    ("stages/OF/ORACLE_OF_eval.npz", False, "NON_HISTORY"),
    ("stages/OF/MOMENTS_x.npz", False, "NON_HISTORY"),
    ("stages/OF/FIT_OF_O.npz", False, "NON_HISTORY"),
    ("stages/OF/BOOT_OF.npz", False, "NON_HISTORY"),
    ("stages/OF/PREC_OF.npz", False, "NON_HISTORY"),
    ("stages/X/PAIR_1.npy", False, "NON_HISTORY"),
    ("stages/X/OTHER_1.npz", False, None),
    ("stages/OF/ACTS_x.npz", False, None),  # a phase-2 prefix, absent from CONTRACT_OF
    ("ORACLE_x.npz", False, None),  # the prefix rule applies under stages/ only
    ("registry/x.npz", False, "NON_HISTORY_REGISTRY"),
    ("artifacts/Checkpoint/abc/payload.npz", False, "NON_HISTORY_ARTIFACT"),
    ("artifacts/Checkpoint/abc/state.pt", False, "NON_HISTORY_ARTIFACT"),
    ("artifacts/EmissionSpec/abc/payload.npz", False, "NON_HISTORY_ARTIFACT"),
    ("artifacts/WorldSpec/abc/payload.npz", False, "NON_HISTORY_ARTIFACT"),
    ("artifacts/ObservationSet/abc/payload.npz", False, None),
    ("artifacts/Checkpoint/abc/other.npz", False, None),
    ("stages/OF/DRYHIST_OF_fit_b0.npz", False, None),
    ("stages/OF/DRYHIST_OF_fit_b0.npz", True, HIST),
    ("stages/OF/HIST_OF_fit_b0.npz", True, None),  # a dry store never holds HIST_* (§8.4)
    ("stages/OF/ORACLE_OF_eval.npz", True, "NON_HISTORY"),
])
def test_name_class(rel, dry, want):
    assert ur.name_class(rel, dry=dry) == want


def test_name_class_non_array_refused():
    for rel in ("stages/OF/OF_REPORT.json", "stages/OF/HIST_OF_fit_b0.txt"):
        with pytest.raises(ValueError):
            ur.name_class(rel)


def test_name_class_reads_contract_prefixes():
    c = copy.deepcopy(uc.CONTRACT)
    c["name_rule"]["phase2"] = {"prefixes": ["ACTS_"]}
    assert ur.name_class("stages/OF/ACTS_x.npz", contract=c) == "NON_HISTORY"
    assert ur.name_class("stages/OF/ACTS_x.npz") is None


def test_save_array_accepts_named_and_history(tmp_path):
    store = tmp_path / "hwsu-store"
    store.mkdir()
    p = Path(ur.save_array(store, "stages/OF/ORACLE_OF_eval.npz", G=np.arange(4.0)))
    assert p == store / "stages" / "OF" / "ORACLE_OF_eval.npz"
    with np.load(p) as z:
        assert sorted(z.files) == ["G"] and np.array_equal(z["G"], np.arange(4.0))
    ur.save_array(store, "stages/OF/HIST_OF_fit_b0.npz", **_hist_arrays())
    with pytest.raises(Exception):  # exclusive create
        ur.save_array(store, "stages/OF/ORACLE_OF_eval.npz", G=np.zeros(1))
    with np.load(p) as z:
        assert np.array_equal(z["G"], np.arange(4.0))


@pytest.mark.parametrize("rel,dry", [("stages/X/OTHER_1.npz", False), ("registry/x.npz", False),
                                     ("artifacts/Checkpoint/a/payload.npz", False),
                                     ("stages/OF/HIST_OF_fit_b0.npz", True),
                                     ("stages/OF/DRYHIST_OF_fit_b0.npz", False)])
def test_save_array_refuses_outside_rule(tmp_path, rel, dry):
    """DRO9 (7): a write outside the frozen name rule is refused before anything is written."""
    store = tmp_path / "hwsu-store"
    store.mkdir()
    with pytest.raises(C1GateFailure) as ei:
        ur.save_array(store, rel, dry=dry, x=np.zeros(2))
    assert ei.value.status == LINEAGE
    assert not (store / rel).exists()
    assert [p for p in store.rglob("*") if p.is_file()] == []


# ------------------------------------------------------------------ writer (J11 form)
def _fixture_store(root):
    store = root / "hwsu-store"
    files = {
        "stages/OF/HIST_OF_fit_b0.npz": _npz(store / "stages/OF/HIST_OF_fit_b0.npz", **_hist_arrays()),
        "stages/OF/ORACLE_OF_eval.npz": _npz(store / "stages/OF/ORACLE_OF_eval.npz"),
        "stages/OF/BOOT_OF.npz": _npz(store / "stages/OF/BOOT_OF.npz", b=np.ones(5)),
        "registry/x.npz": _npz(store / "registry/x.npz", d=np.arange(2)),
        "artifacts/Checkpoint/ck1/payload.npz": _npz(store / "artifacts/Checkpoint/ck1/payload.npz"),
        "artifacts/EmissionSpec/em1/payload.npz": _npz(store / "artifacts/EmissionSpec/em1/payload.npz",
                                                       e=np.eye(2)),
    }
    for t, d in (("Checkpoint", "ck1"), ("EmissionSpec", "em1")):
        (store / "artifacts" / t / d / "meta.json").write_text(
            json.dumps({"artifact_type": t}), encoding="utf-8")
    (store / "GATES.jsonl").write_text("{}\n", encoding="utf-8")
    return store, files


def _expected_entry(rel, path):
    ck = rel.startswith("artifacts/Checkpoint/")
    if "/HIST_" in rel:
        cls, reader, basis = HIST, "k4b_history_table", None
    else:
        cls, reader = "NON_HISTORY", None
        basis = "artifact" if rel.startswith("artifacts/") else (
            "registry" if rel.startswith("registry/") else "name_rule")
    return {"relpath": rel, "sha256": None if ck else _sha(path), "bytes": path.stat().st_size,
            "class": cls, "reader": reader, "basis": basis}


def test_write_obligation_exact_j11_form(tmp_path, monkeypatch):
    store, files = _fixture_store(tmp_path / "root")
    seen = _hook(monkeypatch)
    p = Path(ur.write_obligation(store, "REGISTRY_OBLIGATION_OF.json", "OF", "fixture writer",
                                 attempt=1, reservation_id="RES-HWSU-OF", dry_stores=()))
    monkeypatch.undo()
    assert p == store / "REGISTRY_OBLIGATION_OF.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    assert list(rec) == OB["top_level"] or set(rec) == set(OB["top_level"])
    assert rec["schema"] == "hws-registry-obligation-v1" and rec["track"] == "U"
    assert rec["rule"] == "fail closed" and rec["job"] == "OF" and rec["attempt"] == 1
    assert rec["reservation_id"] == "RES-HWSU-OF" and rec["written_by"] == "fixture writer"
    assert rec["dry_stores"] == [] and rec["name_rules"] == OB["name_rules"]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z", rec["written_utc"])
    assert "\\" not in rec["store"] and Path(rec["store"]).is_absolute()
    assert Path(rec["store"]).resolve() == store.resolve()
    want = [_expected_entry(r, files[r]) for r in sorted(files)]
    assert rec["files"] == want
    for e in rec["files"]:
        assert list(e) == OB["file_keys"] or set(e) == set(OB["file_keys"])
        assert e["sha256"] is None or re.fullmatch(r"[0-9a-f]{64}", e["sha256"])
    ck = _norm(files["artifacts/Checkpoint/ck1/payload.npz"])
    assert ck not in seen  # classed by meta.json, never opened or hashed (J10 1 i, J11)


def test_write_obligation_rules_match_their_files(tmp_path):
    store, files = _fixture_store(tmp_path / "root")
    rec = json.loads(Path(ur.write_obligation(store, "REGISTRY_OBLIGATION_OF.json", "OF", "w",
                                              attempt=1)).read_text(encoding="utf-8"))
    for e in rec["files"]:
        hit = [r["kind"] for r in rec["name_rules"] if re.fullmatch(r["regex"], e["relpath"])]
        assert bool(hit) == (e["basis"] == "name_rule")
    assert {r["kind"] for r in rec["name_rules"]} <= set(OB["name_rule_kinds"])


def test_write_obligation_refuses_unclassifiable(tmp_path):
    store, files = _fixture_store(tmp_path / "root")
    _npz(store / "stages" / "X" / "OTHER_1.npz")
    with pytest.raises(C1GateFailure) as ei:
        ur.write_obligation(store, "REGISTRY_OBLIGATION_OF.json", "OF", "w", attempt=1)
    assert ei.value.status == LINEAGE
    assert not (store / "REGISTRY_OBLIGATION_OF.json").exists()


def test_write_obligation_no_history_and_exclusive(tmp_path):
    store = tmp_path / "root" / "hwsu-store"
    store.mkdir(parents=True)
    (store / "RESERVATION_OF.json").write_text("{}", encoding="utf-8")
    name = ur.obligation_name("OF", 1)
    p = Path(ur.write_obligation(store, name, "OF", "w", attempt=1, reservation_id="RES-HWSU-OF"))
    rec = json.loads(p.read_text(encoding="utf-8"))
    assert rec["files"] == [] and rec["reservation_id"] == "RES-HWSU-OF"
    before = p.read_bytes()
    with pytest.raises(Exception):
        ur.write_obligation(store, name, "OF", "w", attempt=1)
    assert p.read_bytes() == before


def test_write_obligation_dry_store(tmp_path):
    store = tmp_path / "hwsu-dry-of-x"
    _npz(store / "stages/OF/DRYHIST_OF_fit_b0.npz", **_hist_arrays())
    _npz(store / "stages/DRY/PREC_x.npz")
    rec = json.loads(Path(ur.write_obligation(store, "REGISTRY_OBLIGATION.json", "DRO", "w",
                                              dry=True)).read_text(encoding="utf-8"))
    assert rec["attempt"] is None  # null for a dry store (J11)
    assert [(e["relpath"], e["class"]) for e in rec["files"]] == [
        ("stages/DRY/PREC_x.npz", "NON_HISTORY"), ("stages/OF/DRYHIST_OF_fit_b0.npz", HIST)]
    store2 = tmp_path / "hwsu-dry-of-y"
    _npz(store2 / "stages/OF/HIST_OF_fit_b0.npz", **_hist_arrays())
    with pytest.raises(C1GateFailure):
        ur.write_obligation(store2, "REGISTRY_OBLIGATION.json", "DRO", "w", dry=True)


# ------------------------------------------------------------------ registry risk (§2.8)
def test_registry_risk_exact_rationals():
    from fractions import Fraction
    p = C["handoff"]["p_D2a_copy_for_tests"]
    r = ur.registry_risk_u(p, 24576)
    assert r["ok"] is True and r["rows"] == 24576
    assert r["value"] == str(24576 * Fraction(float(p)))
    # TEST_PLAN note: rows * Fraction(float(p)) == 1/100 exactly is unreachable (1/100 is not
    # dyadic); the boundary is checked with the two floats around 1/100 instead.
    assert ur.registry_risk_u(0.01, 1)["ok"] is False  # Fraction(0.01) > 1/100: exact, not float
    assert ur.registry_risk_u(float(np.nextafter(0.01, 0.0)), 1)["ok"] is True
    assert ur.registry_risk_u(0.005, 2)["ok"] is False and ur.registry_risk_u(0.004, 2)["ok"] is True


# ------------------------------------------------------------------ OF-H (§4.2; RC-5; DRO7)
def _p_d2a(T, E, pi):
    s = E[:, :5].sum(axis=1)
    a = pi * s
    for _ in range(31):
        a = (a @ T) * s
    return float(a.sum())


def _ctx(E_low=0.01, planted=False):
    T, pi = np.full((2, 2), 0.5), np.array([0.5, 0.5])
    E = np.full((2, 36), (1 - E_low) / 31)
    E[:, :5] = E_low / 5
    canon = np.full((8, 32), 10, dtype=np.uint8)
    canon[:, 0] = np.arange(8) + 5
    a2 = canon.copy()
    if planted:
        a2[3] = 4  # every symbol in {0..4}: a sealed-D-2a row
    ids = np.arange(8, dtype=np.int64)
    proc = {"T": T, "E_canon_shared": E, "pi": pi, "coords": np.zeros((2, 2)), "ids": {}}
    return {"proc": proc, "fit": {"canon32": canon.copy(), "ids": ids},
            "eval": {"a1": canon.copy(), "a2": a2, "ids_a1": ids, "ids_a2": ids + 8},
            "seeds": dict(uc.DRY_SEEDS_OF), "results": {}}


def _status(fn, *a):
    try:
        d = fn(*a)
    except C1GateFailure as exc:
        return exc.status
    return (d or {}).get("status", "PASS")


def _handoff(monkeypatch, p):
    monkeypatch.setattr(uc, "load_handoff_u",
                        lambda *a, **k: {"p_D2a": float(p), "stage_c_exclusions": ()})


def test_of_h_pass(monkeypatch):
    import hwsu_of as uof
    ctx = _ctx()
    _handoff(monkeypatch, _p_d2a(ctx["proc"]["T"], ctx["proc"]["E_canon_shared"], ctx["proc"]["pi"]))
    assert _status(uof.of_h, ctx) == "PASS"


def test_of_h_sealed_row_first_and_no_oracle(monkeypatch):
    import hwsu_of as uof
    import hwsu_oracle as uo

    def boom(*a, **k):
        raise AssertionError("an oracle value was computed")

    monkeypatch.setattr(uo, "arm_oracle", boom)
    monkeypatch.setattr(uo, "suffix_oracle", boom)
    ctx = _ctx(planted=True)
    _handoff(monkeypatch, 0.5)  # (ii) would fail too: (i) is checked first
    assert _status(uof.of_h, ctx) == "INCONCLUSIVE/REGISTRY_INCOMPLETE"


@pytest.mark.parametrize("where", ["fit", "a1"])
def test_of_h_sealed_row_in_any_split(monkeypatch, where):
    import hwsu_of as uof
    ctx = _ctx()
    _handoff(monkeypatch, _p_d2a(ctx["proc"]["T"], ctx["proc"]["E_canon_shared"], ctx["proc"]["pi"]))
    arr = ctx["fit"]["canon32"] if where == "fit" else ctx["eval"]["a1"]
    arr[-1] = 0
    assert _status(uof.of_h, ctx) == "INCONCLUSIVE/REGISTRY_INCOMPLETE"


def test_of_h_p_d2a_mismatch(monkeypatch):
    import hwsu_of as uof
    ctx = _ctx()
    p = _p_d2a(ctx["proc"]["T"], ctx["proc"]["E_canon_shared"], ctx["proc"]["pi"])
    _handoff(monkeypatch, p * (1 + 1e-9))
    assert _status(uof.of_h, ctx) == "FAIL_TECHNICAL/SAMPLER"


def test_of_h_registry_risk_over_cap(monkeypatch):
    import hwsu_of as uof
    ctx = _ctx(E_low=0.99)  # p_D2a ~ 0.72: 24,576 rows far above 1/100
    _handoff(monkeypatch, _p_d2a(ctx["proc"]["T"], ctx["proc"]["E_canon_shared"], ctx["proc"]["pi"]))
    assert _status(uof.of_h, ctx) == "FAIL_TECHNICAL/SAMPLER"
