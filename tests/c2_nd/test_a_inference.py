"""Author A (job 0121): T-RULES-ND, T-BOOT-ND and T-LADDER-ND.

Protocol C2ND-DESIGN-v1 §4.1, §4.3, §4.5, §7, §8.2-§8.3; names from API.md §2, §8, §10 (P1),
§12.2. Written from the protocol copy, API.md, CONTRACT.json, TEST_PLAN.md and the job 0116
review only. Synthetic inputs; bound dicts built directly where a rule is tested.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_nd") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first: API.md §1 test imports)

# isort: split
import c2_attrib as ca  # noqa: E402
import c2_stats as cs  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_stage_val as nsv  # noqa: E402

MODELS = (1729, 2718, 3141)
PAT = {"+": (0.5, 1.0), "-": (-1.0, -0.5), "s": (-0.5, 0.5)}


def _bd(**cfg):
    return {s: {"mean": sum(PAT[p]) / 2, "L": PAT[p][0], "U": PAT[p][1], "rank_L": 67,
                "rank_U": 19934, "g": 1e-9} for s, p in cfg.items()}


NR = dict(V3x="+", Y1="-", Zc010="+", Zc050="-", Wc="+", Vc="+", NEGc="+", Zc090="-",
          Zc100="-", Z090="s")
DD = dict(V3x="+", Y1="-", Z010="-", Z050="-", Vabs="-", Vrand="-", NEG="+")
NM = dict(V3x="+", Ztau="+", ZMc010="+", ZMc050="-", WMc="+", VMc="+", NEGMc="+")


def _o(family, a, b, c, cnhs=(), kc=False):
    return ndc.overall(family, dict(zip(MODELS, (a, b, c))), list(cnhs), kc_contradicted=kc)


# ---- T-RULES-ND: 2 of 3 (§4.3; C2 §6.5) ----------------------------------------------------
def test_rules_nr_overall():
    N, C, D, X = "NECESSARY", "COMPLEMENT_LOW_ALIGNED", "CODE_DOMINANT", "NOT_NECESSARY"
    assert _o("N-R", N, N, N) == N and _o("N-R", N, N, D) == N
    assert _o("N-R", N, N, "EXCLUDED/LINK") == N
    assert _o("N-R", N, C, D) == C and _o("N-R", C, C, X) == C  # >= 2 in {N, C}
    assert _o("N-R", D, D, X) == D and _o("N-R", X, X, "INC") == X
    assert _o("N-R", D, X, C) == "MIXED" and _o("N-R", D, X, "INC") == "MIXED"
    assert _o("N-R", D, "INC", "INC/NUMERICAL") == "INCONCLUSIVE/PRECISION"
    ex = _o("N-R", D, "EXCLUDED/LINK", "EXCLUDED/MODEL_HEADROOM")
    assert ex == "INCONCLUSIVE/MODEL_HEADROOM"  # the exclusion that left fewer than 2
    assert _o("N-R", "CNHS", "CNHS", D) == "CIRCLE_NOT_HISTORY_SENSITIVE"
    assert _o("N-R", "CNHS", D, D, cnhs=[2718]) == "CIRCLE_NOT_HISTORY_SENSITIVE"
    assert _o("N-R", "FAIL_TECHNICAL/X1", D, D) == "FAIL_TECHNICAL/X1"


def test_rules_d_overall():
    NU, LA, PA, US = "DECOY_NOT_USED", "DECOY_LOW_ALIGNED", "DECOY_PARTIAL", "DECOY_USED"
    assert _o("D", NU, NU, US) == NU and _o("D", NU, LA, US) == LA and _o("D", LA, LA, NU) == LA
    assert _o("D", US, US, PA) == US and _o("D", PA, PA, NU) == PA
    assert _o("D", NU, PA, US) == "MIXED"
    assert _o("D", NU, NU, NU, kc=True) == "KNOWN_CASE_CONTRADICTED"
    assert _o("D", "KNOWN_CASE_CONTRADICTED", NU, NU, kc=True) == "KNOWN_CASE_CONTRADICTED"
    assert _o("D", "FAIL_TECHNICAL/DECOY", NU, NU, kc=True) == "FAIL_TECHNICAL/DECOY"
    assert _o("D", "CNHS", "CNHS", NU) == "CIRCLE_NOT_HISTORY_SENSITIVE"
    ex = _o("D", "EXCLUDED/KNOWN_CASE_UNRESOLVED", "EXCLUDED/MODEL_HEADROOM", NU)
    assert ex == "INCONCLUSIVE/KNOWN_CASE_UNRESOLVED"  # appended to the C2 reason order
    assert _o("D", NU, "INC", "INC") == "INCONCLUSIVE/PRECISION"


def test_rules_nm_overall():
    R, CD, NN = "ROUTED", "CODE_DOMINANT_M", "NOT_NECESSARY_M"
    assert _o("N-M", R, R, CD) == "ROUTED_AROUND"
    assert _o("N-M", CD, CD, R) == CD and _o("N-M", NN, NN, CD) == NN
    assert _o("N-M", "NECESSARY_M", "NECESSARY_M", "INC") == "NECESSARY_M"
    assert _o("N-M", "NECESSARY_M", "COMPLEMENT_LOW_ALIGNED_M", NN) == "COMPLEMENT_LOW_ALIGNED_M"
    assert _o("N-M", CD, NN, "INC") == "MIXED" and _o("N-M", R, CD, "INC") == "MIXED"
    assert _o("N-M", R, "INC", "INC") == "INCONCLUSIVE/PRECISION"
    assert _o("N-M", "CNHS", "CNHS", R) == "CNHS-2"


def _rec(gate, full, model=None, family=None, problem=None, decoy=None, values=None):
    return {"gate": gate, "status": full, "full_status": full, "model": model, "family": family,
            "problem": problem, "decoy": decoy, "scope": "model", "values": values or {}}


def test_rules_endpoint_status():
    h = [_rec("G0", "PASS"), _rec("L1", "EXCLUDED/LINK", 1729, "N-R"),
         _rec("M0-D", "EXCLUDED/CONSTRUCTION", 1729, "D", "RT", "DNULLR"),  # report-only
         _rec("F1", "EXCLUDED/PATCH_MODEL_DEGENERATE", 2718, "N-R", "R_E"),  # a variant
         _rec("T-PRE-MODEL", "EXCLUDED/TEST_GATE", 3141)]
    assert ndc.endpoint_status(1729, "N-R", h) == "NOT_RUN/L1"
    assert ndc.endpoint_status(1729, "D", h) == "SCORED"
    assert ndc.endpoint_status(2718, "N-R", h) == "SCORED"
    assert ndc.endpoint_status(3141, "N-M", h) == "NOT_RUN/T-PRE"
    formed = [_rec("ENDPOINT", "CODE_DOMINANT", None, "N-R", values={"formed": True}),
              _rec("T-PRE-MODEL", "EXCLUDED/TEST_GATE", 3141)]
    assert ndc.endpoint_status(3141, "N-R", formed) == "SEALED_UNSCORED/T-PRE"


def test_rules_qualifier_order():
    nr = {1729: ndc.nr_model(_bd(**dict(NR, NEGc="-")), True), 2718: ndc.nr_model(_bd(**NR), True),
          3141: ndc.nr_model(_bd(**dict(NR, Zc050="+")), True)}
    assert [nr[j]["status"] for j in MODELS] == ["CODE_DOMINANT"] * 2 + ["NOT_NECESSARY"]
    extra = {"variants": {1729: {"R_E": "COMPLEMENT_LOW_ALIGNED", "R_K1": "COMPLEMENT_LOW_ALIGNED",
                                 "R_K2": "CODE_DOMINANT"}}, "dnullr": {}, "kcr": {}, "kc_test": {}}
    assert ndc.qualifiers("N-R", nr, extra, False, {"precision_limited": [3141]}) == [
        "SPECIFICITY_NOT_ESTABLISHED", "NEGATIVE_COMPLEMENT(1729)", "PROJECTOR_DEPENDENT_NR(1729)",
        "HARMONIC_DEPENDENT_NR(1729, 1)", "PRECISION_LIMITED(3141)", "DISSENT(3141: NOT_NECESSARY)"]
    d = {1729: ndc.d_model(_bd(**dict(DD, NEG="-")), True), 2718: ndc.d_model(_bd(**DD), True),
         3141: ndc.d_model(_bd(**dict(DD, Vabs="+")), True)}
    assert [d[j]["status"] for j in MODELS] == ["DECOY_NOT_USED"] * 2 + ["DECOY_LOW_ALIGNED"]
    extra = {"variants": {}, "dnullr": {1729: "DECOY_LOW_ALIGNED", 2718: "NOT_COMPUTED",
                                        3141: "DECOY_LOW_ALIGNED"},
             "kcr": {2718: ["DNULLR"]}, "kc_test": {1729: ["DDOSE"]}}
    assert ndc.qualifiers("D", d, extra, False, {"precision_limited": []}) == [
        "SPECIFICITY_NOT_ESTABLISHED", "NEGATIVE_ALIGNED_CONTRIBUTION(1729)",
        "DECOY_LOCATION_DEPENDENT(1729)", "MOVE_CASE_CONTRADICTED(2718, DNULLR)",
        "KC_TEST_DISAGREES(1729, DDOSE)", "DISSENT(3141: DECOY_LOW_ALIGNED)"]
    nm = {1729: ndc.nm_model(_bd(**NM)), 2718: ndc.nm_model(_bd(**NM)),
          3141: ndc.nm_model(_bd(**dict(NM, Ztau="-")))}
    empty = {"variants": {}, "dnullr": {}, "kcr": {}, "kc_test": {}}
    assert ndc.qualifiers("N-M", nm, empty, False, {"precision_limited": [2718]}) == [
        "PRECISION_LIMITED(2718)", "DISSENT(3141: ROUTED)"]  # no specificity qualifier (ND-C29)


# ---- licences, package statement, caveat, unions (§7, §8.3) ------------------------------
QN = ("These outcomes concern the frozen, nuisance-excluding linear code defined by this fit "
      "and projector.")
QN2 = ("At the linear readout the complement share equals one minus the code share by an exact "
       "identity; it is not an independent measurement.")
KM3 = ("The layer-2 complement includes LayerNorm-scale effects: changing the non-code "
       "coordinates rescales the code inside block 3 and at the final LayerNorm, so a code that "
       "is the only input the readout reads need not be shown necessary here.")
QD1 = ("These outcomes concern constructed decoys of the three models in which the readout of "
       "the registered code is removed or rescaled by an exact head edit, while the code stays "
       "in the activations.")
QD3 = ("The decoy's remaining readout can still depend on the upstream code through the "
       "LayerNorm scale; this is outside the registered interchange.")
DISCLOSE = ("The decoy's remaining readout is amplified by a gain of 6, fixed in advance, and the "
            "readout of the code is removed by an exact edit of the output head.")


def test_licences_carry_the_sentences_and_qcode():
    nr = {"NECESSARY": "sufficient and necessary for this readout response in this sense",
          "COMPLEMENT_LOW_ALIGNED": "This is not a necessity result.",
          "CODE_DOMINANT": "the registered code is the main carrier of this readout response, "
                           "not the only one",
          "NOT_NECESSARY": "the complement alone carries more than half"}
    for outcome, frag in nr.items():
        lic = ndc.licence("N-R", outcome, {})
        assert frag in lic and QN in lic and QN2 in lic and lic.index(frag) < lic.index(QN)
    for outcome in ("COMPLEMENT_LOW_ALIGNED", "CODE_DOMINANT", "NOT_NECESSARY", "MIXED",
                    "INCONCLUSIVE/PRECISION"):
        assert "sufficient and necessary" not in ndc.licence("N-R", outcome, {})
    for outcome in ("CODE_DOMINANT_M", "ROUTED_AROUND", "NECESSARY_M"):
        lic = ndc.licence("N-M", outcome, {})
        for frag in ("residual skip", "radial support screen", "only position 32 is tested",
                     "self-repair can lower τ_M", KM3):
            assert frag in lic, (outcome, frag)
    assert "carries between 10% and 50% of the signed aligned effect of the full layer-2" in (
        ndc.licence("N-M", "CODE_DOMINANT_M", {}))
    d = {"DECOY_NOT_USED": "the registered method, re-estimating the code on fresh data, "
                           "returned NOT_USED",
         "DECOY_USED": "the method called an unread code used",
         "DECOY_PARTIAL": "to a code that the decoy provably does not read",
         "KNOWN_CASE_CONTRADICTED": "whose constructed answer is"}
    for outcome, frag in d.items():
        lic = ndc.licence("D", outcome, {})
        assert frag in lic and QD1 in lic and QD3 in lic and DISCLOSE in lic, outcome
        assert lic.index(frag) < lic.index(QD1) < lic.index(DISCLOSE)


def test_statement_licences():
    # API-AMBIGUITY: API.md §8.4 statement_licence(kind, values) does not name the kinds; the
    # statement flag names "rule6a", "rule6b", "rule6c", "nested" (API.md §2, §14.2) are used.
    frags = {"rule6a": "a positive but below-margin contribution of everything except the code",
             "rule6b": "to a code the decoy does not read",
             "rule6c": "the layer-2 complement interchange carries a certified positive share "
                       "below the 10% margin",
             "nested": "the registered code's own share is certified positive but below 10%"}
    for kind, frag in frags.items():
        assert frag in ndc.statement_licence(kind, {}), kind


def test_package_statement_caveat_and_unions():
    ok = ndc.package_statement("USED", "CODE_DOMINANT", "DECOY_NOT_USED")
    assert ok is not None and "the same method returns not used (C2ND)" in ok
    assert "carries more than half of the model's signed aligned response (C2)" in ok
    assert QN in ok and QD1 in ok
    assert ndc.package_statement("USED", "NECESSARY", "DECOY_NOT_USED") is not None
    for args in (("PARTIAL", "CODE_DOMINANT", "DECOY_NOT_USED"),
                 ("USED", "COMPLEMENT_LOW_ALIGNED", "DECOY_NOT_USED"),
                 ("USED", "NOT_NECESSARY", "DECOY_NOT_USED"),
                 ("USED", "CODE_DOMINANT", "DECOY_LOW_ALIGNED"),
                 ("USED", "CODE_DOMINANT", "KNOWN_CASE_CONTRADICTED")):
        assert ndc.package_statement(*args) is None, args
    for outcome in ("DECOY_PARTIAL", "DECOY_USED"):
        assert ndc.c2_caveat(outcome) == "specificity not established on the decoy"
    for outcome in ("DECOY_NOT_USED", "DECOY_LOW_ALIGNED", "KNOWN_CASE_CONTRADICTED", "MIXED",
                    "INCONCLUSIVE/PRECISION"):
        assert ndc.c2_caveat(outcome) is None
    assert ndc.UNION_DISPLAY == {"package": "0.15", "c2nd": "0.1417", "c2r_plus_c2nd": "0.1917",
                                 "all_six": "0.2917 (<= 0.30)"}
    a_nr, a_d, a_nm = (15 * nc.ALPHA[f] for f in ("N-R", "D", "N-M"))  # 5 events x 3 models
    assert (a_nr, a_d, a_nm) == (F(1, 20), F(1, 20), F(1, 24))
    assert 12 * nc.ALPHA["N-R"] == F(1, 25)  # Y1 inactive: 4 events per model
    assert a_nr + a_d + F(1, 20) == F(3, 20)
    assert f"{float(a_nr + a_d + a_nm):.4f}" == "0.1417"
    assert f"{float(F(1, 20) + a_nr + a_d + a_nm):.4f}" == "0.1917"
    six = 3 * F(1, 20) + a_nr + a_d + a_nm
    assert f"{float(six):.4f}" == "0.2917" and six <= F(3, 10)


# ---- T-BOOT-ND (§4.1) ------------------------------------------------------------------------
def test_boot_shared_index_streams():
    rng = np.random.default_rng(1201)
    probe, other = rng.normal(size=128) + 0.3, rng.normal(size=128)
    seed, alpha, draws = nc.seed("test_NR"), nc.ALPHA["N-R"], nc.TEST_DRAWS
    assert seed == 630503 and draws == 20000
    first = ndc.stream_bounds({"V3x|1729": probe, "Y1|1729": other}, seed, alpha, draws)
    second = ndc.stream_bounds({"V3x|1729": probe, "Zc010|1729": 2 * other,
                                "Zc050|1729": other - 1.0, "Wc|1729": other + 1.0}, seed, alpha,
                               draws)
    for k in ("mean", "L", "U", "rank_L", "rank_U"):
        assert first["V3x|1729"][k] == second["V3x|1729"][k], k
    assert nc.seed("val_KC") == 630506 and nc.VAL_DRAWS == 5000 and nc.VAL_ALPHA == F(1, 60)
    kc = ndc.stream_bounds({"D0:V3x|1729": probe, "D0:Z010|1729": other}, 630506,
                           nc.VAL_ALPHA, nc.VAL_DRAWS)
    kcr = ndc.stream_bounds({"DNULLR:V3x|1729": probe, "DID:Z010|1729": -other}, 630506,
                            nc.VAL_ALPHA, nc.VAL_DRAWS)
    a, b = kc["D0:V3x|1729"], kcr["DNULLR:V3x|1729"]
    assert (a["L"], a["U"], a["mean"]) == (b["L"], b["U"], b["mean"])
    assert (a["rank_L"], a["rank_U"]) == (84, 4917)


def test_boot_fraction_ranks_and_contract():
    for draws, p, lo, hi in ((20000, F(1, 300), 67, 19934), (20000, F(1, 360), 56, 19945),
                             (5000, F(1, 60), 84, 4917), (5000, F(1, 40), 125, 4875)):
        assert nc.rank(draws, p) == lo == math.ceil(F(draws) * p)
        assert nc.rank(draws, 1 - p) == hi == math.ceil(F(draws) * (1 - p))
    assert nc.rank(5000, F(1, 20)) == 250 == math.ceil(F(5000) * F(1, 20))
    R = nc.CONTRACT["bootstrap"]["ranks"]
    assert R["test_NR_D"] == {"L": 67, "U": 19934} and R["test_NM"] == {"L": 56, "U": 19945}
    assert R["val"] == {"L": 84, "U": 4917} and R["h5"] == 250
    assert R["desc_and_kc_test"] == {"L": 125, "U": 4875}
    assert nc.ALPHA == {"N-R": F(1, 300), "D": F(1, 300), "N-M": F(1, 360)}
    assert (nc.H5_ALPHA, nc.DESC_ALPHA, nc.DESC_DRAWS) == (F(1, 20), F(1, 40), 5000)


def test_boot_indicator_form_sign():
    rng = np.random.default_rng(1202)
    s, E = rng.normal(size=400), rng.random(400) < 0.6
    for shift in (-0.5, -0.1, 0.1, 0.5):
        x = s + shift
        ind = np.asarray(ca.ind(x, E))
        assert np.all(ind[~E] == 0.0) and np.array_equal(ind[E], x[E])
        assert np.sign(np.mean(ind)) == np.sign(np.mean(x[E]))  # sign E[s 1_E] = sign E[s | E]
        assert abs(np.mean(ind) - np.mean(E) * np.mean(x[E])) <= 1e-12


def test_boot_ratio_intervals_undefined_and_no_draw_discarded():
    rng = np.random.default_rng(1203)
    n = 64
    num, den = rng.normal(size=n) + 1.0, 0.1 * rng.normal(size=n) + 2.0
    one = np.zeros(n)
    one[0] = 1.0  # some resample omits row 0: a zero resampled denominator
    bad = num.copy()
    bad[3] = np.nan
    seed = nc.seed("desc")
    assert seed == 630508
    pairs = [("a", "d"), ("a", "z"), ("a", "h"), ("bad", "d")]
    out = ca.ratio_intervals({"a": num, "bad": bad}, {"d": den, "z": np.zeros(n), "h": one},
                             pairs, seed, nc.DESC_DRAWS)
    assert out["a/z"] == "UNDEFINED" and out["a/h"] == "UNDEFINED" and out["bad/d"] == "UNDEFINED"
    gen = np.random.Generator(np.random.PCG64(seed))  # the shared stream, every draw kept
    ratios = []
    for _ in range(nc.DESC_DRAWS):
        idx = gen.integers(0, n, size=n)
        ratios.append(np.mean(num[idx]) / np.mean(den[idx]))
    srt = np.sort(ratios)
    assert abs(out["a/d"]["L"] - srt[124]) <= 1e-12 and abs(out["a/d"]["U"] - srt[4874]) <= 1e-12


# ---- T-LADDER-ND (§4.5; API.md §10 P1, ND-C20, ND-C21) ------------------------------------
class _FakePrecision:
    """Records the kernel calls; precision_summary passes model j at N iff (name, N, j) in ok."""

    def __init__(self, arrays, ok):
        self.arrays, self.ok, self.sd, self.c, self.cfg = arrays, ok, [], [], []

    def _name(self, X):
        j = next(iter(X))
        return next(k for k, v in self.arrays.items() if np.array_equal(v[j], X[j]))

    def sd_b4_draws(self, X, r4n, models, seed, draws, size):
        self.sd.append(dict(name=self._name(X), r4n=r4n, seed=seed, draws=draws, size=size))
        shape = (draws, len(models))
        return np.full(shape, float(len(self.sd) - 1)), np.zeros(shape)  # sd encodes the call

    def centered_draws(self, X, models, seed, draws, size):
        self.c.append(dict(name=self._name(X), seed=seed, draws=draws, size=size))
        return np.zeros((draws, len(models)))

    def precision_summary(self, sd, e, models, cfg):
        name, N = self.sd[int(np.asarray(sd)[0, 0])]["name"], int(cfg["projected_N"])
        self.cfg.append((name, N, dict(cfg)))
        good = {j for j in models if (name, N, j) in self.ok}
        per = {j: {"sd_lower": 0.1, "sd_upper": 0.2, "mde_lower": 0.0 if j in good else 9.0,
                   "mde_upper": 0.0 if j in good else 9.0, "q_alpha": 0.0,
                   "power": 1.0 if j in good else 0.0} for j in models}
        met = len(good) == len(models)
        return {"models": per, "status": "PASS" if met else "INCONCLUSIVE", "criterion_met": met}


def _ladder(monkeypatch, family, names, ok_fn):
    rng = np.random.default_rng(1301)
    arrays = {k: {j: rng.normal(size=4096) for j in MODELS} for k in names}
    base = {j: np.abs(rng.normal(size=4096)) + 0.1 * (i + 1) for i, j in enumerate(MODELS)}
    gated = nc.CONTRACT["thresholds"]["p1_gated"][family]
    ok = {(k, N, j) for k in gated for N in nc.N_LADDER for j in MODELS if ok_fn(N, j)}
    fake = _FakePrecision(arrays, ok)
    monkeypatch.setattr(nsv, "precision", fake)
    res = nsv.p1_nd(family, arrays, base, MODELS, nc.ALPHA[family])
    coef = F(3, 100) if family == "D" else F(1, 10)
    alt = float(coef) * min(float(np.mean(base[j])) for j in MODELS)
    assert sorted(c["name"] for c in fake.sd) == sorted(gated) == sorted(set(names) & set(gated))
    for c in fake.sd:  # one SD call per gated array, seed 630516, 5,000 draws, size 4,096
        assert (c["seed"], c["draws"], c["size"]) == (630516, 5000, 4096)
        assert all(np.array_equal(c["r4n"][j], base[j]) for j in MODELS)  # D: G_x 1_Ex (ND-C21)
    assert sorted((c["name"], c["size"]) for c in fake.c) == sorted(
        (k, N) for k in gated for N in nc.N_LADDER)
    assert all((c["seed"], c["draws"]) == (630517, 5000) for c in fake.c)
    for name, N, cfg in fake.cfg:
        want = cs._cfg(nc.ALPHA[family], alt, N)
        assert abs(cfg.pop("alternative") - want.pop("alternative")) <= 1e-12 * alt
        assert cfg == want, (name, N)
    return res


def test_ladder_nr_all_pass_at_first_rung(monkeypatch):
    names = ("Zc010", "Zc050", "Wc", "NEGc")  # only Zc010 and Zc050 are gated
    res = _ladder(monkeypatch, "N-R", names, lambda N, j: True)
    assert res["N_F"] == 4096 and res["status"] == "PASS" and list(res["precision_limited"]) == []


def test_ladder_two_of_three_and_underpowered(monkeypatch):
    res = _ladder(monkeypatch, "D", ("Z010", "Z050", "Vabs", "NEG"),
                  lambda N, j: N >= 8192 and j != 3141)
    assert res["N_F"] == 8192 and res["status"] == "PASS"
    assert list(res["precision_limited"]) == [3141]
    res = _ladder(monkeypatch, "N-M", ("Ztau", "ZMc010", "WMc"), lambda N, j: j == 1729)
    assert res["N_F"] is None and res["status"] == "INCONCLUSIVE/UNDERPOWERED"
    assert cs.n_test({"N-R": 8192, "D": 4096, "N-M": 4096}) == (8192, 2)
