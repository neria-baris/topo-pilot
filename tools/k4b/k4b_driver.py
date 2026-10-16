"""K4b release-A driver: G0 -> P1 (API.md §9; protocol §6 gate table, §11.8 stage records).

Each gate fn returns a details dict or raises; run_gates records it and stops at the first
non-PASS (later gates NOT_RUN). Gate fns share one context dict `ctx` (process, tables, arrays).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import k4b_cert
import k4b_charts
import k4b_config
import k4b_data
import k4b_registry
import k4b_release
import k4b_scores
import k4b_stats
import numpy as np
import op_guard
import scores
import stage_records
from c1_records import C1GateFailure, classify_exception
from k4b_config import MODELS, SEEDS, check_checkpoint_meta, expected_meta  # noqa: F401

GATE_ORDER = ("G0", "H1", "REG1", "H2", "ORACLE-VAL", "B4-VAL", "C0-CAL", "C0-VAL", "CERT-VAL",
              "P1")
K4_FREEZE = k4b_config.ROOT / "x4-circle-history-feas-store-0015" / "FREEZE.json"
OWNER_DIR = Path("archive") / "owner-decisions-20261015"
AUTHORITY_FILES = {"addendum_3_sha256": "OWNER_DECISIONS.addendum-3.md",
                   "addendum_10_sha256": "OWNER_DECISIONS.addendum-10.md",
                   "owner_decisions_v1_a2_sha256": "OWNER_DECISIONS.v1-a73c869.md"}
ARTIFACTS = k4b_config.ROOT / "topo-pilot" / "artifacts"
IDENTITY = "FAIL_TECHNICAL/IDENTITY"


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_gates(out, steps) -> list:
    recs, stopped = [], False
    for gate, fn in steps:
        if stopped:
            stage_records.record_gate(out, gate, "NOT_RUN")
            recs.append({"gate": gate, "status": "NOT_RUN"})
            continue
        try:
            details = fn() or {}
            status = details.pop("status", "PASS") if isinstance(details, dict) else "PASS"
        except Exception as exc:  # noqa: BLE001  every failure is recorded, then stops
            status, reason = classify_exception(exc)
            if "SPLIT_OVERLAP" in str(getattr(exc, "code", "")) + repr(exc):
                status = "FAIL_TECHNICAL/LINEAGE"
            details = {"reason": str(reason)}
        stage_records.record_gate(out, gate, status, **details)
        recs.append(dict(details, gate=gate, status=status))
        stopped = status != "PASS"
    return recs


def begin_stage(out, stage) -> None:
    op_guard.write_marker(out, {"state": "idle", "stage": stage, "label": f"stage {stage}",
                                "seq": 0})
    with (Path(out) / "STAGES.jsonl").open("a", encoding="utf-8") as h:
        h.write(json.dumps({"stage": stage, "event": "BEGIN", "utc": _utc()}) + "\n")


def complete_stage(out, stage, files) -> dict:
    out = Path(out)
    rec = {"stage": stage, "event": "STAGE_COMPLETE", "utc": _utc(),
           "files": {Path(f).resolve().relative_to(out.resolve()).as_posix(): _sha(f)
                     for f in files}}
    with (out / "STAGES.jsonl").open("a", encoding="utf-8") as h:
        h.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def classify_seed_hits(hits) -> dict:
    """RC5: PASS iff every hit is this lineage's declaration; anything else fails closed."""
    bad = [h for h in hits if h.get("kind") != "k4b_declaration"]
    return {"status": "FAIL_TECHNICAL/SEED_SCOPE" if bad else "PASS", "hits": list(hits),
            "failing": bad}


def _stage_dir(out, stage) -> Path:
    d = Path(out) / "stages" / stage
    d.mkdir(parents=True, exist_ok=True)
    return d


