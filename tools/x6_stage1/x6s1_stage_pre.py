"""X6S1 stage content of E0 and E0b (ruling R-0079-1): AUTH-ADMIT, S0, REG1 and the non-test
pools, PF, G0-ORC (a)-(g), SCORE, G0-POS, REG2 with the test draw and SEP, G0-FEAS, HEADROOM-D,
CLOUD-PREP and SMOKE-INGEST (X6S1-FROZEN-v1 §4.6, §5.3, §5.9, §6, §8 rows 0b-12, §12 item 11;
API.md §13 items 27-29). Each gate is fn(ctx) -> {"status", "values"}, run in PLAN order by
x6s1_run.run_stage. Import performs no I/O beyond the imported modules' own (§13 item 24)."""
# fmt: off

from __future__ import annotations

import io
import json
import math
import os
import subprocess
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import x6s1_data as sd  # first: its import applies the API §1 sys.path convention

# isort: split
import numpy as np
import torch
import x6_dp as xd
import x6_exact as xe
import x6_model as xm
import x6_run as xr
import x6s1_cloud as sc
import x6s1_eval as se
import x6s1_ingest as si
import x6s1_pairs as sp
import x6s1_registry as sg
import x6s1_run as sr
import x6s1_stats as ss

from topo_pilot.contracts import ArtifactStore, ObservationSet, SeedTree
from topo_pilot.contracts.backends import LocalFSBackend

T6, FLOOR_MAX = Fraction(1, 10**40), sd.FLOOR + sd.FLOOR_SLACK
SUITES = tuple(f"tests/{d}" for d in (
    "learner", "dataset", "contracts", "oracle", "oracle_profile", "world", "process", "x6_stage0",
    "d2a", "k4b", "c1prime_registry", "x6_stage1"))
BIG = tuple(f"tools/x6_stage1/x6s1_{m}.py" for m in (
    "cloud", "registry", "ingest", "run", "stage_pre", "stage_post", "eval"))  # R-0082-0, R-0084-0
LADDER_G = (("q_empty", "G_empty_32"), ("q_parity", "G_parity_32"), ("q_counts", "G_counts_32"),
            ("q_H1", "G_H1_32"), ("q_Parikh", "G_Parikh_32"), ("q_8", "G_8_32"))


def _r(ok, values=None, bad="FAIL") -> dict:
    return {"status": "PASS" if ok else bad, "values": values}
def _ok(v) -> bool:  # every boolean leaf of a nested record is true
    if isinstance(v, dict):
        return all(_ok(x) for x in v.values())
    return bool(v) if isinstance(v, (bool, np.bool_)) else True
