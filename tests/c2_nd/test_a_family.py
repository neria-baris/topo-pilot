"""Author A (job 0121): T-FAMILY-ND (the exhaustive grid of §8.4) and T-EDGE (MD-9).

Protocol C2ND-DESIGN-v1 §2.3, §2.4, §4.3, §8.1 (Lemma FW-ND tables), §8.4, §3 rows 24-25;
names from API.md §8.2-§8.4. Bound dicts are built directly (TEST_PLAN §1). The expected
statuses and statements below are re-derived from the protocol tables, never from the code.
Coverage: a declared statement that is false in a truth state must force a coverage-failure
event F^L_s = {L(s) > mu_s} or F^U_s = {U(s) < mu_s} listed by §8.1 for that state.
"""

from __future__ import annotations

import functools
import itertools
import sys
from fractions import Fraction as F
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "c2_nd") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402,F401  (first: API.md §1 test imports)

# isort: split
import c2_decide as cdc  # noqa: E402
import nd_decide as ndc  # noqa: E402

G = 0.5  # the guard g of every bound in these dicts
PATS = {"--": (-2.0, -1.0), "-+": (-1.0, 1.0), "++": (1.0, 2.0), "00": (-0.25, 0.25)}
KAPPAS = [F(-1, 2), F(-1, 10), F(-1, 20), F(0), F(1, 20), F(1, 10), F(3, 10), F(1, 2),
          F(7, 10), F(9, 10), F(19, 20), F(1), F(6, 5)]
T10, T50, T90 = F(1, 10), F(1, 2), F(9, 10)
NR_CATS = ("NECESSARY", "COMPLEMENT_LOW_ALIGNED", "CODE_DOMINANT", "NOT_NECESSARY")


def _b(cfg):
    out = {}
    for s, p in cfg.items():
        L, U = PATS[p] if isinstance(p, str) else p
        out[s] = {"mean": (L + U) / 2, "L": L, "U": U, "rank_L": 67, "rank_U": 19934, "g": G}
    return out


def _s(v):
    return 1 if v > G else -1 if v < -G else 0


def _fs(x):
    return (x > 0) - (x < 0)


def _signs(b):
    return lambda s, side: _s(b[s][side])


def _cat(sg, z1, z5, w, v, names):
    """§2.3 table (N-R, N-M): returns the one declared category, else INC(/NUMERICAL)."""
    l1, u1, l5, u5 = sg(z1, "L"), sg(z1, "U"), sg(z5, "L"), sg(z5, "U")
    nec = u1 == -1 and u5 == -1 and sg(w, "L") == 1 and sg(v, "U") == -1
    conds = (nec, u1 == -1 and u5 == -1 and not nec, l1 == 1 and u5 == -1, l5 == 1 and l1 == 1)
    hits = [c for c, on in zip(names, conds) if on]
    assert len(hits) <= 1  # the four categories are mutually exclusive
    return hits[0] if hits else ("INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC")


def _prereq(b, y_active, flags):
    """RESP (L(V3x) > g) and SPEC (U(Y1) < -g when Y1 is active) come first (§4.3)."""
    resp = _s(b["V3x"]["L"]) == 1
    spec = bool(y_active) and _s(b["Y1"]["U"]) == -1
    out = dict(resp=resp, spec=spec, formed=resp and (spec or not y_active))
    if not out["formed"]:
        st = "EXCLUDED/MODEL_HEADROOM" if not resp else "EXCLUDED/NUISANCE_IN_S"
        out.update(dict.fromkeys(flags, False), status=st)
    return out


def nr_expect(b, y_active):
    sg = _signs(b)
    out = _prereq(b, y_active, ("gt010", "lt050", "rule6a", "nested", "negative"))
    if not out["formed"]:
        return out
    st = _cat(sg, "Zc010", "Zc050", "Wc", "Vc", NR_CATS)
    u1, u5 = sg("Zc010", "U"), sg("Zc050", "U")
    return dict(out, status=st, gt010=sg("Zc010", "L") == 1, lt050=u5 == -1,
                rule6a=sg("NEGc", "L") == 1 and u1 == -1 and u5 == -1,
                nested=st == "NOT_NECESSARY" and sg("Zc090", "L") == 1 and sg("Zc100", "U") == -1,
                negative=sg("NEGc", "U") == -1)


