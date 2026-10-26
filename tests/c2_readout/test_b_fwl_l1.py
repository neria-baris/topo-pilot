"""Author B (job 0101): T-FWL (RC-12) and T-L1 (RC-3) (C2-FROZEN-v2 §13.3; §2.4, §2.5, §6.6);
also the D-0107-1 G0 (vii) regression (T-NAMESPACE in part; R-0107-2).

Written from PROTOCOL_C2_v2.md, API.md §8.1, §8.2, §9.2 and CONTRACT.json only;
tools/c2_readout/*.py never read. Synthetic Gaussian fixtures with fixed seeds; tolerances are
derived from each fixture's n and noise level.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402  (first: the sys.path convention)
import c2_code as ck  # noqa: E402
import c2_stats as cs  # noqa: E402
import c1_fit  # noqa: E402

from topo_pilot.analysis import x4f_scores  # noqa: E402
from topo_pilot.experiment.x4f_probe import nested_ridge  # noqa: E402
from topo_pilot.prediction.ridge import RidgeProbe  # noqa: E402

P, PER_CLASS, SIGMA = 127, 60, 1e-3
N = 36 * PER_CLASS
GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)
DEGENERATE = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE"


def _harm(phi, K):
    cols = []
    for k in range(1, K + 1):
        cols += [np.cos(k * phi), np.sin(k * phi)]
    return np.column_stack(cols)


@pytest.fixture(scope="module")
def fwl_data():
    rng = np.random.default_rng(20210)
    w32 = rng.permutation(np.repeat(np.arange(36), PER_CLASS))
    zt, phi = rng.standard_normal((N, 5)), rng.uniform(-np.pi, np.pi, N)
    alpha, Gamma = rng.standard_normal((36, P)), rng.standard_normal((P, 5))
    B = rng.standard_normal((P, 6))
    clean = alpha[w32] + zt @ Gamma.T + _harm(phi, 3) @ B.T
    Y = clean + SIGMA * rng.standard_normal((N, P))
    return {"w32": w32, "zt": zt, "phi": phi, "alpha": alpha, "Gamma": Gamma, "B": B, "Y": Y,
            "clean": clean, "rng": rng}


# ---- T-FWL ----
def test_harmonics_column_order():
    phi = np.linspace(-3.0, 3.0, 11)
    for K in (1, 2, 3):
        h = ck.harmonics(phi, K)
        assert h.shape == (11, 2 * K)
        assert np.max(np.abs(h - _harm(phi, K))) <= 1e-15


def test_fwl_recovers_known_B_with_K3(fwl_data):
    d = fwl_data
    fit = ck.fwl(d["Y"], d["w32"], d["zt"], _harm(d["phi"], 3))
    assert fit["K"] == 3 and fit["p"] == P and fit["rank"] == 47
    assert fit["B"].shape == (P, 6) and fit["Gamma"].shape == (P, 5)
    assert fit["alpha"].shape == (36, P) and fit["resid"].shape == (N, P)
    se = SIGMA * np.sqrt(2.0 / N)  # coefficient SE of a unit-variance-ish regressor
    assert np.max(np.abs(fit["B"] - d["B"])) <= 10 * se
    assert np.max(np.abs(fit["Gamma"] - d["Gamma"])) <= 10 * SIGMA / np.sqrt(N)
    assert np.max(np.abs(fit["alpha"] - d["alpha"])) <= 10 * SIGMA / np.sqrt(PER_CLASS)
    assert np.max(np.abs(fit["resid"])) <= 10 * SIGMA  # Gaussian noise, n*p draws
    assert ck.f1_fwl(fit) == "PASS"


@pytest.mark.parametrize("K", [1, 2, 3])
def test_design_and_whitened_ranks(fwl_data, K):
    d = fwl_data
    f = _harm(d["phi"], K)
    Y = d["clean"] - _harm(d["phi"], 3) @ d["B"].T + f @ d["B"][:, :2 * K].T
    Y = Y + SIGMA * d["rng"].standard_normal(Y.shape)
    fit = ck.fwl(Y, d["w32"], d["zt"], f)
    assert c1_fit.fwl_design(d["w32"], d["zt"], f).shape[1] == 41 + 2 * K
    assert fit["rank"] == 41 + 2 * K == cc.CONTRACT["dims"]["design_columns"][str(K)]
    assert ck.f1_fwl(fit) == "PASS"
    Sigma = ck.ledoit_wolf(fit["resid"])
    assert Sigma.shape == (P, P) and ck.lw_ok(Sigma)
    for S in (Sigma, None):  # GLS whitened design and the Euclidean variant (X_n itself)
        g = ck.gls(fit["Gamma"], fit["B"], S)
        assert g["rank_Xt"] == 5 + 2 * K == cc.CONTRACT["dims"]["whitened_rank"][str(K)]
        assert g["status"] == "PASS" and g["L"].shape == (5 + 2 * K, P)


def test_rank_failures_keep_every_column(fwl_data):
    d = fwl_data
    f = _harm(d["phi"], 3)
    zt = d["zt"].copy()
    zt[:, 0] = np.cos(d["phi"])  # a covariate equal to a harmonic column
    w_missing = np.where(d["w32"] == 7, 8, d["w32"])  # class 7 has no row
    for w, z in ((d["w32"], zt), (w_missing, d["zt"])):
        fit = ck.fwl(d["Y"], w, z, f)
        assert fit["rank"] == 46 and ck.f1_fwl(fit) == DEGENERATE
        assert fit["alpha"].shape == (36, P) and fit["Gamma"].shape == (P, 5)
        assert fit["B"].shape == (P, 6)  # no column dropped for rank


def test_conditioning_failure_at_full_rank(fwl_data):
    d = fwl_data
    zt = d["zt"].copy()
    zt[:, 0] = np.cos(d["phi"]) + 1e-9 * np.random.default_rng(5).standard_normal(N)
    fit = ck.fwl(d["Y"], d["w32"], zt, _harm(d["phi"], 3))
    assert fit["rank"] == 47 and fit["cond"] > 1e8
    assert ck.f1_fwl(fit) == DEGENERATE


def test_degenerate_B_singular_values(fwl_data):
    d = fwl_data
    B0 = d["B"].copy()
    B0[:, 5] = 0.0
    Y = d["alpha"][d["w32"]] + d["zt"] @ d["Gamma"].T + _harm(d["phi"], 3) @ B0.T
    fit = ck.fwl(Y, d["w32"], d["zt"], _harm(d["phi"], 3))
    assert fit["rank"] == 47 and fit["sv_B"][-1] / fit["sv_B"][0] < 1e-6
    assert ck.f1_fwl(fit) == DEGENERATE


def test_whitened_rank_and_conditioning_failures(fwl_data):
    d = fwl_data
    Sigma = np.diag(np.linspace(0.5, 2.0, P))
    B_rank = d["B"].copy()
    B_rank[:, 0] = d["Gamma"][:, 0]  # col(B) meets col(Gamma): rank 10 < 11
    g = ck.gls(d["Gamma"], B_rank, Sigma)
    assert g["rank_Xt"] == 10 and g["status"] == DEGENERATE
    B_cond = d["B"].copy()
    B_cond[:, 0] = d["Gamma"][:, 0] + 1e-10 * np.random.default_rng(6).standard_normal(P)
    g = ck.gls(d["Gamma"], B_cond, Sigma)
    assert g["rank_Xt"] == 11 and g["cond_Xt"] > 1e8 and g["status"] == DEGENERATE
    assert ck.fwl(d["Y"], d["w32"], d["zt"], _harm(d["phi"], 3))["rank"] == 47  # FWL fine


# ---- T-L1 ----
def _l1_case(seed, n, code_fn, zt_fn):
    rng = np.random.default_rng(seed)
    phi, w32 = rng.uniform(-np.pi, np.pi, n), rng.integers(0, 36, n)
    f1 = np.column_stack((np.cos(phi), np.sin(phi)))
    zt = zt_fn(rng, f1, n)
    code, extra = code_fn(rng, f1, n)
    full = np.hstack((code, extra, rng.standard_normal((n, P - code.shape[1]
                                                          - extra.shape[1]))))
    return {"f1": f1, "w32": w32, "zt": zt, "code": code, "full": full}


def _zt_plain(rng, f1, n):
    return rng.standard_normal((n, 5))


def _zt_phase(rng, f1, n):  # the oracle covariates predict the phase very well
    return np.hstack((f1 + 0.05 * rng.standard_normal((n, 2)), rng.standard_normal((n, 3))))


def _code_snr(rng, f1, n):  # all circle information, noise-to-signal 0.5
    return f1 + 0.5 * rng.standard_normal((n, 2)), np.zeros((n, 0))


def _code_half(rng, f1, n):  # the code keeps only cos; y also holds sin
    c = np.column_stack((f1[:, 0] + 0.05 * rng.standard_normal(n), rng.standard_normal(n)))
    return c, (f1[:, 1] + 0.05 * rng.standard_normal(n))[:, None]


def _code_weak(rng, f1, n):
    return f1 + 0.3 * rng.standard_normal((n, 2)), np.zeros((n, 0))


def _run_l1(code_fn, zt_fn, seed):
    fit, feas = _l1_case(seed, 4096, code_fn, zt_fn), _l1_case(seed + 1, 2048, code_fn, zt_fn)
    panel = np.repeat(np.arange(8), 512)
    preds, decs = {}, {}
    extra = {"D0": (), "Dcode": ("code",), "Dlin": ("full",)}
    for kind in ("D0", "Dcode", "Dlin"):
        feats = [cs.decoder_features(kind, s["w32"], s["zt"], **{k: s[k] for k in extra[kind]})
                 for s in (fit, feas)]
        decs[kind] = cs.fit_decoder(feats[0], fit["f1"], panel)
        preds[kind] = decs[kind].predict(feats[1])
    res = cs.l1(feas["f1"], preds["D0"], preds["Dcode"], preds["Dlin"])
    return res, preds, fit, feas, decs


def _sse(Y, pred):
    return float(np.sum((Y - pred) ** 2))


def test_decoder_features_layout():
    rng = np.random.default_rng(3)
    w32, zt = rng.integers(0, 36, 9), rng.standard_normal((9, 5))
    code, full = rng.standard_normal((9, 6)), rng.standard_normal((9, P))
    onehot = (w32[:, None] == np.arange(36)[None, :]).astype(float)
    assert np.array_equal(cs.decoder_features("D0", w32, zt), np.hstack((onehot, zt)))
    assert np.array_equal(cs.decoder_features("Dcode", w32, zt, code=code),
                          np.hstack((onehot, zt, code)))
    assert np.array_equal(cs.decoder_features("Dlin", w32, zt, full=full),
                          np.hstack((onehot, zt, full)))


def test_fit_decoder_recipe_and_equivalence():
    s = _l1_case(77, 4096, _code_snr, _zt_plain)
    panel = np.repeat(np.arange(8), 512)
    F = cs.decoder_features("Dcode", s["w32"], s["zt"], code=s["code"])
    dec = cs.fit_decoder(F, s["f1"], panel)
    mu, sd = x4f_scores.standardizer(F)
    assert np.array_equal(dec.mu_F, mu) and np.array_equal(dec.s_F, sd)
    res = nested_ridge(F, s["f1"], panel, F, s["f1"], grid=GRID)
    assert float(dec.lam) == float(res.lam)
    Ft = (F - mu) / sd
    pred = RidgeProbe([res.lam]).fit(Ft, s["f1"], Ft, s["f1"]).predict(Ft)
    assert np.max(np.abs(dec.predict(F) - pred)) <= 1e-12 * max(1.0, np.max(np.abs(pred)))
    eq = float(np.max(np.abs(pred - np.asarray(res.pred_val).reshape(pred.shape))))
    tol, kappa = c1_fit.equivalence_tolerance(Ft, res.lam, pred)
    assert abs(float(dec.eq) - eq) <= 1e-12 and float(dec.tol) == pytest.approx(tol)
    assert float(dec.eq) <= float(dec.tol) and float(dec.kappa) == pytest.approx(kappa)
    F2 = F.copy()
    F2[:, 40] *= 1e3  # column scale is removed by the explicit standardisation
    dec2 = cs.fit_decoder(F2, s["f1"], panel)
    assert float(dec2.lam) == float(dec.lam)
    assert np.max(np.abs(dec2.predict(F2) - dec.predict(F))) <= 1e-9
    back = cs.decoder_from_arrays(cs.decoder_arrays(dec))
    assert np.array_equal(back.predict(F), dec.predict(F))


def test_snr_fixture_registered_comparator_passes_where_raw_gls_fails():
    res, preds, fit, feas, _ = _run_l1(_code_snr, _zt_plain, 101)
    Y = feas["f1"]
    sst = float(np.sum((Y - fit["f1"].mean(axis=0)) ** 2))
    raw = (1 - _sse(Y, feas["code"]) / sst) / (1 - _sse(Y, preds["Dlin"]) / sst)
    assert raw < 0.9  # raw estimate vs shrinkage decoder: 1 - rho^2 = 0.75 in population
    assert res["status"] == "PASS"
    assert Fraction(res["R2_code_0"]) >= Fraction(1, 2)
    assert Fraction(res["rho_inc"]) >= Fraction(9, 10)
    sse0, ssec, ssel = (_sse(Y, preds[k]) for k in ("D0", "Dcode", "Dlin"))
    assert res["SSE_0"] == pytest.approx(sse0, rel=1e-12)
    assert res["R2_code_0"] == pytest.approx(1 - ssec / sse0, rel=1e-12)
    assert res["rho_inc"] == pytest.approx((sse0 - ssec) / (sse0 - ssel), rel=1e-12)


def test_code_missing_half_the_circle_fails():
    res, *_ = _run_l1(_code_half, _zt_plain, 202)
    assert res["status"] == "EXCLUDED/LINK"
    assert res["rho_inc"] is not None and res["rho_inc"] < 0.9  # about 0.5


def _flat_numbers(obj):
    if isinstance(obj, dict):
        return [x for v in obj.values() for x in _flat_numbers(v)]
    if isinstance(obj, (int, float, np.floating)) and not isinstance(obj, bool):
        return [float(obj)]
    return []


def test_nuisance_predictive_fixture_fails_the_incremental_link():
    res, preds, fit, feas, _ = _run_l1(_code_weak, _zt_phase, 303)
    Y = feas["f1"]
    means = np.zeros((36, 2))
    for c in range(36):
        means[c] = fit["f1"][fit["w32"] == c].mean(axis=0)
    sst_w = float(np.sum((Y - means[feas["w32"]]) ** 2))
    r2 = {k: 1 - _sse(Y, preds[k]) / sst_w for k in preds}
    assert r2["Dcode"] >= 0.50 and r2["Dcode"] >= 0.90 * r2["Dlin"]  # complete scores pass
    assert res["status"] == "EXCLUDED/LINK"
    assert res["R2_code_0"] is None or res["R2_code_0"] < 0.5
    got = _flat_numbers(cs.l1_complete_scores(Y, preds, feas["w32"], means))
    # API-AMBIGUITY: API.md 9.2 names neither the keys of `preds` nor of the result; the test
    # passes the decoder kinds of decoder_features and looks for the two R^2 values.
    for k in ("Dcode", "Dlin"):
        assert any(abs(v - r2[k]) <= 1e-9 for v in got), k


def _pred_with_sse(n, sse):
    """Entries 2 and 1 against Y = 0, so the SSE is the exact integer `sse` (<= 8 entries)."""
    vals, s = [], int(sse)
    while s >= 4:
        vals, s = vals + [2.0], s - 4
    vals += [1.0] * s
    out = np.zeros(2 * n)
    out[:len(vals)] = vals
    return out.reshape(n, 2)


@pytest.mark.parametrize("sse0, ssec, ssel, status", [
    (8.0, 4.0, 4.0, "PASS"),  # R2 = 1/2 exactly (>=), rho = 1
    (10.0, 1.0, 0.0, "PASS"),  # rho = 9/10 exactly (>=)
    (8.0, 2.0, 1.0, "EXCLUDED/LINK"),  # rho = 6/7 < 9/10
    (16.0, 9.0, 9.0, "EXCLUDED/LINK"),  # R2 = 7/16 < 1/2
])
def test_l1_thresholds_exact(sse0, ssec, ssel, status):
    Y = np.zeros((4, 2))
    res = cs.l1(Y, _pred_with_sse(4, sse0), _pred_with_sse(4, ssec), _pred_with_sse(4, ssel))
    assert res["status"] == status
    assert res["SSE_0"] == sse0 and res["SSE_code"] == ssec and res["SSE_lin"] == ssel


def test_l1_denominator_fixtures_fail_link():
    Y = np.zeros((4, 2))
    zero = np.zeros((4, 2))
    res = cs.l1(Y, zero, zero, zero)  # SSE_0 = 0
    assert res["status"] == "EXCLUDED/LINK" and res["R2_code_0"] is None
    for ssel in (8.0, 9.0):  # SSE_0 - SSE_lin = 0 and < 0
        res = cs.l1(Y, _pred_with_sse(4, 8.0), _pred_with_sse(4, 2.0), _pred_with_sse(4, ssel))
        assert res["status"] == "EXCLUDED/LINK" and res["rho_inc"] is None


# ---- T-NAMESPACE (in part): G0 (vii) and the stage's own pre-G0 records (D-0107-1) ----
# R-0107-2 (agent-handoff/jobs/0107/review.md): GATES.jsonl and STAGES.jsonl are admitted iff
# each is an accepted prefix (empty without an accepted manifest; else the leading lines whose
# sha256 is the lineage append_only value) plus this stage's own pre-G0 lines: one STARTED
# line in STAGES.jsonl; only IMPL / AUTH-ADMIT gate lines of this stage, scope study.
# API-AMBIGUITY: c2_data.own_records(store, stage, lineage) is not yet in API.md; it is read
# as returning {relpath: sha256} for the admitted files, with the accepted prefix sha256 taken
# from lineage["GATES.jsonl"] / lineage["STAGES.jsonl"] (absent: empty prefix).
import hashlib  # noqa: E402
import json  # noqa: E402

import c2_data as cd  # noqa: E402

V2 = "51f78976a6d035b3e01dc2155ad66bb80cb870a4ae155cad17b6665d37f24583"


def _jl(**rec):
    return json.dumps(rec, sort_keys=True) + "\n"


def _gate(gate, stage="S1", scope="study"):
    return _jl(gate=gate, status="PASS", criterion_met=True, utc="2026-10-26T00:00:00Z",
               full_status="PASS", reason="", stage=stage, model=None, family=None,
               problem=None, scope=scope, values={})


def _event(stage="S1", event="STARTED"):
    return _jl(stage=stage, event=event, utc="2026-10-26T00:00:00Z")


def _own_store(tmp_path, gates, stages, prefix=("", "")):
    store, lin = tmp_path / "store", {}
    store.mkdir()
    for name, schema in (("FREEZE.json", "c2-freeze-v1"), ("AUTH.json", "c2-auth-v1")):
        (store / name).write_bytes(json.dumps({"schema": schema, "protocol_sha256": V2}).encode())
        lin[name] = hashlib.sha256((store / name).read_bytes()).hexdigest()
    (store / "GATES.jsonl").write_bytes((prefix[0] + "".join(gates)).encode())
    (store / "STAGES.jsonl").write_bytes((prefix[1] + "".join(stages)).encode())
    return store, lin


def _admitted(store, stage, lin, first):
    own = cd.own_records(store, stage, lin)
    return own, cd.store_admission(store, {**lin, **own}, first)["status"] == "PASS"


def test_own_pre_g0_records_admitted_at_s1(tmp_path):
    store, lin = _own_store(tmp_path, [_gate("IMPL"), _gate("AUTH-ADMIT")], [_event()])
    assert cd.store_admission(store, lin, True)["status"] != "PASS"  # the D-0107-1 defect
    own, ok = _admitted(store, "S1", lin, True)
    for name in ("GATES.jsonl", "STAGES.jsonl"):
        assert own[name] == hashlib.sha256((store / name).read_bytes()).hexdigest()
    assert ok


@pytest.mark.parametrize("gates, stages", [
    ([_gate("IMPL"), _gate("AUTH-ADMIT"), _gate("G0")], [_event()]),  # an extra gate
    ([_gate("IMPL"), _gate("AUTH-ADMIT"), _gate("PF")], [_event()]),
    ([_gate("IMPL"), _gate("AUTH-ADMIT", stage="S2")], [_event()]),  # another stage
    ([_gate("IMPL"), _gate("AUTH-ADMIT", scope="model")], [_event()]),  # not study scope
    ([_gate("IMPL"), _gate("AUTH-ADMIT")], [_event(), _event()]),  # two STARTED lines
    ([_gate("IMPL"), _gate("AUTH-ADMIT")], [_event("S2")]),  # STARTED of another stage
    ([_gate("IMPL"), _gate("AUTH-ADMIT")], [_event(), _event(event="COMPLETED")]),
    ([_gate("IMPL"), _jl(foreign="c2-v1")], [_event()]),  # a foreign line
], ids=["extra-G0", "extra-PF", "other-stage", "scope", "two-started", "started-S2",
        "completed", "foreign"])
def test_own_records_near_misses_are_not_admitted(tmp_path, gates, stages):
    store, lin = _own_store(tmp_path, gates, stages)
    assert not _admitted(store, "S1", lin, True)[1]


def test_later_stage_accepted_prefix_plus_own_lines(tmp_path):
    pre_g = "".join(_gate(g) for g in ("IMPL", "AUTH-ADMIT", "G0", "PF", "H1"))
    pre_s = _event() + _event(event="COMPLETED")
    store, lin = _own_store(tmp_path, [_gate("AUTH-ADMIT", stage="S2")], [_event("S2")],
                            prefix=(pre_g, pre_s))
    lin["GATES.jsonl"] = hashlib.sha256(pre_g.encode()).hexdigest()  # accepted append_only
    lin["STAGES.jsonl"] = hashlib.sha256(pre_s.encode()).hexdigest()
    assert _admitted(store, "S2", lin, False)[1]
    bad = pre_g.replace('"PF"', '"PG"', 1)  # one altered byte in the accepted prefix
    (store / "GATES.jsonl").write_bytes((bad + _gate("AUTH-ADMIT", stage="S2")).encode())
    assert not _admitted(store, "S2", lin, False)[1]