def _scratch(ctx) -> Path: return Path(sd.SCRATCH_ROOT) / str(ctx["dispatch"]["job"])
def _e0(store, *rel) -> Path:  # an E0 payload path under stages/E0/ (written by exclusive create)
    p = Path(store).joinpath("stages", "E0", *rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
def _tok(ctx, name) -> np.ndarray: return ctx["obs"][name].tokens

# ---- pools: pools/ is the ArtifactStore of the 35 ObservationSets + POOLS.json (§12 item 1) ----
def ostore(store) -> ArtifactStore:
    return ArtifactStore(LocalFSBackend(Path(store) / "pools"), producer_version="x6s1")
def pools_index(store) -> dict: return json.loads((Path(store) / "pools/POOLS.json").read_bytes())
def load_obs(store, name) -> ObservationSet:
    rec = pools_index(store)[name]
    obs = ostore(store).load(ObservationSet, rec["artifact_id"], consumer="experiment")
    if sd.token_digest(obs.tokens) != rec["token_sha256"]:
        raise ValueError(f"pool {name}: the token digest differs from POOLS.json")
    return obs
def _draw(ctx, specs) -> None:
    """Each pool once from its registered stream (§6.1); train and smoke also as the .npy bundle
    sources pools/npy/<name>.npy (§5.3)."""
    store, recs = Path(ctx["store"]), ctx.setdefault("pools", {})
    for spec in specs:
        tok, seeds = sd.sample_pool(spec), SeedTree(sd.DATA_MASTER)
        seed, obs = seeds.seed(*spec["stream"]), sd.observation_set(spec, tok)
        ctx.setdefault("obs", {})[spec["name"]] = obs
        cfg = {"x6s1_pool": spec["name"], "master": sd.DATA_MASTER, "stream": list(spec["stream"]),
               "code": spec["code"]}
        aid = ostore(store).save(obs, config=cfg, parents=[], seed_map=dict(seeds.issued),
                                 consumer="experiment")
        rec = recs[spec["name"]] = {"artifact_id": aid, "token_sha256": sd.token_digest(tok),
                                    "n_rows": len(tok), "data_seed": seed, "split": spec["split"]}
        if spec["pool"] in ("train", "smoke"):
            (p := store / "pools" / "npy" / f"{spec['name']}.npy").parent.mkdir(exist_ok=True)
            rec.update(npy=p.relative_to(store).as_posix(), file_sha256=sd.save_pool(p, tok))

# ---- AUTH-ADMIT, S0, REG1 and the non-test pools (§8 rows 0b, 1, 6; §6.4) ----
def auth_admit(ctx) -> dict:
    return _r(sr.auth_ok(ctx["store"], sd.PROTOCOL_SHA256), {"AUTH.json": "present"}, "INVALID")
def _s0_dispatch(ctx) -> dict:
    """E0 only (D-0087-2, R-0087-3; API.md §13 item 39): a GATES.jsonl holding exactly this
    run's one AUTH-ADMIT record is an accepted output of S0 (viii); else the dispatch as given."""
    disp, p = ctx["dispatch"], Path(ctx["store"]) / "GATES.jsonl"
    if ctx["stage"] != "E0" or not p.is_file():
        return disp
    try:
        recs = [json.loads(x) for x in p.read_bytes().splitlines() if x.strip()]
    except ValueError:
        return disp
    if len(recs) != 1 or not isinstance(recs[0], dict) or recs[0].get("gate") != "AUTH-ADMIT":
        return disp
    acc = {**(disp.get("accepted_outputs") or {}), "GATES.jsonl": sc.sha256_file(p)}
    return {**disp, "accepted_outputs": acc}  # a new dict: the caller's dispatch is unchanged
def s0(ctx) -> dict:
    out = sr.s0_check(sr.REPO, ctx["head"], ctx["store"], _s0_dispatch(ctx),
                      Path(ctx["store"]) / "FREEZE.json")
    return {"status": out["status"], "values": out}
def _man(m) -> dict: return {k: m[k] for k in ("version", "n", "digest_sha256", "collision_mass")}
def reg1(ctx) -> dict:
    """REG1 from its four sources (the inventory over the dispatch's X6 scratch roots), then the
    32 non-test pools (the pool-construction order of §8)."""
    disp = ctx["dispatch"]
    if not disp.get("x6_scratch_roots"):
        return {"status": sg.INCOMPLETE, "values": {"error": "the dispatch names no scratch roots"}}
    inv = sg.inventory_x6(sd.PROJECT_ROOT, disp["x6_scratch_roots"], disp.get("registered", {}))
    src = {"stage0": sg.stage0_rows(), "handoff": sg.handoff_rows(), "inventory": inv,
           "foreign": sg.foreign_sources()}
    v = {"stage0": {k: src["stage0"][k] for k in ("status", "counts")},
         "inventory": {k: src["inventory"][k] for k in ("status", "unclassified", "foreign")},
         "handoff": {"status": src["handoff"]["status"], "n": len(src["handoff"]["rows"]),
                     "failures": src["handoff"]["failures"]},
         "foreign": {k: src["foreign"].get(k) for k in ("status", "summary", "kreg2", "reason")}}
    try:
        ctx["reg1"] = sg.build_reg1(ctx["store"], src)
    except sg.RegistryError as exc:  # S3R: the registry status is the REG gate's
        return {"status": exc.status, "values": {**v, "error": str(exc)}}
    _draw(ctx, sd.NONTEST_POOLS)
    return _r(True, {**v, "reg1": _man(ctx["reg1"])})

# ---- PF (§8 row 2; §4.6) ----
def _run(ctx, name, args, env) -> subprocess.CompletedProcess:
    r = subprocess.run([sys.executable, "-s", *map(str, args)], cwd=sr.REPO, env=env,
                       capture_output=True, text=True)
    (log := Path(ctx["store"]) / "logs" / f"pf_{name}_{sc.utc_stamp()}.txt").parent.mkdir(
        exist_ok=True)
    with open(log, "x", encoding="utf-8") as fh:
        fh.write(r.stdout + r.stderr)
    return r
def sizes_ok(report) -> bool:
    """check_file_sizes lists no X6S1 file but the seven big modules (§13 items 28, 32, 37)."""
    lim = {p: 600 if p.endswith("x6s1_run.py") else 560 for p in BIG}  # run: addendum 5
    rows = [ln.split(": ") for ln in report.splitlines() if "x6_stage1/" in ln]
    return all(r[0] in lim and int(r[1].split()[0]) <= lim[r[0]] for r in rows)
def pf(ctx) -> dict:
    """The unchanged suites and tests/x6_stage1, the size and import checks, NB-STATIC,
    TRAIN-EQUIV and RUNTIME-ACCT on the stored smoke pool; TEMP and basetemp in scratch."""
    scr = _scratch(ctx)
    (tmp := scr / "tmp").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TEMP=str(tmp), TMP=str(tmp), TMPDIR=str(tmp),
               PYTHONPATH=str(sr.REPO / "src"))
    bt, rec = scr / "pf-basetemp", ctx["pools"]["smoke"]
    suites = _run(ctx, "suites", ["-m", "pytest", "-p", "no:cacheprovider", "--basetemp", bt, "-q",
                                  *SUITES], env)
    sizes = _run(ctx, "sizes", [sr.REPO / "tools" / "check_file_sizes.py"], env)
    imports = _run(ctx, "imports", [sr.REPO / "tools" / "check_imports.py"], env)
    smoke = {"path": Path(ctx["store"]) / rec["npy"], "file_sha256": rec["file_sha256"],
             "data_seed": rec["data_seed"]}
    v = {"suites": suites.returncode == 0, "file_sizes": sizes_ok(sizes.stdout),
         "imports": imports.returncode == 0, "NB-STATIC": sr.nb_static(sr.REPO / sr.NB_REL),
         "TRAIN-EQUIV": sr.train_equiv(scr / "pf", smoke),
         "RUNTIME-ACCT": sr.runtime_acct(scr / "pf", smoke)}
    ok = _ok(v) and all(v[k]["status"] == "PASS" for k in ("NB-STATIC", "TRAIN-EQUIV",
                                                           "RUNTIME-ACCT"))
    return _r(ok, {**v, "file_size_report": sizes.stdout.splitlines(), "TEMP": str(tmp),
                   "basetemp": str(bt)}, "INVALID")

