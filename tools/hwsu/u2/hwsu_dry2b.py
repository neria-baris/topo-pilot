"""HWSU model-phase dry run DRU, cases that need no training (API_U2.md section 6; split from
hwsu_dry2 by size): KS-P, KS-RULES and DRU3-DRU9. Synthetic worlds and roots only, scope
hwsu-dry-v1, nothing under the project root. DRU1, DRU2 and DRU-REG stay in hwsu_dry2, the only
file that may reference hwsb_train.train, hwsc_data.make_train_dev_c and
hwsc_registry_build.build (R-0223-3)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_bind_u2 as bu2
import hwsu_decide as ud
import hwsu_dry as udry
import hwsu_known as uk
import hwsu_model as um
import hwsu_oracle as uo
import hwsu_records as ur
import u2  # noqa: F401
import itertools
import json
from fractions import Fraction as Fr
from pathlib import Path

import c1_oracle
import numpy as np
import stage_records
from c1_records import C1GateFailure


def _res(ok, **details) -> dict:
    return {"status": "PASS" if ok else "FAIL", "details": details}


# --------------------------------------------------------------------------- KS-P, KS-RULES
def _chain_laws(P=4):
    c = udry.nonreversible_chain()
    T, E, pi = c["T_f"], c["E_f"], c["pi_f"]

    def alpha(w):
        a = pi.copy()
        for s in w:
            a = (a * E[:, s]) @ T
        return a  # unnormalised, already advanced one step

    def joint(w):
        a = pi.copy()
        for t, s in enumerate(w):
            b = a * E[:, s]
            if t == len(w) - 1:
                return float(b.sum())
            a = b @ T

    def pred(w):
        q = alpha(w) @ E
        return q / q.sum()
    return pred, joint, P


def ks_p(base) -> dict:
    """Lemma P2 pair moment = conditional covariance (exact Fractions) and Lemma J (floats)."""
    c, P = udry.nonreversible_chain(), 4
    T, E, pi = c["T"], c["E"], c["pi"]

    def joint(w):
        a = pi.copy()
        for t, s in enumerate(w):
            b = a * E[:, s]
            if t == len(w) - 1:
                return sum(b)
            a = b @ T

    pre_all = list(itertools.product(range(2), repeat=P))
    sufs = list(itertools.product(range(2), repeat=4))
    tot = {(p, s): joint(list(p) + list(s)) for p in pre_all for s in sufs}
    z = sum(tot.values())
    ps = {s: sum(tot[(p, s)] for p in pre_all) / z for s in sufs}
    q = {(p, s): tot[(p, s)] / z / ps[s] for p in pre_all for s in sufs}
    fa = lambda p, s: Fr(sum((i + 1) * x for i, x in enumerate(p + s)))  # noqa: E731
    fb = lambda p, s: Fr(sum((x + 1) ** 2 for x in p) - 3 * sum(s))  # noqa: E731
    lhs = rhs = Fr(0)
    for s in sufs:
        ea = sum(q[(p, s)] * fa(p, s) for p in pre_all)
        eb = sum(q[(p, s)] * fb(p, s) for p in pre_all)
        rhs += ps[s] * (sum(q[(p, s)] * fa(p, s) * fb(p, s) for p in pre_all) - ea * eb)
        lhs += ps[s] * sum(q[(p1, s)] * q[(p2, s)] * (fa(p1, s) - fa(p2, s)) * (
            fb(p1, s) - fb(p2, s)) for p1 in pre_all for p2 in pre_all) / 2
    suffix_only = all(fa((0,) * P, s) - fa((0,) * P, s) == 0 for s in sufs)
    pred, jnt, _ = _chain_laws()
    gj = kl = 0.0
    for s in sufs:
        q4 = pred(list(s))
        for p1 in pre_all:
            q1 = pred(list(p1) + list(s))
            w1 = float(q[(p1, s)] * ps[s])
            kl += w1 * float(np.sum(q1 * np.log(q1 / q4)) + np.sum(q4 * np.log(q4 / q1)))
            for p2 in pre_all:
                q2 = pred(list(p2) + list(s))
                w2 = float(q[(p2, s)] * ps[s] * q[(p1, s)])
                gj += w2 * float(c1_oracle.G_hat(q1[None, :], q2[None, :])[0][0])
    return _res(lhs == rhs and suffix_only and abs(gj - kl) < 1e-10 * max(1.0, abs(kl)),
                p2_exact=lhs == rhs, suffix_only_zero=suffix_only, lemma_j=[gj, kl])


def _bj(l1, u1, l3, u3, la, g=0.01) -> dict:
    return {"ZR010": {"L": l1, "U": u1, "g": g}, "ZR030": {"L": l3, "U": u3, "g": g},
            "AF": {"L": la, "U": la + 1.0, "g": g}}


def ks_rules(base) -> dict:
    g, out = 0.01, {}
    cases = {"RESPONDS_j": _bj(0.5, 0.9, 0.3, 0.8, 0.9),
             "WEAK_RESPONSE_j": _bj(0.5, 0.9, -0.5, -0.2, 0.4),
             "LOW_RESPONSE_j": _bj(-0.9, -0.5, -0.8, -0.2, -0.5),
             "INC_j": _bj(-0.5, 0.5, -0.5, 0.5, -0.5),
             "INC_j/NUMERICAL": _bj(0.5, 0.9, -g, -g, 0.4)}
    out["status"] = {k: ud.model_status(v)["status"] == k for k, v in cases.items()}
    edge = ud.model_status(_bj(g, 0.9, g, 0.9, 0.9))["status"]  # a bound exactly at +g is no sign
    out["edge"] = edge in ("INC_j", "INC_j/NUMERICAL")
    out["rule6"] = [ud.model_status(_bj(0.5, 0.9, -0.5, -0.2, 0.4))["rule6"],
                    not ud.model_status(_bj(0.5, 0.9, 0.3, 0.8, 0.9))["rule6"]]
    kinds = ["RESPONDS_j", "WEAK_RESPONSE_j", "LOW_RESPONSE_j", "INC_j", "EXCLUDED_j/MODEL"]
    good = True
    for combo in itertools.product(kinds, repeat=3):
        r = ud.response_outcome(dict(enumerate(combo)))["outcome"]
        live = [c for c in combo if not c.startswith("EXCLUDED")]
        res = [c for c in live if c.split("_j")[0] in ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE")]
        if len(live) < 2:
            want = "INCONCLUSIVE/MODEL"
        else:
            want = next((b for b in ("RESPONDS", "WEAK_RESPONSE", "LOW_RESPONSE")
                         if sum(c.startswith(b) for c in live) >= 2), None)
            want = want or ("MIXED" if len(res) >= 2 else "INCONCLUSIVE/PRECISION")
        good = good and r == want
    out["combos"] = good
    out["fw"] = all(ud.fw_events(r) <= 2 for r in ("<=0", "0<<=0.1", "0.1<<0.3", "=0.3", ">0.3"))
    return _res(all(v if isinstance(v, bool) else all(v.values() if isinstance(v, dict) else v)
                    for v in out.values()), **out)



def _ko_world(n=256):
    w, pr = udry.tiny_pairs(n)
    T, E, pi, co = w["T"], w["E_canon_shared"], w["pi"], w["coords"]
    o1, o2 = (uo.arm_oracle(T, E, pi, pr[a], co) for a in ("a1", "a2"))
    s1, s2 = uo.suffix_oracle(T, E, pi, [pr["a1"], pr["a2"]], co)
    return o1, o2, s1, s2, uo.pair_core(o1, o2)


def dru3(base, ctx=None) -> dict:
    o1, o2, s1, s2, pc = _ko_world()
    N, G, seeds = uo.helmert(36), pc["G"], uc.CONTRACT["seeds"]["dry_u2"]

    def A_of(lam):
        def lg(o, s):
            return s["logq4"] + lam * (o["logq"] - s["logq4"])
        return uo.readout_A(pc["d"], lg(o1, s1), lg(o2, s2), N)

    A = {"oracle": A_of(1.0), "suffix": A_of(0.0), "dose": A_of(0.2)}
    b = ud.family_bounds(A, G, list(A), seeds["family_U"], draws=20000)
    st = {j: ud.model_status({s: b[f"{j}:{s}"] for s in ("ZR010", "ZR030", "AF")}) for j in A}
    ok = (st["oracle"]["status"] == "RESPONDS_j" and st["suffix"]["status"] == "LOW_RESPONSE_j"
          and np.all(A["suffix"] == 0) and st["dose"]["status"] == "WEAK_RESPONSE_j"
          and st["dose"]["rule6"])
    return _res(ok, status={j: v["status"] for j, v in st.items()}, rule6=st["dose"]["rule6"])


def dru4(base, ctx=None) -> dict:
    r = ks_rules(base)
    share = ud.share_outcome({"of_accept_sha256": "0" * 64})
    pm = {1: "RESPONDS_j", 2: "RESPONDS_j", 3: "EXCLUDED_j/M0"}
    prec = ud.response_outcome({1: "RESPONDS_j", 2: "INC_j", 3: "INC_j/NUMERICAL"})
    dis = ud.response_outcome({1: "RESPONDS_j", 2: "RESPONDS_j", 3: "LOW_RESPONSE_j"})
    ok = (r["status"] == "PASS" and ud.response_outcome(pm)["outcome"] == "RESPONDS"
          and prec["outcome"] == "INCONCLUSIVE/PRECISION" and dis["dissent"] == [
              "DISSENT(3: LOW_RESPONSE_j)"] and share["outcome"] == uk.SHARE_OUTCOME)
    return _res(ok, rules=r["status"], share=share["outcome"])


def dru5(base, ctx=None) -> dict:
    rng = np.random.default_rng(649914)
    G = np.ones(4096) + 0.1 * rng.standard_normal(4096)
    seeds = {"p1_sd": 649914, "p1_centred": 649915}
    mk = lambda sd, sh=0.0: {j: 0.5 * G + sd * rng.standard_normal(4096) + sh  # noqa: E731
                             for j in (1, 2, 3)}
    good = ud.p1_u(mk(0.05), G, [1, 2, 3], seeds, ladder=(4096, 8192))
    shifted = ud.p1_u({j: a + 0.3 for j, a in mk(0.05).items()}, G, [1, 2, 3], seeds,
                      ladder=(4096, 8192))
    bad = ud.p1_u(mk(30.0), G, [1, 2, 3], seeds, ladder=(4096,))
    return _res(good["N_RESP"] == 4096 and bad["N_RESP"] is None and shifted["N"] == good["N"],
                good=good["N_RESP"], bad=bad["N_RESP"])


def dru6(base, ctx=None) -> dict:
    base, ok = Path(base), {}
    store = base / "store"
    store.mkdir(parents=True, exist_ok=True)
    try:
        ud.check_unsealed_u({"p1": {"ZR010": 1}})
        ok["refused"] = False
    except C1GateFailure:
        ok["refused"] = True
    arrays = {"G": np.ones(8), "A_1": np.ones(8), "ZR010_1": np.ones(8), "ZR030_1": np.ones(8)}
    sha = ud.write_sealed_u(store, arrays)
    try:
        ud.write_sealed_u(store, arrays)
        ok["once"] = False
    except FileExistsError:
        ok["once"] = True
    ok["sha"] = stage_records.sha256(store / "SEALED_VALIDATION.json") == sha
    return _res(all(ok.values()), **ok)


def dru7(base, ctx=None) -> dict:
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    plants = {"p_load.py": "import c2_model\nc2_model.load_models()\n",
              "p_proc.py": "import c2_oracle\nc2_oracle.load_process()\n",
              "p_p1.py": "import c2_stats\nc2_stats.p1()\n",
              "p_m0.py": "import c2_model\nc2_model.m0()\n",
              "p_seal.py": "import k4b_stats\nk4b_stats.write_sealed()\n",
              "p_cfg.py": "import c2_config\nx = c2_config.SOME_UNLISTED\n"}
    caught = {}
    for n, text in plants.items():
        f = base / n
        f.write_text(text, encoding="utf-8")
        caught[n] = bu2.audit_u2(files=[f])["status"] != "PASS"
    return _res(all(caught.values()), caught=caught)


def dru8(base, ctx=None) -> dict:
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    p = base / "TRAIN_RECORD.json"
    p.write_text(json.dumps({"checkpoint_ids": {"5000": "x"}, "checksums": {}, "run_key": [],
                             "status": "COMPLETE", "dev_ce": {"1": 0.5}}), encoding="utf-8")
    rec = um.read_train_record(p, root=base)
    r = {"dev_ce_dropped": "dev_ce" not in rec, "keys": sorted(rec)}
    try:
        uk.of_binding(base)
        r["of_refused"] = False
    except C1GateFailure as exc:
        r["of_refused"] = exc.status == "INCONCLUSIVE/AUTHORITY"
    return _res(r["dev_ce_dropped"] and r["of_refused"], **r)


def dru9(base, ctx=None) -> dict:
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    led = base / "ledger.json"
    led.unlink(missing_ok=True)
    ur.ledger_append(led, "E1-j-a1", "j", "E1", 1.0, "dry")
    try:
        ur.ledger_append(led, "E1-j-a1", "j", "E1", 1.0, "dry")
        dup = False
    except C1GateFailure:
        dup = True
    caps = uc.CONTRACT["resources"]["u2_memory_cap_bytes"]
    src = (uc.HERE / "u2" / "hwsu_driver.py").read_text(encoding="utf-8")
    pause = "pause_or_raise_u(" in src
    return _res(dup and caps["E1"] == 12 * 2**30 and not pause, dup=dup, caps=caps, pause=pause)