def _got(r, flags):
    out = dict(status=str(r["status"]), resp=bool(r["resp"]), spec=bool(r["spec"]),
               formed=bool(r["endpoint_formed"]), gt010=bool(r["coarse"]["gt010"]),
               lt050=bool(r["coarse"]["lt050"]))
    return dict(out, **{k: bool(r[k]) for k in flags})


nr_got = functools.partial(_got, flags=("rule6a", "nested", "negative"))
d_got = functools.partial(_got, flags=("rule6b", "negative"))


def d_expect(b, y_active):
    sg = _signs(b)
    out = _prereq(b, y_active, ("gt010", "lt050", "rule6b", "negative"))
    if not out["formed"]:
        return out
    l1, u1, l5, u5 = sg("Z010", "L"), sg("Z010", "U"), sg("Z050", "L"), sg("Z050", "U")
    if l5 == 1 and l1 == 1:
        st = "DECOY_USED"
    elif l1 == 1 and u5 == -1:
        st = "DECOY_PARTIAL"
    elif u1 == -1 and u5 == -1:
        nu = sg("Vabs", "U") == -1 and sg("Vrand", "U") == -1
        st = "DECOY_NOT_USED" if nu else "DECOY_LOW_ALIGNED"
    else:
        st = "INC/NUMERICAL" if 0 in (l1, u1, l5, u5) else "INC"
    return dict(out, status=st, gt010=l1 == 1, lt050=u5 == -1,
                rule6b=sg("NEG", "L") == 1 and u1 == -1 and u5 == -1,
                negative=sg("NEG", "U") == -1)


NM_CATS = tuple(c + "_M" for c in NR_CATS)


def nm_expect(b):
    sg = _signs(b)
    resp = sg("V3x", "L") == 1
    if not resp:
        return dict(status="EXCLUDED/MODEL_HEADROOM", resp=False, formed=False, rule6c=False)
    lt, ut = sg("Ztau", "L"), sg("Ztau", "U")
    if ut == -1:
        st = "ROUTED"
    elif lt == 1:
        st = _cat(sg, "ZMc010", "ZMc050", "WMc", "VMc", NM_CATS)
    else:
        st = "INC/NUMERICAL" if 0 in (lt, ut) else "INC"
    r6 = lt == 1 and sg("NEGMc", "L") == 1 and sg("ZMc010", "U") == sg("ZMc050", "U") == -1
    return dict(status=st, resp=True, formed=True, rule6c=r6, gt010=lt == 1, routed=ut == -1)


def nm_got(r):
    out = dict(status=str(r["status"]), resp=bool(r["resp"]), formed=bool(r["endpoint_formed"]),
               rule6c=bool(r["rule6c"]))
    if out["resp"]:
        out.update({k: bool(r["transmission"][k]) for k in ("gt010", "routed")})
    return out


# ---- the §8.1 event tables ---------------------------------------------------------------
def nr_events(k, M=""):
    z1, z5, w, v, ng = (f"Z{M}c010", f"Z{M}c050", f"W{M}c", f"V{M}c", f"NEG{M}c")
    if k <= -T10:
        return {("L", w), ("L", z1), ("L", ng)}
    if k <= 0:
        return {("U", v), ("L", z1), ("L", ng)}
    if k < T10:
        return {("U", v), ("L", z1)}
    if k == T10:
        return {("U", z1), ("L", z1)}
    if k < T50:
        return {("U", z1), ("L", z5)}
    if k == T50:
        return {("L", z5), ("U", z5)}
    if M or k <= T90:  # N-M has no nested entry: "the other regions as C2"
        return {("U", z5)} | (set() if M else {("L", "Zc090")})
    return {("U", "Zc050")} | ({("U", "Zc100")} if k >= 1 else set())


def d_events(p, s_false):
    e = {("U", s_false)} if s_false else set()
    if p <= 0:
        return {("L", "Z010"), ("L", "NEG")} | e
    if p < T10:
        return {("L", "Z010")} | e
    if p == T10:
        return {("L", "Z010"), ("U", "Z010")}
    if p < T50:
        return {("L", "Z050"), ("U", "Z010")}
    return {("L", "Z050"), ("U", "Z050")} if p == T50 else {("U", "Z050")}