# ---- G0-ORC (§8 row 3; S2) ----
def _pairs(ctx, pool) -> dict:
    """The t = 32 partners of `pool` (§2.3) with q* of both members and den = ||Δq*_c||²."""
    tok = _tok(ctx, pool)
    P = sp.partners(sp.class_tables("NA"), tok, 32, pool)
    h, h2 = tok[P["rows"]], P["tokens"]
    q, q2 = se.qstar("NA", h, 32)[0], se.qstar("NA", h2, 32)[0]
    return {**P, "h": h, "q": q, "q2": q2, "den": se.pair_terms(q, q2, q, q2)[1]}
def _t6(enc, name) -> bool:  # T6: a rebuilt enclosure equals the stage-0 one within 1e-40
    c = sd.CONST_MAP[name]
    return all(abs(Fraction(str(enc[k])) - Fraction(c[k])) <= T6 for k in ("lo", "hi"))
def _partner_ok(h, h2) -> bool:  # (d): X6-valid, the same rs_key("Parikh"), and P(h') = P(h)
    h, h2 = tuple(int(w) for w in h[:32]), tuple(int(w) for w in h2[:32])
    try:
        return xe.rs_key("Parikh", h) == xe.rs_key("Parikh", h2) and (
            xm.closed_form("NA", h)["P"] == xm.closed_form("NA", h2)["P"])
    except ValueError:
        return False
