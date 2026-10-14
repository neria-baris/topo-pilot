"""X5 G1 training-study stages, part 1 (x5g1-train-v4 §10-§11; API v4 §6): shared stage plumbing,
``pools`` and ``train``. ``dev-analysis`` and ``final-test`` are in ``x5g1t_stages_eval``.

Every stage validates the configuration first (read-only, before any output directory, store
write, sampler or model). Exports go through ``study_export`` under the full study controls;
prerequisites advance only on a COMPLETE, manifest-matching export with a consistent pool table;
every used pool must prove its semantic identity (API v4.1 §B: config, parents, split, V, layout,
rows, ordered IDs) before any model, oracle or scoring; world, kernels, emission, every used pool
and every ObservationSet read for the collision check are fully re-hashed before use and again
before the result export. Budget checks
at boundaries are periodic safety checks, not an instruction-level CPU kill: an atomic unit (a
draw, a checkpoint write, a scoring batch) can exceed its estimate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import torch

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    ObservationSet,
    SeedTree,
    TransitionSpec,
)
from topo_pilot.learner import ModelConfig

from .config import producer_version
from .x4b import ReadThroughBackend
from .x4b_run import peak_memory_bytes
from .x5g1_controls import RunControls
from .x5g1_safety import ensure_new_output_dir
from .x5g1t_checks import IntegrityFailed, canonical, validate_pool, verify_full
from .x5g1t_config import StudyConfig, read_chain, read_store, validate_config
from .x5g1t_exports import study_export, verify_export_complete
from .x5g1t_lineage import (
    ARMS,
    collisions,
    draw_pair,
    pool_observation,
    sequence_ids,
    stream,
    study_pool_config,
)
from .x5g1t_runtime import (
    EST,
    BudgetPlanner,
    StudyControls,
    evaluation_reserve,
    read_outcome,
)
from .x5g1t_train import study_train_config, train_one


class StudyFailed(RuntimeError):
    """Collision, prerequisite or authorisation failure (not a scientific verdict)."""


def stores(cfg: StudyConfig, repo: Path) -> tuple[ArtifactStore, ArtifactStore]:
    """(read-only sources, read-through study store writing only to ``study_root/store``)."""
    rw = ArtifactStore(ReadThroughBackend(read_chain(cfg.read_roots),
                                          LocalFSBackend(cfg.root / "store")),
                       producer_version=producer_version(repo))
    return read_store(cfg.read_roots), rw


def _controls(cfg: StudyConfig, job: str) -> RunControls:
    return RunControls(Path(cfg.ledger_path), cfg.cap_s, Path(cfg.mailbox) / "STOP", job,
                       cfg.cumulative_cap_s)


def _study(cfg: StudyConfig, ctl: RunControls, name: str) -> StudyControls:
    return StudyControls(ctl, Path(cfg.mailbox), BudgetPlanner(cfg.cumulative_cap_s),
                         cfg.root, cfg.root / "runs" / f"hold_{name}.json")


def _sources(store: ArtifactStore, cfg: StudyConfig):
    kernels = {arm: np.asarray(store.load(TransitionSpec, cfg.sources["T"][arm][0],
                                          consumer="experiment").T) for arm in ARMS}
    emis = store.load(EmissionSpec, cfg.sources["E"][0], consumer="experiment")
    pi = np.asarray(store.load(TransitionSpec, cfg.sources["T"]["a0"][0],
                               consumer="experiment").pi)
    return kernels, np.asarray(emis.E, float), np.asarray(emis.symbol_perm), pi


def _meta(cfg: StudyConfig, repo: Path, ctl: RunControls, stage: str, report: dict) -> dict:
    return {"protocol": cfg.protocol, "mode": cfg.mode, "stage": stage,
            "producer_version": producer_version(repo),
            "protocol_doc_sha256": report["protocol_doc_sha256"],
            "config_check": report, "python": sys.executable, "torch": torch.__version__,
            "threads": torch.get_num_threads(), "cpu_s": round(ctl.cpu(), 3),
            "cpu_prior_cumulative": ctl.prior, "peak_memory_bytes": peak_memory_bytes(),
            "steps": ctl.steps}


def tables(cfg: StudyConfig, *parts: str) -> Path:
    return cfg.root.joinpath("tables", *parts)


def complete_pools(cfg: StudyConfig) -> dict:
    """``pools.json`` of a COMPLETE, manifest-matching pools export whose table has exactly the
    configured keys with 64-hex hashes and whose run record matches the config (API v4.1 §C)."""
    out = tables(cfg, "pools")
    verify_export_complete(out)
    pools = json.loads((out / "pools.json").read_text(encoding="utf-8"))
    run = json.loads((out / "run.json").read_text(encoding="utf-8"))
    keys = {f"{s}:{a}:{m}" for s in ("train", "dev") for a in ARMS for m in cfg.masters}
    table, shas = pools.get("pools"), pools.get("pool_sha256")
    if not (isinstance(table, dict) and isinstance(shas, dict) and set(table) == keys
            and set(shas) == keys and all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v)
                                          for v in shas.values())):
        raise IntegrityFailed("pool table keys/hashes differ from the configuration")
    if run.get("protocol") != cfg.protocol or run.get("mode") != cfg.mode:
        raise IntegrityFailed("pools export was produced under another protocol/mode")
    return pools


def emission_V(store: ArtifactStore, cfg: StudyConfig) -> int:
    return int(np.asarray(store.load(EmissionSpec, cfg.sources["E"][0],
                                     consumer="experiment").E).shape[1])


def validate_pools(store: ArtifactStore, cfg: StudyConfig, pools: dict, which, V: int) -> dict:
    """Semantic identity of each ``(split, arm, master)`` pool in the table (API v4.1 §B)."""
    used: dict = {}
    for split, arm, m in which:
        key = f"{split}:{arm}:{m}"
        used.update(validate_pool(store, pools["pools"][key], pools["pool_sha256"][key], cfg,
                                  split, arm, m, V))
    return used


def collision_inputs(ro: ArtifactStore) -> tuple[np.ndarray, dict]:
    """IDs of every read-root ObservationSet, and ``{id: (cls, sha)}`` recorded at load so the
    same inputs are re-verified before the result export (API v4.1 §D)."""
    ids, used = [], {}
    for aid in ro.find(ObservationSet):
        used[aid] = (ObservationSet, str(ro.meta(aid).payload_sha256))
        ids.append(np.asarray(ro.load(ObservationSet, aid, consumer="experiment").sequence_id,
                              np.int64))
    return np.concatenate(ids or [np.zeros(0, np.int64)]), used


def pool_expected(pools: dict, keys) -> dict:
    return {pools["pools"][k]: (ObservationSet, pools["pool_sha256"][k]) for k in keys}


def complete_outcome(cfg: StudyConfig, arm: str, master) -> dict | None:
    """The recorded outcome; for a COMPLETE model, only with a COMPLETE matching train export."""
    o = read_outcome(cfg.root, arm, master)
    if not (o and o.get("status") == "COMPLETE"):
        return o
    out = tables(cfg, "train", f"{arm}_{master}")
    verify_export_complete(out)
    exported = json.loads((out / "outcome.json").read_text(encoding="utf-8"))
    if canonical(exported) != canonical(o):
        raise IntegrityFailed(f"{arm}/{master}: outcome differs from its train export")
    return o


def run_pools(cfg: StudyConfig, repo: Path) -> dict:
    """Train and dev pools for every master and arm (never the fresh test)."""
    report = validate_config(cfg, repo)
    out = ensure_new_output_dir(tables(cfg, "pools"))
    ro, rw = stores(cfg, repo)
    exp = cfg.expected_sources()
    res: dict = {"pools": {}, "pool_sha256": {}}
    with _controls(cfg, "x5g1t-pools") as ctl:
        sc = _study(cfg, ctl, "pools")
        reserve = evaluation_reserve(0, 0)
        verify_full(ro, exp, "sources before pools")
        plan = {f"{s}:{a}:{m}": sequence_ids(s, a, m, cfg.sizes[s])
                for s in ("train", "dev") for m in cfg.masters for a in ARMS}
        stored, seen = (collision_inputs(ro) if cfg.check_stored_ids
                        else (np.zeros(0, np.int64), {}))
        res["collisions"] = collisions(plan, stored)
        if any(res["collisions"].values()):
            raise StudyFailed(f"namespace collision {res['collisions']}")
        kernels, E, perm, pi = _sources(ro, cfg)
        for split in ("train", "dev"):
            for m in cfg.masters:
                sc.boundary(f"draw {split} {m}", 30.0, reserve)
                named = draw_pair(kernels, E, perm, pi, split, m, cfg.sizes[split])
                sc.boundary(f"draw {split} {m} done", EST["save"], reserve)
                for arm in ARMS:
                    key = f"{split}:{arm}:{m}"
                    obs = pool_observation(split, named[arm], plan[key], E.shape[1])
                    sc.boundary(f"save {key}", EST["save"], reserve)
                    oid = rw.save(obs, config=study_pool_config(split, arm, m, cfg.protocol),
                                  parents=[cfg.sources["T"][arm][0], cfg.sources["E"][0]],
                                  seed_map={"/".join(map(str, (m, *stream(split)))):
                                            SeedTree(m).seed(*stream(split))},
                                  consumer="experiment")
                    res["pools"][key] = oid
                    res["pool_sha256"][key] = rw.meta(oid).payload_sha256
                    sc.boundary(f"save {key} done", EST["save"], reserve)
                res[f"first_symbol_equal:{split}:{m}"] = bool(np.array_equal(
                    named["a0"][:, 0], named["a020"][:, 0]))
        verify_full(ro, exp, "sources after pools")
        verify_full(ro, seen, "collision inputs before export")
        validate_pools(rw, cfg, res, [(s, a, m) for s in ("train", "dev") for m in cfg.masters
                                      for a in ARMS], E.shape[1])
        ctl.outcome = "POOLS_DONE"
        study_export(sc, out, {"pools.json": res,
                               "run.json": _meta(cfg, repo, ctl, "pools", report)},
                     reserve=reserve)
    return res


def run_train(cfg: StudyConfig, repo: Path, arm: str, master) -> dict:
    """One model; the outcome is recorded by ``train_one`` on every exit."""
    report = validate_config(cfg, repo)
    pools = complete_pools(cfg)
    keys = (f"train:{arm}:{master}", f"dev:{arm}:{master}")
    out = ensure_new_output_dir(tables(cfg, "train", f"{arm}_{master}"))
    ro, rw = stores(cfg, repo)
    exp = {**cfg.expected_sources(), **pool_expected(pools, keys)}
    torch.set_num_threads(cfg.threads)
    with _controls(cfg, f"x5g1t-train-{arm}-{master}") as ctl:
        sc = _study(cfg, ctl, f"{arm}_{master}")
        n_models = 2 * len(cfg.masters)
        reserve = evaluation_reserve(len(cfg.grid) * n_models, n_models)
        verify_full(rw, exp, "sources and pools before training")
        validate_pools(rw, cfg, pools, [("train", arm, master), ("dev", arm, master)],
                       emission_V(ro, cfg))
        outcome = train_one(rw, pools["pools"][keys[0]], pools["pools"][keys[1]],
                            ModelConfig(**cfg.model_config),
                            study_train_config(cfg.steps, cfg.grid), master, arm, cfg.root, sc,
                            reserve_s=reserve)
        verify_full(rw, exp, "sources and pools after training")
        ctl.outcome = outcome["status"]
        study_export(sc, out, {"outcome.json": outcome,
                               "run.json": _meta(cfg, repo, ctl, f"train {arm} {master}",
                                                 report)}, reserve=reserve)
    return outcome
