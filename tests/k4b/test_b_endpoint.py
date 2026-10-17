"""Author B, round 2: API §14.2–14.3 and rulings R20–R22 (API §15). Control arrays, the single
610103 bootstrap dict, control summaries, decoder agreement, ratios (B4 = fresh_b4["point"]), the
init qualifier (strict exact L − F > 1/100), two-sided controls per side with no status (R22 key
names point_/central95_minus/plus, which supersede the §14.2 "pair" wording), support entries and
`endpoint` (exact §11 keys, no writes). Synthetic 24-row inputs; expected values from independent
formulas or from order statistics of the captured draws; structure only where internals are open."""

from __future__ import annotations

import builtins
import io
import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import c1_bounds  # noqa: E402
import c1_means  # noqa: E402
import chart  # noqa: E402
import k4b_fresh  # noqa: E402
import k4b_scores  # noqa: E402
import k4b_stats  # noqa: E402
import scores  # noqa: E402
from topo_pilot.analysis import x4f_scores  # noqa: E402

MODELS = (1729, 2718, 3141)
NAMES = ("m4_phase", "sha_suffix", "init", "decoder", "delta1", "delta2", "delta4_orc", "naive")
TWO, FREE = ("init", "delta1", "delta2"), ("m4_phase", "sha_suffix", "delta4_orc")
MARGIN, Z = Fraction(1, 100), Fraction(1, 10**12)
TWO_PI = 2 * math.pi
N, R, D_FEAT, FRESH_POINT = 24, 1.0, 2048, 0.04
B_SIDE = {"minus": Fraction(1, 10**12), "plus": Fraction(2, 10**12), "norm": Fraction(3, 10**12)}
RESULT_KEYS = {"per_model", "controls", "decoder_agreement", "ratios", "fresh_B4",
               "init_qualifier", "overall", "Z_bound", "N", "k", "c1prime_disclosure"}
PER_MODEL_KEYS = {"L", "U", "L_rank", "U_rank", "F_minus", "F_plus", "B_num_minus", "B_num_plus",
                  "status", "labels", "status_without_F", "central95_minus", "central95_plus",
                  "point_minus", "point_plus", "width", "missing_mass", "support"}


def vphase(m):
    p = np.mod(np.arctan2(m[:, 1], m[:, 0]), TWO_PI)
    return np.where(p == TWO_PI, 0.0, p)


def dot(phi, m32, mK):
    return np.cos(phi) * (m32[:, 0] - mK[:, 0]) + np.sin(phi) * (m32[:, 1] - mK[:, 1])


def val(x) -> float:
    return float(x[0]) if isinstance(x, (tuple, list)) else float(x)


def kth(draws, k) -> float:
    return float(np.sort(np.asarray(draws, dtype=np.float64))[k - 1])


def at(d, key):
    return d[key] if key in d else d[str(key)]


def check_side(g, pk, ck, d, X) -> None:  # point: tree mean; central95: ranks 125 and 4875
    assert val(g[pk]) == pytest.approx(float(c1_means.tree_mean(X)), rel=1e-12, abs=1e-15)
    lo, hi = g[ck]
    assert (val(lo), val(hi)) == (kth(d, 125), kth(d, 4875))


def extension(rng):
    idx = np.arange(N)
    res, d8 = np.where(idx < 18, 0.9, 0.1), np.where(idx % 5 == 0, 1.5, 0.5)
    sup = (res >= 0.2) & (d8 <= R)
    return chart.Extension(rng.uniform(0.0, TWO_PI, N), res, d8, sup, np.zeros(N, dtype=bool))


def decoder(seed) -> dict:
    rng = np.random.default_rng(seed)
    omega, b = x4f_scores.rbf_map(144, D_FEAT, 3.0, rng)
    return {"status": "AVAILABLE", "reason": "", "lam": 1.0, "ell": 3.0,
            "mu_in": np.full(144, 1.0 / 36), "s_in": np.full(144, 0.5), "Omega": omega, "b": b,
            "mean_F": np.full(D_FEAT, 0.01), "scale_F": np.full(D_FEAT, 0.9),
            "W": rng.normal(size=(D_FEAT, 2)), "bias": np.array([0.05, -0.02]),
            "equivalence": 0.0, "eq_tol": 1e-10, "kappa": 1.0}


