"""Independent tests, author A (job 0101): T-SCOPE (RC-2, NEW-4; run with the R and the S*
parameterisation), T-LEAK (RC-7) and T-PROJ (C2-FROZEN-v1 2.4-2.6, 3.1, 6.3-6.6, 13.3).

Targets (API.md 8-11): ck.fwl, ck.f1_fwl, ck.ledoit_wolf, ck.lw_ok, ck.gls, ck.gls_identities,
ck.code_phase, ck.zero_code_threshold, ck.r1, ck.fstar, cs.gls_ref, cs.decoder_features,
cs.fit_decoder, cs.l1, ca.partition, ca.energies, ca.random_ref, cdc.stream_bounds,
cdc.guard, cdc.r_model, cdc.variant_category, cdc.qualifiers, cdc.licence.

Synthetic world (p = 14 readout coordinates): y = alpha_w + Gamma z + B f_3(phi) + extra + noise
with col(Gamma), col(B) and the extra directions V mutually Euclidean-orthogonal. FIT is a
balanced design: per class a 24-point phase grid crossed with nuisance draws +xi and -xi, so the
fourth harmonic and the interaction cos(phi) [h - E(h)] (h = the entropy column, index 3) are
orthogonal to every registered additive regressor (NEW-4 sentence). FEAS and TEST rows are
natural (random phase); the arms are phi +- pi/3 with the last symbol and xi kept. The oracle
contrast of a row is d = C M dy / max |C M dy| (the model responds; G = A_full).

API-ASSUMPTION (API.md 11.2 leaves the formats open): r_model gets, per statistic name, the
stream_bounds entry plus "g"; variant_category and qualifiers get r_model outputs as
"primary"/per_model, variants as {model: {variant: category}} and p1 as the cs.p1 result.
"""

from __future__ import annotations

import functools
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_readout") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_decide as cdc  # noqa: E402
import c2_stats as cs  # noqa: E402

P, DPHI = 14, np.pi / 3
QCODE = {"R": "defined by this fit and projector.",
         "S*": "defined by the oracle x-phase fit and projector."}
OUTCOME = {("R", "NOT_USED"): "NOT_USED", ("R", "LOW_ALIGNED"): "LOW_ALIGNED_SHARE",
           ("S*", "NOT_USED"): "X_PHASE_NOT_USED", ("S*", "LOW_ALIGNED"): "X_PHASE_LOW_ALIGNED"}
VALUES = {"k": 2, "list": [1729, 2718], "other": "INC", "psi_hat": 0.01, "lower": -0.01,
          "upper": 0.02, "tau_hat": 0.05, "psi_M_hat": 0.05, "gate": "L1", "values": "-",
          "statuses": "-", "models": [1729, 2718], "registration": 0.95, "R2_code_0": 0.9,
          "rho_inc": 0.97, "intervals": "-", "theta_rot": 0.5, "interval": (0.4, 0.6),
          "s_rot": 0.9, "m": 1}
P1 = {"N_F": 4096, "pass": {}, "status": "PASS", "precision_limited": [], "summaries": {}}


def _harm(phi, K):
    return np.column_stack([f(k * phi) for k in range(1, K + 1) for f in (np.cos, np.sin)])


def _world(kind, seed=21):
    rng = np.random.default_rng(seed)
    Q = np.linalg.qr(rng.normal(size=(P, P)))[0]
    u = np.zeros(36)
    u[[0, 1, 2, 3]] = [0.6, -0.6, 0.3, -0.3]
    return {"kind": kind, "Gam": Q[:, :5] @ rng.normal(size=(5, 5)),
            "Bt": Q[:, 5:11] @ rng.normal(size=(6, 6)), "V": Q[:, 11:13],
            "alpha": rng.normal(size=(36, P)), "u": u}


def _zt(W, phi, xi):
    zt = xi.copy()
    if W["kind"] == "ii":  # imperfect nuisance-phase correlation (NEW-4)
        zt[:, 0] = 0.6 * np.cos(phi) + 0.8 * xi[:, 0]
    return zt


