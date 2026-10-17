"""X6 stage 0: model, closed-form oracle, gates G0/G1 (X6-FROZEN-v1 sections 0-3; API.md 3).
Exact objects are Fractions and Python ints; floats are float(Fraction). Import does no I/O."""

from __future__ import annotations

import itertools
import sys
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

import numpy as np

REPO = Path(__file__).resolve().parents[2]
_EXTRA = (Path(__file__).resolve().parent, REPO / "tools" / "x4_oracle_profile",
          REPO / "tests" / "oracle_profile")
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]

from oracle_profile import validate_process  # noqa: E402  (job-0014, unchanged)

import topo_pilot.world as tw  # noqa: E402
from topo_pilot.process import TransitionBuilder, TransitionConfig  # noqa: E402
from topo_pilot.world.complex import check_boundary_closed  # noqa: E402
from topo_pilot.world.metrics import check_flat_bounds  # noqa: E402

# ---- constants (API 3.1) ----
L_SIDE, N_V, N_FIB, N_S, V, V_NC = 4, 16, 3, 48, 18, 16
ANCHOR, ANCHOR_NB = 10, frozenset({6, 9, 11, 14})
F_STAR_VERTICES, F_STAR_ROW = (0, 3, 12, 15), (15, 12, 3, 0)
P_MOVE, ETA, T_STAR, N_OBS = Fraction(1, 5), Fraction(1, 50), 32, 33
WINDOWS, BLOCKS = (1, 2, 4, 8), ((1, 8), (9, 16), (17, 24), (25, 32))
ARMS = ("NA", "AB", "ZC", "TRIV", "ETA1", "GAUGE-NA", "GAUGE-TRIV", "GAUGE-COV")
ARMS_SEAM = ("NA", "AB", "ZC", "TRIV")
LADDER = ("empty", "parity", "counts", "H1", "Parikh")
EMISSIONS = ("E", "E_cov", "E_nc", "E_sigma")
MASTER_SEED, MC_STREAM = 420700, "x6s0_mc"
MC_ARMS = ("NA", "AB", "ZC", "TRIV", "ETA1", "NOCUE")
MC_ROWS = {"NA": 2**18, "AB": 2**16, "ZC": 2**16, "TRIV": 2**16, "ETA1": 2**16, "NOCUE": 2**14}
N_CHECK, BATCH = 2**14, 2048
TV_MIN, G_MIN, M_MIN = Fraction(3, 10), Fraction(1, 1000), Fraction(1, 32)
THETA_ROW, BETA_MAX = Fraction(1, 100), Fraction(1, 4)
TOL_STRUCT, TOL_NUM, TOL_LOGEV, TOL_G1_REL = 1e-15, 1e-12, 1e-10, 1e-12
TOL_DEC, TOL_LOG = Decimal("1e-45"), Decimal("1e-40")
MC_K, MC_FLOOR, RATIO_5GRAM = 4, 2e-12, 2
FAMILY, PROTOCOL_ID = "_x6_torus_local", "X6-FROZEN-v1"
PROTOCOL_SHA256 = "61DDA37BF5B23648894440B4016F80191C56B6626F04CD2D5A4178D46EF2B572"
REQUEST_SHA256 = "18E77F7E5BAE48AACC08C8A48560DEEDC0A543531C11B2E09D8684B36C9EFBE1"
R_COMMIT = "f8e5f12b2f83ecf8b6a32189705a03ff98afa28d"
KERNEL_BASE = "c364f95e5573940cdc24b569b0fb7c6a16c97ab8"
STORE = "X:/Downloads/projects/topo-pilot/x6-stage0-oracle-store"
WORKTREE = "X:/Downloads/projects/topo-pilot/topo-pilot-x6"
SCRATCH_ROOT = "X:/Downloads/topo-scratch"

# ---- S3 and index helpers (API 3.2) ----
S3_E, S3_A, S3_B, S3_C, S3_C2, S3_T = ((0, 1, 2), (1, 0, 2), (0, 2, 1), (1, 2, 0), (2, 0, 1),
                                       (2, 1, 0))
