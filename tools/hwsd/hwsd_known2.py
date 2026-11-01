"""HWSD known cases KD2 (binding mirrors) and KD3 (stage-C reproduction) with their helpers
(API.md §9; split from hwsd_known by size, API erratum; hwsd_known re-exports every name)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import contextlib
import importlib
import json
import tempfile
from fractions import Fraction
from pathlib import Path

import hwsc_bind
import hwsc_data
import hwsc_known
import hwsd_bind
import hwsd_data
import k4b_cert
import k4b_config
import k4b_data
import k4b_decoder
import k4b_fresh
import k4b_scores
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure

from topo_pilot.contracts import ArtifactStore, SeedTree
from topo_pilot.contracts.backends import MemoryBackend

KNOWN = "FAIL_TECHNICAL/KNOWN_CASE"


# ------------------------------------------------------------------------------------ KD2
def _canon(x):
    if isinstance(x, np.ndarray):
        return ("nd", x.dtype.str, x.shape, x.tobytes())
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_canon(v) for v in x]
    if isinstance(x, (str, int, float, bool, Fraction, type(None), np.generic)):
        return x
    return None  # opaque objects (charts, decoders) are compared through their serial forms


def _fixture_calls(tmp) -> dict:
    import hwsd_dry
    import hwsd_score as ds

    T, E, pi, Xm, Xp, r4 = hwsc_known._fixture()
    F = Fraction(1, 10**4)
    params = {"noise": {"iii": 0.02}, "seeds": {"iii": min(dc.DRY_SEEDS.values())},
              "g_mass": 0.01}
    canon, ids = hwsd_data.sample_block_d(T, E, pi, "cal", 64, "hwsd-dry-v1/KD2", dc.PROCESS)
    res = {"sample": (canon.tobytes(), ids.tobytes()),
           "status": k4b_stats.model_status(0.02, 0.03, F, F),
           "F_plan": k4b_cert.F_plan(Fraction(1, 10**12)),
           "margin": k4b_cert.margin(Fraction(1, 10**8), Fraction(1, 10**12))}
    proc = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()))
    sizes = {s: 512 for s in dc.SPLITS}
    tabs = hwsd_data.sample_tables(proc, "hwsd-dry-v1/KD2", dc.PROCESS, sizes)
    mom = {s: k4b_scores.oracle_moments(proc["T"], proc["E_canon_shared"], proc["pi"],
                                        tabs[s]["canon32"], proc["features"])
           for s in ("cal", "test")}
    acts = {"cal": hwsd_dry.plant_acts("iii", tabs["cal"], mom["cal"], params),
            "val": hwsd_dry.plant_acts("iii", tabs["val"], mom["cal"], params),
            "test": hwsd_dry.plant_acts("iii", tabs["test"], mom["test"], params)}
    cfg, d = k4b_config.chart_cfg(), Path(tmp)
    import c1_chart

    ledger = c1_chart.ConstructionLedger(d / "CHART_CONSTRUCTIONS.json")
    ch = ds.chart_one(dc.MASTERS[0], lambda s: acts[s], tabs, mom["cal"][32], ledger, cfg,
                      d / "chart")
    res["chart"] = {k: ch[k] for k in ("c0_cal", "c0_val", "frozen")}
    res["decoder"] = k4b_decoder.to_arrays(ch["decoder"]) if ch["decoder"] else None
    if ch["prod"] is not None:
        a = ds.arrays_one(ch["prod"], acts["test"], mom["test"], None, None, cfg, planted=True)
        res["arrays"] = {"a": a["arrays"], "cert": a["certificate"], "max_abs": a["max_abs"]}
        res["controls"] = ds.controls_one(mom["test"], tabs["test"]["canon32"], a["ext"],
                                          ch["decoder"])
    return res


def kd2() -> dict:
    with hwsc_bind.suspended():
        checks = {}
        with tempfile.TemporaryDirectory(prefix="kd2a") as t1, \
                tempfile.TemporaryDirectory(prefix="kd2b") as t2:
            unbound = _canon(_fixture_calls(t1))
            with hwsd_bind.bound_hwsd(hwsd_bind.load_table(which="identity")):
                bound = _canon(_fixture_calls(t2))
        checks["a_identity"] = unbound == bound
        live = {(r["module"], r["name"]): getattr(importlib.import_module(r["module"]),
                                                  r["name"]) for r in hwsd_bind.load_table()}
        with hwsd_bind.bound_hwsd():
            au = hwsd_bind.audit()
            checks["b_audit"] = au["status"] == "PASS"
            g1 = k4b_data.history_generator("cal", 0).integers(0, 2**63, 64)
            g2 = SeedTree(0).generator("data", "hwsd-v1", "cal", 0, *dc.PROCESS).integers(
                0, 2**63, 64)
            g3 = SeedTree(0).generator("data", "hwsc-v1", "cal", 0, *dc.PROCESS).integers(
                0, 2**63, 64)
            checks["b_stream"] = bool(np.array_equal(g1, g2)) and not np.array_equal(g1, g3)
        checks["c_restored"] = all(getattr(importlib.import_module(m), n) is obj
                                   for (m, n), obj in live.items())
    return {"status": "PASS" if all(checks.values()) else KNOWN, "checks": checks,
            "audit_unlisted": au["unlisted"]}


# ------------------------------------------------------------------------------------ KD3
def c0_val_line(gates_path) -> dict:
    keep = []
    with open(gates_path, encoding="utf-8") as handle:
        for line in handle:
            if '"C0-VAL"' not in line:
                continue
            obj = json.loads(line)
            if obj.get("gate") == "C0-VAL":
                keep.append(obj)
            del obj
    if len(keep) != 1:
        raise C1GateFailure(KNOWN, f"{len(keep)} C0-VAL lines in GATES.jsonl")
    return keep[0].get("c0_val", keep[0])


@contextlib.contextmanager
def _write_guard(hwsc):
    """Decision 13: refuse any write under hwsc while KD3 runs."""
    base = Path(hwsc).resolve().as_posix().lower()

    def check(p):
        q = Path(p).resolve().as_posix().lower()
        if q == base or q.startswith(base + "/"):
            raise C1GateFailure(KNOWN, f"KD3 write refused: {p}")

    saved = (stage_records.write_new, stage_records.save_npz, Path.open)

    def w_new(path, *a, **k):
        check(path)
        return saved[0](path, *a, **k)

    def s_npz(path, *a, **k):
        check(path)
        return saved[1](path, *a, **k)

    def p_open(self, mode="r", *a, **k):
        if any(c in mode for c in "wxa+"):
            check(self)
        return saved[2](self, mode, *a, **k)

    stage_records.write_new, stage_records.save_npz, Path.open = w_new, s_npz, p_open
    try:
        yield
    finally:
        stage_records.write_new, stage_records.save_npz, Path.open = saved


def _npz(path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _same(a, b) -> bool:
    return set(a) == set(b) and all(
        a[k].dtype == b[k].dtype and a[k].shape == b[k].shape and a[k].tobytes() == b[k].tobytes()
        for k in a)


def _val(x):
    return float(x[0] if isinstance(x, (list, tuple)) else x)


def _load_table(hwsc, stage, name, split) -> dict:
    t = k4b_fresh.load_recorded(hwsc, stage, name)
    return dict(t, split=split, block=0)


def repro_c(out, hwsc=dc.HWSC_STORE) -> dict:
    import hwsd_score as ds

    out, hwsc, kd = Path(out), Path(hwsc), dc.CONTRACT["known_cases"]["KD3"]
    checks = {}
    with hwsc_bind.suspended(), _write_guard(hwsc), hwsc_bind.bound_stage_c():
        proc = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()))
        tabs = {"cal": _load_table(hwsc, "S3", "HIST_cal_b0.npz", "cal"),
                "val": _load_table(hwsc, "S3", "HIST_val_b0.npz", "val"),
                "test": _load_table(hwsc, "S7", "HIST_test_b0.npz", "test")}
        m = {s: k4b_scores.oracle_moments(proc["T"], proc["E_canon_shared"], proc["pi"],
                                          tabs[s]["canon32"], proc["features"])
             for s in ("cal", "test")}
        cfg, s4a = k4b_config.chart_cfg(), hwsc / "stages" / "S4a"
        stored_acts = k4b_fresh.load_recorded(hwsc, "S4a", "ACTS_cal_b0.npz")
        frozen = dc.read_json(s4a / "PRODUCTION_FROZEN.json")
        gate_val = c0_val_line(hwsc / "GATES.jsonl")
        result = dc.read_json(hwsc / "stages" / "S8" / "RESULT.json")
        import c1_chart

        arr, res, a0, a, b = {}, {}, {}, {}, {}
        for j in dc.MASTERS:
            for step, label in ((5000, "step5000"), (0, "step0")):
                ckpt, model64, _ = ds.load_checkpoint_d(j, step)
                acts = ds.acts_fn(model64, proc["perm"][j])
                A = {s: acts(tabs[s]["canon32"]) for s in ("cal", "val", "test")}
                a0[f"{j}_{label}"] = np.array_equal(A["cal"], stored_acts[f"{j}_{label}"])
                d = out / "stages" / "KD" / "REPRO" / str(j) / f"s{step}"
                led = c1_chart.ConstructionLedger(d / "CHART_CONSTRUCTIONS.json")
                ch = ds.chart_one(j, lambda s, A=A: A[s], tabs, m["cal"][32], led, cfg, d,
                                  skip_direct=step == 0)
                res[(j, step)] = ch
                if ch["prod"] is not None:
                    r = ds.arrays_one(ch["prod"], A["test"], m["test"], None, None, cfg,
                                      planted=True)
                    arr[(j, step)] = r["arrays"]
                if step == 5000:
                    ser = _npz(d / "CHART.npz") if ch["prod"] is not None else None
                    a[f"{j}_chart"] = ser is not None and _same(ser, _npz(s4a / f"CHART_{j}.npz"))
                    a[f"{j}_decoder"] = ch["decoder"] is not None and _same(
                        _npz(d / "DECODER.npz"), _npz(s4a / f"DECODER_{j}.npz"))
                    cv, g = ch["c0_val"] or {}, gate_val.get(str(j), {})
                    b[j] = bool(cv) and all(cv.get(k) == g.get(k) for k in (
                        "fidelity", "n_supported", "bins", "resultant"))
                elif j == dc.MASTERS[0]:
                    a[f"{j}_init_chart"] = ch["prod"] is not None and _same(
                        _npz(d / "CHART.npz"), _npz(s4a / f"INIT_CHART_{j}.npz"))
                else:
                    a[f"{j}_init_unavailable"] = ch["c0_cal"]["status"] != "PASS" and \
                        frozen["init_status"].get(str(j)) not in (None, "PASS")
        inputs = {}
        for j in dc.MASTERS:
            inputs[f"X:{j}:-"], inputs[f"X:{j}:+"] = arr[(j, 5000)]["X_minus"], \
                arr[(j, 5000)]["X_plus"]
        j0 = dc.MASTERS[0]
        inputs[f"init:{j0}:-"], inputs[f"init:{j0}:+"] = arr[(j0, 0)]["X_minus"], \
            arr[(j0, 0)]["X_plus"]
        draws = k4b_stats.joint_bootstrap(inputs, kd["seed"])
        c = {}
        for j in dc.MASTERS:
            bd = k4b_stats.bounds(draws[f"X:{j}:-"], draws[f"X:{j}:+"])
            pm = result["per_model"][str(j)]
            c[f"{j}_LU"] = _val(bd["L"]) == _val(pm["L"]) and _val(bd["U"]) == _val(pm["U"])
        bd = k4b_stats.bounds(draws[f"init:{j0}:-"], draws[f"init:{j0}:+"])
        ref = result["controls"]["init"][str(j0)]
        c["init_bounds"] = (_val(bd["L"]) == _val(ref["alpha_bound"])
                            and _val(bd["U"]) == _val(ref["one_minus_alpha_bound"]))
    checks = {"a0": a0, "a": a, "b": b, "c": c}
    flat = list(a0.values()) + list(a.values()) + list(b.values()) + list(c.values())
    return {"status": "PASS" if flat and all(flat) else KNOWN, "checks": checks}