def g0(out, release, mailbox) -> dict:
    c, mailbox = k4b_config.CONTRACT, Path(mailbox)
    auth = {}
    for key, name in AUTHORITY_FILES.items():
        p = mailbox / OWNER_DIR / name
        if not p.is_file():
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"authority file absent: {name}")
        if _sha(p) != c["authority"][key]:
            raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", f"authority hash: {name}")
        auth[name] = c["authority"][key]
    w1 = {}
    for ev in c["authority"]["window_w1_evidence"]:
        if ev.startswith("main commit"):
            continue
        if not (mailbox / ev).is_file():
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"W1 evidence absent: {ev}")
        w1[ev] = _sha(mailbox / ev)
    for key in ("w3_attestation", "kreg1_reservation", "seed_hits"):
        if release.get(key) is None:
            raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"release A lacks {key}")
    seeds = classify_seed_hits(release["seed_hits"])
    if seeds["status"] != "PASS":
        raise C1GateFailure(seeds["status"], json.dumps(seeds["failing"], default=str))
    lineage = k4b_release.lineage_ok(out)
    if _sha(K4_FREEZE) != c["authority"]["k4_freeze_sha256"]:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "K4 FREEZE.json hash")
    text = K4_FREEZE.read_text(encoding="utf-8")
    for f in c["authority"]["k4_freeze_checked_files"]:
        if _sha(k4b_config.REPO / "tools" / "x4_circle_history" / f) not in text:
            raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"K4 FREEZE hash of {f}")
    eq = k4b_config.check_chart_equality()
    if not (eq["equal"] and eq["giant_equal"] and eq["val_support_equal"]):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"chart cfg differs from C1': {eq}")
    return {"authority": auth, "w1": w1, "seed_hits": len(seeds["hits"]), "lineage": lineage,
            "chart_equality": eq}


def load_checkpoint(artifact_id):
    from topo_pilot.contracts import ArtifactStore, Checkpoint
    from topo_pilot.contracts.backends import LocalFSBackend

    store = ArtifactStore(LocalFSBackend(ARTIFACTS))
    return store.load(Checkpoint, artifact_id, consumer="experiment")


def checkpoint_meta(artifact_root, artifact_id) -> dict:
    """API.md §14.1: reads only <root>/Checkpoint/<id>/meta.json."""
    try:
        meta = json.loads((Path(artifact_root) / "Checkpoint" / artifact_id / "meta.json")
                          .read_bytes().decode("utf-8"))
        assert isinstance(meta, dict), "not a JSON object"
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(IDENTITY, f"checkpoint meta {artifact_id}: {exc!r}") from exc
    return meta


def check_checkpoints(artifact_root=ARTIFACTS) -> dict:
    """All six meta checks before any checkpoint load; the first non-PASS raises."""
    res = {}
    for j, label in ((j, s) for j in MODELS for s in ("step5000", "step0")):
        exp = expected_meta(j, label)
        res[f"{j}/{label}"] = r = check_checkpoint_meta(checkpoint_meta(artifact_root,
                                                                         exp["artifact_id"]), exp)
        if r["status"] != "PASS":
            raise C1GateFailure(IDENTITY, json.dumps(r["mismatches"], default=str)[:2000])
    return res


def h1(out, ctx) -> dict:
    import c1_cert
    import c1_model
    import oracle_profile
    import torch

    meta = check_checkpoints()
    try:
        proc = k4b_data.load_process()
        models, shas = {}, {}
        for j in MODELS:
            ids = k4b_config.CONTRACT["checkpoints"][str(j)]
            for step in ("step5000", "step0"):
                models[(j, step)], shas[f"{j}/{step}"] = c1_model.load_model64(
                    load_checkpoint(ids[step]))
            oracle_profile.validate_process(proc["T"], proc["E_canon"][j], proc["pi"])
        tb = k4b_cert.transport_bound(proc["T"], proc["E_canon_shared"], proc["pi"],
                                      proc["coords"])
        selftest = c1_cert.a1_selftest()
        threads = torch.get_num_threads()
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001  any H1 defect is an identity defect
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", repr(exc)) from exc
    if threads != 1:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"{threads} threads")
    ctx.update(proc=proc, models=models, Z=tb["Z_bound"])
    return {"checkpoint_meta": meta, "state_sha": shas, "Z_bound": str(tb["Z_bound"]),
            "z_job0018_report_only": k4b_config.CONTRACT["certificate"][
                "z_bound_job0018_report_only"],
            "a1_selftest": selftest, "threads": threads}


