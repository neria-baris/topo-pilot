"""Author B, T-POLICY-ND (protocol §3, §6.7, §10.1, §12) and T-SEAL-ND (§6.7 L5, §12 S12);
API.md §8.3, §9.1, §9.4, §9.6, §14.1. Synthetic stores under pytest's tmp_path only."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_driver as ndr  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

ORDER = ("IMPL", "AUTH-ADMIT", "G0", "PF", "H1", "REG", "H2", "H3", "H4", "H5", "ORACLE-FEAS",
         "M0", "M0-D", "C0c", "F1", "SUP", "L1", "R1", "N2", "SURVIVAL", "X1", "DX", "V3x",
         "V3y", "Y1", "V3x'", "Y1'", "V3x'-g1", "KC", "KC-R", "P1", "ACCEPT", "REG2", "T-PRE",
         "T-PRE-MODEL", "RESP-SPEC", "NUM", "ENDPOINT", "REPORT")
ALLOWED = {"m0": {"M0", "M0-D", "T-PRE"}, "x1": {"X1", "T-PRE"}, "dx": {"DX", "T-PRE"},
           "val_gate": {"V3x", "V3y", "Y1", "V3x'", "Y1'", "V3x'-g1"}, "val_kc": {"KC", "KC-R"},
           "val_sealed": {"P1"}, "construction": {"M0-D", "F1", "DX", "T-PRE"},
           "test_endpoint": {"RESP-SPEC", "NUM", "ENDPOINT", "REPORT"}}
RELEASE_ONLY = ("V3x'", "Y1'", "V3x'-g1", "KC", "KC-R")


def at_gate(gate):
    pol = ndr.LogitPolicy(done=ndr.GATE_ORDER[: ndr.GATE_ORDER.index(gate)])
    pol.begin(gate)
    return pol


def status_of(exc_info):
    return getattr(exc_info.value, "status", str(exc_info.value))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ctx_for(store, policy=None, job="0130"):
    Path(store).mkdir(parents=True, exist_ok=True)
    return ndr.Ctx(store=Path(store), worktree=Path(store).parent, head="c0ffee", job=job,
                   task_sha256="ab" * 32, session="sess-b", release=None, policy=policy,
                   data={}, dry=False)


def gates_file(store, rows):
    path = Path(store) / "GATES.jsonl"
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            rec = {"gate": r[0], "status": r[1], "full_status": r[1], "scope": r[2],
                   "family": r[3] if len(r) > 3 else None, "model": None,
                   "utc": "2026-10-26T00:00:00Z"}
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return path


# ---- T-POLICY-ND ------------------------------------------------------------------------------
def test_gate_order_is_the_protocol_list():
    assert tuple(ndr.GATE_ORDER) == ORDER and len(ORDER) == 39
    assert all(g.isascii() for g in ORDER)
    assert tuple(nc.CONTRACT["gate_order"]) == ORDER
    assert tuple(ndr.STAGE_ENTRY) == ("AUTH-ADMIT", "G0")
    assert tuple(nc.CONTRACT["release_pass_fail_only"]) == RELEASE_ONLY


def test_begin_in_order_and_out_of_order():
    pol = ndr.LogitPolicy()
    for g in ORDER:
        pol.begin(g)
        pol.end(g)
    pol = ndr.LogitPolicy()
    pol.begin("IMPL")
    pol.end("IMPL")
    with pytest.raises(C1GateFailure):
        pol.begin("G0")  # AUTH-ADMIT skipped
    pol = ndr.LogitPolicy(done=ORDER[: ORDER.index("ORACLE-FEAS")])
    with pytest.raises(C1GateFailure):
        pol.begin("M0")  # ORACLE-FEAS skipped
    pol = at_gate("DX")
    with pytest.raises(C1GateFailure):
        pol.begin("V3x")  # DX still open


def test_stage_entry_repeats_are_allowed():
    pol = ndr.LogitPolicy(done=ORDER[: ORDER.index("M0")])
    for g in ("AUTH-ADMIT", "G0", "M0", "M0-D"):
        pol.begin(g)
        pol.end(g)
    with pytest.raises(C1GateFailure):
        pol.begin("PF")  # not a stage-entry gate: no going back


@pytest.mark.parametrize("gate", ORDER)
def test_require_matrix(gate):
    for kind, allowed in ALLOWED.items():
        pol = at_gate(gate)
        if gate in allowed:
            pol.require(kind)
        else:
            with pytest.raises(C1GateFailure) as ei:
                pol.require(kind)
            assert status_of(ei).startswith("FAIL_TECHNICAL"), (gate, kind)


def test_no_feas_logit_and_no_endpoint_before_t_pre():
    for gate in ("SUP", "L1", "R1", "N2", "SURVIVAL"):  # DFEAS: no logit of any kind
        assert not any(gate in a for a in ALLOWED.values())
        for kind in ALLOWED:
            with pytest.raises(C1GateFailure):
                at_gate(gate).require(kind)
    for gate in ORDER[: ORDER.index("RESP-SPEC")]:
        with pytest.raises(C1GateFailure):
            at_gate(gate).require("test_endpoint")


@pytest.mark.parametrize("gate", ("X1", "DX", "T-PRE"))
def test_no_write_during_identity_gates(gate):
    for kind in ALLOWED:
        with pytest.raises(C1GateFailure) as ei:
            at_gate(gate).require_write(kind)
        assert status_of(ei) == "INVALID/LEAKAGE"


def test_require_write_outside_allowed():
    at_gate("P1").require_write("val_sealed")
    at_gate("ENDPOINT").require_write("test_endpoint")
    for gate, kind in (("V3x", "val_sealed"), ("REG2", "test_endpoint"), ("KC", "val_sealed")):
        with pytest.raises(C1GateFailure) as ei:
            at_gate(gate).require_write(kind)
        assert status_of(ei) == "INVALID/LEAKAGE"


def test_dtest_sampling_needs_release_r5(tmp_path):
    store = tmp_path / "store"
    ctx = ctx_for(store)
    assert ndr.release_ok(ctx, "S5")["ok"] is False  # no RELEASE_R5.json
    (store / "FREEZE.json").write_text('{"schema": "c2nd-freeze-v1"}\n', encoding="utf-8")
    (store / "stages" / "S4").mkdir(parents=True)
    p1 = {"N_test": 4096, "k": 1}
    (store / "stages" / "S4" / "P1.json").write_text(json.dumps(p1), encoding="utf-8")
    rel = {"schema": "c2nd-release-v1", "release": "R5", "stages": ["S5"], "job": ctx.job,
           "task_sha256": ctx.task_sha256, "head": ctx.head,
           "protocol_sha256": nc.PROTOCOL_SHA256, "freeze_sha256": sha(store / "FREEZE.json"),
           "N_test": 4096, "k": 1, "accept_review_sha256": "cd" * 32, "coordinator": "c",
           "utc": "2026-10-26T00:00:00Z"}

    def ok_with(**change):
        path = store / "RELEASE_R5.json"
        path.write_text(json.dumps(dict(rel, **change)), encoding="utf-8")
        return ndr.release_ok(ctx, "S5")["ok"]

    assert ok_with() is True
    assert ok_with(k=2) is False  # differs from the S4 P1 record
    assert ok_with(accept_review_sha256=None) is False
    assert ok_with(stages=["S4"]) is False
    assert ok_with(protocol_sha256="0" * 64) is False


def d_inputs(n=8):
    rng = np.random.default_rng(12)
    a = np.abs(rng.normal(size=n)) + 0.1
    q = {"A_full": a, "A_S": 0.1 * a, "e_full": a * a, "e_S": 0.01 * a * a, "r": a * a}
    E = np.ones(n, dtype=bool)
    return q, {"A_full": a, "A_S": 0.0 * a}, 2.0 * a, E


@pytest.mark.parametrize("problem", ("construction", "R"))
def test_d_stream_refuses_the_construction_projector(problem):
    qx, qy, G, E = d_inputs()
    with pytest.raises(C1GateFailure) as ei:
        nat.d_stream(qx, qy, G, E, E, refit={"problem": problem})
    assert status_of(ei) == "INVALID/LEAKAGE"
    out = nat.d_stream(qx, qy, G, E, E, refit={"problem": "RD"})
    assert set(out) == {"V3x", "Y1", "Z010", "Z050", "Vabs", "Vrand", "NEG"}


def s_sequence():
    seq = list(ORDER[:11])
    seq += ["AUTH-ADMIT", "G0", "M0", "M0-D", "M0-D", "M0-D", "C0c", "C0c", "F1"]
    seq += ["AUTH-ADMIT", "G0"] + list(ORDER[15:20])
    seq += ["AUTH-ADMIT", "G0"] + list(ORDER[20:31])
    seq += ["AUTH-ADMIT", "G0"] + list(ORDER[31:])
    return seq


def test_check_sequence(tmp_path):
    seq = s_sequence()
    assert ndr.check_sequence(gates_file(tmp_path, [(g, "PASS", "study") for g in seq]))
    bad = list(seq)
    i, j = bad.index("H3"), bad.index("H4")
    bad[i], bad[j] = bad[j], bad[i]
    assert not ndr.check_sequence(gates_file(tmp_path, [(g, "PASS", "study") for g in bad]))
    unknown = seq[:5] + ["Y1*"] + seq[5:]  # a C2 gate name is not an ND gate
    assert not ndr.check_sequence(gates_file(tmp_path, [(g, "PASS", "study") for g in unknown]))


# ---- T-SEAL-ND --------------------------------------------------------------------------------
# API-AMBIGUITY: API.md §9.1 lists require_release(gate, values) under LogitPolicy while
# TEST_PLAN names it "ndr.require_release (policy)"; it is called here as a LogitPolicy method.
@pytest.mark.parametrize("gate", RELEASE_ONLY)
def test_releases_carry_pass_fail_only(gate):
    pol = ndr.LogitPolicy()
    good = {"cases": {"D0": "PASS", "DONLY": "FAIL"}} if gate.startswith("KC") else {
        "result": "PASS"}
    pol.require_release(gate, good)
    pol.require_release(gate, dict(good, model=1729))
    for key in ("mean", "L", "U", "category", "bounds", "theta", "psi"):
        with pytest.raises(C1GateFailure) as ei:
            pol.require_release(gate, dict(good, **{key: 0.5}))
        assert status_of(ei) == "INVALID/LEAKAGE", key


def test_kc_gate_full_statuses():
    ok = ndc.kc_gate({"D0": "PASS", "DONLY": "PASS", "DDOSE": "PASS"})
    assert ok == {"status": "PASS", "full_status": "PASS",
                  "cases": {"D0": "PASS", "DONLY": "PASS", "DDOSE": "PASS"}}
    both = ndc.kc_gate({"D0": "PASS", "DONLY": "CONTRADICTED", "DDOSE": "UNRESOLVED"})
    assert both["status"] == "FAIL" and both["full_status"] == "KNOWN_CASE_CONTRADICTED"
    assert both["cases"] == {"D0": "PASS", "DONLY": "FAIL", "DDOSE": "FAIL"}
    unres = ndc.kc_gate({"D0": "UNRESOLVED", "DONLY": "PASS", "DDOSE": "PASS"})
    assert unres["status"] == "FAIL"
    assert unres["full_status"] == "EXCLUDED/KNOWN_CASE_UNRESOLVED"
    for res in (ok, both, unres):  # no mean, bound or declared category in the record
        assert set(res) == {"status", "full_status", "cases"}
        assert set(res["cases"].values()) <= {"PASS", "FAIL"}


# API-AMBIGUITY: API.md §8.3 does not say how a case that could not be formed is passed to
# kcr_gate; the per-case value "NOT_COMPUTED" is used here.
def test_kcr_gate_full_statuses():
    def g(r, i):
        return ndc.kcr_gate({"DNULLR": r, "DID": i})

    assert g("PASS", "PASS") == {"status": "PASS", "full_status": "PASS",
                                 "cases": {"DNULLR": "PASS", "DID": "PASS"}}
    c = g("CONTRADICTED", "UNRESOLVED")
    assert (c["status"], c["full_status"]) == ("FAIL", "MOVE_CASE_CONTRADICTED")
    u = g("UNRESOLVED", "PASS")
    assert (u["status"], u["full_status"]) == ("FAIL", "UNRESOLVED")
    n = g("NOT_COMPUTED", "NOT_COMPUTED")
    assert (n["status"], n["full_status"]) == ("NOT_RUN", "NOT_COMPUTED")
    for res in (c, u):
        assert set(res) == {"status", "full_status", "cases"}


def test_seal_exclusive_and_p1_only(tmp_path):
    store = tmp_path / "store"
    ctx = ctx_for(store, at_gate("P1"))
    arrays = {"A_S": np.arange(5.0), "A_comp": -np.arange(5.0)}
    s = ndr.seal(ctx, "VAL_NR_1729", arrays)
    path = store / "sealed" / "VAL_NR_1729.npz"
    assert path.is_file() and s == sha(path)
    rec = json.loads((store / "stages" / "S4" / "SEALED.json").read_text(encoding="utf-8"))
    assert rec["VAL_NR_1729"] == s
    with pytest.raises(Exception):
        ndr.seal(ctx, "VAL_NR_1729", arrays)  # exclusive create
    assert sha(path) == s
    for gate in ("X1", "KC", "REPORT"):
        ctx.policy = at_gate(gate)
        with pytest.raises(C1GateFailure) as ei:
            ndr.seal(ctx, f"VAL_D_{gate}", arrays)
        assert status_of(ei) == "INVALID/LEAKAGE"
        assert not (store / "sealed" / f"VAL_D_{gate}.npz").exists()


def sealed_store(tmp_path, name):
    store = tmp_path / name
    ctx = ctx_for(store, at_gate("P1"))
    arrays = {"x": np.linspace(0.0, 1.0, 7)}
    s = ndr.seal(ctx, "VAL_KC_1729", arrays)
    ctx.policy = at_gate("REPORT")
    return ctx, s, arrays


def endpoint(fam):
    return ("ENDPOINT", "PASS", "family", fam)


def test_unseal_needs_every_alive_endpoint(tmp_path):
    ctx, s, arrays = sealed_store(tmp_path, "a")
    gates_file(ctx.store, [("P1", "PASS", "family", "N-R"), endpoint("N-R"), endpoint("D")])
    with pytest.raises(Exception) as ei:
        ndr.unseal(ctx, "VAL_KC_1729", s)
    assert "LEAKAGE" in str(ei.value)
    gates_file(ctx.store, [endpoint("N-R"), endpoint("D"), endpoint("N-M")])
    out = ndr.unseal(ctx, "VAL_KC_1729", s)
    assert np.array_equal(out["x"], arrays["x"])
    with pytest.raises(Exception):
        ndr.unseal(ctx, "VAL_KC_1729", "0" * 64)  # re-hash mismatch


def test_unseal_after_family_or_study_stop(tmp_path):
    ctx, s, arrays = sealed_store(tmp_path, "b")
    gates_file(ctx.store, [("SURVIVAL", "FAIL", "family", "N-M"), endpoint("N-R"),
                           endpoint("D")])
    assert np.array_equal(ndr.unseal(ctx, "VAL_KC_1729", s)["x"], arrays["x"])
    ctx2, s2, _ = sealed_store(tmp_path, "c")
    gates_file(ctx2.store, [("REG2", "FAIL", "study")])
    assert "x" in ndr.unseal(ctx2, "VAL_KC_1729", s2)
    ctx3, s3, _ = sealed_store(tmp_path, "d")
    gates_file(ctx3.store, [("ACCEPT", "PASS", "study")])
    with pytest.raises(Exception):
        ndr.unseal(ctx3, "VAL_KC_1729", s3)
