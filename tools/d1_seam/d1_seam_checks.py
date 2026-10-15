"""D-1 seam check part 2 (D1-FROZEN-v1 + addenda; API.md): G4 float cross-check, G5 Decimal
reference, G6 controls, and run (S0 re-check, mandatory-preflight rule, stop rules, report.json,
model.npz). Imports part 1; part 1 re-exports these names (addendum 2)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from decimal import Decimal, Inexact, localcontext
from fractions import Fraction as Fr
from pathlib import Path

import d1_seam as d
import independent_reference
import numpy as np

from topo_pilot.oracle import BayesFilter, FutureOperator

PLANNING = Path(r"X:\Downloads\projects\topo-pilot\agent-handoff\planning")
_SHA = (
    "68EBD82F9FD8E3C82114ADEF713F3AA9F7283BEBFF7AE38C5FFB266E62E10B21",
    "1EE0291D7AEB071BAE961E963950A75743EF8259DD889C7134E1C886983D2669",
    "2258ED96222B151E5E3F416DA8C66FF1DD0A60303FF0E5A25254328DD69C3F6F",
    "45B0E80152E324D2A0833DC5BC3B75853E1E9FD18B27C152887E41346CEB7528",
)
_FILES = (
    "responses/D1-FROZEN-v1.md",
    "responses/D1-FROZEN-v1.coordinator-addendum.md",
    "responses/D1-FROZEN-v1.coordinator-addendum-2.md",
    "requests/coord-d1-oracle-proof-20261015.md",
)
BOUND = dict(zip(_FILES, _SHA))
BASE_COMMIT = "4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c"
GATES = ("G0", "G0S", "G0O", "G1", "G2", "G3", "G4", "G5", "G6")
TOL = {
    "belief": 1e-12,
    "pi_block": 1e-11,
    "pi_expit": 1e-10,
    "evidence_rel": 1e-10,
    "log_evidence": 1e-10,
    "future": 1e-12,
    "tv": 1e-12,
    "onestep": 1e-12,
    "mixture_future": 1e-12,
    "sums": 1e-12,
}
NS = d.NS


def _f(x):
    return np.array(x, dtype=object).astype(np.float64)


def _row(h):
    r = d.exact_history(h)
    return (h, r["b_C"], r["b_M"], r["pi"], r["P"], r["Q1_C"], r["Q1_M"], r["J_C"], r["J_M"])


def gate_G4(enum):
    """Unchanged BayesFilter/FutureOperator against the exact G2 enumeration and the witnesses."""
    fm = d.float_model()
    flt = {
        k: BayesFilter(*args)
        for k, args in (
            ("X", (fm["T"], fm["E_mix"], fm["mu"])),
            ("C", (fm["T_C"], fm["E"], fm["mu_C"])),
            ("M", (fm["T_M"], fm["E"], fm["mu_M"])),
        )
    }
    fut = {
        "X": FutureOperator(fm["T"], fm["E_mix"]),
        "C": FutureOperator(fm["T_C"], fm["E"]),
        "M": FutureOperator(fm["T_M"], fm["E"]),
    }
    err, bad, named = dict.fromkeys(TOL, 0.0), 0, {}

    def up(key, arr):
        err[key] = max(err[key], float(np.max(np.abs(arr), initial=0.0)))

    groups = [rows for _, rows in sorted(enum["_data"].items())]
    groups += [[_row(h)] for h in (d.H_A, d.H_B, d.H_EDGE)]
    for rows in groups:
        tok = np.array([r[0] for r in rows], dtype=np.int64)
        res = {k: f.run(tok) for k, f in flt.items()}  # raises on IMPOSSIBLE_HISTORY (Lemma B)
        b = {k: res[k].b[:, -1] for k in res}
        exC, exM = _f([r[1] for r in rows]), _f([r[2] for r in rows])
        exX = _f([[(1 - r[3]) * v for v in r[1]] + [r[3] * v for v in r[2]] for r in rows])
        pi, P = _f([r[3] for r in rows]), _f([r[4] for r in rows])
        for got, ex in ((b["X"], exX), (b["C"], exC), (b["M"], exM)):
            up("belief", got - ex)
            up("sums", got.sum(1) - 1)
            bad += int(not (np.isfinite(got).all() and (got >= 0).all()))
        up("pi_block", b["X"][:, NS:].sum(1) - pi)
        up("pi_expit", 1 / (1 + np.exp(res["C"].log_evidence - res["M"].log_evidence)) - pi)
        up("evidence_rel", np.exp(res["X"].log_evidence) / P - 1)
        up("log_evidence", res["X"].log_evidence - np.log(P))
        idx = [i for i, r in enumerate(rows) if len(r) > 5]
        if not idx:
            continue
        ex = [rows[i] for i in idx]
        F1 = {k: fut[k].F1(b[k][idx]) for k in fut}
        F2 = {k: fut[k].F2(b[k][idx]) for k in fut}
        q1C, q1M = _f([r[5] for r in ex]), _f([r[6] for r in ex])
        JC, JM = _f([r[7] for r in ex]), _f([r[8] for r in ex])
        pf = _f([r[3] for r in ex])[:, None]
        mixQ1 = _f([[(1 - r[3]) * x + r[3] * y for x, y in zip(r[5], r[6])] for r in ex])
        mixJ = _f(
            [
                [[(1 - r[3]) * x + r[3] * y for x, y in zip(rc, rm)] for rc, rm in zip(r[7], r[8])]
                for r in ex
            ]
        )
        for got, want in (
            (F1["C"], q1C),
            (F1["M"], q1M),
            (F1["X"], mixQ1),
            (F2["C"], JC),
            (F2["M"], JM),
            (F2["X"], mixJ),
            (F2["C"].sum(1), JC.sum(1)),
            (F2["M"].sum(1), JM.sum(1)),
            (F2["X"].sum(1), mixJ.sum(1)),
        ):
            up("future", got - want)
            bad += int(not (np.isfinite(got).all() and (got >= 0).all()))
        up("mixture_future", F1["X"] - ((1 - pf) * F1["C"] + pf * F1["M"]))
        up("mixture_future", F2["X"] - ((1 - pf[:, :, None]) * F2["C"] + pf[:, :, None] * F2["M"]))
        up("sums", F2["X"].sum((1, 2)) - 1)
        exact_tv = [(d.tv(r[5], r[6]), d.tv(r[7], r[8])) for r in ex]
        up("tv", 0.5 * np.abs(F1["C"] - F1["M"]).sum(1) - _f([t[0] for t in exact_tv]))
        up("tv", 0.5 * np.abs(F2["C"] - F2["M"]).sum((1, 2)) - _f([t[1] for t in exact_tv]))
        hi = [k for k, r in enumerate(ex) if r[0][-1] == d.S3]
        up("onestep", (F1["C"] - F1["M"])[hi])
        if len(rows) == 1:
            named[rows[0][0]] = (F1["C"][0], F1["M"][0], F2["X"][0])
    pair = 0.5 * float(np.abs(named[d.H_A][2] - named[d.H_B][2]).sum())
    edge = 0.5 * float(np.abs(named[d.H_EDGE][0] - named[d.H_EDGE][1]).sum())
    err["tv"] = max(err["tv"], abs(pair - 0.01), abs(edge - 0.1))
    ck = {k: err[k] <= TOL[k] for k in TOL} | {"finite_nonnegative": bad == 0}
    return {
        "status": "PASS" if all(ck.values()) else "FAIL",
        "values": {
            "max_errors": err,
            "tolerances": TOL,
            "pair_tv": pair,
            "edge_tv1": edge,
            "checks": ck,
        },
    }


def _dec(q):
    with localcontext() as ctx:
        ctx.prec, ctx.traps[Inexact] = 100, True
        return Decimal(str(Decimal(q.numerator) / Decimal(q.denominator)))


def gate_G5():
    """job-0014 Decimal reference (digits 80, Decimal inputs from exact strings), 650 histories."""
    m = d.exact_model()
    T, E = ([[_dec(v) for v in r] for r in m[k]] for k in ("T", "E"))
    mu = [_dec(v) for v in m["mu"]]
    hists = list(dict.fromkeys([n[0] for n in d._nodes(m, 5)] + [d.H_A, d.H_B, d.H_EDGE, d.H_MAX]))
    worst, lim = Fr(0), Fr(1, 10**45)
    for h in hists:
        post = [
            Fr(x) for x in independent_reference.decimal_suffix_posterior(T, E, mu, list(h), 80)
        ]
        ex = d.exact_history(h, model=m)["b_mix"]
        worst = max(
            [worst, abs(sum(post[NS:], Fr(0)) - sum(ex[NS:], Fr(0)))]
            + [abs(x - y) for x, y in zip(post, ex)]
        )
    ok = {"count_650": len(hists) == 650, "within_1e-45": worst <= lim}
    return {
        "status": "PASS" if all(ok.values()) else "FAIL",
        "values": {"histories": len(hists), "max_abs_error": worst, "checks": ok},
    }


def gate_G6():
    """Controls N1, N2, N3 (full K = 8 enumerations), L1, L2 and P1 (§5.2 G6)."""
    ck, vals = {}, {}
    for v in ("N1", "N2", "N3"):
        g = d.gate_G2(v)
        vio, D = g["values"]["violations"] | g["values"]["control_counters"], g["values"]["D_t"]
        vals[v] = {"D_t": D, "violations": vio}
        ck[v + "_D_zero"] = all(x == 0 for x in D)
        hA, hB, hs, he = (d.exact_history(h, v) for h in (d.H_A, d.H_B, d.H_STAR, d.H_EDGE))
        if v == "N1":
            m = d.exact_model(v)
            nb = {f: d._nb(m["T_" + f]) for f in "CM"}
            sparse = lambda vec: {i: x for i, x in enumerate(vec) if x}  # noqa: E731
            tv2 = sum(
                int(d._J(sparse(bC), nb["C"], m["E_C"]) != d._J(sparse(bM), nb["M"], m["E_M"]))
                for rows in g["_data"].values()
                for _, bC, bM, *_rest in rows
            )
            vals[v]["tv2_nonzero_all_nodes"] = tv2
            ck["N1"] = (
                vio["pi_not_half"] == 0
                and vio["tv1_nonzero"] == 0
                and tv2 == 0
                and hA["pi"] == hB["pi"] == d.HALF
                and d.tv(hA["J"], hB["J"]) == 0
            )
        if v == "N2":
            ck["N2"] = vio["pi_not_half"] == 0 and vio["tv2_nonzero_HI"] == 0
        if v == "N3":
            inf = d.exact_history((d.A, d.A, d.S2, d.S3, d.S0, d.A), v)
            vals[v]["informed_ratio_PC_PM"] = inf["P_C"] / inf["P_M"]
            ck["N3"] = (
                d.tv(hs["J_C"], hs["J_M"]) == 0
                and hA["pi"] == hB["pi"] == d.HALF
                and d.tv(hA["J"], hB["J"]) == 0
                and d.tv(he["Q1_C"], he["Q1_M"]) == 0
                and vio["thmCa"] == 0
            )
        del g
    worlds, mL1 = d.build_worlds(), d.exact_model("L1")
    g0 = d.gate_G0(worlds, E_mix=np.array([[float(x) for x in r] for r in mL1["E"]]))
    leak = d.exact_history((d.A,), "L1")
    vals["L1"] = {
        "E_blocks_check": g0["values"]["checks"]["E_blocks"],
        "pi_A": leak["pi"],
        "thmCa_violations_K1": d.gate_G2("L1", K=1)["values"]["violations"]["thmCa"],
    }
    ck["L1"] = (
        not vals["L1"]["E_blocks_check"]
        and leak["pi"] == Fr(1, 4)
        and vals["L1"]["thmCa_violations_K1"] > 0
    )
    mL2 = d.exact_model("L2")
    rows = [d._q1({d.st(3, y): Fr(1)}, d._nb(mL2["T_C"]), mL2["E_C"]) for y in (0, 2)]
    g1 = d.gate_G1("L2")["values"]["checks"]
    vals["L2"] = {"row_3_0": rows[0], "row_3_2": rows[1], "thmA_rows_check": g1["C_thmA_rows"]}
    ck["L2"] = rows[0] != rows[1] and not g1["C_thmA_rows"] and not g1["M_thmA_rows"]
    he = d.exact_history(d.H_EDGE)
    vals["P1"] = {"h_edge_tv1": d.tv(he["Q1_C"], he["Q1_M"])}
    ck["P1"] = vals["P1"]["h_edge_tv1"] == Fr(1, 10)
    return {"status": "PASS" if all(ck.values()) else "FAIL", "values": dict(vals, checks=ck)}


def _git(*args):
    out = subprocess.run(["git", "-C", str(d.REPO), *args], capture_output=True, text=True)
    return out.returncode, out.stdout.strip()


def s0_check():
    got = {p: hashlib.sha256((PLANNING / p).read_bytes()).hexdigest().upper() for p in BOUND}
    code, diff = _git(
        "diff", BASE_COMMIT, "HEAD", "--", "src", "tools/x4_oracle_profile", "tests/oracle_profile"
    )
    return {
        "hashes_ok": got == BOUND,
        "kernel_diff_empty": code == 0 and diff == "",
        "head": _git("rev-parse", "HEAD")[1],
        "hashes": got,
    }


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items() if k != "_data"}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (Fr, Decimal)):
        return str(x)
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    return x.tolist() if isinstance(x, np.ndarray) else x


def run(out_dir, preflight):
    """Mandatory preflight, S0, then G0..G6 in order; stop at the first FAIL or INVALID."""
    out, t0 = Path(out_dir), time.process_time()
    out.mkdir(parents=True, exist_ok=True)
    rep = {
        "protocol": "D1-FROZEN-v1 (+ addenda 1, 2)",
        "verdict": "PASS",
        "first_failed": None,
        "gates": {g: {"status": "NOT_RUN"} for g in GATES},
        "preflight": dict(preflight),
        "S0": s0_check(),
    }
    if not preflight or not all(preflight.values()):
        rep.update(verdict="INVALID", reason="mandatory preflight failed or missing")
    elif not (rep["S0"]["hashes_ok"] and rep["S0"]["kernel_diff_empty"]):
        rep.update(verdict="INVALID", reason="S0: protocol/request hash or kernel diff mismatch")
    else:
        state = {}
        calls = {
            "G0": lambda: d.gate_G0(state["w"]),
            "G0S": lambda: d.gate_G0S(state["w"]),
            "G0O": lambda: d.gate_G0O(state["w"]),
            "G1": d.gate_G1,
            "G2": d.gate_G2,
            "G3": d.gate_G3,
            "G4": lambda: gate_G4(state["G2"]),
            "G5": gate_G5,
            "G6": gate_G6,
        }
        for g in GATES:
            try:
                if g == "G0":
                    state["w"] = d.build_worlds()  # S2: any builder/validation exception -> INVALID
                res = state[g] = calls[g]()
            except Exception as exc:  # noqa: BLE001  inability to evaluate a gate -> INVALID
                rep["gates"][g] = {"status": "INVALID", "error": repr(exc)}
                rep.update(verdict="INVALID", first_failed=g)
                break
            rep["gates"][g] = {k: v for k, v in res.items() if k != "_data"}
            if res["status"] != "PASS":
                rep.update(verdict="FAIL", first_failed=g)
                break
        if "w" in state:
            fm = d.float_model(state["w"])
            arrays = {k: fm[k] for k in ("T_C", "T_M", "E", "mu")}
            np.savez(out / "model.npz", **arrays)
            rep["model_sha256"] = {
                k: hashlib.sha256(v.tobytes()).hexdigest() for k, v in arrays.items()
            }
    rep["cpu_s"] = time.process_time() - t0
    rep = _jsonable(rep)
    (out / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True), encoding="utf-8")
    return rep


if __name__ == "__main__":
    args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
    pre = json.loads(Path(args["--preflight"]).read_text(encoding="utf-8"))
    print(json.dumps(run(Path(args["--out"]), pre)["verdict"]))
