"""HWSU model-phase dry run: the stage jobs KC, E1, REG2 and E2 through run_job on a synthetic
store (API_U2.md section 6, DRU1; R-0223-9 part 1; the HWSC/HWSG planted-adapter precedent).

Every gate of a job runs the real kernel on the tiny world unless it is listed in `planted`;
the record names both sets. A planted adapter stands in for a gate whose input is a real object
the synthetic store cannot hold (stage-C identities, real OF files, real checkpoints, the
geometry of the production world). Synthetic roots only, scope hwsu-dry-v1.
"""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_dry as udry
import hwsc_data
import hwsc_dry
import hwsu_driver as udrv
import hwsu_oracle as uo
import hwsu_records as ur
import u2  # noqa: F401
import hashlib
import json
import time
from pathlib import Path

import c1_means
import numpy as np
import stage_records
import topo_pilot.learner as tpl
import torch


def _w(path, data) -> Path:
    return udry._w(path, data)


def synthetic_root_u(base) -> dict:
    """The phase-1 synthetic root with the phase-2 authority fixtures added."""
    sr = udry.synthetic_root(base)
    C, mb = sr["contract"], sr["mailbox"]
    A2 = C["authority_u2"]
    for a in A2["addenda"].values():
        a["sha256"] = udry._h(_w(mb / a["path"], f"fixture addendum {a['addendum']}\n"))
    ra = A2["run_approval"]
    ra["sha256"] = A2["addenda"][str(ra["addendum"])]["sha256"]
    ra["path"] = A2["addenda"][str(ra["addendum"])]["path"]
    return sr


def of_fixture(store, sr) -> dict:
    """Synthetic OF store files: FREEZE_OF, OF_ACCEPT, OF_REPORT and two blocks of OF eval pairs
    on the tiny world, hashed into an OF_S STAGE_COMPLETE; the patched contract carries their
    hashes (planted input: the real OF files are not available to a dry store)."""
    store, C = Path(store), sr["contract"]
    A = C["authority_u2"]
    ac = A["of_accept"]
    store.mkdir(parents=True, exist_ok=True)
    fz = store / "FREEZE_OF.json"
    stage_records.write_new(fz, {"fixture": True})
    fzs = stage_records.sha256(fz)
    w = udry.tiny_world()
    arms, files = {"a1": [], "a2": []}, []
    for b in uc.BLOCKS_OF:
        _, pr = udry.tiny_pairs(256, block=b)
        for arm in ("a1", "a2"):
            f = store / "stages" / "OF" / f"DRYHIST_OF_eval_{arm}_b{b}.npz"
            f.parent.mkdir(parents=True, exist_ok=True)
            np.savez(f, canon32=np.asarray(pr[arm]))
            arms[arm].append(np.asarray(pr[arm]))
            files.append(f)
    o = {a: uo.arm_oracle(w["T"], w["E_canon_shared"], w["pi"], np.concatenate(arms[a]),
                          w["coords"]) for a in arms}
    G = uo.pair_core(o["a1"], o["a2"])["G"]
    rep = store / "stages" / "OF" / "OF_REPORT.json"
    stage_records.write_new(rep, {"EG": {"point": float(c1_means.tree_mean(G)),
                                      "L": 0.5 * float(c1_means.tree_mean(G))}})
    ur.complete_stage(store, "OF_S", files + [rep])
    acc = store / "OF_ACCEPT.json"
    stage_records.write_new(acc, {
        "schema": "fixture", "verdict": "ACCEPT", "outcome": "OF_PASS_RESPONSE_ONLY",
        "N_resp": 4096, "freeze_of_sha256": fzs, "of_report_sha256": stage_records.sha256(rep),
        "h_exec": "0" * 40})
    ac.update(sha256=stage_records.sha256(acc), freeze_of_sha256=fzs,
              of_report_sha256=stage_records.sha256(rep))
    A["freeze_of"]["sha256"] = fzs
    return {"world": w}


def registry_sources() -> dict:
    """Planted registry sources (hwsc_dry stubs): the stores of earlier studies are not scanned."""
    src = hwsc_dry.stub_sources(("a" * 63 + "1", "b" * 63 + "2"))
    src["own"] = src["dry"]
    for t in ("hwsc", "hwsu_dry", "hwsd"):
        src[t] = src["dry"]
    src["kreg2_c"] = lambda: {"status": "PASS", "digests": np.array([], dtype="<U64"),
                              "seq_ids": np.array([], dtype=np.int64), "n": 0}
    return src