def _model_arrays(report) -> dict:  # (a): the arrays of NA, AB, ZC = stage-0's model_sha256
    arr = {"T_base": xm.to_float(xm.t_base_exact()), "E": xm.to_float(xm.emission("E")),
           **{f"T_lift_{a}": xm.model(a)["Tf"] for a in sd.ARMS}}
    return {k: sc.sha256_bytes(np.ascontiguousarray(a).tobytes()) == report["model_sha256"][k]
            for k, a in arr.items()}
def _designed(ctx, report) -> dict:
    """(f) on D: fraction_filter = closed_form at every designed readout, prefix invariance of
    q*, W2 cue TV = λ_18, control-set spread 0 and the W2 β table = stage 0's (all exact)."""
    D, m, q, ff = ctx["D"], xm.model("NA"), {}, True
    for h in [p[k] for f in sp.PAIR_FAMILIES for p in D[f] for k in "ab"] + D["W3"] + D["W3p"]:
        q[h] = tuple(xm.closed_form("NA", h)["q"])
        ff &= tuple(xe.fraction_filter(m["T"], m["E"], m["pi"], h)["q"][-1]) == q[h]
    groups: dict = {}
    for f in sp.PAIR_FAMILIES:
        for p in D[f]:
            for k in "ab":
                groups.setdefault((f, k, p["y"]), set()).add(q[p[k]])
    bt, rep = xe.beta_table()["W2"], report["exact"]["G3"]["beta"]["W2"]
    inv = all(len(x) == 1 for x in groups.values())
    return {"fraction_filter": bool(ff), "prefix_invariance": inv,
            "W2_tv": all(xe._cue_tv(q[p["a"]], q[p["b"]]) == xm.lam(18) for p in D["W2"]),
            "control_spread": all(q[p["a"]] == q[p["b"]] for c in sp.CONTROL_SETS for p in D[c]),
            "W2_beta": all(bt[k]["pooled"] == Fraction(rep[k]["pooled"]["value"]) and list(
                bt[k]["per_y"]) == [Fraction(x["value"]) for x in rep[k]["per_y"]] for k in rep)}
def g0_orc(ctx) -> dict:
    """(a)-(g); persists tables/class_tables_NA.json and tables/designed.npz (D frozen in E0)."""
    store, g = Path(ctx["store"]), {a: _tok(ctx, f"gate_{a}") for a in sd.ARMS}
    report = json.loads((Path(sd.STAGE0_STORE) / "run" / "report.json").read_bytes())
    (store / "tables").mkdir(exist_ok=True)
    tables, nat, gaps = sp.class_tables("NA"), xd.natural("NA"), sp.gap_enclosures()
    tsha = sp.save_tables(store / "tables" / "class_tables_NA.json", tables)
    D = ctx["D"] = sp.designed_set(_tok(ctx, "prefix"))
    A = sp.designed_arrays(D)
    dsha = {"designed_sha256": sp.designed_sha256(A),
            "file_sha256": se._npz(store / "tables" / "designed.npz", A)}
    pr = ctx["pairs_gate"] = _pairs(ctx, "gate_NA")
    par, q8 = (se.OraclePredictor("NA", k) for k in ("q_Parikh", "q_8"))
    num_par = se.pair_terms(par(pr["h"], 32), par(pr["tokens"], 32), pr["q"], pr["q2"])[0]
    d8 = float(np.max(np.abs(q8(pr["h"], 32) - q8(pr["tokens"], 32)), initial=0.0))
    v = {"a": _model_arrays(report),
         "b": {a: bool(xr._filter_check(a, g[a])["pass"]) for a in sd.ARMS},
         "c": {"G_Parikh_32": _t6(nat["G"]["Parikh"][32], "G_Parikh_32"), "tables_sha256": tsha},
         "d": {"exhaustive": sp.exhaustive_check(6)["status"] == "PASS",
               "totals": sp.validate_tables(tables)["status"] == "PASS",
               "partners": all(_partner_ok(a, b) for a, b in zip(pr["h"], pr["tokens"]))},
         "e": {"beta_qstar": abs(se.beta_fsum(pr["den"], pr["den"]) - 1) <= 1e-12,
               "beta_qParikh": not np.any(num_par), "dq8": d8 <= 1e-12},
         "f": _designed(ctx, report),
         "g": {"G_8_32": _t6(nat["G_k"][8][32], "G_8_32"), **{
             n: abs(Fraction(e["v80"]) - Fraction(sd.CONST_MAP[n]["value"])) <= T6
             for n, e in gaps.items()}}}
    return _r(_ok(v), {**v, "designed": dsha, "gate_pairs": len(pr["rows"]), "dq8_max": d8,
                       "lo": {n: e["lo"] for n, e in gaps.items()}})  # Δ_W2^lo, Δ_W3^lo

