"""HWSU model-phase dry run DRU, response family (API_U2.md section 6; protocol 9).

Synthetic worlds and roots only, scope hwsu-dry-v1, nothing under the project root. This file
holds the cases that train tiny models or call the builder of stage C (DRU1, DRU2, DRU-REG): the
only file that may reference hwsb_train.train, hwsc_data.make_train_dev_c and
hwsc_registry_build.build (R-0223-3). The other cases live in hwsu_dry2b (split by size) and are
re-exported here.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_dry2b as d2b
import hwsu_dry2c as d2c
import hwsu_dry2d as d2d
import hwsu_freeze as ufz
import hwsu_known as uk
import hwsu_model as um
import hwsu_records as ur
import hwsu_registry as ureg
import hwsu_dry as udry
import u2  # noqa: F401
import json
from pathlib import Path

import c1_model
import c2_model
import hwsb_config
import hwsb_dry
import hwsb_train
import hwsc_data
import hwsc_dry
import hwsc_registry_build
import numpy as np
import stage_records
import topo_pilot.contracts as tpc
import topo_pilot.contracts.backends as tpb
import topo_pilot.learner as tpl
import torch

_res = d2b._res
ks_p, ks_rules = d2b.ks_p, d2b.ks_rules
dru3, dru4, dru5, dru6, dru7, dru8, dru9 = (d2b.dru3, d2b.dru4, d2b.dru5, d2b.dru6, d2b.dru7,
                                            d2b.dru8, d2b.dru9)
CASES = ("dru1", "dru2", "dru3", "dru4", "dru5", "dru6", "dru7", "dru8", "dru9", "dru_reg")
DRU_SITE = "resid_post_0"  # the tiny model has one layer (hwsb tiny_site)


def tiny_plan(case="DRU1"):
    """The tiny training plan: CONTRACT dry_run_u2 tiny_model / tiny_train / tiny_masters, sizes
    train and dev only (R-0223-7 b)."""
    d = uc.CONTRACT["dry_run_u2"]
    tt = dict(d["tiny_train"])
    tt["checkpoint_steps"] = tuple(int(s) for s in tt["checkpoint_steps"])
    sizes = {k: int(d["tiny_sizes"][k]) for k in ("train", "dev")}
    return hwsb_config.Plan("dry_tiny", tuple(int(m) for m in d["tiny_masters"]),
                            tpl.ModelConfig(**d["tiny_model"]), tpl.TrainConfig(**tt), sizes,
                            DRU_SITE, str(case), ("cylinder", "overlap", "1.0"),
                            int(tt["steps"]), 0)


class DryMasters:
    """Dry-only rebinding of hwsb_config.DRY_MASTERS (CONTRACT binding.dry_rebinding_u2).

    hwsb_data admits only hwsb_config.DRY_MASTERS for a dry plan; U's tiny masters (OPEN-6) are
    admitted inside the with block. The constant is set on entry and restored on exit, also when
    the block raises; synthetic training only (R-0223-9 part 2)."""

    def __init__(self, masters):
        self.masters, self.old = tuple(int(m) for m in masters), None

    def __enter__(self):
        self.old = hwsb_config.DRY_MASTERS
        hwsb_config.DRY_MASTERS = self.masters
        return self

    def __exit__(self, *exc):
        hwsb_config.DRY_MASTERS = self.old
        return False


def _train_one(store, proc, plan, m) -> dict:
    with DryMasters(plan.masters):
        obs = hwsc_data.make_train_dev_c(store, proc, m, plan, scope=uc.SCOPE_DRY)
        return hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, m, plan=plan)


def tiny_models(store, proc, plan=None) -> dict:
    """Three tiny models trained by hwsb_train.train on make_train_dev_c ObservationSets under
    the dry scope; the record keeps no dev_ce."""
    plan = plan or tiny_plan()
    out = {}
    for m in plan.masters:
        res = _train_one(store, proc, plan, m)
        out[int(m)] = {"master": int(m), "status": "COMPLETE", "run_key": res["run_key"],
                       "checkpoint_ids": {str(k): v for k, v in res["checkpoint_ids"].items()},
                       "checksums": {str(k): v for k, v in res["checksums"].items()}}
    return out


def dru1(base, ctx=None) -> dict:
    """The tiny world with real training: three tiny models, their checkpoints, TRAIN_RECORD
    fixtures through the stage-C reader, the readout basis of each trained model."""
    base = Path(base)
    plan, r = tiny_plan(), {}
    store = tpc.ArtifactStore(tpb.LocalFSBackend(base / "artifacts"))
    proc = hwsb_dry.build_tiny_process(store, masters=plan.masters)
    recs = tiny_models(store, proc, plan)
    steps = [str(s) for s in plan.train_cfg.checkpoint_steps]
    r["steps"] = all(sorted(v["checkpoint_ids"]) == sorted(steps) for v in recs.values())
    ids = {v["checkpoint_ids"][str(plan.gate_step)] for v in recs.values()}
    r["distinct"] = len(ids) == len(recs)
    r["trained"] = all(v["checkpoint_ids"]["0"] != v["checkpoint_ids"][str(plan.gate_step)]
                       for v in recs.values())
    ok = {}
    for m, v in recs.items():
        ck = store.load(tpc.Checkpoint, v["checkpoint_ids"][str(plan.gate_step)],
                        consumer="experiment")
        model64, _ = c1_model.load_model64(ck)
        ok[m] = bool(um.basis_u(model64)["rank_ok"])
        p = base / "stages" / "TRAIN" / str(m) / "TRAIN_RECORD.json"
        um.write_json(p, dict(v, dev_ce={"1": 0.5}))
        back = um.read_train_record(p, root=base)
        ok[f"{m}:record"] = "dev_ce" not in back and back["status"] == "COMPLETE"
    r["rank_and_record"] = all(ok.values())
    r["no_hist_name"] = not any(p.name.startswith("HIST_") for p in base.rglob("*.npz"))
    stg = d2c.run_stages(base / "stages_job")
    r["run_job_stages"] = stg
    return _res(all(v for k, v in r.items() if k != "run_job_stages") and stg["ok"], **r)


def dru2(base, ctx=None) -> dict:
    """Real architecture, random init (seed 649910), 2,048 in-memory w* DRY pairs: BASIS, M0, X1
    through the model-part gates and A_full against the closed-form half dot."""
    cfg = tpl.ModelConfig(vocab_in=37, vocab_out=36, n_ctx=33, n_layers=4, d_model=128, n_heads=4,
                      d_mlp=512)
    torch.manual_seed(649910)
    model64 = tpl.TransformerLM(cfg).double().eval()
    n, j = int(uc.CONTRACT["dry_run_u2"]["dru2"]["pairs"]), 649907
    o1, o2, s1, s2, pc = d2b._ko_world(n)
    _, pr = udry.tiny_pairs(n)
    perm = np.random.default_rng(649910).permutation(36)
    C = json.loads(json.dumps(uc.CONTRACT))
    C["stage_c_u2"]["checkpoint_ids"] = {str(j): "dru2-random-init"}
    models, policy = {j: {"model64": model64, "state_sha": "0" * 64}}, um.UPolicy()
    r = {"basis": um.basis_gate(models, pr["a1"], {j: perm}, policy)["per_model"][j]}
    b = um.basis_u(model64)
    canon = np.asarray(pr["a1"])[:1024]
    policy.begin("M0")
    inputs = um.named_inputs(canon, perm)
    acts, z = c2_model.natural_pass(model64, inputs, policy, "m0")
    ident = {"master": j, "checkpoint_id": "dru2-random-init", "state_sha": "0" * 64,
             "canon32": canon}
    m0 = um.m0_u(model64, "0" * 64, ident, inputs, acts, z, b, np.asarray(pc["d"])[:1024], perm,
                 policy, contract=C)
    policy.end("M0")
    del acts, z
    r["m0"] = m0["status"]
    x1 = um.x1_gate(models, pr, {j: perm}, {j: b}, policy)
    r["x1_n_over"] = sum(a["n_over"] for a in x1["arms"].values())
    y1, y2 = (um.readout_y(model64, pr[a], perm, b) for a in ("a1", "a2"))
    d_named = um.named_d(pc["d"], perm)
    A = um.a_full(d_named, b["M"], y1, y2)
    z1, z2 = c2_model.closed_logits(y1, b), c2_model.closed_logits(y2, b)
    ref = 0.5 * np.sum(d_named * (z1 - z2), axis=1)
    tol = 1e-9 * max(1.0, float(np.max(np.abs(z1))), float(np.max(np.abs(z2))))
    r["a_full_dev"] = float(np.max(np.abs(A - ref)))
    ok = (b["rank_ok"] and m0["status"] == "PASS" and x1["ids_over"] == []
          and r["a_full_dev"] <= tol)
    return _res(ok, **r)


EQ_KEYS = ("status", "problems", "n_digests", "digests_sha256", "seq_id_union_sha256", "x6",
           "union_sha256", "sources", "classes", "coverage", "predicates", "inventory",
           "sealed_ranges", "d2a_ranges", "handoff_validation", "version", "known_gaps")


def _build_equality(base) -> dict:
    """build_u equals hwsc_registry_build.build on a synthetic root with stage C's source map
    (R-0223-7 c): same sources, empty U-only sources; the common manifest fields and the digest
    file contents are compared."""
    base = Path(base)
    syn = hwsc_dry.synthetic_root(base / "syn")
    dig = ("a" * 63 + "1", "b" * 63 + "2", "c" * 63 + "3")
    src = hwsc_dry.stub_sources(dig)
    src["own"] = src["dry"]
    handoff = {"store_inventory": {}, "N_C": 3072, "Z_bound": None, "F_plan": None,
               "p_D2a": 1e-15, "stage_c_exclusions": ()}
    empty = src["dry"]
    extra = {t: empty for t in ("hwsc", "hwsu_dry", "hwsd")}
    extra["kreg2_c"] = lambda: {"status": "PASS", "digests": np.array([], dtype="<U64"),
                                "seq_ids": np.array([], dtype=np.int64), "n": 0}
    ma = hwsc_registry_build.build("K-REG1", base / "a" / "reg", root=syn["root"],
                                   scratch=syn["scratch"], handoff=handoff, own_expected={},
                                   sources=src)
    mb = ureg.build_u("K-REG1", base / "b" / "reg", syn["root"], syn["scratch"], handoff,
                      own={}, sources={**src, **extra})
    same = {k: ma.get(k) == mb.get(k) for k in EQ_KEYS}
    npz = []
    for d in ("a", "b"):
        with np.load(base / d / "reg" / "K-REG1_digests.npz", allow_pickle=False) as z:
            npz.append((z["digests"].astype(str).tolist(), z["seq_ids"].tolist()))
    same["digest_file"] = npz[0] == npz[1] and len(npz[0][0]) >= len(dig)
    same["status_pass"] = ma["status"] == "PASS" == mb["status"]
    return same


def dru_reg(base, ctx=None) -> dict:
    base, r = Path(base), {}
    base.mkdir(parents=True, exist_ok=True)
    store = base / "store"
    (store / "reservations").mkdir(parents=True, exist_ok=True)
    ob = store / "REGISTRY_OBLIGATION.json"
    ob.write_text("{}", encoding="utf-8")
    rec = {"obligation_file": "REGISTRY_OBLIGATION.json"}
    e = store / "reservations" / "X.END.json"
    r["store_relative"] = uk.end_obligation_path(rec, e, base) == store / "REGISTRY_OBLIGATION.json"
    r["outside_is_live"] = uk.end_obligation_path({"obligation_file": "../../x.json"}, e,
                                                  base) is None
    (base / "x.json").write_text("{}", encoding="utf-8")
    r["s2"] = ureg.superset_diagnostic(np.array(["a" * 64, "c" * 64]), np.array(
        ["a" * 64, "b" * 64]))["n_missing"] == 1
    dry = base / "hwsd-dry-fixture"
    dry.mkdir(exist_ok=True)
    np.savez(dry / "HIST_x.npz", canon32=np.zeros((1, 32), dtype=np.uint8))
    r["no_obligation_incomplete"] = ureg.read_obligation_u2(dry)["status"] == ureg.INC
    eq = _build_equality(base / "equality")
    r["equality_with_build"] = all(eq.values())
    fx = d2d.fixtures(base / "fixtures")
    r["planted_defect_fixtures"] = fx["ok"]
    return _res(all(r.values()), equality=eq, fixtures=fx, **r)


def run_dru(out, only=None) -> dict:
    out = Path(out)
    try:
        out.resolve().relative_to(uc.ROOT.resolve())
        return {"status": "REFUSED", "reason": "dry store under the project root"}
    except ValueError:
        pass
    if not uc.dry_store_ok(out) or not out.name.startswith("hwsu-dry"):
        return {"status": "REFUSED", "reason": "not X:/Downloads/topo-scratch/hwsu-dry*"}
    job = out.name.replace("hwsu-dry-u2-", "").replace("hwsu-dry-", "")
    work, cases = uc.SCRATCH / f"test_hwsu-{job}", {}
    inv0 = ur.root_inventory(uc.ROOT)
    for name in (only or list(CASES)):
        base = work / name.lower()
        base.mkdir(parents=True, exist_ok=True)
        try:
            cases[name.upper()] = globals()[name.lower()](base)
        except Exception as exc:  # noqa: BLE001  a crashing case is a FAIL
            cases[name.upper()] = {"status": "FAIL", "details": {"exception": repr(exc)[:500]}}
    inv1 = ur.root_inventory(uc.ROOT)
    h = ufz._git(uc.REPO, "rev-parse", "HEAD").decode().strip()
    files = uk.implementation_files_u(uc.REPO, h)
    rep = {"cases": cases, "all_pass": all(c["status"] == "PASS" for c in cases.values())
           and inv0 == inv1, "implementation_files": files,
           "implementation_sha256": ur._canon_sha(files), "h_exec": h,
           "tree_clean": not ufz._git(uc.REPO, "status", "--porcelain", "--",
                                         "tools/hwsu").strip(),
           "inventory_before": inv0, "inventory_after": inv1}
    (out / "stages" / "DRY").mkdir(parents=True, exist_ok=True)
    stage_records.write_new(out / "stages" / "DRY" / "DRY_U2_REPORT.json",
                            json.loads(json.dumps(rep, default=str)))
    ur.write_obligation(out, "REGISTRY_OBLIGATION.json", "DRU", "hwsu_dry2.run_dru", dry=True)
    return rep
