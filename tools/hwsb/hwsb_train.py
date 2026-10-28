"""HWSB training: Trainer.fit with a LearnerStage-mirroring callback, threads, the hold rule
and the KB2/KB3 known-case harness (API.md §3; protocol §2.1 item 3, §3 KB2/KB3, §8.2 RC-14).

The callback body is LearnerStage.run's `save` closure (mirrored; DRB2 tests it bitwise). The
hold keeps the live process at ~0 CPU (sleep polling); training is never resumed from weights.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import dataclasses
import json
import os
import time
from pathlib import Path

import stage_records
import torch

from topo_pilot.contracts import (
    Checkpoint,
    ErrorCode,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    payload_checksum,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import Trainer
from topo_pilot.learner.stage import serialise_state

KNOWN = "FAIL_TECHNICAL/KNOWN_CASE"


def _plain(x):
    if isinstance(x, (list, tuple)):
        return [_plain(v) for v in x]
    if isinstance(x, dict):
        return {k: _plain(v) for k, v in x.items()}
    return x


def check_recipe(model_cfg, train_cfg, reference=None) -> dict:
    ref = reference or hc.CONTRACT["recipe"]
    diff = []
    for name, cfg in (("model_config", model_cfg), ("train_config", train_cfg)):
        found, want = _plain(dataclasses.asdict(cfg)), _plain(dict(ref[name]))
        for f in sorted(set(found) | set(want)):
            a, b = want.get(f, "<missing>"), found.get(f, "<missing>")
            if a != b or type(a) is not type(b):
                diff.append({"field": f"{name}.{f}", "expected": a, "found": b})
    return {"status": KNOWN if diff else "PASS", "diff": diff}


def set_threads(n) -> dict:
    n = int(n)
    torch.set_num_threads(n)
    if n == 1:
        os.environ["OMP_NUM_THREADS"] = os.environ["MKL_NUM_THREADS"] = "1"
    return {
        "requested": n,
        "torch_threads": torch.get_num_threads(),
        "torch_version": torch.__version__,
        "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
        "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
    }


def torch_versions(repo=hc.REPO) -> dict:
    lock = None
    path = Path(repo) / "requirements.lock"
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("torch=="):
                lock = line.strip()
                break
    return {"lock": lock, "in_use": torch.__version__}


class SentinelStop(Exception):
    """Raised by the checkpoint callback to stop training after a step (KB2, KB3)."""

    def __init__(self, step):
        super().__init__(f"sentinel stop after step {step}")
        self.step = int(step)


def build_checkpoint(step, model, info, run_id, observation_id, model_cfg, train_cfg):
    return Checkpoint(
        run_id=run_id,
        step=step,
        observation_id=observation_id,
        state=serialise_state(model, info),
        model_config=dataclasses.asdict(model_cfg),
        train_config=dataclasses.asdict(train_cfg),
        has_optimizer_state="optimizer_state" in info,
    )


class CheckpointSaver:
    """The on_checkpoint callback: LearnerStage's save, then the hold, then a sentinel."""

    def __init__(
        self,
        store,
        obs_train_id,
        obs_dev_id,
        model_cfg,
        train_cfg,
        seeds,
        run_key,
        *,
        observation_id=None,
        run_id=None,
        hold=None,
        stop_after=None,
    ):
        self.store, self.train_id, self.dev_id = store, obs_train_id, obs_dev_id
        self.model_cfg, self.train_cfg, self.seeds = model_cfg, train_cfg, seeds
        self.run_key = tuple(run_key)
        self.run_id = run_id or "-".join(map(str, self.run_key))
        self.observation_id = observation_id or obs_train_id
        self.hold, self.stop_after = hold, stop_after
        self.ids, self.checksums, self.dev_ce, self.train_loss, self.checkpoints = (
            [],
            {},
            {},
            {},
            {},
        )
        self.id_by_step = {}

    def __call__(self, step, model, info) -> None:
        step = int(step)
        ckpt = build_checkpoint(
            step, model, info, self.run_id, self.observation_id, self.model_cfg, self.train_cfg
        )
        self.checksums[step] = payload_checksum(*ckpt.to_payload())
        self.dev_ce[step] = float(info["dev_ce"])
        self.train_loss[step] = info.get("train_loss")
        if self.store is not None:
            md, td = dataclasses.asdict(self.model_cfg), dataclasses.asdict(self.train_cfg)
            config = {
                "run_key": list(self.run_key),
                "step": step,
                "model_config": md,
                "train_config": td,
            }
            aid = self.store.save(
                ckpt,
                config=config,
                parents=[self.train_id, self.dev_id],
                seed_map=dict(self.seeds.issued),
                consumer="learner",
            )
            self.ids.append(aid)
            self.id_by_step[step] = aid
        else:
            self.checkpoints[step] = ckpt
        if self.hold is not None:
            self.hold(step)
        if self.stop_after is not None and step >= int(self.stop_after):
            raise SentinelStop(step)


def hold_check(step, cpu_s, steps=5000, cap_s=7275.0, from_step=1000) -> dict:
    step, cpu_s = int(step), float(cpu_s)
    projected = cpu_s * steps / step if step >= from_step and step > 0 else None
    by_proj = projected is not None and projected > cap_s
    by_spent = cpu_s > cap_s
    trig = (
        "BOTH"
        if by_proj and by_spent
        else "PROJECTED"
        if by_proj
        else "SPENT"
        if by_spent
        else None
    )
    return {
        "hold": by_proj or by_spent,
        "trigger": trig,
        "step": step,
        "cpu_s": cpu_s,
        "projected_s": projected,
    }


