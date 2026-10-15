"""X2a stage 0, part 1 (X2A-FROZEN-v1; API.md): construction, exact k <= 4 enumeration, closed
forms, stencil filter, gates G0-G2. Local unregistered torus builder; point_distances is never
called."""

from __future__ import annotations

import math
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path
from typing import ClassVar

import numpy as np

REPO = Path(__file__).resolve().parents[2]
_EXTRA = (Path(__file__).resolve().parent, REPO / "tools" / "x4_oracle_profile",
          REPO / "tests" / "oracle_profile")
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]

from oracle_profile import validate_process  # noqa: E402  (job-0014, unchanged)
from scipy.special import expit, logsumexp  # noqa: E402

import topo_pilot.world as tw  # noqa: E402
from topo_pilot.process import TransitionBuilder, TransitionConfig  # noqa: E402
from topo_pilot.process.emission import axis_state_perm, draw_axis_permutation  # noqa: E402
from topo_pilot.world.complex import check_boundary_closed  # noqa: E402
from topo_pilot.world.metrics import check_flat_bounds  # noqa: E402

N_SIDE, N, N_MIX, V = 12, 144, 288, 36
SIGMA, P_STAY, ALPHA = 1.25, 0.2, 0.2
T_STAR, K_S, WINDOWS, BLOCK, N_BLOCKS = 32, 8, (1, 2, 4, 8), 8, 4
TAU, Z99, MASTER_X2A0, FAMILY = 1e-12, 2.576, 20261015, "_x2a_torus_local"
BASE_COMMIT = "c364f95e5573940cdc24b569b0fb7c6a16c97ab8"
REQUEST_SHA256 = "4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595"
PROTOCOL_SHA256 = "C80808CB7F22D9A171385FCB1AB7D03973E80DAFE638DFA758B6A84CA8341939"
VARIANTS = ("main", "N-iso", "N-same", "N-id", "N-swap", "P-ref", "N-local")
EXACT_VARIANTS = ("main", "N-iso", "N-same", "P-ref", "N-local")
LN2 = math.log(2.0)
_X, _Y = np.divmod(np.arange(N), N_SIDE)
HAND = {"p(d)": [0.589233, 0.310698, 0.0863856, 0.0126647, 0.000979, 0.0000399],
        "Z": 1.566641, "G": [0.902705, 0.769235, 0.475989, 0.213878, 0.069815, 0.016887, 0.005687],
        "delta_rep": 0.010267, "P_A_repeat": 0.179622, "P_B_repeat": 0.169355,
        "JS_repeat_nats": 9.149e-5, "min_E_A": 1.6e-9, "reading_variance": 1.56246,
        "S_A": 0.0707764, "S_N": 0.0573220, "e0_sq": 0.902705, "Ke0_sq": 0.716659,
        "P_N_repeat": 0.145669}

def state(x, y):
    return N_SIDE * (x % N_SIDE) + (y % N_SIDE)

def token(a, b):
    return 6 * a + b

def delta12(u, v):
    d = np.abs(np.asarray(u, dtype=np.float64) - np.asarray(v, dtype=np.float64)) % N_SIDE
    return np.minimum(d, N_SIDE - d)

class _X2aTorusBuilder(tw.QuotientLatticeBuilder):  # deliberately NOT @register_world (§2.1)
    family: ClassVar[str] = FAMILY
    expected_betti: ClassVar[dict] = {2: (1, 2, 1), 3: (1, 2, 1)}
    identifications: ClassVar[tuple] = (tw.Identification(0, "periodic"),
                                        tw.Identification(1, "periodic"))

def build_world():
    spec = _X2aTorusBuilder().build(tw.WorldConfig(FAMILY, (N_SIDE, N_SIDE), "flat"))
    spec.validate()
    check_boundary_closed(tw.CubicalComplex(spec.n_states, spec.cells))
    check_flat_bounds(spec.dist, spec.dist_graph, 2)
    return spec

def kernel(spec):
    return TransitionBuilder().build(spec, TransitionConfig(p_stay=P_STAY)).T

def field_e():
    w = np.exp(-delta12(np.arange(N_SIDE)[:, None], 0.5 + 2 * np.arange(6)[None, :]) ** 2
               / (2 * SIGMA**2))
    return w / w.sum(axis=1, keepdims=True)

