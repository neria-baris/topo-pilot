"""HWSB synthetic dry run DRB1-DRB16 and DRB13b (API.md §9; TEST_PLAN §4; protocol §7).

Streams ("data", "hwsb-v1", "DRY", <case>, ...) and masters 629901/629902 only. Persisted
histories come only from the tiny world, under the dry store, never named HIST_*.npz; w* rows
(DRB2, DRB12 builds) stay in memory. Planted fixtures are labelled "fixture": true.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import dataclasses
import json
import shutil
import subprocess
import time
from fractions import Fraction
from pathlib import Path

import hws_worlds
import hwsb_data as hd
import hwsb_driver as hdr
import hwsb_eval as he
import hwsb_gates as hg
import hwsb_known as hk
import hwsb_records
import hwsb_stages as hs
import hwsb_train as ht
import numpy as np
import stage_records

from topo_pilot.activations import ActivationExtractor
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    MemoryBackend,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.dataset import DatasetConfig, DatasetStage, PanelBuilder
from topo_pilot.learner import LearnerStage, TransformerLM
from topo_pilot.process import TransitionConfig
from topo_pilot.process._diagnostics import emission_diagnostics
from topo_pilot.process.stage import ProcessStage
from topo_pilot.world import WorldConfig
from topo_pilot.world.stage import WorldStage

FIX = {"fixture": True}


def build_tiny_process(store, masters=hc.DRY_MASTERS) -> dict:
    wid = WorldStage().run(WorldConfig("cylinder", (6, 2), "flat"), store)
    tid = ProcessStage().run_transition(wid, TransitionConfig(p_stay=0.5), store)
    E_canon = np.asarray(hws_worlds.build_tiny()["E"], dtype=np.float64)
    ems, eid = {}, {}
    for m in masters:
        perm = SeedTree(int(m)).generator("symbol_names", "cylinder", int(m)).permutation(3)
        E_named = np.empty_like(E_canon)
        E_named[:, perm] = E_canon
        spec = EmissionSpec(
            E=E_named,
            symbol_perm=perm.astype(np.int64),
            mode="overlap",
            sigma=1.0,
            centers=np.column_stack((0.5 + 2.0 * np.arange(3), np.full(3, 0.5))),
            center_strategy="dry_tiny",
            diagnostics=emission_diagnostics(E_named, E_canon, (6, 2), 0.0),
        )
        eid[int(m)] = store.save(
            spec,
            config={"dry_tiny": True, "replicate": int(m)},
            parents=[wid],
            seed_map={},
            consumer="process",
        )
        ems[int(m)] = store.load(EmissionSpec, eid[int(m)], consumer=hd.READER)
    world = store.load(WorldSpec, wid, consumer=hd.READER)
    trans = store.load(TransitionSpec, tid, consumer=hd.READER)
    feats = hws_worlds.features(np.asarray(world.coords, dtype=np.float64), 6)
    proc = hd.assemble(
        world, trans, ems, {"world": wid, "transition": tid, "emission": eid}, feats, n_axial=1
    )
    proc.update(sigma=Fraction(1), neighbour=Fraction(1, 8))
    return proc


def _res(ok, **details) -> dict:
    return {"status": "PASS" if ok else "FAIL", "details": hk.jsonable(details)}


def _dir(out, case) -> Path:
    d = Path(out) / case / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d.mkdir(parents=True, exist_ok=False)
    return d


def _fs(d) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(d) / "artifacts"))


def _mem() -> ArtifactStore:
    return ArtifactStore(MemoryBackend())


def _tiny_plan(case, steps=None, ckpts=None, sizes=None):
    p = hc.dry_plan("dry_tiny", case)
    tc = (
        p.train_cfg
        if steps is None
        else dataclasses.replace(
            p.train_cfg, steps=steps, checkpoint_steps=tuple(ckpts), warmup=min(20, steps)
        )
    )
    return dataclasses.replace(p, train_cfg=tc, sizes=dict(sizes or p.sizes), gate_step=tc.steps)


def drb1(out, ctx) -> dict:
    d, plan = _dir(out, "DRB1"), _tiny_plan("DRB1")
    store = _fs(d)
    proc = build_tiny_process(store)
    recs = {m: hs.train_core(d, store, proc, m, plan) for m in plan.masters}
    rep = hs.eval_core(d, plan, proc, store, recs)
    keys = ("outcome", "licence", "gates", "per_model", "h2b")
    ok = (
        all(r["status"] == "COMPLETE" for r in recs.values())
        and all(k in rep for k in keys)
        and (d / "HANDOFF.json").exists()
        and not list(d.rglob("HIST_*.npz"))
        and set(rep["gates"])
        == {"BLOCKS", "H2-B", "KB7", "B1", "B4", "B8a", "B6", "B5", "B7", "B9a"}
    )
    return _res(ok, outcome=rep["outcome"], gates=rep["gates"])


def drb2(out, ctx) -> dict:
    plan = hc.dry_plan("dry_e4", "DRB2")
    m, res = plan.masters[0], []
    for _ in range(2):
        st = _mem()
        proc = hd.build_process(st, masters=(m,))
        res.append((st, hd.make_train_dev(st, proc, m, plan)))
    (sa, ia), (sb, ib) = res
    a = ht.train(sa, ia, m, plan)
    b = LearnerStage().run(
        ib["train"], ib["dev"], plan.model_cfg, plan.train_cfg, SeedTree(m), hc.run_key(plan, m), sb
    )
    steps = sorted(a["checkpoint_ids"])
    ids_eq = [a["checkpoint_ids"][s] for s in steps] == b
    ck_eq = all(sb.meta(i).payload_sha256 == a["checksums"][s] for s, i in zip(steps, b))
    cfg = plan.model_cfg
    shapes = cfg.vocab_in == 37 and cfg.vocab_out == 36 and hc.BOS == 36 and steps == [0, 10, 20]
    import hwsb_dry2

    ev = hwsb_dry2.e4_eval_check(sa, a["checkpoint_ids"][20], res[0][1], proc, m, plan)
    return _res(ids_eq and ck_eq and shapes and ev["ok"], ids=b, eval=ev, persisted=False)


def drb3(out, ctx) -> dict:
    extra = hc.ROOT / "topo-pilot" / "artifacts" / "Checkpoint" / "c3358e3cb9c352fb" / "extra.json"
    e = json.loads(extra.read_text(encoding="utf-8"))
    ref = {"model_config": e["model_config"], "train_config": e["train_config"]}
    base = [
        ht.check_recipe(hc.MODEL_CFG, hc.TRAIN_CFG)["status"],
        ht.check_recipe(hc.MODEL_CFG, hc.TRAIN_CFG, ref)["status"],
    ]
    refused = []
    for which, cfg in (("model_config", hc.MODEL_CFG), ("train_config", hc.TRAIN_CFG)):
        for f in dataclasses.fields(cfg):
            v = getattr(cfg, f.name)
            bad = (
                (not v)
                if isinstance(v, bool)
                else (v + (1,))
                if isinstance(v, tuple)
                else (v + "x")
                if isinstance(v, str)
                else v * 2 + 1
            )
            mc = (
                dataclasses.replace(hc.MODEL_CFG, **{f.name: bad})
                if which == "model_config"
                else hc.MODEL_CFG
            )
            tc = (
                dataclasses.replace(hc.TRAIN_CFG, **{f.name: bad})
                if which == "train_config"
                else hc.TRAIN_CFG
            )
            r = ht.check_recipe(mc, tc)
            refused.append(
                r["status"] != "PASS" and any(x["field"] == f"{which}.{f.name}" for x in r["diff"])
            )
    return _res(base == ["PASS", "PASS"] and all(refused), n_planted=len(refused))


def drb4(out, ctx) -> dict:
    st = _mem()
    proc = hk.w0_process(st)
    cfg = DatasetConfig(n_train=600, n_dev=300, n_test=128, n_panels=1, panel_size=64)
    ids = DatasetStage().run(
        proc["ids"]["transition"], proc["ids"]["emission"][1729], cfg, SeedTree(1729), st
    )
    ok = []
    for split, n in (("train", 600), ("dev", 300)):
        ref = st.load(ObservationSet, ids[f"obs_{split}"], consumer="experiment").tokens
        rng = SeedTree(1729).generator("data", split, "cylinder", "overlap", "1.25", 1729)
        got = hd.sample_observations(
            proc["T"], proc["E_named"][1729], proc["pi"], proc["perm"][1729], n, rng, split
        )
        ok.append(got.dtype == ref.dtype and got.tobytes() == ref.tobytes())
    return _res(all(ok), equal=ok)


def _dirichlet(rng, n, V=36) -> np.ndarray:
    return rng.dirichlet(np.ones(V), size=n)


def drb5(out, ctx) -> dict:
    rng = np.random.default_rng(5)
    q = {1: _dirichlet(rng, 64), 4: _dirichlet(rng, 64), 32: _dirichlet(rng, 64)}
    r32, r1, r4 = he.b1(q, q[32]), he.b1(q, q[1]), he.b2(q, q[4])
    perm = rng.permutation(36)
    named = np.empty_like(q[32])
    named[:, perm] = q[32]
    marg = he.b3(q, q[32])
    ok = (
        abs(r32["regret"]) <= 1e-12
        and abs(r32["captured"] - 1) <= 1e-12
        and abs(r1["captured"]) <= 1e-12
        and abs(r4["d_mean"]) <= 1e-12
        and r4["L"] <= 0
        and np.array_equal(he.to_canonical(named, perm), q[32])
        and abs(marg["d_mean"] - marg["G_hat"]) <= 1e-12
    )
    return _res(ok, **FIX)


def drb6(out, ctx) -> dict:
    import torch

    cfg = hc.dry_plan("dry_tiny", "DRB6").model_cfg
    torch.manual_seed(6)
    model = TransformerLM(cfg).eval()
    rng = np.random.default_rng(6)
    obs = ObservationSet(
        split="test",
        V=3,
        sequence_id=np.arange(128, dtype=np.int64),
        tokens=rng.integers(0, 3, (128, 33)).astype(np.uint8),
    )
    idx = PanelBuilder().build(
        obs,
        DatasetConfig(n_test=128, n_panels=1, panel_size=128),
        np.random.default_rng(7),
        dataset_id="drb6",
    )
    _, ref, _ = ActivationExtractor(("resid_post_0",), 256).extract(model, obs, idx)
    pos = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    rows = np.array([pos[int(s)] for s in idx.sequence_id.tolist()])
    inputs = torch.from_numpy(SequenceLayout().model_inputs(obs.tokens[rows], 3))
    got = he.logits32(model, inputs)
    return _res(got.dtype == ref.dtype and got.tobytes() == ref.tobytes(), **FIX)


def _embed(rng, th, B, noise=0.01) -> np.ndarray:
    X = np.cos(th)[:, None] * B[:, 0] + np.sin(th)[:, None] * B[:, 1]
    return X + noise * rng.normal(size=(th.size, B.shape[0]))


def drb7(out, ctx) -> dict:
    rng, d = np.random.default_rng(7), _dir(out, "DRB7")
    ms, ids = list(hc.DRY_MASTERS), np.arange(512, dtype=np.int64) + 10**9
    th, thv = rng.uniform(0, 2 * np.pi, 512), rng.uniform(0, 2 * np.pi, 512)
    Bs = {m: np.linalg.qr(rng.normal(size=(128, 2)))[0] for m in ms}
    Xc = {m: _embed(rng, th, Bs[m]) for m in ms}
    Xv = {m: _embed(rng, thv, Bs[m]) for m in ms}
    Xi = {m: rng.normal(size=(512, 128)) for m in ms}
    m32 = 0.9 * np.column_stack((np.cos(th), np.sin(th)))
    cal = hg.b4_cal(d, Xc, ids, m32)
    init = hg.b4_init(d, Xi, ids, m32)
    hg.b4_freeze(d, cal, init)
    val = hg.b4_val(d, cal, Xv, ids + 512)
    s = hg.b4_status(cal, val, ms)
    trained, _ = hg.k4b_charts.open_ledgers(d)
    try:
        trained.claim(ms[0], "production")
        twice = False
    except Exception:  # noqa: BLE001  the ledger refuses a second claim
        twice = True
    refrozen = bool(hg.k4b_charts.require_frozen(d))
    sc = hg.b4_cal(
        _dir(out, "DRB7-scrambled"), {m: rng.normal(size=(512, 128)) for m in ms}, ids, m32
    )
    s2 = hg.b4_status(sc, {"status": {m: hg.NOT_CHARTED for m in ms}}, ms)
    init_st = [init["per_model"][m]["status"] for m in ms]
    ok = (
        s["pass"]
        and twice
        and refrozen
        and s2["criterion"] == "C0_CAL"
        and all(x in ("PASS", "INIT_UNAVAILABLE") for x in init_st)
    )
    return _res(ok, status=s, scrambled=s2, init=init_st, **FIX)


def _tiny_store(d, case, sizes=None, steps=None):
    store = _fs(d) if d is not None else _mem()
    proc = build_tiny_process(store)
    plan = _tiny_plan(
        case,
        steps,
        (0, 10, 20) if steps else None,
        sizes or {"train": 256, "dev": 64, "LGATE": 64, "CAL": 64, "VAL": 64},
    )
    return store, proc, plan


CASE_NAMES = (
    "DRB1",
    "DRB2",
    "DRB3",
    "DRB4",
    "DRB5",
    "DRB6",
    "DRB7",
    "DRB8",
    "DRB9",
    "DRB10",
    "DRB11",
    "DRB12",
    "DRB13",
    "DRB13b",
    "DRB14",
    "DRB15",
    "DRB16",
)
CASES = [(n, globals()[n.lower()]) for n in CASE_NAMES[:7]] + [(n, None) for n in CASE_NAMES[7:]]


def run_dry(out=hc.DRY_STORE, sched=None, only=None) -> dict:
    import hwsb_dry2

    CASES[7:] = [(n, getattr(hwsb_dry2, n.lower())) for n in CASE_NAMES[7:]]
    if not hdr.sched_ok(sched, "DRY")["ok"]:
        return {"status": "REFUSED", "reason": "P-SCHED rule 2 not met"}
    out = Path(out)
    cases, ctx = {}, {}
    for name, fn in CASES:
        if only and name not in only:
            continue
        try:
            cases[name] = fn(out, ctx)
        except Exception as exc:  # noqa: BLE001  a crashing case is a FAIL, recorded
            cases[name] = {"status": "FAIL", "details": f"{type(exc).__name__}: {exc}"}
    head = subprocess.run(
        ["git", "-C", str(hc.REPO), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "-C", str(hc.REPO), "status", "--porcelain", "--", "tools/hwsb", "tests/hwsb"],
        capture_output=True,
        text=True,
    ).stdout
    files = hwsb_records.implementation_files(hc.REPO, head)
    rep = {
        "cases": cases,
        "all_pass": all(c["status"] == "PASS" for c in cases.values()) and len(cases) == len(CASES),
        "implementation_files": files,
        "implementation_sha256": hwsb_records.hws_records.sha_bytes(
            hwsb_records.canonical_json(files).encode("utf-8")
        ),
        "h_exec": head,
        "tree_clean": dirty.strip() == "",
        "utc": hwsb_records.utc(),
    }
    path = out / "stages" / "DRY" / "DRY_REPORT.json"
    if path.exists():
        arch = out / "superseded" / f"DRY-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
        arch.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path.parent), str(arch))
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, hk.jsonable(rep))
    return rep
