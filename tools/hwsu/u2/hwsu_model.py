"""HWSU model part: stage-C loading, readout, response arrays, M0/X1 mirrors, logit policy
(API_U2.md section 1; protocol 2.3-2.5, 2.10, 3.1, 6 rows 6, 11, 12).

No logit is formed outside BASIS, M0, X1 and T-PRE; every logit is deleted after its identity
check. c2_model.m0, c2_driver.LogitPolicy, k4b_driver.* are never called (mirrored here).
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import u2  # noqa: F401
import json
from pathlib import Path

import c1_model
import c1_oracle
import c2_attrib
import c2_model
import hwsc_gates
import k4b_config
import numpy as np
import stage_records
import topo_pilot.contracts as tpc
import topo_pilot.contracts.backends as tpb
import torch
from c1_records import C1GateFailure

IDENT, MODEL, X1F, BIND = ("FAIL_TECHNICAL/IDENTITY", "FAIL_TECHNICAL/MODEL",
                           "FAIL_TECHNICAL/X1", "FAIL_TECHNICAL/BINDING")
TRAIN_KEYS = ("checkpoint_ids", "checksums", "run_key", "status")
GATE_ORDER_U = ("BASIS", "M0", "X1", "P1", "T-PRE", "NUM", "ENDPOINT")
ALLOWED_U = {"basis": {"BASIS"}, "m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"},
             "test_endpoint": {"NUM", "ENDPOINT"}}


def _c(contract=None) -> dict:
    return (uc.CONTRACT if contract is None else contract)["stage_c_u2"]


# ------------------------------------------------------------------- identity and loading
class _Pairs(list):
    """Inert object body: nothing is looked up by key until the whitelist is applied."""


def _plain(x):
    if isinstance(x, _Pairs):
        return {k: _plain(v) for k, v in x}
    if isinstance(x, list):
        return [_plain(v) for v in x]
    return x


def read_train_record(path, root=uc.ROOT) -> dict:
    raw = uc.read_bytes(path, root)
    top = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_Pairs)
    if not isinstance(top, _Pairs):
        raise C1GateFailure(IDENT, "TRAIN_RECORD is not an object")
    kept = {k: _plain(v) for k, v in top if k in TRAIN_KEYS}  # other keys (dev_ce) dropped
    missing = [k for k in TRAIN_KEYS if k not in kept]
    if missing:
        raise C1GateFailure(IDENT, f"TRAIN_RECORD lacks {missing}")
    return kept


def stage_complete_sha(store, stage, relpath):
    want = None
    for ln in uc.read_bytes(Path(store) / "STAGES.jsonl").decode("utf-8-sig").splitlines():
        if not ln.strip():
            continue
        e = json.loads(ln)
        if e.get("stage") == stage and e.get("event") == "STAGE_COMPLETE":
            want = e.get("files", {}).get(relpath, want)
    return want


def checkpoint_meta_u(artifact_root, artifact_id) -> dict:
    try:
        meta = uc.read_json(Path(artifact_root) / "Checkpoint" / str(artifact_id) / "meta.json")
    except (OSError, ValueError) as exc:
        raise C1GateFailure(IDENT, f"checkpoint meta {artifact_id}: {exc!r}") from exc
    if not isinstance(meta, dict):
        raise C1GateFailure(IDENT, f"checkpoint meta {artifact_id} is not an object")
    return meta


def load_checkpoint_u(artifact_root, artifact_id):
    store = tpc.ArtifactStore(tpb.LocalFSBackend(Path(artifact_root)))
    return store.load(tpc.Checkpoint, artifact_id, consumer="experiment")


def identity_c(hwsc_store, handoff, contract=None) -> dict:
    C, store = _c(contract), Path(hwsc_store)
    recs, metas, ids = {}, {}, {}
    for j in uc.MASTERS:
        tr = C["train_records"][str(j)]
        p = store / tr["relpath"]
        sha = uc.sha256_file(p)
        if sha != tr["sha256"] or sha != stage_complete_sha(store, tr["stage"], tr["relpath"]):
            raise C1GateFailure(IDENT, f"TRAIN_RECORD {j} differs from CONTRACT/STAGE_COMPLETE")
        rec = read_train_record(p)
        if rec["status"] != "COMPLETE" or rec["checkpoint_ids"].get("5000") != C[
                "checkpoint_ids"][str(j)]:
            raise C1GateFailure(IDENT, f"TRAIN_RECORD {j}: status or checkpoint id")
        exp = hwsc_gates.expected_meta_c(j, C["step"], rec)
        meta = checkpoint_meta_u(store / "artifacts", exp["artifact_id"])
        chk = k4b_config.check_checkpoint_meta(meta, exp)
        if chk["status"] != "PASS":
            raise C1GateFailure(IDENT, f"checkpoint meta {j}: {chk}")
        recs[j], metas[j], ids[j] = rec, chk, exp["artifact_id"]
    if not hwsc_gates.exclusion_check(list(ids.values()), handoff)["ok"]:
        raise C1GateFailure(IDENT, "a checkpoint id is in stage_c_exclusions")
    return {"records": recs, "meta": metas, "ids": ids}


def charts_identity(hwsc_store, contract=None) -> dict:
    C, store = _c(contract), Path(hwsc_store)
    pf = C["production_frozen"]
    p = store / pf["relpath"]
    if uc.sha256_file(p) != pf["sha256"]:
        raise C1GateFailure(IDENT, "PRODUCTION_FROZEN.json differs from CONTRACT")
    rec = uc.read_json(p)
    for name, want in pf["charts"].items():
        got = uc.sha256_file(p.parent / name)
        if got != want or rec.get("files", {}).get(name) != want:
            raise C1GateFailure(IDENT, f"{name} differs from CONTRACT/record")
    if rec.get("gauges") != pf["gauges"]:
        raise C1GateFailure(IDENT, "chart gauges differ from the CONTRACT copy")
    return {"production_frozen": pf["sha256"], "charts": dict(pf["charts"]),
            "gauges": rec["gauges"]}


def load_stage_c(hwsc_store, ident, contract=None) -> dict:
    torch.set_num_threads(1)
    if torch.get_num_threads() != 1:
        raise C1GateFailure(IDENT, "torch threads != 1")
    out = {}
    for j in uc.MASTERS:
        ck = load_checkpoint_u(Path(hwsc_store) / "artifacts", ident["ids"][j])
        model64, sha = c1_model.load_model64(ck)
        out[j] = {"model64": model64, "state_sha": sha, "checkpoint_id": ident["ids"][j]}
    return out


# ------------------------------------------------------ inputs, activations, readout
def named_inputs(canon32, perm):
    return c1_model.model_inputs(np.asarray(perm)[np.asarray(canon32, dtype=np.int64)])


def basis_u(model64) -> dict:
    return c2_model.readout_basis(model64)


def readout_y(model64, canon32, perm, basis, batch=1024) -> np.ndarray:
    acts = c2_model.activations3(model64, named_inputs(canon32, perm), batch)
    y = c2_model.readout_coords(acts["ln_final_out"], basis)
    del acts
    return y


def a_full(d_named, M, y1, y2) -> np.ndarray:
    return c2_attrib.half_dot(d_named, (np.asarray(y1) - np.asarray(y2)) @ np.asarray(M).T)


def response_arrays(A, G) -> dict:
    A, G = np.asarray(A, dtype=np.float64), np.asarray(G, dtype=np.float64)
    return {"ZR010": A - float(uc.RESP_LO) * G, "ZR030": A - float(uc.RESP_HI) * G, "AF": A}


def row_cross_check(q1bar_named, q4bar_named, y1, basis) -> np.ndarray:
    z1 = c2_model.closed_logits(y1, basis)
    return np.sum((np.asarray(q1bar_named) - np.asarray(q4bar_named)) * z1, axis=1)


def named_d(d_canon, perm):
    return c1_oracle.named_from_canonical(d_canon, perm)


# ------------------------------------------------------------------------------ policy
class UPolicy:
    def __init__(self, done=()):
        self.done, self.current, self.passed = list(dict.fromkeys(done)), None, set()

    def begin(self, gate) -> None:
        if gate not in GATE_ORDER_U:
            raise C1GateFailure(BIND, f"gate {gate} not in the logit order")
        pos = max((GATE_ORDER_U.index(g) for g in self.done if g in GATE_ORDER_U), default=-1)
        if self.current is not None or GATE_ORDER_U.index(gate) < pos:
            raise C1GateFailure(BIND, f"gate {gate} out of order ({self.current})")
        self.current = gate
        self.done += [] if gate in self.done else [gate]

    def end(self, gate) -> None:
        self.current = None

    def mark_pass(self, gate) -> None:
        self.passed.add(gate)

    def require(self, kind) -> None:
        tpre = kind != "test_endpoint" or "T-PRE" in self.passed
        if self.current not in ALLOWED_U.get(kind, ()) or not tpre:
            raise C1GateFailure(BIND, f"{kind} logits refused at {self.current}")


# ------------------------------------------------------------------ BASIS, M0, X1
def basis_gate(models, fit_canon, perm_of, policy) -> dict:
    out = {}
    for j, m in models.items():
        b = basis_u(m["model64"])
        if not b["rank_ok"]:
            raise C1GateFailure(MODEL, f"model {j}: readout rank")
        policy.begin("BASIS")
        acts, z = c2_model.natural_pass(m["model64"], named_inputs(fit_canon[:1024], perm_of[j]),
                                        policy, "basis")
        y = c2_model.readout_coords(acts["ln_final_out"], b)
        kappa = c2_model.kappa_x1(acts["ln_final_out"], y, b, z)
        ok = c2_model.x1_attainable(kappa)
        del z, acts
        policy.end("BASIS")
        if not ok:
            raise C1GateFailure(MODEL, f"model {j}: X1 attainability, kappa {kappa}")
        out[j] = {"rank_ok": True, "R_diag_min_max": [float(b["R_diag"].min()),
                                                      float(b["R_diag"].max())],
                  "kappa_x1": kappa, "attainable": ok}
    return {"per_model": out}


def m0_u(model64, sha, ident_j, inputs, acts, z_net, basis, d_canon, perm, policy,
         contract=None) -> dict:
    policy.require("m0")
    j = ident_j.get("master")
    y = c2_model.readout_coords(acts["ln_final_out"], basis)
    checks = {"ids": ident_j["checkpoint_id"] == _c(contract)["checkpoint_ids"].get(str(j)),
              "state_sha": str(sha) == str(ident_j["state_sha"]), "roundtrip": True}
    patch = c2_model.identity_patch(model64, inputs, acts, policy)
    checks.update(identity=all(patch.values()), rank=bool(basis["rank_ok"]))
    rid = c2_model.readout_identity(z_net, y, basis)
    d_named = named_d(d_canon, perm)
    route = c2_model.two_route(d_canon, d_named, z_net, perm)
    kappa = c2_model.kappa_x1(acts["ln_final_out"], y, basis, z_net)
    checks.update(readout=rid["ok"], two_route=route["ok"],
                  symbol_a=c2_model.symbol_order_a(inputs, ident_j["canon32"], perm),
                  symbol_b=c2_model.symbol_order_b(perm),
                  symbol_c=c2_model.symbol_order_c(d_canon, perm),
                  attainable=c2_model.x1_attainable(kappa))
    ok = all(v for k, v in checks.items() if k != "attainable")
    status = MODEL if not ok else "PASS" if checks["attainable"] else "INCONCLUSIVE/NUMERICAL"
    return {"status": status, "checks": checks,
            "values": {"model": j, "patch": patch, "readout": rid, "two_route": route,
                       "kappa_x1": kappa}}


def m0_gate(models, ident, val_a1, perm_of, d_canon, policy) -> dict:
    out = {}
    policy.begin("M0")
    for j, m in models.items():
        canon = np.asarray(val_a1)[:1024]
        inputs = named_inputs(canon, perm_of[j])
        acts, z = c2_model.natural_pass(m["model64"], inputs, policy, "m0")
        ij = {"master": j, "checkpoint_id": ident["ids"][j], "state_sha": m["state_sha"],
              "canon32": canon}
        r = m0_u(m["model64"], m["state_sha"], ij, inputs, acts, z, basis_u(m["model64"]),
                 np.asarray(d_canon)[:1024], perm_of[j], policy)
        del z, acts
        out[j] = r
        if r["status"] != "PASS":
            policy.end("M0")
            raise C1GateFailure(r["status"], f"M0 model {j}: {r['checks']}")
    policy.end("M0")
    return out


def x1_gate(models, val, perm_of, basis_of, policy) -> dict:
    out, over = {}, []
    policy.begin("X1")
    for j, m in models.items():
        arms = {}
        for k in ("a1", "a2"):
            inputs = named_inputs(val[k], perm_of[j])
            acts, z = c2_model.natural_pass(m["model64"], inputs, policy, "x1")
            y = c2_model.readout_coords(acts["ln_final_out"], basis_of[j])
            arms[f"{j}:{k}"] = (inputs, y, z, val[f"ids_{k}"])
            del acts
        r = c2_model.x1(m["model64"], arms, basis_of[j], policy)
        del arms
        out.update({n: {"max_dev": a["max_dev"], "n_over": a["n_over"]}
                    for n, a in r["arms"].items()})
        over += r["ids_over"]
        if r["status"] != "PASS":
            policy.end("X1")
            raise C1GateFailure(X1F, f"X1 model {j}: {r['arms']}")
    policy.end("X1")
    return {"arms": out, "ids_over": sorted(set(over))}


def write_json(path, obj) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(p, json.loads(json.dumps(obj, default=str)))
    return p