class HoldRule:
    """The RC-14 hold: write HOLD_<step>.json, poll DECISION_<step>.json with sleep."""

    def __init__(
        self,
        out_dir,
        cap_s=7275.0,
        steps=5000,
        from_step=1000,
        cpu_fn=time.process_time,
        poll_s=30.0,
        sleep=time.sleep,
    ):
        self.out_dir = Path(out_dir)
        self.cap_s, self.steps, self.from_step = float(cap_s), int(steps), int(from_step)
        self.cpu_fn, self.poll_s, self.sleep = cpu_fn, float(poll_s), sleep
        self.events, self.exempt = [], False

    def __call__(self, step):
        if self.exempt:
            return None
        chk = hold_check(step, self.cpu_fn(), self.steps, self.cap_s, self.from_step)
        if not chk["hold"]:
            return None
        self.out_dir.mkdir(parents=True, exist_ok=True)
        rec = {k: chk[k] for k in ("step", "cpu_s", "projected_s", "trigger")}
        rec["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        stage_records.write_new(self.out_dir / f"HOLD_{int(step)}.json", rec)
        path = self.out_dir / f"DECISION_{int(step)}.json"
        while not path.exists():
            self.sleep(self.poll_s)
        try:
            decision = json.loads(path.read_text(encoding="utf-8"))["decision"]
        except Exception as exc:  # noqa: BLE001
            raise hc.HwsbStop("FAIL_TECHNICAL/HOLD", f"unreadable decision: {exc}") from exc
        event = dict(rec, decision=decision)
        self.events.append(event)
        if decision == "CONTINUE":
            self.exempt = True
            return event
        if decision == "STOP":
            raise hc.HwsbStop(
                "INCONCLUSIVE/RESOURCE_OR_AUTHORITY", f"owner STOP at hold step {step}"
            )
        raise hc.HwsbStop("FAIL_TECHNICAL/HOLD", f"unknown decision {decision!r}")


def _datasets(train_obs, dev_obs) -> tuple:
    layout = SequenceLayout()
    return PublicTokenDataset(train_obs, layout), PublicTokenDataset(dev_obs, layout)


def _fit(trainer, train, dev, saver):
    try:
        return trainer.fit(train, dev, saver)
    except StageFailure as exc:
        if exc.code == ErrorCode.NONFINITE_LOSS:
            raise hc.HwsbStop("FAIL_TECHNICAL/NONFINITE", str(exc)) from exc
        raise


def _summary(s) -> dict:
    return {
        k: getattr(s, k)
        for k in (
            "steps_done",
            "final_train_loss",
            "wall_time_s",
            "tokens_per_second",
            "device",
            "torch_version",
        )
    }


def train(store, obs_ids, master, plan=hc.REAL_PLAN, hold=None, seeds=None) -> dict:
    """LearnerStage.run, composed: same loads, datasets, Trainer and checkpoint identities."""
    tid, did = obs_ids["train"], obs_ids["dev"]
    train_obs = store.load(ObservationSet, tid, consumer="learner")
    dev_obs = store.load(ObservationSet, did, consumer="learner")
    tr, dv = _datasets(train_obs, dev_obs)
    seeds = seeds or SeedTree(int(master))
    rk = hc.run_key(plan, master)
    saver = CheckpointSaver(store, tid, did, plan.model_cfg, plan.train_cfg, seeds, rk, hold=hold)
    summary = _fit(Trainer(plan.model_cfg, plan.train_cfg, seeds, rk), tr, dv, saver)
    return {
        "run_key": list(rk),
        "checkpoint_ids": dict(saver.id_by_step),
        "checksums": dict(saver.checksums),
        "dev_ce": dict(saver.dev_ce),
        "train_loss": dict(saver.train_loss),
        "summary": _summary(summary),
        "holds": list(hold.events) if hold is not None else [],
    }


def train_known(
    obs_train,
    obs_dev,
    master,
    run_key,
    run_id,
    observation_id,
    stop_after,
    threads,
    model_cfg=hc.MODEL_CFG,
    train_cfg=hc.TRAIN_CFG,
) -> dict:
    """KB2/KB3: in-memory ObservationSets, stopped by a sentinel; nothing persisted."""
    info = set_threads(threads)
    tr, dv = _datasets(obs_train, obs_dev)
    seeds = SeedTree(int(master))
    saver = CheckpointSaver(
        None,
        observation_id,
        "",
        model_cfg,
        train_cfg,
        seeds,
        run_key,
        observation_id=observation_id,
        run_id=run_id,
        stop_after=stop_after,
    )
    stopped = None
    try:
        _fit(Trainer(model_cfg, train_cfg, seeds, tuple(run_key)), tr, dv, saver)
    except SentinelStop as exc:
        stopped = exc.step
    return {
        "checksums": dict(saver.checksums),
        "dev_ce": dict(saver.dev_ce),
        "checkpoints": dict(saver.checkpoints),
        "threads": info,
        "stopped_at": stopped,
    }