def nm_events(t, k):
    if t < T10:
        return {("L", "Ztau")}
    if t == T10:
        return {("L", "Ztau"), ("U", "Ztau")}
    return {("U", "Ztau")} | nr_events(k, M="M")


def _forced(signs, mu):
    ev = {("L", s) for s, m in mu.items() if signs[s][0] == 1 and m <= 0}
    return ev | {("U", s) for s, m in mu.items() if signs[s][1] == -1 and m >= 0}


def _cover(cache, truth, mu, listed):
    used = set()
    for signs, decl in cache:
        false = [k for k, on in decl.items() if on and not truth[k]]
        if false:
            hit = _forced(signs, mu) & listed
            assert hit, (false, signs, mu)
            used |= hit
    return used


def _grid(stats, fixed, model, expect, got, cats, flags):
    """Every sign pattern of `stats`: the rule equals the protocol table (so the categories
    are exclusive, nested only inside NOT_NECESSARY); returns (signs, declarations)."""
    cache = []
    for combo in itertools.product(PATS, repeat=len(stats)):
        cfg = dict(fixed, **dict(zip(stats, combo)))
        b = _b(cfg)
        r, e = got(model(b)), expect(b)
        assert r == e, (cfg, r, e)
        signs = {s: (_s(PATS[p][0]), _s(PATS[p][1])) for s, p in zip(stats, combo)}
        decl = {c: r["status"] == c for c in cats}
        cache.append((signs, dict(decl, **{k: r[k] for k in flags})))
    return cache


# ---- T-FAMILY-ND (§8.1, §8.4) ------------------------------------------------------------
def test_family_nr_grid():
    stats = ("Zc010", "Zc050", "Wc", "Vc", "NEGc", "Zc090", "Zc100")
    fixed = {"V3x": "++", "Y1": "--", "Z090": "-+"}  # RESP declared; Y1 inactive
    cache = _grid(stats, fixed, lambda b: ndc.nr_model(b, False), lambda b: nr_expect(b, False),
                  nr_got, NR_CATS, ("gt010", "lt050", "rule6a", "nested"))
    assert all(not d["nested"] or d["NOT_NECESSARY"] for _, d in cache)
    assert all(sum(d[c] for c in NR_CATS) <= 1 for _, d in cache)  # never CLA with NECESSARY
    for k, ev in itertools.product(KAPPAS, (-1, 0, 1)):  # ev: sign of eta_comp - 0.10
        truth = {"NECESSARY": -T10 < k < T10 and ev < 0, "COMPLEMENT_LOW_ALIGNED": k < T10,
                 "CODE_DOMINANT": T10 < k < T50, "NOT_NECESSARY": k > T50, "gt010": k > T10,
                 "lt050": k < T50, "rule6a": 0 < k < T10, "nested": T90 < k < 1}
        mu = {"Zc010": _fs(k - T10), "Zc050": _fs(k - T50), "Wc": _fs(k + T10), "Vc": ev,
              "NEGc": _fs(k), "Zc090": _fs(k - T90), "Zc100": _fs(k - 1)}
        listed = nr_events(k)
        used = _cover(cache, truth, mu, listed)
        assert len(listed) <= 3 and len(used) + 1 <= 4  # + RESP: <= 4 with Y1 inactive


def test_family_d_grid():
    stats = ("Z010", "Z050", "Vabs", "Vrand", "NEG")
    fixed = {"V3x": "++", "Y1": "--"}
    cats = ("DECOY_USED", "DECOY_PARTIAL", "DECOY_LOW_ALIGNED", "DECOY_NOT_USED")
    cache = _grid(stats, fixed, lambda b: ndc.d_model(b, False), lambda b: d_expect(b, False),
                  d_got, cats, ("gt010", "lt050", "rule6b"))
    for p, va, vr in itertools.product(KAPPAS, (-1, 1), (-1, 1)):
        truth = {"DECOY_USED": p > T50, "DECOY_PARTIAL": T10 < p < T50,
                 "DECOY_LOW_ALIGNED": p < T10, "DECOY_NOT_USED": p < T10 and va < 0 and vr < 0,
                 "gt010": p > T10, "lt050": p < T50, "rule6b": 0 < p < T10}
        mu = {"Z010": _fs(p - T10), "Z050": _fs(p - T50), "NEG": _fs(p), "Vabs": va, "Vrand": vr}
        s_false = "Vabs" if va >= 0 else "Vrand" if vr >= 0 else None
        listed = d_events(p, s_false)
        used = _cover(cache, truth, mu, listed)
        assert len(listed) <= 3 and len(used) + 1 <= 4