def inputs(reason="degenerate bandwidth") -> dict:
    rng = np.random.default_rng(4711)
    return {"m": {K: rng.normal(scale=0.2, size=(N, 2)) for K in (1, 2, 4, 32)},
            "canon32": rng.integers(0, 36, (N, 32)).astype(np.uint8),
            "ext": {j: extension(rng) for j in MODELS},
            "init_ext": {1729: extension(rng), 2718: extension(rng),
                         3141: {"unavailable": "chart unavailable"}},
            "decoders": {1729: decoder(1), 2718: decoder(2),
                         3141: {"status": "UNAVAILABLE", "reason": reason}}}


def psi_of(dec, canon32):  # pinned recipe: one-hot 36·p + symbol, standardise, RFF, W, bias
    X = np.zeros((canon32.shape[0], 144))
    for p in range(4):
        X[np.arange(canon32.shape[0]), 36 * p + canon32[:, 28 + p].astype(int)] = 1.0
    F = x4f_scores.rbf_features((X - dec["mu_in"]) / dec["s_in"], dec["Omega"], dec["b"])
    return vphase(((F - dec["mean_F"]) / dec["scale_F"]) @ dec["W"] + dec["bias"])


def agreement(I, j) -> float:
    e, psi = I["ext"][j], psi_of(I["decoders"][j], I["canon32"])
    return float(abs(np.mean(np.exp(1j * (e.phase[e.supported] - psi[e.supported])))))


def one(phi, m32, mK) -> dict:
    return {"X": dot(phi, m32, mK), "phi": phi}


def two(phi, sup, m32, mK) -> dict:
    r, x = np.sqrt(np.sum((m32 - mK) ** 2, axis=1)), dot(phi, m32, mK)
    return {"X_minus": np.where(sup, x, -r), "X_plus": np.where(sup, x, r), "r4n": r,
            "phi": phi, "supported": sup}


def my_controls(I) -> dict:
    m, c32, ext, iext, dec = I["m"], I["canon32"], I["ext"], I["init_ext"], I["decoders"]
    m32, m4, sha = m[32], m[4], np.mod([scores.sha256_phase(r[28:32]) for r in c32], TWO_PI)
    return {
        "m4_phase": {"all": one(vphase(m4), m32, m4)},
        "sha_suffix": {"all": one(sha, m32, m4)},
        "init": {j: (dict(iext[j]) if isinstance(iext[j], dict)
                     else two(iext[j].phase, iext[j].supported, m32, m4)) for j in MODELS},
        "decoder": {j: (one(psi_of(dec[j], c32), m32, m4) if dec[j]["status"] == "AVAILABLE"
                        else {"unavailable": dec[j]["reason"]}) for j in MODELS},
        "delta1": {j: two(ext[j].phase, ext[j].supported, m32, m[1]) for j in MODELS},
        "delta2": {j: two(ext[j].phase, ext[j].supported, m32, m[2]) for j in MODELS},
        "delta4_orc": {"all": one(vphase(m32), m32, m4)},
        "naive": {j: one(ext[j].phase, m32, m4) for j in MODELS},
    }


def endpoint_arrays_for(I) -> dict:
    bounds = {"B_minus": [B_SIDE["minus"]] * N, "B_plus": [B_SIDE["plus"]] * N,
              "B_norm": [B_SIDE["norm"]] * N, "max": dict(B_SIDE)}
    return {j: {k: v for k, v in two(I["ext"][j].phase, I["ext"][j].supported, I["m"][32],
                                     I["m"][4]).items() if k in ("X_minus", "X_plus", "r4n")}
            | {"bounds": bounds} for j in MODELS}


def expected_keys(controls) -> list:
    keys = [f"X:{j}:{s}" for j in MODELS for s in "-+"]
    for name in NAMES:
        for key, e in controls[name].items():
            if "unavailable" not in e:
                keys += [f"{name}:{key}:{s}" for s in "-+"] if name in TWO else [f"{name}:{key}"]
    return keys


def bounds_for(controls, uncertified=()) -> dict:
    out = {name: {key: (dict(e) if "unavailable" in e
                        else {"max_B": Fraction(1, 10**12), "certified": True})
                  for key, e in controls[name].items()} for name in NAMES}
    for name, key in uncertified:
        out[name][key] = {"max_B": Fraction(1, 10**3), "certified": False}
    return out


