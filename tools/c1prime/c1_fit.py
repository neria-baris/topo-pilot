"""C1' FWL phase map, forced states, within-class whitening, Haar control frames, M1 identities
and fixed decoders (API.md §9; protocol §5.2-§5.5, §6, §7). Calibration fits only."""

from __future__ import annotations

from dataclasses import dataclass

import c1_config  # noqa: F401  (sys.path)
import numpy as np
from c1_records import C1GateFailure

from topo_pilot.analysis import x4f_scores as xs
from topo_pilot.contracts import SeedTree
from topo_pilot.experiment.x4f_probe import nested_ridge
from topo_pilot.prediction.ridge import RidgeProbe

GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)
N_FEATURES, BW_ROWS = 2048, 1024


def standardise_nuisance(z_cal) -> tuple:
    z = np.asarray(z_cal, dtype=np.float64)
    sd = z.std(axis=0)
    return z.mean(axis=0), np.where(sd > 0, sd, 1.0)


def unit(phi) -> np.ndarray:
    phi = np.asarray(phi, dtype=np.float64)
    return np.column_stack((np.cos(phi), np.sin(phi)))


def fwl_design(w32, zt, f) -> np.ndarray:
    w32 = np.asarray(w32, dtype=np.int64)
    onehot = (w32[:, None] == np.arange(36)[None, :]).astype(np.float64)
    return np.hstack((onehot, np.asarray(zt, dtype=np.float64), np.asarray(f, dtype=np.float64)))


def fit_fwl(a, w32, zt, phi) -> dict:
    X = fwl_design(w32, zt, unit(phi))
    coef, _, rank, sv = np.linalg.lstsq(X, np.asarray(a, dtype=np.float64), rcond=None)
    cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
    B = coef[39:41].T
    sv_B = np.linalg.svd(B, compute_uv=False)
    return {"alpha": coef[:36], "Gamma": coef[36:39], "B": B, "rank": int(rank), "cond": cond,
            "sv_B": sv_B}


def f1_check(fit) -> str:
    s = fit["sv_B"]
    ok = fit["rank"] == 41 and fit["cond"] <= 1e8 and s[0] > 0 and s[-1] / s[0] >= 1e-6
    return "PASS" if ok else "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"


def partial_r2(a, w32, zt, phi) -> float:
    """Within-class partial R^2 of f(phi) (reported, not gated)."""
    a = np.asarray(a, dtype=np.float64)
    base = fwl_design(w32, zt, np.zeros((len(a), 0)))
    full = fwl_design(w32, zt, unit(phi))
    rss = (lambda X: float(np.sum((a - X @ np.linalg.lstsq(X, a, rcond=None)[0]) ** 2)))  # noqa
    r0 = rss(base)
    return 1.0 - rss(full) / r0 if r0 > 0 else float("nan")


def forced(a, B, phi_s, phi_d) -> np.ndarray:
    return np.asarray(a, dtype=np.float64) + (unit(phi_d) - unit(phi_s)) @ np.asarray(B).T


def residual(a, w32, zt, fit) -> np.ndarray:
    return np.asarray(a, dtype=np.float64) - fit["alpha"][np.asarray(w32, dtype=np.int64)] \
        - np.asarray(zt, dtype=np.float64) @ fit["Gamma"]


def whitening(r_cal) -> dict:
    mean, S = xs.ledoit_wolf(r_cal)
    lam, vec = np.linalg.eigh(S)
    status = "PASS" if lam[0] > 1e-12 * lam[-1] else "INCONCLUSIVE/SUPPORT_DEGENERATE"
    if status != "PASS":
        return {"status": status, "mean": mean, "Sigma": S, "eig": lam}
    W = (vec / np.sqrt(lam)) @ vec.T
    W_inv = (vec * np.sqrt(lam)) @ vec.T
    return {"status": status, "mean": mean, "Sigma": S, "W": W, "W_inv": W_inv, "eig": lam}


