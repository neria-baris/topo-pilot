"""Author A (job 0198): the OF gates OF-2 ... OF-5, the outcome rule and the tails report
(protocol §4.2, §4.3, S3 §4.1; DRO4, DRO5, DRO8) on hand-built gate contexts (API §4)."""

from __future__ import annotations  # noqa: I001

import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_pairs as up  # noqa: E402
import hwsu_oracle as uo  # noqa: E402
import hwsu_of as uof  # noqa: E402
import hwsu_driver_of as udr  # noqa: E402
import hwsu_dry as udry  # noqa: E402
import c1_means  # noqa: E402
import c1_records  # noqa: E402
import c2_attrib  # noqa: E402
import c2_decide  # noqa: E402
import c2_stats  # noqa: E402
import numpy as np  # noqa: E402
import precision  # noqa: E402
import pytest  # noqa: E402
from topo_pilot.dataset import sampler as tsampler  # noqa: E402

SEEDS = uc.DRY_SEEDS_OF
FEAS = "INCONCLUSIVE/ORACLE_FEASIBILITY"


def make_ctx(tmp_path, **kw):
    ctx = udr.build_ctx(tmp_path / "hwsu-dry-of", "0198t", 1, "RES-HWSU-OF", root=tmp_path,
                        mailbox=tmp_path / "agent-handoff", hwsc_store=tmp_path / "hwsc-store",
                        scope=uc.SCOPE_DRY, seeds=SEEDS, dry=True)
    ctx.update(kw)
    return ctx


def status(fn, ctx):
    """A gate returns details with "status" or raises C1GateFailure (API §4); both count."""
    try:
        det = fn(ctx) or {}
    except c1_records.C1GateFailure as exc:
        return exc.status, {}
    return det.get("status", "PASS"), det


def fr(x):
    return Fraction(str(x))


# ---- OF-2: headroom, L(mean G) > 0.02 nat, exact comparison ---------------------------------
def _of2_with_bound(tmp_path, monkeypatch, L, rank=250):
    G = np.full(64, 0.03)
    seen = {}

    def fake(arrays, seed, alpha, draws=20000):
        seen.update(keys=list(arrays), seed=seed, alpha=alpha, draws=draws, G=arrays["G"])
        return {"G": {"mean": 0.03, "L": L, "U": 0.04, "rank_L": rank, "rank_U": 4751}}

    monkeypatch.setattr(c2_decide, "stream_bounds", fake)
    st = status(uof.of_2, make_ctx(tmp_path, pc={"G": G, "d": np.zeros((64, 36))}))[0]
    assert seen, "OF-2 must call c2_decide.stream_bounds at call time (API §0, §4 OF-2)"
    assert seen["keys"] == ["G"] and np.array_equal(seen["G"], G)
    got = (seen["seed"], fr(seen["alpha"]), seen["draws"])
    assert got == (SEEDS["headroom"], Fraction(1, 20), 5000)
    return st


def test_of_2_boundary_is_exact(tmp_path, monkeypatch):
    below = float(np.nextafter(0.02, 0.0))
    assert Fraction(below) < Fraction(1, 50) < Fraction(0.02)  # the double 0.02 lies above 1/50
    assert _of2_with_bound(tmp_path, monkeypatch, below) == FEAS
    # SPEC-QUESTION: TEST_PLAN says "L = 0.02 exactly ... is not a pass"; under the protocol's
    # exact comparison (API: Fraction(float(L)) > 1/50) the double 0.02 exceeds 1/50 and passes.
    assert _of2_with_bound(tmp_path, monkeypatch, 0.02) == "PASS"
    assert _of2_with_bound(tmp_path, monkeypatch, float(np.nextafter(0.02, 1.0))) == "PASS"
    assert _of2_with_bound(tmp_path, monkeypatch, -0.5) == FEAS


def test_of_2_rank_is_checked(tmp_path, monkeypatch):
    # API-AMBIGUITY: the status of a wrong rank is not named; it must not be PASS.
    assert _of2_with_bound(tmp_path, monkeypatch, 0.5, rank=251) != "PASS"


