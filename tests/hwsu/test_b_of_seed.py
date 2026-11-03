"""Author B (job 0198): the J9 seed-search mirror, the declaration fragments, the namespace
overlap check (D-16) and G0-OF (protocol §4.2 OF-0; RC-3, J3, J5, J9, J10; API §6). TEST_PLAN §3
row test_b_of_seed; DRO6. Synthetic roots and a synthetic mailbox under tmp_path only.

Note: pytest's basetemp (X:/Downloads/topo-scratch/test_hwsu-<job>/...) itself contains the
declaration fragment "/topo-scratch/test_hwsu-", so every hit inside tmp_path is declared by
construction. Classification is therefore checked on hits re-based to a fake project root
("Z:/projects/topo-pilot/<relpath>"), as the real search reports them under the real root."""

from __future__ import annotations

import builtins
import copy
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_records as ur  # noqa: E402
import hwsu_seed as us  # noqa: E402
import hwsb_config  # noqa: E402
import hwsc_known  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
FAKE = "Z:/projects/topo-pilot/"


def _norm(p) -> str:
    return os.path.normcase(os.path.abspath(str(p)))


def _hook(monkeypatch) -> list:
    seen, real_open = [], builtins.open

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
    return seen


def _w(p, text) -> Path:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8") if isinstance(text, str) else text)
    return p


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _rebase(hits, root):
    return [dict(h, path=FAKE + Path(h["path"]).relative_to(root).as_posix()) for h in hits]


# ------------------------------------------------------------------ search mirror (J5, J9)
def _plain_root(root):
    _w(root / "topo-pilot/tools/hwsu/CONTRACT.json", '{"d": "hwsd-v1", "s": 629950}\n')
    _w(root / "topo-pilot/src/x.py", "a = 1\nseed = 640101\nscope = 'hwsu-of-v1'\n")
    _w(root / "agent-handoff/records/X.json", '{"s": "hwsu-store", "n": 649901}\n')
    _w(root / "notes/a.txt", "x 640120 y\n")
    _w(root / "notes/b.npz", b"640101")  # not a text suffix
    _w(root / "notes/sealed/c.txt", "640101\n")  # a skipped directory
    _w(root / "notes/.git/d.md", "640101\n")


def test_seed_search_equals_stage_c_mirror(tmp_path):
    root = tmp_path / "root"
    _plain_root(root)
    nd = us.needles()
    got = us.seed_search_u(root, nd)
    assert got == hwsc_known.seed_search_c(root, nd)
    assert {(Path(h["path"]).name, h["needle"]) for h in got} == {
        ("CONTRACT.json", "hwsd-v1"), ("CONTRACT.json", "629950"), ("x.py", "640101"),
        ("x.py", "hwsu-of-v1"), ("X.json", "hwsu-store"), ("X.json", "649901"), ("a.txt", "640120")}
    assert all(set(h) == {"path", "needle", "line"} for h in got)


def test_digit_needles_whole_tokens(tmp_path):
    root = tmp_path / "root"
    _w(root / "a.txt", "6401011\na640101\nx_640101\n640101b\n(640101)\n")
    hits = us.seed_search_u(root, ["640101"])
    assert [h["line"] for h in hits] == [5]


def _blinded_fixtures(root):
    _w(root / "agent-handoff/planning/coord-hws-dyn-x.md", "hwsu-v1 640101\n")
    _w(root / "agent-handoff/planning/HWSD-v1.md", "hwsu-v1\n")
    _w(root / "agent-handoff/records/HWSD_DESIGN_FREEZE.json", '"hwsu-v1"\n')
    _w(root / "hwsd-store/x.json", '{"t": "hwsu-v1"}\n')
    _w(root / "hwsd-store/stages/y.json", '{"t": "640102"}\n')
    _w(root / "hwsc-store/stages/S8/RESULT.json", '{"t": "640103"}\n')
    return [root / "agent-handoff/planning/coord-hws-dyn-x.md",
            root / "agent-handoff/planning/HWSD-v1.md",
            root / "agent-handoff/records/HWSD_DESIGN_FREEZE.json", root / "hwsd-store/x.json",
            root / "hwsd-store/stages/y.json", root / "hwsc-store/stages/S8/RESULT.json"]


def test_blinded_files_pruned_unopened(tmp_path, monkeypatch):
    root = tmp_path / "root"
    blind = _blinded_fixtures(root)
    _w(root / "hwsd-store/REGISTRY_OBLIGATION.json", '{"t": "hwsu-store"}\n')
    _w(root / "hwsd-store/reservations/x.END.json", '{"t": "hwsu-store"}\n')
    _w(root / "hwsd-store/RESERVATION_X.json", '{"t": "hwsu-store"}\n')
    seen = _hook(monkeypatch)
    hits = us.seed_search_u(root, us.needles())
    monkeypatch.undo()
    assert not any(_norm(b) in seen for b in blind)
    found = {Path(h["path"]).relative_to(root).as_posix() for h in hits}
    assert found == {"hwsd-store/REGISTRY_OBLIGATION.json", "hwsd-store/reservations/x.END.json",
                     "hwsd-store/RESERVATION_X.json"}  # J9: searched and declared