def qr_pos(M) -> np.ndarray:
    Q, R = np.linalg.qr(np.asarray(M, dtype=np.float64))
    return Q * np.sign(np.diag(R))[None, :]


def primary_coords(W, B, Delta) -> tuple:
    Qt = qr_pos(np.asarray(W) @ np.asarray(B))
    return Qt, (np.asarray(Delta) @ np.asarray(W).T) @ Qt


def haar_frames(model_seed, count=32) -> list:
    tree = SeedTree(0)
    return [qr_pos(tree.generator("c1-sf-v1", "frame", int(model_seed), r)
                   .standard_normal((128, 2))) for r in range(int(count))]


def control_delta(W_inv, Q_r, c) -> np.ndarray:
    return (np.asarray(c) @ np.asarray(Q_r).T) @ np.asarray(W_inv).T


def _rel_norm(primary, other) -> float:
    if primary > 0:
        return abs(other - primary) / primary
    return 0.0 if other == 0 else float("inf")


def _spectrum_dev(S_p, S_r) -> float:
    ep, er = np.sort(np.linalg.eigvalsh(S_p)), np.sort(np.linalg.eigvalsh(S_r))
    denom = float(np.max(np.abs(ep)))
    if denom > 0:
        return float(np.max(np.abs(ep - er))) / denom
    return 0.0 if not np.any(S_p) and not np.any(S_r) else float("inf")


def m1_report(W, Delta_pm, Qt, frames, c_pm, W_inv=None) -> dict:
    W = np.asarray(W)
    W_inv = np.linalg.inv(W) if W_inv is None else np.asarray(W_inv)
    norm_dev, spec_dev, ortho = 0.0, 0.0, 0.0
    c_all = np.vstack(c_pm)
    centred = c_all - c_all.mean(axis=0)
    for Delta, c in zip(Delta_pm, c_pm):
        primary = np.linalg.norm(np.asarray(Delta) @ W.T, axis=1)
        zero = primary == 0
        if np.any(np.asarray(c)[zero] != 0):
            norm_dev = float("inf")  # zero primary norm requires exactly zero coordinates
        for Q in frames:
            ctrl = control_delta(W_inv, Q, c)
            if np.any(ctrl[zero] != 0):
                norm_dev = float("inf")
            other = np.linalg.norm(ctrl @ W.T, axis=1)
            norm_dev = max(norm_dev, max((_rel_norm(p, o) for p, o, z in
                                          zip(primary, other, zero) if not z), default=0.0))
    for Q in frames:
        ortho = max(ortho, float(np.max(np.abs(Q.T @ Q - np.eye(Q.shape[1])))))
        for C in (c_all, centred):
            S = C.T @ C
            spec_dev = max(spec_dev, _spectrum_dev(Qt @ S @ Qt.T, Q @ S @ Q.T))
    ok = norm_dev <= 1e-10 and spec_dev <= 1e-10 and ortho <= 1e-12
    return {"norm_rel_dev": norm_dev, "spectrum_rel_dev": spec_dev, "orthonormality": ortho,
            "status": "PASS" if ok else "FAIL_TECHNICAL"}


@dataclass
class Decoder:
    mu_a: np.ndarray
    s_a: np.ndarray
    omega: np.ndarray
    b: np.ndarray
    mu_F: np.ndarray
    s_F: np.ndarray
    probe: RidgeProbe
    lam: float
    equivalence: float
    eq_tol: float = 1e-10
    kappa: float = float("nan")

    def features(self, a) -> np.ndarray:
        return xs.rbf_features((np.asarray(a, dtype=np.float64) - self.mu_a) / self.s_a,
                               self.omega, self.b)

    def predict(self, a) -> np.ndarray:
        return self.probe.predict((self.features(a) - self.mu_F) / self.s_F)


EQ_C = 64.0  # ruling R13 (job 0042): forward-error constant for the solver-equivalence check