def test_of_2_real_bounds(tmp_path):
    rng = np.random.Generator(np.random.PCG64(41))
    hi = 0.05 + 0.01 * rng.random(512)
    st, _ = status(uof.of_2, make_ctx(tmp_path / "a", pc={"G": hi}))
    b = c2_decide.stream_bounds({"G": hi}, SEEDS["headroom"], Fraction(1, 20), 5000)
    assert b["G"]["rank_L"] == 250 and st == "PASS" and Fraction(b["G"]["L"]) > Fraction(1, 50)
    assert status(uof.of_2, make_ctx(tmp_path / "b", pc={"G": hi / 5}))[0] == FEAS


# ---- OF-3: the code-share ceiling on a planted oracle (DRO4) ---------------------------------
def _of3_ctx(tmp_path, c, rng):
    n = 400
    G = 0.02 + 0.03 * rng.random(n)
    q1 = rng.dirichlet(np.ones(36), size=n)
    q2 = rng.dirichlet(np.ones(36), size=n)
    o = {k: {"qbar": q, "logq": np.log(q)} for k, q in (("o1", q1), ("o2", q2))}
    of = {"logq": np.log(rng.dirichlet(np.ones(36), size=n)), "nuis": rng.normal(size=(n, 5)),
          "m32": rng.normal(size=(n, 2))}
    fit = {"canon32": rng.integers(0, 36, size=(n, 32)).astype(np.uint8), "ids": np.arange(n)}
    pc = {"G": G, "d": q1 - q2}
    return make_ctx(tmp_path, of=of, fit=fit, pc=pc, o1=o["o1"], o2=o["o2"]), G, c * G


def _plant(monkeypatch, A_S, A_full, bad=()):
    """Seams: c2_stats.f1_problem (the fit status per (K, euclidean)) and c2_attrib.partition
    (the planted A_S). Each variant gets a distinct share ratio so it can be recognised."""
    calls = []

    def f1(Y, w32, zt, f, euclidean=False, fit=None):
        K = np.shape(f)[1] // 2
        calls.append((K, bool(euclidean)))
        p = np.shape(Y)[1]
        st = "INCONCLUSIVE/PATCH_MODEL_DEGENERATE" if (K, bool(euclidean)) in bad else "PASS"
        tag = {(3, False): 1.0, (1, False): 0.5, (3, True): 0.25}[(K, bool(euclidean))]
        return {"status": st, "ref": {"delta_P_S": "0"}, "euclidean": bool(euclidean),
                "fit": {"rank": 41 + 2 * K}, "Sigma": np.eye(p),
                "g": {"P_S": np.eye(p) * tag, "P_G": np.zeros((p, p))}}

    def part(d, M, dy, P_S, P_G):
        t = float(P_S[0, 0])
        return {"A_full": A_full, "A_S": t * A_S, "A_G": np.zeros_like(A_S),
                "A_rest": A_full - t * A_S}

    monkeypatch.setattr(c2_stats, "f1_problem", f1)
    monkeypatch.setattr(c2_attrib, "partition", part)
    return calls


