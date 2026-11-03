"""HWSU OF dry run DRO1-DRO4 and run_dro (API.md §10; protocol §9). Synthetic worlds and roots only;
scope hwsu-dry-v1 and the dry seeds. DRO5-DRO9 and the J11 reader fixture live in hwsu_dry_b
(split by size, API erratum) and are reachable here as hwsu_dry.<name>."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_driver_of as udr
import hwsu_freeze as ufz
import hwsu_of as uof
import hwsu_oracle as uo
import hwsu_pairs as up
import hwsu_records as ur
import copy
import itertools
import json
from fractions import Fraction as Fr
from pathlib import Path

import c2_decide
import hwsb_dry
import hwsc_data
import numpy as np
import stage_records
from c1_records import C1GateFailure
from topo_pilot.contracts import ArtifactStore, MemoryBackend

SEEDS = uc.DRY_SEEDS_OF


def tiny_world() -> dict:
    p = hwsb_dry.build_tiny_process(ArtifactStore(MemoryBackend()), masters=(649906,))
    xy = np.asarray(p["coords"], dtype=np.float64)
    a, b = np.divmod(np.arange(36), 6)
    logit = (2.0 * np.cos(2 * np.pi * (xy[:, :1] - a[None, :]) / 6.0)
             - (xy[:, 1:2] - b[None, :] / 5.0) ** 2)
    E = np.exp(logit)
    return {"T": np.asarray(p["T"], dtype=np.float64),
            "E_canon_shared": E / E.sum(1, keepdims=True),
            "pi": np.asarray(p["pi"], dtype=np.float64), "coords": xy, "N": 12, "V": 36}


def nonreversible_chain() -> dict:
    T = [[Fr(0), Fr(3, 4), Fr(1, 4)], [Fr(1, 4), Fr(0), Fr(3, 4)], [Fr(3, 4), Fr(1, 4), Fr(0)]]
    E = [[Fr(3, 4), Fr(1, 4)], [Fr(1, 2), Fr(1, 2)], [Fr(1, 5), Fr(4, 5)]]
    pi = [Fr(1, 3)] * 3
    return {"T": np.array(T, dtype=object), "E": np.array(E, dtype=object),
            "pi": np.array(pi, dtype=object), "T_f": np.array(T, dtype=float),
            "E_f": np.array(E, dtype=float), "pi_f": np.array(pi, dtype=float), "L": 8}


def _w(path, text) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
    return path


def _h(path) -> str:
    return ur._sha(Path(path).read_bytes())


def synthetic_root(base) -> dict:
    root = Path(base) / "root"
    mb, hc = root / "agent-handoff", root / "hwsc-store"
    C = copy.deepcopy(uc.CONTRACT)
    A = C["authority"]
    for d in ("hwsu-store", "tools/hwsu", "tools/hwsd", "docs/code_index/files/tools/hwsu",
              "topo-pilot/src"):
        (root / d).mkdir(parents=True, exist_ok=True)
    for a in A["addenda"]:
        a["sha256"] = _h(_w(mb / a["path"], f"fixture addendum {a['addendum']}\n"))
    d = A["design"]
    d["sha256"] = _h(_w(mb / d["path"], uc.PROTOCOL_PATH.read_bytes()))
    d["freeze_record"]["sha256"] = _h(_w(mb / d["freeze_record"]["path"],
                                         json.dumps({"fixture": True})))
    res = _w(hc / "RESERVATION_W2.json", json.dumps({"id": "RES-HWSC-W2", "state": "ACTIVE"}))
    lock, op = _w(hc / "RUN.lock", "fixture"), _w(hc / "OPERATION_ACTIVE.json", "{}")
    _w(hc / "artifacts" / "WorldSpec" / "fixture" / "meta.json",
       json.dumps({"artifact_type": "WorldSpec"}))
    w2 = {"reservation_file": "hwsc-store/RESERVATION_W2.json",
          "reservation_file_sha256": _h(res), "run_lock_file": "hwsc-store/RUN.lock",
          "run_lock_sha256": _h(lock), "operation_active_file": "hwsc-store/OPERATION_ACTIVE.json",
          "operation_active_sha256": _h(op), "fixture": True}
    tracks = {"U": C["namespace"]["U"], "D": C["namespace"]["D_declared"]}
    files = {"HWS_UD_NAMESPACE": json.dumps({"tracks": tracks}), "HWSC_W2_END": json.dumps(w2)}
    for k, r in A["records"].items():
        r["sha256"] = _h(_w(mb / r["path"], files.get(k, f"fixture {k}\n")))
    return {"root": root, "mailbox": mb, "hwsc_store": hc, "hwsu_store": root / "hwsu-store",
            "contract": C}


def tiny_pairs(n, block=0):
    w = tiny_world()
    return w, up.sample_pairs(w["T"], w["E_canon_shared"], w["pi"], uc.SCOPE_DRY, "of-eval",
                              block, n)


def dro1(base) -> dict:
    store = Path(base)
    sr = synthetic_root(Path(str(store) + "-root"))
    w = tiny_world()
    store.mkdir(parents=True, exist_ok=True)
    ur.write_reservation(store, "RES-HWSU-OF", uc.SCOPE_DRY, ur.utc(), "hwsu_dry.dro1")
    stage_records.write_new(store / "FREEZE_OF.json", {"fixture": True})
    ap = _w(sr["mailbox"] / "approvals" / "OWNER_OK.md", "fixture approval\n")
    stage_records.write_new(store / "AUTH_OF_DRO.json", {
        "owner_approval": {"path": "approvals/OWNER_OK.md", "sha256": _h(ap)},
        "freeze_of_sha256": stage_records.sha256(store / "FREEZE_OF.json")})
    p = float(hwsc_data.p_d2a_check(w, 1.0)["p_D2a"])
    ho = _w(sr["root"] / "handoff.json", json.dumps({"p_D2a": p, "stage_c_exclusions": []}))
    ctx = udr.build_ctx(store, "DRO", 1, "RES-HWSU-OF", root=sr["root"], mailbox=sr["mailbox"],
                        hwsc_store=sr["hwsc_store"], scope=uc.SCOPE_DRY, seeds=SEEDS, dry=True)
    ctx.update(proc=w, block_n=512, draws=200, decimal_rows=2, contract=sr["contract"],
               dry_skip_of_b=True, handoff_path=ho, handoff_sha256=_h(ho))
    res = udr.run_of(store, "DRO", ctx=ctx, dry_continue=True)
    got = {r["gate"]: r["status"] for r in res["records"]}
    loader, work = {}, Path(str(store) + "-loader")
    sha_of = _h(uc.CONTRACT_OF_PATH)
    for name, doc in (("wrong_sha", {"contract_of_sha256": "0" * 64}),
                      ("override", {"contract_of_sha256": sha_of, "seeds": {"of": {
                          "headroom": 1}}}),
                      ("added_key", {"contract_of_sha256": sha_of, "contract_phase2": {"x": 1}})):
        f = _w(work / f"{name}.json", json.dumps(doc))
        try:
            uc.load_contract(uc.CONTRACT_OF_PATH, f)
            loader[name] = "accepted"
        except C1GateFailure as exc:
            loader[name] = exc.status
    okl = (loader["wrong_sha"] == loader["override"] == "FAIL_TECHNICAL/BINDING"
           and loader["added_key"] == "accepted")
    need = {"OF-0", "OF-P", "RESERVATION", "OF-S", "OF-H", "OF-1", "OF-2", "OF-3", "OF-4", "OF-5"}
    ok = need <= set(got) and "NOT_RUN" not in got.values() and okl
    return {"status": "PASS" if ok else "FAIL", "details": {"gates": got, "loader": loader}}


def _law(P, kern):
    """Exact law of the prefix given the suffix from a kernel dict (API.md §2.1)."""
    out = {}
    for pre in itertools.product(range(2), repeat=P):
        tot = Fr(0)
        for zs in itertools.product(range(3), repeat=P):
            v = kern["bridge"][zs[-1]]
            for t in range(P):
                v = v * kern["E"][zs[t], pre[t]]
                if t:
                    v = v * kern["T_rev"][zs[t], zs[t - 1]]
            tot += v
        out[pre] = tot
    return out


def dro2(base) -> dict:
    c, suf, P = nonreversible_chain(), (0, 1, 1, 0), 4
    T, E, pi = c["T"], c["E"], c["pi"]

    def joint(w):
        a = pi.copy()
        for t, s in enumerate(w):
            b = a * E[:, s]
            if t == len(w) - 1:
                return sum(b)
            a = b @ T

    tot = {pre: joint(list(pre) + list(suf)) for pre in itertools.product(range(2), repeat=P)}
    z = sum(tot.values())
    exact = {k: v / z for k, v in tot.items()}
    k = up.prefix_kernels(T, E, pi, suf, P)
    real = _law(P, k) == exact
    wrong_t = _law(P, dict(k, T_rev=T)) != exact
    no_beta = _law(P, dict(k, bridge=np.array([Fr(1, 3)] * 3, dtype=object))) != exact
    n = 100000
    arm1 = np.tile(np.array([0] * P + list(suf), dtype=np.uint8), (n, 1))
    a2 = up.sample_prefix(c["T_f"], c["E_f"], c["pi_f"], arm1, np.random.default_rng(649901))
    cnt = {}
    for row in a2[:, :P]:
        key = tuple(int(x) for x in row)
        cnt[key] = cnt.get(key, 0) + 1
    dev = max(abs(cnt.get(q, 0) / n - float(exact[q])) for q in exact)
    ok = real and wrong_t and no_beta and dev < 0.005 and not np.array_equal(
        up.time_reversal(T, pi), T)
    return {"status": "PASS" if ok else "FAIL", "details": {
        "real_exact": real, "planted_T_caught": wrong_t, "planted_beta_caught": no_beta,
        "max_freq_dev": dev}}


def dro3(base) -> dict:
    w, pr = tiny_pairs(256)
    T, E, pi, co = w["T"], w["E_canon_shared"], w["pi"], w["coords"]
    a1, a2 = pr["a1"], pr["a2"]
    o1, o2 = uo.arm_oracle(T, E, pi, a1, co), uo.arm_oracle(T, E, pi, a2, co)
    s1, s2 = uo.suffix_oracle(T, E, pi, [a1, a2], co)
    pc, N = uo.pair_core(o1, o2), uo.helmert(36)

    def ko(lam):
        out = {}
        for k in uo.CASES:
            def lg(o, s, k=k):
                if k == "KO3":
                    return s["logq4"] + lam * (o["logq"] - s["logq4"])
                return uo.ko_logits(o, s, k)

            out[k] = uo.readout_A(pc["d"], lg(o1, s1), lg(o2, s2), N)
        return uo.ko_identities(pc["G"], out)

    good, bad_lam = ko(0.2), ko(0.25)
    w1, w2 = uo.suffix_oracle(T, E, pi, [a1[:, 27:31], a2[:, 27:31]], co)
    window = not np.array_equal(w1["q4bar"], w2["q4bar"])
    unplanted = np.array_equal(s1["q4bar"], s2["q4bar"]) and all(v["ok"] for v in good.values())
    ok = unplanted and window and not bad_lam["KO3"]["ok"]
    return {"status": "PASS" if ok else "FAIL", "details": {
        "unplanted_ok": unplanted, "window_caught": window,
        "lambda_caught": not bad_lam["KO3"]["ok"]}}


def dro4(base) -> dict:
    rng = np.random.default_rng(SEEDS["share"])
    G = 1.0 + 0.1 * rng.standard_normal(2048)
    out = {}
    for name, frac in (("pass", 0.5), ("fail", 0.1)):
        Z = frac * G + 0.01 * rng.standard_normal(2048) - 0.2 * G
        b, _ = uof._bounds({"Z020": Z}, SEEDS["share"], uc.ALPHA_VAL, 300)
        out[name] = "PASS" if c2_decide.sign(b["Z020"]["L"], c2_decide.guard(Z)) == 1 \
            else "SHARE_DROPPED"

    def prec(sd_resp, sd_share):
        z = rng.standard_normal(2048)
        ctx = {"pc": {"G": np.ones(2048)}, "seeds": SEEDS, "draws": 100, "results": {},
               "sa": {"A_full": 0.3 + sd_resp * z, "A_S": 0.1 + sd_share * z}}
        return uof.of_4(ctx).get("status", "PASS")

    out["of4_pass"], out["of4_share_fail"] = prec(0.2, 0.1), prec(0.2, 20.0)
    out["of4_resp_fail"] = prec(50.0, 0.1)
    want = {"pass": "PASS", "fail": "SHARE_DROPPED", "of4_pass": "PASS",
            "of4_share_fail": "SHARE_DROPPED", "of4_resp_fail": "INCONCLUSIVE/ORACLE_FEASIBILITY"}
    return {"status": "PASS" if out == want else "FAIL", "details": out}


CASES = ("dro1", "dro2", "dro3", "dro4", "dro5", "dro6", "dro7", "dro8", "dro9")


def __getattr__(name):
    import importlib

    b = importlib.import_module("hwsu_dry_b")
    if hasattr(b, name):
        return getattr(b, name)
    raise AttributeError(f"module 'hwsu_dry' has no attribute {name!r}")


def run_dro(out=uc.DRY_STORE, only=None) -> dict:
    import hwsu_dry as me

    out = Path(out)
    try:
        out.resolve().relative_to(uc.ROOT.resolve())
        return {"status": "REFUSED", "reason": "dry store under the project root"}
    except ValueError:
        pass
    work, cases = Path(str(out) + "-cases"), {}
    inv0 = ur.root_inventory(uc.ROOT)
    for name in (only or [c.upper() for c in CASES]):
        base = out if name.upper() == "DRO1" else work / name.upper()
        base.mkdir(parents=True, exist_ok=True)
        try:
            cases[name.upper()] = getattr(me, name.lower())(base)
        except Exception as exc:  # noqa: BLE001  a crashing case is a FAIL
            cases[name.upper()] = {"status": "FAIL", "details": {"exception": repr(exc)[:500]}}
    inv1 = ur.root_inventory(uc.ROOT)
    h = ufz._git(uc.REPO, "rev-parse", "HEAD").decode().strip()
    files = ufz.implementation_files(uc.REPO, h)
    clean = not ufz._git(uc.REPO, "status", "--porcelain", "--", "tools/hwsu").strip()
    rep = {"cases": cases, "all_pass": all(c["status"] == "PASS" for c in cases.values())
           and inv0 == inv1, "implementation_files": files,
           "implementation_sha256": ufz._canon_sha(files), "h_exec": h, "tree_clean": clean,
           "inventory_before": inv0, "inventory_after": inv1}
    (out / "stages" / "DRY").mkdir(parents=True, exist_ok=True)
    stage_records.write_new(out / "stages" / "DRY" / "DRY_OF_REPORT.json",
                            json.loads(json.dumps(rep, default=str)))
    ur.write_obligation(out, "REGISTRY_OBLIGATION.json", "DRO", "hwsu_dry.run_dro", dry=True)
    return rep