def emission_A(e=None):
    e = field_e() if e is None else e
    return np.einsum("xa,yb->xyab", e, e).reshape(N, V)

def _perm(dx_of):
    return (N_SIDE * ((_X + dx_of) % N_SIDE) + _Y).astype(np.int64)

def dehn_perm():
    return _perm(_Y)

def iso_perm():
    return _perm(1)

def emission_local(E_A):
    return 0.75 * E_A + 0.125 * E_A[_perm(2)] + 0.125 * E_A[_perm(-2)]

def emission_pref(spec, E_A):
    sx, sy = draw_axis_permutation(spec)
    perm = axis_state_perm(sx, sy, (N_SIDE, N_SIDE))
    return E_A[perm], sx, sy, perm

def mixture(T, E1, E2):
    n = T.shape[0]
    Z = np.zeros((n, n))
    return np.block([[T, Z], [Z, T]]), np.vstack((E1, E2)), np.full(2 * n, 1.0 / (2 * n))

def variant_model(variant, spec=None):
    spec = build_world() if spec is None else spec
    T, EA = kernel(spec), emission_A()
    EB, extra = EA[dehn_perm()], {}
    flat = np.full((N, V), 1.0 / V)
    if variant == "P-ref":
        EP, sx, sy, perm = emission_pref(spec, EA)
        extra = {"sx": sx, "sy": sy, "state_perm": perm}
    blocks = {"main": lambda: (EA, EB), "N-iso": lambda: (EA, EA[iso_perm()]),
              "N-same": lambda: (EA, EA.copy()), "N-id": lambda: (flat, flat.copy()),
              "N-swap": lambda: (EB, EA), "P-ref": lambda: (EA, EP),
              "N-local": lambda: (EA, emission_local(EA))}
    if variant not in blocks:
        raise ValueError(f"unknown variant {variant!r}")
    E1, E2 = blocks[variant]()
    Tt, Et, pit = mixture(T, E1, E2)
    return {"spec": spec, "T": T, "E1": E1, "E2": E2, "Tt": Tt, "Et": Et, "pit": pit, **extra}

# ---- exact enumeration (§4.1) ----------------------------------------------------------------
def window_law(T, E, k):
    T, E = np.asarray(T, dtype=np.float64), np.asarray(E, dtype=np.float64)
    n = T.shape[0]
    alpha = E.T / n  # [V, n]: alpha[w1, z] = u(z) E(z, w1)
    if k == 1:
        return alpha.sum(axis=1)
    for _ in range(k - 2):
        alpha = ((alpha @ T)[:, None, :] * E.T[None, :, :]).reshape(-1, n)
    return ((alpha @ T) @ E).reshape(-1)

def js_phi(r):
    r = np.atleast_1d(np.asarray(r, dtype=np.float64))
    out, small = np.empty_like(r), np.abs(r) < 1e-3
    r2 = r[small] ** 2
    out[small] = r2 / 2 + r2**2 / 12 + r2**3 / 30 + r2**4 / 56
    rb = r[~small]
    with np.errstate(divide="ignore", invalid="ignore"):
        big = 0.5 * ((1 + rb) * np.log1p(rb) + (1 - rb) * np.log1p(-rb))
    big[np.abs(rb) == 1.0] = LN2
    out[~small] = big
    return out

