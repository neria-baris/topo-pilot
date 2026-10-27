"""Author A (job 0121): T-NEC-KNOWN (with erratum E-C2ND-1), T-RULE6, T-PROJ-ND and T-COPY.

Protocol C2ND-DESIGN-v1 §2.3, §2.4, §2.5 (failure 1), §4.3, §5.1; review 0116 E-C2ND-1 (the
"half and half" fixture is replaced by psi = 0.3, 0.7 and 0.5). Names from API.md §7-§8.
Written from the protocol copy, API.md, CONTRACT.json, TEST_PLAN.md and the 0116 review only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_nd") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first: API.md §1 test imports)

# isort: split
import c2_attrib as ca  # noqa: E402
import c2_code as ck  # noqa: E402
import c2_decide as cdc  # noqa: E402
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402

P, NOUT = 31, 8
EXTRA = {"variants": {}, "dnullr": {}, "kcr": {}, "kc_test": {}}
NO_P1 = {"precision_limited": []}


def _centre(v):
    return v - v.mean(axis=1, keepdims=True)


def _bounds(arrays, j=1729, seed=630506, draws=2000):
    """One shared stream (VAL level 1/60, 2,000 draws) and C2 guards with beta = 0."""
    res = ndc.stream_bounds({f"{s}|{j}": a for s, a in arrays.items()}, seed, nc.VAL_ALPHA, draws)
    return ndc.model_bounds(res, {s: ndc.guard(a) for s, a in arrays.items()}, j)


def _known(psi, seed, n=2048, cancel=False):
    """A readout with a known code share: outputs 0-3 read only col(B) (scale a), outputs 4-7
    read only the complement (I - P_S) (scale b); psi = a mean(X_S) / mean(A_full) exactly."""
    rng = np.random.default_rng(seed)
    Gamma, B = rng.normal(size=(P, 5)), rng.normal(size=(P, 6))
    A = rng.normal(size=(P, P))
    Sigma = A @ A.T / P + 0.5 * np.eye(P)
    g = ck.gls(Gamma, B, Sigma)
    P_S, P_G, I = g["P_S"], g["P_G"], np.eye(P)  # noqa: E741
    y2, dy = rng.normal(size=(n, P)), rng.normal(size=(n, P))
    if cancel:  # rows 2k and 2k+1 are equal except for the sign of the complement contrast
        y2[1::2], dy[1::2] = y2[0::2], dy[0::2]
    K1, K2 = rng.normal(size=(4, P)), rng.normal(size=(4, P))
    v1, v2 = (dy @ P_S.T) @ K1.T, (dy @ (I - P_S).T) @ K2.T
    c1, c2 = _centre(v1), _centre(v2)
    sgn = np.where(np.arange(n) % 2 == 1, -1.0, 1.0)[:, None] if cancel else 1.0
    rms = [np.sqrt(np.mean(np.sum(c * c, axis=1))) for c in (c1, c2)]
    d = np.hstack((c1 / rms[0], sgn * c2 / rms[1]))  # sum_v d_v = 0 per row
    XS, XC = 0.5 * np.sum(d[:, :4] * v1, axis=1), 0.5 * np.sum(d[:, 4:] * v2, axis=1)
    a = psi / np.mean(XS) if not cancel else 1.0 / np.mean(XS)
    b = (1.0 - psi) / np.mean(XC) if not cancel else 1.0 / np.std(XC)
    M = np.vstack((a * (K1 @ P_S), b * (K2 @ (I - P_S))))
    return dict(d=d, M=M, y1=y2 + dy, y2=y2, P_S=P_S, P_G=P_G, Sigma=Sigma, n=n)


def _run_known(f, y_active=False):
    q = nat.nr_quantities(f["d"], f["M"], f["y1"], f["y2"], f["P_S"])
    G, E = np.asarray(q["A_full"], dtype=np.float64).copy(), np.ones(f["n"], dtype=bool)
    b_nr = _bounds(nat.nr_stream(q, q, G, E, E))
    qx = ca.pair(f["d"], f["M"], f["y1"], f["y2"], f["P_S"], f["P_G"], f["Sigma"])
    b_r = _bounds(ca.r_arrays(qx, qx, G, E, E))
    return q, b_nr, ndc.nr_model(b_nr, y_active), cdc.r_model(b_r, y_active)


# ---- T-NEC-KNOWN (§5.1; E-C2ND-1) ----------------------------------------------------------
@pytest.mark.parametrize(
    "psi, r_cat, nr_cat",
    [(1.0, "USED", "NECESSARY"), (0.0, "NOT_USED", "NOT_NECESSARY"),
     (0.3, "PARTIAL", "NOT_NECESSARY"), (0.7, "USED", "CODE_DOMINANT")],
)
def test_nec_known_categories(psi, r_cat, nr_cat):
    f = _known(psi, seed=int(1000 * psi) + 7)
    q, _, nr, r = _run_known(f)
    share = float(np.mean(q["A_S"])) / float(np.mean(q["A_full"]))
    assert abs(share - psi) <= 1e-9  # fixture: the known code share
    if psi == 0.0:  # a head reading only Gamma and P_rest: zero code energy
        assert float(np.max(np.abs(q["e_S"]))) <= 1e-20 * max(1.0, float(np.max(q["e_full"])))
    assert r["status"] == r_cat and nr["status"] == nr_cat


def test_nec_known_half_share_is_neither_partial_nor_code_dominant():
    # E-C2ND-1: psi = 0.5 exactly puts Zc050 (and Z050) at mean 0: INC on both rules
    f = _known(0.5, seed=505)
    q, b_nr, nr, r = _run_known(f)
    assert abs(float(np.mean(q["A_comp"])) / float(np.mean(q["A_full"])) - 0.5) <= 1e-9
    assert b_nr["Zc050"]["L"] < -b_nr["Zc050"]["g"] and b_nr["Zc050"]["U"] > b_nr["Zc050"]["g"]
    assert nr["status"] == "INC" and r["status"] == "INC"


def test_nec_known_cancellation_is_low_aligned_not_necessary():
    f = _known(0.0, seed=606, n=4096, cancel=True)
    q, b_nr, nr, _ = _run_known(f)
    A_comp, A_full = np.asarray(q["A_comp"]), np.asarray(q["A_full"])
    assert abs(float(np.mean(A_comp))) <= 1e-9 * float(np.mean(A_full))  # E[A_comp] ~ 0
    assert float(np.mean(np.abs(A_comp))) > 0.3 * float(np.mean(A_full))  # large |A_comp|
    assert float(np.mean(q["e_comp"])) / float(np.mean(q["e_full"])) > 0.10  # eta_comp
    assert nr["status"] == "COMPLEMENT_LOW_ALIGNED"
    assert b_nr["Wc"]["L"] > b_nr["Wc"]["g"] and b_nr["Vc"]["U"] > -b_nr["Vc"]["g"]


def test_nec_known_negative_complement():
    f = _known(1.4, seed=1407)  # psi_comp = -0.4
    q, b_nr, nr, _ = _run_known(f)
    psi_comp = float(np.mean(q["A_comp"])) / float(np.mean(q["A_full"]))
    assert abs(psi_comp + 0.4) <= 1e-9
    assert nr["status"] == "COMPLEMENT_LOW_ALIGNED" and nr["negative"]
    assert b_nr["Wc"]["L"] < -b_nr["Wc"]["g"]  # the lower bound blocks NECESSARY
    quals = ndc.qualifiers("N-R", {1729: nr}, EXTRA, False, NO_P1)
    assert "NEGATIVE_COMPLEMENT(1729)" in quals
    assert quals.index("SPECIFICITY_NOT_ESTABLISHED") < quals.index("NEGATIVE_COMPLEMENT(1729)")


# ---- bound dicts built directly (TEST_PLAN §1) ------------------------------------------
PAT = {"+": (0.5, 1.0), "-": (-1.0, -0.5), "s": (-0.5, 0.5), "0": (-1e-10, 1e-10)}
GRD = 1e-9


def _bd(**cfg):
    out = {}
    for s, p in cfg.items():
        L, U = PAT[p] if isinstance(p, str) else p
        out[s] = {"mean": (L + U) / 2, "L": L, "U": U, "rank_L": 67, "rank_U": 19934, "g": GRD}
    return out


NR = dict(V3x="+", Y1="-", Zc010="-", Zc050="-", Wc="+", Vc="-", NEGc="+", Zc090="-",
          Zc100="-", Z090="s")
DD = dict(V3x="+", Y1="-", Z010="-", Z050="-", Vabs="-", Vrand="-", NEG="+")
NM = dict(V3x="+", Ztau="+", ZMc010="-", ZMc050="-", WMc="+", VMc="-", NEGMc="+")


def _nr(y_active=True, **kw):
    return ndc.nr_model(_bd(**dict(NR, **kw)), y_active)


# ---- T-RULE6 (§2.3, §2.4, §4.3, §5.1) ----------------------------------------------------
def test_rule6a_complement_positive_below_margin():
    r = _nr()
    assert r["status"] == "NECESSARY" and r["rule6a"]
    r = _nr(Vc="+")
    assert r["status"] == "COMPLEMENT_LOW_ALIGNED" and r["rule6a"]
    assert not _nr(Zc050="s")["rule6a"]  # RC-6: the upper conjunct U(Zc050) < 0
    r = _nr(Zc050=(-1.0, -GRD))  # U(Zc050) = -g exactly: not declared
    assert not r["rule6a"] and r["status"] == "INC/NUMERICAL"
    assert not _nr(NEGc="s")["rule6a"]
    r = _nr(Y1="s")  # Y1 active and SPEC undeclared
    assert r["status"] == "EXCLUDED/NUISANCE_IN_S" and not r["rule6a"]
    assert not _nr(V3x="s")["rule6a"]


def test_rule6b_decoy_positive_below_margin():
    r = ndc.d_model(_bd(**DD), True)
    assert r["status"] == "DECOY_NOT_USED" and r["rule6b"]
    r = ndc.d_model(_bd(**dict(DD, Vabs="+")), True)
    assert r["status"] == "DECOY_LOW_ALIGNED" and r["rule6b"]
    r = ndc.d_model(_bd(**dict(DD, Vrand="s")), True)
    assert r["status"] == "DECOY_LOW_ALIGNED" and r["rule6b"]
    assert not ndc.d_model(_bd(**dict(DD, Z050="s")), True)["rule6b"]
    assert not ndc.d_model(_bd(**dict(DD, NEG="s")), True)["rule6b"]
    r = ndc.d_model(_bd(**dict(DD, V3x="s")), True)
    assert r["status"] == "EXCLUDED/MODEL_HEADROOM" and not r["rule6b"]


def test_nested_entry_only_inside_not_necessary():
    nn = dict(Zc010="+", Zc050="+", Zc090="+", Zc100="-")
    r = _nr(**nn)
    assert r["status"] == "NOT_NECESSARY" and r["nested"]
    r = _nr(**dict(nn, Zc050="-"))  # the same Zc090/Zc100 signs with CODE_DOMINANT
    assert r["status"] == "CODE_DOMINANT" and not r["nested"]
    assert not _nr(**dict(nn, Zc090="s"))["nested"]
    assert not _nr(**dict(nn, Zc100="s"))["nested"]
    assert not _nr(**dict(nn, V3x="s"))["nested"]


def test_rule6c_layer2_and_routed():
    r = ndc.nm_model(_bd(**NM))
    assert r["status"] == "NECESSARY_M" and r["rule6c"]
    r = ndc.nm_model(_bd(**dict(NM, VMc="+")))
    assert r["status"] == "COMPLEMENT_LOW_ALIGNED_M" and r["rule6c"]
    r = ndc.nm_model(_bd(**dict(NM, Ztau="-")))
    assert r["status"] == "ROUTED" and not r["rule6c"]
    assert not ndc.nm_model(_bd(**dict(NM, NEGMc="s")))["rule6c"]
    assert not ndc.nm_model(_bd(**dict(NM, Ztau="s")))["rule6c"]


def test_statement_count_needs_two_models():
    yes, no = _nr(), _nr(NEGc="s")
    sc = ndc.statement_count({1729: yes, 2718: no, 3141: yes}, "rule6a")
    assert sorted(sc["models"]) == [1729, 3141] and sc["licensed"]
    sc = ndc.statement_count({1729: no, 2718: yes, 3141: no}, "rule6a")
    assert list(sc["models"]) == [2718] and not sc["licensed"]
    sc = ndc.statement_count({1729: no, 2718: no, 3141: no}, "rule6a")
    assert list(sc["models"]) == [] and not sc["licensed"]


# ---- T-PROJ-ND (§2.3; RC-1; API.md ND-C19) -----------------------------------------------
def _quals(primary, cats):
    extra = dict(EXTRA, variants={1729: cats})
    return ndc.qualifiers("N-R", {1729: primary}, extra, True, NO_P1)


def test_proj_variant_categories_and_qualifiers():
    cd = dict(NR, Zc010="+", Zc050="-")
    var = {"R_E:Zc010": "-", "R_E:Zc050": "-", "R_K1:Zc010": "-", "R_K1:Zc050": "-",
           "R_K2:Zc010": "+", "R_K2:Zc050": "-"}
    b = _bd(**cd, **var)
    prim = ndc.nr_model(b, True)
    plain = ndc.nr_model(_bd(**cd), True)
    assert prim["status"] == plain["status"] == "CODE_DOMINANT"  # variants never change it
    assert prim["coarse"] == plain["coarse"] and prim["rule6a"] == plain["rule6a"]
    cats = {v: ndc.nr_variant_category(b, v, prim) for v in ("R_E", "R_K1", "R_K2")}
    assert cats == {"R_E": "COMPLEMENT_LOW_ALIGNED", "R_K1": "COMPLEMENT_LOW_ALIGNED",
                    "R_K2": "CODE_DOMINANT"}
    q = _quals(prim, cats)
    assert "PROJECTOR_DEPENDENT_NR(1729)" in q and "HARMONIC_DEPENDENT_NR(1729, 1)" in q
    assert "HARMONIC_DEPENDENT_NR(1729, 2)" not in q
    assert q.index("PROJECTOR_DEPENDENT_NR(1729)") < q.index("HARMONIC_DEPENDENT_NR(1729, 1)")
    same = {v: "CODE_DOMINANT" for v in cats}
    assert not [x for x in _quals(prim, same) if "_DEPENDENT_NR" in x]
    # NOT_NECESSARY, INC and INC/NUMERICAL variant categories (no lower-bound conjunct)
    b2 = _bd(**cd, **{"R_E:Zc010": "+", "R_E:Zc050": "+", "R_K1:Zc010": "s",
                      "R_K1:Zc050": "-", "R_K2:Zc010": "0", "R_K2:Zc050": "-"})
    assert ndc.nr_variant_category(b2, "R_E", prim) == "NOT_NECESSARY"
    assert ndc.nr_variant_category(b2, "R_K1", prim) == "INC"
    assert ndc.nr_variant_category(b2, "R_K2", prim) == "INC/NUMERICAL"


def test_proj_excluded_absent_and_necessary_primary():
    var = {"R_E:Zc010": "-", "R_E:Zc050": "-"}
    b = _bd(**dict(NR, V3x="s"), **var)
    prim = ndc.nr_model(b, True)
    assert prim["status"] == "EXCLUDED/MODEL_HEADROOM"
    assert ndc.nr_variant_category(b, "R_E", prim) == "EXCLUDED/MODEL_HEADROOM"
    b = _bd(**dict(NR, Zc010="+", Zc050="-"))
    prim = ndc.nr_model(b, True)
    assert ndc.nr_variant_category(b, "R_E", prim) == "NOT_COMPUTED"
    assert not [x for x in _quals(prim, {"R_E": "NOT_COMPUTED"}) if "_DEPENDENT_NR" in x]
    # ND-C19: a primary NECESSARY is compared as COMPLEMENT_LOW_ALIGNED
    b = _bd(**NR, **var)
    prim = ndc.nr_model(b, True)
    assert prim["status"] == "NECESSARY"
    cat = ndc.nr_variant_category(b, "R_E", prim)
    assert cat == "COMPLEMENT_LOW_ALIGNED"
    assert "PROJECTOR_DEPENDENT_NR(1729)" not in _quals(prim, {"R_E": cat})
    assert "PROJECTOR_DEPENDENT_NR(1729)" in _quals(prim, {"R_E": "CODE_DOMINANT"})


# ---- T-COPY (§2.5 failure 1, §5.1) -------------------------------------------------------
def _copy_case(kind, seed=701, n_fit=4096, n_eval=1024):
    rng = np.random.default_rng(seed)
    Gamma, B = rng.normal(size=(P, 5)), rng.normal(size=(P, 6))
    alpha, M = rng.normal(size=(36, P)), rng.normal(size=(NOUT, P))
    L_B, I = ck.gls(Gamma, B)["L_B"], np.eye(P)  # noqa: E741  (L_B B = I6, L_B Gamma = 0)
    V0 = np.linalg.svd(M)[2][NOUT:].T  # an orthonormal basis of ker(M) (23 columns)
    if kind == "copy_in_K":  # col(U) in K = ker(CM)
        X = ca.null_projector(M) @ rng.normal(size=(P, 6))
        T = I + X @ L_B
    elif kind == "move_and_visible_copy":  # code moved to U0 in ker(M), a copy at B + U2
        U0, U2 = V0 @ rng.normal(size=(V0.shape[1], 6)), V0 @ rng.normal(size=(V0.shape[1], 6))
        X = U0 + U2
        T = I + (U0 - B) @ L_B + (B + U2) @ L_B
    else:  # "null_copy": an appended copy in ker(M), the code not moved
        X = V0 @ rng.normal(size=(V0.shape[1], 6))
        T = I + X @ L_B

    def rows(n):
        w32 = rng.permutation(np.arange(n) % 36)
        zt, phi = rng.normal(size=(n, 5)), rng.uniform(0.0, 2.0 * np.pi, n)
        return w32, zt, phi, alpha[w32] + zt @ Gamma.T

    def noise(n):
        return 0.01 * rng.normal(size=(n, P))

    w32, zt, phi, base = rows(n_fit)
    f = ck.harmonics(phi, 3)
    pr = ck.problem((base + f @ B.T + noise(n_fit)) @ T.T, w32, zt, f)
    _, _, phi_e, base_e = rows(n_eval)
    Ye1 = base_e + ck.harmonics(phi_e, 3) @ B.T + noise(n_eval)
    Ye2 = base_e + ck.harmonics(phi_e + 0.8, 3) @ B.T + noise(n_eval)
    dz = _centre((Ye1 - Ye2) @ M.T)
    d = dz / np.abs(dz).max() + 0.02 * _centre(rng.normal(size=(n_eval, NOUT)))
    return dict(pr=pr, B=B, X=X, T=T, M=M, d=d, y1=Ye1 @ T.T, y2=Ye2 @ T.T, n=n_eval)


@pytest.mark.parametrize("kind", ["copy_in_K", "move_and_visible_copy", "null_copy"])
def test_copy_is_absorbed_and_used(kind):
    c = _copy_case(kind)
    pr, M = c["pr"], c["M"]
    assert np.max(np.abs((M - M.mean(axis=0)) @ c["X"])) <= 1e-10 * np.max(np.abs(c["X"]))
    angles = np.asarray(nat.canonical_angles(pr["fit"]["B"], c["B"] + c["X"]))
    assert np.max(angles) < 1e-3  # FWL puts the copy direction inside col(B-hat)
    g = pr["g"]
    qx = ca.pair(c["d"], M, c["y1"], c["y2"], g["P_S"], g["P_G"], pr["Sigma"])
    E = np.ones(c["n"], dtype=bool)
    G = np.asarray(qx["A_full"], dtype=np.float64).copy()
    r = cdc.r_model(_bounds(ca.r_arrays(qx, qx, G, E, E)), False)
    assert r["status"] == "USED"