# ---- SCORE and G0-POS (§8 rows 4-5; §7.4; T13-T18) ----
def _quantiser(laws) -> dict:
    k, f = se.quantise(laws), np.floor(laws * sd.Q)
    R, u = sd.Q - f.sum(1), np.floor(sd.Q / 18)  # ties: 1/18 everywhere gives R = 4 on 0..3
    try:
        se.quantise(np.full((1, 18), 1 / 17))
        refused = False
    except se.QuantInvalid:
        refused = True
    return {"conservation": bool((k.sum(1) == sd.Q).all()), "zero_rule": bool((k[laws == 0] == 0)
            .all()), "R_range": bool(((R >= 0) & (R <= 18)).all()), "positivity": bool(
            (se.readout(k[:64]) >= float(sd.EPS) / 18).all()), "QUANT_INVALID": refused,
            "ties": se.quantise(np.full((1, 18), 1 / 18))[0].tolist() == [u + 1] * 4 + [u] * 14}
def score(ctx) -> dict:
    """Quantiser on synthetic and gate laws, the certified tables (tables/log_tables.npz), the
    per-row scoring error on 2^14 gate rows with q_empty, the oracle-readout floor and the EB
    self-test (SCORING_INVALID → CONSTRUCTION_FAIL, S2)."""
    t = ctx["tables"] = ss.log_tables()
    fsha = se._npz(Path(ctx["store"]) / "tables" / "log_tables.npz",
                   {k: np.asarray(t[k]) for k in ("lnp", "qlnq", "fl_q", "qvals")})
    g, n = _tok(ctx, "gate_NA"), 2**14
    q, codes = ctx["qstar_gate"] = se.qstar("NA", g, 32)
    syn = np.zeros((3, 18))
    syn[0, 0], syn[1], syn[2, :2] = 1.0, 1 / 18, 0.5
    floor = ctx["floor"] = float(np.max(se.score(codes, se.quantise(q), t)))
    ke = se.quantise(se.OraclePredictor("NA", "q_empty")(g[:n], 32))
    xh = se.score(codes[:n], ke, t)
    err = max(abs(Decimal(float(x)) - ss.decimal_kl(sp.q_exact("NA", r, 32), se.readout_exact(k)))
              for x, r, k in zip(xh, g[:n], ke))
    xp, zp = ss.outward_inputs(xh)
    eb = {str(d): ss.eb_bound(xp, zp, n, d) - ss.eb_reference(xp, zp, n, d)
          for d in (sd.DELTA_LEARN, sd.DELTA_SHARP)}
    v = {"quantiser": {"synthetic": _quantiser(syn), "gate": _quantiser(q)},
         "tables": {"sha256": t["sha256"], "file_sha256": fsha, "max_diag": t["max_diag"]},
         "e_row": {"max": str(err), "ok": err <= Decimal("1e-13")},
         "floor": {"max": floor, "ok": Fraction(floor) <= FLOOR_MAX},
         "eb": {"outward_minus_reference": {d: str(x) for d, x in eb.items()},
                "ok": all(0 <= x <= Decimal("1e-50") for x in eb.values())}}
    return _r(_ok(v), v)