def _flat(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from _flat(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _flat(v)
    else:
        yield x


@pytest.mark.parametrize("c,want", [(0.5, "PASS"), (0.1, "SHARE_DROPPED")])
def test_of_3_share_ceiling(tmp_path, monkeypatch, c, want):
    ctx, G, A_S = _of3_ctx(tmp_path, c, np.random.Generator(np.random.PCG64(42)))
    calls = _plant(monkeypatch, A_S, G.copy(), bad={(3, True)})
    st, det = status(uof.of_3, ctx)
    assert st == want
    assert calls[0] == (3, False) and set(calls) == {(3, False), (1, False), (3, True)}
    Z = {"Z020": A_S - 0.2 * G, "Z050": A_S - 0.5 * G, "AS": A_S, "G": G}
    b = c2_decide.stream_bounds(Z, SEEDS["share"], Fraction(1, 60), 5000)
    assert b["Z020"]["rank_L"] == 84
    # the planted δ_P is 0, so the A_S-term guard β is 0 and g = c2_decide.guard(Z020)
    assert (b["Z020"]["L"] > c2_decide.guard(Z["Z020"])) == (want == "PASS")
    psi = float(c1_means.tree_mean(A_S) / c1_means.tree_mean(G))
    blob = list(_flat(det)) + list(_flat(ctx.get("psi", {})))
    # API-AMBIGUITY: where ψ_orc and the variants sit in the details / ctx["psi"] is not fixed;
    # the point value, the K = 1 variant (ratio 0.5ψ) and NOT_COMPUTED (Euclidean) must appear.
    assert any(isinstance(v, float) and v == pytest.approx(psi, rel=1e-12) for v in blob)
    assert any(isinstance(v, float) and v == pytest.approx(0.5 * psi, rel=1e-12) for v in blob)
    assert "NOT_COMPUTED" in blob
    assert "pr" in ctx and "sa" in ctx
    if want == "SHARE_DROPPED":
        assert "INCONCLUSIVE/ORACLE_FEASIBILITY" in blob  # the share outcome (S3)


def test_of_3_degenerate_primary_fit(tmp_path, monkeypatch):
    ctx, G, A_S = _of3_ctx(tmp_path, 0.5, np.random.Generator(np.random.PCG64(43)))
    _plant(monkeypatch, A_S, G.copy(), bad={(3, False)})
    assert status(uof.of_3, ctx)[0] == "FAIL_TECHNICAL/NUMERICAL"


# ---- OF-4 gate logic with recording precision kernels (the real kernels: test_a_of_ladder) ---
LADDER = (4096, 8192, 16384, 32768)


def _of4(tmp_path, monkeypatch, passes, results, n=300, shift=0.0):
    rng = np.random.Generator(np.random.PCG64(44))
    G = 0.01 + rng.random(n)
    A_full, A_S = G * 1.0 + shift, 0.3 * G + 0.01 * rng.random(n)
    arrays = {"ZR010": A_full - 0.1 * G, "ZR030": A_full - 0.3 * G,
              "Z010": A_S - 0.1 * G, "Z050": A_S - 0.5 * G}
    names = list(arrays)
    log = {"sd": [], "e": [], "cfg": []}

    def which(X):
        hit = [k for k in names if np.allclose(X["oracle"], arrays[k], rtol=0, atol=1e-15)]
        assert len(hit) == 1
        return names.index(hit[0])

    def sd_draws(X, r4n, models, seed, draws, size):
        assert np.array_equal(r4n["oracle"], G) and list(models) == ["oracle"]
        log["sd"].append((names[which(X)], seed, draws, size))
        return np.full((draws, 1), float(which(X))), np.zeros((draws, 1))

    def c_draws(X, models, seed, draws, size):
        log["e"].append((names[which(X)], seed, draws, size))
        return np.full((draws, 1), float(size))

    def summary(sd, e, models, cfg):
        name, N = names[int(sd[0, 0])], int(e[0, 0])
        log["cfg"].append((name, dict(cfg)))
        assert cfg["projected_N"] == N
        met = N >= passes[name] if passes[name] else False
        m = {"sd_lower": 1.0, "sd_upper": 1.0, "mde_lower": 0.0, "mde_upper": 0.0,
             "q_alpha": 0.0, "power": 1.0 if met else 0.0}
        return {"models": {"oracle": m}, "status": "PASS" if met else "INCONCLUSIVE",
                "criterion_met": met}

    monkeypatch.setattr(precision, "sd_b4_draws", sd_draws)
    monkeypatch.setattr(precision, "centered_draws", c_draws)
    monkeypatch.setattr(precision, "precision_summary", summary)
    ctx = make_ctx(tmp_path, sa={"A_full": A_full, "A_S": A_S, "A_G": 0 * G, "A_rest": 0 * G},
                   pc={"G": G, "d": np.zeros((n, 36))}, results=dict(results))
    st = status(uof.of_4, ctx)[0]
    return st, ctx, log, G


def test_of_4_calls_and_alternatives(tmp_path, monkeypatch):
    passes = {"ZR010": 4096, "ZR030": 8192, "Z010": 16384, "Z050": 8192}
    st, ctx, log, G = _of4(tmp_path, monkeypatch, passes, {"OF-3": "PASS"})
    assert st == "PASS" and (ctx["N_resp"], ctx["N_share"]) == (8192, 16384)
    assert [x[0] for x in log["sd"]] == ["ZR010", "ZR030", "Z010", "Z050"]
    assert all(x[1:] == (SEEDS["p1_sd"], 5000, len(G)) for x in log["sd"])
    assert [(x[0], x[3]) for x in log["e"]] == [(k, N) for k in passes for N in LADDER]
    assert all(x[1:3] == (SEEDS["p1_centred"], 5000) for x in log["e"])
    mG = float(c1_means.tree_mean(G))
    for name, cfg in log["cfg"]:
        alt = (0.10 if name.startswith("ZR") else 0.03) * mG
        assert cfg["alternative"] == pytest.approx(alt, rel=1e-14), name
        assert cfg["alpha"] == pytest.approx(1 / 300, rel=1e-15)
        assert (cfg["power"], cfg["delta"]) == (pytest.approx(0.8, rel=1e-15), 0.0)


@pytest.mark.parametrize("passes,prior,want,nr,ns", [
    ({"ZR010": 4096, "ZR030": 4096, "Z010": None, "Z050": 4096}, "PASS", "SHARE_DROPPED", 4096,
     None),
    ({"ZR010": None, "ZR030": 4096, "Z010": 4096, "Z050": 4096}, "PASS", FEAS, None, 4096),
    ({"ZR010": 32768, "ZR030": 4096, "Z010": 4096, "Z050": 4096}, "SHARE_DROPPED", "SHARE_DROPPED",
     32768, 4096),
    ({"ZR010": 8192, "ZR030": None, "Z010": 4096, "Z050": 4096}, "SHARE_DROPPED", FEAS, None, 4096),
])
def test_of_4_family_rules(tmp_path, monkeypatch, passes, prior, want, nr, ns):
    st, ctx, log, _ = _of4(tmp_path, monkeypatch, passes, {"OF-3": prior})
    assert st == want
    assert ctx.get("N_resp") == nr
    # after an OF-3 SHARE_DROPPED every array is still computed (API OF-4, D-21).
    # SPEC-QUESTION: protocol §4.1 S3 / DRO8 say "no share array is formed downstream"; whether
    # that covers OF-4's share proxy arrays is not asserted here either way.
    assert len(log["sd"]) == 4
    if prior == "PASS" and want != FEAS:  # API-AMBIGUITY: ctx after a raised failure is open
        assert ctx.get("N_share") == ns


# ---- OF-5: Lemma P cross-check on tiny-world pairs (DRO5) ------------------------------------
@pytest.fixture(scope="module")
def tiny():
    w = udry.tiny_world()
    p = up.sample_pairs(w["T"], w["E_canon_shared"], w["pi"], uc.SCOPE_DRY, "of-eval", 0, 2048)
    return w, p["a1"], p["a2"]


def _pi_sampler(T, E, pi, a1, rng):
    """Planted defect: z_28 ~ π instead of the bridge (β dropped); otherwise API §2.2."""
    n, P = len(a1), a1.shape[1] - 4
    Tr = (pi[None, :] * T.T) / pi[:, None]
    cumE, cumR = tsampler._cumulative_rows(E), tsampler._cumulative_rows(Tr)
    z = tsampler._draw(tsampler._cumulative_rows(np.tile(pi, (n, 1))), np.arange(n), rng.random(n))
    out = a1.copy()
    for t in range(P, 0, -1):
        out[:, t - 1] = tsampler._draw(cumE, z, rng.random(n))
        if t > 1:
            z = tsampler._draw(cumR, z, rng.random(n))
    return out


def _lemma_ctx(tmp_path, w, a1, a2):
    T, E, pi, co = w["T"], w["E_canon_shared"], w["pi"], w["coords"]
    o1, o2 = uo.arm_oracle(T, E, pi, a1, co), uo.arm_oracle(T, E, pi, a2, co)
    s1 = uo.suffix_oracle(T, E, pi, [a1, a2], co)[0]
    return make_ctx(tmp_path, o1=o1, o2=o2, s1=s1, pc=uo.pair_core(o1, o2))


def _my_lemma(ctx):
    o1, o2, s1, G = ctx["o1"], ctx["o2"], ctx["s1"], ctx["pc"]["G"]

    def unit(m):
        ok = np.hypot(m[:, 0], m[:, 1]) > 1e-12
        ph = np.where(ok, np.arctan2(m[:, 1], m[:, 0]), 0.0)
        return np.column_stack((np.cos(ph), np.sin(ph)))

    u1, u2 = unit(o1["m32"]), unit(o2["m32"])
    a = {"pairU": 0.5 * np.sum((u1 - u2) * (o1["m32"] - o2["m32"]), axis=1),
         "rowU": np.sum(u1 * (o1["m32"] - s1["m4"]), axis=1), "pairG": G,
         "rowG": np.sum((o1["qbar"] - s1["q4bar"]) * o1["logq"], axis=1)}
    m = c1_means.bootstrap_means(a, SEEDS["lemma_p"], 5000)
    ok = True
    for Q in "UG":
        diff = c1_means.tree_mean(a["pair" + Q]) - c1_means.tree_mean(a["row" + Q])
        se = np.std(m["pair" + Q] - m["row" + Q], ddof=1)
        ok = ok and Fraction(abs(float(diff))) <= 5 * Fraction(float(se))
    return a, ok


def test_of_5_real_sampler_passes(tmp_path, tiny):
    w, a1, a2 = tiny
    ctx = _lemma_ctx(tmp_path, w, a1, a2)
    a, ok = _my_lemma(ctx)
    assert ok and status(uof.of_5, ctx)[0] == "PASS"
    for k, v in a.items():
        assert np.allclose(ctx["lemma"][k], v, rtol=1e-12, atol=1e-15), k


def test_of_5_planted_pi_sampler_fails(tmp_path, tiny):
    w, a1, _ = tiny
    T, E, pi = (np.asarray(w[k], dtype=np.float64) for k in ("T", "E_canon_shared", "pi"))
    bad = _pi_sampler(T, E, pi, a1, np.random.Generator(np.random.PCG64(SEEDS["lemma_p"])))
    ctx = _lemma_ctx(tmp_path, w, a1, bad)
    assert not _my_lemma(ctx)[1]
    assert status(uof.of_5, ctx)[0] == "FAIL_TECHNICAL/SAMPLER"


# ---- the OF outcome (DRO8) and the tails report ---------------------------------------------
GATES = ("OF-B", "OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2", "OF-3", "OF-4",
         "OF-5")


def recs(**over):
    return [{"gate": g, "status": over.get(g.replace("-", "_"), "PASS")} for g in GATES]


def test_of_outcome():
    assert uof.of_outcome(recs()) == "OF_PASS"
    assert uof.of_outcome(recs(OF_3="SHARE_DROPPED")) == "OF_PASS_RESPONSE_ONLY"
    r = recs(OF_3="SHARE_DROPPED", OF_4="SHARE_DROPPED")
    assert uof.of_outcome(r) == "OF_PASS_RESPONSE_ONLY"
    r = recs(OF_3="SHARE_DROPPED", OF_4=FEAS, OF_5="NOT_RUN")
    assert uof.of_outcome(r) == FEAS
    r = recs(OF_1="FAIL_TECHNICAL/ORACLE", OF_2="NOT_RUN", OF_3="NOT_RUN", OF_4="NOT_RUN",
             OF_5="NOT_RUN")
    assert uof.of_outcome(r) == "FAIL_TECHNICAL/ORACLE"
    assert uof.of_outcome([{"gate": "OF-B", "status": "INVALID"}]) == "INVALID"
    assert uof.of_outcome(recs(OF_2="PAUSE", OF_3="NOT_RUN")) == "PAUSE"


def test_tails():
    G = np.arange(1, 251) / 256.0  # exact dyadic values
    t = uof.tails(G)
    k = math.ceil(0.01 * 250)
    vals = [Fraction(int(i), 256) for i in range(1, 251)]
    top = sum(sorted(vals)[-k:]) / sum(vals)
    mean = sum(vals) / len(vals)
    m2 = sum((v - mean) ** 2 for v in vals) / len(vals)
    m4 = sum((v - mean) ** 4 for v in vals) / len(vals)
    assert (k, top) == (3, Fraction(747, 31375))
    assert t["top1pct_share"] == pytest.approx(float(top), rel=1e-12)
    assert t["kurtosis"] == pytest.approx(float(m4 / m2 ** 2), rel=1e-12)
    two = uof.tails(np.array([0.0, 1.0] * 50))
    assert two["kurtosis"] == pytest.approx(1.0, rel=1e-12)  # Pearson, not excess
    assert two["top1pct_share"] == pytest.approx(1 / 50, rel=1e-12)
