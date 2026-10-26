"""Author A (job 0119): z constants, bounds, ranks, nulls, E5 and the Pinsker count.

TEST_PLAN §2 `test_a_stats.py`; protocol §5.3 items 1-5, §2.5 (E5), §2.3 (Pinsker count).
Expected values are computed here (NormalDist, an own tree mean, planted vectors); the CONTRACT
file is read only for its frozen arguments.
"""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
HWS_DIR = str(REPO / "tools" / "hws")
if HWS_DIR not in sys.path:
    sys.path.insert(0, HWS_DIR)

import hws_worlds as hw  # noqa: E402,F401  (first import: sets the tool paths)
import hws_stats as hs  # noqa: E402
import c1_means  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
TWO_PI = 2.0 * np.pi
CENTRES = (np.arange(12) + 0.5) * TWO_PI / 12  # one phase in the middle of each E5 bin


def _z(alpha):
    return NormalDist().inv_cdf(float(1 - alpha))


def _tree_mean(x):
    level = [float(v) for v in x]
    n = len(level)
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0] / n


def _m32(phases, norms=1.0):
    phases = np.asarray(phases, dtype=np.float64)
    return np.column_stack((norms * np.cos(phases), norms * np.sin(phases)))


ZCASES = [("Z1", "Z1", Fraction(1, 100), 2.326), ("ZW", "ZW", Fraction(1, 24640), 3.941),
          ("Z3", "Z3", Fraction(1, 320), 2.734), ("ZNULL", "ZNULL", Fraction(1, 432600), 4.581),
          ("Z975", "central95", Fraction(1, 40), 1.960)]


def test_alpha_derivations():
    assert 150 + 102 + 40 + 16 == 308  # N_slots: S1 + X1 + S2 + S3
    assert 7 * (1 + 292 + 16) == 2163  # N_null
    assert Fraction(5, 100) / (4 * 308) == Fraction(1, 24640)
    assert Fraction(1, 100) / (2 * 2163) == Fraction(1, 432600)
    assert Fraction(5, 100) / 16 == Fraction(1, 320)
    z = CONTRACT["z"]
    assert z["ZW"]["N_slots"] == 308 and sum(z["ZW"]["slots"].values()) == 308
    assert z["ZNULL"]["N_null"] == 2163
    for _, ckey, alpha, _ in ZCASES:
        key = "alpha_each_side" if ckey == "central95" else "alpha"
        assert Fraction(z[ckey][key]) == alpha


@pytest.mark.parametrize("name, ckey, alpha, approx", ZCASES)
def test_z_constants(name, ckey, alpha, approx):
    val = getattr(hs, name)
    assert isinstance(val, float)
    assert val == _z(alpha)
    assert hs.z_of(alpha) == _z(alpha)
    assert abs(val - approx) < 5e-4
    assert abs(val - CONTRACT["z"][ckey]["report_only"]) < 1e-9


def test_rank_f_is_16():
    assert hs.RANK_F == 16 == math.ceil(Fraction(5000) * Fraction(1, 320))


def test_summary_tree_mean_and_ddof1():
    s = hs.summary(np.array([1.0, 2.0, 3.0, 4.0]))
    assert s["n"] == 4 and s["mean"] == 2.5
    assert s["sd"] == pytest.approx(math.sqrt(5.0 / 3.0), rel=1e-15)
    assert s["se"] == pytest.approx(math.sqrt(5.0 / 3.0) / 2.0, rel=1e-15)
    x = np.random.default_rng(119101).normal(0.03, 0.07, size=1001)
    s = hs.summary(x)
    assert s["mean"] == _tree_mean(x)
    assert abs(s["mean"] - math.fsum(x) / x.size) <= 1e-15
    assert s["sd"] == pytest.approx(float(np.std(x, ddof=1)), rel=1e-14)
    assert s["se"] == pytest.approx(s["sd"] / math.sqrt(x.size), rel=1e-14)