def js_information(PA, PB):
    PA = np.ravel(np.asarray(PA, dtype=np.float64))
    PB = np.ravel(np.asarray(PB, dtype=np.float64))
    M, keep = 0.5 * (PA + PB), (PA + PB) > 0
    terms = M[keep] * js_phi((PA[keep] - PB[keep]) / (PA[keep] + PB[keep]))
    chunks = np.array_split(terms, max(1, terms.size // V))
    return math.fsum(math.fsum(c.tolist()) for c in chunks)

def bayes_accuracy(PA, PB):
    return math.fsum(np.maximum(np.ravel(PA), np.ravel(PB)).tolist()) / 2

def exact_curve(T, E1, E2, kmax=4):
    out = {"I": [], "acc": []}
    for k in range(1, kmax + 1):
        PA, PB = window_law(T, E1, k), window_law(T, E2, k)
        out["I"].append(js_information(PA, PB))
        out["acc"].append(bayes_accuracy(PA, PB))
    return out

def G_overlap(e, d):
    return float(np.dot(e[:, 0], np.roll(e[:, 0], -d)))

def delta_rep_closed(e):
    return ALPHA / 2 * G_overlap(e, 1) * (G_overlap(e, 0) - G_overlap(e, 1))

def pair_law(T, E):
    return E.T @ T @ E / T.shape[0]

# ---- stencil reference filter (§5.4 G3.1): never forms T -------------------------------------
def _stencil(E, tok):
    R, P = tok.shape
    Eg, a = E.reshape(N_SIDE, N_SIDE, -1), np.full((R, N_SIDE, N_SIDE), 1.0 / N)
    b, le, acc = np.empty((R, P, N)), np.empty((R, P)), np.zeros(R)
    for t in range(P):
        if t:
            a = 0.2 * (a + np.roll(a, 1, 1) + np.roll(a, -1, 1) + np.roll(a, 1, 2)
                       + np.roll(a, -1, 2))
        a = a * np.moveaxis(Eg[:, :, tok[:, t]], 2, 0)
        m = a.sum(axis=(1, 2))
        acc, a = acc + np.log(m), a / m[:, None, None]
        b[:, t], le[:, t] = a.reshape(R, N), acc
    return b, le

def stencil_filter(E1, E2, tokens):
    tok = np.asarray(tokens, dtype=np.int64)
    (bA, lA), (bB, lB) = _stencil(E1, tok), _stencil(E2, tok)
    pi, qa = expit(lB - lA), expit(lA - lB)
    b = np.concatenate((qa[..., None] * bA, pi[..., None] * bB), axis=-1)
    return {"b": b, "pi": pi, "llr": lB - lA,
            "log_evidence": np.logaddexp(lA[:, -1], lB[:, -1]) - LN2}

# ---- gates G0-G2 ---------------------------------------------------------------------------
def _status(checks):
    return "PASS" if all(bool(v) for v in checks.values()) else "FAIL"

def _fraction_T():
    nb = {(state(x, y), state(x + dx, y + dy)) for x in range(N_SIDE) for y in range(N_SIDE)
          for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))}
    return nb

def gate_G0(spec, T):
    cx = tw.CubicalComplex(spec.n_states, spec.cells)
    counts = {k: len(cx.cells.get(k, ())) for k in (0, 1, 2)}
    dd = abs(cx.boundary_matrix(1) @ cx.boundary_matrix(2)).max()
    deg = np.bincount(np.asarray(spec.edges).ravel(), minlength=N)
    support = _fraction_T()
    err = max(abs(Fr(float(T[i, j])) - (Fr(1, 5) if (i, j) in support else 0))
              for i in range(N) for j in range(N))
    m = variant_model("main", spec)
    Tt, pit = m["Tt"], m["pit"]
    try:
        vp = validate_process(Tt, m["Et"], pit, tol=1e-12)
    except Exception as exc:  # noqa: BLE001  a failed process check is a G0 FAIL (S3)
        vp = {"error": repr(exc)}
    vals = {"counts": counts, "euler": cx.euler_characteristic(), "betti_2": cx.betti(2),
            "betti_3": cx.betti(3), "d1d2_max": float(dd), "deg_min": int(deg.min()),
            "deg_max": int(deg.max()), "T_fraction_err": float(err),
            "stationarity_err": float(np.abs(pit @ m["Tt"] - pit).max()), "validate_process": vp}
    checks = {
        "counts": counts == {0: 144, 1: 288, 2: 144}, "euler": vals["euler"] == 0,
        "betti": vals["betti_2"] == (1, 2, 1) and vals["betti_3"] == (1, 2, 1),
        "boundary_closed": dd == 0, "degree_4": vals["deg_min"] == vals["deg_max"] == 4,
        "T_fraction": err <= Fr(1, 10**15), "T_symmetric": bool(np.array_equal(T, T.T)),
        "T_support": {tuple(ij) for ij in np.argwhere(T > 0).tolist()} == support,
        "blockdiag": bool(np.array_equal(Tt[:N, :N], T) and np.array_equal(Tt[N:, N:], T)
                          and not Tt[:N, N:].any() and not Tt[N:, :N].any()),
        "stationary": vals["stationarity_err"] <= 1e-15, "validate_process": "error" not in vp}
    return {"status": _status(checks), "checks": checks, **vals}