def reg1(out, ctx) -> dict:
    if ctx["release"].get("kreg1_certificate") is None:
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", "no coordinator completeness certificate")
    reg_dir = Path(out) / "registry"
    reg_dir.mkdir(parents=True, exist_ok=True)
    begin_stage(out, "REG1")
    m = k4b_registry.build("K-REG1", reg_dir)
    complete_stage(out, "REG1", [reg_dir / "K-REG1.json", reg_dir / "K-REG1_digests.npz"])
    if m["status"] != "PASS":
        raise C1GateFailure(m["status"], "; ".join(m["problems"])[:2000])
    ctx["reg1"] = k4b_registry.load(reg_dir, "K-REG1")
    return {"n_digests": m["n_digests"], "digests_sha256": m["digests_sha256"]}


def h2(out, ctx) -> dict:
    rel, p = ctx["release"], ctx["proc"]
    res = k4b_release.verify_reservation(ctx["reservation_path"], rel)
    if res["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"{res['status']}: {res['reason']}")
    begin_stage(out, "S3")
    d, files, tabs = _stage_dir(out, "S3"), [], {}
    for split in ("cal", "val"):
        canon, ids = k4b_data.sample_block(p["T"], p["E_canon_shared"], p["pi"], split, 0)
        tabs[split] = t = k4b_data.history_table(canon, ids, split, 0)
        f = d / f"HIST_{split}_b0.npz"
        stage_records.save_npz(f, **{k: v for k, v in t.items() if isinstance(v, np.ndarray)})
        files.append(f)
    complete_stage(out, "S3", files)
    ctx["tables"] = tabs
    digests, seq_union, ranges, predicates, _ = ctx["reg1"]
    sep = k4b_data.separation_cal_val(set(tabs["cal"]["digest"].tolist()),
                                      set(tabs["val"]["digest"].tolist()), digests)
    disj = k4b_data.seq_disjoint({s: tabs[s]["seq_ids"] for s in tabs}, seq_union,
                                 list(ranges.values()))
    pred = {s: k4b_data.predicate_check(tabs[s]["canon32"], predicates) for s in tabs}
    dup = {s: k4b_data.duplicates(tabs[s]["canon32"]) for s in tabs}
    for r in (sep, disj, *pred.values()):
        if r["status"] != "PASS":
            raise C1GateFailure(r["status"], json.dumps(r, default=str)[:2000])
    return {"separation": sep, "seq_disjoint": disj, "predicates": pred, "duplicates": dup}


def oracle_val(out, ctx) -> dict:
    p, tabs = ctx["proc"], ctx["tables"]
    begin_stage(out, "S4")
    d, mom = _stage_dir(out, "S4"), {}
    for s in ("cal", "val"):
        mom[s] = k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"],
                                           tabs[s]["canon32"], p["features"])
        stage_records.save_npz(d / f"ORACLE_{s}.npz", **{f"m{K}": v for K, v in mom[s].items()})
    refs = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                               tabs["val"]["canon32"])
    chk = k4b_cert.moment_check(mom["val"], refs)
    complete_stage(out, "S4", [d / "ORACLE_cal.npz", d / "ORACLE_val.npz"])
    if not chk["ok"]:
        raise C1GateFailure("FAIL_TECHNICAL/ORACLE", f"{chk['n_fail']} rows above MOMENT_TOL")
    ctx.update(moments=mom, refs_val=refs, eps=k4b_cert.envelopes())
    return {"max_gap": str(chk["max_gap"])}


