"""HWSC gates: H1-C, L1, P1 (p1c and the N rule), the POSITIVE_BELOW_MARGIN annotation, the
outcome precedence and the licences (API.md §6, §11.2, §12; protocol §5, §6)."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
import math
from fractions import Fraction
from pathlib import Path

import c1_cert
import c1_model
import hwsb_eval
import hwsb_gates
import hwsb_law
import hwsc_data
import k4b_cert
import k4b_config
import k4b_driver
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import SeedTree

IDENTITY, LAW = "FAIL_TECHNICAL/IDENTITY", "FAIL_TECHNICAL/LAW_BOUND"
NUMERICAL, UNDERPOWERED = "FAIL_TECHNICAL/NUMERICAL", "INCONCLUSIVE/UNDERPOWERED"
STEP_LABEL = {5000: "step5000", 0: "step0"}


def _fr(x) -> Fraction:
    x = x[0] if isinstance(x, (tuple, list)) else x
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    return Fraction(float(x))


def _write(out, name, obj) -> Path:
    p = Path(out) / "stages" / "E1" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, obj)
    return p


# ------------------------------------------------------------------------------- H1-C (gate 1)
def expected_meta_c(j, step, record) -> dict:
    j = int(j)
    return {"artifact_id": record["checkpoint_ids"][str(step)], "artifact_type": "Checkpoint",
            "run_key": [cc.SCOPE, cc.KEY, j], "step": int(step), "status": "complete",
            "init_seed_key": f"init/{cc.SCOPE}/{cc.KEY}/{j}",
            "init_seed": SeedTree(j).seed("init", cc.SCOPE, cc.KEY, j),
            "payload_sha256": record["checksums"][str(step)]}


def exclusion_check(ids, handoff) -> dict:
    bad = sorted(set(ids) & set(handoff["stage_c_exclusions"]))
    return {"ok": not bad, "excluded": bad}


def law_identity(proc, handoff) -> dict:
    try:
        law = hwsb_law.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"],
                                 cc.SIGMA, cc.NEIGHBOUR)
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(LAW, repr(exc)) from exc
    if law["status"] != "BOUNDED" or law["Z_bound"] != handoff["Z_bound"]:
        raise C1GateFailure(LAW, f"law {law['status']}, Z_bound {law['Z_bound']} != HANDOFF")
    return {"status": "PASS", "Z_bound": law["Z_bound"], "kappa": law["kappa"],
            "delta": law["delta"], "sigma": law["sigma"], "neighbour": law["neighbour"]}


def _stage_complete_sha(out, stage, rel) -> str | None:
    want = None
    for e in stage_records.stages_so_far(Path(out)):
        if e.get("stage") == stage and e.get("event") == "STAGE_COMPLETE":
            want = e.get("files", {}).get(rel, want)
    return want


def h1c(out, ctx, handoff, store, stage="E1") -> dict:
    import torch

    out = Path(out)
    rel = ctx.get("release") or {}
    try:
        recs, metas, ids = {}, {}, []
        for j in cc.MASTERS:
            relp = f"stages/TRAIN/{j}/TRAIN_RECORD.json"
            sha = stage_records.sha256(out / relp)
            if sha != (rel.get("train_records") or {}).get(str(j)) or \
                    sha != _stage_complete_sha(out, f"TRAIN_{j}", relp):
                raise C1GateFailure(IDENTITY, f"TRAIN record {j} not bound")
            recs[j] = cc.read_json(out / relp)
            if recs[j].get("status") != "COMPLETE":
                raise C1GateFailure(IDENTITY, f"TRAIN record {j} status {recs[j].get('status')}")
            seeds = set()
            for step in (5000, 0):
                exp = expected_meta_c(j, step, recs[j])
                meta = k4b_driver.checkpoint_meta(out / "artifacts", exp["artifact_id"])
                r = k4b_config.check_checkpoint_meta(meta, exp)
                if r["status"] != "PASS":
                    raise C1GateFailure(IDENTITY, json.dumps(r["mismatches"], default=str))
                seeds.add(meta["seed_map"][exp["init_seed_key"]])
                metas[f"{j}/{STEP_LABEL[step]}"] = r
                ids.append(exp["artifact_id"])
            if len(seeds) != 1:
                raise C1GateFailure(IDENTITY, f"init seeds differ for {j}")
        ex = exclusion_check(ids, handoff)
        if not ex["ok"]:
            raise C1GateFailure(IDENTITY, f"pilot checkpoint ids {ex['excluded']}")
        models, ckpts, shas = {}, {}, {}
        for j in cc.MASTERS:
            for step in (5000, 0):
                ck = k4b_driver.load_checkpoint(recs[j]["checkpoint_ids"][str(step)])
                ckpts[(j, step)] = ck
                models[(j, STEP_LABEL[step])], shas[f"{j}/{STEP_LABEL[step]}"] = \
                    c1_model.load_model64(ck)
        proc = hwsc_data.build_process_c(store)
        ident = hwsc_data.process_identity(store, proc)
        if not ident["ok"]:
            raise C1GateFailure(IDENTITY, json.dumps(ident["checks"]))
        law = law_identity(proc, handoff)
        selftest = c1_cert.a1_selftest()
        threads = torch.get_num_threads()
        pd = hwsc_data.p_d2a_check(proc, handoff["p_D2a"])
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001  any H1-C defect is an identity defect
        raise C1GateFailure(IDENTITY, repr(exc)) from exc
    if threads != 1:
        raise C1GateFailure(IDENTITY, f"{threads} threads")
    if not pd["ok"]:
        raise C1GateFailure(IDENTITY, f"p_D2a rel diff {pd['rel_diff']}")
    ctx.update(proc=proc, models=models, ckpts=ckpts, Z=law["Z_bound"], p_d2a=pd["p_D2a"])
    rec = {"checkpoint_meta": metas, "state_sha": shas, "identity": ident["checks"],
           "law": {k: str(v) for k, v in law.items()}, "p_D2a": pd, "a1_selftest": selftest,
           "threads": threads}
    p = Path(out) / "stages" / stage / ("H1C.json" if stage == "E1" else "H1C_E2.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, json.loads(json.dumps(rec, default=str)))
    return {"Z_bound": str(law["Z_bound"]), "threads": threads, "p_D2a": pd}


# --------------------------------------------------------------------------------- L1 (gate 4)
def l1(out, ctx) -> dict:
    proc, lg = ctx["proc"], ctx["tables"]["lgate"]["canon32"]
    q = hwsb_eval.oracle_predictives(proc, lg)
    per = {}
    for j in cc.MASTERS:
        p = hwsb_eval.model_predictive(ctx["ckpts"][(j, 5000)], lg, proc["perm"][j])
        per[j] = hwsb_eval.b1(q, p)
    for j, r in per.items():
        if r["status"] == "INCONCLUSIVE" or not math.isfinite(float(r["captured"])):
            raise C1GateFailure(NUMERICAL, f"L1 model {j}: G_C {r['G_C']}, {r['captured']}")
    failing = [j for j in cc.MASTERS if per[j]["status"] == "FAIL"]
    rec = {"per_model": {str(j): r for j, r in per.items()}, "failing": failing,
           "k": len(failing)}
    _write(out, "L1.json", json.loads(json.dumps(rec, default=float)))
    if failing:
        raise C1GateFailure("INCONCLUSIVE/NOT_LEARNED", f"{len(failing)}/3: {failing}")
    return {"per_model": {str(j): {"captured": r["captured"], "status": r["status"]}
                          for j, r in per.items()}}


# --------------------------------------------------------------------------------- P1 (gate 10)
def p1c_ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict:
    return hwsb_gates.ladder_pilot(X_minus, X_plus, r4n, F_plan, models=cc.MASTERS,
                                   seeds=cc.P1C_SEEDS, D_bar=D_bar, ladder=cc.LADDER)


def choose_N(N_C, ladder_result) -> dict:
    n_p1 = ladder_result["N"]
    if n_p1 is None:
        return {"status": UNDERPOWERED, "N": None, "k": None, "N_P1": None, "N_C": int(N_C)}
    N = max(int(N_C), int(n_p1))
    if N not in cc.LADDER:
        raise C1GateFailure(NUMERICAL, f"N = {N} is not a ladder value")
    return {"status": "PASS", "N": N, "k": N // cc.BLOCK, "N_P1": int(n_p1), "N_C": int(N_C)}


def p1c(out, ctx, handoff) -> dict:
    out, a = Path(out), ctx["val_arrays"]
    F = k4b_cert.F_plan(ctx["Z"])
    D = {j: float(np.mean(a[j]["X_plus"] - a[j]["X_minus"]) / 2) for j in cc.MASTERS}
    lad = p1c_ladder({j: a[j]["X_minus"] for j in cc.MASTERS},
                     {j: a[j]["X_plus"] for j in cc.MASTERS},
                     {j: a[j]["r4n"] for j in cc.MASTERS}, F, D)
    sealed = k4b_stats.write_sealed(out, {"mean_X_minus": {j: a[j]["X_minus"] for j in cc.MASTERS},
                                          "mean_X_plus": {j: a[j]["X_plus"] for j in cc.MASTERS}})
    nc = choose_N(handoff["N_C"], lad)
    risk = hwsc_data.registry_risk(ctx["p_d2a"], nc["N"]) if nc["N"] else None
    report = {"gates": stage_records.gates_so_far(out), "support": ctx["support"],
              "B4": {k: str(v) for k, v in ctx["B4"].items()},
              "sdU": {f"{j}{s}": v for (j, s), v in lad["sdU"].items()},
              "ladder": {"status": lad["status"], "N": nc["N"], "k": nc["k"], "N_P1": nc["N_P1"],
                         "N_C": nc["N_C"], "candidates": lad["candidates"]},
              "certificate": {k: str(v) for k, v in ctx["certificate"]["max_B"].items()},
              "F_plan": str(F), "Z_bound": str(ctx["Z"]), "sealed_sha256": sealed,
              "registry_risk": risk, "lineage_disclosure": cc.DISCLOSURE}
    k4b_stats.check_unsealed(report)
    k4b_driver.begin_stage(out, "S5")
    f = out / "stages" / "S5" / "VALIDATION_REPORT.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, report)
    k4b_driver.complete_stage(out, "S5", [f])
    if nc["status"] != "PASS":
        raise C1GateFailure(UNDERPOWERED, "no ladder candidate qualifies")
    if not risk["ok"]:
        raise C1GateFailure("INCONCLUSIVE/REGISTRY_INCOMPLETE", f"registry risk {risk['value']}")
    return {"N": nc["N"], "k": nc["k"], "N_P1": nc["N_P1"], "N_C": nc["N_C"],
            "sealed_sha256": sealed}


from hwsc_outcome import (  # noqa: E402,F401  (split by size, API erratum)
    annotations,
    licence,
    outcome,
    positive_below_margin,
    state_from_gates,
)
