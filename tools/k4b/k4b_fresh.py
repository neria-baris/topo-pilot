"""K4b release-B stages: K-REG2, H2-FRESH, T-PRE, ENDPOINT, export (API.md §10).

Protocol §6 rows 10-12, §8 (decision), §9 (controls, reported only), §11 (report keys). No test
row is sampled or read before require_release_b passes.
"""

from __future__ import annotations  # noqa: I001  (k4b_config sets sys.path first)

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import k4b_config
import k4b_cert
import k4b_charts
import k4b_data
import k4b_decoder
import k4b_driver
import k4b_registry
import k4b_release
import k4b_scores
import k4b_stats
import c1_means
import numpy as np
import stage_records
from c1_records import C1GateFailure
from k4b_cert import control_bounds_all  # noqa: F401  (API.md §14.2 names, re-exported)
from k4b_config import MODELS, SEEDS
from k4b_decoder import decoder_agreement
from k4b_scores import control_arrays, support_entries  # noqa: F401
from k4b_stats import ratios

AUTHORITY = "FAIL_TECHNICAL/AUTHORITY"
FRESH_ORDER = ("H2-FRESH", "T-PRE", "ENDPOINT")
CONTROL_NAMES = ("m4_phase", "sha_suffix", "init", "decoder", "delta1", "delta2", "delta4_orc",
                 "naive")
TWO_SIDED = k4b_cert.CONTROL_K  # two-sided control -> K of its reference
STEPS = ("step5000", "step0")
ACTS_FILE = "ACTS_cal_b0.npz"  # stages/S4a; written by k4b_driver.c0_cal_stage


def kreg2_step(out, release_b_draft, tables) -> dict:
    """Identity-only K-REG2 inside the W2 reservation (extra: K4b's cal b0 and val b0 tables)."""
    reg_dir = Path(out) / "registry"
    m = k4b_registry.build("K-REG2", reg_dir, extra=[tables["cal"], tables["val"]])
    k4b_driver.complete_stage(out, "REG2", [reg_dir / "K-REG2.json",
                                            reg_dir / "K-REG2_digests.npz"])
    return m