def _kc2(ctx) -> dict:
    ids = {j: ctx["contract"]["stage_c_u2"]["checkpoint_ids"][str(j)] for j in uc.MASTERS}
    return {"ids": ids, "no_checkpoint_loaded": True, "planted": True}


def _h1u(ctx) -> dict:
    """Three random-init 4-layer models stand in for the stage-C checkpoints."""
    cfg = tpl.ModelConfig(vocab_in=37, vocab_out=36, n_ctx=33, n_layers=4, d_model=128,
                          n_heads=4, d_mlp=512)
    models, perm_of, ids = {}, {}, {}
    for i, j in enumerate(uc.MASTERS):
        torch.manual_seed(649910 + i)
        ids[j] = ctx["contract"]["stage_c_u2"]["checkpoint_ids"][str(j)]
        models[j] = {"model64": tpl.TransformerLM(cfg).double().eval(), "state_sha": "0" * 64,
                     "checkpoint_id": ids[j]}
        perm_of[j] = np.random.default_rng(649910 + i).permutation(36)
    ctx.update(models=models, ident={"ids": ids}, perm_of=perm_of)
    return {"ids": ids, "planted": True}


def _h5u(ctx) -> dict:
    """H5-U headroom is a property of the production geometry; the tiny world has none."""
    return {"planted": True, "reason": "tiny-world headroom is not the production quantity"}


def stage_extra(sr) -> dict:
    """Dry-only seams of the E2 job: the stage-C loader (planted models) and the H5 floor."""
    return {"stage_c_loader": _h1u, "h5_floor": 0}


def planted_default(sr) -> dict:
    return {"KC2": _kc2, "H1-U": _h1u, "H5-U": _h5u}


def write_auth(store, job, stage, sr) -> Path:
    store = Path(store)
    store.mkdir(parents=True, exist_ok=True)
    fz = store / "FREEZE.json"
    if not fz.exists():
        stage_records.write_new(fz, {"fixture": True})
    ra = sr["contract"]["authority_u2"]["run_approval"]
    f = store / f"AUTH_U_{job}.json"
    stage_records.write_new(f, {
        "stage": stage, "owner_approval": {"path": ra["path"], "sha256": ra["sha256"]},
        "freeze_sha256": stage_records.sha256(fz)})
    return f


def stage_ctx(store, sr, job, stage, planted, **extra) -> dict:
    rid = extra.pop("reservation_id", None)
    ctx = udrv.build_ctx_u(store, job, 1, stage, rid, root=sr["root"], mailbox=sr["mailbox"],
                           hwsc_store=sr["hwsc_store"], scope=uc.SCOPE_DRY, dry=True)
    p = float(hwsc_data.p_d2a_check(udry.tiny_world(), 1.0)["p_D2a"])
    ho = _w(sr["root"] / "handoff.json", json.dumps({
        "p_D2a": p, "stage_c_exclusions": [], "store_inventory": {}}))
    (sr["root"] / "scratch").mkdir(parents=True, exist_ok=True)
    ctx.update(proc=udry.tiny_world(), block_n=512, draws=200, decimal_rows=2,
               contract=sr["contract"], dry_skip_s0=True, handoff_path=ho,
               handoff_sha256=udry._h(ho), scratch=sr["root"] / "scratch", planted_u2=planted,
               registry_sources=registry_sources(), **stage_extra(sr))
    ctx.update(extra)
    return ctx


def prepare(store, stage, rid) -> None:
    """Coordinator-side files of a drawing job: reservation and the release record."""
    store = Path(store)
    if not (store / ur.reservation_file(rid)).exists():  # E2 continues the reservation of E1
        ur.write_reservation(store, rid, uc.SCOPE_DRY, ur.utc(), "hwsu_dry2c")
    if stage == "E2":
        p1 = json.loads((store / "stages" / "E1" / "VALIDATION_REPORT.json").read_text(
            encoding="utf-8"))["p1"]
        acc = store / "ACCEPT_VALIDATION.json"
        stage_records.write_new(acc, {"fixture": True})
        reg = store / "registry"
        stage_records.write_new(store / "RELEASE_B.json", {
            "reservation_id": rid, "freeze_sha256": stage_records.sha256(store / "FREEZE.json"),
            "k_reg2": {"manifest_sha256": stage_records.sha256(reg / "K-REG2.json"),
                       "digest_file_sha256": stage_records.sha256(reg / "K-REG2_digests.npz")},
            "worker_session": "dru", "N": p1["N"], "k": p1["k"],
            "accept_sha256": stage_records.sha256(acc)})
    if stage == "E1":
        reh = store / "registry" / "rehearsal" / "REHEARSAL.json"
        stage_records.write_new(store / "RELEASE_A.json", {
            "reservation_id": rid, "freeze_sha256": stage_records.sha256(store / "FREEZE.json"),
            "completeness_certificate": {"rehearsal_manifest_sha256": stage_records.sha256(reh)}})


