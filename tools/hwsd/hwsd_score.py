"""HWSD per-checkpoint scorer (API.md section 6 and section 16): learning, chart_one, arrays_one,
controls_one, statuses, determinism, acceptance. Reused functions are called through their module
attributes at call time, so the binding applies."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import re
from fractions import Fraction
from pathlib import Path

import c1_chart
import c1_model
import c1_records
import hwsb_eval
import hwsd_records
import k4b_cert
import k4b_charts
import k4b_config
import k4b_data
import k4b_decoder
import k4b_driver
import k4b_scores
import numpy as np
import stage_records
from c1_records import C1GateFailure

NUMERICAL = "FAIL_TECHNICAL/NUMERICAL"
STATUSES = ("SCORED", "SCORED_UNVALIDATED", "CHART_UNAVAILABLE", "UNCERTIFIED")


def _jsonable(x):
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return _jsonable(x.tolist())
    return x.item() if isinstance(x, np.generic) else x


def checkpoint_dir(out, j, step) -> Path:
    return Path(out) / "stages" / "SCORE" / str(j) / f"s{step}"


def ledger_for(out, j, step):
    d = checkpoint_dir(out, j, step)
    d.mkdir(parents=True, exist_ok=True)
    return c1_chart.ConstructionLedger(d / "CHART_CONSTRUCTIONS.json")


def load_checkpoint_d(j, step) -> tuple:
    row = dc.CHECKPOINTS[(int(j), int(step))]
    ckpt = k4b_driver.load_checkpoint(row["id"])
    model64, sha = c1_model.load_model64(ckpt)
    return ckpt, model64, sha


def acts_fn(model64, perm):
    return lambda canon32: c1_model.activations(
        model64, k4b_data.model_inputs(canon32, perm))


def learning_one(ckpt, canon32, perm, q, z=dc.Z, z_s=dc.Z_S) -> dict:
    p = hwsb_eval.model_predictive(ckpt, canon32, perm)
    r = hwsb_eval.b1(q, p)
    if r["status"] == "INCONCLUSIVE" or not np.isfinite(r["captured"]):
        raise C1GateFailure(NUMERICAL, "learning: captured is not finite or not decidable")
    b2z = hwsb_eval.forcing(q[32], q[4], p, z)
    b2s = hwsb_eval.forcing(q[32], q[4], p, z_s)
    return {"captured": r["captured"], "regret": r["regret"], "G_C": r["G_C"],
            "status": r["status"], "regret_sd": r["regret_sd"], "regret_se": r["regret_se"],
            "G_C_sd": r["G_C_sd"], "n": r["n"], "B2_z": b2z, "B2_zS": b2s, "z": z, "z_S": z_s,
            "learn_pass": r["status"] == "PASS", "B2_L_zS": b2s["L"]}


def _is_wall(status, reason) -> bool:
    r = str(reason)
    return r.startswith("NATIVE_WALL") or (r.startswith("native operation ") and " wall" in r)


def _text(status, reason) -> str:
    r = str(reason)
    if r.startswith("NATIVE_WALL"):
        return r
    return f"NATIVE_WALL: {r}" if _is_wall(status, r) else f"{status}: {r}"


def map_build(res, where):
    status, reason = res["status"], res.get("reason", "")
    if str(status).startswith("FAIL_TECHNICAL"):
        raise C1GateFailure(status, f"{where}: {reason}")
    if status == "PASS":
        return None
    if status == "INCONCLUSIVE" and _is_wall(status, reason):
        return {"kind": "NATIVE_WALL", "text": _text(status, reason)}
    return {"kind": status, "text": f"{status}: {reason}"}


def _exc_status(exc) -> tuple:
    mapped = c1_records.adapt_chart_exception(exc)
    status, reason = mapped if mapped is not None else c1_records.classify_exception(exc)
    if status == "INCONCLUSIVE" and str(reason).startswith("CHART_UNAVAILABLE"):
        status = "INCONCLUSIVE/CHART_UNAVAILABLE"
    return status, reason


def _sha(path) -> str:
    return stage_records.sha256(path)


def chart_one(j, acts, tables, m32_cal, ledger, cfg, out_dir, timed=None, skip_direct=False):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    A = acts("cal")
    land = np.asarray(tables["cal"]["landmark"], dtype=bool)
    ids = tables["cal"]["seq_ids"]
    m32 = np.asarray(m32_cal)
    prod = k4b_charts.build_chart(A[land], ids[land], m32[land], ledger, j, "production", cfg,
                                  timed=timed)
    map_build(prod, f"C0-CAL {j}")
    res = {"c0_cal": {"status": prod["status"], "reason": prod["reason"],
                      "diagnostics": prod["diagnostics"]},
           "c0_val": None, "prod": None, "decoder": None, "frozen": None, "acts_cal": A}
    if prod["status"] != "PASS":
        return res
    ext = k4b_charts.extend(prod["chart"], prod["gauge"], A[~land], cfg)
    dec = k4b_decoder.fit(tables["cal"]["canon32"][~land], ids[~land], ext.phase, j)
    stage_records.save_npz(out_dir / "CHART.npz", **prod["serial"])
    stage_records.save_npz(out_dir / "DECODER.npz", **k4b_decoder.to_arrays(dec))
    stage_records.save_npz(out_dir / "ACTS_cal.npz", acts=A)
    g = prod["gauge"]
    frozen = {"files": {n: _sha(out_dir / n) for n in ("CHART.npz", "DECODER.npz", "ACTS_cal.npz")},
              "gauge": [int(g.sign), float(g.shift), float(g.alignment)],
              "decoder_status": dec.get("status"), "c0_cal": "PASS"}
    stage_records.write_new(out_dir / "FROZEN.json", frozen)
    res.update(prod=prod, decoder=dec, frozen=frozen)
    if skip_direct:
        return res
    V = acts("val")
    vt = tables["val"]
    vl = np.asarray(vt["landmark"], dtype=bool)
    direct = k4b_charts.build_chart(V[vl], vt["seq_ids"][vl], None, ledger, j, "direct", cfg,
                                    timed=timed)
    map_build(direct, f"C0-VAL direct {j}")
    cv = {"status": "PASS", "reason": "", "criteria": None, "n": None, "n_supported": None,
          "fidelity": None, "bins": None, "resultant": None, "direct_status": direct["status"],
          "direct_reason": direct["reason"], "direct_diagnostics": direct["diagnostics"]}
    if direct["status"] != "PASS":
        cv.update(status=direct["status"], reason=direct["reason"])
    else:
        try:
            c0 = c1_chart.c0_val(prod["chart"], prod["gauge"], V[vl], direct["chart"], cfg)
            cv.update({k: c0[k] for k in ("n", "n_supported", "fidelity", "bins", "resultant",
                                          "criteria", "status")})
            if c0["status"] != "PASS":
                cv["reason"] = "criteria failed: " + ",".join(
                    sorted(k for k, v in c0["criteria"].items() if not v))
        except Exception as exc:  # noqa: BLE001  mapped by the section 16 rules
            s, r = _exc_status(exc)
            map_build({"status": s, "reason": r}, f"C0-VAL {j}")
            cv.update(status=s, reason=r)
    res["c0_val"] = cv
    return res


def arrays_one(prod, acts_test, m, refs, eps, cfg, planted=False) -> dict:
    ext = k4b_charts.extend(prod["chart"], prod["gauge"], acts_test, cfg)
    ph = np.asarray(ext.phase, dtype=np.float64)
    if not (np.all(np.isfinite(ph)) and np.all((ph >= 0) & (ph < 2 * np.pi))):
        raise C1GateFailure(NUMERICAL, "extension phase outside [0, 2pi)")
    a = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])
    if planted:
        b = None
        z = Fraction(0)
        cert = {"status": "PASS", "max_B": {"X_minus": z, "X_plus": z, "n_hat": z},
                "certified": {"X_minus": True, "X_plus": True, "n_hat": True}, "planted": True}
    else:
        b = k4b_cert.endpoint_bounds(a, ext.supported, ext.phase, refs, eps)
        cert = k4b_cert.certify({
            "X_minus": {"X": a["X_minus"], "max_B": b["max"]["minus"]},
            "X_plus": {"X": a["X_plus"], "max_B": b["max"]["plus"]},
            "n_hat": {"X": a["r4n"], "max_B": b["max"]["norm"]}}, {})
    return {"ext": ext, "arrays": a, "bounds": b, "certificate": cert,
            "max_abs": {"X_minus": float(np.max(np.abs(a["X_minus"]))),
                        "X_plus": float(np.max(np.abs(a["X_plus"])))}}


def controls_one(m, canon32, ext, decoder) -> dict:
    m32, m4 = m[32], m[4]
    if decoder.get("status") != "AVAILABLE":
        dec = {"unavailable": str(decoder.get("reason", ""))}
    else:
        phi = k4b_decoder.predict_phase(decoder, canon32)
        dec = {"X": k4b_scores.phase_scores(phi, m32, m4), "phi": phi}

    def two(K):
        return dict(k4b_scores.secondary_arrays(ext.phase, ext.supported, m, K), phi=ext.phase,
                    supported=np.asarray(ext.supported, dtype=bool))

    return {"decoder": dec, "delta1": two(1), "delta2": two(2),
            "naive": {"X": k4b_scores.naive_scores(ext.phase, m32, m4), "phi": ext.phase}}


def status_of_checkpoint(ch, cert) -> tuple:
    c = ch["c0_cal"]
    if c["status"] != "PASS":
        return "CHART_UNAVAILABLE", "CHART_UNAVAILABLE/" + _text(c["status"], c["reason"])
    if cert is None or cert["status"] != "PASS":
        names = ",".join(n for n, v in (cert or {}).get("certified", {}).items() if not v)
        return "UNCERTIFIED", f"UNCERTIFIED/{(cert or {}).get('status')}: {names}"
    v = ch.get("c0_val")
    if v is not None and v["status"] == "PASS":
        return "SCORED", "SCORED"
    if v is None:
        return "SCORED_UNVALIDATED", "SCORED_UNVALIDATED/NOT_RUN"
    if v["direct_status"] != "PASS":
        return "SCORED_UNVALIDATED", "SCORED_UNVALIDATED/" + _text(v["direct_status"],
                                                                    v["direct_reason"])
    if v.get("criteria"):
        bad = sorted(k for k, ok in v["criteria"].items() if not ok)
        return "SCORED_UNVALIDATED", "SCORED_UNVALIDATED/CRITERIA: " + ",".join(bad)
    return "SCORED_UNVALIDATED", "SCORED_UNVALIDATED/" + _text(v["status"], v["reason"])


def archived_wall(out, j, step):
    sup = Path(out) / "superseded"
    if not sup.is_dir():
        return None
    found = []
    for d in sup.iterdir():
        m = re.fullmatch(r".+-a(\d+)", d.name)
        led = d / "stages" / "SCORE" / str(j) / f"s{step}" / "CHART_CONSTRUCTIONS.json"
        if m and led.is_file():
            found.append((int(m.group(1)), d, led))
    if not found:
        return None
    _, d, led = max(found, key=lambda t: t[0])
    claims = dc.read_json(led).get("claims", [])
    if not claims or int(claims[-1][0]) != int(j):
        return None
    if (led.parent / "CHECKPOINT_RECORD.json").exists():
        return None
    marker = d / "OPERATION_ACTIVE.json"
    if not marker.is_file():
        return None
    rec = dc.read_json(marker)
    if rec.get("state") != "active":
        return None
    return {"role": claims[-1][1], "label": rec.get("label")}


def _write_json(path, obj) -> None:
    stage_records.write_new(path, _jsonable(obj))


def score_checkpoint(ctx, j, step, ckpt=None, model64=None, perm=None, acts=None, learn=None):
    out, cdir, tables = ctx["out"], checkpoint_dir(ctx["out"], j, step), ctx["tables"]
    cdir.mkdir(parents=True, exist_ok=True)
    perm = ctx["proc"]["perm"][j] if perm is None else perm
    if learn is None:
        learn = learning_one(ckpt, tables["lgate"]["canon32"], perm, ctx["q"])
    if acts is None:
        fn = acts_fn(model64, perm)
        acts = lambda split: fn(tables[split]["canon32"])  # noqa: E731
    m_cal, m = ctx["moments"]["cal"], ctx["moments"]["test"]
    w = archived_wall(out, j, step)
    label_w = None if w is None else f"NATIVE_WALL: {w['label']} (archived)"
    if w is not None and w["role"] == "production":
        ch = {"c0_cal": {"status": "INCONCLUSIVE", "reason": label_w, "diagnostics": {}},
              "c0_val": None, "prod": None, "decoder": None, "frozen": None}
    else:
        ch = chart_one(j, acts, tables, m_cal[32], ledger_for(out, j, step), ctx["cfg"], cdir,
                       ctx.get("timed"), skip_direct=w is not None)
        if w is not None:
            ch["c0_val"] = {"status": "INCONCLUSIVE", "reason": label_w, "criteria": None,
                            "n": None, "n_supported": None, "fidelity": None, "bins": None,
                            "resultant": None, "direct_status": "INCONCLUSIVE",
                            "direct_reason": label_w, "direct_diagnostics": {}}
    ch.pop("acts_cal", None)
    cert = r = sup = agree = None
    cb, cons = {}, {}
    if ch["prod"] is not None:
        canon = tables["test"]["canon32"]
        r = arrays_one(ch["prod"], acts("test"), m, ctx["refs_test"], ctx["eps"], ctx["cfg"],
                       ctx["planted"])
        cert, dec = r["certificate"], ch["decoder"]
        cons = controls_one(m, canon, r["ext"], dec)
        if not ctx["planted"]:
            cb = k4b_cert.control_bounds_all(
                {n: {"k": e} for n, e in cons.items() if "unavailable" not in e},
                ctx["refs_test"], ctx["eps"])
        sup = k4b_scores.support_report(r["ext"], ch["prod"]["chart"].support_radius,
                                        r["arrays"]["r4n"], r["ext"].phase, m[32], m[4], False)
        agree = (k4b_decoder.agreement(r["ext"].phase, k4b_decoder.predict_phase(dec, canon),
                                       r["ext"].supported)
                 if dec.get("status") == "AVAILABLE" else
                 f"unavailable ({dec.get('reason', '')})")
    status, label = status_of_checkpoint(ch, cert)
    _write_json(cdir / "LEARN.json", learn)
    arrays_sha = None
    if r is not None:
        a = r["arrays"]
        arr = {"X_minus": a["X_minus"], "X_plus": a["X_plus"], "r4n": a["r4n"],
               "phi": np.asarray(r["ext"].phase, dtype=np.float64),
               "supported": np.asarray(r["ext"].supported, dtype=bool),
               "delta1_X_minus": cons["delta1"]["X_minus"], "delta1_X_plus": cons["delta1"]["X_plus"],
               "delta2_X_minus": cons["delta2"]["X_minus"], "delta2_X_plus": cons["delta2"]["X_plus"],
               "naive_X": cons["naive"]["X"]}
        if "unavailable" not in cons["decoder"]:
            arr.update(decoder_X=cons["decoder"]["X"], decoder_phi=cons["decoder"]["phi"])
        stage_records.save_npz(cdir / "ARRAYS.npz", **arr)
        arrays_sha = _sha(cdir / "ARRAYS.npz")
        if cb:
            _write_json(cdir / "CONTROLS_B.json", {n: e["k"] for n, e in cb.items()
                                                   if "max_B" in e["k"]})
    certificate = None
    if cert is not None:
        certificate = {"status": cert["status"], "max_B": {k: str(v) for k, v in
                                                          cert["max_B"].items()},
                       "max_abs": r["max_abs"], "n": int(len(r["arrays"]["X_minus"])),
                       "planted": bool(ctx["planted"])}
    wall = None
    for role, st, rs in (("production", ch["c0_cal"]["status"], ch["c0_cal"]["reason"]),
                         ("direct", (ch["c0_val"] or {}).get("direct_status"),
                          (ch["c0_val"] or {}).get("direct_reason"))):
        if rs and _is_wall(st, rs):
            wall = {"role": role, "text": _text(st, rs)}
    dec = ch["decoder"]
    rec = {"master": int(j), "step": int(step), "k": dc.K_OF[int(step)],
           "checkpoint_id": dc.CHECKPOINTS[(int(j), int(step))]["id"] if (int(j), int(step))
           in dc.CHECKPOINTS else None,
           "status": status, "label": label,
           "valid": ch["c0_cal"]["status"] == "PASS" and bool(ch["c0_val"]) and
           ch["c0_val"]["status"] == "PASS",
           "c0_cal": ch["c0_cal"], "c0_val": ch["c0_val"],
           "decoder": None if dec is None else {"status": dec.get("status"),
                                                "reason": dec.get("reason", "")},
           "certificate": certificate, "support": sup, "decoder_agreement": agree,
           "controls_certified": {n: bool(e["k"].get("certified")) for n, e in cb.items()
                                  if "certified" in e["k"]},
           "arrays_sha256": arrays_sha,
           "frozen_sha256": _sha(cdir / "FROZEN.json") if ch["frozen"] else None,
           "learn_sha256": _sha(cdir / "LEARN.json"), "native_wall": wall,
           "planted": bool(ctx["planted"])}
    rec = _jsonable(rec)
    stage_records.write_new(cdir / "CHECKPOINT_RECORD.json", rec)
    return rec


def run_checkpoints(ctx, j, pause=None) -> list:
    recs = []
    for step in dc.STEPS:
        ckpt, model64, _ = load_checkpoint_d(j, step)
        recs.append(score_checkpoint(ctx, j, step, ckpt=ckpt, model64=model64,
                                     perm=ctx["proc"]["perm"][j]))
        del ckpt, model64
        if pause is not None:
            pause()
    return recs


def determinism_d(ctx, j, records) -> dict:
    good = [r for r in records if r["c0_cal"]["status"] == "PASS"]
    picks = [] if not good else ([good[0]] if good[0] is good[-1] else [good[0], good[-1]])
    for r in picks:
        _, model64, _ = load_checkpoint_d(j, r["step"])
        perm = ctx["proc"]["perm"][j]
        new = acts_fn(model64, perm)(ctx["tables"]["cal"]["canon32"])
        with np.load(checkpoint_dir(ctx["out"], j, r["step"]) / "ACTS_cal.npz") as f:
            stored = f["acts"]
        det = k4b_charts.determinism_check({"acts": stored}, {"acts": new})
        if det["status"] != "PASS":
            raise C1GateFailure("FAIL_TECHNICAL/DETERMINISM", str(det["mismatch"]))
    return {"status": "PASS", "n": len(picks), "steps": [r["step"] for r in picks]}


def acceptance(out, j, job, attempt, records, cpu_s, freeze_sha256) -> dict:
    out = Path(out)
    root = out / "stages" / "SCORE" / str(j)
    files = {f.relative_to(out).as_posix(): _sha(f)
             for f in sorted(root.rglob("*")) if f.is_file()}
    rec = {"job": job, "master": int(j), "attempt": attempt,
           "counts": {s: sum(1 for r in records if r["status"] == s) for s in STATUSES},
           "fail_technical": None, "files_sha256": files, "cpu_s": cpu_s,
           "protocol_sha256": dc.PROTOCOL_SHA256, "freeze_sha256": freeze_sha256,
           "utc": hwsd_records.utc()}
    hwsd_records.acceptance_check(rec)
    stage_records.write_new(root / "ACCEPTANCE.json", rec)
    return rec