def test_family_nm_grid():
    stats = ("Ztau", "ZMc010", "ZMc050", "WMc", "VMc", "NEGMc")
    cache = _grid(stats, {"V3x": "++"}, ndc.nm_model, nm_expect, nm_got, NM_CATS + ("ROUTED",),
                  ("gt010", "rule6c"))
    for t, k, ev in itertools.product((F(1, 20), T10, T50), KAPPAS, (-1, 1)):
        on = t > T10
        truth = {"ROUTED": t < T10, "gt010": on, "NECESSARY_M": on and -T10 < k < T10 and ev < 0,
                 "COMPLEMENT_LOW_ALIGNED_M": on and k < T10,
                 "CODE_DOMINANT_M": on and T10 < k < T50, "NOT_NECESSARY_M": on and k > T50,
                 "rule6c": on and 0 < k < T10}
        mu = {"Ztau": _fs(t - T10), "ZMc010": _fs(k - T10), "ZMc050": _fs(k - T50),
              "WMc": _fs(k + T10), "VMc": ev, "NEGMc": _fs(k)}
        listed = nm_events(t, k)
        used = _cover(cache, truth, mu, listed)
        assert len(listed) <= 4 and len(used) + 1 <= 5


def test_family_prerequisites_resp_and_spec():
    cores = [dict(Zc010="--", Zc050="--", Wc="++", Vc="--", NEGc="++"),
             dict(Zc010="++", Zc050="--", Wc="++", Vc="++", NEGc="++"),
             dict(Zc010="++", Zc050="++", Wc="++", Vc="++", NEGc="++")]
    for core, v3, y1, act in itertools.product(cores, PATS, PATS, (False, True)):
        b = _b(dict(core, V3x=v3, Y1=y1, Zc090="++", Zc100="--", Z090="-+"))
        r, e = nr_got(ndc.nr_model(b, act)), nr_expect(b, act)
        assert r == e
        # nothing is declared without RESP (F^L_V3) and, when Y1 is active, SPEC (F^U_Y1)
        assert not r["formed"] or (_s(b["V3x"]["L"]) == 1 and (not act or _s(b["Y1"]["U"]) == -1))
        bd = _b(dict(V3x=v3, Y1=y1, Z010="--", Z050="--", Vabs="--", Vrand="--", NEG="++"))
        assert d_got(ndc.d_model(bd, act)) == d_expect(bd, act)
        bm = _b(dict(V3x=v3, Ztau="++", ZMc010="--", ZMc050="--", WMc="++", VMc="--",
                     NEGMc="++"))
        assert nm_got(ndc.nm_model(bm)) == nm_expect(bm)
    assert nc.CONTRACT["levels"]["events_per_model"] == {"N-R": 5, "D": 5, "N-M": 5}


# ---- KC routing (§3 rows 24-25, §4.3, §8.4) ----------------------------------------------
R_CASE = dict(V3x="++", Y1="--", Z010="++", Z050="++", Vabs="++", Vrand="++", NEG="++",
              V3y="++")
NEC_KEYS = {"DONLY": dict(Zc010="--", Zc050="--", Wc="++", Vc="--", NEGc="++"),
            "DDOSE": dict(Z050="--", Zc010="++", Zc050="++", Wc="++", Vc="++", NEGc="++")}


def _kc(case, y_active=False, **kw):
    # API-AMBIGUITY: kc_case gets the case's own prefixed keys of API.md §7.3 case_arrays;
    # those carry no Zc090/Zc100, so the nested entry (not a listed KC statement) has no input.
    cfg = {**R_CASE, **NEC_KEYS.get(case, {}), **kw}
    return ndc.kc_case(case, _b({f"{case}:{s}": p for s, p in cfg.items()}), y_active)