def _rep(W, w, zt, phi, rng):
    y = W["alpha"][w] + zt @ W["Gam"].T + _harm(phi, 3) @ W["Bt"].T
    if W["kind"] == "i-a":  # the representation also carries a fourth harmonic
        y = y + 2.0 * np.column_stack((np.cos(4 * phi), np.sin(4 * phi))) @ W["V"].T
    elif W["kind"] == "i-b":  # interaction cos(phi) [h - E(h)], h centred and phase-free
        y = y + 2.0 * np.outer(np.cos(phi) * zt[:, 3], W["V"][:, 0])
    return y + 0.02 * rng.normal(size=y.shape)


def _head(W, fit):
    r = {"i-a": W["V"][:, 0], "i-b": W["V"][:, 0], "ii": W["Gam"][:, 0]}[W["kind"]]
    return np.outer(W["u"], r / np.linalg.norm(r))


def _regressors(fam, phi, K):
    m32 = 0.8 * np.column_stack((np.cos(phi), np.sin(phi)))
    return _harm(phi, K) if fam == "R" else ck.fstar(m32, K)[0]


def _pairs(W, fam, g, fit, n, seed):
    rng = np.random.default_rng(seed)
    w, phi, xi = rng.integers(0, 36, n), rng.uniform(-np.pi, np.pi, n), rng.normal(size=(n, 5))
    arms = {}
    for s, name in ((1, "p"), (-1, "m")):
        ph = phi + s * DPHI
        arms[name] = (_rep(W, w, _zt(W, ph, xi), ph, rng), ph)
    nat = _rep(W, w, _zt(W, phi, xi), phi, rng)
    return w, phi, xi, arms, nat


def _arrays(d, M, dy, P_S, P_G, G, Sigma, prefix=""):
    part, en = ca.partition(d, M, dy, P_S, P_G), ca.energies(M, dy, P_S)
    r = ca.random_ref(M, Sigma, dy, en["e_full"])["r"]
    out = {prefix + "Z010": part["A_S"] - 0.1 * part["A_full"],
           prefix + "Z050": part["A_S"] - 0.5 * part["A_full"],
           prefix + "Vabs": en["e_S"] - 0.1 * en["e_full"],
           prefix + "Vrand": en["e_S"] - (127 / 60) * r}
    if not prefix:
        out.update({"V3x": part["A_full"] - 0.3 * G, "NEG": part["A_S"],
                    "Y1": -0.5 * np.ones(len(d))})
    return out, part


def _b(stats, model=1729, draws=2000):
    keyed = {f"{s}|{model}": np.asarray(v, dtype=np.float64) for s, v in stats.items()}
    res = cdc.stream_bounds(keyed, cc.seed("test_R"), cc.ALPHA["R"], draws=draws)
    return {s: dict(res[f"{s}|{model}"], g=cdc.guard(stats[s])) for s in stats}