def b4_val(out, ctx) -> dict:
    m, refs, eps = ctx["moments"]["val"], ctx["refs_val"], ctx["eps"]
    r4n = scores.r4_norms(m[32], m[4])
    Bn = max(k4b_cert.norm_bound(r4n[i], ref[32], ref[4], eps[4], eps[32])
             for i, ref in enumerate(refs))
    g = k4b_cert.b4_guard(r4n, Bn, ctx["Z"], SEEDS["val_b4"], len(r4n))
    ctx["B4"] = g
    if g["status"] != "PASS":
        raise C1GateFailure(g["status"], f"B4 lower {g['lower']}")
    return {"B4": {k: str(v) if not isinstance(v, (int, float)) else v for k, v in g.items()}}


def _acts(ctx, split) -> dict:
    import c1_model

    t, p = ctx["tables"][split], ctx["proc"]
    return {(j, s): c1_model.activations(ctx["models"][(j, s)],
                                         k4b_data.model_inputs(t["canon32"], p["perm"][j]))
            for j in MODELS for s in ("step5000", "step0")}


def c0_cal_stage(out, ctx) -> dict:
    import k4b_decoder

    cfg, t, m32 = k4b_config.chart_cfg(), ctx["tables"]["cal"], ctx["moments"]["cal"][32]
    acts = ctx["acts_cal"] = _acts(ctx, "cal")
    land = np.asarray(t["landmark"], dtype=bool)
    ids = t["seq_ids"][land]
    X = {j: acts[(j, "step5000")][land] for j in MODELS}
    cal = k4b_charts.c0_cal(MODELS, X, ids, m32[land], out, cfg)
    if cal["status"] != "PASS":
        raise C1GateFailure(cal["status"], str(cal.get("reason")))
    init = k4b_charts.init_charts(MODELS, {j: acts[(j, "step0")][land] for j in MODELS}, ids,
                                  m32[land], out, cfg)
    dec = {}
    for j in MODELS:
        ext = k4b_charts.extend(cal["per_model"][j]["chart"], cal["per_model"][j]["gauge"],
                                acts[(j, "step5000")][~land], cfg)
        dec[j] = k4b_decoder.fit(t["canon32"][~land], t["seq_ids"][~land], ext.phase, j)
    rec = k4b_charts.freeze_production(out, cal["per_model"], init, dec)
    ctx.update(prod=cal["per_model"], init=init["per_model"], decoders=dec)
    return {"chart_diagnostics": {j: r["diagnostics"] for j, r in cal["per_model"].items()},
            "init": {j: r["status"] for j, r in init["per_model"].items()},
            "decoders": {j: d["status"] for j, d in dec.items()}, "frozen": rec["files"]}


def c0_val_stage(out, ctx) -> dict:
    k4b_charts.require_frozen(out)
    acts = ctx["acts_val"] = _acts(ctx, "val")
    t = ctx["tables"]["val"]
    land = np.asarray(t["landmark"], dtype=bool)
    res = k4b_charts.c0_val_gate(MODELS, ctx["prod"], {j: acts[(j, "step5000")][land]
                                                       for j in MODELS}, t["seq_ids"][land],
                                 out, k4b_config.chart_cfg())
    if res["status"] != "PASS":
        raise C1GateFailure(res["status"], json.dumps(res["per_model"], default=str)[:2000])
    return {"c0_val": res["per_model"]}


