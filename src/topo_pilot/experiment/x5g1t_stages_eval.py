"""X5 G1 training-study stages, part 2 (x5g1-train-v4 §10-§11; API v4 §6): ``dev-analysis`` and
the separately authorised ``final-test``.

Both validate the configuration first and advance only on COMPLETE, manifest-matching
prerequisite exports. Every used pool proves its semantic identity (API v4.1 §B) and every used
checkpoint passes ``validate_checkpoints`` (grid, identity, parents, full hash) before any oracle
or scoring; every 512-row scoring batch and every oracle batch is bracketed by the study
controls. In final-test every train/dev pool is identity-checked first; the fresh test IDs are
then collision-checked against the read roots and those pools BEFORE the fresh draw (the
ObservationSets read for that check are re-hashed before the export); a collision or a STOP
before the draw means the fresh test is never drawn. Used sources, pools and checkpoints
are re-hashed before the result export; an integrity failure exports nothing scientific.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import numpy as np
import torch

from topo_pilot.analysis import (
    PairEvidence,
    cohort_verdict,
    dev_auc,
    difference_bounds,
    grid_event,
    paired_bootstrap_endpoint,
    pass_sequence,
    ratio_curve,
)
from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    ObservationSet,
    SeedTree,
    SequenceLayout,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import load_model

from .x5g1_safety import ensure_new_output_dir
from .x5g1t_checks import validate_checkpoints, validate_pool, verify_full
from .x5g1t_config import StudyConfig, validate_config
from .x5g1t_exports import study_export, verify_export_complete
from .x5g1t_lineage import (
    ARMS,
    NAMESPACE,
    TEST_MASTER,
    collisions,
    draw_pair,
    pool_observation,
    sequence_ids,
    stream,
    study_pool_config,
)
from .x5g1t_oracle import oracle_q32
from .x5g1t_runtime import EST, StudyControls, evaluation_reserve
from .x5g1t_score import regret_rows
from .x5g1t_stages import (
    StudyFailed,
    _controls,
    _meta,
    _sources,
    _study,
    collision_inputs,
    complete_outcome,
    complete_pools,
    stores,
    tables,
    validate_pools,
)


def _inputs(obs: ObservationSet) -> torch.Tensor:
    ds = PublicTokenDataset(obs, SequenceLayout())
    return torch.stack([ds[i][0] for i in range(len(ds))])


def _guard(sc: StudyControls, reserve: float):
    return lambda what: sc.boundary(what, 1.0, reserve)


def _regret_curve(rw: ArtifactStore, sc: StudyControls, ckpts: list, inputs, q,
                  reserve: float) -> np.ndarray:
    """Regret per row and checkpoint; checkpoints were validated by ``validate_checkpoints``."""
    reg = np.empty((inputs.shape[0], len(ckpts)))
    for k, c in enumerate(ckpts):
        sc.boundary(f"score {c['checkpoint_id']}", EST["score"], reserve)
        model = load_model(rw.load(Checkpoint, c["checkpoint_id"], consumer="experiment"))
        reg[:, k] = regret_rows(model, inputs, q, guard=_guard(sc, reserve))
    return reg


def _complete(o) -> bool:
    return bool(o) and o.get("status") == "COMPLETE"


def run_dev_analysis(cfg: StudyConfig, repo: Path) -> dict:
    """Dense dev regret curves, grid events, paired bootstrap and the cohort verdict."""
    report = validate_config(cfg, repo)
    pools = complete_pools(cfg)
    outcomes = {(a, m): complete_outcome(cfg, a, m) for m in cfg.masters for a in ARMS}
    out = ensure_new_output_dir(tables(cfg, "dev_analysis"))
    ro, rw = stores(cfg, repo)
    exp = cfg.expected_sources()
    torch.set_num_threads(cfg.threads)
    res: dict = {"pairs": {}, "failures": []}
    arrays: dict = {}
    used: dict = {}
    with _controls(cfg, "x5g1t-dev-analysis") as ctl:
        sc = _study(cfg, ctl, "dev_analysis")
        reserve = evaluation_reserve(0, 2 * len(cfg.masters))
        verify_full(ro, exp, "sources before dev analysis")
        kernels, E, _, pi = _sources(ro, cfg)
        scored = [(a, m) for m in cfg.masters for a in ARMS
                  if all(_complete(outcomes[(x, m)]) for x in ARMS)]
        # every used input proven BEFORE any checkpoint, oracle or scoring: pools, then checkpoints
        used.update(validate_pools(rw, cfg, pools, [(s, a, m) for a, m in scored
                                                     for s in ("train", "dev")], E.shape[1]))
        for a, m in scored:
            used.update(validate_checkpoints(rw, outcomes[(a, m)], cfg, a, m,
                                             pools["pools"][f"train:{a}:{m}"],
                                             pools["pools"][f"dev:{a}:{m}"]))
        pairs: list[PairEvidence | None] = []
        for m in cfg.masters:
            oc = {a: outcomes[(a, m)] for a in ARMS}
            if not all(_complete(o) for o in oc.values()):
                res["pairs"][str(m)] = {"status": "INCOMPLETE_PAIR",
                                        "outcomes": {a: o and o["status"] for a, o in oc.items()}}
                pairs.append(None)
                continue
            reg = {}
            for arm in ARMS:
                key = f"dev:{arm}:{m}"
                obs = rw.load(ObservationSet, pools["pools"][key], consumer="experiment")
                q = oracle_q32(kernels[arm], E, pi, obs.tokens, guard=_guard(sc, reserve))
                reg[arm] = _regret_curve(rw, sc, oc[arm]["checkpoints"], _inputs(obs), q,
                                         reserve)
                arrays[f"regret_{arm}_{m}.npz"] = {"regret": reg[arm],
                                                   "grid": np.asarray(cfg.grid)}
            rc = {a: ratio_curve(reg[a], cfg.gc[a]) for a in ARMS}
            ev = {a: grid_event(list(pass_sequence(rc[a])), cfg.grid) for a in ARMS}
            boot = paired_bootstrap_endpoint(
                reg["a020"], reg["a0"], cfg.gc["a020"], cfg.gc["a0"],
                SeedTree(m).generator(NAMESPACE, "endpoint_bootstrap"),
                n_draws=cfg.bootstrap_draws, grid=cfg.grid, guard=_guard(sc, reserve))
            pe = PairEvidence(difference_bounds(ev["a020"], ev["a0"]), boot.q025_low,
                              boot.q975_high, (ev["a020"], ev["a0"]))
            pairs.append(pe)
            res["pairs"][str(m)] = {
                "events": {a: dataclasses.asdict(e) for a, e in ev.items()},
                "point": dataclasses.asdict(pe.point), "q025_low": pe.q025_low,
                "q975_high": pe.q975_high, "censored_frac": {
                    "a020": boot.censored_curved_frac, "a0": boot.censored_flat_frac},
                "ratios": {a: rc[a].tolist() for a in ARMS},
                "dev_auc": {a: dev_auc(rc[a], cfg.grid) for a in ARMS}}
        verify_full(ro, exp, "sources before export")
        verify_full(rw, used, "used pools and checkpoints before export")
        res["verdict"], res["reason"] = cohort_verdict(pairs, res["failures"],
                                                       len(cfg.masters))
        ctl.outcome = f"{res['verdict']}: {res['reason']}"
        study_export(sc, out, {"result.json": res,
                               "run.json": _meta(cfg, repo, ctl, "dev-analysis", report),
                               "verdict.json": {"verdict": res["verdict"],
                                                "reason": res["reason"]}}, arrays,
                     reserve=reserve)
    return res


def _pool_ids(rw: ArtifactStore, pools: dict) -> np.ndarray:
    """Sequence IDs of the study's (already identity-checked) train and dev pools."""
    return np.concatenate([np.asarray(rw.load(ObservationSet, oid, consumer="experiment")
                                      .sequence_id, np.int64) for oid in pools["pools"].values()])