@functools.lru_cache(maxsize=None)
def _pipeline(kind, fam):
    W = _world(kind)
    rng = np.random.default_rng(22)
    off, xis = rng.uniform(0, 2 * np.pi / 24, 36), rng.normal(size=(36, 5))
    w = np.repeat(np.arange(36), 48)
    k = np.tile(np.repeat(np.arange(24), 2), 36)
    sgn = np.tile([1.0, -1.0], 36 * 24)
    phi = off[w] + 2 * np.pi * k / 24
    zt = _zt(W, phi, sgn[:, None] * xis[w])
    Y = _rep(W, w, zt, phi, rng)
    fit = ck.fwl(Y, w, zt, _regressors(fam, phi, 3))
    Sigma = ck.ledoit_wolf(fit["resid"])
    g = ck.gls(fit["Gamma"], fit["B"], Sigma)
    out = {"W": W, "fit": fit, "Sigma": Sigma, "g": g, "w": w, "zt": zt, "Y": Y, "phi": phi}
    # F1 prerequisites (NEW-4: validity first)
    ref = cs.gls_ref(Sigma, fit["Gamma"], fit["B"], g["P_S"], g["P_G"])
    out["F1"] = (ck.f1_fwl(fit) == "PASS" and ck.lw_ok(Sigma) and g["status"] == "PASS"
                 and bool(ck.gls_identities(g, fit["Gamma"], fit["B"], Sigma)["ok"])
                 and bool(ref["accepted"]))
    # L1 on FEAS (fitted decoders on FIT, scored on natural FEAS rows)
    panel = np.arange(len(w)) % 8
    fw, fphi, fxi, farms, fnat = _pairs(W, fam, g, fit, 720, 23)
    fzt = _zt(W, fphi, fxi)
    feats = {}
    for kind_d, kw, fkw in (("D0", {}, {}), ("Dcode", {"code": Y @ g["L_B"].T},
                                              {"code": fnat @ g["L_B"].T}),
                            ("Dlin", {"full": Y}, {"full": fnat})):
        dec = cs.fit_decoder(cs.decoder_features(kind_d, w, zt, **kw),
                             _regressors(fam, phi, 1), panel)
        assert dec.eq <= dec.tol
        feats[kind_d] = dec.predict(cs.decoder_features(kind_d, fw, fzt, **fkw))
    out["L1"] = cs.l1(_regressors(fam, fphi, 1), feats["D0"], feats["Dcode"], feats["Dlin"])
    # R1 on FEAS pairs
    thr = ck.zero_code_threshold(ck.code_phase(Y, fit["alpha"], w, g["L_B"])[1])
    ph = {s: ck.code_phase(farms[s][0], fit["alpha"], fw, g["L_B"]) for s in ("p", "m")}
    m32 = {s: 0.8 * np.column_stack((np.cos(farms[s][1]), np.sin(farms[s][1]))) for s in ph}
    out["R1"] = ck.r1(ph["p"][0], ph["m"][0], ph["p"][1], ph["m"][1], m32["p"], m32["m"], thr)
    # TEST endpoint
    _, _, _, arms, _ = _pairs(W, fam, g, fit, 1200, 24)
    dy = arms["p"][0] - arms["m"][0]
    M = _head(W, fit)
    zd = dy @ M.T
    d = (zd - zd.mean(1, keepdims=True)) / np.max(np.abs(zd))
    G = 0.5 * np.sum(d * zd, axis=1)
    out["stats"], out["part"] = _arrays(d, M, dy, g["P_S"], g["P_G"], G, Sigma)
    out["M"], out["d"], out["dy"] = M, d, dy
    return out


# ---- T-SCOPE ---------------------------------------------------------------------------------
@pytest.mark.parametrize("fam", ["R", "S*"])
@pytest.mark.parametrize("kind", ["i-a", "i-b", "ii"])
def test_out_of_code_and_excluded_direction_fixtures(kind, fam):
    out = _pipeline(kind, fam)
    assert out["F1"] is True  # F1 first ...
    assert out["L1"]["status"] == "PASS"  # ... then the incremental L1 ...
    assert out["R1"]["status"] == "PASS"  # ... and R1 (the code moves with the counterfactual)
    res = cdc.r_model(_b(out["stats"]), False)
    assert res["resp"]  # RESP declared before the outcome is read
    part = out["part"]
    psi = part["A_S"].mean() / part["A_full"].mean()
    assert abs(psi) < 0.02
    if kind == "ii":
        assert part["A_G"].mean() / part["A_full"].mean() > 0.5  # psi_Gamma reported large
        assert res["status"] in ("NOT_USED", "LOW_ALIGNED")
    else:
        assert res["status"] == "NOT_USED"
    text = cdc.licence(fam, OUTCOME[(fam, res["status"])], VALUES)
    assert QCODE[fam] in text and "They do not exclude predictive use of phase" in text
    assert "the circle is not used" not in text.lower()


