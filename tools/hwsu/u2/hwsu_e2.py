"""HWSU E2 gates: RELEASE-B, S7, H2-FRESH-U, T-PRE, NUM, ENDPOINT, SEALED_OPENED and the report
(API_U2.md sections 4.3-4.8). Split from hwsu_gates by size (API erratum); every name stays
reachable as hwsu_gates.<name>. Response family only.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_decide as ud
import hwsu_gates as ug
import hwsu_known as uk
import hwsu_oracle as uo
import hwsu_model as um
import hwsu_pairs as up
import hwsu_records as ur
import hwsu_registry as ureg
import u2  # noqa: F401
import json
from fractions import Fraction
from pathlib import Path

import c1_means
import c1_oracle
import c2_decide
import c2_model
import hwsc_records
import numpy as np
import stage_records
from c1_records import C1GateFailure

FAIL, AUTH, TEST_GATE = C1GateFailure, "INCONCLUSIVE/AUTHORITY", "INCONCLUSIVE/TEST_GATE"


def _sha(out, rel) -> str:
    return stage_records.sha256(Path(out) / rel)


def release_b_check(out, ctx) -> dict:
    out = Path(out)
    try:
        rb = uc.read_json(out / "RELEASE_B.json")
        p1 = uc.read_json(out / "stages" / "E1" / "VALIDATION_REPORT.json")["p1"]
        ok = (rb["freeze_sha256"] == _sha(out, "FREEZE.json")
              and rb["k_reg2"]["manifest_sha256"] == _sha(out, "registry/K-REG2.json")
              and rb["k_reg2"]["digest_file_sha256"] == _sha(out, "registry/K-REG2_digests.npz")
              and rb["reservation_id"] == ctx.get("reservation_id")
              and rb["worker_session"] == ctx.get("worker_session", rb["worker_session"])
              and rb["N"] == p1["N"] and rb["k"] == p1["k"]
              and rb["accept_sha256"] == _sha(out, "ACCEPT_VALIDATION.json"))
    except (OSError, ValueError, KeyError, TypeError, C1GateFailure):
        ok = False
    if not ok:
        raise FAIL(AUTH, "RELEASE_B.json absent or differs")
    ctx["N"], ctx["k"] = rb["N"], rb["k"]
    return {"N": rb["N"], "k": rb["k"]}


def sample_e2(out, ctx) -> dict:
    p, dry, n = ug.ensure_proc(ctx), bool(ctx.get("dry")), int(ctx.get("block_n", uc.BLOCK_OF))
    T, E, pi, scope, k = p["T"], p["E_canon_shared"], p["pi"], ctx["scope"], ctx["k"]
    ur.begin_stage(out, "E2_S7")
    ctx["rows_drawn"] = True
    blocks = []
    try:
        blocks = [up.sample_pairs(T, E, pi, scope, "test", i, n) for i in range(k)]
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise FAIL(ug.SAMPLER, f"sampling: {exc!r}") from exc
    files = []
    for i, b in enumerate(blocks):
        for arm in ("a1", "a2"):
            rel = f"stages/E2/{'DRYHIST' if dry else 'HIST'}_test_{arm}_b{i}.npz"
            t = up.history_table(b[arm], b[f"ids_{arm}"], f"of-eval-{arm}", i)
            ur.save_array(out, rel, dry=dry, **up.table_arrays(t))
            files.append(rel)
    ur.complete_stage(out, "E2_S7", files)
    ctx["test"] = {x: np.concatenate([b[x] for b in blocks]) for x in
                   ("a1", "a2", "ids_a1", "ids_a2")}
    ctx["kreg2"] = ureg.load_registry_sets(Path(out) / "registry", "K-REG2")[:2]
    return {"files": files, "k": k}


def h2_fresh(ctx) -> dict:
    t = ctx["test"]
    tables = {"test_a1": {"canon32": t["a1"], "seq_ids": t["ids_a1"]},
              "test_a2": {"canon32": t["a2"], "seq_ids": t["ids_a2"]}}
    return ug.h2_check(ctx, tables, ctx["kreg2"], 24576 + 32768 + 8192 * ctx["k"])


def _tpre_models(ctx, pol) -> dict:
    """M0 (arm 1) and X1 (natural arms) on the 1,024 lowest-id test pairs; ephemeral logits."""
    t = ctx["test"]
    o = np.argsort(t["ids_a1"], kind="stable")[:1024]
    a1, a2 = t["a1"][o], t["a2"][o]
    d = ctx["pc"]["d"][o]
    out = {}
    for j, m in ctx["models"].items():
        perm, b = ctx["perm_of"][j], um.basis_u(m["model64"])
        inputs = um.named_inputs(a1, perm)
        acts, z = c2_model.natural_pass(m["model64"], inputs, pol, "m0")
        ij = {"master": j, "checkpoint_id": ctx["ident"]["ids"][j], "state_sha": m["state_sha"],
              "canon32": a1}
        r = um.m0_u(m["model64"], m["state_sha"], ij, inputs, acts, z, b, d, perm, pol)
        del acts, z
        if r["status"] != "PASS":
            raise FAIL(TEST_GATE, f"T-PRE M0 model {j}: {r['checks']}")
        arms = {}
        for k, a in (("a1", a1), ("a2", a2)):
            inp = um.named_inputs(a, perm)
            acts, z = c2_model.natural_pass(m["model64"], inp, pol, "x1")
            arms[f"{j}:{k}"] = (inp, c2_model.readout_coords(acts["ln_final_out"], b), z,
                                t[f"ids_{k}"][o])
            del acts
        x = c2_model.x1(m["model64"], arms, b, pol)
        del arms
        if x["status"] != "PASS":
            raise FAIL(TEST_GATE, f"T-PRE X1 model {j}: {x['arms']}")
        out[j] = {"m0": r["status"], "x1": x["status"]}
    return out


def t_pre(out, ctx) -> dict:
    pol, t, store = ctx["policy"], ctx["test"], Path(ctx["hwsc_store"])
    pol.begin("T-PRE")
    try:
        ident = um.identity_c(store, ug._handoff(ctx))
        um.charts_identity(store)
        models = um.load_stage_c(store, ident)
        h1 = uc.read_json(Path(out) / "stages" / "E1" / "H1U.json")["state_sha"]
        if any(h1.get(str(j)) != m["state_sha"] for j, m in models.items()):
            raise FAIL(um.IDENT, "state_sha differs from E1 H1U.json")
        if hwsc_records.lineage_c(store)["status"] != "PASS":
            raise FAIL(um.IDENT, "hwsc lineage")
        ctx.update(models=models, ident=ident, perm_of={j: ctx["proc"]["perm"][j] for j in models})
        r3 = ug.h3_split(ctx, t["a1"], t["a2"], "test")
        ctx.update(h3=r3, pc=r3["pc"], o1=r3["o1"], o2=r3["o2"], s1=r3["s1"], A_KO=r3["A_KO"])
        b = ug.h5_bounds(r3["pc"]["G"], ctx["seeds"]["h5_test"], uc.ALPHA_HEADROOM)
        if not Fraction(float(b["L"])) > Fraction(1, 100):
            raise FAIL(TEST_GATE, f"H5-U at test: L {b['L']}")
        ctx["basis_of"] = {j: um.basis_u(m["model64"]) for j, m in models.items()}
        res = _tpre_models(ctx, pol)
    except C1GateFailure as exc:
        pol.end("T-PRE")
        raise FAIL(TEST_GATE, f"T-PRE: {exc.status} {exc.reason}"[:600]) from exc
    pol.mark_pass("T-PRE")
    pol.end("T-PRE")
    um.write_json(Path(out) / "stages" / "E2" / "TPRE.json", {"models": res, "H5_L": b["L"]})
    return {"models": res}


def num_gate(out, ctx) -> dict:
    out, dry, t, pc = Path(out), bool(ctx.get("dry")), ctx["test"], ctx["pc"]
    pol, models = ctx["policy"], list(ctx["models"])
    pol.begin("NUM")
    A, rows = ug.model_A(ctx, t["a1"], t["a2"], pc["d"])
    pol.end("NUM")
    G, o1, s1 = pc["G"], ctx["o1"], ctx["s1"]
    rowA = {j: um.row_cross_check(c1_oracle.named_from_canonical(o1["qbar"], ctx["perm_of"][j]),
                                  c1_oracle.named_from_canonical(s1["q4bar"], ctx["perm_of"][j]),
                                  rows[j][0], ctx["basis_of"][j]) for j in models}
    draws = int(ctx.get("family_draws", 20000))
    b = ud.family_bounds(A, G, models, ctx["seeds"]["family_U"], draws=draws)
    ok = {j: all(c2_decide.sign(b[f"{j}:{s}"][e], b[f"{j}:{s}"]["g"]) != 0
                 for s, e in (("ZR010", "L"), ("ZR010", "U"), ("ZR030", "L"), ("ZR030", "U"),
                              ("AF", "L"))) for j in models}
    ctx.update(A_test=A, rowA=rowA, bounds=b, num_ok=ok)
    arrays = {f"{j}:{s}": v for j in models for s, v in um.response_arrays(A[j], G).items()}
    ur.save_array(out, "stages/E2/ORACLE_E2_test.npz", dry=dry, G=G, d=pc["d"],
                  le_a1=o1["le"], le_a2=ctx["o2"]["le"])
    pair = {}
    for j in models:
        ra = um.response_arrays(A[j], G)
        pair.update({f"A_{j}": A[j], f"ZR010_{j}": ra["ZR010"], f"ZR030_{j}": ra["ZR030"],
                     f"rowA_{j}": rowA[j]})
    ur.save_array(out, "stages/E2/PAIR_E2_test.npz", dry=dry, **pair)
    boot = c1_means.bootstrap_means(arrays, ctx["seeds"]["family_U"], draws)
    ur.save_array(out, "stages/E2/BOOT_E2.npz", dry=dry, **{k.replace(":", "_"): v
                                                           for k, v in boot.items()})
    return {"models": {j: "OK" if ok[j] else f"INC_{j}/NUMERICAL" for j in models}}


def sealed_opened(out, ctx) -> Path:
    p = Path(out) / "SEALED_VALIDATION.json"
    means = json.loads(p.read_bytes().decode("utf-8"))["means"]
    return um.write_json(Path(out) / "stages" / "E2" / "SEALED_OPENED.json", {
        "sealed_sha256": stage_records.sha256(p), "means": means, "opened_utc": ur.utc()})


def endpoint(out, ctx) -> dict:
    out, pol, G = Path(out), ctx["policy"], ctx["pc"]["G"]
    models, b = list(ctx["models"]), ctx["bounds"]
    pol.begin("ENDPOINT")
    per = {}
    for j in models:
        if ctx["num_ok"][j]:
            per[j] = ud.model_status({s: b[f"{j}:{s}"] for s in ("ZR010", "ZR030", "AF")})
        else:
            per[j] = {"status": f"INC_{j}/NUMERICAL", "rule6": False, "coarse": [], "bounds": None}
    resp = ud.response_outcome({j: v["status"] for j, v in per.items()},
                               {j: v["rule6"] for j, v in per.items()})
    share = ud.share_outcome(uk.of_binding(out))
    desc = ud.descriptives(ctx["A_test"], G, ctx["rowA"], models)
    A_KO = ctx["A_KO"]
    ids = uo.ko_identities(G, A_KO)
    cats = uo.ko_categories(G, A_KO, ctx["seeds"]["kc_test"], draws=int(ctx.get("draws", uc.DRAWS)))
    ko = {"identities": {k: v["ok"] for k, v in ids.items()},
          "categories": {k: cats[k]["category"] for k in uo.CASES}, "tails": desc["tails"]}
    lic = ud.licences(resp, {j: v["status"] for j, v in per.items()}, b, desc)
    ctx.update(resp=resp, share=share, per_model=per, desc=desc, licences=lic, ko_test=ko)
    f1 = um.write_json(out / "stages" / "E2" / "ENDPOINT.json", {
        "family_bounds": b, "per_model": per, "response": resp, "share": share})
    f2 = sealed_opened(out, ctx)
    ur.complete_stage(out, "ENDPOINT", [f1, f2, out / "SEALED_VALIDATION.json"])
    pol.end("ENDPOINT")
    return {"outcome": resp["outcome"], "share_outcome": share["outcome"]}


def report_u(out, ctx, records) -> Path:
    resp, share = ctx["resp"], ctx["share"]
    rec = {"schema": "hwsu-report-v1", "outcome": ud.study_outcome(
        [{"status": r["status"]} for r in records], resp, share),
        "response": {"outcome": resp["outcome"], "per_model": {j: v["status"] for j, v in ctx[
            "per_model"].items()}, "rule6": resp["rule6"], "coarse": {j: v["coarse"] for j, v in
                                                                      ctx["per_model"].items()},
                     "dissent": resp["dissent"], "qualifiers": resp["qualifiers"]},
        "share": share, "family": {"alpha": "1/300", "fw_events_per_model": 2,
                                   "family_error": "0.02 <= 0.05"},
        "bounds": ctx["bounds"], "descriptives": ctx["desc"], "ko_test": ctx["ko_test"],
        "licences": ctx["licences"], "disclosure": ctx["licences"]["disclosure"],
        "does_not_establish": ctx["licences"]["does_not_establish"], "N": ctx["N"],
        "k": ctx["k"], "gates": {r["gate"]: r["status"] for r in records},
        "cpu_s": ctx.get("cpu_s"), "protocol_sha256": uc.CONTRACT["protocol_sha256"],
        "contract_of_sha256": uc.CONTRACT_SHA256["of"],
        "contract_sha256": uc.CONTRACT_SHA256["phase2"],
        "freeze_sha256": _sha(out, "FREEZE.json"),
        "freeze_of_sha256": uk.of_binding(out)["freeze_of_sha256"],
        "of_accept_sha256": share["of_accept_sha256"], "written_utc": ur.utc()}
    return um.write_json(Path(out) / "stages" / "E2" / "REPORT.json", rec)