def check_summary(s, draws, controls, bounds_all) -> None:
    for name in NAMES:
        for key, e in controls[name].items():
            g = at(at(s, name), key)
            if "unavailable" in e:
                assert g == e  # unavailable entries pass through unchanged
                continue
            b = bounds_all[name][key]
            assert "status" not in g, (name, key)  # R22: no status for a control
            assert g.get("label") == (None if b["certified"] else "uncertified")
            for k, r in (("alpha_bound", 84), ("one_minus_alpha_bound", 4917)):
                assert not isinstance(g[k], (tuple, list)) or int(g[k][1]) == r
            if name in TWO:  # R22: α from the X− draws, 1 − α from the X+ draws, per side
                sides = [(f"point_{s}", f"central95_{s}", draws[f"{name}:{key}:{c}"], e[f"X_{s}"])
                         for s, c in (("minus", "-"), ("plus", "+"))]
            else:
                sides = [("point", "central95", draws[f"{name}:{key}"], e["X"])]
                assert g["max_B"] == str(b["max_B"]) and bool(g["certified"]) is b["certified"]
            assert val(g["alpha_bound"]) == kth(sides[0][2], 84)
            assert val(g["one_minus_alpha_bound"]) == kth(sides[-1][2], 4917)
            for side in sides:
                check_side(g, *side)


def test_control_arrays_names_entries_shapes_and_values():
    assert tuple(k4b_fresh.CONTROL_NAMES) == NAMES
    I = inputs()
    got = k4b_fresh.control_arrays(I["m"], I["canon32"], I["ext"], I["init_ext"], I["decoders"])
    want = my_controls(I)
    assert set(got) == set(NAMES)
    for name in NAMES:
        assert set(got[name]) == set(want[name]), name  # "all" or the int models
        for key, w in want[name].items():
            g = got[name][key]
            if "unavailable" in w:
                assert set(g) == {"unavailable"} and w["unavailable"] in g["unavailable"]
                continue
            if name in TWO:
                assert {"X_minus", "X_plus", "phi", "supported"} <= set(g) and "X" not in g
                for k in ("X_minus", "X_plus"):
                    np.testing.assert_allclose(g[k], w[k], rtol=1e-12, atol=1e-14)
                assert np.array_equal(np.asarray(g["supported"], dtype=bool), w["supported"])
            else:
                assert {"X", "phi"} <= set(g) and "X_minus" not in g
                np.testing.assert_allclose(g["X"], w["X"], rtol=1e-9, atol=1e-12)
            dphi = np.angle(np.exp(1j * (np.asarray(g["phi"]) - w["phi"])))
            assert dphi.shape == (N,) and np.allclose(dphi, 0.0, atol=1e-9)


def test_bootstrap_inputs_fixed_order_one_dict():
    I = inputs()
    arrays, mine = endpoint_arrays_for(I), my_controls(I)
    controls = {name: mine[name] for name in reversed(NAMES)}  # insertion order must not matter
    got = k4b_fresh.bootstrap_inputs(arrays, controls)
    want = expected_keys(mine)
    assert list(got) == want and len(want) == 30
    assert "init:3141:-" not in got and "decoder:3141" not in got
    for k in want:
        p = k.split(":")
        if p[0] == "X":
            src = arrays[int(p[1])]["X_minus" if p[2] == "-" else "X_plus"]
        else:
            e = mine[p[0]][p[1] if p[1] == "all" else int(p[1])]
            src = e["X"] if len(p) == 2 else e["X_minus" if p[2] == "-" else "X_plus"]
        assert np.array_equal(np.asarray(got[k], dtype=np.float64), src)
    # control_summary on synthetic draws keyed as above (pure; R22 per-side form)
    rng = np.random.default_rng(8)
    draws = {k: rng.normal(size=5000) for k in want}
    bounds_all = bounds_for(mine, [("delta2", 1729), ("sha_suffix", "all")])
    check_summary(k4b_fresh.control_summary(draws, mine, bounds_all), draws, mine, bounds_all)


@pytest.mark.parametrize("reason", ["degenerate bandwidth", "equivalence"])
def test_decoder_agreement_and_unavailable_form(reason):
    I = inputs(reason)
    a = k4b_fresh.decoder_agreement(I["ext"], I["decoders"], I["canon32"])
    assert set(a) == set(MODELS)
    for j in (1729, 2718):
        assert float(a[j]) == pytest.approx(agreement(I, j), rel=1e-9, abs=1e-12)
    assert a[3141] == f"unavailable ({reason})"


@pytest.mark.parametrize("bad", [None, 0.0, -0.0, -1e-3, float("nan"), float("inf"),
                                 float("-inf")])
def test_ratios_values_and_undefined_denominators(bad):
    B4, D4, U, ap = "EX_minus_over_B4", "EX_minus_over_delta4_orc", "undefined", pytest.approx
    r = k4b_fresh.ratios(0.02, 0.04, 0.01)
    assert isinstance(r[B4], float) and r == {B4: ap(0.5), D4: ap(2.0)}
    assert k4b_fresh.ratios(-0.01, 0.02, 0.05) == {B4: ap(-0.5), D4: ap(-0.2)}
    assert k4b_fresh.ratios(0.02, bad, 0.01) == {B4: U, D4: ap(2.0)}
    assert k4b_fresh.ratios(0.02, 0.04, bad) == {B4: ap(0.5), D4: U}
    assert k4b_fresh.ratios(0.02, bad, bad) == {B4: U, D4: U}