def test_family_kc_cases_and_gates():
    assert [_kc(c) for c in ("D0", "DONLY", "DDOSE")] == ["PASS"] * 3
    assert _kc("D0", Z050="--") == "CONTRADICTED"  # PARTIAL declared on D0
    assert _kc("D0", Z050="-+") == "UNRESOLVED"
    assert _kc("D0", V3x="-+") == "UNRESOLVED"  # EXCLUDED/MODEL_HEADROOM: undeclared
    assert _kc("DONLY", Vc="++") == "CONTRADICTED"  # COMPLEMENT_LOW_ALIGNED, not NECESSARY
    assert _kc("DONLY", Zc010="-+") == "UNRESOLVED"
    assert _kc("DONLY", Z050="--", Zc010="-+") == "CONTRADICTED"  # contradiction wins
    assert _kc("DDOSE", Z050="++") == "CONTRADICTED"  # USED on the dose case
    assert _kc("DDOSE", Zc050="--") == "CONTRADICTED"  # CODE_DOMINANT, not NOT_NECESSARY
    # ND-C31: the case's Y1 is active iff y_active and L(<case>:V3y) > g
    assert _kc("D0", y_active=True, Y1="-+") == "UNRESOLVED"
    assert _kc("D0", y_active=True, Y1="-+", V3y="--") == "PASS"
    g = ndc.kc_gate({"D0": "PASS", "DONLY": "UNRESOLVED", "DDOSE": "PASS"})
    assert g["status"] == "FAIL" and g["full_status"] == "EXCLUDED/KNOWN_CASE_UNRESOLVED"
    assert g["cases"] == {"D0": "PASS", "DONLY": "FAIL", "DDOSE": "PASS"}
    g = ndc.kc_gate({"D0": "PASS", "DONLY": "UNRESOLVED", "DDOSE": "CONTRADICTED"})
    assert g["status"] == "FAIL" and g["full_status"] == "KNOWN_CASE_CONTRADICTED"
    g = ndc.kc_gate({"D0": "PASS", "DONLY": "PASS", "DDOSE": "PASS"})
    assert g["status"] == "PASS" and g["full_status"] == "PASS"
    g = ndc.kcr_gate({"DNULLR": "CONTRADICTED", "DID": "PASS"})
    assert g["status"] == "FAIL" and g["full_status"] == "MOVE_CASE_CONTRADICTED"


def test_family_kc_contradiction_blocks_not_used_and_kcr_does_not():
    nu = {1729: "DECOY_NOT_USED", 2718: "DECOY_NOT_USED", 3141: "DECOY_NOT_USED"}
    assert ndc.overall("D", nu, [], kc_contradicted=True) == "KNOWN_CASE_CONTRADICTED"
    assert ndc.overall("D", nu, [], kc_contradicted=False) == "DECOY_NOT_USED"
    per = {j: ndc.d_model(_b(dict(D_BASES[0], V3x="++", Y1="--")), True) for j in nu}
    extra = {"variants": {}, "dnullr": {}, "kcr": {2718: ["DNULLR"]}, "kc_test": {}}
    q = ndc.qualifiers("D", per, extra, True, {"precision_limited": []})
    assert "MOVE_CASE_CONTRADICTED(2718, DNULLR)" in q  # a qualifier only
    ex = {1729: "EXCLUDED/KNOWN_CASE_UNRESOLVED", 2718: "EXCLUDED/KNOWN_CASE_UNRESOLVED",
          3141: "DECOY_NOT_USED"}
    assert ndc.overall("D", ex, []) == "INCONCLUSIVE/KNOWN_CASE_UNRESOLVED"


# ---- T-EDGE (§2.3, §2.4, §4.3, MD-9) ------------------------------------------------------
EDGES = {"L=g": (G, 2.0), "U=-g": (-2.0, -G), "inside": (-G / 2, G / 2), "straddle": (-1.0, 1.0),
         "L=U=0": (0.0, 0.0)}
NR_BASES = [dict(Zc010="--", Zc050="--", Wc="++", Vc="--", NEGc="++", Zc090="--", Zc100="--"),
            dict(Zc010="++", Zc050="--", Wc="++", Vc="++", NEGc="++", Zc090="--", Zc100="--"),
            dict(Zc010="++", Zc050="++", Wc="++", Vc="++", NEGc="++", Zc090="++", Zc100="--"),
            dict(Zc010="--", Zc050="--", Wc="--", Vc="++", NEGc="--", Zc090="--", Zc100="--")]
