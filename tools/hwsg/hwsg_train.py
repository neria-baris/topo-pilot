"""HWSG parallel training children (API.md §5; protocol §9; G7, DRG12, DRG13, KG4)."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_bind
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import hwsb_registry
import hwsb_train
import hwsc_data
import k4b_driver
import k4b_release
import stage_records
from c1_records import C1GateFailure

RAM_PER_CHILD, RAM_RESERVE = 1610612736, 4294967296
RES = "FAIL_TECHNICAL/RESOURCE"


def _tools_path() -> str:
    return os.pathsep.join(str(gc.REPO / "tools" / s) for s in gc._ORDER)


def child_env(job, out, master=0) -> dict:
    tmp = Path(out) / "tmp" / f"tmp-{job}-{master}"
    env = dict(os.environ)
    env.update(PYTHONPATH=os.pathsep.join([str(gc.REPO / "src"), _tools_path()]),
               OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               NUMEXPR_NUM_THREADS="1", TEMP=str(tmp), TMP=str(tmp), TMPDIR=str(tmp))
    return env


def child_argv(w, master, out, job, attempt, sub="child") -> list:
    return [sys.executable, "-s", "-m", "hwsg_train", sub, "--world", gc.world(w).key,
            "--master", str(int(master)), "--out", str(out), "--job", str(job),
            "--attempt", str(int(attempt))]


def ram_ok(n_children=3, free_bytes=None) -> dict:
    if free_bytes is None:
        import psutil

        free_bytes = int(psutil.virtual_memory().available)
    need = int(n_children) * RAM_PER_CHILD + RAM_RESERVE
    return {"ok": int(free_bytes) >= need, "free_bytes": int(free_bytes), "need_bytes": need}


def _peak_rss():
    try:
        import psutil

        i = psutil.Process().memory_info()
        return int(getattr(i, "peak_wset", 0) or i.rss)
    except Exception:  # noqa: BLE001
        return None


def _files_under(d) -> set:
    d = Path(d)
    return {p for p in d.rglob("*") if p.is_file()} if d.is_dir() else set()


def child(world_key, master, out, job, attempt) -> dict:
    d, master, out = gc.world(world_key), int(master), Path(out)
    wd = gc.world_dir(out, d.tag)
    tdir = wd / "stages" / "TRAIN" / str(master)
    t0, rec = time.process_time(), {"world": d.key, "master": master, "status": "COMPLETE"}
    status = "COMPLETE"
    try:
        with hwsg_bind.world(d.tag):
            import hwsb_config
            import hwsg_oracle

            plan = gc.plan(d.tag)
            hwsb_config.STORE = wd
            store = hwsg_oracle.store_for(wd)
            proc = hwsg_oracle.build_process_g(store, d.tag)
            ident = hwsg_oracle.identity_checker(d.tag)(store, proc)
            if not ident["ok"]:
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"process identity {ident['checks']}")
            obs = hwsc_data.make_train_dev_c(store, proc, master, plan, scope=gc.SCOPE)
            threads = hwsb_train.set_threads(1)
            hold = hwsb_train.HoldRule(tdir, cap_s=gc.HOLD_S, steps=gc.STEPS,
                                       from_step=gc.HOLD_FROM)
            res = hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, master,
                                   plan=plan, hold=hold)
            rk = list(gc.run_key(d.tag, master))
            steps = list(plan.train_cfg.checkpoint_steps)
            if list(res["run_key"]) != rk or sorted(res["checkpoint_ids"]) != sorted(steps):
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "run key or checkpoint steps")
            if res["summary"]["steps_done"] != gc.STEPS:
                raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "steps_done")
            rec.update(run_key=rk, observation_ids={"train": obs["train"], "dev": obs["dev"]},
                       streams=obs["streams"], sequence_id_replicates=obs["replicates"],
                       checkpoint_ids={str(k): v for k, v in res["checkpoint_ids"].items()},
                       checksums={str(k): v for k, v in res["checksums"].items()},
                       summary=res["summary"], threads=threads, holds=res["holds"],
                       process_ids=proc["ids"],
                       dev_ce={str(k): v for k, v in res["dev_ce"].items()})
    except Exception as exc:  # noqa: BLE001
        import hwsg_records

        status = hwsg_records.status_of(exc)
        if status.endswith("NONFINITE") or "NONFINITE" in status:
            status = "FAIL_TECHNICAL/TRAINING"
        if "HOLD" in status or "STOP" in status:
            status = RES
        rec.update(status=status, reason=str(exc)[:2000])
    rec["process_cpu_s"] = cpu = time.process_time() - t0
    tdir.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(tdir / "TRAIN_RECORD.json", json.loads(json.dumps(rec, default=str)))
    logs = wd / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(logs / f"CHILD_{master}_a{int(attempt)}.json",
                            {"master": master, "pid": os.getpid(), "cpu_s": cpu,
                             "peak_rss": _peak_rss(), "status": status, "job": job,
                             "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    return rec


def _next_attempt(wd, master) -> int:
    return len(list((Path(wd) / "logs").glob(f"CHILD_{master}_a*.json"))) + 1


def run_train(out, w, auth, sched, kc_accept, job, launcher=None) -> dict:
    import hwsg_handoff
    import hwsg_records as rec

    out, d = Path(out), gc.world(w)
    wd = gc.world_dir(out, d.tag)
    pf = rec.preflight(out, "TRAIN", auth, sched)
    if pf.get("refused"):
        return pf
    kc = out / "stages" / "KC" / "KG_RECORD.json"
    acc = kc_accept or {}
    if not (acc.get("accept") is True and kc.is_file()
            and acc.get("kc_record_sha256") == stage_records.sha256(kc)
            and gc.read_json(kc).get("status") == "PASS"):
        stage_records.record_gate(out, "KC_ACCEPT", "REFUSED")
        return {"refused": True, "reason": "KC_ACCEPT"}
    stage_records.record_gate(out, "KC_ACCEPT", "PASS")
    try:
        hwsg_handoff.load(d.tag, out)
    except C1GateFailure as exc:
        stage_records.record_gate(out, "HANDOFF", "REFUSED", reason=exc.reason)
        return {"refused": True, "reason": "WORLD_HANDOFF absent or invalid"}
    ram = ram_ok(len(d.masters))
    if not ram["ok"]:
        stage_records.record_gate(out, "RAM", "REFUSED", **ram)
        return {"refused": True, "reason": "RAM", "ram": ram}
    stage_records.record_gate(out, "RAM", "PASS", **ram)
    before = _files_under(wd / "artifacts")
    launcher = launcher or (lambda argv, env: subprocess.Popen(argv, env=env, cwd=gc.REPO))
    procs, attempts = {}, {}
    for m in d.masters:
        tdir = wd / "stages" / "TRAIN" / str(m)
        attempts[m] = _next_attempt(wd, m)
        if tdir.is_dir() and any(tdir.iterdir()):
            k4b_release.archive_attempt(wd, f"{job}-{m}-a{attempts[m] - 1}",
                                        sorted(p for p in tdir.rglob("*") if p.is_file()), {})
        env = child_env(job, out, m)
        Path(env["TEMP"]).mkdir(parents=True, exist_ok=True)
        procs[m] = launcher(child_argv(d.tag, m, out, job, attempts[m]), env)
    for p in procs.values():
        p.wait()
    status, recs = {}, {}
    for m in d.masters:
        f = wd / "stages" / "TRAIN" / str(m) / "TRAIN_RECORD.json"
        status[m] = gc.read_json(f)["status"] if f.is_file() else RES
        recs[m] = f
    world_status = next((s for s in status.values() if s != "COMPLETE"), "COMPLETE")
    for m in d.masters:
        tdir = wd / "stages" / "TRAIN" / str(m)
        fs = [recs[m]] if recs[m].is_file() else []
        fs += sorted(p for p in tdir.glob("HOLD_*") if p.is_file())
        k4b_driver.complete_stage(wd, f"TRAIN_{m}", fs)
    k4b_driver.complete_stage(wd, "TRAIN", sorted(_files_under(wd / "artifacts") - before))
    stage_records.record_gate(wd, f"T_{d.tag}", "PASS" if world_status == "COMPLETE"
                              else world_status, models={str(m): s for m, s in status.items()})
    if world_status == "COMPLETE":
        inv = hwsb_registry.history_inventory(wd)
        f = wd / "stages" / "TRAIN" / "OBS_INVENTORY.json"
        stage_records.write_new(f, inv)
        k4b_driver.complete_stage(wd, "TRAIN_INVENTORY", [f])
    return {"status": world_status, "models": {str(m): s for m, s in status.items()}}


def aggregate(world_dir, job, ledger_path) -> dict:
    import hwsg_records as rec

    wd = Path(world_dir)
    tag = next((t for t in gc.TAGS if gc.WORLDS[t].key == wd.name), wd.name)
    n, led = 0, rec.ledger_read(ledger_path)
    have = {e["label"] for e in led["entries"]}
    for f in sorted((wd / "logs").glob("CHILD_*_a*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        k = int(f.stem.rsplit("_a", 1)[1])
        label = f"{job}-TRAIN-{tag}-{c['master']}-a{k}"
        if label in have:
            continue
        rec.ledger_append(ledger_path, label, job, "TRAIN", c["cpu_s"], f.name, tag,
                          c["master"])
        n += 1
    return {"appended": n}


def kg4_child(master, out, steps=100, persist=True) -> dict:
    """One one-thread 100-step training on dry data of a dry master (KG4); writes the checksums."""
    import hwsg_oracle
    from topo_pilot.contracts import ArtifactStore, SeedTree
    from topo_pilot.contracts.backends import MemoryBackend

    import hwsb_config
    import hwsb_data

    m = int(master)
    tag = next(t for t in gc.TAGS if m in gc.DRY_MASTERS[t])
    d = gc.WORLDS[tag]
    store = ArtifactStore(MemoryBackend())
    proc = hwsg_oracle.build_process_g(store, tag, masters=gc.DRY_MASTERS[tag])
    tree = SeedTree(m)
    obs = {}
    for split, n in (("train", 2048), ("dev", 256)):
        tok = hwsb_data.sample_observations(proc["T"], proc["E_named"][m], proc["pi"],
                                            proc["perm"][m], n,
                                            tree.generator("data", "kg4", split, m), split)
        from topo_pilot.contracts import ObservationSet
        from topo_pilot.dataset.checks import make_sequence_ids, process_code

        ids = make_sequence_ids(process_code("cylinder", "overlap", f"{d.sigma_str}|kg4", str(m)),
                                split, n)
        obs[split] = ObservationSet(split=split, V=proc["V"], sequence_id=ids, tokens=tok)
    cfg = hwsb_config.TRAIN_CFG
    if int(steps) not in cfg.checkpoint_steps:
        import dataclasses

        cfg = dataclasses.replace(cfg, checkpoint_steps=(0, int(steps)))
    r = hwsb_train.train_known(obs["train"], obs["dev"], m, ("hwsg-v1", "KG4", m), f"kg4-{m}",
                               f"kg4-obs-{m}", stop_after=int(steps), threads=1,
                               model_cfg=hwsb_config.MODEL_CFG, train_cfg=cfg)
    rec = {"master": m, "checksums": {str(k): v for k, v in r["checksums"].items()},
           "stopped_at": r["stopped_at"], "threads": r["threads"]}
    if persist:
        Path(out).mkdir(parents=True, exist_ok=True)
        stage_records.write_new(Path(out) / f"KG4_{m}_{int(time.time() * 1000)}.json", rec)
    return rec


def _launch_kill(out) -> bool:
    """Start a dry child and kill it at once (DRG12): it must leave no record."""
    m = gc.DRY_MASTERS[gc.TAGS[0]][0]
    p = subprocess.Popen(child_argv(gc.TAGS[0], m, out, "kill", 1, sub="kg4"),
                         env=child_env("kill", out, m), cwd=gc.REPO)
    p.kill()
    p.wait()
    return p.returncode != 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="hwsg_train")
    ap.add_argument("sub", choices=("child", "kg4"))
    ap.add_argument("--world")
    ap.add_argument("--master", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--job", default="")
    ap.add_argument("--attempt", type=int, default=1)
    a = ap.parse_args(argv)
    if a.sub == "kg4":
        kg4_child(a.master, a.out)
        return 0
    r = child(a.world, a.master, a.out, a.job, a.attempt)
    return 0 if r.get("status") == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
