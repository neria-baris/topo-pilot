"""HWSB stage cores: one model's training and the EVAL gate sequence (API.md §8; protocol §4,
§5, §6.1). Split out of hwsb_driver by size (the HWS E16 pattern); the driver adds preflight,
authority, pauses and the CLI. A Plan argument lets the dry run use the same code.

EVAL's B9a hashes and reads stage B's OWN history payloads in its own store (ruling c7).
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import time
from pathlib import Path

import hws_exact
import hwsb_data as hd
import hwsb_eval as he
import hwsb_gates as hg
import hwsb_known as hk
import hwsb_law as hl
import hwsb_train as ht
import k4b_cert
import k4b_charts
import k4b_config
import numpy as np
import stage_records

from topo_pilot.contracts import Checkpoint


def _gate(out, gate, status, **details) -> str:
    return stage_records.record_gate(Path(out), gate, status, **hk.jsonable(details))


def train_core(out, store, proc, master, plan=hc.REAL_PLAN, hold=None) -> dict:
    """make_train_dev, then ht.train; TRAIN_RECORD.json (also written on a stop)."""
    d = Path(out) / "stages" / "TRAIN" / str(master)
    d.mkdir(parents=True, exist_ok=True)
    ids = hd.make_train_dev(store, proc, master, plan)
    rec = {
        "master": int(master),
        "observation_ids": {s: ids[s] for s in ("train", "dev")},
        "streams": ids["streams"],
        "run_key": list(hc.run_key(plan, master)),
    }
    try:
        res = ht.train(store, ids, master, plan, hold)
    except hc.HwsbStop as exc:
        rec.update(
            status=exc.status,
            reason=exc.reason,
            holds=list(hold.events) if hold is not None else [],
        )
        stage_records.write_new(d / "TRAIN_RECORD.json", hk.jsonable(rec))
        raise
    rec.update(
        status="COMPLETE",
        **{k: res[k] for k in ("checkpoint_ids", "checksums", "dev_ce", "summary", "holds")},
    )
    rec.update(torch=ht.torch_versions(), process_cpu_s=time.process_time())
    stage_records.write_new(d / "TRAIN_RECORD.json", hk.jsonable(rec))
    return rec


def _ckpt(store, rec, step) -> Checkpoint:
    ids = rec["checkpoint_ids"]
    return store.load(
        Checkpoint, ids[str(step)] if str(step) in ids else ids[step], consumer="experiment"
    )


def _acts(store, rec, step, canon32, perm, plan) -> np.ndarray:
    model64, _ = he.load64(_ckpt(store, rec, step))
    return he.activations(model64, hd.model_inputs(canon32, perm), plan.site)


def _cpu_by_model(ledger_path, masters) -> dict:
    import hwsb_driver as hdr

    if ledger_path is None:
        return {}
    ent = [e for e in hdr.ledger_read(ledger_path)["entries"] if e["stage"] == "TRAIN"]
    return {int(e["master"]): float(e["cpu_s"]) for e in ent if e.get("master") in masters}


def eval_core(
    out,
    plan,
    proc,
    store,
    train_records,
    hws_digests=None,
    p_d2a_ref=None,
    kb4_z=None,
    ledger_path=None,
    pause=None,
    freeze_sha256=None,
) -> dict:
    """Every EVAL gate in the §4 order; gates are computed whatever an earlier decision gave."""
    out, ms, cfg = Path(out), list(plan.masters), k4b_config.chart_cfg()
    pause = pause or (lambda: None)
    rep = {
        "label": "pilot, uncertified",
        "per_model": {m: {} for m in ms},
        "gates": {},
        "freeze_sha256": freeze_sha256,
    }
    st = {
        "fail": None,
        "incomplete": None,
        "b1": {},
        "b4": {},
        "b5": None,
        "b6": None,
        "b5_positive": False,
        "b8a": None,
        "b9a": None,
    }
    c = {}

    def g_blocks():
        c["blk"] = {r: hd.make_block(proc, r, plan) for r in hd.BLOCKS}
        for b in c["blk"].values():
            hd.save_block(out, b)
        return "PASS", {r: b["stream"] for r, b in c["blk"].items()}

    def g_h2b():
        td = {
            f"{s}_{m}": hd.train_dev_canonical(
                store, train_records[m]["observation_ids"][s], proc["perm"][m]
            )
            for m in ms
            for s in ("train", "dev")
        }
        r = hd.separation(c["blk"], td, hws_digests)
        (out / "stages" / "EVAL").mkdir(parents=True, exist_ok=True)
        stage_records.write_new(out / "stages" / "EVAL" / "H2B.json", hk.jsonable(r))
        rep["h2b"] = r
        if r["status"] != "PASS":
            raise hc.HwsbStop(r["status"], "H2-B separation")
        return "PASS", {"collisions": r["collisions"]}

    def g_kb7():
        rep["kb7"] = hk.kb7(proc, c["blk"]["VAL"]) if not plan.dry else {"status": "NOT_RUN"}
        return rep["kb7"]["status"], {}

    def g_b123():
        q = he.oracle_predictives(proc, c["blk"]["LGATE"]["canon32"], (1, 4))
        for m in ms:
            p = he.model_predictive(
                _ckpt(store, train_records[m], plan.gate_step),
                c["blk"]["LGATE"]["canon32"],
                proc["perm"][m],
            )
            pm = rep["per_model"][m]
            pm["b1"], pm["b2"], pm["b3"] = he.b1(q, p), he.b2(q, p), he.b3(q, p, proc["n_axial"])
            st["b1"][m] = pm["b1"]["status"]
        ok = all(v == "PASS" for v in st["b1"].values())
        return ("PASS" if ok else "FAIL"), {"per_model": st["b1"]}

    def g_b4():
        cal, val = c["blk"]["CAL"], c["blk"]["VAL"]
        c["mC"], c["mV"] = he.moments(proc, cal["canon32"]), he.moments(proc, val["canon32"])
        land, vland = hd.lowest_rows(cal["seq_ids"]), hd.lowest_rows(val["seq_ids"])
        Xc = {
            m: _acts(
                store, train_records[m], plan.gate_step, cal["canon32"][land], proc["perm"][m], plan
            )
            for m in ms
        }
        Xi = {
            m: _acts(
                store, train_records[m], plan.init_step, cal["canon32"][land], proc["perm"][m], plan
            )
            for m in ms
        }
        ids, m32 = np.asarray(cal["seq_ids"])[land], c["mC"][32][land]
        cal_r = hg.b4_cal(out, Xc, ids, m32, cfg)
        init = hg.b4_init(out, Xi, ids, m32, cfg)
        rep["b4_frozen"] = hg.b4_freeze(out, cal_r, init)
        Xv = {
            m: _acts(store, train_records[m], plan.gate_step, val["canon32"], proc["perm"][m], plan)
            for m in ms
            if cal_r["status"][m] == "PASS"
        }
        val_r = hg.b4_val(
            out,
            cal_r,
            {m: (Xv[m][vland] if m in Xv else None) for m in ms},
            np.asarray(val["seq_ids"])[vland],
            cfg,
        )
        s = hg.b4_status(cal_r, val_r, ms)
        c["charted"], c["ends"] = [m for m in ms if m in Xv], {}
        for m in c["charted"]:
            prod = cal_r["per_model"][m]
            ext = k4b_charts.extend(prod["chart"], prod["gauge"], Xv[m], cfg)
            c["ends"][m] = he.endpoints(ext, c["mV"])
            rep["per_model"][m]["support"] = he.support(
                ext, prod["chart"].support_radius, c["ends"][m], c["mV"]
            )
        for m in ms:
            rep["per_model"][m]["b4"] = {
                "c0_cal": cal_r["status"][m],
                "c0_val": val_r["status"][m],
                "diagnostics": cal_r["per_model"][m]["diagnostics"],
                "c0_val_record": val_r["per_model"][m],
                "init": init["per_model"][m]["status"],
            }
            st["b4"][m] = (
                "PASS"
                if s["per_model"][m]["pass"]
                else ("C0_CAL" if cal_r["status"][m] != "PASS" else "C0_VAL")
            )
        if s["technical"]:
            raise hc.HwsbStop(s["technical"], "chart code")
        return ("PASS" if s["pass"] else "FAIL"), s

    def g_b8a():
        law = hl.law_bound(
            proc["T"],
            proc["E_canon_shared"],
            proc["pi"],
            proc["coords"],
            proc.get("sigma", hc.SIGMA),
            proc.get("neighbour", hc.NEIGHBOUR),
        )
        ok = law["status"] == "BOUNDED" and (kb4_z is None or law["Z_bound"] == kb4_z)
        st["b8a"] = "PASS" if ok else "FAIL_TECHNICAL/LAW_BOUND"
        c["Z"] = law["Z_bound"] if ok else hc.Z_STANDIN
        c["F"] = k4b_cert.F_plan(c["Z"])
        rep["b8a"], rep["F_plan"] = {k: v for k, v in law.items() if k != "raw"}, c["F"]
        return st["b8a"], {"Z_bound": c["Z"]}

    def g_b6():
        ch = c.get("charted", [])
        if not ch:
            rep["b6"] = {"status": "NOT_RUN"}
            return "NOT_RUN", {}
        e = c["ends"]
        lad = hg.ladder_pilot(
            {m: e[m]["X_minus"] for m in ch},
            {m: e[m]["X_plus"] for m in ch},
            {m: e[m]["r4n"] for m in ch},
            c["F"],
            ch,
        )
        c["lad"], rep["b6"] = lad, lad
        if len(ch) == len(ms):
            st["b6"] = "PASS" if lad["status"] == "PASS" else "FAIL"
        return lad["status"], {"N": lad["N"], "gated": len(ch) == len(ms)}

    def g_b5():
        ch = c.get("charted", [])
        if not ch:
            return "NOT_RUN", {}
        e, lad = c["ends"], c["lad"]
        r = hg.b5(
            {m: e[m]["X_minus"] for m in ch},
            he.d4_rows(c["mV"]),
            {m: lad["sdU"][(m, "-")] for m in ch},
            hg.b5_N(lad),
            c["F"],
            ch,
        )
        rep["b5"] = r
        st["b5"] = {m: ("PASS" if r["per_model"][m]["pass"] else "FAIL") for m in ch}
        st["b5_positive"] = r["positive_below_planning"]
        return r["status"], {"N_C": r["N_C"]}

    def g_b7():
        rep["b7"] = hg.b7(_cpu_by_model(ledger_path, ms), hg.b5_N(c.get("lad")))
        return "REPORTED", rep["b7"]

    def g_b9a():
        p = hws_exact.p_d2a(proc["T"], proc["E_canon_shared"], proc["pi"])
        r = hg.b9a(out, hg.b5_N(c.get("lad")), p, p if p_d2a_ref is None else p_d2a_ref, c["blk"])
        rep["b9a"], st["b9a"] = r, r["status"]
        return r["status"], {"value": r["value"]}

    steps = [
        ("BLOCKS", g_blocks),
        ("H2-B", g_h2b),
        ("KB7", g_kb7),
        ("B1", g_b123),
        ("B4", g_b4),
        ("B8a", g_b8a),
        ("B6", g_b6),
        ("B5", g_b5),
        ("B7", g_b7),
        ("B9a", g_b9a),
    ]
    for name, fn in steps:
        if st["fail"]:
            _gate(out, name, "NOT_RUN")
            continue
        pause()
        try:
            status, det = fn()
        except hc.HwsbStop as exc:
            st["fail"] = exc.status if exc.status.startswith("FAIL_TECHNICAL") else None
            st["incomplete"] = None if st["fail"] else exc.reason
            status, det = exc.status, {"reason": exc.reason}
        except Exception as exc:  # noqa: BLE001  mapped; later gates NOT_RUN
            import hwsb_driver as hdr

            st["fail"] = hdr.status_of(exc)
            status, det = st["fail"], {"reason": f"{type(exc).__name__}: {exc}"}
        rep["gates"][name] = {"status": status}
        _gate(out, name, status, **det)
    oc = hg.outcome(st)
    lad = c.get("lad") or {}
    fill = {
        "N_C": lad.get("N"),
        "training_forecast_s": (rep.get("b7") or {}).get("training_forecast_s"),
        "Z_bound": c.get("Z"),
    }
    rep.update(
        outcome=oc["outcome"],
        annotations=oc["annotations"],
        state=st,
        licence=hg.licence(oc, fill),
        protocol_sha256=hc.CONTRACT["protocol_sha256"],
        margin={"M": hc.M},
        own_payloads_hashed_by_B9a=True,
    )
    _gate(out, "OUTCOME", oc["outcome"])
    stage_records.write_new(out / "REPORT.json", hk.jsonable(rep))
    b7 = rep.get("b7") or {}
    excl = sorted(v for r in train_records.values() for v in r.get("checkpoint_ids", {}).values())
    h = hg.handoff_record(
        {
            "outcome": oc["outcome"],
            "N_C": lad.get("N"),
            "k_C": lad.get("k"),
            "model_count": 3,
            "training_forecast_s": b7.get("training_forecast_s"),
            "evaluation_forecast_s": b7.get("evaluation_forecast_s"),
            "Z_bound": c.get("Z"),
            "F_plan": c.get("F"),
            "p_D2a": (rep.get("b9a") or {}).get("p_D2a"),
            "registry_value": (rep.get("b9a") or {}).get("value"),
            "store_inventory": (rep.get("b9a") or {}).get("inventory"),
            "stage_c_exclusions": excl,
            "registry_obligation": hc.CONTRACT["handoff"]["registry_obligation"],
            "protocol_sha256": hc.CONTRACT["protocol_sha256"],
            "freeze_sha256": rep.get("freeze_sha256"),
            "report_sha256": stage_records.sha256(out / "REPORT.json"),
        }
    )
    stage_records.write_new(out / "HANDOFF.json", hk.jsonable(h))
    return rep
