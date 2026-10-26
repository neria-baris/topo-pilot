"""C2 statistics (the pre-allowlisted overflow module): GLS-REF, the 80-digit Decimal reference of
every projector problem accepted by the composed residual bound with verified inverse-norm
bounds (Lemmas GR, INV), the L1 decoders D0/D_code/D_lin with the explicit standardisation recipe
and the R13 equivalence check, the P1 ladder and the MDE reports (API.md §9; C2-FROZEN-v1 §2.5,
§6.6, §6.7, §9.2, §9.3 T12, T17).

Every Decimal operation runs in the context of dctx (correctly rounded, traps on); u_D is read
from the active context precision (API.md §19.1 E-3). The two solves of gls_ref go through the
module attribute dsolve at call time (E-4); the precision kernels through `precision` (E-13).
"""

from __future__ import annotations

import decimal
import operator
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_fit
import c2_code as ck
import numpy as np
import precision

from topo_pilot.analysis import x4f_scores
from topo_pilot.experiment.x4f_probe import nested_ridge
from topo_pilot.prediction.ridge import RidgeProbe

NUMERICAL, LINK = "EXCLUDED/NUMERICAL", "EXCLUDED/LINK"
TRAPS = (decimal.Overflow, decimal.Underflow, decimal.Subnormal, decimal.DivisionByZero)
TRAPS += (decimal.InvalidOperation,)
ZERO = Decimal(0)  # exact in every context
P1_SEEDS = {"R": ("val_p1_R_sd", "val_p1_R_c"), "M": ("val_p1_M_sd", "val_p1_M_c")}
P1_SEEDS["S*"] = ("val_p1_S_sd", "val_p1_S_c")
P1_ARRAYS = {"R": ("Z010", "Z050"), "S*": ("Z010", "Z050"), "M": ("Ztau",)}


# ---- Decimal kernels (§2.5; API.md §9.1) -----------------------------------------------------
def dctx(prec=80) -> decimal.Context:
    return decimal.Context(prec=int(prec), rounding=decimal.ROUND_HALF_EVEN, traps=list(TRAPS))


def D(M) -> list:
    """Exact Decimal(float) entries of a 2-d array."""
    return [[Decimal(float(x)) for x in row] for row in np.atleast_2d(np.asarray(M, float))]


def dmatmul(A, B) -> list:
    cols = list(zip(*B))
    return [[sum(map(operator.mul, r, c), ZERO) for c in cols] for r in A]


def dsub(A, B) -> list:
    return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]


def dabs(A) -> list:
    return [[abs(x) for x in r] for r in A]


def deye(n) -> list:
    return [[Decimal(int(i == j)) for j in range(n)] for i in range(n)]


def dT(A) -> list:
    return [list(r) for r in zip(*A)]


def frob(A) -> Decimal:
    return sum((x * x for r in A for x in r), ZERO).sqrt()


def inflate(x) -> Decimal:
    return x * (1 + Decimal(10) ** -70)


def deflate(x) -> Decimal:
    return x * (1 - Decimal(10) ** -70)


def theta(q) -> Decimal:
    """theta_q = q u_D / (1 - q u_D), u_D = 1/2 10^(1 - p) at the active precision p."""
    u = Decimal(5) * Decimal(10) ** (-decimal.getcontext().prec)
    t = int(q) * u
    return t / (1 - t)


