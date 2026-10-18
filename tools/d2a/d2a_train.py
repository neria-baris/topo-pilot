"""D-2a training: runs, waves, children, resource supervisor, controls and meter binding
(D2A-FROZEN-v1 §4, §10.7 S5/S6/S8, §11.3; tools/d2a/API.md §2.3).

Top-level imports are standard library only: the store-local meter binding imports this module
under the base interpreter, and the wave parent does supervision only (no numerical work).
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from functools import partial
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ROOT = REPO.parent
STORE = ROOT / "d2a-store"
MAILBOX = ROOT / "agent-handoff"
VENV_PY = ROOT / "topo-pilot" / ".venv" / "Scripts" / "python.exe"
for _p in (HERE, REPO / "tools" / "x4_oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

RUNS = {f"d2a-s{s}-H{H}": (s, H, "CM") for s in (1, 2, 3, 4) for H in (1, 2, 3)}
RUNS.update({f"d2a-s{s}-N": (s, 3, "CC") for s in (1, 2)})
WAVES = {"W1": ("d2a-s1-H3", "d2a-s2-H3"), "W2": ("d2a-s1-H1", "d2a-s1-H2", "d2a-s2-H1"),
         "W3": ("d2a-s2-H2", "d2a-s3-H1", "d2a-s3-H2"),
         "W4": ("d2a-s3-H3", "d2a-s4-H1", "d2a-s4-H2"),
         "W5": ("d2a-s4-H3", "d2a-s1-N", "d2a-s2-N")}
WAVE_STAGE = {"W1": "stage1", "W2": "stage2", "W3": "stage2", "W4": "stage2", "W5": "stage2"}
THREADS = {"intra": 2, "interop": 1}
THREAD_VARS = ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
               "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
EXIT_NONFINITE, EXIT_STOP = 3, 4
GIB, HOUR = 1024**3, 3600.0


class D2AStop(RuntimeError):
    """STOP or INVALID control state (owner STOP, malformed control): stop at the boundary."""


def train_config():
    from topo_pilot.learner import TrainConfig

    return TrainConfig(steps=10000, checkpoint_steps=(0, 1000, 2500, 5000, 7500, 10000),
                       device="cpu")


def model_config():
    from topo_pilot.learner import ModelConfig

    return ModelConfig(vocab_in=6, vocab_out=5)


TRAIN_CFG, MODEL_CFG = train_config(), model_config()
WAVE_MAX_CPU_S = {"W1": 50_400, "W2": 75_600, "W3": 75_600, "W4": 75_600, "W5": 75_600}  # Q3
MAX_WALL_S = 6 * 3600


def make_trainer(run_id: str, model_cfg=None, train_cfg=None):
    """Trainer for a registered run (§4.5); H = 1 is exactly the default path."""
    from d2a_world import MODEL

    from topo_pilot.contracts import SeedTree
    from topo_pilot.learner import Trainer
    from topo_pilot.learner.multihorizon import MultiHorizonLM, multi_horizon_loss

    s, H, _ = RUNS[run_id]
    args = (model_cfg or model_config(), train_cfg or train_config(), SeedTree(MODEL), ("d2a", s))
    if H == 1:
        return Trainer(*args)
    aux = SeedTree(MODEL).seed("init_joint", "d2a", s)
    return Trainer(*args, model_factory=partial(MultiHorizonLM, horizon=H, aux_seed=aux),
                   loss_fn=partial(multi_horizon_loss, horizon=H))


def checkpoint_callback(store, obs_train_id, obs_dev_id, run_id, horizon, proc, model_cfg,
                        train_cfg, seeds, run_key, before, after, record):
    """x5g1t_train.checkpoint_callback with run_id and horizon added to the identity (§2.5)."""
    from topo_pilot.contracts import Checkpoint
    from topo_pilot.learner import serialise_state

    model_dict, train_dict = dataclasses.asdict(model_cfg), dataclasses.asdict(train_cfg)

    def on_checkpoint(step, model, info):
        import torch

        before(step)
        ckpt = Checkpoint(run_id=run_id, step=step, observation_id=obs_train_id,
                          state=serialise_state(model, info), model_config=model_dict,
                          train_config=train_dict, has_optimizer_state="optimizer_state" in info)
        config = {"run_key": list(run_key), "step": step, "model_config": model_dict,
                  "train_config": train_dict, "horizon": horizon, "process": proc,
                  "threads": {"intra": torch.get_num_threads(),
                              "interop": torch.get_num_interop_threads()}}
        cid = store.save(ckpt, config=config, parents=[obs_train_id, obs_dev_id],
                         seed_map=dict(seeds.issued), consumer="experiment")
        record.append({"step": step, "checkpoint_id": cid, "dev_ce": info["dev_ce"],
                       "payload_sha256": store.meta(cid).payload_sha256})
        after(step)

    return on_checkpoint


def bound_controls(out, job_id, task_sha256):
    """The job-0014 controls module bound to the current dispatch identities (in this process)."""
    import controls

    controls.JOB_ID, controls.TASK_SHA256 = str(job_id), str(task_sha256).upper()
    return lambda: controls.classify_all([controls.MAILBOX], Path(out), "run")


def boundary(classify, sleep=time.sleep, poll_s: float = 30.0) -> None:
    """Safe boundary: CONTINUE returns, HOLD waits, STOP / INVALID raise ``D2AStop``."""
    while True:
        state, why = classify()
        if state == "CONTINUE":
            return
        if state in ("STOP", "INVALID"):
            raise D2AStop(f"{state}: {why}")
        sleep(poll_s)


def disk_reason(usage=shutil.disk_usage):
    for drive, minimum in (("C:\\", 2_000_000_000), ("X:\\", 30_000_000_000)):
        try:
            free = usage(drive).free
        except OSError as exc:
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


@dataclasses.dataclass(frozen=True)
class Limits:
    model_cpu_s: float = 7 * HOUR  # S6 as amended by owner addendum 5
    process_mem: int = 3 * GIB
    stage_cpu_s: dict = dataclasses.field(default_factory=lambda: {
        "preflight": 2 * HOUR, "stage0": 2 * HOUR, "stage1": 14 * HOUR, "stage2": 84 * HOUR,
        "stage3": 12 * HOUR})
    total_cpu_s: float = 114 * HOUR
    job_mem: int = 12 * GIB
    poll_s: float = 2.0


def stage_spent(ledger: dict, stage: str) -> float:
    return float(sum(e.get("charged_cpu_s") or 0.0 for e in ledger.get("entries", [])
                     if str(e.get("label", "")).startswith(stage + "__")))


def total_spent(ledger: dict) -> float:
    return float(ledger.get("cumulative_cpu_s", 0.0))


def admit(stage, spent_stage, spent_total, limits=Limits(), need_s: float = 0.0) -> bool:
    return (limits.stage_cpu_s[stage] - spent_stage >= need_s
            and limits.total_cpu_s - spent_total >= need_s)


class Supervisor:
    """Polling per-model CPU, per-process memory and stage/total budget enforcement (S6)."""

    def __init__(self, limits, cpu_of, mem_of, kill, clock=time.monotonic):
        self.limits, self.cpu_of, self.mem_of, self.kill, self.clock = (
            limits, cpu_of, mem_of, kill, clock)

    def check(self, children: dict, spent_stage: float, spent_total: float, stage: str) -> dict:
        lim, out = self.limits, {}
        cpu = {r: float(self.cpu_of(h)) for r, h in children.items()}
        for run, h in children.items():
            if cpu[run] > lim.model_cpu_s:
                out[run] = "INCOMPLETE:MODEL_CPU"
            elif self.mem_of(h) > lim.process_mem:
                out[run] = "INCOMPLETE:PROCESS_MEMORY"
        live = sum(cpu.values())
        over = ("INCOMPLETE:STAGE_CPU" if spent_stage + live > lim.stage_cpu_s[stage] else
                "INCOMPLETE:TOTAL_CPU" if spent_total + live > lim.total_cpu_s else None)
        if over:
            out = {run: over for run in children}
        for run in out:
            self.kill(children[run])
        return {run: {"reason": why, "polling_interval_s": lim.poll_s, "cpu_s": cpu[run],
                      "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                for run, why in out.items()}


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def jsonable(x):
    if isinstance(x, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k)) if isinstance(k, tuple)
                 else str(k)): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x.tolist() if hasattr(x, "tolist") else x  # numpy arrays and scalars, stdlib only


def write_json(path, rec) -> None:
    """Exclusive-create JSON write of ``jsonable(rec)`` (stage records are never overwritten)."""
    with Path(path).open("x", encoding="utf-8") as fh:
        json.dump(jsonable(rec), fh, indent=1, default=str)


def verify_identity(mailbox, job_id, task_sha256, session, lock_path) -> None:
    """Dispatch identities (ruling D6): request, task.json, task.md digest, RUN.lock session."""
    from topo_pilot.contracts import ErrorCode, StageFailure

    def bad(check, detail):
        return StageFailure(ErrorCode.INVALID_CONFIG, "d2a.train", check, detail)

    mailbox, want = Path(mailbox), str(task_sha256).upper()
    try:
        req, task = _read(mailbox / "request.json"), _read(mailbox / "jobs" / job_id / "task.json")
        md = (mailbox / "jobs" / job_id / "task.md").read_bytes()
        lock = _read(lock_path)
    except (OSError, ValueError) as exc:
        raise bad("identity_unreadable", f"{type(exc).__name__}: {exc}") from exc
    if (req.get("command"), req.get("job_id"), str(req.get("task_sha256", "")).upper()) != (
            "RUN_NEXT", job_id, want):
        raise bad("request", "request.json is not RUN_NEXT for this job and digest")
    if str(task.get("task_sha256", "")).upper() != want or task.get("job_id") != job_id:
        raise bad("task_json", "task.json job id or digest differs")
    if hashlib.sha256(md).hexdigest().upper() != want:
        raise bad("task_md", "task.md digest differs")
    if lock.get("session") != session:
        raise bad("lock_session", "RUN.lock session differs from the executing worker")


def bind_meter(meter, controls, winjob, out, job_id, task_sha256, session) -> None:
    """Store-local rebinding of the unchanged job-0014 meter (§11.3; module names only)."""
    out = Path(out)
    meter.OUT, meter.LEDGER, meter.LOCK = out, out / "cpu_ledger.json", out / "RUN.lock"
    meter.EMERGENCY, meter.ACTIVE = out / "cpu_ledger.emergency.jsonl", out / "METER_ACTIVE.lock"
    meter.LOG_DIR = out / "logs"
    meter.CAP_S = meter.STOP_NEW_S = float("inf")
    meter.OUTPUT_CAP = 4 * GIB
    winjob.MEMORY_CAP = 12 * GIB
    controls.JOB_ID, controls.TASK_SHA256 = str(job_id), str(task_sha256).upper()
    meter.WORKER_SESSION = str(session)


def _set_threads():
    import torch

    torch.set_num_threads(THREADS["intra"])
    torch.set_num_interop_threads(THREADS["interop"])
    got = (torch.get_num_threads(), torch.get_num_interop_threads())
    if got != (THREADS["intra"], THREADS["interop"]):
        raise RuntimeError(f"thread assertion failed: {got}")
    return torch


def child_main(run_id: str, store_root=STORE) -> int:
    """One training (CLI ``child RUN``): threads first, then train, saving every checkpoint."""
    torch = _set_threads()
    import d2a_world as W

    from topo_pilot import contracts as C
    from topo_pilot.dataset import PublicTokenDataset

    s, H, proc = RUNS[run_id]
    root, start = Path(store_root), time.perf_counter()
    pools, store = W.pool_index(root), W.open_store(root)
    names = (f"train-s{s}", f"dev-s{s}") if proc == "CM" else (f"trainN-s{s}", f"devN-s{s}")
    ids = [pools[n]["id"] for n in names]
    sets = [PublicTokenDataset(store.load(C.ObservationSet, i, consumer="learner"),
                               C.SequenceLayout()) for i in ids]
    ident, trainer, record = W.dispatch(root), make_trainer(run_id), []
    classify = bound_controls(root, ident["JOB_ID"], ident["TASK_SHA256"])

    def hook(step):
        boundary(classify)

    cb = checkpoint_callback(store, ids[0], ids[1], run_id, H, proc, trainer.model_cfg,
                             trainer.train_cfg, C.SeedTree(W.MODEL), trainer.run_key, hook, hook,
                             record)
    rec = {"run_id": run_id, "seed": s, "horizon": H, "process": proc, "threads": THREADS,
           "torch": torch.__version__, "pools": dict(zip(names, ids)), "checkpoints": record}
    code = 0
    try:
        summary = trainer.fit(sets[0], sets[1], cb)
        rec.update(status="COMPLETE", final_train_loss=summary.final_train_loss,
                   train_wall_s=summary.wall_time_s)
    except C.StageFailure as exc:
        if exc.code != C.ErrorCode.NONFINITE_LOSS:
            raise
        rec["status"], code = "INVALID:NONFINITE_LOSS", EXIT_NONFINITE
    except D2AStop as exc:
        rec["status"], rec["stop"], code = "INCOMPLETE:STOP", str(exc), EXIT_STOP
    rec["wall_s"] = time.perf_counter() - start
    (root / "runs").mkdir(exist_ok=True)
    (root / "runs" / f"{run_id}.attempt.json").write_text(json.dumps(rec, indent=1), "utf-8")
    return code


def _launch(run_id, root):
    from process_tree import TrainingProcess

    env = dict(os.environ, **{v: str(THREADS["intra"]) for v in THREAD_VARS},
               PYTHONPATH=str(REPO / "src"), PYTHONDONTWRITEBYTECODE="1")
    log = (Path(root) / "logs" / f"child_{run_id}_{time.strftime('%Y%m%dT%H%M%SZ')}.txt")
    with log.open("xb") as out:
        return TrainingProcess([str(VENV_PY), str(HERE / "d2a_train.py"), "child", run_id],
                               stdout=out, stderr=subprocess.STDOUT, env=env, cwd=str(REPO))


def wave_main(wave: str, store_root=STORE, limits=Limits()) -> int:
    from process_tree import wave_lease

    with wave_lease(Path(store_root), wave):
        return _wave_main(wave, store_root, limits)


def _wave_main(wave: str, store_root, limits) -> int:
    """CLI ``wave W``: ≤ 3 children, supervised; the S5 rerun rule; waves/{W}.json."""
    root, stage, runs = Path(store_root), WAVE_STAGE[wave], WAVES[wave]
    outputs = [root / "waves" / f"{wave}.json"]
    outputs += [root / "runs" / f"{r}{suffix}.json" for r in runs for suffix in ("", ".attempt")]
    if any(path.exists() for path in outputs):
        raise FileExistsError("wave or run records already exist; refusing duplicate training")
    ledger = _read(root / "cpu_ledger.json")
    base_stage, base_total = stage_spent(ledger, stage), total_spent(ledger)
    sup = Supervisor(limits, lambda p: p.cpu_s(), lambda p: p.memory_bytes(),
                     lambda p: p.terminate())
    rec = {"wave": wave, "stage": stage, "runs": {}, "polling_interval_s": limits.poll_s}
    attempts = {r: 0 for r in runs}
    pending, live, done_cpu = list(runs), {}, 0.0
    try:
        while pending or live:
            while pending and len(live) < 3:
                run = pending.pop(0)
                if not admit(stage, base_stage + done_cpu, base_total + done_cpu, limits):
                    rec["runs"][run] = {"status": "INCOMPLETE:NOT_ADMITTED"}
                    continue
                attempts[run] += 1
                live[run] = _launch(run, root)
            time.sleep(limits.poll_s)
            disk = disk_reason()
            killed = sup.check(live, base_stage + done_cpu, base_total + done_cpu, stage)
            if disk:
                for run, p in live.items():
                    p.terminate()
                    killed[run] = {"reason": "INCOMPLETE:DISK", "detail": disk}
                pending.clear()
            for run, p in list(live.items()):
                if p.poll() is None and run not in killed:
                    continue
                p.wait()
                cpu = p.cpu_s()
                p.close()
                done_cpu += cpu
                del live[run]
                att = root / "runs" / f"{run}.attempt.json"
                entry = {"exit_code": p.returncode, "cpu_s": cpu, "attempts": attempts[run]}
                if run in killed:
                    entry.update(status=killed[run]["reason"], supervisor=killed[run])
                elif p.returncode in (0, EXIT_NONFINITE, EXIT_STOP) and att.exists():
                    entry.update(_read(att), cpu_s=cpu)
                elif attempts[run] == 1:
                    rec.setdefault("interruptions", []).append({"run": run, **entry})
                    pending.insert(0, run)
                    continue
                else:
                    entry["status"] = "INCOMPLETE:INTERRUPTED_TWICE"
                entry["rerun"] = attempts[run] > 1
                rec["runs"][run] = entry
                with (root / "runs" / f"{run}.json").open("x", encoding="utf-8") as f:
                    json.dump(entry, f, indent=1)
                if att.exists():
                    att.unlink()
    finally:
        for child in live.values():
            try:
                child.terminate()
            finally:
                child.close()
    (root / "waves").mkdir(exist_ok=True)
    with (root / "waves" / f"{wave}.json").open("x", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
    return 0 if all(r.get("status") == "COMPLETE" for r in rec["runs"].values()) else 2


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "child":
        sys.exit(child_main(sys.argv[2]))
    if cmd == "wave":
        sys.exit(wave_main(sys.argv[2]))
    raise SystemExit(f"unknown command {cmd!r}")