def test_search_root_for_guard(tmp_path):
    root = tmp_path / "root"
    _blinded_fixtures(root)
    sub = root / "hwsd-store"
    assert us.seed_search_u(sub, ["hwsu-v1"], root_for_guard=root) == []


# ------------------------------------------------------------------ classification (J9)
def _decl_root(root):
    _w(root / "hwsu-store/FREEZE_OF.json", '{"scope": "hwsu-of-v1"}\n')
    _w(root / "topo-pilot/docs/code_index/files/tools/hwsu/x.md", "640105\n")
    _w(root / "topo-pilot/tools/hwsd/CONTRACT.json", '{"u": "hwsu-v1"}\n')
    _w(root / "topo-pilot/tools/hwsu/CONTRACT.json", '{"d": "hwsd-dry-v1", "s": 620400}\n')
    _w(root / "topo-pilot/tests/hwsu/t.py", "649902\n")
    _w(root / "hwsd-store/REGISTRY_OBLIGATION.json", '{"t": "hwsu-store"}\n')
    _w(root / "agent-handoff/jobs/0198/task.md", "hwsu-dry-v1\n")
    _w(root / "coord-scratch/n.md", "640104\n")


def test_classify_declarations(tmp_path):
    root = tmp_path / "root"
    _decl_root(root)
    hits = _rebase(us.seed_search_u(root, us.needles()), root)
    assert len(hits) >= 9
    c = us.classify_hits_u(hits)
    assert c["status"] == "PASS"
    assert {h["kind"] for h in c["hits"]} == {"hwsu_declaration"}


@pytest.mark.parametrize("rel,text", [("topo-pilot/src/x.py", "seed = 640101\n"),
                                      ("topo-pilot/src/y.py", "s = 'hwsd-v1'\n"),
                                      ("other-store/r.json", '"629999"\n'),
                                      ("topo-pilot/tools/hwsc/x.md", "hwsu-store\n")])
