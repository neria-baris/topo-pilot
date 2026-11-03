"""Author B (job 0198): the OF job order, stopped-attempt obligations and reservation ends (D-17,
J10 item 3), exit codes, and OF-P's stage-C identity binding (protocol §4.1 J6/J10, §3.1, §4.2
OF-P; API §4, §9; D-11). TEST_PLAN §3 row test_b_of_driver; DRO1 order, DRO7, DRO9 (5).
The gate computations are stubbed here (author A tests them); the records, obligations and
reservations are real and written under tmp_path. The full tiny-world OF run is the DRO1 case."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_driver_of as udr  # noqa: E402
import hwsu_of as uof  # noqa: E402
import hwsu_records as ur  # noqa: E402
import hwsu_seed as us  # noqa: E402
import hwsb_data  # noqa: E402
import k4b_data  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402
from topo_pilot.contracts import ArtifactStore, MemoryBackend  # noqa: E402

GATES = ["OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2", "OF-3", "OF-4", "OF-5"]
STUB = {"OF-P": "of_p", "RESERVATION": "reservation_check", "OF-H": "of_h", "OF-1": "of_1",
        "OF-2": "of_2", "OF-3": "of_3", "OF-4": "of_4", "OF-5": "of_5"}
UTC = "2026-11-01T00:00:00Z"


def _table(b, sym):
    canon = np.full((4, 32), sym, dtype=np.uint8)
    canon[:, 2] = np.arange(4) + 5
    t = k4b_data.history_table(canon, np.arange(4, dtype=np.int64) + 10 * b, "of-fit", b)
    return {k: t[k] for k in ("canon32", "seq_ids", "digest", "landmark", "ref_row", "decoder_panel")}


def _world(tmp_path, monkeypatch, fail=None, ofb=None):
    """fail: {gate: exception or details dict}. Returns (root, out, calls)."""
    root = tmp_path / "root"
    out = root / "hwsu-store"
    out.mkdir(parents=True)
    calls = []

    def gate(name):
        def fn(*a):
            calls.append(name)
            if name == "OF-S":
                ctx = a[-1]
                ctx["rows_drawn"] = True
                files = []
                for i, kind in enumerate(("fit", "eval_a1", "eval_a2")):
                    for b in (0, 1):
                        files.append(ur.save_array(out, f"stages/OF/HIST_OF_{kind}_b{b}.npz",
                                                   **_table(b, 10 + i)))
            act = (fail or {}).get(name)
            if isinstance(act, BaseException):
                raise act
            return dict(act) if act else {"status": "PASS"}
        return fn

    monkeypatch.setattr(ur, "of_b", ofb or (lambda *a, **k: {"status": "PASS", "h_exec": "f"}))
    monkeypatch.setattr(us, "g0_of", gate("OF-0"))
    monkeypatch.setattr(uof, "of_s", gate("OF-S"))
    for g, fn in STUB.items():
        monkeypatch.setattr(uof, fn, gate(g))

    def report(o, ctx, records):
        calls.append("REPORT")
        return ur.save_array(o, "stages/OF/ORACLE_OF_eval.npz", G=np.arange(3.0))

    monkeypatch.setattr(uof, "of_report", report)
    return root, out, calls


def _ctx(root, out, attempt=1, rid="RES-HWSU-OF"):
    return udr.build_ctx(out, "0300", attempt, rid, root=root, mailbox=root / "agent-handoff",
                         hwsc_store=root / "hwsc-store", dry=False)


def _run(root, out, attempt=1, rid="RES-HWSU-OF", reserve=True, **kw):
    if reserve:
        ur.write_reservation(out, rid, uc.SCOPE_OF, UTC, "fixture coordinator")
    return udr.run_of(out, "0300", attempt=attempt, reservation_id=rid,
                      ctx=_ctx(root, out, attempt, rid), **kw)


def _obl(out, name):
    return json.loads((out / name).read_text(encoding="utf-8"))


def _end(out, rid):
    return json.loads((out / "reservations" / f"{rid}.END.json").read_text(encoding="utf-8"))


def _sha(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ build_ctx (API §9)
def test_build_ctx(tmp_path):
    out = tmp_path / "s"
    ctx = udr.build_ctx(out, "0300", 2, "RES-HWSU-OF-a2", root=tmp_path, mailbox=tmp_path / "m",
                        hwsc_store=tmp_path / "h")
    assert Path(ctx["reservation_path"]) == out / "RESERVATION_OF-a2.json"
    assert ctx["rows_drawn"] is False and ctx["scope"] == uc.SCOPE_OF == "hwsu-of-v1"
    assert dict(ctx["seeds"]) == dict(uc.SEEDS_OF) and ctx["dry"] is False
    assert (ctx["job"], ctx["attempt"], ctx["reservation_id"]) == ("0300", 2, "RES-HWSU-OF-a2")
    assert Path(ctx["out"]) == out and Path(ctx["mailbox"]) == tmp_path / "m"


# ------------------------------------------------------------------ success (J6, J10; DRO9 (5))
def test_success_order_obligation_then_end(tmp_path, monkeypatch):
    root, out, calls = _world(tmp_path, monkeypatch)
    r = _run(root, out)
    assert r["exit"] == 0 and r["outcome"] == "OF_PASS" and r["rows_drawn"] is True
    assert [c for c in calls if c != "REPORT"] == GATES  # of_report may live in a split module
    assert [x["gate"] for x in r["records"]] == GATES
    assert Path(r["obligation"]).name == "REGISTRY_OBLIGATION_OF.json"
    ob = _obl(out, "REGISTRY_OBLIGATION_OF.json")
    cls = {e["relpath"]: e["class"] for e in ob["files"]}
    hist = {f"stages/OF/HIST_OF_{k}_b{b}.npz" for k in ("fit", "eval_a1", "eval_a2") for b in (0, 1)}
    assert {p for p, c in cls.items() if c == "K4b history table"} == hist
    present = {q.relative_to(out).as_posix() for q in out.rglob("*") if q.suffix in (".npz", ".npy", ".pt")}
    assert set(cls) == present  # every array file then in the store (J10 item 2)
    assert all(c == "NON_HISTORY" for p, c in cls.items() if p not in hist)
    assert ob["job"] == "OF" and ob["track"] == "U"
    # SPEC-QUESTION: API §9 predates the J11 erratum; the driver is read as passing the attempt
    # and the reservation id it ends into the J11 obligation fields.
    assert ob["attempt"] == 1 and ob["reservation_id"] == "RES-HWSU-OF"
    end = _end(out, "RES-HWSU-OF")
    assert end["obligation_file"] == "hwsu-store/REGISTRY_OBLIGATION_OF.json"
    assert end["obligation_sha256"] == _sha(out / "REGISTRY_OBLIGATION_OF.json")
    assert ur.w2_attestation(root)["status"] == "PASS"


def test_share_dropped_gives_response_only(tmp_path, monkeypatch):
    root, out, calls = _world(tmp_path, monkeypatch, fail={"OF-3": {"status": "SHARE_DROPPED"}})
    r = _run(root, out)
    assert (r["exit"], r["outcome"]) == (0, "OF_PASS_RESPONSE_ONLY")
    assert [c for c in calls if c != "REPORT"] == GATES
    assert (out / "REGISTRY_OBLIGATION_OF.json").is_file()


# ------------------------------------------------------------------ refusals and stops
def test_of_b_failure_writes_only_the_gate_line(tmp_path, monkeypatch):
    def ofb(*a, **k):
        raise C1GateFailure("INVALID", "phase-1 file changed after FREEZE_OF")
    root, out, calls = _world(tmp_path, monkeypatch, ofb=ofb)
    ur.write_reservation(out, "RES-HWSU-OF", uc.SCOPE_OF, UTC, "fixture")
    before = {p.relative_to(out).as_posix() for p in out.rglob("*")}
    r = udr.run_of(out, "0300", ctx=_ctx(root, out))
    assert (r["exit"], r["outcome"]) == (2, "INVALID") and calls == []
    after = {p.relative_to(out).as_posix() for p in out.rglob("*")}
    assert after - before == {"GATES.jsonl"}
    g = [json.loads(x) for x in (out / "GATES.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert [(x["gate"], x["status"]) for x in g] == [("OF-B", "INVALID")]


def test_stop_before_first_row_then_rerun(tmp_path, monkeypatch):
    """D-17 / J10 item 3: a no-history obligation ends RES-HWSU-OF; the rerun uses RES-HWSU-OF-a2."""
    fail = {"RESERVATION": C1GateFailure("INCONCLUSIVE/AUTHORITY", "reservation check")}
    root, out, calls = _world(tmp_path, monkeypatch, fail=fail)
    r = _run(root, out)
    assert r["exit"] == 2 and r["outcome"] == "INCONCLUSIVE/AUTHORITY" and r["rows_drawn"] is False
    assert "OF-S" not in calls and "REPORT" not in calls
    assert [x["status"] for x in r["records"]][3:] == ["NOT_RUN"] * 7
    ob = _obl(out, "REGISTRY_OBLIGATION_OF-a1.json")
    assert ob["files"] == [] and not (out / "REGISTRY_OBLIGATION_OF.json").exists()
    end = _end(out, "RES-HWSU-OF")
    assert end["obligation_file"] == "hwsu-store/REGISTRY_OBLIGATION_OF-a1.json"
    assert ur.w2_attestation(root)["status"] == "PASS"
    # the rerun: a new id in a new file, accepted by the attestation
    fail.clear()
    ur.write_reservation(out, "RES-HWSU-OF-a2", uc.SCOPE_OF, UTC, "fixture coordinator")
    assert ur.w2_attestation(root, own="RES-HWSU-OF-a2")["status"] == "PASS"
    r2 = udr.run_of(out, "0300", attempt=2, reservation_id="RES-HWSU-OF-a2",
                    ctx=_ctx(root, out, 2, "RES-HWSU-OF-a2"))
    assert (r2["exit"], r2["outcome"]) == (0, "OF_PASS")
    assert _end(out, "RES-HWSU-OF-a2")["obligation_file"] == "hwsu-store/REGISTRY_OBLIGATION_OF.json"
    assert ur.w2_attestation(root)["status"] == "PASS"


def test_of_0_failure_refused(tmp_path, monkeypatch):
    root, out, calls = _world(tmp_path, monkeypatch,
                              fail={"OF-0": C1GateFailure("FAIL_TECHNICAL/SEED_SCOPE", "hit")})
    r = _run(root, out)
    assert r["exit"] == 2 and r["outcome"] == "FAIL_TECHNICAL/SEED_SCOPE" and calls == ["OF-0"]
    assert _obl(out, "REGISTRY_OBLIGATION_OF-a1.json")["files"] == []
    assert (out / "reservations" / "RES-HWSU-OF.END.json").is_file()


@pytest.mark.parametrize("gate,exc,code", [
    ("OF-1", C1GateFailure("FAIL_TECHNICAL/ORACLE", "KO3"), 3),
    ("OF-H", C1GateFailure("INCONCLUSIVE/REGISTRY_INCOMPLETE", "sealed row"), 5),
    ("OF-2", C1GateFailure("INCONCLUSIVE/ORACLE_FEASIBILITY", "headroom"), 5),
    ("OF-5", C1GateFailure("FAIL_TECHNICAL/SAMPLER", "lemma P"), 3),
])
def test_stop_after_rows_exit_codes_and_obligation(tmp_path, monkeypatch, gate, exc, code):
    root, out, calls = _world(tmp_path, monkeypatch, fail={gate: exc})
    r = _run(root, out, attempt=1)
    assert r["exit"] == code and r["outcome"] == exc.status and r["rows_drawn"] is True
    assert calls[-1] in (gate, "REPORT") and calls.index(gate) == GATES.index(gate)
    ob = _obl(out, "REGISTRY_OBLIGATION_OF-a1.json")
    assert sum(e["class"] == "K4b history table" for e in ob["files"]) == 6
    assert not (out / "REGISTRY_OBLIGATION_OF.json").exists()
    assert _end(out, "RES-HWSU-OF")["obligation_sha256"] == _sha(out / "REGISTRY_OBLIGATION_OF-a1.json")


def test_pause_exit_4_with_obligation(tmp_path, monkeypatch):
    root, out, calls = _world(tmp_path, monkeypatch)
    ledger = tmp_path / "HWSU_CPU_LEDGER.json"
    ur.ledger_append(ledger, "OF-0300-a0", "0300", "OF", 3000.0, "fixture")
    r = _run(root, out, ledger_path=ledger)
    assert (r["exit"], r["outcome"]) == (4, "PAUSE") and calls == []
    assert _obl(out, "REGISTRY_OBLIGATION_OF-a1.json")["files"] == []
    assert (out / "reservations" / "RES-HWSU-OF.END.json").is_file()
    g = [json.loads(x) for x in (out / "GATES.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert any(x["gate"] == "PAUSE_OF" and x["status"] == "PAUSE" for x in g)


def test_dry_continue_runs_every_gate(tmp_path, monkeypatch):
    root, out, calls = _world(tmp_path, monkeypatch,
                              fail={"OF-1": C1GateFailure("FAIL_TECHNICAL/ORACLE", "planted")})
    r = _run(root, out, dry_continue=True)
    assert [c for c in calls if c != "REPORT"] == GATES
    assert all(x["status"] != "NOT_RUN" for x in r["records"])
    assert r["outcome"] == "FAIL_TECHNICAL/ORACLE"


def test_main_unknown_subcommand():
    try:
        code = udr.main(["no-such-subcommand"])
    except SystemExit as exc:  # API-AMBIGUITY: argparse's exit(2)
        code = exc.code
    assert code not in (0, None)  # API §9 leaves the code open; an unknown command is not success


# ------------------------------------------------------------------ OF-P (§3.1; D-11)
@pytest.fixture(scope="module")
def real_ids():
    proc = hwsb_data.build_process(ArtifactStore(MemoryBackend()), masters=uc.MASTERS)
    return proc["ids"]


def _hwsc_meta(hs, ids, skip=None, **bad):
    def put(t, i, rec):
        p = hs / "artifacts" / t / i / "meta.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rec), encoding="utf-8")
    put("WorldSpec", ids["world"], {"artifact_type": "WorldSpec"})
    put("TransitionSpec", ids["transition"], {"artifact_type": "TransitionSpec"})
    for m, e in ids["emission"].items():
        if m != skip:
            put("EmissionSpec", e, {"artifact_type": bad.get("atype", "EmissionSpec"),
                                    "config": {"replicate": bad.get("rep", {}).get(m, m)}})


def _of_p_status(ctx):
    try:
        d = uof.of_p(ctx)
    except C1GateFailure as exc:
        return exc.status
    return (d or {}).get("status", "PASS")


def test_of_p_pass_and_explicit_masters(tmp_path, monkeypatch, real_ids):
    root = tmp_path / "root"
    _hwsc_meta(root / "hwsc-store", real_ids)
    seen = []
    real = hwsb_data.build_process

    def spy(store, *a, **k):
        seen.append((a, k))
        return real(store, *a, **k)

    monkeypatch.setattr(hwsb_data, "build_process", spy)
    ctx = _ctx(root, root / "hwsu-store")
    assert _of_p_status(ctx) == "PASS"
    assert len(seen) == 1
    a, k = seen[0]
    masters = k["masters"] if "masters" in k else (a[0] if a else None)
    assert tuple(masters) == tuple(uc.MASTERS)  # passed explicitly (conditional-read rule)
    p = ctx["proc"]
    assert p["ids"]["world"] == "21feee1d8ee5422e" and p["ids"]["transition"] == "e4dafc7b9785c172"
    assert set(p) >= {"T", "E_canon_shared", "pi", "coords", "ids"}


@pytest.mark.parametrize("case", ["missing_620302", "replicate", "atype", "no_world"])
def test_of_p_identity_failures(tmp_path, real_ids, case):
    root = tmp_path / "root"
    hs = root / "hwsc-store"
    if case == "missing_620302":
        _hwsc_meta(hs, real_ids, skip=620302)
    elif case == "replicate":
        _hwsc_meta(hs, real_ids, rep={620303: 620301})
    elif case == "atype":
        _hwsc_meta(hs, real_ids, atype="Checkpoint")
    else:
        _hwsc_meta(hs, real_ids)
        (hs / "artifacts" / "WorldSpec" / real_ids["world"] / "meta.json").unlink()
    assert _of_p_status(_ctx(root, root / "hwsu-store")) == "FAIL_TECHNICAL/IDENTITY"
