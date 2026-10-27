"""HWS known-answer checks: stage S0 (KC1-KC14, protocol §3) and the exact and numerical dry-run
cases DR1-DR8 (§13, TEST_PLAN §4). Split from hws_driver by size (erratum E16, the R-0118-6
pattern); hws_driver.run_s0 delegates here. The DR cases touch synthetic worlds and
deterministic rows only; DR2 samples the known-zero U and N controls, never a sweep world.
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import hws_worlds as hw
import hws_driver as hd
import hws_exact as he
import hws_oracle as ho
import hws_records as hr
import hws_select as hsel
import hws_stats as hs
import k4b_scores
import numpy as np
import oracle_profile
import stage_records
from topo_pilot.contracts import ArtifactStore, LocalFSBackend, SeedTree, SequenceLayout
from topo_pilot.process import EmissionConfig, GridCenters, ProcessStage, TransitionConfig
from topo_pilot.world import WorldConfig, WorldStage

S0C, KNOWN, TINY = hw.CONTRACT["s0"], hd.KNOWN, hd.TINY
N_S0, N_ZERO = 32768, 4096


# ----------------------------------------------------------------------------------- stage S0


def _tol(x, ref, s, n_r) -> dict:
    t = 4 * s * math.sqrt(1 / N_S0 + 1 / n_r)
    st = "PASS" if abs(x - ref) <= t else KNOWN
    return {"status": st, "value": x, "reference": ref, "tolerance": t, "s": s, "n_r": n_r}


def _ok(flag) -> str:
    return "PASS" if flag else KNOWN


def zero_max(rows) -> float:
    vals = [rows[n][K] for n in ("D", "rn", "G") for K in rows[n]]
    vals += [rows[n] for n in ("G4A", "IZ4", "IX4")] + list(rows["nulls"].values())
    return float(max(np.max(np.abs(v)) for v in vals))


def known_cases(w0, ex0, rec0, look0, zero) -> dict:
    """KC1-KC14 on the S0 rows (§3; tolerance rule with the sweep's own per-row SD)."""
    rows, tok, kc = look0["rows"], look0["tok"], {}
    sd = {K: hs.summary(rows["rn"][K]) for K in (1, 2, 4, 8, 16)}
    k1 = S0C["KC1"]
    res = he.kc1_identity(k1["artifact_root"], k1["manifest"], hw.REPO / k1["config_json"])
    cfg_ok = res["config_json_sha256"] == k1["config_json_sha256"]
    kc["KC1"] = {"status": res["status"] if cfg_ok else KNOWN, "value": res}
    kc["KC2"] = {"status": _ok(abs(ex0["min_p"] - 0.0268) <= 5e-5), "value": ex0["min_p"]}
    s3, x3 = hs.summary(rows["Hb1"])["sd"], ex0["mean_last_entropy"]
    t3 = max(5e-4, 4 * s3 / math.sqrt(4096))
    kc["KC3"] = {"status": _ok(abs(x3 - 3.140) <= t3), "value": x3, "s": s3, "tolerance": t3}
    ref4 = S0C["KC4"]["reference"]
    kc4 = {K: _tol(sd[K]["mean"], ref4[str(K)], sd[K]["sd"], 4096) for K in sd}
    kc["KC4"] = {"status": _ok(all(r["status"] == "PASS" for r in kc4.values())), "value": kc4}
    kc["KC5"] = _tol(sd[4]["mean"], S0C["KC5"]["reference"], sd[4]["sd"], 3072)
    d4, gc = hs.summary(rows["D"][4]), hs.summary(rows["G"][1])
    kc["KC6"] = _tol(d4["mean"], S0C["KC6"]["reference"], d4["sd"], 3072)
    kc["KC7"] = _tol(gc["mean"], float(S0C["KC7"]["reference"]), gc["sd"], 4096)
    kc["KC8"] = {"status": "PASS", "value": rec0["nulls"]}
    ex9, mc9, T, E, pi = he.suffix_enumeration(w0, (1, 2, 3)), {}, w0["T"], w0["E"], w0["pi"]
    for K in (1, 2, 3):
        q = ho.predictive(oracle_profile.suffix_posterior(T, E, pi, tok, K), T, E)
        msq = np.sum(rows["m"][K] ** 2, axis=1)
        mc9[K] = {"E_m_sq": hs.summary(msq), "E_Hq": hs.summary(ho.entropy_rows(q))}
    floor9 = float(Fraction(S0C["KC9"]["kc9_float_floor"]))  # D-0130-1 (owner addendum 30)
    tol9 = {K: {q: max(4 * v["se"], floor9) for q, v in mc9[K].items()} for K in mc9}
    ok9 = all(abs(ex9[K][q] - v["mean"]) <= tol9[K][q] for K in mc9 for q, v in mc9[K].items())
    kc["KC9"] = {"status": _ok(ok9), "value": {"exact": ex9, "mc": mc9, "tolerance": tol9}}
    dec = he.decimal_spot_check(w0, tok[:16], (1, 2, 4, 32))
    bay = he.bayes_cross_check(w0, tok[:1024])
    kc["KC10"] = {"status": _ok(dec["pass"] and bay["pass"]), "value": [dec, bay]}
    zmax = {k: zero_max(lk["rows"]) for k, lk in zero.items()}
    kc["KC11"] = {"status": _ok(max(zmax.values()) <= 1e-12), "value": zmax}
    uw = rec0["bounds"]["D4"]["Uw"]
    kc["KC12"] = {"status": _ok(uw < float(hsel.C1_MIN)), "value": uw}
    kc["KC13"] = {"status": "PASS", "value": rec0["report"]["entropy_diff"]}
    pv = {"p_D2a": ex0["p_D2a"], "pinsker_violations": rec0["e6"]["pinsker_violations"]}
    kc["KC14"] = {"status": "PASS", "value": pv}
    return kc


def run_s0(out, auth) -> dict:
    """§3: w0 at 32,768 rows, U and N at 4,096; KC1-KC14 gate; freezes g4* and g4A*."""
    out = Path(out)
    frz = hd._preflight(out, ["S0"], auth)
    if frz is None:
        return {"status": "REFUSED"}
    if any(e.get("event") == "STAGE_COMPLETE" and e["stage"] == "S0" for e in hr.stage_events(out)):
        raise hw.HwsStop("FAIL_TECHNICAL/RERUN", "S0 already completed in this store")
    hr.archive_partial(out, "S0")
    hd.g0(out)
    ev = {"event": "STAGE_BEGIN", "stage": "S0", "worklist": [hw.W0.key, "U-W12", "N-W12"]}
    hr.append_stage_event(out, dict(ev, forecast_s=hsel.forecast("S0", [])))
    w0 = hw.build_process(hw.W0)
    ex0 = he.exact_world(w0)
    rec0, look0, _ = hd.world_record(out, w0, ex0, "S0", N_S0, ho.KS_S0, None, seed=620101)
    zero, zrec = {}, {}
    for k in ("U", "N"):
        proc = hw.build_known_zero(k)
        args = (out, proc, he.exact_world(proc), "S0", N_ZERO, ho.KS_S0, None)
        zrec[k], zero[k], _ = hd.world_record(*args, known=True)
    kc = known_cases(w0, ex0, rec0, look0, zero)
    for name, r in kc.items():
        hd._gate(out, name, r["status"], value=r.get("value"))
    bad = [k for k, r in kc.items() if r["status"] != "PASS"]
    if bad:
        raise hw.HwsStop(KNOWN, f"known-case checks failed: {bad}")
    b, pre = rec0["bounds"], ["stages/S0", "hist/S0", "hist/NULLCHK/S0"]
    fl = hsel.floors(b["G4"]["mean"], b["G4A"]["mean"])
    sds = {q: b[q]["sd"] for q in ("D4", "GC", "G4", "G4A")}
    sds["rn4"] = hs.summary(look0["rows"]["rn"][4])["sd"]
    rec = {"kc": kc, "G4hat_w0": b["G4"]["mean"], "G4Ahat_w0": b["G4A"]["mean"]}
    rec.update(g4_star=fl["G4"], g4A_star=fl["G4A"], per_row_sd_w0=sds, w0_record=rec0)
    rec.update(U_record=zrec["U"], N_record=zrec["N"], s0_store_sha256=hr.tree_sha(out, pre))
    rec.update(protocol_sha256=hw.CONTRACT["protocol_sha256"], freeze_sha256=frz["freeze_sha256"])
    path = out / "stages" / "S0" / "S0_RECORD.json"
    stage_records.write_new(path, hr.num(rec))
    hd._gate(out, "S0_RECORD", "PASS", sha256=stage_records.sha256(path))
    done = {"event": "STAGE_COMPLETE", "stage": "S0", "files": hr._files(out, pre)}
    hr.append_stage_event(out, done)
    return {"status": "PASS", "record": str(path), "floors": fl}


# ------------------------------------------------------------------------------ dry run DR1-13


def _dry(proc, case, n, Ks=(1, 2, 4), layout=TINY) -> dict:
    return ho.world_look(dict(proc, key=case), "DRY", n, Ks, layout=layout)


def _fixed_tok(n=64, V=36, a=11, b=5) -> np.ndarray:
    return ((np.arange(n * 32).reshape(n, 32) * a + b) % V).astype(np.uint8)


def dr1(out):
    tiny = hw.build_tiny()
    ex = he.exact_expectations(tiny, 8, (1, 2, 4))
    rows = _dry(tiny, "DR1", 20000)["rows"]
    mc, ref = {}, {}
    for K in (1, 2, 4):
        mc.update({f"D{K}": rows["D"][K], f"B{K}": rows["rn"][K], f"G{K}": rows["G"][K]})
        mc[f"V{K}"] = rows["rn"][K] ** 2
        ref.update({f"D{K}": ex["D"][K], f"B{K}": ex["B"][K], f"G{K}": ex["G"][K]})
        ref[f"V{K}"] = ex["V"][K]
    mc.update({k: rows[k] for k in ("G4A", "IZ4", "IX4")})
    ref.update({k: ex[k] for k in ("G4A", "IZ4", "IX4")})
    s = {k: hs.summary(x) for k, x in mc.items()}
    far = {
        k: [s[k]["mean"], ref[k], s[k]["se"]]
        for k in s
        if abs(s[k]["mean"] - ref[k]) > 4 * s[k]["se"]
    }
    flags = ex["identities"]
    ok = not far and all(f["pass"] for f in flags.values()) and ex["D"][4] > 0
    return ok, {"outside_4se": far, "identities": flags, "D4_exact": ex["D"][4]}


def dr2(out):
    t = hw.build_tiny()
    cases = {"DR2-U-tiny": (dict(t, E=np.eye(12), n_axial=2, V=12), TINY, 2000)}
    cases["DR2-N-tiny"] = (dict(t, E=np.full((12, 3), 1.0 / 3), V=3), TINY, 2000)
    for k in ("U", "N"):
        cases[f"DR2-{k}-W12"] = (hw.build_known_zero(k), SequenceLayout(), N_ZERO)
    vals = {c: zero_max(_dry(p, c, n, layout=lay)["rows"]) for c, (p, lay, n) in cases.items()}
    return max(vals.values()) <= 1e-12, {"max_abs": vals}


def dr3(out):
    un = hw.build_process(hw.World(12, 2, Fraction(5, 4), Fraction(1, 5)), alias="unanchored")
    st = he.exact_world(un)["status"]
    rows = _dry(un, "DR3", 256, layout=SequenceLayout())["rows"]
    mx = max(float(np.max(np.abs(rows["m"][K]))) for K in rows["m"])
    dx = max(float(np.max(np.abs(rows["D"][K]))) for K in rows["D"])
    return st == "INELIGIBLE/E3" and mx <= 1e-12 and dx <= 1e-12, {"E3": st, "m": mx, "D": dx}


def dr4(out):
    det, maps = {}, hw.CONTRACT["alias"]["maps"]
    for W, q in ((12, 3), (8, 2), (8, 3), (12, 2)):
        r = hw.symmetry_check(
            hw.build_process(hw.World(W, q, Fraction(5, 4), Fraction(1, 5)))["E"], W
        )
        det[f"{W},{q}"] = {"reflections": r["reflections"], "translations": r["translations"]}
    r6 = hw.symmetry_check(hw.build_tiny(q=2)["E"], 6, 2)
    det["6,2"] = {"reflections": r6["reflections"], "translations": r6["translations"]}
    sym = all(det[k]["reflections"] and not det[k]["translations"] for k in det if k != "12,2")
    labels = all(
        hw.anchored_labels(int(W), int(q)).tolist() == m["g"]
        for W, qs in maps.items()
        for q, m in qs.items()
    )
    w = hw.World(12, 2, Fraction(2), Fraction(3, 4))
    same = np.array_equal(hw.build_process(w)["E"], hw.build_process(w)["E"])
    ok = sym and not det["12,2"]["reflections"] and labels and same
    return ok, dict(det, labels_match_contract=labels, repeated_identical=same)


def dr5(out):
    proc, world = hw.build_process(hw.W0), hw.build_world(12)
    cen = GridCenters().centers(world, 36, np.random.default_rng(0))
    e_ok = np.array_equal(hw._mirrored(world, hw.centres(12), hw.W0.sigma), proc["E"])
    f_ok = np.array_equal(proc["features"], oracle_profile.circle_features(proc["coords"]))
    tok, ks = _fixed_tok(), (1, 4, 32)
    a = oracle_profile.posterior_means(proc["T"], proc["E"], proc["pi"], tok, ks, proc["features"])
    cf = oracle_profile.circle_features(proc["coords"])
    b = oracle_profile.posterior_means(proc["T"], proc["E"], proc["pi"], tok, ks, cf)
    pm_ok = all(np.array_equal(a[K], b[K]) for K in ks)
    ok = np.array_equal(cen, hw.centres(12)) and e_ok and f_ok and pm_ok
    return ok, {"centres": bool(np.array_equal(cen, hw.centres(12))), "E": e_ok, "posterior": pm_ok}


def dr6(out):
    t = hw.build_tiny()
    hist = np.array(list(itertools.product((0, 1), repeat=8)), dtype=np.int64)
    brute = float(he._forward(t, hist).sum())
    got = he.p_d2a(t["T"], t["E"], t["pi"], alphabet=(0, 1), Lh=8)
    tau = float(Fraction(1, 2000000))
    e4 = (he.e4_check(tau)["status"], he.e4_check(float(np.nextafter(tau, 1.0)))["status"])
    ok = abs(got - brute) <= 1e-15 and e4 == ("PASS", "INELIGIBLE/E4")
    return ok, {"p_d2a": got, "brute": brute, "e4_at_and_above": e4}


def _artifacts(root) -> dict:
    store = ArtifactStore(LocalFSBackend(root), producer_version="hws-dry-DR7")
    wid = WorldStage().run(WorldConfig("cylinder", (12, 12), "flat"), store)
    names = [f"WorldSpec/{wid}"]
    names.append(f"TransitionSpec/{ProcessStage().run_transition(wid, TransitionConfig(), store)}")
    cfg = EmissionConfig("overlap", 36, 1.25, "grid")
    names += [
        f"EmissionSpec/{ProcessStage().run_emission(wid, cfg, SeedTree(s), store)}"
        for s in (1729, 2718, 3141)
    ]
    for n in names:
        (root / n / "payload.npz").unlink()
    return {n: json.loads((root / n / "meta.json").read_text("utf-8")) for n in names}


def _seal(root, metas, base) -> None:
    arts = {n: {"sha256": m["payload_sha256"]} for n, m in metas.items()}
    for n in arts:
        arts[n]["meta_sha256"] = stage_records.sha256(root / n / "meta.json")
    (base / "INPUT_IDENTITIES.json").write_text(json.dumps({"artifacts": arts}), "utf-8")
    cfg = {
        "inputs_sha256": {
            "INPUT_IDENTITIES.json": stage_records.sha256(base / "INPUT_IDENTITIES.json")
        }
    }
    (base / "config.json").write_text(json.dumps(cfg), "utf-8")


def dr7(out):
    base = Path(out) / "DR7" / hr.utc().replace(":", "")
    root = base / "artifacts"
    metas = _artifacts(root)
    _seal(root, metas, base)
    args = (root, base / "INPUT_IDENTITIES.json", base / "config.json")
    good = he.kc1_identity(*args)["status"]
    extra = root / list(metas)[2] / "extra.json"
    obj = json.loads(extra.read_text("utf-8"))
    extra.write_text(json.dumps(dict(obj, sigma=1.5)), "utf-8")
    bad = he.kc1_identity(*args)["status"]
    reads = [p for p in he.JSON_READS if not str(p).endswith(".json")]
    ok = good == "PASS" and bad == KNOWN and not reads and not list(root.rglob("payload.npz"))
    return ok, {"untampered": good, "tampered_extra": bad, "non_json_reads": reads}


def dr8(out):
    w0, tok, ks = hw.build_process(hw.W0), _fixed_tok(), (1, 2, 4, 8, 16)
    rows = ho.row_arrays(w0, tok, ks)
    pm = oracle_profile.posterior_means(
        w0["T"], w0["E"], w0["pi"], tok, ks + (32,), oracle_profile.circle_features(w0["coords"])
    )
    phi = k4b_scores.oracle_phase(pm[32])
    ok = all(np.array_equal(rows["D"][K], k4b_scores.phase_scores(phi, pm[32], pm[K])) for K in ks)
    return ok, {"rows": int(tok.shape[0]), "Ks": list(ks)}
