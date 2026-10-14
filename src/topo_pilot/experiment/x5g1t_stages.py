"""X5 G1 training-study stages (x5g1-train-v3 §10): ``pools``, ``train``, ``dev_analysis`` and
``final_test``, each inside ``RunControls`` on the scientific ledger, with full-hash source
checks before and after, guarded saves and an immutable, manifested output directory.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
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
    EmissionSpec,
    LocalFSBackend,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    TransitionSpec,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import ModelConfig, load_model

from .config import producer_version
from .x4b import ReadThroughBackend
from .x4b_run import peak_memory_bytes
from .x5g1_controls import RunControls
from .x5g1_safety import ensure_new_output_dir, guarded_export, verify_sources_full
from .x5g1t_lineage import (
    ARMS,
    NAMESPACE,
    TEST_MASTER,
    collisions,
    draw_pair,
    pool_config,
    pool_observation,
    sequence_ids,
    stream,
)
from .x5g1t_oracle import oracle_q32
from .x5g1t_runtime import (
    EST,
    BudgetPlanner,
    StudyControls,
    evaluation_reserve,
    read_outcome,
)
from .x5g1t_score import regret_rows
from .x5g1t_train import study_train_config, train_one

PROTOCOL_DOC = "docs/proposals/X5_G1_TRAINING_PROTOCOL_V3.md"


class StudyFailed(RuntimeError):
    """Integrity, collision, prerequisite or authorisation failure (not a scientific verdict)."""


@dataclasses.dataclass(frozen=True)
class StudyConfig:
    protocol: str
    read_roots: tuple[str, ...]
    study_root: str
    ledger_path: str
    mailbox: str
    sources: dict
    masters: tuple
    sizes: dict
    model_config: dict
    steps: int
    grid: tuple[int, ...]
    gc: dict
    threads: int = 1
    bootstrap_draws: int = 2000
    cap_s: float = 21600.0
    cumulative_cap_s: float = 21600.0
    check_stored_ids: bool = True

    @classmethod
    def load(cls, path: Path) -> StudyConfig:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        for k in ("read_roots", "masters", "grid"):
            d[k] = tuple(d[k])
        return cls(**d)

    @property
    def root(self) -> Path:
        return Path(self.study_root)


def _chain(roots) -> object:
    backends = [LocalFSBackend(Path(r)) for r in roots]
    ro = backends[0]
    for b in backends[1:]:
        ro = ReadThroughBackend(b, ro)
    return ro


def stores(cfg: StudyConfig, repo: Path) -> tuple[ArtifactStore, ArtifactStore]:
    """(read-only sources, read-through study store writing only to ``study_root/store``)."""
    ro = ArtifactStore(_chain(cfg.read_roots))
    rw = ArtifactStore(ReadThroughBackend(_chain(cfg.read_roots),
                                          LocalFSBackend(cfg.root / "store")),
                       producer_version=producer_version(repo))
    return ro, rw


def expected_sources(cfg: StudyConfig) -> dict:
    exp = {aid: (TransitionSpec, sha) for aid, sha in cfg.sources["T"].values()}
    eid, esha = cfg.sources["E"]
    exp[eid] = (EmissionSpec, esha)
    return exp


def _verify(store: ArtifactStore, expected: dict, when: str) -> None:
    bad = verify_sources_full(store, expected)
    if bad:
        raise StudyFailed(f"integrity {when}: " + "; ".join(bad))


def _sources(store: ArtifactStore, cfg: StudyConfig):
    kernels = {arm: np.asarray(store.load(TransitionSpec, cfg.sources["T"][arm][0],
                                          consumer="experiment").T) for arm in ARMS}
    emis = store.load(EmissionSpec, cfg.sources["E"][0], consumer="experiment")
    pi = np.asarray(store.load(TransitionSpec, cfg.sources["T"]["a0"][0],
                               consumer="experiment").pi)
    return kernels, np.asarray(emis.E, float), np.asarray(emis.symbol_perm), pi


def _controls(cfg: StudyConfig, job: str) -> RunControls:
    return RunControls(Path(cfg.ledger_path), cfg.cap_s, Path(cfg.mailbox) / "STOP", job,
                       cfg.cumulative_cap_s)


def _study(cfg: StudyConfig, ctl: RunControls, name: str) -> StudyControls:
    return StudyControls(ctl, Path(cfg.mailbox), BudgetPlanner(cfg.cumulative_cap_s),
                         cfg.root, cfg.root / "runs" / f"hold_{name}.json")


def _export(ctl: RunControls, out: Path, files: dict, arrays: dict | None = None) -> None:
    def write(name: str, obj) -> None:
        (out / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")

    def manifest() -> None:
        sums = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                for f in sorted(out.iterdir()) if f.name != "MANIFEST.json"}
        (out / "MANIFEST.json").write_text(json.dumps(sums, indent=1), encoding="utf-8")

    steps = [(n, (lambda n=n, o=o: write(n, o))) for n, o in files.items()]
    steps += [(n, (lambda n=n, a=a: np.savez(out / n, **a))) for n, a in (arrays or {}).items()]
    guarded_export(ctl, steps + [("manifest", manifest)], out / "EXPORT_STATUS.json")


def _meta(cfg: StudyConfig, repo: Path, ctl: RunControls, stage: str) -> dict:
    doc = Path(repo) / PROTOCOL_DOC
    return {"protocol": cfg.protocol, "stage": stage, "producer_version": producer_version(repo),
            "protocol_doc_sha256": hashlib.sha256(doc.read_bytes()).hexdigest()
            if doc.exists() else None, "python": sys.executable, "torch": torch.__version__,
            "threads": torch.get_num_threads(), "cpu_s": round(ctl.cpu(), 3),
            "cpu_prior_cumulative": ctl.prior, "peak_memory_bytes": peak_memory_bytes(),
            "steps": ctl.steps}


def run_pools(cfg: StudyConfig, repo: Path) -> dict:
    """Train and dev pools for every master and arm (never the fresh test)."""
    out = ensure_new_output_dir(cfg.root / "tables" / "pools")
    ro, rw = stores(cfg, repo)
    exp = expected_sources(cfg)
    res: dict = {"pools": {}, "pool_sha256": {}}
    with _controls(cfg, "x5g1t-pools") as ctl:
        sc = _study(cfg, ctl, "pools")
        reserve = evaluation_reserve(0, 0)
        _verify(ro, exp, "before")
        plan = {f"{s}:{a}:{m}": sequence_ids(s, a, m, cfg.sizes[s])
                for s in ("train", "dev") for m in cfg.masters for a in ARMS}
        stored = (np.concatenate([np.asarray(ro.load(ObservationSet, a, consumer="experiment")
                                             .sequence_id, np.int64)
                                  for a in ro.find(ObservationSet)] or [np.zeros(0, np.int64)])
                  if cfg.check_stored_ids else np.zeros(0, np.int64))
        res["collisions"] = collisions(plan, stored)
        if any(res["collisions"].values()):
            raise StudyFailed(f"namespace collision {res['collisions']}")
        kernels, E, perm, pi = _sources(ro, cfg)
        for split in ("train", "dev"):
            for m in cfg.masters:
                sc.boundary(f"pools {split} {m}", 30.0, reserve)
                named = draw_pair(kernels, E, perm, pi, split, m, cfg.sizes[split])
                for arm in ARMS:
                    key = f"{split}:{arm}:{m}"
                    obs = pool_observation(split, named[arm], plan[key], E.shape[1])
                    sc.boundary(f"save {key}", EST["save"], reserve)
                    oid = rw.save(obs, config=pool_config(split, arm, m),
                                  parents=[cfg.sources["T"][arm][0], cfg.sources["E"][0]],
                                  seed_map={"/".join(map(str, (m, *stream(split)))):
                                            SeedTree(m).seed(*stream(split))},
                                  consumer="experiment")
                    res["pools"][key] = oid
                    res["pool_sha256"][key] = rw.meta(oid).payload_sha256
                    sc.boundary(f"save {key} done", EST["save"], reserve)
                res[f"first_symbol_equal:{split}:{m}"] = bool(np.array_equal(
                    named["a0"][:, 0], named["a020"][:, 0]))
        _verify(ro, exp, "after")
        ctl.outcome = "POOLS_DONE"
        _export(ctl, out, {"pools.json": res, "run.json": _meta(cfg, repo, ctl, "pools")})
    return res


def _pools(cfg: StudyConfig) -> dict:
    p = cfg.root / "tables" / "pools" / "pools.json"
    if not p.exists():
        raise StudyFailed("pools stage has not completed")
    return json.loads(p.read_text(encoding="utf-8"))


def _pool_expected(pools: dict, keys) -> dict:
    return {pools["pools"][k]: (ObservationSet, pools["pool_sha256"][k]) for k in keys}


def run_train(cfg: StudyConfig, repo: Path, arm: str, master) -> dict:
    """One model; the outcome is recorded by ``train_one`` on every exit."""
    pools = _pools(cfg)
    keys = (f"train:{arm}:{master}", f"dev:{arm}:{master}")
    out = ensure_new_output_dir(cfg.root / "tables" / "train" / f"{arm}_{master}")
    ro, rw = stores(cfg, repo)
    exp = {**expected_sources(cfg), **_pool_expected(pools, keys)}
    torch.set_num_threads(cfg.threads)
    with _controls(cfg, f"x5g1t-train-{arm}-{master}") as ctl:
        sc = _study(cfg, ctl, f"{arm}_{master}")
        n_models = 2 * len(cfg.masters)
        reserve = evaluation_reserve(len(cfg.grid) * n_models, n_models)
        _verify(rw, exp, "before")
        outcome = train_one(rw, pools["pools"][keys[0]], pools["pools"][keys[1]],
                            ModelConfig(**cfg.model_config),
                            study_train_config(cfg.steps, cfg.grid), master, arm, cfg.root, sc,
                            reserve_s=reserve)
        _verify(rw, exp, "after")
        ctl.outcome = outcome["status"]
        _export(ctl, out, {"outcome.json": outcome,
                           "run.json": _meta(cfg, repo, ctl, f"train {arm} {master}")})
    return outcome


def _inputs(obs: ObservationSet) -> torch.Tensor:
    ds = PublicTokenDataset(obs, SequenceLayout())
    return torch.stack([ds[i][0] for i in range(len(ds))])


def _regret_curve(rw: ArtifactStore, sc: StudyControls, ckpts: list, inputs, q,
                  reserve: float) -> np.ndarray:
    reg = np.empty((inputs.shape[0], len(ckpts)))
    for k, c in enumerate(ckpts):
        sc.boundary(f"score {c['checkpoint_id']}", EST["score"], reserve)
        _verify(rw, {c["checkpoint_id"]: (Checkpoint, c["payload_sha256"])}, "checkpoint")
        model = load_model(rw.load(Checkpoint, c["checkpoint_id"], consumer="experiment"))
        reg[:, k] = regret_rows(model, inputs, q)
    return reg


def run_dev_analysis(cfg: StudyConfig, repo: Path) -> dict:
    """Dense dev regret curves, grid events, paired bootstrap and the cohort verdict."""
    pools = _pools(cfg)
    out = ensure_new_output_dir(cfg.root / "tables" / "dev_analysis")
    ro, rw = stores(cfg, repo)
    exp = expected_sources(cfg)
    torch.set_num_threads(cfg.threads)
    res: dict = {"pairs": {}, "failures": []}
    arrays: dict = {}
    with _controls(cfg, "x5g1t-dev-analysis") as ctl:
        sc = _study(cfg, ctl, "dev_analysis")
        reserve = evaluation_reserve(0, 2 * len(cfg.masters))
        _verify(ro, exp, "before")
        kernels, E, _, pi = _sources(ro, cfg)
        pairs: list[PairEvidence | None] = []
        for m in cfg.masters:
            oc = {a: read_outcome(cfg.root, a, m) for a in ARMS}
            if not all(o and o["status"] == "COMPLETE"
                       and [c["step"] for c in o["checkpoints"]] == list(cfg.grid)
                       for o in oc.values()):
                res["pairs"][str(m)] = {"status": "INCOMPLETE_PAIR",
                                        "outcomes": {a: o and o["status"] for a, o in oc.items()}}
                pairs.append(None)
                continue
            reg = {}
            for arm in ARMS:
                key = f"dev:{arm}:{m}"
                _verify(rw, _pool_expected(pools, [key]), "dev pool")
                obs = rw.load(ObservationSet, pools["pools"][key], consumer="experiment")
                q = oracle_q32(kernels[arm], E, pi, obs.tokens)
                reg[arm] = _regret_curve(rw, sc, oc[arm]["checkpoints"], _inputs(obs), q,
                                         reserve)
                arrays[f"regret_{arm}_{m}.npz"] = {"regret": reg[arm],
                                                   "grid": np.asarray(cfg.grid)}
            rc = {a: ratio_curve(reg[a], cfg.gc[a]) for a in ARMS}
            ev = {a: grid_event(list(pass_sequence(rc[a])), cfg.grid) for a in ARMS}
            boot = paired_bootstrap_endpoint(
                reg["a020"], reg["a0"], cfg.gc["a020"], cfg.gc["a0"],
                SeedTree(m).generator(NAMESPACE, "endpoint_bootstrap"),
                n_draws=cfg.bootstrap_draws, grid=cfg.grid,
                guard=lambda s: sc.boundary(s, 1.0, reserve))
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
        _verify(ro, exp, "after")
        res["verdict"], res["reason"] = cohort_verdict(pairs, res["failures"],
                                                       len(cfg.masters))
        ctl.outcome = f"{res['verdict']}: {res['reason']}"
        _export(ctl, out, {"result.json": res,
                           "run.json": _meta(cfg, repo, ctl, "dev-analysis"),
                           "verdict.json": {"verdict": res["verdict"],
                                            "reason": res["reason"]}}, arrays)
    return res


def run_final_test(cfg: StudyConfig, repo: Path, authorized: bool) -> dict:
    """Fresh test (generated here only), step-final checkpoints only; needs authorisation."""
    if not authorized:
        raise StudyFailed("final-test requires explicit authorisation (--authorized-final)")
    if not (cfg.root / "tables" / "dev_analysis" / "verdict.json").exists():
        raise StudyFailed("final-test refused: dev-analysis verdict not written")
    out = ensure_new_output_dir(cfg.root / "tables" / "final_test")
    ro, rw = stores(cfg, repo)
    exp = expected_sources(cfg)
    torch.set_num_threads(cfg.threads)
    res: dict = {"test_pools": {}, "models": {}}
    with _controls(cfg, "x5g1t-final-test") as ctl:
        sc = _study(cfg, ctl, "final_test")
        reserve = evaluation_reserve(0, 0)
        _verify(ro, exp, "before")
        kernels, E, perm, pi = _sources(ro, cfg)
        n = cfg.sizes["test"]
        named = draw_pair(kernels, E, perm, pi, "test", TEST_MASTER, n)
        tests = {}
        for arm in ARMS:
            obs = pool_observation("test", named[arm],
                                   sequence_ids("test", arm, TEST_MASTER, n), E.shape[1])
            sc.boundary(f"save test {arm}", EST["save"], reserve)
            res["test_pools"][arm] = rw.save(
                obs, config=pool_config("test", arm, TEST_MASTER),
                parents=[cfg.sources["T"][arm][0], cfg.sources["E"][0]],
                seed_map={"/".join(map(str, (0, *stream("test")))):
                          SeedTree(0).seed(*stream("test"))}, consumer="experiment")
            sc.boundary(f"save test {arm} done", EST["save"], reserve)
            tests[arm] = (_inputs(obs), oracle_q32(kernels[arm], E, pi, obs.tokens))
        for m in cfg.masters:
            for arm in ARMS:
                o = read_outcome(cfg.root, arm, m)
                if not (o and o["status"] == "COMPLETE"):
                    res["models"][f"{arm}_{m}"] = {"status": o and o["status"]}
                    continue
                reg = _regret_curve(rw, sc, o["checkpoints"][-1:], *tests[arm], reserve)
                res["models"][f"{arm}_{m}"] = {"step": o["checkpoints"][-1]["step"],
                                              "regret": float(reg.mean()),
                                              "ratio": float(reg.mean() / cfg.gc[arm])}
        _verify(ro, exp, "after")
        ctl.outcome = "FINAL_TEST_DONE"
        _export(ctl, out, {"result.json": res, "run.json": _meta(cfg, repo, ctl, "final-test")})
    return res