def cert_val(out, ctx) -> dict:
    cfg, m = k4b_config.chart_cfg(), ctx["moments"]["val"]
    arrays, primary, support = {}, {}, {}
    for j in MODELS:
        ext = k4b_charts.extend(ctx["prod"][j]["chart"], ctx["prod"][j]["gauge"],
                                ctx["acts_val"][(j, "step5000")], cfg)
        a = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])
        b = k4b_cert.endpoint_bounds(a, ext.supported, ext.phase, ctx["refs_val"], ctx["eps"])
        arrays[j] = dict(a, phi=ext.phase, supported=ext.supported, bounds=b)
        primary[f"X_minus_{j}"] = {"X": a["X_minus"], "max_B": b["max"]["minus"]}
        primary[f"X_plus_{j}"] = {"X": a["X_plus"], "max_B": b["max"]["plus"]}
        support[j] = {"val": k4b_scores.support_report(ext, cfg.get("support_radius", 0.0),
                                                       a["r4n"], ext.phase, m[32], m[4], True)}
    primary["n_hat"] = {"X": arrays[MODELS[0]]["r4n"], "max_B": max(
        arrays[j]["bounds"]["max"]["norm"] for j in MODELS)}
    cert = k4b_cert.certify(primary, {})
    ctx.update(val_arrays=arrays, support=support, certificate=cert)
    if cert["status"] != "PASS":
        raise C1GateFailure(cert["status"], "a primary row bound exceeds the cap")
    return {"certificate": {k: str(v) for k, v in cert["max_B"].items()}}


def p1(out, ctx) -> dict:
    a = ctx["val_arrays"]
    F = k4b_cert.F_plan(ctx["Z"])
    D = {j: float(np.mean(a[j]["X_plus"] - a[j]["X_minus"]) / 2) for j in MODELS}
    lad = k4b_stats.ladder({j: a[j]["X_minus"] for j in MODELS},
                           {j: a[j]["X_plus"] for j in MODELS},
                           {j: a[j]["r4n"] for j in MODELS}, F, D)
    sealed = k4b_stats.write_sealed(out, {"mean_X_minus": {j: a[j]["X_minus"] for j in MODELS},
                                          "mean_X_plus": {j: a[j]["X_plus"] for j in MODELS}})
    gates = stage_records.gates_so_far(out)
    report = {"gates": gates, "support": ctx["support"], "B4": {k: str(v) for k, v in
                                                                ctx["B4"].items()},
              "sdU": {f"{j}{s}": v for (j, s), v in lad["sdU"].items()},
              "ladder": {"status": lad["status"], "N": lad["N"], "k": lad["k"],
                         "candidates": lad["candidates"]},
              "certificate": {k: str(v) for k, v in ctx["certificate"]["max_B"].items()},
              "F_plan": str(F), "Z_bound": str(ctx["Z"]), "sealed_sha256": sealed,
              "c1prime_disclosure": k4b_config.CONTRACT["authority"]["c1prime_disclosure"]}
    k4b_stats.check_unsealed(report)
    begin_stage(out, "S5")
    f = _stage_dir(out, "S5") / "VALIDATION_REPORT.json"
    stage_records.write_new(f, report)
    complete_stage(out, "S5", [f])
    if lad["status"] != "PASS":
        raise C1GateFailure(lad["status"], "no ladder candidate qualifies")
    return {"N": lad["N"], "k": lad["k"], "sealed_sha256": sealed}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="K4b release A: G0 -> P1")
    ap.add_argument("--release", required=True)
    ap.add_argument("--out", default=str(k4b_config.STORE))
    ap.add_argument("--task-sha256", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--mailbox", default=str(k4b_config.ROOT / "agent-handoff"))
    a = ap.parse_args(argv)
    out = Path(a.out)
    rel = k4b_release.verify_release(a.release, "A", a.task_sha256, a.session, out / "FREEZE.json")
    ctx = {"release": rel, "reservation_path": Path(a.mailbox) / rel["reservation"]}
    steps = [("G0", lambda: g0(out, rel, a.mailbox)), ("H1", lambda: h1(out, ctx)),
             ("REG1", lambda: reg1(out, ctx)), ("H2", lambda: h2(out, ctx)),
             ("ORACLE-VAL", lambda: oracle_val(out, ctx)), ("B4-VAL", lambda: b4_val(out, ctx)),
             ("C0-CAL", lambda: c0_cal_stage(out, ctx)), ("C0-VAL", lambda: c0_val_stage(out, ctx)),
             ("CERT-VAL", lambda: cert_val(out, ctx)), ("P1", lambda: p1(out, ctx))]
    recs = run_gates(out, steps)
    return 0 if all(r["status"] == "PASS" for r in recs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
