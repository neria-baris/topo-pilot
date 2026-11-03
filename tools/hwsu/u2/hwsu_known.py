"""HWSU binding, freeze, S0, authority, attestation, G0U and the known cases KC0-KC6
(API_U2.md section 2; protocol 4.1, 6 rows KC and 0). Response family only: the KU
constructions are not implemented (R-0223-1) and fail closed.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_bind_u2 as bu2
import hwsu_dry as udry
import hwsu_freeze as ufz
import hwsu_model as um
import hwsu_of as uof
import hwsu_oracle as uo
import hwsu_records as ur
import hwsu_registry as ureg
import hwsu_seed as us
import u2  # noqa: F401
import fnmatch
import importlib
import json
import os
import platform
import sys
from pathlib import Path

import c1_means
import numpy as np
import stage_records
from c1_records import C1GateFailure

AUTH, KNOWN, FREEZE = "INCONCLUSIVE/AUTHORITY", "FAIL_TECHNICAL/KNOWN_CASE", "FAIL_TECHNICAL/FREEZE"
SHARE_OUTCOME = "INCONCLUSIVE/ORACLE_FEASIBILITY"
TEST_PATTERNS = ("tests/hwsu/test_a_u2_*.py", "tests/hwsu/test_b_u2_*.py",
                 "tests/hwsu/AUTHORSHIP_A_U2.md", "tests/hwsu/AUTHORSHIP_B_U2.md")


def _C(contract=None) -> dict:
    return uc.CONTRACT if contract is None else contract

# --------------------------------------------------------------------- OF binding (R-0206-1)
def of_binding(store=uc.STORE, contract=None) -> dict:
    A = _C(contract)["authority_u2"]
    ac, store = A["of_accept"], Path(store)
    try:
        raw = uc.read_bytes(store / "OF_ACCEPT.json")
        sha = ur._sha(raw)
        full = json.loads(raw.decode("utf-8-sig"))
        acc = {k: full[k] for k in ac["keys_read"]}
        fz = uc.sha256_file(store / "FREEZE_OF.json")
        bad = [n for n, ok in (
            ("OF_ACCEPT sha256", sha == ac["sha256"]), ("verdict", acc["verdict"] == "ACCEPT"),
            ("outcome", acc["outcome"] == ac["outcome"] == "OF_PASS_RESPONSE_ONLY"),
            ("N_resp", acc["N_resp"] == ac["N_resp"] == 4096),
            ("freeze_of_sha256", acc["freeze_of_sha256"] == fz == ac["freeze_of_sha256"]
             == A["freeze_of"]["sha256"])) if not ok]
    except (OSError, ValueError, KeyError, TypeError, C1GateFailure) as exc:
        raise C1GateFailure(AUTH, f"OF binding: {exc!r}"[:300]) from exc
    if bad:
        raise C1GateFailure(AUTH, f"OF binding differs: {bad}")
    return {"status": "PASS", "outcome": acc["outcome"], "share_outcome": SHARE_OUTCOME,
            "freeze_of_sha256": fz, "of_accept_sha256": sha}


# ------------------------------------------------------------------ freeze, S0 (protocol 4.1)
def _tables(contract=None) -> dict:
    C = _C(contract)
    return dict(C["reuse_sha256"], **C["reuse_sha256_u2"])


def implementation_files_u(repo, h_exec, contract=None) -> dict:
    C = _C(contract)
    names = ufz._git(repo, "ls-tree", "-r", "--name-only", h_exec).decode().splitlines()
    tests = sorted(n for n in names if any(fnmatch.fnmatchcase(n, p) for p in TEST_PATTERNS))
    blobs = ufz._blobs(repo, h_exec, list(C["phase2_files"]) + tests)
    return {p: ur._sha(b) for p, b in blobs.items()}


def freeze_u(store, repo, h_exec, dru_report, j_u_records, written_by) -> dict:
    C = uc.CONTRACT
    ufz.verify_freeze_of(store, repo)
    ob = of_binding(store)
    files = implementation_files_u(repo, h_exec)
    impl = ur._canon_sha(files)
    reuse = {p: ur._sha(b) for p, b in ufz._blobs(repo, h_exec, _tables()).items()}
    bad = [p for p, h in reuse.items() if _tables()[p] != h]
    if bad:
        raise C1GateFailure(FREEZE, f"reuse files differ at h_exec: {bad[:10]}")
    rep = json.loads(Path(dru_report).read_text(encoding="utf-8"))
    if rep.get("implementation_sha256") != impl or rep.get("all_pass") is not True:
        raise C1GateFailure(FREEZE, "dry report implementation_sha256 differs or not all_pass")
    ju = []
    for r in j_u_records:
        path, want = (r["path"], r.get("sha256")) if isinstance(r, dict) else (r, None)
        h = stage_records.sha256(path)
        if want is not None and want != h:
            raise C1GateFailure(FREEZE, f"J-U record differs: {path}")
        ju.append({"path": str(path), "sha256": h})
    def blob(n):
        return ufz._blob(repo, h_exec, f"tools/hwsu/{n}")

    rec = {"protocol": C["protocol"], "protocol_sha256": ur._sha(blob("PROTOCOL_HWSU_v1.md")),
           "contract_of_sha256": ur._sha(blob("CONTRACT_OF.json")),
           "contract_sha256": ur._sha(blob("CONTRACT.json")),
           "api_u2_sha256": ur._sha(blob("API_U2.md")),
           "test_plan_u2_sha256": ur._sha(blob("TEST_PLAN_U2.md")),
           "freeze_of_sha256": ob["freeze_of_sha256"], "of_accept_sha256": ob["of_accept_sha256"],
           "h_exec": h_exec, "r_ref": C["s0_u2"]["r_ref"], "implementation_files": files,
           "implementation_sha256": impl, "reuse_sha256": reuse,
           "dry_run_report_path": str(dru_report),
           "dry_run_report_sha256": stage_records.sha256(dru_report), "j_u_records": ju,
           "environment": {"python": sys.version, "numpy": np.__version__,
                           "platform": platform.platform()},
           "written_by": written_by, "created_utc": ur.utc()}
    stage_records.write_new(Path(store) / "FREEZE.json", rec)
    return rec


def verify_freeze_u(store, repo) -> dict:
    f, repo = Path(store) / "FREEZE.json", Path(repo)
    if not f.is_file():
        raise C1GateFailure("INVALID", "FREEZE.json absent")
    ufz.verify_freeze_of(store, repo)
    frz = json.loads(f.read_text(encoding="utf-8"))
    bad = [p for p, h in frz["implementation_files"].items()
           if not (repo / p).is_file() or ur._sha((repo / p).read_bytes()) != h]
    for p, h in _tables().items():
        if frz["reuse_sha256"].get(p) != h or not (repo / p).is_file() or ur._sha(
                (repo / p).read_bytes()) != h:
            bad.append(p)
    if bad:
        raise C1GateFailure("INVALID", f"FREEZE mismatch: {bad[:10]}")
    return {"status": "PASS", "freeze": frz, "freeze_sha256": stage_records.sha256(f)}


def _allowed_s0(status, path, contract=None) -> bool:
    idx = path.startswith("docs/code_index/")
    return idx if status == "M" else status == "A" and (idx or path in _C(contract)[
        "phase2_files"] or any(fnmatch.fnmatchcase(path, p) for p in TEST_PATTERNS))


def s0_u(store, repo, r_ref=None) -> dict:
    C = uc.CONTRACT
    frz = verify_freeze_u(store, repo)["freeze"]
    r_ref = C["s0_u2"]["r_ref"] if r_ref is None else r_ref
    h = frz["h_exec"]
    diff = ufz._git(repo, "diff", "--no-renames", "--name-status", r_ref, h).decode().splitlines()
    bad = [ln for ln in diff if ln.strip() and not _allowed_s0(*[
        x.strip() for x in ln.split("\t", 1)])]
    if bad:
        raise C1GateFailure("INVALID", f"diff outside the allowlist: {bad[:10]}")
    try:
        at_h, at_r = (ufz._blobs(repo, ref, _tables()) for ref in (h, r_ref))
    except C1GateFailure as exc:
        raise C1GateFailure("INVALID", exc.reason) from exc
    for p, want in _tables().items():
        if ur._sha(at_h[p]) != want or ur._sha(at_r[p]) != want:
            raise C1GateFailure("INVALID", f"reuse hash differs: {p}")
    audit = bu2.audit_u2()
    if audit["status"] != "PASS":
        raise C1GateFailure("INVALID", "binding audit failed")
    return {"status": "PASS", "h_exec": h, "diff": diff, "audit": {"status": "PASS"}}


# --------------------------------------------------------------- authority, attestation
def auth_u(store, job, stage, mailbox=uc.MAILBOX, contract=None) -> dict:
    ap_want = _C(contract)["authority_u2"]["run_approval"]
    try:
        rec = json.loads((Path(store) / f"AUTH_U_{job}.json").read_text(encoding="utf-8"))
        ap = rec["owner_approval"]
        ok = (rec["stage"] == stage and ap["path"] == ap_want["path"]
              and ap["sha256"] == ap_want["sha256"]
              and uc.sha256_file(Path(mailbox) / ap["path"]) == ap["sha256"]
              and rec["freeze_sha256"] == stage_records.sha256(Path(store) / "FREEZE.json"))
    except (OSError, ValueError, KeyError, TypeError, C1GateFailure):
        ok = False
    if not ok:
        raise C1GateFailure(AUTH, f"AUTH_U_{job} record differs or is absent")
    return {"stage": stage, "job": job}


def end_obligation_path(end_rec, end_path, root):
    """R-0213-1: first existing of <store>/<rel> and <root>/<rel>, bounded to that store."""
    store = Path(end_path).parent.parent
    try:
        rel = end_rec["obligation_file"]
        inside = store.resolve()
    except (KeyError, TypeError, OSError):
        return None
    for cand in (store / rel, Path(root) / rel):
        try:
            if cand.exists():
                cand.resolve().relative_to(inside)
                return cand
        except (ValueError, OSError):
            continue
    return None


def _ended_u2(rec, f, root, w2_end, w2_sha):
    rid, sha = rec.get("id"), stage_records.sha256(f)
    if rid == "RES-HWSC-W2":
        try:
            if uc.sha256_file(w2_end) == w2_sha and uc.read_json(w2_end).get(
                    "reservation_file_sha256") == sha:
                return "a"
        except (OSError, ValueError, C1GateFailure):
            pass
    store = f.parent.parent if f.parent.name == "reservations" else f.parent
    e = store / "reservations" / f"{rid}.END.json"
    try:
        r = uc.read_json(e, root)
        ob = end_obligation_path(r, e, root)
        if (ob is not None and r.get("schema") == "hws-reservation-end-v1"
                and r.get("reservation_sha256") == sha
                and r.get("obligation_sha256") == uc.sha256_file(ob, root)):
            return "b"
    except (OSError, ValueError, KeyError, C1GateFailure):
        pass
    return None


def w2_attestation_u2(root, own=None, w2_end=None, w2_end_sha256=None) -> dict:
    root = Path(root)
    w2_end = uc.MAILBOX / "records" / "HWSC_W2_END.json" if w2_end is None else w2_end
    w2_sha = (uc.CONTRACT["authority"]["records"]["HWSC_W2_END"]["sha256"]
              if w2_end_sha256 is None else w2_end_sha256)
    files = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        files += sorted(d.glob("RESERVATION*.json")) + sorted((d / "reservations").glob("*.json"))
    active, ended, live = [], {}, []
    for f in files:
        if f.name.endswith(".END.json") or uc.blinded(f, root):
            continue
        try:
            rec = uc.read_json(f, root)
        except (OSError, ValueError):
            live.append(str(f))
            continue
        if not isinstance(rec, dict) or rec.get("state") != "ACTIVE" or (
                own is not None and rec.get("id") == own):
            continue
        rid = rec.get("id", str(f))
        active.append(rid)
        how = _ended_u2(rec, f, root, w2_end, w2_sha)
        if how:
            ended[rid] = how
        else:
            live.append(rid)
    return {"status": "PASS" if not live else AUTH, "active": active, "ended": ended,
            "live": live}


# -------------------------------------------------------------------------- G0U, KC0-KC6
def g0_u(out, ctx, stage) -> dict:
    C = ctx.get("contract") or uc.CONTRACT
    A, A2, checks = C["authority"], C["authority_u2"], {}
    mb, root = Path(ctx["mailbox"]), ctx["root"]
    bad = [f"addendum {a['addendum']}" for a in list(A["addenda"]) + list(A2["addenda"].values())
           if not us._sha_ok(mb / a["path"], a["sha256"], root)]
    d = A["design"]
    bad += [n for n, p, h in (("design", mb / d["path"], d["sha256"]),
                              ("protocol copy", uc.PROTOCOL_PATH, d["sha256"]),
                              ("design freeze", mb / d["freeze_record"]["path"],
                               d["freeze_record"]["sha256"])) if not us._sha_ok(p, h, root)]
    if bad:
        raise C1GateFailure(AUTH, f"authority: {bad}")
    auth_u(out, ctx["job"], stage, mb, C)
    checks.update(authority=True, of_binding=of_binding(out, C)["status"] == "PASS")
    us._records(ctx, checks)
    ns = uc.read_json(mb / A["records"]["HWS_UD_NAMESPACE"]["path"], root)["tracks"]
    if ns["U"] != C["namespace"]["U"]:
        raise C1GateFailure(AUTH, "namespace record tracks.U differs from CONTRACT")
    over = us.namespace_overlap(ns["U"], ns["D"])
    checks["namespace"] = not over
    if over:
        raise C1GateFailure("FAIL_TECHNICAL/SEED_SCOPE", f"namespace overlap: {over[:5]}")
    checks["store"] = ur.lineage_u(out)["status"] == "PASS"
    w2 = w2_attestation_u2(root, own=ctx.get("reservation_id"), w2_end=mb / "records" /
                           "HWSC_W2_END.json",
                           w2_end_sha256=A["records"]["HWSC_W2_END"]["sha256"])
    checks["attestation"] = w2["status"] == "PASS"
    if not checks["attestation"]:
        raise C1GateFailure(AUTH, f"live reservations: {w2['live']}")
    c = us.classify_hits_u(us.seed_search_u(root, us.needles(C)), C["g0"]["declaration_fragments"],
                           C["g0"]["job_scratch"])
    f = Path(out) / "stages" / stage / "G0U.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, {"hits": c["hits"], "status": c["status"], "checks": checks})
    if c["status"] != "PASS":
        raise C1GateFailure("FAIL_TECHNICAL/SEED_SCOPE", f"unclassified needle hits: {c['status']}")
    return {"status": "PASS", "n_hits": len(c["hits"]), "checks": checks}


def kc0(out, ctx) -> dict:
    return g0_u(out, ctx, "KC")


def kc1(ctx) -> dict:
    return uof.of_p(ctx)


def kc2(ctx) -> dict:
    ident = um.identity_c(ctx["hwsc_store"], uc.load_handoff_u())
    ch = um.charts_identity(ctx["hwsc_store"])
    return {"ids": ident["ids"], "charts": ch["charts"], "no_checkpoint_loaded": True}


def _need_pass(name, r) -> None:
    if r.get("status") != "PASS":
        raise C1GateFailure(KNOWN, f"{name}: {r.get('status')} {r.get('details', '')}"[:600])
def kc3(ctx) -> dict:
    base = uc.SCRATCH / f"test_hwsu-{ctx['job']}" / "kc3"
    d2 = importlib.import_module("hwsu_dry2")
    res = {}
    for name, fn in (("KS-PAIR", udry.dro2), ("KS-P", d2.ks_p), ("KS-RULES", d2.ks_rules)):
        sub = base / name
        sub.mkdir(parents=True, exist_ok=True)
        res[name] = fn(sub)
        _need_pass(name, res[name])
    return {"cases": {k: v.get("status") for k, v in res.items()}}


def kc4(ctx=None) -> dict:
    a = bu2.audit_u2()
    if a["status"] != "PASS":
        raise C1GateFailure(KNOWN, f"audit_u2: {a['status']}")
    return {"audit": a["status"], "by_path": a["by_path"]}


def _bytes(root) -> int:
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(root) for f in fs)


def kc5(out, ctx) -> dict:
    out = Path(out)
    reh = out / "registry" / "rehearsal"
    hd = json.loads(uc.read_bytes(ctx.get("handoff_path", uc.HANDOFF_PATH)).decode("utf-8"))
    man = ureg.build_u("REHEARSAL", reh, root=ctx["root"], scratch=ctx.get("scratch", uc.SCRATCH),
                       handoff=hd, own=None)
    now, reg_b = _bytes(out), _bytes(reh)
    hist = [p.stat().st_size for p in out.rglob("HIST_*.npz")]
    per_row = (sum(hist) / 24576.0) if hist else 320.0
    size_end = now + 2 * reg_b + per_row * (57344 + 8192 * 8)
    cap = uc.CONTRACT["resources"]["output_cap_bytes"]
    rec = {"rehearsal_status": man["status"], "cpu_s": man.get("cpu_s"),
           "peak_memory_bytes": man.get("peak_memory_bytes"), "store_bytes": now,
           "rehearsal_bytes": reg_b, "projection": {"size_end": size_end, "cap_half": cap / 2},
           "manifest_sha256": stage_records.sha256(reh / "REHEARSAL.json")}
    ctx["kc5"] = rec
    if man["status"] != "PASS":
        raise C1GateFailure(man["status"], f"rehearsal registry {man['problems'][:5]}")
    if size_end > cap / 2:
        raise C1GateFailure("INCONCLUSIVE/RESOURCE_OR_AUTHORITY", f"projected size {size_end}")
    return rec


def kc6(out, ctx) -> dict:
    out = Path(out)
    A = uc.CONTRACT["authority_u2"]["of_accept"]
    rp = out / "stages" / "OF" / "OF_REPORT.json"
    if uc.sha256_file(rp) != A["of_report_sha256"]:
        raise C1GateFailure(KNOWN, "OF_REPORT.json does not re-hash")
    p, arms = ctx["proc"], {}
    for arm in ("a1", "a2"):
        parts = []
        for b in uc.BLOCKS_OF:
            rel = f"stages/OF/HIST_OF_eval_{arm}_b{b}.npz"
            if stage_records.sha256(out / rel) != um.stage_complete_sha(out, "OF_S", rel):
                raise C1GateFailure(KNOWN, f"{rel} differs from the OF STAGE_COMPLETE")
            with np.load(out / rel, allow_pickle=False) as z:
                parts.append(np.asarray(z["canon32"]))
        arms[arm] = uo.arm_oracle(p["T"], p["E_canon_shared"], p["pi"], np.concatenate(parts),
                                  p["coords"])
    G = uo.pair_core(arms["a1"], arms["a2"])["G"]
    got, want = repr(float(c1_means.tree_mean(G))), repr(float(uc.read_json(rp)["EG"]["point"]))
    if got != want:
        raise C1GateFailure(KNOWN, f"OF reproduction: E[G] {got} != {want}")
    return {"EG_point": got}


def kc_report(out, records) -> Path:
    rec = next((r for r in records if r.get("gate") == "KC5"), {})
    f = Path(out) / "stages" / "KC" / "KC_REPORT.json"
    body = {"schema": "hwsu-kc-report-v1", "gates": {r["gate"]: r["status"] for r in records},
            "rehearsal": {k: rec.get(k) for k in ("rehearsal_status", "cpu_s",
                                                   "peak_memory_bytes", "manifest_sha256")},
            "store_bytes": rec.get("store_bytes"), "projection": rec.get("projection"),
            "written_utc": ur.utc()}
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, json.loads(json.dumps(body, default=str)))
    return f


def ku_cases(*args, **kwargs):
    raise C1GateFailure("FAIL_TECHNICAL/BINDING", "share family dropped at OF (S3; R-0223-1)")