def test_interaction_fixture_is_orthogonal_to_the_additive_regressors():
    out = _pipeline("i-b", "R")
    w, zt, phi = out["w"], out["zt"], out["phi"]
    inter = np.cos(phi) * zt[:, 3]
    onehot = (w[:, None] == np.arange(36)).astype(float)
    X = np.hstack((onehot, zt, _harm(phi, 3)))
    assert np.max(np.abs(X.T @ inter)) <= 1e-9 * len(w)  # the balanced design (NEW-4)
    h4 = np.cos(4 * phi)
    assert np.max(np.abs(X.T @ h4)) <= 1e-9 * len(w)


# ---- T-LEAK (RC-7) ---------------------------------------------------------------------------
def _placebo(out, coef_code, coef_other, n=1200, seed=31):
    g, W = out["g"], out["W"]
    b0, q = out["fit"]["B"][:, 0], W["V"][:, 0]
    r = np.linalg.lstsq(np.vstack((b0, q)), np.array([coef_code, coef_other]), rcond=None)[0]
    t = np.random.default_rng(seed).uniform(0.5, 1.5, n)[:, None]
    a = 1.0 if coef_other == 0 else 5.0
    c = 0.0 if coef_other == 0 else 6.0
    dyR = t * (a * b0 + c * q)
    MR = np.outer(W["u"], r)
    z = dyR @ MR.T
    dR = (z - z.mean(1, keepdims=True)) / np.max(np.abs(z))
    part = ca.partition(dR, MR, dyR, g["P_S"], g["P_G"])
    return part["A_S"] - 0.1 * part["A_full"], part


def test_planted_y_direction_inside_col_B_fails_y1():
    out = _pipeline("i-a", "R")
    y1, part = _placebo(out, 1.0, 0.0)
    assert part["A_S"].mean() / part["A_full"].mean() > 0.9
    stats = dict(out["stats"], Y1=y1)
    res = cdc.r_model(_b(stats), True)
    assert res["status"] == "EXCLUDED/NUISANCE_IN_S"


def test_large_negative_placebo_passes_y1_and_licence_states_only_the_inequality():
    out = _pipeline("i-a", "R")
    y1, part = _placebo(out, -1.0, 1.0)
    assert part["A_S"].mean() / part["A_full"].mean() < -4.0  # a large opposing contribution
    n = len(y1)
    wob = 0.01 * np.sin(np.arange(n))
    stats = {"V3x": 0.5 + wob, "Z010": 0.6 + wob, "Z050": 0.3 + wob, "Vabs": 1.0 + wob,
             "Vrand": 1.0 + wob, "NEG": 0.8 + wob, "Y1": y1}
    res = cdc.r_model(_b(stats), True)
    assert res["spec"] and res["status"] == "USED"
    text = cdc.licence("R", "USED", VALUES)
    if "placebo" in text:
        assert ("mean signed placebo contribution is below 0.10 times the mean full placebo "
                "contrast") in text
    for claim in ("placebo ratio", "no placebo effect", "nuisance-free", "small placebo"):
        assert claim not in text.lower()


# ---- T-PROJ ----------------------------------------------------------------------------------
def _proj_problem(seed=41):
    rng = np.random.default_rng(seed)
    p = 10
    Gamma, B = rng.normal(size=(p, 5)), rng.normal(size=(p, 4))
    U = np.linalg.qr(rng.normal(size=(p, p)))[0]
    Sigma = (U * np.exp(rng.uniform(-2, 2, p))) @ U.T
    return Gamma, B, (Sigma + Sigma.T) / 2, rng


def _rows_through(M_dir, dirs, n=1200, seed=42):
    t = np.random.default_rng(seed).uniform(0.5, 1.5, n)[:, None]
    dy = t * dirs
    u = np.zeros(36)
    u[[4, 5]] = [0.7, -0.7]
    M = np.outer(u, M_dir)
    z = dy @ M.T
    d = (z - z.mean(1, keepdims=True)) / np.max(np.abs(z))
    return d, M, dy, 0.5 * np.sum(d * z, axis=1)


