"""HWS synthetic dry run: the decision, records and meter cases DR9-DR13, the R-0118-1 design
check and run_dry with the DRY_REPORT writer (protocol §13, TEST_PLAN §4). Split from hws_driver
by size (erratum E16); hws_driver.run_dry delegates here. Planted decision fixtures are labelled
"fixture": true and never enter hist/; running the dry run is a separate metered job.
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import math
from fractions import Fraction
from pathlib import Path

import hws_worlds as hw
import hws_driver as hd
import hws_exact as he
import hws_known as hk
import hws_oracle as ho
import hws_records as hr
import hws_select as hsel
import hws_stats as hs
import numpy as np
import stage_records
from hws_known import TINY, KNOWN, _dry
from topo_pilot.dataset.sampler import HMMSampler


def _b(mean, se=0.001) -> dict:
    z = {"L1": -hs.Z1, "U1": hs.Z1, "Lw": -hs.ZW, "Uw": hs.ZW}
    return dict({k: mean + v * se for k, v in z.items()}, mean=mean, se=se, n=4096)


def _fx(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig="ELIGIBLE", se=0.001) -> dict:
    """A planted decision fixture (labelled), classified by hws_select under FIX floors."""
    w = hw.World(W, q, Fraction(str(s)), Fraction(str(p)))
    b = {"D4": _b(d4, se), "GC": _b(gc, se), "G4": _b(g4, se), "G4A": _b(g4a, se)}
    for q_ in b:
        b[q_]["L3"] = b[q_]["mean"]
    rec = {"fixture": True, "key": w.key, "W": W, "q": q, "sigma": str(w.sigma), "p": str(w.p)}
    t = None if (W, q) == (12, 3) else hw.tier(w)
    rec.update(tier=t, changed=hw.changed_factors(w), distance=str(hw.distance(w)), bounds=b)
    rec.update(eligibility=elig, e6_ok=True)
    return dict(rec, **hsel.classify(rec, FIX))


FIX = {"D4": 0.03, "GC": 0.10, "G4": 0.0078, "G4A": 0.004}


def _oc(recs, ordinary=(), fallback=(), quals=(), below=(), complete=True, fail=None) -> str:
    s3 = {
        r["key"]: hsel.s3_evaluate(r, FIX, "ordinary" if r["key"] in ordinary else "fallback_only")
        for r in recs
        if r["key"] in set(ordinary) | set(fallback)
    }
    for k in s3:
        s3[k].update(qualifies=k in quals, below_3x=k in below or k in quals)
    st = {"fail": fail, "complete": complete, "records": recs, "s3": s3, "floors": FIX}
    st["finalists"] = {"ordinary": list(ordinary), "fallback_only": list(fallback)}
    return hsel.outcome(st)


def dr9(out):
    a, b2, c = _fx(12, 1, 1.25, 0.875), _fx(12, 2, 1.25, 0.2), _fx(16, 1, 1.25, 0.875)
    ex1, ex2 = _fx(16, 1, 1.25, 0.2, d4=0.004), _fx(16, 2, 1.5, 0.2, d4=0.05, gc=0.05)
    marg, inel = _fx(16, 3, 1.25, 0.5, d4=0.027), _fx(8, 1, 2, 0.5, elig="INELIGIBLE/E5")
    k = [r["key"] for r in (a, b2, c)]
    got = {f"T{i}": _oc([a, b2, c], k, quals=k[i:])["outcome"] for i in range(3)}
    got["BELOW_shown"] = _oc([ex1, inel], [ex1["key"]], below=[ex1["key"]])["outcome"]
    nshown = _oc([ex1, marg], [ex1["key"]], below=[ex1["key"]])
    got["BELOW_not_shown"] = nshown["outcome"] + ("" if nshown["absence_3x_shown"] else "/not")
    got["NWC"] = _oc([ex1, marg], [ex1["key"]])["outcome"]
    got["HEADROOM"] = _oc([ex1, inel])["outcome"]
    got["FILTER"] = _oc([ex1, ex2])["outcome"]
    got["FILTER_no_eligible"] = _oc([inel])["outcome"]
    got["PAUSED"] = _oc([ex1, inel], complete=False)["outcome"]
    got["FAIL"] = _oc([ex1], fail="NULL")["outcome"]
    fb = _oc([marg], fallback=[marg["key"]], below=[marg["key"]])
    got["FALLBACK_ONLY"] = (fb["outcome"], fb["selected"], fb["fallback_list"])
    want = {
        "T0": "HWS_SELECTED/T0",
        "T1": "HWS_SELECTED/T1",
        "T2": "HWS_SELECTED/T2",
        "BELOW_shown": "HWS_BELOW_3X",
        "BELOW_not_shown": "HWS_BELOW_3X/not",
        "NWC": "HWS_NO_WORLD_CONFIRMED",
        "HEADROOM": "HWS_NO_SUITABLE_WORLD/HEADROOM",
        "FILTER": "HWS_NO_SUITABLE_WORLD/FILTER",
        "PAUSED": hd.REFUSE,
        "FILTER_no_eligible": "HWS_NO_SUITABLE_WORLD/FILTER",
        "FAIL": "FAIL_TECHNICAL/NULL",
        "FALLBACK_ONLY": ("HWS_BELOW_3X", None, []),
    }
    eq = hsel.criteria({q: {"L3": v} for q, v in FIX.items()}, FIX, "L3")
    got["equality"] = all(eq.values()) and he.e4_check(Fraction(1, 2000000))["status"] == "PASS"
    try:
        hsel.classify({"eligibility": "ELIGIBLE", "bounds": {"D4": {"Uw": math.nan}}}, FIX)
        got["nan"] = "no stop"
    except hw.HwsStop as exc:
        got["nan"] = exc.status
    got["marginal_slot"] = hsel.finalists([marg, ex1])["ordinary"] == []
    tie = [_fx(12, 1, 1.25, 0.9375, d4=0.012), _fx(12, 1, 1.5, 0.2, d4=0.012)]
    got["x1_tie"] = hsel.x1_trigger(tie)["world"] == "W12-q1-s1.25-p0.9375"
    got["annotations"] = hsel.annotations({"Lw": 0.002, "Uw": 0.009}) != []
    rep = hr.report_record({"records": [ex1], "finalists": {}, "floors": FIX}, _oc([ex1]), {})
    got["report_keys"] = {"outcome", "licence", "worlds", "z"} <= set(rep)
    ok = all(got[k] == v for k, v in want.items()) and got["nan"].startswith("FAIL_TECHNICAL")
    ok = ok and all(
        got[k] is True
        for k in ("equality", "marginal_slot", "x1_tie", "annotations", "report_keys")
    )
    return ok, {"fixture": True, "got": got}


def dr10(out):
    tiny, res = dict(hw.build_tiny(), key="DR10-a"), {}
    planted = {"rows": {"nulls": {"m4_phase": np.array([1.0, 1.0 + 1e-9] * 8)}}, "layout": TINY}
    res["not_reproduced"] = hd.null_recheck(out, tiny, "DRY", planted, 512, (1, 2, 4))
    stored = (Path(out) / "hist" / "NULLCHK" / "DRY" / "DR10-a.npz").exists()
    real = ho.world_look
    ho.world_look = lambda proc, *a, **k: dict(real(proc, *a, **k), rows=planted["rows"])
    try:
        for stage, key in (("DRY", "DR10-b"), ("S0", "DR10-c")):
            try:
                hd.null_recheck(out, dict(tiny, key=key), stage, planted, 64, (1, 2, 4))
                res[stage] = "continued"
            except hw.HwsStop as exc:
                res[stage] = exc.status
    finally:
        ho.world_look = real
    ok = not res["not_reproduced"]["reproduced"] and stored
    ok = ok and res["DRY"] == "FAIL_TECHNICAL/NULL" and res["S0"] == KNOWN
    return ok, hr.num(dict(res, stored=stored))


def _ref_m(T, E, pi, tok, K, c, trap=None) -> np.ndarray:
    """Independent suffix filter (restart from pi, emit first) and its five alignment traps."""
    TT, EE = (T.T if trap == "transposed_T" else T), (E[:, [1, 2, 0]] if trap == "symbols" else E)
    n, L = tok.shape
    out = np.empty((n, 2))
    for r in range(n):
        seq = (
            tok[r] if trap == "inherited" else (tok[r, :K] if trap == "prefix" else tok[r, L - K :])
        )
        b = pi.copy()
        for t, w in enumerate(seq):
            b = (b @ TT if t else b) * EE[:, int(w)]
            b = b / b.sum()
        out[r] = (b @ TT if trap == "trailing" else b) @ c
    return out


def dr11(out):
    rng = np.random.default_rng(13011)
    tiny = hw.build_tiny()
    T = rng.random((12, 12)) + 0.05
    T /= T.sum(axis=1, keepdims=True)
    pi = np.linalg.matrix_power(T.T, 2000) @ np.full(12, 1.0 / 12)
    proc = dict(tiny, T=T, pi=pi / pi.sum())
    look = _dry(proc, "DR11", 300)
    tok, m2, c = look["tok"], look["rows"]["m"][2], tiny["features"]
    good = float(np.max(np.abs(_ref_m(T, tiny["E"], proc["pi"], tok, 2, c) - m2)))
    traps = ("transposed_T", "symbols", "prefix", "inherited", "trailing")
    dev = {
        t: float(np.max(np.abs(_ref_m(T, tiny["E"], proc["pi"], tok, 2, c, t) - m2))) for t in traps
    }
    return good <= 1e-12 and min(dev.values()) > 1e-6, {"correct": good, "traps": dev}


def dr12(out):
    import controls
    import hws_meter_bind as hm
    import k4b_meter_bind
    import meter
    import winjob

    base, det = Path(out) / "DR12" / hr.utc().replace(":", ""), {}
    base.mkdir(parents=True)
    stage_records.write_new(base / "x.json", {"a": 1})
    try:
        stage_records.write_new(base / "x.json", {"a": 2})
        det["exclusive"] = False
    except FileExistsError:
        det["exclusive"] = True
    ctx = {"out": base, "cont": set(), "cum_fc": 10**9}
    for name, args in (("stage", (301.0, 100)), ("cumulative", (0.0, 10**9))):
        ctx["cum_fc"] = 10**9 if name == "stage" else 1e-9
        try:
            hd._pause(ctx, "DRY", *args)
            det[name] = "no pause"
        except hd.Paused:
            det[name] = "paused"
    calls, real = [], HMMSampler.sample
    HMMSampler.sample = lambda self, n, rng: calls.append(n) or real(self, n, rng)
    try:
        first = _dry(hw.build_tiny(), "DR12", 64)
    finally:
        HMMSampler.sample = real
    hr.save_hist(base, "DRY", "DR12", first["tok"])
    hr.append_stage_event(base, {"event": "STAGE_BEGIN", "stage": "DRY", "worklist": ["DR12"]})
    moved = hr.archive_partial(base, "DRY")
    again = _dry(hw.build_tiny(), "DR12", 64)
    det["resume_identical"] = bool(moved) and np.array_equal(first["tok"], again["tok"])
    det["one_sample_call"] = calls == [64]
    keep = [
        (m, k, getattr(m, k))
        for m, ks in (
            (
                meter,
                (
                    "OUT",
                    "LEDGER",
                    "EMERGENCY",
                    "LOCK",
                    "ACTIVE",
                    "LOG_DIR",
                    "CAP_S",
                    "STOP_NEW_S",
                    "OUTPUT_CAP",
                    "WORKER_SESSION",
                ),
            ),
            (controls, ("JOB_ID", "TASK_SHA256")),
            (winjob, ("MEMORY_CAP",)),
            (k4b_meter_bind, ("TEMP_ROOT",)),
        )
        for k in ks
    ]
    try:
        hm.bind("DRY", "0" * 64, base, "dry-session")
        det["meter"] = hr.num(hm.effective_settings())
        argv = k4b_meter_bind.rewrite_argv(["--label", "x", "--max-cpu", "600", "--", "py"])
    finally:
        for m, k, v in keep:
            setattr(m, k, v)
    eff = det["meter"]
    det["meter_ok"] = eff["memory_cap"] == hm.MEMORY_CAP and eff["temp_root"] == str(base)
    det["argv_inf"] = argv[2:6] == ["--max-cpu", "inf", "--max-wall", "inf"]
    want = {"exclusive": True, "stage": "paused", "cumulative": "paused"}
    ok = all(det[k] == v for k, v in want.items())
    ok = ok and all(det[k] for k in ("resume_identical", "one_sample_call", "meter_ok", "argv_inf"))
    return ok, det


def dr13(out):
    det = {}
    for s in (Fraction(3, 2), Fraction(11, 8)):
        rep = he.law_bound_report(hw.build_process(hw.World(12, 1, s, Fraction(1, 5))))
        det[str(s)] = rep["status"]
    recs = [_fx(12, 1, 1.5, 0.875), _fx(12, 1, 1.25, 0.875, se=0.003)]
    before = hsel.finalists(recs)
    after = hsel.finalists([dict(r, law_bound=det["3/2"]) for r in recs])
    proc = hw.build_process(hw.World(12, 1, Fraction(3, 2), Fraction(1, 5)))

    def broken(*args):
        raise RuntimeError("planted technical failure")

    try:
        he.law_bound_report(proc, enclosure=broken)
        det["other_exception"] = "swallowed"
    except RuntimeError:
        det["other_exception"] = "propagated"
    det["bounded_clause"] = "NOT_APPLICABLE (R-0118-3: no reviewed enclosure in J1)"
    ok = set(det[k] for k in ("3/2", "11/8")) == {"UNAVAILABLE/NONTERMINATING_LOGIT"}
    ok = ok and before == after and det["other_exception"] == "propagated"
    return ok, dict(det, ranking_unchanged=before == after)


def design_checks() -> dict:
    """R-0118-1: the exact p-weighted SD of H(r_w) under the rebuilt w0 spec (a note)."""
    w0 = hw.build_process(hw.W0)
    p, h = he.symbol_law(w0), ho.entropy_rows(he.last_symbol_posteriors(w0))
    mean = float(p @ h)
    sd = math.sqrt(float(p @ (h - mean) ** 2))
    return {
        "KC3_exact_mean": mean,
        "KC3_exact_sd": sd,
        "KC3_reference": 3.140,
        "KC3_owner_flag_if_sd_below": 0.018,
        "note": "design check, not a gate",
    }


CASES = {
    f"DR{i}": f
    for i, f in enumerate(
        (
            hk.dr1,
            hk.dr2,
            hk.dr3,
            hk.dr4,
            hk.dr5,
            hk.dr6,
            hk.dr7,
            hk.dr8,
            dr9,
            dr10,
            dr11,
            dr12,
            dr13,
        ),
        1,
    )
}


def run_dry(out=hw.DRY_STORE) -> dict:
    """§13 synthetic dry run with the real records, selection and report code (J1 AUTH)."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    hr.append_stage_event(out, {"event": "STAGE_BEGIN", "stage": "DRY", "worklist": list(CASES)})
    cases = {}
    for name, fn in CASES.items():
        try:
            ok, det = fn(out)
            cases[name] = {"status": "PASS" if ok else "FAIL", "details": hr.num(det)}
        except Exception as exc:  # noqa: BLE001  a defect is reported, never hidden
            cases[name] = {"status": "FAIL", "details": {"error": f"{type(exc).__name__}: {exc}"}}
    head = hr._git(hw.REPO, "rev-parse", "HEAD").decode().strip()
    dirty = hr._git(hw.REPO, "status", "--porcelain", "--", "tools/hws", "tests/hws").strip()
    files = hr.implementation_files(hw.REPO, head)
    rep = {"cases": cases, "all_pass": all(c["status"] == "PASS" for c in cases.values())}
    rep.update(h_exec=head, tree_clean=not dirty, implementation_files=files)
    rep["implementation_sha256"] = hr.sha_bytes(hr.canonical_json(files).encode("utf-8"))
    rep["design_checks"] = design_checks()
    path = out / "stages" / "DRY" / "DRY_REPORT.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(path, hr.num(rep))
    files = {path.relative_to(out).as_posix(): stage_records.sha256(path)}
    hr.append_stage_event(out, {"event": "STAGE_COMPLETE", "stage": "DRY", "files": files})
    return {"status": "PASS" if rep["all_pass"] else "FAIL", "report": str(path)}