def dsolve(A, Bm) -> list:
    """A^-1 Bm by Gauss-Jordan elimination with partial pivoting (largest |entry|, ties to the
    lowest index); a zero pivot raises the context's DivisionByZero/InvalidOperation trap."""
    n = len(A)
    M = [list(A[i]) + list(Bm[i]) for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        row = [x / p for x in M[c][c:]]
        M[c] = M[c][:c] + row
        for r in range(n):
            f = M[r][c]
            if r != c and f:
                M[r] = M[r][:c] + [x - f * y for x, y in zip(M[r][c:], row)]
    return [M[i][n:] for i in range(n)]


def dinverse(A) -> list:
    return dsolve(A, deye(len(A)))


def enclosure(R_tilde, fixed, left, right, q) -> Decimal:
    """Verified upper bound on ||R||_F of R = fixed - left right (inner dimension q), from the
    computed R_tilde: ||R_tilde|| + theta_{q+1} || |fixed| + |left||right| ||; without a fixed
    term, theta_q || |left||right| || (§2.5 (i)); every term inflated (ii)."""
    prod = dmatmul(dabs(left), dabs(right))
    if fixed is None:
        return inflate(theta(q) * frob(prod))
    bound = [[abs(a) + b for a, b in zip(r, s)] for r, s in zip(fixed, prod)]
    return inflate(frob(R_tilde)) + inflate(theta(q + 1) * frob(bound))


# ---- GLS-REF (Lemmas GR, INV; T12) -----------------------------------------------------------
def _ref(o, A, Gamma, B, PS_hat, PG_hat, euclidean) -> None:
    """The §2.5 steps in order; fills `o` (Decimal values as str)."""
    up = inflate
    Xn, nz = np.hstack((Gamma, B)), Gamma.shape[1]
    n, m = Xn.shape
    X, XT, BD, GD = D(Xn), dT(D(Xn)), D(B), D(Gamma)
    if euclidean:
        Y, e_Y = X, ZERO
        o["omega_A"] = "1"
    else:
        AD = D(A)
        Y = dsolve(AD, X)
        R_A = enclosure(dsub(dmatmul(AD, Y), X), X, AD, Y, n)
        VA = D(np.linalg.inv(np.asarray(A, dtype=np.float64)))
        th_A = enclosure(dsub(deye(n), dmatmul(VA, AD)), deye(n), VA, AD, n)
        o["theta_A"] = str(th_A)
        if not th_A < 1:
            return
        om_A = up(up(frob(VA)) / deflate(1 - th_A))
        e_Y = up(om_A * R_A)
        o["omega_A"] = str(om_A)
    G = dmatmul(XT, Y)
    R_C = enclosure(dsub(G, dmatmul(XT, Y)), G, XT, Y, n)
    YT = dT(Y)
    Ls = dsolve(G, YT)
    R_G = enclosure(dsub(dmatmul(G, Ls), YT), YT, G, Ls, m)
    VG = dinverse(G)
    nX, nVG, nL = up(frob(X)), up(frob(VG)), up(frob(Ls))
    e_G = up(up(nX * e_Y) + R_C)
    th_G = up(enclosure(dsub(deye(m), dmatmul(VG, G)), deye(m), VG, G, m) + up(nVG * e_G))
    o.update(theta_G=str(th_G), e_Y=str(e_Y))
    if not th_G < 1:
        return
    om_G = up(nVG / deflate(1 - th_G))
    e_L = up(om_G * up(up(R_G + up(R_C * nL)) + up(e_Y * up(1 + up(nX * nL)))))
    nL_low = deflate(frob(Ls))
    rho = up(e_L / nL_low)
    res = {}
    for tag, F, Lrows, q, hat in (
        ("S", BD, Ls[nz:], m - nz, PS_hat),
        ("G", GD, Ls[:nz], nz, PG_hat),
    ):
        P = dmatmul(F, Lrows)
        eps = up(up(up(frob(F)) * e_L) + enclosure(None, None, F, Lrows, q))
        dev = up(frob(dsub(D(hat), P)))
        delta = up(dev + eps)
        gate = delta <= Decimal(cc.GLSREF_PROJ) * deflate(frob(P))
        res[tag] = (eps, dev, delta, gate)
    o.update(omega_G=str(om_G), e_L=str(e_L), L_star_norm=str(nL_low), rho_ref=str(rho))
    for tag in ("S", "G"):
        eps, dev, delta, gate = res[tag]
        o.update({f"eps_P_{tag}": str(eps), f"dev_{tag}": str(dev)})
        o.update({f"delta_P_{tag}": str(delta), f"gate_{tag}": bool(gate)})
    o["accepted"] = bool(rho <= Decimal(cc.GLSREF_RHO))


KEYS = ("theta_A", "theta_G", "omega_A", "omega_G", "e_Y", "e_L", "L_star_norm", "rho_ref")
KEYS += ("eps_P_S", "eps_P_G", "dev_S", "dev_G", "delta_P_S", "delta_P_G")


def gls_ref(A, Gamma, B, P_S_hat, P_G_hat, euclidean=False, prec=80) -> dict:
    """GLS-REF of one projector problem (A = Sigma_eps; Euclidean: A = I, Y* = X_n). Accepted
    iff no trap, theta_A < 1 (GLS), theta_G < 1 and rho_ref <= 1e-20; status PASS iff accepted
    and both projector gates hold, else EXCLUDED/NUMERICAL (fail-closed)."""
    Gamma, B = np.asarray(Gamma, dtype=np.float64), np.asarray(B, dtype=np.float64)
    o = dict.fromkeys(KEYS)
    o.update(accepted=False, trap=None, gate_S=False, gate_G=False)
    o.update(n=int(Gamma.shape[0]), m=int(Gamma.shape[1] + B.shape[1]))
    with decimal.localcontext(dctx(prec)):
        try:
            _ref(o, A, Gamma, B, P_S_hat, P_G_hat, euclidean)
        except decimal.DecimalException as exc:
            o["accepted"], o["trap"] = False, type(exc).__name__
        except (np.linalg.LinAlgError, ValueError, ArithmeticError) as exc:
            o["accepted"], o["trap"] = False, f"{type(exc).__name__}: {exc}"
    ok = o["accepted"] and o["gate_S"] and o["gate_G"]
    o["status"] = "PASS" if ok else NUMERICAL
    return o


def delta_p(ref, tag="S") -> float:
    """delta_P as a float upper bound for the NUM guard (inf if not available)."""
    v = ref.get(f"delta_P_{tag}")
    return float(np.nextafter(float(Decimal(v)), np.inf)) if v is not None else float("inf")


# ---- L1 decoders (§6.6; API.md §9.2) ---------------------------------------------------------
@dataclass
class Decoder:
    mu_F: np.ndarray
    s_F: np.ndarray
    W: np.ndarray
    b: np.ndarray
    lam: float
    eq: float
    tol: float
    kappa: float

    def predict(self, F) -> np.ndarray:
        return ((np.asarray(F, dtype=np.float64) - self.mu_F) / self.s_F) @ self.W + self.b

    @property
    def ok(self) -> bool:
        return bool(self.eq <= self.tol)


FIELDS = ("mu_F", "s_F", "W", "b", "lam", "eq", "tol", "kappa")


def fit_decoder(F_fit, Y_fit, panel_fit) -> Decoder:
    """lambda* by nested_ridge (LOPO over the FIT panels; standardises internally), then
    RidgeProbe([lambda*]) on explicitly standardised features; FIT predictions compared with
    nested_ridge's within c1_fit.equivalence_tolerance (the R13 rule)."""
    F = np.asarray(F_fit, dtype=np.float64)
    Y = np.asarray(Y_fit, dtype=np.float64)
    res = nested_ridge(F, Y, np.asarray(panel_fit), F, Y, grid=cc.RIDGE_GRID)
    mu, s = x4f_scores.standardizer(F)
    Ft = (F - mu) / s
    probe = RidgeProbe([res.lam]).fit(Ft, Y, Ft, Y)
    pred = probe.predict(Ft)
    eq = float(np.max(np.abs(pred - np.asarray(res.pred_val).reshape(pred.shape))))
    tol, kappa = c1_fit.equivalence_tolerance(Ft, res.lam, pred)
    return Decoder(mu, s, probe.W, probe.b, float(res.lam), eq, float(tol), float(kappa))


def decoder_features(kind, w32, zt, code=None, full=None) -> np.ndarray:
    w = np.asarray(w32, dtype=np.int64)
    onehot = (w[:, None] == np.arange(cc.V)[None, :]).astype(np.float64)
    parts = [onehot, np.asarray(zt, dtype=np.float64)]
    extra = {"D0": None, "Dcode": code, "Dlin": full}[kind]
    if extra is not None:
        parts.append(np.asarray(extra, dtype=np.float64))
    return np.hstack(parts)


def decoder_arrays(dec) -> dict:
    return {k: np.asarray(getattr(dec, k)) for k in FIELDS}


def decoder_from_arrays(d) -> Decoder:
    vals = {k: np.asarray(d[k]) for k in FIELDS}
    for k in ("lam", "eq", "tol", "kappa"):
        vals[k] = float(vals[k])
    return Decoder(**vals)


def _sse(Y, pred) -> float:
    return float(np.sum((np.asarray(Y, np.float64) - np.asarray(pred, np.float64)) ** 2))


def l1(Y, pred0, pred_code, pred_lin) -> dict:
    """PASS iff SSE_0 > 0, SSE_0 - SSE_lin > 0, R2_code|0 >= 1/2 and rho_inc >= 9/10 (exact
    rationals of the float sums); an undefined denominator is a LINK failure (RC-3)."""
    s0, sc, sl = _sse(Y, pred0), _sse(Y, pred_code), _sse(Y, pred_lin)
    out = {"status": LINK, "SSE_0": s0, "SSE_code": sc, "SSE_lin": sl}
    out.update(R2_code_0=None, rho_inc=None)
    f0, fc, fl = Fraction(s0), Fraction(sc), Fraction(sl)
    if not f0 > 0:
        return out
    r2 = 1 - fc / f0
    out["R2_code_0"] = float(r2)
    if not f0 - fl > 0:
        return out
    rho = (f0 - fc) / (f0 - fl)
    out["rho_inc"] = float(rho)
    if r2 >= cc.L1_R2 and rho >= cc.L1_RHO:
        out["status"] = "PASS"
    return out


def l1_complete_scores(Y, preds, w32, class_means_fit) -> dict:
    """Descriptive R^2_X = 1 - SSE_X / sum ||f1 - f1-bar_w||^2 and R^2_code / R^2_lin."""
    w = np.asarray(w32, dtype=np.int64)
    sst = _sse(Y, np.asarray(class_means_fit)[w])
    out = {f"R2_{k}": 1.0 - _sse(Y, preds[k]) / sst for k in ("D0", "Dcode", "Dlin")}
    out["R2_code_over_lin"] = out["R2_Dcode"] / out["R2_Dlin"]
    return out


# ---- P1 ladder and MDE reports (§6.7; API.md §9.3) -------------------------------------------
def _cfg(alpha, alternative, N) -> dict:
    c = {"alpha": float(alpha), "power": float(cc.POWER), "delta": 0.0}
    return dict(c, alternative=float(alternative), projected_N=int(N))


def _summaries(arrays, afull, models, seeds, alpha, alternative) -> dict:
    """One sd_b4_draws call per array (4,096 VAL rows) and one centered_draws +
    precision_summary per ladder N."""
    sd_seed, c_seed = (cc.seed(s) for s in seeds)
    out = {}
    for name, X in arrays.items():
        X, r4n = {j: X[j] for j in models}, {j: afull[j] for j in models}
        kw = {"models": models, "draws": cc.VAL_DRAWS}
        sd, _ = precision.sd_b4_draws(X=X, r4n=r4n, seed=sd_seed, size=cc.BLOCK, **kw)
        out[name] = {}
        for N in cc.N_LADDER:
            e = precision.centered_draws(X=X, seed=c_seed, size=N, **kw)
            out[name][N] = precision.precision_summary(sd, e, models, _cfg(alpha, alternative, N))
    return out


def p1(family, arrays, afull, models, alpha) -> dict:
    """N_F = the smallest N at which every model passes every gated array; else the smallest N
    at which >= 2 pass (the others PRECISION_LIMITED); else INCONCLUSIVE/UNDERPOWERED."""
    models = list(models)
    alternative = 0.10 * min(float(np.mean(afull[j])) for j in models)
    gated = {k: arrays[k] for k in P1_ARRAYS[family]}
    summ = _summaries(gated, afull, models, P1_SEEDS[family], alpha, alternative)
    passing = {}
    for N in cc.N_LADDER:
        ok = set(models)
        for name in gated:
            per = summ[name][N]["models"]
            good = (
                per[j]["mde_upper"] <= alternative and per[j]["power"] >= cc.POWER for j in models
            )
            ok &= {j for j, g in zip(models, good) if g}
        passing[N] = sorted(ok)
    full = [N for N in cc.N_LADDER if len(passing[N]) == len(models)]
    two = [N for N in cc.N_LADDER if len(passing[N]) >= 2]
    N_F = full[0] if full else two[0] if two else None
    limited = [j for j in models if N_F is not None and j not in passing[N_F]]
    status = "PASS" if N_F is not None else "INCONCLUSIVE/UNDERPOWERED"
    out = {"N_F": N_F, "pass": passing, "status": status, "precision_limited": limited}
    return dict(out, summaries=summ, alternative=alternative)


def mde_report(arrays, models, seed_sd, seed_c, alpha) -> dict:
    """The same kernels for the arrays that are reported only (energy, M share); seeds by
    CONTRACT name; afull is not used (the SD stream's r4 input is the array itself)."""
    models = list(models)
    first = next(iter(arrays.values()))
    summ = _summaries(arrays, first, models, (seed_sd, seed_c), alpha, 0.0)
    return {
        name: {N: {j: s["models"][j]["mde_upper"] for j in models} for N, s in by.items()}
        for name, by in summ.items()
    }


def n_test(N_by_family) -> tuple:
    N = max(int(v) for v in N_by_family.values())
    return N, N // cc.BLOCK


# ---- compositions used by the driver (F1, L1 on a split) -------------------------------------
def f1_problem(Y, w32, zt, f, euclidean=False, fit=None) -> dict:
    """c2_code.problem plus GLS-REF (only when the float part passed): F1 of one problem."""
    pr = ck.problem(Y, w32, zt, f, euclidean=euclidean, fit=fit)
    pr["ref"] = None
    if pr["status"] == "PASS":
        fit, g = pr["fit"], pr["g"]
        A = np.eye(fit["p"]) if euclidean else pr["Sigma"]
        pr["ref"] = gls_ref(A, fit["Gamma"], fit["B"], g["P_S"], g["P_G"], euclidean=euclidean)
        pr["status"] = pr["ref"]["status"]
    return pr


KINDS = ("D0", "Dcode", "Dlin")


def fit_decoders(w32, zt, code, full, target, panel) -> dict:
    return {
        k: fit_decoder(decoder_features(k, w32, zt, code=code, full=full), target, panel)
        for k in KINDS
    }


def l1_split(decs, w32, zt, code, full, target) -> dict:
    """The frozen FIT decoders scored on another split's natural rows (FEAS, TEST)."""
    pred = {k: decs[k].predict(decoder_features(k, w32, zt, code=code, full=full)) for k in KINDS}
    return dict(l1(target, pred["D0"], pred["Dcode"], pred["Dlin"]), preds=pred)