def test_projector_dependent_when_euclidean_complement_changes_the_category():
    Gamma, B, Sigma, rng = _proj_problem()
    gG, gE = ck.gls(Gamma, B, Sigma), ck.gls(Gamma, B)
    Xn = np.hstack((Gamma, B))
    v = rng.normal(size=10)
    v -= Xn @ np.linalg.lstsq(Xn, v, rcond=None)[0]  # Euclidean complement: L^E v = 0
    a1, a3 = B @ rng.normal(size=4), gG["P_S"] @ v
    assert np.max(np.abs(gE["P_S"] @ v)) <= 1e-10 and np.linalg.norm(a3) > 1e-2
    r = np.linalg.lstsq(np.vstack((a1, v, a3)), np.array([0.3, 0.7, 0.6]), rcond=None)[0]
    d, M, dy, G = _rows_through(r, a1 + v)
    st, part = _arrays(d, M, dy, gG["P_S"], gG["P_G"], G, Sigma)
    var, vpart = _arrays(d, M, dy, gE["P_S"], gE["P_G"], G, Sigma, prefix="R_E:")
    assert abs(part["A_S"].mean() / part["A_full"].mean() - 0.9) <= 1e-6
    assert abs(vpart["A_S"].mean() / vpart["A_full"].mean() - 0.3) <= 1e-6
    b = _b(dict(st, **var))
    primary = cdc.r_model(b, False)
    assert primary["status"] == "USED"
    cat = cdc.variant_category(b, "R_E", primary)
    assert cat == "PARTIAL"
    same = {"R_E": "USED", "R_K1": "USED", "R_K2": "USED"}
    q = cdc.qualifiers("R", {1729: primary, 2718: primary, 3141: primary},
                       {1729: dict(same, R_E=cat), 2718: same, 3141: same}, False, P1)
    assert "PROJECTOR_DEPENDENT(1729)" in q
    assert not any(x.startswith(("PROJECTOR_DEPENDENT(2718", "PROJECTOR_DEPENDENT(3141"))
                   for x in q)
    assert "SPECIFICITY_NOT_ESTABLISHED" in q


def test_harmonic_dependent_when_the_k1_variant_changes_the_category():
    Gamma, B, Sigma, rng = _proj_problem(seed=43)
    gK2, gK1 = ck.gls(Gamma, B, Sigma), ck.gls(Gamma, B[:, :2], Sigma)
    a = B[:, 2]  # the response runs through the second harmonic
    a4 = gK1["P_S"] @ a
    r = np.linalg.lstsq(np.vstack((a, a4)), np.array([1.0, 0.02]), rcond=None)[0]
    d, M, dy, G = _rows_through(r, a)
    st, part = _arrays(d, M, dy, gK2["P_S"], gK2["P_G"], G, Sigma)
    var, vpart = _arrays(d, M, dy, gK1["P_S"], gK1["P_G"], G, Sigma, prefix="R_K1:")
    assert abs(part["A_S"].mean() / part["A_full"].mean() - 1.0) <= 1e-6
    assert abs(vpart["A_S"].mean() / vpart["A_full"].mean() - 0.02) <= 1e-6
    b = _b(dict(st, **var))
    primary = cdc.r_model(b, False)
    assert primary["status"] == "USED"
    cat = cdc.variant_category(b, "R_K1", primary)
    assert cat in ("NOT_USED", "LOW_ALIGNED")
    same = {"R_E": "USED", "R_K1": "USED", "R_K2": "USED"}
    q = cdc.qualifiers("R", {1729: primary, 2718: primary, 3141: primary},
                       {1729: dict(same, R_K1=cat), 2718: same, 3141: same}, False, P1)
    assert "HARMONIC_DEPENDENT(1729, 1)" in q
    assert not any(x.startswith("PROJECTOR_DEPENDENT") for x in q)