def _brute_E_A():
    c = 0.5 + 2 * np.arange(6)
    cx, cy = np.repeat(c, 6), np.tile(c, 6)
    sh = 12.0 * np.array([-1, 0, 1])
    dx = (_X[:, None, None] - cx[None, :, None] + sh[None, None, :]) ** 2
    dy = (_Y[:, None, None] - cy[None, :, None] + sh[None, None, :]) ** 2
    d2 = np.min(dx[:, :, :, None] + dy[:, :, None, :], axis=(2, 3))  # minimum over 9 images
    logit = -d2 / (2 * SIGMA**2)
    return np.exp(logit - logsumexp(logit, axis=1, keepdims=True))

def gate_G1(models):
    m, EA = models["main"], models["main"]["E1"]
    EB, EN, EP = m["E2"], models["N-local"]["E2"], models["P-ref"]["E2"]
    ref = _brute_E_A()
    ab = np.abs(EA - ref)
    A4 = EA.reshape(12, 12, 6, 6)
    eq_x = np.abs(np.roll(np.roll(A4, -2, 0), -1, 2) - A4).max()
    eq_y = np.abs(np.roll(np.roll(A4, -2, 1), -1, 3) - A4).max()
    phi = dehn_perm()
    edges = {tuple(sorted(e)) for e in np.asarray(m["spec"].edges).tolist()}
    mapped = {tuple(sorted((int(phi[i]), int(phi[j])))) for i, j in edges}
    loc = 0.75 * EA + 0.125 * np.roll(EA.reshape(12, 12, V), -2, 0).reshape(N, V) \
        + 0.125 * np.roll(EA.reshape(12, 12, V), 2, 0).reshape(N, V)
    A4s = EA.reshape(N, 6, 6)
    chan = 0.75 * A4s + 0.125 * np.roll(A4s, 1, 1) + 0.125 * np.roll(A4s, -1, 1)
    rows = {k: float(np.abs(M.sum(1) - 1).max()) for k, M in
            {"E_A": EA, "E_B": EB, "E_N": EN, "E_P": EP}.items()}
    four = {"E_A": EA, "E_B": EB, "E_N": EN, "E_P": EP}
    vals = {"E_A_abs_err": float(ab.max()), "E_A_rel_err": float((ab / ref).max()),
            "row_sum_err": rows, "min_entry": {k: float(M.min()) for k, M in four.items()},
            "equivariance_x": float(eq_x), "equivariance_y": float(eq_y),
            "edges_preserved_by_phi": len(edges & mapped),
            "E_N_err": float(np.abs(EN - loc).max()),
            "E_N_channel_err": float(np.abs(EN - chan.reshape(N, V)).max())}
    checks = {
        "E_A_min_image": vals["E_A_abs_err"] <= 1e-15 and vals["E_A_rel_err"] <= 1e-12,
        "row_sums": max(rows.values()) <= 1e-14,
        "positive": min(vals["min_entry"].values()) > 0,
        "equivariance": max(eq_x, eq_y) <= 1e-15,
        "E_B_bitwise": bool(np.array_equal(EB, EA[phi])),
        "E_B_row_multiset": bool(np.array_equal(np.sort(EA, 0), np.sort(EB, 0))),
        "phi_bijection": bool(np.array_equal(np.sort(phi), np.arange(N))),
        "phi_not_automorphism": (state(0, 0), state(1, 1)) not in edges
        and int(phi[state(0, 1)]) == state(1, 1) and int(phi[state(0, 0)]) == state(0, 0),
        "Et_blocks": bool(np.array_equal(m["Et"][:N], EA) and np.array_equal(m["Et"][N:], EB)),
        "E_P_bitwise": bool(np.array_equal(EP, EA[models["P-ref"]["state_perm"]])),
        "E_P_multiset": bool(np.array_equal(np.sort(EA, 0), np.sort(EP, 0))),
        "E_N_formula": vals["E_N_err"] <= 1e-15, "E_N_channel": vals["E_N_channel_err"] <= 1e-15}
    return {"status": _status(checks), "checks": checks, **vals}

def _translate(law, k, da, db):
    a, b = np.divmod(np.arange(V), 6)
    p = 6 * ((a + da) % 6) + (b + db) % 6
    L = law.reshape((V,) * k)
    for ax in range(k):
        L = np.take(L, p, axis=ax)
    return L.reshape(-1)

