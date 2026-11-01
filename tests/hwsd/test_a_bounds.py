"""Author A (job 0197): per-checkpoint bounds and F (§5.1, §5.6, §7 row 13; DRD5, S2).

Ranks 84/4,917 (125/4,875) of the main 5,000-draw joint bootstrap (seed 620413) and the
strong ranks 70/49,931 of the separate 50,000-draw bootstrap (seed 620416; dry 629965).
Expected values: an independent np.sort index, an independent PCG64 index stream, and the
reused c1_means/k4b_cert functions as stated in their public APIs.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_bind as db  # noqa: E402
import hwsd_summary as dsum  # noqa: E402
import c1_means  # noqa: E402
import k4b_cert  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

J = (620301, 620302, 620303)


def own_draws(arrays, seed, draws):
    """Independent stream: one PCG64(seed); per draw one integers(0, n, size=n) for all arrays."""
    rng = np.random.Generator(np.random.PCG64(seed))
    n = len(next(iter(arrays.values())))
    out = {k: np.empty(draws) for k in arrays}
    for d in range(draws):
        idx = rng.integers(0, n, size=n)
        for k, a in arrays.items():
            out[k][d] = float(np.mean(a[idx]))
    return out


# ---- constants and rank rules ----
def test_rank_constants():
    assert dc.DRAWS == 5000 and dc.STRONG_DRAWS == 50000
    assert dc.STRONG_RANKS == {"lo": 70, "hi": 49931}
    assert {k: dc.RANKS[k] for k in ("alpha", "one_minus_alpha", "central_lo", "central_hi",
                                     "b4_lower")} == {"alpha": 84, "one_minus_alpha": 4917,
                                                      "central_lo": 125, "central_hi": 4875,
                                                      "b4_lower": 250}
    assert dc.P_LO == Fraction(1, 720) and dc.P_HI == Fraction(719, 720)
    assert math.ceil(50000 * Fraction(1, 720)) == 70
    assert math.ceil(50000 * Fraction(719, 720)) == 49931
    assert math.ceil(5000 * Fraction(1, 60)) == 84 and math.ceil(5000 * Fraction(59, 60)) == 4917
    assert dc.SEEDS["endpoint"] == 620413 and dc.STRONG_SEED == 620416
    assert dc.DRY_STRONG_SEED == 629965
    assert dc.ALPHA == Fraction(1, 60) and 12 * Fraction(1, 720) == dc.ALPHA  # Bonferroni §5.6


# ---- strong_bounds ----
def test_strong_bounds_ranks_70_and_49931():
    rng = np.random.default_rng(3)
    dm = rng.permutation(np.linspace(-1.0, 1.0, 50000))
    dp = rng.normal(size=50000)
    r = dsum.strong_bounds(dm, dp)
    assert r["L_S"] == np.sort(dm)[69] and r["U_S"] == np.sort(dp)[49930]
    assert r["L_S_rank"] == 70 and r["U_S_rank"] == 49931


@pytest.mark.parametrize("bad", ["nan", "inf", "short"])
def test_strong_bounds_refuses_bad_draws(bad):
    d = np.random.default_rng(4).normal(size=50000)
    if bad == "nan":
        d[123] = np.nan
    elif bad == "inf":
        d[7] = np.inf
    else:
        d = d[:5000]
    with pytest.raises(C1GateFailure) as e:
        dsum.strong_bounds(d, np.sort(np.abs(d)))
    assert e.value.status == "FAIL_TECHNICAL/NUMERICAL"


# ---- main bootstrap (seed 620413) ----
def _arrays(n=64, seed=8):
    rng = np.random.default_rng(seed)
    return {"X:620301:0:-": rng.normal(size=n), "X:620301:0:+": rng.normal(size=n) + 0.1,
            "m4_phase:all": rng.normal(size=n)}


def test_main_bootstrap_equals_c1_means_and_own_stream():
    a = _arrays()
    d = dsum.main_bootstrap(a, seed=620413)
    ref = c1_means.bootstrap_means(a, 620413, 5000)
    assert set(d) == set(a)
    for k in a:
        assert len(d[k]) == 5000 and np.array_equal(np.asarray(d[k]), ref[k])
    own = own_draws(a, 620413, 40)
    for k in a:
        np.testing.assert_allclose(np.asarray(d[k])[:40], own[k], rtol=0, atol=1e-12)


def test_main_bootstrap_default_seed_inside_binding_and_stream_shared():
    a = _arrays()
    with db.bound_hwsd():
        d = dsum.main_bootstrap(a)
    assert np.array_equal(np.asarray(d["X:620301:0:-"]),
                          np.asarray(dsum.main_bootstrap(a, seed=620413)["X:620301:0:-"]))
    solo = dsum.main_bootstrap({"m4_phase:all": a["m4_phase:all"]}, seed=620413)
    rev = dsum.main_bootstrap(dict(reversed(list(a.items()))), seed=620413)
    assert np.array_equal(np.asarray(solo["m4_phase:all"]), np.asarray(d["m4_phase:all"]))
    assert np.array_equal(np.asarray(rev["m4_phase:all"]), np.asarray(d["m4_phase:all"]))


# ---- strong bootstrap (seed 620416 / dry 629965) ----
def _scores(n=3072, with_arrays=((620301, 100), (620302, 0)), seed=9):
    rng = np.random.default_rng(seed)
    sc = {}
    for j in J:
        for step in dc.STEPS:
            arrays = None
            if (j, step) in with_arrays:
                xm = rng.normal(size=n)
                arrays = {"X_minus": xm, "X_plus": xm + np.abs(rng.normal(size=n)) * 0.01,
                          "r4n": np.abs(rng.normal(size=n)), "phi": rng.uniform(0, 6, n),
                          "supported": np.ones(n, dtype=bool),
                          "delta1_X_minus": rng.normal(size=n), "delta1_X_plus": rng.normal(size=n),
                          "delta2_X_minus": rng.normal(size=n), "delta2_X_plus": rng.normal(size=n),
                          "naive_X": rng.normal(size=n)}
                if j == 620301:
                    arrays["decoder_X"] = rng.normal(size=n)
                    arrays["decoder_phi"] = rng.uniform(0, 6, n)
            dec = {"status": "AVAILABLE" if (arrays is not None and j == 620301) else "UNAVAILABLE",
                   "reason": ""}
            sc[(j, step)] = {"record": {"master": j, "step": step, "decoder": dec},
                             "learn": {}, "arrays": arrays}
    return sc


X_KEYS = ["X:620301:100:-", "X:620301:100:+", "X:620302:0:-", "X:620302:0:+"]


def _x_arrays(sc):
    return {"X:620301:100:-": sc[(620301, 100)]["arrays"]["X_minus"],
            "X:620301:100:+": sc[(620301, 100)]["arrays"]["X_plus"],
            "X:620302:0:-": sc[(620302, 0)]["arrays"]["X_minus"],
            "X:620302:0:+": sc[(620302, 0)]["arrays"]["X_plus"]}


def test_strong_bootstrap_seed_draws_and_keys_spy(monkeypatch, tmp_path):
    # API-AMBIGUITY: `scores[(j, step)]["arrays"]` read as a mapping with the ARRAYS.npz keys.
    calls = []
    real = c1_means.bootstrap_means

    def spy(arrays, seed, draws=5000):
        calls.append((list(arrays), seed, draws))
        return real({k: v[:8] for k, v in arrays.items()}, seed, 3)

    monkeypatch.setattr(c1_means, "bootstrap_means", spy)
    sc = _scores()
    with db.bound_hwsd():
        dsum.strong_bootstrap(sc)
    with db.bound_hwsd(db.load_table(which="dry", case="A", case_dir=tmp_path)):
        dsum.strong_bootstrap(sc)
    dsum.strong_bootstrap(sc, seed=12345)
    assert [c[0] for c in calls] == [X_KEYS] * 3
    assert [c[1] for c in calls] == [620416, 629965, 12345]
    assert [c[2] for c in calls] == [50000] * 3


@pytest.mark.slow
def test_strong_bootstrap_bitwise_and_seed_sensitive():
    sc = _scores()
    with db.bound_hwsd():
        d = dsum.strong_bootstrap(sc)
    xs = _x_arrays(sc)
    ref = c1_means.bootstrap_means(xs, 620416, 50000)
    for k in X_KEYS:
        assert np.array_equal(np.asarray(d[k]), ref[k])
    own16, own13 = own_draws(xs, 620416, 30), own_draws(xs, 620413, 30)
    np.testing.assert_allclose(np.asarray(d[X_KEYS[0]])[:30], own16[X_KEYS[0]], rtol=0, atol=1e-12)
    assert not np.allclose(np.asarray(d[X_KEYS[0]])[:30], own13[X_KEYS[0]], rtol=0, atol=1e-9)
    b = dsum.strong_bounds(d[X_KEYS[0]], d[X_KEYS[1]])
    assert b["L_S"] == np.sort(ref[X_KEYS[0]])[69] and b["U_S"] == np.sort(ref[X_KEYS[1]])[49930]


# ---- F per side ----
def test_f_sides_planted_and_certified():
    Fm, Fp = dsum.f_sides({"planted": True}, Fraction(1, 10**8))
    assert Fm == Fp == Fraction(1, 10**9) == dc.F_PLANTED
    Z = Fraction(87876736540276863476307541, 78125 * 10**33)
    rec = {"planted": False, "certificate": {
        "max_B": {"X_minus": "1/1000000", "X_plus": "3/1000000", "n_hat": "0"},
        "max_abs": {"X_minus": 0.25, "X_plus": 0.5}}}
    Fm, Fp = dsum.f_sides(rec, Z)
    for F, side in ((Fm, "X_minus"), (Fp, "X_plus")):
        bn = k4b_cert.b_num(Fraction(rec["certificate"]["max_B"][side]),
                            rec["certificate"]["max_abs"][side], 3072)
        assert F == k4b_cert.margin(bn, Z) == max(bn, Fraction(1, 10**9)) + Z
        assert isinstance(F, Fraction)
    assert Fp > Fm  # larger max_B and max_abs on the + side
    Fm2, _ = dsum.f_sides(rec, Z, n=1024)
    assert Fm2 == k4b_cert.margin(k4b_cert.b_num(Fraction(1, 10**6), 0.25, 1024), Z)
    zero = {"X_minus": "0", "X_plus": "0", "n_hat": "0"}
    tiny = {"planted": False, "certificate": {"max_B": zero,
                                              "max_abs": {"X_minus": 0.0, "X_plus": 0.0}}}
    bn0 = k4b_cert.b_num(Fraction(0), 0.0, 3072)
    assert dsum.f_sides(tiny, Z) == (max(bn0, Fraction(1, 10**9)) + Z,) * 2


# ---- bootstrap inputs: names and registered order (§7 row 13) ----
def test_bootstrap_inputs_d_order_and_values():
    sc = _scores(n=3072, with_arrays=((620301, 50), (620301, 100), (620303, 4000)))
    rng = np.random.default_rng(1)
    shared = {name: {"all": {"X": rng.normal(size=3072), "phi": rng.uniform(0, 6, 3072)}}
              for name in ("m4_phase", "sha_suffix", "delta4_orc")}
    inp = dsum.bootstrap_inputs_d(sc, shared)
    want = []
    for j, step in ((620301, 50), (620301, 100), (620303, 4000)):
        want += [f"X:{j}:{step}:-", f"X:{j}:{step}:+"]
        if j == 620301:
            want.append(f"decoder:{j}:{step}")
        want += [f"delta1:{j}:{step}:-", f"delta1:{j}:{step}:+", f"delta2:{j}:{step}:-",
                 f"delta2:{j}:{step}:+", f"naive:{j}:{step}"]
    want += ["m4_phase:all", "sha_suffix:all", "delta4_orc:all"]
    assert list(inp) == want
    a = sc[(620301, 100)]["arrays"]
    for key, src in (("X:620301:100:-", "X_minus"), ("X:620301:100:+", "X_plus"),
                     ("decoder:620301:100", "decoder_X"), ("delta1:620301:100:-", "delta1_X_minus"),
                     ("delta2:620301:100:+", "delta2_X_plus"), ("naive:620301:100", "naive_X")):
        assert np.array_equal(np.asarray(inp[key]), a[src])
    assert np.array_equal(np.asarray(inp["sha_suffix:all"]), shared["sha_suffix"]["all"]["X"])
    for v in inp.values():
        assert np.asarray(v).dtype == np.float64 and np.asarray(v).shape == (3072,)
