"""HWSU E1 gates, share-family stubs and the validation report (API_U2.md section 4.1, 4.7, 4.9).

Response family only: SUP, F1, L1, R1-U and DX are NOT_RUN/SHARE_DROPPED (R-0223-1). The decision
side lives in hwsu_decide and the E2 gates in hwsu_e2 (split by size; reachable here by name).
Every gate takes ctx and returns a details dict (optionally with "status") or raises.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_decide as ud
import hwsu_known as uk
import hwsu_model as um
import hwsu_of as uof
import hwsu_oracle as uo
import hwsu_pairs as up
import hwsu_records as ur
import hwsu_registry as ureg
import u2  # noqa: F401
import importlib
import json
from fractions import Fraction
from pathlib import Path

import c1_means
import c2_decide
import hwsc_data
import hwsc_records
import k4b_data
import numpy as np
import stage_records
from c1_records import C1GateFailure

FAIL = C1GateFailure
SAMPLER, ORACLE, LIN = "FAIL_TECHNICAL/SAMPLER", "FAIL_TECHNICAL/ORACLE", "FAIL_TECHNICAL/LINEAGE"
AUTH, INC_REG = "INCONCLUSIVE/AUTHORITY", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
SPLIT = ("release_b_check", "sample_e2", "h2_fresh", "t_pre", "num_gate", "endpoint",
         "sealed_opened", "report_u")
OF_HIST = [f"stages/OF/HIST_OF_{k}_b{b}.npz" for k in ("fit", "eval_a1", "eval_a2")
           for b in uc.BLOCKS_OF]


def __getattr__(name):
    if name in SPLIT:
        return getattr(importlib.import_module("hwsu_e2"), name)
    return getattr(ud, name) if hasattr(ud, name) else _missing(name)


def _missing(name):
    raise AttributeError(f"module 'hwsu_gates' has no attribute {name!r}")


def share_dropped(ctx=None) -> dict:
    return {"status": "NOT_RUN/SHARE_DROPPED",
            "reason": "OF_PASS_RESPONSE_ONLY (S3; R-0223-1)"}


def share_family(*args, **kwargs):
    raise FAIL("FAIL_TECHNICAL/BINDING", "share family dropped at OF (S3; R-0223-1)")


share_arrays_u = haar_frames_u = share_family


def qsum_tol() -> Fraction:
    return Fraction(str(uc.read_json(uc.REPO / "tools" / "c2_readout" / "CONTRACT.json")[
        "tolerances"]["q_sum"]))


def _handoff(ctx) -> dict:
    return uc.load_handoff_u(ctx.get("handoff_path", uc.HANDOFF_PATH), ctx.get("handoff_sha256"))


def ensure_proc(ctx) -> dict:
    if ctx.get("proc") is None:
        uof.of_p(ctx)
    return ctx["proc"]


def register_new(out, stage, rel_dir) -> list:
    """STAGE_COMPLETE for every file of rel_dir not yet recorded (registry files, J10 lineage)."""
    out = Path(out)
    done = set()
    for e in stage_records.stages_so_far(out):
        if e.get("event") == "STAGE_COMPLETE":
            done |= set(e.get("files", {}))
    files = sorted(p.relative_to(out).as_posix() for p in (out / rel_dir).rglob("*")
                   if p.is_file())
    new = [f for f in files if f not in done]
    ur.complete_stage(out, stage, new)
    return new


# ------------------------------------------------------------------------ G0U, H1-U, REG1
def g0u_e1(out, ctx) -> dict:
    r = uk.g0_u(out, ctx, "E1")
    try:
        rel = uc.read_json(Path(out) / "RELEASE_A.json")
        ok = rel.get("reservation_id") == ctx.get("reservation_id") and rel.get(
            "freeze_sha256") == stage_records.sha256(Path(out) / "FREEZE.json")
    except (OSError, ValueError, C1GateFailure):
        ok = False
    if not ok:
        raise FAIL(AUTH, "RELEASE_A.json absent or differs")
    return r


def h1_u(out, ctx) -> dict:
    C, store = uc.CONTRACT["stage_c_u2"], Path(ctx["hwsc_store"])
    ident = um.identity_c(store, _handoff(ctx))
    charts = um.charts_identity(store)
    models = um.load_stage_c(store, ident)
    proc = uof.of_p(ctx)
    lin = hwsc_records.lineage_c(store)
    if lin["status"] != "PASS":
        raise FAIL(um.IDENT, f"hwsc lineage {lin}")
    for rel, want in (("FREEZE.json", C["freeze_sha256"]),
                      ("STAGES.jsonl", C["stages_jsonl"]["sha256_2026_11_03"])):
        if uc.sha256_file(store / rel) != want:
            raise FAIL(um.IDENT, f"{rel} differs from CONTRACT")
    rp = C["result_presence"]
    if um.stage_complete_sha(store, rp["stage"], rp["relpath"]) != rp["sha256"]:
        raise FAIL(um.IDENT, "S8 RESULT.json presence/hash differs")
    ctx.update(models=models, ident=ident, perm_of={j: ctx["proc"]["perm"][j] for j in models})
    um.write_json(Path(out) / "stages" / "E1" / "H1U.json", {
        "ids": ident["ids"], "meta": ident["meta"], "charts": charts, "threads": 1,
        "state_sha": {j: m["state_sha"] for j, m in models.items()}, "process": proc})
    return {"ids": ident["ids"], "state_sha": {j: m["state_sha"] for j, m in models.items()}}


def reg1(out, ctx) -> dict:
    out = Path(out)
    hd = json.loads(uc.read_bytes(ctx.get("handoff_path", uc.HANDOFF_PATH)).decode("utf-8"))
    man = ureg.build_u("K-REG1", out / "registry", root=ctx["root"],
                       scratch=ctx.get("scratch", uc.SCRATCH), handoff=hd, own=OF_HIST)
    if man["status"] != "PASS":
        raise FAIL(man["status"], f"K-REG1 {man['problems'][:5]}")
    try:
        cert = uc.read_json(out / "RELEASE_A.json")["completeness_certificate"]
        want = cert["rehearsal_manifest_sha256"]
        got = stage_records.sha256(out / "registry" / "rehearsal" / "REHEARSAL.json")
    except (OSError, KeyError, ValueError, C1GateFailure):
        want, got = None, 0
    if want != got:
        raise FAIL(AUTH, "release A certificate does not bind the rehearsal manifest")
    register_new(out, "E1_REG1", "registry")
    ctx["kreg1"] = ureg.load_registry_sets(out / "registry", "K-REG1")[:2]
    ctx["kreg1_manifest_sha256"] = stage_records.sha256(out / "registry" / "K-REG1.json")
    return {"n_digests": man["n_digests"], "manifest_sha256": stage_records.sha256(
        out / "registry" / "K-REG1.json"), "superset_diagnostic": man["superset_diagnostic"]}


# ------------------------------------------------------------------------- S3, H2-U, H3-U
def _table_files(out, dry, order) -> list:
    files = []
    for split, arm, b, canon, ids in order:
        label = "of-fit" if split == "fit" else f"of-eval-{arm}"
        rel = f"stages/E1/{'DRYHIST' if dry else 'HIST'}_{split}_{arm}_b{b}.npz"
        ur.save_array(out, rel, dry=dry, **up.table_arrays(up.history_table(canon, ids, label, b)))
        files.append(rel)
    return files


def sample_e1(out, ctx) -> dict:
    p, dry, n = ensure_proc(ctx), bool(ctx.get("dry")), int(ctx.get("block_n", uc.BLOCK_OF))
    T, E, pi, scope = p["T"], p["E_canon_shared"], p["pi"], ctx["scope"]
    ur.begin_stage(out, "E1_S3")
    ctx["rows_drawn"] = True
    try:
        fit = {b: up.sample_singles(T, E, pi, scope, "fit", b, n) for b in uc.BLOCKS_OF}
        val = up.sample_pairs(T, E, pi, scope, "val", 0, n)
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise FAIL(SAMPLER, f"sampling: {exc!r}") from exc
    order = [("fit", "s", b, fit[b]["canon32"], fit[b]["ids"]) for b in uc.BLOCKS_OF]
    order += [("val", "a1", 0, val["a1"], val["ids_a1"]), ("val", "a2", 0, val["a2"],
                                                           val["ids_a2"])]
    files = _table_files(out, dry, order)
    ur.complete_stage(out, "E1_S3", files)
    canon = np.concatenate([fit[b]["canon32"] for b in uc.BLOCKS_OF])
    ids = np.concatenate([fit[b]["ids"] for b in uc.BLOCKS_OF])
    o = np.argsort(ids, kind="stable")
    ctx["fit"] = {"canon32": canon[o], "ids": ids[o]}
    ctx["val"] = {k: val[k] for k in ("a1", "a2", "ids_a1", "ids_a2")}
    return {"files": files, "n_fit": len(ids), "n_pairs": len(val["a1"])}


def h2_check(ctx, tables, kreg, rows) -> dict:
    """Separation from the registry, sealed-D-2a predicate, registry risk (H2-U, H2-FRESH-U)."""
    sep = ureg.separation_u(kreg[0], tables, kreg[1])
    if not sep["ok"]:
        raise FAIL(LIN, f"separation: {sep['collisions']} {sep['seq_overlap']}")
    stack = np.vstack([t["canon32"] for t in tables.values()])
    pc = k4b_data.predicate_check(stack, ("sealed_d2a",))
    if pc["status"] != "PASS":
        return {"status": INC_REG, "predicate": pc}
    h = hwsc_data.p_d2a_check(ctx["proc"], _handoff(ctx)["p_D2a"])
    risk = ur.registry_risk_u(h["p_D2a"], rows)
    if not (h["ok"] and risk["ok"]):
        raise FAIL(LIN, f"p_D2a / registry risk {risk}")
    return {"separation": sep, "predicate": pc, "p_d2a": h, "registry_risk": risk}


def h2_u(ctx) -> dict:
    f, v = ctx["fit"], ctx["val"]
    tables = {"fit": {"canon32": f["canon32"], "seq_ids": f["ids"]},
              "val_a1": {"canon32": v["a1"], "seq_ids": v["ids_a1"]},
              "val_a2": {"canon32": v["a2"], "seq_ids": v["ids_a2"]}}
    ctx["h2"] = h2_check(ctx, tables, ctx["kreg1"], 24576 + 32768 + 8192 * 8)
    return ctx["h2"]


def h3_split(ctx, a1, a2, label) -> dict:
    """OF-1 (i)-(v) on one pair split plus the sum of q (H3-U, T-PRE)."""
    p = ctx["proc"]
    T, E, pi, co = p["T"], p["E_canon_shared"], p["pi"], p["coords"]
    o1, o2 = (uo.arm_oracle(T, E, pi, x, co) for x in (a1, a2))
    s1, s2 = uo.suffix_oracle(T, E, pi, [a1, a2], co)
    pc = uo.pair_core(o1, o2)
    if not up.suffix_equal(a1, a2).all():
        raise FAIL(SAMPLER, f"{label}: arm suffixes differ")
    m4c = uo.m4_check(T, E, pi, a1, co, s1["m4"])
    if not (np.array_equal(s1["q4bar"], s2["q4bar"]) and np.array_equal(s1["m4"], s2["m4"])
            and m4c["ok"]):
        raise FAIL(SAMPLER, f"{label}: q4/m4 differ or m4 check {m4c}")
    if not all(np.all(np.isfinite(o["le"])) for o in (o1, o2)):
        raise FAIL(SAMPLER, f"{label}: non-finite log evidence")
    N = uo.helmert(36)
    A_KO = {k: uo.readout_A(pc["d"], uo.ko_logits(o1, s1, k), uo.ko_logits(o2, s2, k), N)
            for k in uo.CASES}
    ids = uo.ko_identities(pc["G"], A_KO)
    if not all(v["ok"] for v in ids.values()):
        raise FAIL(ORACLE, f"{label}: KO identities {ids}")
    dec = uo.decimal_rows(T, E, pi, a1, a2, o1, o2, s1, pc, k=ctx.get("decimal_rows", 4))
    tol = qsum_tol()
    qs = max(float(np.max(np.abs(o["qbar"].sum(axis=1) - 1.0))) for o in (o1, o2))
    if not dec["ok"] or Fraction(qs) > tol:
        raise FAIL(ORACLE, f"{label}: Decimal rows {dec['ok']} / sum q {qs}")
    return {"o1": o1, "o2": o2, "s1": s1, "s2": s2, "pc": pc, "A_KO": A_KO, "ko_identities": ids,
            "decimal": dec, "qsum": qs, "m4_check": m4c}


def h3_u(ctx) -> dict:
    p, v, f = ctx["proc"], ctx["val"], ctx["fit"]
    r = h3_split(ctx, v["a1"], v["a2"], "val")
    of = uo.arm_oracle(p["T"], p["E_canon_shared"], p["pi"], f["canon32"], p["coords"])
    if not np.all(np.isfinite(of["le"])) or Fraction(float(np.max(np.abs(
            of["qbar"].sum(axis=1) - 1.0)))) > qsum_tol():
        raise FAIL(SAMPLER, "fit: non-finite log evidence or sum q")
    ctx.update(h3=r, pc=r["pc"], o1=r["o1"], o2=r["o2"], s1=r["s1"], s2=r["s2"], A_KO=r["A_KO"])
    out = Path(ctx["out"])
    ur.save_array(out, "stages/E1/ORACLE_E1_val.npz", dry=bool(ctx.get("dry")), G=r["pc"]["G"],
                  d=r["pc"]["d"], le_a1=r["o1"]["le"], le_a2=r["o2"]["le"])
    ur.save_array(out, "stages/E1/ORACLE_E1_fit.npz", dry=bool(ctx.get("dry")), le=of["le"])
    return {"qsum": r["qsum"], "m4_check": r["m4_check"], "ko_identities": r["ko_identities"],
            "decimal_ok": r["decimal"]["ok"]}


def h5_bounds(G, seed, alpha) -> dict:
    b = c2_decide.stream_bounds({"G": G}, seed, float(alpha), uc.DRAWS)["G"]
    if b["rank_L"] != 250:
        raise FAIL("FAIL_TECHNICAL/NUMERICAL", "H5-U rank_L != 250")
    return b


def h5_u(ctx) -> dict:
    b = h5_bounds(ctx["pc"]["G"], ctx["seeds"]["h5_val"], uc.ALPHA_HEADROOM)
    ok_a = Fraction(float(b["L"])) > Fraction(1, 100)
    A = uc.CONTRACT["authority_u2"]["of_accept"]
    rp = Path(ctx["out"]) / "stages" / "OF" / "OF_REPORT.json"
    ok_b = (uc.sha256_file(rp) == A["of_report_sha256"]
            and Fraction(float(uc.read_json(rp)["EG"]["L"])) > uc.HEADROOM)
    ctx.setdefault("boot", {})["headroom_G"] = c1_means.bootstrap_means(
        {"G": ctx["pc"]["G"]}, ctx["seeds"]["h5_val"], uc.DRAWS)["G"]
    out = {"EG": {"mean": b["mean"], "L": b["L"], "rank_L": b["rank_L"]}, "val_L_gt_1_100": ok_a,
           "of_L_gt_1_50": ok_b}
    if not (ok_a and ok_b):
        out["status"] = "INCONCLUSIVE/HEADROOM"
    return out


# ----------------------------------------------------------------- BASIS, M0, X1, KC-U, P1
def basis_step(ctx) -> dict:
    r = um.basis_gate(ctx["models"], ctx["fit"]["canon32"], ctx["perm_of"], ctx["policy"])
    ctx["basis_of"] = {j: um.basis_u(m["model64"]) for j, m in ctx["models"].items()}
    ctx["basis_ok"] = True
    return r


def m0_step(ctx) -> dict:
    r = um.m0_gate(ctx["models"], ctx["ident"], ctx["val"]["a1"], ctx["perm_of"],
                   ctx["pc"]["d"], ctx["policy"])
    return {j: {"status": v["status"], "checks": v["checks"]} for j, v in r.items()}


def x1_step(ctx) -> dict:
    return um.x1_gate(ctx["models"], ctx["val"], ctx["perm_of"], ctx["basis_of"], ctx["policy"])


def kc_u(ctx) -> dict:
    G = ctx["pc"]["G"]
    ids = uo.ko_identities(G, ctx["A_KO"])
    cats = uo.ko_categories(G, ctx["A_KO"], ctx["seeds"]["kc_val"],
                            draws=int(ctx.get("draws", uc.DRAWS)))
    if not (all(v["ok"] for v in ids.values()) and cats["ok"]):
        raise FAIL("FAIL_TECHNICAL/KNOWN_CASE", f"KC-U {ids} {cats}")
    return {"ko_identities": {k: v["ok"] for k, v in ids.items()},
            "ko_categories": {k: cats[k]["category"] for k in uo.CASES}}


def model_A(ctx, a1, a2, d_canon) -> tuple:
    """A_full per model from the readout coordinates (closed form; no logit)."""
    A, rows = {}, {}
    for j, m in ctx["models"].items():
        b, perm = ctx["basis_of"][j], ctx["perm_of"][j]
        y1 = um.readout_y(m["model64"], a1, perm, b)
        y2 = um.readout_y(m["model64"], a2, perm, b)
        A[j] = um.a_full(um.named_d(d_canon, perm), b["M"], y1, y2)
        rows[j] = (y1, y2)
    return A, rows


def p1_step(out, ctx) -> dict:
    out, dry = Path(out), bool(ctx.get("dry"))
    ctx["policy"].begin("P1")
    G, v = ctx["pc"]["G"], ctx["val"]
    A, _ = model_A(ctx, v["a1"], v["a2"], ctx["pc"]["d"])
    ctx["policy"].end("P1")
    p = ud.p1_u(A, G, list(ctx["models"]), ctx["seeds"])
    ctx["P1"] = {k: p[k] for k in p if k != "prec"}
    arrays = {"G": G}
    pair = {}
    for j in A:
        ra = um.response_arrays(A[j], G)
        pair.update({f"A_{j}": A[j], f"ZR010_{j}": ra["ZR010"], f"ZR030_{j}": ra["ZR030"]})
    arrays.update(pair)
    ctx["sealed_sha256"] = ud.write_sealed_u(out, arrays)
    ur.save_array(out, "stages/E1/PAIR_E1_val.npz", dry=dry, **pair)
    ur.save_array(out, "stages/E1/PREC_E1.npz", dry=dry, **p["prec"])
    ur.save_array(out, "stages/E1/BOOT_E1.npz", dry=dry, **ctx.get("boot", {}))
    if p["N_RESP"] is None:
        raise FAIL("INCONCLUSIVE/UNDERPOWERED", "no ladder N powers two models on both arrays")
    return {"N_RESP": p["N_RESP"], "N": p["N"], "k": p["k"],
            "precision_limited": p["precision_limited"]}


def validation_report(out, ctx, records) -> Path:
    P = ctx.get("P1", {})
    mde = {X: {N: P["passes"][X]["summary"][N] for N in P["passes"][X]["summary"]}
           for X in P.get("passes", {})}
    rec = {"schema": "hwsu-validation-v1", "gates": {r["gate"]: r["status"] for r in records},
           "G": {"mean": float(c1_means.tree_mean(ctx["pc"]["G"])) if "pc" in ctx else None},
           "ko": {"identities": "PASS" if "pc" in ctx else None, "categories": "PASS" if ctx.get(
               "A_KO") else None},
           "p1": {"N_RESP": P.get("N_RESP"), "N": P.get("N"), "k": P.get("k"), "mde": mde,
                  "precision_limited": P.get("precision_limited")},
           "basis": ctx.get("basis_ok"), "h2": ctx.get("h2"),
           "registry": {"K-REG1": ctx.get("kreg1_manifest_sha256")},
           "sealed_sha256": ctx.get("sealed_sha256"), "share": "NOT_RUN/SHARE_DROPPED",
           "written_utc": ur.utc()}
    ud.check_unsealed_u(rec)
    return um.write_json(Path(out) / "stages" / "E1" / "VALIDATION_REPORT.json", rec)