ENTRY = two(np.zeros(N), np.ones(N, dtype=bool), np.ones((N, 2)), np.zeros((N, 2)))


@pytest.mark.parametrize("L,F,want", [
    (Fraction(3, 100), Fraction(2, 100), False),  # L − F exactly 1/100: strict, not True
    (Fraction(3, 100) + Fraction(1, 10**40), Fraction(2, 100), True),
    (Fraction(3, 100) - Fraction(1, 10**40), Fraction(2, 100), False),
    (Fraction(-1, 2), Fraction(1, 10**9), False),
    (Fraction(1, 2), Fraction(1, 10**9), True),
] + [(F + 0.01, F, None) for F in (1e-9, 2.5e-3, 0.07, 0.1, 0.123456789, 0.2, 0.3, 0.6)])
def test_init_qualifier_strict_exact(L, F, want):
    if want is None:  # float inputs: the exact L − F may fall on either side of 1/100
        want = Fraction(L) - Fraction(F) > Fraction(1, 100)
        assert k4b_fresh.init_qualifier(ENTRY, L, Fraction(F)) is want
    assert k4b_fresh.init_qualifier(ENTRY, L, F) is want
    for reason in ("chart unavailable", "uncertified"):
        got = k4b_fresh.init_qualifier({"unavailable": reason}, L, F)
        assert got == f"unavailable ({reason})"


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    I = inputs()
    arrays, controls = endpoint_arrays_for(I), my_controls(I)
    controls["init"][1729].update(X_minus=np.full(N, 0.5), X_plus=np.full(N, 0.6))
    controls["delta4_orc"]["all"]["X"] = np.full(N, -0.02)  # nonpositive comparator (§9.6)
    bounds_all = bounds_for(controls, [("init", 2718)])
    fresh_b4 = {"lower": 0.03, "rank": 250, "B_H": Fraction(1, 10**12), "Z_bound": Z,
                "status": "PASS", "point": FRESH_POINT}
    work = tmp_path_factory.mktemp("endpoint_cwd")
    calls, writes, real_open = {"c1": [], "js": []}, [], builtins.open

    def spy(layer, real):
        def fn(*a, **k):
            calls[layer].append((a, k, real(*a, **k)))
            return calls[layer][-1][2]
        return fn

    def spy_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            writes.append((str(file), mode))
        return real_open(file, mode, *a, **k)

    before = sorted(p.as_posix() for p in work.rglob("*"))
    with pytest.MonkeyPatch.context() as mp:
        mp.chdir(work)
        mp.setattr(c1_means, "bootstrap_means", spy("c1", c1_means.bootstrap_means))
        mp.setattr(k4b_stats, "joint_bootstrap", spy("js", k4b_stats.joint_bootstrap))
        if hasattr(k4b_fresh, "joint_bootstrap"):
            mp.setattr(k4b_fresh, "joint_bootstrap", k4b_stats.joint_bootstrap)
        mp.setattr(builtins, "open", spy_open)
        mp.setattr(io, "open", spy_open)
        result = k4b_fresh.endpoint(arrays, controls, bounds_all, fresh_b4, Z, I["decoders"],
                                    I["ext"], I["canon32"], I["m"], R)
    layer, after = calls["c1"] or calls["js"], sorted(p.as_posix() for p in work.rglob("*"))
    return {"I": I, "arrays": arrays, "controls": controls, "bounds_all": bounds_all,
            "result": result, "calls": calls, "draws": layer[-1][2] if layer else {},
            "writes": writes, "before": before, "after": after}


def test_endpoint_keys_single_stream_and_no_writes(run):
    res = run["result"]
    assert set(res) == RESULT_KEYS and set(res["controls"]) == set(NAMES)
    assert all(set(at(res["per_model"], j)) == PER_MODEL_KEYS for j in MODELS)
    assert isinstance(res["Z_bound"], str) and Fraction(res["Z_bound"]) == Z
    assert isinstance(res["c1prime_disclosure"], str) and res["c1prime_disclosure"]
    assert run["writes"] == [] and run["before"] == run["after"]
    c1, js = run["calls"]["c1"], run["calls"]["js"]
    assert (c1 or js) and len(c1) <= 1 and len(js) <= 1  # one joint stream
    for a, k, out in c1 + js:
        assert int(a[1] if len(a) > 1 else k["seed"]) == 610103
        assert list(a[0] if a else k["arrays"]) == expected_keys(run["controls"])
        assert all(len(v) == 5000 for v in out.values())