def g0_pos(ctx) -> dict:
    """On gate(NA) 2^16: (a) the readout floor per row; (b) raw Δ_nat(q_S) vs G_S(32) within
    4·SE + 2e-12; (c) Δ^Q − Δ^raw within the row-mean exact quantisation bounds + 2e-12 (T18)."""
    g, (q, codes), t = _tok(ctx, "gate_NA"), ctx["qstar_gate"], ctx["tables"]
    v, pos, eps, Q, n = {"a": Fraction(ctx["floor"]) <= FLOOR_MAX}, q > 0, float(sd.EPS), sd.Q, len(
        q)
    for kind, name in LADDER_G:
        p = se.OraclePredictor("NA", kind)(g, 32)
        raw, xq = se.kl_rows(q, p), se.score(codes, se.quantise(p), t)
        G, m = float(Fraction(sd.CONST_MAP[name]["lo"])), math.fsum(raw) / n
        sem = float(np.std(raw, ddof=1)) / math.sqrt(n)
        with np.errstate(divide="ignore", invalid="ignore"):
            lo = np.where(pos, -q * (1 / Q + eps / 18) / p, 0.0).sum(1)
            hi = np.where(pos, q * (-math.log1p(-eps) - np.log1p(-1 / (Q * p))), 0.0).sum(1)
        a_lo, a_hi, d = math.fsum(lo) / n, math.fsum(hi) / n, math.fsum(xq - raw) / n
        v[kind] = {"mean_raw": m, "se": sem, "b": abs(m - G) <= 4 * sem + 2e-12, "dQ": d,
                   "A": [a_lo, a_hi], "c": a_lo - 2e-12 <= d <= a_hi + 2e-12}
    return _r(_ok(v), v)

# ---- REG: REG2, the test draw and SEP (§6.4-§6.5; S3R) ----
def reg2_sep(ctx) -> dict:
    """REG2 and the test draw inside the reservation window, POOLS.json, SEP on every row; ρ̄.
    The separation record is persisted (stages/E0/separation.json), released by status."""
    store, t0 = Path(ctx["store"]), sc.utc_iso()
    try:
        reg2 = sg.build_reg2(store, ctx["reg1"], dict(ctx["obs"]))
        _draw(ctx, sd.TEST_POOLS)
        window = {"start": t0, "end": sc.utc_iso()}
        psha = si._xwrite(store / "pools" / "POOLS.json", sr._cj(ctx["pools"]))
        sep = sg.separation(sg.open_reg(store, "X6-REG2", reg2), ctx["obs"])
    except sg.RegistryError as exc:
        return {"status": exc.status, "values": {"error": str(exc)}}
    return {"status": sep["status"], "values": {
        "reg2": _man(reg2), "rho_bar": reg2["collision_mass"], "reservation_window": window,
        "POOLS.json": psha, "separation.json": se._json(_e0(store, "separation.json"), sep)}}

# ---- G0-FEAS and HEADROOM-D (§8 rows 7-8; oracle only) ----
def g0_feas(ctx) -> dict:
    """(a)-(d) (FEASIBILITY_NO_GO, S3). The test partners (t = 32) are drawn and persisted: test(NA)
    with den and the informative flags, test(AB), test(ZC) for the §2.8 own-process spread; test-
    derived numbers are released only as PASS/FAIL (§12 item 11). FEAS-POWER: one fair registered
    coin per val(NA) row; the full-row bootstrap."""
    te, va, D = _pairs(ctx, "test_NA"), _pairs(ctx, "val_NA"), ctx["D"]
    nv = len(_tok(ctx, "val_NA"))
    inf = te["den"] > 0
    psha = se._npz(_e0(ctx["store"], "partners_test_NA_t32.npz"), {
        "rows": te["rows"], "tokens": te["tokens"], "den": te["den"], "informative": inf})
    osha = {a: se._npz(_e0(ctx["store"], f"partners_test_{a}_t32.npz"), sp.partners(  # R-0082-2
        sp.class_tables("NA"), _tok(ctx, f"test_{a}"), 32, f"test_{a}")) for a in ("AB", "ZC")}
    coin = SeedTree(sd.DATA_MASTER).generator("x6s1", "feas").integers(0, 2, size=nv)[va["rows"]]
    par = se.OraclePredictor("NA", "q_Parikh")
    num = np.where(coin == 1, va["den"], se.pair_terms(par(va["h"], 32), par(va["tokens"], 32),
                                                       va["q"], va["q2"])[0])
    keep = va["den"] > 0
    ns, ds = ss.cord_draws(num[keep][None], va["den"][keep], nv, sd.B_MODEL, ss.boot_stream("feas"))
    fse = float(np.std(ns[:, 0] / ds, ddof=1))
    v = {"a": bool(inf.sum() >= sd.FEAS_PAIRS),
         "b": bool(te["den"].sum() > 0 and va["den"].sum() > 0),
         "c": {"se": fse, "ok": fse <= sd.FEAS_SE},
         "d": {"prefixes": len(D["prefixes"]) == 1030, "W2": len(D["W2"]) == 3090, "W3": len(
             D["W3"]) == 72, "controls": sum(len(D[c]) for c in sp.CONTROL_SETS) == 12360}}
    return _r(_ok(v), {**v, "partners_sha256": psha, "own_partners_sha256": osha})