def test_screen_bounds_formulas():
    x = np.random.default_rng(119102).normal(0.02, 0.05, size=4096)
    b = hs.screen_bounds(x)
    m, se = b["mean"], b["se"]
    assert m == _tree_mean(x)
    for key, val in (("L1", m - _z(Fraction(1, 100)) * se), ("U1", m + _z(Fraction(1, 100)) * se),
                     ("Lw", m - _z(Fraction(1, 24640)) * se),
                     ("Uw", m + _z(Fraction(1, 24640)) * se)):
        assert b[key] == pytest.approx(val, rel=1e-14, abs=1e-17), key
    assert b["Lw"] < b["L1"] < m < b["U1"] < b["Uw"]


@pytest.mark.parametrize("winner", ["bootstrap", "normal"])
def test_s3_bounds_l3_is_the_smaller_side(winner):
    rng = np.random.default_rng(119103)
    x = rng.normal(0.05, 0.07, size=4096)
    mean = _tree_mean(x)
    if winner == "bootstrap":
        boot = rng.permutation(np.linspace(-1.0, 1.0, 5000))
    else:
        boot = rng.permutation(mean + 1.0 + np.linspace(0.0, 1e-3, 5000))
    b = hs.s3_bounds(x, boot)
    srt = np.sort(boot)
    l3n = mean - _z(Fraction(1, 320)) * b["se"]
    assert b["L3_normal"] == pytest.approx(l3n, rel=1e-14, abs=1e-17)
    assert b["L3_boot"] == srt[15]  # rank 16 of 5,000 (one-based)
    expect = srt[15] if winner == "bootstrap" else b["L3_normal"]
    assert b["L3"] == expect == min(b["L3_normal"], b["L3_boot"])
    # API-AMBIGUITY: central95_boot read as a 2-sequence (rank 125, rank 4,875)
    lo, hi = b["central95_boot"]
    assert (lo, hi) == (srt[124], srt[4874])
    for key in ("L1", "U1", "Lw", "Uw"):
        assert key in b


def test_normal95_and_bootstrap_kernel():
    x = np.random.default_rng(119104).normal(size=200)
    s = hs.summary(x)
    lo, hi = hs.normal95(s)
    z = _z(Fraction(1, 40))
    assert lo == pytest.approx(s["mean"] - z * s["se"], rel=1e-14, abs=1e-17)
    assert hi == pytest.approx(s["mean"] + z * s["se"], rel=1e-14, abs=1e-17)
    arrays = {"a": x[:50].copy(), "b": x[50:100].copy()}
    got = hs.bootstrap(arrays, 620103)
    ref = c1_means.bootstrap_means(arrays, 620103, 5000)
    assert set(got) == {"a", "b"}
    for k in arrays:
        assert np.asarray(got[k]).shape == (5000,)
        assert np.array_equal(np.asarray(got[k]), ref[k])


def test_null_z_se_zero_cases():
    z0 = hs.null_z(np.zeros(10))
    assert z0["se"] == 0.0 and z0["z"] == 0.0 and not z0["exceeds"]
    zinf = hs.null_z(np.full(10, 0.5))
    assert zinf["se"] == 0.0 and zinf["z"] == math.inf and zinf["exceeds"]


def test_null_z_threshold_is_strict():
    # x = (m + 1, m - 1): mean m exactly, sd = sqrt(2), se = sqrt(2)/sqrt(2) = 1.0 (API §2:
    # se = sd/sqrt(n)), so z = m exactly.
    m = hs.ZNULL
    at = hs.null_z(np.array([m + 1.0, m - 1.0]))
    assert at["mean"] == m and at["se"] == 1.0 and at["z"] == m
    assert not at["exceeds"]  # exactly at ZNULL is not an exceedance
    m2 = float(np.nextafter(hs.ZNULL, np.inf))
    above = hs.null_z(np.array([m2 + 1.0, m2 - 1.0]))
    assert above["z"] > hs.ZNULL and above["exceeds"]
    neg = hs.null_z(np.array([-m2 - 1.0, -m2 + 1.0]))  # two-sided: |mean| / se
    assert neg["exceeds"]