def require_release_b(out, release_path, session) -> dict:
    try:
        rel = json.loads(Path(release_path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(AUTHORITY, f"no release B: {exc!r}") from exc
    rel = k4b_release.verify_release(release_path, "B", str(rel.get("task_sha256", "")), session)
    if rel.get("w3_attestation") is None or rel["accept"].get("verdict") != "ACCEPT":
        raise C1GateFailure(AUTHORITY, "release B lacks the W3 record or the coordinator ACCEPT")
    reg = Path(out) / "registry" / "K-REG2.json"
    if not reg.is_file() or stage_records.sha256(reg) != rel["kreg2_sha256"]:
        raise C1GateFailure(AUTHORITY, "release B does not bind this store's K-REG2")
    if int(rel["N"]) != int(rel["k"]) * k4b_config.BLOCK or int(rel["N"]) not in \
            k4b_config.LADDER:
        raise C1GateFailure(AUTHORITY, "release B N/k inconsistent")
    return rel


def sample_test(out, proc, release, reservation_path) -> dict:
    res = k4b_release.verify_reservation(reservation_path, release)
    if res["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"{res['status']}: {res['reason']}")
    k4b_driver.begin_stage(out, "S7")
    d = Path(out) / "stages" / "S7"
    d.mkdir(parents=True, exist_ok=True)
    tabs, files = [], []
    for b in range(int(release["k"])):
        canon, ids = k4b_data.sample_block(proc["T"], proc["E_canon_shared"], proc["pi"],
                                           "test", b)
        t = k4b_data.history_table(canon, ids, "test", b)
        f = d / f"HIST_test_b{b}.npz"
        stage_records.save_npz(f, **{k: v for k, v in t.items() if isinstance(v, np.ndarray)})
        tabs.append(t)
        files.append(f)
    k4b_driver.complete_stage(out, "S7", files)
    return {"canon32": np.concatenate([t["canon32"] for t in tabs]),
            "seq_ids": np.concatenate([t["seq_ids"] for t in tabs]),
            "digest": np.concatenate([t["digest"] for t in tabs]), "blocks": tabs}


def h2_fresh(out, ctx) -> dict:
    res = k4b_release.verify_reservation(ctx["reservation_path"], ctx["release"],
                                         sampling_began=True)
    if res["status"] != "PASS":
        raise C1GateFailure(res["status"], res["reason"])
    digests, seq_union, ranges, predicates, _ = k4b_registry.load(Path(out) / "registry",
                                                                  "K-REG2")
    test = ctx["test"]
    blocks = {f"test_b{i}": t["seq_ids"] for i, t in enumerate(test["blocks"])}
    blocks.update({s: ctx["tables"][s]["seq_ids"] for s in ("cal", "val")})
    k4b_union = set(ctx["tables"]["cal"]["seq_ids"].tolist()) | set(
        ctx["tables"]["val"]["seq_ids"].tolist())
    checks = {"separation": k4b_data.separation_fresh(test["digest"].tolist(), digests),
              "seq_disjoint": k4b_data.seq_disjoint(blocks, set(seq_union) - k4b_union,
                                                    list(ranges.values())),
              "predicates": k4b_data.predicate_check(test["canon32"], predicates)}
    for r in checks.values():
        if r["status"] != "PASS":
            raise C1GateFailure(r["status"], json.dumps(r, default=str)[:2000])
    return checks


def t_pre(out, ctx) -> dict:
    """Oracle + references on every test row; determinism; extension; certificate; fresh B4."""
    p, test, cfg = ctx["proc"], ctx["test"], k4b_config.chart_cfg()
    k4b_charts.require_frozen(out)
    m = k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"], test["canon32"],
                                  p["features"])
    refs = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                               test["canon32"])
    chk = k4b_cert.moment_check(m, refs)
    if not chk["ok"]:
        raise C1GateFailure("FAIL_TECHNICAL/ORACLE", f"{chk['n_fail']} test rows")
    det = k4b_charts.determinism_check(ctx["stored_cal_acts"], ctx["recompute_cal_acts"]())
    if det["status"] != "PASS":
        raise C1GateFailure(det["status"], str(det["mismatch"]))
    eps, arrays, primary, ext, init_ext = k4b_cert.envelopes(), {}, {}, {}, {}
    for j in MODELS:
        e = ext[j] = k4b_charts.extend(ctx["prod"][j]["chart"], ctx["prod"][j]["gauge"],
                                       ctx["test_acts"](j, "step5000"), cfg)
        a = k4b_scores.endpoint_arrays(e.phase, e.supported, m[32], m[4])
        b = k4b_cert.endpoint_bounds(a, e.supported, e.phase, refs, eps)
        arrays[j] = dict(a, phi=e.phase, supported=e.supported, bounds=b)
        primary[f"X_minus_{j}"] = {"X": a["X_minus"], "max_B": b["max"]["minus"]}
        primary[f"X_plus_{j}"] = {"X": a["X_plus"], "max_B": b["max"]["plus"]}
        ini = ctx["init"][j]
        init_ext[j] = dict(ini) if "unavailable" in ini else k4b_charts.extend(
            ini["chart"], ini["gauge"], ctx["test_acts"](j, "step0"), cfg)
    controls = control_arrays(m, test["canon32"], ext, init_ext, ctx["decoders"])
    bounds_all = control_bounds_all(controls, refs, eps)
    r4n = arrays[MODELS[0]]["r4n"]
    primary["n_hat"] = {"X": r4n, "max_B": max(arrays[j]["bounds"]["max"]["norm"]
                                                for j in MODELS)}
    cert = k4b_cert.certify(primary, {})
    b4 = k4b_cert.b4_guard(r4n, primary["n_hat"]["max_B"], ctx["Z"], SEEDS["fresh_b4"],
                           len(r4n))
    b4["FRESH_B4_LOW"] = b4["status"] != "PASS"
    ctx.update(test_moments=m, test_arrays=arrays, ext=ext, controls=controls,
               bounds_all=bounds_all, certificate=cert, fresh_b4=b4)
    if cert["status"] != "PASS":
        raise C1GateFailure(cert["status"], "a primary test row bound exceeds the cap")
    return {"max_gap": str(chk["max_gap"]), "determinism": det["status"],
            "certificate": {k: str(v) for k, v in cert["max_B"].items()},
            "controls_certified": {f"{n}:{k}": bool(b.get("certified")) for n, d in
                                   bounds_all.items() for k, b in d.items()},
            "fresh_B4_status": b4["status"]}


def _plain(x):
    """JSON-ready copy: Fraction -> str, numpy scalars -> Python; containers recursively."""
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return {k: _plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return type(x)(_plain(v) for v in x)
    return x.item() if isinstance(x, np.generic) else x


def _fr(x) -> Fraction:
    x = x[0] if isinstance(x, (tuple, list)) else x
    return x if isinstance(x, Fraction) else Fraction(x) if isinstance(x, int) \
        else Fraction(float(x))


def _keys(entries) -> list:  # int models in MODELS order, then the rest ("all")
    return [k for k in MODELS if k in entries] + [k for k in entries if k not in MODELS]


def bootstrap_inputs(arrays, controls) -> dict:
    """The one ordered dict of the single 610103 bootstrap (API.md §14.2)."""
    d = {}
    for j in MODELS:
        d[f"X:{j}:-"], d[f"X:{j}:+"] = arrays[j]["X_minus"], arrays[j]["X_plus"]
    for name in CONTROL_NAMES:
        entries = controls.get(name, {})
        for key in _keys(entries):
            e = entries[key]
            if "unavailable" in e:
                continue
            if name in TWO_SIDED:
                d[f"{name}:{key}:-"], d[f"{name}:{key}:+"] = e["X_minus"], e["X_plus"]
            else:
                d[f"{name}:{key}"] = e["X"]
    return {k: np.asarray(v, dtype=np.float64) for k, v in d.items()}


def _tm(x) -> float:
    return float(c1_means.tree_mean(np.asarray(x, dtype=np.float64)))


def control_summary(draws, controls, bounds_all) -> dict:
    """Per entry: point, central 95%, alpha / 1-alpha bounds, max B, certified; no status (R22).
    Two-sided entries: alpha from the X- draws, 1-alpha from the X+ draws, both sides reported."""
    out = {}
    for name in CONTROL_NAMES:
        entries, out[name] = controls.get(name, {}), {}
        for key in _keys(entries):
            e = entries[key]
            if "unavailable" in e:
                out[name][key] = e
                continue
            b = bounds_all[name][key]
            if name in TWO_SIDED:
                bd = k4b_stats.bounds(draws[f"{name}:{key}:-"], draws[f"{name}:{key}:+"])
                s = {"point_minus": _tm(e["X_minus"]), "point_plus": _tm(e["X_plus"]),
                     "central95_minus": bd["central95_minus"],
                     "central95_plus": bd["central95_plus"],
                     "max_B_minus": str(_fr(b.get("max_B_minus", b["max_B"]))),
                     "max_B_plus": str(_fr(b.get("max_B_plus", b["max_B"])))}
            else:
                bd = k4b_stats.bounds(draws[f"{name}:{key}"], draws[f"{name}:{key}"])
                s = {"point": _tm(e["X"]), "central95": bd["central95_minus"]}
            s.update(alpha_bound=bd["L"], one_minus_alpha_bound=bd["U"],
                     max_B=str(_fr(b["max_B"])), certified=bool(b["certified"]))
            if not s["certified"]:
                s["label"] = "uncertified"
            out[name][key] = s
    return out


def init_qualifier(init_entry, L_init, F_init):
    """§9.3, R21: L-_init - F_init > 1/100, strict and exact."""
    if "unavailable" in init_entry:
        return f"unavailable ({init_entry['unavailable']})"
    return bool(_fr(L_init) - _fr(F_init) > k4b_config.MARGIN)


def endpoint(arrays, controls, bounds_all, fresh_b4, Z_bound, decoders, ext, canon32, m,
             R) -> dict:
    """API.md §14.3: one joint bootstrap (610103); the RESULT dict with the §11 keys only."""
    n = len(arrays[MODELS[0]]["X_minus"])
    draws = k4b_stats.joint_bootstrap(bootstrap_inputs(arrays, controls), SEEDS["endpoint"])
    sup = support_entries(ext, R, arrays, m)
    per, statuses = {}, {}
    for j in MODELS:
        a = arrays[j]
        bd = k4b_stats.bounds(draws[f"X:{j}:-"], draws[f"X:{j}:+"])
        Bm = k4b_cert.b_num(a["bounds"]["max"]["minus"], float(np.max(np.abs(a["X_minus"]))), n)
        Bp = k4b_cert.b_num(a["bounds"]["max"]["plus"], float(np.max(np.abs(a["X_plus"]))), n)
        Fm, Fp = k4b_cert.margin(Bm, Z_bound), k4b_cert.margin(Bp, Z_bound)
        st = k4b_stats.model_status(bd["L"], bd["U"], Fm, Fp)
        statuses[j] = st["status"]
        per[j] = {"L": bd["L"][0], "U": bd["U"][0], "L_rank": bd["L_rank"],
                  "U_rank": bd["U_rank"], "F_minus": Fm, "F_plus": Fp, "B_num_minus": Bm,
                  "B_num_plus": Bp, "status": st["status"], "labels": list(st["labels"]),
                  "status_without_F": st["status_without_F"],
                  "central95_minus": bd["central95_minus"],
                  "central95_plus": bd["central95_plus"], "point_minus": _tm(a["X_minus"]),
                  "point_plus": _tm(a["X_plus"]), "width": sup[j]["width"],
                  "missing_mass": sup[j]["missing_mass"], "support": sup[j]}
    summ = control_summary(draws, controls, bounds_all)
    d4 = summ.get("delta4_orc", {}).get("all", {}).get("point")
    qual = {}
    for j in MODELS:
        e, b = controls["init"][j], bounds_all["init"][j]
        if "unavailable" in e or not b.get("certified"):
            qual[j] = init_qualifier(e if "unavailable" in e else {"unavailable": "uncertified"},
                                     0, 0)
            continue
        F = k4b_cert.margin(k4b_cert.b_num(b.get("max_B_minus", b["max_B"]), float(
            np.max(np.abs(e["X_minus"]))), n), Z_bound)
        qual[j] = init_qualifier(e, summ["init"][j]["alpha_bound"], F)
    b4 = {k: v for k, v in fresh_b4.items() if k != "FRESH_B4_LOW"}
    if fresh_b4.get("FRESH_B4_LOW", fresh_b4.get("status") != "PASS"):
        b4["FRESH_B4_LOW"] = True
    return _plain({"per_model": per, "controls": summ,
                   "decoder_agreement": decoder_agreement(ext, decoders, canon32),
                   "ratios": {j: ratios(per[j]["point_minus"], fresh_b4.get("point"), d4)
                              for j in MODELS},
                   "fresh_B4": b4, "init_qualifier": qual,
                   "overall": k4b_stats.overall(statuses), "Z_bound": _fr(Z_bound), "N": n,
                   "k": n // k4b_config.BLOCK,
                   "c1prime_disclosure": k4b_config.CONTRACT["authority"]["c1prime_disclosure"]})


def export(out, result) -> Path:
    d = Path(out) / "stages" / "S8"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "RESULT.json"
    stage_records.write_new(f, result)
    k4b_driver.complete_stage(out, "S8", [f])
    sealed = Path(out) / k4b_stats.SEALED_FILE
    if sealed.is_file():
        stage_records.write_new(d / "SEALED_OPENED.json",
                                json.loads(sealed.read_text(encoding="utf-8")))
    return f


def _npz(path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def load_recorded(out, stage, name) -> dict:
    """Arrays of stages/<stage>/<name>, re-hashed against its STAGE_COMPLETE record."""
    rel, want = f"stages/{stage}/{name}", None
    for line in (Path(out) / "STAGES.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("stage") == stage and r.get("event") == "STAGE_COMPLETE":
            want = r["files"].get(rel, want)
    f = Path(out) / rel
    if want is None or not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != want:
        raise C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"{rel} does not re-hash to its record")
    return _npz(f)


def load_frozen(out) -> dict:
    """API.md §14.3: the frozen production charts, step-0 charts and decoders; no refit."""
    import chart

    rec, d = k4b_charts.require_frozen(out), Path(out) / "stages" / "S4a"
    prod, init, dec = {}, {}, {}
    for j in MODELS:
        c, g = chart.chart_from_arrays(_npz(d / f"CHART_{j}.npz"))
        prod[j] = {"chart": c, "gauge": g}
        if f"INIT_CHART_{j}.npz" in rec["files"]:
            c, g = chart.chart_from_arrays(_npz(d / f"INIT_CHART_{j}.npz"))
            init[j] = {"chart": c, "gauge": g}
        else:
            init[j] = {"unavailable": str(rec.get("init_status", {}).get(str(j), "absent"))}
        dec[j] = k4b_decoder.from_arrays(_npz(d / f"DECODER_{j}.npz"))
    return {"prod": prod, "init": init, "decoders": dec}


def endpoint_gate(ctx) -> dict:
    ctx["result"] = r = endpoint(
        ctx["test_arrays"], ctx["controls"], ctx["bounds_all"], ctx["fresh_b4"], ctx["Z"],
        ctx["decoders"], ctx["ext"], ctx["test"]["canon32"], ctx["test_moments"],
        {j: float(ctx["prod"][j]["chart"].support_radius) for j in MODELS})
    return {"overall": r["overall"], "per_model": {j: p["status"] for j, p in
                                                    r["per_model"].items()}}


def main(argv=None) -> int:
    import c1_model

    ap = argparse.ArgumentParser(description="K4b release B (E2): H2-FRESH -> ENDPOINT")
    ap.add_argument("--release", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--out", default=str(k4b_config.STORE))
    ap.add_argument("--mailbox", default=str(k4b_config.ROOT / "agent-handoff"))
    a = ap.parse_args(argv)
    out = Path(a.out)
    rel = require_release_b(out, a.release, a.session)
    proc = k4b_data.load_process()
    meta = k4b_driver.check_checkpoints()
    ck = k4b_config.CONTRACT["checkpoints"]
    models = {(j, s): c1_model.load_model64(k4b_driver.load_checkpoint(ck[str(j)][s]))[0]
              for j in MODELS for s in STEPS}
    tables = {s: load_recorded(out, "S3", f"HIST_{s}_b0.npz") for s in ("cal", "val")}
    stored = load_recorded(out, "S4a", ACTS_FILE)
    frozen = load_frozen(out)
    Z = k4b_cert.transport_bound(proc["T"], proc["E_canon_shared"], proc["pi"],
                                 proc["coords"])["Z_bound"]
    res_path = Path(a.mailbox) / rel["reservation"]
    test = sample_test(out, proc, rel, res_path)

    def acts(canon32, j, s):  # the identical call of release A (k4b_driver._acts)
        return c1_model.activations(models[(j, s)], k4b_data.model_inputs(canon32,
                                                                           proc["perm"][j]))

    ctx = dict(frozen, release=rel, reservation_path=res_path, proc=proc, tables=tables,
               test=test, Z=Z, checkpoint_meta=meta, stored_cal_acts=stored,
               recompute_cal_acts=lambda: {f"{j}_{s}": acts(tables["cal"]["canon32"], j, s)
                                           for j in MODELS for s in STEPS},
               test_acts=lambda j, s: acts(test["canon32"], j, s))
    recs = k4b_driver.run_gates(out, [("H2-FRESH", lambda: h2_fresh(out, ctx)),
                                      ("T-PRE", lambda: t_pre(out, ctx)),
                                      ("ENDPOINT", lambda: endpoint_gate(ctx))])
    if all(r["status"] == "PASS" for r in recs):
        export(out, ctx["result"])
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