def headroom(ctx) -> dict:
    """β_8 and mean ||d||² over all val(NA) rows (oracle only; se.gamma, R-0081-1: rows where q*
    has no cue mass contribute 0) → sealed/headroom.json (§2.8; API.md §13 item 30)."""
    r = se.gamma(se.OraclePredictor("NA", "q_Parikh"), _tok(ctx, "val_NA"))
    sha = sr.seal(ctx["store"], "headroom.json", {k: r[k] for k in ("beta_8", "d2_mean", "rows")})
    return _r(True, {"sealed": {"headroom.json": sha}})

# ---- CLOUD-PREP (§8 row 9; §5.3) ----
def cloud_prep(ctx) -> dict:
    """init(1..4) and the smoke init (stages/E0/init/) with digests; bundles C0, C1, C2 (tickets
    with every chunk's expected digests; allowed classes); stages/E0/frozen_<wave>.json."""
    store, head, recs, inits, pools, out = Path(ctx["store"]), str(ctx["head"]).lower(), ctx[
        "pools"], {}, {}, {}
    for m in ("SMOKE",) + sd.MODELS:
        key = "smoke" if m == "SMOKE" else f"s{sd.parse_model(m)[1]}"
        if not (p := _e0(store, "init", f"init_{key}.pt")).exists():
            torch.save(sd.init_state(m if m == "SMOKE" else f"init-{key}"), buf := io.BytesIO())
            si._xwrite(p, buf.getvalue())
        inits[m] = {"path": p, "file_sha256": sc.sha256_file(p), "weights_sha256": si._weights(p)}
        r = recs["smoke" if m == "SMOKE" else f"train_{m.replace('-', '_')}"]
        pools[m] = {"path": store / r["npy"], **{k: r[k] for k in (
            "file_sha256", "token_sha256", "n_rows", "data_seed")}}
    for w in ("C0", "C1", "C2"):
        b = si.build_bundle(w, _scratch(ctx) / "cloud_bundle", head, sr.REPO, pools, inits,
                            sr.REPO / sr.NB_REL)
        ticket = json.loads((tp := Path(b["bundle_dir"]) / f"ticket_{w}.json").read_bytes())
        fz = {"code_commit": head, "protocol_sha256": sd.PROTOCOL_SHA256, "ticket": ticket,
              "bundle_sha256": b["bundle_sha256"], "ticket_sha256": sc.sha256_file(tp),
              "steps": ticket["steps"], "K": ticket["K"], "bundle_id": b["bundle_id"],
              "bundle_dir": b["bundle_dir"]}
        out[w] = {"bundle_id": b["bundle_id"], "bundle_sha256": b["bundle_sha256"],
                  "frozen_sha256": se._json(_e0(store, f"frozen_{w}.json"), fz)}
    keep = ("file_sha256", "weights_sha256")
    return _r(True, {"bundles": out, "inits": {m: {k: i[k] for k in keep} for m, i in inits.items()
                                                }})