def test_e5_norm_fraction_boundary():
    phases = np.tile(CENTRES, 10)  # 120 rows, 10 per bin
    norms = np.ones(120)
    norms[:6] = 0.1  # 114 of 120 = 95 % have norm >= 0.2
    r = hs.e5(_m32(phases, norms))
    assert r["frac_norm_ge_0.2"] == pytest.approx(0.95, abs=1e-15)
    assert list(r["bin_counts"]) == [10] * 12 and r["min_bin"] == 10
    assert r["resultant"] < 1e-12
    assert r["pass"]
    norms[6] = 0.1  # one row fewer
    assert not hs.e5(_m32(phases, norms))["pass"]


def _bins(counts):
    return np.concatenate([np.full(c, CENTRES[k]) for k, c in enumerate(counts)])


def test_e5_bin_count_boundary():
    counts = [12] + [64] * 5 + [116] + [64] * 5  # n = 768, 64 * 12 = 768 = n
    r = hs.e5(_m32(_bins(counts)))
    assert sum(counts) == 768 and list(r["bin_counts"]) == counts and r["min_bin"] == 12
    assert r["resultant"] == pytest.approx(104 / 768, abs=1e-12)
    assert r["pass"]
    more = list(counts)
    more[6] += 1  # n = 769 > 64 * 12
    assert not hs.e5(_m32(_bins(more)))["pass"]
    moved = list(counts)
    moved[0], moved[6] = 11, 117  # n = 768, 64 * 11 < n
    assert not hs.e5(_m32(_bins(moved)))["pass"]


def _patch_unit_vectors(monkeypatch, planted):
    def fake(phi):
        assert len(phi) == planted.shape[0]
        return planted.copy()

    monkeypatch.setattr(sys.modules["scores"], "unit_vectors", fake)
    if hasattr(hs, "unit_vectors"):
        monkeypatch.setattr(hs, "unit_vectors", fake)


@pytest.mark.parametrize("plus, minus, ok", [(33, 15, True), (34, 14, False)])
def test_e5_resultant_boundary(monkeypatch, plus, minus, ok):
    # API §2: u = scores.unit_vectors(phase). Planted exact unit vectors give a mean of
    # ((plus - minus)/60, 0): exactly 0.30 (passes, equality) or 1/3 (fails).
    u = np.array([(1.0, 0.0)] * plus + [(-1.0, 0.0)] * minus + [(0.0, 1.0)] * 6
                 + [(0.0, -1.0)] * 6)
    _patch_unit_vectors(monkeypatch, u)
    r = hs.e5(_m32(np.tile(CENTRES, 5)))  # 60 rows, 5 per bin, norms 1
    assert r["resultant"] == (plus - minus) / 60
    assert bool(r["pass"]) == ok


def test_e5_phase_conventions():
    rows = np.vstack((_m32(CENTRES[:11]), [[1.0, -1e-9], [1.0, -1e-9]]))
    r = hs.e5(rows)  # phase 2*pi - 1e-9 lands in bin 11
    assert list(r["bin_counts"]) == [1] * 11 + [2]
    z = hs.e5(np.zeros((5, 2)))  # an exact zero has phase 0: bin 0, unit vector (1, 0)
    assert list(z["bin_counts"]) == [5] + [0] * 11
    assert z["resultant"] == 1.0 and z["frac_norm_ge_0.2"] == 0.0 and not z["pass"]


def test_pinsker_violations_counts_only_below_minus_tol():
    slack = np.array([0.0, -1e-12, -1.0000001e-12, -1.0, 5.0, -0.5e-12])
    assert hs.pinsker_violations(slack) == 2
    assert hs.pinsker_violations(slack, tol=0.6e-12) == 3
    assert hs.pinsker_violations(np.abs(slack)) == 0