def run_stage(store, sr, job, stage, planted, reservation_id=None, dry_continue=True,
              **extra) -> dict:
    if not (Path(store) / "FREEZE_OF.json").exists():
        of_fixture(store, sr)
    write_auth(store, job, stage, sr)
    if reservation_id is not None:
        prepare(store, stage, reservation_id)
    ctx = stage_ctx(store, sr, job, stage, planted, reservation_id=reservation_id, **extra)
    res = udrv.run_job(stage, store, job, reservation_id=reservation_id, ctx=ctx,
                       dry_continue=dry_continue)
    got = {r["gate"]: r["status"] for r in res["records"]}
    return {"result": res, "gates": got, "planted": sorted(planted), "ctx": ctx}


PLANTED_INPUTS = {
    "KC2": "stage-C identities (TRAIN_RECORD, checkpoint meta): ids from the patched CONTRACT",
    "H1-U": "three random-init 4-layer models (seeds 649910-649912) in place of the checkpoints",
    "H5-U": "headroom is a property of the production geometry; the tiny world has none",
    "T-PRE loader": "the same planted models and ids (stage_c_loader); H5 floor 0 at TEST",
    "registry sources": "hwsc_dry stub sources (KC5, REG1, REG2); the stores of earlier studies "
                        "are not scanned",
    "OF files": "synthetic OF_ACCEPT, FREEZE_OF, OF_REPORT and eval blocks from the tiny world, "
                "hash-chained through OF_S STAGE_COMPLETE and the patched CONTRACT",
    "coordinator files": "FREEZE.json, AUTH_U_<job>, RELEASE_A/B, ACCEPT_VALIDATION, reservation",
    "process": "udry.tiny_world (W=6, H=2, L=32, V=36) with a handoff p_D2a computed on it",
    "sizes": "block_n 512, 200 draws, 2 Decimal rows"}


def run_stages(base) -> dict:
    """KC, E1, REG2 and E2 through run_job on one synthetic store (R-0223-9 part 1)."""
    base = Path(base)
    sr = synthetic_root_u(base / "root")
    tag = hashlib.sha1(str(base).encode()).hexdigest()[:8]
    store = uc.SCRATCH / f"hwsu-dry-u2-{tag}-{time.time_ns() % 10**9}"
    planted = planted_default(sr)
    out, stages = {}, {}
    for stage, rid in (("KC", None), ("E1", "RES-HWSU-U"), ("REG2", None), ("E2", "RES-HWSU-U")):
        r = run_stage(store, sr, f"DRU1-{stage}", stage, planted, reservation_id=rid)
        stages[stage] = r["gates"]
        out[stage] = r["result"]["outcome"]
    ran = {s: [g for g in gs if g not in planted] for s, gs in stages.items()}
    share_ok = all(v == "NOT_RUN/SHARE_DROPPED" for g in ("SUP", "F1", "L1", "R1-U", "DX")
                   for v in [stages["E1"][g]])
    good = (out["KC"] == "KC_PASS" and out["E1"] == "E1_PASS" and out["REG2"] == "REG2_PASS"
            and not out["E2"].startswith(("FAIL_TECHNICAL", "INVALID", "INCONCLUSIVE"))
            and all(v in ("PASS", "NOT_RUN/SHARE_DROPPED") for gs in stages.values()
                    for v in gs.values()))
    names = [p.name for p in store.rglob("*.npz")]
    return {"ok": good and share_ok and not any(n.startswith("HIST_") for n in names),
            "store": str(store), "outcomes": out, "gates": stages,
            "kernels_run_directly": ran, "planted_adapters": sorted(planted),
            "planted_inputs": PLANTED_INPUTS}