# ---- E0b: SMOKE-INGEST (§8 row 12; §5.9) ----
def frozen(store, wave) -> dict: return json.loads(_e0(store, f"frozen_{wave}.json").read_bytes())
def local_digests(fz) -> dict:  # the ingest `local` of a wave from its frozen ticket (B1)
    return {e["model"]: {k: e[k] for k in ("data_sha256", "token_sha256", "init_weights_sha256",
                                           "expected")} for e in fz["ticket"]["models"]}
def _replay(d, chain, toks):
    """Descriptive (§5.9): 100 local CPU updates from the GPU step-100 checkpoint against the GPU
    step-200 weights (maximum absolute difference); never a gate."""
    try:
        by, k = {r["step"]: d / r["file"] for r in chain}, sd.K_SMOKE
        st = sc.restore_state(sc.load_checkpoint(by[k], "cpu"), sd.MODEL_CFG, sd.SMOKE_CFG,
                              torch.device("cpu"))
        x, y = sc.materialise(toks)
        sc.train_chunk(st, x, y, sc.draw_indices(st.gen, len(toks), k, sd.SMOKE_CFG.batch_size))
        gpu = torch.load(by[2 * k], map_location="cpu", weights_only=True)["model"]
        return max(float((st.model.state_dict()[k] - w).abs().max()) for k, w in gpu.items())
    except Exception as exc:  # noqa: BLE001  (descriptive only)
        return f"{type(exc).__name__}: {exc}"
def smoke_ingest(ctx) -> dict:
    """The four integrity gates on the smoke, the float64 forward (t = 32) on 1,024 smoke rows,
    the resumed 3-record chain, the session records; the owner's runbook report (dispatch
    "runbook") and the CPU replay are recorded. Dispatch: "snapshot", "manifest_sha256",
    "downloads" (default 1). Any failure is INVALID (S1); TRANSFER_RETRY or HOLD:* is HOLD."""
    store, d = Path(ctx["store"]), ctx["dispatch"]
    fz, snap = frozen(store, "C0"), Path(d["snapshot"])
    res = si.ingest(snap, d["manifest_sha256"], "C0", store, local_digests(fz), fz,
                    redownload_ok=int(d.get("downloads", 1)) < 3)["SMOKE"]
    v = {"ingest": res, "runbook": d.get("runbook")}
    if res["status"] != "DONE":
        return {"status": "HOLD" if res["status"].startswith(("TRANSFER", "HOLD")) else "INVALID",
                "values": v}
    se.set_threads()
    md, e, _ = si._store_chain(store, "SMOKE")
    ver, prec = si.verify_admitted(store, "SMOKE"), pools_index(store)["smoke"]
    toks = sd.load_pool(store / prec["npy"], prec["file_sha256"])
    sr.log_evaluation(store, "SMOKE", "smoke_forward", "E0b")
    p = se.ModelPredictor(ver["path"], ver["file_sha256"], ver["weights_sha256"])(
        toks[:sd.N_SMOKE_EVAL], 32)
    v["checks"] = {"admitted": ver["status"] == "PASS", "forward": bool(
        np.isfinite(p).all() and (p >= 0).all() and (np.abs(p.sum(1) - 1) <= sd.SUM_TOL).all()),
        "resume": fz["ticket"]["smoke_resume"] is True and [r["step"] for r in e["chain"]] == [
            0, sd.K_SMOKE, sd.SMOKE_CFG.steps],
        "sessions": {k: any((snap / "sessions").glob(f"*.{k}.json")) for k in ("start", "final")}}
    sr.log_evaluation(store, "SMOKE", "cpu_replay", "E0b")
    v["replay_max_abs"] = _replay(md, e["chain"], toks)
    return _r(_ok(v["checks"]), v, "INVALID")

PLAN = {"E0": (("AUTH-ADMIT", auth_admit, True), ("S0", s0, True), ("REG/1", reg1, True),
               ("PF", pf, True), ("G0-ORC", g0_orc, True), ("SCORE", score, True),
               ("G0-POS", g0_pos, True), ("REG", reg2_sep, True), ("G0-FEAS", g0_feas, True),
               ("HEADROOM-D", headroom, False), ("CLOUD-PREP", cloud_prep, True)),
        "E0b": (("S0", s0, True), ("SMOKE-INGEST", smoke_ingest, True))}