def run_final_test(cfg: StudyConfig, repo: Path, authorized: bool) -> dict:
    """Fresh test (generated here only), step-final checkpoints only; needs authorisation."""
    report = validate_config(cfg, repo)
    if not authorized:
        raise StudyFailed("final-test requires explicit authorisation (--authorized-final)")
    verify_export_complete(tables(cfg, "dev_analysis"))
    pools = complete_pools(cfg)
    outcomes = {(a, m): complete_outcome(cfg, a, m) for m in cfg.masters for a in ARMS}
    out = ensure_new_output_dir(tables(cfg, "final_test"))
    ro, rw = stores(cfg, repo)
    exp = cfg.expected_sources()
    torch.set_num_threads(cfg.threads)
    res: dict = {"test_pools": {}, "models": {}}
    with _controls(cfg, "x5g1t-final-test") as ctl:
        sc = _study(cfg, ctl, "final_test")
        reserve = evaluation_reserve(0, 0)
        verify_full(ro, exp, "sources before final test")
        V = int(_sources(ro, cfg)[1].shape[1])
        used = validate_pools(rw, cfg, pools, [(s, a, m) for s in ("train", "dev")
                                               for m in cfg.masters for a in ARMS], V)
        for (arm, m), o in outcomes.items():
            if _complete(o):
                used.update(validate_checkpoints(
                    rw, o, cfg, arm, m, pools["pools"][f"train:{arm}:{m}"],
                    pools["pools"][f"dev:{arm}:{m}"]))
        n = cfg.sizes["test"]
        plan = {f"test:{a}:{TEST_MASTER}": sequence_ids("test", a, TEST_MASTER, n)
                for a in ARMS}
        stored, seen = collision_inputs(ro)
        res["collisions"] = collisions(plan, np.concatenate([stored, _pool_ids(rw, pools)]))
        if any(res["collisions"].values()):
            raise StudyFailed(f"fresh test namespace collision {res['collisions']}")
        kernels, E, perm, pi = _sources(ro, cfg)
        sc.boundary("draw test", 30.0, reserve)
        named = draw_pair(kernels, E, perm, pi, "test", TEST_MASTER, n)
        sc.boundary("draw test done", EST["save"], reserve)
        tests = {}
        for arm in ARMS:
            obs = pool_observation("test", named[arm], plan[f"test:{arm}:{TEST_MASTER}"],
                                   E.shape[1])
            sc.boundary(f"save test {arm}", EST["save"], reserve)
            oid = rw.save(obs, config=study_pool_config("test", arm, TEST_MASTER, cfg.protocol),
                          parents=[cfg.sources["T"][arm][0], cfg.sources["E"][0]],
                          seed_map={"/".join(map(str, (0, *stream("test")))):
                                    SeedTree(0).seed(*stream("test"))}, consumer="experiment")
            res["test_pools"][arm] = oid
            sc.boundary(f"save test {arm} done", EST["save"], reserve)
            used.update(validate_pool(rw, oid, rw.meta(oid).payload_sha256, cfg, "test", arm,
                                      TEST_MASTER, V))
            tests[arm] = (_inputs(obs), oracle_q32(kernels[arm], E, pi, obs.tokens,
                                                   guard=_guard(sc, reserve)))
        for m in cfg.masters:
            for arm in ARMS:
                o = outcomes[(arm, m)]
                if not _complete(o):
                    res["models"][f"{arm}_{m}"] = {"status": o and o["status"]}
                    continue
                reg = _regret_curve(rw, sc, o["checkpoints"][-1:], *tests[arm], reserve)
                res["models"][f"{arm}_{m}"] = {"step": o["checkpoints"][-1]["step"],
                                              "regret": float(reg.mean()),
                                              "ratio": float(reg.mean() / cfg.gc[arm])}
        verify_full(ro, exp, "sources before export")
        verify_full(ro, seen, "collision inputs before export")
        verify_full(rw, used, "pools and checkpoints before export")
        ctl.outcome = "FINAL_TEST_DONE"
        study_export(sc, out, {"result.json": res,
                               "run.json": _meta(cfg, repo, ctl, "final-test", report)},
                     reserve=reserve)
    return res