def equivalence_tolerance(Ft, lam, pred) -> tuple:
    """R13: the M1 cho_solve-vs-lstsq tolerance. Both solvers are backward stable on the same
    normal equations (Xc'Xc + λI) w = Xc'Y, so their predictions may differ by at most about
    c·ε·κ₂(Xc'Xc + λI)·‖pred‖∞ (Higham, forward error of a backward-stable solve). Returns
    (max(1e-10, EQ_C·ε·κ·‖pred‖∞), κ): the frozen 1e-10 when well conditioned, else the
    floating-point floor; a genuine implementation mismatch (O(1) differences) still fails."""
    Xc = np.asarray(Ft, dtype=np.float64) - np.mean(Ft, axis=0)
    ev = np.linalg.eigvalsh(Xc.T @ Xc + float(lam) * np.eye(Xc.shape[1]))
    kappa = float(ev[-1] / ev[0]) if ev[0] > 0 else float("inf")
    scale = float(np.max(np.abs(pred))) if np.size(pred) else 0.0
    return max(1e-10, EQ_C * float(np.finfo(np.float64).eps) * kappa * scale), kappa


def fit_decoder(a_cal, Y_cal, panel_cal, model_seed, target) -> Decoder:
    tree = SeedTree(0)
    mu_a, s_a = xs.standardizer(a_cal)
    at = (np.asarray(a_cal, dtype=np.float64) - mu_a) / s_a
    ell, why = xs.rbf_bandwidth(at, tree.generator("c1-sf-v1", "rbf_bandwidth", int(model_seed),
                                                   target), BW_ROWS)
    if ell is None:
        raise C1GateFailure("INCONCLUSIVE/RBF_DEGENERATE", f"{target}: {why}")
    omega, b = xs.rbf_map(at.shape[1], N_FEATURES, ell,
                          tree.generator("c1-sf-v1", "rbf", int(model_seed), target))
    Fc = xs.rbf_features(at, omega, b)
    Y = np.asarray(Y_cal, dtype=np.float64)
    res = nested_ridge(Fc, Y, np.asarray(panel_cal), Fc, Y, grid=GRID)
    mu_F, s_F = xs.standardizer(Fc)
    Ft = (Fc - mu_F) / s_F
    probe = RidgeProbe([res.lam]).fit(Ft, Y, Ft, Y)
    pred = probe.predict(Ft)
    eq = float(np.max(np.abs(pred - np.asarray(res.pred_val).reshape(pred.shape))))
    tol, kappa = equivalence_tolerance(Ft, res.lam, pred)
    return Decoder(mu_a, s_a, omega, b, mu_F, s_F, probe, float(res.lam), eq, tol, kappa)


def w_hat(dec_w, a) -> np.ndarray:
    return np.argmax(dec_w.predict(a), axis=1)


def decoder_arrays(dec) -> dict:
    return {"mu_a": dec.mu_a, "s_a": dec.s_a, "omega": dec.omega, "b": dec.b, "mu_F": dec.mu_F,
            "s_F": dec.s_F, "W": dec.probe.W, "bias": dec.probe.b, "lam": np.array(dec.lam),
            "equivalence": np.array(dec.equivalence), "eq_tol": np.array(dec.eq_tol),
            "kappa": np.array(dec.kappa)}


def decoder_from_arrays(a) -> Decoder:
    """Rebuild the frozen decoder (no refit): RidgeProbe with its stored W and bias."""
    probe = RidgeProbe([float(a["lam"])])
    probe.W, probe.b, probe.lam = np.asarray(a["W"]), np.asarray(a["bias"]), float(a["lam"])
    return Decoder(a["mu_a"], a["s_a"], a["omega"], a["b"], a["mu_F"], a["s_F"], probe,
                   float(a["lam"]), float(a["equivalence"]),
                   float(a["eq_tol"]) if "eq_tol" in a else 1e-10,
                   float(a["kappa"]) if "kappa" in a else float("nan"))