def test_classify_unclassified(tmp_path, rel, text):
    root = tmp_path / "root"
    _decl_root(root)
    _w(root / rel, text)
    c = us.classify_hits_u(_rebase(us.seed_search_u(root, us.needles()), root))
    assert c["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    bad = [h for h in c["hits"] if h["kind"] == "unclassified"]
    assert {h["path"] for h in bad} == {FAKE + rel}


def test_classify_explicit_lists_never_read_stage_b_contract(monkeypatch):
    """Ruling (conditional reads): HWSU always passes both lists, so hwsb_config.CONTRACT
    ["seeds"] is never read, also through the defaults of classify_hits_u."""
    monkeypatch.setattr(hwsb_config, "CONTRACT", {})
    hits = [{"path": FAKE + "agent-handoff/a.md", "needle": "640101", "line": 1}]
    assert us.classify_hits_u(hits)["status"] == "PASS"
    c = us.classify_hits_u(hits, fragments=["/nowhere/"], job_scratch=[])
    assert c["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    c = us.classify_hits_u(hits, fragments=[], job_scratch=[FAKE.lower()])
    assert c["status"] == "PASS" and c["hits"][0]["kind"] == "hwsu_declaration"


def test_needles_are_contract_lists():
    nd = list(us.needles())
    assert len(nd) == 44 + 155 == len(C["g0"]["needles_u"]) + len(C["g0"]["needles_d"])
    assert nd == C["g0"]["needles_u"] + C["g0"]["needles_d"]
    assert {"hwsd-dry", "test_hwsd-", "620400", "629999"} <= set(nd)  # D-24 glob tokens


def test_contract_fragments_are_j9_list():
    t, o = "hwsu", "hwsd"
    own = [f"/tools/{t}/", f"/tests/{t}/", "/agent-handoff/", f"/{t}-store/", "/coord-scratch/",
           "/docs/code_index/", f"/topo-scratch/{t}-dry", f"/topo-scratch/test_{t}-"]
    other = [f"/tools/{o}/", f"/tests/{o}/", f"/topo-scratch/{o}-dry", f"/topo-scratch/test_{o}-",
             f"/{o}-store/"]
    assert sorted(C["g0"]["declaration_fragments"]) == sorted(own + other)
    assert C["g0"]["job_scratch"] == []


# ------------------------------------------------------------------ namespace overlap (D-16)
def _ns():
    rec = json.loads((Path(C["resources"]["mailbox"]) / "records" / "HWS_UD_NAMESPACE.json")
                     .read_text(encoding="utf-8")) if (Path(C["resources"]["mailbox"]) / "records" /
                                                       "HWS_UD_NAMESPACE.json").is_file() else None
    if rec is None:
        rec = {"tracks": {"U": C["namespace"]["U"], "D": C["namespace"]["D_declared"]}}
    return rec["tracks"]["U"], rec["tracks"]["D"]


def test_namespace_real_record_disjoint():
    u, d = _ns()
    assert u == C["namespace"]["U"]
    assert us.namespace_overlap(u, d) == []


@pytest.mark.parametrize("change", [
    lambda d: d["scopes"].append("hwsu-v1"),
    lambda d: d["scopes"].append("HWSU-DRY-V1"),
    lambda d: d["scopes"].append("x-hwsu-of-v1-y"),
    lambda d: d.update(seed_blocks=[[620400, 620499], [640120, 640130]]),
    lambda d: d.update(seed_blocks=[[649000, 649901]]),
    lambda d: d.update(store="X:/Downloads/projects/topo-pilot/hwsu-store-x"),
    lambda d: d.update(dry_store_glob="X:/Downloads/topo-scratch/hwsu-dry*"),
    lambda d: d.update(test_root_glob="X:/Downloads/topo-scratch/test_hwsu-*"),
])
def test_namespace_overlap_detected(change):
    u, d = _ns()
    d = copy.deepcopy(d)
    change(d)
    assert us.namespace_overlap(u, d) != []


def test_namespace_adjacent_seed_blocks_disjoint():
    u, d = _ns()
    d = dict(copy.deepcopy(d), seed_blocks=[[640121, 640200], [649921, 649999], [640000, 640100]])
    assert us.namespace_overlap(u, d) == []


# ------------------------------------------------------------------ G0-OF (OF-0; API §6)
def _g0_world(tmp_path, d_track=None, u_track=None):
    root = tmp_path / "root"
    mb, out, job = root / "agent-handoff", root / "hwsu-store", "0300"
    c = copy.deepcopy(uc.CONTRACT)
    a = c["authority"]
    for ad in a["addenda"]:
        ad["sha256"] = _sha(_w(mb / ad["path"], f"addendum {ad['addendum']} fixture\n"))
    _w(mb / a["design"]["path"], Path(uc.PROTOCOL_PATH).read_bytes())  # sha256 stays 9efbabdf...
    fr = a["design"]["freeze_record"]
    fr["sha256"] = _sha(_w(mb / fr["path"], '{"fixture": true}\n'))
    a["request"]["sha256"] = _sha(_w(mb / a["request"]["path"], "request fixture\n"))
    ns = {"schema": "hws-ud-namespace-v1", "fixture": True,
          "tracks": {"U": u_track or c["namespace"]["U"], "D": d_track or c["namespace"]["D_declared"]}}
    hs = root / "hwsc-store"
    bound = {"reservation_file": _w(hs / "RESERVATION_W2.json", '{"id": "RES-HWSC-W2"}\n'),
             "run_lock_file": _w(hs / "RUN.lock", "job 0196\n"),
             "operation_active_file": _w(hs / "OPERATION_ACTIVE.json", '{"state": "idle"}\n')}
    w2 = {"schema": "hwsc-w2-end-v1", "reservation_id": "RES-HWSC-W2", "fixture": True}
    for k, p in bound.items():
        w2[k] = p.relative_to(root).as_posix()
        w2[k.replace("_file", "_sha256") if k != "reservation_file" else "reservation_file_sha256"] = _sha(p)
    texts = {"HWS_UD_NAMESPACE": json.dumps(ns, indent=1), "HWSC_W2_END": json.dumps(w2, indent=1)}
    for k, rec in a["records"].items():
        rec["sha256"] = _sha(_w(mb / rec["path"], texts.get(k, f"{k} fixture\n")))
    approval = _w(mb / "archive" / "owner-approval-OF-fixture.md", "owner: approved (fixture)\n")
    frz = _w(out / "FREEZE_OF.json", '{"fixture": true}\n')
    _w(out / f"AUTH_OF_{job}.json", json.dumps({
        "schema": "hwsu-auth-v1", "stage": "OF", "job": job,
        "owner_approval": {"path": approval.relative_to(mb).as_posix(), "sha256": _sha(approval)},
        "freeze_of_sha256": _sha(frz), "written_by": "fixture", "written_utc": "2026-11-01T00:00:00Z"}))
    ur.write_reservation(out, "RES-HWSU-OF", "hwsu-of-v1", "2026-11-01T00:00:00Z", "fixture")
    ctx = {"out": out, "job": job, "attempt": 1, "reservation_id": "RES-HWSU-OF",
           "reservation_path": out / "RESERVATION_OF.json", "root": root, "mailbox": mb,
           "hwsc_store": hs, "scope": uc.SCOPE_OF, "seeds": dict(uc.SEEDS_OF), "dry": False,
           "rows_drawn": False, "results": {}}
    return c, ctx


def _g0(monkeypatch, c, ctx):
    monkeypatch.setattr(uc, "CONTRACT", c)
    try:
        d = us.g0_of(ctx["out"], ctx)
    except C1GateFailure as exc:
        return exc.status
    return (d or {}).get("status", "PASS")


def test_g0_of_pass_writes_record(tmp_path, monkeypatch):
    c, ctx = _g0_world(tmp_path)
    assert _g0(monkeypatch, c, ctx) == "PASS"
    rec = json.loads((ctx["out"] / "stages/OF/G0_OF.json").read_text(encoding="utf-8"))
    assert rec["status"] == "PASS" and rec["hits"]
    assert set(rec["checks"]) >= {"authority", "records", "namespace", "store", "attestation"}
    assert all(set(h) >= {"path", "needle", "line", "kind"} for h in rec["hits"])


AUTH_CASES = {
    "addendum_missing": lambda c, x: (x["mailbox"] / c["authority"]["addenda"][1]["path"]).unlink(),
    "addendum_byte": lambda c, x: _w(x["mailbox"] / c["authority"]["addenda"][3]["path"], "Addendum\n"),
    "freeze_record": lambda c, x: _w(x["mailbox"] / "records/HWSU_DESIGN_FREEZE.json", "{}"),
    "auth_missing": lambda c, x: (x["out"] / "AUTH_OF_0300.json").unlink(),
    "approval_changed": lambda c, x: _w(x["mailbox"] / "archive/owner-approval-OF-fixture.md", "no"),
    "freeze_of_changed": lambda c, x: _w(x["out"] / "FREEZE_OF.json", '{"fixture": 2}'),
    "rulings_add3": lambda c, x: _w(x["mailbox"] / c["authority"]["records"][
        "joint_rulings_addendum_3"]["path"], "changed\n"),
    "w2_bound_lock": lambda c, x: _w(x["root"] / "hwsc-store/RUN.lock", "job 0197\n"),
    "live_reservation": lambda c, x: _w(x["root"] / "x-store/RESERVATION_X.json",
                                        '{"id": "RES-X", "state": "ACTIVE"}'),
}


@pytest.mark.parametrize("case", sorted(AUTH_CASES))
def test_g0_of_authority_failures(tmp_path, monkeypatch, case):
    c, ctx = _g0_world(tmp_path)
    AUTH_CASES[case](c, ctx)
    assert _g0(monkeypatch, c, ctx) == "INCONCLUSIVE/AUTHORITY"
    if case != "live_reservation":  # authority and records come before the needle search
        assert not (ctx["out"] / "stages/OF/G0_OF.json").exists()


def test_g0_of_namespace_u_differs(tmp_path, monkeypatch):
    u = dict(copy.deepcopy(C["namespace"]["U"]), seed_blocks=[[640101, 640121], [649901, 649920]])
    c, ctx = _g0_world(tmp_path, u_track=u)
    assert _g0(monkeypatch, c, ctx) == "INCONCLUSIVE/AUTHORITY"


def test_g0_of_overlap_is_seed_scope(tmp_path, monkeypatch):
    d = copy.deepcopy(C["namespace"]["D_declared"])
    d["scopes"] = d["scopes"] + ["hwsu-v1"]
    c, ctx = _g0_world(tmp_path, d_track=d)
    assert _g0(monkeypatch, c, ctx) == "FAIL_TECHNICAL/SEED_SCOPE"


def test_g0_of_store_lineage(tmp_path, monkeypatch):
    c, ctx = _g0_world(tmp_path)
    _w(ctx["out"] / "stages/OF/ORACLE_x.npz", b"unrecorded")
    assert _g0(monkeypatch, c, ctx) == "FAIL_TECHNICAL/LINEAGE"


def test_g0_of_unclassified_hit(tmp_path, monkeypatch):
    c, ctx = _g0_world(tmp_path)
    _w(ctx["root"] / "topo-pilot/src/x.py", "seed = 640103\n")
    real = us.seed_search_u
    monkeypatch.setattr(us, "seed_search_u",
                        lambda root, nd, *a, **k: _rebase(real(root, nd, *a, **k), ctx["root"]))
    assert _g0(monkeypatch, c, ctx) == "FAIL_TECHNICAL/SEED_SCOPE"
    rec = json.loads((ctx["out"] / "stages/OF/G0_OF.json").read_text(encoding="utf-8"))
    assert rec["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    assert [h["path"] for h in rec["hits"] if h["kind"] == "unclassified"] == [
        FAKE + "topo-pilot/src/x.py"]
