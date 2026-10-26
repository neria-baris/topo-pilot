"""X6ZC core: constants and bindings, fresh prefixes and loop-sign variants, exact geometry (K0)
and the q*_NA cache, synthetic predictors, pair terms and K1-K3/F1, the paired cluster bootstrap,
ratio intervals, B9 sizing, the §9 decision, qualifiers, licences and the reuse verdict
(X6ZC-DESIGN-v1; API.md §3-§9, §20). Import reads CONTRACT.json and the protocol bytes only."""
# fmt: off

from __future__ import annotations

import hashlib
import io
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (REPO / "tools" / "x6_stage1", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import x6s1_data as sd  # noqa: E402  (first: its import applies the X6S1 sys.path convention)

# isort: split
import numpy as np  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_stats as ss  # noqa: E402

from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402

# ---- loading, names and bindings (API §3) ----
CONTRACT_PATH, PROTOCOL_FILE = HERE / "CONTRACT.json", HERE / "PROTOCOL_X6ZC_v1.md"
def load_contract(path=CONTRACT_PATH) -> dict:
    c = json.loads(Path(path).read_text("utf-8"))
    if hashlib.sha256(PROTOCOL_FILE.read_bytes()).hexdigest() != c["protocol"]["sha256"].lower():
        raise ValueError("PROTOCOL_X6ZC_v1.md sha256 differs from CONTRACT.json protocol.sha256")
    return c
def frac(s) -> Fraction: return Fraction(str(s))
CONTRACT = load_contract()
KC, _PA, _X = CONTRACT["constants"], CONTRACT["paths"], CONTRACT["x6s1"]
PROTOCOL_ID, PROTOCOL_SHA256 = CONTRACT["protocol"]["id"], CONTRACT["protocol"]["sha256"]
PROJECT_ROOT, X6S1_STORE, STORE = _PA["project_root"], _PA["x6s1_store"], _PA["store"]
WORKTREE, SCRATCH_ROOT, DRY_STORE = _PA["worktree"], _PA["scratch_root"], _PA["dry_store"]
METER_IMPORT_DIR, NA_DIR = _PA["meter_import_dir"], "ZC_NOT_COMMUTATIVE/NA_DIRECTION"
H3, MERGE_COMMIT, CLOSURE = _X["H3"], _X["merge_commit"], tuple(_X["closure_paths"])
X6ZC_MASTER, FAMILIES, VARIANT_ORDER = int(KC["x6zc_master"]), tuple(KC["families"]), tuple(
    KC["variant_order"])
VARIANT_SIGN, W1_TAIL = dict(KC["variant_sign"]), dict(KC["w1_tail_tokens"])
VARIANTS = {F: {v: tuple(tuple(m) for m in ms) for v, ms in KC["variants"][F].items()}
            for F in FAMILIES}
W1_CROSS_STEPS = {v: tuple(s) for v, s in KC["w1_crossing_steps"].items()}
READOUT_OFFSET, LAMBDA_INDEX = dict(KC["readout_offset"]), dict(KC["lambda_index"])
ANSWERS = {v: {k: tuple(x) for k, x in KC["answers"][v].items()} for v in VARIANT_ORDER}
CELLS = {c: {**d, "beta_D": float(d["beta_D"]), "sign": int(d["sign"]), "z": float(d["z"]),
             "b_q": tuple(map(Fraction, d["b_q"])), "r_q": tuple(map(Fraction, d["r_q"]))}
         for c, d in KC["cells"].items()}
CELL_ORDER, _PR = tuple(KC["cell_order"]), {k: tuple(v) for k, v in KC["predictors"].items()}
MODELS, INITS, STAGE_B_ORDER = _PR["models"], _PR["inits"], _PR["stage_b_order"]
FOCAL, K5_MODELS, NA_MODELS = _PR["focal"], _PR["k5"], _PR["na_models"]
K6_CONTROLS, K6_MIN = {F: tuple(m) for F, m in KC["k6_controls"].items()}, dict(KC["k6_min_pass"])
T = {k: (tuple(map(frac, v)) if isinstance(v, list) else frac(v) if isinstance(v, str) else v)
     for k, v in CONTRACT["thresholds"].items()}
B_DRAWS, N_FLOOR, N_D = int(T["b_draws"]), int(T["n_floor"]), int(T["n_d"])
N_LADDER, _S3N = tuple(int(x) for x in T["n_ladder"]), {xm.perm_name(g): g for g in xm.S3_LIST}
_MISS = {"miss1": frozenset({0}), "miss2": frozenset({1}), "miss_both": frozenset({0, 1})}
def stream(name) -> np.random.Generator:
    return SeedTree(X6ZC_MASTER).generator(*KC["streams"][name])
def dry_stream(*names) -> np.random.Generator:
    return SeedTree(X6ZC_MASTER).generator("x6zc", "dry", *names)
def _fl(x) -> float: return float(x)  # a bar compared in float, as written (§20 E-1)
def _ints(row) -> tuple: return tuple(int(w) for w in row)

# ---- fresh prefixes and variant construction (API §4) ----
def prefix_yields(prefix_tokens, rnd_len) -> list:
    out, ok_v = [], sp.NB | {sp.ANCHOR}
    for r, row in enumerate(prefix_tokens):
        lmax = int(rnd_len.integers(1, 15))  # one call per row, skipped rows included
        ok = [L for L in range(1, lmax + 1) if xm.vertex(int(row[L - 1])) in ok_v]
        out += [(r, _ints(row[:ok[-1]]))] if ok else []
    return out
def fresh_prefixes(prefix_tokens, d_prefixes) -> dict:
    def gen(): return SeedTree(sd.DATA_MASTER).generator(*_X["prefix_len_stream"])
    ys = prefix_yields(prefix_tokens, gen())
    if len(ys) < 1024:
        raise ValueError(f"only {len(ys)} yields; 1,024 needed")
    first, dset, fresh = [p for _, p in ys[:1024]], [_ints(p) for _, p in d_prefixes], ys[1024:]
    dco = np.array([p in set(dset) for _, p in fresh], bool)
    return {"n_rows": len(prefix_tokens), "n_yields": len(ys), "r_star": ys[1023][0],
            "first_1024_equal": first == sp.natural_prefixes(prefix_tokens, gen()),
            "d_equal": first == dset[6:], "fresh": fresh, "n_avail": len(fresh),
            "d_coincident": dco, "n_d_coincident": int(dco.sum()),
            "not_enough_data": len(fresh) < N_FLOOR}
def variant_path(family, variant, member) -> tuple:
    spec, sc = VARIANTS[family][variant]["ab".index(member)], KC["w2_scaffold"]
    return _ints(spec) if family == "W1" else (
        tuple(sc["head"]) + xe.LOOPS[spec[0]] + xe.LOOPS[spec[1]] + tuple(sc["tail"]))
def variant_history(family, variant, member, prefix, y) -> tuple:
    return (_ints(prefix) + (15 + int(y),)
            + tuple(xm.tok(v) for v in variant_path(family, variant, member)))
def variant_arrays(prefixes, family) -> dict:
    rows, A = [(i, y) for i in range(len(prefixes)) for y in range(3)], {}
    for v, m in ((v, m) for v in VARIANT_ORDER for m in "ab"):
        A[f"{v}_{m}"] = sp._pad([variant_history(family, v, m, prefixes[i], y) for i, y in rows])
        A[f"{v}_t"] = np.array([len(prefixes[i]) + READOUT_OFFSET[family] for i, _ in rows],
                               np.int16)
        A[f"{v}_y"] = np.array([y for _, y in rows], np.int8)
    return {**A, "prefix": np.array([i for i, _ in rows], np.int32)}
def d_cluster(n_rows) -> np.ndarray: return (np.arange(n_rows) // 3).astype(np.int32)

# ---- exact geometry (K0) and the q*_NA cache (API §5) ----
@lru_cache(maxsize=None)
def _qx(arm, h) -> tuple: return tuple(xm.closed_form(arm, h)["q"])
def qx(arm, history) -> tuple:  # q*_arm; closed_form's law depends only on the last cue onwards
    h = _ints(history)
    cues = [i for i, w in enumerate(h) if w >= 15]
    return _qx(arm, h[cues[-1]:] if cues else h)
def crossings(path) -> list:
    full = (xm.ANCHOR,) + tuple(path)
    return [(k + 1, lt) for k, (u, w) in enumerate(zip(full, full[1:]))
            if (lt := xm.seam_letter(u, w))]
def holonomy_missing(arm, segment, skip) -> tuple:
    lab, g, j = xm.edge_labels(arm), xm.S3_E, 0
    for u, w in zip(segment, segment[1:]):
        h = lab[(u, w)]
        if xm.seam_letter(u, w):
            h, j = (xm.S3_E if j in skip else h), j + 1
        g = xm.compose(h, g)
    return g
def missed_law(history, which) -> tuple:
    h = _ints(history)
    z, p = qx("ZC", h), xm.parse(h)
    g, pc = holonomy_missing("ZC", p["segment"], _MISS[which]), sum(z[15:18])
    return z[:15] + tuple(pc * x for x in xm.point_law(p["n"] + 1, g[p["y"]]))
def answer_names(history) -> dict:
    seg = xm.parse(history)["segment"]
    out = {a: xm.perm_name(xm.holonomy(seg, xm.edge_labels(a))) for a in ("NA", "ZC", "AB")}
    return {**out, **{f"ZC_{k}": xm.perm_name(holonomy_missing("ZC", seg, s))
                      for k, s in _MISS.items()}}
def _cn(q) -> tuple: return tuple(x / sum(q[15:18]) for x in q[15:18])
def _dna(lam, y) -> list: return [lam * ((z == xm.S3_C2[y]) - (z == xm.S3_C[y])) for z in range(3)]
def _w1_stats(h, p) -> tuple:
    k = xm.parikh(p["segment"])
    return (len(h), p["n"], p["v"], p["prefix"], p["y"], k,
            *(xm.statistic(S, k) for S in ("H1", "counts", "parity")))
def _k0_pair(ha, hb, family, v, lam):  # (item, detail) of the first failing item, or None
    try:
        pa, pb = xm.parse(ha), xm.parse(hb)
    except ValueError as e:
        return 4, f"illegal history: {e}"
    if any(sp.q_exact(a, ha, len(ha)) != sp.q_exact(a, hb, len(hb)) for a in ("ZC", "AB")):
        return 1, "q*_ZC or q*_AB differs between the members"
    na, nb = sp.q_exact("NA", ha, len(ha)), sp.q_exact("NA", hb, len(hb))
    if not (sum(na[15:18]) and sum(nb[15:18]) and pa["y"] is not None) or [
            x - w for x, w in zip(_cn(na), _cn(nb))] != _dna(lam, pa["y"]):
        return 2, "cue-normalised q*_NA difference (or zero cue mass) at the readout"
    ga, gb = answer_names(ha), answer_names(hb)
    if any((ga[k], gb[k]) != ab for k, ab in ANSWERS[v].items()):
        return 3, "answer table"
    sa, sb, (sx, sy) = pa["segment"][1:], pb["segment"][1:], ("+-"[v[0] == "M"], "+-"[v[1] == "M"])
    ca, cb = crossings(sa), crossings(sb)
    tail = next((k for k in range(1, min(len(ha), len(hb)) + 1) if ha[-k] != hb[-k]), 1) - 1
    la, lb = [lt for _, lt in ca], [lt for _, lt in cb]
    ok = (la, lb) == ([f"x{sx}", f"y{sy}"], [f"y{sy}", f"x{sx}"])
    ok &= sa[0] in xm.ANCHOR_NB and sa[-1] in xm.ANCHOR_NB
    if family == "W2":
        ok &= (Counter(ha) == Counter(hb) and Counter(zip(ha, ha[1:])) == Counter(zip(hb, hb[1:]))
               and xm.parikh(pa["segment"]) == xm.parikh(pb["segment"]) and tail >= 8
               and (pa["n"], pa["v"], pa["y"]) == (pb["n"], pb["v"], pb["y"]))
    else:
        da, db = Counter(ha) - Counter(hb), Counter(hb) - Counter(ha)
        ok &= (_w1_stats(ha, pa) == _w1_stats(hb, pb) and sum(na[15:18]) == Fraction(1, 5)
               and sum(da.values()) == sum(db.values()) == 1 and tail == W1_TAIL[v]
               and [s for s, _ in ca] == [s for s, _ in cb] == list(W1_CROSS_STEPS[v]))
    return None if ok else (4, "variant matching, crossing letters or start/end vertex")
def oracle_geometry(arrays, family, keys=VARIANT_ORDER) -> dict:
    lam, fresh = xm.lam(LAMBDA_INDEX[family]), "prefix" in arrays
    checks, cex, n, ref, ctrl = {f"item{i}": True for i in range(1, 6)}, None, 0, {}, {}
    for key in keys:
        v, A, B = (key if key in VARIANT_ORDER else "PP"), arrays[f"{key}_a"], arrays[f"{key}_b"]
        ts, ys = np.asarray(arrays[f"{key}_t"], np.int64), arrays[f"{key}_y"]
        for r in range(len(A)):
            ha, hb = _ints(A[r, :ts[r]]), _ints(B[r, :ts[r]])
            if key in sp.CONTROL_SETS:  # C-3: q* of a equals q* of b, recorded, not gated
                ctrl[key] = ctrl.get(key, 0) + all(sp.q_exact(a, ha, len(ha)) == sp.q_exact(
                    a, hb, len(hb)) for a in ("NA", "ZC", "AB"))
                continue
            n, bad = n + 1, _k0_pair(ha, hb, family, v, lam)
            for m, h in ((("a", ha), ("b", hb)) if bad is None and fresh else ()):
                if ref.setdefault((v, m, int(ys[r])), qx("NA", h)) != qx("NA", h):
                    bad = 5, "q*_NA not prefix-invariant"
            if bad is not None:
                checks[f"item{bad[0]}"] = False
                cex = cex or {"key": key, "row": r, "item": bad[0], "detail": bad[1]}
    return {"status": "PASS" if cex is None else "FAIL", "checks": checks, "counterexample": cex,
            "n_pairs": n, "controls_equal": ctrl}
def _cos(u, d) -> tuple:  # (cos² as "p/q", sign, float cosine)
    ip, nu, nd = sum(a * b for a, b in zip(u, d)), sum(a * a for a in u), sum(b * b for b in d)
    c2, sg = (ip * ip / (nu * nd), (ip > 0) - (ip < 0)) if nu and nd else (Fraction(0), 0)
    return str(c2), sg, sg * math.sqrt(c2)
def coupling_table() -> dict:
    out = {F: {v: {} for v in VARIANT_ORDER} for F in FAMILIES}
    for F, v, y in ((F, v, y) for F in FAMILIES for v in VARIANT_ORDER for y in range(3)):
        d, rec = _dna(xm.lam(LAMBDA_INDEX[F]), y), {}
        for m in "ab":
            nm = answer_names(variant_history(F, v, m, (), y))
            z = _S3N[nm["ZC"]][y]
            e = _cos([Fraction(int(k == z)) - Fraction(1, 3) for k in range(3)], d)
            rec[m] = {"zc": nm["ZC"], **dict(zip(("cos2_e", "sign_e", "cos_e"), e))}
            for k in ("miss1", "miss2"):
                x = _cos([int(i == _S3N[nm["ZC_" + k]][y]) - int(i == z) for i in range(3)], d)
                rec[m][k] = {"to": nm["ZC_" + k], **dict(zip(("cos2", "sign", "cos"), x))}
        out[F][v][str(y)] = rec
    return out
class QStarCache:
    """q*_NA rows computed once per distinct (w_{1:t}, t); bitwise equal to se.qstar("NA")."""
    def __init__(self, table): self.table = table
    @staticmethod
    def key(row, t) -> str:
        return hashlib.sha256(bytes(np.asarray(row[:t], np.uint8))
                              + int(t).to_bytes(2, "little")).hexdigest()
    @classmethod
    def build(cls, array_dicts) -> QStarCache:
        table = {}
        for A in array_dicts:
            for k in sorted(x for x in A if x.endswith(("_a", "_b")) and f"{x[:-2]}_t" in A):
                tok, ts = A[k], np.asarray(A[f"{k[:-2]}_t"], np.int64)
                keys = [cls.key(r, t) for r, t in zip(tok, ts)]
                miss = {kk: i for i, kk in reversed(list(enumerate(keys))) if kk not in table}
                if miss:
                    q, c = se.qstar("NA", tok[list(miss.values())], ts[list(miss.values())])
                    table.update(zip(miss, zip(q, c)))
        return cls(table)
    def __call__(self, tokens, t) -> tuple:
        tok = np.asarray(tokens)
        ts = np.broadcast_to(np.asarray(t, np.int64), (len(tok),))
        q, c = np.empty((len(tok), 18), np.float64), np.empty((len(tok), 18), np.int16)
        for i, (r, k) in enumerate(zip(tok, ts)):
            q[i], c[i] = self.table[self.key(r, k)]  # KeyError for an uncached history
        return q, c
    def save(self, path) -> str:
        keys, buf = sorted(self.table), io.BytesIO()
        np.savez(buf, keys=np.array(keys, "<U64"),
                 q=np.array([self.table[k][0] for k in keys], np.float64).reshape(-1, 18),
                 codes=np.array([self.table[k][1] for k in keys], np.int16).reshape(-1, 18))
        with open(path, "xb") as fh:
            fh.write(buf.getvalue())
        return hashlib.sha256(buf.getvalue()).hexdigest()
    @classmethod
    def load(cls, path, sha256) -> QStarCache:
        data = Path(path).read_bytes()
        if hashlib.sha256(data).hexdigest() != str(sha256).lower():
            raise ValueError(f"q* cache sha256 mismatch: {path}")
        z = np.load(io.BytesIO(data), allow_pickle=False)
        return cls({str(k): (q, c) for k, q, c in zip(z["keys"], z["q"], z["codes"])})

# ---- synthetic and analytic predictors (API §6) ----
def member_of(history) -> str:
    seg = xm.parse(history)["segment"]
    cr = crossings(seg[1:]) if seg else []
    if len(cr) < 2:
        raise ValueError("fewer than two seam crossings after the last cue")
    return "a" if cr[0][1][0] == "x" else "b"
def _mix(*terms) -> tuple: return tuple(sum(w * q[i] for w, q in terms) for i in range(18))
_MK = {"M2a": "miss1", "M2b": "miss2", "M6": "miss_both", "M0+M2a": "miss1"}
class SyntheticPredictor:
    def __init__(self, kind, **params):
        self.kind, self.name = kind, f"{kind}{sorted(params.items())}"
        self.params = {k: v if isinstance(v, str) else frac(v) for k, v in params.items()}
    def exact(self, history) -> tuple:
        h, k, P = _ints(history), self.kind, self.params
        if k == "set_constant":
            return (Fraction(4, 75),) * 15 + (Fraction(1, 15),) * 3
        p, Z = xm.parse(h), qx("ZC", h)
        if k == "matched_key":
            blob = canonical_json([list(p["prefix"]), p["y"], p["n"], p["v"],
                                   list(xm.parikh(p["segment"]))]).encode("utf-8")
            K = int(hashlib.sha256(blob).hexdigest()[:8], 16) % int(KC["matched_key_modulus"])
            m = Fraction(1 + K % 7, 10)
            return ((1 - m) / 15,) * 15 + tuple(m * Fraction(K + j, 3 * K + 6) for j in (1, 2, 3))
        if k in ("mixture", "M0"):
            w = P["delta" if k == "mixture" else "w"]
            return _mix((1 - w, sp.q_stat(P["S"], h, len(h)) if k == "mixture" else Z),
                        (w, qx("NA", h)))
        pc, z = sum(Z[15:18]), xm.holonomy(p["segment"], xm.edge_labels("ZC"))[p["y"]]
        if k == "W1_token_identity":
            s = (3 in p["segment"]) - (12 in p["segment"])
            return Z[:15] + tuple(pc * (c + s * P["eps"] * ((j == p["y"]) - Fraction(1, 3)))
                                  for j, c in enumerate(_cn(Z)))
        m = member_of(h)
        if k == "M1":
            kap = P["kappa_" + m]
            return Z[:15] + tuple(pc * ((1 - kap) / 3 + kap * (j == z)) for j in range(3))
        if k == "M4":
            j = [i for i, (_, lt) in enumerate(crossings(p["segment"][1:])) if lt[0] == P["seam"]]
            pi = P["pi"] if m == P["member"] else 0
            return _mix((1 - pi, Z), (pi, missed_law(h, ("miss1", "miss2")[j[0]])))
        pi, w = P["pi_" + m], P.get("w", 0) if k == "M0+M2a" else 0
        return _mix((1 - w - pi, Z), (w, qx("NA", h)), (pi, missed_law(h, _MK[k])))
    def __call__(self, tokens, t) -> np.ndarray:
        tok = np.asarray(tokens)
        ts = np.broadcast_to(np.asarray(t, np.int64), (len(tok),))
        return np.array([[float(x) for x in self.exact(r[:k])] for r, k in zip(tok, ts)],
                        np.float64).reshape(len(tok), 18)
def oracle(arm, kind) -> se.OraclePredictor: return se.OraclePredictor(arm, kind)
def sym_arrays(p_a, p_b) -> tuple:
    s = (np.asarray(p_a, np.float64) + np.asarray(p_b, np.float64)) / 2
    return s, s.copy()

# ---- pair terms and the K1, K2, K3/F1 checks (API §7) ----
def pair_arrays(pred, arrays, key, qstar_fn) -> dict:
    a, b, t, y = (arrays[f"{key}_{s}"] for s in ("a", "b", "t", "y"))
    if not len(a) == len(b) == len(t) == len(y):
        raise ValueError(f"mismatched join in {key}: lengths differ")
    ts = np.asarray(t, np.int64)
    p_a, p_b, (q_a, c_a), (q_b, c_b) = pred(a, ts), pred(b, ts), qstar_fn(a, ts), qstar_fn(b, ts)
    num, den = se.pair_terms(p_a, p_b, q_a, q_b)
    cl = np.asarray(arrays["prefix"], np.int64) if "prefix" in arrays else d_cluster(len(a))
    return {"p_a": p_a, "p_b": p_b, "q_a": q_a, "q_b": q_b, "codes_a": c_a, "codes_b": c_b,
            "num": num, "den": den, "y": np.asarray(y, np.int64), "t": ts, "cluster": cl,
            "tok_a": a, "tok_b": b}
def pair_stats(terms) -> dict:
    num, den, y = terms["num"], terms["den"], np.asarray(terms["y"])
    dp = se.cue_normalise(terms["p_a"]) - se.cue_normalise(terms["p_b"])
    dq = se.cue_normalise(terms["q_a"]) - se.cue_normalise(terms["q_b"])
    n, beta = len(num), se.beta_fsum(num, den)
    dd = math.fsum((dq * dq).sum(1)) / n if n else math.nan
    return {"beta": beta, "beta_y": [se.beta_fsum(num[y == z], den[y == z]) for z in range(3)],
            "rho": math.fsum((dp * dp).sum(1)) / n / dd if dd else math.nan,
            "max_pair_diff": float(np.abs(dp).max()) if n else 0.0,
            "nonfinite": bool(not np.isfinite(dp).all() or not math.isfinite(beta))}
def k1_check(terms) -> dict:
    st, num = pair_stats(terms), np.asarray(terms["num"])
    nz, bz = bool((num == 0.0).all()), se.beta_exact(num, terms["den"]) == 0
    ok = st["beta"] == 0.0 and st["rho"] == 0.0 and nz and bz
    return {"status": "PASS" if ok else "FAIL", "beta": st["beta"], "rho": st["rho"],
            "num_zero": nz, "beta_exact_zero": bz}
_K2 = {"qstar": (1, (1, 1, 1)), "h_last": (0, (0.5, -1, 0.5)), "h_first": (None, (-0.5, 1, -0.5)),
       "h_rev": (-1, None)}  # K2 targets: (pooled, per cue); None = not gated by the protocol
def k2_check(terms_by_ref, family) -> dict:
    tol, vals, failed = _fl(T["ref_abs"]), {}, []
    for ref, terms in terms_by_ref.items():
        st, (pooled, per_y) = pair_stats(terms), _K2[ref]
        vals[ref] = {"beta": st["beta"], "beta_y": st["beta_y"]}
        ok = pooled is None or abs(st["beta"] - pooled) <= tol
        failed += [] if ok and (per_y is None or all(
            abs(b - w) <= tol for b, w in zip(st["beta_y"], per_y))) else [ref]
    return {"status": "FAIL" if failed else "PASS", "family": family, "values": vals,
            "failed": failed}
def beta_exact_pi0(law_fn, family, variant, ys=(0, 1, 2)) -> Fraction:
    num = den = Fraction(0)
    for y in ys:
        ha, hb = (variant_history(family, variant, m, (), y) for m in "ab")
        dp = [a - b for a, b in zip(_cn(law_fn(ha)), _cn(law_fn(hb)))]
        dq = [a - b for a, b in zip(_cn(qx("NA", ha)), _cn(qx("NA", hb)))]
        num, den = num + sum(a * b for a, b in zip(dp, dq)), den + sum(b * b for b in dq)
    return num / den
def k2_exact_variants(family) -> dict:  # recorded known cases on MM, PM, MP (not gated)
    def law(kind): return lambda h: sp.q_heuristic(kind, h, len(h))
    return {f"h_{k}": {v: {"pooled": beta_exact_pi0(law(k), family, v), "per_y": [
        beta_exact_pi0(law(k), family, v, (y,)) for y in range(3)]} for v in VARIANT_ORDER[1:]}
        for k in ("last", "first", "rev")}
def k3_grid() -> list:
    k3 = KC["k3"]
    ws, pairs = [frac(x) for x in k3["w"]], [tuple(map(frac, p)) for p in k3["pairs"]]
    g = [("M0", {"w": w}) for w in ws] + [("M1", {"kappa_a": a, "kappa_b": b}) for a, b in pairs]
    g += [(k, {"pi_a": a, "pi_b": b}) for k in ("M2a", "M2b", "M6") for a, b in pairs]
    return g + [("M4", {"pi": p, "seam": s, "member": m}) for p in ws
                for s in k3["m4_seams"] for m in k3["m4_members"]]
def k3_exact(family) -> dict:
    out = {}
    for kind, params in k3_grid():
        pred = SyntheticPredictor(kind, **params)
        beta = {v: beta_exact_pi0(pred.exact, family, v) for v in VARIANT_ORDER}
        out[f"{kind}|" + ",".join(f"{k}={v}" for k, v in sorted(params.items()))] = {
            "kind": kind, "params": params, "beta": beta,
            "r": {v: beta[v] / beta["PP"] if beta["PP"] else None for v in VARIANT_ORDER}}
    return out
def k3_float_check(family, arrays, qstar_fn) -> dict:
    tol, worst, failed = _fl(T["ref_abs"]), 0.0, []
    for mid, e in k3_exact(family).items():
        pred = SyntheticPredictor(e["kind"], **e["params"])
        for v in VARIANT_ORDER:
            t = pair_arrays(pred, arrays, v, qstar_fn)
            d = abs(se.beta_fsum(t["num"], t["den"]) - float(e["beta"][v]))
            worst, failed = max(worst, d if d == d else math.inf), failed + [[mid, v]] * (
                not d <= tol)
    return {"status": "FAIL" if failed else "PASS", "max_abs": worst, "failed": failed}
def f1(k3) -> dict:
    m0 = all(e["r"][v] == 1 for e in k3.values() if e["kind"] == "M0" for v in VARIANT_ORDER)
    kinds, dist = {}, T["f1_min_distance"]
    for kind in KC["k3"]["sign_symmetric"]:
        es = [e for e in k3.values() if e["kind"] == kind]
        kinds[kind] = {"far": all(any(e["r"][v] is not None and abs(e["r"][v] - 1) >= dist
                                      for v in VARIANT_ORDER[1:]) for e in es),
                       "r_mm_minus_one": all(e["r"]["MM"] == -1 for e in es)}
    failed = ([] if m0 else ["M0"]) + [k for k, x in kinds.items() if not all(x.values())]
    return {"m0_ok": m0, "kinds": kinds, "passed": not failed, "failed": failed}

# ---- paired cluster bootstrap, ratios and B9 sizing (API §8) ----
def cluster_sums(values, cluster, P) -> np.ndarray:
    v, c = np.asarray(values, np.float64), np.asarray(cluster, np.int64)
    o = np.argsort(c, kind="stable")
    b = np.searchsorted(c[o], np.arange(P + 1))
    return np.array([math.fsum(v[o[b[i]:b[i + 1]]]) for i in range(P)], np.float64)
def paired_cluster_boot(num, den, B, gen) -> dict:
    keys = list(num)
    N, D = (np.stack([np.asarray(x[k], np.float64) for k in keys]) for x in (num, den))
    out = np.empty((len(keys), B), np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        for b in range(B):
            idx = gen.integers(0, N.shape[1], size=N.shape[1])  # one index array per draw
            G, H = N[:, idx], D[:, idx]  # each row summed as a 1-D array: the boot_beta sum
            out[:, b] = np.array([g.sum() for g in G]) / np.array([h.sum() for h in H])
    return {k: out[i] for i, k in enumerate(keys)}
def interval(draws, q) -> tuple:
    d = np.asarray(draws, np.float64)
    if not np.isfinite(d).all():
        raise ValueError("non-finite bootstrap draws: no interval (C-21)")
    return ss.quantile(d, float(q[0])), ss.quantile(d, float(q[1]))
def ratio_interval(draws_v, draws_pp, sign, q) -> dict:
    v, pp = np.asarray(draws_v, np.float64), np.asarray(draws_pp, np.float64)
    ok = sign * pp > 0
    nd = int(ok.sum())
    lo, hi = interval(v[ok] / pp[ok], q) if nd else (None, None)
    return {"lo": lo, "hi": hi, "n_defined": nd, "undefined": len(pp) - nd,
            "undefined_frac": (len(pp) - nd) / len(pp), "n_draws": len(pp)}
def _ratio(a, b): return a / b if b else None
def cell_statistics(point, draws, cell) -> dict:
    c, (lo_b, hi_b) = CELLS[cell], T["r_band"]
    m, F, s = c["model"], c["family"], c["sign"]
    pp, dpp = point[(m, F, "PP")], np.asarray(draws[f"{m}|{F}|PP|beta"], np.float64)
    out = {"model": m, "family": F, "sign": s, "b": s * pp, "beta_pp": pp, "r": {}, "r_w1_p": None}
    out["b_lo"], out["b_hi"] = interval(s * dpp, c["b_q"])
    for v in VARIANT_ORDER[1:]:
        ri = ratio_interval(draws[f"{m}|{F}|{v}|beta"], dpp, s, c["r_q"])
        out["r"][v] = {"point": _ratio(point[(m, F, v)], pp), "lo": ri["lo"], "hi": ri["hi"],
                       "n_defined": ri["n_defined"]}
        out.update({k: ri[k] for k in ("undefined", "undefined_frac", "n_draws")})
    sb = interval(0.5 * (dpp + np.asarray(draws[f"{m}|{F}|MM|beta"])), T["beta_sb_q"])
    out["beta_sb"] = {"point": 0.5 * (pp + point[(m, F, "MM")]), "lo": sb[0], "hi": sb[1]}
    if cell == "P" and (m, "W1", "PP") in point and f"{m}|W1|PP|beta" in draws:
        ri = ratio_interval(draws[f"{m}|W1|PP|beta"], dpp, s, T["r_w1_p_q"])
        lab = (None if ri["lo"] is None or Fraction(ri["undefined"], ri["n_draws"])
               > T["undefined_max"] else "W2_ONLY" if ri["hi"] < _fl(lo_b) else
               "NA_BOTH_FAMILIES" if _fl(lo_b) < ri["lo"] and ri["hi"] < _fl(hi_b) else None)
        out["r_w1_p"] = {"point": _ratio(point[(m, "W1", "PP")], pp), "lo": ri["lo"],
                         "hi": ri["hi"], "undefined_frac": ri["undefined_frac"], "label": lab}
    return out
def halfwidth(n, se_d, beta_d, z) -> float:
    return (z * math.sqrt(2) * se_d * math.sqrt(N_D / n)
            / max(abs(beta_d) - 2 * se_d, _fl(T["se_floor"])))
def choose_n(n_avail, se) -> dict:
    out = {"n": n_avail, "status": "NOT_ENOUGH_DATA", "candidates": [], "h": {},
           "underpowered": dict.fromkeys(CELL_ORDER, False),
           "low_feasibility": list(KC["feasibility_ratio"]["low_feasibility"])}
    if n_avail < N_FLOOR:
        return out
    cand, ht = sorted({n for n in (*N_LADDER, n_avail) if N_FLOOR <= n <= n_avail}), _fl(
        T["h_target"])
    h = {c: {str(n): halfwidth(n, se[c], CELLS[c]["beta_D"], CELLS[c]["z"]) for n in cand}
         for c in CELL_ORDER}
    ok = [n for n in cand if h["P"][str(n)] <= ht]
    n = ok[0] if ok else n_avail
    out.update(n=n, status="OK" if ok else "UNDERPOWERED", candidates=cand, h=h)
    out["underpowered"] = {"P": not ok, **{c: h[c][str(n)] > ht for c in CELL_ORDER[1:]}}
    return out

# ---- decision (§9.1), licences, qualifiers, reuse verdict (API §9) ----
def _ascii(rule) -> str: return rule.replace("′", "'")
def _lt(x, bar) -> bool: return x is not None and x < _fl(bar)
def _gt(x, bar) -> bool: return x is not None and x > _fl(bar)
def _unstable(s) -> bool:  # counts compared as integers when present (§20 E-1)
    if "undefined" in s and "n_draws" in s:
        return Fraction(s["undefined"], s["n_draws"]) > T["undefined_max"]
    return s["undefined_frac"] > _fl(T["undefined_max"])
def _cell_rule(ev, c) -> tuple:
    F, s, b9, (lo_b, hi_b), bm = (CELLS[c]["family"], ev["cells"].get(c), ev["b9"], T["r_band"],
                                  T["b_margin"])
    pre = ("R4a" if b9["status"] == "NOT_ENOUGH_DATA" else "R4b" if b9["underpowered"].get(c)
           else "R5" if not ev["k6"][F] else None)
    if pre:
        return pre, None
    if s is None:
        raise ValueError(f"cell {c}: no statistics")
    r = s["r"]
    if _lt(s["b_hi"], bm) and s["b_lo"] <= 0:
        return "R6", None
    if _lt(s["b"], bm) or s["b_lo"] <= _fl(T["lo_margin"]):
        return "R7", "positive" if s["b_lo"] > 0 and _lt(s["b"], bm) else "ambiguous"
    rule = ("R7b" if _unstable(s) else "R8" if _lt(r["MM"]["hi"], 0) else
            "R8b" if any(_lt(r[v]["hi"], lo_b) or _gt(r[v]["lo"], hi_b) for v in r) else
            "R10" if not all(_gt(r[v]["lo"], lo_b) and _lt(r[v]["hi"], hi_b) for v in r) else
            "R9" if ev["f1"][F]["passed"] else "R9′")
    return rule, None
def decide_x6zc(ev) -> dict:
    out = {"global_rule": None, "global_outcome": None, "cells": {}, "headline": None,
           "defect_elsewhere": [r["id"] for r in ev.get("rulings", []) if r["cause_identified"]
                                and not r["affects_beta"] and not r.get("setup")]}
    g = "G-R0" if ev["k0"] == "FAIL" else "G-R1" if ev.get("incomplete") else None
    if g is None:
        rul, failed = {}, [k for k, s in ev["checks"].items() if s in ("FAIL", "DEFECT_CANDIDATE")]
        for r in ev.get("rulings", []):
            rul.setdefault(r["check"], []).append(r)
        if any(k not in rul for k in failed):
            raise ValueError(f"failed checks without a ruling: {sorted(set(failed) - set(rul))}")
        rs = [r for k in failed for r in rul[k]]
        g = ("G-R2" if any(r["cause_identified"] and r["affects_beta"] for r in rs) else
             "G-R2′" if any(not r["cause_identified"] for r in rs) else
             "G-R3" if ev["k1"] == "FAIL" and ev["a2_k5_pass"] else None)
    if g is not None:
        o = CONTRACT["outcomes"]["global"][_ascii(g)]
        cell = {"rule": g, "outcome": o, "licence_case": None, "descriptive": False}
        return {**out, "global_rule": g, "global_outcome": o, "headline": o,
                "cells": {c: dict(cell) for c in CELL_ORDER}}
    for c in CELL_ORDER:
        rule, case = _cell_rule(ev, c)
        o = CONTRACT["outcomes"]["cell"][_ascii(rule)]["P" if c == "P" else "S"].format(
            mechanisms=", ".join(ev["f1"][CELLS[c]["family"]]["failed"]))
        out["cells"][c] = {"rule": rule, "outcome": o, "licence_case": case,
                           "descriptive": rule in ("R4a", "R4b")}
    return {**out, "headline": out["cells"]["P"]["outcome"]}
def _lkey(outcome, table, case=None) -> str:
    if outcome == "UNEXPLAINED/WEAK_REPLICATION":
        return f"{outcome}:{case or 'ambiguous'}"
    return outcome if outcome in table else "UNEXPLAINED/*"
def licence(outcome, values, case=None) -> str:
    L = CONTRACT["licences"]
    if outcome in ("STOP_REPLAN", "INVALID"):
        return ""
    txt = L[_lkey(outcome, L, case)].format(**{**values, "outcome": outcome})
    w1 = values["cell"] in ("S3", "S4") if "cell" in values else values.get("family") == "W1"
    return txt + L[NA_DIR + ":W1_suffix"] if outcome == NA_DIR and w1 else txt
def not_licensed(outcome, case=None) -> str:
    return CONTRACT["not_licensed"][_lkey(outcome, CONTRACT["not_licensed"], case)]
def qualifiers(ev, decision, census) -> dict:
    cen, out = census or {}, {}
    for c in CELL_ORDER:
        d, m, F = decision["cells"][c], CELLS[c]["model"], CELLS[c]["family"]
        q, s = [], (ev.get("cells") or {}).get(c) or {}
        if d["outcome"].startswith("ZC_NOT_COMMUTATIVE/"):
            q += ["ORIGIN_UNRESOLVED"] + list(cen.get("qualifiers", {}).get(f"{m}|{F}", []))
            q += [s["r_w1_p"]["label"]] if c == "P" and (s.get("r_w1_p") or {}).get("label") else []
            for line, name in (("A4", "SENSITIVITY_A4"), ("DPREFIX", "SENSITIVITY_D_PREFIX")):
                alt = cen.get("sensitivity", {}).get(line, {}).get(c)
                q += [f"{name}({alt})"] if alt is not None and alt != d["outcome"] else []
        q += [f"LOW_FEASIBILITY({c})"] * (c in ev["b9"].get("low_feasibility", []))
        q += [f"UNDERPOWERED({c})"] * bool(ev["b9"]["underpowered"].get(c))
        q += ["ENV_DRIFT"] * (ev["checks"].get("K4") == "ENV_DRIFT")
        q += [f"NUMERIC_DRIFT({m}, {F})"] * (f"{m}|{F}" in cen.get("numeric_drift", []))
        q += [f"DEFECT_ELSEWHERE({i})" for i in decision["defect_elsewhere"]]
        out[c] = q + ["DESCRIPTIVE"] * bool(d["descriptive"])
    return out
def reuse_verdict(ev, decision) -> dict:
    R, g, cells, h = (CONTRACT["reuse"], decision["global_outcome"], decision["cells"],
                      decision["headline"])
    a1 = ("NOT_FIT" if g in ("DEFECT_FOUND", "ESTIMATOR_ARTIFACT/NON_INVARIANT") else
          "UNDETERMINED" if g in ("UNEXPLAINED/IRREPRODUCIBLE", "INVALID", "STOP_REPLAN") else
          "VALID")
    if a1 != "VALID":
        return {"axis1": a1, "axis2": "NOT_ASSESSED", "amendments": [], "amendment_1_mark": None,
                "statement": None}
    a2, bo = ("UNDETERMINED" if cells["P"]["outcome"] == NA_DIR else "FIT_WITH_AMENDMENT",
              R["by_outcome"])
    am = {a for c in CELL_ORDER for a in bo.get(cells[c]["outcome"], bo["UNEXPLAINED/*"])}
    am |= {2, 3} if a2 == "UNDETERMINED" else set()
    gen = h.startswith("UNEXPLAINED/") and h not in ("UNEXPLAINED/NOT_NA_INVARIANT",
                                                     "UNEXPLAINED/WEAK_REPLICATION")
    return {"axis1": a1, "axis2": a2, "amendments": sorted(am), "statement": R["statement"],
            "amendment_1_mark": R["amendment_1_inconclusive_mark"] if 1 in am and gen else None}