S3_LIST = (S3_E, S3_A, S3_B, S3_C, S3_C2, S3_T)
_NAMES = dict(zip(S3_LIST, ("e", "a", "b", "c", "c2", "t")))

def compose(g, h) -> tuple:
    return (g[h[0]], g[h[1]], g[h[2]])
def inverse(g) -> tuple:
    return tuple(tuple(g).index(x) for x in range(3))
def perm_name(g) -> str:
    return _NAMES[tuple(g)]
def state(i: int, x: int) -> int:
    return 3 * i + x
def split_state(s: int) -> tuple:
    return divmod(s, 3)
def tok(i: int) -> int:
    if i == ANCHOR or not 0 <= i < N_V:
        raise ValueError(f"no vertex token for vertex {i}")
    return i if i < ANCHOR else i - 1
def vertex(w: int) -> int:
    if not 0 <= w <= 17:
        raise ValueError(f"token {w} outside 0..17")
    return ANCHOR if w >= 15 else (w if w < ANCHOR else w + 1)
def cue(x: int) -> int:
    return 15 + x

NEIGHBOURS = tuple((4 * ((i // 4 + 1) % 4) + i % 4, 4 * ((i // 4 - 1) % 4) + i % 4,
                    4 * (i // 4) + (i % 4 + 1) % 4, 4 * (i // 4) + (i % 4 - 1) % 4, i)
                   for i in range(N_V))
_LETTERS = ("x+", "x-", "y+", "y-")

def seam_letter(i: int, j: int):
    (xi, yi), (xj, yj) = divmod(i, 4), divmod(j, 4)
    if yi == yj and {xi, xj} == {0, 3}:
        return "x+" if xi == 3 else "x-"
    if xi == xj and {yi, yj} == {0, 3}:
        return "y+" if yi == 3 else "y-"
    return None

# ---- labels and gauge arrays (API 3.3) ----
H_COV = tuple(S3_LIST[i % 6] for i in range(N_V))
H_FIX = H_COV[:ANCHOR] + (S3_E,) + H_COV[ANCHOR + 1:]
_SEAM = {"NA": (S3_A, S3_B), "AB": (S3_A, S3_A), "ZC": (S3_C, S3_C), "TRIV": (S3_E, S3_E),
         "ETA1": (S3_A, S3_B)}
_GAUGE = {"GAUGE-NA": ("NA", H_FIX), "GAUGE-TRIV": ("TRIV", H_FIX), "GAUGE-COV": ("NA", H_COV)}

def seam_labels(arm: str) -> dict:
    if arm not in _SEAM:
        raise ValueError(f"{arm} is not seam-supported")
    gx, gy = _SEAM[arm]
    return {"x+": gx, "x-": inverse(gx), "y+": gy, "y-": inverse(gy)}
@lru_cache(maxsize=None)
def _edge_labels(arm: str) -> tuple:
    base, h = _GAUGE.get(arm, (arm, None))
    lab, out = seam_labels(base), []
    for i in range(N_V):
        for j in NEIGHBOURS[i]:
            g = S3_E if i == j else lab.get(seam_letter(i, j), S3_E)
            out.append(((i, j), g if h is None else compose(h[j], compose(g, inverse(h[i])))))
    return tuple(out)

def edge_labels(arm: str) -> dict:
    return dict(_edge_labels(arm))
def eta(arm: str) -> Fraction:
    return Fraction(1) if arm == "ETA1" else ETA

# ---- world, complexes, kernel and emissions (API 3.4) ----
class _X6TorusBuilder(tw.QuotientLatticeBuilder):  # deliberately NOT @register_world
    family: ClassVar[str] = FAMILY
    expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
    identifications: ClassVar[tuple] = (tw.Identification(0, "periodic"),
                                         tw.Identification(1, "periodic"))

def build_world():
    spec = _X6TorusBuilder().build(tw.WorldConfig(FAMILY, (L_SIDE, L_SIDE), "flat"))
    spec.validate()
    check_boundary_closed(tw.CubicalComplex(spec.n_states, spec.cells))
    check_flat_bounds(spec.dist, spec.dist_graph, 2)
    return spec
def kernel(spec) -> np.ndarray:
    return TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T
def f_star_index(spec) -> int:
    (r,) = [r for r in range(len(spec.cells[2])) if sorted(spec.cells[2][r]) == [0, 3, 12, 15]]
    return r
def punctured_complex(spec):
    return tw.CubicalComplex(N_V, {0: spec.cells[0], 1: spec.cells[1],
                                   2: np.delete(spec.cells[2], f_star_index(spec), axis=0)})
def t_base_exact() -> list:
    return [[P_MOVE if j in NEIGHBOURS[i] else Fraction(0) for j in range(N_V)]
            for i in range(N_V)]
def lift(T_base, labels, eta) -> list:
    T, on, off = [[Fraction(0)] * N_S for _ in range(N_S)], (1 - eta) + eta / 3, eta / 3
    for i, j in itertools.product(range(N_V), range(N_V)):
        if T_base[i][j]:
            for x, x2 in itertools.product(range(3), range(3)):
                hit = x2 == labels[(i, j)][x]
                T[state(i, x)][state(j, x2)] = T_base[i][j] * (on if hit else off)
    return T

def sigma_tok(w: int) -> int:
    return (w + 7) % 15 if w <= 14 else w
def emission(kind: str) -> list:
    if kind not in EMISSIONS:
        raise ValueError(kind)
    M = [[Fraction(0)] * (V_NC if kind == "E_nc" else V) for _ in range(N_S)]
    for i, x in itertools.product(range(N_V), range(3)):
        xx = inverse(H_COV[i])[x] if kind == "E_cov" else x
        w = i if kind == "E_nc" else (cue(xx) if i == ANCHOR else tok(i))
        M[state(i, x)][sigma_tok(w) if kind == "E_sigma" else w] = Fraction(1)
    return M

def to_float(M) -> np.ndarray:
    return np.array([[float(v) for v in r] for r in M] if isinstance(M[0], (list, tuple))
                    else [float(v) for v in M], dtype=np.float64)
@lru_cache(maxsize=None)
def _model(arm: str, kind: str) -> dict:
    labels = edge_labels(arm)
    T, E, pi = lift(t_base_exact(), labels, eta(arm)), emission(kind), [Fraction(1, N_S)] * N_S
    return {"arm": arm, "kind": kind, "eta": eta(arm), "labels": labels, "T": T, "E": E,
            "pi": pi, "Tf": to_float(T), "Ef": to_float(E), "pif": to_float(pi)}
def model(arm: str, kind=None) -> dict:
    """Cached record (callers never mutate it); kind None: E_cov for GAUGE-COV, else E."""
    if arm not in ARMS:
        raise ValueError(arm)
    return _model(arm, kind or ("E_cov" if arm == "GAUGE-COV" else "E"))

# ---- faces, flux and cover (API 3.5) ----
def face_cycle(row) -> tuple:
    return tuple(int(row[k]) for k in (0, 2, 3, 1, 0))
def holonomy(path, labels) -> tuple:
    g = S3_E
    for u, v in zip(path, path[1:]):
        g = compose(labels[(u, v)], g)
    return g
def face_holonomies(spec, labels) -> list:
    return [holonomy(face_cycle(row), labels) for row in spec.cells[2].tolist()]
def flux(spec, labels) -> tuple:
    return face_holonomies(spec, labels)[f_star_index(spec)]
def cover_complex(spec, labels):
    c1 = [[state(i, x), state(j, labels[(i, j)][x])] for i, j in spec.cells[1].tolist()
          for x in range(3)]
    fs, c2 = f_star_index(spec), []
    for k, (r0, r1, r2, r3) in enumerate(spec.cells[2].tolist()):
        g01, g02, g23 = labels[(r0, r1)], labels[(r0, r2)], labels[(r2, r3)]
        c2 += [[state(r0, x), state(r1, g01[x]), state(r2, g02[x]), state(r3, g23[g02[x]])]
               for x in range(3) if k != fs]
    return tw.CubicalComplex(N_S, {0: np.arange(N_S).reshape(-1, 1), 1: np.array(c1),
                                   2: np.array(c2)})

def boundary_circles(cx) -> int:
    use, parent = {}, {}
    for sq in cx.cells[2].tolist():
        for a, b in ((0, 1), (2, 3), (0, 2), (1, 3)):
            use[frozenset((sq[a], sq[b]))] = use.get(frozenset((sq[a], sq[b])), 0) + 1

    def root(v):
        while parent.setdefault(v, v) != v:
            v = parent[v]
        return v
    for u, v in cx.cells[1].tolist():
        if use.get(frozenset((u, v)), 0) == 1:
            parent[root(u)] = root(v)
    return len({root(v) for v in list(parent)})

def cover_betti(cx) -> dict:
    return {2: tuple(cx.betti(2)), 3: tuple(cx.betti(3))}

# ---- path statistics (API 3.6) ----
def path_letters(path) -> list:
    return [lt for u, v in zip(path, path[1:]) if (lt := seam_letter(u, v)) is not None]
def parikh(path) -> tuple:
    k = [0, 0, 0, 0]
    for lt in path_letters(path):
        k[_LETTERS.index(lt)] += 1
    return tuple(k)
def statistic(S: str, kappa):
    k = tuple(kappa)
    return {"empty": lambda: (), "parity": lambda: sum(k) % 2,
            "counts": lambda: (k[0] + k[1], k[2] + k[3]),
            "H1": lambda: (k[0] - k[1], k[2] - k[3]), "Parikh": lambda: k}[S]()

ZC_WITNESS = ((10, 14, 2, 6, 6, 6, 6, 6), (10, 9, 5, 1, 13, 9, 5, 6))

# ---- closed-form oracle (API 3.7, Theorem 1) ----
@lru_cache(maxsize=None)
def lam(m: int, eta=ETA) -> Fraction:
    return (1 - Fraction(eta)) ** m
@lru_cache(maxsize=None)
def point_law(m: int, z: int, eta=ETA) -> tuple:
    lm = lam(m, eta)
    return tuple((1 - lm) / 3 + (lm if k == z else 0) for k in range(3))
def parse(tokens) -> dict:
    toks = [int(w) for w in tokens]
    path = [vertex(w) for w in toks]
    if any(v not in NEIGHBOURS[u] for u, v in zip(path, path[1:])):
        raise ValueError("non-adjacent consecutive vertices")
    cues, t = [k + 1 for k, w in enumerate(toks) if w >= 15], len(toks)
    out = {"t": t, "path": tuple(path), "v": path[-1] if path else None}
    if not cues:
        return {**out, "s": None, "y": None, "n": None, "segment": None, "prefix": tuple(toks)}
    s = cues[-1]
    return {**out, "s": s, "y": toks[s - 1] - 15, "n": t - s, "segment": tuple(path[s - 1:]),
            "prefix": tuple(toks[:s - 1])}

def closed_form(arm: str, tokens) -> dict:
    if arm not in ARMS_SEAM + ("ETA1",):
        raise ValueError(f"closed form undefined for {arm}")
    p, labels, e, third = parse(tokens), edge_labels(arm), eta(arm), Fraction(1, 3)
    rho = None if p["s"] is None else holonomy(p["segment"], labels)
    fibre = (third,) * 3 if rho is None else point_law(p["n"], rho[p["y"]], e)
    v, q = p["v"], [Fraction(0)] * V
    b = [fibre[s % 3] if s // 3 == v else Fraction(0) for s in range(N_S)]
    for j in NEIGHBOURS[v]:
        if j != ANCHOR:
            q[tok(j)] += P_MOVE
            continue
        g, nxt = labels[(v, j)], [e / 3] * 3
        for x in range(3):
            nxt[g[x]] += (1 - e) * fibre[x]
        for z in range(3):
            q[cue(z)] += P_MOVE * nxt[z]
    path, toks = p["path"], [int(w) for w in tokens]
    cues = [k for k, w in enumerate(toks) if w >= 15]
    P = Fraction(1, N_V) * P_MOVE ** (p["t"] - 1) * (third if cues else 1)
    for a, c in zip(cues, cues[1:]):
        g, lm = holonomy(path[a:c + 1], labels), lam(c - a, e)
        P *= lm * (toks[c] - 15 == g[toks[a] - 15]) + (1 - lm) / 3
    return {"fibre": fibre, "b": b, "q": q, "P": P, "rho": rho, "n": p["n"], "y": p["y"]}

def cue_normalised(q) -> tuple:
    return tuple(v / sum(q[15:18]) for v in q[15:18])

# ---- k-gram laws (API 3.8, Corollary 4') ----
def kgram_law(m: dict, k: int) -> dict:
    """Exact stationary law of (w_1..w_k) over reachable strings (prefix-shared DFS)."""
    Ts, E = [[(j, v) for j, v in enumerate(r) if v] for r in m["T"]], m["E"]
    cols, out = [[s for s in range(len(E)) if E[s][w]] for w in range(len(E[0]))], {}

    def dfs(alpha, prefix):
        for w, states in enumerate(cols):
            a = {s: alpha[s] for s in states if s in alpha}
            if not (tot := sum(a.values())):
                continue
            if len(prefix) + 1 == k:
                out[prefix + (w,)] = tot
                continue
            nxt = {}
            for s, v in a.items():
                for j, tv in Ts[s]:
                    nxt[j] = nxt.get(j, 0) + v * tv
            dfs(nxt, prefix + (w,))
    dfs(dict(enumerate(m["pi"])), ())
    return out

def five_gram(y: int, y2: int) -> tuple:
    return (15 + y, 10, 8, 9, 15 + y2)

# ---- gates (API 3.9) ----
_COVER_EXPECT = {"NA": ((1, 4, 0), 1), "ZC": ((1, 4, 0), 3), "AB": ((2, 5, 0), 3),
                 "TRIV": ((3, 6, 0), 3)}
_FLUX_EXPECT = {"NA": {"c"}, "AB": {"e"}, "ZC": {"e"}, "TRIV": {"e"}, "ETA1": {"c"},
                "GAUGE-NA": {"c", "c2"}, "GAUGE-TRIV": {"e"}, "GAUGE-COV": {"c", "c2"}}

def _passes(fn, *args) -> bool:
    try:
        fn(*args)
        return True
    except Exception:  # noqa: BLE001  (StageFailure/ProfileError: recorded as a failed check)
        return False
def _lift_ok(arm: str, T) -> bool:
    """Entrywise against the section 2.5 values; exact row and column sums."""
    e, tb, lab = eta(arm), t_base_exact(), edge_labels(arm)
    for (i, x), (j, x2) in itertools.product(itertools.product(range(N_V), range(3)), repeat=2):
        want = tb[i][j] * ((1 - e) * (x2 == lab[(i, j)][x]) + e / 3) if tb[i][j] else 0
        if T[state(i, x)][state(j, x2)] != want:
            return False
    return all(sum(r) == 1 for r in T) and all(sum(c) == 1 for c in zip(*T))

def gate_G0(spec=None) -> dict:
    spec = build_world() if spec is None else spec
    full, punct = tw.CubicalComplex(N_V, spec.cells), punctured_complex(spec)
    kf, tb, fs = np.asarray(kernel(spec)), to_float(t_base_exact()), f_star_index(spec)
    out = {"counts": tuple(len(spec.cells[k]) for k in (0, 1, 2)),
           "betti": {2: tuple(full.betti(2)), 3: tuple(full.betti(3))},
           "punctured": {"counts": tuple(len(punct.cells[k]) for k in (0, 1, 2)),
                         "chi": int(punct.euler_characteristic()), "betti": cover_betti(punct),
                         "closed": _passes(check_boundary_closed, punct),
                         "boundary_cycles": boundary_circles(punct)},
           "t_base_max_err": float(np.max(np.abs(kf - tb))),
           "t_base_support_ok": bool(np.array_equal(kf > 0, tb > 0)),
           "lift_ok": {}, "lift_max_err": {}, "validate_process": {}, "faces": {}, "flux": {},
           "cover": {}}
    pu, ok = out["punctured"], True
    for arm in ARMS:
        m = model(arm)
        out["lift_ok"][arm] = _lift_ok(arm, m["T"])
        out["lift_max_err"][arm] = max(float(np.max(np.abs(m[f] - to_float(m[k]))))
                                       for f, k in (("Tf", "T"), ("Ef", "E"), ("pif", "pi")))
        out["validate_process"][arm] = _passes(validate_process, m["Tf"], m["Ef"], m["pif"])
        faces = [perm_name(g) for g in face_holonomies(spec, m["labels"])]
        out["faces"][arm], out["flux"][arm] = faces, faces[fs]
        ok &= out["lift_ok"][arm] and out["validate_process"][arm]
        ok &= out["lift_max_err"][arm] <= TOL_STRUCT and faces[fs] in _FLUX_EXPECT[arm]
        ok &= all(f == "e" for k, f in enumerate(faces) if k != fs)
    for arm in ARMS_SEAM:
        cx = cover_complex(spec, edge_labels(arm))
        rec = out["cover"][arm] = {"counts": tuple(len(cx.cells[k]) for k in (0, 1, 2)),
                                   "betti": cover_betti(cx), "circles": boundary_circles(cx),
                                   "closed": _passes(check_boundary_closed, cx)}
        betti, circ = _COVER_EXPECT[arm]
        ok &= rec["counts"] == (48, 96, 45) and rec["betti"] == {2: betti, 3: betti}
        ok &= rec["circles"] == circ and rec["closed"]
    ok &= out["counts"] == (16, 32, 16) and out["betti"] == {2: (1, 2, 1), 3: (1, 2, 1)}
    ok &= pu["counts"] == (16, 32, 15) and pu["chi"] == -1 and pu["closed"]
    ok &= pu["betti"] == {2: (1, 2, 0), 3: (1, 2, 0)} and pu["boundary_cycles"] == 1
    ok &= out["t_base_max_err"] <= TOL_STRUCT and out["t_base_support_ok"]
    return {"status": "PASS" if ok else "FAIL", **out}

def _one_hot(kind: str) -> bool:
    M, ref = emission(kind), emission("E")
    if any(sorted(r) != [0] * (len(r) - 1) + [1] for r in M):
        return False
    want = {"E": lambda i, x: ref[state(i, x)][cue(x) if i == ANCHOR else tok(i)] == 1,
            "E_cov": lambda i, x: M[state(i, x)] == ref[state(i, inverse(H_COV[i])[x])],
            "E_nc": lambda i, x: M[state(i, x)][i] == 1,
            "E_sigma": lambda i, x: all(M[state(i, x)][sigma_tok(w)] == ref[state(i, x)][w]
                                        for w in range(V))}[kind]
    return all(want(i, x) for i, x in itertools.product(range(N_V), range(3)))

def gate_G1() -> dict:
    one_hot = {k: _one_hot(k) for k in EMISSIONS}
    bij = sorted(tok(i) for i in range(N_V) if i != ANCHOR) == list(range(15))
    laws = {k: [kgram_law(model(a), k) for a in ARMS_SEAM] for k in (1, 2, 3, 4)}
    kg_equal = {k: all(x == v[0] for x in v) and sum(v[0].values()) == 1 for k, v in laws.items()}
    five = {a: kgram_law(model(a), 5) for a in ARMS_SEAM}
    grams = [five_gram(y, y2) for y, y2 in itertools.product(range(3), range(3))]
    ratio = {f"{a}|{b}": max(max(five[a][g], five[b][g]) / min(five[a][g], five[b][g])
                             for g in grams) for a, b in itertools.combinations(ARMS_SEAM, 2)}
    ok = all(one_hot.values()) and bij and all(kg_equal.values())
    ok &= all(r > RATIO_5GRAM for r in ratio.values())
    return {"status": "PASS" if ok else "FAIL", "one_hot": one_hot, "tok_bijection": bij,
            "kgram_equal": kg_equal, "five_gram_ratio": ratio}