def _hand(models):
    e, T = field_e(), models["main"]["T"]
    g = e[:, 0]
    Lg = 0.6 * g + 0.2 * np.roll(g, 1) + 0.2 * np.roll(g, -1)
    Kg = 0.75 * g + 0.125 * np.roll(g, 2) + 0.125 * np.roll(g, -2)
    LKg = 0.6 * Kg + 0.2 * np.roll(Kg, 1) + 0.2 * np.roll(Kg, -1)
    pa, pb = (float(np.trace(pair_law(T, models["main"][k]))) for k in ("E1", "E2"))
    m = (pa + pb) / 2
    js = 0.5 * sum(p * math.log(p / m) + (1 - p) * math.log((1 - p) / (1 - m)) for p in (pa, pb))
    w = np.exp(-(np.arange(6) + 0.5) ** 2 / (2 * SIGMA**2))
    return {"p(d)": (w / w.sum()).tolist(), "Z": float(w.sum()),
            "G": [G_overlap(e, d) for d in range(7)], "delta_rep": delta_rep_closed(e),
            "P_A_repeat": pa, "P_B_repeat": pb, "JS_repeat_nats": js,
            "min_E_A": float(emission_A().min()),
            "reading_variance": float((w / w.sum() * (np.arange(6) + 0.5) ** 2).sum()),
            "S_A": float(g @ Lg / 12), "S_N": float(Kg @ LKg / 12), "e0_sq": float(g @ g),
            "Ke0_sq": float(Kg @ Kg),
            "P_N_repeat": float(np.trace(pair_law(T, models["N-local"]["E2"])))}

def gate_G2(models):
    m, e = models["main"], field_e()
    T, EA, EB = m["T"], m["E1"], m["E2"]
    exact = {v: exact_curve(T, models[v]["E1"], models[v]["E2"]) for v in EXACT_VARIANTS}
    Im = exact["main"]["I"]
    MA, MB = pair_law(T, EA), pair_law(T, EB)
    Tu = np.zeros((N, N))
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (1, 1), (-1, -1)):
        Tu[np.arange(N), state(_X + dx, _Y + dy)] = 0.2
    col = {k: float(np.abs(M.sum(0) - 4).max()) for k, M in
           {"E_A": EA, "E_B": EB, "E_N": models["N-local"]["E2"],
            "E_P": models["P-ref"]["E2"]}.items()}
    PA1, PB1 = window_law(T, EA, 1), window_law(T, EB, 1)
    trans = 0.0
    for k in range(1, 5):
        for E in (EA, EB):
            law = window_law(T, E, k)
            for da in range(6):
                for db in range(6):
                    trans = max(trans, float(np.max(np.abs(_translate(law, k, da, db) - law)
                                                    / law)))
    dtr, closed = float(np.trace(MA) - np.trace(MB)), delta_rep_closed(e)
    js2 = js_information(MA, MB)
    vals = {"exact": exact, "column_sum_err": col, "pi1_dev": float(np.abs(PB1 / (PA1 + PB1)
                                                                          - 0.5).max()),
            "trace_diff": dtr, "delta_rep_closed": closed,
            "lemma_U_err": float(np.abs(MB - EA.T @ Tu @ EA / N).max()),
            "translation_rel_err": trans, "I2_vs_JS_pair_rel": abs(Im[1] - js2) / js2,
            "steps": [Im[k + 1] - Im[k] for k in range(3)], "hand": HAND, "computed": _hand(models)}
    checks = {"T1_columns": max(col.values()) <= 1e-12, "T1_pi1": vals["pi1_dev"] <= 1e-14,
              "I1": Im[0] <= 1e-15, "T2_closed": abs(dtr - closed) <= 1e-14 and dtr > 0,
              "lemma_U": vals["lemma_U_err"] <= 1e-15, "translations": trans <= 1e-12,
              "monotone": min(vals["steps"]) >= -1e-15, "I2_positive": Im[1] > 0,
              "I2_JS_pair": vals["I2_vs_JS_pair_rel"] <= 1e-10}
    return {"status": _status(checks), "checks": checks, **vals}

# ---- shared helpers for the runner (x2a_ph.run) ----------------------------------------------
def _git(*args):
    p = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()

def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    return x.tolist() if isinstance(x, np.ndarray) else x