def expected_status(L, U, Fm, Fp):  # §8.1 in exact rationals, strict inequalities
    Lf, Uf = Fraction(L), Fraction(U)
    st = ["SUPPORT" if Lf - f > MARGIN else "EXCLUDE" if Uf + g < MARGIN and Lf - f > -MARGIN
          else "UNRESOLVED" for f, g in ((Fm, Fp), (0, 0))]
    s = "UNRESOLVED/NUMERICAL" if st[0] == "UNRESOLVED" != st[1] else st[0]
    return s, st[1], Uf + Fp < -MARGIN


def test_endpoint_per_model_bounds_margins_status_support_and_overall(run):
    I, res, draws, arrays = run["I"], run["result"], run["draws"], run["arrays"]
    m, statuses = I["m"], []
    ref = k4b_fresh.support_entries(I["ext"], R, arrays, m)
    for j in MODELS:
        p, e = at(res["per_model"], j), I["ext"][j]
        dm, dp = draws[f"X:{j}:-"], draws[f"X:{j}:+"]
        assert (p["L_rank"], p["U_rank"]) == (84, 4917)
        L, U = val(p["L"]), val(p["U"])
        assert (L, U) == (kth(dm, 84), kth(dp, 4917))
        F = {}
        for side, X, d in (("minus", arrays[j]["X_minus"], dm), ("plus", arrays[j]["X_plus"], dp)):
            b = c1_bounds.B_constant(B_SIDE[side], float(np.max(np.abs(X))), N)
            assert Fraction(p[f"B_num_{side}"]) == b and isinstance(p[f"F_{side}"], str)
            F[side] = max(b, c1_bounds.FLOOR) + Z
            assert Fraction(p[f"F_{side}"]) == F[side]
            check_side(p, f"point_{side}", f"central95_{side}", d, X)
        s, s0, neg = expected_status(L, U, F["minus"], F["plus"])
        assert (p["status"], p["status_without_F"]) == (s, s0)
        assert ("NEGATIVE_ALIGNMENT" in list(p["labels"])) is neg
        statuses.append(s)
        # support_entries: the unsealed support_report form; missing_mass = mean((1 − A)·r4n)
        sup = k4b_scores.support_report(e, R, arrays[j]["r4n"], e.phase, m[32], m[4], False)
        assert set(at(ref, j)) == set(sup) == set(p["support"])
        assert "supported_contribution" in at(ref, j)
        assert int(at(ref, j)["n_supported"]) == int(e.supported.sum())
        missing = float(np.mean((1.0 - e.supported.astype(float)) * arrays[j]["r4n"]))
        assert all(float(mm) == pytest.approx(missing, rel=1e-12, abs=1e-15)
                   for mm in (p["missing_mass"], at(ref, j)["missing_mass"], float(p["width"]) / 2))
    definite = [s for s in statuses if s in ("SUPPORT", "EXCLUDE")]
    want = "INCONCLUSIVE" + ("/NUMERICAL" if "UNRESOLVED/NUMERICAL" in statuses else "")
    if definite:
        want = "MIXED" if len(definite) < 3 or len(set(definite)) > 1 else \
            {"SUPPORT": "SUPPORT", "EXCLUDE": "EXCLUSION"}[definite[0]]
    assert res["overall"] == want


def test_endpoint_summaries_ratios_init_qualifier_and_agreement(run):  # R20, R21, R22
    res, I = run["result"], run["I"]
    check_summary(res["controls"], run["draws"], run["controls"], run["bounds_all"])
    for j in MODELS:
        r, pm = at(res["ratios"], j), val(at(res["per_model"], j)["point_minus"])
        assert float(r["EX_minus_over_B4"]) == pytest.approx(pm / FRESH_POINT, rel=1e-12)
        assert r["EX_minus_over_delta4_orc"] == "undefined"
    assert float(res["fresh_B4"]["point"]) == FRESH_POINT
    assert "FRESH_B4_LOW" not in repr(res["fresh_B4"])
    q, a = res["init_qualifier"], res["decoder_agreement"]
    assert at(q, 1729) is True and at(q, 2718) == "unavailable (uncertified)"
    assert at(q, 3141) == "unavailable (chart unavailable)"
    for j in (1729, 2718):
        assert float(at(a, j)) == pytest.approx(agreement(I, j), rel=1e-9, abs=1e-12)
    assert at(a, 3141) == "unavailable (degenerate bandwidth)"