D_BASES = [dict(Z010="--", Z050="--", Vabs="--", Vrand="--", NEG="++"),
           dict(Z010="++", Z050="--", Vabs="++", Vrand="++", NEG="++"),
           dict(Z010="++", Z050="++", Vabs="++", Vrand="++", NEG="++"),
           dict(Z010="--", Z050="--", Vabs="--", Vrand="++", NEG="--")]
NM_BASES = [dict(Ztau="++", ZMc010="--", ZMc050="--", WMc="++", VMc="--", NEGMc="++"),
            dict(Ztau="--", ZMc010="--", ZMc050="--", WMc="++", VMc="--", NEGMc="++"),
            dict(Ztau="++", ZMc010="++", ZMc050="--", WMc="++", VMc="++", NEGMc="++")]


def test_edge_every_threshold_array():
    for sign in (cdc.sign, ndc.sign):  # a bound at the guard is neither sign
        assert sign(G, G) == 0 and sign(-G, G) == 0 and sign(0.0, G) == 0
        assert sign(G * (1 + 1e-12), G) == 1 and sign(-G * (1 + 1e-12), G) == -1
    for base, s, (L, U) in itertools.product(NR_BASES, list(NR_BASES[0]) + ["V3x", "Y1"],
                                             EDGES.values()):
        b = _b({**base, "V3x": "++", "Y1": "--", "Z090": "-+", s: (L, U)})
        assert nr_got(ndc.nr_model(b, True)) == nr_expect(b, True), (base, s, L, U)
    for base, s, (L, U) in itertools.product(D_BASES, list(D_BASES[0]) + ["V3x", "Y1"],
                                             EDGES.values()):
        b = _b({**base, "V3x": "++", "Y1": "--", s: (L, U)})
        assert d_got(ndc.d_model(b, True)) == d_expect(b, True), (base, s, L, U)
    for base, s, (L, U) in itertools.product(NM_BASES, list(NM_BASES[0]) + ["V3x"],
                                             EDGES.values()):
        b = _b({**base, "V3x": "++", s: (L, U)})
        assert nm_got(ndc.nm_model(b)) == nm_expect(b), (base, s, L, U)


def test_edge_named_cases():
    cd = dict(NR_BASES[1], V3x="++", Y1="--")
    assert ndc.nr_model(_b(cd), True)["status"] == "CODE_DOMINANT"
    assert ndc.nr_model(_b(dict(cd, Zc010=EDGES["L=g"])), True)["status"] == "INC/NUMERICAL"
    assert ndc.nr_model(_b(dict(cd, Zc050=EDGES["U=-g"])), True)["status"] == "INC/NUMERICAL"
    assert ndc.nr_model(_b(dict(cd, Zc050=EDGES["straddle"])), True)["status"] == "INC"
    assert ndc.nr_model(_b(dict(cd, Zc010=EDGES["L=U=0"])), True)["status"] == "INC/NUMERICAL"
    nec = dict(NR_BASES[0], V3x="++", Y1="--")
    assert ndc.nr_model(_b(nec), True)["status"] == "NECESSARY"
    r = ndc.nr_model(_b(dict(nec, Wc=EDGES["L=g"])), True)
    assert r["status"] == "COMPLEMENT_LOW_ALIGNED"
    r = ndc.nr_model(_b(dict(nec, V3x=EDGES["L=g"])), True)
    assert r["status"] == "EXCLUDED/MODEL_HEADROOM"
    r = ndc.nr_model(_b(dict(nec, Y1=EDGES["U=-g"])), True)
    assert r["status"] == "EXCLUDED/NUISANCE_IN_S"
    nm = dict(NM_BASES[0], V3x="++")
    assert ndc.nm_model(_b(dict(nm, Ztau=EDGES["L=g"])))["status"] == "INC/NUMERICAL"
    assert ndc.nm_model(_b(dict(nm, Ztau=EDGES["straddle"])))["status"] == "INC"
    dd = dict(D_BASES[0], V3x="++", Y1="--")
    assert ndc.d_model(_b(dict(dd, Vrand=EDGES["U=-g"])), True)["status"] == "DECOY_LOW_ALIGNED"
    assert ndc.d_model(_b(dict(dd, Z050=EDGES["L=U=0"])), True)["status"] == "INC/NUMERICAL"
