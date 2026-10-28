"""HWSB dry-run cases DRB8-DRB16 and DRB13b (API.md §9; TEST_PLAN §4); split from hwsb_dry
by size. Same rules: DRY streams and masters only; planted fixtures labelled "fixture": true.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import json
import shutil
import types
from fractions import Fraction
from pathlib import Path

import hws_driver
import hwsb_data as hd
import hwsb_driver as hdr
import hwsb_eval as he
import hwsb_gates as hg
import hwsb_known as hk
import hwsb_law as hl
import hwsb_meter_bind as hm
import hwsb_train as ht
import k4b_stats
import numpy as np
import precision
import process_law
import scores
import stage_records
from hwsb_dry import FIX, _dir, _mem, _res, _tiny_store

from topo_pilot.activations import ActivationExtractor
from topo_pilot.contracts import Checkpoint, ObservationSet
from topo_pilot.dataset import DatasetConfig, PanelBuilder
from topo_pilot.process import EmissionConfig


def e4_eval_check(store, ckpt_id, ids, proc, m, plan) -> dict:
    """DRB2 extension: the real 36-symbol EVAL path (model_inputs BOS 36, model_predictive,
    float64 activations at resid_post_3) on an in-memory DRY w* block, against the src
    ActivationExtractor logits (s3 softmax, canonical re-indexing)."""
    blk = hd.make_block(proc, "CAL", plan)
    canon, perm = blk["canon32"][:256], proc["perm"][m]
    ck = store.load(Checkpoint, ckpt_id, consumer="experiment")
    inp = hd.model_inputs(canon, perm)
    named = np.hstack((hd.named32(canon, perm), np.zeros((256, 1), np.uint8)))
    ids = np.arange(256, dtype=np.int64)
    obs = ObservationSet(split="test", V=36, sequence_id=ids, tokens=named)
    idx = PanelBuilder().build(obs, DatasetConfig(n_test=256, n_panels=1, panel_size=256),
                               np.random.default_rng(2), dataset_id="drb2")
    _, lg, _ = ActivationExtractor((hc.SITE,), 256).extract(he.load_float32(ck), obs, idx)
    order = np.asarray(idx.sequence_id)  # index order = the extractor's batch rows
    p = he.model_predictive(ck, canon[order], perm)
    ref = he.to_canonical(he.softmax64(lg), perm)
    acts = he.activations(he.load64(ck)[0], inp)
    ok = (int(inp[0, 0]) == 36 and tuple(inp.shape) == (256, 33) and np.array_equal(p, ref)
          and acts.shape == (256, 128) and acts.dtype == np.float64)
    return {"ok": bool(ok), "max_abs_diff": float(np.max(np.abs(p - ref)))}


def drb8(out, ctx) -> dict:
    rng = np.random.default_rng(8)
    n = 256
    m32, m4 = rng.normal(0, 0.3, (n, 2)), rng.normal(0, 0.3, (n, 2))
    sup = rng.random(n) < 0.6
    ext = types.SimpleNamespace(
        phase=rng.uniform(0, 2 * np.pi, n),
        supported=sup,
        resultant=rng.random(n),
        eighth_distance=rng.random(n),
        duplicate=np.zeros(n, bool),
    )
    a = he.endpoints(ext, {32: m32, 4: m4})
    r4 = np.linalg.norm(m32 - m4, axis=1)
    x = scores.scores(scores.unit_vectors(ext.phase), m32, m4)
    rep = he.support(ext, 1.0, a, {32: m32, 4: m4})
    mm = float(hg.c1_means.tree_mean((1.0 - sup) * r4))
    ok = (
        np.array_equal(a["X_minus"][sup], x[sup])
        and np.array_equal(a["X_minus"][~sup], -r4[~sup])
        and np.array_equal(a["X_plus"][~sup], r4[~sup])
        and np.all(a["X_minus"] <= a["X_plus"])
        and rep["missing_mass"] == mm
        and rep["width"] == 2 * mm
    )
    return _res(ok, **FIX)


def drb9(out, ctx) -> dict:
    rng, M = np.random.default_rng(9), hg.k4b_config.MODELS
    r4 = {j: np.abs(rng.normal(0.1, 0.05, 3072)) for j in M}
    xm = {j: rng.normal(0.03, 0.05, 3072) for j in M}
    xp = {j: xm[j] + 0.01 for j in M}
    D = {j: 0.004 for j in M}
    F = Fraction(1, 10**4)
    same = k4b_stats.ladder(xm, xp, r4, F, D) == hg.ladder_pilot(
        xm, xp, r4, F, M, (610101, 610105), D
    )
    two = hg.ladder_pilot(xm, xp, r4, F, M[:2])
    sd, _ = precision.sd_b4_draws(
        {j: xm[j] for j in M[:2]},
        {j: r4[j] for j in M[:2]},
        list(M[:2]),
        hc.SEEDS["sd_upper"],
        hc.DRAWS,
        3072,
    )
    sd_ok = two["sdU"][(M[0], "-")] == hg.c1_means.quantile_with_rank(sd[:, 0], 1 - hc.ALPHA_C)[0]
    cfg = {"delta": float(hc.M + F), "alpha": float(hc.ALPHA_C), "power": 0.80, "projected_N": 3072}
    s = (0.02 - cfg["delta"]) * np.sqrt(3072) / hc.Z_SUM
    while precision.mde(s, cfg) > 0.02:
        s = np.nextafter(s, 0)
    while precision.mde(np.nextafter(s, 1), cfg) <= 0.02:
        s = np.nextafter(s, 1)
    edge = hg._mde_ok({0: s}, 3072, F) and not hg._mde_ok({0: np.nextafter(s, 1)}, 3072, F)
    return _res(same and sd_ok and edge, N=two["N"], **FIX)


def drb10(out, ctx) -> dict:
    c = hg.c_min(0.09, 3072, Fraction(1, 10**4), 0.047)
    ok = (
        hg.capture_pass(c, c)
        and not hg.capture_pass(np.nextafter(c, -np.inf), c)
        and hg.b5_N({"N": None}) == 12288
        and hg.b5_N({"N": 6144}) == 6144
    )
    return _res(ok, c_min=c, **FIX)


def drb11(out, ctx) -> dict:
    P = {620201: "PASS", 620202: "PASS"}
    base = {"b1": P, "b4": P, "b5": P, "b6": "PASS", "b8a": "PASS", "b9a": "PASS"}
    cases = [
        ({"fail": "LINEAGE"}, "FAIL_TECHNICAL/LINEAGE"),
        ({"b1": {620201: "INCONCLUSIVE", 620202: "PASS"}}, "FAIL_TECHNICAL/NUMERICAL"),
        ({"b8a": "FAIL"}, "FAIL_TECHNICAL/LAW_BOUND"),
        ({"b9a": "FAIL"}, "FAIL_TECHNICAL/REGISTRY"),
        ({"incomplete": "STOP at hold"}, "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"),
        ({"b1": {620201: "FAIL", 620202: "PASS"}}, "HWSB_NOT_LEARNED"),
        ({"b4": {620201: "PASS", 620202: "C0_VAL"}}, "HWSB_NO_CIRCLE/C0_VAL"),
        ({"b6": "FAIL", "b5": {620201: "FAIL", 620202: "PASS"}}, "HWSB_UNDERPOWERED/LADDER"),
        (
            {"b5": {620201: "FAIL", 620202: "PASS"}, "b5_positive": True},
            "HWSB_UNDERPOWERED/CAPTURE",
        ),
        ({}, "HWSB_PASS"),
        ({"b6": None}, "FAIL_TECHNICAL/OUTCOME"),
    ]
    got, lic = [], []
    for patch, want in cases:
        oc = hg.outcome(dict(base, **patch))
        got.append(oc["outcome"] == want)
        lic.append(
            bool(hg.licence(oc, {"N_C": 3072, "training_forecast_s": 7000, "Z_bound": "1/10"}))
        )
    return _res(all(got) and all(lic), results=got, **FIX)


def drb12(out, ctx) -> dict:
    st = [(s // 12, s % 12) for s in range(144)]
    saved = (process_law.LAW["sigma"], process_law.softmax_enclosure)
    orig = process_law.softmax_enclosure
    with hl.bound_law(Fraction(5, 4), Fraction(1, 5)):
        a, b, d0 = hl.softmax_enclosure_rounded(st), orig(st), hl.rounding_delta(st)
    same = a[1] == b[1] and a[2] == b[2] and a[0] == b[0] and d0["delta"] == 0
    star = hd.build_process(_mem(), masters=(hc.DRY_MASTERS[0],))
    s15 = hd.build_process(
        _mem(),
        masters=(hc.DRY_MASTERS[0],),
        emission_cfg=EmissionConfig("overlap", 36, 1.5, "grid"),
    )
    r7 = hl.law_bound(star["T"], star["E_canon_shared"], star["pi"], star["coords"])
    r15 = hl.law_bound(s15["T"], s15["E_canon_shared"], s15["pi"], s15["coords"], Fraction(3, 2))
    with hl.bound_law(hc.SIGMA, hc.NEIGHBOUR):
        enc = hl.softmax_enclosure_rounded(st)
        ent = [(0, 0), (0, 35), (77, 20), (143, 17), (5, 30)]
        good, bad = hl.decimal_check(st, enc, ent), hl.decimal_check(st, (enc[0], 1, 1), ent)
    restored = (process_law.LAW["sigma"], process_law.softmax_enclosure) == saved
    ok = (
        same
        and r7["status"] == r15["status"] == "BOUNDED"
        and r7["delta"] > 0
        and r7["delta"] <= r7["u"] * r7["Q_max"]
        and good["pass"]
        and not bad["pass"]
        and restored
    )
    return _res(ok, Z_w_star=r7["Z_bound"], delta=r7["delta"])


def drb13(out, ctx) -> dict:
    d = _dir(out, "DRB13")
    store, proc, plan = _tiny_store(d, "DRB13")
    hd.make_train_dev(store, proc, plan.masters[0], plan)
    blocks = {r: hd.make_block(proc, r, plan) for r in hd.BLOCKS}
    for b in blocks.values():
        hd.save_block(d, b)
    inv = hd.history_inventory(d)
    reg = hd.registry_digests(d, inv)
    want = set().union(*(set(b["digest_canon32"]) for b in blocks.values()))
    fails = []
    for kind in ("missing", "renamed", "unreadable"):
        c = d.parent / f"{d.name}-{kind}"
        shutil.copytree(d, c)
        f = c / "hist" / "VAL.npz"
        if kind == "missing":
            f.unlink()
        elif kind == "renamed":
            f.rename(c / "hist" / "VAL2.npz")
        else:
            f.write_bytes(b"not an npz")
        fails.append(hd.registry_digests(c, inv)["status"] != "PASS")
    c = blocks["CAL"]["canon32"]
    inv_ok = np.array_equal(
        hd.canonical32(hd.named32(c, proc["perm"][plan.masters[0]]), proc["perm"][plan.masters[0]]),
        c,
    )
    ok = reg["status"] == "PASS" and want <= reg["digests"] and all(fails) and inv_ok
    return _res(ok, n_rows=reg["n_rows"], fail_closed=fails)


def drb13b(out, ctx) -> dict:
    paths = hm.job_paths("DRB13b", "test")
    saved = hm.k4b_meter_bind.TEMP_ROOT
    try:
        hm.k4b_meter_bind.TEMP_ROOT = str(paths["temp_root"])
        eff = hm.effective_settings()
    finally:
        hm.k4b_meter_bind.TEMP_ROOT = saved
    pl = hm.placement_ok(paths)
    return _res(
        pl["ok"] and Path(eff["temp_root"]).parent == hc.SCRATCH,
        placement=pl,
        temp_root=eff["temp_root"],
    )


def drb14(out, ctx) -> dict:
    d = _dir(out, "DRB14")
    try:
        stage_records.write_new(d / "x.json", {})
        stage_records.write_new(d / "x.json", {})
        excl = False
    except FileExistsError:
        excl = True
    hold_dir = d / "hold"

    def sleep(_):
        (hold_dir / "DECISION_10.json").write_text(json.dumps({"decision": "CONTINUE"}), "utf-8")

    runs = []
    for held in (False, True):
        store, proc, plan = _tiny_store(None, "DRB14", steps=20)
        m = plan.masters[0]
        ids = hd.make_train_dev(store, proc, m, plan)
        hold = (
            ht.HoldRule(
                hold_dir, cap_s=1.5, steps=20, from_step=10, cpu_fn=lambda: 1.0, sleep=sleep
            )
            if held
            else None
        )
        runs.append(ht.train(store, ids, m, plan, hold))
        again = ht.train(store, ids, m, plan)  # a rerun regenerates identical content
    stop_dir = d / "stop"
    stop = ht.HoldRule(
        stop_dir,
        cap_s=1.0,
        from_step=0,
        cpu_fn=lambda: 5.0,
        sleep=lambda _: (stop_dir / "DECISION_1.json").write_text(
            json.dumps({"decision": "STOP"}), "utf-8"
        ),
    )
    try:
        stop(1)
        stopped = False
    except hc.HwsbStop as exc:
        stopped = exc.status == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    trig = [
        hdr.pause_check("TRAIN", 14551, 0)["trigger"],
        hdr.pause_check("EVAL", 0, 19951)["trigger"],
        hdr.pause_check("KB", 1500, 4200)["pause"],
    ]
    ok = (
        excl
        and runs[0]["checksums"] == runs[1]["checksums"]
        and again["checksums"] == runs[1]["checksums"]
        and len(runs[1]["holds"]) == 1
        and stopped
        and trig == ["STAGE", "CUMULATIVE", False]
    )
    return _res(ok, holds=runs[1]["holds"], triggers=trig)


def drb15(out, ctx) -> dict:
    d = _dir(out, "DRB15")
    (d / "tools" / "hwsb").mkdir(parents=True)
    (d / "elsewhere").mkdir()
    (d / "tools" / "hwsb" / "a.json").write_text('{"seed": 620201}', "utf-8")
    (d / "elsewhere" / "b.md").write_text("x620201y 620202\n", "utf-8")
    found = hws_driver.seed_search(d, list(hc.NEEDLES))
    # paths relative to the synthetic root, so the dry folder's own name does not match
    hits = [dict(h, path="/" + Path(h["path"]).relative_to(d).as_posix()) for h in found]
    res = hk.classify_hits(hits)
    H = hws_driver.C["seeds"]
    same = hk.classify_hits(
        hits, H["g0_declaration_fragments"], H["g0_hws_job_scratch"], "hws_declaration"
    ) == hws_driver.classify_seed_hits(hits)
    needles = sorted((Path(h["path"]).name, h["needle"]) for h in hits)
    ok = (
        same
        and res["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
        and needles == [("a.json", "620201"), ("b.md", "620202")]
    )
    return _res(ok, hits=needles, **FIX)


def drb16(out, ctx) -> dict:
    rng = np.random.default_rng(16)
    canon = {r: rng.integers(0, 36, (32, 32)).astype(np.uint8) for r in hd.BLOCKS}
    blocks = {
        r: {
            "role": r,
            "canon32": c,
            "seq_ids": np.arange(32) + 1000 * i,
            "digest_canon32": scores.history_digests(c),
        }
        for i, (r, c) in enumerate(canon.items())
    }
    train = np.vstack([rng.integers(0, 36, (16, 32)).astype(np.uint8), canon["VAL"][:1]])
    r = hd.separation(blocks, {"train_x": (train, np.arange(17) + 10**6)})
    return _res(
        r["status"] == "FAIL_TECHNICAL/LINEAGE" and r["collisions"]["VAL|train_dev"] == 1, **FIX
    )
